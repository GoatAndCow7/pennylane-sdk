from __future__ import annotations

import json
from decimal import Decimal

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.supplier_invoices import (
    AsyncSupplierInvoices,
    SupplierInvoices,
)

from ..conftest import BASE_URL

SUPPLIER_INVOICE = {
    "id": 42,
    "label": "Office supplies",
    "invoice_number": "INV-0001",
    "currency": "EUR",
    "amount": "600.00",
    "currency_amount": "600.00",
    "currency_amount_before_tax": "500.00",
    "exchange_rate": "1.0",
    "date": "2026-01-05",
    "deadline": "2026-02-05",
    "currency_tax": "100.00",
    "tax": "100.00",
    "reconciled": False,
    "accounting_status": "draft",
    "filename": "invoice.pdf",
    "public_file_url": "https://files.example/invoice.pdf",
    "remaining_amount_with_tax": "600.00",
    "remaining_amount_without_tax": "500.00",
    "ledger_entry": {"id": 99},
    "supplier": {"id": 7, "url": "https://api.example/suppliers/7"},
    "invoice_lines": {"url": "https://api.example/supplier_invoices/42/invoice_lines"},
    "categories": {"url": "https://api.example/supplier_invoices/42/categories"},
    "transaction_reference": None,
    "payment_status": "to_be_paid",
    "paid": False,
    "payments": {"url": "https://api.example/supplier_invoices/42/payments"},
    "matched_transactions": {
        "url": "https://api.example/supplier_invoices/42/matched_transactions"
    },
    "external_reference": "EXT-1",
    "e_invoicing": None,
    "archived_at": None,
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}

INVOICE_LINE = {
    "id": 444,
    "label": "Office chair",
    "amount": "50.4",
    "currency_amount": "50.4",
    "description": "Lorem ipsum",
    "vat_rate": "FR_200",
    "currency_amount_before_tax": "42.0",
    "currency_tax": "8.4",
    "tax": "8.4",
    "imputation_dates": None,
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-05T09:00:00Z",
}

PAYMENT = {
    "id": 5,
    "label": "Bank transfer",
    "currency": "EUR",
    "currency_amount": "600.00",
    "status": "matched",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-05T09:00:00Z",
}

MATCHED_TRANSACTION = {
    "id": 88,
    "label": "Virement Acme",
    "attachment_required": False,
    "date": "2026-01-06",
    "outstanding_balance": "0.00",
    "created_at": "2026-01-06T09:00:00Z",
    "updated_at": "2026-01-06T09:00:00Z",
    "archived_at": None,
    "currency": "EUR",
    "currency_amount": "600.00",
    "amount": "600.00",
    "currency_fee": None,
    "fee": None,
    "journal": {"id": 1},
    "bank_account": {"id": 2, "url": "https://api.example/bank_accounts/2"},
    "pro_account_expense": None,
    "supplier": {"id": 7, "url": "https://api.example/suppliers/7"},
    "categories": [],
}

CATEGORY = {
    "id": 426,
    "label": "Office - Supplies",
    "weight": "1",
    "category_group": {"id": 229},
    "analytical_code": "CODE123",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-05T09:00:00Z",
}


class TestSupplierInvoices:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/supplier_invoices").mock(
            return_value=httpx.Response(
                200, json={"items": [SUPPLIER_INVOICE], "has_more": False, "next_cursor": None}
            )
        )
        page = SupplierInvoices(sync_client).list(limit=50, sort="-id")
        assert route.calls.last.request.url.params["limit"] == "50"
        assert route.calls.last.request.url.params["sort"] == "-id"
        invoice = page.items[0]
        assert invoice.id == 42
        assert invoice.amount == Decimal("600.00")
        assert invoice.supplier is not None
        assert invoice.supplier.id == 7
        assert invoice.ledger_entry is not None
        assert invoice.ledger_entry.id == 99

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/supplier_invoices/42").mock(
            return_value=httpx.Response(200, json=SUPPLIER_INVOICE)
        )
        invoice = SupplierInvoices(sync_client).get(42)
        assert invoice.invoice_number == "INV-0001"

    @respx.mock
    def test_update_sends_only_provided_fields(self, sync_client: SyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/supplier_invoices/42").mock(
            return_value=httpx.Response(200, json=SUPPLIER_INVOICE)
        )
        SupplierInvoices(sync_client).update(42, label="New label")
        assert json.loads(route.calls.last.request.content) == {"label": "New label"}

    @respx.mock
    def test_update_sends_money_as_string(self, sync_client: SyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/supplier_invoices/42").mock(
            return_value=httpx.Response(200, json=SUPPLIER_INVOICE)
        )
        SupplierInvoices(sync_client).update(42, currency_amount=Decimal("600.00"))
        assert json.loads(route.calls.last.request.content) == {"currency_amount": "600.00"}

    @respx.mock
    def test_import_from_file(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/supplier_invoices/import").mock(
            return_value=httpx.Response(201, json=SUPPLIER_INVOICE)
        )
        invoice = SupplierInvoices(sync_client).import_from_file(
            file_attachment_id=11,
            supplier_id=7,
            date="2026-01-05",
            deadline="2026-02-05",
            currency_amount_before_tax=Decimal("500.00"),
            currency_amount=Decimal("600.00"),
            currency_tax=Decimal("100.00"),
            invoice_lines=[{"currency_amount": "600.00", "vat_rate": "FR_200"}],
        )
        assert invoice.id == 42
        body = json.loads(route.calls.last.request.content)
        assert body["file_attachment_id"] == 11
        assert body["supplier_id"] == 7
        assert body["currency_amount_before_tax"] == "500.00"
        assert body["invoice_lines"] == [{"currency_amount": "600.00", "vat_rate": "FR_200"}]

    @respx.mock
    def test_import_e_invoice_uploads_multipart_with_options(
        self, sync_client: SyncAPIClient
    ) -> None:
        route = respx.post(f"{BASE_URL}/supplier_invoices/e_invoices/imports").mock(
            return_value=httpx.Response(201, json={"id": 1, "url": "https://files.example/e.pdf"})
        )
        result = SupplierInvoices(sync_client).import_e_invoice(
            file=b"%PDF-1.4 ...",
            filename="invoice.pdf",
            invoice_options={"supplier_id": 7},
        )
        assert result.id == 1
        request = route.calls.last.request
        assert b'name="file"' in request.content
        assert b'name="invoice_options"' in request.content
        assert b'"supplier_id": 7' in request.content

    @respx.mock
    def test_import_e_invoice_without_options(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/supplier_invoices/e_invoices/imports").mock(
            return_value=httpx.Response(201, json={"id": 1, "url": "https://files.example/e.pdf"})
        )
        result = SupplierInvoices(sync_client).import_e_invoice(
            file=b"%PDF-1.4 ...", filename="invoice.pdf"
        )
        assert result.id == 1
        assert b'name="invoice_options"' not in route.calls.last.request.content

    @respx.mock
    def test_validate_accounting(self, sync_client: SyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/supplier_invoices/42/validate_accounting").mock(
            return_value=httpx.Response(
                200, json={**SUPPLIER_INVOICE, "accounting_status": "complete"}
            )
        )
        invoice = SupplierInvoices(sync_client).validate_accounting(42)
        assert invoice.accounting_status == "complete"

    @respx.mock
    def test_update_payment_status(self, sync_client: SyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/supplier_invoices/42/payment_status").mock(
            return_value=httpx.Response(204)
        )
        result = SupplierInvoices(sync_client).update_payment_status(42, payment_status="paid")
        assert result is None
        assert json.loads(route.calls.last.request.content) == {"payment_status": "paid"}

    @respx.mock
    def test_update_e_invoice_status_dispute(self, sync_client: SyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/supplier_invoices/42/e_invoice_status").mock(
            return_value=httpx.Response(200, json=SUPPLIER_INVOICE)
        )
        invoice = SupplierInvoices(sync_client).update_e_invoice_status(
            42, status="disputed", reason="incorrect_vat_rate"
        )
        assert invoice.id == 42
        assert json.loads(route.calls.last.request.content) == {
            "status": "disputed",
            "reason": "incorrect_vat_rate",
        }

    @respx.mock
    def test_update_e_invoice_status_approve_has_no_reason(
        self, sync_client: SyncAPIClient
    ) -> None:
        route = respx.put(f"{BASE_URL}/supplier_invoices/42/e_invoice_status").mock(
            return_value=httpx.Response(200, json=SUPPLIER_INVOICE)
        )
        SupplierInvoices(sync_client).update_e_invoice_status(42, status="approved")
        assert json.loads(route.calls.last.request.content) == {"status": "approved"}

    @respx.mock
    def test_list_invoice_lines(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/supplier_invoices/42/invoice_lines").mock(
            return_value=httpx.Response(
                200, json={"items": [INVOICE_LINE], "has_more": False, "next_cursor": None}
            )
        )
        page = SupplierInvoices(sync_client).list_invoice_lines(42)
        line = page.items[0]
        assert line.id == 444
        assert line.amount == Decimal("50.4")

    @respx.mock
    def test_list_categories(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/supplier_invoices/42/categories").mock(
            return_value=httpx.Response(
                200, json={"items": [CATEGORY], "has_more": False, "next_cursor": None}
            )
        )
        page = SupplierInvoices(sync_client).list_categories(42)
        category = page.items[0]
        assert category.weight == Decimal("1")
        assert category.category_group is not None
        assert category.category_group.id == 229

    @respx.mock
    def test_categorize_sends_raw_array_body_and_parses_response(
        self, sync_client: SyncAPIClient
    ) -> None:
        route = respx.put(f"{BASE_URL}/supplier_invoices/42/categories").mock(
            return_value=httpx.Response(200, json=[CATEGORY])
        )
        result = SupplierInvoices(sync_client).categorize(
            42, categories=[{"id": 426, "weight": "1"}]
        )
        assert json.loads(route.calls.last.request.content) == [{"id": 426, "weight": "1"}]
        assert len(result) == 1
        assert result[0].id == 426
        assert result[0].weight == Decimal("1")

    @respx.mock
    def test_list_payments(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/supplier_invoices/42/payments").mock(
            return_value=httpx.Response(
                200, json={"items": [PAYMENT], "has_more": False, "next_cursor": None}
            )
        )
        page = SupplierInvoices(sync_client).list_payments(42)
        assert page.items[0].status == "matched"

    @respx.mock
    def test_list_matched_transactions(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/supplier_invoices/42/matched_transactions").mock(
            return_value=httpx.Response(
                200, json={"items": [MATCHED_TRANSACTION], "has_more": False, "next_cursor": None}
            )
        )
        page = SupplierInvoices(sync_client).list_matched_transactions(42)
        transaction = page.items[0]
        assert transaction.id == 88
        assert transaction.bank_account is not None
        assert transaction.bank_account.id == 2

    @respx.mock
    def test_match_transaction(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/supplier_invoices/42/matched_transactions").mock(
            return_value=httpx.Response(204)
        )
        result = SupplierInvoices(sync_client).match_transaction(42, transaction_id=88)
        assert result is None
        assert json.loads(route.calls.last.request.content) == {"transaction_id": 88}

    @respx.mock
    def test_unmatch_transaction(self, sync_client: SyncAPIClient) -> None:
        route = respx.delete(
            f"{BASE_URL}/supplier_invoices/42/matched_transactions/88"
        ).mock(return_value=httpx.Response(204))
        result = SupplierInvoices(sync_client).unmatch_transaction(42, 88)
        assert result is None
        assert route.calls.last.request.method == "DELETE"

    @respx.mock
    def test_link_purchase_requests(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/supplier_invoices/42/linked_purchase_requests").mock(
            return_value=httpx.Response(204)
        )
        result = SupplierInvoices(sync_client).link_purchase_requests(
            42, purchase_request_id=17
        )
        assert result is None
        assert json.loads(route.calls.last.request.content) == {"purchase_request_id": 17}


