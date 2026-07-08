"""Models for the Companies resource (Firm API v1)."""

from __future__ import annotations

from ..._models import PennylaneModel

__all__ = ["FirmCompany"]


class FirmCompany(PennylaneModel):
    """A company managed by the accounting firm.

    Reference: https://firm-pennylane.readme.io/reference/company
    """

    id: int
    name: str | None = None
    billing_company_name: str | None = None
    siren: str | None = None
    address: str | None = None
    city: str | None = None
    postal_code: str | None = None
    activity_nomenclature: str | None = None
    activity_code: str | None = None
    external_id: str | None = None
    client_code: str | None = None
