"""DMS (document management, GED) and File Attachments resources (Firm API v1).

Reference: https://firm-pennylane.readme.io/reference/company-dms-files
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..._files import FileInput, to_httpx_file
from ..._models import drop_none
from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...filters import FiltersInput
from ...types.firm.dms import DmsFile, DmsFolder, FileAttachment

if TYPE_CHECKING:
    from ..._base_client import AsyncAPIClient, SyncAPIClient

__all__ = [
    "AsyncFirmDms",
    "AsyncFirmDmsFiles",
    "AsyncFirmDmsFolders",
    "AsyncFirmFileAttachments",
    "FirmDms",
    "FirmDmsFiles",
    "FirmDmsFolders",
    "FirmFileAttachments",
]


class FirmDmsFiles(SyncAPIResource):
    """Manage files stored in the Firm DMS (GED)."""

    def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
    ) -> SyncCursorPage[DmsFile]:
        """List a company's DMS files.

        Scope: ``dms_files:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/company-dms-files

        Args:
            company_id: Identifier of the company.
            cursor: Pagination cursor from a previous page.
            limit: Results per page.
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
        """
        return self._get_page(
            f"/companies/{company_id}/dms/files",
            item_type=DmsFile,
            params={"cursor": cursor, "limit": limit, "filter": filter},
        )

    def create(
        self,
        company_id: int,
        file: FileInput,
        *,
        name: str | None = None,
        parent_folder_id: int | None = None,
    ) -> DmsFile:
        """Upload a file to the DMS.

        Scope: ``dms_files:all``.
        Reference: https://firm-pennylane.readme.io/reference/postdmsfiles

        Args:
            company_id: Identifier of the company.
            file: A path, raw bytes, a binary file-like object, or a
                ``(filename, content)`` tuple.
            name: Name of the file. Defaults to the uploaded file's own name.
            parent_folder_id: Parent folder to upload into. Defaults to root level.
        """
        return self._post(
            f"/companies/{company_id}/dms/files",
            cast_to=DmsFile,
            files={"file": to_httpx_file(file, filename=name)},
            data=drop_none({"name": name, "parent_folder_id": parent_folder_id}),
        )


class FirmDmsFolders(SyncAPIResource):
    """Manage folders stored in the Firm DMS (GED)."""

    def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
    ) -> SyncCursorPage[DmsFolder]:
        """List a company's DMS folders.

        Scope: ``dms_files:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/listdmsfolders

        Args:
            company_id: Identifier of the company.
            cursor: Pagination cursor from a previous page.
            limit: Results per page.
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
        """
        return self._get_page(
            f"/companies/{company_id}/dms/folders",
            item_type=DmsFolder,
            params={"cursor": cursor, "limit": limit, "filter": filter},
        )

    def create(
        self,
        company_id: int,
        *,
        name: str,
        parent_folder_id: int | None = None,
    ) -> DmsFolder:
        """Create a DMS folder.

        Scope: ``dms_files:all``.
        Reference: https://firm-pennylane.readme.io/reference/postdmsfolders

        Args:
            company_id: Identifier of the company.
            name: Name of the folder.
            parent_folder_id: Parent folder. Defaults to root level.
        """
        body = drop_none({"name": name, "parent_folder_id": parent_folder_id})
        return self._post(
            f"/companies/{company_id}/dms/folders", cast_to=DmsFolder, body=body
        )


class FirmDms(SyncAPIResource):
    """Namespace for the Firm DMS (GED): files and folders."""

    def __init__(self, client: SyncAPIClient) -> None:
        super().__init__(client)
        self.files = FirmDmsFiles(client)
        self.folders = FirmDmsFolders(client)


class FirmFileAttachments(SyncAPIResource):
    """Upload files to attach to other resources."""

    def create(
        self, company_id: int, file: FileInput, *, filename: str | None = None
    ) -> FileAttachment:
        """Upload a file to attach to any resource that provides a ``file_attachment_id``.

        This does not upload the file into the DMS (GED).

        Scope: ``file_attachments:all``.
        Reference: https://firm-pennylane.readme.io/reference/postfileattachments

        Args:
            company_id: Identifier of the company.
            file: A path, raw bytes, a binary file-like object, or a
                ``(filename, content)`` tuple.
            filename: Name of the file. Defaults to the uploaded file's own name.
        """
        return self._post(
            f"/companies/{company_id}/file_attachments",
            cast_to=FileAttachment,
            files={"file": to_httpx_file(file, filename=filename)},
            data=drop_none({"filename": filename}),
        )


class AsyncFirmDmsFiles(AsyncAPIResource):
    """Manage files stored in the Firm DMS (GED) (async)."""

    async def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
    ) -> AsyncCursorPage[DmsFile]:
        """List a company's DMS files.

        Scope: ``dms_files:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/company-dms-files
        """
        return await self._get_page(
            f"/companies/{company_id}/dms/files",
            item_type=DmsFile,
            params={"cursor": cursor, "limit": limit, "filter": filter},
        )

    async def create(
        self,
        company_id: int,
        file: FileInput,
        *,
        name: str | None = None,
        parent_folder_id: int | None = None,
    ) -> DmsFile:
        """Upload a file to the DMS.

        Scope: ``dms_files:all``.
        Reference: https://firm-pennylane.readme.io/reference/postdmsfiles
        """
        return await self._post(
            f"/companies/{company_id}/dms/files",
            cast_to=DmsFile,
            files={"file": to_httpx_file(file, filename=name)},
            data=drop_none({"name": name, "parent_folder_id": parent_folder_id}),
        )


class AsyncFirmDmsFolders(AsyncAPIResource):
    """Manage folders stored in the Firm DMS (GED) (async)."""

    async def list(
        self,
        company_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
    ) -> AsyncCursorPage[DmsFolder]:
        """List a company's DMS folders.

        Scope: ``dms_files:readonly``.
        Reference: https://firm-pennylane.readme.io/reference/listdmsfolders
        """
        return await self._get_page(
            f"/companies/{company_id}/dms/folders",
            item_type=DmsFolder,
            params={"cursor": cursor, "limit": limit, "filter": filter},
        )

    async def create(
        self,
        company_id: int,
        *,
        name: str,
        parent_folder_id: int | None = None,
    ) -> DmsFolder:
        """Create a DMS folder.

        Scope: ``dms_files:all``.
        Reference: https://firm-pennylane.readme.io/reference/postdmsfolders
        """
        body = drop_none({"name": name, "parent_folder_id": parent_folder_id})
        return await self._post(
            f"/companies/{company_id}/dms/folders", cast_to=DmsFolder, body=body
        )


class AsyncFirmDms(AsyncAPIResource):
    """Namespace for the Firm DMS (GED): files and folders (async)."""

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.files = AsyncFirmDmsFiles(client)
        self.folders = AsyncFirmDmsFolders(client)


class AsyncFirmFileAttachments(AsyncAPIResource):
    """Upload files to attach to other resources (async)."""

    async def create(
        self, company_id: int, file: FileInput, *, filename: str | None = None
    ) -> FileAttachment:
        """Upload a file to attach to any resource that provides a ``file_attachment_id``.

        This does not upload the file into the DMS (GED).

        Scope: ``file_attachments:all``.
        Reference: https://firm-pennylane.readme.io/reference/postfileattachments
        """
        return await self._post(
            f"/companies/{company_id}/file_attachments",
            cast_to=FileAttachment,
            files={"file": to_httpx_file(file, filename=filename)},
            data=drop_none({"filename": filename}),
        )
