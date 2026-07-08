"""Models for the File Attachments resource (Company API v2)."""

from __future__ import annotations

import datetime as dt

from ..._models import PennylaneModel

__all__ = ["FileAttachment"]


class FileAttachment(PennylaneModel):
    """A file uploaded through the file attachments endpoint.

    Reference: https://pennylane.readme.io/reference/postfileattachments
    """

    id: int
    url: str | None = None
    filename: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
