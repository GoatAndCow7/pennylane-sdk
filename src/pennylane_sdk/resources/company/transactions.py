"""Transactions resource (Company API v2).

Reference: https://pennylane.readme.io/reference/gettransactions
"""

from __future__ import annotations

from typing import Any

from ..._models import MoneyInput, drop_none
from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...filters import FiltersInput
from ...types.company.transactions import (
    MatchedInvoiceLink,
    Transaction,
    TransactionCategoriesResponse,
    TransactionCategory,
)

__all__ = ["AsyncTransactions", "Transactions"]


class Transactions(SyncAPIResource):
    """Manage bank transactions."""

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[Transaction]:
        """List transactions.

        Scope: ``transactions:readonly``.
        Reference: https://pennylane.readme.io/reference/gettransactions

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            "/transactions",
            item_type=Transaction,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    def create(
        self,
        *,
        bank_account_id: int,
        label: str,
        date: str,
        amount: MoneyInput,
        fee: MoneyInput | None = None,
    ) -> Transaction:
        """Create a transaction.

        Scope: ``transactions:all``.
        Reference: https://pennylane.readme.io/reference/createtransaction

        Args:
            bank_account_id: Bank account the transaction is registered on.
            label: Transaction label.
            date: Transaction date (``YYYY-MM-DD``).
            amount: Transaction amount (``Decimal`` or string).
            fee: Transaction fee (``Decimal`` or string).
        """
        body = drop_none(
            {
                "bank_account_id": bank_account_id,
                "label": label,
                "date": date,
                "amount": amount,
                "fee": fee,
            }
        )
        return self._post("/transactions", cast_to=Transaction, body=body)

    def get(self, transaction_id: int) -> Transaction:
        """Retrieve a transaction by its Pennylane identifier.

        Scope: ``transactions:readonly``.
        Reference: https://pennylane.readme.io/reference/gettransaction
        """
        return self._get(f"/transactions/{transaction_id}", cast_to=Transaction)

    def update(
        self,
        transaction_id: int,
        *,
        customer_id: int | None = None,
        supplier_id: int | None = None,
    ) -> Transaction:
        """Update a transaction, linking it to a customer or a supplier.

        The body is a ``oneOf``: pass either ``customer_id`` or ``supplier_id``
        (either may be ``None`` to unlink).

        Scope: ``transactions:all``.
        Reference: https://pennylane.readme.io/reference/updatetransaction
        """
        body = drop_none({"customer_id": customer_id, "supplier_id": supplier_id})
        return self._put(f"/transactions/{transaction_id}", cast_to=Transaction, body=body)

    def list_categories(
        self,
        transaction_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> SyncCursorPage[TransactionCategory]:
        """List the analytical categories of a bank transaction.

        Scope: ``transactions:readonly``.
        Reference: https://pennylane.readme.io/reference/gettransactioncategories
        """
        return self._get_page(
            f"/transactions/{transaction_id}/categories",
            item_type=TransactionCategory,
            params={"cursor": cursor, "limit": limit},
        )

    def categorize(
        self, transaction_id: int, *, categories: list[dict[str, Any]]
    ) -> list[TransactionCategory]:
        """Set the analytical categories of a bank transaction.

        Categories may belong to different category groups; the weights of
        categories from the same group must sum to ``1``.

        Scope: ``transactions:all``.
        Reference: https://pennylane.readme.io/reference/puttransactioncategories

        Args:
            transaction_id: The transaction to categorize.
            categories: A list of ``{"id": <category id>, "weight": "<0-1>"}``.
        """
        response = self._put(
            f"/transactions/{transaction_id}/categories",
            cast_to=TransactionCategoriesResponse,
            body=categories,
        )
        return response.items

    def list_matched_invoices(
        self,
        transaction_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> SyncCursorPage[MatchedInvoiceLink]:
        """List the invoices matched to a bank transaction.

        Scope: ``transactions:readonly``.
        Reference: https://pennylane.readme.io/reference/gettransactionmatchedinvoices
        """
        return self._get_page(
            f"/transactions/{transaction_id}/matched_invoices",
            item_type=MatchedInvoiceLink,
            params={"cursor": cursor, "limit": limit},
        )


class AsyncTransactions(AsyncAPIResource):
    """Manage bank transactions (async)."""

    async def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[Transaction]:
        """List transactions.

        Scope: ``transactions:readonly``.
        Reference: https://pennylane.readme.io/reference/gettransactions
        """
        return await self._get_page(
            "/transactions",
            item_type=Transaction,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    async def create(
        self,
        *,
        bank_account_id: int,
        label: str,
        date: str,
        amount: MoneyInput,
        fee: MoneyInput | None = None,
    ) -> Transaction:
        """Create a transaction.

        Scope: ``transactions:all``.
        Reference: https://pennylane.readme.io/reference/createtransaction
        """
        body = drop_none(
            {
                "bank_account_id": bank_account_id,
                "label": label,
                "date": date,
                "amount": amount,
                "fee": fee,
            }
        )
        return await self._post("/transactions", cast_to=Transaction, body=body)

    async def get(self, transaction_id: int) -> Transaction:
        """Retrieve a transaction by its Pennylane identifier.

        Scope: ``transactions:readonly``.
        Reference: https://pennylane.readme.io/reference/gettransaction
        """
        return await self._get(f"/transactions/{transaction_id}", cast_to=Transaction)

    async def update(
        self,
        transaction_id: int,
        *,
        customer_id: int | None = None,
        supplier_id: int | None = None,
    ) -> Transaction:
        """Update a transaction, linking it to a customer or a supplier.

        The body is a ``oneOf``: pass either ``customer_id`` or ``supplier_id``
        (either may be ``None`` to unlink).

        Scope: ``transactions:all``.
        Reference: https://pennylane.readme.io/reference/updatetransaction
        """
        body = drop_none({"customer_id": customer_id, "supplier_id": supplier_id})
        return await self._put(f"/transactions/{transaction_id}", cast_to=Transaction, body=body)

    async def list_categories(
        self,
        transaction_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> AsyncCursorPage[TransactionCategory]:
        """List the analytical categories of a bank transaction.

        Scope: ``transactions:readonly``.
        Reference: https://pennylane.readme.io/reference/gettransactioncategories
        """
        return await self._get_page(
            f"/transactions/{transaction_id}/categories",
            item_type=TransactionCategory,
            params={"cursor": cursor, "limit": limit},
        )

    async def categorize(
        self, transaction_id: int, *, categories: list[dict[str, Any]]
    ) -> list[TransactionCategory]:
        """Set the analytical categories of a bank transaction.

        Categories may belong to different category groups; the weights of
        categories from the same group must sum to ``1``.

        Scope: ``transactions:all``.
        Reference: https://pennylane.readme.io/reference/puttransactioncategories

        Args:
            transaction_id: The transaction to categorize.
            categories: A list of ``{"id": <category id>, "weight": "<0-1>"}``.
        """
        response = await self._put(
            f"/transactions/{transaction_id}/categories",
            cast_to=TransactionCategoriesResponse,
            body=categories,
        )
        return response.items

    async def list_matched_invoices(
        self,
        transaction_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> AsyncCursorPage[MatchedInvoiceLink]:
        """List the invoices matched to a bank transaction.

        Scope: ``transactions:readonly``.
        Reference: https://pennylane.readme.io/reference/gettransactionmatchedinvoices
        """
        return await self._get_page(
            f"/transactions/{transaction_id}/matched_invoices",
            item_type=MatchedInvoiceLink,
            params={"cursor": cursor, "limit": limit},
        )
