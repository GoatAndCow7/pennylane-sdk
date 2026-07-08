"""Models for the Customer Invoice Templates resource (Company API v2)."""

from __future__ import annotations

import datetime as dt

from ..._models import PennylaneModel

__all__ = ["CustomerInvoiceTemplate"]


class CustomerInvoiceTemplate(PennylaneModel):
    """A customer invoice template.

    Reference: https://pennylane.readme.io/reference/getcustomerinvoicetemplates
    """

    id: int
    name: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
