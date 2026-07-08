"""Models for the Ledger Entries and Ledger Attachments resources (Company API v2)."""

from __future__ import annotations

import datetime as dt

from ..._models import Money, PennylaneModel

__all__ = [
    "LedgerAttachment",
    "LedgerEntry",
    "LedgerEntryAttachment",
    "LedgerEntryCategory",
    "LedgerEntryCategoryGroup",
    "LedgerEntryJournal",
    "LedgerEntryLedgerAccount",
    "LedgerEntryLine",
]


class LedgerEntryJournal(PennylaneModel):
    """Journal reference embedded in a ledger entry."""

    id: int | None = None
    url: str | None = None


class LedgerEntryLedgerAccount(PennylaneModel):
    """Ledger account reference embedded in a ledger entry line."""

    id: int | None = None
    number: str | None = None
    url: str | None = None


class LedgerEntryCategoryGroup(PennylaneModel):
    """Category group reference embedded in a ledger entry category."""

    id: int | None = None


class LedgerEntryCategory(PennylaneModel):
    """An analytical category applied to a ledger entry."""

    id: int | None = None
    label: str | None = None
    weight: str | None = None
    category_group: LedgerEntryCategoryGroup | None = None
    analytical_code: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class LedgerEntryAttachment(PennylaneModel):
    """The file attached to a ledger entry."""

    filename: str | None = None
    url: str | None = None


class LedgerEntryLine(PennylaneModel):
    """A debit/credit line of a ledger entry.

    Reference: https://pennylane.readme.io/reference/getledgerentrieslederentrylines
    """

    id: int
    debit: Money | None = None
    credit: Money | None = None
    label: str | None = None
    ledger_account_id: int | None = None
    """Deprecated. Use ``ledger_account.id`` instead."""
    ledger_account: LedgerEntryLedgerAccount | None = None


class LedgerEntry(PennylaneModel):
    """An accounting ledger entry.

    Reference: https://pennylane.readme.io/reference/getledgerentry
    """

    id: int
    label: str | None = None
    piece_number: str | None = None
    date: dt.date | None = None
    due_date: dt.date | None = None
    invoice_number: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
    journal_id: int | None = None
    """Deprecated. Use ``journal.id`` instead."""
    journal: LedgerEntryJournal | None = None
    status: str | None = None
    categories: list[LedgerEntryCategory] | None = None
    ledger_attachment_filename: str | None = None
    """Deprecated. Use ``attachment.filename`` instead."""
    attachment: LedgerEntryAttachment | None = None
    ledger_entry_lines: list[LedgerEntryLine] | None = None


class LedgerAttachment(PennylaneModel):
    """The result of uploading a file to attach to a ledger entry.

    Reference: https://pennylane.readme.io/reference/postledgerattachments

    .. deprecated:: Pennylane has deprecated this endpoint.
    """

    id: int
    url: str | None = None
    filename: str | None = None
