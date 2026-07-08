from __future__ import annotations

import json

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.firm.exports import AsyncFirmExports, FirmExports

FIRM_BASE_URL = "https://app.pennylane.com/api/external/firm/v1"

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


def sync_client() -> SyncAPIClient:
    return SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)


def async_client() -> AsyncAPIClient:
    return AsyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)


class TestFirmFecExports:
    @respx.mock
    def test_create(self) -> None:
        route = respx.post(f"{FIRM_BASE_URL}/companies/10/exports/fecs").mock(
            return_value=httpx.Response(201, json=FEC_EXPORT_CREATE)
        )
        export = FirmExports(sync_client()).fecs.create(
            10, period_start="2026-01-01", period_end="2026-01-31"
        )
        assert json.loads(route.calls.last.request.content) == {
            "period_start": "2026-01-01",
            "period_end": "2026-01-31",
        }
        assert export.id == 1
        assert export.status == "pending"

    @respx.mock
    def test_get(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/10/exports/fecs/1").mock(
            return_value=httpx.Response(200, json=FEC_EXPORT_GET)
        )
        export = FirmExports(sync_client()).fecs.get(10, 1)
        assert export.status == "ready"
        assert export.file_url == "https://files.pennylane.com/fec/1.txt"


class TestFirmAnalyticalGeneralLedgerExports:
    @respx.mock
    def test_create(self) -> None:
        route = respx.post(
            f"{FIRM_BASE_URL}/companies/10/exports/analytical_general_ledgers"
        ).mock(return_value=httpx.Response(201, json=AGL_EXPORT_CREATE))
        export = FirmExports(sync_client()).analytical_general_ledgers.create(
            10, period_start="2026-01-01", period_end="2026-01-31", mode="in_column"
        )
        assert json.loads(route.calls.last.request.content) == {
            "period_start": "2026-01-01",
            "period_end": "2026-01-31",
            "mode": "in_column",
        }
        assert export.id == 3

    @respx.mock
    def test_create_without_mode(self) -> None:
        route = respx.post(
            f"{FIRM_BASE_URL}/companies/10/exports/analytical_general_ledgers"
        ).mock(return_value=httpx.Response(201, json=AGL_EXPORT_CREATE))
        FirmExports(sync_client()).analytical_general_ledgers.create(
            10, period_start="2026-01-01", period_end="2026-01-31"
        )
        assert json.loads(route.calls.last.request.content) == {
            "period_start": "2026-01-01",
            "period_end": "2026-01-31",
        }

    @respx.mock
    def test_get(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/10/exports/analytical_general_ledgers/3").mock(
            return_value=httpx.Response(200, json=AGL_EXPORT_GET)
        )
        export = FirmExports(sync_client()).analytical_general_ledgers.get(10, 3)
        assert export.status == "ready"


class TestAsyncFirmExports:
    @respx.mock
    async def test_fecs_create(self) -> None:
        respx.post(f"{FIRM_BASE_URL}/companies/10/exports/fecs").mock(
            return_value=httpx.Response(201, json=FEC_EXPORT_CREATE)
        )
        export = await AsyncFirmExports(async_client()).fecs.create(
            10, period_start="2026-01-01", period_end="2026-01-31"
        )
        assert export.id == 1

    @respx.mock
    async def test_fecs_get(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/10/exports/fecs/1").mock(
            return_value=httpx.Response(200, json=FEC_EXPORT_GET)
        )
        export = await AsyncFirmExports(async_client()).fecs.get(10, 1)
        assert export.status == "ready"

    @respx.mock
    async def test_analytical_general_ledgers_create(self) -> None:
        respx.post(
            f"{FIRM_BASE_URL}/companies/10/exports/analytical_general_ledgers"
        ).mock(return_value=httpx.Response(201, json=AGL_EXPORT_CREATE))
        export = await AsyncFirmExports(async_client()).analytical_general_ledgers.create(
            10, period_start="2026-01-01", period_end="2026-01-31"
        )
        assert export.id == 3

    @respx.mock
    async def test_analytical_general_ledgers_get(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/10/exports/analytical_general_ledgers/3").mock(
            return_value=httpx.Response(200, json=AGL_EXPORT_GET)
        )
        export = await AsyncFirmExports(async_client()).analytical_general_ledgers.get(10, 3)
        assert export.status == "ready"
