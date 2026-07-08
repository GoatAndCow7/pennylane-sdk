"""Models for the banking resources (Firm API v1): bank accounts and transactions."""

from __future__ import annotations

import datetime as dt

from ..._models import Money, PennylaneModel

__all__ = [
    "FirmBankAccount",
    "FirmBankAccountBankEstablishment",
    "FirmBankAccountJournal",
    "FirmBankAccountLedgerAccount",
    "FirmTransaction",
    "FirmTransactionBankAccount",
    "FirmTransactionCategory",
    "FirmTransactionCategoryGroup",
    "FirmTransactionCustomer",
    "FirmTransactionEmployee",
    "FirmTransactionJournal",
    "FirmTransactionProAccountExpense",
    "FirmTransactionSupplier",
]


class FirmBankAccountBankEstablishment(PennylaneModel):
    """Bank establishment a bank account belongs to."""

    id: int | None = None


class FirmBankAccountJournal(PennylaneModel):
    """Journal a bank account is booked in."""

    id: int | None = None
    url: str | None = None


class FirmBankAccountLedgerAccount(PennylaneModel):
    """Ledger account a bank account is booked on."""

    id: int | None = None
    url: str | None = None


class FirmBankAccount(PennylaneModel):
    """A bank account of a client company.

    Reference: https://firm-pennylane.readme.io/reference/getbankaccounts
    """

    id: int
    name: str | None = None
    currency: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
    bank_establishment: FirmBankAccountBankEstablishment | None = None
    journal: FirmBankAccountJournal | None = None
    ledger_account: FirmBankAccountLedgerAccount | None = None


class FirmTransactionJournal(PennylaneModel):
    """Journal a transaction is booked in."""

    id: int | None = None
    url: str | None = None


class FirmTransactionBankAccount(PennylaneModel):
    """Bank account a transaction is registered on."""

    id: int | None = None
    url: str | None = None


class FirmTransactionEmployee(PennylaneModel):
    """Employee associated with a pro account expense."""

    id: int | None = None
    first_name: str | None = None
    last_name: str | None = None


class FirmTransactionProAccountExpense(PennylaneModel):
    """Pro account expense details of a transaction."""

    employee: FirmTransactionEmployee | None = None
    card_masked_number: str | None = None


class FirmTransactionCustomer(PennylaneModel):
    """Customer matched to a transaction."""

    id: int | None = None
    url: str | None = None


class FirmTransactionSupplier(PennylaneModel):
    """Supplier matched to a transaction."""

    id: int | None = None
    url: str | None = None


class FirmTransactionCategoryGroup(PennylaneModel):
    """Category group a transaction category belongs to."""

    id: int | None = None


class FirmTransactionCategory(PennylaneModel):
    """A category assigned to a transaction."""

    id: int
    label: str | None = None
    weight: str | None = None
    category_group: FirmTransactionCategoryGroup | None = None
    analytical_code: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class FirmTransaction(PennylaneModel):
    """A bank transaction of a client company.

    Reference: https://firm-pennylane.readme.io/reference/gettransactions
    """

    id: int
    label: str | None = None
    attachment_required: bool | None = None
    date: dt.date | None = None
    outstanding_balance: Money | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
    archived_at: dt.datetime | None = None
    currency: str | None = None
    currency_amount: Money | None = None
    amount: Money | None = None
    currency_fee: Money | None = None
    fee: Money | None = None
    journal: FirmTransactionJournal | None = None
    bank_account: FirmTransactionBankAccount | None = None
    pro_account_expense: FirmTransactionProAccountExpense | None = None
    customer: FirmTransactionCustomer | None = None
    supplier: FirmTransactionSupplier | None = None
    categories: list[FirmTransactionCategory] | None = None
