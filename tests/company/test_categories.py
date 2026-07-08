from __future__ import annotations

import json

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.categories import (
    AsyncCategories,
    AsyncCategoryGroups,
    Categories,
    CategoryGroups,
)

from ..conftest import BASE_URL

CATEGORY = {
    "id": 42,
    "label": "Alimentaire",
    "direction": "cash_out",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
    "category_group": {"id": 7},
    "analytical_code": "CODE123",
}

CATEGORY_GROUP = {
    "id": 7,
    "label": "Purchases",
    "categories": {"url": "https://app.pennylane.com/api/external/v2/category_groups/7/categories"},
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}


class TestCategories:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/categories").mock(
            return_value=httpx.Response(
                200, json={"items": [CATEGORY], "has_more": False, "next_cursor": None}
            )
        )
        page = Categories(sync_client).list(limit=50, sort="-id")
        assert route.calls.last.request.url.params["limit"] == "50"
        assert route.calls.last.request.url.params["sort"] == "-id"
        category = page.items[0]
        assert category.id == 42
        assert category.direction == "cash_out"
        assert category.category_group is not None
        assert category.category_group.id == 7

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/categories/42").mock(
            return_value=httpx.Response(200, json=CATEGORY)
        )
        category = Categories(sync_client).get(42)
        assert category.label == "Alimentaire"

    @respx.mock
    def test_create_drops_none(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/categories").mock(
            return_value=httpx.Response(201, json=CATEGORY)
        )
        Categories(sync_client).create(label="Alimentaire", category_group_id=7)
        body = json.loads(route.calls.last.request.content)
        assert body == {"label": "Alimentaire", "category_group_id": 7}

    @respx.mock
    def test_create_with_direction_and_analytical_code(
        self, sync_client: SyncAPIClient
    ) -> None:
        route = respx.post(f"{BASE_URL}/categories").mock(
            return_value=httpx.Response(201, json=CATEGORY)
        )
        Categories(sync_client).create(
            label="Alimentaire",
            category_group_id=7,
            direction="cash_in",
            analytical_code="CODE123",
        )
        body = json.loads(route.calls.last.request.content)
        assert body == {
            "label": "Alimentaire",
            "category_group_id": 7,
            "direction": "cash_in",
            "analytical_code": "CODE123",
        }

    @respx.mock
    def test_update_sends_only_provided_fields(self, sync_client: SyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/categories/42").mock(
            return_value=httpx.Response(200, json=CATEGORY)
        )
        Categories(sync_client).update(42, label="New label")
        assert json.loads(route.calls.last.request.content) == {"label": "New label"}


class TestCategoryGroups:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/category_groups").mock(
            return_value=httpx.Response(
                200, json={"items": [CATEGORY_GROUP], "has_more": False, "next_cursor": None}
            )
        )
        page = CategoryGroups(sync_client).list(limit=10)
        assert route.calls.last.request.url.params["limit"] == "10"
        group = page.items[0]
        assert group.id == 7
        assert group.label == "Purchases"
        assert group.categories is not None

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/category_groups/7").mock(
            return_value=httpx.Response(200, json=CATEGORY_GROUP)
        )
        group = CategoryGroups(sync_client).get(7)
        assert group.label == "Purchases"

    @respx.mock
    def test_list_categories(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/category_groups/7/categories").mock(
            return_value=httpx.Response(
                200, json={"items": [CATEGORY], "has_more": False, "next_cursor": None}
            )
        )
        page = CategoryGroups(sync_client).list_categories(7, limit=25)
        assert route.calls.last.request.url.params["limit"] == "25"
        assert page.items[0].id == 42


class TestAsyncCategories:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/categories").mock(
            return_value=httpx.Response(
                200, json={"items": [CATEGORY], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncCategories(async_client).list()
        assert page.items[0].id == 42

    @respx.mock
    async def test_create(self, async_client: AsyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/categories").mock(
            return_value=httpx.Response(201, json=CATEGORY)
        )
        category = await AsyncCategories(async_client).create(
            label="Alimentaire", category_group_id=7
        )
        assert category.id == 42
        body = json.loads(route.calls.last.request.content)
        assert body == {"label": "Alimentaire", "category_group_id": 7}

    @respx.mock
    async def test_update(self, async_client: AsyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/categories/42").mock(
            return_value=httpx.Response(200, json=CATEGORY)
        )
        category = await AsyncCategories(async_client).update(42, direction="cash_in")
        assert category.id == 42


class TestAsyncCategoryGroups:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/category_groups").mock(
            return_value=httpx.Response(
                200, json={"items": [CATEGORY_GROUP], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncCategoryGroups(async_client).list()
        assert page.items[0].id == 7

    @respx.mock
    async def test_get(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/category_groups/7").mock(
            return_value=httpx.Response(200, json=CATEGORY_GROUP)
        )
        group = await AsyncCategoryGroups(async_client).get(7)
        assert group.id == 7

    @respx.mock
    async def test_list_categories(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/category_groups/7/categories").mock(
            return_value=httpx.Response(
                200, json={"items": [CATEGORY], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncCategoryGroups(async_client).list_categories(7)
        assert page.items[0].id == 42
