from __future__ import annotations

import json
from decimal import Decimal

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.customer_invoices import (
    AsyncCustomerInvoices,
    CustomerInvoices,
)

from ..conftest import BASE_URL

CUSTOMER_INVOICE = {
    "id": 42,
    "label": None,
    "invoice_number": "F-0001",
    "currency": "EUR",
    "amount": "600.00",
    "currency_amount": "600.00",
    "currency_amount_before_tax": "500.00",
    "exchange_rate": "1.0",
    "date": "2026-01-05",
    "deadline": "2026-02-05",
    "currency_tax": "100.00",
    "tax": "100.00",
    "language": "fr_FR",
    "paid": False,
    "status": "upcoming",
    "discount": {"type": "absolute", "value": "10.00"},
    "ledger_entry": {"id": 99},
    "public_file_url": "https://files.example/invoice.pdf",
    "filename": "invoice.pdf",
    "remaining_amount_with_tax": "600.00",
    "remaining_amount_without_tax": "500.00",
    "draft": False,
    "special_mention": None,
    "customer": {"id": 7, "url": "https://api.example/customers/7"},
    "invoice_line_sections": {
        "url": "https://api.example/customer_invoices/42/invoice_line_sections"
    },
    "invoice_lines": {"url": "https://api.example/customer_invoices/42/invoice_lines"},
    "custom_header_fields": {
        "url": "https://api.example/customer_invoices/42/custom_header_fields"
    },
    "categories": {"url": "https://api.example/customer_invoices/42/categories"},
    "pdf_invoice_free_text": "",
    "pdf_invoice_subject": "",
    "pdf_description": None,
    "billing_subscription": None,
    "credited_invoice": None,
    "customer_invoice_template": {"id": 3},
    "transaction_reference": None,
    "payments": {"url": "https://api.example/customer_invoices/42/payments"},
    "matched_transactions": {
        "url": "https://api.example/customer_invoices/42/matched_transactions"
    },
    "appendices": {"url": "https://api.example/customer_invoices/42/appendices"},
    "quote": None,
    "external_reference": "EXT-1",
    "e_invoicing": None,
    "factur_x": False,
    "archived_at": None,
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}

INVOICE_LINE = {
    "id": 444,
    "label": "Consulting fees",
    "unit": "piece",
    "quantity": "12",
    "amount": "50.4",
    "currency_amount": "50.4",
    "description": "Lorem ipsum",
    "product": {"id": 3049, "url": "https://api.example/products/3049"},
    "vat_rate": "FR_200",
    "currency_amount_before_tax": "42.0",
    "currency_tax": "8.4",
    "tax": "8.4",
    "raw_currency_unit_price": "4.2",
    "discount": {"type": "relative", "value": "0"},
    "section_rank": None,
    "imputation_dates": None,
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-05T09:00:00Z",
}

INVOICE_LINE_SECTION = {
    "id": 9,
    "title": "Section 1",
    "description": "First section",
    "rank": 1,
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
    "customer": {"id": 7, "url": "https://api.example/customers/7"},
    "categories": [],
}

APPENDIX = {
    "id": 5,
    "url": "https://files.example/appendix.pdf",
    "filename": "appendix.pdf",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-05T09:00:00Z",
}

CATEGORY = {
    "id": 426,
    "label": "HR - Salaries",
    "weight": "1",
    "category_group": {"id": 229},
    "analytical_code": "CODE123",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-05T09:00:00Z",
}

CUSTOM_HEADER_FIELD = {
    "id": 3,
    "title": "PO number",
    "value": "PO-123",
    "rank": 1,
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-05T09:00:00Z",
}


