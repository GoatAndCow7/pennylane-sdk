"""Ledger Entries and Ledger Attachments resources (Company API v2).

Reference: https://pennylane.readme.io/reference/getledgerentries
"""

from __future__ import annotations

from typing import Any

from ..._files import FileInput, to_httpx_file
from ..._models import drop_none
from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...filters import FiltersInput
from ...types.company.ledger_entries import LedgerAttachment, LedgerEntry, LedgerEntryLine

__all__ = ["AsyncLedgerAttachments", "AsyncLedgerEntries", "LedgerAttachments", "LedgerEntries"]


class LedgerEntries(SyncAPIResource):
    """Manage the company's accounting ledger entries."""

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[LedgerEntry]:
        """List ledger entries.

        Scope: ``ledger_entries:readonly``.
        Reference: https://pennylane.readme.io/reference/getledgerentries

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            "/ledger_entries",
            item_type=LedgerEntry,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    def get(self, ledger_entry_id: int) -> LedgerEntry:
        """Retrieve a ledger entry by its Pennylane identifier.

        Scope: ``ledger_entries:readonly``.
        Reference: https://pennylane.readme.io/reference/getledgerentry
        """
        return self._get(f"/ledger_entries/{ledger_entry_id}", cast_to=LedgerEntry)

    def create(
        self,
        *,
        date: str,
        label: str,
        journal_id: int,
        ledger_entry_lines: list[dict[str, Any]],
        due_date: str | None = None,
        ledger_attachment_id: int | None = None,
        file_attachment_id: int | None = None,
        currency: str | None = None,
        piece_number: str | None = None,
    ) -> LedgerEntry:
        """Create a ledger entry.

        Scope: ``ledger_entries:all``.
        Reference: https://pennylane.readme.io/reference/postledgerentries

        Args:
            date: Date of the ledger entry (ISO 8601).
            label: Label that describes the ledger entry.
            journal_id: The journal ID where you want to create the ledger entry.
            ledger_entry_lines: Entry lines, each a dict with ``debit``,
                ``credit`` (Money strings) and ``ledger_account_id``, plus an
                optional ``label``. Must balance. Max 1,000 lines per request.
            due_date: Due date of the ledger entry (ISO 8601).
            ledger_attachment_id: Deprecated, use ``file_attachment_id`` instead.
            file_attachment_id: File attachment ID.
            currency: ISO 4217 currency code applied to all lines (default EUR).
            piece_number: Your own tracking identifier for this ledger entry.
        """
        body = drop_none(
            {
                "date": date,
                "label": label,
                "journal_id": journal_id,
                "ledger_entry_lines": ledger_entry_lines,
                "due_date": due_date,
                "ledger_attachment_id": ledger_attachment_id,
                "file_attachment_id": file_attachment_id,
                "currency": currency,
                "piece_number": piece_number,
            }
        )
        return self._post("/ledger_entries", cast_to=LedgerEntry, body=body)

    def update(
        self,
        ledger_entry_id: int,
        *,
        date: str | None = None,
        label: str | None = None,
        journal_id: int | None = None,
        ledger_entry_lines: dict[str, Any] | None = None,
        ledger_attachment_id: int | None = None,
        file_attachment_id: int | None = None,
        currency: str | None = None,
        piece_number: str | None = None,
    ) -> LedgerEntry:
        """Update a ledger entry. Only the provided fields are modified.

        Scope: ``ledger_entries:all``.
        Reference: https://pennylane.readme.io/reference/putledgerentries

        Args:
            date: Date of the ledger entry (ISO 8601).
            label: Label that describes the ledger entry.
            journal_id: The journal ID where you want to move the ledger entry.
            ledger_entry_lines: A dict with optional ``create``, ``update`` and
                ``delete`` lists to add, modify or remove entry lines. The
                resulting entry must balance. Max 1,000 lines affected per
                request.
            ledger_attachment_id: Deprecated, use ``file_attachment_id`` instead.
            file_attachment_id: File attachment ID.
            currency: ISO 4217 currency code applied to all lines.
            piece_number: The piece number assigned during creation.
        """
        body = drop_none(
            {
                "date": date,
                "label": label,
                "journal_id": journal_id,
                "ledger_entry_lines": ledger_entry_lines,
                "ledger_attachment_id": ledger_attachment_id,
                "file_attachment_id": file_attachment_id,
                "currency": currency,
                "piece_number": piece_number,
            }
        )
        return self._put(f"/ledger_entries/{ledger_entry_id}", cast_to=LedgerEntry, body=body)

    def list_lines(
        self,
        ledger_entry_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[LedgerEntryLine]:
        """List the entry lines of a ledger entry.

        Scope: ``ledger_entries:readonly``.
        Reference: https://pennylane.readme.io/reference/getledgerentriesledgerentrylines

        Args:
            ledger_entry_id: The ledger entry's Pennylane identifier.
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            f"/ledger_entries/{ledger_entry_id}/ledger_entry_lines",
            item_type=LedgerEntryLine,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )


