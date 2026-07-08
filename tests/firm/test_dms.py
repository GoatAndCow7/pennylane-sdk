from __future__ import annotations

import json

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.firm.dms import (
    AsyncFirmDms,
    AsyncFirmFileAttachments,
    FirmDms,
    FirmFileAttachments,
)

FIRM_BASE_URL = "https://app.pennylane.com/api/external/firm/v1"

DMS_FILE = {
    "id": 1,
    "name": "invoice.pdf",
    "path": "/invoice.pdf",
    "parent_folder": None,
    "url": "https://files.pennylane.com/dms/1.pdf",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-05T09:00:00Z",
}
DMS_FOLDER = {
    "id": 2,
    "name": "Invoices",
    "path": "/Invoices",
    "parent_folder": None,
    "files": {"url": "https://app.pennylane.com/api/external/firm/v1/companies/10/dms/files"},
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-05T09:00:00Z",
}
FILE_ATTACHMENT = {
    "id": 3,
    "url": "https://files.pennylane.com/attachments/3.pdf",
    "filename": "Invoice3.pdf",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-05T09:00:00Z",
}


def sync_client() -> SyncAPIClient:
    return SyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)


def async_client() -> AsyncAPIClient:
    return AsyncAPIClient(api_token="test-token", base_url=FIRM_BASE_URL)


class TestFirmDmsFiles:
    @respx.mock
    def test_list(self) -> None:
        route = respx.get(f"{FIRM_BASE_URL}/companies/10/dms/files").mock(
            return_value=httpx.Response(
                200, json={"items": [DMS_FILE], "has_more": False, "next_cursor": None}
            )
        )
        page = FirmDms(sync_client()).files.list(10, limit=20)
        assert route.calls.last.request.url.params["limit"] == "20"
        assert page.items[0].id == 1
        assert page.items[0].url == "https://files.pennylane.com/dms/1.pdf"

    @respx.mock
    def test_create(self) -> None:
        route = respx.post(f"{FIRM_BASE_URL}/companies/10/dms/files").mock(
            return_value=httpx.Response(201, json=DMS_FILE)
        )
        dms_file = FirmDms(sync_client()).files.create(
            10, b"%PDF-1.4 fake content", name="invoice.pdf", parent_folder_id=5
        )
        assert dms_file.id == 1
        request = route.calls.last.request
        assert b'name="file"' in request.content
        assert b'name="parent_folder_id"' in request.content


class TestFirmDmsFolders:
    @respx.mock
    def test_list(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/10/dms/folders").mock(
            return_value=httpx.Response(
                200, json={"items": [DMS_FOLDER], "has_more": False, "next_cursor": None}
            )
        )
        page = FirmDms(sync_client()).folders.list(10)
        assert page.items[0].id == 2
        assert page.items[0].files is not None

    @respx.mock
    def test_create(self) -> None:
        route = respx.post(f"{FIRM_BASE_URL}/companies/10/dms/folders").mock(
            return_value=httpx.Response(201, json=DMS_FOLDER)
        )
        folder = FirmDms(sync_client()).folders.create(10, name="Invoices")
        assert json.loads(route.calls.last.request.content) == {"name": "Invoices"}
        assert folder.id == 2


class TestFirmFileAttachments:
    @respx.mock
    def test_create(self) -> None:
        route = respx.post(f"{FIRM_BASE_URL}/companies/10/file_attachments").mock(
            return_value=httpx.Response(201, json=FILE_ATTACHMENT)
        )
        attachment = FirmFileAttachments(sync_client()).create(
            10, b"%PDF-1.4 fake content", filename="Invoice3.pdf"
        )
        assert attachment.id == 3
        request = route.calls.last.request
        assert b'name="file"' in request.content
        assert b"Invoice3.pdf" in request.content


class TestAsyncFirmDms:
    @respx.mock
    async def test_files_list(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/10/dms/files").mock(
            return_value=httpx.Response(
                200, json={"items": [DMS_FILE], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncFirmDms(async_client()).files.list(10)
        assert page.items[0].id == 1

    @respx.mock
    async def test_files_create(self) -> None:
        respx.post(f"{FIRM_BASE_URL}/companies/10/dms/files").mock(
            return_value=httpx.Response(201, json=DMS_FILE)
        )
        dms_file = await AsyncFirmDms(async_client()).files.create(
            10, b"%PDF-1.4 fake content", name="invoice.pdf"
        )
        assert dms_file.id == 1

    @respx.mock
    async def test_folders_list(self) -> None:
        respx.get(f"{FIRM_BASE_URL}/companies/10/dms/folders").mock(
            return_value=httpx.Response(
                200, json={"items": [DMS_FOLDER], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncFirmDms(async_client()).folders.list(10)
        assert page.items[0].id == 2

    @respx.mock
    async def test_folders_create(self) -> None:
        respx.post(f"{FIRM_BASE_URL}/companies/10/dms/folders").mock(
            return_value=httpx.Response(201, json=DMS_FOLDER)
        )
        folder = await AsyncFirmDms(async_client()).folders.create(10, name="Invoices")
        assert folder.id == 2


class TestAsyncFirmFileAttachments:
    @respx.mock
    async def test_create(self) -> None:
        respx.post(f"{FIRM_BASE_URL}/companies/10/file_attachments").mock(
            return_value=httpx.Response(201, json=FILE_ATTACHMENT)
        )
        attachment = await AsyncFirmFileAttachments(async_client()).create(
            10, b"%PDF-1.4 fake content", filename="Invoice3.pdf"
        )
        assert attachment.id == 3
