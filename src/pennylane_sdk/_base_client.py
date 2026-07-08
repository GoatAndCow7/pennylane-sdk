"""HTTP engine shared by the four Pennylane clients.

Responsibilities: authentication headers, query-parameter preparation
(including filter encoding), JSON body serialization (Decimal/date aware),
client-side throttling, automatic retries and defensive error parsing.

Retry policy: designed for an accounting API with NO server-side idempotency
(re-sending a create can produce a duplicate invoice or ledger entry):

- 429 (rate limit): safe to retry for every method: the request was rejected
  before being processed. Honors the ``retry-after`` header.
- 500/502/503/504: retried only for idempotent methods (GET/PUT/DELETE).
  POST is NOT retried on 5xx because the server may have processed it.
- Connect errors/timeouts (request never sent): retried for every method.
- Read errors/timeouts (request possibly processed): retried only for
  idempotent methods.
"""

from __future__ import annotations

import math
import random
import time
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, TypeVar, overload
from urllib.parse import urlsplit

import anyio
import httpx

from . import filters as _filters
from ._exceptions import (
    APIConnectionError,
    APITimeoutError,
    InvalidResponseError,
    make_status_error,
)
from ._models import PennylaneModel, jsonable
from ._pagination import (
    AsyncCursorPage,
    AsyncNumberedPage,
    SyncCursorPage,
    SyncNumberedPage,
)
from ._throttle import AsyncRateThrottle, RateThrottle
from ._version import __version__

__all__ = ["AsyncAPIClient", "RateLimitInfo", "SyncAPIClient"]

T = TypeVar("T", bound=PennylaneModel)

DEFAULT_TIMEOUT = httpx.Timeout(60.0, connect=10.0)
DEFAULT_MAX_RETRIES = 3

_RETRYABLE_STATUS = frozenset({429, 500, 502, 503, 504})
_IDEMPOTENT_METHODS = frozenset({"GET", "PUT", "DELETE", "HEAD"})
_MAX_BACKOFF = 8.0
_INITIAL_BACKOFF = 0.5
# Upper bound applied to server-provided retry-after values, so a
# misconfigured proxy cannot park a worker for hours.
_MAX_RETRY_AFTER = 60.0
_LOCAL_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})


def _validate_base_url(base_url: str) -> str:
    """Require https, tolerating plain http only for local development."""
    parts = urlsplit(base_url)
    if parts.scheme == "https":
        return base_url
    if parts.scheme == "http" and parts.hostname in _LOCAL_HOSTS:
        return base_url
    raise ValueError(
        f"base_url must use https (got {base_url!r}). Plain http is allowed "
        "only for localhost, to avoid sending your API token in cleartext."
    )


@dataclass(frozen=True)
class RateLimitInfo:
    """Rate-limit state reported by the API on every response.

    Attributes:
        limit: Request budget of the current window (``ratelimit-limit``).
        remaining: Requests left in the window (``ratelimit-remaining``).
        reset: Unix timestamp at which the window resets (``ratelimit-reset``).
    """

    limit: int | None
    remaining: int | None
    reset: int | None

    @classmethod
    def from_response(cls, response: httpx.Response) -> RateLimitInfo | None:
        def _int(name: str) -> int | None:
            raw = response.headers.get(name)
            if raw is None:
                return None
            try:
                return int(raw)
            except ValueError:
                return None

        limit = _int("ratelimit-limit")
        remaining = _int("ratelimit-remaining")
        reset = _int("ratelimit-reset")
        if limit is None and remaining is None and reset is None:
            return None
        return cls(limit=limit, remaining=remaining, reset=reset)


class BaseAPIClient:
    """Request preparation and retry policy shared by sync/async clients."""

    def __init__(
        self,
        *,
        api_token: str,
        base_url: str,
        timeout: float | httpx.Timeout | None = None,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        if not api_token or not api_token.strip():
            raise ValueError("api_token must be a non-empty string")
        self._api_token = api_token
        self.base_url = _validate_base_url(base_url.rstrip("/"))
        self.timeout = DEFAULT_TIMEOUT if timeout is None else timeout
        if max_retries < 0:
            raise ValueError("max_retries must be >= 0")
        self.max_retries = max_retries
        #: Rate-limit state from the most recent API response, if any.
        self.last_rate_limit: RateLimitInfo | None = None

    # -- request preparation -------------------------------------------------

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_token}",
            "Accept": "application/json",
            "User-Agent": f"pennylane-sdk-python/{__version__}",
        }

    @staticmethod
    def prepare_params(params: Mapping[str, Any] | None) -> dict[str, Any]:
        """Drop ``None`` values and encode the ``filter`` parameter."""
        if not params:
            return {}
        prepared: dict[str, Any] = {}
        for key, value in params.items():
            if value is None:
                continue
            if key == "filter":
                prepared[key] = _filters.encode_filters(value)
            else:
                prepared[key] = value
        return prepared

    # -- retry policy ---------------------------------------------------------

    def _should_retry_status(self, method: str, status_code: int) -> bool:
        if status_code not in _RETRYABLE_STATUS:
            return False
        if status_code == 429:
            return True
        return method.upper() in _IDEMPOTENT_METHODS

    def _retry_delay(self, attempt: int, response: httpx.Response | None) -> float:
        if response is not None and response.status_code == 429:
            retry_after: str | None = response.headers.get("retry-after")
            if retry_after is not None:
                try:
                    value = float(retry_after)
                except ValueError:
                    value = math.nan
                if math.isfinite(value):
                    return min(max(0.0, value), _MAX_RETRY_AFTER)
        delay = min(_INITIAL_BACKOFF * (1 << attempt), _MAX_BACKOFF)
        return delay + random.uniform(0, delay / 4)

    def _can_retry_transport(self, method: str, attempt: int, request_sent: bool) -> bool:
        if attempt >= self.max_retries:
            return False
        if not request_sent:
            return True
        return method in _IDEMPOTENT_METHODS

    def _track_response(self, response: httpx.Response) -> None:
        info = RateLimitInfo.from_response(response)
        if info is not None:
            self.last_rate_limit = info

    @staticmethod
    def _parse_json(response: httpx.Response) -> Any:
        if response.status_code == 204 or not response.content:
            return None
        try:
            return response.json()
        except Exception as exc:
            content_type = response.headers.get("content-type", "unknown")
            excerpt = response.text[:200]
            raise InvalidResponseError(
                f"Expected a JSON body but got content-type {content_type!r} "
                f"(HTTP {response.status_code}): {excerpt!r}",
                response=response,
            ) from exc


class SyncAPIClient(BaseAPIClient):
    """Synchronous HTTP engine (used by ``Pennylane`` and ``PennylaneFirm``)."""

    def __init__(
        self,
        *,
        api_token: str,
        base_url: str,
        timeout: float | httpx.Timeout | None = None,
        max_retries: int = DEFAULT_MAX_RETRIES,
        throttle: RateThrottle | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        super().__init__(
            api_token=api_token, base_url=base_url, timeout=timeout, max_retries=max_retries
        )
        self._throttle = throttle
        self._http = http_client or httpx.Client(timeout=self.timeout)
        self._owns_http = http_client is None

    # -- lifecycle ------------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        if self._owns_http:
            self._http.close()

    def __enter__(self) -> SyncAPIClient:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    # -- public request API ---------------------------------------------------

    @overload
    def request(
        self,
        method: str,
        path: str,
        *,
        cast_to: type[T],
        params: Mapping[str, Any] | None = None,
        body: Any = None,
        files: Any = None,
        data: Mapping[str, Any] | None = None,
    ) -> T: ...

    @overload
    def request(
        self,
        method: str,
        path: str,
        *,
        cast_to: None = None,
        params: Mapping[str, Any] | None = None,
        body: Any = None,
        files: Any = None,
        data: Mapping[str, Any] | None = None,
    ) -> None: ...

    def request(
        self,
        method: str,
        path: str,
        *,
        cast_to: type[T] | None = None,
        params: Mapping[str, Any] | None = None,
        body: Any = None,
        files: Any = None,
        data: Mapping[str, Any] | None = None,
    ) -> T | None:
        """Send a request and parse the response into ``cast_to``.

        Args:
            method: HTTP method (``"GET"``, ``"POST"``...).
            path: Endpoint path relative to the API base URL (``"/products"``).
            cast_to: Model to validate the JSON response into, or ``None``
                when no response body is expected (204).
            params: Query parameters; ``None`` values are dropped and the
                ``filter`` value may be a list of :class:`~pennylane_sdk.filters.Filter`.
            body: JSON body (dicts/models/Decimals/dates are auto-encoded).
            files: Multipart file payload (httpx format).
            data: Multipart form fields, used together with ``files``.
        """
        payload = self._request_json(method, path, params=params, body=body, files=files, data=data)
        if cast_to is None or payload is None:
            return None
        return cast_to.model_validate(payload)

    def request_page(
        self,
        path: str,
        *,
        item_type: type[T],
        params: Mapping[str, Any] | None = None,
    ) -> SyncCursorPage[T]:
        """GET a list endpoint and wrap the response in an auto-paginating page."""
        prepared = self.prepare_params(params)
        payload = self._request_json("GET", path, params=prepared, _params_prepared=True)
        page_params = {key: value for key, value in prepared.items() if key != "cursor"}
        data = payload if isinstance(payload, dict) else {}
        return SyncCursorPage(
            client=self, item_type=item_type, path=path, params=page_params, data=data
        )

    def request_numbered_page(
        self,
        path: str,
        *,
        item_type: type[T],
        params: Mapping[str, Any] | None = None,
    ) -> SyncNumberedPage[T]:
        """GET a page-number paginated endpoint (Firm API: page/per_page)."""
        prepared = self.prepare_params(params)
        payload = self._request_json("GET", path, params=prepared, _params_prepared=True)
        page_params = {key: value for key, value in prepared.items() if key != "page"}
        data = payload if isinstance(payload, dict) else {}
        return SyncNumberedPage(
            client=self, item_type=item_type, path=path, params=page_params, data=data
        )

    # -- engine ---------------------------------------------------------------

    def _request_json(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        body: Any = None,
        files: Any = None,
        data: Mapping[str, Any] | None = None,
        _params_prepared: bool = False,
    ) -> Any:
        method = method.upper()
        query = dict(params or {}) if _params_prepared else self.prepare_params(params)
        json_body = jsonable(body) if body is not None else None

        attempt = 0
        while True:
            if self._throttle is not None:
                self._throttle.acquire()
            try:
                response = self._http.request(
                    method,
                    self.base_url + path,
                    params=query or None,
                    json=json_body,
                    files=files,
                    data=dict(data) if data else None,
                    headers=self._headers(),
                )
            except httpx.TimeoutException as exc:
                # Connect/pool timeouts never reached the server: always retryable.
                request_sent = not isinstance(exc, (httpx.ConnectTimeout, httpx.PoolTimeout))
                if self._can_retry_transport(method, attempt, request_sent):
                    time.sleep(self._retry_delay(attempt, None))
                    attempt += 1
                    continue
                raise APITimeoutError(f"Request to {path} timed out.") from exc
            except httpx.TransportError as exc:
                request_sent = not isinstance(exc, httpx.ConnectError)
                if self._can_retry_transport(method, attempt, request_sent):
                    time.sleep(self._retry_delay(attempt, None))
                    attempt += 1
                    continue
                raise APIConnectionError(f"Connection error while requesting {path}.") from exc

            self._track_response(response)
            if 200 <= response.status_code < 300:
                return self._parse_json(response)

            if attempt < self.max_retries and self._should_retry_status(
                method, response.status_code
            ):
                time.sleep(self._retry_delay(attempt, response))
                attempt += 1
                continue

            raise make_status_error(response)


class AsyncAPIClient(BaseAPIClient):
    """Asynchronous HTTP engine (used by ``AsyncPennylane`` and ``AsyncPennylaneFirm``)."""

    def __init__(
        self,
        *,
        api_token: str,
        base_url: str,
        timeout: float | httpx.Timeout | None = None,
        max_retries: int = DEFAULT_MAX_RETRIES,
        throttle: AsyncRateThrottle | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        super().__init__(
            api_token=api_token, base_url=base_url, timeout=timeout, max_retries=max_retries
        )
        self._throttle = throttle
        self._http = http_client or httpx.AsyncClient(timeout=self.timeout)
        self._owns_http = http_client is None

    # -- lifecycle ------------------------------------------------------------

    async def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        if self._owns_http:
            await self._http.aclose()

    async def __aenter__(self) -> AsyncAPIClient:
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.close()

    # -- public request API ---------------------------------------------------

    @overload
    async def request(
        self,
        method: str,
        path: str,
        *,
        cast_to: type[T],
        params: Mapping[str, Any] | None = None,
        body: Any = None,
        files: Any = None,
        data: Mapping[str, Any] | None = None,
    ) -> T: ...

    @overload
    async def request(
        self,
        method: str,
        path: str,
        *,
        cast_to: None = None,
        params: Mapping[str, Any] | None = None,
        body: Any = None,
        files: Any = None,
        data: Mapping[str, Any] | None = None,
    ) -> None: ...

    async def request(
        self,
        method: str,
        path: str,
        *,
        cast_to: type[T] | None = None,
        params: Mapping[str, Any] | None = None,
        body: Any = None,
        files: Any = None,
        data: Mapping[str, Any] | None = None,
    ) -> T | None:
        """Async counterpart of :meth:`SyncAPIClient.request`."""
        payload = await self._request_json(
            method, path, params=params, body=body, files=files, data=data
        )
        if cast_to is None or payload is None:
            return None
        return cast_to.model_validate(payload)

    async def request_page(
        self,
        path: str,
        *,
        item_type: type[T],
        params: Mapping[str, Any] | None = None,
    ) -> AsyncCursorPage[T]:
        """GET a list endpoint and wrap the response in an auto-paginating page."""
        prepared = self.prepare_params(params)
        payload = await self._request_json("GET", path, params=prepared, _params_prepared=True)
        page_params = {key: value for key, value in prepared.items() if key != "cursor"}
        data = payload if isinstance(payload, dict) else {}
        return AsyncCursorPage(
            client=self, item_type=item_type, path=path, params=page_params, data=data
        )

    async def request_numbered_page(
        self,
        path: str,
        *,
        item_type: type[T],
        params: Mapping[str, Any] | None = None,
    ) -> AsyncNumberedPage[T]:
        """GET a page-number paginated endpoint (Firm API: page/per_page)."""
        prepared = self.prepare_params(params)
        payload = await self._request_json("GET", path, params=prepared, _params_prepared=True)
        page_params = {key: value for key, value in prepared.items() if key != "page"}
        data = payload if isinstance(payload, dict) else {}
        return AsyncNumberedPage(
            client=self, item_type=item_type, path=path, params=page_params, data=data
        )

    # -- engine ---------------------------------------------------------------

    async def _request_json(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        body: Any = None,
        files: Any = None,
        data: Mapping[str, Any] | None = None,
        _params_prepared: bool = False,
    ) -> Any:
        method = method.upper()
        query = dict(params or {}) if _params_prepared else self.prepare_params(params)
        json_body = jsonable(body) if body is not None else None

        attempt = 0
        while True:
            if self._throttle is not None:
                await self._throttle.acquire()
            try:
                response = await self._http.request(
                    method,
                    self.base_url + path,
                    params=query or None,
                    json=json_body,
                    files=files,
                    data=dict(data) if data else None,
                    headers=self._headers(),
                )
            except httpx.TimeoutException as exc:
                # Connect/pool timeouts never reached the server: always retryable.
                request_sent = not isinstance(exc, (httpx.ConnectTimeout, httpx.PoolTimeout))
                if self._can_retry_transport(method, attempt, request_sent):
                    await anyio.sleep(self._retry_delay(attempt, None))
                    attempt += 1
                    continue
                raise APITimeoutError(f"Request to {path} timed out.") from exc
            except httpx.TransportError as exc:
                request_sent = not isinstance(exc, httpx.ConnectError)
                if self._can_retry_transport(method, attempt, request_sent):
                    await anyio.sleep(self._retry_delay(attempt, None))
                    attempt += 1
                    continue
                raise APIConnectionError(f"Connection error while requesting {path}.") from exc

            self._track_response(response)
            if 200 <= response.status_code < 300:
                return self._parse_json(response)

            if attempt < self.max_retries and self._should_retry_status(
                method, response.status_code
            ):
                await anyio.sleep(self._retry_delay(attempt, response))
                attempt += 1
                continue

            raise make_status_error(response)
