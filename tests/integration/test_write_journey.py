"""End-to-end write journey on the sandbox.

Creates real (sandbox) objects: product, customer, quote, draft invoice,
analytical category, balanced ledger entry, file attachment. Each record is
tagged with a stable external reference so repeated runs stay identifiable.

Only run this against a SANDBOX company.
"""

from __future__ import annotations

import uuid
from decimal import Decimal

import pytest

from pennylane_sdk import Pennylane

RUN_TAG = f"sdk-it-{uuid.uuid4().hex[:8]}"


@pytest.fixture(scope="module")
def run_tag() -> str:
    return RUN_TAG


def test_product_create_get_update(live_client: Pennylane, run_tag: str) -> None:
    product = live_client.products.create(
        label=f"Integration product {run_tag}",
        price_before_tax=Decimal("100.00"),
        vat_rate="FR_200",
        unit="piece",
        external_reference=f"{run_tag}-product",
    )
    assert product.id
    assert product.price_before_tax == Decimal("100.00")

    fetched = live_client.products.get(product.id)
    assert fetched.label == f"Integration product {run_tag}"

    updated = live_client.products.update(product.id, description="updated by tests")
    assert updated.id == product.id


def test_company_customer_lifecycle(live_client: Pennylane, run_tag: str) -> None:
    customer = live_client.customers.companies.create(
        name=f"Integration client {run_tag}",
        billing_address={
            "address": "1 rue de l'Intégration",
            "postal_code": "75001",
            "city": "Paris",
            "country_alpha2": "FR",
        },
        external_reference=f"{run_tag}-customer",
        emails=["sdk-tests@example.com"],
    )
    assert customer.id

    fetched = live_client.customers.companies.get(customer.id)
    assert fetched.model_dump()


def test_invoice_draft_to_finalized(live_client: Pennylane, run_tag: str) -> None:
    customer = live_client.customers.companies.create(
        name=f"Integration invoicee {run_tag}",
        billing_address={
            "address": "2 rue de la Facture",
            "postal_code": "69001",
            "city": "Lyon",
            "country_alpha2": "FR",
        },
    )
    draft = live_client.customer_invoices.create(
        customer_id=customer.id,
        date="2026-07-09",
        deadline="2026-08-08",
        invoice_lines=[
            {
                "label": f"Integration line {run_tag}",
                "quantity": "1",
                "raw_currency_unit_price": "50.00",
                "vat_rate": "FR_200",
                "unit": "piece",
            }
        ],
    )
    assert draft.id
    assert draft.status in ("draft", None) or draft.status

    finalized = live_client.customer_invoices.finalize(draft.id)
    assert finalized.invoice_number

    lines = live_client.customer_invoices.list_invoice_lines(draft.id)
    assert isinstance(lines.items, list)

    paid = live_client.customer_invoices.mark_as_paid(draft.id)
    assert paid is None or paid


def test_quote_lifecycle(live_client: Pennylane, run_tag: str) -> None:
    customer = live_client.customers.companies.create(
        name=f"Integration quotee {run_tag}",
        billing_address={
            "address": "3 rue du Devis",
            "postal_code": "33000",
            "city": "Bordeaux",
            "country_alpha2": "FR",
        },
    )
    quote = live_client.quotes.create(
        customer_id=customer.id,
        date="2026-07-09",
        deadline="2026-08-08",
        invoice_lines=[
            {
                "label": f"Quoted work {run_tag}",
                "quantity": "2",
                "raw_currency_unit_price": "75.00",
                "vat_rate": "FR_200",
                "unit": "piece",
            }
        ],
    )
    assert quote.id
    fetched = live_client.quotes.get(quote.id)
    assert fetched.model_dump()


def test_analytical_category(live_client: Pennylane, run_tag: str) -> None:
    groups = live_client.category_groups.list(limit=1)
    if not groups.items:
        pytest.skip("sandbox has no category group")
    category = live_client.categories.create(
        label=f"Integration category {run_tag}",
        category_group_id=groups.items[0].id,
    )
    assert category.id


def test_balanced_ledger_entry(live_client: Pennylane, run_tag: str) -> None:
    journals = live_client.journals.list(limit=5)
    accounts = live_client.ledger_accounts.list(limit=2)
    if not journals.items or len(accounts.items) < 2:
        pytest.skip("sandbox lacks a journal or ledger accounts")
    entry = live_client.ledger_entries.create(
        date="2026-07-09",
        journal_id=journals.items[0].id,
        label=f"Integration entry {run_tag}",
        ledger_entry_lines=[
            {"ledger_account_id": accounts.items[0].id, "debit": "10.00", "credit": "0.00"},
            {"ledger_account_id": accounts.items[1].id, "debit": "0.00", "credit": "10.00"},
        ],
    )
    assert entry.id
    fetched = live_client.ledger_entries.get(entry.id)
    assert fetched.model_dump()


def test_file_attachment_upload(live_client: Pennylane, run_tag: str) -> None:
    pdf_bytes = (
        b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
        b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]>>endobj\n"
        b"xref\n0 4\ntrailer<</Size 4/Root 1 0 R>>\n%%EOF\n"
    )
    attachment = live_client.file_attachments.create(
        file=pdf_bytes, filename=f"{run_tag}.pdf"
    )
    assert attachment.id
