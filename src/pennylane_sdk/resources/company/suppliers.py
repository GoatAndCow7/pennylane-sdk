"""Suppliers resource (Company API v2).

Reference: https://pennylane.readme.io/reference/getsuppliers
"""

from __future__ import annotations

import builtins
from typing import Any

from ..._models import drop_none
from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...filters import FiltersInput
from ...types.company.suppliers import Supplier, SupplierCategory

__all__ = ["AsyncSuppliers", "Suppliers"]


class Suppliers(SyncAPIResource):
    """Manage suppliers."""

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[Supplier]:
        """List suppliers.

        Scope: ``suppliers:readonly``.
        Reference: https://pennylane.readme.io/reference/getsuppliers

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            "/suppliers",
            item_type=Supplier,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    def create(
        self,
        *,
        name: str,
        establishment_no: str | None = None,
        reg_no: str | None = None,
        postal_address: dict[str, Any] | None = None,
        vat_number: str | None = None,
        ledger_account: dict[str, Any] | None = None,
        emails: builtins.list[str] | None = None,
        iban: str | None = None,
        supplier_payment_method: str | None = None,
        supplier_due_date_delay: int | None = None,
        supplier_due_date_rule: str | None = None,
        external_reference: str | None = None,
    ) -> Supplier:
        """Create a supplier.

        Scope: ``suppliers:all``.
        Reference: https://pennylane.readme.io/reference/postsupplier

        Args:
            name: Supplier name.
            establishment_no: SIRET (14-digit French establishment number).
            reg_no: SIREN (9-digit French registration number).
            postal_address: ``{"address", "postal_code", "city", "country_alpha2"}``.
            vat_number: VAT number.
            ledger_account: ``{"number": <ledger account number>}``.
            emails: Email addresses.
            iban: Supplier IBAN.
            supplier_payment_method: One of ``automatic_transfer``, ``manual_transfer``,
                ``automatic_debiting``, ``bill_of_exchange``, ``check``, ``cash``,
                ``card``, ``other``.
            supplier_due_date_delay: Number of days before payment is due.
            supplier_due_date_rule: ``days`` or ``days_or_end_of_month``.
            external_reference: Your own unique reference (auto-assigned if omitted).
        """
        body = drop_none(
            {
                "name": name,
                "establishment_no": establishment_no,
                "reg_no": reg_no,
                "postal_address": postal_address,
                "vat_number": vat_number,
                "ledger_account": ledger_account,
                "emails": emails,
                "iban": iban,
                "supplier_payment_method": supplier_payment_method,
                "supplier_due_date_delay": supplier_due_date_delay,
                "supplier_due_date_rule": supplier_due_date_rule,
                "external_reference": external_reference,
            }
        )
        return self._post("/suppliers", cast_to=Supplier, body=body)

    def get(self, supplier_id: int) -> Supplier:
        """Retrieve a supplier by its Pennylane identifier.

        Scope: ``suppliers:readonly``.
        Reference: https://pennylane.readme.io/reference/getsupplier
        """
        return self._get(f"/suppliers/{supplier_id}", cast_to=Supplier)

    def update(
        self,
        supplier_id: int,
        *,
        name: str | None = None,
        establishment_no: str | None = None,
        reg_no: str | None = None,
        postal_address: dict[str, Any] | None = None,
        vat_number: str | None = None,
        emails: builtins.list[str] | None = None,
        iban: str | None = None,
        supplier_payment_method: str | None = None,
        supplier_due_date_delay: int | None = None,
        supplier_due_date_rule: str | None = None,
        external_reference: str | None = None,
    ) -> Supplier:
        """Update a supplier. Only the provided fields are modified.

        Scope: ``suppliers:all``.
        Reference: https://pennylane.readme.io/reference/putsupplier
        """
        body = drop_none(
            {
                "name": name,
                "establishment_no": establishment_no,
                "reg_no": reg_no,
                "postal_address": postal_address,
                "vat_number": vat_number,
                "emails": emails,
                "iban": iban,
                "supplier_payment_method": supplier_payment_method,
                "supplier_due_date_delay": supplier_due_date_delay,
                "supplier_due_date_rule": supplier_due_date_rule,
                "external_reference": external_reference,
            }
        )
        return self._put(f"/suppliers/{supplier_id}", cast_to=Supplier, body=body)

    def list_categories(
        self,
        supplier_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> SyncCursorPage[SupplierCategory]:
        """List the categories assigned to a supplier.

        Scope: ``suppliers:readonly``.
        Reference: https://pennylane.readme.io/reference/getsuppliercategories
        """
        return self._get_page(
            f"/suppliers/{supplier_id}/categories",
            item_type=SupplierCategory,
            params={"cursor": cursor, "limit": limit},
        )

    def categorize(self, supplier_id: int, *, categories: builtins.list[dict[str, Any]]) -> None:
        """Replace the categories assigned to a supplier.

        Scope: ``suppliers:all``.
        Reference: https://pennylane.readme.io/reference/putsuppliercategories

        Args:
            categories: List of ``{"id": <category id>, "weight": <str fraction, e.g. "0.6575">}``.
        """
        self._put(f"/suppliers/{supplier_id}/categories", cast_to=None, body=categories)


class AsyncSuppliers(AsyncAPIResource):
    """Manage suppliers (async)."""

    async def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[Supplier]:
        """List suppliers.

        Scope: ``suppliers:readonly``.
        Reference: https://pennylane.readme.io/reference/getsuppliers
        """
        return await self._get_page(
            "/suppliers",
            item_type=Supplier,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    async def create(
        self,
        *,
        name: str,
        establishment_no: str | None = None,
        reg_no: str | None = None,
        postal_address: dict[str, Any] | None = None,
        vat_number: str | None = None,
        ledger_account: dict[str, Any] | None = None,
        emails: builtins.list[str] | None = None,
        iban: str | None = None,
        supplier_payment_method: str | None = None,
        supplier_due_date_delay: int | None = None,
        supplier_due_date_rule: str | None = None,
        external_reference: str | None = None,
    ) -> Supplier:
        """Create a supplier.

        Scope: ``suppliers:all``.
        Reference: https://pennylane.readme.io/reference/postsupplier
        """
        body = drop_none(
            {
                "name": name,
                "establishment_no": establishment_no,
                "reg_no": reg_no,
                "postal_address": postal_address,
                "vat_number": vat_number,
                "ledger_account": ledger_account,
                "emails": emails,
                "iban": iban,
                "supplier_payment_method": supplier_payment_method,
                "supplier_due_date_delay": supplier_due_date_delay,
                "supplier_due_date_rule": supplier_due_date_rule,
                "external_reference": external_reference,
            }
        )
        return await self._post("/suppliers", cast_to=Supplier, body=body)

    async def get(self, supplier_id: int) -> Supplier:
        """Retrieve a supplier by its Pennylane identifier.

        Scope: ``suppliers:readonly``.
        Reference: https://pennylane.readme.io/reference/getsupplier
        """
        return await self._get(f"/suppliers/{supplier_id}", cast_to=Supplier)

    async def update(
        self,
        supplier_id: int,
        *,
        name: str | None = None,
        establishment_no: str | None = None,
        reg_no: str | None = None,
        postal_address: dict[str, Any] | None = None,
        vat_number: str | None = None,
        emails: builtins.list[str] | None = None,
        iban: str | None = None,
        supplier_payment_method: str | None = None,
        supplier_due_date_delay: int | None = None,
        supplier_due_date_rule: str | None = None,
        external_reference: str | None = None,
    ) -> Supplier:
        """Update a supplier. Only the provided fields are modified.

        Scope: ``suppliers:all``.
        Reference: https://pennylane.readme.io/reference/putsupplier
        """
        body = drop_none(
            {
                "name": name,
                "establishment_no": establishment_no,
                "reg_no": reg_no,
                "postal_address": postal_address,
                "vat_number": vat_number,
                "emails": emails,
                "iban": iban,
                "supplier_payment_method": supplier_payment_method,
                "supplier_due_date_delay": supplier_due_date_delay,
                "supplier_due_date_rule": supplier_due_date_rule,
                "external_reference": external_reference,
            }
        )
        return await self._put(f"/suppliers/{supplier_id}", cast_to=Supplier, body=body)

    async def list_categories(
        self,
        supplier_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> AsyncCursorPage[SupplierCategory]:
        """List the categories assigned to a supplier.

        Scope: ``suppliers:readonly``.
        Reference: https://pennylane.readme.io/reference/getsuppliercategories
        """
        return await self._get_page(
            f"/suppliers/{supplier_id}/categories",
            item_type=SupplierCategory,
            params={"cursor": cursor, "limit": limit},
        )

    async def categorize(self, supplier_id: int, *, categories: builtins.list[dict[str, Any]]) -> None:
        """Replace the categories assigned to a supplier.

        Scope: ``suppliers:all``.
        Reference: https://pennylane.readme.io/reference/putsuppliercategories
        """
        await self._put(f"/suppliers/{supplier_id}/categories", cast_to=None, body=categories)
