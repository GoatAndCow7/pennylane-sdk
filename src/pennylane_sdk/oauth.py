"""OAuth 2.0 helpers for Pennylane partner integrations.

Pennylane supports the authorization-code flow for multi-company partner
apps (https://pennylane.readme.io/docs/oauth-20-walkthrough):

1. Send the user to :meth:`OAuthApp.authorization_url`.
2. Exchange the received code with :meth:`OAuthApp.exchange_code`.
3. Use ``Pennylane(api_token=tokens.access_token)``: access tokens expire
   after 24 hours (``expires_in=86400``).
4. Refresh with :meth:`OAuthApp.refresh`.

.. warning::
   Pennylane applies **Refresh Token Rotation**: every refresh invalidates
   BOTH previous tokens. Never run two refreshes concurrently, and persist
   the new pair immediately after every refresh. These helpers serialize
   refreshes within the current process (lock), but persistence across
   processes/restarts is your responsibility.
"""

from __future__ import annotations

import asyncio
import threading
from urllib.parse import urlencode

import httpx

from ._exceptions import make_status_error
from ._models import PennylaneModel

__all__ = ["AsyncOAuthApp", "OAuthApp", "OAuthTokens"]

DEFAULT_AUTHORIZE_URL = "https://app.pennylane.com/oauth/authorize"
DEFAULT_TOKEN_URL = "https://app.pennylane.com/oauth/oauth/token"


class OAuthTokens(PennylaneModel):
    """Token pair returned by the Pennylane OAuth token endpoint."""

    access_token: str
    refresh_token: str | None = None
    token_type: str | None = None
    expires_in: int | None = None
    """Access token lifetime in seconds (Pennylane: 86400 = 24 hours)."""
    scope: str | None = None
    created_at: int | None = None


class _BaseOAuthApp:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        *,
        authorize_url: str = DEFAULT_AUTHORIZE_URL,
        token_url: str = DEFAULT_TOKEN_URL,
    ) -> None:
        self.client_id = client_id
        self._client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.authorize_url = authorize_url
        self.token_url = token_url

    def authorization_url(
        self,
        *,
        scopes: str | list[str],
        state: str | None = None,
    ) -> str:
        """Build the URL where the user grants your app access.

        Args:
            scopes: Requested scopes (e.g. ``["customer_invoices:all"]``),
                or an already space-separated string.
            state: Opaque anti-CSRF value returned to your redirect URI.
        """
        scope = " ".join(scopes) if isinstance(scopes, list) else scopes
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": scope,
        }
        if state is not None:
            params["state"] = state
        return f"{self.authorize_url}?{urlencode(params)}"

    def _exchange_payload(self, code: str) -> dict[str, str]:
        return {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self._client_secret,
        }

    def _refresh_payload(self, refresh_token: str) -> dict[str, str]:
        return {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
            "client_secret": self._client_secret,
        }

    @staticmethod
    def _parse_tokens(response: httpx.Response) -> OAuthTokens:
        if response.status_code >= 400:
            raise make_status_error(response)
        return OAuthTokens.model_validate(response.json())


class OAuthApp(_BaseOAuthApp):
    """Synchronous OAuth 2.0 helper. See the module docstring for the flow."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        *,
        authorize_url: str = DEFAULT_AUTHORIZE_URL,
        token_url: str = DEFAULT_TOKEN_URL,
        http_client: httpx.Client | None = None,
    ) -> None:
        super().__init__(
            client_id,
            client_secret,
            redirect_uri,
            authorize_url=authorize_url,
            token_url=token_url,
        )
        self._http = http_client or httpx.Client(timeout=30.0)
        self._owns_http = http_client is None
        self._refresh_lock = threading.Lock()

    def exchange_code(self, code: str) -> OAuthTokens:
        """Exchange the authorization code for the initial token pair."""
        response = self._http.post(self.token_url, data=self._exchange_payload(code))
        return self._parse_tokens(response)

    def refresh(self, refresh_token: str) -> OAuthTokens:
        """Get a new token pair (serialized: see Refresh Token Rotation).

        Persist the returned pair immediately: the pair you passed in is now
        invalid.
        """
        with self._refresh_lock:
            response = self._http.post(
                self.token_url, data=self._refresh_payload(refresh_token)
            )
            return self._parse_tokens(response)

    def close(self) -> None:
        if self._owns_http:
            self._http.close()

    def __enter__(self) -> OAuthApp:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()


class AsyncOAuthApp(_BaseOAuthApp):
    """Asynchronous OAuth 2.0 helper. See the module docstring for the flow."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        *,
        authorize_url: str = DEFAULT_AUTHORIZE_URL,
        token_url: str = DEFAULT_TOKEN_URL,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        super().__init__(
            client_id,
            client_secret,
            redirect_uri,
            authorize_url=authorize_url,
            token_url=token_url,
        )
        self._http = http_client or httpx.AsyncClient(timeout=30.0)
        self._owns_http = http_client is None
        self._refresh_lock = asyncio.Lock()

    async def exchange_code(self, code: str) -> OAuthTokens:
        """Exchange the authorization code for the initial token pair."""
        response = await self._http.post(self.token_url, data=self._exchange_payload(code))
        return self._parse_tokens(response)

    async def refresh(self, refresh_token: str) -> OAuthTokens:
        """Get a new token pair (serialized: see Refresh Token Rotation).

        Persist the returned pair immediately: the pair you passed in is now
        invalid.
        """
        async with self._refresh_lock:
            response = await self._http.post(
                self.token_url, data=self._refresh_payload(refresh_token)
            )
            return self._parse_tokens(response)

    async def close(self) -> None:
        if self._owns_http:
            await self._http.aclose()

    async def __aenter__(self) -> AsyncOAuthApp:
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.close()
