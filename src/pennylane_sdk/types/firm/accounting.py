"""Models for the Firm accounting resources (Firm API v1).

Covers fiscal years, trial balance, journals, ledger accounts, ledger
entries and ledger entry lines.
"""

from __future__ import annotations

import datetime as dt

from ..._models import Money, PennylaneModel

__all__ = [
    "FirmFiscalYear",
    "FirmJournal",
    "FirmLedgerAccount",
    "FirmLedgerEntry",
    "FirmLedgerEntryCategory",
    "FirmLedgerEntryCategoryGroup",
    "FirmLedgerEntryLedgerAccount",
    "FirmLedgerEntryLine",
    "FirmLedgerEntryLineImputationDate",
    "FirmLedgerEntryLineJournal",
    "FirmLedgerEntryLineLedgerEntry",
    "FirmLedgerEntryLineLettering",
    "FirmTrialBalanceRow",
]


class FirmFiscalYear(PennylaneModel):
    """A company's fiscal year.

    Reference: https://firm-pennylane.readme.io/reference/company-fiscal-years
    """

    id: int
    start: dt.date | None = None
    finish: dt.date | None = None
    status: str | None = None


class FirmTrialBalanceRow(PennylaneModel):
    """One ledger account row of a company's trial balance.

    Reference: https://firm-pennylane.readme.io/reference/company-trial-balance
    """

    number: str | None = None
    label: str | None = None
    debits: Money | None = None
    credits: Money | None = None
    formatted_number: str | None = None


class FirmJournal(PennylaneModel):
    """A company's accounting journal.

    Reference: https://firm-pennylane.readme.io/reference/getjournal
    """

    id: int
    code: str | None = None
    label: str | None = None
    type: str | None = None


class FirmLedgerAccount(PennylaneModel):
    """A company's ledger account.

    Reference: https://firm-pennylane.readme.io/reference/getledgeraccount
    """

    id: int
    number: str | None = None
    label: str | None = None
    vat_rate: str | None = None
    country_alpha2: str | None = None
    enabled: bool | None = None
    letterable: bool | None = None
    archived_at: dt.datetime | None = None


class FirmLedgerEntryLineJournal(PennylaneModel):
    """Journal reference embedded in a ledger entry."""

    id: int | None = None
    url: str | None = None


class FirmLedgerEntryLedgerAccount(PennylaneModel):
    """Ledger account reference embedded in a ledger entry line."""

    id: int | None = None
    number: str | None = None
    url: str | None = None


class FirmLedgerEntryCategoryGroup(PennylaneModel):
    """Category group reference embedded in a ledger entry category."""

    id: int | None = None


class FirmLedgerEntryCategory(PennylaneModel):
    """An analytical category applied to a ledger entry."""

    id: int | None = None
    label: str | None = None
    weight: str | None = None
    category_group: FirmLedgerEntryCategoryGroup | None = None
    analytical_code: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class FirmLedgerEntryAttachment(PennylaneModel):
    """The file attached to a ledger entry."""

    filename: str | None = None
    url: str | None = None


class FirmLedgerEntry(PennylaneModel):
    """An accounting ledger entry.

    Reference: https://firm-pennylane.readme.io/reference/getledgerentry
    """

    id: int
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
    label: str | None = None
    piece_number: str | None = None
    date: dt.date | None = None
    journal: FirmLedgerEntryLineJournal | None = None
    due_date: dt.date | None = None
    invoice_number: str | None = None
    status: str | None = None
    categories: list[FirmLedgerEntryCategory] | None = None
    attachment: FirmLedgerEntryAttachment | None = None


class FirmLedgerEntryLineLedgerEntry(PennylaneModel):
    """Ledger entry reference embedded in a ledger entry line."""

    id: int | None = None
    url: str | None = None


class FirmLedgerEntryLineLettering(PennylaneModel):
    """Ledger entry lines lettered with a given entry line."""

    ids: list[int] | None = None
    url: str | None = None


class FirmLedgerEntryLineImputationDate(PennylaneModel):
    """An imputation period associated with a ledger entry line."""

    start_date: dt.date | None = None
    end_date: dt.date | None = None


class FirmLedgerEntryLine(PennylaneModel):
    """A debit/credit line of a ledger entry.

    Reference: https://firm-pennylane.readme.io/reference/getledgerentryline
    """

    id: int
    debit: Money | None = None
    credit: Money | None = None
    label: str | None = None
    categories: list[FirmLedgerEntryCategory] | None = None
    ledger_account: FirmLedgerEntryLedgerAccount | None = None
    journal: FirmLedgerEntryLineJournal | None = None
    date: dt.date | None = None
    ledger_entry: FirmLedgerEntryLineLedgerEntry | None = None
    lettered_ledger_entry_lines: FirmLedgerEntryLineLettering | None = None
    imputation_dates: list[FirmLedgerEntryLineImputationDate] | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
