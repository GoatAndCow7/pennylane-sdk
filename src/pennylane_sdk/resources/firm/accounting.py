"""Accounting resources (Firm API v1): fiscal years, trial balance, journals,
ledger accounts, ledger entries and ledger entry lines.

Reference: https://firm-pennylane.readme.io/reference/company-fiscal-years
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from ..._models import drop_none
from ..._pagination import AsyncCursorPage, AsyncNumberedPage, SyncCursorPage, SyncNumberedPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...filters import FiltersInput
from ...types.firm.accounting import (
    FirmFiscalYear,
    FirmJournal,
    FirmLedgerAccount,
    FirmLedgerEntry,
    FirmLedgerEntryLine,
    FirmTrialBalanceRow,
)

__all__ = [
    "AsyncFirmFiscalYears",
    "AsyncFirmJournals",
    "AsyncFirmLedgerAccounts",
    "AsyncFirmLedgerEntries",
    "AsyncFirmLedgerEntryLines",
    "AsyncFirmTrialBalance",
    "FirmFiscalYears",
    "FirmJournals",
    "FirmLedgerAccounts",
    "FirmLedgerEntries",
    "FirmLedgerEntryLines",
    "FirmTrialBalance",
]


class FirmFiscalYears(SyncAPIResource):
    """Manage a company's fiscal years."""

    def list(
        self,
        company_id: int,
        *,
        page: int | None = None,
        per_page: int | None = None,
    ) -> SyncNumberedPage[FirmFiscalYear]:
        """List a company's fiscal years.

        Scope: ``fiscal_years:all`` or ``fiscal_years:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/company-fiscal-years

        Args:
            company_id: The company's Pennylane identifier.
            page: Page index, starting at 1.
            per_page: Results per page.
        """
        return self._get_numbered_page(
            f"/companies/{company_id}/fiscal_years",
            item_type=FirmFiscalYear,
            params={"page": page, "per_page": per_page},
        )

    def create(self, company_id: int, *, start: str, finish: str) -> FirmFiscalYear:
        """Create a fiscal year for a company.

        Scope: ``fiscal_years:all``.
        Reference: https://firm-pennylane.readme.io/reference/postfiscalyears

        Args:
            company_id: The company's Pennylane identifier.
            start: Date at which the fiscal year starts (ISO 8601). Fiscal
                years must be consecutive.
            finish: Date at which the fiscal year ends (ISO 8601).
        """
        body = {"start": start, "finish": finish}
        return self._post(
            f"/companies/{company_id}/fiscal_years", cast_to=FirmFiscalYear, body=body
        )


class FirmTrialBalance(SyncAPIResource):
    """Read a company's trial balance."""

    def list(
        self,
        company_id: int,
        *,
        period_start: str,
        period_end: str,
        is_auxiliary: bool | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> SyncNumberedPage[FirmTrialBalanceRow]:
        """List the trial balance rows of a company for a period.

        Scope: ``trial_balance:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/company-trial-balance

        Args:
            company_id: The company's Pennylane identifier.
            period_start: Period start date (``YYYY-MM-DD``).
            period_end: Period end date (``YYYY-MM-DD``).
            is_auxiliary: Whether to include auxiliary ledger accounts.
            page: Page index, starting at 1.
            per_page: Results per page.
        """
        return self._get_numbered_page(
            f"/companies/{company_id}/trial_balance",
            item_type=FirmTrialBalanceRow,
            params={
                "period_start": period_start,
                "period_end": period_end,
                "is_auxiliary": is_auxiliary,
                "page": page,
                "per_page": per_page,
            },
        )


class FirmJournals(SyncAPIResource):
    """Manage a company's accounting journals."""

    def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
    ) -> SyncCursorPage[FirmJournal]:
        """List a company's journals.

        Scope: ``journals:all`` or ``journals:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getjournals

        Args:
            company_id: The company's Pennylane identifier.
            cursor: Pagination cursor from a previous page.
            limit: Results per page.
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
        """
        return self._get_page(
            f"/companies/{company_id}/journals",
            item_type=FirmJournal,
            params={"cursor": cursor, "limit": limit, "filter": filter},
        )

    def get(self, company_id: int, journal_id: int) -> FirmJournal:
        """Retrieve a journal by its Pennylane identifier.

        Scope: ``journals:all`` or ``journals:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getjournal
        """
        return self._get(f"/companies/{company_id}/journals/{journal_id}", cast_to=FirmJournal)

    def create(self, company_id: int, *, code: str, label: str) -> FirmJournal:
        """Create a journal for a company.

        Scope: ``journals:all``.
        Reference: https://firm-pennylane.readme.io/reference/postjournals

        Args:
            company_id: The company's Pennylane identifier.
            code: 2 to 5 letters that represent the journal.
            label: Label that describes the journal.
        """
        body = {"code": code, "label": label}
        return self._post(f"/companies/{company_id}/journals", cast_to=FirmJournal, body=body)


