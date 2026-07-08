"""Purchase requests resource (Company API v2).

Reference: https://pennylane.readme.io/reference/getpurchaserequests
"""

from __future__ import annotations

import builtins
import datetime as dt
from typing import Any

from ..._models import MoneyInput, drop_none, jsonable
from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...filters import FiltersInput
from ...types.company.purchase_requests import PurchaseRequest

__all__ = ["AsyncPurchaseRequests", "PurchaseRequests"]


class PurchaseRequests(SyncAPIResource):
    """Read and import purchase requests (French: demandes d'achat)."""

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[PurchaseRequest]:
        """List purchase requests.

        Scope: ``purchase_requests:readonly``.
        Reference: https://pennylane.readme.io/reference/getpurchaserequests

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            "/purchase_requests",
            item_type=PurchaseRequest,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    def get(self, purchase_request_id: int) -> PurchaseRequest:
        """Retrieve a purchase request by its Pennylane identifier.

        Scope: ``purchase_requests:readonly``.
        Reference: https://pennylane.readme.io/reference/getpurchaserequest
        """
        return self._get(f"/purchase_requests/{purchase_request_id}", cast_to=PurchaseRequest)

    def import_from_file(
        self,
        *,
        file_attachment_id: int,
        reason: str,
        supplier_id: int,
        purchase_order_number: str,
        currency_amount_before_tax: MoneyInput,
        currency_amount: MoneyInput,
        currency_tax: MoneyInput,
        delivery_address: dict[str, Any],
        purchase_request_lines: builtins.list[dict[str, Any]],
        estimated_delivery_date: dt.date | str | None = None,
        currency: str | None = None,
        amount: MoneyInput | None = None,
        tax: MoneyInput | None = None,
    ) -> PurchaseRequest:
        """Import a purchase order from a previously uploaded file attachment.

        Scope: ``purchase_requests:all``.
        Reference: https://pennylane.readme.io/reference/createpurchaserequestimport

        Args:
            file_attachment_id: ID of a file uploaded through ``/file_attachments``,
                containing the purchase order to import.
            reason: Reason of the purchase request.
            supplier_id: Supplier identifier.
            purchase_order_number: Purchase order number.
            delivery_address: ``{"address", "postal_code", "city", "country_alpha2"}``.
            purchase_request_lines: Lines, each a dict with ``currency_amount``,
                ``currency_tax``, ``label``, ``quantity``, ``unit_price``, ``unit``,
                ``vat_rate`` and optionally ``amount``, ``tax``, ``description``.
            estimated_delivery_date: Estimated delivery date (ISO 8601).
        """
        body = drop_none(
            {
                "file_attachment_id": file_attachment_id,
                "reason": reason,
                "estimated_delivery_date": jsonable(estimated_delivery_date),
                "supplier_id": supplier_id,
                "purchase_order_number": purchase_order_number,
                "currency": currency,
                "currency_amount_before_tax": jsonable(currency_amount_before_tax),
                "currency_amount": jsonable(currency_amount),
                "amount": jsonable(amount),
                "currency_tax": jsonable(currency_tax),
                "tax": jsonable(tax),
                "delivery_address": delivery_address,
                "purchase_request_lines": purchase_request_lines,
            }
        )
        return self._post("/purchase_requests/imports", cast_to=PurchaseRequest, body=body)


class AsyncPurchaseRequests(AsyncAPIResource):
    """Read and import purchase requests (French: demandes d'achat) (async)."""

    async def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[PurchaseRequest]:
        """List purchase requests.

        Scope: ``purchase_requests:readonly``.
        Reference: https://pennylane.readme.io/reference/getpurchaserequests
        """
        return await self._get_page(
            "/purchase_requests",
            item_type=PurchaseRequest,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    async def get(self, purchase_request_id: int) -> PurchaseRequest:
        """Retrieve a purchase request by its Pennylane identifier.

        Scope: ``purchase_requests:readonly``.
        Reference: https://pennylane.readme.io/reference/getpurchaserequest
        """
        return await self._get(
            f"/purchase_requests/{purchase_request_id}", cast_to=PurchaseRequest
        )

    async def import_from_file(
        self,
        *,
        file_attachment_id: int,
        reason: str,
        supplier_id: int,
        purchase_order_number: str,
        currency_amount_before_tax: MoneyInput,
        currency_amount: MoneyInput,
        currency_tax: MoneyInput,
        delivery_address: dict[str, Any],
        purchase_request_lines: builtins.list[dict[str, Any]],
        estimated_delivery_date: dt.date | str | None = None,
        currency: str | None = None,
        amount: MoneyInput | None = None,
        tax: MoneyInput | None = None,
    ) -> PurchaseRequest:
        """Import a purchase order from a previously uploaded file attachment.

        Scope: ``purchase_requests:all``.
        Reference: https://pennylane.readme.io/reference/createpurchaserequestimport

        See :meth:`PurchaseRequests.import_from_file` for the full body documentation.
        """
        body = drop_none(
            {
                "file_attachment_id": file_attachment_id,
                "reason": reason,
                "estimated_delivery_date": jsonable(estimated_delivery_date),
                "supplier_id": supplier_id,
                "purchase_order_number": purchase_order_number,
                "currency": currency,
                "currency_amount_before_tax": jsonable(currency_amount_before_tax),
                "currency_amount": jsonable(currency_amount),
                "amount": jsonable(amount),
                "currency_tax": jsonable(currency_tax),
                "tax": jsonable(tax),
                "delivery_address": delivery_address,
                "purchase_request_lines": purchase_request_lines,
            }
        )
        return await self._post(
            "/purchase_requests/imports", cast_to=PurchaseRequest, body=body
        )
