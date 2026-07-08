from __future__ import annotations

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.e_invoices import (
    AsyncEInvoices,
    AsyncPaRegistrations,
    EInvoices,
    PaRegistrations,
)

from ..conftest import BASE_URL

E_INVOICE_IMPORT = {
    "id": 1,
    "url": "https://app.pennylane.com/e_invoices/1",
}

PA_REGISTRATION = {
    "id": 1,
    "siret": None,
    "siren": "123456789",
    "status": "activated",
    "exchange_direction": "emission_and_reception",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}


class TestEInvoices:
    @respx.mock
    def test_import_e_invoice(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/e-invoices/imports").mock(
            return_value=httpx.Response(201, json=E_INVOICE_IMPORT)
        )
        result = EInvoices(sync_client).import_e_invoice(
            file=b"<xml/>", type="customer", filename="invoice.xml"
        )
        request = route.calls.last.request
        assert b'name="type"' in request.content
        assert b"customer" in request.content
        assert b'filename="invoice.xml"' in request.content
        assert result.id == 1
        assert result.url == "https://app.pennylane.com/e_invoices/1"


class TestPaRegistrations:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/pa_registrations").mock(
            return_value=httpx.Response(
                200, json={"items": [PA_REGISTRATION], "has_more": False, "next_cursor": None}
            )
        )
        page = PaRegistrations(sync_client).list()
        registration = page.items[0]
        assert registration.id == 1
        assert registration.siren == "123456789"
        assert registration.status == "activated"


class TestAsyncEInvoices:
    @respx.mock
    async def test_import_e_invoice(self, async_client: AsyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/e-invoices/imports").mock(
            return_value=httpx.Response(201, json=E_INVOICE_IMPORT)
        )
        result = await AsyncEInvoices(async_client).import_e_invoice(
            file=b"<xml/>", type="supplier", filename="invoice.xml"
        )
        request = route.calls.last.request
        assert b"supplier" in request.content
        assert result.id == 1


class TestAsyncPaRegistrations:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/pa_registrations").mock(
            return_value=httpx.Response(
                200, json={"items": [PA_REGISTRATION], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncPaRegistrations(async_client).list()
        assert page.items[0].id == 1
