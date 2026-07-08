"""Models for the Quotes resource (Company API v2)."""

from __future__ import annotations

import datetime as dt

from ..._models import Money, PennylaneModel

__all__ = [
    "Quote",
    "QuoteAppendix",
    "QuoteCustomer",
    "QuoteDiscount",
    "QuoteInvoiceLine",
    "QuoteInvoiceLineProduct",
    "QuoteInvoiceLineSection",
    "QuoteLink",
    "QuoteTemplate",
]


class QuoteDiscount(PennylaneModel):
    """Discount applied to a quote or an invoice line."""

    type: str | None = None
    value: Money | None = None


class QuoteCustomer(PennylaneModel):
    """Customer linked to a quote."""

    id: int | None = None
    url: str | None = None


class QuoteLink(PennylaneModel):
    """URL to a related sub-collection of a quote."""

    url: str | None = None


class QuoteTemplate(PennylaneModel):
    """Quote template used to generate a quote."""

    id: int | None = None


class Quote(PennylaneModel):
    """A quote.

    Reference: https://pennylane.readme.io/reference/getquote
    """

    id: int
    label: str | None = None
    quote_number: str | None = None
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
    status: str | None = None
    discount: QuoteDiscount | None = None
    public_file_url: str | None = None
    filename: str | None = None
    special_mention: str | None = None
    customer: QuoteCustomer | None = None
    invoice_line_sections: QuoteLink | None = None
    invoice_lines: QuoteLink | None = None
    linked_invoices: QuoteLink | None = None
    pdf_invoice_free_text: str | None = None
    pdf_invoice_subject: str | None = None
    pdf_description: str | None = None
    quote_template: QuoteTemplate | None = None
    appendices: QuoteLink | None = None
    external_reference: str | None = None
    archived_at: dt.datetime | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class QuoteAppendix(PennylaneModel):
    """A file appendix attached to a quote."""

    id: int
    url: str | None = None
    filename: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class QuoteInvoiceLineProduct(PennylaneModel):
    """Product referenced by a quote invoice line."""

    id: int | None = None
    url: str | None = None


class QuoteInvoiceLine(PennylaneModel):
    """An invoice line of a quote."""

    id: int
    label: str | None = None
    unit: str | None = None
    quantity: Money | None = None
    amount: Money | None = None
    currency_amount: Money | None = None
    description: str | None = None
    product: QuoteInvoiceLineProduct | None = None
    vat_rate: str | None = None
    currency_amount_before_tax: Money | None = None
    currency_tax: Money | None = None
    tax: Money | None = None
    raw_currency_unit_price: Money | None = None
    discount: QuoteDiscount | None = None
    section_rank: int | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class QuoteInvoiceLineSection(PennylaneModel):
    """An invoice line section of a quote."""

    id: int
    title: str | None = None
    description: str | None = None
    rank: int | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