class TestAsyncSupplierInvoices:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/supplier_invoices").mock(
            return_value=httpx.Response(
                200, json={"items": [SUPPLIER_INVOICE], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncSupplierInvoices(async_client).list()
        assert page.items[0].id == 42

    @respx.mock
    async def test_get(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/supplier_invoices/42").mock(
            return_value=httpx.Response(200, json=SUPPLIER_INVOICE)
        )
        invoice = await AsyncSupplierInvoices(async_client).get(42)
        assert invoice.id == 42

    @respx.mock
    async def test_update(self, async_client: AsyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/supplier_invoices/42").mock(
            return_value=httpx.Response(200, json=SUPPLIER_INVOICE)
        )
        invoice = await AsyncSupplierInvoices(async_client).update(42, currency="USD")
        assert invoice.id == 42

    @respx.mock
    async def test_import_from_file(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/supplier_invoices/import").mock(
            return_value=httpx.Response(201, json=SUPPLIER_INVOICE)
        )
        invoice = await AsyncSupplierInvoices(async_client).import_from_file(
            file_attachment_id=11,
            supplier_id=7,
            date="2026-01-05",
            deadline="2026-02-05",
            currency_amount_before_tax="500.00",
            currency_amount="600.00",
            currency_tax="100.00",
            invoice_lines=[{"currency_amount": "600.00", "vat_rate": "FR_200"}],
        )
        assert invoice.id == 42

    @respx.mock
    async def test_import_e_invoice(self, async_client: AsyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/supplier_invoices/e_invoices/imports").mock(
            return_value=httpx.Response(201, json={"id": 1, "url": "https://files.example/e.pdf"})
        )
        result = await AsyncSupplierInvoices(async_client).import_e_invoice(
            file=b"%PDF-1.4 ...", filename="invoice.pdf"
        )
        assert result.id == 1
        assert b'name="file"' in route.calls.last.request.content

    @respx.mock
    async def test_validate_accounting(self, async_client: AsyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/supplier_invoices/42/validate_accounting").mock(
            return_value=httpx.Response(200, json=SUPPLIER_INVOICE)
        )
        invoice = await AsyncSupplierInvoices(async_client).validate_accounting(42)
        assert invoice.id == 42

    @respx.mock
    async def test_update_payment_status(self, async_client: AsyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/supplier_invoices/42/payment_status").mock(
            return_value=httpx.Response(204)
        )
        result = await AsyncSupplierInvoices(async_client).update_payment_status(
            42, payment_status="to_be_paid"
        )
        assert result is None

    @respx.mock
    async def test_update_e_invoice_status(self, async_client: AsyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/supplier_invoices/42/e_invoice_status").mock(
            return_value=httpx.Response(200, json=SUPPLIER_INVOICE)
        )
        invoice = await AsyncSupplierInvoices(async_client).update_e_invoice_status(
            42, status="approved"
        )
        assert invoice.id == 42

    @respx.mock
    async def test_list_invoice_lines(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/supplier_invoices/42/invoice_lines").mock(
            return_value=httpx.Response(
                200, json={"items": [INVOICE_LINE], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncSupplierInvoices(async_client).list_invoice_lines(42)
        assert page.items[0].id == 444

    @respx.mock
    async def test_list_categories(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/supplier_invoices/42/categories").mock(
            return_value=httpx.Response(
                200, json={"items": [CATEGORY], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncSupplierInvoices(async_client).list_categories(42)
        assert page.items[0].id == 426

    @respx.mock
    async def test_categorize(self, async_client: AsyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/supplier_invoices/42/categories").mock(
            return_value=httpx.Response(200, json=[CATEGORY])
        )
        result = await AsyncSupplierInvoices(async_client).categorize(
            42, categories=[{"id": 426, "weight": "1"}]
        )
        assert json.loads(route.calls.last.request.content) == [{"id": 426, "weight": "1"}]
        assert result[0].id == 426

    @respx.mock
    async def test_list_payments(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/supplier_invoices/42/payments").mock(
            return_value=httpx.Response(
                200, json={"items": [PAYMENT], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncSupplierInvoices(async_client).list_payments(42)
        assert page.items[0].id == 5

    @respx.mock
    async def test_list_matched_transactions(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/supplier_invoices/42/matched_transactions").mock(
            return_value=httpx.Response(
                200, json={"items": [MATCHED_TRANSACTION], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncSupplierInvoices(async_client).list_matched_transactions(42)
        assert page.items[0].id == 88

    @respx.mock
    async def test_match_transaction(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/supplier_invoices/42/matched_transactions").mock(
            return_value=httpx.Response(204)
        )
        result = await AsyncSupplierInvoices(async_client).match_transaction(
            42, transaction_id=88
        )
        assert result is None

    @respx.mock
    async def test_unmatch_transaction(self, async_client: AsyncAPIClient) -> None:
        respx.delete(f"{BASE_URL}/supplier_invoices/42/matched_transactions/88").mock(
            return_value=httpx.Response(204)
        )
        result = await AsyncSupplierInvoices(async_client).unmatch_transaction(42, 88)
        assert result is None

    @respx.mock
    async def test_link_purchase_requests(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/supplier_invoices/42/linked_purchase_requests").mock(
            return_value=httpx.Response(204)
        )
        result = await AsyncSupplierInvoices(async_client).link_purchase_requests(
            42, purchase_request_id=17
        )
        assert result is None
