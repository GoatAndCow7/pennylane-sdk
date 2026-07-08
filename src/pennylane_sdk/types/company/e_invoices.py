"""Models for the E-Invoices and PA Registrations resources (Company API v2)."""

from __future__ import annotations

import datetime as dt

from ..._models import PennylaneModel

__all__ = ["EInvoiceImport", "PaRegistration"]


class EInvoiceImport(PennylaneModel):
    """Result of an e-invoice import.

    .. deprecated:: Pennylane has deprecated this endpoint.

    Reference: https://pennylane.readme.io/reference/createeinvoiceimport
    """

    id: int
    url: str | None = None


class PaRegistration(PennylaneModel):
    """A Plateforme Agréée (PA) registration record.

    Reference: https://pennylane.readme.io/reference/getparegistrations
    """

    id: int
    siret: str | None = None
    siren: str | None = None
    status: str | None = None
    exchange_direction: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
