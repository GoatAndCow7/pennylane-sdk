from __future__ import annotations

import json
from decimal import Decimal

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.ledger_entry_lines import (
    AsyncLedgerEntryLines,
    LedgerEntryLines,
)

from ..conftest import BASE_URL

LEDGER_ENTRY_LINE = {
    "id": 1,
    "debit": "100.00",
    "credit": "0.00",
    "label": "Purchase of goods",
    "categories": [
        {
            "id": 421,
            "label": "HR - Salaries",
            "weight": "0.25",
            "category_group": {"id": 229},
            "analytical_code": "CODE123",
            "created_at": "2023-08-30T09:00:00Z",
            "updated_at": "2023-08-30T09:00:00Z",
        }
    ],
    "ledger_account": {"id": 7, "number": "607000", "url": "https://api/ledger_accounts/7"},
    "journal": {"id": 3, "url": "https://api/journals/3"},
    "date": "2026-01-05",
    "ledger_entry": {"id": 99},
    "lettered_ledger_entry_lines": {
        "ids": [1, 2],
        "url": "https://api/ledger_entry_lines/1/lettered_ledger_entry_lines",
    },
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}

CATEGORY = LEDGER_ENTRY_LINE["categories"][0]


class TestLedgerEntryLines:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/ledger_entry_lines").mock(
            return_value=httpx.Response(
                200, json={"items": [LEDGER_ENTRY_LINE], "has_more": False, "next_cursor": None}
            )
        )
        page = LedgerEntryLines(sync_client).list(limit=50, sort="-id")
        assert route.calls.last.request.url.params["limit"] == "50"
        assert route.calls.last.request.url.params["sort"] == "-id"
        line = page.items[0]
        assert line.id == 1
        assert line.debit == Decimal("100.00")
        assert line.ledger_account is not None
        assert line.ledger_account.id == 7
        assert line.categories is not None
        assert line.categories[0].id == 421

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/ledger_entry_lines/1").mock(
            return_value=httpx.Response(200, json=LEDGER_ENTRY_LINE)
        )
        line = LedgerEntryLines(sync_client).get(1)
        assert line.label == "Purchase of goods"
        assert line.lettered_ledger_entry_lines is not None
        assert line.lettered_ledger_entry_lines.ids == [1, 2]

    @respx.mock
    def test_letter(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/ledger_entry_lines/lettering").mock(
            return_value=httpx.Response(200, json={})
        )
        result = LedgerEntryLines(sync_client).letter(
            unbalanced_lettering_strategy="none",
            ledger_entry_lines=[{"id": 1}, {"id": 2}],
        )
        assert result is None
        body = json.loads(route.calls.last.request.content)
        assert body == {
            "unbalanced_lettering_strategy": "none",
            "ledger_entry_lines": [{"id": 1}, {"id": 2}],
        }

    @respx.mock
    def test_unletter(self, sync_client: SyncAPIClient) -> None:
        route = respx.delete(f"{BASE_URL}/ledger_entry_lines/lettering").mock(
            return_value=httpx.Response(204)
        )
        result = LedgerEntryLines(sync_client).unletter(
            unbalanced_lettering_strategy="partial",
            ledger_entry_lines=[{"id": 1}],
        )
        assert result is None
        body = json.loads(route.calls.last.request.content)
        assert body == {
            "unbalanced_lettering_strategy": "partial",
            "ledger_entry_lines": [{"id": 1}],
        }

    @respx.mock
    def test_list_lettered_lines(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(
            f"{BASE_URL}/ledger_entry_lines/1/lettered_ledger_entry_lines"
        ).mock(
            return_value=httpx.Response(
                200, json={"items": [LEDGER_ENTRY_LINE], "has_more": False, "next_cursor": None}
            )
        )
        page = LedgerEntryLines(sync_client).list_lettered_lines(1, limit=10)
        assert route.calls.last.request.url.params["limit"] == "10"
        assert page.items[0].id == 1

    @respx.mock
    def test_list_categories(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/ledger_entry_lines/1/categories").mock(
            return_value=httpx.Response(
                200, json={"items": [CATEGORY], "has_more": False, "next_cursor": None}
            )
        )
        page = LedgerEntryLines(sync_client).list_categories(1, sort="-id")
        assert route.calls.last.request.url.params["sort"] == "-id"
        assert page.items[0].id == 421
        assert page.items[0].category_group is not None
        assert page.items[0].category_group.id == 229

    @respx.mock
    def test_categorize(self, sync_client: SyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/ledger_entry_lines/1/categories").mock(
            return_value=httpx.Response(
                200,
                json={
                    "ledger_entry_line": {
                        "id": 1,
                        "label": "Purchase of goods",
                        "categories": [CATEGORY],
                    }
                },
            )
        )
        result = LedgerEntryLines(sync_client).categorize(
            1, categories=[{"id": 421, "weight": "1"}]
        )
        body = json.loads(route.calls.last.request.content)
        assert body == [{"id": 421, "weight": "1"}]
        assert result.ledger_entry_line is not None
        assert result.ledger_entry_line.id == 1
        assert result.ledger_entry_line.categories is not None
        assert result.ledger_entry_line.categories[0].id == 421


class TestAsyncLedgerEntryLines:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/ledger_entry_lines").mock(
            return_value=httpx.Response(
                200, json={"items": [LEDGER_ENTRY_LINE], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncLedgerEntryLines(async_client).list()
        assert page.items[0].id == 1

    @respx.mock
    async def test_get(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/ledger_entry_lines/1").mock(
            return_value=httpx.Response(200, json=LEDGER_ENTRY_LINE)
        )
        line = await AsyncLedgerEntryLines(async_client).get(1)
        assert line.id == 1

    @respx.mock
    async def test_letter(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/ledger_entry_lines/lettering").mock(
            return_value=httpx.Response(200, json={})
        )
        result = await AsyncLedgerEntryLines(async_client).letter(
            unbalanced_lettering_strategy="none",
            ledger_entry_lines=[{"id": 1}, {"id": 2}],
        )
        assert result is None

    @respx.mock
    async def test_unletter(self, async_client: AsyncAPIClient) -> None:
        respx.delete(f"{BASE_URL}/ledger_entry_lines/lettering").mock(
            return_value=httpx.Response(204)
        )
        result = await AsyncLedgerEntryLines(async_client).unletter(
            unbalanced_lettering_strategy="none",
            ledger_entry_lines=[{"id": 1}],
        )
        assert result is None

    @respx.mock
    async def test_list_categories(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/ledger_entry_lines/1/categories").mock(
            return_value=httpx.Response(
                200, json={"items": [CATEGORY], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncLedgerEntryLines(async_client).list_categories(1)
        assert page.items[0].id == 421

    @respx.mock
    async def test_categorize(self, async_client: AsyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/ledger_entry_lines/1/categories").mock(
            return_value=httpx.Response(
                200,
                json={
                    "ledger_entry_line": {
                        "id": 1,
                        "label": "Purchase of goods",
                        "categories": [CATEGORY],
                    }
                },
            )
        )
        result = await AsyncLedgerEntryLines(async_client).categorize(
            1, categories=[{"id": 421, "weight": "1"}]
        )
        body = json.loads(route.calls.last.request.content)
        assert body == [{"id": 421, "weight": "1"}]
        assert result.ledger_entry_line is not None
        assert result.ledger_entry_line.id == 1

    @respx.mock
    async def test_list_lettered_lines(self, async_client: AsyncAPIClient) -> None:
        respx.get(
            f"{BASE_URL}/ledger_entry_lines/1/lettered_ledger_entry_lines"
        ).mock(
            return_value=httpx.Response(
                200, json={"items": [LEDGER_ENTRY_LINE], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncLedgerEntryLines(async_client).list_lettered_lines(1)
        assert page.items[0].id == 1
