from __future__ import annotations

from decimal import Decimal

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.commercial_documents import (
    AsyncCommercialDocuments,
    CommercialDocuments,
)

from ..conftest import BASE_URL

COMMERCIAL_DOCUMENT = {
    "id": 42,
    "label": "Proforma for Acme",
    "document_number": "P-0001",
    "document_type": "proforma",
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
    "discount": {"type": "absolute", "value": "10.00"},
    "public_file_url": "https://files.example/doc.pdf",
    "filename": "doc.pdf",
    "special_mention": None,
    "customer": {"id": 7, "url": "https://api.example/customers/7"},
    "invoice_line_sections": {
        "url": "https://api.example/commercial_documents/42/invoice_line_sections"
    },
    "invoice_lines": {"url": "https://api.example/commercial_documents/42/invoice_lines"},
    "quote": {"id": 12, "url": "https://api.example/quotes/12"},
    "pdf_invoice_free_text": "",
    "pdf_invoice_subject": "",
    "pdf_description": None,
    "commercial_document_template": {"id": 3},
    "appendices": {"url": "https://api.example/commercial_documents/42/appendices"},
    "external_reference": "EXT-1",
    "archived_at": None,
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}

APPENDIX = {
    "id": 5,
    "url": "https://files.example/appendix.pdf",
    "filename": "appendix.pdf",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-05T09:00:00Z",
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


class TestCommercialDocuments:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/commercial_documents").mock(
            return_value=httpx.Response(
                200,
                json={"items": [COMMERCIAL_DOCUMENT], "has_more": False, "next_cursor": None},
            )
        )
        page = CommercialDocuments(sync_client).list(limit=50, sort="-id")
        assert route.calls.last.request.url.params["limit"] == "50"
        doc = page.items[0]
        assert doc.id == 42
        assert doc.document_type == "proforma"
        assert doc.amount == Decimal("600.00")
        assert doc.quote is not None
        assert doc.quote.id == 12

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/commercial_documents/42").mock(
            return_value=httpx.Response(200, json=COMMERCIAL_DOCUMENT)
        )
        doc = CommercialDocuments(sync_client).get(42)
        assert doc.document_number == "P-0001"

    @respx.mock
    def test_list_appendices(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/commercial_documents/42/appendices").mock(
            return_value=httpx.Response(
                200, json={"items": [APPENDIX], "has_more": False, "next_cursor": None}
            )
        )
        page = CommercialDocuments(sync_client).list_appendices(42)
        assert page.items[0].filename == "appendix.pdf"

    @respx.mock
    def test_add_appendix_uploads_multipart(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/commercial_documents/42/appendices").mock(
            return_value=httpx.Response(201, json=APPENDIX)
        )
        appendix = CommercialDocuments(sync_client).add_appendix(
            42, file=b"%PDF-1.4 ...", filename="appendix.pdf"
        )
        assert appendix.id == 5
        assert b"appendix.pdf" in route.calls.last.request.content

    @respx.mock
    def test_list_invoice_lines(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/commercial_documents/42/invoice_lines").mock(
            return_value=httpx.Response(
                200, json={"items": [INVOICE_LINE], "has_more": False, "next_cursor": None}
            )
        )
        page = CommercialDocuments(sync_client).list_invoice_lines(42)
        line = page.items[0]
        assert line.id == 444
        assert line.quantity == Decimal("12")

    @respx.mock
    def test_list_invoice_line_sections(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/commercial_documents/42/invoice_line_sections").mock(
            return_value=httpx.Response(
                200,
                json={"items": [INVOICE_LINE_SECTION], "has_more": False, "next_cursor": None},
            )
        )
        page = CommercialDocuments(sync_client).list_invoice_line_sections(42)
        assert page.items[0].title == "Section 1"


class TestAsyncCommercialDocuments:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/commercial_documents").mock(
            return_value=httpx.Response(
                200,
                json={"items": [COMMERCIAL_DOCUMENT], "has_more": False, "next_cursor": None},
            )
        )
        page = await AsyncCommercialDocuments(async_client).list()
        assert page.items[0].id == 42

    @respx.mock
    async def test_get(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/commercial_documents/42").mock(
            return_value=httpx.Response(200, json=COMMERCIAL_DOCUMENT)
        )
        doc = await AsyncCommercialDocuments(async_client).get(42)
        assert doc.id == 42

    @respx.mock
    async def test_list_appendices(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/commercial_documents/42/appendices").mock(
            return_value=httpx.Response(
                200, json={"items": [APPENDIX], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncCommercialDocuments(async_client).list_appendices(42)
        assert page.items[0].id == 5

    @respx.mock
    async def test_add_appendix(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/commercial_documents/42/appendices").mock(
            return_value=httpx.Response(201, json=APPENDIX)
        )
        appendix = await AsyncCommercialDocuments(async_client).add_appendix(
            42, file=b"%PDF", filename="a.pdf"
        )
        assert appendix.filename == "appendix.pdf"

    @respx.mock
    async def test_list_invoice_lines(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/commercial_documents/42/invoice_lines").mock(
            return_value=httpx.Response(
                200, json={"items": [INVOICE_LINE], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncCommercialDocuments(async_client).list_invoice_lines(42)
        assert page.items[0].id == 444

    @respx.mock
    async def test_list_invoice_line_sections(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/commercial_documents/42/invoice_line_sections").mock(
            return_value=httpx.Response(
                200,
                json={"items": [INVOICE_LINE_SECTION], "has_more": False, "next_cursor": None},
            )
        )
        page = await AsyncCommercialDocuments(async_client).list_invoice_line_sections(42)
        assert page.items[0].id == 9
