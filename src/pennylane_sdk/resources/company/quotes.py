"""Quotes resource (Company API v2).

Reference: https://pennylane.readme.io/reference/getquotes
"""

from __future__ import annotations

import datetime as dt
from typing import Any

from ..._files import FileInput, to_httpx_file
from ..._models import drop_none
from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...filters import FiltersInput
from ...types.company.quotes import (
    Quote,
    QuoteAppendix,
    QuoteInvoiceLine,
    QuoteInvoiceLineSection,
)

__all__ = ["AsyncQuotes", "Quotes"]


class Quotes(SyncAPIResource):
    """Manage quotes."""

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[Quote]:
        """List quotes.

        Scope: ``quotes:readonly``.
        Reference: https://pennylane.readme.io/reference/listquotes

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            "/quotes",
            item_type=Quote,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    def get(self, quote_id: int) -> Quote:
        """Retrieve a quote by its Pennylane identifier.

        Scope: ``quotes:readonly``.
        Reference: https://pennylane.readme.io/reference/getquote
        """
        return self._get(f"/quotes/{quote_id}", cast_to=Quote)

    def create(
        self,
        *,
        date: dt.date | str,
        deadline: dt.date | str,
        customer_id: int,
        invoice_lines: list[dict[str, Any]],
        quote_template_id: int | None = None,
        pdf_invoice_free_text: str | None = None,
        pdf_invoice_subject: str | None = None,
        pdf_description: str | None = None,
        currency: str | None = None,
        special_mention: str | None = None,
        language: str | None = None,
        discount: dict[str, Any] | None = None,
        invoice_line_sections: list[dict[str, Any]] | None = None,
        external_reference: str | None = None,
    ) -> Quote:
        """Create a quote.

        Scope: ``quotes:all``.
        Reference: https://pennylane.readme.io/reference/postquotes

        Args:
            date: Quote date (ISO 8601).
            deadline: Quote validity deadline (ISO 8601).
            customer_id: Customer identifier.
            invoice_lines: Invoice lines. Each item is either a product-based line
                (``{"product_id": ..., "quantity": ..., ...}``) or a standard line
                (``{"label": ..., "quantity": ..., "raw_currency_unit_price": ...,
                "vat_rate": ..., ...}``).
            quote_template_id: The quote template ID.
            pdf_invoice_free_text: For example, the contact details of the person to contact.
            pdf_invoice_subject: Quote title.
            pdf_description: Quote description.
            currency: ISO currency code (default EUR).
            special_mention: Additional details.
            language: Document language (``fr_FR``, ``en_GB`` or ``de_DE``).
            discount: ``{"type": "absolute" | "relative", "value": "..."}``.
            invoice_line_sections: Sections used to group invoice lines, each with a
                ``rank`` and optional ``title`` / ``description``.
            external_reference: A unique external reference you can provide to track
                this quote. If not provided, Pennylane generates one.
        """
        body = drop_none(
            {
                "date": date,
                "deadline": deadline,
                "customer_id": customer_id,
                "invoice_lines": invoice_lines,
                "quote_template_id": quote_template_id,
                "pdf_invoice_free_text": pdf_invoice_free_text,
                "pdf_invoice_subject": pdf_invoice_subject,
                "pdf_description": pdf_description,
                "currency": currency,
                "special_mention": special_mention,
                "language": language,
                "discount": discount,
                "invoice_line_sections": invoice_line_sections,
                "external_reference": external_reference,
            }
        )
        return self._post("/quotes", cast_to=Quote, body=body)

    def update(
        self,
        quote_id: int,
        *,
        date: dt.date | str | None = None,
        deadline: dt.date | str | None = None,
        customer_id: int | None = None,
        quote_template_id: int | None = None,
        pdf_invoice_free_text: str | None = None,
        pdf_invoice_subject: str | None = None,
        pdf_description: str | None = None,
        currency: str | None = None,
        special_mention: str | None = None,
        discount: dict[str, Any] | None = None,
        language: str | None = None,
        invoice_lines: dict[str, Any] | None = None,
        external_reference: str | None = None,
    ) -> Quote:
        """Update a quote. Only the provided fields are modified.

        Scope: ``quotes:all``.
        Reference: https://pennylane.readme.io/reference/updatequote

        Args:
            invoice_lines: ``{"create": [...], "update": [...], "delete": [...]}`` —
                add, update or delete invoice lines. ``update``/``delete`` entries
                require an ``id``; ``create`` entries follow the same shape as in
                :meth:`create`.
            (see :meth:`create` for the other arguments)
        """
        body = drop_none(
            {
                "date": date,
                "deadline": deadline,
                "customer_id": customer_id,
                "quote_template_id": quote_template_id,
                "pdf_invoice_free_text": pdf_invoice_free_text,
                "pdf_invoice_subject": pdf_invoice_subject,
                "pdf_description": pdf_description,
                "currency": currency,
                "special_mention": special_mention,
                "discount": discount,
                "language": language,
                "invoice_lines": invoice_lines,
                "external_reference": external_reference,
            }
        )
        return self._put(f"/quotes/{quote_id}", cast_to=Quote, body=body)

    def update_status(self, quote_id: int, *, status: str) -> Quote:
        """Update the status of a quote.

        Scope: ``quotes:all``.
        Reference: https://pennylane.readme.io/reference/updatestatusquote

        Args:
            status: One of ``pending``, ``accepted``, ``denied``, ``invoiced``, ``expired``.
        """
        return self._put(
            f"/quotes/{quote_id}/update_status", cast_to=Quote, body={"status": status}
        )

    def send_by_email(self, quote_id: int, *, recipients: list[str] | None = None) -> None:
        """Send a quote by email.

        Scope: ``quotes:all``.
        Reference: https://pennylane.readme.io/reference/sendbyemailquote

        Args:
            recipients: Email recipients. If empty, the email is sent to the
                recipient email addresses specified on the customer.
        """
        body = drop_none({"recipients": recipients})
        self._post(f"/quotes/{quote_id}/send_by_email", cast_to=None, body=body)

    def list_appendices(
        self,
        quote_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> SyncCursorPage[QuoteAppendix]:
        """List the appendices attached to a quote.

        Scope: ``quotes:readonly``.
        Reference: https://pennylane.readme.io/reference/getquoteappendices
        """
        return self._get_page(
            f"/quotes/{quote_id}/appendices",
            item_type=QuoteAppendix,
            params={"cursor": cursor, "limit": limit},
        )

    def add_appendix(
        self, quote_id: int, *, file: FileInput, filename: str | None = None
    ) -> QuoteAppendix:
        """Upload an appendix for a quote.

        Scope: ``quotes:all``.
        Reference: https://pennylane.readme.io/reference/postquoteappendices

        Args:
            file: The appendix file (path, bytes, file-like object or
                ``(filename, content)`` tuple).
            filename: Overrides the filename sent to the API.
        """
        return self._post(
            f"/quotes/{quote_id}/appendices",
            cast_to=QuoteAppendix,
            files={"file": to_httpx_file(file, filename=filename)},
        )

    def list_invoice_lines(
        self,
        quote_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[QuoteInvoiceLine]:
        """List the invoice lines of a quote.

        Scope: ``quotes:readonly``.
        Reference: https://pennylane.readme.io/reference/getquoteinvoicelines
        """
        return self._get_page(
            f"/quotes/{quote_id}/invoice_lines",
            item_type=QuoteInvoiceLine,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    def list_invoice_line_sections(
        self,
        quote_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[QuoteInvoiceLineSection]:
        """List the invoice line sections of a quote.

        Scope: ``quotes:readonly``.
        Reference: https://pennylane.readme.io/reference/getquoteinvoicelinesections
        """
        return self._get_page(
            f"/quotes/{quote_id}/invoice_line_sections",
            item_type=QuoteInvoiceLineSection,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )


class AsyncQuotes(AsyncAPIResource):
    """Manage quotes (async)."""

    async def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[Quote]:
        """List quotes.

        Scope: ``quotes:readonly``.
        Reference: https://pennylane.readme.io/reference/listquotes
        """
        return await self._get_page(
            "/quotes",
            item_type=Quote,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    async def get(self, quote_id: int) -> Quote:
        """Retrieve a quote by its Pennylane identifier.

        Scope: ``quotes:readonly``.
        Reference: https://pennylane.readme.io/reference/getquote
        """
        return await self._get(f"/quotes/{quote_id}", cast_to=Quote)

    async def create(
        self,
        *,
        date: dt.date | str,
        deadline: dt.date | str,
        customer_id: int,
        invoice_lines: list[dict[str, Any]],
        quote_template_id: int | None = None,
        pdf_invoice_free_text: str | None = None,
        pdf_invoice_subject: str | None = None,
        pdf_description: str | None = None,
        currency: str | None = None,
        special_mention: str | None = None,
        language: str | None = None,
        discount: dict[str, Any] | None = None,
        invoice_line_sections: list[dict[str, Any]] | None = None,
        external_reference: str | None = None,
    ) -> Quote:
        """Create a quote.

        Scope: ``quotes:all``.
        Reference: https://pennylane.readme.io/reference/postquotes
        """
        body = drop_none(
            {
                "date": date,
                "deadline": deadline,
                "customer_id": customer_id,
                "invoice_lines": invoice_lines,
                "quote_template_id": quote_template_id,
                "pdf_invoice_free_text": pdf_invoice_free_text,
                "pdf_invoice_subject": pdf_invoice_subject,
                "pdf_description": pdf_description,
                "currency": currency,
                "special_mention": special_mention,
                "language": language,
                "discount": discount,
                "invoice_line_sections": invoice_line_sections,
                "external_reference": external_reference,
            }
        )
        return await self._post("/quotes", cast_to=Quote, body=body)

    async def update(
        self,
        quote_id: int,
        *,
        date: dt.date | str | None = None,
        deadline: dt.date | str | None = None,
        customer_id: int | None = None,
        quote_template_id: int | None = None,
        pdf_invoice_free_text: str | None = None,
        pdf_invoice_subject: str | None = None,
        pdf_description: str | None = None,
        currency: str | None = None,
        special_mention: str | None = None,
        discount: dict[str, Any] | None = None,
        language: str | None = None,
        invoice_lines: dict[str, Any] | None = None,
        external_reference: str | None = None,
    ) -> Quote:
        """Update a quote. Only the provided fields are modified.

        Scope: ``quotes:all``.
        Reference: https://pennylane.readme.io/reference/updatequote
        """
        body = drop_none(
            {
                "date": date,
                "deadline": deadline,
                "customer_id": customer_id,
                "quote_template_id": quote_template_id,
                "pdf_invoice_free_text": pdf_invoice_free_text,
                "pdf_invoice_subject": pdf_invoice_subject,
                "pdf_description": pdf_description,
                "currency": currency,
                "special_mention": special_mention,
                "discount": discount,
                "language": language,
                "invoice_lines": invoice_lines,
                "external_reference": external_reference,
            }
        )
        return await self._put(f"/quotes/{quote_id}", cast_to=Quote, body=body)

    async def update_status(self, quote_id: int, *, status: str) -> Quote:
        """Update the status of a quote.

        Scope: ``quotes:all``.
        Reference: https://pennylane.readme.io/reference/updatestatusquote
        """
        return await self._put(
            f"/quotes/{quote_id}/update_status", cast_to=Quote, body={"status": status}
        )

    async def send_by_email(self, quote_id: int, *, recipients: list[str] | None = None) -> None:
        """Send a quote by email.

        Scope: ``quotes:all``.
        Reference: https://pennylane.readme.io/reference/sendbyemailquote
        """
        body = drop_none({"recipients": recipients})
        await self._post(f"/quotes/{quote_id}/send_by_email", cast_to=None, body=body)

    async def list_appendices(
        self,
        quote_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> AsyncCursorPage[QuoteAppendix]:
        """List the appendices attached to a quote.

        Scope: ``quotes:readonly``.
        Reference: https://pennylane.readme.io/reference/getquoteappendices
        """
        return await self._get_page(
            f"/quotes/{quote_id}/appendices",
            item_type=QuoteAppendix,
            params={"cursor": cursor, "limit": limit},
        )

    async def add_appendix(
        self, quote_id: int, *, file: FileInput, filename: str | None = None
    ) -> QuoteAppendix:
        """Upload an appendix for a quote.

        Scope: ``quotes:all``.
        Reference: https://pennylane.readme.io/reference/postquoteappendices
        """
        return await self._post(
            f"/quotes/{quote_id}/appendices",
            cast_to=QuoteAppendix,
            files={"file": to_httpx_file(file, filename=filename)},
        )

    async def list_invoice_lines(
        self,
        quote_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[QuoteInvoiceLine]:
        """List the invoice lines of a quote.

        Scope: ``quotes:readonly``.
        Reference: https://pennylane.readme.io/reference/getquoteinvoicelines
        """
        return await self._get_page(
            f"/quotes/{quote_id}/invoice_lines",
            item_type=QuoteInvoiceLine,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    async def list_invoice_line_sections(
        self,
        quote_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[QuoteInvoiceLineSection]:
        """List the invoice line sections of a quote.

        Scope: ``quotes:readonly``.
        Reference: https://pennylane.readme.io/reference/getquoteinvoicelinesections
        """
        return await self._get_page(
            f"/quotes/{quote_id}/invoice_line_sections",
            item_type=QuoteInvoiceLineSection,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )
