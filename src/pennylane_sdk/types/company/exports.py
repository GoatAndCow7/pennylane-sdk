"""Models for the Exports resource (Company API v2)."""

from __future__ import annotations

import datetime as dt

from ..._models import PennylaneModel

__all__ = ["AnalyticalGeneralLedgerExport", "FecExport", "GeneralLedgerExport"]


class FecExport(PennylaneModel):
    """A FEC (Fichier des Ecritures Comptables) export job.

    Reference: https://pennylane.readme.io/reference/getfecexport
    """

    id: int
    file_url: str | None = None
    status: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class GeneralLedgerExport(PennylaneModel):
    """A General Ledger export job.

    Reference: https://pennylane.readme.io/reference/getgeneralledgerexport
    """

    id: int
    file_url: str | None = None
    status: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class AnalyticalGeneralLedgerExport(PennylaneModel):
    """An Analytical General Ledger export job.

    Reference: https://pennylane.readme.io/reference/getanalyticalgeneralledgerexport
    """

    id: int
    file_url: str | None = None
    status: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
