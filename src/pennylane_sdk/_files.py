"""Helpers to normalize file inputs for multipart upload endpoints.

Endpoints like ``POST /file_attachments`` or invoice imports accept a file as
multipart form data. The SDK lets callers pass a filesystem path, raw bytes or
a file-like object; :func:`to_httpx_file` normalizes any of these into the
``(filename, content, content_type)`` tuple httpx expects.
"""

from __future__ import annotations

import mimetypes
import os
from pathlib import Path
from typing import IO, Any, Union

__all__ = ["FileInput", "to_httpx_file"]

# A file argument accepted by SDK upload methods.
FileInput = Union[str, "os.PathLike[str]", bytes, IO[bytes], tuple[str, bytes | IO[bytes]]]

_DEFAULT_CONTENT_TYPE = "application/octet-stream"


def _guess_content_type(filename: str | None) -> str:
    if not filename:
        return _DEFAULT_CONTENT_TYPE
    guessed, _ = mimetypes.guess_type(filename)
    return guessed or _DEFAULT_CONTENT_TYPE


def to_httpx_file(
    file: FileInput,
    *,
    filename: str | None = None,
) -> tuple[str, Any, str]:
    """Normalize a user-provided file into an httpx multipart tuple.

    Args:
        file: A path (``str`` / ``Path``), raw ``bytes``, a binary file-like
            object, or a ``(filename, content)`` tuple.
        filename: Overrides the filename sent to the API. Required when
            ``file`` is raw bytes or a file-like object without a ``name``.

    Returns:
        A ``(filename, content, content_type)`` tuple for ``httpx`` ``files=``.
    """
    if isinstance(file, tuple):
        tuple_name, content = file
        final_name = filename or tuple_name
        return (final_name, content, _guess_content_type(final_name))

    if isinstance(file, (str, os.PathLike)):
        path = Path(file)
        final_name = filename or path.name
        return (final_name, path.read_bytes(), _guess_content_type(final_name))

    if isinstance(file, bytes):
        if not filename:
            raise ValueError("filename is required when passing raw bytes")
        return (filename, file, _guess_content_type(filename))

    # File-like object.
    inferred = getattr(file, "name", None)
    resolved_name: str | None = filename or (
        Path(inferred).name if isinstance(inferred, str) else None
    )
    if not resolved_name:
        raise ValueError("filename is required when the file object has no usable name")
    return (resolved_name, file, _guess_content_type(resolved_name))
