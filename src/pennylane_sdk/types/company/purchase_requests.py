"""Models for the Purchase requests resource (Company API v2)."""

from __future__ import annotations

import datetime as dt

from ..._models import Money, PennylaneModel

__all__ = [
    "LinkedInvoice",
    "LinkedInvoices",
    "PurchaseOrderFile",
    "PurchaseRequest",
    "PurchaseRequestDeliveryAddress",
    "PurchaseRequestSupplier",
]


class PurchaseRequestSupplier(PennylaneModel):
    """Supplier snippet embedded in a purchase request."""

    id: int | None = None
    url: str | None = None


class PurchaseRequestDeliveryAddress(PennylaneModel):
    """Delivery address of a purchase request."""

    address: str | None = None
    postal_code: str | None = None
    city: str | None = None
    country_alpha2: str | None = None


class PurchaseOrderFile(PennylaneModel):
    """The purchase order file attached to a purchase request."""

    filename: str | None = None
    url: str | None = None


class LinkedInvoice(PennylaneModel):
    """A supplier invoice linked to a purchase request."""

    id: int | None = None
    url: str | None = None


class LinkedInvoices(PennylaneModel):
    """Supplier invoices linked to a purchase request."""

    items: list[LinkedInvoice] | None = None


class PurchaseRequest(PennylaneModel):
    """A purchase request.

    Reference: https://pennylane.readme.io/reference/getpurchaserequest
    """

    id: int
    purchase_order_number: str | None = None
    supplier: PurchaseRequestSupplier | None = None
    delivery_address: PurchaseRequestDeliveryAddress | None = None
    status: str | None = None
    currency: str | None = None
    reason: str | None = None
    estimated_delivery_date: dt.date | None = None
    amount: Money | None = None
    currency_amount: Money | None = None
    currency_amount_before_tax: Money | None = None
    exchange_rate: Money | None = None
    currency_tax: Money | None = None
    tax: Money | None = None
    purchase_order: PurchaseOrderFile | None = None
    linked_invoices: LinkedInvoices | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