class LedgerAttachments(SyncAPIResource):
    """Upload files to attach to ledger entries."""

    def create(self, file: FileInput, filename: str | None = None) -> LedgerAttachment:
        """Upload a file to attach to a ledger entry.

        Scope: ``ledger``.
        Reference: https://pennylane.readme.io/reference/postledgerattachments

        .. deprecated:: Pennylane has deprecated this endpoint.

        Args:
            file: The file to upload (path, bytes, file-like object or
                ``(filename, content)`` tuple). Allowed content types include
                ``image/png``, ``image/jpeg`` and PDF.
            filename: Name of the file. Defaults to the uploaded file's name.
        """
        return self._post(
            "/ledger_attachments",
            cast_to=LedgerAttachment,
            files={"file": to_httpx_file(file, filename=filename)},
            data=drop_none({"filename": filename}),
        )


class AsyncLedgerEntries(AsyncAPIResource):
    """Manage the company's accounting ledger entries (async)."""

    async def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[LedgerEntry]:
        """List ledger entries.

        Scope: ``ledger_entries:readonly``.
        Reference: https://pennylane.readme.io/reference/getledgerentries
        """
        return await self._get_page(
            "/ledger_entries",
            item_type=LedgerEntry,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    async def get(self, ledger_entry_id: int) -> LedgerEntry:
        """Retrieve a ledger entry by its Pennylane identifier.

        Scope: ``ledger_entries:readonly``.
        Reference: https://pennylane.readme.io/reference/getledgerentry
        """
        return await self._get(f"/ledger_entries/{ledger_entry_id}", cast_to=LedgerEntry)

    async def create(
        self,
        *,
        date: str,
        label: str,
        journal_id: int,
        ledger_entry_lines: list[dict[str, Any]],
        due_date: str | None = None,
        ledger_attachment_id: int | None = None,
        file_attachment_id: int | None = None,
        currency: str | None = None,
        piece_number: str | None = None,
    ) -> LedgerEntry:
        """Create a ledger entry.

        Scope: ``ledger_entries:all``.
        Reference: https://pennylane.readme.io/reference/postledgerentries
        """
        body = drop_none(
            {
                "date": date,
                "label": label,
                "journal_id": journal_id,
                "ledger_entry_lines": ledger_entry_lines,
                "due_date": due_date,
                "ledger_attachment_id": ledger_attachment_id,
                "file_attachment_id": file_attachment_id,
                "currency": currency,
                "piece_number": piece_number,
            }
        )
        return await self._post("/ledger_entries", cast_to=LedgerEntry, body=body)

    async def update(
        self,
        ledger_entry_id: int,
        *,
        date: str | None = None,
        label: str | None = None,
        journal_id: int | None = None,
        ledger_entry_lines: dict[str, Any] | None = None,
        ledger_attachment_id: int | None = None,
        file_attachment_id: int | None = None,
        currency: str | None = None,
        piece_number: str | None = None,
    ) -> LedgerEntry:
        """Update a ledger entry. Only the provided fields are modified.

        Scope: ``ledger_entries:all``.
        Reference: https://pennylane.readme.io/reference/putledgerentries
        """
        body = drop_none(
            {
                "date": date,
                "label": label,
                "journal_id": journal_id,
                "ledger_entry_lines": ledger_entry_lines,
                "ledger_attachment_id": ledger_attachment_id,
                "file_attachment_id": file_attachment_id,
                "currency": currency,
                "piece_number": piece_number,
            }
        )
        return await self._put(
            f"/ledger_entries/{ledger_entry_id}", cast_to=LedgerEntry, body=body
        )

    async def list_lines(
        self,
        ledger_entry_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[LedgerEntryLine]:
        """List the entry lines of a ledger entry.

        Scope: ``ledger_entries:readonly``.
        Reference: https://pennylane.readme.io/reference/getledgerentriesledgerentrylines
        """
        return await self._get_page(
            f"/ledger_entries/{ledger_entry_id}/ledger_entry_lines",
            item_type=LedgerEntryLine,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )


class AsyncLedgerAttachments(AsyncAPIResource):
    """Upload files to attach to ledger entries (async)."""

    async def create(self, file: FileInput, filename: str | None = None) -> LedgerAttachment:
        """Upload a file to attach to a ledger entry.

        Scope: ``ledger``.
        Reference: https://pennylane.readme.io/reference/postledgerattachments

        .. deprecated:: Pennylane has deprecated this endpoint.
        """
        return await self._post(
            "/ledger_attachments",
            cast_to=LedgerAttachment,
            files={"file": to_httpx_file(file, filename=filename)},
            data=drop_none({"filename": filename}),
        )
