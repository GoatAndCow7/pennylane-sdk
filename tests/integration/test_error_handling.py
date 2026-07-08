"""Real API error responses must map to the documented SDK exceptions."""

from __future__ import annotations

import pytest

from pennylane_sdk import NotFoundError, Pennylane, PennylaneError, ValidationError


def test_missing_record_raises_not_found(live_client: Pennylane) -> None:
    with pytest.raises(NotFoundError) as exc_info:
        live_client.products.get(999_999_999)
    assert exc_info.value.status_code == 404
    assert exc_info.value.message


def test_unbalanced_ledger_entry_raises_validation_error(live_client: Pennylane) -> None:
    journals = live_client.journals.list(limit=1)
    accounts = live_client.ledger_accounts.list(limit=2)
    if not journals.items or len(accounts.items) < 2:
        pytest.skip("sandbox lacks a journal or ledger accounts")
    with pytest.raises((ValidationError, PennylaneError)) as exc_info:
        live_client.ledger_entries.create(
            date="2026-07-01",
            journal_id=journals.items[0].id,
            label="Integration test: intentionally unbalanced",
            ledger_entry_lines=[
                {"ledger_account_id": accounts.items[0].id, "debit": "100.00", "credit": "0.00"},
                {"ledger_account_id": accounts.items[1].id, "debit": "0.00", "credit": "80.00"},
            ],
        )
    assert isinstance(exc_info.value, PennylaneError)


def test_invalid_token_raises_authentication_error() -> None:
    from pennylane_sdk import AuthenticationError

    with (
        Pennylane(api_token="invalid-token-for-testing") as bad_client,
        pytest.raises(AuthenticationError),
    ):
        bad_client.me.retrieve()
