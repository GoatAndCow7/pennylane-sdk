from __future__ import annotations

import json

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.mandates import (
    AsyncGocardlessMandates,
    AsyncProAccount,
    AsyncSepaMandates,
    GocardlessMandates,
    ProAccount,
    SepaMandates,
)

from ..conftest import BASE_URL

SEPA_MANDATE = {
    "id": 1,
    "bank": "BNP Paribas",
    "bic": "BNPAFRPP",
    "iban": "FR7630006000011234567890189",
    "sequence_type": "RCUR",
    "signed_at": "2026-01-05",
    "identifier": "MANDATE-1",
    "customer": {"id": 7, "url": "https://app.pennylane.com/api/external/v2/customers/7"},
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}

GOCARDLESS_MANDATE = {
    "id": 2,
    "external_reference": "GC-REF-1",
    "customer": {"id": 7, "url": "https://app.pennylane.com/api/external/v2/customers/7"},
    "status": "active",
    "external_customer_account": "GC-CUST-1",
    "external_customer_label": "Acme Corp",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}

MANDATE_MIGRATION_CANDIDATE = {
    "id": 3,
    "status": "available",
    "direct_debit_method": "GoCardless",
    "signed_at": "2026-01-05",
    "error_message": None,
    "migrated_at": None,
    "migration_started_at": None,
    "mandate": {"id": 2, "type": "Mandate"},
    "customer": {
        "id": 7,
        "url": "https://app.pennylane.com/api/external/v2/customers/7",
        "pro_account_mandate": None,
    },
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}

MANDATE_MIGRATION = {
    "mandate_migration": {
        "id": 4,
        "status": "available",
        "direct_debit_method": "GoCardless",
        "signed_at": "2026-01-05",
        "error_message": None,
        "migrated_at": None,
        "migration_started_at": None,
        "created_at": "2026-01-05T09:00:00Z",
        "updated_at": "2026-01-06T10:00:00Z",
        "mandate": {"id": 2, "type": "Mandate"},
        "customer": {
            "id": 7,
            "url": "https://app.pennylane.com/api/external/v2/customers/7",
            "pro_account_mandate": None,
        },
    }
}

PRO_ACCOUNT_MANDATE = {
    "status": "active",
    "early_execution_date_permitted": False,
    "active_billing_subscription": True,
    "signed_at": "2026-01-05",
    "created_at": "2026-01-05T09:00:00Z",
    "pdf_url": "https://files.pennylane.com/mandate.pdf",
    "customer": {"id": 7, "url": "https://app.pennylane.com/api/external/v2/customers/7"},
}


class TestSepaMandates:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/sepa_mandates").mock(
            return_value=httpx.Response(
                200, json={"items": [SEPA_MANDATE], "has_more": False, "next_cursor": None}
            )
        )
        page = SepaMandates(sync_client).list(limit=50, sort="-id")
        assert route.calls.last.request.url.params["limit"] == "50"
        assert route.calls.last.request.url.params["sort"] == "-id"
        mandate = page.items[0]
        assert mandate.id == 1
        assert mandate.iban == "FR7630006000011234567890189"
        assert mandate.customer is not None
        assert mandate.customer.id == 7

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/sepa_mandates/1").mock(
            return_value=httpx.Response(200, json=SEPA_MANDATE)
        )
        mandate = SepaMandates(sync_client).get(1)
        assert mandate.bic == "BNPAFRPP"

    @respx.mock
    def test_create_drops_none(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/sepa_mandates").mock(
            return_value=httpx.Response(201, json=SEPA_MANDATE)
        )
        SepaMandates(sync_client).create(
            bic="BNPAFRPP",
            iban="FR7630006000011234567890189",
            signed_at="2026-01-05",
            identifier="MANDATE-1",
            customer_id=7,
        )
        body = json.loads(route.calls.last.request.content)
        assert body == {
            "bic": "BNPAFRPP",
            "iban": "FR7630006000011234567890189",
            "signed_at": "2026-01-05",
            "identifier": "MANDATE-1",
            "customer_id": 7,
        }

    @respx.mock
    def test_update_sends_only_provided_fields(self, sync_client: SyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/sepa_mandates/1").mock(
            return_value=httpx.Response(200, json=SEPA_MANDATE)
        )
        SepaMandates(sync_client).update(1, bank="Societe Generale")
        assert json.loads(route.calls.last.request.content) == {"bank": "Societe Generale"}

    @respx.mock
    def test_delete(self, sync_client: SyncAPIClient) -> None:
        route = respx.delete(f"{BASE_URL}/sepa_mandates/1").mock(
            return_value=httpx.Response(204)
        )
        result = SepaMandates(sync_client).delete(1)
        assert result is None
        assert route.called


