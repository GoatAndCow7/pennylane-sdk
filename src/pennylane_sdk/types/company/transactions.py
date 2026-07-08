"""Models for the Transactions resource (Company API v2)."""

from __future__ import annotations

import datetime as dt

from pydantic import model_validator

from ..._models import Money, PennylaneModel

__all__ = [
    "MatchedInvoiceLink",
    "MatchedInvoicesLink",
    "Transaction",
    "TransactionBankAccount",
    "TransactionCategoriesResponse",
    "TransactionCategory",
    "TransactionCategoryGroup",
    "TransactionCustomer",
    "TransactionJournal",
    "TransactionProAccountExpense",
    "TransactionProAccountExpenseEmployee",
    "TransactionSupplier",
]


class TransactionJournal(PennylaneModel):
    """Journal a transaction is booked in."""

    id: int | None = None
    url: str | None = None


class TransactionBankAccount(PennylaneModel):
    """Bank account a transaction belongs to."""

    id: int | None = None
    url: str | None = None


class TransactionProAccountExpenseEmployee(PennylaneModel):
    """Employee attached to a pro account expense."""

    id: int | None = None
    first_name: str | None = None
    last_name: str | None = None


class TransactionProAccountExpense(PennylaneModel):
    """Pro account expense details of a transaction."""

    employee: TransactionProAccountExpenseEmployee | None = None
    card_masked_number: str | None = None


class TransactionCustomer(PennylaneModel):
    """Customer linked to a transaction."""

    id: int | None = None
    url: str | None = None


class TransactionSupplier(PennylaneModel):
    """Supplier linked to a transaction."""

    id: int | None = None
    url: str | None = None


class TransactionCategoryGroup(PennylaneModel):
    """Category group of a transaction category."""

    id: int | None = None


class TransactionCategory(PennylaneModel):
    """Analytical category attached to a transaction.

    Reference: https://pennylane.readme.io/reference/gettransactioncategories
    """

    id: int
    label: str | None = None
    weight: str | None = None
    category_group: TransactionCategoryGroup | None = None
    analytical_code: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class TransactionCategoriesResponse(PennylaneModel):
    """Response of the categorize endpoint (a bare JSON array of categories).

    Not an API object in its own right — a thin wrapper so the bare JSON
    array returned by ``PUT /transactions/{id}/categories`` can be parsed
    through the standard ``cast_to`` machinery.
    """

    items: list[TransactionCategory] = []

    @model_validator(mode="before")
    @classmethod
    def _wrap_bare_list(cls, data: object) -> object:
        if isinstance(data, list):
            return {"items": data}
        return data


class MatchedInvoicesLink(PennylaneModel):
    """Link to the invoices matched to a transaction."""

    url: str | None = None


class MatchedInvoiceLink(PennylaneModel):
    """An invoice matched to a bank transaction.

    Reference: https://pennylane.readme.io/reference/gettransactionmatchedinvoices
    """

    id: int
    type: str | None = None
    url: str | None = None


class Transaction(PennylaneModel):
    """A bank transaction.

    Reference: https://pennylane.readme.io/reference/gettransaction
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
    journal: TransactionJournal | None = None
    bank_account: TransactionBankAccount | None = None
    pro_account_expense: TransactionProAccountExpense | None = None
    customer: TransactionCustomer | None = None
    supplier: TransactionSupplier | None = None
    categories: list[TransactionCategory] | None = None
    matched_invoices: MatchedInvoicesLink | None = None
    interbank_code: str | None = None
