"""Models for the Changelogs resource (Company API v2)."""

from __future__ import annotations

import datetime as dt

from ..._models import PennylaneModel

__all__ = ["ChangelogEvent"]


class ChangelogEvent(PennylaneModel):
    """A change event for a tracked resource record.

    Reference: https://pennylane.readme.io/reference/getcustomerinvoiceschanges
    """

    id: int
    operation: str | None = None
    processed_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
    created_at: dt.datetime | None = None
