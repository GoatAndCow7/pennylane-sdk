"""Models for the Journals resource (Company API v2)."""

from __future__ import annotations

from ..._models import PennylaneModel

__all__ = ["Journal"]


class Journal(PennylaneModel):
    """An accounting journal.

    Reference: https://pennylane.readme.io/reference/getjournal
    """

    id: int
    code: str | None = None
    label: str | None = None
    type: str | None = None
