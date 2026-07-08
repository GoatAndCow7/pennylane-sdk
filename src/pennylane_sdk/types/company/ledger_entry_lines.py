"""Models for the Ledger Entry Lines resource (Company API v2)."""

from __future__ import annotations

import datetime as dt

from ..._models import Money, PennylaneModel

__all__ = [
    "CategorizedLedgerEntryLine",
    "CategorizedLedgerEntryLineResult",
    "LedgerEntryLine",
    "LedgerEntryLineCategory",
    "LedgerEntryLineCategoryGroup",
    "LedgerEntryLineEntry",
    "LedgerEntryLineJournal",
    "LedgerEntryLineLedgerAccount",
    "LetteredLedgerEntryLines",
]


class LedgerEntryLineLedgerAccount(PennylaneModel):
    """Ledger account associated with a ledger entry line."""

    id: int | None = None
    number: str | None = None
    url: str | None = None


class LedgerEntryLineJournal(PennylaneModel):
    """Journal associated with a ledger entry line."""

    id: int | None = None
    url: str | None = None


class LedgerEntryLineEntry(PennylaneModel):
    """Ledger entry associated with a ledger entry line."""

    id: int | None = None


class LetteredLedgerEntryLines(PennylaneModel):
    """Ledger entry lines lettered together with this entry line."""

    ids: list[int] | None = None
    url: str | None = None


class LedgerEntryLineCategoryGroup(PennylaneModel):
    """Category group of an analytical category."""

    id: int | None = None


class LedgerEntryLineCategory(PennylaneModel):
    """Analytical category attached to a ledger entry line."""

    id: int
    label: str | None = None
    weight: str | None = None
    category_group: LedgerEntryLineCategoryGroup | None = None
    analytical_code: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class LedgerEntryLine(PennylaneModel):
    """A ledger entry line.

    Reference: https://pennylane.readme.io/reference/getledgerentryline
    """

    id: int
    debit: Money | None = None
    credit: Money | None = None
    label: str | None = None
    categories: list[LedgerEntryLineCategory] | None = None
    ledger_account: LedgerEntryLineLedgerAccount | None = None
    journal: LedgerEntryLineJournal | None = None
    date: dt.date | None = None
    ledger_entry: LedgerEntryLineEntry | None = None
    lettered_ledger_entry_lines: LetteredLedgerEntryLines | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class CategorizedLedgerEntryLineResult(PennylaneModel):
    """Ledger entry line as returned after (re)assigning its categories."""

    id: int
    label: str | None = None
    categories: list[LedgerEntryLineCategory] | None = None


class CategorizedLedgerEntryLine(PennylaneModel):
    """Response of the categorize endpoint.

    Reference: https://pennylane.readme.io/reference/putledgerentrylinescategories
    """

    ledger_entry_line: CategorizedLedgerEntryLineResult | None = None
