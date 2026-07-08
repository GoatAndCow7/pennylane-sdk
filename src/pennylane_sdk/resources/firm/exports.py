"""Exports resource (Firm API v1).

Reference: https://firm-pennylane.readme.io/reference/postfecexport
"""

from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING

from ..._resource import AsyncAPIResource, SyncAPIResource
from ...types.firm.exports import AnalyticalGeneralLedgerExport, FecExport

if TYPE_CHECKING:
    from ..._base_client import AsyncAPIClient, SyncAPIClient

__all__ = [
    "AsyncFirmAnalyticalGeneralLedgerExports",
    "AsyncFirmExports",
    "AsyncFirmFecExports",
    "FirmAnalyticalGeneralLedgerExports",
    "FirmExports",
    "FirmFecExports",
]


class FirmFecExports(SyncAPIResource):
    """Manage FEC (Fichier des Ecritures Comptables) exports."""

    def create(
        self,
        company_id: int,
        *,
        period_start: dt.date | str,
        period_end: dt.date | str,
    ) -> FecExport:
        """Create a FEC export.

        Scope: ``exports:fec``.
        Reference: https://firm-pennylane.readme.io/reference/postfecexport

        Args:
            company_id: Identifier of the company.
            period_start: Start date of the period to export.
            period_end: End date of the period to export.
        """
        body = {"period_start": str(period_start), "period_end": str(period_end)}
        return self._post(
            f"/companies/{company_id}/exports/fecs", cast_to=FecExport, body=body
        )

    def get(self, company_id: int, export_id: int) -> FecExport:
        """Retrieve a FEC export.

        Scope: ``exports:fec``.
        Reference: https://firm-pennylane.readme.io/reference/getfecexport
        """
        return self._get(
            f"/companies/{company_id}/exports/fecs/{export_id}", cast_to=FecExport
        )


class FirmAnalyticalGeneralLedgerExports(SyncAPIResource):
    """Manage Analytical General Ledger exports."""

    def create(
        self,
        company_id: int,
        *,
        period_start: dt.date | str,
        period_end: dt.date | str,
        mode: str | None = None,
    ) -> AnalyticalGeneralLedgerExport:
        """Create an Analytical General Ledger export.

        Scope: ``exports:agl``.
        Reference: https://firm-pennylane.readme.io/reference/postanalyticalgeneralledgerexport

        Args:
            company_id: Identifier of the company.
            period_start: Start date of the period to export.
            period_end: End date of the period to export.
            mode: Export layout, ``"in_line"`` (default) or ``"in_column"``.
        """
        body = {"period_start": str(period_start), "period_end": str(period_end)}
        if mode is not None:
            body["mode"] = mode
        return self._post(
            f"/companies/{company_id}/exports/analytical_general_ledgers",
            cast_to=AnalyticalGeneralLedgerExport,
            body=body,
        )

    def get(self, company_id: int, export_id: int) -> AnalyticalGeneralLedgerExport:
        """Retrieve an Analytical General Ledger export.

        Scope: ``exports:agl``.
        Reference: https://firm-pennylane.readme.io/reference/getanalyticalgeneralledgerexport
        """
        return self._get(
            f"/companies/{company_id}/exports/analytical_general_ledgers/{export_id}",
            cast_to=AnalyticalGeneralLedgerExport,
        )


class FirmExports(SyncAPIResource):
    """Namespace for company data exports (FEC, Analytical General Ledger)."""

    def __init__(self, client: SyncAPIClient) -> None:
        super().__init__(client)
        self.fecs = FirmFecExports(client)
        self.analytical_general_ledgers = FirmAnalyticalGeneralLedgerExports(client)


class AsyncFirmFecExports(AsyncAPIResource):
    """Manage FEC (Fichier des Ecritures Comptables) exports (async)."""

    async def create(
        self,
        company_id: int,
        *,
        period_start: dt.date | str,
        period_end: dt.date | str,
    ) -> FecExport:
        """Create a FEC export.

        Scope: ``exports:fec``.
        Reference: https://firm-pennylane.readme.io/reference/postfecexport
        """
        body = {"period_start": str(period_start), "period_end": str(period_end)}
        return await self._post(
            f"/companies/{company_id}/exports/fecs", cast_to=FecExport, body=body
        )

    async def get(self, company_id: int, export_id: int) -> FecExport:
        """Retrieve a FEC export.

        Scope: ``exports:fec``.
        Reference: https://firm-pennylane.readme.io/reference/getfecexport
        """
        return await self._get(
            f"/companies/{company_id}/exports/fecs/{export_id}", cast_to=FecExport
        )


class AsyncFirmAnalyticalGeneralLedgerExports(AsyncAPIResource):
    """Manage Analytical General Ledger exports (async)."""

    async def create(
        self,
        company_id: int,
        *,
        period_start: dt.date | str,
        period_end: dt.date | str,
        mode: str | None = None,
    ) -> AnalyticalGeneralLedgerExport:
        """Create an Analytical General Ledger export.

        Scope: ``exports:agl``.
        Reference: https://firm-pennylane.readme.io/reference/postanalyticalgeneralledgerexport
        """
        body = {"period_start": str(period_start), "period_end": str(period_end)}
        if mode is not None:
            body["mode"] = mode
        return await self._post(
            f"/companies/{company_id}/exports/analytical_general_ledgers",
            cast_to=AnalyticalGeneralLedgerExport,
            body=body,
        )

    async def get(self, company_id: int, export_id: int) -> AnalyticalGeneralLedgerExport:
        """Retrieve an Analytical General Ledger export.

        Scope: ``exports:agl``.
        Reference: https://firm-pennylane.readme.io/reference/getanalyticalgeneralledgerexport
        """
        return await self._get(
            f"/companies/{company_id}/exports/analytical_general_ledgers/{export_id}",
            cast_to=AnalyticalGeneralLedgerExport,
        )


class AsyncFirmExports(AsyncAPIResource):
    """Namespace for company data exports (FEC, Analytical General Ledger), async."""

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.fecs = AsyncFirmFecExports(client)
        self.analytical_general_ledgers = AsyncFirmAnalyticalGeneralLedgerExports(client)
