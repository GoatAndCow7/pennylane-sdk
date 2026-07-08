"""Models for the Changelogs resource (Firm API v1)."""

from __future__ import annotations

import datetime as dt

from ..._models import PennylaneModel

__all__ = ["ChangelogEvent"]


class ChangelogEvent(PennylaneModel):
    """A change event for a tracked resource record.

    Reference: https://firm-pennylane.readme.io/reference/getledgerentrylinechanges
    """

    id: int
    operation: str | None = None
    processed_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
    created_at: dt.datetime | None = None
