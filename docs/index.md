# pennylane-sdk

**The unofficial Python SDK for the [Pennylane](https://www.pennylane.com) API**, the French accounting and invoicing platform used by tens of thousands of companies and accounting firms.

!!! note "Not affiliated"
    This is a community project, not affiliated with Pennylane SAS. It is also unrelated to the PennyLane quantum computing framework, which owns the `pennylane` name on PyPI. This package is `pennylane-sdk`.

## Why this SDK

- **Complete**: every operation of the Company API v2 (165 operations) and the Firm API v1 (48 operations) is implemented, in both sync and async flavors. Coverage is measured against the official OpenAPI specs by an audit script that runs in CI.
- **Typed**: every response is a Pydantic model. Monetary amounts are `Decimal`, never floats, matching the API contract (amounts travel as strings to avoid rounding errors).
- **Safe for accounting data**: the Pennylane API has no server-side idempotency, so the SDK never retries a POST after a server error. You will not create duplicate invoices because of a network hiccup.
- **Rate-limit aware**: requests are paced client-side to the official limits (25 requests per 5 seconds for companies, 5 per second for firms), and 429 responses are retried honoring `retry-after`. Bulk exports just work.
- **Pagination that disappears**: iterate over a list call and the SDK fetches the next pages for you, under the rate limit, re-sending your filters as the API requires.

## Install

```bash
pip install pennylane-sdk
```

Requires Python 3.10+.

## A taste

```python
from decimal import Decimal
from pennylane_sdk import Pennylane, filters

client = Pennylane()  # reads PENNYLANE_API_TOKEN

# Walk through every invoice since January, newest first
for invoice in client.customer_invoices.list(
    filter=[filters.gte("date", "2026-01-01")],
    sort="-date",
):
    print(invoice.invoice_number, invoice.currency_amount)

# Create and finalize an invoice
invoice = client.customer_invoices.create(
    customer_id=123,
    invoice_lines=[{"product_id": 45, "quantity": "2"}],
)
client.customer_invoices.finalize(invoice.id)
client.customer_invoices.send_by_email(invoice.id)
```

Async version, same surface:

```python
from pennylane_sdk import AsyncPennylane

async with AsyncPennylane() as client:
    page = await client.customer_invoices.list(limit=100)
    async for invoice in page:
        ...
```

Accounting firms can operate across their whole portfolio:

```python
from pennylane_sdk import PennylaneFirm

firm = PennylaneFirm()  # reads PENNYLANE_FIRM_API_TOKEN
for company in firm.companies.list():
    balance = firm.trial_balance.list(
        company.id, period_start="2026-01-01", period_end="2026-06-30"
    )
```

## Where to go next

- [Getting started](getting-started.md): tokens, first call, sandbox.
- [Guides](guides/authentication.md): authentication, pagination, error handling, invoicing lifecycle, the 2026 French e-invoicing reform, webhooks.
- [API reference](api/clients.md): every resource and model, generated from the code.
