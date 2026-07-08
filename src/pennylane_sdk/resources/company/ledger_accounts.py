"""Ledger Accounts resource (Company API v2).

Reference: https://pennylane.readme.io/reference/getledgeraccounts
"""

from __future__ import annotations

from ..._models import drop_none
from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...filters import FiltersInput
from ...types.company.ledger_accounts import LedgerAccount

__all__ = ["AsyncLedgerAccounts", "LedgerAccounts"]


class LedgerAccounts(SyncAPIResource):
    """Manage the company's chart of accounts."""

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[LedgerAccount]:
        """List ledger accounts.

        Scope: ``ledger_accounts:readonly``.
        Reference: https://pennylane.readme.io/reference/getledgeraccounts

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            "/ledger_accounts",
            item_type=LedgerAccount,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    def get(self, ledger_account_id: int) -> LedgerAccount:
        """Retrieve a ledger account by its Pennylane identifier.

        Scope: ``ledger_accounts:readonly``.
        Reference: https://pennylane.readme.io/reference/getledgeraccount
        """
        return self._get(f"/ledger_accounts/{ledger_account_id}", cast_to=LedgerAccount)

    def create(
        self,
        *,
        number: str,
        label: str,
        vat_rate: str | None = None,
        country_alpha2: str | None = None,
    ) -> LedgerAccount:
        """Create a ledger account.

        Scope: ``ledger_accounts:all``.
        Reference: https://pennylane.readme.io/reference/postledgeraccounts

        Args:
            number: Ledger account's number. If the number starts with ``401``
                (supplier) or ``411`` (customer), a corresponding third-party
                account may be created.
            label: Ledger account's label.
            vat_rate: VAT rate code, e.g. ``"FR_200"``.
            country_alpha2: Ledger account's country code (alpha2).
        """
        body = drop_none(
            {
                "number": number,
                "label": label,
                "vat_rate": vat_rate,
                "country_alpha2": country_alpha2,
            }
        )
        return self._post("/ledger_accounts", cast_to=LedgerAccount, body=body)

    def update(
        self,
        ledger_account_id: int,
        *,
        label: str | None = None,
        letterable: bool | None = None,
    ) -> LedgerAccount:
        """Update a ledger account. Only the provided fields are modified.

        Scope: ``ledger_accounts:all``.
        Reference: https://pennylane.readme.io/reference/updateledgeraccount

        Args:
            label: Label that describes the ledger account.
            letterable: Whether the ledger entries of this ledger account are
                letterable.
        """
        body = drop_none({"label": label, "letterable": letterable})
        return self._put(
            f"/ledger_accounts/{ledger_account_id}", cast_to=LedgerAccount, body=body
        )


class AsyncLedgerAccounts(AsyncAPIResource):
    """Manage the company's chart of accounts (async)."""

    async def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[LedgerAccount]:
        """List ledger accounts.

        Scope: ``ledger_accounts:readonly``.
        Reference: https://pennylane.readme.io/reference/getledgeraccounts
        """
        return await self._get_page(
            "/ledger_accounts",
            item_type=LedgerAccount,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    async def get(self, ledger_account_id: int) -> LedgerAccount:
        """Retrieve a ledger account by its Pennylane identifier.

        Scope: ``ledger_accounts:readonly``.
        Reference: https://pennylane.readme.io/reference/getledgeraccount
        """
        return await self._get(f"/ledger_accounts/{ledger_account_id}", cast_to=LedgerAccount)

    async def create(
        self,
        *,
        number: str,
        label: str,
        vat_rate: str | None = None,
        country_alpha2: str | None = None,
    ) -> LedgerAccount:
        """Create a ledger account.

        Scope: ``ledger_accounts:all``.
        Reference: https://pennylane.readme.io/reference/postledgeraccounts
        """
        body = drop_none(
            {
                "number": number,
                "label": label,
                "vat_rate": vat_rate,
                "country_alpha2": country_alpha2,
            }
        )
        return await self._post("/ledger_accounts", cast_to=LedgerAccount, body=body)

    async def update(
        self,
        ledger_account_id: int,
        *,
        label: str | None = None,
        letterable: bool | None = None,
    ) -> LedgerAccount:
        """Update a ledger account. Only the provided fields are modified.

        Scope: ``ledger_accounts:all``.
        Reference: https://pennylane.readme.io/reference/updateledgeraccount
        """
        body = drop_none({"label": label, "letterable": letterable})
        return await self._put(
            f"/ledger_accounts/{ledger_account_id}", cast_to=LedgerAccount, body=body
        )
