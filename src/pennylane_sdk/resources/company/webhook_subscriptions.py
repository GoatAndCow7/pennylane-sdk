"""Webhook Subscriptions resource (Company API v2).

Beta — undocumented endpoints, subject to change.

Reference: https://pennylane.readme.io/reference/postwebhooksubscriptions
"""

from __future__ import annotations

from ..._models import drop_none
from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...types.company.webhook_subscriptions import WebhookSubscription

__all__ = ["AsyncWebhookSubscriptions", "WebhookSubscriptions"]


class WebhookSubscriptions(SyncAPIResource):
    """Manage webhook subscriptions.

    Beta — subject to change.
    """

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> SyncCursorPage[WebhookSubscription]:
        """List webhook subscriptions.

        Beta — subject to change.

        Reference: https://pennylane.readme.io/reference/getwebhooksubscriptions

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (API default 20).
        """
        return self._get_page(
            "/webhook_subscriptions",
            item_type=WebhookSubscription,
            params={"cursor": cursor, "limit": limit},
        )

    def get(self, webhook_subscription_id: int) -> WebhookSubscription:
        """Retrieve a webhook subscription.

        Beta — subject to change.

        Reference: https://pennylane.readme.io/reference/getwebhooksubscription
        """
        return self._get(
            f"/webhook_subscriptions/{webhook_subscription_id}", cast_to=WebhookSubscription
        )

    def create(
        self,
        *,
        callback_url: str,
        events: list[str],
        enabled: bool | None = None,
    ) -> WebhookSubscription:
        """Create a webhook subscription.

        Beta — subject to change.

        The response's ``secret`` field is the HMAC signing secret for
        verifying webhook deliveries. It is generated automatically and
        returned **only in this creation response** — store it immediately,
        it cannot be retrieved again afterwards.

        Reference: https://pennylane.readme.io/reference/postwebhooksubscriptions

        Args:
            callback_url: HTTPS URL where webhook events will be sent.
            events: Event types to subscribe to.
            enabled: Whether the subscription is active (API default ``True``).
        """
        body = drop_none(
            {
                "callback_url": callback_url,
                "events": events,
                "enabled": enabled,
            }
        )
        return self._post("/webhook_subscriptions", cast_to=WebhookSubscription, body=body)

    def update(
        self,
        webhook_subscription_id: int,
        *,
        callback_url: str | None = None,
        events: list[str] | None = None,
        enabled: bool | None = None,
    ) -> WebhookSubscription:
        """Update a webhook subscription. Only the provided fields are modified.

        Beta — subject to change.

        Reference: https://pennylane.readme.io/reference/putwebhooksubscription
        """
        body = drop_none(
            {
                "callback_url": callback_url,
                "events": events,
                "enabled": enabled,
            }
        )
        return self._put(
            f"/webhook_subscriptions/{webhook_subscription_id}",
            cast_to=WebhookSubscription,
            body=body,
        )

    def delete(self, webhook_subscription_id: int) -> None:
        """Delete a webhook subscription.

        Beta — subject to change.

        Reference: https://pennylane.readme.io/reference/deletewebhooksubscription
        """
        return self._delete(f"/webhook_subscriptions/{webhook_subscription_id}", cast_to=None)


class AsyncWebhookSubscriptions(AsyncAPIResource):
    """Manage webhook subscriptions (async).

    Beta — subject to change.
    """

    async def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> AsyncCursorPage[WebhookSubscription]:
        """List webhook subscriptions.

        Beta — subject to change.

        Reference: https://pennylane.readme.io/reference/getwebhooksubscriptions
        """
        return await self._get_page(
            "/webhook_subscriptions",
            item_type=WebhookSubscription,
            params={"cursor": cursor, "limit": limit},
        )

    async def get(self, webhook_subscription_id: int) -> WebhookSubscription:
        """Retrieve a webhook subscription.

        Beta — subject to change.

        Reference: https://pennylane.readme.io/reference/getwebhooksubscription
        """
        return await self._get(
            f"/webhook_subscriptions/{webhook_subscription_id}", cast_to=WebhookSubscription
        )

    async def create(
        self,
        *,
        callback_url: str,
        events: list[str],
        enabled: bool | None = None,
    ) -> WebhookSubscription:
        """Create a webhook subscription.

        Beta — subject to change.

        The response's ``secret`` field is the HMAC signing secret for
        verifying webhook deliveries. It is generated automatically and
        returned **only in this creation response** — store it immediately,
        it cannot be retrieved again afterwards.

        Reference: https://pennylane.readme.io/reference/postwebhooksubscriptions
        """
        body = drop_none(
            {
                "callback_url": callback_url,
                "events": events,
                "enabled": enabled,
            }
        )
        return await self._post("/webhook_subscriptions", cast_to=WebhookSubscription, body=body)

    async def update(
        self,
        webhook_subscription_id: int,
        *,
        callback_url: str | None = None,
        events: list[str] | None = None,
        enabled: bool | None = None,
    ) -> WebhookSubscription:
        """Update a webhook subscription. Only the provided fields are modified.

        Beta — subject to change.

        Reference: https://pennylane.readme.io/reference/putwebhooksubscription
        """
        body = drop_none(
            {
                "callback_url": callback_url,
                "events": events,
                "enabled": enabled,
            }
        )
        return await self._put(
            f"/webhook_subscriptions/{webhook_subscription_id}",
            cast_to=WebhookSubscription,
            body=body,
        )

    async def delete(self, webhook_subscription_id: int) -> None:
        """Delete a webhook subscription.

        Beta — subject to change.

        Reference: https://pennylane.readme.io/reference/deletewebhooksubscription
        """
        return await self._delete(
            f"/webhook_subscriptions/{webhook_subscription_id}", cast_to=None
        )
