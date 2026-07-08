"""Firm API integration tests: STRICTLY read-only.

A Firm token gives access to an accounting firm's REAL client companies,
so these tests never write anything. They run only when
``PENNYLANE_FIRM_API_TOKEN`` is set:

    PENNYLANE_FIRM_API_TOKEN=... uv run pytest tests/integration/test_firm_readonly.py -q

A read-only token is enough (and recommended).
"""

from __future__ import annotations

import os

import pytest

from pennylane_sdk import NotFoundError, PennylaneFirm

_FIRM_TOKEN = os.environ.get("PENNYLANE_FIRM_API_TOKEN")

pytestmark = pytest.mark.skipif(
    not _FIRM_TOKEN,
    reason="PENNYLANE_FIRM_API_TOKEN not set: firm integration tests need a firm token",
)


@pytest.fixture(scope="module")
def firm() -> PennylaneFirm:
    client = PennylaneFirm()  # throttled to the official 5 req/s
    yield client
    client.close()


@pytest.fixture(scope="module")
def company_id(firm: PennylaneFirm) -> int:
    page = firm.companies.list(per_page=1)
    if not page.items:
        pytest.skip("this firm has no client companies")
    return page.items[0].id


def test_companies_list_and_get(firm: PennylaneFirm, company_id: int) -> None:
    company = firm.companies.get(company_id)
    assert company.id == company_id
    assert company.model_dump()


def test_companies_numbered_pagination(firm: PennylaneFirm) -> None:
    first = firm.companies.list(per_page=1)
    assert len(first.items) <= 1
    if first.has_more:
        second = first.next_page()
        assert second is not None
        assert second.current_page == 2


def test_fiscal_years(firm: PennylaneFirm, company_id: int) -> None:
    page = firm.fiscal_years.list(company_id)
    assert isinstance(page.items, list)
    for fy in page.items:
        assert fy.model_dump()


def test_trial_balance(firm: PennylaneFirm, company_id: int) -> None:
    page = firm.trial_balance.list(
        company_id, period_start="2026-01-01", period_end="2026-12-31"
    )
    assert isinstance(page.items, list)


def test_accounting_reads(firm: PennylaneFirm, company_id: int) -> None:
    assert isinstance(firm.journals.list(company_id, limit=2).items, list)
    assert isinstance(firm.ledger_accounts.list(company_id, limit=2).items, list)
    assert isinstance(firm.ledger_entries.list(company_id, limit=2).items, list)
    assert isinstance(firm.ledger_entry_lines.list(company_id, limit=2).items, list)


def test_directory_reads(firm: PennylaneFirm, company_id: int) -> None:
    assert isinstance(firm.customers.list(company_id, limit=2).items, list)
    assert isinstance(firm.suppliers.list(company_id, limit=2).items, list)
    assert isinstance(firm.bank_accounts.list(company_id, limit=2).items, list)
    assert isinstance(firm.categories.list(company_id, limit=2).items, list)
    assert isinstance(firm.category_groups.list(company_id, limit=2).items, list)


def test_invoicing_reads_beta(firm: PennylaneFirm, company_id: int) -> None:
    try:
        assert isinstance(firm.customer_invoices.list(company_id, limit=2).items, list)
        assert isinstance(firm.supplier_invoices.list(company_id, limit=2).items, list)
    except NotFoundError:
        pytest.skip("invoicing endpoints (beta) not enabled for this firm")


def test_dms_reads(firm: PennylaneFirm, company_id: int) -> None:
    assert isinstance(firm.dms.folders.list(company_id, limit=2).items, list)
    assert isinstance(firm.dms.files.list(company_id, limit=2).items, list)


def test_changelogs(firm: PennylaneFirm, company_id: int) -> None:
    assert isinstance(firm.changelogs.ledger_entry_lines(company_id, limit=2).items, list)
    assert isinstance(firm.changelogs.dms_files(company_id, limit=2).items, list)


def test_rate_limit_is_firm_limit(firm: PennylaneFirm, company_id: int) -> None:
    firm.companies.get(company_id)
    info = firm.last_rate_limit
    assert info is not None
