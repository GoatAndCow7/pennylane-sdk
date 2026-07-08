from __future__ import annotations

import datetime as dt
import json
from decimal import Decimal

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.firm.accounting import (
    AsyncFirmFiscalYears,
    AsyncFirmJournals,
    AsyncFirmLedgerAccounts,
    AsyncFirmLedgerEntries,
    AsyncFirmLedgerEntryLines,
    AsyncFirmTrialBalance,
    FirmFiscalYears,
    FirmJournals,
    FirmLedgerAccounts,
    FirmLedgerEntries,
    FirmLedgerEntryLines,
    FirmTrialBalance,
)

FIRM_BASE_URL = "https://app.pennylane.com/api/external/firm/v1"

FISCAL_YEAR = {"id": 1, "start": "2026-01-01", "finish": "2026-12-31", "status": "open"}

TRIAL_BALANCE_ROW = {
    "number": "401000",
    "label": "Suppliers",
    "debits": "100.00",
    "credits": "50.00",
    "formatted_number": "401",
}

JOURNAL = {"id": 3, "code": "VE", "label": "Sales", "type": "sales"}

LEDGER_ACCOUNT = {
    "id": 9,
    "number": "401000",
    "label": "Suppliers",
    "vat_rate": "FR_200",
    "country_alpha2": "FR",
    "enabled": True,
    "letterable": True,
    "archived_at": None,
}

LEDGER_ENTRY = {
    "id": 55,
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
    "label": "Purchase",
    "piece_number": "PC-1",
    "date": "2026-01-05",
    "journal": {"id": 3, "url": "https://app.pennylane.com/journals/3"},
    "due_date": None,
    "invoice_number": None,
    "status": "draft",
    "categories": [],
    "attachment": None,
}

LEDGER_ENTRY_LINE = {
    "id": 101,
    "debit": "100.00",
    "credit": "0.00",
    "label": "Purchase line",
    "categories": [],
    "ledger_account": {"id": 9, "number": "401000", "url": "https://x/ledger_accounts/9"},
    "journal": {"id": 3, "url": "https://x/journals/3"},
    "date": "2026-01-05",
    "ledger_entry": {"id": 55, "url": "https://x/ledger_entries/55"},
    "lettered_ledger_entry_lines": {"ids": [101], "url": "https://x/lettered"},
    "imputation_dates": [{"start_date": "2026-01-01", "end_date": "2026-01-31"}],
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}


class TestFirmFiscalYears:
    @respx.mock
    def test_list(self) -> None:
        client = SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        route = respx.get(f"{FIRM_BASE_URL}/companies/7/fiscal_years").mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [FISCAL_YEAR],
                    "total_pages": 1,
                    "current_page": 1,
                    "total_items": 1,
                    "per_page": 20,
                },
            )
        )
        page = FirmFiscalYears(client).list(7, page=1)
        assert route.calls.last.request.url.params["page"] == "1"
        assert page.items[0].id == 1
        assert page.items[0].start == dt.date(2026, 1, 1)

    @respx.mock
    def test_create(self) -> None:
        client = SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        route = respx.post(f"{FIRM_BASE_URL}/companies/7/fiscal_years").mock(
            return_value=httpx.Response(201, json=FISCAL_YEAR)
        )
        fiscal_year = FirmFiscalYears(client).create(7, start="2026-01-01", finish="2026-12-31")
        assert fiscal_year.id == 1
        assert json.loads(route.calls.last.request.content) == {
            "start": "2026-01-01",
            "finish": "2026-12-31",
        }


class TestFirmTrialBalance:
    @respx.mock
    def test_list(self) -> None:
        client = SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        route = respx.get(f"{FIRM_BASE_URL}/companies/7/trial_balance").mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [TRIAL_BALANCE_ROW],
                    "total_pages": 1,
                    "current_page": 1,
                    "total_items": 1,
                    "per_page": 20,
                },
            )
        )
        page = FirmTrialBalance(client).list(
            7, period_start="2026-01-01", period_end="2026-12-31"
        )
        assert route.calls.last.request.url.params["period_start"] == "2026-01-01"
        row = page.items[0]
        assert row.debits == Decimal("100.00")
        assert row.credits == Decimal("50.00")


