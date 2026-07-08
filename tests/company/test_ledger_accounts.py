from __future__ import annotations

import json

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.ledger_accounts import AsyncLedgerAccounts, LedgerAccounts

from ..conftest import BASE_URL

LEDGER_ACCOUNT = {
    "id": 12,
    "number": "706000",
    "label": "Prestations de services",
    "vat_rate": "FR_200",
    "country_alpha2": "FR",
    "enabled": True,
    "type": "income",
    "letterable": False,
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}


class TestLedgerAccounts:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/ledger_accounts").mock(
            return_value=httpx.Response(
                200, json={"items": [LEDGER_ACCOUNT], "has_more": False, "next_cursor": None}
            )
        )
        page = LedgerAccounts(sync_client).list(limit=50, sort="-id")
        assert route.calls.last.request.url.params["limit"] == "50"
        assert route.calls.last.request.url.params["sort"] == "-id"
        account = page.items[0]
        assert account.id == 12
        assert account.number == "706000"
        assert account.letterable is False

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/ledger_accounts/12").mock(
            return_value=httpx.Response(200, json=LEDGER_ACCOUNT)
        )
        account = LedgerAccounts(sync_client).get(12)
        assert account.label == "Prestations de services"

    @respx.mock
    def test_create_drops_none(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/ledger_accounts").mock(
            return_value=httpx.Response(201, json=LEDGER_ACCOUNT)
        )
        LedgerAccounts(sync_client).create(number="706000", label="Prestations de services")
        body = json.loads(route.calls.last.request.content)
        assert body == {"number": "706000", "label": "Prestations de services"}

    @respx.mock
    def test_update_sends_only_provided_fields(self, sync_client: SyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/ledger_accounts/12").mock(
            return_value=httpx.Response(200, json=LEDGER_ACCOUNT)
        )
        LedgerAccounts(sync_client).update(12, letterable=True)
        assert json.loads(route.calls.last.request.content) == {"letterable": True}


class TestAsyncLedgerAccounts:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/ledger_accounts").mock(
            return_value=httpx.Response(
                200, json={"items": [LEDGER_ACCOUNT], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncLedgerAccounts(async_client).list()
        assert page.items[0].id == 12

    @respx.mock
    async def test_create(self, async_client: AsyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/ledger_accounts").mock(
            return_value=httpx.Response(201, json=LEDGER_ACCOUNT)
        )
        account = await AsyncLedgerAccounts(async_client).create(
            number="706000", label="Prestations de services", vat_rate="FR_200"
        )
        assert account.id == 12
        body = json.loads(route.calls.last.request.content)
        assert body["vat_rate"] == "FR_200"

    @respx.mock
    async def test_update(self, async_client: AsyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/ledger_accounts/12").mock(
            return_value=httpx.Response(200, json=LEDGER_ACCOUNT)
        )
        account = await AsyncLedgerAccounts(async_client).update(12, label="New label")
        assert account.id == 12