class FirmLedgerAccounts(SyncAPIResource):
    """Manage a company's ledger accounts."""

    def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
    ) -> SyncCursorPage[FirmLedgerAccount]:
        """List a company's ledger accounts.

        Scope: ``ledger_accounts:all`` or ``ledger_accounts:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getledgeraccounts

        Args:
            company_id: The company's Pennylane identifier.
            cursor: Pagination cursor from a previous page.
            limit: Results per page.
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
        """
        return self._get_page(
            f"/companies/{company_id}/ledger_accounts",
            item_type=FirmLedgerAccount,
            params={"cursor": cursor, "limit": limit, "filter": filter},
        )

    def get(self, company_id: int, ledger_account_id: int) -> FirmLedgerAccount:
        """Retrieve a ledger account by its Pennylane identifier.

        Scope: ``ledger_accounts:all`` or ``ledger_accounts:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getledgeraccount
        """
        return self._get(
            f"/companies/{company_id}/ledger_accounts/{ledger_account_id}",
            cast_to=FirmLedgerAccount,
        )

    def create(
        self,
        company_id: int,
        *,
        number: str,
        label: str,
        vat_rate: str | None = None,
        country_alpha2: str | None = None,
    ) -> FirmLedgerAccount:
        """Create a ledger account for a company.

        Scope: ``ledger_accounts:all``.
        Reference: https://firm-pennylane.readme.io/reference/postledgeraccounts

        Args:
            company_id: The company's Pennylane identifier.
            number: Ledger account number. If it starts with 401 (supplier)
                or 411 (customer), a corresponding third party is created.
            label: Ledger account label.
            vat_rate: VAT rate code.
            country_alpha2: Country code (alpha2).
        """
        body = drop_none(
            {
                "number": number,
                "label": label,
                "vat_rate": vat_rate,
                "country_alpha2": country_alpha2,
            }
        )
        return self._post(
            f"/companies/{company_id}/ledger_accounts", cast_to=FirmLedgerAccount, body=body
        )

    def update(
        self,
        company_id: int,
        ledger_account_id: int,
        *,
        label: str | None = None,
        letterable: bool | None = None,
    ) -> FirmLedgerAccount:
        """Update a ledger account. Only the provided fields are modified.

        Scope: ``ledger_accounts:all``.
        Reference: https://firm-pennylane.readme.io/reference/updateledgeraccount

        Args:
            company_id: The company's Pennylane identifier.
            ledger_account_id: The ledger account's Pennylane identifier.
            label: Label that describes the ledger account.
            letterable: Whether the ledger entries of this ledger account are
                letterable.
        """
        body = drop_none({"label": label, "letterable": letterable})
        return self._put(
            f"/companies/{company_id}/ledger_accounts/{ledger_account_id}",
            cast_to=FirmLedgerAccount,
            body=body,
        )


