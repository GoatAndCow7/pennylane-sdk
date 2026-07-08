"""Models for the Bank Accounts and Bank Establishments resources (Company API v2)."""

from __future__ import annotations

import datetime as dt

from ..._models import Money, PennylaneModel

__all__ = [
    "BankAccount",
    "BankAccountBankEstablishment",
    "BankAccountJournal",
    "BankAccountLedgerAccount",
    "BankEstablishment",
]


class BankAccountBankEstablishment(PennylaneModel):
    """Bank establishment a bank account belongs to."""

    id: int | None = None


class BankAccountJournal(PennylaneModel):
    """Journal a bank account is booked in."""

    id: int | None = None
    url: str | None = None


class BankAccountLedgerAccount(PennylaneModel):
    """Ledger account a bank account is booked on."""

    id: int | None = None
    url: str | None = None


class BankAccount(PennylaneModel):
    """A bank account.

    Reference: https://pennylane.readme.io/reference/getbankaccount
    """

    id: int
    name: str | None = None
    currency: str | None = None
    balance: Money | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
    bank_establishment: BankAccountBankEstablishment | None = None
    journal: BankAccountJournal | None = None
    ledger_account: BankAccountLedgerAccount | None = None


class BankEstablishment(PennylaneModel):
    """A bank establishment.

    Reference: https://pennylane.readme.io/reference/getbankestablishments
    """

    id: int
    name: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
