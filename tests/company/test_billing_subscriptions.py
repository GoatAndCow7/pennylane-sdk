from __future__ import annotations

import json
from decimal import Decimal

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.billing_subscriptions import (
    AsyncBillingSubscriptions,
    BillingSubscriptions,
)

from ..conftest import BASE_URL

BILLING_SUBSCRIPTION = {
    "id": 42,
    "next_occurrence": "2026-02-01",
    "prev_occurrence": "2026-01-01",
    "stopped_at": None,
    "start": "2026-01-01",
    "finish": None,
    "status": "in_progress",
    "mode": "finalized",
    "activated_at": "2026-01-01T09:00:00Z",
    "payment_conditions": "30_days",
    "payment_method": "offline",
    "label": "Monthly consulting",
    "email_settings": None,
    "recurring_rule": {
        "day_of_month": [1],
        "month_of_year": None,
        "week_start": None,
        "day": None,
        "rule_type": "monthly",
        "interval": 1,
        "count": None,
        "until": None,
    },
    "customer": {"id": 7, "url": "https://app.pennylane.com/api/external/v2/customers/7"},
    "customer_invoice_data": {
        "label": "Demo label",
        "currency": "EUR",
        "amount": "230.32",
        "currency_amount": "230.32",
        "currency_amount_before_tax": "196.32",
        "exchange_rate": "1.0",
        "currency_tax": "34.0",
        "language": "fr_FR",
        "customer_invoice_template": {"id": 1},
        "discount": {"type": "absolute", "value": "0"},
        "pdf_invoice_free_text": "Thanks",
        "pdf_invoice_subject": "Invoice subject",
        "pdf_description": None,
        "special_mention": None,
        "invoice_line_sections": {
            "url": "https://app.pennylane.com/api/external/v2/billing_subscriptions/42/invoice_line_sections"
        },
        "invoice_lines": {
            "url": "https://app.pennylane.com/api/external/v2/billing_subscriptions/42/invoice_lines"
        },
    },
    "created_at": "2026-01-01T09:00:00Z",
    "updated_at": "2026-01-02T09:00:00Z",
}

INVOICE_LINE = {
    "id": 444,
    "label": "Demo label",
    "unit": "piece",
    "quantity": "12",
    "amount": "50.4",
    "currency_amount": "50.4",
    "description": "Line description",
    "product": {"id": 3049, "url": "https://app.pennylane.com/api/external/v2/products/42"},
    "vat_rate": "FR_200",
    "currency_amount_before_tax": "30",
    "currency_tax": "10",
    "tax": "10",
    "raw_currency_unit_price": "5",
    "discount": {"type": "absolute", "value": "25"},
    "section_rank": 1,
    "imputation_dates": {"start_date": "2020-06-30", "end_date": "2021-06-30"},
    "created_at": "2026-01-01T09:00:00Z",
    "updated_at": "2026-01-01T09:00:00Z",
}

INVOICE_LINE_SECTION = {
    "id": 444,
    "title": "Section 1",
    "description": "Lorem ipsum",
    "rank": 1,
    "created_at": "2026-01-01T09:00:00Z",
    "updated_at": "2026-01-01T09:00:00Z",
}


class TestBillingSubscriptions:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/billing_subscriptions").mock(
            return_value=httpx.Response(
                200, json={"items": [BILLING_SUBSCRIPTION], "has_more": False, "next_cursor": None}
            )
        )
        page = BillingSubscriptions(sync_client).list(limit=50, sort="-id")
        assert route.calls.last.request.url.params["limit"] == "50"
        assert route.calls.last.request.url.params["sort"] == "-id"
        subscription = page.items[0]
        assert subscription.id == 42
        assert subscription.customer_invoice_data is not None
        assert subscription.customer_invoice_data.amount == Decimal("230.32")
        assert subscription.customer is not None
        assert subscription.customer.id == 7
        assert subscription.recurring_rule is not None
        assert subscription.recurring_rule.rule_type == "monthly"

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/billing_subscriptions/42").mock(
            return_value=httpx.Response(200, json=BILLING_SUBSCRIPTION)
        )
        subscription = BillingSubscriptions(sync_client).get(42)
        assert subscription.label == "Monthly consulting"

    @respx.mock
    def test_create_drops_none_and_sends_nested_dicts(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/billing_subscriptions").mock(
            return_value=httpx.Response(201, json=BILLING_SUBSCRIPTION)
        )
        BillingSubscriptions(sync_client).create(
            start="2026-01-01",
            mode={"type": "finalized"},
            payment_conditions="30_days",
            payment_method="offline",
            recurring_rule={"type": "monthly", "interval": 1, "day_of_month": 1},
            customer_id=7,
            customer_invoice_data={
                "invoice_lines": [
                    {
                        "label": "Consulting",
                        "quantity": 1,
                        "unit": "day",
                        "raw_currency_unit_price": "500.00",
                        "vat_rate": "FR_200",
                    }
                ]
            },
        )
        body = json.loads(route.calls.last.request.content)
        assert body == {
            "start": "2026-01-01",
            "mode": {"type": "finalized"},
            "payment_conditions": "30_days",
            "payment_method": "offline",
            "recurring_rule": {"type": "monthly", "interval": 1, "day_of_month": 1},
            "customer_id": 7,
            "customer_invoice_data": {
                "invoice_lines": [
                    {
                        "label": "Consulting",
                        "quantity": 1,
                        "unit": "day",
                        "raw_currency_unit_price": "500.00",
                        "vat_rate": "FR_200",
                    }
                ]
            },
        }

    @respx.mock
    def test_update_sends_only_provided_fields(self, sync_client: SyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/billing_subscriptions/42").mock(
            return_value=httpx.Response(200, json=BILLING_SUBSCRIPTION)
        )
        BillingSubscriptions(sync_client).update(42, stop=True)
        assert json.loads(route.calls.last.request.content) == {"stop": True}

    @respx.mock
    def test_list_invoice_lines(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/billing_subscriptions/42/invoice_lines").mock(
            return_value=httpx.Response(
                200, json={"items": [INVOICE_LINE], "has_more": False, "next_cursor": None}
            )
        )
        page = BillingSubscriptions(sync_client).list_invoice_lines(42, limit=10)
        assert route.calls.last.request.url.params["limit"] == "10"
        line = page.items[0]
        assert line.id == 444
        assert line.amount == Decimal("50.4")
        assert line.product is not None
        assert line.product.id == 3049

    @respx.mock
    def test_list_invoice_line_sections(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/billing_subscriptions/42/invoice_line_sections").mock(
            return_value=httpx.Response(
                200, json={"items": [INVOICE_LINE_SECTION], "has_more": False, "next_cursor": None}
            )
        )
        page = BillingSubscriptions(sync_client).list_invoice_line_sections(42)
        section = page.items[0]
        assert section.id == 444
        assert section.rank == 1


class TestAsyncBillingSubscriptions:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/billing_subscriptions").mock(
            return_value=httpx.Response(
                200, json={"items": [BILLING_SUBSCRIPTION], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncBillingSubscriptions(async_client).list()
        assert page.items[0].id == 42

    @respx.mock
    async def test_get(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/billing_subscriptions/42").mock(
            return_value=httpx.Response(200, json=BILLING_SUBSCRIPTION)
        )
        subscription = await AsyncBillingSubscriptions(async_client).get(42)
        assert subscription.id == 42

    @respx.mock
    async def test_create(self, async_client: AsyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/billing_subscriptions").mock(
            return_value=httpx.Response(201, json=BILLING_SUBSCRIPTION)
        )
        subscription = await AsyncBillingSubscriptions(async_client).create(
            start="2026-01-01",
            mode={"type": "awaiting_validation"},
            payment_conditions="30_days",
            payment_method="offline",
            recurring_rule={"type": "yearly"},
            customer_id=7,
            customer_invoice_data={"invoice_lines": []},
        )
        assert subscription.id == 42
        body = json.loads(route.calls.last.request.content)
        assert body["mode"] == {"type": "awaiting_validation"}

    @respx.mock
    async def test_update(self, async_client: AsyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/billing_subscriptions/42").mock(
            return_value=httpx.Response(200, json=BILLING_SUBSCRIPTION)
        )
        subscription = await AsyncBillingSubscriptions(async_client).update(
            42, payment_method="gocardless_direct_debit"
        )
        assert subscription.id == 42

    @respx.mock
    async def test_list_invoice_lines(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/billing_subscriptions/42/invoice_lines").mock(
            return_value=httpx.Response(
                200, json={"items": [INVOICE_LINE], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncBillingSubscriptions(async_client).list_invoice_lines(42)
        assert page.items[0].id == 444

    @respx.mock
    async def test_list_invoice_line_sections(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/billing_subscriptions/42/invoice_line_sections").mock(
            return_value=httpx.Response(
                200, json={"items": [INVOICE_LINE_SECTION], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncBillingSubscriptions(async_client).list_invoice_line_sections(42)
        assert page.items[0].id == 444
