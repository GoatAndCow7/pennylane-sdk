"""Ledger Entry Lines resource (Company API v2).

Reference: https://pennylane.readme.io/reference/getledgerentrylines
"""

from __future__ import annotations

from typing import Any

from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...filters import FiltersInput
from ...types.company.ledger_entry_lines import (
    CategorizedLedgerEntryLine,
    LedgerEntryLine,
    LedgerEntryLineCategory,
)

__all__ = ["AsyncLedgerEntryLines", "LedgerEntryLines"]


class LedgerEntryLines(SyncAPIResource):
    """Read ledger entry lines and manage their lettering and analytical categories."""

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[LedgerEntryLine]:
        """List ledger entry lines.

        Scope: ``ledger_entries:readonly``.
        Reference: https://pennylane.readme.io/reference/getledgerentrylines

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page.
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            "/ledger_entry_lines",
            item_type=LedgerEntryLine,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    def get(self, ledger_entry_line_id: int) -> LedgerEntryLine:
        """Retrieve a ledger entry line by its Pennylane identifier.

        Scope: ``ledger_entries:readonly``.
        Reference: https://pennylane.readme.io/reference/getledgerentryline
        """
        return self._get(f"/ledger_entry_lines/{ledger_entry_line_id}", cast_to=LedgerEntryLine)

    def letter(
        self,
        *,
        unbalanced_lettering_strategy: str,
        ledger_entry_lines: list[dict[str, Any]],
    ) -> None:
        """Letter ledger entry lines together.

        Scope: ``ledger_entries:all``.
        Reference: https://pennylane.readme.io/reference/postledgerentrylineslet

        Args:
            unbalanced_lettering_strategy: ``"none"`` to reject unbalanced letterings,
                ``"partial"`` to allow them.
            ledger_entry_lines: Ledger entry lines to letter, e.g. ``[{"id": 1}, {"id": 2}]``.
        """
        self._post(
            "/ledger_entry_lines/lettering",
            cast_to=None,
            body={
                "unbalanced_lettering_strategy": unbalanced_lettering_strategy,
                "ledger_entry_lines": ledger_entry_lines,
            },
        )
        return None

    def unletter(
        self,
        *,
        unbalanced_lettering_strategy: str,
        ledger_entry_lines: list[dict[str, Any]],
    ) -> None:
        """Unletter ledger entry lines.

        Scope: ``ledger_entries:all``.
        Reference: https://pennylane.readme.io/reference/deleteledgerentrylinesun

        Args:
            unbalanced_lettering_strategy: ``"none"`` to reject unbalanced letterings,
                ``"partial"`` to allow them.
            ledger_entry_lines: Ledger entry lines to unletter, e.g. ``[{"id": 1}]``.
        """
        self._delete(
            "/ledger_entry_lines/lettering",
            cast_to=None,
            body={
                "unbalanced_lettering_strategy": unbalanced_lettering_strategy,
                "ledger_entry_lines": ledger_entry_lines,
            },
        )
        return None

    def list_lettered_lines(
        self,
        ledger_entry_line_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[LedgerEntryLine]:
        """List ledger entry lines lettered together with a given ledger entry line.

        Scope: ``ledger_entries:readonly``.
        Reference: https://pennylane.readme.io/reference/getledgerentrylineslette
        """
        return self._get_page(
            f"/ledger_entry_lines/{ledger_entry_line_id}/lettered_ledger_entry_lines",
            item_type=LedgerEntryLine,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    def list_categories(
        self,
        ledger_entry_line_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[LedgerEntryLineCategory]:
        """List the analytical categories attached to a ledger entry line.

        Scope: ``ledger_entries:readonly``.
        Reference: https://pennylane.readme.io/reference/getledgerentrylinescate
        """
        return self._get_page(
            f"/ledger_entry_lines/{ledger_entry_line_id}/categories",
            item_type=LedgerEntryLineCategory,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    def categorize(
        self,
        ledger_entry_line_id: int,
        *,
        categories: list[dict[str, Any]],
    ) -> CategorizedLedgerEntryLine:
        """Replace the analytical categories attached to a ledger entry line.

        Passing an empty list removes every category from the ledger entry line.

        Scope: ``ledger_entries:all``.
        Reference: https://pennylane.readme.io/reference/putledgerentrylinescate

        Args:
            categories: List of ``{"id": int, "weight": str}`` (weight between
                ``"0"`` and ``"1"``, up to 7 decimals).
        """
        return self._put(
            f"/ledger_entry_lines/{ledger_entry_line_id}/categories",
            cast_to=CategorizedLedgerEntryLine,
            body=categories,
        )


class AsyncLedgerEntryLines(AsyncAPIResource):
    """Read ledger entry lines and manage their lettering and analytical categories (async)."""

    async def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[LedgerEntryLine]:
        """List ledger entry lines.

        Scope: ``ledger_entries:readonly``.
        Reference: https://pennylane.readme.io/reference/getledgerentrylines
        """
        return await self._get_page(
            "/ledger_entry_lines",
            item_type=LedgerEntryLine,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    async def get(self, ledger_entry_line_id: int) -> LedgerEntryLine:
        """Retrieve a ledger entry line by its Pennylane identifier.

        Scope: ``ledger_entries:readonly``.
        Reference: https://pennylane.readme.io/reference/getledgerentryline
        """
        return await self._get(
            f"/ledger_entry_lines/{ledger_entry_line_id}", cast_to=LedgerEntryLine
        )

    async def letter(
        self,
        *,
        unbalanced_lettering_strategy: str,
        ledger_entry_lines: list[dict[str, Any]],
    ) -> None:
        """Letter ledger entry lines together.

        Scope: ``ledger_entries:all``.
        Reference: https://pennylane.readme.io/reference/postledgerentrylineslet
        """
        await self._post(
            "/ledger_entry_lines/lettering",
            cast_to=None,
            body={
                "unbalanced_lettering_strategy": unbalanced_lettering_strategy,
                "ledger_entry_lines": ledger_entry_lines,
            },
        )
        return None

    async def unletter(
        self,
        *,
        unbalanced_lettering_strategy: str,
        ledger_entry_lines: list[dict[str, Any]],
    ) -> None:
        """Unletter ledger entry lines.

        Scope: ``ledger_entries:all``.
        Reference: https://pennylane.readme.io/reference/deleteledgerentrylinesun
        """
        await self._delete(
            "/ledger_entry_lines/lettering",
            cast_to=None,
            body={
                "unbalanced_lettering_strategy": unbalanced_lettering_strategy,
                "ledger_entry_lines": ledger_entry_lines,
            },
        )
        return None

    async def list_lettered_lines(
        self,
        ledger_entry_line_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[LedgerEntryLine]:
        """List ledger entry lines lettered together with a given ledger entry line.

        Scope: ``ledger_entries:readonly``.
        Reference: https://pennylane.readme.io/reference/getledgerentrylineslette
        """
        return await self._get_page(
            f"/ledger_entry_lines/{ledger_entry_line_id}/lettered_ledger_entry_lines",
            item_type=LedgerEntryLine,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    async def list_categories(
        self,
        ledger_entry_line_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[LedgerEntryLineCategory]:
        """List the analytical categories attached to a ledger entry line.

        Scope: ``ledger_entries:readonly``.
        Reference: https://pennylane.readme.io/reference/getledgerentrylinescate
        """
        return await self._get_page(
            f"/ledger_entry_lines/{ledger_entry_line_id}/categories",
            item_type=LedgerEntryLineCategory,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    async def categorize(
        self,
        ledger_entry_line_id: int,
        *,
        categories: list[dict[str, Any]],
    ) -> CategorizedLedgerEntryLine:
        """Replace the analytical categories attached to a ledger entry line.

        Passing an empty list removes every category from the ledger entry line.

        Scope: ``ledger_entries:all``.
        Reference: https://pennylane.readme.io/reference/putledgerentrylinescate

        Args:
            categories: List of ``{"id": int, "weight": str}`` (weight between
                ``"0"`` and ``"1"``, up to 7 decimals).
        """
        return await self._put(
            f"/ledger_entry_lines/{ledger_entry_line_id}/categories",
            cast_to=CategorizedLedgerEntryLine,
            body=categories,
        )
