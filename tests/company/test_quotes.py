from __future__ import annotations

import json
from decimal import Decimal

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.quotes import AsyncQuotes, Quotes

from ..conftest import BASE_URL

QUOTE = {
    "id": 42,
    "label": "Quote for Acme",
    "quote_number": "Q-0001",
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
    "status": "pending",
    "discount": {"type": "absolute", "value": "10.00"},
    "public_file_url": "https://files.example/quote.pdf",
    "filename": "quote.pdf",
    "special_mention": None,
    "customer": {"id": 7, "url": "https://api.example/customers/7"},
    "invoice_line_sections": {"url": "https://api.example/quotes/42/invoice_line_sections"},
    "invoice_lines": {"url": "https://api.example/quotes/42/invoice_lines"},
    "linked_invoices": {"url": "https://api.example/quotes/42/linked_invoices"},
    "pdf_invoice_free_text": "",
    "pdf_invoice_subject": "",
    "pdf_description": None,
    "quote_template": {"id": 3},
    "appendices": {"url": "https://api.example/quotes/42/appendices"},
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


class TestQuotes:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/quotes").mock(
            return_value=httpx.Response(
                200, json={"items": [QUOTE], "has_more": False, "next_cursor": None}
            )
        )
        page = Quotes(sync_client).list(limit=50, sort="-id")
        assert route.calls.last.request.url.params["limit"] == "50"
        quote = page.items[0]
        assert quote.id == 42
        assert quote.amount == Decimal("600.00")
        assert quote.discount is not None
        assert quote.discount.value == Decimal("10.00")
        assert quote.customer is not None
        assert quote.customer.id == 7

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/quotes/42").mock(return_value=httpx.Response(200, json=QUOTE))
        quote = Quotes(sync_client).get(42)
        assert quote.quote_number == "Q-0001"

    @respx.mock
    def test_create_drops_none_and_sends_lines(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/quotes").mock(
            return_value=httpx.Response(201, json=QUOTE)
        )
        Quotes(sync_client).create(
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
            "invoice_lines": [{"product_id": 3049, "quantity": 2}],
        }

    @respx.mock
    def test_update_sends_only_provided_fields(self, sync_client: SyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/quotes/42").mock(
            return_value=httpx.Response(200, json=QUOTE)
        )
        Quotes(sync_client).update(42, special_mention="Thanks!")
        assert json.loads(route.calls.last.request.content) == {"special_mention": "Thanks!"}

    @respx.mock
    def test_update_status(self, sync_client: SyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/quotes/42/update_status").mock(
            return_value=httpx.Response(200, json={**QUOTE, "status": "accepted"})
        )
        quote = Quotes(sync_client).update_status(42, status="accepted")
        assert json.loads(route.calls.last.request.content) == {"status": "accepted"}
        assert quote.status == "accepted"

    @respx.mock
    def test_send_by_email(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/quotes/42/send_by_email").mock(
            return_value=httpx.Response(204)
        )
        result = Quotes(sync_client).send_by_email(42, recipients=["a@example.com"])
        assert result is None
        assert json.loads(route.calls.last.request.content) == {
            "recipients": ["a@example.com"]
        }

    @respx.mock
    def test_list_appendices(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/quotes/42/appendices").mock(
            return_value=httpx.Response(
                200, json={"items": [APPENDIX], "has_more": False, "next_cursor": None}
            )
        )
        page = Quotes(sync_client).list_appendices(42)
        assert page.items[0].filename == "appendix.pdf"

    @respx.mock
    def test_add_appendix_uploads_multipart(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/quotes/42/appendices").mock(
            return_value=httpx.Response(201, json=APPENDIX)
        )
        appendix = Quotes(sync_client).add_appendix(
            42, file=b"%PDF-1.4 ...", filename="appendix.pdf"
        )
        assert appendix.id == 5
        assert b"appendix.pdf" in route.calls.last.request.content

    @respx.mock
    def test_list_invoice_lines(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/quotes/42/invoice_lines").mock(
            return_value=httpx.Response(
                200, json={"items": [INVOICE_LINE], "has_more": False, "next_cursor": None}
            )
        )
        page = Quotes(sync_client).list_invoice_lines(42)
        line = page.items[0]
        assert line.id == 444
        assert line.quantity == Decimal("12")
        assert line.product is not None
        assert line.product.id == 3049

    @respx.mock
    def test_list_invoice_line_sections(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/quotes/42/invoice_line_sections").mock(
            return_value=httpx.Response(
                200,
                json={"items": [INVOICE_LINE_SECTION], "has_more": False, "next_cursor": None},
            )
        )
        page = Quotes(sync_client).list_invoice_line_sections(42)
        assert page.items[0].title == "Section 1"


class TestAsyncQuotes:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/quotes").mock(
            return_value=httpx.Response(
                200, json={"items": [QUOTE], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncQuotes(async_client).list()
        assert page.items[0].id == 42

    @respx.mock
    async def test_create(self, async_client: AsyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/quotes").mock(
            return_value=httpx.Response(201, json=QUOTE)
        )
        quote = await AsyncQuotes(async_client).create(
            date="2026-01-05",
            deadline="2026-02-05",
            customer_id=7,
            invoice_lines=[{"product_id": 3049, "quantity": 2}],
        )
        assert quote.id == 42
        body = json.loads(route.calls.last.request.content)
        assert body["customer_id"] == 7

    @respx.mock
    async def test_update(self, async_client: AsyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/quotes/42").mock(return_value=httpx.Response(200, json=QUOTE))
        quote = await AsyncQuotes(async_client).update(42, currency="USD")
        assert quote.id == 42

    @respx.mock
    async def test_update_status(self, async_client: AsyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/quotes/42/update_status").mock(
            return_value=httpx.Response(200, json={**QUOTE, "status": "denied"})
        )
        quote = await AsyncQuotes(async_client).update_status(42, status="denied")
        assert quote.status == "denied"

    @respx.mock
    async def test_send_by_email(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/quotes/42/send_by_email").mock(
            return_value=httpx.Response(204)
        )
        result = await AsyncQuotes(async_client).send_by_email(42)
        assert result is None

    @respx.mock
    async def test_list_appendices(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/quotes/42/appendices").mock(
            return_value=httpx.Response(
                200, json={"items": [APPENDIX], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncQuotes(async_client).list_appendices(42)
        assert page.items[0].id == 5

    @respx.mock
    async def test_add_appendix(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/quotes/42/appendices").mock(
            return_value=httpx.Response(201, json=APPENDIX)
        )
        appendix = await AsyncQuotes(async_client).add_appendix(42, file=b"%PDF", filename="a.pdf")
        assert appendix.filename == "appendix.pdf"

    @respx.mock
    async def test_list_invoice_lines(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/quotes/42/invoice_lines").mock(
            return_value=httpx.Response(
                200, json={"items": [INVOICE_LINE], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncQuotes(async_client).list_invoice_lines(42)
        assert page.items[0].id == 444

    @respx.mock
    async def test_list_invoice_line_sections(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/quotes/42/invoice_line_sections").mock(
            return_value=httpx.Response(
                200,
                json={"items": [INVOICE_LINE_SECTION], "has_more": False, "next_cursor": None},
            )
        )
        page = await AsyncQuotes(async_client).list_invoice_line_sections(42)
        assert page.items[0].id == 9