class TestCustomerInvoices:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/customer_invoices").mock(
            return_value=httpx.Response(
                200, json={"items": [CUSTOMER_INVOICE], "has_more": False, "next_cursor": None}
            )
        )
        page = CustomerInvoices(sync_client).list(limit=50, sort="-id", include="invoice_lines")
        assert route.calls.last.request.url.params["limit"] == "50"
        assert route.calls.last.request.url.params["include"] == "invoice_lines"
        invoice = page.items[0]
        assert invoice.id == 42
        assert invoice.amount == Decimal("600.00")
        assert invoice.discount is not None
        assert invoice.discount.value == Decimal("10.00")
        assert invoice.customer is not None
        assert invoice.customer.id == 7
        assert invoice.customer_invoice_template is not None
        assert invoice.customer_invoice_template.id == 3

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/customer_invoices/42").mock(
            return_value=httpx.Response(200, json=CUSTOMER_INVOICE)
        )
        invoice = CustomerInvoices(sync_client).get(42)
        assert invoice.invoice_number == "F-0001"

    @respx.mock
    def test_create_draft_drops_none_and_sends_lines(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/customer_invoices").mock(
            return_value=httpx.Response(201, json=CUSTOMER_INVOICE)
        )
        CustomerInvoices(sync_client).create(
            date="2026-01-05",
            deadline="2026-02-05",
            customer_id=7,
            invoice_lines=[{"product_id": 3049, "quantity": 2}],
        )
        body = json.loads(route.calls.last.request.content)
        assert body == {
            "date": "2026-01-05",
            "deadline": "2026-02-05",
            "customer_id": 7,
            "draft": True,
            "invoice_lines": [{"product_id": 3049, "quantity": 2}],
        }

    @respx.mock
    def test_create_finalized_with_transaction_reference(
        self, sync_client: SyncAPIClient
    ) -> None:
        route = respx.post(f"{BASE_URL}/customer_invoices").mock(
            return_value=httpx.Response(201, json=CUSTOMER_INVOICE)
        )
        CustomerInvoices(sync_client).create(
            date="2026-01-05",
            deadline="2026-02-05",
            customer_id=7,
            draft=False,
            invoice_lines=[{"product_id": 3049, "quantity": 2}],
            transaction_reference={
                "banking_provider": "stripe",
                "provider_field_name": "payment_id",
                "provider_field_value": "pi_123",
            },
        )
        body = json.loads(route.calls.last.request.content)
        assert body["draft"] is False
        assert body["transaction_reference"]["banking_provider"] == "stripe"

    @respx.mock
    def test_update_sends_only_provided_fields(self, sync_client: SyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/customer_invoices/42").mock(
            return_value=httpx.Response(200, json=CUSTOMER_INVOICE)
        )
        CustomerInvoices(sync_client).update(42, special_mention="Thanks!")
        assert json.loads(route.calls.last.request.content) == {"special_mention": "Thanks!"}

    @respx.mock
    def test_delete(self, sync_client: SyncAPIClient) -> None:
        route = respx.delete(f"{BASE_URL}/customer_invoices/42").mock(
            return_value=httpx.Response(204)
        )
        result = CustomerInvoices(sync_client).delete(42)
        assert result is None
        assert route.calls.last.request.method == "DELETE"

    @respx.mock
    def test_finalize(self, sync_client: SyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/customer_invoices/42/finalize").mock(
            return_value=httpx.Response(200, json={**CUSTOMER_INVOICE, "draft": False})
        )
        invoice = CustomerInvoices(sync_client).finalize(42)
        assert invoice.draft is False

    @respx.mock
    def test_mark_as_paid(self, sync_client: SyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/customer_invoices/42/mark_as_paid").mock(
            return_value=httpx.Response(204)
        )
        result = CustomerInvoices(sync_client).mark_as_paid(42)
        assert result is None

    @respx.mock
    def test_send_by_email(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/customer_invoices/42/send_by_email").mock(
            return_value=httpx.Response(204)
        )
        result = CustomerInvoices(sync_client).send_by_email(42, recipients=["a@example.com"])
        assert result is None
        assert json.loads(route.calls.last.request.content) == {
            "recipients": ["a@example.com"]
        }

    @respx.mock
    def test_send_to_pa(self, sync_client: SyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/customer_invoices/42/send_to_pa").mock(
            return_value=httpx.Response(204)
        )
        result = CustomerInvoices(sync_client).send_to_pa(42)
        assert result is None

    @respx.mock
    def test_link_credit_note(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/customer_invoices/42/link_credit_note").mock(
            return_value=httpx.Response(200, json=CUSTOMER_INVOICE)
        )
        invoice = CustomerInvoices(sync_client).link_credit_note(42, credit_note_id=99)
        assert invoice.id == 42
        assert json.loads(route.calls.last.request.content) == {"credit_note_id": 99}

    @respx.mock
    def test_update_imported(self, sync_client: SyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/customer_invoices/42/update_imported").mock(
            return_value=httpx.Response(200, json=CUSTOMER_INVOICE)
        )
        CustomerInvoices(sync_client).update_imported(
            42, currency_amount=Decimal("600.00"), invoice_number="F-0002"
        )
        body = json.loads(route.calls.last.request.content)
        assert body == {"currency_amount": "600.00", "invoice_number": "F-0002"}

    @respx.mock
    def test_import_from_file(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/customer_invoices/import").mock(
            return_value=httpx.Response(201, json=CUSTOMER_INVOICE)
        )
        CustomerInvoices(sync_client).import_from_file(
            file_attachment_id=11,
            date="2026-01-05",
            deadline="2026-02-05",
            customer_id=7,
            currency_amount_before_tax=Decimal("500.00"),
            currency_amount=Decimal("600.00"),
            currency_tax=Decimal("100.00"),
            invoice_lines=[{"quantity": 1, "raw_currency_unit_price": "500.00"}],
        )
        body = json.loads(route.calls.last.request.content)
        assert body["file_attachment_id"] == 11
        assert body["currency_amount_before_tax"] == "500.00"
        assert body["invoice_lines"] == [{"quantity": 1, "raw_currency_unit_price": "500.00"}]

    @respx.mock
    def test_import_e_invoice_uploads_multipart_with_options(
        self, sync_client: SyncAPIClient
    ) -> None:
        route = respx.post(f"{BASE_URL}/customer_invoices/e_invoices/imports").mock(
            return_value=httpx.Response(201, json={"id": 1, "url": "https://files.example/e.pdf"})
        )
        result = CustomerInvoices(sync_client).import_e_invoice(
            file=b"%PDF-1.4 ...",
            filename="invoice.pdf",
            invoice_options={"customer_id": 7},
        )
        assert result.id == 1
        request = route.calls.last.request
        assert b'name="file"' in request.content
        assert b'name="invoice_options"' in request.content
        assert b'"customer_id": 7' in request.content

    @respx.mock
    def test_create_from_quote(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/customer_invoices/create_from_quote").mock(
            return_value=httpx.Response(201, json=CUSTOMER_INVOICE)
        )
        invoice = CustomerInvoices(sync_client).create_from_quote(quote_id=17, draft=True)
        assert invoice.id == 42
        assert json.loads(route.calls.last.request.content) == {
            "quote_id": 17,
            "draft": True,
        }

    @respx.mock
    def test_list_invoice_lines(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/customer_invoices/42/invoice_lines").mock(
            return_value=httpx.Response(
                200, json={"items": [INVOICE_LINE], "has_more": False, "next_cursor": None}
            )
        )
        page = CustomerInvoices(sync_client).list_invoice_lines(42)
        line = page.items[0]
        assert line.id == 444
        assert line.quantity == Decimal("12")
        assert line.product is not None
        assert line.product.id == 3049

    @respx.mock
    def test_list_invoice_line_sections(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/customer_invoices/42/invoice_line_sections").mock(
            return_value=httpx.Response(
                200,
                json={"items": [INVOICE_LINE_SECTION], "has_more": False, "next_cursor": None},
            )
        )
        page = CustomerInvoices(sync_client).list_invoice_line_sections(42)
        assert page.items[0].title == "Section 1"

    @respx.mock
    def test_list_payments(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/customer_invoices/42/payments").mock(
            return_value=httpx.Response(
                200, json={"items": [PAYMENT], "has_more": False, "next_cursor": None}
            )
        )
        page = CustomerInvoices(sync_client).list_payments(42)
        assert page.items[0].status == "matched"

    @respx.mock
    def test_list_matched_transactions(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/customer_invoices/42/matched_transactions").mock(
            return_value=httpx.Response(
                200,
                json={"items": [MATCHED_TRANSACTION], "has_more": False, "next_cursor": None},
            )
        )
        page = CustomerInvoices(sync_client).list_matched_transactions(42)
        transaction = page.items[0]
        assert transaction.id == 88
        assert transaction.bank_account is not None
        assert transaction.bank_account.id == 2

    @respx.mock
    def test_match_transaction(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/customer_invoices/42/matched_transactions").mock(
            return_value=httpx.Response(204)
        )
        result = CustomerInvoices(sync_client).match_transaction(42, transaction_id=88)
        assert result is None
        assert json.loads(route.calls.last.request.content) == {"transaction_id": 88}

    @respx.mock
    def test_unmatch_transaction(self, sync_client: SyncAPIClient) -> None:
        route = respx.delete(
            f"{BASE_URL}/customer_invoices/42/matched_transactions/88"
        ).mock(return_value=httpx.Response(204))
        result = CustomerInvoices(sync_client).unmatch_transaction(42, 88)
        assert result is None
        assert route.calls.last.request.method == "DELETE"

    @respx.mock
    def test_list_appendices(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/customer_invoices/42/appendices").mock(
            return_value=httpx.Response(
                200, json={"items": [APPENDIX], "has_more": False, "next_cursor": None}
            )
        )
        page = CustomerInvoices(sync_client).list_appendices(42)
        assert page.items[0].filename == "appendix.pdf"

    @respx.mock
    def test_add_appendix_uploads_multipart(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/customer_invoices/42/appendices").mock(
            return_value=httpx.Response(201, json=APPENDIX)
        )
        appendix = CustomerInvoices(sync_client).add_appendix(
            42, file=b"%PDF-1.4 ...", filename="appendix.pdf"
        )
        assert appendix.id == 5
        assert b"appendix.pdf" in route.calls.last.request.content

    @respx.mock
    def test_list_categories(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/customer_invoices/42/categories").mock(
            return_value=httpx.Response(
                200, json={"items": [CATEGORY], "has_more": False, "next_cursor": None}
            )
        )
        page = CustomerInvoices(sync_client).list_categories(42)
        category = page.items[0]
        assert category.weight == Decimal("1")
        assert category.category_group is not None
        assert category.category_group.id == 229

    @respx.mock
    def test_categorize_sends_raw_array_body(self, sync_client: SyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/customer_invoices/42/categories").mock(
            return_value=httpx.Response(200, json=[])
        )
        result = CustomerInvoices(sync_client).categorize(
            42, categories=[{"id": 426, "weight": "1"}]
        )
        assert result is None
        assert json.loads(route.calls.last.request.content) == [{"id": 426, "weight": "1"}]

    @respx.mock
    def test_list_custom_header_fields(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/customer_invoices/42/custom_header_fields").mock(
            return_value=httpx.Response(
                200,
                json={"items": [CUSTOM_HEADER_FIELD], "has_more": False, "next_cursor": None},
            )
        )
        page = CustomerInvoices(sync_client).list_custom_header_fields(42)
        assert page.items[0].title == "PO number"


