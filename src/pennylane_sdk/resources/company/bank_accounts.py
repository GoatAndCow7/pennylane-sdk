"""Bank Accounts and Bank Establishments resources (Company API v2).

Reference: https://pennylane.readme.io/reference/getbankaccounts
"""

from __future__ import annotations

from ..._models import drop_none
from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...filters import FiltersInput
from ...types.company.bank_accounts import BankAccount, BankEstablishment

__all__ = ["AsyncBankAccounts", "AsyncBankEstablishments", "BankAccounts", "BankEstablishments"]


class BankAccounts(SyncAPIResource):
    """Manage bank accounts."""

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[BankAccount]:
        """List bank accounts.

        Scope: ``bank_accounts:readonly``.
        Reference: https://pennylane.readme.io/reference/getbankaccounts

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            "/bank_accounts",
            item_type=BankAccount,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    def create(
        self,
        *,
        name: str,
        bank_establishment_id: int | None = None,
        iban: str | None = None,
        bic: str | None = None,
        currency: str | None = None,
        account_type: str | None = None,
    ) -> BankAccount:
        """Create a bank account.

        Scope: ``bank_accounts:all``.
        Reference: https://pennylane.readme.io/reference/postbankaccount

        Args:
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
        return self._post("/bank_accounts", cast_to=BankAccount, body=body)

    def get(self, bank_account_id: int) -> BankAccount:
        """Retrieve a bank account by its Pennylane identifier.

        Scope: ``bank_accounts:readonly``.
        Reference: https://pennylane.readme.io/reference/getbankaccount
        """
        return self._get(f"/bank_accounts/{bank_account_id}", cast_to=BankAccount)


class BankEstablishments(SyncAPIResource):
    """Browse the reference list of bank establishments."""

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[BankEstablishment]:
        """List bank establishments.

        Scope: ``bank_establishments:readonly``.
        Reference: https://pennylane.readme.io/reference/getbankestablishments

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            "/bank_establishments",
            item_type=BankEstablishment,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )


class AsyncBankAccounts(AsyncAPIResource):
    """Manage bank accounts (async)."""

    async def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[BankAccount]:
        """List bank accounts.

        Scope: ``bank_accounts:readonly``.
        Reference: https://pennylane.readme.io/reference/getbankaccounts
        """
        return await self._get_page(
            "/bank_accounts",
            item_type=BankAccount,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    async def create(
        self,
        *,
        name: str,
        bank_establishment_id: int | None = None,
        iban: str | None = None,
        bic: str | None = None,
        currency: str | None = None,
        account_type: str | None = None,
    ) -> BankAccount:
        """Create a bank account.

        Scope: ``bank_accounts:all``.
        Reference: https://pennylane.readme.io/reference/postbankaccount
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
        return await self._post("/bank_accounts", cast_to=BankAccount, body=body)

    async def get(self, bank_account_id: int) -> BankAccount:
        """Retrieve a bank account by its Pennylane identifier.

        Scope: ``bank_accounts:readonly``.
        Reference: https://pennylane.readme.io/reference/getbankaccount
        """
        return await self._get(f"/bank_accounts/{bank_account_id}", cast_to=BankAccount)


class AsyncBankEstablishments(AsyncAPIResource):
    """Browse the reference list of bank establishments (async)."""

    async def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[BankEstablishment]:
        """List bank establishments.

        Scope: ``bank_establishments:readonly``.
        Reference: https://pennylane.readme.io/reference/getbankestablishments
        """
        return await self._get_page(
            "/bank_establishments",
            item_type=BankEstablishment,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )
