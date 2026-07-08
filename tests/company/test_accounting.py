from __future__ import annotations

from decimal import Decimal

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.accounting import (
    AsyncFiscalYears,
    AsyncTrialBalance,
    FiscalYears,
    TrialBalance,
)

from ..conftest import BASE_URL

TRIAL_BALANCE_ROW = {
    "number": "607000",
    "formatted_number": "607000",
    "label": "Purchase of goods",
    "debits": "1000.00",
    "credits": "0.00",
}

FISCAL_YEAR = {
    "id": 1,
    "start": "2026-01-01",
    "finish": "2026-12-31",
    "status": "open",
    "created_at": "2026-01-01T09:00:00Z",
    "updated_at": "2026-01-01T09:00:00Z",
}


class TestTrialBalance:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/trial_balance").mock(
            return_value=httpx.Response(
                200, json={"items": [TRIAL_BALANCE_ROW], "has_more": False, "next_cursor": None}
            )
        )
        page = TrialBalance(sync_client).list(
            period_start="2026-01-01", period_end="2026-12-31", is_auxiliary=True, limit=50
        )
        params = route.calls.last.request.url.params
        assert params["period_start"] == "2026-01-01"
        assert params["period_end"] == "2026-12-31"
        assert params["is_auxiliary"] == "true"
        assert params["limit"] == "50"
        row = page.items[0]
        assert row.number == "607000"
        assert row.debits == Decimal("1000.00")


class TestFiscalYears:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/fiscal_years").mock(
            return_value=httpx.Response(
                200, json={"items": [FISCAL_YEAR], "has_more": False, "next_cursor": None}
            )
        )
        page = FiscalYears(sync_client).list(sort="-id")
        assert route.calls.last.request.url.params["sort"] == "-id"
        year = page.items[0]
        assert year.id == 1
        assert year.status == "open"
        assert str(year.start) == "2026-01-01"


class TestAsyncTrialBalance:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/trial_balance").mock(
            return_value=httpx.Response(
                200, json={"items": [TRIAL_BALANCE_ROW], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncTrialBalance(async_client).list(
            period_start="2026-01-01", period_end="2026-12-31"
        )
        assert page.items[0].label == "Purchase of goods"


class TestAsyncFiscalYears:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/fiscal_years").mock(
            return_value=httpx.Response(
                200, json={"items": [FISCAL_YEAR], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncFiscalYears(async_client).list()
        assert page.items[0].id == 1
