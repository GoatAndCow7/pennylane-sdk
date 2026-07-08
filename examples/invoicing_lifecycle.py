"""Full life of an invoice: draft, finalize, send, mark as paid.

Run with: PENNYLANE_API_TOKEN=... python examples/invoicing_lifecycle.py
(Use a sandbox: this creates real documents.)
"""

from decimal import Decimal

from pennylane_sdk import Pennylane

with Pennylane() as client:
    # A customer and a product to bill (create them if missing)
    customer = client.customers.companies.create(
        name="ACME SARL",
        reg_no="123456789",  # SIREN
        billing_address={
            "address": "1 rue de la Paix",
            "postal_code": "75002",
            "city": "Paris",
            "country_alpha2": "FR",
        },
    )
    product = client.products.create(
        label="Consulting day",
        price_before_tax=Decimal("500.00"),
        vat_rate="FR_200",
        unit="day",
    )

    # Draft with one catalog line and one free line
    draft = client.customer_invoices.create(
        customer_id=customer.id,
        date="2026-07-08",
        deadline="2026-08-07",
        invoice_lines=[
            {"product_id": product.id, "quantity": "2"},
            {
                "label": "Travel expenses",
                "quantity": "1",
                "raw_currency_unit_price": "120.00",
                "vat_rate": "FR_200",
            },
        ],
    )
    print("Draft:", draft.id, draft.status)

    # Finalize (assigns the legal invoice number, irreversible)
    invoice = client.customer_invoices.finalize(draft.id)
    print("Finalized:", invoice.invoice_number)

    # Send it
    client.customer_invoices.send_by_email(invoice.id)

    # Later: record the payment
    client.customer_invoices.mark_as_paid(invoice.id)
