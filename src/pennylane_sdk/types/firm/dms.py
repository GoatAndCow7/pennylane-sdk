"""Models for the DMS (document management) and File Attachments resources (Firm API v1)."""

from __future__ import annotations

import datetime as dt

from ..._models import PennylaneModel

__all__ = ["DmsFile", "DmsFolder", "DmsFolderFiles", "DmsParentFolder", "FileAttachment"]


class DmsParentFolder(PennylaneModel):
    """Parent folder reference for a DMS file or folder."""

    id: int | None = None


class DmsFolderFiles(PennylaneModel):
    """Link to the files contained in a DMS folder."""

    url: str | None = None


class DmsFile(PennylaneModel):
    """A file stored in the Firm DMS (GED).

    Reference: https://firm-pennylane.readme.io/reference/company-dms-files
    """

    id: int
    name: str | None = None
    path: str | None = None
    parent_folder: DmsParentFolder | None = None
    url: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class DmsFolder(PennylaneModel):
    """A folder stored in the Firm DMS (GED).

    Reference: https://firm-pennylane.readme.io/reference/listdmsfolders
    """

    id: int
    name: str | None = None
    path: str | None = None
    parent_folder: DmsParentFolder | None = None
    files: DmsFolderFiles | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class FileAttachment(PennylaneModel):
    """A file uploaded through the file attachments endpoint.

    Reference: https://firm-pennylane.readme.io/reference/postfileattachments
    """

    id: int
    url: str | None = None
    filename: str | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None
