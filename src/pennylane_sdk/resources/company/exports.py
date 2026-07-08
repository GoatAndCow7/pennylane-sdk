"""Exports resource (Company API v2).

Reference: https://pennylane.readme.io/reference/exportfec
"""

from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING

from ..._resource import AsyncAPIResource, SyncAPIResource
from ...types.company.exports import (
    AnalyticalGeneralLedgerExport,
    FecExport,
    GeneralLedgerExport,
)

if TYPE_CHECKING:
    from ..._base_client import AsyncAPIClient, SyncAPIClient

__all__ = [
    "AnalyticalGeneralLedgerExports",
    "AsyncAnalyticalGeneralLedgerExports",
    "AsyncExports",
    "AsyncFecExports",
    "AsyncGeneralLedgerExports",
    "Exports",
    "FecExports",
    "GeneralLedgerExports",
]


class FecExports(SyncAPIResource):
    """Manage FEC (Fichier des Ecritures Comptables) exports."""

    def create(
        self,
        *,
        period_start: dt.date | str,
        period_end: dt.date | str,
    ) -> FecExport:
        """Create a FEC export.

        Scope: ``exports:fec``.
        Reference: https://pennylane.readme.io/reference/exportfec

        Args:
            period_start: Start date of the period to export.
            period_end: End date of the period to export.
        """
        body = {"period_start": str(period_start), "period_end": str(period_end)}
        return self._post("/exports/fecs", cast_to=FecExport, body=body)

    def get(self, export_id: int) -> FecExport:
        """Retrieve a FEC export.

        Scope: ``exports:fec``.
        Reference: https://pennylane.readme.io/reference/getfecexport
        """
        return self._get(f"/exports/fecs/{export_id}", cast_to=FecExport)


class GeneralLedgerExports(SyncAPIResource):
    """Manage General Ledger exports."""

    def create(
        self,
        *,
        period_start: dt.date | str,
        period_end: dt.date | str,
    ) -> GeneralLedgerExport:
        """Create a General Ledger export.

        Scope: ``exports:gl``.
        Reference: https://pennylane.readme.io/reference/exportgeneralledger

        Args:
            period_start: Start date of the period to export.
            period_end: End date of the period to export.
        """
        body = {"period_start": str(period_start), "period_end": str(period_end)}
        return self._post("/exports/general_ledgers", cast_to=GeneralLedgerExport, body=body)

    def get(self, export_id: int) -> GeneralLedgerExport:
        """Retrieve a General Ledger export.

        Scope: ``exports:gl``.
        Reference: https://pennylane.readme.io/reference/getgeneralledgerexport
        """
        return self._get(f"/exports/general_ledgers/{export_id}", cast_to=GeneralLedgerExport)


class AnalyticalGeneralLedgerExports(SyncAPIResource):
    """Manage Analytical General Ledger exports."""

    def create(
        self,
        *,
        period_start: dt.date | str,
        period_end: dt.date | str,
        mode: str | None = None,
    ) -> AnalyticalGeneralLedgerExport:
        """Create an Analytical General Ledger export.

        Scope: ``exports:agl``.
        Reference: https://pennylane.readme.io/reference/exportanalyticalgeneralledger

        Args:
            period_start: Start date of the period to export.
            period_end: End date of the period to export.
            mode: Export layout, ``"in_line"`` (default) or ``"in_column"``.
        """
        body = {"period_start": str(period_start), "period_end": str(period_end)}
        if mode is not None:
            body["mode"] = mode
        return self._post(
            "/exports/analytical_general_ledgers",
            cast_to=AnalyticalGeneralLedgerExport,
            body=body,
        )

    def get(self, export_id: int) -> AnalyticalGeneralLedgerExport:
        """Retrieve an Analytical General Ledger export.

        Scope: ``exports:agl``.
        Reference: https://pennylane.readme.io/reference/getanalyticalgeneralledgerexport
        """
        return self._get(
            f"/exports/analytical_general_ledgers/{export_id}",
            cast_to=AnalyticalGeneralLedgerExport,
        )


