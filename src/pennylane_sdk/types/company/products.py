"""Models for the Products resource (Company API v2)."""

from __future__ import annotations

import datetime as dt

from ..._models import Money, PennylaneModel

__all__ = ["Product", "ProductLedgerAccount"]


class ProductLedgerAccount(PennylaneModel):
    """Ledger account associated with a product."""

    id: int | None = None


class Product(PennylaneModel):
    """A product from the company catalog.

    Reference: https://pennylane.readme.io/reference/getproduct
    """

    id: int
    label: str | None = None
    description: str | None = None
    external_reference: str | None = None
    price_before_tax: Money | None = None
    vat_rate: str | None = None
    price: Money | None = None
    unit: str | None = None
    currency: str | None = None
    reference: str | None = None
    ledger_account: ProductLedgerAccount | None = None
    archived_at: dt.datetime | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
