from __future__ import annotations

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.firm.changelogs import AsyncFirmChangelogs, FirmChangelogs

FIRM_BASE_URL = "https://app.pennylane.com/api/external/firm/v1"

CHANGELOG_PAGE = {
    "items": [
        {
            "id": 1,
            "operation": "update",
            "processed_at": "2026-01-05T09:00:00Z",
            "updated_at": "2026-01-05T09:00:00Z",
            "created_at": "2026-01-01T09:00:00Z",
        }
    ],
    "has_more": False,
    "next_cursor": None,
}


def sync_client() -> SyncAPIClient:
    return SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)


def async_client() -> AsyncAPIClient:
    return AsyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)


class TestFirmChangelogs:
    @respx.mock
    def test_dms_files(self) -> None:
        route = respx.get(f"{FIRM_BASE_URL}/companies/10/changelogs/dms_files").mock(
            return_value=httpx.Response(200, json=CHANGELOG_PAGE)
        )
        page = FirmChangelogs(sync_client()).dms_files(10, limit=10)
        assert route.calls.last.request.url.params["limit"] == "10"
        assert page.items[0].operation == "update"

    @respx.mock
    def test_ledger_entry_lines(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/10/changelogs/ledger_entry_lines").mock(
            return_value=httpx.Response(200, json=CHANGELOG_PAGE)
        )
        page = FirmChangelogs(sync_client()).ledger_entry_lines(10)
        assert page.items[0].id == 1

    @respx.mock
    def test_supplier_invoices(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/10/changelogs/supplier_invoices").mock(
            return_value=httpx.Response(200, json=CHANGELOG_PAGE)
        )
        page = FirmChangelogs(sync_client()).supplier_invoices(10)
        assert page.items[0].id == 1

    @respx.mock
    def test_customer_invoices(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/10/changelogs/customer_invoices").mock(
            return_value=httpx.Response(200, json=CHANGELOG_PAGE)
        )
        page = FirmChangelogs(sync_client()).customer_invoices(10)
        assert page.items[0].id == 1


class TestAsyncFirmChangelogs:
    @respx.mock
    async def test_dms_files(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/10/changelogs/dms_files").mock(
            return_value=httpx.Response(200, json=CHANGELOG_PAGE)
        )
        page = await AsyncFirmChangelogs(async_client()).dms_files(10)
        assert page.items[0].id == 1

    @respx.mock
    async def test_ledger_entry_lines(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/10/changelogs/ledger_entry_lines").mock(
            return_value=httpx.Response(200, json=CHANGELOG_PAGE)
        )
        page = await AsyncFirmChangelogs(async_client()).ledger_entry_lines(10)
        assert page.items[0].id == 1

    @respx.mock
    async def test_supplier_invoices(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/10/changelogs/supplier_invoices").mock(
            return_value=httpx.Response(200, json=CHANGELOG_PAGE)
        )
        page = await AsyncFirmChangelogs(async_client()).supplier_invoices(10)
        assert page.items[0].id == 1

    @respx.mock
    async def test_customer_invoices(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/10/changelogs/customer_invoices").mock(
            return_value=httpx.Response(200, json=CHANGELOG_PAGE)
        )
        page = await AsyncFirmChangelogs(async_client()).customer_invoices(10)
        assert page.items[0].id == 1
