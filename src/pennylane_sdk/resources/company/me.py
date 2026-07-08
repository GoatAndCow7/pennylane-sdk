"""Me resource (Company API v2).

Reference: https://pennylane.readme.io/reference/getme
"""

from __future__ import annotations

from ..._resource import AsyncAPIResource, SyncAPIResource
from ...types.company.me import Me as MeProfile

__all__ = ["AsyncMe", "Me"]


class Me(SyncAPIResource):
    """Retrieve the authenticated user and company profile."""

    def retrieve(self) -> MeProfile:
        """Return information about the company and the user tied to the token.

        Scope: none (available with any valid token).
        Reference: https://pennylane.readme.io/reference/getme
        """
        return self._get("/me", cast_to=MeProfile)


class AsyncMe(AsyncAPIResource):
    """Retrieve the authenticated user and company profile (async)."""

    async def retrieve(self) -> MeProfile:
        """Return information about the company and the user tied to the token.

        Scope: none (available with any valid token).
        Reference: https://pennylane.readme.io/reference/getme
        """
        return await self._get("/me", cast_to=MeProfile)
