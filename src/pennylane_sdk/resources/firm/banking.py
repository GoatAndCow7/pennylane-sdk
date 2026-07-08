"""Banking resources (Firm API v1): bank accounts and transactions.

Reference: https://firm-pennylane.readme.io/reference/getbankaccounts
"""

from __future__ import annotations

from ..._models import MoneyInput, drop_none
from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...filters import FiltersInput
from ...types.firm.banking import FirmBankAccount, FirmTransaction

__all__ = [
    "AsyncFirmBankAccounts",
    "AsyncFirmTransactions",
    "FirmBankAccounts",
    "FirmTransactions",
]


class FirmBankAccounts(SyncAPIResource):
    """Manage a client company's bank accounts."""

    def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[FirmBankAccount]:
        """List bank accounts of a client company.

        Scope: ``bank_accounts:readonly`` or ``bank_accounts:all``.
        Reference: https://firm-pennylane.readme.io/reference/getbankaccounts

        Args:
            company_id: Identifier of the client company.
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            f"/companies/{company_id}/bank_accounts",
            item_type=FirmBankAccount,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    def create(
        self,
        company_id: int,
        *,
        name: str,
        bank_establishment_id: int | None = None,
        iban: str | None = None,
        bic: str | None = None,
        currency: str | None = None,
        account_type: str | None = None,
    ) -> FirmBankAccount:
        """Create a bank account for a client company.

        Scope: ``bank_accounts:all``.
        Reference: https://firm-pennylane.readme.io/reference/postbankaccount

        Args:
            company_id: Identifier of the client company.
            name: The name of the bank account.
            bank_establishment_id: Bank establishment id (``Other`` if omitted).
            iban: International Bank Account Number.
            bic: Bank Identifier Code.
            currency: ISO currency code (default EUR).
            account_type: One of ``current`` (deprecated), ``card``, ``savings``,
                ``shares``, ``loan``, ``life_insurance``, ``other``, ``checking``.
        """
        body = drop_none(
            {
                "name": name,
                "bank_establishment_id": bank_establishment_id,
                "iban": iban,
                "bic": bic,
                "currency": currency,
                "account_type": account_type,
            }
        )
        return self._post(
            f"/companies/{company_id}/bank_accounts", cast_to=FirmBankAccount, body=body
        )


class FirmTransactions(SyncAPIResource):
    """Manage a client company's bank transactions."""

    def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[FirmTransaction]:
        """List transactions of a client company.

        Scope: ``transactions:readonly`` or ``transactions:all``.
        Reference: https://firm-pennylane.readme.io/reference/gettransactions

        Args:
            company_id: Identifier of the client company.
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            f"/companies/{company_id}/transactions",
            item_type=FirmTransaction,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    def create(
        self,
        company_id: int,
        *,
        bank_account_id: int,
        label: str,
        date: str,
        amount: MoneyInput,
        fee: MoneyInput | None = None,
    ) -> FirmTransaction:
        """Create a transaction for a client company.

        Scope: ``transactions:all``.
        Reference: https://firm-pennylane.readme.io/reference/createtransaction

        Args:
            company_id: Identifier of the client company.
            bank_account_id: The bank account where the transaction is registered.
            label: Transaction label.
            date: Transaction date (ISO 8601).
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
        return self._post(
            f"/companies/{company_id}/transactions", cast_to=FirmTransaction, body=body
        )

    def update(
        self,
        company_id: int,
        transaction_id: int,
        *,
        customer_id: int | None = None,
        supplier_id: int | None = None,
    ) -> FirmTransaction:
        """Match a transaction of a client company with a customer or a supplier.

        Scope: ``transactions:all``.
        Reference: https://firm-pennylane.readme.io/reference/updatetransaction

        Args:
            company_id: Identifier of the client company.
            transaction_id: Identifier of the transaction to update.
            customer_id: Identifier of the customer to match (mutually exclusive
                with ``supplier_id``).
            supplier_id: Identifier of the supplier to match (mutually exclusive
                with ``customer_id``).
        """
        body = drop_none({"customer_id": customer_id, "supplier_id": supplier_id})
        return self._put(
            f"/companies/{company_id}/transactions/{transaction_id}",
            cast_to=FirmTransaction,
            body=body,
        )


class AsyncFirmBankAccounts(AsyncAPIResource):
    """Manage a client company's bank accounts (async)."""

    async def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[FirmBankAccount]:
        """List bank accounts of a client company.

        Scope: ``bank_accounts:readonly`` or ``bank_accounts:all``.
        Reference: https://firm-pennylane.readme.io/reference/getbankaccounts
        """
        return await self._get_page(
            f"/companies/{company_id}/bank_accounts",
            item_type=FirmBankAccount,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    async def create(
        self,
        company_id: int,
        *,
        name: str,
        bank_establishment_id: int | None = None,
        iban: str | None = None,
        bic: str | None = None,
        currency: str | None = None,
        account_type: str | None = None,
    ) -> FirmBankAccount:
        """Create a bank account for a client company.

        Scope: ``bank_accounts:all``.
        Reference: https://firm-pennylane.readme.io/reference/postbankaccount
        """
        body = drop_none(
            {
                "name": name,
                "bank_establishment_id": bank_establishment_id,
                "iban": iban,
                "bic": bic,
                "currency": currency,
                "account_type": account_type,
            }
        )
        return await self._post(
            f"/companies/{company_id}/bank_accounts", cast_to=FirmBankAccount, body=body
        )


class AsyncFirmTransactions(AsyncAPIResource):
    """Manage a client company's bank transactions (async)."""

    async def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[FirmTransaction]:
        """List transactions of a client company.

        Scope: ``transactions:readonly`` or ``transactions:all``.
        Reference: https://firm-pennylane.readme.io/reference/gettransactions
        """
        return await self._get_page(
            f"/companies/{company_id}/transactions",
            item_type=FirmTransaction,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    async def create(
        self,
        company_id: int,
        *,
        bank_account_id: int,
        label: str,
        date: str,
        amount: MoneyInput,
        fee: MoneyInput | None = None,
    ) -> FirmTransaction:
        """Create a transaction for a client company.

        Scope: ``transactions:all``.
        Reference: https://firm-pennylane.readme.io/reference/createtransaction
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
        return await self._post(
            f"/companies/{company_id}/transactions", cast_to=FirmTransaction, body=body
        )

    async def update(
        self,
        company_id: int,
        transaction_id: int,
        *,
        customer_id: int | None = None,
        supplier_id: int | None = None,
    ) -> FirmTransaction:
        """Match a transaction of a client company with a customer or a supplier.

        Scope: ``transactions:all``.
        Reference: https://firm-pennylane.readme.io/reference/updatetransaction
        """
        body = drop_none({"customer_id": customer_id, "supplier_id": supplier_id})
        return await self._put(
            f"/companies/{company_id}/transactions/{transaction_id}",
            cast_to=FirmTransaction,
            body=body,
        )
