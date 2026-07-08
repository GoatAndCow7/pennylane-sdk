"""Invoicing resources (Firm API v1): customer invoices, supplier invoices,
customers and suppliers.

Reference: https://firm-pennylane.readme.io/reference/getcustomerinvoices
"""

from __future__ import annotations

from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...filters import FiltersInput
from ...types.firm.invoicing import (
    FirmCustomer,
    FirmCustomerInvoice,
    FirmSupplier,
    FirmSupplierInvoice,
)

__all__ = [
    "AsyncFirmCustomerInvoices",
    "AsyncFirmCustomers",
    "AsyncFirmSupplierInvoices",
    "AsyncFirmSuppliers",
    "FirmCustomerInvoices",
    "FirmCustomers",
    "FirmSupplierInvoices",
    "FirmSuppliers",
]


class FirmCustomerInvoices(SyncAPIResource):
    """Browse a client company's customer invoices."""

    def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[FirmCustomerInvoice]:
        """List customer invoices of a client company.

        Beta: undocumented endpoint, subject to change.

        Scope: ``customer_invoices:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getcustomerinvoices

        Args:
            company_id: Identifier of the client company.
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            f"/companies/{company_id}/customer_invoices",
            item_type=FirmCustomerInvoice,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    def get(self, company_id: int, customer_invoice_id: int) -> FirmCustomerInvoice:
        """Retrieve a customer invoice of a client company.

        Beta: undocumented endpoint, subject to change.

        Scope: ``customer_invoices:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getcustomerinvoice
        """
        return self._get(
            f"/companies/{company_id}/customer_invoices/{customer_invoice_id}",
            cast_to=FirmCustomerInvoice,
        )


class FirmSupplierInvoices(SyncAPIResource):
    """Browse a client company's supplier invoices."""

    def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[FirmSupplierInvoice]:
        """List supplier invoices of a client company.

        Beta: undocumented endpoint, subject to change.

        Scope: ``supplier_invoices:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getsupplierinvoices

        Args:
            company_id: Identifier of the client company.
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            f"/companies/{company_id}/supplier_invoices",
            item_type=FirmSupplierInvoice,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    def get(self, company_id: int, supplier_invoice_id: int) -> FirmSupplierInvoice:
        """Retrieve a supplier invoice of a client company.

        Beta: undocumented endpoint, subject to change.

        Scope: ``supplier_invoices:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getsupplierinvoice
        """
        return self._get(
            f"/companies/{company_id}/supplier_invoices/{supplier_invoice_id}",
            cast_to=FirmSupplierInvoice,
        )


class FirmCustomers(SyncAPIResource):
    """Browse a client company's customers."""

    def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[FirmCustomer]:
        """List customers of a client company.

        Scope: ``customers:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getcustomers

        Args:
            company_id: Identifier of the client company.
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            f"/companies/{company_id}/customers",
            item_type=FirmCustomer,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )


class FirmSuppliers(SyncAPIResource):
    """Browse a client company's suppliers."""

    def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[FirmSupplier]:
        """List suppliers of a client company.

        Scope: ``suppliers:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getsuppliers

        Args:
            company_id: Identifier of the client company.
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            f"/companies/{company_id}/suppliers",
            item_type=FirmSupplier,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )


class AsyncFirmCustomerInvoices(AsyncAPIResource):
    """Browse a client company's customer invoices (async)."""

    async def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[FirmCustomerInvoice]:
        """List customer invoices of a client company.

        Beta: undocumented endpoint, subject to change.

        Scope: ``customer_invoices:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getcustomerinvoices
        """
        return await self._get_page(
            f"/companies/{company_id}/customer_invoices",
            item_type=FirmCustomerInvoice,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    async def get(self, company_id: int, customer_invoice_id: int) -> FirmCustomerInvoice:
        """Retrieve a customer invoice of a client company.

        Beta: undocumented endpoint, subject to change.

        Scope: ``customer_invoices:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getcustomerinvoice
        """
        return await self._get(
            f"/companies/{company_id}/customer_invoices/{customer_invoice_id}",
            cast_to=FirmCustomerInvoice,
        )


class AsyncFirmSupplierInvoices(AsyncAPIResource):
    """Browse a client company's supplier invoices (async)."""

    async def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[FirmSupplierInvoice]:
        """List supplier invoices of a client company.

        Beta: undocumented endpoint, subject to change.

        Scope: ``supplier_invoices:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getsupplierinvoices
        """
        return await self._get_page(
            f"/companies/{company_id}/supplier_invoices",
            item_type=FirmSupplierInvoice,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    async def get(self, company_id: int, supplier_invoice_id: int) -> FirmSupplierInvoice:
        """Retrieve a supplier invoice of a client company.

        Beta: undocumented endpoint, subject to change.

        Scope: ``supplier_invoices:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getsupplierinvoice
        """
        return await self._get(
            f"/companies/{company_id}/supplier_invoices/{supplier_invoice_id}",
            cast_to=FirmSupplierInvoice,
        )


class AsyncFirmCustomers(AsyncAPIResource):
    """Browse a client company's customers (async)."""

    async def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[FirmCustomer]:
        """List customers of a client company.

        Scope: ``customers:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getcustomers
        """
        return await self._get_page(
            f"/companies/{company_id}/customers",
            item_type=FirmCustomer,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )


class AsyncFirmSuppliers(AsyncAPIResource):
    """Browse a client company's suppliers (async)."""

    async def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[FirmSupplier]:
        """List suppliers of a client company.

        Scope: ``suppliers:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getsuppliers
        """
        return await self._get_page(
            f"/companies/{company_id}/suppliers",
            item_type=FirmSupplier,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )
