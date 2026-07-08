from __future__ import annotations

from urllib.parse import parse_qs, urlparse

import httpx
import pytest
import respx

from pennylane_sdk._exceptions import APIStatusError
from pennylane_sdk.oauth import DEFAULT_TOKEN_URL, AsyncOAuthApp, OAuthApp

TOKENS = {
    "access_token": "at_1",
    "refresh_token": "rt_1",
    "token_type": "Bearer",
    "expires_in": 86400,
    "scope": "customer_invoices:all",
    "created_at": 1750000000,
}


def _app() -> OAuthApp:
    return OAuthApp("cid", "csecret", "https://example.com/callback")


class TestAuthorizationUrl:
    def test_builds_url_with_scopes_list(self) -> None:
        url = _app().authorization_url(
            scopes=["customer_invoices:all", "products:readonly"], state="xyz"
        )
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        assert parsed.netloc == "app.pennylane.com"
        assert parsed.path == "/oauth/authorize"
        assert query["client_id"] == ["cid"]
        assert query["redirect_uri"] == ["https://example.com/callback"]
        assert query["response_type"] == ["code"]
        assert query["scope"] == ["customer_invoices:all products:readonly"]
        assert query["state"] == ["xyz"]

    def test_accepts_scope_string(self) -> None:
        url = _app().authorization_url(scopes="ledger_entries:all")
        assert "scope=ledger_entries%3Aall" in url


class TestExchangeAndRefresh:
    @respx.mock
    def test_exchange_code(self) -> None:
        route = respx.post(DEFAULT_TOKEN_URL).mock(
            return_value=httpx.Response(200, json=TOKENS)
        )
        with _app() as app:
            tokens = app.exchange_code("auth-code")
        body = parse_qs(route.calls.last.request.content.decode())
        assert body["grant_type"] == ["authorization_code"]
        assert body["code"] == ["auth-code"]
        assert body["client_secret"] == ["csecret"]
        assert tokens.access_token == "at_1"
        assert tokens.expires_in == 86400

    @respx.mock
    def test_refresh_sends_refresh_grant(self) -> None:
        route = respx.post(DEFAULT_TOKEN_URL).mock(
            return_value=httpx.Response(200, json={**TOKENS, "access_token": "at_2"})
        )
        with _app() as app:
            tokens = app.refresh("rt_1")
        body = parse_qs(route.calls.last.request.content.decode())
        assert body["grant_type"] == ["refresh_token"]
        assert body["refresh_token"] == ["rt_1"]
        assert tokens.access_token == "at_2"

    @respx.mock
    def test_error_response_raises_status_error(self) -> None:
        respx.post(DEFAULT_TOKEN_URL).mock(
            return_value=httpx.Response(
                401, json={"error": "invalid_grant", "status": 401}
            )
        )
        with _app() as app, pytest.raises(APIStatusError) as exc_info:
            app.refresh("expired-rt")
        assert exc_info.value.error_code == "invalid_grant"


class TestAsyncOAuthApp:
    @respx.mock
    async def test_exchange_and_refresh(self) -> None:
        respx.post(DEFAULT_TOKEN_URL).mock(return_value=httpx.Response(200, json=TOKENS))
        async with AsyncOAuthApp("cid", "csecret", "https://example.com/cb") as app:
            tokens = await app.exchange_code("code")
            assert tokens.access_token == "at_1"
            refreshed = await app.refresh("rt_1")
            assert refreshed.refresh_token == "rt_1"
