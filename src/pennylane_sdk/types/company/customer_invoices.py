"""Models for the Customer invoices resource (Company API v2).

The ``CustomerInvoice`` model and its sub-resources (invoice lines, payments,
matched transactions, appendices, categories, custom header fields) are the
richest object graph of the SDK. Small reference models (``IdRef``,
``ResourceLink``...) are shared across several fields to avoid duplication.
"""

from __future__ import annotations

import datetime as dt

from ..._models import Money, PennylaneModel

__all__ = [
    "Appendix",
    "CustomHeaderField",
    "CustomerInvoice",
    "CustomerInvoiceCategory",
    "CustomerInvoiceCustomer",
    "CustomerInvoiceDiscount",
    "CustomerInvoiceEInvoicing",
    "CustomerInvoiceEInvoicingFlow",
    "CustomerInvoiceImportResult",
    "CustomerInvoiceLedgerEntry",
    "IdRef",
    "IdUrlRef",
    "ImputationDates",
    "InvoiceLine",
    "InvoiceLineProduct",
    "InvoiceLineSection",
    "MatchedTransaction",
    "MatchedTransactionBankAccount",
    "MatchedTransactionEmployee",
    "MatchedTransactionJournal",
    "MatchedTransactionProAccountExpense",
    "Payment",
    "ResourceLink",
    "TransactionReference",
]


class ResourceLink(PennylaneModel):
    """A ``{"url": ...}`` pointer to a sub-resource collection."""

    url: str | None = None


class IdRef(PennylaneModel):
    """A bare ``{"id": ...}`` reference to another object."""

    id: int | None = None


class IdUrlRef(PennylaneModel):
    """An ``{"id": ..., "url": ...}`` reference to another object."""

    id: int | None = None
    url: str | None = None


class CustomerInvoiceDiscount(PennylaneModel):
    """A discount applied to an invoice or invoice line."""

    type: str | None = None
    value: Money | None = None


class CustomerInvoiceLedgerEntry(PennylaneModel):
    """The ledger entry booked for an invoice."""

    id: int | None = None


class CustomerInvoiceCustomer(PennylaneModel):
    """Customer snippet embedded in a customer invoice."""

    id: int | None = None
    url: str | None = None


class TransactionReference(PennylaneModel):
    """Automatic bank-transaction reconciliation reference."""

    banking_provider: str | None = None
    provider_field_name: str | None = None
    provider_field_value: str | None = None


class CustomerInvoiceEInvoicingFlow(PennylaneModel):
    """The AFNOR flow associated with an e-invoice."""

    id: str | None = None


class CustomerInvoiceEInvoicing(PennylaneModel):
    """E-invoicing lifecycle information managed by the PA."""

    status: str | None = None
    reason: str | None = None
    flow: CustomerInvoiceEInvoicingFlow | None = None


class CustomerInvoice(PennylaneModel):
    """A customer invoice.

    Reference: https://pennylane.readme.io/reference/getcustomerinvoice
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
    language: str | None = None
    paid: bool | None = None
    status: str | None = None
    discount: CustomerInvoiceDiscount | None = None
    ledger_entry: CustomerInvoiceLedgerEntry | None = None
    public_file_url: str | None = None
    filename: str | None = None
    remaining_amount_with_tax: Money | None = None
    remaining_amount_without_tax: Money | None = None
    draft: bool | None = None
    special_mention: str | None = None
    customer: CustomerInvoiceCustomer | None = None
    invoice_line_sections: ResourceLink | None = None
    invoice_lines: ResourceLink | None = None
    custom_header_fields: ResourceLink | None = None
    categories: ResourceLink | None = None
    pdf_invoice_free_text: str | None = None
    pdf_invoice_subject: str | None = None
    pdf_description: str | None = None
    billing_subscription: IdRef | None = None
    credited_invoice: IdUrlRef | None = None
    customer_invoice_template: IdRef | None = None
    transaction_reference: TransactionReference | None = None
    payments: ResourceLink | None = None
    matched_transactions: ResourceLink | None = None
    appendices: ResourceLink | None = None
    quote: IdRef | None = None
    external_reference: str | None = None
    e_invoicing: CustomerInvoiceEInvoicing | None = None
    factur_x: bool | None = None
    schematron_validation_status: str | None = None
    """Schematron validation result for Factur-X invoices: pending, valid or invalid."""
    archived_at: dt.datetime | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class InvoiceLineProduct(PennylaneModel):
    """Product snippet referenced by an invoice line."""

    id: int | None = None
    url: str | None = None


class ImputationDates(PennylaneModel):
    """The accounting period an invoice line should be imputed to."""

    start_date: dt.date | None = None
    end_date: dt.date | None = None


class InvoiceLine(PennylaneModel):
    """An invoice line of a customer invoice.
    substance: str | None = None

    Reference: https://pennylane.readme.io/reference/getcustomerinvoiceinvoicelines
    """

    id: int
    label: str | None = None
    unit: str | None = None
    quantity: Money | None = None
    amount: Money | None = None
    currency_amount: Money | None = None
    description: str | None = None
    product: InvoiceLineProduct | None = None
    vat_rate: str | None = None
    currency_amount_before_tax: Money | None = None
    currency_tax: Money | None = None
    tax: Money | None = None
    raw_currency_unit_price: Money | None = None
    discount: CustomerInvoiceDiscount | None = None
    section_rank: int | None = None
    imputation_dates: ImputationDates | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class InvoiceLineSection(PennylaneModel):
    """An invoice line section (a group header for invoice lines).

    Reference: https://pennylane.readme.io/reference/getcustomerinvoiceinvoicelinesections
    """

    id: int
    title: str | None = None
    description: str | None = None
    rank: int | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class Payment(PennylaneModel):
    """A payment recorded against a customer invoice.

    Reference: https://pennylane.readme.io/reference/getcustomerinvoicepayments
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


class CustomerInvoiceCategory(PennylaneModel):
    """A category weight assigned to a customer invoice (or a bank transaction).

    Reference: https://pennylane.readme.io/reference/getcustomerinvoicecategories
    """

    id: int
    label: str | None = None
    weight: Money | None = None
    category_group: IdRef | None = None
    analytical_code: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class MatchedTransaction(PennylaneModel):
    """A bank transaction matched to a customer invoice.

    Reference: https://pennylane.readme.io/reference/getcustomerinvoicematchedtransactions
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
    customer: CustomerInvoiceCustomer | None = None
    categories: list[CustomerInvoiceCategory] | None = None


class Appendix(PennylaneModel):
    """A file appended to a customer invoice.

    Reference: https://pennylane.readme.io/reference/getcustomerinvoiceappendices
    """

    id: int
    url: str | None = None
    filename: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class CustomHeaderField(PennylaneModel):
    """A custom header field displayed on a customer invoice.

    Reference: https://pennylane.readme.io/reference/getcustomerinvoicecustomheaderfields
    """

    id: int
    title: str | None = None
    value: str | None = None
    rank: int | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class CustomerInvoiceImportResult(PennylaneModel):
    """Response of the customer e-invoice import endpoint."""

    id: int
    url: str | None = None
