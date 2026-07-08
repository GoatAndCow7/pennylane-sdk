from __future__ import annotations

import json

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.customers import (
    AsyncCompanyCustomers,
    AsyncCustomers,
    AsyncIndividualCustomers,
    CompanyCustomers,
    Customers,
    IndividualCustomers,
)

from ..conftest import BASE_URL

COMPANY_CUSTOMER = {
    "id": 42,
    "name": "Acme Corp",
    "billing_iban": None,
    "payment_conditions": "30_days",
    "recipient": "John Doe",
    "phone": "0102030405",
    "reference": None,
    "notes": None,
    "vat_number": "FR123456789",
    "reg_no": "123456789",
    "ledger_account": {"id": 7},
    "emails": ["billing@acme.example"],
    "billing_address": {
        "address": "1 rue de Paris",
        "postal_code": "75001",
        "city": "Paris",
        "country_alpha2": "FR",
    },
    "delivery_address": {
        "address": "1 rue de Paris",
        "postal_code": "75001",
        "city": "Paris",
        "country_alpha2": "FR",
    },
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
    "customer_type": "company",
    "external_reference": "CUST-1",
    "billing_language": "fr_FR",
    "mandates": {"url": "/gocardless_mandates?customer_id=42"},
    "pro_account_mandates": {"url": "/pro_account/mandates?customer_id=42"},
    "contacts": {"url": "/customers/42/contacts"},
}

INDIVIDUAL_CUSTOMER = {
    **{k: v for k, v in COMPANY_CUSTOMER.items() if k not in ("vat_number", "reg_no")},
    "id": 43,
    "name": "Jane Smith",
    "first_name": "Jane",
    "last_name": "Smith",
    "customer_type": "individual",
}

CATEGORY = {
    "id": 421,
    "label": "HR - Salaries",
    "weight": "1.0",
    "category_group": {"id": 9},
    "analytical_code": None,
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}

CONTACT = {
    "id": 5,
    "first_name": "Alice",
    "last_name": "Martin",
    "role": "Accountant",
    "email": "alice@acme.example",
    "telephone_number": "0102030405",
    "mobile_number": "0607080910",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}


class TestCustomers:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/customers").mock(
            return_value=httpx.Response(
                200, json={"items": [COMPANY_CUSTOMER], "has_more": False, "next_cursor": None}
            )
        )
        page = Customers(sync_client).list(limit=50, sort="-id")
        assert route.calls.last.request.url.params["limit"] == "50"
        customer = page.items[0]
        assert customer.id == 42
        assert customer.name == "Acme Corp"
        assert customer.ledger_account is not None
        assert customer.ledger_account.id == 7

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/customers/42").mock(
            return_value=httpx.Response(200, json=COMPANY_CUSTOMER)
        )
        customer = Customers(sync_client).get(42)
        assert customer.name == "Acme Corp"

    @respx.mock
    def test_list_categories(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/customers/42/categories").mock(
            return_value=httpx.Response(
                200, json={"items": [CATEGORY], "has_more": False, "next_cursor": None}
            )
        )
        page = Customers(sync_client).list_categories(42, limit=10)
        assert route.calls.last.request.url.params["limit"] == "10"
        assert page.items[0].id == 421
        assert page.items[0].category_group is not None
        assert page.items[0].category_group.id == 9

    @respx.mock
    def test_categorize(self, sync_client: SyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/customers/42/categories").mock(
            return_value=httpx.Response(200, json=[CATEGORY])
        )
        result = Customers(sync_client).categorize(42, categories=[{"id": 421, "weight": "1.0"}])
        assert json.loads(route.calls.last.request.content) == [{"id": 421, "weight": "1.0"}]
        assert result is None

    @respx.mock
    def test_list_contacts(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/customers/42/contacts").mock(
            return_value=httpx.Response(
                200, json={"items": [CONTACT], "has_more": False, "next_cursor": None}
            )
        )
        page = Customers(sync_client).list_contacts(42, sort="-id")
        assert route.calls.last.request.url.params["sort"] == "-id"
        assert page.items[0].email == "alice@acme.example"


class TestCompanyCustomers:
    @respx.mock
    def test_create(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/company_customers").mock(
            return_value=httpx.Response(201, json=COMPANY_CUSTOMER)
        )
        customer = CompanyCustomers(sync_client).create(
            name="Acme Corp",
            billing_address={
                "address": "1 rue de Paris",
                "postal_code": "75001",
                "city": "Paris",
                "country_alpha2": "FR",
            },
            vat_number="FR123456789",
        )
        body = json.loads(route.calls.last.request.content)
        assert body == {
            "name": "Acme Corp",
            "billing_address": {
                "address": "1 rue de Paris",
                "postal_code": "75001",
                "city": "Paris",
                "country_alpha2": "FR",
            },
            "vat_number": "FR123456789",
        }
        assert customer.id == 42

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/company_customers/42").mock(
            return_value=httpx.Response(200, json=COMPANY_CUSTOMER)
        )
        customer = CompanyCustomers(sync_client).get(42)
        assert customer.id == 42

    @respx.mock
    def test_update(self, sync_client: SyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/company_customers/42").mock(
            return_value=httpx.Response(200, json=COMPANY_CUSTOMER)
        )
        CompanyCustomers(sync_client).update(42, name="New name")
        assert json.loads(route.calls.last.request.content) == {"name": "New name"}