class Exports(SyncAPIResource):
    """Namespace for company data exports (FEC, General Ledger, Analytical General Ledger)."""

    def __init__(self, client: SyncAPIClient) -> None:
        super().__init__(client)
        self.fecs = FecExports(client)
        self.general_ledgers = GeneralLedgerExports(client)
        self.analytical_general_ledgers = AnalyticalGeneralLedgerExports(client)


class AsyncFecExports(AsyncAPIResource):
    """Manage FEC (Fichier des Ecritures Comptables) exports (async)."""

    async def create(
        self,
        *,
        period_start: dt.date | str,
        period_end: dt.date | str,
    ) -> FecExport:
        """Create a FEC export.

        Scope: ``exports:fec``.
        Reference: https://pennylane.readme.io/reference/exportfec
        """
        body = {"period_start": str(period_start), "period_end": str(period_end)}
        return await self._post("/exports/fecs", cast_to=FecExport, body=body)

    async def get(self, export_id: int) -> FecExport:
        """Retrieve a FEC export.

        Scope: ``exports:fec``.
        Reference: https://pennylane.readme.io/reference/getfecexport
        """
        return await self._get(f"/exports/fecs/{export_id}", cast_to=FecExport)


class AsyncGeneralLedgerExports(AsyncAPIResource):
    """Manage General Ledger exports (async)."""

    async def create(
        self,
        *,
        period_start: dt.date | str,
        period_end: dt.date | str,
    ) -> GeneralLedgerExport:
        """Create a General Ledger export.

        Scope: ``exports:gl``.
        Reference: https://pennylane.readme.io/reference/exportgeneralledger
        """
        body = {"period_start": str(period_start), "period_end": str(period_end)}
        return await self._post(
            "/exports/general_ledgers", cast_to=GeneralLedgerExport, body=body
        )

    async def get(self, export_id: int) -> GeneralLedgerExport:
        """Retrieve a General Ledger export.

        Scope: ``exports:gl``.
        Reference: https://pennylane.readme.io/reference/getgeneralledgerexport
        """
        return await self._get(
            f"/exports/general_ledgers/{export_id}", cast_to=GeneralLedgerExport
        )


class AsyncAnalyticalGeneralLedgerExports(AsyncAPIResource):
    """Manage Analytical General Ledger exports (async)."""

    async def create(
        self,
        *,
        period_start: dt.date | str,
        period_end: dt.date | str,
        mode: str | None = None,
    ) -> AnalyticalGeneralLedgerExport:
        """Create an Analytical General Ledger export.

        Scope: ``exports:agl``.
        Reference: https://pennylane.readme.io/reference/exportanalyticalgeneralledger
        """
        body = {"period_start": str(period_start), "period_end": str(period_end)}
        if mode is not None:
            body["mode"] = mode
        return await self._post(
            "/exports/analytical_general_ledgers",
            cast_to=AnalyticalGeneralLedgerExport,
            body=body,
        )

    async def get(self, export_id: int) -> AnalyticalGeneralLedgerExport:
        """Retrieve an Analytical General Ledger export.

        Scope: ``exports:agl``.
        Reference: https://pennylane.readme.io/reference/getanalyticalgeneralledgerexport
        """
        return await self._get(
            f"/exports/analytical_general_ledgers/{export_id}",
            cast_to=AnalyticalGeneralLedgerExport,
        )


class AsyncExports(AsyncAPIResource):
    """Namespace for company data exports (FEC, General Ledger, Analytical General Ledger), async."""

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.fecs = AsyncFecExports(client)
        self.general_ledgers = AsyncGeneralLedgerExports(client)
        self.analytical_general_ledgers = AsyncAnalyticalGeneralLedgerExports(client)
