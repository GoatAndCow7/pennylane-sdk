from __future__ import annotations

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.customer_invoice_templates import (
    AsyncCustomerInvoiceTemplates,
    CustomerInvoiceTemplates,
)

from ..conftest import BASE_URL

TEMPLATE = {
    "id": 3,
    "name": "Default template",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}


class TestCustomerInvoiceTemplates:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/customer_invoice_templates").mock(
            return_value=httpx.Response(
                200, json={"items": [TEMPLATE], "has_more": False, "next_cursor": None}
            )
        )
        page = CustomerInvoiceTemplates(sync_client).list(limit=50, sort="-id")
        assert route.calls.last.request.url.params["limit"] == "50"
        assert route.calls.last.request.url.params["sort"] == "-id"
        template = page.items[0]
        assert template.id == 3
        assert template.name == "Default template"


class TestAsyncCustomerInvoiceTemplates:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/customer_invoice_templates").mock(
            return_value=httpx.Response(
                200, json={"items": [TEMPLATE], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncCustomerInvoiceTemplates(async_client).list()
        assert page.items[0].id == 3
