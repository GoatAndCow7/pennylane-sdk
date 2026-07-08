"""E-Invoices and PA Registrations resources (Company API v2).

Reference: https://pennylane.readme.io/reference/createeinvoiceimport
"""

from __future__ import annotations

from ..._files import FileInput, to_httpx_file
from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...types.company.e_invoices import EInvoiceImport, PaRegistration

__all__ = ["AsyncEInvoices", "AsyncPaRegistrations", "EInvoices", "PaRegistrations"]


class EInvoices(SyncAPIResource):
    """Import e-invoice files (Factur-X, UBL, CII)."""

    def import_e_invoice(
        self,
        *,
        file: FileInput,
        type: str,
        filename: str | None = None,
    ) -> EInvoiceImport:
        """Import an e-invoice file.

        .. deprecated:: Pennylane has deprecated this endpoint.

        Beta: undocumented endpoint, subject to change.

        Scope: ``e_invoices:all``.
        Reference: https://pennylane.readme.io/reference/createeinvoiceimport

        Args:
            file: The invoice file to import: a Factur-X PDF, a UBL XML
                invoice, or a CII XML invoice.
            type: The type of the invoice, ``"customer"`` or ``"supplier"``.
            filename: Overrides the filename sent to the API.
        """
        return self._post(
            "/e-invoices/imports",
            cast_to=EInvoiceImport,
            files={"file": to_httpx_file(file, filename=filename)},
            data={"type": type},
        )


class PaRegistrations(SyncAPIResource):
    """List Plateforme Agréée (PA) registrations for the company."""

    def list(self) -> SyncCursorPage[PaRegistration]:
        """List PA registrations for the company.

        Scope: ``pa_registrations:readonly``.
        Reference: https://pennylane.readme.io/reference/getparegistrations
        """
        return self._get_page("/pa_registrations", item_type=PaRegistration)


class AsyncEInvoices(AsyncAPIResource):
    """Import e-invoice files (Factur-X, UBL, CII) (async)."""

    async def import_e_invoice(
        self,
        *,
        file: FileInput,
        type: str,
        filename: str | None = None,
    ) -> EInvoiceImport:
        """Import an e-invoice file.

        .. deprecated:: Pennylane has deprecated this endpoint.

        Beta: undocumented endpoint, subject to change.

        Scope: ``e_invoices:all``.
        Reference: https://pennylane.readme.io/reference/createeinvoiceimport
        """
        return await self._post(
            "/e-invoices/imports",
            cast_to=EInvoiceImport,
            files={"file": to_httpx_file(file, filename=filename)},
            data={"type": type},
        )


class AsyncPaRegistrations(AsyncAPIResource):
    """List Plateforme Agréée (PA) registrations for the company (async)."""

    async def list(self) -> AsyncCursorPage[PaRegistration]:
        """List PA registrations for the company.

        Scope: ``pa_registrations:readonly``.
        Reference: https://pennylane.readme.io/reference/getparegistrations
        """
        return await self._get_page("/pa_registrations", item_type=PaRegistration)
