"""Customers resource (Company API v2).

Reference: https://pennylane.readme.io/reference/getcustomers
"""

from __future__ import annotations

import builtins
from typing import TYPE_CHECKING, Any

from ..._models import drop_none
from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...filters import FiltersInput
from ...types.company.customers import Customer, CustomerCategory, CustomerContact

if TYPE_CHECKING:
    from ..._base_client import AsyncAPIClient, SyncAPIClient

__all__ = [
    "AsyncCompanyCustomers",
    "AsyncCustomers",
    "AsyncIndividualCustomers",
    "CompanyCustomers",
    "Customers",
    "IndividualCustomers",
]


class Customers(SyncAPIResource):
    """Manage customers (company and individual).

    ``.companies`` and ``.individuals`` expose the type-specific create/update
    endpoints, e.g. ``client.customers.companies.create(...)``.
    """

    def __init__(self, client: SyncAPIClient) -> None:
        super().__init__(client)
        self.companies = CompanyCustomers(client)
        self.individuals = IndividualCustomers(client)

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[Customer]:
        """List customers (company and individual).

        Scope: ``customers:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomers

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`.
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            "/customers",
            item_type=Customer,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    def get(self, customer_id: int) -> Customer:
        """Retrieve a customer by its Pennylane identifier.

        Scope: ``customers:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomer
        """
        return self._get(f"/customers/{customer_id}", cast_to=Customer)

    def list_categories(
        self,
        customer_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> SyncCursorPage[CustomerCategory]:
        """List the categories assigned to a customer.

        Scope: ``customers:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomercategories
        """
        return self._get_page(
            f"/customers/{customer_id}/categories",
            item_type=CustomerCategory,
            params={"cursor": cursor, "limit": limit},
        )

    def categorize(
        self, customer_id: int, *, categories: builtins.list[dict[str, Any]]
    ) -> None:
        """Replace the categories assigned to a customer.

        Scope: ``customers:all``.
        Reference: https://pennylane.readme.io/reference/putcustomercategories

        Args:
            categories: List of ``{"id": <category id>, "weight": <str fraction, e.g. "0.6575">}``.
        """
        self._put(f"/customers/{customer_id}/categories", cast_to=None, body=categories)

    def list_contacts(
        self,
        customer_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[CustomerContact]:
        """List the contacts of a customer.

        Scope: ``customers:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomercontacts
        """
        return self._get_page(
            f"/customers/{customer_id}/contacts",
            item_type=CustomerContact,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )


class CompanyCustomers(SyncAPIResource):
    """Manage company customers."""

    def create(
        self,
        *,
        name: str,
        billing_address: dict[str, Any],
        vat_number: str | None = None,
        reg_no: str | None = None,
        ledger_account: dict[str, Any] | None = None,
        phone: str | None = None,
        delivery_address: dict[str, Any] | None = None,
        payment_conditions: str | None = None,
        billing_iban: str | None = None,
        recipient: str | None = None,
        reference: str | None = None,
        notes: str | None = None,
        emails: list[str] | None = None,
        external_reference: str | None = None,
        billing_language: str | None = None,
    ) -> Customer:
        """Create a company customer.

        Scope: ``customers:all``.
        Reference: https://pennylane.readme.io/reference/postcompanycustomer

        Args:
            name: Company name.
            billing_address: ``{"address", "postal_code", "city", "country_alpha2"}``.
            vat_number: VAT number.
            reg_no: Registration number (SIREN in France).
            ledger_account: ``{"number": <ledger account number>}``.
            phone: Phone number.
            delivery_address: Same shape as ``billing_address``.
            payment_conditions: One of ``upon_receipt``, ``custom``, ``7_days``,
                ``15_days``, ``30_days``, ``30_days_end_of_month``, ``45_days``,
                ``45_days_end_of_month``, ``60_days`` (default ``30_days``).
            billing_iban: Billing IBAN.
            recipient: Name of the person the invoice is addressed to.
            reference: Your own reference for this customer.
            notes: Free-form notes.
            emails: Email addresses.
            external_reference: Your own unique reference (auto-assigned if omitted).
            billing_language: One of ``fr_FR``, ``en_GB``, ``de_DE`` (default ``fr_FR``).
        """
        body = drop_none(
            {
                "name": name,
                "billing_address": billing_address,
                "vat_number": vat_number,
                "reg_no": reg_no,
                "ledger_account": ledger_account,
                "phone": phone,
                "delivery_address": delivery_address,
                "payment_conditions": payment_conditions,
                "billing_iban": billing_iban,
                "recipient": recipient,
                "reference": reference,
                "notes": notes,
                "emails": emails,
                "external_reference": external_reference,
                "billing_language": billing_language,
            }
        )
        return self._post("/company_customers", cast_to=Customer, body=body)

    def get(self, company_customer_id: int) -> Customer:
        """Retrieve a company customer by its Pennylane identifier.

        Scope: ``customers:readonly``.
        Reference: https://pennylane.readme.io/reference/getcompanycustomer
        """
        return self._get(f"/company_customers/{company_customer_id}", cast_to=Customer)

    def update(
        self,
        company_customer_id: int,
        *,
        name: str | None = None,
        vat_number: str | None = None,
        reg_no: str | None = None,
        phone: str | None = None,
        billing_address: dict[str, Any] | None = None,
        delivery_address: dict[str, Any] | None = None,
        payment_conditions: str | None = None,
        billing_iban: str | None = None,
        recipient: str | None = None,
        reference: str | None = None,
        notes: str | None = None,
        emails: list[str] | None = None,
        external_reference: str | None = None,
        billing_language: str | None = None,
    ) -> Customer:
        """Update a company customer. Only the provided fields are modified.

        Scope: ``customers:all``.
        Reference: https://pennylane.readme.io/reference/putcompanycustomer
        """
        body = drop_none(
            {
                "name": name,
                "vat_number": vat_number,
                "reg_no": reg_no,
                "phone": phone,
                "billing_address": billing_address,
                "delivery_address": delivery_address,
                "payment_conditions": payment_conditions,
                "billing_iban": billing_iban,
                "recipient": recipient,
                "reference": reference,
                "notes": notes,
                "emails": emails,
                "external_reference": external_reference,
                "billing_language": billing_language,
            }
        )
        return self._put(f"/company_customers/{company_customer_id}", cast_to=Customer, body=body)


class IndividualCustomers(SyncAPIResource):
    """Manage individual customers."""

    def create(
        self,
        *,
        first_name: str,
        last_name: str,
        billing_address: dict[str, Any],
        phone: str | None = None,
        delivery_address: dict[str, Any] | None = None,
        payment_conditions: str | None = None,
        billing_iban: str | None = None,
        recipient: str | None = None,
        reference: str | None = None,
        ledger_account: dict[str, Any] | None = None,
        notes: str | None = None,
        emails: list[str] | None = None,
        external_reference: str | None = None,
        billing_language: str | None = None,
    ) -> Customer:
        """Create an individual customer.

        Scope: ``customers:all``.
        Reference: https://pennylane.readme.io/reference/postindividualcustomer

        Args:
            first_name: Given name.
            last_name: Family name.
            billing_address: ``{"address", "postal_code", "city", "country_alpha2"}``.
            phone: Phone number.
            delivery_address: Same shape as ``billing_address``.
            payment_conditions: See :meth:`CompanyCustomers.create`.
            billing_iban: Billing IBAN.
            recipient: Name of the person the invoice is addressed to.
            reference: Your own reference for this customer.
            ledger_account: ``{"number": <ledger account number>}``.
            notes: Free-form notes.
            emails: Email addresses.
            external_reference: Your own unique reference (auto-assigned if omitted).
            billing_language: One of ``fr_FR``, ``en_GB``, ``de_DE`` (default ``fr_FR``).
        """
        body = drop_none(
            {
                "first_name": first_name,
                "last_name": last_name,
                "billing_address": billing_address,
                "phone": phone,
                "delivery_address": delivery_address,
                "payment_conditions": payment_conditions,
                "billing_iban": billing_iban,
                "recipient": recipient,
                "reference": reference,
                "ledger_account": ledger_account,
                "notes": notes,
                "emails": emails,
                "external_reference": external_reference,
                "billing_language": billing_language,
            }
        )
        return self._post("/individual_customers", cast_to=Customer, body=body)

    def get(self, individual_customer_id: int) -> Customer:
        """Retrieve an individual customer by its Pennylane identifier.

        Scope: ``customers:readonly``.
        Reference: https://pennylane.readme.io/reference/getindividualcustomer
        """
        return self._get(f"/individual_customers/{individual_customer_id}", cast_to=Customer)

    def update(
        self,
        individual_customer_id: int,
        *,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None,
        billing_address: dict[str, Any] | None = None,
        delivery_address: dict[str, Any] | None = None,
        payment_conditions: str | None = None,
        billing_iban: str | None = None,
        recipient: str | None = None,
        reference: str | None = None,
        notes: str | None = None,
        emails: list[str] | None = None,
        external_reference: str | None = None,
        billing_language: str | None = None,
    ) -> Customer:
        """Update an individual customer. Only the provided fields are modified.

        Scope: ``customers:all``.
        Reference: https://pennylane.readme.io/reference/putindividualcustomer
        """
        body = drop_none(
            {
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone,
                "billing_address": billing_address,
                "delivery_address": delivery_address,
                "payment_conditions": payment_conditions,
                "billing_iban": billing_iban,
                "recipient": recipient,
                "reference": reference,
                "notes": notes,
                "emails": emails,
                "external_reference": external_reference,
                "billing_language": billing_language,
            }
        )
        return self._put(
            f"/individual_customers/{individual_customer_id}", cast_to=Customer, body=body
        )


class AsyncCustomers(AsyncAPIResource):
    """Manage customers (company and individual), async."""

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.companies = AsyncCompanyCustomers(client)
        self.individuals = AsyncIndividualCustomers(client)

    async def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[Customer]:
        """List customers (company and individual).

        Scope: ``customers:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomers
        """
        return await self._get_page(
            "/customers",
            item_type=Customer,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    async def get(self, customer_id: int) -> Customer:
        """Retrieve a customer by its Pennylane identifier.

        Scope: ``customers:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomer
        """
        return await self._get(f"/customers/{customer_id}", cast_to=Customer)

    async def list_categories(
        self,
        customer_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> AsyncCursorPage[CustomerCategory]:
        """List the categories assigned to a customer.

        Scope: ``customers:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomercategories
        """
        return await self._get_page(
            f"/customers/{customer_id}/categories",
            item_type=CustomerCategory,
            params={"cursor": cursor, "limit": limit},
        )

    async def categorize(
        self, customer_id: int, *, categories: builtins.list[dict[str, Any]]
    ) -> None:
        """Replace the categories assigned to a customer.

        Scope: ``customers:all``.
        Reference: https://pennylane.readme.io/reference/putcustomercategories
        """
        await self._put(f"/customers/{customer_id}/categories", cast_to=None, body=categories)

    async def list_contacts(
        self,
        customer_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[CustomerContact]:
        """List the contacts of a customer.

        Scope: ``customers:readonly``.
        Reference: https://pennylane.readme.io/reference/getcustomercontacts
        """
        return await self._get_page(
            f"/customers/{customer_id}/contacts",
            item_type=CustomerContact,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )


class AsyncCompanyCustomers(AsyncAPIResource):
    """Manage company customers (async)."""

    async def create(
        self,
        *,
        name: str,
        billing_address: dict[str, Any],
        vat_number: str | None = None,
        reg_no: str | None = None,
        ledger_account: dict[str, Any] | None = None,
        phone: str | None = None,
        delivery_address: dict[str, Any] | None = None,
        payment_conditions: str | None = None,
        billing_iban: str | None = None,
        recipient: str | None = None,
        reference: str | None = None,
        notes: str | None = None,
        emails: list[str] | None = None,
        external_reference: str | None = None,
        billing_language: str | None = None,
    ) -> Customer:
        """Create a company customer.

        Scope: ``customers:all``.
        Reference: https://pennylane.readme.io/reference/postcompanycustomer
        """
        body = drop_none(
            {
                "name": name,
                "billing_address": billing_address,
                "vat_number": vat_number,
                "reg_no": reg_no,
                "ledger_account": ledger_account,
                "phone": phone,
                "delivery_address": delivery_address,
                "payment_conditions": payment_conditions,
                "billing_iban": billing_iban,
                "recipient": recipient,
                "reference": reference,
                "notes": notes,
                "emails": emails,
                "external_reference": external_reference,
                "billing_language": billing_language,
            }
        )
        return await self._post("/company_customers", cast_to=Customer, body=body)

    async def get(self, company_customer_id: int) -> Customer:
        """Retrieve a company customer by its Pennylane identifier.

        Scope: ``customers:readonly``.
        Reference: https://pennylane.readme.io/reference/getcompanycustomer
        """
        return await self._get(f"/company_customers/{company_customer_id}", cast_to=Customer)

    async def update(
        self,
        company_customer_id: int,
        *,
        name: str | None = None,
        vat_number: str | None = None,
        reg_no: str | None = None,
        phone: str | None = None,
        billing_address: dict[str, Any] | None = None,
        delivery_address: dict[str, Any] | None = None,
        payment_conditions: str | None = None,
        billing_iban: str | None = None,
        recipient: str | None = None,
        reference: str | None = None,
        notes: str | None = None,
        emails: list[str] | None = None,
        external_reference: str | None = None,
        billing_language: str | None = None,
    ) -> Customer:
        """Update a company customer. Only the provided fields are modified.

        Scope: ``customers:all``.
        Reference: https://pennylane.readme.io/reference/putcompanycustomer
        """
        body = drop_none(
            {
                "name": name,
                "vat_number": vat_number,
                "reg_no": reg_no,
                "phone": phone,
                "billing_address": billing_address,
                "delivery_address": delivery_address,
                "payment_conditions": payment_conditions,
                "billing_iban": billing_iban,
                "recipient": recipient,
                "reference": reference,
                "notes": notes,
                "emails": emails,
                "external_reference": external_reference,
                "billing_language": billing_language,
            }
        )
        return await self._put(
            f"/company_customers/{company_customer_id}", cast_to=Customer, body=body
        )


class AsyncIndividualCustomers(AsyncAPIResource):
    """Manage individual customers (async)."""

    async def create(
        self,
        *,
        first_name: str,
        last_name: str,
        billing_address: dict[str, Any],
        phone: str | None = None,
        delivery_address: dict[str, Any] | None = None,
        payment_conditions: str | None = None,
        billing_iban: str | None = None,
        recipient: str | None = None,
        reference: str | None = None,
        ledger_account: dict[str, Any] | None = None,
        notes: str | None = None,
        emails: list[str] | None = None,
        external_reference: str | None = None,
        billing_language: str | None = None,
    ) -> Customer:
        """Create an individual customer.

        Scope: ``customers:all``.
        Reference: https://pennylane.readme.io/reference/postindividualcustomer
        """
        body = drop_none(
            {
                "first_name": first_name,
                "last_name": last_name,
                "billing_address": billing_address,
                "phone": phone,
                "delivery_address": delivery_address,
                "payment_conditions": payment_conditions,
                "billing_iban": billing_iban,
                "recipient": recipient,
                "reference": reference,
                "ledger_account": ledger_account,
                "notes": notes,
                "emails": emails,
                "external_reference": external_reference,
                "billing_language": billing_language,
            }
        )
        return await self._post("/individual_customers", cast_to=Customer, body=body)

    async def get(self, individual_customer_id: int) -> Customer:
        """Retrieve an individual customer by its Pennylane identifier.

        Scope: ``customers:readonly``.
        Reference: https://pennylane.readme.io/reference/getindividualcustomer
        """
        return await self._get(f"/individual_customers/{individual_customer_id}", cast_to=Customer)

    async def update(
        self,
        individual_customer_id: int,
        *,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None,
        billing_address: dict[str, Any] | None = None,
        delivery_address: dict[str, Any] | None = None,
        payment_conditions: str | None = None,
        billing_iban: str | None = None,
        recipient: str | None = None,
        reference: str | None = None,
        notes: str | None = None,
        emails: list[str] | None = None,
        external_reference: str | None = None,
        billing_language: str | None = None,
    ) -> Customer:
        """Update an individual customer. Only the provided fields are modified.

        Scope: ``customers:all``.
        Reference: https://pennylane.readme.io/reference/putindividualcustomer
        """
        body = drop_none(
            {
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone,
                "billing_address": billing_address,
                "delivery_address": delivery_address,
                "payment_conditions": payment_conditions,
                "billing_iban": billing_iban,
                "recipient": recipient,
                "reference": reference,
                "notes": notes,
                "emails": emails,
                "external_reference": external_reference,
                "billing_language": billing_language,
            }
        )
        return await self._put(
            f"/individual_customers/{individual_customer_id}", cast_to=Customer, body=body
        )
