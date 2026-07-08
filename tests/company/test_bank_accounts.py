from __future__ import annotations

import json
from decimal import Decimal

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.bank_accounts import (
    AsyncBankAccounts,
    AsyncBankEstablishments,
    BankAccounts,
    BankEstablishments,
)

from ..conftest import BASE_URL

BANK_ACCOUNT = {
    "id": 7,
    "name": "Main account",
    "currency": "EUR",
    "balance": "1000.00",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
    "bank_establishment": {"id": 3},
    "journal": {"id": 1, "url": "https://example.com/journals/1"},
    "ledger_account": {"id": 2, "url": "https://example.com/ledger_accounts/2"},
}

BANK_ESTABLISHMENT = {
    "id": 3,
    "name": "Some Bank",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}


class TestBankAccounts:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/bank_accounts").mock(
            return_value=httpx.Response(
                200, json={"items": [BANK_ACCOUNT], "has_more": False, "next_cursor": None}
            )
        )
        page = BankAccounts(sync_client).list(limit=50, sort="-id")
        assert route.calls.last.request.url.params["limit"] == "50"
        assert route.calls.last.request.url.params["sort"] == "-id"
        account = page.items[0]
        assert account.id == 7
        assert account.balance == Decimal("1000.00")
        assert account.bank_establishment is not None
        assert account.bank_establishment.id == 3

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/bank_accounts/7").mock(
            return_value=httpx.Response(200, json=BANK_ACCOUNT)
        )
        account = BankAccounts(sync_client).get(7)
        assert account.name == "Main account"

    @respx.mock
    def test_create_drops_none(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/bank_accounts").mock(
            return_value=httpx.Response(201, json=BANK_ACCOUNT)
        )
        BankAccounts(sync_client).create(name="Main account", iban="FR7630006000011234567890189")
        body = json.loads(route.calls.last.request.content)
        assert body == {"name": "Main account", "iban": "FR7630006000011234567890189"}


class TestBankEstablishments:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/bank_establishments").mock(
            return_value=httpx.Response(
                200,
                json={"items": [BANK_ESTABLISHMENT], "has_more": False, "next_cursor": None},
            )
        )
        page = BankEstablishments(sync_client).list(limit=20)
        assert route.calls.last.request.url.params["limit"] == "20"
        assert page.items[0].id == 3
        assert page.items[0].name == "Some Bank"


class TestAsyncBankAccounts:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/bank_accounts").mock(
            return_value=httpx.Response(
                200, json={"items": [BANK_ACCOUNT], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncBankAccounts(async_client).list()
        assert page.items[0].id == 7

    @respx.mock
    async def test_create(self, async_client: AsyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/bank_accounts").mock(
            return_value=httpx.Response(201, json=BANK_ACCOUNT)
        )
        account = await AsyncBankAccounts(async_client).create(
            name="Main account", account_type="checking"
        )
        assert account.id == 7
        body = json.loads(route.calls.last.request.content)
        assert body == {"name": "Main account", "account_type": "checking"}

    @respx.mock
    async def test_get(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/bank_accounts/7").mock(
            return_value=httpx.Response(200, json=BANK_ACCOUNT)
        )
        account = await AsyncBankAccounts(async_client).get(7)
        assert account.id == 7


class TestAsyncBankEstablishments:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/bank_establishments").mock(
            return_value=httpx.Response(
                200,
                json={"items": [BANK_ESTABLISHMENT], "has_more": False, "next_cursor": None},
            )
        )
        page = await AsyncBankEstablishments(async_client).list()
        assert page.items[0].id == 3
