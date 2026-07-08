"""Models for the Me resource (Company API v2)."""

from __future__ import annotations

from ..._models import PennylaneModel

__all__ = ["Me", "MeCompany", "MeUser"]


class MeUser(PennylaneModel):
    """The user associated with the access token."""

    id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    locale: str | None = None


class MeCompany(PennylaneModel):
    """The company associated with the access token."""

    id: int | None = None
    name: str | None = None
    reg_no: str | None = None
    accounting_logic: str | None = None


class Me(PennylaneModel):
    """The authenticated user, company and OAuth scopes.

    This response has no top-level ``id`` field.

    Reference: https://pennylane.readme.io/reference/getme
    """

    user: MeUser | None = None
    company: MeCompany | None = None
    scopes: list[str] | None = None
