"""Read-only sweep: every list endpoint against the real API.

Validates that the Pydantic models parse real responses (not just the
OpenAPI spec they were built from) and that pagination behaves.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest

from pennylane_sdk import Pennylane, filters

# (test id, callable(client) -> page). limit=2 keeps the sweep fast and
# exercises serialization on real records when the sandbox has data.
LIST_CALLS: list[tuple[str, Callable[[Pennylane], Any]]] = [
    ("customer_invoices", lambda c: c.customer_invoices.list(limit=2)),
    ("customer_invoice_templates", lambda c: c.customer_invoice_templates.list(limit=2)),
    ("quotes", lambda c: c.quotes.list(limit=2)),
    ("commercial_documents", lambda c: c.commercial_documents.list(limit=2)),
    ("billing_subscriptions", lambda c: c.billing_subscriptions.list(limit=2)),
    ("customers", lambda c: c.customers.list(limit=2)),
    ("products", lambda c: c.products.list(limit=2)),
    ("suppliers", lambda c: c.suppliers.list(limit=2)),
    ("supplier_invoices", lambda c: c.supplier_invoices.list(limit=2)),
    ("purchase_requests", lambda c: c.purchase_requests.list(limit=2)),
    ("transactions", lambda c: c.transactions.list(limit=2)),
    ("bank_accounts", lambda c: c.bank_accounts.list(limit=2)),
    ("bank_establishments", lambda c: c.bank_establishments.list(limit=2)),
    ("journals", lambda c: c.journals.list(limit=2)),
    ("ledger_accounts", lambda c: c.ledger_accounts.list(limit=2)),
    ("ledger_entries", lambda c: c.ledger_entries.list(limit=2)),
    ("ledger_entry_lines", lambda c: c.ledger_entry_lines.list(limit=2)),
    ("fiscal_years", lambda c: c.fiscal_years.list()),
    ("categories", lambda c: c.categories.list(limit=2)),
    ("category_groups", lambda c: c.category_groups.list(limit=2)),
    ("sepa_mandates", lambda c: c.sepa_mandates.list(limit=2)),
    ("gocardless_mandates", lambda c: c.gocardless_mandates.list(limit=2)),
    ("pa_registrations", lambda c: c.pa_registrations.list()),
    ("webhook_subscriptions", lambda c: c.webhook_subscriptions.list()),
    ("pro_account_mandates", lambda c: c.pro_account.list_mandates()),
    ("changelog_customer_invoices", lambda c: c.changelogs.customer_invoices(limit=2)),
    ("changelog_supplier_invoices", lambda c: c.changelogs.supplier_invoices(limit=2)),
    ("changelog_customers", lambda c: c.changelogs.customers(limit=2)),
    ("changelog_suppliers", lambda c: c.changelogs.suppliers(limit=2)),
    ("changelog_products", lambda c: c.changelogs.products(limit=2)),
    ("changelog_ledger_entry_lines", lambda c: c.changelogs.ledger_entry_lines(limit=2)),
    ("changelog_transactions", lambda c: c.changelogs.transactions(limit=2)),
    ("changelog_quotes", lambda c: c.changelogs.quotes(limit=2)),
]


@pytest.mark.parametrize(("name", "call"), LIST_CALLS, ids=[n for n, _ in LIST_CALLS])
def test_list_parses_real_response(
    live_client: Pennylane, name: str, call: Callable[[Pennylane], Any]
) -> None:
    from pennylane_sdk import NotFoundError

    try:
        page = call(live_client)
    except NotFoundError as exc:
        # Some features are absent from a given company (e.g. no Pro Account).
        pytest.skip(f"feature not enabled on this company: {exc.message}")
    assert isinstance(page.items, list)
    # Serialization round-trip must hold on real data.
    for item in page.items:
        assert item.model_dump() is not None


def test_me(live_client: Pennylane) -> None:
    me = live_client.me.retrieve()
    assert me.model_dump()


def test_trial_balance_with_required_params(live_client: Pennylane) -> None:
    page = live_client.trial_balance.list(
        period_start="2026-01-01", period_end="2026-12-31"
    )
    assert isinstance(page.items, list)


def test_real_pagination_walks_pages(live_client: Pennylane) -> None:
    first = live_client.ledger_accounts.list(limit=1)
    assert len(first.items) <= 1
    if first.has_more:
        second = first.next_page()
        assert second is not None
        assert second.items[0].id != first.items[0].id


def test_real_filtering(live_client: Pennylane) -> None:
    page = live_client.customer_invoices.list(
        filter=[filters.gte("date", "2000-01-01")], limit=2
    )
    assert isinstance(page.items, list)


def test_get_on_listed_record(live_client: Pennylane) -> None:
    accounts = live_client.ledger_accounts.list(limit=1)
    if not accounts.items:
        pytest.skip("sandbox has no ledger accounts")
    account = live_client.ledger_accounts.get(accounts.items[0].id)
    assert account.id == accounts.items[0].id


def test_rate_limit_headers_are_tracked(live_client: Pennylane) -> None:
    live_client.me.retrieve()
    info = live_client.last_rate_limit
    assert info is not None
    assert info.limit == 25
