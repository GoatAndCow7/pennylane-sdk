"""Changelogs resource (Company API v2).

Reference: https://pennylane.readme.io/reference/getcustomerinvoiceschanges
"""

from __future__ import annotations

import datetime as dt

from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...types.company.changelogs import ChangelogEvent

__all__ = ["AsyncChangelogs", "Changelogs"]


class Changelogs(SyncAPIResource):
    """Track change events (insert/update/delete) for company resources."""

    def customer_invoices(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> SyncCursorPage[ChangelogEvent]:
        """List customer invoice change events.

        Scope: ``customer_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomerinvoiceschanges

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-1000, API default 20).
            start_date: Only return events processed on or after this date.
        """
        return self._get_page(
            "/changelogs/customer_invoices",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )

    def supplier_invoices(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> SyncCursorPage[ChangelogEvent]:
        """List supplier invoice change events.

        Scope: ``supplier_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getsupplierinvoiceschanges

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-1000, API default 20).
            start_date: Only return events processed on or after this date.
        """
        return self._get_page(
            "/changelogs/supplier_invoices",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )

    def customers(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> SyncCursorPage[ChangelogEvent]:
        """List customer change events.

        Scope: ``customers:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomerchanges

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-1000, API default 20).
            start_date: Only return events processed on or after this date.
        """
        return self._get_page(
            "/changelogs/customers",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )

    def suppliers(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> SyncCursorPage[ChangelogEvent]:
        """List supplier change events.

        Scope: ``suppliers:readonly``.
        Reference: https://pennylane.readme.io/reference/getsupplierchanges

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-1000, API default 20).
            start_date: Only return events processed on or after this date.
        """
        return self._get_page(
            "/changelogs/suppliers",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )

    def products(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> SyncCursorPage[ChangelogEvent]:
        """List product change events.

        Scope: ``products:readonly``.
        Reference: https://pennylane.readme.io/reference/getproductchanges

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-1000, API default 20).
            start_date: Only return events processed on or after this date.
        """
        return self._get_page(
            "/changelogs/products",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )

    def ledger_entry_lines(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> SyncCursorPage[ChangelogEvent]:
        """List ledger entry line change events.

        Scope: ``ledger_entries:readonly``.
        Reference: https://pennylane.readme.io/reference/getledgerentrylinechanges

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-1000, API default 20).
            start_date: Only return events processed on or after this date.
        """
        return self._get_page(
            "/changelogs/ledger_entry_lines",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )

    def transactions(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> SyncCursorPage[ChangelogEvent]:
        """List transaction change events.

        Scope: ``transactions:readonly``.
        Reference: https://pennylane.readme.io/reference/gettransactionchanges

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-1000, API default 20).
            start_date: Only return events processed on or after this date.
        """
        return self._get_page(
            "/changelogs/transactions",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )

    def quotes(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> SyncCursorPage[ChangelogEvent]:
        """List quote change events.

        Scope: ``quotes:readonly``.
        Reference: https://pennylane.readme.io/reference/getquotechanges

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-1000, API default 20).
            start_date: Only return events processed on or after this date.
        """
        return self._get_page(
            "/changelogs/quotes",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )


    def ledger_entries_categories(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> SyncCursorPage[ChangelogEvent]:
        """List ledger entry category change events.

        Scope: ``ledger_entries:readonly``.
        Reference: https://pennylane.readme.io/reference/getledgerentriescategorychanges

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-1000, API default 20).
            start_date: Only return events processed on or after this date.
        """
        return self._get_page(
            "/changelogs/ledger_entries_categories",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )

    def ledger_entry_lines_categories(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> SyncCursorPage[ChangelogEvent]:
        """List ledger entry line category change events.

        Scope: ``ledger_entries:readonly``.
        Reference: https://pennylane.readme.io/reference/getledgerentrylinescategorychanges

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-1000, API default 20).
            start_date: Only return events processed on or after this date.
        """
        return self._get_page(
            "/changelogs/ledger_entry_lines_categories",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )

class AsyncChangelogs(AsyncAPIResource):
    """Track change events (insert/update/delete) for company resources (async)."""

    async def customer_invoices(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> AsyncCursorPage[ChangelogEvent]:
        """List customer invoice change events.

        Scope: ``customer_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomerinvoiceschanges
        """
        return await self._get_page(
            "/changelogs/customer_invoices",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )

    async def supplier_invoices(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> AsyncCursorPage[ChangelogEvent]:
        """List supplier invoice change events.

        Scope: ``supplier_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getsupplierinvoiceschanges
        """
        return await self._get_page(
            "/changelogs/supplier_invoices",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )

    async def customers(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> AsyncCursorPage[ChangelogEvent]:
        """List customer change events.

        Scope: ``customers:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomerchanges
        """
        return await self._get_page(
            "/changelogs/customers",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )

    async def suppliers(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> AsyncCursorPage[ChangelogEvent]:
        """List supplier change events.

        Scope: ``suppliers:readonly``.
        Reference: https://pennylane.readme.io/reference/getsupplierchanges
        """
        return await self._get_page(
            "/changelogs/suppliers",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )

    async def products(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> AsyncCursorPage[ChangelogEvent]:
        """List product change events.

        Scope: ``products:readonly``.
        Reference: https://pennylane.readme.io/reference/getproductchanges
        """
        return await self._get_page(
            "/changelogs/products",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )

    async def ledger_entry_lines(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> AsyncCursorPage[ChangelogEvent]:
        """List ledger entry line change events.

        Scope: ``ledger_entries:readonly``.
        Reference: https://pennylane.readme.io/reference/getledgerentrylinechanges
        """
        return await self._get_page(
            "/changelogs/ledger_entry_lines",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )

    async def transactions(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> AsyncCursorPage[ChangelogEvent]:
        """List transaction change events.

        Scope: ``transactions:readonly``.
        Reference: https://pennylane.readme.io/reference/gettransactionchanges
        """
        return await self._get_page(
            "/changelogs/transactions",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )

    async def quotes(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> AsyncCursorPage[ChangelogEvent]:
        """List quote change events.

        Scope: ``quotes:readonly``.
        Reference: https://pennylane.readme.io/reference/getquotechanges
        """
        return await self._get_page(
            "/changelogs/quotes",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )

    async def ledger_entries_categories(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> AsyncCursorPage[ChangelogEvent]:
        """List ledger entry category change events.

        Scope: ``ledger_entries:readonly``.
        Reference: https://pennylane.readme.io/reference/getledgerentriescategorychanges

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-1000, API default 20).
            start_date: Only return events processed on or after this date.
        """
        return await self._get_page(
            "/changelogs/ledger_entries_categories",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )

    async def ledger_entry_lines_categories(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> AsyncCursorPage[ChangelogEvent]:
        """List ledger entry line category change events.

        Scope: ``ledger_entries:readonly``.
        Reference: https://pennylane.readme.io/reference/getledgerentrylinescategorychanges

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-1000, API default 20).
            start_date: Only return events processed on or after this date.
        """
        return await self._get_page(
            "/changelogs/ledger_entry_lines_categories",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )
