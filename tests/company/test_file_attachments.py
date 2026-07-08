from __future__ import annotations

from pathlib import Path

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.file_attachments import (
    AsyncFileAttachments,
    FileAttachments,
)

from ..conftest import BASE_URL

FILE_ATTACHMENT = {
    "id": 42,
    "url": "http://www.pennylane.com/rails/active_storage/blobs/redirect/xyz/Invoice42.pdf",
    "filename": "Invoice42.pdf",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-05T09:00:00Z",
}


class TestFileAttachments:
    @respx.mock
    def test_create_from_bytes(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/file_attachments").mock(
            return_value=httpx.Response(201, json=FILE_ATTACHMENT)
        )
        attachment = FileAttachments(sync_client).create(
            b"%PDF-1.4 fake content", filename="Invoice42.pdf"
        )
        assert attachment.id == 42
        assert attachment.filename == "Invoice42.pdf"

        request = route.calls.last.request
        assert b'name="file"' in request.content
        assert b"Invoice42.pdf" in request.content
        assert b'name="filename"' in request.content

    @respx.mock
    def test_create_from_path(self, sync_client: SyncAPIClient, tmp_path: Path) -> None:
        file_path = tmp_path / "report.pdf"
        file_path.write_bytes(b"%PDF-1.4 report")

        respx.post(f"{BASE_URL}/file_attachments").mock(
            return_value=httpx.Response(201, json=FILE_ATTACHMENT)
        )
        attachment = FileAttachments(sync_client).create(file_path)
        assert attachment.id == 42


class TestAsyncFileAttachments:
    @respx.mock
    async def test_create(self, async_client: AsyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/file_attachments").mock(
            return_value=httpx.Response(201, json=FILE_ATTACHMENT)
        )
        attachment = await AsyncFileAttachments(async_client).create(
            b"%PDF-1.4 fake content", filename="Invoice42.pdf"
        )
        assert attachment.id == 42
        request = route.calls.last.request
        assert b'name="file"; filename="Invoice42.pdf"' in request.content
