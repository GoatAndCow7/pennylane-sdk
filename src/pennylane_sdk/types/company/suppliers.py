"""Models for the Suppliers resource (Company API v2)."""

from __future__ import annotations

import datetime as dt

from ..._models import PennylaneModel

__all__ = [
    "Supplier",
    "SupplierCategory",
    "SupplierCategoryGroup",
    "SupplierLedgerAccount",
    "SupplierPostalAddress",
]


class SupplierPostalAddress(PennylaneModel):
    """A supplier's postal address."""

    address: str | None = None
    postal_code: str | None = None
    city: str | None = None
    country_alpha2: str | None = None


class SupplierLedgerAccount(PennylaneModel):
    """Ledger account associated with a supplier."""

    id: int | None = None


class Supplier(PennylaneModel):
    """A supplier.

    Reference: https://pennylane.readme.io/reference/getsupplier
    """

    id: int
    name: str | None = None
    establishment_no: str | None = None
    reg_no: str | None = None
    vat_number: str | None = None
    ledger_account: SupplierLedgerAccount | None = None
    emails: list[str] | None = None
    iban: str | None = None
    postal_address: SupplierPostalAddress | None = None
    supplier_payment_method: str | None = None
    supplier_due_date_delay: int | None = None
    supplier_due_date_rule: str | None = None
    external_reference: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class SupplierCategoryGroup(PennylaneModel):
    """Category group a supplier category belongs to."""

    id: int | None = None


class SupplierCategory(PennylaneModel):
    """A category assigned to a supplier.

    Reference: https://pennylane.readme.io/reference/getsuppliercategories
    """

    id: int
    label: str | None = None
    weight: str | None = None
    category_group: SupplierCategoryGroup | None = None
    analytical_code: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
