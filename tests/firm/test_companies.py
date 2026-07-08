from __future__ import annotations

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.firm.companies import AsyncFirmCompanies, FirmCompanies

FIRM_BASE_URL = "https://app.pennylane.com/api/external/firm/v1"

COMPANY = {
    "id": 7,
    "name": "Acme SAS",
    "billing_company_name": "Acme",
    "siren": "123456789",
    "address": "1 rue de Paris",
    "city": "Paris",
    "postal_code": "75001",
    "activity_nomenclature": "NAF",
    "activity_code": "6201Z",
    "external_id": "ext-7",
    "client_code": "CLI-7",
}


class TestFirmCompanies:
    @respx.mock
    def test_list(self) -> None:
        client = SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        route = respx.get(f"{FIRM_BASE_URL}/companies").mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [COMPANY],
                    "total_pages": 1,
                    "current_page": 1,
                    "total_items": 1,
                    "per_page": 20,
                },
            )
        )
        page = FirmCompanies(client).list(page=1, per_page=20)
        assert route.calls.last.request.url.params["page"] == "1"
        assert route.calls.last.request.url.params["per_page"] == "20"
        company = page.items[0]
        assert company.id == 7
        assert company.siren == "123456789"
        assert page.total_pages == 1
        assert page.current_page == 1

    @respx.mock
    def test_get(self) -> None:
        client = SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        respx.get(f"{FIRM_BASE_URL}/companies/7").mock(
            return_value=httpx.Response(200, json=COMPANY)
        )
        company = FirmCompanies(client).get(7)
        assert company.name == "Acme SAS"


class TestAsyncFirmCompanies:
    @respx.mock
    async def test_list(self) -> None:
        client = AsyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        respx.get(f"{FIRM_BASE_URL}/companies").mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [COMPANY],
                    "total_pages": 1,
                    "current_page": 1,
                    "total_items": 1,
                    "per_page": 20,
                },
            )
        )
        page = await AsyncFirmCompanies(client).list()
        assert page.items[0].id == 7

    @respx.mock
    async def test_get(self) -> None:
        client = AsyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)
        respx.get(f"{FIRM_BASE_URL}/companies/7").mock(
            return_value=httpx.Response(200, json=COMPANY)
        )
        company = await AsyncFirmCompanies(client).get(7)
        assert company.id == 7