class TestGocardlessMandates:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/gocardless_mandates").mock(
            return_value=httpx.Response(
                200,
                json={"items": [GOCARDLESS_MANDATE], "has_more": False, "next_cursor": None},
            )
        )
        page = GocardlessMandates(sync_client).list()
        assert page.items[0].id == 2
        assert page.items[0].status == "active"

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/gocardless_mandates/2").mock(
            return_value=httpx.Response(200, json=GOCARDLESS_MANDATE)
        )
        mandate = GocardlessMandates(sync_client).get(2)
        assert mandate.external_reference == "GC-REF-1"

    @respx.mock
    def test_send_mail_request(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/gocardless_mandates/mail_requests").mock(
            return_value=httpx.Response(204)
        )
        result = GocardlessMandates(sync_client).send_mail_request(
            customer_id=7, recipients=["client@example.com"], subject="Sign your mandate"
        )
        assert result is None
        body = json.loads(route.calls.last.request.content)
        assert body == {
            "customer_id": 7,
            "email": {"recipients": ["client@example.com"], "subject": "Sign your mandate"},
        }

    @respx.mock
    def test_cancel(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/gocardless_mandates/2/cancellations").mock(
            return_value=httpx.Response(204)
        )
        result = GocardlessMandates(sync_client).cancel(2)
        assert result is None
        assert route.called

    @respx.mock
    def test_associate(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/gocardless_mandates/2/associations").mock(
            return_value=httpx.Response(200)
        )
        result = GocardlessMandates(sync_client).associate(2, customer_id=7)
        assert result is None
        assert json.loads(route.calls.last.request.content) == {"customer_id": 7}


class TestProAccount:
    @respx.mock
    def test_request_mandate(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/pro_account/mandate_requests").mock(
            return_value=httpx.Response(201)
        )
        result = ProAccount(sync_client).request_mandate(customer_id=7)
        assert result is None
        assert json.loads(route.calls.last.request.content) == {"customer_id": 7}

    @respx.mock
    def test_list_mandate_migrations(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/pro_account/mandate_migrations").mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [MANDATE_MIGRATION_CANDIDATE],
                    "has_more": False,
                    "next_cursor": None,
                },
            )
        )
        page = ProAccount(sync_client).list_mandate_migrations()
        candidate = page.items[0]
        assert candidate.id == 3
        assert candidate.mandate is not None
        assert candidate.mandate.type == "Mandate"

    @respx.mock
    def test_migrate_mandate(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/pro_account/mandate_migrations").mock(
            return_value=httpx.Response(201, json=MANDATE_MIGRATION)
        )
        migration = ProAccount(sync_client).migrate_mandate(
            mandate_type="Mandate", mandate_id=2
        )
        assert migration.id == 4
        body = json.loads(route.calls.last.request.content)
        assert body == {"mandate_type": "Mandate", "mandate_id": 2}

    @respx.mock
    def test_list_mandates(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/pro_account/mandates").mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [PRO_ACCOUNT_MANDATE],
                    "has_more": False,
                    "next_cursor": None,
                },
            )
        )
        page = ProAccount(sync_client).list_mandates()
        mandate = page.items[0]
        assert mandate.status == "active"
        assert mandate.active_billing_subscription is True


