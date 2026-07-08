from __future__ import annotations

import httpx
import pytest
import respx

from pennylane_sdk import filters
from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk._exceptions import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from pennylane_sdk._models import PennylaneModel

from .conftest import BASE_URL


class Thing(PennylaneModel):
    id: int
    name: str | None = None


class TestRequestBasics:
    @respx.mock
    def test_sends_auth_and_user_agent_headers(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/me").mock(return_value=httpx.Response(200, json={"id": 1}))
        sync_client.request("GET", "/me", cast_to=Thing)
        sent = route.calls.last.request
        assert sent.headers["authorization"] == "Bearer test-token"
        assert sent.headers["user-agent"].startswith("pennylane-sdk-python/")
        assert sent.headers["accept"] == "application/json"

    @respx.mock
    def test_casts_response_to_model(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/things/1").mock(
            return_value=httpx.Response(200, json={"id": 1, "name": "a", "extra": True})
        )
        thing = sync_client.request("GET", "/things/1", cast_to=Thing)
        assert thing.id == 1
        assert thing.name == "a"

    @respx.mock
    def test_204_returns_none(self, sync_client: SyncAPIClient) -> None:
        respx.delete(f"{BASE_URL}/things/1").mock(return_value=httpx.Response(204))
        assert sync_client.request("DELETE", "/things/1") is None

    @respx.mock
    def test_drops_none_params_and_encodes_filters(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/things").mock(
            return_value=httpx.Response(200, json={"id": 1})
        )
        sync_client.request(
            "GET",
            "/things",
            cast_to=Thing,
            params={
                "limit": 50,
                "cursor": None,
                "filter": [filters.eq("status", "draft")],
            },
        )
        import json

        sent = route.calls.last.request
        assert "cursor" not in str(sent.url)
        assert sent.url.params["limit"] == "50"
        assert json.loads(sent.url.params["filter"]) == [
            {"field": "status", "operator": "eq", "value": "draft"}
        ]

    @respx.mock
    def test_serializes_decimals_in_body(self, sync_client: SyncAPIClient) -> None:
        import json
        from decimal import Decimal

        route = respx.post(f"{BASE_URL}/things").mock(
            return_value=httpx.Response(201, json={"id": 1})
        )
        sync_client.request(
            "POST", "/things", cast_to=Thing, body={"amount": Decimal("12.30")}
        )
        assert json.loads(route.calls.last.request.content) == {"amount": "12.30"}

    @respx.mock
    def test_tracks_rate_limit_headers(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/me").mock(
            return_value=httpx.Response(
                200,
                json={"id": 1},
                headers={
                    "ratelimit-limit": "25",
                    "ratelimit-remaining": "24",
                    "ratelimit-reset": "1750000000",
                },
            )
        )
        sync_client.request("GET", "/me", cast_to=Thing)
        info = sync_client.last_rate_limit
        assert info is not None
        assert info.limit == 25
        assert info.remaining == 24
        assert info.reset == 1750000000


class TestErrors:
    @respx.mock
    def test_401_raises_authentication_error(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/me").mock(
            return_value=httpx.Response(401, json={"error": "Unauthorized", "status": 401})
        )
        with pytest.raises(AuthenticationError):
            sync_client.request("GET", "/me", cast_to=Thing)

    @respx.mock
    def test_422_raises_validation_error_with_details(self, sync_client: SyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/things").mock(
            return_value=httpx.Response(
                422,
                json={
                    "error": "unprocessable_entity",
                    "message": "Entry lines are not balanced",
                    "details": {"debit_total": "100.00"},
                },
            )
        )
        with pytest.raises(ValidationError) as exc_info:
            sync_client.request("POST", "/things", cast_to=Thing, body={})
        assert exc_info.value.details == {"debit_total": "100.00"}


class TestRetries:
    @respx.mock
    def test_429_is_retried_then_succeeds(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/me")
        route.side_effect = [
            httpx.Response(429, json={"error": "rate limited"}, headers={"retry-after": "1"}),
            httpx.Response(200, json={"id": 1}),
        ]
        thing = sync_client.request("GET", "/me", cast_to=Thing)
        assert thing.id == 1
        assert route.call_count == 2

    @respx.mock
    def test_429_exhausts_retries(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/me").mock(
            return_value=httpx.Response(429, json={"error": "rate limited"})
        )
        with pytest.raises(RateLimitError):
            sync_client.request("GET", "/me", cast_to=Thing)

    @respx.mock
    def test_500_get_is_retried(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/me")
        route.side_effect = [
            httpx.Response(500, json={"error": "boom"}),
            httpx.Response(200, json={"id": 1}),
        ]
        assert sync_client.request("GET", "/me", cast_to=Thing).id == 1
        assert route.call_count == 2

    @respx.mock
    def test_500_post_is_not_retried(self, sync_client: SyncAPIClient) -> None:
        """POST must NOT be retried on 5xx: no server-side idempotency
        a retry could create a duplicate invoice."""
        route = respx.post(f"{BASE_URL}/things")
        route.mock(return_value=httpx.Response(500, json={"error": "boom"}))
        with pytest.raises(ServerError):
            sync_client.request("POST", "/things", cast_to=Thing, body={})
        assert route.call_count == 1

    @respx.mock
    def test_429_post_is_retried(self, sync_client: SyncAPIClient) -> None:
        """429 means the request was rejected unprocessed: safe for POST."""
        route = respx.post(f"{BASE_URL}/things")
        route.side_effect = [
            httpx.Response(429, json={"error": "rate limited"}),
            httpx.Response(201, json={"id": 7}),
        ]
        assert sync_client.request("POST", "/things", cast_to=Thing, body={}).id == 7
        assert route.call_count == 2

    @respx.mock
    def test_connect_error_is_retried_even_for_post(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/things")
        route.side_effect = [
            httpx.ConnectError("boom"),
            httpx.Response(201, json={"id": 7}),
        ]
        assert sync_client.request("POST", "/things", cast_to=Thing, body={}).id == 7

    @respx.mock
    def test_read_timeout_is_not_retried_for_post(self, sync_client: SyncAPIClient) -> None:
        """A read timeout means the server may have processed the POST."""
        route = respx.post(f"{BASE_URL}/things")
        route.side_effect = httpx.ReadTimeout("slow")
        with pytest.raises(APITimeoutError):
            sync_client.request("POST", "/things", cast_to=Thing, body={})
        assert route.call_count == 1

    @respx.mock
    def test_read_timeout_is_retried_for_get(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/me")
        route.side_effect = [httpx.ReadTimeout("slow"), httpx.Response(200, json={"id": 1})]
        assert sync_client.request("GET", "/me", cast_to=Thing).id == 1

    @respx.mock
    def test_connection_errors_exhaust_retries(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/me").side_effect = httpx.ConnectError("down")
        with pytest.raises(APIConnectionError):
            sync_client.request("GET", "/me", cast_to=Thing)


class TestAsyncClient:
    @respx.mock
    async def test_basic_request(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/me").mock(return_value=httpx.Response(200, json={"id": 1}))
        thing = await async_client.request("GET", "/me", cast_to=Thing)
        assert thing.id == 1

    @respx.mock
    async def test_retry_on_429(self, async_client: AsyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/me")
        route.side_effect = [
            httpx.Response(429, json={"error": "rate limited"}),
            httpx.Response(200, json={"id": 1}),
        ]
        thing = await async_client.request("GET", "/me", cast_to=Thing)
        assert thing.id == 1
        assert route.call_count == 2

    @respx.mock
    async def test_500_post_is_not_retried(self, async_client: AsyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/things")
        route.mock(return_value=httpx.Response(500, json={"error": "boom"}))
        with pytest.raises(ServerError):
            await async_client.request("POST", "/things", cast_to=Thing, body={})
        assert route.call_count == 1
