"""Supplier invoices resource (Company API v2).

Reference: https://pennylane.readme.io/reference/getsupplierinvoices
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
from ...types.company.supplier_invoices import (
    InvoiceLine,
    MatchedTransaction,
    Payment,
    SupplierEInvoiceImportResult,
    SupplierInvoice,
    SupplierInvoiceCategoriesResponse,
    SupplierInvoiceCategory,
)

__all__ = ["AsyncSupplierInvoices", "SupplierInvoices"]


class SupplierInvoices(SyncAPIResource):
    """Manage supplier invoices (French: factures d'achat)."""

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[SupplierInvoice]:
        """List supplier invoices.

        Scope: ``supplier_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getsupplierinvoices

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            "/supplier_invoices",
            item_type=SupplierInvoice,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    def get(self, supplier_invoice_id: int) -> SupplierInvoice:
        """Retrieve a supplier invoice by its Pennylane identifier.

        Scope: ``supplier_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getsupplierinvoice
        """
        return self._get(f"/supplier_invoices/{supplier_invoice_id}", cast_to=SupplierInvoice)

    def update(
        self,
        supplier_invoice_id: int,
        *,
        supplier_id: int | None = None,
        date: dt.date | str | None = None,
        deadline: dt.date | str | None = None,
        invoice_number: str | None = None,
        label: str | None = None,
        currency: str | None = None,
        currency_amount_before_tax: MoneyInput | None = None,
        currency_amount: MoneyInput | None = None,
        amount: MoneyInput | None = None,
        currency_tax: MoneyInput | None = None,
        tax: MoneyInput | None = None,
        transaction_reference: dict[str, Any] | None = None,
        invoice_lines: dict[str, Any] | None = None,
        external_reference: str | None = None,
    ) -> SupplierInvoice:
        """Update a supplier invoice. Only the provided fields are modified.

        Scope: ``supplier_invoices:all``.
        Reference: https://pennylane.readme.io/reference/putsupplierinvoice

        Args:
            transaction_reference: ``{"banking_provider", "provider_field_name",
                "provider_field_value"}`` to auto-reconcile with a bank transaction.
            invoice_lines: ``{"create": [...], "update": [...], "delete": [...]}``.
        """
        body = drop_none(
            {
                "supplier_id": supplier_id,
                "date": jsonable(date),
                "deadline": jsonable(deadline),
                "invoice_number": invoice_number,
                "label": label,
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
            f"/supplier_invoices/{supplier_invoice_id}", cast_to=SupplierInvoice, body=body
        )

    def import_from_file(
        self,
        *,
        file_attachment_id: int,
        supplier_id: int,
        date: dt.date | str,
        deadline: dt.date | str,
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
        external_reference: str | None = None,
    ) -> SupplierInvoice:
        """Import a supplier invoice from a previously uploaded file attachment.

        Scope: ``supplier_invoices:all``.
        Reference: https://pennylane.readme.io/reference/importsupplierinvoice

        Args:
            file_attachment_id: ID of a file uploaded through ``/file_attachments``.
            import_as_incomplete: Set the invoice to ``Incomplete`` status.
            invoice_lines: Invoice lines, each a dict of invoice line fields
                (``label``, ``description``, ``currency_amount``, ``currency_tax``,
                ``ledger_account_id``, ``vat_rate``, ``imputation_dates``,
                ``ledger_entry_line``...).
            transaction_reference: ``{"banking_provider", "provider_field_name",
                "provider_field_value"}`` to auto-reconcile with a bank transaction.
        """
        body = drop_none(
            {
                "file_attachment_id": file_attachment_id,
                "import_as_incomplete": import_as_incomplete,
                "supplier_id": supplier_id,
                "date": jsonable(date),
                "deadline": jsonable(deadline),
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
                "external_reference": external_reference,
            }
        )
        return self._post("/supplier_invoices/import", cast_to=SupplierInvoice, body=body)

    def import_e_invoice(
        self,
        *,
        file: FileInput,
        filename: str | None = None,
        invoice_options: dict[str, Any] | None = None,
    ) -> SupplierEInvoiceImportResult:
        """Import a supplier e-invoice file (Factur-X PDF, UBL XML or CII XML).

        Scope: ``supplier_invoices:all``.
        Reference: https://pennylane.readme.io/reference/createsupplierinvoiceeinvoiceimport

        Args:
            file: The e-invoice file (path, bytes or file-like object).
            filename: Overrides the filename sent to the API.
            invoice_options: Optional payload to enrich the imported invoice:
                ``{"supplier_id": ..., "invoice_lines": [{"e_invoice_line_id",
                "ledger_account_id"}, ...]}``.
        """
        data = None
        if invoice_options is not None:
            data = {"invoice_options": json.dumps(jsonable(invoice_options))}
        return self._post(
            "/supplier_invoices/e_invoices/imports",
            cast_to=SupplierEInvoiceImportResult,
            files={"file": to_httpx_file(file, filename=filename)},
            data=data,
        )

    def validate_accounting(self, supplier_invoice_id: int) -> SupplierInvoice:
        """Validate the accounting of a supplier invoice.

        Scope: ``supplier_invoices:all``.
        Reference: https://pennylane.readme.io/reference/validateaccountingsupplierinvoice
        """
        return self._put(
            f"/supplier_invoices/{supplier_invoice_id}/validate_accounting",
            cast_to=SupplierInvoice,
        )

    def update_payment_status(self, supplier_invoice_id: int, *, payment_status: str) -> None:
        """Update the payment status of a supplier invoice.

        Scope: ``supplier_invoices:all``.
        Reference: https://pennylane.readme.io/reference/updatesupplierinvoicepaymentstatus

        Args:
            payment_status: ``"paid"`` or ``"to_be_paid"``.
        """
        body = {"payment_status": payment_status}
        return self._put(f"/supplier_invoices/{supplier_invoice_id}/payment_status", body=body)

    def update_e_invoice_status(
        self,
        supplier_invoice_id: int,
        *,
        status: str,
        reason: str | None = None,
    ) -> SupplierInvoice:
        """Update the e-invoice lifecycle status of a supplier invoice.

        Scope: ``supplier_invoices:all``.
        Reference: https://pennylane.readme.io/reference/putsupplierinvoiceeinvoicestatus

        The request body is a ``oneOf`` of three variants:

        - **Dispute** (``status="disputed"``): requires ``reason`` from the
          dispute set (``incorrect_vat_rate``, ``incorrect_unit_prices``,
          ``incorrect_billed_quantity``, ``incorrect_billed_item``,
          ``defective_delivered_item``, ``delivery_issue``, ``bank_details_error``,
          ``incorrect_payment_terms``, ``missing_legal_notice``,
          ``missing_contractual_reference``, ``recipient_error``).
        - **Refuse** (``status="refused"``): requires ``reason`` from the
          refuse set (``incorrect_vat_rate``, ``contract_completed``,
          ``duplicate_invoice``, ``recipient_error``, ``incorrect_prices``,
          ``non_compliant_invoice``).
        - **Undispute** (``status="approved"``): no ``reason``.

        Args:
            status: ``"disputed"``, ``"refused"`` or ``"approved"``.
            reason: Required for ``"disputed"`` and ``"refused"``.
        """
        body = drop_none({"status": status, "reason": reason})
        return self._put(
            f"/supplier_invoices/{supplier_invoice_id}/e_invoice_status",
            cast_to=SupplierInvoice,
            body=body,
        )

    def list_invoice_lines(
        self,
        supplier_invoice_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[InvoiceLine]:
        """List the invoice lines of a supplier invoice.

        Scope: ``supplier_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getsupplierinvoicelines
        """
        return self._get_page(
            f"/supplier_invoices/{supplier_invoice_id}/invoice_lines",
            item_type=InvoiceLine,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    def list_categories(
        self,
        supplier_invoice_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> SyncCursorPage[SupplierInvoiceCategory]:
        """List the analytic categories assigned to a supplier invoice.

        Scope: ``supplier_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getsupplierinvoicecategories
        """
        return self._get_page(
            f"/supplier_invoices/{supplier_invoice_id}/categories",
            item_type=SupplierInvoiceCategory,
            params={"cursor": cursor, "limit": limit},
        )

    def categorize(
        self, supplier_invoice_id: int, *, categories: builtins.list[dict[str, Any]]
    ) -> builtins.list[SupplierInvoiceCategory]:
        """Replace the analytic categories assigned to a supplier invoice.

        Categories may belong to different category groups; the weights of
        categories from the same group must sum to ``1``.

        Scope: ``supplier_invoices:all``.
        Reference: https://pennylane.readme.io/reference/putsupplierinvoicecategories

        Args:
            categories: List of ``{"id": <category_id>, "weight": "<0..1>"}`` dicts.
        """
        response = self._put(
            f"/supplier_invoices/{supplier_invoice_id}/categories",
            cast_to=SupplierInvoiceCategoriesResponse,
            body=categories,
        )
        return response.items

    def list_payments(
        self,
        supplier_invoice_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[Payment]:
        """List the payments of a supplier invoice.

        Scope: ``supplier_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getsupplierinvoicepayments
        """
        return self._get_page(
            f"/supplier_invoices/{supplier_invoice_id}/payments",
            item_type=Payment,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    def list_matched_transactions(
        self,
        supplier_invoice_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[MatchedTransaction]:
        """List the bank transactions matched to a supplier invoice.

        Scope: ``supplier_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getsupplierinvoicematchedtransactions
        """
        return self._get_page(
            f"/supplier_invoices/{supplier_invoice_id}/matched_transactions",
            item_type=MatchedTransaction,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    def match_transaction(self, supplier_invoice_id: int, *, transaction_id: int) -> None:
        """Match a bank transaction to a supplier invoice.

        Scope: ``supplier_invoices:all``.
        Reference: https://pennylane.readme.io/reference/postsupplierinvoicematchedtransactions

        Args:
            transaction_id: ID of the transaction to match.
        """
        body = {"transaction_id": transaction_id}
        return self._post(
            f"/supplier_invoices/{supplier_invoice_id}/matched_transactions", body=body
        )

    def unmatch_transaction(self, supplier_invoice_id: int, transaction_id: int) -> None:
        """Unmatch a bank transaction from a supplier invoice.

        Scope: ``supplier_invoices:all``.
        Reference: https://pennylane.readme.io/reference/deletesupplierinvoicematchedtransactions
        """
        return self._delete(
            f"/supplier_invoices/{supplier_invoice_id}/matched_transactions/{transaction_id}"
        )

    def link_purchase_requests(
        self, supplier_invoice_id: int, *, purchase_request_id: int
    ) -> None:
        """Link a purchase request to a supplier invoice.

        Scope: ``supplier_invoices:all``.
        Reference: https://pennylane.readme.io/reference/postsupplierinvoicelinkedpurchaserequests

        Args:
            purchase_request_id: ID of the purchase request to link.
        """
        body = {"purchase_request_id": purchase_request_id}
        return self._post(
            f"/supplier_invoices/{supplier_invoice_id}/linked_purchase_requests", body=body
        )


class AsyncSupplierInvoices(AsyncAPIResource):
    """Manage supplier invoices (French: factures d'achat) (async)."""

    async def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[SupplierInvoice]:
        """List supplier invoices.

        Scope: ``supplier_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getsupplierinvoices
        """
        return await self._get_page(
            "/supplier_invoices",
            item_type=SupplierInvoice,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    async def get(self, supplier_invoice_id: int) -> SupplierInvoice:
        """Retrieve a supplier invoice by its Pennylane identifier.

        Scope: ``supplier_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getsupplierinvoice
        """
        return await self._get(
            f"/supplier_invoices/{supplier_invoice_id}", cast_to=SupplierInvoice
        )

    async def update(
        self,
        supplier_invoice_id: int,
        *,
        supplier_id: int | None = None,
        date: dt.date | str | None = None,
        deadline: dt.date | str | None = None,
        invoice_number: str | None = None,
        label: str | None = None,
        currency: str | None = None,
        currency_amount_before_tax: MoneyInput | None = None,
        currency_amount: MoneyInput | None = None,
        amount: MoneyInput | None = None,
        currency_tax: MoneyInput | None = None,
        tax: MoneyInput | None = None,
        transaction_reference: dict[str, Any] | None = None,
        invoice_lines: dict[str, Any] | None = None,
        external_reference: str | None = None,
    ) -> SupplierInvoice:
        """Update a supplier invoice. Only the provided fields are modified.

        Scope: ``supplier_invoices:all``.
        Reference: https://pennylane.readme.io/reference/putsupplierinvoice

        See :meth:`SupplierInvoices.update` for the full body documentation.
        """
        body = drop_none(
            {
                "supplier_id": supplier_id,
                "date": jsonable(date),
                "deadline": jsonable(deadline),
                "invoice_number": invoice_number,
                "label": label,
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
            f"/supplier_invoices/{supplier_invoice_id}", cast_to=SupplierInvoice, body=body
        )

    async def import_from_file(
        self,
        *,
        file_attachment_id: int,
        supplier_id: int,
        date: dt.date | str,
        deadline: dt.date | str,
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
        external_reference: str | None = None,
    ) -> SupplierInvoice:
        """Import a supplier invoice from a previously uploaded file attachment.

        Scope: ``supplier_invoices:all``.
        Reference: https://pennylane.readme.io/reference/importsupplierinvoice

        See :meth:`SupplierInvoices.import_from_file` for the full body documentation.
        """
        body = drop_none(
            {
                "file_attachment_id": file_attachment_id,
                "import_as_incomplete": import_as_incomplete,
                "supplier_id": supplier_id,
                "date": jsonable(date),
                "deadline": jsonable(deadline),
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
                "external_reference": external_reference,
            }
        )
        return await self._post("/supplier_invoices/import", cast_to=SupplierInvoice, body=body)

    async def import_e_invoice(
        self,
        *,
        file: FileInput,
        filename: str | None = None,
        invoice_options: dict[str, Any] | None = None,
    ) -> SupplierEInvoiceImportResult:
        """Import a supplier e-invoice file (Factur-X PDF, UBL XML or CII XML).

        Scope: ``supplier_invoices:all``.
        Reference: https://pennylane.readme.io/reference/createsupplierinvoiceeinvoiceimport
        """
        data = None
        if invoice_options is not None:
            data = {"invoice_options": json.dumps(jsonable(invoice_options))}
        return await self._post(
            "/supplier_invoices/e_invoices/imports",
            cast_to=SupplierEInvoiceImportResult,
            files={"file": to_httpx_file(file, filename=filename)},
            data=data,
        )

    async def validate_accounting(self, supplier_invoice_id: int) -> SupplierInvoice:
        """Validate the accounting of a supplier invoice.

        Scope: ``supplier_invoices:all``.
        Reference: https://pennylane.readme.io/reference/validateaccountingsupplierinvoice
        """
        return await self._put(
            f"/supplier_invoices/{supplier_invoice_id}/validate_accounting",
            cast_to=SupplierInvoice,
        )

    async def update_payment_status(
        self, supplier_invoice_id: int, *, payment_status: str
    ) -> None:
        """Update the payment status of a supplier invoice.

        Scope: ``supplier_invoices:all``.
        Reference: https://pennylane.readme.io/reference/updatesupplierinvoicepaymentstatus

        Args:
            payment_status: ``"paid"`` or ``"to_be_paid"``.
        """
        body = {"payment_status": payment_status}
        return await self._put(
            f"/supplier_invoices/{supplier_invoice_id}/payment_status", body=body
        )

    async def update_e_invoice_status(
        self,
        supplier_invoice_id: int,
        *,
        status: str,
        reason: str | None = None,
    ) -> SupplierInvoice:
        """Update the e-invoice lifecycle status of a supplier invoice.

        Scope: ``supplier_invoices:all``.
        Reference: https://pennylane.readme.io/reference/putsupplierinvoiceeinvoicestatus

        See :meth:`SupplierInvoices.update_e_invoice_status` for the variants.
        """
        body = drop_none({"status": status, "reason": reason})
        return await self._put(
            f"/supplier_invoices/{supplier_invoice_id}/e_invoice_status",
            cast_to=SupplierInvoice,
            body=body,
        )

    async def list_invoice_lines(
        self,
        supplier_invoice_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[InvoiceLine]:
        """List the invoice lines of a supplier invoice.

        Scope: ``supplier_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getsupplierinvoicelines
        """
        return await self._get_page(
            f"/supplier_invoices/{supplier_invoice_id}/invoice_lines",
            item_type=InvoiceLine,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    async def list_categories(
        self,
        supplier_invoice_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> AsyncCursorPage[SupplierInvoiceCategory]:
        """List the analytic categories assigned to a supplier invoice.

        Scope: ``supplier_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getsupplierinvoicecategories
        """
        return await self._get_page(
            f"/supplier_invoices/{supplier_invoice_id}/categories",
            item_type=SupplierInvoiceCategory,
            params={"cursor": cursor, "limit": limit},
        )

    async def categorize(
        self, supplier_invoice_id: int, *, categories: builtins.list[dict[str, Any]]
    ) -> builtins.list[SupplierInvoiceCategory]:
        """Replace the analytic categories assigned to a supplier invoice.

        Categories may belong to different category groups; the weights of
        categories from the same group must sum to ``1``.

        Scope: ``supplier_invoices:all``.
        Reference: https://pennylane.readme.io/reference/putsupplierinvoicecategories

        Args:
            categories: List of ``{"id": <category_id>, "weight": "<0..1>"}`` dicts.
        """
        response = await self._put(
            f"/supplier_invoices/{supplier_invoice_id}/categories",
            cast_to=SupplierInvoiceCategoriesResponse,
            body=categories,
        )
        return response.items

    async def list_payments(
        self,
        supplier_invoice_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[Payment]:
        """List the payments of a supplier invoice.

        Scope: ``supplier_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getsupplierinvoicepayments
        """
        return await self._get_page(
            f"/supplier_invoices/{supplier_invoice_id}/payments",
            item_type=Payment,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    async def list_matched_transactions(
        self,
        supplier_invoice_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[MatchedTransaction]:
        """List the bank transactions matched to a supplier invoice.

        Scope: ``supplier_invoices:readonly``.
        Reference: https://pennylane.readme.io/reference/getsupplierinvoicematchedtransactions
        """
        return await self._get_page(
            f"/supplier_invoices/{supplier_invoice_id}/matched_transactions",
            item_type=MatchedTransaction,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    async def match_transaction(self, supplier_invoice_id: int, *, transaction_id: int) -> None:
        """Match a bank transaction to a supplier invoice.

        Scope: ``supplier_invoices:all``.
        Reference: https://pennylane.readme.io/reference/postsupplierinvoicematchedtransactions
        """
        body = {"transaction_id": transaction_id}
        return await self._post(
            f"/supplier_invoices/{supplier_invoice_id}/matched_transactions", body=body
        )

    async def unmatch_transaction(self, supplier_invoice_id: int, transaction_id: int) -> None:
        """Unmatch a bank transaction from a supplier invoice.

        Scope: ``supplier_invoices:all``.
        Reference: https://pennylane.readme.io/reference/deletesupplierinvoicematchedtransactions
        """
        return await self._delete(
            f"/supplier_invoices/{supplier_invoice_id}/matched_transactions/{transaction_id}"
        )

    async def link_purchase_requests(
        self, supplier_invoice_id: int, *, purchase_request_id: int
    ) -> None:
        """Link a purchase request to a supplier invoice.

        Scope: ``supplier_invoices:all``.
        Reference: https://pennylane.readme.io/reference/postsupplierinvoicelinkedpurchaserequests
        """
        body = {"purchase_request_id": purchase_request_id}
        return await self._post(
            f"/supplier_invoices/{supplier_invoice_id}/linked_purchase_requests", body=body
        )
