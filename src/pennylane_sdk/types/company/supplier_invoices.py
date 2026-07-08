"""Models for the Supplier invoices resource (Company API v2)."""

from __future__ import annotations

import datetime as dt

from pydantic import Field, model_validator

from ..._models import Money, PennylaneModel

__all__ = [
    "ImputationDates",
    "InvoiceLine",
    "LinkedFlow",
    "MatchedTransaction",
    "MatchedTransactionBankAccount",
    "MatchedTransactionEmployee",
    "MatchedTransactionJournal",
    "MatchedTransactionProAccountExpense",
    "Payment",
    "ResourceLink",
    "SupplierEInvoiceImportResult",
    "SupplierInvoice",
    "SupplierInvoiceCategoriesResponse",
    "SupplierInvoiceCategory",
    "SupplierInvoiceCategoryGroup",
    "SupplierInvoiceEInvoicing",
    "SupplierInvoiceLedgerEntry",
    "SupplierInvoiceSupplier",
    "TransactionReference",
]


class ResourceLink(PennylaneModel):
    """A ``{"url": ...}`` pointer to a sub-resource collection."""

    url: str | None = None


class SupplierInvoiceLedgerEntry(PennylaneModel):
    """The ledger entry booked for a supplier invoice."""

    id: int | None = None


class SupplierInvoiceSupplier(PennylaneModel):
    """Supplier snippet embedded in a supplier invoice."""

    id: int | None = None
    url: str | None = None


class TransactionReference(PennylaneModel):
    """Automatic bank-transaction reconciliation reference."""

    banking_provider: str | None = None
    provider_field_name: str | None = None
    provider_field_value: str | None = None


class LinkedFlow(PennylaneModel):
    """The AFNOR flow associated with an e-invoice."""

    id: str | None = None


class SupplierInvoiceEInvoicing(PennylaneModel):
    """E-invoicing lifecycle information managed by the PA."""

    status: str | None = None
    reason: str | None = None
    flow: LinkedFlow | None = None
    source_file_url: str | None = None


class SupplierInvoice(PennylaneModel):
    """A supplier invoice.

    Reference: https://pennylane.readme.io/reference/getsupplierinvoice
    """

    id: int
    label: str | None = None
    invoice_number: str | None = None
    currency: str | None = None
    amount: Money | None = None
    currency_amount: Money | None = None
    currency_amount_before_tax: Money | None = None
    exchange_rate: Money | None = None
    date: dt.date | None = None
    deadline: dt.date | None = None
    currency_tax: Money | None = None
    tax: Money | None = None
    reconciled: bool | None = None
    accounting_status: str | None = None
    filename: str | None = None
    public_file_url: str | None = None
    remaining_amount_with_tax: Money | None = None
    remaining_amount_without_tax: Money | None = None
    ledger_entry: SupplierInvoiceLedgerEntry | None = None
    supplier: SupplierInvoiceSupplier | None = None
    invoice_lines: ResourceLink | None = None
    categories: ResourceLink | None = None
    transaction_reference: TransactionReference | None = None
    payment_status: str | None = None
    paid: bool | None = None
    payments: ResourceLink | None = None
    matched_transactions: ResourceLink | None = None
    external_reference: str | None = None
    e_invoicing: SupplierInvoiceEInvoicing | None = None
    archived_at: dt.datetime | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class ImputationDates(PennylaneModel):
    """The accounting period an invoice line should be imputed to."""

    start_date: dt.date | None = None
    end_date: dt.date | None = None


class InvoiceLine(PennylaneModel):
    """An invoice line of a supplier invoice.

    Reference: https://pennylane.readme.io/reference/getsupplierinvoicelines
    """

    id: int
    label: str | None = None
    amount: Money | None = None
    currency_amount: Money | None = None
    description: str | None = None
    vat_rate: str | None = None
    currency_amount_before_tax: Money | None = None
    currency_tax: Money | None = None
    tax: Money | None = None
    imputation_dates: ImputationDates | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class SupplierInvoiceCategoryGroup(PennylaneModel):
    """Category group of an analytical category."""

    id: int | None = None


class SupplierInvoiceCategory(PennylaneModel):
    """A category weight assigned to a supplier invoice (or a bank transaction).

    Reference: https://pennylane.readme.io/reference/getsupplierinvoicecategories
    """

    id: int
    label: str | None = None
    weight: Money | None = None
    category_group: SupplierInvoiceCategoryGroup | None = None
    analytical_code: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class SupplierInvoiceCategoriesResponse(PennylaneModel):
    """Response of the categorize endpoint (a bare JSON array of categories).

    Not an API object in its own right: a thin wrapper so the bare JSON
    array returned by ``PUT /supplier_invoices/{id}/categories`` can be
    parsed through the standard ``cast_to`` machinery.
    """

    items: list[SupplierInvoiceCategory] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def _wrap_bare_list(cls, data: object) -> object:
        if isinstance(data, list):
            return {"items": data}
        return data


class Payment(PennylaneModel):
    """A payment recorded against a supplier invoice.

    Reference: https://pennylane.readme.io/reference/getsupplierinvoicepayments
    """

    id: int
    label: str | None = None
    currency: str | None = None
    currency_amount: Money | None = None
    status: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class MatchedTransactionJournal(PennylaneModel):
    """Journal snippet of a matched bank transaction."""

    id: int | None = None


class MatchedTransactionBankAccount(PennylaneModel):
    """Bank account snippet of a matched bank transaction."""

    id: int | None = None
    url: str | None = None


class MatchedTransactionEmployee(PennylaneModel):
    """Employee snippet of a pro account expense."""

    id: int | None = None
    first_name: str | None = None
    last_name: str | None = None


class MatchedTransactionProAccountExpense(PennylaneModel):
    """Pro account expense details of a matched bank transaction."""

    employee: MatchedTransactionEmployee | None = None
    card_masked_number: str | None = None


class MatchedTransaction(PennylaneModel):
    """A bank transaction matched to a supplier invoice.

    Reference: https://pennylane.readme.io/reference/getsupplierinvoicematchedtransactions
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
    journal: MatchedTransactionJournal | None = None
    bank_account: MatchedTransactionBankAccount | None = None
    pro_account_expense: MatchedTransactionProAccountExpense | None = None
    supplier: SupplierInvoiceSupplier | None = None
    categories: list[SupplierInvoiceCategory] | None = None


class SupplierEInvoiceImportResult(PennylaneModel):
    """Response of the supplier e-invoice import endpoint."""

    id: int
    url: str | None = None
