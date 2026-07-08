"""Models for the Ledger Accounts resource (Company API v2)."""

from __future__ import annotations

import datetime as dt

from ..._models import PennylaneModel

__all__ = ["LedgerAccount"]


class LedgerAccount(PennylaneModel):
    """A ledger account of the company's chart of accounts.

    Reference: https://pennylane.readme.io/reference/getledgeraccount
    """

    id: int
    number: str | None = None
    label: str | None = None
    vat_rate: str | None = None
    country_alpha2: str | None = None
    enabled: bool | None = None
    type: str | None = None
    letterable: bool | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
