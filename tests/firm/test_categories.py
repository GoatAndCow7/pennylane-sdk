from __future__ import annotations

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.firm.categories import (
    AsyncFirmCategories,
    AsyncFirmCategoryGroups,
    FirmCategories,
    FirmCategoryGroups,
)

FIRM_BASE_URL = "https://app.pennylane.com/api/external/firm/v1"

CATEGORY = {
    "id": 42,
    "label": "Alimentaire",
    "direction": "cash_out",
    "analytical_code": "CODE123",
    "category_group": {"id": 7},
    "archived_at": None,
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}

CATEGORY_GROUP = {
    "id": 7,
    "label": "Purchases",
    "categories": {
        "url": "https://app.pennylane.com/api/external/firm/v1/companies/1/category_groups/7/categories"
    },
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}


def sync_client() -> SyncAPIClient:
    return SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)


def async_client() -> AsyncAPIClient:
    return AsyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)


class TestFirmCategories:
    @respx.mock
    def test_list(self) -> None:
        route = respx.get(f"{FIRM_BASE_URL}/companies/1/categories").mock(
            return_value=httpx.Response(
                200, json={"items": [CATEGORY], "has_more": False, "next_cursor": None}
            )
        )
        page = FirmCategories(sync_client()).list(1, limit=50, sort="-id")
        assert route.calls.last.request.url.params["limit"] == "50"
        category = page.items[0]
        assert category.id == 42
        assert category.direction == "cash_out"

    @respx.mock
    def test_get(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/1/categories/42").mock(
            return_value=httpx.Response(200, json=CATEGORY)
        )
        category = FirmCategories(sync_client()).get(1, 42)
        assert category.label == "Alimentaire"


class TestFirmCategoryGroups:
    @respx.mock
    def test_list(self) -> None:
        route = respx.get(f"{FIRM_BASE_URL}/companies/1/category_groups").mock(
            return_value=httpx.Response(
                200, json={"items": [CATEGORY_GROUP], "has_more": False, "next_cursor": None}
            )
        )
        page = FirmCategoryGroups(sync_client()).list(1, limit=20)
        assert route.calls.last.request.url.params["limit"] == "20"
        assert page.items[0].id == 7

    @respx.mock
    def test_get(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/1/category_groups/7").mock(
            return_value=httpx.Response(200, json=CATEGORY_GROUP)
        )
        group = FirmCategoryGroups(sync_client()).get(1, 7)
        assert group.label == "Purchases"

    @respx.mock
    def test_list_categories(self) -> None:
        route = respx.get(f"{FIRM_BASE_URL}/companies/1/category_groups/7/categories").mock(
            return_value=httpx.Response(
                200, json={"items": [CATEGORY], "has_more": False, "next_cursor": None}
            )
        )
        page = FirmCategoryGroups(sync_client()).list_categories(1, 7)
        assert route.calls.last.request.url.path.endswith("/category_groups/7/categories")
        assert page.items[0].id == 42


class TestAsyncFirmCategories:
    @respx.mock
    async def test_list(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/1/categories").mock(
            return_value=httpx.Response(
                200, json={"items": [CATEGORY], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncFirmCategories(async_client()).list(1)
        assert page.items[0].id == 42

    @respx.mock
    async def test_get(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/1/categories/42").mock(
            return_value=httpx.Response(200, json=CATEGORY)
        )
        category = await AsyncFirmCategories(async_client()).get(1, 42)
        assert category.id == 42


class TestAsyncFirmCategoryGroups:
    @respx.mock
    async def test_list(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/1/category_groups").mock(
            return_value=httpx.Response(
                200, json={"items": [CATEGORY_GROUP], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncFirmCategoryGroups(async_client()).list(1)
        assert page.items[0].id == 7

    @respx.mock
    async def test_get(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/1/category_groups/7").mock(
            return_value=httpx.Response(200, json=CATEGORY_GROUP)
        )
        group = await AsyncFirmCategoryGroups(async_client()).get(1, 7)
        assert group.id == 7

    @respx.mock
    async def test_list_categories(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/1/category_groups/7/categories").mock(
            return_value=httpx.Response(
                200, json={"items": [CATEGORY], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncFirmCategoryGroups(async_client()).list_categories(1, 7)
        assert page.items[0].id == 42
