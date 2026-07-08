"""Trial Balance and Fiscal Years resources (Company API v2).

Reference: https://pennylane.readme.io/reference/gettrialbalance
"""

from __future__ import annotations

from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...types.company.accounting import FiscalYear, TrialBalanceRow

__all__ = ["AsyncFiscalYears", "AsyncTrialBalance", "FiscalYears", "TrialBalance"]


class TrialBalance(SyncAPIResource):
    """Read the company trial balance."""

    def list(
        self,
        *,
        period_start: str,
        period_end: str,
        is_auxiliary: bool | None = None,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> SyncCursorPage[TrialBalanceRow]:
        """List the trial balance rows for a period.

        Scope: ``trial_balance:readonly``.
        Reference: https://pennylane.readme.io/reference/gettrialbalance

        Args:
            period_start: Period start date (``YYYY-MM-DD``).
            period_end: Period end date (``YYYY-MM-DD``).
            is_auxiliary: Whether to include auxiliary ledger accounts.
            cursor: Pagination cursor from a previous page.
            limit: Results per page.
        """
        return self._get_page(
            "/trial_balance",
            item_type=TrialBalanceRow,
            params={
                "period_start": period_start,
                "period_end": period_end,
                "is_auxiliary": is_auxiliary,
                "cursor": cursor,
                "limit": limit,
            },
        )


class FiscalYears(SyncAPIResource):
    """Read the company fiscal years."""

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[FiscalYear]:
        """List the company's fiscal years.

        Scope: ``fiscal_years:readonly``.
        Reference: https://pennylane.readme.io/reference/company-fiscal-years

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page.
            sort: Sort field, prefixed with ``-`` for descending.
        """
        return self._get_page(
            "/fiscal_years",
            item_type=FiscalYear,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )


class AsyncTrialBalance(AsyncAPIResource):
    """Read the company trial balance (async)."""

    async def list(
        self,
        *,
        period_start: str,
        period_end: str,
        is_auxiliary: bool | None = None,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> AsyncCursorPage[TrialBalanceRow]:
        """List the trial balance rows for a period.

        Scope: ``trial_balance:readonly``.
        Reference: https://pennylane.readme.io/reference/gettrialbalance
        """
        return await self._get_page(
            "/trial_balance",
            item_type=TrialBalanceRow,
            params={
                "period_start": period_start,
                "period_end": period_end,
                "is_auxiliary": is_auxiliary,
                "cursor": cursor,
                "limit": limit,
            },
        )


class AsyncFiscalYears(AsyncAPIResource):
    """Read the company fiscal years (async)."""

    async def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[FiscalYear]:
        """List the company's fiscal years.

        Scope: ``fiscal_years:readonly``.
        Reference: https://pennylane.readme.io/reference/company-fiscal-years
        """
        return await self._get_page(
            "/fiscal_years",
            item_type=FiscalYear,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )
