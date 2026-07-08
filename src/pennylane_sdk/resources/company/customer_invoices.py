"""Customer invoices resource (Company API v2).

Reference: https://pennylane.readme.io/reference/getcustomerinvoices
"""

from __future__ import annotations

import builtins
import datetime as dt
import json
from typing import Any

from ..._files import FileInput, to_httpx_file
from ..._models import MoneyInput, drop_none, jsonable
from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...filters import FiltersInput
from ...types.company.customer_invoices import (
    Appendix,
    CustomerInvoice,
    CustomerInvoiceCategory,
    CustomerInvoiceImportResult,
    CustomHeaderField,
    InvoiceLine,
    InvoiceLineSection,
    MatchedTransaction,
    Payment,
)

__all__ = ["AsyncCustomerInvoices", "CustomerInvoices"]


class CustomerInvoices(SyncAPIResource):
    """Manage customer invoices (French: factures de vente)."""

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
        include: str | None = None,
    ) -> SyncCursorPage[CustomerInvoice]:
        """List customer invoices.

        Scope: ``customer_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomerinvoices

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
            include: Comma-separated list of resources to embed (e.g. ``invoice_lines``).
        """
        return self._get_page(
            "/customer_invoices",
            item_type=CustomerInvoice,
            params={
                "cursor": cursor,
                "limit": limit,
                "filter": filter,
                "sort": sort,
                "include": include,
            },
        )

    def create(
        self,
        *,
        date: dt.date | str,
        deadline: dt.date | str,
        customer_id: int,
        invoice_lines: builtins.list[dict[str, Any]],
        draft: bool = True,
        customer_invoice_template_id: int | None = None,
        pdf_invoice_free_text: str | None = None,
        pdf_invoice_subject: str | None = None,
        pdf_description: str | None = None,
        currency: str | None = None,
        special_mention: str | None = None,
        language: str | None = None,
        discount: dict[str, Any] | None = None,
        invoice_line_sections: builtins.list[dict[str, Any]] | None = None,
        label: str | None = None,
        external_reference: str | None = None,
        transaction_reference: dict[str, Any] | None = None,
    ) -> CustomerInvoice:
        """Create a customer invoice, as a draft or already finalized.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/postcustomerinvoices

        The request body is an ``anyOf`` of two variants:

        - **Draft invoice** (``draft=True``, the default): accepts ``discount``
          and ``label``; ``transaction_reference`` is not allowed.
        - **Finalized invoice** (``draft=False``): accepts ``transaction_reference``
          to auto-reconcile the invoice with a bank transaction; ``discount`` and
          ``label`` are not allowed.

        Args:
            date: Invoice date (ISO 8601).
            deadline: Invoice payment deadline (ISO 8601).
            customer_id: Customer identifier.
            invoice_lines: Invoice lines, each a dict of invoice line fields
                (``label``, ``quantity``, ``raw_currency_unit_price``, ``unit``,
                ``vat_rate``, ``product_id``, ``ledger_account_id``, ``discount``,
                ``imputation_dates``, ``section_rank``...).
            draft: Whether the invoice is created as a draft (default) or finalized.
            customer_invoice_template_id: The customer invoice template ID.
            pdf_invoice_free_text: Free text shown on the PDF (e.g. contact details).
            pdf_invoice_subject: Invoice title.
            pdf_description: Invoice description (max 5,000 characters).
            currency: ISO currency code (default EUR).
            special_mention: Additional details (max 20,000 characters).
            language: Invoice language (``fr_FR``, ``en_GB`` or ``de_DE``).
            discount: ``{"type": "absolute" | "relative", "value": "..."}``: draft only.
            invoice_line_sections: List of ``{"title", "description", "rank"}`` dicts.
            label: Custom label used on accounting (ledger) entries: draft only.
            external_reference: Your own unique reference for this invoice.
            transaction_reference: ``{"banking_provider", "provider_field_name",
                "provider_field_value"}`` to auto-reconcile: finalized only.
        """
        body = drop_none(
            {
                "date": jsonable(date),
                "deadline": jsonable(deadline),
                "customer_id": customer_id,
                "draft": draft,
                "customer_invoice_template_id": customer_invoice_template_id,
                "pdf_invoice_free_text": pdf_invoice_free_text,
                "pdf_invoice_subject": pdf_invoice_subject,
                "pdf_description": pdf_description,
                "currency": currency,
                "special_mention": special_mention,
                "language": language,
                "discount": discount,
                "invoice_line_sections": invoice_line_sections,
                "label": label,
                "external_reference": external_reference,
                "transaction_reference": transaction_reference,
                "invoice_lines": invoice_lines,
            }
        )
        return self._post("/customer_invoices", cast_to=CustomerInvoice, body=body)

    def get(self, customer_invoice_id: int) -> CustomerInvoice:
        """Retrieve a customer invoice by its Pennylane identifier.

        Scope: ``customer_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomerinvoice
        """
        return self._get(f"/customer_invoices/{customer_invoice_id}", cast_to=CustomerInvoice)

    def update(
        self,
        customer_invoice_id: int,
        *,
        date: dt.date | str | None = None,
        deadline: dt.date | str | None = None,
        customer_id: int | None = None,
        customer_invoice_template_id: int | None = None,
        pdf_invoice_free_text: str | None = None,
        pdf_invoice_subject: str | None = None,
        pdf_description: str | None = None,
        currency: str | None = None,
        special_mention: str | None = None,
        discount: dict[str, Any] | None = None,
        language: str | None = None,
        invoice_lines: dict[str, Any] | None = None,
        label: str | None = None,
        external_reference: str | None = None,
        transaction_reference: dict[str, Any] | None = None,
    ) -> CustomerInvoice:
        """Update a customer invoice. Only the provided fields are modified.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/putcustomerinvoice

        The request body is an ``anyOf`` of two variants:

        - **Draft invoice**: accepts ``date``, ``deadline``, ``customer_id``,
          ``customer_invoice_template_id``, ``discount``, ``language`` and
          ``invoice_lines`` as ``{"create": [...], "update": [...], "delete": [...]}``.
        - **Finalized invoice**: only accepts ``label``, ``transaction_reference``,
          ``external_reference`` and ``invoice_lines`` as ``{"update": [...]}``.

        Args:
            invoice_lines: ``{"create": [...], "update": [...], "delete": [...]}``
                (finalized invoices only support ``update``).
            transaction_reference: ``{"banking_provider", "provider_field_name",
                "provider_field_value"}``: finalized invoices only.
        """
        body = drop_none(
            {
                "date": jsonable(date),
                "deadline": jsonable(deadline),
                "customer_id": customer_id,
                "customer_invoice_template_id": customer_invoice_template_id,
                "pdf_invoice_free_text": pdf_invoice_free_text,
                "pdf_invoice_subject": pdf_invoice_subject,
                "pdf_description": pdf_description,
                "currency": currency,
                "special_mention": special_mention,
                "discount": discount,
                "language": language,
                "invoice_lines": invoice_lines,
                "label": label,
                "external_reference": external_reference,
                "transaction_reference": transaction_reference,
            }
        )
        return self._put(
            f"/customer_invoices/{customer_invoice_id}", cast_to=CustomerInvoice, body=body
        )

    def delete(self, customer_invoice_id: int) -> None:
        """Delete a draft customer invoice.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/deletecustomerinvoices
        """
        return self._delete(f"/customer_invoices/{customer_invoice_id}")

    def finalize(self, customer_invoice_id: int) -> CustomerInvoice:
        """Turn a draft invoice into a finalized invoice.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/finalizecustomerinvoice
        """
        return self._put(
            f"/customer_invoices/{customer_invoice_id}/finalize", cast_to=CustomerInvoice
        )

    def mark_as_paid(self, customer_invoice_id: int) -> None:
        """Mark a customer invoice as paid.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/markaspaidcustomerinvoice
        """
        return self._put(f"/customer_invoices/{customer_invoice_id}/mark_as_paid")

    def send_by_email(
        self, customer_invoice_id: int, *, recipients: builtins.list[str] | None = None
    ) -> None:
        """Send a customer invoice by email.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/sendbyemailcustomerinvoice

        Args:
            recipients: Email recipients. If empty, defaults to the recipient
                addresses configured on the customer.
        """
        body = drop_none({"recipients": recipients})
        return self._post(f"/customer_invoices/{customer_invoice_id}/send_by_email", body=body)

    def send_to_pa(self, customer_invoice_id: int) -> None:
        """Send a customer e-invoice to the Partner Platform (PA).

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/sendtopacustomerinvoice
        """
        return self._post(f"/customer_invoices/{customer_invoice_id}/send_to_pa")

    def link_credit_note(self, customer_invoice_id: int, *, credit_note_id: int) -> CustomerInvoice:
        """Link a credit note to a customer invoice.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/linkcreditnote

        Args:
            credit_note_id: The credit note (customer invoice) ID.
        """
        body = {"credit_note_id": credit_note_id}
        return self._post(
            f"/customer_invoices/{customer_invoice_id}/link_credit_note",
            cast_to=CustomerInvoice,
            body=body,
        )

    def update_imported(
        self,
        customer_invoice_id: int,
        *,
        date: dt.date | str | None = None,
        deadline: dt.date | str | None = None,
        customer_id: int | None = None,
        invoice_number: str | None = None,
        currency: str | None = None,
        currency_amount_before_tax: MoneyInput | None = None,
        currency_amount: MoneyInput | None = None,
        amount: MoneyInput | None = None,
        currency_tax: MoneyInput | None = None,
        tax: MoneyInput | None = None,
        transaction_reference: dict[str, Any] | None = None,
        invoice_lines: dict[str, Any] | None = None,
        external_reference: str | None = None,
    ) -> CustomerInvoice:
        """Update an imported customer invoice (whose amounts are set manually).

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/updateimportedcustomerinvoice

        Args:
            invoice_lines: ``{"create": [...], "update": [...], "delete": [...]}``.
        """
        body = drop_none(
            {
                "date": jsonable(date),
                "deadline": jsonable(deadline),
                "customer_id": customer_id,
                "invoice_number": invoice_number,
                "currency": currency,
                "currency_amount_before_tax": jsonable(currency_amount_before_tax),
                "currency_amount": jsonable(currency_amount),
                "amount": jsonable(amount),
                "currency_tax": jsonable(currency_tax),
                "tax": jsonable(tax),
                "transaction_reference": transaction_reference,
                "invoice_lines": invoice_lines,
                "external_reference": external_reference,
            }
        )
        return self._put(
            f"/customer_invoices/{customer_invoice_id}/update_imported",
            cast_to=CustomerInvoice,
            body=body,
        )

    def import_from_file(
        self,
        *,
        file_attachment_id: int,
        date: dt.date | str,
        deadline: dt.date | str,
        customer_id: int,
        currency_amount_before_tax: MoneyInput,
        currency_amount: MoneyInput,
        currency_tax: MoneyInput,
        invoice_lines: builtins.list[dict[str, Any]],
        import_as_incomplete: bool | None = None,
        invoice_number: str | None = None,
        currency: str | None = None,
        amount: MoneyInput | None = None,
        tax: MoneyInput | None = None,
        label: str | None = None,
        transaction_reference: dict[str, Any] | None = None,
    ) -> CustomerInvoice:
        """Import a customer invoice from a previously uploaded file attachment.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/importcustomerinvoices

        Args:
            file_attachment_id: ID of a file uploaded through ``/file_attachments``.
            import_as_incomplete: Set the invoice to ``Incomplete`` status.
            invoice_lines: Invoice lines, each a dict of invoice line fields
                (``currency_amount``, ``currency_tax``, ``quantity``,
                ``raw_currency_unit_price``, ``unit``, ``vat_rate``...).
        """
        body = drop_none(
            {
                "file_attachment_id": file_attachment_id,
                "import_as_incomplete": import_as_incomplete,
                "date": jsonable(date),
                "deadline": jsonable(deadline),
                "customer_id": customer_id,
                "invoice_number": invoice_number,
                "currency": currency,
                "currency_amount_before_tax": jsonable(currency_amount_before_tax),
                "currency_amount": jsonable(currency_amount),
                "amount": jsonable(amount),
                "currency_tax": jsonable(currency_tax),
                "tax": jsonable(tax),
                "label": label,
                "transaction_reference": transaction_reference,
                "invoice_lines": invoice_lines,
            }
        )
        return self._post("/customer_invoices/import", cast_to=CustomerInvoice, body=body)

    def import_e_invoice(
        self,
        *,
        file: FileInput,
        filename: str | None = None,
        invoice_options: dict[str, Any] | None = None,
    ) -> CustomerInvoiceImportResult:
        """Import a customer e-invoice file (Factur-X PDF, UBL XML or CII XML).

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/createcustomerinvoiceeinvoiceimport

        Args:
            file: The e-invoice file (path, bytes or file-like object).
            filename: Overrides the filename sent to the API.
            invoice_options: Optional payload to enrich the imported invoice:
                ``{"customer_id": ..., "invoice_lines": [{"e_invoice_line_id",
                "ledger_account_id", "product_id"}, ...]}``.
        """
        data = None
        if invoice_options is not None:
            data = {"invoice_options": json.dumps(jsonable(invoice_options))}
        return self._post(
            "/customer_invoices/e_invoices/imports",
            cast_to=CustomerInvoiceImportResult,
            files={"file": to_httpx_file(file, filename=filename)},
            data=data,
        )

    def create_from_quote(
        self,
        *,
        quote_id: int,
        draft: bool,
        external_reference: str | None = None,
        customer_invoice_template_id: int | None = None,
    ) -> CustomerInvoice:
        """Create a customer invoice from an accepted quote.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/createcustomerinvoicefromquote

        Args:
            quote_id: Quote identifier to create the invoice from.
            draft: Whether the invoice should be created as a draft.
            external_reference: Your own unique reference for this invoice.
            customer_invoice_template_id: The customer invoice template ID.
        """
        body = drop_none(
            {
                "quote_id": quote_id,
                "draft": draft,
                "external_reference": external_reference,
                "customer_invoice_template_id": customer_invoice_template_id,
            }
        )
        return self._post(
            "/customer_invoices/create_from_quote", cast_to=CustomerInvoice, body=body
        )

    def list_invoice_lines(
        self,
        customer_invoice_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[InvoiceLine]:
        """List the invoice lines of a customer invoice.

        Scope: ``customer_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomerinvoiceinvoicelines
        """
        return self._get_page(
            f"/customer_invoices/{customer_invoice_id}/invoice_lines",
            item_type=InvoiceLine,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    def list_invoice_line_sections(
        self,
        customer_invoice_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[InvoiceLineSection]:
        """List the invoice line sections of a customer invoice.

        Scope: ``customer_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomerinvoiceinvoicelinesections
        """
        return self._get_page(
            f"/customer_invoices/{customer_invoice_id}/invoice_line_sections",
            item_type=InvoiceLineSection,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    def list_payments(
        self,
        customer_invoice_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[Payment]:
        """List the payments of a customer invoice.

        Scope: ``customer_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomerinvoicepayments
        """
        return self._get_page(
            f"/customer_invoices/{customer_invoice_id}/payments",
            item_type=Payment,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    def list_matched_transactions(
        self,
        customer_invoice_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[MatchedTransaction]:
        """List the bank transactions matched to a customer invoice.

        Scope: ``customer_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomerinvoicematchedtransactions
        """
        return self._get_page(
            f"/customer_invoices/{customer_invoice_id}/matched_transactions",
            item_type=MatchedTransaction,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    def match_transaction(self, customer_invoice_id: int, *, transaction_id: int) -> None:
        """Match a bank transaction to a customer invoice.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/postcustomerinvoicematchedtransactions

        Args:
            transaction_id: ID of the transaction to match.
        """
        body = {"transaction_id": transaction_id}
        return self._post(
            f"/customer_invoices/{customer_invoice_id}/matched_transactions", body=body
        )

    def unmatch_transaction(self, customer_invoice_id: int, transaction_id: int) -> None:
        """Unmatch a bank transaction from a customer invoice.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/deletecustomerinvoicematchedtransactions
        """
        return self._delete(
            f"/customer_invoices/{customer_invoice_id}/matched_transactions/{transaction_id}"
        )

    def list_appendices(
        self,
        customer_invoice_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> SyncCursorPage[Appendix]:
        """List the appendices attached to a customer invoice.

        Scope: ``customer_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomerinvoiceappendices
        """
        return self._get_page(
            f"/customer_invoices/{customer_invoice_id}/appendices",
            item_type=Appendix,
            params={"cursor": cursor, "limit": limit},
        )

    def add_appendix(
        self, customer_invoice_id: int, *, file: FileInput, filename: str | None = None
    ) -> Appendix:
        """Upload an appendix file for a customer invoice.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/postcustomerinvoiceappendices

        Args:
            file: The appendix file (path, bytes or file-like object). Allowed
                content types: PNG, JPEG, PDF (see the API reference for the full list).
            filename: Overrides the filename sent to the API.
        """
        return self._post(
            f"/customer_invoices/{customer_invoice_id}/appendices",
            cast_to=Appendix,
            files={"file": to_httpx_file(file, filename=filename)},
        )

    def list_categories(
        self,
        customer_invoice_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> SyncCursorPage[CustomerInvoiceCategory]:
        """List the analytic categories assigned to a customer invoice.

        Scope: ``customer_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomerinvoicecategories
        """
        return self._get_page(
            f"/customer_invoices/{customer_invoice_id}/categories",
            item_type=CustomerInvoiceCategory,
            params={"cursor": cursor, "limit": limit},
        )

    def categorize(
        self, customer_invoice_id: int, *, categories: builtins.list[dict[str, Any]]
    ) -> None:
        """Assign analytic categories to a customer invoice.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/putcustomerinvoicecategories

        Args:
            categories: List of ``{"id": <category_id>, "weight": "<0..1>"}`` dicts.
                The weights across all categories of the same category group must sum to 1.
        """
        return self._put(
            f"/customer_invoices/{customer_invoice_id}/categories", body=categories
        )

    def list_custom_header_fields(
        self,
        customer_invoice_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[CustomHeaderField]:
        """List the custom header fields of a customer invoice.

        Scope: ``customer_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomerinvoicecustomheaderfields
        """
        return self._get_page(
            f"/customer_invoices/{customer_invoice_id}/custom_header_fields",
            item_type=CustomHeaderField,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )


class AsyncCustomerInvoices(AsyncAPIResource):
    """Manage customer invoices (French: factures de vente) (async)."""

    async def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
        include: str | None = None,
    ) -> AsyncCursorPage[CustomerInvoice]:
        """List customer invoices.

        Scope: ``customer_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomerinvoices
        """
        return await self._get_page(
            "/customer_invoices",
            item_type=CustomerInvoice,
            params={
                "cursor": cursor,
                "limit": limit,
                "filter": filter,
                "sort": sort,
                "include": include,
            },
        )

    async def create(
        self,
        *,
        date: dt.date | str,
        deadline: dt.date | str,
        customer_id: int,
        invoice_lines: builtins.list[dict[str, Any]],
        draft: bool = True,
        customer_invoice_template_id: int | None = None,
        pdf_invoice_free_text: str | None = None,
        pdf_invoice_subject: str | None = None,
        pdf_description: str | None = None,
        currency: str | None = None,
        special_mention: str | None = None,
        language: str | None = None,
        discount: dict[str, Any] | None = None,
        invoice_line_sections: builtins.list[dict[str, Any]] | None = None,
        label: str | None = None,
        external_reference: str | None = None,
        transaction_reference: dict[str, Any] | None = None,
    ) -> CustomerInvoice:
        """Create a customer invoice, as a draft or already finalized.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/postcustomerinvoices

        See :meth:`CustomerInvoices.create` for the full body documentation.
        """
        body = drop_none(
            {
                "date": jsonable(date),
                "deadline": jsonable(deadline),
                "customer_id": customer_id,
                "draft": draft,
                "customer_invoice_template_id": customer_invoice_template_id,
                "pdf_invoice_free_text": pdf_invoice_free_text,
                "pdf_invoice_subject": pdf_invoice_subject,
                "pdf_description": pdf_description,
                "currency": currency,
                "special_mention": special_mention,
                "language": language,
                "discount": discount,
                "invoice_line_sections": invoice_line_sections,
                "label": label,
                "external_reference": external_reference,
                "transaction_reference": transaction_reference,
                "invoice_lines": invoice_lines,
            }
        )
        return await self._post("/customer_invoices", cast_to=CustomerInvoice, body=body)

    async def get(self, customer_invoice_id: int) -> CustomerInvoice:
        """Retrieve a customer invoice by its Pennylane identifier.

        Scope: ``customer_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomerinvoice
        """
        return await self._get(
            f"/customer_invoices/{customer_invoice_id}", cast_to=CustomerInvoice
        )

    async def update(
        self,
        customer_invoice_id: int,
        *,
        date: dt.date | str | None = None,
        deadline: dt.date | str | None = None,
        customer_id: int | None = None,
        customer_invoice_template_id: int | None = None,
        pdf_invoice_free_text: str | None = None,
        pdf_invoice_subject: str | None = None,
        pdf_description: str | None = None,
        currency: str | None = None,
        special_mention: str | None = None,
        discount: dict[str, Any] | None = None,
        language: str | None = None,
        invoice_lines: dict[str, Any] | None = None,
        label: str | None = None,
        external_reference: str | None = None,
        transaction_reference: dict[str, Any] | None = None,
    ) -> CustomerInvoice:
        """Update a customer invoice. Only the provided fields are modified.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/putcustomerinvoice

        See :meth:`CustomerInvoices.update` for the full body documentation.
        """
        body = drop_none(
            {
                "date": jsonable(date),
                "deadline": jsonable(deadline),
                "customer_id": customer_id,
                "customer_invoice_template_id": customer_invoice_template_id,
                "pdf_invoice_free_text": pdf_invoice_free_text,
                "pdf_invoice_subject": pdf_invoice_subject,
                "pdf_description": pdf_description,
                "currency": currency,
                "special_mention": special_mention,
                "discount": discount,
                "language": language,
                "invoice_lines": invoice_lines,
                "label": label,
                "external_reference": external_reference,
                "transaction_reference": transaction_reference,
            }
        )
        return await self._put(
            f"/customer_invoices/{customer_invoice_id}", cast_to=CustomerInvoice, body=body
        )

    async def delete(self, customer_invoice_id: int) -> None:
        """Delete a draft customer invoice.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/deletecustomerinvoices
        """
        return await self._delete(f"/customer_invoices/{customer_invoice_id}")

    async def finalize(self, customer_invoice_id: int) -> CustomerInvoice:
        """Turn a draft invoice into a finalized invoice.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/finalizecustomerinvoice
        """
        return await self._put(
            f"/customer_invoices/{customer_invoice_id}/finalize", cast_to=CustomerInvoice
        )

    async def mark_as_paid(self, customer_invoice_id: int) -> None:
        """Mark a customer invoice as paid.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/markaspaidcustomerinvoice
        """
        return await self._put(f"/customer_invoices/{customer_invoice_id}/mark_as_paid")

    async def send_by_email(
        self, customer_invoice_id: int, *, recipients: builtins.list[str] | None = None
    ) -> None:
        """Send a customer invoice by email.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/sendbyemailcustomerinvoice
        """
        body = drop_none({"recipients": recipients})
        return await self._post(
            f"/customer_invoices/{customer_invoice_id}/send_by_email", body=body
        )

    async def send_to_pa(self, customer_invoice_id: int) -> None:
        """Send a customer e-invoice to the Partner Platform (PA).

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/sendtopacustomerinvoice
        """
        return await self._post(f"/customer_invoices/{customer_invoice_id}/send_to_pa")

    async def link_credit_note(
        self, customer_invoice_id: int, *, credit_note_id: int
    ) -> CustomerInvoice:
        """Link a credit note to a customer invoice.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/linkcreditnote
        """
        body = {"credit_note_id": credit_note_id}
        return await self._post(
            f"/customer_invoices/{customer_invoice_id}/link_credit_note",
            cast_to=CustomerInvoice,
            body=body,
        )

    async def update_imported(
        self,
        customer_invoice_id: int,
        *,
        date: dt.date | str | None = None,
        deadline: dt.date | str | None = None,
        customer_id: int | None = None,
        invoice_number: str | None = None,
        currency: str | None = None,
        currency_amount_before_tax: MoneyInput | None = None,
        currency_amount: MoneyInput | None = None,
        amount: MoneyInput | None = None,
        currency_tax: MoneyInput | None = None,
        tax: MoneyInput | None = None,
        transaction_reference: dict[str, Any] | None = None,
        invoice_lines: dict[str, Any] | None = None,
        external_reference: str | None = None,
    ) -> CustomerInvoice:
        """Update an imported customer invoice (whose amounts are set manually).

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/updateimportedcustomerinvoice
        """
        body = drop_none(
            {
                "date": jsonable(date),
                "deadline": jsonable(deadline),
                "customer_id": customer_id,
                "invoice_number": invoice_number,
                "currency": currency,
                "currency_amount_before_tax": jsonable(currency_amount_before_tax),
                "currency_amount": jsonable(currency_amount),
                "amount": jsonable(amount),
                "currency_tax": jsonable(currency_tax),
                "tax": jsonable(tax),
                "transaction_reference": transaction_reference,
                "invoice_lines": invoice_lines,
                "external_reference": external_reference,
            }
        )
        return await self._put(
            f"/customer_invoices/{customer_invoice_id}/update_imported",
            cast_to=CustomerInvoice,
            body=body,
        )

    async def import_from_file(
        self,
        *,
        file_attachment_id: int,
        date: dt.date | str,
        deadline: dt.date | str,
        customer_id: int,
        currency_amount_before_tax: MoneyInput,
        currency_amount: MoneyInput,
        currency_tax: MoneyInput,
        invoice_lines: builtins.list[dict[str, Any]],
        import_as_incomplete: bool | None = None,
        invoice_number: str | None = None,
        currency: str | None = None,
        amount: MoneyInput | None = None,
        tax: MoneyInput | None = None,
        label: str | None = None,
        transaction_reference: dict[str, Any] | None = None,
    ) -> CustomerInvoice:
        """Import a customer invoice from a previously uploaded file attachment.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/importcustomerinvoices
        """
        body = drop_none(
            {
                "file_attachment_id": file_attachment_id,
                "import_as_incomplete": import_as_incomplete,
                "date": jsonable(date),
                "deadline": jsonable(deadline),
                "customer_id": customer_id,
                "invoice_number": invoice_number,
                "currency": currency,
                "currency_amount_before_tax": jsonable(currency_amount_before_tax),
                "currency_amount": jsonable(currency_amount),
                "amount": jsonable(amount),
                "currency_tax": jsonable(currency_tax),
                "tax": jsonable(tax),
                "label": label,
                "transaction_reference": transaction_reference,
                "invoice_lines": invoice_lines,
            }
        )
        return await self._post("/customer_invoices/import", cast_to=CustomerInvoice, body=body)

    async def import_e_invoice(
        self,
        *,
        file: FileInput,
        filename: str | None = None,
        invoice_options: dict[str, Any] | None = None,
    ) -> CustomerInvoiceImportResult:
        """Import a customer e-invoice file (Factur-X PDF, UBL XML or CII XML).

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/createcustomerinvoiceeinvoiceimport
        """
        data = None
        if invoice_options is not None:
            data = {"invoice_options": json.dumps(jsonable(invoice_options))}
        return await self._post(
            "/customer_invoices/e_invoices/imports",
            cast_to=CustomerInvoiceImportResult,
            files={"file": to_httpx_file(file, filename=filename)},
            data=data,
        )

    async def create_from_quote(
        self,
        *,
        quote_id: int,
        draft: bool,
        external_reference: str | None = None,
        customer_invoice_template_id: int | None = None,
    ) -> CustomerInvoice:
        """Create a customer invoice from an accepted quote.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/createcustomerinvoicefromquote
        """
        body = drop_none(
            {
                "quote_id": quote_id,
                "draft": draft,
                "external_reference": external_reference,
                "customer_invoice_template_id": customer_invoice_template_id,
            }
        )
        return await self._post(
            "/customer_invoices/create_from_quote", cast_to=CustomerInvoice, body=body
        )

    async def list_invoice_lines(
        self,
        customer_invoice_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[InvoiceLine]:
        """List the invoice lines of a customer invoice.

        Scope: ``customer_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomerinvoiceinvoicelines
        """
        return await self._get_page(
            f"/customer_invoices/{customer_invoice_id}/invoice_lines",
            item_type=InvoiceLine,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    async def list_invoice_line_sections(
        self,
        customer_invoice_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[InvoiceLineSection]:
        """List the invoice line sections of a customer invoice.

        Scope: ``customer_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomerinvoiceinvoicelinesections
        """
        return await self._get_page(
            f"/customer_invoices/{customer_invoice_id}/invoice_line_sections",
            item_type=InvoiceLineSection,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    async def list_payments(
        self,
        customer_invoice_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[Payment]:
        """List the payments of a customer invoice.

        Scope: ``customer_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomerinvoicepayments
        """
        return await self._get_page(
            f"/customer_invoices/{customer_invoice_id}/payments",
            item_type=Payment,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    async def list_matched_transactions(
        self,
        customer_invoice_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[MatchedTransaction]:
        """List the bank transactions matched to a customer invoice.

        Scope: ``customer_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomerinvoicematchedtransactions
        """
        return await self._get_page(
            f"/customer_invoices/{customer_invoice_id}/matched_transactions",
            item_type=MatchedTransaction,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    async def match_transaction(
        self, customer_invoice_id: int, *, transaction_id: int
    ) -> None:
        """Match a bank transaction to a customer invoice.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/postcustomerinvoicematchedtransactions
        """
        body = {"transaction_id": transaction_id}
        return await self._post(
            f"/customer_invoices/{customer_invoice_id}/matched_transactions", body=body
        )

    async def unmatch_transaction(self, customer_invoice_id: int, transaction_id: int) -> None:
        """Unmatch a bank transaction from a customer invoice.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/deletecustomerinvoicematchedtransactions
        """
        return await self._delete(
            f"/customer_invoices/{customer_invoice_id}/matched_transactions/{transaction_id}"
        )

    async def list_appendices(
        self,
        customer_invoice_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> AsyncCursorPage[Appendix]:
        """List the appendices attached to a customer invoice.

        Scope: ``customer_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomerinvoiceappendices
        """
        return await self._get_page(
            f"/customer_invoices/{customer_invoice_id}/appendices",
            item_type=Appendix,
            params={"cursor": cursor, "limit": limit},
        )

    async def add_appendix(
        self, customer_invoice_id: int, *, file: FileInput, filename: str | None = None
    ) -> Appendix:
        """Upload an appendix file for a customer invoice.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/postcustomerinvoiceappendices
        """
        return await self._post(
            f"/customer_invoices/{customer_invoice_id}/appendices",
            cast_to=Appendix,
            files={"file": to_httpx_file(file, filename=filename)},
        )

    async def list_categories(
        self,
        customer_invoice_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> AsyncCursorPage[CustomerInvoiceCategory]:
        """List the analytic categories assigned to a customer invoice.

        Scope: ``customer_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomerinvoicecategories
        """
        return await self._get_page(
            f"/customer_invoices/{customer_invoice_id}/categories",
            item_type=CustomerInvoiceCategory,
            params={"cursor": cursor, "limit": limit},
        )

    async def categorize(
        self, customer_invoice_id: int, *, categories: builtins.list[dict[str, Any]]
    ) -> None:
        """Assign analytic categories to a customer invoice.

        Scope: ``customer_invoices:all``.
        Reference: https://pennylane.readme.io/reference/putcustomerinvoicecategories
        """
        return await self._put(
            f"/customer_invoices/{customer_invoice_id}/categories", body=categories
        )

    async def list_custom_header_fields(
        self,
        customer_invoice_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[CustomHeaderField]:
        """List the custom header fields of a customer invoice.

        Scope: ``customer_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomerinvoicecustomheaderfields
        """
        return await self._get_page(
            f"/customer_invoices/{customer_invoice_id}/custom_header_fields",
            item_type=CustomHeaderField,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )
