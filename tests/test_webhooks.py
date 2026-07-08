from __future__ import annotations

import base64
import hashlib
import hmac

import pytest

from pennylane_sdk import PennylaneError
from pennylane_sdk.webhooks import (
    WebhookSignatureError,
    parse_event,
    verify_signature,
)

SECRET = "whsec_test_secret"
PAYLOAD = b'{"event":"dms_file.created","data":{"id":42}}'


def _hex_sig(payload: bytes = PAYLOAD, secret: str = SECRET) -> str:
    return hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()


def _b64_sig(payload: bytes = PAYLOAD, secret: str = SECRET) -> str:
    return base64.b64encode(hmac.new(secret.encode(), payload, hashlib.sha256).digest()).decode()


class TestVerifySignature:
    def test_hex_signature(self) -> None:
        assert verify_signature(PAYLOAD, _hex_sig(), SECRET) is True

    def test_base64_signature(self) -> None:
        assert verify_signature(PAYLOAD, _b64_sig(), SECRET) is True

    def test_sha256_prefixed_signature(self) -> None:
        assert verify_signature(PAYLOAD, f"sha256={_hex_sig()}", SECRET) is True

    def test_str_payload(self) -> None:
        assert verify_signature(PAYLOAD.decode(), _hex_sig(), SECRET) is True

    def test_wrong_secret_fails(self) -> None:
        assert verify_signature(PAYLOAD, _hex_sig(secret="other"), SECRET) is False

    def test_tampered_payload_fails(self) -> None:
        assert verify_signature(b'{"event":"evil"}', _hex_sig(), SECRET) is False

    def test_empty_signature_fails(self) -> None:
        assert verify_signature(PAYLOAD, "", SECRET) is False

    def test_non_ascii_signature_fails_gracefully(self) -> None:
        assert verify_signature(PAYLOAD, "sïgnature", SECRET) is False


class TestParseEvent:
    def test_parses_event_and_data(self) -> None:
        event = parse_event(PAYLOAD)
        assert event.event == "dms_file.created"
        assert event.data == {"id": 42}

    def test_verifies_signature_when_secret_given(self) -> None:
        event = parse_event(PAYLOAD, signature=_hex_sig(), secret=SECRET)
        assert event.event == "dms_file.created"

    def test_raises_on_bad_signature(self) -> None:
        with pytest.raises(WebhookSignatureError):
            parse_event(PAYLOAD, signature="bad", secret=SECRET)

    def test_raises_when_secret_given_but_signature_missing(self) -> None:
        with pytest.raises(WebhookSignatureError):
            parse_event(PAYLOAD, secret=SECRET)

    def test_raises_on_invalid_json(self) -> None:
        with pytest.raises(PennylaneError, match="not valid JSON"):
            parse_event(b"not-json")

    def test_raises_on_non_object_json(self) -> None:
        with pytest.raises(PennylaneError, match="JSON object"):
            parse_event(b"[1, 2]")

    def test_unknown_fields_preserved(self) -> None:
        event = parse_event(b'{"event":"x","company_id":7}')
        assert event.company_id == 7  # type: ignore[attr-defined]
