from __future__ import annotations

import json

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.exports import AsyncExports, Exports

from ..conftest import BASE_URL

FEC_EXPORT_CREATE = {
    "id": 1,
    "status": "pending",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-05T09:00:00Z",
}
FEC_EXPORT_GET = {
    "id": 1,
    "file_url": "https://files.pennylane.com/fec/1.txt",
    "status": "ready",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-05T09:05:00Z",
}
GL_EXPORT_CREATE = {
    "id": 2,
    "status": "pending",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-05T09:00:00Z",
}
GL_EXPORT_GET = {
    "id": 2,
    "file_url": "https://files.pennylane.com/gl/2.txt",
    "status": "ready",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-05T09:05:00Z",
}
AGL_EXPORT_CREATE = {
    "id": 3,
    "status": "pending",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-05T09:00:00Z",
}
AGL_EXPORT_GET = {
    "id": 3,
    "file_url": "https://files.pennylane.com/agl/3.txt",
    "status": "ready",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-05T09:05:00Z",
}


class TestFecExports:
    @respx.mock
    def test_create(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/exports/fecs").mock(
            return_value=httpx.Response(201, json=FEC_EXPORT_CREATE)
        )
        export = Exports(sync_client).fecs.create(
            period_start="2026-01-01", period_end="2026-01-31"
        )
        assert json.loads(route.calls.last.request.content) == {
            "period_start": "2026-01-01",
            "period_end": "2026-01-31",
        }
        assert export.id == 1
        assert export.status == "pending"

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/exports/fecs/1").mock(
            return_value=httpx.Response(200, json=FEC_EXPORT_GET)
        )
        export = Exports(sync_client).fecs.get(1)
        assert export.status == "ready"
        assert export.file_url == "https://files.pennylane.com/fec/1.txt"


class TestGeneralLedgerExports:
    @respx.mock
    def test_create(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/exports/general_ledgers").mock(
            return_value=httpx.Response(201, json=GL_EXPORT_CREATE)
        )
        export = Exports(sync_client).general_ledgers.create(
            period_start="2026-01-01", period_end="2026-01-31"
        )
        assert json.loads(route.calls.last.request.content) == {
            "period_start": "2026-01-01",
            "period_end": "2026-01-31",
        }
        assert export.id == 2

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/exports/general_ledgers/2").mock(
            return_value=httpx.Response(200, json=GL_EXPORT_GET)
        )
        export = Exports(sync_client).general_ledgers.get(2)
        assert export.status == "ready"


class TestAnalyticalGeneralLedgerExports:
    @respx.mock
    def test_create(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/exports/analytical_general_ledgers").mock(
            return_value=httpx.Response(201, json=AGL_EXPORT_CREATE)
        )
        export = Exports(sync_client).analytical_general_ledgers.create(
            period_start="2026-01-01", period_end="2026-01-31", mode="in_column"
        )
        assert json.loads(route.calls.last.request.content) == {
            "period_start": "2026-01-01",
            "period_end": "2026-01-31",
            "mode": "in_column",
        }
        assert export.id == 3

    @respx.mock
    def test_create_without_mode(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/exports/analytical_general_ledgers").mock(
            return_value=httpx.Response(201, json=AGL_EXPORT_CREATE)
        )
        Exports(sync_client).analytical_general_ledgers.create(
            period_start="2026-01-01", period_end="2026-01-31"
        )
        assert json.loads(route.calls.last.request.content) == {
            "period_start": "2026-01-01",
            "period_end": "2026-01-31",
        }

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/exports/analytical_general_ledgers/3").mock(
            return_value=httpx.Response(200, json=AGL_EXPORT_GET)
        )
        export = Exports(sync_client).analytical_general_ledgers.get(3)
        assert export.status == "ready"


class TestAsyncExports:
    @respx.mock
    async def test_fecs_create(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/exports/fecs").mock(
            return_value=httpx.Response(201, json=FEC_EXPORT_CREATE)
        )
        export = await AsyncExports(async_client).fecs.create(
            period_start="2026-01-01", period_end="2026-01-31"
        )
        assert export.id == 1

    @respx.mock
    async def test_fecs_get(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/exports/fecs/1").mock(
            return_value=httpx.Response(200, json=FEC_EXPORT_GET)
        )
        export = await AsyncExports(async_client).fecs.get(1)
        assert export.status == "ready"

    @respx.mock
    async def test_general_ledgers_create(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/exports/general_ledgers").mock(
            return_value=httpx.Response(201, json=GL_EXPORT_CREATE)
        )
        export = await AsyncExports(async_client).general_ledgers.create(
            period_start="2026-01-01", period_end="2026-01-31"
        )
        assert export.id == 2

    @respx.mock
    async def test_general_ledgers_get(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/exports/general_ledgers/2").mock(
            return_value=httpx.Response(200, json=GL_EXPORT_GET)
        )
        export = await AsyncExports(async_client).general_ledgers.get(2)
        assert export.status == "ready"

    @respx.mock
    async def test_analytical_general_ledgers_create(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/exports/analytical_general_ledgers").mock(
            return_value=httpx.Response(201, json=AGL_EXPORT_CREATE)
        )
        export = await AsyncExports(async_client).analytical_general_ledgers.create(
            period_start="2026-01-01", period_end="2026-01-31", mode="in_line"
        )
        assert export.id == 3

    @respx.mock
    async def test_analytical_general_ledgers_get(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/exports/analytical_general_ledgers/3").mock(
            return_value=httpx.Response(200, json=AGL_EXPORT_GET)
        )
        export = await AsyncExports(async_client).analytical_general_ledgers.get(3)
        assert export.status == "ready"