class FirmLedgerEntries(SyncAPIResource):
    """Manage a company's accounting ledger entries."""

    def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[FirmLedgerEntry]:
        """List a company's ledger entries.

        Scope: ``ledger_entries:all`` or ``ledger_entries:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getledgerentries

        Args:
            company_id: The company's Pennylane identifier.
            cursor: Pagination cursor from a previous page.
            limit: Results per page.
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending.
        """
        return self._get_page(
            f"/companies/{company_id}/ledger_entries",
            item_type=FirmLedgerEntry,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    def get(self, company_id: int, ledger_entry_id: int) -> FirmLedgerEntry:
        """Retrieve a ledger entry by its Pennylane identifier.

        Scope: ``ledger_entries:all`` or ``ledger_entries:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getledgerentry
        """
        return self._get(
            f"/companies/{company_id}/ledger_entries/{ledger_entry_id}", cast_to=FirmLedgerEntry
        )

    def create(
        self,
        company_id: int,
        *,
        date: str,
        label: str,
        journal_id: int,
        ledger_entry_lines: Sequence[dict[str, Any]],
        file_attachment_id: int | None = None,
        currency: str | None = None,
    ) -> FirmLedgerEntry:
        """Create a ledger entry for a company.

        Scope: ``ledger_entries:all``.
        Reference: https://firm-pennylane.readme.io/reference/postledgerentries

        Args:
            company_id: The company's Pennylane identifier.
            date: Date of the ledger entry (ISO 8601).
            label: Label that describes the ledger entry.
            journal_id: The journal ID where you want to create the ledger entry.
            ledger_entry_lines: Entry lines, each a dict with ``debit``,
                ``credit`` (Money strings) and ``ledger_account_id``, plus an
                optional ``label``. The API requires BOTH debit and credit on
                every line (set the unused side to ``"0.00"``). Must balance.
            file_attachment_id: File attachment ID.
            currency: ISO currency code applied to all lines (default EUR).
        """
        body = drop_none(
            {
                "date": date,
                "label": label,
                "journal_id": journal_id,
                "ledger_entry_lines": ledger_entry_lines,
                "file_attachment_id": file_attachment_id,
                "currency": currency,
            }
        )
        return self._post(
            f"/companies/{company_id}/ledger_entries", cast_to=FirmLedgerEntry, body=body
        )

    def update(
        self,
        company_id: int,
        ledger_entry_id: int,
        *,
        date: str | None = None,
        label: str | None = None,
        journal_id: int | None = None,
        ledger_entry_lines: dict[str, Any] | None = None,
        file_attachment_id: int | None = None,
        currency: str | None = None,
    ) -> FirmLedgerEntry:
        """Update a ledger entry. Only the provided fields are modified.

        Scope: ``ledger_entries:all``.
        Reference: https://firm-pennylane.readme.io/reference/putledgerentries

        Args:
            company_id: The company's Pennylane identifier.
            ledger_entry_id: The ledger entry's Pennylane identifier.
            date: Date of the ledger entry (ISO 8601).
            label: Label that describes the ledger entry.
            journal_id: The journal ID where you want to move the ledger entry.
            ledger_entry_lines: A dict with optional ``create``, ``update`` and
                ``delete`` lists to add, modify or remove entry lines. The
                resulting entry must balance.
            file_attachment_id: File attachment ID.
            currency: ISO currency code applied to all lines.
        """
        body = drop_none(
            {
                "date": date,
                "label": label,
                "journal_id": journal_id,
                "ledger_entry_lines": ledger_entry_lines,
                "file_attachment_id": file_attachment_id,
                "currency": currency,
            }
        )
        return self._put(
            f"/companies/{company_id}/ledger_entries/{ledger_entry_id}",
            cast_to=FirmLedgerEntry,
            body=body,
        )


class FirmLedgerEntryLines(SyncAPIResource):
    """Read a company's ledger entry lines."""

    def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[FirmLedgerEntryLine]:
        """List a company's ledger entry lines.

        Scope: ``ledger_entries:all`` or ``ledger_entries:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getledgerentrylines

        Args:
            company_id: The company's Pennylane identifier.
            cursor: Pagination cursor from a previous page.
            limit: Results per page.
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            f"/companies/{company_id}/ledger_entry_lines",
            item_type=FirmLedgerEntryLine,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    def get(self, company_id: int, ledger_entry_line_id: int) -> FirmLedgerEntryLine:
        """Retrieve a ledger entry line by its Pennylane identifier.

        Scope: ``ledger_entries:all`` or ``ledger_entries:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getledgerentryline
        """
        return self._get(
            f"/companies/{company_id}/ledger_entry_lines/{ledger_entry_line_id}",
            cast_to=FirmLedgerEntryLine,
        )

    def list_lettered_lines(
        self,
        company_id: int,
        ledger_entry_line_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[FirmLedgerEntryLine]:
        """List the ledger entry lines lettered with a given entry line.

        Scope: ``ledger_entries:all`` or ``ledger_entries:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getledgerentrylineslettered

        Args:
            company_id: The company's Pennylane identifier.
            ledger_entry_line_id: The ledger entry line's Pennylane identifier.
            cursor: Pagination cursor from a previous page.
            limit: Results per page.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            f"/companies/{company_id}/ledger_entry_lines/{ledger_entry_line_id}/lettered_ledger_entry_lines",
            item_type=FirmLedgerEntryLine,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )


class AsyncFirmFiscalYears(AsyncAPIResource):
    """Manage a company's fiscal years (async)."""

    async def list(
        self,
        company_id: int,
        *,
        page: int | None = None,
        per_page: int | None = None,
    ) -> AsyncNumberedPage[FirmFiscalYear]:
        """List a company's fiscal years.

        Scope: ``fiscal_years:all`` or ``fiscal_years:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/company-fiscal-years
        """
        return await self._get_numbered_page(
            f"/companies/{company_id}/fiscal_years",
            item_type=FirmFiscalYear,
            params={"page": page, "per_page": per_page},
        )

    async def create(self, company_id: int, *, start: str, finish: str) -> FirmFiscalYear:
        """Create a fiscal year for a company.

        Scope: ``fiscal_years:all``.
        Reference: https://firm-pennylane.readme.io/reference/postfiscalyears
        """
        body = {"start": start, "finish": finish}
        return await self._post(
            f"/companies/{company_id}/fiscal_years", cast_to=FirmFiscalYear, body=body
        )


class AsyncFirmTrialBalance(AsyncAPIResource):
    """Read a company's trial balance (async)."""

    async def list(
        self,
        company_id: int,
        *,
        period_start: str,
        period_end: str,
        is_auxiliary: bool | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> AsyncNumberedPage[FirmTrialBalanceRow]:
        """List the trial balance rows of a company for a period.

        Scope: ``trial_balance:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/company-trial-balance
        """
        return await self._get_numbered_page(
            f"/companies/{company_id}/trial_balance",
            item_type=FirmTrialBalanceRow,
            params={
                "period_start": period_start,
                "period_end": period_end,
                "is_auxiliary": is_auxiliary,
                "page": page,
                "per_page": per_page,
            },
        )


class AsyncFirmJournals(AsyncAPIResource):
    """Manage a company's accounting journals (async)."""

    async def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
    ) -> AsyncCursorPage[FirmJournal]:
        """List a company's journals.

        Scope: ``journals:all`` or ``journals:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getjournals
        """
        return await self._get_page(
            f"/companies/{company_id}/journals",
            item_type=FirmJournal,
            params={"cursor": cursor, "limit": limit, "filter": filter},
        )

    async def get(self, company_id: int, journal_id: int) -> FirmJournal:
        """Retrieve a journal by its Pennylane identifier.

        Scope: ``journals:all`` or ``journals:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getjournal
        """
        return await self._get(
            f"/companies/{company_id}/journals/{journal_id}", cast_to=FirmJournal
        )

    async def create(self, company_id: int, *, code: str, label: str) -> FirmJournal:
        """Create a journal for a company.

        Scope: ``journals:all``.
        Reference: https://firm-pennylane.readme.io/reference/postjournals
        """
        body = {"code": code, "label": label}
        return await self._post(
            f"/companies/{company_id}/journals", cast_to=FirmJournal, body=body
        )


class AsyncFirmLedgerAccounts(AsyncAPIResource):
    """Manage a company's ledger accounts (async)."""

    async def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
    ) -> AsyncCursorPage[FirmLedgerAccount]:
        """List a company's ledger accounts.

        Scope: ``ledger_accounts:all`` or ``ledger_accounts:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getledgeraccounts
        """
        return await self._get_page(
            f"/companies/{company_id}/ledger_accounts",
            item_type=FirmLedgerAccount,
            params={"cursor": cursor, "limit": limit, "filter": filter},
        )

    async def get(self, company_id: int, ledger_account_id: int) -> FirmLedgerAccount:
        """Retrieve a ledger account by its Pennylane identifier.

        Scope: ``ledger_accounts:all`` or ``ledger_accounts:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getledgeraccount
        """
        return await self._get(
            f"/companies/{company_id}/ledger_accounts/{ledger_account_id}",
            cast_to=FirmLedgerAccount,
        )

    async def create(
        self,
        company_id: int,
        *,
        number: str,
        label: str,
        vat_rate: str | None = None,
        country_alpha2: str | None = None,
    ) -> FirmLedgerAccount:
        """Create a ledger account for a company.

        Scope: ``ledger_accounts:all``.
        Reference: https://firm-pennylane.readme.io/reference/postledgeraccounts
        """
        body = drop_none(
            {
                "number": number,
                "label": label,
                "vat_rate": vat_rate,
                "country_alpha2": country_alpha2,
            }
        )
        return await self._post(
            f"/companies/{company_id}/ledger_accounts", cast_to=FirmLedgerAccount, body=body
        )

    async def update(
        self,
        company_id: int,
        ledger_account_id: int,
        *,
        label: str | None = None,
        letterable: bool | None = None,
    ) -> FirmLedgerAccount:
        """Update a ledger account. Only the provided fields are modified.

        Scope: ``ledger_accounts:all``.
        Reference: https://firm-pennylane.readme.io/reference/updateledgeraccount
        """
        body = drop_none({"label": label, "letterable": letterable})
        return await self._put(
            f"/companies/{company_id}/ledger_accounts/{ledger_account_id}",
            cast_to=FirmLedgerAccount,
            body=body,
        )


