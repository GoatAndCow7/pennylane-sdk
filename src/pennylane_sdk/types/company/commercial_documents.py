"""Models for the Commercial Documents resource (Company API v2)."""

from __future__ import annotations

import datetime as dt

from ..._models import Money, PennylaneModel

__all__ = [
    "CommercialDocument",
    "CommercialDocumentAppendix",
    "CommercialDocumentCustomer",
    "CommercialDocumentDiscount",
    "CommercialDocumentInvoiceLine",
    "CommercialDocumentInvoiceLineProduct",
    "CommercialDocumentInvoiceLineSection",
    "CommercialDocumentLink",
    "CommercialDocumentQuote",
    "CommercialDocumentTemplate",
]


class CommercialDocumentDiscount(PennylaneModel):
    """Discount applied to a commercial document or an invoice line."""

    type: str | None = None
    value: Money | None = None


class CommercialDocumentCustomer(PennylaneModel):
    """Customer linked to a commercial document."""

    id: int | None = None
    url: str | None = None


class CommercialDocumentLink(PennylaneModel):
    """URL to a related sub-collection of a commercial document."""

    url: str | None = None


class CommercialDocumentQuote(PennylaneModel):
    """Quote linked to a commercial document."""

    id: int | None = None
    url: str | None = None


class CommercialDocumentTemplate(PennylaneModel):
    """Template used to generate a commercial document."""

    id: int | None = None


class CommercialDocument(PennylaneModel):
    """A commercial document (proforma, shipping order, purchasing order).

    Reference: https://pennylane.readme.io/reference/getcommercialdocument
    """

    id: int
    label: str | None = None
    document_number: str | None = None
    document_type: str | None = None
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
    discount: CommercialDocumentDiscount | None = None
    public_file_url: str | None = None
    filename: str | None = None
    special_mention: str | None = None
    customer: CommercialDocumentCustomer | None = None
    invoice_line_sections: CommercialDocumentLink | None = None
    invoice_lines: CommercialDocumentLink | None = None
    quote: CommercialDocumentQuote | None = None
    pdf_invoice_free_text: str | None = None
    pdf_invoice_subject: str | None = None
    pdf_description: str | None = None
    commercial_document_template: CommercialDocumentTemplate | None = None
    appendices: CommercialDocumentLink | None = None
    external_reference: str | None = None
    archived_at: dt.datetime | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class CommercialDocumentAppendix(PennylaneModel):
    """A file appendix attached to a commercial document."""

    id: int
    url: str | None = None
    filename: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class CommercialDocumentInvoiceLineProduct(PennylaneModel):
    """Product referenced by a commercial document invoice line."""

    id: int | None = None
    url: str | None = None


class CommercialDocumentInvoiceLine(PennylaneModel):
    """An invoice line of a commercial document."""

    id: int
    label: str | None = None
    unit: str | None = None
    quantity: Money | None = None
    amount: Money | None = None
    currency_amount: Money | None = None
    description: str | None = None
    product: CommercialDocumentInvoiceLineProduct | None = None
    vat_rate: str | None = None
    currency_amount_before_tax: Money | None = None
    currency_tax: Money | None = None
    tax: Money | None = None
    raw_currency_unit_price: Money | None = None
    discount: CommercialDocumentDiscount | None = None
    section_rank: int | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class CommercialDocumentInvoiceLineSection(PennylaneModel):
    """An invoice line section of a commercial document."""

    id: int
    title: str | None = None
    description: str | None = None
    rank: int | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
