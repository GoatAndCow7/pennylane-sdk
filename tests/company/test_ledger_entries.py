from __future__ import annotations

import json
from decimal import Decimal

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.ledger_entries import (
    AsyncLedgerAttachments,
    AsyncLedgerEntries,
    LedgerAttachments,
    LedgerEntries,
)

from ..conftest import BASE_URL

LEDGER_ENTRY_LINE = {
    "id": 501,
    "debit": "100.00",
    "credit": "0.00",
    "label": "Transaction label",
    "ledger_account_id": 706,
    "ledger_account": {"id": 706, "number": "706000", "url": "https://example.test/706"},
}

LEDGER_ENTRY = {
    "id": 99,
    "label": "Payment for Services",
    "piece_number": "TENSNYLUGV",
    "date": "2026-01-05",
    "due_date": None,
    "invoice_number": None,
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
    "journal_id": 7,
    "journal": {"id": 7, "url": "https://example.test/journals/7"},
    "status": "draft",
    "categories": [],
    "ledger_attachment_filename": None,
    "attachment": None,
    "ledger_entry_lines": [LEDGER_ENTRY_LINE],
}

LEDGER_ATTACHMENT = {"id": 5, "url": "https://example.test/files/5", "filename": "receipt.pdf"}


class TestLedgerEntries:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/ledger_entries").mock(
            return_value=httpx.Response(
                200, json={"items": [LEDGER_ENTRY], "has_more": False, "next_cursor": None}
            )
        )
        page = LedgerEntries(sync_client).list(limit=50, sort="-id")
        assert route.calls.last.request.url.params["limit"] == "50"
        entry = page.items[0]
        assert entry.id == 99
        assert entry.journal is not None
        assert entry.journal.id == 7
        assert entry.ledger_entry_lines is not None
        assert entry.ledger_entry_lines[0].debit == Decimal("100.00")

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/ledger_entries/99").mock(
            return_value=httpx.Response(200, json=LEDGER_ENTRY)
        )
        entry = LedgerEntries(sync_client).get(99)
        assert entry.label == "Payment for Services"

    @respx.mock
    def test_create_sends_lines_and_drops_none(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/ledger_entries").mock(
            return_value=httpx.Response(201, json=LEDGER_ENTRY)
        )
        LedgerEntries(sync_client).create(
            date="2026-01-05",
            label="Payment for Services",
            journal_id=7,
            ledger_entry_lines=[
                {"debit": "100.00", "credit": "0.00", "ledger_account_id": 706},
                {"debit": "0.00", "credit": "100.00", "ledger_account_id": 512},
            ],
        )
        body = json.loads(route.calls.last.request.content)
        assert body == {
            "date": "2026-01-05",
            "label": "Payment for Services",
            "journal_id": 7,
            "ledger_entry_lines": [
                {"debit": "100.00", "credit": "0.00", "ledger_account_id": 706},
                {"debit": "0.00", "credit": "100.00", "ledger_account_id": 512},
            ],
        }

    @respx.mock
    def test_update_sends_only_provided_fields(self, sync_client: SyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/ledger_entries/99").mock(
            return_value=httpx.Response(200, json=LEDGER_ENTRY)
        )
        LedgerEntries(sync_client).update(
            99,
            label="New label",
            ledger_entry_lines={"delete": [{"id": 501}]},
        )
        assert json.loads(route.calls.last.request.content) == {
            "label": "New label",
            "ledger_entry_lines": {"delete": [{"id": 501}]},
        }

    @respx.mock
    def test_list_lines(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/ledger_entries/99/ledger_entry_lines").mock(
            return_value=httpx.Response(
                200, json={"items": [LEDGER_ENTRY_LINE], "has_more": False, "next_cursor": None}
            )
        )
        page = LedgerEntries(sync_client).list_lines(99, limit=10)
        assert route.calls.last.request.url.params["limit"] == "10"
        line = page.items[0]
        assert line.id == 501
        assert line.credit == Decimal("0.00")
        assert line.ledger_account is not None
        assert line.ledger_account.number == "706000"


class TestLedgerAttachments:
    @respx.mock
    def test_create_uploads_multipart(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/ledger_attachments").mock(
            return_value=httpx.Response(201, json=LEDGER_ATTACHMENT)
        )
        attachment = LedgerAttachments(sync_client).create(
            (b"%PDF-1.4 ..."), filename="receipt.pdf"
        )
        assert attachment.id == 5
        assert attachment.filename == "receipt.pdf"
        request = route.calls.last.request
        assert b"receipt.pdf" in request.content


class TestAsyncLedgerEntries:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/ledger_entries").mock(
            return_value=httpx.Response(
                200, json={"items": [LEDGER_ENTRY], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncLedgerEntries(async_client).list()
        assert page.items[0].id == 99

    @respx.mock
    async def test_create(self, async_client: AsyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/ledger_entries").mock(
            return_value=httpx.Response(201, json=LEDGER_ENTRY)
        )
        entry = await AsyncLedgerEntries(async_client).create(
            date="2026-01-05",
            label="Payment for Services",
            journal_id=7,
            ledger_entry_lines=[
                {"debit": "100.00", "credit": "0.00", "ledger_account_id": 706},
            ],
        )
        assert entry.id == 99
        body = json.loads(route.calls.last.request.content)
        assert body["journal_id"] == 7

    @respx.mock
    async def test_update(self, async_client: AsyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/ledger_entries/99").mock(
            return_value=httpx.Response(200, json=LEDGER_ENTRY)
        )
        entry = await AsyncLedgerEntries(async_client).update(99, label="New label")
        assert entry.id == 99

    @respx.mock
    async def test_list_lines(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/ledger_entries/99/ledger_entry_lines").mock(
            return_value=httpx.Response(
                200, json={"items": [LEDGER_ENTRY_LINE], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncLedgerEntries(async_client).list_lines(99)
        assert page.items[0].id == 501


class TestAsyncLedgerAttachments:
    @respx.mock
    async def test_create(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/ledger_attachments").mock(
            return_value=httpx.Response(201, json=LEDGER_ATTACHMENT)
        )
        attachment = await AsyncLedgerAttachments(async_client).create(
            b"%PDF-1.4 ...", filename="receipt.pdf"
        )
        assert attachment.id == 5