class TestIndividualCustomers:
    @respx.mock
    def test_create(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/individual_customers").mock(
            return_value=httpx.Response(201, json=INDIVIDUAL_CUSTOMER)
        )
        customer = IndividualCustomers(sync_client).create(
            first_name="Jane",
            last_name="Smith",
            billing_address={
                "address": "1 rue de Paris",
                "postal_code": "75001",
                "city": "Paris",
                "country_alpha2": "FR",
            },
        )
        body = json.loads(route.calls.last.request.content)
        assert body == {
            "first_name": "Jane",
            "last_name": "Smith",
            "billing_address": {
                "address": "1 rue de Paris",
                "postal_code": "75001",
                "city": "Paris",
                "country_alpha2": "FR",
            },
        }
        assert customer.first_name == "Jane"

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/individual_customers/43").mock(
            return_value=httpx.Response(200, json=INDIVIDUAL_CUSTOMER)
        )
        customer = IndividualCustomers(sync_client).get(43)
        assert customer.last_name == "Smith"

    @respx.mock
    def test_update(self, sync_client: SyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/individual_customers/43").mock(
            return_value=httpx.Response(200, json=INDIVIDUAL_CUSTOMER)
        )
        IndividualCustomers(sync_client).update(43, first_name="Janet")
        assert json.loads(route.calls.last.request.content) == {"first_name": "Janet"}


class TestCustomersSubResources:
    def test_sub_resources_share_client(self, sync_client: SyncAPIClient) -> None:
        customers = Customers(sync_client)
        assert isinstance(customers.companies, CompanyCustomers)
        assert isinstance(customers.individuals, IndividualCustomers)


class TestAsyncCustomers:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/customers").mock(
            return_value=httpx.Response(
                200, json={"items": [COMPANY_CUSTOMER], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncCustomers(async_client).list()
        assert page.items[0].id == 42

    @respx.mock
    async def test_get(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/customers/42").mock(
            return_value=httpx.Response(200, json=COMPANY_CUSTOMER)
        )
        customer = await AsyncCustomers(async_client).get(42)
        assert customer.id == 42

    @respx.mock
    async def test_categorize(self, async_client: AsyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/customers/42/categories").mock(
            return_value=httpx.Response(200, json=[CATEGORY])
        )
        result = await AsyncCustomers(async_client).categorize(
            42, categories=[{"id": 421, "weight": "1.0"}]
        )
        assert result is None

    @respx.mock
    async def test_list_contacts(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/customers/42/contacts").mock(
            return_value=httpx.Response(
                200, json={"items": [CONTACT], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncCustomers(async_client).list_contacts(42)
        assert page.items[0].id == 5

    @respx.mock
    async def test_list_categories(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/customers/42/categories").mock(
            return_value=httpx.Response(
                200, json={"items": [CATEGORY], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncCustomers(async_client).list_categories(42)
        assert page.items[0].id == 421


class TestAsyncCompanyCustomers:
    @respx.mock
    async def test_create(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/company_customers").mock(
            return_value=httpx.Response(201, json=COMPANY_CUSTOMER)
        )
        customer = await AsyncCompanyCustomers(async_client).create(
            name="Acme Corp",
            billing_address={
                "address": "1 rue de Paris",
                "postal_code": "75001",
                "city": "Paris",
                "country_alpha2": "FR",
            },
        )
        assert customer.id == 42

    @respx.mock
    async def test_get(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/company_customers/42").mock(
            return_value=httpx.Response(200, json=COMPANY_CUSTOMER)
        )
        customer = await AsyncCompanyCustomers(async_client).get(42)
        assert customer.id == 42

    @respx.mock
    async def test_update(self, async_client: AsyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/company_customers/42").mock(
            return_value=httpx.Response(200, json=COMPANY_CUSTOMER)
        )
        customer = await AsyncCompanyCustomers(async_client).update(42, name="New name")
        assert customer.id == 42


class TestAsyncIndividualCustomers:
    @respx.mock
    async def test_create(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/individual_customers").mock(
            return_value=httpx.Response(201, json=INDIVIDUAL_CUSTOMER)
        )
        customer = await AsyncIndividualCustomers(async_client).create(
            first_name="Jane",
            last_name="Smith",
            billing_address={
                "address": "1 rue de Paris",
                "postal_code": "75001",
                "city": "Paris",
                "country_alpha2": "FR",
            },
        )
        assert customer.first_name == "Jane"

    @respx.mock
    async def test_get(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/individual_customers/43").mock(
            return_value=httpx.Response(200, json=INDIVIDUAL_CUSTOMER)
        )
        customer = await AsyncIndividualCustomers(async_client).get(43)
        assert customer.id == 43

    @respx.mock
    async def test_update(self, async_client: AsyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/individual_customers/43").mock(
            return_value=httpx.Response(200, json=INDIVIDUAL_CUSTOMER)
        )
        customer = await AsyncIndividualCustomers(async_client).update(43, first_name="Janet")
        assert customer.id == 43
