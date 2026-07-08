"""Webhook signature verification and payload parsing.

Pennylane webhooks (beta) POST a JSON payload to your HTTPS endpoint when an
event occurs. When you create a subscription
(``client.webhook_subscriptions.create``), the response contains a ``secret``
returned only once: used to sign deliveries with an HMAC.

.. warning::
   As of mid-2026 Pennylane documents the HMAC secret but NOT the exact
   signature header name or encoding. This module therefore verifies
   signatures defensively: it accepts hex or base64 encodings, with or
   without a ``sha256=`` prefix. Check your webhook deliveries to find the
   signature header (commonly ``X-Pennylane-Signature``), and keep the
   changelog endpoints (``client.changelogs``) as a fallback while the
   feature is in beta, as Pennylane itself recommends.

Known event types: ``customer_invoice.e_invoicing_status_updated``,
``dms_file.created``.
"""

from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import json
from typing import Any

from ._exceptions import PennylaneError
from ._models import PennylaneModel

__all__ = ["WebhookEvent", "WebhookSignatureError", "parse_event", "verify_signature"]


class WebhookSignatureError(PennylaneError):
    """The webhook payload signature could not be verified."""


class WebhookEvent(PennylaneModel):
    """A webhook delivery payload.

    Unknown fields are preserved (``extra="allow"``): inspect ``raw`` or the
    model's extra attributes for event-specific data.
    """

    event: str | None = None
    """Event type, e.g. ``customer_invoice.e_invoicing_status_updated``."""

    data: dict[str, Any] | None = None
    """Event payload, when the delivery wraps it in a ``data`` object."""


def _candidate_digests(payload: bytes, secret: str) -> list[bytes]:
    digest = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).digest()
    return [
        digest.hex().encode("ascii"),
        base64.b64encode(digest),
    ]


def _normalize_signature(signature: str) -> bytes:
    cleaned = signature.strip()
    for prefix in ("sha256=", "hmac-sha256="):
        if cleaned.lower().startswith(prefix):
            cleaned = cleaned[len(prefix):]
            break
    return cleaned.encode("ascii", errors="replace")


def verify_signature(payload: bytes | str, signature: str, secret: str) -> bool:
    """Check a webhook delivery signature (constant-time comparison).

    Args:
        payload: The RAW request body, exactly as received (bytes preferred
            re-serializing the JSON would change the bytes and the HMAC).
        signature: Value of the signature header of the delivery.
        secret: The subscription secret returned at creation time.

    Returns:
        ``True`` when the signature matches the HMAC-SHA256 of the payload,
        trying hex and base64 encodings, with or without a ``sha256=`` prefix.
    """
    if not signature or not secret:
        return False
    body = payload.encode("utf-8") if isinstance(payload, str) else payload
    provided = _normalize_signature(signature)
    return any(
        hmac.compare_digest(provided, candidate)
        for candidate in _candidate_digests(body, secret)
    )


def parse_event(
    payload: bytes | str,
    *,
    signature: str | None = None,
    secret: str | None = None,
) -> WebhookEvent:
    """Parse a webhook delivery, optionally verifying its signature first.

    Args:
        payload: The raw request body.
        signature: Signature header value; verified when ``secret`` is given.
        secret: Subscription secret. When provided together with
            ``signature``, the payload is verified before parsing and a
            :class:`WebhookSignatureError` is raised on mismatch.

    Raises:
        WebhookSignatureError: When verification was requested and failed.
        PennylaneError: When the payload is not valid JSON.
    """
    if secret is not None and (
        signature is None or not verify_signature(payload, signature, secret)
    ):
        raise WebhookSignatureError(
            "Webhook signature verification failed. Ensure you pass the raw "
            "request body and the secret returned when creating the subscription."
        )
    body = payload.decode("utf-8") if isinstance(payload, bytes) else payload
    try:
        parsed = json.loads(body)
    except (json.JSONDecodeError, UnicodeDecodeError, binascii.Error) as exc:
        raise PennylaneError(f"Webhook payload is not valid JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise PennylaneError("Webhook payload must be a JSON object.")
    return WebhookEvent.model_validate(parsed)