class TestAsyncSepaMandates:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/sepa_mandates").mock(
            return_value=httpx.Response(
                200, json={"items": [SEPA_MANDATE], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncSepaMandates(async_client).list()
        assert page.items[0].id == 1

    @respx.mock
    async def test_create(self, async_client: AsyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/sepa_mandates").mock(
            return_value=httpx.Response(201, json=SEPA_MANDATE)
        )
        mandate = await AsyncSepaMandates(async_client).create(
            bic="BNPAFRPP",
            iban="FR7630006000011234567890189",
            signed_at="2026-01-05",
            identifier="MANDATE-1",
            customer_id=7,
        )
        assert mandate.id == 1
        assert route.called

    @respx.mock
    async def test_update(self, async_client: AsyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/sepa_mandates/1").mock(
            return_value=httpx.Response(200, json=SEPA_MANDATE)
        )
        mandate = await AsyncSepaMandates(async_client).update(1, identifier="NEW-ID")
        assert mandate.id == 1

    @respx.mock
    async def test_delete(self, async_client: AsyncAPIClient) -> None:
        respx.delete(f"{BASE_URL}/sepa_mandates/1").mock(return_value=httpx.Response(204))
        result = await AsyncSepaMandates(async_client).delete(1)
        assert result is None


class TestAsyncGocardlessMandates:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/gocardless_mandates").mock(
            return_value=httpx.Response(
                200,
                json={"items": [GOCARDLESS_MANDATE], "has_more": False, "next_cursor": None},
            )
        )
        page = await AsyncGocardlessMandates(async_client).list()
        assert page.items[0].id == 2

    @respx.mock
    async def test_send_mail_request(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/gocardless_mandates/mail_requests").mock(
            return_value=httpx.Response(204)
        )
        result = await AsyncGocardlessMandates(async_client).send_mail_request(
            customer_id=7, recipients=["client@example.com"]
        )
        assert result is None

    @respx.mock
    async def test_cancel(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/gocardless_mandates/2/cancellations").mock(
            return_value=httpx.Response(204)
        )
        result = await AsyncGocardlessMandates(async_client).cancel(2)
        assert result is None

    @respx.mock
    async def test_associate(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/gocardless_mandates/2/associations").mock(
            return_value=httpx.Response(200)
        )
        result = await AsyncGocardlessMandates(async_client).associate(2, customer_id=7)
        assert result is None


class TestAsyncProAccount:
    @respx.mock
    async def test_request_mandate(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/pro_account/mandate_requests").mock(
            return_value=httpx.Response(201)
        )
        result = await AsyncProAccount(async_client).request_mandate(customer_id=7)
        assert result is None

    @respx.mock
    async def test_list_mandate_migrations(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/pro_account/mandate_migrations").mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [MANDATE_MIGRATION_CANDIDATE],
                    "has_more": False,
                    "next_cursor": None,
                },
            )
        )
        page = await AsyncProAccount(async_client).list_mandate_migrations()
        assert page.items[0].id == 3

    @respx.mock
    async def test_migrate_mandate(self, async_client: AsyncAPIClient) -> None:
        respx.post(f"{BASE_URL}/pro_account/mandate_migrations").mock(
            return_value=httpx.Response(201, json=MANDATE_MIGRATION)
        )
        migration = await AsyncProAccount(async_client).migrate_mandate(
            mandate_type="SepaMandate", mandate_id=1
        )
        assert migration.id == 4

    @respx.mock
    async def test_list_mandates(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/pro_account/mandates").mock(
            return_value=httpx.Response(
                200,
                json={"items": [PRO_ACCOUNT_MANDATE], "has_more": False, "next_cursor": None},
            )
        )
        page = await AsyncProAccount(async_client).list_mandates()
        assert page.items[0].status == "active"
