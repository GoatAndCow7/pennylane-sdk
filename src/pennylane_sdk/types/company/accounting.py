"""Models for the Trial Balance and Fiscal Years resources (Company API v2)."""

from __future__ import annotations

import datetime as dt

from ..._models import Money, PennylaneModel

__all__ = ["FiscalYear", "TrialBalanceRow"]


class TrialBalanceRow(PennylaneModel):
    """A single ledger account row of the trial balance.

    Reference: https://pennylane.readme.io/reference/gettrialbalance
    """

    number: str | None = None
    formatted_number: str | None = None
    label: str | None = None
    debits: Money | None = None
    credits: Money | None = None


class FiscalYear(PennylaneModel):
    """A company fiscal year.

    Reference: https://pennylane.readme.io/reference/company-fiscal-years
    """

    id: int
    start: dt.date | None = None
    finish: dt.date | None = None
    status: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
