from __future__ import annotations

import json

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.journals import AsyncJournals, Journals

from ..conftest import BASE_URL

JOURNAL = {"id": 7, "code": "VEN", "label": "Ventes", "type": "sales"}


class TestJournals:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/journals").mock(
            return_value=httpx.Response(
                200, json={"items": [JOURNAL], "has_more": False, "next_cursor": None}
            )
        )
        page = Journals(sync_client).list(limit=50, sort="-id")
        assert route.calls.last.request.url.params["limit"] == "50"
        assert route.calls.last.request.url.params["sort"] == "-id"
        journal = page.items[0]
        assert journal.id == 7
        assert journal.code == "VEN"
        assert journal.type == "sales"

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/journals/7").mock(
            return_value=httpx.Response(200, json=JOURNAL)
        )
        journal = Journals(sync_client).get(7)
        assert journal.label == "Ventes"

    @respx.mock
    def test_create(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/journals").mock(
            return_value=httpx.Response(201, json=JOURNAL)
        )
        journal = Journals(sync_client).create(code="VEN", label="Ventes")
        assert journal.id == 7
        body = json.loads(route.calls.last.request.content)
        assert body == {"code": "VEN", "label": "Ventes"}


class TestAsyncJournals:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/journals").mock(
            return_value=httpx.Response(
                200, json={"items": [JOURNAL], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncJournals(async_client).list()
        assert page.items[0].id == 7

    @respx.mock
    async def test_get(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/journals/7").mock(
            return_value=httpx.Response(200, json=JOURNAL)
        )
        journal = await AsyncJournals(async_client).get(7)
        assert journal.id == 7

    @respx.mock
    async def test_create(self, async_client: AsyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/journals").mock(
            return_value=httpx.Response(201, json=JOURNAL)
        )
        journal = await AsyncJournals(async_client).create(code="VEN", label="Ventes")
        assert journal.id == 7
        body = json.loads(route.calls.last.request.content)
        assert body == {"code": "VEN", "label": "Ventes"}
