"""Models for the SEPA/GoCardless/Pro Account mandates resources (Company API v2)."""

from __future__ import annotations

import datetime as dt

from ..._models import PennylaneModel

__all__ = [
    "GocardlessMandate",
    "GocardlessMandateCustomer",
    "MandateCustomer",
    "MandateMigration",
    "MandateMigrationCandidate",
    "MandateMigrationCustomer",
    "MandateMigrationMandate",
    "MandateMigrationResponse",
    "ProAccountMandate",
    "SepaMandate",
]


class MandateCustomer(PennylaneModel):
    """Customer reference attached to a mandate."""

    id: int | None = None
    url: str | None = None


class SepaMandate(PennylaneModel):
    """A SEPA direct debit mandate.

    Reference: https://pennylane.readme.io/reference/getsepamandate
    """

    id: int
    bank: str | None = None
    bic: str | None = None
    iban: str | None = None
    sequence_type: str | None = None
    signed_at: dt.date | None = None
    identifier: str | None = None
    customer: MandateCustomer | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class GocardlessMandateCustomer(PennylaneModel):
    """Customer reference attached to a Gocardless mandate."""

    id: int | None = None
    url: str | None = None


class GocardlessMandate(PennylaneModel):
    """A GoCardless direct debit mandate.

    Reference: https://pennylane.readme.io/reference/getgocardlessmandate
    """

    id: int
    external_reference: str | None = None
    customer: GocardlessMandateCustomer | None = None
    status: str | None = None
    external_customer_account: str | None = None
    external_customer_label: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class MandateMigrationMandate(PennylaneModel):
    """Polymorphic mandate reference (SepaMandate or Gocardless mandate)."""

    id: int | None = None
    type: str | None = None


class MandateMigrationCustomer(PennylaneModel):
    """Customer reference attached to a mandate migration."""

    id: int | None = None
    url: str | None = None
    pro_account_mandate: dict[str, object] | None = None


class MandateMigrationCandidate(PennylaneModel):
    """A mandate eligible (or migrated) for Pro Account migration.

    Reference: https://pennylane.readme.io/reference/getproaccountmandatemigrations
    """

    id: int
    status: str | None = None
    direct_debit_method: str | None = None
    signed_at: dt.date | None = None
    error_message: str | None = None
    migrated_at: dt.datetime | None = None
    migration_started_at: dt.datetime | None = None
    mandate: MandateMigrationMandate | None = None
    customer: MandateMigrationCustomer | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class MandateMigration(PennylaneModel):
    """A mandate migration to Pro Account.

    Reference: https://pennylane.readme.io/reference/postproaccountmandatemigrations
    """

    id: int
    status: str | None = None
    direct_debit_method: str | None = None
    signed_at: dt.date | None = None
    error_message: str | None = None
    migrated_at: dt.datetime | None = None
    migration_started_at: dt.datetime | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
    mandate: MandateMigrationMandate | None = None
    customer: MandateMigrationCustomer | None = None


class MandateMigrationResponse(PennylaneModel):
    """Response of ``POST /pro_account/mandate_migrations``.

    Not an API object in its own right — a thin wrapper so the
    ``{"mandate_migration": {...}}`` envelope can be parsed through the
    standard ``cast_to`` machinery.
    """

    mandate_migration: MandateMigration


class ProAccountMandate(PennylaneModel):
    """A Pro Account payment mandate.

    Note: the API does not expose an ``id`` field for this resource.

    Reference: https://pennylane.readme.io/reference/getproaccountmandates
    """

    status: str | None = None
    early_execution_date_permitted: bool | None = None
    active_billing_subscription: bool | None = None
    signed_at: dt.date | None = None
    created_at: dt.datetime | None = None
    pdf_url: str | None = None
    customer: MandateCustomer | None = None
