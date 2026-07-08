from __future__ import annotations

import json
from decimal import Decimal

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.transactions import AsyncTransactions, Transactions

from ..conftest import BASE_URL

TRANSACTION = {
    "id": 42,
    "label": "Client payment",
    "attachment_required": True,
    "date": "2026-01-05",
    "outstanding_balance": "100.00",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
    "archived_at": None,
    "currency": "EUR",
    "currency_amount": "500.00",
    "amount": "500.00",
    "currency_fee": None,
    "fee": None,
    "journal": {"id": 1, "url": "https://example.com/journals/1"},
    "bank_account": {"id": 7, "url": "https://example.com/bank_accounts/7"},
    "pro_account_expense": None,
    "customer": {"id": 5, "url": "https://example.com/customers/5"},
    "supplier": None,
    "categories": [],
    "matched_invoices": {"url": "https://example.com/transactions/42/matched_invoices"},
    "interbank_code": None,
}

TRANSACTION_CATEGORY = {
    "id": 421,
    "label": "HR - Salaries",
    "weight": "0.25",
    "category_group": {"id": 229},
    "analytical_code": "CODE123",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}

MATCHED_INVOICE = {
    "id": 99,
    "type": "customer",
    "url": "https://example.com/customer_invoices/99",
}


class TestTransactions:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/transactions").mock(
            return_value=httpx.Response(
                200, json={"items": [TRANSACTION], "has_more": False, "next_cursor": None}
            )
        )
        page = Transactions(sync_client).list(limit=50, sort="-id")
        assert route.calls.last.request.url.params["limit"] == "50"
        assert route.calls.last.request.url.params["sort"] == "-id"
        transaction = page.items[0]
        assert transaction.id == 42
        assert transaction.amount == Decimal("500.00")
        assert transaction.bank_account is not None
        assert transaction.bank_account.id == 7

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/transactions/42").mock(
            return_value=httpx.Response(200, json=TRANSACTION)
        )
        transaction = Transactions(sync_client).get(42)
        assert transaction.label == "Client payment"

    @respx.mock
    def test_create_sends_money_as_string_and_drops_none(
        self, sync_client: SyncAPIClient
    ) -> None:
        route = respx.post(f"{BASE_URL}/transactions").mock(
            return_value=httpx.Response(201, json=TRANSACTION)
        )
        Transactions(sync_client).create(
            bank_account_id=7,
            label="Client payment",
            date="2026-01-05",
            amount=Decimal("500.00"),
        )
        body = json.loads(route.calls.last.request.content)
        assert body == {
            "bank_account_id": 7,
            "label": "Client payment",
            "date": "2026-01-05",
            "amount": "500.00",
        }

    @respx.mock
    def test_update_customer(self, sync_client: SyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/transactions/42").mock(
            return_value=httpx.Response(200, json=TRANSACTION)
        )
        Transactions(sync_client).update(42, customer_id=5)
        assert json.loads(route.calls.last.request.content) == {"customer_id": 5}
        assert route.calls.last.request.url.path.endswith("/transactions/42")

    @respx.mock
    def test_list_categories(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/transactions/42/categories").mock(
            return_value=httpx.Response(
                200,
                json={"items": [TRANSACTION_CATEGORY], "has_more": False, "next_cursor": None},
            )
        )
        page = Transactions(sync_client).list_categories(42, limit=10)
        assert route.calls.last.request.url.params["limit"] == "10"
        assert page.items[0].id == 421
        assert page.items[0].category_group is not None
        assert page.items[0].category_group.id == 229

    @respx.mock
    def test_categorize(self, sync_client: SyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/transactions/42/categories").mock(
            return_value=httpx.Response(200, json=[TRANSACTION_CATEGORY])
        )
        categories = Transactions(sync_client).categorize(
            42, categories=[{"id": 421, "weight": "1"}]
        )
        assert json.loads(route.calls.last.request.content) == [{"id": 421, "weight": "1"}]
        assert len(categories) == 1
        assert categories[0].id == 421
        assert categories[0].weight == "0.25"

    @respx.mock
    def test_list_matched_invoices(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/transactions/42/matched_invoices").mock(
            return_value=httpx.Response(
                200, json={"items": [MATCHED_INVOICE], "has_more": False, "next_cursor": None}
            )
        )
        page = Transactions(sync_client).list_matched_invoices(42)
        assert route.calls.last.request.url.path.endswith("/transactions/42/matched_invoices")
        assert page.items[0].id == 99
        assert page.items[0].type == "customer"


class TestAsyncTransactions:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/transactions").mock(
            return_value=httpx.Response(
                200, json={"items": [TRANSACTION], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncTransactions(async_client).list()
        assert page.items[0].id == 42

    @respx.mock
    async def test_create(self, async_client: AsyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/transactions").mock(
            return_value=httpx.Response(201, json=TRANSACTION)
        )
        transaction = await AsyncTransactions(async_client).create(
            bank_account_id=7,
            label="Client payment",
            date="2026-01-05",
            amount="500.00",
        )
        assert transaction.id == 42
        body = json.loads(route.calls.last.request.content)
        assert body["amount"] == "500.00"

    @respx.mock
    async def test_update(self, async_client: AsyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/transactions/42").mock(
            return_value=httpx.Response(200, json=TRANSACTION)
        )
        transaction = await AsyncTransactions(async_client).update(42, supplier_id=8)
        assert transaction.id == 42

    @respx.mock
    async def test_categorize(self, async_client: AsyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/transactions/42/categories").mock(
            return_value=httpx.Response(200, json=[TRANSACTION_CATEGORY])
        )
        categories = await AsyncTransactions(async_client).categorize(
            42, categories=[{"id": 421, "weight": "1"}]
        )
        assert categories[0].id == 421

    @respx.mock
    async def test_list_matched_invoices(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/transactions/42/matched_invoices").mock(
            return_value=httpx.Response(
                200, json={"items": [MATCHED_INVOICE], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncTransactions(async_client).list_matched_invoices(42)
        assert page.items[0].id == 99