class TestFirmJournals:
    @respx.mock
    def test_list(self) -> None:
        client = SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        respx.get(f"{FIRM_BASE_URL}/companies/7/journals").mock(
            return_value=httpx.Response(
                200, json={"items": [JOURNAL], "has_more": False, "next_cursor": None}
            )
        )
        page = FirmJournals(client).list(7)
        assert page.items[0].code == "VE"

    @respx.mock
    def test_get(self) -> None:
        client = SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        respx.get(f"{FIRM_BASE_URL}/companies/7/journals/3").mock(
            return_value=httpx.Response(200, json=JOURNAL)
        )
        journal = FirmJournals(client).get(7, 3)
        assert journal.label == "Sales"

    @respx.mock
    def test_create(self) -> None:
        client = SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        route = respx.post(f"{FIRM_BASE_URL}/companies/7/journals").mock(
            return_value=httpx.Response(201, json=JOURNAL)
        )
        journal = FirmJournals(client).create(7, code="VE", label="Sales")
        assert journal.id == 3
        assert json.loads(route.calls.last.request.content) == {"code": "VE", "label": "Sales"}


class TestFirmLedgerAccounts:
    @respx.mock
    def test_list(self) -> None:
        client = SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        respx.get(f"{FIRM_BASE_URL}/companies/7/ledger_accounts").mock(
            return_value=httpx.Response(
                200, json={"items": [LEDGER_ACCOUNT], "has_more": False, "next_cursor": None}
            )
        )
        page = FirmLedgerAccounts(client).list(7)
        assert page.items[0].number == "401000"

    @respx.mock
    def test_get(self) -> None:
        client = SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        respx.get(f"{FIRM_BASE_URL}/companies/7/ledger_accounts/9").mock(
            return_value=httpx.Response(200, json=LEDGER_ACCOUNT)
        )
        account = FirmLedgerAccounts(client).get(7, 9)
        assert account.id == 9

    @respx.mock
    def test_create_drops_none(self) -> None:
        client = SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        route = respx.post(f"{FIRM_BASE_URL}/companies/7/ledger_accounts").mock(
            return_value=httpx.Response(201, json=LEDGER_ACCOUNT)
        )
        FirmLedgerAccounts(client).create(7, number="401000", label="Suppliers")
        assert json.loads(route.calls.last.request.content) == {
            "number": "401000",
            "label": "Suppliers",
        }

    @respx.mock
    def test_update_sends_only_provided_fields(self) -> None:
        client = SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        route = respx.put(f"{FIRM_BASE_URL}/companies/7/ledger_accounts/9").mock(
            return_value=httpx.Response(200, json=LEDGER_ACCOUNT)
        )
        FirmLedgerAccounts(client).update(7, 9, letterable=False)
        assert json.loads(route.calls.last.request.content) == {"letterable": False}


class TestFirmLedgerEntries:
    @respx.mock
    def test_list(self) -> None:
        client = SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        respx.get(f"{FIRM_BASE_URL}/companies/7/ledger_entries").mock(
            return_value=httpx.Response(
                200, json={"items": [LEDGER_ENTRY], "has_more": False, "next_cursor": None}
            )
        )
        page = FirmLedgerEntries(client).list(7)
        assert page.items[0].id == 55
        assert page.items[0].journal is not None
        assert page.items[0].journal.id == 3

    @respx.mock
    def test_get(self) -> None:
        client = SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        respx.get(f"{FIRM_BASE_URL}/companies/7/ledger_entries/55").mock(
            return_value=httpx.Response(200, json=LEDGER_ENTRY)
        )
        entry = FirmLedgerEntries(client).get(7, 55)
        assert entry.label == "Purchase"

    @respx.mock
    def test_create(self) -> None:
        client = SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        route = respx.post(f"{FIRM_BASE_URL}/companies/7/ledger_entries").mock(
            return_value=httpx.Response(201, json=LEDGER_ENTRY)
        )
        entry = FirmLedgerEntries(client).create(
            7,
            date="2026-01-05",
            label="Purchase",
            journal_id=3,
            ledger_entry_lines=[
                {"debit": "100.00", "credit": "0.00", "ledger_account_id": 9},
                {"debit": "0.00", "credit": "100.00", "ledger_account_id": 10},
            ],
        )
        assert entry.id == 55
        body = json.loads(route.calls.last.request.content)
        assert body["journal_id"] == 3
        assert len(body["ledger_entry_lines"]) == 2

    @respx.mock
    def test_update(self) -> None:
        client = SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        route = respx.put(f"{FIRM_BASE_URL}/companies/7/ledger_entries/55").mock(
            return_value=httpx.Response(200, json=LEDGER_ENTRY)
        )
        FirmLedgerEntries(client).update(7, 55, label="Purchase updated")
        assert json.loads(route.calls.last.request.content) == {"label": "Purchase updated"}