class AsyncFirmLedgerEntries(AsyncAPIResource):
    """Manage a company's accounting ledger entries (async)."""

    async def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[FirmLedgerEntry]:
        """List a company's ledger entries.

        Scope: ``ledger_entries:all`` or ``ledger_entries:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getledgerentries
        """
        return await self._get_page(
            f"/companies/{company_id}/ledger_entries",
            item_type=FirmLedgerEntry,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    async def get(self, company_id: int, ledger_entry_id: int) -> FirmLedgerEntry:
        """Retrieve a ledger entry by its Pennylane identifier.

        Scope: ``ledger_entries:all`` or ``ledger_entries:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getledgerentry
        """
        return await self._get(
            f"/companies/{company_id}/ledger_entries/{ledger_entry_id}", cast_to=FirmLedgerEntry
        )

    async def create(
        self,
        company_id: int,
        *,
        date: str,
        label: str,
        journal_id: int,
        ledger_entry_lines: Sequence[dict[str, Any]],
        file_attachment_id: int | None = None,
        currency: str | None = None,
    ) -> FirmLedgerEntry:
        """Create a ledger entry for a company.

        Scope: ``ledger_entries:all``.
        Reference: https://firm-pennylane.readme.io/reference/postledgerentries
        """
        body = drop_none(
            {
                "date": date,
                "label": label,
                "journal_id": journal_id,
                "ledger_entry_lines": ledger_entry_lines,
                "file_attachment_id": file_attachment_id,
                "currency": currency,
            }
        )
        return await self._post(
            f"/companies/{company_id}/ledger_entries", cast_to=FirmLedgerEntry, body=body
        )

    async def update(
        self,
        company_id: int,
        ledger_entry_id: int,
        *,
        date: str | None = None,
        label: str | None = None,
        journal_id: int | None = None,
        ledger_entry_lines: dict[str, Any] | None = None,
        file_attachment_id: int | None = None,
        currency: str | None = None,
    ) -> FirmLedgerEntry:
        """Update a ledger entry. Only the provided fields are modified.

        Scope: ``ledger_entries:all``.
        Reference: https://firm-pennylane.readme.io/reference/putledgerentries
        """
        body = drop_none(
            {
                "date": date,
                "label": label,
                "journal_id": journal_id,
                "ledger_entry_lines": ledger_entry_lines,
                "file_attachment_id": file_attachment_id,
                "currency": currency,
            }
        )
        return await self._put(
            f"/companies/{company_id}/ledger_entries/{ledger_entry_id}",
            cast_to=FirmLedgerEntry,
            body=body,
        )


class AsyncFirmLedgerEntryLines(AsyncAPIResource):
    """Read a company's ledger entry lines (async)."""

    async def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[FirmLedgerEntryLine]:
        """List a company's ledger entry lines.

        Scope: ``ledger_entries:all`` or ``ledger_entries:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getledgerentrylines
        """
        return await self._get_page(
            f"/companies/{company_id}/ledger_entry_lines",
            item_type=FirmLedgerEntryLine,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    async def get(self, company_id: int, ledger_entry_line_id: int) -> FirmLedgerEntryLine:
        """Retrieve a ledger entry line by its Pennylane identifier.

        Scope: ``ledger_entries:all`` or ``ledger_entries:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getledgerentryline
        """
        return await self._get(
            f"/companies/{company_id}/ledger_entry_lines/{ledger_entry_line_id}",
            cast_to=FirmLedgerEntryLine,
        )

    async def list_lettered_lines(
        self,
        company_id: int,
        ledger_entry_line_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[FirmLedgerEntryLine]:
        """List the ledger entry lines lettered with a given entry line.

        Scope: ``ledger_entries:all`` or ``ledger_entries:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/getledgerentrylineslettered
        """
        return await self._get_page(
            f"/companies/{company_id}/ledger_entry_lines/{ledger_entry_line_id}/lettered_ledger_entry_lines",
            item_type=FirmLedgerEntryLine,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )
