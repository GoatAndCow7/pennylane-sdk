"""SEPA mandates, GoCardless mandates and Pro Account mandates resources (Company API v2).

Reference: https://pennylane.readme.io/reference/getsepamandates
"""

from __future__ import annotations

from collections.abc import Sequence

from ..._models import drop_none
from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...filters import FiltersInput
from ...types.company.mandates import (
    GocardlessMandate,
    MandateMigration,
    MandateMigrationCandidate,
    MandateMigrationResponse,
    ProAccountMandate,
    SepaMandate,
)

__all__ = [
    "AsyncGocardlessMandates",
    "AsyncProAccount",
    "AsyncSepaMandates",
    "GocardlessMandates",
    "ProAccount",
    "SepaMandates",
]


class SepaMandates(SyncAPIResource):
    """Manage SEPA direct debit mandates."""

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[SepaMandate]:
        """List SEPA mandates.

        Scope: ``customer_mandates:readonly``.
        Reference: https://pennylane.readme.io/reference/getsepamandates

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            "/sepa_mandates",
            item_type=SepaMandate,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    def get(self, sepa_mandate_id: int) -> SepaMandate:
        """Retrieve a SEPA mandate by its Pennylane identifier.

        Scope: ``customer_mandates:readonly``.
        Reference: https://pennylane.readme.io/reference/getsepamandate
        """
        return self._get(f"/sepa_mandates/{sepa_mandate_id}", cast_to=SepaMandate)

    def create(
        self,
        *,
        bic: str,
        iban: str,
        signed_at: str,
        identifier: str,
        customer_id: int,
        bank: str | None = None,
        sequence_type: str | None = None,
    ) -> SepaMandate:
        """Create a SEPA mandate.

        Scope: ``customer_mandates:all``.
        Reference: https://pennylane.readme.io/reference/postsepamandates

        Args:
            bic: Bank Identifier Code (BIC) of the customer's bank.
            iban: International Bank Account Number (IBAN) of the customer.
            signed_at: Date when the mandate was signed (ISO 8601 date).
            identifier: Unique identifier for the mandate.
            customer_id: ID of the customer for which the mandate is created.
            bank: Name of the customer's bank.
            sequence_type: SEPA mandate sequence type (``FRST``, ``OOFF``, ``RCUR``,
                ``FNAL``; default ``RCUR``).
        """
        body = drop_none(
            {
                "bic": bic,
                "iban": iban,
                "signed_at": signed_at,
                "identifier": identifier,
                "customer_id": customer_id,
                "bank": bank,
                "sequence_type": sequence_type,
            }
        )
        return self._post("/sepa_mandates", cast_to=SepaMandate, body=body)

    def update(
        self,
        sepa_mandate_id: int,
        *,
        bic: str | None = None,
        iban: str | None = None,
        signed_at: str | None = None,
        identifier: str | None = None,
        customer_id: int | None = None,
        bank: str | None = None,
        sequence_type: str | None = None,
    ) -> SepaMandate:
        """Update a SEPA mandate. Only the provided fields are modified.

        Scope: ``customer_mandates:all``.
        Reference: https://pennylane.readme.io/reference/putsepamandate
        """
        body = drop_none(
            {
                "bic": bic,
                "iban": iban,
                "signed_at": signed_at,
                "identifier": identifier,
                "customer_id": customer_id,
                "bank": bank,
                "sequence_type": sequence_type,
            }
        )
        return self._put(f"/sepa_mandates/{sepa_mandate_id}", cast_to=SepaMandate, body=body)

    def delete(self, sepa_mandate_id: int) -> None:
        """Delete a SEPA mandate.

        Scope: ``customer_mandates:all``.
        Reference: https://pennylane.readme.io/reference/deletesepamandate
        """
        return self._delete(f"/sepa_mandates/{sepa_mandate_id}", cast_to=None)


class GocardlessMandates(SyncAPIResource):
    """Manage GoCardless direct debit mandates."""

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[GocardlessMandate]:
        """List GoCardless mandates.

        Scope: ``customer_mandates:readonly``.
        Reference: https://pennylane.readme.io/reference/getgocardlessmandates

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            "/gocardless_mandates",
            item_type=GocardlessMandate,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    def get(self, gocardless_mandate_id: int) -> GocardlessMandate:
        """Retrieve a GoCardless mandate by its Pennylane identifier.

        Scope: ``customer_mandates:readonly``.
        Reference: https://pennylane.readme.io/reference/getgocardlessmandate
        """
        return self._get(
            f"/gocardless_mandates/{gocardless_mandate_id}", cast_to=GocardlessMandate
        )

    def send_mail_request(
        self,
        *,
        customer_id: int,
        recipients: Sequence[str],
        subject: str | None = None,
        body: str | None = None,
    ) -> None:
        """Send a GoCardless mandate email request to a customer.

        Scope: ``customer_mandates:all``.
        Reference: https://pennylane.readme.io/reference/postgocardlessmandatemailrequests

        Args:
            customer_id: Customer identifier.
            recipients: Email recipient addresses.
            subject: Email subject line.
            body: Email body content.
        """
        payload = drop_none(
            {
                "customer_id": customer_id,
                "email": drop_none(
                    {"subject": subject, "body": body, "recipients": recipients}
                ),
            }
        )
        return self._post("/gocardless_mandates/mail_requests", cast_to=None, body=payload)

    def cancel(self, gocardless_mandate_id: int) -> None:
        """Cancel a GoCardless mandate.

        Scope: ``customer_mandates:all``.
        Reference: https://pennylane.readme.io/reference/postgocardlessmandatecancellations
        """
        return self._post(
            f"/gocardless_mandates/{gocardless_mandate_id}/cancellations", cast_to=None
        )

    def associate(self, gocardless_mandate_id: int, *, customer_id: int) -> None:
        """Associate a GoCardless mandate to a customer.

        Scope: ``customer_mandates:all``.
        Reference: https://pennylane.readme.io/reference/postgocardlessmandateassociations

        Args:
            customer_id: Customer identifier.
        """
        body = {"customer_id": customer_id}
        return self._post(
            f"/gocardless_mandates/{gocardless_mandate_id}/associations",
            cast_to=None,
            body=body,
        )


class ProAccount(SyncAPIResource):
    """Manage Pennylane Pro Account mandates and migrations."""

    def request_mandate(self, *, customer_id: int) -> None:
        """Send a Pro Account SEPA mandate request to a customer.

        Scope: ``customer_mandates:all``.
        Reference: https://pennylane.readme.io/reference/postproaccountmandatemailrequests

        Args:
            customer_id: Customer identifier.
        """
        body = {"customer_id": customer_id}
        return self._post("/pro_account/mandate_requests", cast_to=None, body=body)

    def list_mandate_migrations(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[MandateMigrationCandidate]:
        """List mandate migration candidates for the Pro Account.

        Scope: ``customer_mandates:readonly``.
        Reference: https://pennylane.readme.io/reference/getproaccountmandatemigrations

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            "/pro_account/mandate_migrations",
            item_type=MandateMigrationCandidate,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    def migrate_mandate(
        self,
        *,
        mandate_type: str,
        mandate_id: int,
        early_execution_date_permitted: bool | None = None,
    ) -> MandateMigration:
        """Migrate a mandate to Pro Account.

        Scope: ``customer_mandates:all``.
        Reference: https://pennylane.readme.io/reference/postproaccountmandatemigrations

        Args:
            mandate_type: Type of the mandate to migrate (``SepaMandate`` or
                ``Mandate`` for GoCardless mandates).
            mandate_id: ID of the mandate to migrate.
            early_execution_date_permitted: Whether to permit early execution date
                for the migration (defaults to ``False``).
        """
        body = drop_none(
            {
                "mandate_type": mandate_type,
                "mandate_id": mandate_id,
                "early_execution_date_permitted": early_execution_date_permitted,
            }
        )
        response = self._post(
            "/pro_account/mandate_migrations", cast_to=MandateMigrationResponse, body=body
        )
        return response.mandate_migration

    def list_mandates(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[ProAccountMandate]:
        """List Pro Account payment mandates.

        Scope: ``customer_mandates:readonly``.
        Reference: https://pennylane.readme.io/reference/getproaccountmandates

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            "/pro_account/mandates",
            item_type=ProAccountMandate,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )


class AsyncSepaMandates(AsyncAPIResource):
    """Manage SEPA direct debit mandates (async)."""

    async def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[SepaMandate]:
        """List SEPA mandates.

        Scope: ``customer_mandates:readonly``.
        Reference: https://pennylane.readme.io/reference/getsepamandates
        """
        return await self._get_page(
            "/sepa_mandates",
            item_type=SepaMandate,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    async def get(self, sepa_mandate_id: int) -> SepaMandate:
        """Retrieve a SEPA mandate by its Pennylane identifier.

        Scope: ``customer_mandates:readonly``.
        Reference: https://pennylane.readme.io/reference/getsepamandate
        """
        return await self._get(f"/sepa_mandates/{sepa_mandate_id}", cast_to=SepaMandate)

    async def create(
        self,
        *,
        bic: str,
        iban: str,
        signed_at: str,
        identifier: str,
        customer_id: int,
        bank: str | None = None,
        sequence_type: str | None = None,
    ) -> SepaMandate:
        """Create a SEPA mandate.

        Scope: ``customer_mandates:all``.
        Reference: https://pennylane.readme.io/reference/postsepamandates
        """
        body = drop_none(
            {
                "bic": bic,
                "iban": iban,
                "signed_at": signed_at,
                "identifier": identifier,
                "customer_id": customer_id,
                "bank": bank,
                "sequence_type": sequence_type,
            }
        )
        return await self._post("/sepa_mandates", cast_to=SepaMandate, body=body)

    async def update(
        self,
        sepa_mandate_id: int,
        *,
        bic: str | None = None,
        iban: str | None = None,
        signed_at: str | None = None,
        identifier: str | None = None,
        customer_id: int | None = None,
        bank: str | None = None,
        sequence_type: str | None = None,
    ) -> SepaMandate:
        """Update a SEPA mandate. Only the provided fields are modified.

        Scope: ``customer_mandates:all``.
        Reference: https://pennylane.readme.io/reference/putsepamandate
        """
        body = drop_none(
            {
                "bic": bic,
                "iban": iban,
                "signed_at": signed_at,
                "identifier": identifier,
                "customer_id": customer_id,
                "bank": bank,
                "sequence_type": sequence_type,
            }
        )
        return await self._put(
            f"/sepa_mandates/{sepa_mandate_id}", cast_to=SepaMandate, body=body
        )

    async def delete(self, sepa_mandate_id: int) -> None:
        """Delete a SEPA mandate.

        Scope: ``customer_mandates:all``.
        Reference: https://pennylane.readme.io/reference/deletesepamandate
        """
        return await self._delete(f"/sepa_mandates/{sepa_mandate_id}", cast_to=None)


class AsyncGocardlessMandates(AsyncAPIResource):
    """Manage GoCardless direct debit mandates (async)."""

    async def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[GocardlessMandate]:
        """List GoCardless mandates.

        Scope: ``customer_mandates:readonly``.
        Reference: https://pennylane.readme.io/reference/getgocardlessmandates
        """
        return await self._get_page(
            "/gocardless_mandates",
            item_type=GocardlessMandate,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    async def get(self, gocardless_mandate_id: int) -> GocardlessMandate:
        """Retrieve a GoCardless mandate by its Pennylane identifier.

        Scope: ``customer_mandates:readonly``.
        Reference: https://pennylane.readme.io/reference/getgocardlessmandate
        """
        return await self._get(
            f"/gocardless_mandates/{gocardless_mandate_id}", cast_to=GocardlessMandate
        )

    async def send_mail_request(
        self,
        *,
        customer_id: int,
        recipients: Sequence[str],
        subject: str | None = None,
        body: str | None = None,
    ) -> None:
        """Send a GoCardless mandate email request to a customer.

        Scope: ``customer_mandates:all``.
        Reference: https://pennylane.readme.io/reference/postgocardlessmandatemailrequests
        """
        payload = drop_none(
            {
                "customer_id": customer_id,
                "email": drop_none(
                    {"subject": subject, "body": body, "recipients": recipients}
                ),
            }
        )
        return await self._post(
            "/gocardless_mandates/mail_requests", cast_to=None, body=payload
        )

    async def cancel(self, gocardless_mandate_id: int) -> None:
        """Cancel a GoCardless mandate.

        Scope: ``customer_mandates:all``.
        Reference: https://pennylane.readme.io/reference/postgocardlessmandatecancellations
        """
        return await self._post(
            f"/gocardless_mandates/{gocardless_mandate_id}/cancellations", cast_to=None
        )

    async def associate(self, gocardless_mandate_id: int, *, customer_id: int) -> None:
        """Associate a GoCardless mandate to a customer.

        Scope: ``customer_mandates:all``.
        Reference: https://pennylane.readme.io/reference/postgocardlessmandateassociations
        """
        body = {"customer_id": customer_id}
        return await self._post(
            f"/gocardless_mandates/{gocardless_mandate_id}/associations",
            cast_to=None,
            body=body,
        )


class AsyncProAccount(AsyncAPIResource):
    """Manage Pennylane Pro Account mandates and migrations (async)."""

    async def request_mandate(self, *, customer_id: int) -> None:
        """Send a Pro Account SEPA mandate request to a customer.

        Scope: ``customer_mandates:all``.
        Reference: https://pennylane.readme.io/reference/postproaccountmandatemailrequests
        """
        body = {"customer_id": customer_id}
        return await self._post("/pro_account/mandate_requests", cast_to=None, body=body)

    async def list_mandate_migrations(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[MandateMigrationCandidate]:
        """List mandate migration candidates for the Pro Account.

        Scope: ``customer_mandates:readonly``.
        Reference: https://pennylane.readme.io/reference/getproaccountmandatemigrations
        """
        return await self._get_page(
            "/pro_account/mandate_migrations",
            item_type=MandateMigrationCandidate,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    async def migrate_mandate(
        self,
        *,
        mandate_type: str,
        mandate_id: int,
        early_execution_date_permitted: bool | None = None,
    ) -> MandateMigration:
        """Migrate a mandate to Pro Account.

        Scope: ``customer_mandates:all``.
        Reference: https://pennylane.readme.io/reference/postproaccountmandatemigrations
        """
        body = drop_none(
            {
                "mandate_type": mandate_type,
                "mandate_id": mandate_id,
                "early_execution_date_permitted": early_execution_date_permitted,
            }
        )
        response = await self._post(
            "/pro_account/mandate_migrations", cast_to=MandateMigrationResponse, body=body
        )
        return response.mandate_migration

    async def list_mandates(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[ProAccountMandate]:
        """List Pro Account payment mandates.

        Scope: ``customer_mandates:readonly``.
        Reference: https://pennylane.readme.io/reference/getproaccountmandates
        """
        return await self._get_page(
            "/pro_account/mandates",
            item_type=ProAccountMandate,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )
