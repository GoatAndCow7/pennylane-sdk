"""Unofficial Python SDK for the Pennylane API.

Pennylane (https://www.pennylane.com) is a French accounting and invoicing
platform. This SDK covers both its public APIs:

- the **Company API v2** via :class:`Pennylane` / :class:`AsyncPennylane`
- the **Firm API v1** (accounting firms) via :class:`PennylaneFirm` /
  :class:`AsyncPennylaneFirm`

This project is not affiliated with Pennylane SAS, and is unrelated to the
PennyLane quantum computing framework.
"""

from . import filters, oauth, webhooks
from ._base_client import RateLimitInfo
from ._client import AsyncPennylane, AsyncPennylaneFirm, Pennylane, PennylaneFirm
from ._exceptions import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    NotFoundError,
    PennylaneError,
    PermissionDeniedError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from ._models import Money, PennylaneModel
from ._pagination import (
    AsyncCursorPage,
    AsyncNumberedPage,
    SyncCursorPage,
    SyncNumberedPage,
)
from ._version import __version__

__all__ = [
    "APIConnectionError",
    "APIStatusError",
    "APITimeoutError",
    "AsyncCursorPage",
    "AsyncNumberedPage",
    "AsyncPennylane",
    "AsyncPennylaneFirm",
    "AuthenticationError",
    "BadRequestError",
    "ConflictError",
    "Money",
    "NotFoundError",
    "Pennylane",
    "PennylaneError",
    "PennylaneFirm",
    "PennylaneModel",
    "PermissionDeniedError",
    "RateLimitError",
    "RateLimitInfo",
    "ServerError",
    "SyncCursorPage",
    "SyncNumberedPage",
    "ValidationError",
    "__version__",
    "filters",
    "oauth",
    "webhooks",
]
