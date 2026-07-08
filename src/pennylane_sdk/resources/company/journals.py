"""Journals resource (Company API v2).

Reference: https://pennylane.readme.io/reference/getjournals
"""

from __future__ import annotations

from ..._models import drop_none
from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...filters import FiltersInput
from ...types.company.journals import Journal

__all__ = ["AsyncJournals", "Journals"]


class Journals(SyncAPIResource):
    """Manage the company's accounting journals."""

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[Journal]:
        """List journals.

        Scope: ``journals:readonly``.
        Reference: https://pennylane.readme.io/reference/getjournals

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            "/journals",
            item_type=Journal,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    def get(self, journal_id: int) -> Journal:
        """Retrieve a journal by its Pennylane identifier.

        Scope: ``journals:readonly``.
        Reference: https://pennylane.readme.io/reference/getjournal
        """
        return self._get(f"/journals/{journal_id}", cast_to=Journal)

    def create(self, *, code: str, label: str) -> Journal:
        """Create a journal.

        Scope: ``journals:all``.
        Reference: https://pennylane.readme.io/reference/postjournals

        Args:
            code: 2 to 5 letters that represent the journal.
            label: Label that describes the journal.
        """
        body = drop_none({"code": code, "label": label})
        return self._post("/journals", cast_to=Journal, body=body)


class AsyncJournals(AsyncAPIResource):
    """Manage the company's accounting journals (async)."""

    async def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[Journal]:
        """List journals.

        Scope: ``journals:readonly``.
        Reference: https://pennylane.readme.io/reference/getjournals
        """
        return await self._get_page(
            "/journals",
            item_type=Journal,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    async def get(self, journal_id: int) -> Journal:
        """Retrieve a journal by its Pennylane identifier.

        Scope: ``journals:readonly``.
        Reference: https://pennylane.readme.io/reference/getjournal
        """
        return await self._get(f"/journals/{journal_id}", cast_to=Journal)

    async def create(self, *, code: str, label: str) -> Journal:
        """Create a journal.

        Scope: ``journals:all``.
        Reference: https://pennylane.readme.io/reference/postjournals
        """
        body = drop_none({"code": code, "label": label})
        return await self._post("/journals", cast_to=Journal, body=body)
