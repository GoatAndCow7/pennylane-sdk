"""Categories and category groups resources (Firm API v1).

Reference: https://firm-pennylane.readme.io/reference/getcategories
"""

from __future__ import annotations

from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...filters import FiltersInput
from ...types.firm.categories import FirmCategory, FirmCategoryGroup

__all__ = ["AsyncFirmCategories", "AsyncFirmCategoryGroups", "FirmCategories", "FirmCategoryGroups"]


class FirmCategories(SyncAPIResource):
    """Browse a client company's categories used to classify transactions and invoice
    lines.
    """

    def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[FirmCategory]:
        """List categories of a client company.

        Scope: ``categories:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getcategories

        Args:
            company_id: Identifier of the client company.
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            f"/companies/{company_id}/categories",
            item_type=FirmCategory,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    def get(self, company_id: int, category_id: int) -> FirmCategory:
        """Retrieve a category of a client company by its Pennylane identifier.

        Scope: ``categories:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getcategory
        """
        return self._get(
            f"/companies/{company_id}/categories/{category_id}", cast_to=FirmCategory
        )


class FirmCategoryGroups(SyncAPIResource):
    """Browse a client company's category groups."""

    def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> SyncCursorPage[FirmCategoryGroup]:
        """List category groups of a client company.

        Scope: ``categories:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getcategorygroups

        Args:
            company_id: Identifier of the client company.
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
        """
        return self._get_page(
            f"/companies/{company_id}/category_groups",
            item_type=FirmCategoryGroup,
            params={"cursor": cursor, "limit": limit},
        )

    def get(self, company_id: int, category_group_id: int) -> FirmCategoryGroup:
        """Retrieve a category group of a client company by its Pennylane identifier.

        Scope: ``categories:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getcategorygroup
        """
        return self._get(
            f"/companies/{company_id}/category_groups/{category_group_id}",
            cast_to=FirmCategoryGroup,
        )

    def list_categories(
        self,
        company_id: int,
        category_group_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> SyncCursorPage[FirmCategory]:
        """List the categories belonging to a category group of a client company.

        Scope: ``categories:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getcategorygroupcategories

        Args:
            company_id: Identifier of the client company.
            category_group_id: Identifier of the parent category group.
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
        """
        return self._get_page(
            f"/companies/{company_id}/category_groups/{category_group_id}/categories",
            item_type=FirmCategory,
            params={"cursor": cursor, "limit": limit},
        )


class AsyncFirmCategories(AsyncAPIResource):
    """Browse a client company's categories used to classify transactions and invoice
    lines (async).
    """

    async def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[FirmCategory]:
        """List categories of a client company.

        Scope: ``categories:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getcategories
        """
        return await self._get_page(
            f"/companies/{company_id}/categories",
            item_type=FirmCategory,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    async def get(self, company_id: int, category_id: int) -> FirmCategory:
        """Retrieve a category of a client company by its Pennylane identifier.

        Scope: ``categories:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getcategory
        """
        return await self._get(
            f"/companies/{company_id}/categories/{category_id}", cast_to=FirmCategory
        )


class AsyncFirmCategoryGroups(AsyncAPIResource):
    """Browse a client company's category groups (async)."""

    async def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> AsyncCursorPage[FirmCategoryGroup]:
        """List category groups of a client company.

        Scope: ``categories:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getcategorygroups
        """
        return await self._get_page(
            f"/companies/{company_id}/category_groups",
            item_type=FirmCategoryGroup,
            params={"cursor": cursor, "limit": limit},
        )

    async def get(self, company_id: int, category_group_id: int) -> FirmCategoryGroup:
        """Retrieve a category group of a client company by its Pennylane identifier.

        Scope: ``categories:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getcategorygroup
        """
        return await self._get(
            f"/companies/{company_id}/category_groups/{category_group_id}",
            cast_to=FirmCategoryGroup,
        )

    async def list_categories(
        self,
        company_id: int,
        category_group_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> AsyncCursorPage[FirmCategory]:
        """List the categories belonging to a category group of a client company.

        Scope: ``categories:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getcategorygroupcategories
        """
        return await self._get_page(
            f"/companies/{company_id}/category_groups/{category_group_id}/categories",
            item_type=FirmCategory,
            params={"cursor": cursor, "limit": limit},
        )
