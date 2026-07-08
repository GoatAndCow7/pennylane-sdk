from __future__ import annotations

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.firm.invoicing import (
    AsyncFirmCustomerInvoices,
    AsyncFirmCustomers,
    AsyncFirmSupplierInvoices,
    AsyncFirmSuppliers,
    FirmCustomerInvoices,
    FirmCustomers,
    FirmSupplierInvoices,
    FirmSuppliers,
)

FIRM_BASE_URL = "https://app.pennylane.com/api/external/firm/v1"

CUSTOMER_INVOICE = {
    "id": 100,
    "label": "Invoice 100",
    "invoice_number": "INV-100",
    "currency": "EUR",
    "amount": "120.00",
    "currency_amount": "120.00",
    "currency_amount_before_tax": "100.00",
    "exchange_rate": "1.0",
    "date": "2026-01-05",
    "deadline": "2026-02-05",
    "currency_tax": "20.00",
    "tax": "20.00",
    "language": "fr_FR",
    "paid": False,
    "status": "incomplete",
    "discount": {"type": "relative", "value": "0"},
    "ledger_entry": {"id": 5},
    "public_file_url": None,
    "filename": None,
    "remaining_amount_with_tax": "120.00",
    "remaining_amount_without_tax": "100.00",
    "draft": False,
    "special_mention": None,
    "customer": {"id": 9, "url": "https://x/customers/9"},
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}

SUPPLIER_INVOICE = {
    "id": 200,
    "label": "Invoice 200",
    "invoice_number": "SUP-200",
    "currency": "EUR",
    "amount": "60.00",
    "currency_amount": "60.00",
    "currency_amount_before_tax": "50.00",
    "exchange_rate": "1.0",
    "date": "2026-01-05",
    "deadline": "2026-02-05",
    "currency_tax": "10.00",
    "tax": "10.00",
    "reconciled": False,
    "accounting_status": "draft",
    "filename": None,
    "public_file_url": None,
    "remaining_amount_with_tax": "60.00",
    "remaining_amount_without_tax": "50.00",
    "ledger_entry": {"id": 6},
    "supplier": {"id": 11, "url": "https://x/suppliers/11"},
    "payment_status": "to_be_processed",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}

CUSTOMER = {
    "id": 9,
    "name": "Acme Corp",
    "billing_iban": None,
    "payment_conditions": "30_days",
    "recipient": "John Doe",
    "phone": "+33612345678",
    "reference": "REF-1",
    "notes": None,
    "vat_number": "FR12345678901",
    "reg_no": "123456789",
    "ledger_account": {"id": 3},
    "emails": ["billing@acme.test"],
    "billing_address": None,
    "delivery_address": None,
    "customer_type": "company",
    "external_reference": None,
    "billing_language": "fr_FR",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}

SUPPLIER = {
    "id": 11,
    "name": "Best Supplier",
    "establishment_no": None,
    "reg_no": None,
    "vat_number": "FR98765432109",
    "ledger_account": {"id": 4},
    "emails": ["contact@supplier.test"],
    "iban": None,
    "postal_address": None,
    "supplier_payment_method": None,
    "supplier_due_date_delay": None,
    "supplier_due_date_rule": None,
    "external_reference": None,
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}


def sync_client() -> SyncAPIClient:
    return SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)


def async_client() -> AsyncAPIClient:
    return AsyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)


class TestFirmCustomerInvoices:
    @respx.mock
    def test_list(self) -> None:
        route = respx.get(f"{FIRM_BASE_URL}/companies/1/customer_invoices").mock(
            return_value=httpx.Response(
                200, json={"items": [CUSTOMER_INVOICE], "has_more": False, "next_cursor": None}
            )
        )
        page = FirmCustomerInvoices(sync_client()).list(1, limit=50)
        assert route.calls.last.request.url.params["limit"] == "50"
        assert page.items[0].id == 100

    @respx.mock
    def test_get(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/1/customer_invoices/100").mock(
            return_value=httpx.Response(200, json=CUSTOMER_INVOICE)
        )
        invoice = FirmCustomerInvoices(sync_client()).get(1, 100)
        assert invoice.invoice_number == "INV-100"


class TestFirmSupplierInvoices:
    @respx.mock
    def test_list(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/1/supplier_invoices").mock(
            return_value=httpx.Response(
                200, json={"items": [SUPPLIER_INVOICE], "has_more": False, "next_cursor": None}
            )
        )
        page = FirmSupplierInvoices(sync_client()).list(1)
        assert page.items[0].id == 200

    @respx.mock
    def test_get(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/1/supplier_invoices/200").mock(
            return_value=httpx.Response(200, json=SUPPLIER_INVOICE)
        )
        invoice = FirmSupplierInvoices(sync_client()).get(1, 200)
        assert invoice.invoice_number == "SUP-200"


class TestFirmCustomers:
    @respx.mock
    def test_list(self) -> None:
        route = respx.get(f"{FIRM_BASE_URL}/companies/1/customers").mock(
            return_value=httpx.Response(
                200, json={"items": [CUSTOMER], "has_more": False, "next_cursor": None}
            )
        )
        page = FirmCustomers(sync_client()).list(1, sort="-id")
        assert route.calls.last.request.url.params["sort"] == "-id"
        assert page.items[0].name == "Acme Corp"


class TestFirmSuppliers:
    @respx.mock
    def test_list(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/1/suppliers").mock(
            return_value=httpx.Response(
                200, json={"items": [SUPPLIER], "has_more": False, "next_cursor": None}
            )
        )
        page = FirmSuppliers(sync_client()).list(1)
        assert page.items[0].name == "Best Supplier"


class TestAsyncFirmCustomerInvoices:
    @respx.mock
    async def test_list(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/1/customer_invoices").mock(
            return_value=httpx.Response(
                200, json={"items": [CUSTOMER_INVOICE], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncFirmCustomerInvoices(async_client()).list(1)
        assert page.items[0].id == 100

    @respx.mock
    async def test_get(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/1/customer_invoices/100").mock(
            return_value=httpx.Response(200, json=CUSTOMER_INVOICE)
        )
        invoice = await AsyncFirmCustomerInvoices(async_client()).get(1, 100)
        assert invoice.id == 100


class TestAsyncFirmSupplierInvoices:
    @respx.mock
    async def test_list(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/1/supplier_invoices").mock(
            return_value=httpx.Response(
                200, json={"items": [SUPPLIER_INVOICE], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncFirmSupplierInvoices(async_client()).list(1)
        assert page.items[0].id == 200

    @respx.mock
    async def test_get(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/1/supplier_invoices/200").mock(
            return_value=httpx.Response(200, json=SUPPLIER_INVOICE)
        )
        invoice = await AsyncFirmSupplierInvoices(async_client()).get(1, 200)
        assert invoice.id == 200


class TestAsyncFirmCustomers:
    @respx.mock
    async def test_list(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/1/customers").mock(
            return_value=httpx.Response(
                200, json={"items": [CUSTOMER], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncFirmCustomers(async_client()).list(1)
        assert page.items[0].id == 9


class TestAsyncFirmSuppliers:
    @respx.mock
    async def test_list(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/1/suppliers").mock(
            return_value=httpx.Response(
                200, json={"items": [SUPPLIER], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncFirmSuppliers(async_client()).list(1)
        assert page.items[0].id == 11
