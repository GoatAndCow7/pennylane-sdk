"""File attachments resource (Company API v2).

Reference: https://pennylane.readme.io/reference/postfileattachments
"""

from __future__ import annotations

from ..._files import FileInput, to_httpx_file
from ..._models import drop_none
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...types.company.file_attachments import FileAttachment

__all__ = ["AsyncFileAttachments", "FileAttachments"]


class FileAttachments(SyncAPIResource):
    """Upload files to attach to other resources."""

    def create(self, file: FileInput, *, filename: str | None = None) -> FileAttachment:
        """Upload a file to attach to any resource that provides a ``file_attachment_id``.

        This does not upload the file into the DMS (GED). The maximum allowed
        file size is 100MB. Allowed content types: ``image/png``,
        ``image/jpeg``, ``image/tiff``, ``image/bmp``, ``image/gif``,
        ``application/pdf``.

        Scope: ``file_attachments:all``.
        Reference: https://pennylane.readme.io/reference/postfileattachments

        Args:
            file: A path, raw bytes, a binary file-like object, or a
                ``(filename, content)`` tuple.
            filename: Name of the file (max 255 characters). Defaults to the
                uploaded file's own name.
        """
        return self._post(
            "/file_attachments",
            cast_to=FileAttachment,
            files={"file": to_httpx_file(file, filename=filename)},
            data=drop_none({"filename": filename}),
        )


class AsyncFileAttachments(AsyncAPIResource):
    """Upload files to attach to other resources (async)."""

    async def create(self, file: FileInput, *, filename: str | None = None) -> FileAttachment:
        """Upload a file to attach to any resource that provides a ``file_attachment_id``.

        This does not upload the file into the DMS (GED). The maximum allowed
        file size is 100MB. Allowed content types: ``image/png``,
        ``image/jpeg``, ``image/tiff``, ``image/bmp``, ``image/gif``,
        ``application/pdf``.

        Scope: ``file_attachments:all``.
        Reference: https://pennylane.readme.io/reference/postfileattachments

        Args:
            file: A path, raw bytes, a binary file-like object, or a
                ``(filename, content)`` tuple.
            filename: Name of the file (max 255 characters). Defaults to the
                uploaded file's own name.
        """
        return await self._post(
            "/file_attachments",
            cast_to=FileAttachment,
            files={"file": to_httpx_file(file, filename=filename)},
            data=drop_none({"filename": filename}),
        )