class TestAsyncCustomerInvoices:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/customer_invoices").mock(
            return_value=httpx.Response(
                200, json={"items": [CUSTOMER_INVOICE], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncCustomerInvoices(async_client).list()
        assert page.items[0].id == 42

    @respx.mock
    async def test_create(self, async_client: AsyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/customer_invoices").mock(
            return_value=httpx.Response(201, json=CUSTOMER_INVOICE)
        )
        invoice = await AsyncCustomerInvoices(async_client).create(
            date="2026-01-05",
            deadline="2026-02-05",
            customer_id=7,
            invoice_lines=[{"product_id": 3049, "quantity": 2}],
        )
        assert invoice.id == 42
        body = json.loads(route.calls.last.request.content)
        assert body["customer_id"] == 7
        assert body["draft"] is True

    @respx.mock
    async def test_get(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/customer_invoices/42").mock(
            return_value=httpx.Response(200, json=CUSTOMER_INVOICE)
        )
        invoice = await AsyncCustomerInvoices(async_client).get(42)
        assert invoice.id == 42

    @respx.mock
    async def test_update(self, async_client: AsyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/customer_invoices/42").mock(
            return_value=httpx.Response(200, json=CUSTOMER_INVOICE)
        )
        invoice = await AsyncCustomerInvoices(async_client).update(42, currency="USD")
        assert invoice.id == 42

    @respx.mock
    async def test_delete(self, async_client: AsyncAPIClient) -> None:
        respx.delete(f"{BASE_URL}/customer_invoices/42").mock(
            return_value=httpx.Response(204)
        )
        result = await AsyncCustomerInvoices(async_client).delete(42)
        assert result is None

    @respx.mock
    async def test_finalize(self, async_client: AsyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/customer_invoices/42/finalize").mock(
            return_value=httpx.Response(200, json={**CUSTOMER_INVOICE, "draft": False})
        )
        invoice = await AsyncCustomerInvoices(async_client).finalize(42)
        assert invoice.draft is False

    @respx.mock
    async def test_mark_as_paid(self, async_client: AsyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/customer_invoices/42/mark_as_paid").mock(
            return_value=httpx.Response(204)
        )
        result = await AsyncCustomerInvoices(async_client).mark_as_paid(42)
        assert result is None

    @respx.mock
    async def test_send_by_email(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/customer_invoices/42/send_by_email").mock(
            return_value=httpx.Response(204)
        )
        result = await AsyncCustomerInvoices(async_client).send_by_email(42)
        assert result is None

    @respx.mock
    async def test_send_to_pa(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/customer_invoices/42/send_to_pa").mock(
            return_value=httpx.Response(204)
        )
        result = await AsyncCustomerInvoices(async_client).send_to_pa(42)
        assert result is None

    @respx.mock
    async def test_link_credit_note(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/customer_invoices/42/link_credit_note").mock(
            return_value=httpx.Response(200, json=CUSTOMER_INVOICE)
        )
        invoice = await AsyncCustomerInvoices(async_client).link_credit_note(
            42, credit_note_id=99
        )
        assert invoice.id == 42

    @respx.mock
    async def test_update_imported(self, async_client: AsyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/customer_invoices/42/update_imported").mock(
            return_value=httpx.Response(200, json=CUSTOMER_INVOICE)
        )
        invoice = await AsyncCustomerInvoices(async_client).update_imported(
            42, invoice_number="F-0003"
        )
        assert invoice.id == 42

    @respx.mock
    async def test_import_from_file(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/customer_invoices/import").mock(
            return_value=httpx.Response(201, json=CUSTOMER_INVOICE)
        )
        invoice = await AsyncCustomerInvoices(async_client).import_from_file(
            file_attachment_id=11,
            date="2026-01-05",
            deadline="2026-02-05",
            customer_id=7,
            currency_amount_before_tax="500.00",
            currency_amount="600.00",
            currency_tax="100.00",
            invoice_lines=[{"quantity": 1, "raw_currency_unit_price": "500.00"}],
        )
        assert invoice.id == 42

    @respx.mock
    async def test_import_e_invoice(self, async_client: AsyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/customer_invoices/e_invoices/imports").mock(
            return_value=httpx.Response(201, json={"id": 1, "url": "https://files.example/e.pdf"})
        )
        result = await AsyncCustomerInvoices(async_client).import_e_invoice(
            file=b"%PDF-1.4 ...", filename="invoice.pdf"
        )
        assert result.id == 1
        assert b'name="file"' in route.calls.last.request.content

    @respx.mock
    async def test_create_from_quote(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/customer_invoices/create_from_quote").mock(
            return_value=httpx.Response(201, json=CUSTOMER_INVOICE)
        )
        invoice = await AsyncCustomerInvoices(async_client).create_from_quote(
            quote_id=17, draft=False
        )
        assert invoice.id == 42

    @respx.mock
    async def test_list_invoice_lines(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/customer_invoices/42/invoice_lines").mock(
            return_value=httpx.Response(
                200, json={"items": [INVOICE_LINE], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncCustomerInvoices(async_client).list_invoice_lines(42)
        assert page.items[0].id == 444

    @respx.mock
    async def test_list_invoice_line_sections(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/customer_invoices/42/invoice_line_sections").mock(
            return_value=httpx.Response(
                200,
                json={"items": [INVOICE_LINE_SECTION], "has_more": False, "next_cursor": None},
            )
        )
        page = await AsyncCustomerInvoices(async_client).list_invoice_line_sections(42)
        assert page.items[0].id == 9

    @respx.mock
    async def test_list_payments(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/customer_invoices/42/payments").mock(
            return_value=httpx.Response(
                200, json={"items": [PAYMENT], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncCustomerInvoices(async_client).list_payments(42)
        assert page.items[0].id == 5

    @respx.mock
    async def test_list_matched_transactions(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/customer_invoices/42/matched_transactions").mock(
            return_value=httpx.Response(
                200,
                json={"items": [MATCHED_TRANSACTION], "has_more": False, "next_cursor": None},
            )
        )
        page = await AsyncCustomerInvoices(async_client).list_matched_transactions(42)
        assert page.items[0].id == 88

    @respx.mock
    async def test_match_transaction(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/customer_invoices/42/matched_transactions").mock(
            return_value=httpx.Response(204)
        )
        result = await AsyncCustomerInvoices(async_client).match_transaction(
            42, transaction_id=88
        )
        assert result is None

    @respx.mock
    async def test_unmatch_transaction(self, async_client: AsyncAPIClient) -> None:
        respx.delete(f"{BASE_URL}/customer_invoices/42/matched_transactions/88").mock(
            return_value=httpx.Response(204)
        )
        result = await AsyncCustomerInvoices(async_client).unmatch_transaction(42, 88)
        assert result is None

    @respx.mock
    async def test_list_appendices(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/customer_invoices/42/appendices").mock(
            return_value=httpx.Response(
                200, json={"items": [APPENDIX], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncCustomerInvoices(async_client).list_appendices(42)
        assert page.items[0].id == 5

    @respx.mock
    async def test_add_appendix(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/customer_invoices/42/appendices").mock(
            return_value=httpx.Response(201, json=APPENDIX)
        )
        appendix = await AsyncCustomerInvoices(async_client).add_appendix(
            42, file=b"%PDF", filename="a.pdf"
        )
        assert appendix.filename == "appendix.pdf"

    @respx.mock
    async def test_list_categories(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/customer_invoices/42/categories").mock(
            return_value=httpx.Response(
                200, json={"items": [CATEGORY], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncCustomerInvoices(async_client).list_categories(42)
        assert page.items[0].id == 426

    @respx.mock
    async def test_categorize(self, async_client: AsyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/customer_invoices/42/categories").mock(
            return_value=httpx.Response(200, json=[])
        )
        result = await AsyncCustomerInvoices(async_client).categorize(
            42, categories=[{"id": 426, "weight": "1"}]
        )
        assert result is None
        assert json.loads(route.calls.last.request.content) == [{"id": 426, "weight": "1"}]

    @respx.mock
    async def test_list_custom_header_fields(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/customer_invoices/42/custom_header_fields").mock(
            return_value=httpx.Response(
                200,
                json={"items": [CUSTOM_HEADER_FIELD], "has_more": False, "next_cursor": None},
            )
        )
        page = await AsyncCustomerInvoices(async_client).list_custom_header_fields(42)
        assert page.items[0].id == 3
