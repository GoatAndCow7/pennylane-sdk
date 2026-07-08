"""Smallest possible tour: who am I, list some data.

Run with: PENNYLANE_API_TOKEN=... python examples/quickstart.py
"""

from pennylane_sdk import Pennylane, filters

with Pennylane() as client:
    # Authenticated profile
    me = client.me.retrieve()
    print("Connected:", me)

    # Ten most recent finalized invoices of 2026
    page = client.customer_invoices.list(
        filter=[filters.gte("date", "2026-01-01")],
        sort="-date",
        limit=10,
    )
    for invoice in page.items:
        print(invoice.invoice_number, invoice.date, invoice.currency_amount)

    # Rate limit budget left on this token
    print("Rate limit:", client.last_rate_limit)
