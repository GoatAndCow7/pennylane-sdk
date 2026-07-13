from __future__ import annotations

import datetime as dt

import httpx
import pytest
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.changelogs import AsyncChangelogs, Changelogs

from ..conftest import BASE_URL

EVENT = {
    "id": 42,
    "operation": "update",
    "processed_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-05T09:00:00Z",
    "created_at": "2026-01-01T09:00:00Z",
}

RESOURCES = [
    "customer_invoices",
    "supplier_invoices",
    "customers",
    "suppliers",
    "products",
    "ledger_entry_lines",
    "transactions",
    "quotes",
]


class TestChangelogs:
    @pytest.mark.parametrize("resource", RESOURCES)
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient, resource: str) -> None:
        route = respx.get(f"{BASE_URL}/changelogs/{resource}").mock(
            return_value=httpx.Response(
                200, json={"items": [EVENT], "has_more": False, "next_cursor": None}
            )
        )
        method = getattr(Changelogs(sync_client), resource)
        page = method(limit=25, start_date=dt.date(2026, 1, 1))
        assert route.calls.last.request.url.params["limit"] == "25"
        assert route.calls.last.request.url.params["start_date"] == "2026-01-01"
        event = page.items[0]
        assert event.id == 42
        assert event.operation == "update"


class TestAsyncChangelogs:
    @pytest.mark.parametrize("resource", RESOURCES)
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient, resource: str) -> None:
        respx.get(f"{BASE_URL}/changelogs/{resource}").mock(
            return_value=httpx.Response(
                200, json={"items": [EVENT], "has_more": False, "next_cursor": None}
            )
        )
        method = getattr(AsyncChangelogs(async_client), resource)
        page = await method()
        assert page.items[0].id == 42


class TestCategoryChangelogs:
    @respx.mock
    def test_ledger_entries_categories(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/changelogs/ledger_entries_categories").mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [
                        {
                            "id": 7,
                            "operation": "insert",
                            "ledger_entry": {"id": 42, "type": "ledger_entry"},
                            "processed_at": "2026-07-10T08:00:00Z",
                        }
                    ],
                    "has_more": False,
                    "next_cursor": None,
                },
            )
        )
        page = Changelogs(sync_client).ledger_entries_categories(limit=500)
        assert route.calls.last.request.url.params["limit"] == "500"
        event = page.items[0]
        assert event.id == 7
        assert event.operation == "insert"

    @respx.mock
    def test_ledger_entry_lines_categories(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/changelogs/ledger_entry_lines_categories").mock(
            return_value=httpx.Response(
                200, json={"items": [], "has_more": False, "next_cursor": None}
            )
        )
        page = Changelogs(sync_client).ledger_entry_lines_categories(
            start_date=dt.date(2026, 7, 1)
        )
        assert page.items == []

    @respx.mock
    async def test_async_ledger_entries_categories(
        self, async_client: AsyncAPIClient
    ) -> None:
        respx.get(f"{BASE_URL}/changelogs/ledger_entries_categories").mock(
            return_value=httpx.Response(
                200, json={"items": [], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncChangelogs(async_client).ledger_entries_categories()
        assert page.items == []