class TestFirmLedgerEntryLines:
    @respx.mock
    def test_list(self) -> None:
        client = SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        respx.get(f"{FIRM_BASE_URL}/companies/7/ledger_entry_lines").mock(
            return_value=httpx.Response(
                200, json={"items": [LEDGER_ENTRY_LINE], "has_more": False, "next_cursor": None}
            )
        )
        page = FirmLedgerEntryLines(client).list(7)
        assert page.items[0].debit == Decimal("100.00")

    @respx.mock
    def test_get(self) -> None:
        client = SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        respx.get(f"{FIRM_BASE_URL}/companies/7/ledger_entry_lines/101").mock(
            return_value=httpx.Response(200, json=LEDGER_ENTRY_LINE)
        )
        line = FirmLedgerEntryLines(client).get(7, 101)
        assert line.id == 101
        assert line.imputation_dates is not None
        assert line.imputation_dates[0].start_date is not None

    @respx.mock
    def test_list_lettered_lines(self) -> None:
        client = SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        route = respx.get(
            f"{FIRM_BASE_URL}/companies/7/ledger_entry_lines/101/lettered_ledger_entry_lines"
        ).mock(
            return_value=httpx.Response(
                200, json={"items": [LEDGER_ENTRY_LINE], "has_more": False, "next_cursor": None}
            )
        )
        page = FirmLedgerEntryLines(client).list_lettered_lines(7, 101, limit=10)
        assert route.calls.last.request.url.params["limit"] == "10"
        assert page.items[0].id == 101


class TestAsyncFirmAccounting:
    @respx.mock
    async def test_fiscal_years_list(self) -> None:
        client = AsyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        respx.get(f"{FIRM_BASE_URL}/companies/7/fiscal_years").mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [FISCAL_YEAR],
                    "total_pages": 1,
                    "current_page": 1,
                    "total_items": 1,
                    "per_page": 20,
                },
            )
        )
        page = await AsyncFirmFiscalYears(client).list(7)
        assert page.items[0].id == 1

    @respx.mock
    async def test_trial_balance_list(self) -> None:
        client = AsyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        respx.get(f"{FIRM_BASE_URL}/companies/7/trial_balance").mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [TRIAL_BALANCE_ROW],
                    "total_pages": 1,
                    "current_page": 1,
                    "total_items": 1,
                    "per_page": 20,
                },
            )
        )
        page = await AsyncFirmTrialBalance(client).list(
            7, period_start="2026-01-01", period_end="2026-12-31"
        )
        assert page.items[0].number == "401000"

    @respx.mock
    async def test_journals_create(self) -> None:
        client = AsyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        respx.post(f"{FIRM_BASE_URL}/companies/7/journals").mock(
            return_value=httpx.Response(201, json=JOURNAL)
        )
        journal = await AsyncFirmJournals(client).create(7, code="VE", label="Sales")
        assert journal.id == 3

    @respx.mock
    async def test_ledger_accounts_update(self) -> None:
        client = AsyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        respx.put(f"{FIRM_BASE_URL}/companies/7/ledger_accounts/9").mock(
            return_value=httpx.Response(200, json=LEDGER_ACCOUNT)
        )
        account = await AsyncFirmLedgerAccounts(client).update(7, 9, label="New label")
        assert account.id == 9

    @respx.mock
    async def test_ledger_entries_create(self) -> None:
        client = AsyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        respx.post(f"{FIRM_BASE_URL}/companies/7/ledger_entries").mock(
            return_value=httpx.Response(201, json=LEDGER_ENTRY)
        )
        entry = await AsyncFirmLedgerEntries(client).create(
            7,
            date="2026-01-05",
            label="Purchase",
            journal_id=3,
            ledger_entry_lines=[{"debit": "100.00", "credit": "0.00", "ledger_account_id": 9}],
        )
        assert entry.id == 55

    @respx.mock
    async def test_ledger_entry_lines_list_lettered_lines(self) -> None:
        client = AsyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        respx.get(
            f"{FIRM_BASE_URL}/companies/7/ledger_entry_lines/101/lettered_ledger_entry_lines"
        ).mock(
            return_value=httpx.Response(
                200, json={"items": [LEDGER_ENTRY_LINE], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncFirmLedgerEntryLines(client).list_lettered_lines(7, 101)
        assert page.items[0].id == 101
