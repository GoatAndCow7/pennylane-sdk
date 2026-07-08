"""Companies resource (Firm API v1).

Reference: https://firm-pennylane.readme.io/reference/companies
"""

from __future__ import annotations

from ..._pagination import AsyncNumberedPage, SyncNumberedPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...filters import FiltersInput
from ...types.firm.companies import FirmCompany

__all__ = ["AsyncFirmCompanies", "FirmCompanies"]


class FirmCompanies(SyncAPIResource):
    """Read the companies managed by the accounting firm."""

    def list(
        self,
        *,
        page: int | None = None,
        per_page: int | None = None,
        filter: FiltersInput | None = None,
    ) -> SyncNumberedPage[FirmCompany]:
        """List the firm's companies.

        Scope: ``companies:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/companies

        Args:
            page: Page index, starting at 1.
            per_page: Results per page (1-1000, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
        """
        return self._get_numbered_page(
            "/companies",
            item_type=FirmCompany,
            params={"page": page, "per_page": per_page, "filter": filter},
        )

    def get(self, company_id: int) -> FirmCompany:
        """Retrieve a company by its Pennylane identifier.

        Scope: ``companies:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/company
        """
        return self._get(f"/companies/{company_id}", cast_to=FirmCompany)


class AsyncFirmCompanies(AsyncAPIResource):
    """Read the companies managed by the accounting firm (async)."""

    async def list(
        self,
        *,
        page: int | None = None,
        per_page: int | None = None,
        filter: FiltersInput | None = None,
    ) -> AsyncNumberedPage[FirmCompany]:
        """List the firm's companies.

        Scope: ``companies:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/companies
        """
        return await self._get_numbered_page(
            "/companies",
            item_type=FirmCompany,
            params={"page": page, "per_page": per_page, "filter": filter},
        )

    async def get(self, company_id: int) -> FirmCompany:
        """Retrieve a company by its Pennylane identifier.

        Scope: ``companies:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/company
        """
        return await self._get(f"/companies/{company_id}", cast_to=FirmCompany)
