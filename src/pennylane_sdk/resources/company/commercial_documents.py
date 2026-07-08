"""Commercial Documents resource (Company API v2).

Reference: https://pennylane.readme.io/reference/getcommercialdocuments
"""

from __future__ import annotations

from ..._files import FileInput, to_httpx_file
from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...filters import FiltersInput
from ...types.company.commercial_documents import (
    CommercialDocument,
    CommercialDocumentAppendix,
    CommercialDocumentInvoiceLine,
    CommercialDocumentInvoiceLineSection,
)

__all__ = ["AsyncCommercialDocuments", "CommercialDocuments"]


class CommercialDocuments(SyncAPIResource):
    """Read commercial documents (proforma, shipping orders, purchasing orders)."""

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[CommercialDocument]:
        """List commercial documents.

        Scope: ``commercial_documents:readonly``.
        Reference: https://pennylane.readme.io/reference/listcommercialdocuments

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            "/commercial_documents",
            item_type=CommercialDocument,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    def get(self, commercial_document_id: int) -> CommercialDocument:
        """Retrieve a commercial document by its Pennylane identifier.

        Scope: ``commercial_documents:readonly``.
        Reference: https://pennylane.readme.io/reference/getcommercialdocument
        """
        return self._get(
            f"/commercial_documents/{commercial_document_id}", cast_to=CommercialDocument
        )

    def list_appendices(
        self,
        commercial_document_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> SyncCursorPage[CommercialDocumentAppendix]:
        """List the appendices attached to a commercial document.

        Scope: ``commercial_documents:readonly``.
        Reference: https://pennylane.readme.io/reference/getcommercialdocumentappendices
        """
        return self._get_page(
            f"/commercial_documents/{commercial_document_id}/appendices",
            item_type=CommercialDocumentAppendix,
            params={"cursor": cursor, "limit": limit},
        )

    def add_appendix(
        self,
        commercial_document_id: int,
        *,
        file: FileInput,
        filename: str | None = None,
    ) -> CommercialDocumentAppendix:
        """Upload an appendix for a commercial document.

        Scope: ``commercial_documents:all``.
        Reference: https://pennylane.readme.io/reference/postcommercialdocumentappendices

        Args:
            file: The appendix file (path, bytes, file-like object or
                ``(filename, content)`` tuple).
            filename: Overrides the filename sent to the API.
        """
        return self._post(
            f"/commercial_documents/{commercial_document_id}/appendices",
            cast_to=CommercialDocumentAppendix,
            files={"file": to_httpx_file(file, filename=filename)},
        )

    def list_invoice_lines(
        self,
        commercial_document_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[CommercialDocumentInvoiceLine]:
        """List the invoice lines of a commercial document.

        Scope: ``commercial_documents:readonly``.
        Reference: https://pennylane.readme.io/reference/getcommercialdocumentinvoicelines
        """
        return self._get_page(
            f"/commercial_documents/{commercial_document_id}/invoice_lines",
            item_type=CommercialDocumentInvoiceLine,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    def list_invoice_line_sections(
        self,
        commercial_document_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[CommercialDocumentInvoiceLineSection]:
        """List the invoice line sections of a commercial document.

        Scope: ``commercial_documents:readonly``.
        Reference: https://pennylane.readme.io/reference/getcommercialdocumentinvoicelinesections
        """
        return self._get_page(
            f"/commercial_documents/{commercial_document_id}/invoice_line_sections",
            item_type=CommercialDocumentInvoiceLineSection,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )


class AsyncCommercialDocuments(AsyncAPIResource):
    """Read commercial documents (proforma, shipping orders, purchasing orders) (async)."""

    async def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[CommercialDocument]:
        """List commercial documents.

        Scope: ``commercial_documents:readonly``.
        Reference: https://pennylane.readme.io/reference/listcommercialdocuments
        """
        return await self._get_page(
            "/commercial_documents",
            item_type=CommercialDocument,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    async def get(self, commercial_document_id: int) -> CommercialDocument:
        """Retrieve a commercial document by its Pennylane identifier.

        Scope: ``commercial_documents:readonly``.
        Reference: https://pennylane.readme.io/reference/getcommercialdocument
        """
        return await self._get(
            f"/commercial_documents/{commercial_document_id}", cast_to=CommercialDocument
        )

    async def list_appendices(
        self,
        commercial_document_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> AsyncCursorPage[CommercialDocumentAppendix]:
        """List the appendices attached to a commercial document.

        Scope: ``commercial_documents:readonly``.
        Reference: https://pennylane.readme.io/reference/getcommercialdocumentappendices
        """
        return await self._get_page(
            f"/commercial_documents/{commercial_document_id}/appendices",
            item_type=CommercialDocumentAppendix,
            params={"cursor": cursor, "limit": limit},
        )

    async def add_appendix(
        self,
        commercial_document_id: int,
        *,
        file: FileInput,
        filename: str | None = None,
    ) -> CommercialDocumentAppendix:
        """Upload an appendix for a commercial document.

        Scope: ``commercial_documents:all``.
        Reference: https://pennylane.readme.io/reference/postcommercialdocumentappendices
        """
        return await self._post(
            f"/commercial_documents/{commercial_document_id}/appendices",
            cast_to=CommercialDocumentAppendix,
            files={"file": to_httpx_file(file, filename=filename)},
        )

    async def list_invoice_lines(
        self,
        commercial_document_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[CommercialDocumentInvoiceLine]:
        """List the invoice lines of a commercial document.

        Scope: ``commercial_documents:readonly``.
        Reference: https://pennylane.readme.io/reference/getcommercialdocumentinvoicelines
        """
        return await self._get_page(
            f"/commercial_documents/{commercial_document_id}/invoice_lines",
            item_type=CommercialDocumentInvoiceLine,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    async def list_invoice_line_sections(
        self,
        commercial_document_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[CommercialDocumentInvoiceLineSection]:
        """List the invoice line sections of a commercial document.

        Scope: ``commercial_documents:readonly``.
        Reference: https://pennylane.readme.io/reference/getcommercialdocumentinvoicelinesections
        """
        return await self._get_page(
            f"/commercial_documents/{commercial_document_id}/invoice_line_sections",
            item_type=CommercialDocumentInvoiceLineSection,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )
