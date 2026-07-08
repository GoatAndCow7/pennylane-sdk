"""The four public Pennylane clients.

- :class:`Pennylane` / :class:`AsyncPennylane` — Company API v2, for a single
  company managing its own accounting and invoicing.
- :class:`PennylaneFirm` / :class:`AsyncPennylaneFirm` — Firm API v1, for
  accounting firms operating on their client portfolio.
"""

from __future__ import annotations

import os

import httpx

from ._base_client import (
    DEFAULT_MAX_RETRIES,
    AsyncAPIClient,
    RateLimitInfo,
    SyncAPIClient,
)
from ._exceptions import PennylaneError
from ._throttle import AsyncRateThrottle, RateThrottle

__all__ = ["AsyncPennylane", "AsyncPennylaneFirm", "Pennylane", "PennylaneFirm"]

DEFAULT_COMPANY_BASE_URL = "https://app.pennylane.com/api/external/v2"
DEFAULT_FIRM_BASE_URL = "https://app.pennylane.com/api/external/firm/v1"

# Official API rate limits (requests, window seconds), applied per token.
COMPANY_RATE_LIMIT = (25, 5.0)
FIRM_RATE_LIMIT = (5, 1.0)

_COMPANY_TOKEN_ENV = "PENNYLANE_API_TOKEN"
_FIRM_TOKEN_ENV = "PENNYLANE_FIRM_API_TOKEN"


def _resolve_token(explicit: str | None, env_var: str, client_name: str) -> str:
    token = explicit if explicit is not None else os.environ.get(env_var)
    if not token:
        raise PennylaneError(
            f"The api_token client option must be set: pass api_token to {client_name}() "
            f"or set the {env_var} environment variable. Generate a token in Pennylane "
            "under Settings > Connectivity > Developers."
        )
    return token


class Pennylane:
    """Synchronous client for the Pennylane Company API (v2).

    Args:
        api_token: Company API token. Falls back to the ``PENNYLANE_API_TOKEN``
            environment variable.
        base_url: Override the API base URL (e.g. for a proxy).
        timeout: Request timeout in seconds or an ``httpx.Timeout`` (default 60s).
        max_retries: Automatic retry budget (default 3). See the retry policy
            in :mod:`pennylane_sdk._base_client`.
        auto_throttle: When ``True`` (default), outgoing requests are paced
            client-side to the official limit of 25 requests / 5 seconds so
            bulk operations never hit HTTP 429.
        http_client: Custom ``httpx.Client`` (advanced: proxies, transports...).

    Usage::

        from pennylane_sdk import Pennylane

        client = Pennylane()
        for invoice in client.customer_invoices.list():
            print(invoice.invoice_number)
    """

    def __init__(
        self,
        api_token: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float | httpx.Timeout | None = None,
        max_retries: int = DEFAULT_MAX_RETRIES,
        auto_throttle: bool = True,
        http_client: httpx.Client | None = None,
    ) -> None:
        token = _resolve_token(api_token, _COMPANY_TOKEN_ENV, "Pennylane")
        throttle = RateThrottle(*COMPANY_RATE_LIMIT) if auto_throttle else None
        self._client = SyncAPIClient(
            api_token=token,
            base_url=base_url or DEFAULT_COMPANY_BASE_URL,
            timeout=timeout,
            max_retries=max_retries,
            throttle=throttle,
            http_client=http_client,
        )
        self._attach_resources()

    def _attach_resources(self) -> None:
        # Resource wiring is generated once all resource modules exist
        # (see docs/design/resource-map.md).
        pass

    @property
    def last_rate_limit(self) -> RateLimitInfo | None:
        """Rate-limit state from the most recent API response."""
        return self._client.last_rate_limit

    def close(self) -> None:
        """Release the underlying HTTP connection pool."""
        self._client.close()

    def __enter__(self) -> Pennylane:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()


class AsyncPennylane:
    """Asynchronous client for the Pennylane Company API (v2).

    Same options as :class:`Pennylane`. Usage::

        from pennylane_sdk import AsyncPennylane

        async with AsyncPennylane() as client:
            async for invoice in await client.customer_invoices.list():
                print(invoice.invoice_number)
    """

    def __init__(
        self,
        api_token: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float | httpx.Timeout | None = None,
        max_retries: int = DEFAULT_MAX_RETRIES,
        auto_throttle: bool = True,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        token = _resolve_token(api_token, _COMPANY_TOKEN_ENV, "AsyncPennylane")
        throttle = AsyncRateThrottle(*COMPANY_RATE_LIMIT) if auto_throttle else None
        self._client = AsyncAPIClient(
            api_token=token,
            base_url=base_url or DEFAULT_COMPANY_BASE_URL,
            timeout=timeout,
            max_retries=max_retries,
            throttle=throttle,
            http_client=http_client,
        )
        self._attach_resources()

    def _attach_resources(self) -> None:
        pass

    @property
    def last_rate_limit(self) -> RateLimitInfo | None:
        """Rate-limit state from the most recent API response."""
        return self._client.last_rate_limit

    async def close(self) -> None:
        """Release the underlying HTTP connection pool."""
        await self._client.close()

    async def __aenter__(self) -> AsyncPennylane:
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.close()


class PennylaneFirm:
    """Synchronous client for the Pennylane Firm API (v1) — accounting firms.

    Args:
        api_token: Firm API token. Falls back to the
            ``PENNYLANE_FIRM_API_TOKEN`` environment variable.
        auto_throttle: When ``True`` (default), paces requests to the official
            Firm API limit of 5 requests / second.

    Other options are identical to :class:`Pennylane`. Usage::

        from pennylane_sdk import PennylaneFirm

        firm = PennylaneFirm()
        for company in firm.companies.list():
            print(company.name)
    """

    def __init__(
        self,
        api_token: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float | httpx.Timeout | None = None,
        max_retries: int = DEFAULT_MAX_RETRIES,
        auto_throttle: bool = True,
        http_client: httpx.Client | None = None,
    ) -> None:
        token = _resolve_token(api_token, _FIRM_TOKEN_ENV, "PennylaneFirm")
        throttle = RateThrottle(*FIRM_RATE_LIMIT) if auto_throttle else None
        self._client = SyncAPIClient(
            api_token=token,
            base_url=base_url or DEFAULT_FIRM_BASE_URL,
            timeout=timeout,
            max_retries=max_retries,
            throttle=throttle,
            http_client=http_client,
        )
        self._attach_resources()

    def _attach_resources(self) -> None:
        pass

    @property
    def last_rate_limit(self) -> RateLimitInfo | None:
        """Rate-limit state from the most recent API response."""
        return self._client.last_rate_limit

    def close(self) -> None:
        """Release the underlying HTTP connection pool."""
        self._client.close()

    def __enter__(self) -> PennylaneFirm:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()


class AsyncPennylaneFirm:
    """Asynchronous client for the Pennylane Firm API (v1) — accounting firms.

    Same options as :class:`PennylaneFirm`.
    """

    def __init__(
        self,
        api_token: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float | httpx.Timeout | None = None,
        max_retries: int = DEFAULT_MAX_RETRIES,
        auto_throttle: bool = True,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        token = _resolve_token(api_token, _FIRM_TOKEN_ENV, "AsyncPennylaneFirm")
        throttle = AsyncRateThrottle(*FIRM_RATE_LIMIT) if auto_throttle else None
        self._client = AsyncAPIClient(
            api_token=token,
            base_url=base_url or DEFAULT_FIRM_BASE_URL,
            timeout=timeout,
            max_retries=max_retries,
            throttle=throttle,
            http_client=http_client,
        )
        self._attach_resources()

    def _attach_resources(self) -> None:
        pass

    @property
    def last_rate_limit(self) -> RateLimitInfo | None:
        """Rate-limit state from the most recent API response."""
        return self._client.last_rate_limit

    async def close(self) -> None:
        """Release the underlying HTTP connection pool."""
        await self._client.close()

    async def __aenter__(self) -> AsyncPennylaneFirm:
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.close()
