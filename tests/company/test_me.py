from __future__ import annotations

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.me import AsyncMe, Me

from ..conftest import BASE_URL

ME = {
    "user": {
        "id": 12345,
        "first_name": "John",
        "last_name": "Doe",
        "email": "jdoe@pennylane.com",
        "locale": "fr",
    },
    "company": {
        "id": 123456,
        "name": "Pennylane",
        "reg_no": "123456789",
        "accounting_logic": "FR_PCG",
    },
    "scopes": ["customer_invoices", "suppliers"],
}


class TestMe:
    @respx.mock
    def test_retrieve(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/me").mock(return_value=httpx.Response(200, json=ME))
        me = Me(sync_client).retrieve()
        assert me.user is not None
        assert me.user.id == 12345
        assert me.user.email == "jdoe@pennylane.com"
        assert me.company is not None
        assert me.company.id == 123456
        assert me.company.accounting_logic == "FR_PCG"
        assert me.scopes == ["customer_invoices", "suppliers"]


class TestAsyncMe:
    @respx.mock
    async def test_retrieve(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/me").mock(return_value=httpx.Response(200, json=ME))
        me = await AsyncMe(async_client).retrieve()
        assert me.company is not None
        assert me.company.name == "Pennylane"
