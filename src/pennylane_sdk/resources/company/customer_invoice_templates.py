"""Customer Invoice Templates resource (Company API v2).

Reference: https://pennylane.readme.io/reference/getcustomerinvoicetemplates
"""

from __future__ import annotations

from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...types.company.customer_invoice_templates import CustomerInvoiceTemplate

__all__ = ["AsyncCustomerInvoiceTemplates", "CustomerInvoiceTemplates"]


class CustomerInvoiceTemplates(SyncAPIResource):
    """Read customer invoice templates."""

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[CustomerInvoiceTemplate]:
        """List customer invoice templates.

        Scope: ``customer_invoice_templates:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomerinvoicetemplates

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            "/customer_invoice_templates",
            item_type=CustomerInvoiceTemplate,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )


class AsyncCustomerInvoiceTemplates(AsyncAPIResource):
    """Read customer invoice templates (async)."""

    async def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[CustomerInvoiceTemplate]:
        """List customer invoice templates.

        Scope: ``customer_invoice_templates:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomerinvoicetemplates
        """
        return await self._get_page(
            "/customer_invoice_templates",
            item_type=CustomerInvoiceTemplate,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )
