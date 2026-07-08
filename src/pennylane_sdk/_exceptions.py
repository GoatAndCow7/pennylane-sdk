"""Exception hierarchy for the Pennylane SDK.

Every error raised by the SDK derives from :class:`PennylaneError`:

- :class:`APIConnectionError` / :class:`APITimeoutError`: the request never
  produced an HTTP response (network failure, DNS, timeout).
- :class:`APIStatusError`: the API answered with a 4xx/5xx status. One
  subclass exists per documented status code (:class:`AuthenticationError`,
  :class:`RateLimitError`, ...).

The Pennylane API error body is inconsistent across endpoints (the guide
documents ``{"error", "message", "details"}`` while the OpenAPI spec declares
``{"error", "status"}``), so parsing is defensive: every field is optional.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import httpx

__all__ = [
    "APIConnectionError",
    "APIStatusError",
    "APITimeoutError",
    "AuthenticationError",
    "BadRequestError",
    "ConflictError",
    "NotFoundError",
    "PennylaneError",
    "PermissionDeniedError",
    "RateLimitError",
    "ServerError",
    "ValidationError",
]


class PennylaneError(Exception):
    """Base class for every error raised by the Pennylane SDK."""


class APIConnectionError(PennylaneError):
    """The request could not be completed (network issue, DNS failure...)."""

    def __init__(self, message: str = "Connection error.") -> None:
        super().__init__(message)


class APITimeoutError(APIConnectionError):
    """The request timed out before the API answered."""

    def __init__(self, message: str = "Request timed out.") -> None:
        super().__init__(message)


class APIStatusError(PennylaneError):
    """The API answered with an error status code (4xx / 5xx).

    Attributes:
        status_code: HTTP status code of the response.
        error_code: Machine-readable code from the body ``error`` field when
            present (e.g. ``"unprocessable_entity"``). Some endpoints put a
            human message in ``error`` instead; both are preserved verbatim.
        message: Best-effort human-readable message (``message`` field,
            falling back to ``error``, falling back to the raw body).
        details: Optional structured details from the body ``details`` field
            (e.g. per-field validation errors).
        body: The parsed JSON body, or ``None`` if the body was not JSON.
        response: The raw :class:`httpx.Response`.
    """

    def __init__(
        self,
        message: str,
        *,
        response: httpx.Response,
        error_code: str | None = None,
        details: Any = None,
        body: Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.response = response
        self.status_code: int = response.status_code
        self.error_code = error_code
        self.details = details
        self.body = body


class BadRequestError(APIStatusError):
    """400: malformed JSON, wrong types or unsupported fields."""


class AuthenticationError(APIStatusError):
    """401: missing, invalid or expired API token."""


class PermissionDeniedError(APIStatusError):
    """403: the token lacks the required scope for this endpoint."""


class NotFoundError(APIStatusError):
    """404: the resource does not exist or is not accessible."""


class ConflictError(APIStatusError):
    """409: conflict, e.g. a duplicate of an existing document."""


class ValidationError(APIStatusError):
    """422: the request is well-formed but fails business validation."""


class RateLimitError(APIStatusError):
    """429: rate limit exceeded (Company: 25 req/5s, Firm: 5 req/s).

    Attributes:
        retry_after: Seconds to wait before retrying, from the
            ``retry-after`` response header when present.
    """

    def __init__(
        self,
        message: str,
        *,
        response: httpx.Response,
        error_code: str | None = None,
        details: Any = None,
        body: Any = None,
    ) -> None:
        super().__init__(
            message, response=response, error_code=error_code, details=details, body=body
        )
        self.retry_after: float | None = _parse_retry_after(response)


class ServerError(APIStatusError):
    """5xx: transient Pennylane server error (500, 503...)."""


_STATUS_TO_ERROR: dict[int, type[APIStatusError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    409: ConflictError,
    422: ValidationError,
    429: RateLimitError,
}


def _parse_retry_after(response: httpx.Response) -> float | None:
    raw = response.headers.get("retry-after")
    if raw is None:
        return None
    try:
        return max(0.0, float(raw))
    except ValueError:
        return None


def make_status_error(response: httpx.Response) -> APIStatusError:
    """Build the appropriate :class:`APIStatusError` subclass for a response.

    Parses the error body defensively: the API sometimes returns
    ``{"error", "message", "details"}``, sometimes ``{"error", "status"}``,
    and sometimes a non-JSON body entirely.
    """
    body: Any = None
    error_code: str | None = None
    message: str | None = None
    details: Any = None

    try:
        body = response.json()
    except Exception:
        body = None

    if isinstance(body, dict):
        raw_error = body.get("error")
        if isinstance(raw_error, str):
            error_code = raw_error
        raw_message = body.get("message")
        if isinstance(raw_message, str):
            message = raw_message
        details = body.get("details")

    if message is None:
        message = error_code
    if message is None:
        text = response.text.strip()
        message = text[:500] if text else f"HTTP {response.status_code}"

    if response.status_code >= 500:
        cls: type[APIStatusError] = ServerError
    else:
        cls = _STATUS_TO_ERROR.get(response.status_code, APIStatusError)
    return cls(message, response=response, error_code=error_code, details=details, body=body)
