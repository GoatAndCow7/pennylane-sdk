"""Changelogs resource (Firm API v1).

Reference: https://firm-pennylane.readme.io/reference/getledgerentrylinechanges
"""

from __future__ import annotations

import datetime as dt

from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...types.firm.changelogs import ChangelogEvent

__all__ = ["AsyncFirmChangelogs", "FirmChangelogs"]


class FirmChangelogs(SyncAPIResource):
    """Track change events (insert/update/delete) for company resources."""

    def dms_files(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> SyncCursorPage[ChangelogEvent]:
        """List DMS file change events.

        Scope: ``dms_files:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getdmsfileschanges

        Args:
            company_id: Identifier of the company.
            cursor: Pagination cursor from a previous page.
            limit: Results per page.
            start_date: Only return events processed on or after this date.
        """
        return self._get_page(
            f"/companies/{company_id}/changelogs/dms_files",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )

    def ledger_entry_lines(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> SyncCursorPage[ChangelogEvent]:
        """List ledger entry line change events.

        Scope: ``ledger_entries:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getledgerentrylinechanges

        Args:
            company_id: Identifier of the company.
            cursor: Pagination cursor from a previous page.
            limit: Results per page.
            start_date: Only return events processed on or after this date.
        """
        return self._get_page(
            f"/companies/{company_id}/changelogs/ledger_entry_lines",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )

    def supplier_invoices(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> SyncCursorPage[ChangelogEvent]:
        """List supplier invoice change events.

        Beta: undocumented endpoint, subject to change.

        Scope: ``supplier_invoices:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getsupplierinvoiceschanges

        Args:
            company_id: Identifier of the company.
            cursor: Pagination cursor from a previous page.
            limit: Results per page.
            start_date: Only return events processed on or after this date.
        """
        return self._get_page(
            f"/companies/{company_id}/changelogs/supplier_invoices",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )

    def customer_invoices(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> SyncCursorPage[ChangelogEvent]:
        """List customer invoice change events.

        Beta: undocumented endpoint, subject to change.

        Scope: ``customer_invoices:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getcustomerinvoiceschanges

        Args:
            company_id: Identifier of the company.
            cursor: Pagination cursor from a previous page.
            limit: Results per page.
            start_date: Only return events processed on or after this date.
        """
        return self._get_page(
            f"/companies/{company_id}/changelogs/customer_invoices",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )


class AsyncFirmChangelogs(AsyncAPIResource):
    """Track change events (insert/update/delete) for company resources (async)."""

    async def dms_files(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> AsyncCursorPage[ChangelogEvent]:
        """List DMS file change events.

        Scope: ``dms_files:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getdmsfileschanges
        """
        return await self._get_page(
            f"/companies/{company_id}/changelogs/dms_files",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )

    async def ledger_entry_lines(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> AsyncCursorPage[ChangelogEvent]:
        """List ledger entry line change events.

        Scope: ``ledger_entries:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getledgerentrylinechanges
        """
        return await self._get_page(
            f"/companies/{company_id}/changelogs/ledger_entry_lines",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )

    async def supplier_invoices(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> AsyncCursorPage[ChangelogEvent]:
        """List supplier invoice change events.

        Beta: undocumented endpoint, subject to change.

        Scope: ``supplier_invoices:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getsupplierinvoiceschanges
        """
        return await self._get_page(
            f"/companies/{company_id}/changelogs/supplier_invoices",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )

    async def customer_invoices(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        start_date: dt.date | None = None,
    ) -> AsyncCursorPage[ChangelogEvent]:
        """List customer invoice change events.

        Beta: undocumented endpoint, subject to change.

        Scope: ``customer_invoices:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getcustomerinvoiceschanges
        """
        return await self._get_page(
            f"/companies/{company_id}/changelogs/customer_invoices",
            item_type=ChangelogEvent,
            params={"cursor": cursor, "limit": limit, "start_date": start_date},
        )
