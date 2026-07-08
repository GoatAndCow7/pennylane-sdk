"""Models for the Customers resource (Company API v2)."""

from __future__ import annotations

import datetime as dt

from ..._models import PennylaneModel

__all__ = [
    "Customer",
    "CustomerAddress",
    "CustomerCategory",
    "CustomerCategoryGroup",
    "CustomerContact",
    "CustomerLedgerAccount",
    "CustomerResourceLink",
]


class CustomerAddress(PennylaneModel):
    """A billing or delivery address."""

    address: str | None = None
    postal_code: str | None = None
    city: str | None = None
    country_alpha2: str | None = None


class CustomerLedgerAccount(PennylaneModel):
    """Ledger account associated with a customer."""

    id: int | None = None


class CustomerResourceLink(PennylaneModel):
    """A link to a related sub-resource collection."""

    url: str | None = None


class Customer(PennylaneModel):
    """A customer, either a company or an individual.

    Company and individual customers share this response shape; ``customer_type``
    (present on ``/customers`` list/get responses) discriminates between them, and
    ``first_name``/``last_name`` are only set for individual customers.

    Reference: https://pennylane.readme.io/reference/getcustomer
    """

    id: int
    name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    billing_iban: str | None = None
    payment_conditions: str | None = None
    recipient: str | None = None
    phone: str | None = None
    reference: str | None = None
    notes: str | None = None
    vat_number: str | None = None
    reg_no: str | None = None
    ledger_account: CustomerLedgerAccount | None = None
    emails: list[str] | None = None
    billing_address: CustomerAddress | None = None
    delivery_address: CustomerAddress | None = None
    customer_type: str | None = None
    external_reference: str | None = None
    billing_language: str | None = None
    mandates: CustomerResourceLink | None = None
    pro_account_mandates: CustomerResourceLink | None = None
    contacts: CustomerResourceLink | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class CustomerCategoryGroup(PennylaneModel):
    """Category group a customer category belongs to."""

    id: int | None = None


class CustomerCategory(PennylaneModel):
    """A category assigned to a customer.

    Reference: https://pennylane.readme.io/reference/getcustomercategories
    """

    id: int
    label: str | None = None
    weight: str | None = None
    category_group: CustomerCategoryGroup | None = None
    analytical_code: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class CustomerContact(PennylaneModel):
    """A contact person of a customer.

    Reference: https://pennylane.readme.io/reference/getcustomercontacts
    """

    id: int
    first_name: str | None = None
    last_name: str | None = None
    role: str | None = None
    email: str | None = None
    telephone_number: str | None = None
    mobile_number: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
