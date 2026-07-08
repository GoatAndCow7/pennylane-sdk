"""Models for the invoicing resources (Firm API v1): customer invoices, supplier
invoices, customers and suppliers.
"""

from __future__ import annotations

import datetime as dt

from ..._models import Money, PennylaneModel

__all__ = [
    "FirmCustomer",
    "FirmCustomerAddress",
    "FirmCustomerInvoice",
    "FirmCustomerInvoiceBillingSubscription",
    "FirmCustomerInvoiceCreditedInvoice",
    "FirmCustomerInvoiceCustomer",
    "FirmCustomerInvoiceCustomerTemplate",
    "FirmCustomerInvoiceDiscount",
    "FirmCustomerInvoiceLedgerEntry",
    "FirmCustomerInvoiceQuote",
    "FirmCustomerInvoiceResourceLink",
    "FirmCustomerInvoiceTransactionReference",
    "FirmCustomerLedgerAccount",
    "FirmCustomerResourceLink",
    "FirmSupplier",
    "FirmSupplierInvoice",
    "FirmSupplierInvoiceLedgerEntry",
    "FirmSupplierInvoiceResourceLink",
    "FirmSupplierInvoiceSupplier",
    "FirmSupplierInvoiceTransactionReference",
    "FirmSupplierLedgerAccount",
    "FirmSupplierPostalAddress",
]


class FirmCustomerInvoiceDiscount(PennylaneModel):
    """Discount applied on a customer invoice."""

    type: str | None = None
    value: str | None = None


class FirmCustomerInvoiceLedgerEntry(PennylaneModel):
    """Ledger entry a customer invoice is booked on."""

    id: int | None = None


class FirmCustomerInvoiceCustomer(PennylaneModel):
    """Customer of a customer invoice."""

    id: int | None = None
    url: str | None = None


class FirmCustomerInvoiceResourceLink(PennylaneModel):
    """A link to a related sub-resource collection of a customer invoice."""

    url: str | None = None


class FirmCustomerInvoiceBillingSubscription(PennylaneModel):
    """Billing subscription at the origin of a customer invoice."""

    id: int | None = None


class FirmCustomerInvoiceCreditedInvoice(PennylaneModel):
    """The credited invoice if the invoice is a credit note."""

    id: int | None = None
    url: str | None = None


class FirmCustomerInvoiceCustomerTemplate(PennylaneModel):
    """Customer invoice template used to generate a customer invoice."""

    id: int | None = None


class FirmCustomerInvoiceTransactionReference(PennylaneModel):
    """Reconciliation reference matching a customer invoice to a transaction."""

    banking_provider: str | None = None
    provider_field_name: str | None = None
    provider_field_value: str | None = None


class FirmCustomerInvoiceQuote(PennylaneModel):
    """The quote at the origin of a customer invoice."""

    id: int | None = None


class FirmCustomerInvoice(PennylaneModel):
    """A customer invoice.

    Reference: https://firm-pennylane.readme.io/reference/getcustomerinvoice
    """

    id: int
    label: str | None = None
    invoice_number: str | None = None
    currency: str | None = None
    amount: Money | None = None
    currency_amount: Money | None = None
    currency_amount_before_tax: Money | None = None
    exchange_rate: str | None = None
    date: dt.date | None = None
    deadline: dt.date | None = None
    currency_tax: Money | None = None
    tax: Money | None = None
    language: str | None = None
    paid: bool | None = None
    status: str | None = None
    discount: FirmCustomerInvoiceDiscount | None = None
    ledger_entry: FirmCustomerInvoiceLedgerEntry | None = None
    public_file_url: str | None = None
    filename: str | None = None
    remaining_amount_with_tax: Money | None = None
    remaining_amount_without_tax: Money | None = None
    draft: bool | None = None
    special_mention: str | None = None
    customer: FirmCustomerInvoiceCustomer | None = None
    invoice_line_sections: FirmCustomerInvoiceResourceLink | None = None
    invoice_lines: FirmCustomerInvoiceResourceLink | None = None
    custom_header_fields: FirmCustomerInvoiceResourceLink | None = None
    categories: FirmCustomerInvoiceResourceLink | None = None
    pdf_invoice_free_text: str | None = None
    pdf_invoice_subject: str | None = None
    pdf_description: str | None = None
    billing_subscription: FirmCustomerInvoiceBillingSubscription | None = None
    credited_invoice: FirmCustomerInvoiceCreditedInvoice | None = None
    customer_invoice_template: FirmCustomerInvoiceCustomerTemplate | None = None
    transaction_reference: FirmCustomerInvoiceTransactionReference | None = None
    payments: FirmCustomerInvoiceResourceLink | None = None
    matched_transactions: FirmCustomerInvoiceResourceLink | None = None
    appendices: FirmCustomerInvoiceResourceLink | None = None
    quote: FirmCustomerInvoiceQuote | None = None
    external_reference: str | None = None
    archived_at: dt.datetime | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class FirmSupplierInvoiceLedgerEntry(PennylaneModel):
    """Ledger entry a supplier invoice is booked on."""

    id: int | None = None


class FirmSupplierInvoiceSupplier(PennylaneModel):
    """Supplier of a supplier invoice."""

    id: int | None = None
    url: str | None = None


class FirmSupplierInvoiceResourceLink(PennylaneModel):
    """A link to a related sub-resource collection of a supplier invoice."""

    url: str | None = None


class FirmSupplierInvoiceTransactionReference(PennylaneModel):
    """Reconciliation reference matching a supplier invoice to a transaction."""

    banking_provider: str | None = None
    provider_field_name: str | None = None
    provider_field_value: str | None = None


class FirmSupplierInvoice(PennylaneModel):
    """A supplier invoice.

    Reference: https://firm-pennylane.readme.io/reference/getsupplierinvoice
    """

    id: int
    label: str | None = None
    invoice_number: str | None = None
    currency: str | None = None
    amount: Money | None = None
    currency_amount: Money | None = None
    currency_amount_before_tax: Money | None = None
    exchange_rate: str | None = None
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
    ledger_entry: FirmSupplierInvoiceLedgerEntry | None = None
    supplier: FirmSupplierInvoiceSupplier | None = None
    invoice_lines: FirmSupplierInvoiceResourceLink | None = None
    categories: FirmSupplierInvoiceResourceLink | None = None
    transaction_reference: FirmSupplierInvoiceTransactionReference | None = None
    payment_status: str | None = None
    payments: FirmSupplierInvoiceResourceLink | None = None
    matched_transactions: FirmSupplierInvoiceResourceLink | None = None
    external_reference: str | None = None
    archived_at: dt.datetime | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class FirmCustomerAddress(PennylaneModel):
    """A billing or delivery address."""

    address: str | None = None
    postal_code: str | None = None
    city: str | None = None
    country_alpha2: str | None = None


class FirmCustomerLedgerAccount(PennylaneModel):
    """Ledger account associated with a customer."""

    id: int | None = None


class FirmCustomerResourceLink(PennylaneModel):
    """A link to a related sub-resource collection of a customer."""

    url: str | None = None


class FirmCustomer(PennylaneModel):
    """A customer, either a company or an individual.

    Company and individual customers share this response shape:
    ``first_name``/``last_name`` are only set for individual customers.

    Reference: https://firm-pennylane.readme.io/reference/getcustomers
    """

    id: int
    name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    billing_iban: str | None = None
    payment_conditions: str | None = None
    recipient: str | None = None
    phone: str | None = None
    reference: str | None = None
    notes: str | None = None
    vat_number: str | None = None
    reg_no: str | None = None
    ledger_account: FirmCustomerLedgerAccount | None = None
    emails: list[str] | None = None
    billing_address: FirmCustomerAddress | None = None
    delivery_address: FirmCustomerAddress | None = None
    customer_type: str | None = None
    external_reference: str | None = None
    billing_language: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class FirmSupplierPostalAddress(PennylaneModel):
    """A supplier's postal address."""

    address: str | None = None
    postal_code: str | None = None
    city: str | None = None
    country_alpha2: str | None = None


class FirmSupplierLedgerAccount(PennylaneModel):
    """Ledger account associated with a supplier."""

    id: int | None = None


class FirmSupplier(PennylaneModel):
    """A supplier.

    Reference: https://firm-pennylane.readme.io/reference/getsuppliers
    """

    id: int
    name: str | None = None
    establishment_no: str | None = None
    reg_no: str | None = None
    vat_number: str | None = None
    ledger_account: FirmSupplierLedgerAccount | None = None
    emails: list[str] | None = None
    iban: str | None = None
    postal_address: FirmSupplierPostalAddress | None = None
    supplier_payment_method: str | None = None
    supplier_due_date_delay: int | None = None
    supplier_due_date_rule: str | None = None
    external_reference: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
