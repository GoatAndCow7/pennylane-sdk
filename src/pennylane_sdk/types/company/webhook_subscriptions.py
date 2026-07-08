"""Models for the Webhook Subscriptions resource (Company API v2).

Beta — undocumented endpoints, subject to change.
"""

from __future__ import annotations

import datetime as dt

from ..._models import PennylaneModel

__all__ = ["WebhookSubscription"]


class WebhookSubscription(PennylaneModel):
    """A webhook subscription.

    Beta — undocumented endpoint, subject to change.

    ``secret`` is the HMAC signing secret; it is only ever returned by
    ``create`` and is ``None`` on every other response (``get``, ``list``,
    ``update``). Store it when you receive it — it cannot be retrieved again.

    Reference: https://pennylane.readme.io/reference/postwebhooksubscriptions
    """

    id: int
    callback_url: str | None = None
    events: list[str] | None = None
    enabled: bool | None = None
    secret: str | None = None
    disabled_at: dt.datetime | None = None
    disabled_reason: str | None = None
    last_failure_status: int | None = None
    last_failure_at: dt.datetime | None = None
    consecutive_failures: int | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
