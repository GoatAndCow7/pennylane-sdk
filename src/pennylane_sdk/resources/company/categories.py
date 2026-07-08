"""Categories and category groups resources (Company API v2).

Reference: https://pennylane.readme.io/reference/getcategories
"""

from __future__ import annotations

from ..._models import drop_none
from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...filters import FiltersInput
from ...types.company.categories import Category, CategoryGroup

__all__ = ["AsyncCategories", "AsyncCategoryGroups", "Categories", "CategoryGroups"]


class Categories(SyncAPIResource):
    """Manage the company categories used to classify transactions and invoice lines."""

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[Category]:
        """List categories.

        Scope: ``categories:readonly``.
        Reference: https://pennylane.readme.io/reference/getcategories

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            "/categories",
            item_type=Category,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    def get(self, category_id: int) -> Category:
        """Retrieve a category by its Pennylane identifier.

        Scope: ``categories:readonly``.
        Reference: https://pennylane.readme.io/reference/getcategory
        """
        return self._get(f"/categories/{category_id}", cast_to=Category)

    def create(
        self,
        *,
        label: str,
        category_group_id: int,
        direction: str | None = None,
        analytical_code: str | None = None,
    ) -> Category:
        """Create a category.

        Scope: ``categories:all``.
        Reference: https://pennylane.readme.io/reference/postcategories

        Args:
            label: Category label.
            category_group_id: Identifier of the category group this category belongs to.
            direction: Only applicable for _treasury_ categories. Defaults to
                ``"cash_out"`` if not provided (``"cash_in"`` or ``"cash_out"``).
            analytical_code: Analytical code for the category.
        """
        body = drop_none(
            {
                "label": label,
                "category_group_id": category_group_id,
                "direction": direction,
                "analytical_code": analytical_code,
            }
        )
        return self._post("/categories", cast_to=Category, body=body)

    def update(
        self,
        category_id: int,
        *,
        label: str | None = None,
        direction: str | None = None,
        analytical_code: str | None = None,
    ) -> Category:
        """Update a category. Only the provided fields are modified.

        Scope: ``categories:all``.
        Reference: https://pennylane.readme.io/reference/updatecategory

        Args:
            label: Category label.
            direction: Only applicable for _treasury_ categories (``"cash_in"`` or
                ``"cash_out"``).
            analytical_code: Analytical code for the category.
        """
        body = drop_none(
            {
                "label": label,
                "direction": direction,
                "analytical_code": analytical_code,
            }
        )
        return self._put(f"/categories/{category_id}", cast_to=Category, body=body)


class CategoryGroups(SyncAPIResource):
    """Manage the company category groups."""

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> SyncCursorPage[CategoryGroup]:
        """List category groups.

        Scope: ``categories:readonly``.
        Reference: https://pennylane.readme.io/reference/getcategorygroups

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
        """
        return self._get_page(
            "/category_groups",
            item_type=CategoryGroup,
            params={"cursor": cursor, "limit": limit},
        )

    def get(self, category_group_id: int) -> CategoryGroup:
        """Retrieve a category group by its Pennylane identifier.

        Scope: ``categories:readonly``.
        Reference: https://pennylane.readme.io/reference/getcategorygroup
        """
        return self._get(f"/category_groups/{category_group_id}", cast_to=CategoryGroup)

    def list_categories(
        self,
        category_group_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> SyncCursorPage[Category]:
        """List the categories belonging to a category group.

        Scope: ``categories:readonly``.
        Reference: https://pennylane.readme.io/reference/getcategorygroupcategories

        Args:
            category_group_id: Identifier of the parent category group.
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
        """
        return self._get_page(
            f"/category_groups/{category_group_id}/categories",
            item_type=Category,
            params={"cursor": cursor, "limit": limit},
        )


class AsyncCategories(AsyncAPIResource):
    """Manage the company categories used to classify transactions and invoice lines (async)."""

    async def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[Category]:
        """List categories.

        Scope: ``categories:readonly``.
        Reference: https://pennylane.readme.io/reference/getcategories
        """
        return await self._get_page(
            "/categories",
            item_type=Category,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    async def get(self, category_id: int) -> Category:
        """Retrieve a category by its Pennylane identifier.

        Scope: ``categories:readonly``.
        Reference: https://pennylane.readme.io/reference/getcategory
        """
        return await self._get(f"/categories/{category_id}", cast_to=Category)

    async def create(
        self,
        *,
        label: str,
        category_group_id: int,
        direction: str | None = None,
        analytical_code: str | None = None,
    ) -> Category:
        """Create a category.

        Scope: ``categories:all``.
        Reference: https://pennylane.readme.io/reference/postcategories
        """
        body = drop_none(
            {
                "label": label,
                "category_group_id": category_group_id,
                "direction": direction,
                "analytical_code": analytical_code,
            }
        )
        return await self._post("/categories", cast_to=Category, body=body)

    async def update(
        self,
        category_id: int,
        *,
        label: str | None = None,
        direction: str | None = None,
        analytical_code: str | None = None,
    ) -> Category:
        """Update a category. Only the provided fields are modified.

        Scope: ``categories:all``.
        Reference: https://pennylane.readme.io/reference/updatecategory
        """
        body = drop_none(
            {
                "label": label,
                "direction": direction,
                "analytical_code": analytical_code,
            }
        )
        return await self._put(f"/categories/{category_id}", cast_to=Category, body=body)


class AsyncCategoryGroups(AsyncAPIResource):
    """Manage the company category groups (async)."""

    async def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> AsyncCursorPage[CategoryGroup]:
        """List category groups.

        Scope: ``categories:readonly``.
        Reference: https://pennylane.readme.io/reference/getcategorygroups
        """
        return await self._get_page(
            "/category_groups",
            item_type=CategoryGroup,
            params={"cursor": cursor, "limit": limit},
        )

    async def get(self, category_group_id: int) -> CategoryGroup:
        """Retrieve a category group by its Pennylane identifier.

        Scope: ``categories:readonly``.
        Reference: https://pennylane.readme.io/reference/getcategorygroup
        """
        return await self._get(f"/category_groups/{category_group_id}", cast_to=CategoryGroup)

    async def list_categories(
        self,
        category_group_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> AsyncCursorPage[Category]:
        """List the categories belonging to a category group.

        Scope: ``categories:readonly``.
        Reference: https://pennylane.readme.io/reference/getcategorygroupcategories

        Args:
            category_group_id: Identifier of the parent category group.
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
        """
        return await self._get_page(
            f"/category_groups/{category_group_id}/categories",
            item_type=Category,
            params={"cursor": cursor, "limit": limit},
        )
