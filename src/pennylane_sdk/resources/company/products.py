"""Products resource (Company API v2).

Reference: https://pennylane.readme.io/reference/getproducts
"""

from __future__ import annotations

from ..._models import MoneyInput, drop_none
from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...filters import FiltersInput
from ...types.company.products import Product

__all__ = ["AsyncProducts", "Products"]


class Products(SyncAPIResource):
    """Manage the company product catalog."""

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[Product]:
        """List products.

        Scope: ``products:readonly``.
        Reference: https://pennylane.readme.io/reference/getproducts

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            "/products",
            item_type=Product,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    def get(self, product_id: int) -> Product:
        """Retrieve a product by its Pennylane identifier.

        Scope: ``products:readonly``.
        Reference: https://pennylane.readme.io/reference/getproduct
        """
        return self._get(f"/products/{product_id}", cast_to=Product)

    def create(
        self,
        *,
        label: str,
        price_before_tax: MoneyInput,
        vat_rate: str,
        description: str | None = None,
        external_reference: str | None = None,
        unit: str | None = None,
        currency: str | None = None,
        reference: str | None = None,
        ledger_account_id: int | None = None,
    ) -> Product:
        """Create a product.

        Scope: ``products:all``.
        Reference: https://pennylane.readme.io/reference/postproducts

        Args:
            label: Product label.
            price_before_tax: Price without taxes (``Decimal`` or string).
            vat_rate: VAT rate code: a 20% French VAT is ``"FR_200"``.
            description: Product description (max 5,000 characters).
            external_reference: Your own unique reference for this product.
            unit: Product unit.
            currency: ISO currency code (default EUR).
            reference: Product reference shown on documents.
            ledger_account_id: Ledger account to book sales on.
        """
        body = drop_none(
            {
                "label": label,
                "price_before_tax": price_before_tax,
                "vat_rate": vat_rate,
                "description": description,
                "external_reference": external_reference,
                "unit": unit,
                "currency": currency,
                "reference": reference,
                "ledger_account_id": ledger_account_id,
            }
        )
        return self._post("/products", cast_to=Product, body=body)

    def update(
        self,
        product_id: int,
        *,
        label: str | None = None,
        price_before_tax: MoneyInput | None = None,
        vat_rate: str | None = None,
        description: str | None = None,
        external_reference: str | None = None,
        unit: str | None = None,
        currency: str | None = None,
        reference: str | None = None,
        ledger_account_id: int | None = None,
    ) -> Product:
        """Update a product. Only the provided fields are modified.

        Scope: ``products:all``.
        Reference: https://pennylane.readme.io/reference/putproduct
        """
        body = drop_none(
            {
                "label": label,
                "price_before_tax": price_before_tax,
                "vat_rate": vat_rate,
                "description": description,
                "external_reference": external_reference,
                "unit": unit,
                "currency": currency,
                "reference": reference,
                "ledger_account_id": ledger_account_id,
            }
        )
        return self._put(f"/products/{product_id}", cast_to=Product, body=body)


class AsyncProducts(AsyncAPIResource):
    """Manage the company product catalog (async)."""

    async def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[Product]:
        """List products.

        Scope: ``products:readonly``.
        Reference: https://pennylane.readme.io/reference/getproducts
        """
        return await self._get_page(
            "/products",
            item_type=Product,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    async def get(self, product_id: int) -> Product:
        """Retrieve a product by its Pennylane identifier.

        Scope: ``products:readonly``.
        Reference: https://pennylane.readme.io/reference/getproduct
        """
        return await self._get(f"/products/{product_id}", cast_to=Product)

    async def create(
        self,
        *,
        label: str,
        price_before_tax: MoneyInput,
        vat_rate: str,
        description: str | None = None,
        external_reference: str | None = None,
        unit: str | None = None,
        currency: str | None = None,
        reference: str | None = None,
        ledger_account_id: int | None = None,
    ) -> Product:
        """Create a product.

        Scope: ``products:all``.
        Reference: https://pennylane.readme.io/reference/postproducts
        """
        body = drop_none(
            {
                "label": label,
                "price_before_tax": price_before_tax,
                "vat_rate": vat_rate,
                "description": description,
                "external_reference": external_reference,
                "unit": unit,
                "currency": currency,
                "reference": reference,
                "ledger_account_id": ledger_account_id,
            }
        )
        return await self._post("/products", cast_to=Product, body=body)

    async def update(
        self,
        product_id: int,
        *,
        label: str | None = None,
        price_before_tax: MoneyInput | None = None,
        vat_rate: str | None = None,
        description: str | None = None,
        external_reference: str | None = None,
        unit: str | None = None,
        currency: str | None = None,
        reference: str | None = None,
        ledger_account_id: int | None = None,
    ) -> Product:
        """Update a product. Only the provided fields are modified.

        Scope: ``products:all``.
        Reference: https://pennylane.readme.io/reference/putproduct
        """
        body = drop_none(
            {
                "label": label,
                "price_before_tax": price_before_tax,
                "vat_rate": vat_rate,
                "description": description,
                "external_reference": external_reference,
                "unit": unit,
                "currency": currency,
                "reference": reference,
                "ledger_account_id": ledger_account_id,
            }
        )
        return await self._put(f"/products/{product_id}", cast_to=Product, body=body)
