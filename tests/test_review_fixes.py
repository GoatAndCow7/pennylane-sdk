"""Regression tests for issues found during the hardening review."""

from __future__ import annotations

import httpx
import pytest
import respx

from pennylane_sdk import (
    APIConnectionError,
    APIStatusError,
    InvalidResponseError,
    Pennylane,
)
from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk._models import PennylaneModel
from pennylane_sdk._throttle import RateThrottle
from pennylane_sdk.oauth import DEFAULT_TOKEN_URL, OAuthApp, OAuthTokens
from pennylane_sdk.webhooks import verify_signature

from .conftest import BASE_URL, REAL_RETRY_DELAY


class Thing(PennylaneModel):
    id: int


class TestRedirectHandling:
    """3xx responses must raise a clear SDK error, never a silent None."""

    @respx.mock
    def test_redirect_raises_status_error(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/me").mock(
            return_value=httpx.Response(
                301, headers={"location": "https://app.pennylane.com/elsewhere"}
            )
        )
        with pytest.raises(APIStatusError, match=r"redirect.*base_url"):
            sync_client.request("GET", "/me", cast_to=Thing)

    @respx.mock
    async def test_redirect_raises_in_async_too(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/things").mock(return_value=httpx.Response(302))
        with pytest.raises(APIStatusError, match="redirect"):
            await async_client.request("POST", "/things", cast_to=Thing, body={})


class TestNonJsonSuccessBody:
    """A 200 with an HTML body (proxy, captive portal) must raise a typed error."""

    @respx.mock
    def test_html_body_raises_invalid_response_error(
        self, sync_client: SyncAPIClient
    ) -> None:
        respx.get(f"{BASE_URL}/me").mock(
            return_value=httpx.Response(
                200, text="<html>maintenance</html>", headers={"content-type": "text/html"}
            )
        )
        with pytest.raises(InvalidResponseError, match="text/html"):
            sync_client.request("GET", "/me", cast_to=Thing)


class TestRetryAfterBounds:
    def _client(self) -> SyncAPIClient:
        return SyncAPIClient(api_token="t", base_url=BASE_URL)

    def _response_429(self, retry_after: str) -> httpx.Response:
        return httpx.Response(
            429,
            headers={"retry-after": retry_after},
            request=httpx.Request("GET", f"{BASE_URL}/me"),
        )

    def test_huge_retry_after_is_clamped(self) -> None:
        delay = REAL_RETRY_DELAY(self._client(), 0, self._response_429("86400"))
        assert delay <= 60.0

    def test_infinite_retry_after_falls_back_to_backoff(self) -> None:
        delay = REAL_RETRY_DELAY(self._client(), 0, self._response_429("inf"))
        assert delay < 10.0

    def test_nan_retry_after_falls_back_to_backoff(self) -> None:
        delay = REAL_RETRY_DELAY(self._client(), 0, self._response_429("nan"))
        assert delay < 10.0

    def test_normal_retry_after_is_honored(self) -> None:
        assert REAL_RETRY_DELAY(self._client(), 0, self._response_429("3")) == 3.0


class TestPoolTimeoutRetry:
    @respx.mock
    def test_pool_timeout_is_retried_for_post(self, sync_client: SyncAPIClient) -> None:
        """PoolTimeout means the request never left the pool: safe to retry POST."""
        route = respx.post(f"{BASE_URL}/things")
        route.side_effect = [httpx.PoolTimeout("busy"), httpx.Response(201, json={"id": 1})]
        assert sync_client.request("POST", "/things", cast_to=Thing, body={}).id == 1


class TestThrottleClientWiring:
    """The throttle must gate every HTTP attempt made through the client."""

    @respx.mock
    def test_acquire_called_once_per_attempt_including_retries(self) -> None:
        throttle = RateThrottle(100, 1.0)
        acquires: list[float] = []
        original = throttle.acquire

        def counting_acquire() -> None:
            acquires.append(1.0)
            original()

        throttle.acquire = counting_acquire  # type: ignore[method-assign]
        client = SyncAPIClient(api_token="t", base_url=BASE_URL, throttle=throttle)

        route = respx.get(f"{BASE_URL}/me")
        route.side_effect = [
            httpx.Response(429, json={"error": "rate limited"}),
            httpx.Response(200, json={"id": 1}),
        ]
        client.request("GET", "/me", cast_to=Thing)
        assert len(acquires) == 2  # initial attempt + retry both throttled


class TestClientClose:
    def test_context_manager_closes_owned_pool(self) -> None:
        with Pennylane(api_token="t") as client:
            http = client._client._http
        assert http.is_closed

    def test_injected_http_client_is_not_closed(self) -> None:
        external = httpx.Client()
        try:
            with Pennylane(api_token="t", http_client=external):
                pass
            assert not external.is_closed
        finally:
            external.close()


class TestHttpsEnforcement:
    def test_http_base_url_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="https"):
            Pennylane(api_token="t", base_url="http://evil.example.com/api")

    def test_http_localhost_is_allowed_for_dev(self) -> None:
        with Pennylane(api_token="t", base_url="http://localhost:8080/api") as client:
            assert client._client.base_url.startswith("http://localhost")

    def test_oauth_http_token_url_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="https"):
            OAuthApp("cid", "secret", "https://cb", token_url="http://evil.example.com/token")


class TestOAuthHardening:
    def test_tokens_repr_does_not_leak_secrets(self) -> None:
        tokens = OAuthTokens(access_token="SECRET_AT", refresh_token="SECRET_RT")
        rendered = f"{tokens!r} {tokens}"
        assert "SECRET_AT" not in rendered
        assert "SECRET_RT" not in rendered
        # Explicit access still works (needed to use and persist the tokens).
        assert tokens.access_token == "SECRET_AT"
        assert tokens.model_dump()["refresh_token"] == "SECRET_RT"

    @respx.mock
    def test_connection_error_is_wrapped(self) -> None:
        respx.post(DEFAULT_TOKEN_URL).side_effect = httpx.ConnectError("down")
        with OAuthApp("cid", "secret", "https://cb") as app, pytest.raises(APIConnectionError):
            app.exchange_code("code")

    @respx.mock
    def test_non_json_token_response_is_wrapped(self) -> None:
        respx.post(DEFAULT_TOKEN_URL).mock(
            return_value=httpx.Response(200, text="<html>proxy</html>")
        )
        with OAuthApp("cid", "secret", "https://cb") as app, pytest.raises(InvalidResponseError):
            app.refresh("rt")


class TestWebhookHardening:
    def test_uppercase_hex_signature_is_accepted(self) -> None:
        import hashlib
        import hmac as hmac_mod

        payload = b'{"event":"x"}'
        secret = "s3cret"
        upper = hmac_mod.new(secret.encode(), payload, hashlib.sha256).hexdigest().upper()
        assert verify_signature(payload, upper, secret) is True

    def test_non_utf8_payload_raises_pennylane_error(self) -> None:
        from pennylane_sdk import PennylaneError
        from pennylane_sdk.webhooks import parse_event

        with pytest.raises(PennylaneError, match="not valid JSON"):
            parse_event(b"\xff\xfe\x00invalid")
