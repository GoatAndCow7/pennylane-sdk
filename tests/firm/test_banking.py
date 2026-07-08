from __future__ import annotations

import json
from decimal import Decimal

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.firm.banking import (
    AsyncFirmBankAccounts,
    AsyncFirmTransactions,
    FirmBankAccounts,
    FirmTransactions,
)

FIRM_BASE_URL = "https://app.pennylane.com/api/external/firm/v1"

BANK_ACCOUNT = {
    "id": 3,
    "name": "Main account",
    "currency": "EUR",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
    "bank_establishment": {"id": 1},
    "journal": {"id": 2, "url": "https://x/journals/2"},
    "ledger_account": {"id": 4, "url": "https://x/ledger_accounts/4"},
}

TRANSACTION = {
    "id": 55,
    "label": "Wire transfer",
    "attachment_required": True,
    "date": "2026-01-05",
    "outstanding_balance": "100.00",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
    "archived_at": None,
    "currency": "EUR",
    "currency_amount": "100.00",
    "amount": "100.00",
    "currency_fee": None,
    "fee": None,
    "journal": {"id": 2, "url": "https://x/journals/2"},
    "bank_account": {"id": 3, "url": "https://x/bank_accounts/3"},
    "pro_account_expense": None,
    "customer": None,
    "supplier": None,
    "categories": [],
}


def sync_client() -> SyncAPIClient:
    return SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)


def async_client() -> AsyncAPIClient:
    return AsyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)


class TestFirmBankAccounts:
    @respx.mock
    def test_list(self) -> None:
        route = respx.get(f"{FIRM_BASE_URL}/companies/1/bank_accounts").mock(
            return_value=httpx.Response(
                200, json={"items": [BANK_ACCOUNT], "has_more": False, "next_cursor": None}
            )
        )
        page = FirmBankAccounts(sync_client()).list(1, sort="-id")
        assert route.calls.last.request.url.params["sort"] == "-id"
        assert page.items[0].id == 3

    @respx.mock
    def test_create(self) -> None:
        route = respx.post(f"{FIRM_BASE_URL}/companies/1/bank_accounts").mock(
            return_value=httpx.Response(201, json=BANK_ACCOUNT)
        )
        account = FirmBankAccounts(sync_client()).create(1, name="Main account")
        assert account.id == 3
        body = json.loads(route.calls.last.request.content)
        assert body == {"name": "Main account"}


class TestFirmTransactions:
    @respx.mock
    def test_list(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/1/transactions").mock(
            return_value=httpx.Response(
                200, json={"items": [TRANSACTION], "has_more": False, "next_cursor": None}
            )
        )
        page = FirmTransactions(sync_client()).list(1)
        assert page.items[0].id == 55
        assert page.items[0].amount == Decimal("100.00")

    @respx.mock
    def test_create(self) -> None:
        route = respx.post(f"{FIRM_BASE_URL}/companies/1/transactions").mock(
            return_value=httpx.Response(201, json=TRANSACTION)
        )
        FirmTransactions(sync_client()).create(
            1, bank_account_id=3, label="Wire transfer", date="2026-01-05", amount=Decimal("100.00")
        )
        body = json.loads(route.calls.last.request.content)
        assert body == {
            "bank_account_id": 3,
            "label": "Wire transfer",
            "date": "2026-01-05",
            "amount": "100.00",
        }

    @respx.mock
    def test_update(self) -> None:
        route = respx.put(f"{FIRM_BASE_URL}/companies/1/transactions/55").mock(
            return_value=httpx.Response(200, json=TRANSACTION)
        )
        transaction = FirmTransactions(sync_client()).update(1, 55, customer_id=9)
        assert transaction.id == 55
        assert json.loads(route.calls.last.request.content) == {"customer_id": 9}


class TestAsyncFirmBankAccounts:
    @respx.mock
    async def test_list(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/1/bank_accounts").mock(
            return_value=httpx.Response(
                200, json={"items": [BANK_ACCOUNT], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncFirmBankAccounts(async_client()).list(1)
        assert page.items[0].id == 3

    @respx.mock
    async def test_create(self) -> None:
        respx.post(f"{FIRM_BASE_URL}/companies/1/bank_accounts").mock(
            return_value=httpx.Response(201, json=BANK_ACCOUNT)
        )
        account = await AsyncFirmBankAccounts(async_client()).create(1, name="Main account")
        assert account.id == 3


class TestAsyncFirmTransactions:
    @respx.mock
    async def test_list(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/1/transactions").mock(
            return_value=httpx.Response(
                200, json={"items": [TRANSACTION], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncFirmTransactions(async_client()).list(1)
        assert page.items[0].id == 55

    @respx.mock
    async def test_create(self) -> None:
        respx.post(f"{FIRM_BASE_URL}/companies/1/transactions").mock(
            return_value=httpx.Response(201, json=TRANSACTION)
        )
        transaction = await AsyncFirmTransactions(async_client()).create(
            1, bank_account_id=3, label="Wire transfer", date="2026-01-05", amount="100.00"
        )
        assert transaction.id == 55

    @respx.mock
    async def test_update(self) -> None:
        respx.put(f"{FIRM_BASE_URL}/companies/1/transactions/55").mock(
            return_value=httpx.Response(200, json=TRANSACTION)
        )
        transaction = await AsyncFirmTransactions(async_client()).update(1, 55, supplier_id=11)
        assert transaction.id == 55
