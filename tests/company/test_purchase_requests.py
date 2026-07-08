from __future__ import annotations

import json
from decimal import Decimal

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.purchase_requests import (
    AsyncPurchaseRequests,
    PurchaseRequests,
)

from ..conftest import BASE_URL

PURCHASE_REQUEST = {
    "id": 17,
    "purchase_order_number": "PO-0001",
    "supplier": {"id": 7, "url": "https://api.example/suppliers/7"},
    "delivery_address": {
        "address": "1 rue de Paris",
        "postal_code": "75001",
        "city": "Paris",
        "country_alpha2": "FR",
    },
    "status": "to_be_validated",
    "currency": "EUR",
    "reason": "New laptops",
    "estimated_delivery_date": "2026-02-01",
    "amount": "1234.56",
    "currency_amount": "1234.56",
    "currency_amount_before_tax": "1029.00",
    "exchange_rate": "1.0",
    "currency_tax": "205.56",
    "tax": "205.56",
    "purchase_order": {"filename": "po.pdf", "url": "https://files.example/po.pdf"},
    "linked_invoices": {"items": []},
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}


class TestPurchaseRequests:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/purchase_requests").mock(
            return_value=httpx.Response(
                200, json={"items": [PURCHASE_REQUEST], "has_more": False, "next_cursor": None}
            )
        )
        page = PurchaseRequests(sync_client).list(limit=50, sort="-id")
        assert route.calls.last.request.url.params["limit"] == "50"
        assert route.calls.last.request.url.params["sort"] == "-id"
        request = page.items[0]
        assert request.id == 17
        assert request.amount == Decimal("1234.56")
        assert request.supplier is not None
        assert request.supplier.id == 7
        assert request.delivery_address is not None
        assert request.delivery_address.city == "Paris"

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/purchase_requests/17").mock(
            return_value=httpx.Response(200, json=PURCHASE_REQUEST)
        )
        request = PurchaseRequests(sync_client).get(17)
        assert request.purchase_order_number == "PO-0001"
        assert request.linked_invoices is not None
        assert request.linked_invoices.items == []

    @respx.mock
    def test_import_from_file(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/purchase_requests/imports").mock(
            return_value=httpx.Response(201, json=PURCHASE_REQUEST)
        )
        request = PurchaseRequests(sync_client).import_from_file(
            file_attachment_id=11,
            reason="New laptops",
            supplier_id=7,
            purchase_order_number="PO-0001",
            currency_amount_before_tax=Decimal("1029.00"),
            currency_amount=Decimal("1234.56"),
            currency_tax=Decimal("205.56"),
            delivery_address={
                "address": "1 rue de Paris",
                "postal_code": "75001",
                "city": "Paris",
                "country_alpha2": "FR",
            },
            purchase_request_lines=[
                {
                    "currency_amount": "1234.56",
                    "label": "Laptop",
                    "quantity": 2,
                    "unit_price": "617.28",
                    "unit": "piece",
                    "vat_rate": "FR_200",
                }
            ],
        )
        assert request.id == 17
        body = json.loads(route.calls.last.request.content)
        assert body["file_attachment_id"] == 11
        assert body["reason"] == "New laptops"
        assert body["currency_amount_before_tax"] == "1029.00"
        assert body["delivery_address"]["city"] == "Paris"
        assert body["purchase_request_lines"][0]["label"] == "Laptop"

    @respx.mock
    def test_import_from_file_drops_none(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/purchase_requests/imports").mock(
            return_value=httpx.Response(201, json=PURCHASE_REQUEST)
        )
        PurchaseRequests(sync_client).import_from_file(
            file_attachment_id=11,
            reason="New laptops",
            supplier_id=7,
            purchase_order_number="PO-0001",
            currency_amount_before_tax=Decimal("1029.00"),
            currency_amount=Decimal("1234.56"),
            currency_tax=Decimal("205.56"),
            delivery_address={"address": "1 rue de Paris"},
            purchase_request_lines=[],
        )
        body = json.loads(route.calls.last.request.content)
        assert "estimated_delivery_date" not in body
        assert "currency" not in body
        assert "amount" not in body
        assert "tax" not in body


class TestAsyncPurchaseRequests:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/purchase_requests").mock(
            return_value=httpx.Response(
                200, json={"items": [PURCHASE_REQUEST], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncPurchaseRequests(async_client).list()
        assert page.items[0].id == 17

    @respx.mock
    async def test_get(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/purchase_requests/17").mock(
            return_value=httpx.Response(200, json=PURCHASE_REQUEST)
        )
        request = await AsyncPurchaseRequests(async_client).get(17)
        assert request.id == 17

    @respx.mock
    async def test_import_from_file(self, async_client: AsyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/purchase_requests/imports").mock(
            return_value=httpx.Response(201, json=PURCHASE_REQUEST)
        )
        request = await AsyncPurchaseRequests(async_client).import_from_file(
            file_attachment_id=11,
            reason="New laptops",
            supplier_id=7,
            purchase_order_number="PO-0001",
            currency_amount_before_tax="1029.00",
            currency_amount="1234.56",
            currency_tax="205.56",
            delivery_address={
                "address": "1 rue de Paris",
                "postal_code": "75001",
                "city": "Paris",
                "country_alpha2": "FR",
            },
            purchase_request_lines=[
                {
                    "currency_amount": "1234.56",
                    "label": "Laptop",
                    "quantity": 2,
                    "unit_price": "617.28",
                    "unit": "piece",
                    "vat_rate": "FR_200",
                }
            ],
        )
        assert request.id == 17
        body = json.loads(route.calls.last.request.content)
        assert body["supplier_id"] == 7
