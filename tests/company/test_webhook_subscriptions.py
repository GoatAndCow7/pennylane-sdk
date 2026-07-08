from __future__ import annotations

import json

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.webhook_subscriptions import (
    AsyncWebhookSubscriptions,
    WebhookSubscriptions,
)

from ..conftest import BASE_URL

WEBHOOK_SUBSCRIPTION = {
    "id": 7,
    "callback_url": "https://example.com/webhooks/pennylane",
    "events": ["customer_invoice.e_invoicing_status_updated"],
    "enabled": True,
    "disabled_at": None,
    "disabled_reason": None,
    "last_failure_status": None,
    "last_failure_at": None,
    "consecutive_failures": 0,
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}

WEBHOOK_SUBSCRIPTION_CREATED = {
    **WEBHOOK_SUBSCRIPTION,
    "secret": "whsec_abcdef1234567890",
}


class TestWebhookSubscriptions:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/webhook_subscriptions").mock(
            return_value=httpx.Response(
                200,
                json={"items": [WEBHOOK_SUBSCRIPTION], "has_more": False, "next_cursor": None},
            )
        )
        page = WebhookSubscriptions(sync_client).list(limit=10)
        assert route.calls.last.request.url.params["limit"] == "10"
        assert page.items[0].id == 7
        assert page.items[0].secret is None

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/webhook_subscriptions/7").mock(
            return_value=httpx.Response(200, json=WEBHOOK_SUBSCRIPTION)
        )
        subscription = WebhookSubscriptions(sync_client).get(7)
        assert subscription.callback_url == "https://example.com/webhooks/pennylane"
        assert subscription.secret is None

    @respx.mock
    def test_create_returns_secret_once(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/webhook_subscriptions").mock(
            return_value=httpx.Response(201, json=WEBHOOK_SUBSCRIPTION_CREATED)
        )
        subscription = WebhookSubscriptions(sync_client).create(
            callback_url="https://example.com/webhooks/pennylane",
            events=["customer_invoice.e_invoicing_status_updated"],
        )
        assert json.loads(route.calls.last.request.content) == {
            "callback_url": "https://example.com/webhooks/pennylane",
            "events": ["customer_invoice.e_invoicing_status_updated"],
        }
        assert subscription.secret == "whsec_abcdef1234567890"

    @respx.mock
    def test_update_sends_only_provided_fields(self, sync_client: SyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/webhook_subscriptions/7").mock(
            return_value=httpx.Response(200, json=WEBHOOK_SUBSCRIPTION)
        )
        WebhookSubscriptions(sync_client).update(7, enabled=False)
        assert json.loads(route.calls.last.request.content) == {"enabled": False}

    @respx.mock
    def test_delete(self, sync_client: SyncAPIClient) -> None:
        route = respx.delete(f"{BASE_URL}/webhook_subscriptions/7").mock(
            return_value=httpx.Response(204)
        )
        result = WebhookSubscriptions(sync_client).delete(7)
        assert result is None
        assert route.calls.last.request.url.path.endswith("/webhook_subscriptions/7")


class TestAsyncWebhookSubscriptions:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/webhook_subscriptions").mock(
            return_value=httpx.Response(
                200,
                json={"items": [WEBHOOK_SUBSCRIPTION], "has_more": False, "next_cursor": None},
            )
        )
        page = await AsyncWebhookSubscriptions(async_client).list()
        assert page.items[0].id == 7

    @respx.mock
    async def test_create(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/webhook_subscriptions").mock(
            return_value=httpx.Response(201, json=WEBHOOK_SUBSCRIPTION_CREATED)
        )
        subscription = await AsyncWebhookSubscriptions(async_client).create(
            callback_url="https://example.com/webhooks/pennylane",
            events=["customer_invoice.e_invoicing_status_updated"],
            enabled=True,
        )
        assert subscription.secret == "whsec_abcdef1234567890"

    @respx.mock
    async def test_update(self, async_client: AsyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/webhook_subscriptions/7").mock(
            return_value=httpx.Response(200, json=WEBHOOK_SUBSCRIPTION)
        )
        subscription = await AsyncWebhookSubscriptions(async_client).update(
            7, callback_url="https://example.com/new"
        )
        assert subscription.id == 7

    @respx.mock
    async def test_delete(self, async_client: AsyncAPIClient) -> None:
        respx.delete(f"{BASE_URL}/webhook_subscriptions/7").mock(
            return_value=httpx.Response(204)
        )
        result = await AsyncWebhookSubscriptions(async_client).delete(7)
        assert result is None
