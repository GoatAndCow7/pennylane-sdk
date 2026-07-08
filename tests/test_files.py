from __future__ import annotations

import io
from pathlib import Path

import pytest

from pennylane_sdk._files import to_httpx_file


class TestToHttpxFile:
    def test_path_input(self, tmp_path: Path) -> None:
        pdf = tmp_path / "invoice.pdf"
        pdf.write_bytes(b"%PDF-1.4")
        name, content, content_type = to_httpx_file(pdf)
        assert name == "invoice.pdf"
        assert content == b"%PDF-1.4"
        assert content_type == "application/pdf"

    def test_string_path_input(self, tmp_path: Path) -> None:
        file = tmp_path / "data.xml"
        file.write_bytes(b"<xml/>")
        name, _content, content_type = to_httpx_file(str(file))
        assert name == "data.xml"
        assert "xml" in content_type

    def test_bytes_require_filename(self) -> None:
        with pytest.raises(ValueError, match="filename is required"):
            to_httpx_file(b"raw")

    def test_bytes_with_filename(self) -> None:
        name, _content, content_type = to_httpx_file(b"%PDF-1.4", filename="facture.pdf")
        assert name == "facture.pdf"
        assert content_type == "application/pdf"

    def test_file_object_uses_its_name(self, tmp_path: Path) -> None:
        file = tmp_path / "doc.pdf"
        file.write_bytes(b"%PDF-1.4")
        with file.open("rb") as handle:
            name, _content, _content_type = to_httpx_file(handle)
            assert name == "doc.pdf"

    def test_anonymous_file_object_requires_filename(self) -> None:
        buffer = io.BytesIO(b"data")
        with pytest.raises(ValueError, match="filename is required"):
            to_httpx_file(buffer)
        name, _, _ = to_httpx_file(buffer, filename="x.bin")
        assert name == "x.bin"

    def test_tuple_input(self) -> None:
        name, content, content_type = to_httpx_file(("report.pdf", b"%PDF"))
        assert name == "report.pdf"
        assert content == b"%PDF"
        assert content_type == "application/pdf"

    def test_filename_override_wins(self, tmp_path: Path) -> None:
        file = tmp_path / "internal-name.pdf"
        file.write_bytes(b"%PDF")
        name, _, _ = to_httpx_file(file, filename="customer-facing.pdf")
        assert name == "customer-facing.pdf"
