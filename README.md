# pennylane-sdk

> The unofficial Python SDK for the [Pennylane](https://www.pennylane.com) API, the French accounting and invoicing platform.

🇫🇷 [Version française](README.fr.md)

[![CI](https://github.com/GoatAndCow7/pennylane-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/GoatAndCow7/pennylane-sdk/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/pennylane-sdk)](https://pypi.org/project/pennylane-sdk/)
[![Python](https://img.shields.io/pypi/pyversions/pennylane-sdk)](https://pypi.org/project/pennylane-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-teal.svg)](LICENSE)

**[Documentation](https://goatandcow7.github.io/pennylane-sdk/)** | [API coverage: 213/213 operations](#complete-api-coverage)

- **Complete**: every operation of the Company API v2 (165) and the Firm API v1 (48), in sync and async, audited against the official OpenAPI specs in CI.
- **Typed**: Pydantic models everywhere; monetary amounts are `Decimal`, never floats.
- **Safe for accounting**: the API has no idempotency, so POST is never retried after a server error. No duplicate invoices from a network hiccup.
- **Rate-limit proof**: built-in client-side throttling to the official limits, plus `retry-after` aware retries on 429.
- **Effortless pagination**: iterate a list call, the SDK fetches the pages.

> Not affiliated with Pennylane SAS. Unrelated to the PennyLane quantum computing framework (which owns `pennylane` on PyPI; this package is `pennylane-sdk`).

## Install

```bash
pip install pennylane-sdk
```

Python 3.10+.

## Quickstart

Create an API token in Pennylane (**Settings > Connectivity > Developers**), then:

```python
from pennylane_sdk import Pennylane, filters

client = Pennylane()  # reads PENNYLANE_API_TOKEN

# List and filter, with transparent pagination
for invoice in client.customer_invoices.list(
    filter=[filters.gte("date", "2026-01-01")],
    sort="-date",
):
    print(invoice.invoice_number, invoice.currency_amount)

# Create, finalize, send
invoice = client.customer_invoices.create(
    customer_id=123,
    date="2026-07-08",
    deadline="2026-08-07",
    invoice_lines=[{"product_id": 45, "quantity": "2"}],
)
client.customer_invoices.finalize(invoice.id)
client.customer_invoices.send_by_email(invoice.id)
```

Async, same surface:

```python
from pennylane_sdk import AsyncPennylane

async with AsyncPennylane() as client:
    page = await client.customer_invoices.list(limit=100)
    async for invoice in page:
        ...
```

Accounting firms, across the whole portfolio:

```python
from pennylane_sdk import PennylaneFirm

firm = PennylaneFirm()  # reads PENNYLANE_FIRM_API_TOKEN
for company in firm.companies.list():
    for row in firm.trial_balance.list(
        company.id, period_start="2026-01-01", period_end="2026-06-30"
    ):
        ...
```

French e-invoicing (2026 reform), Pennylane being an accredited Plateforme Agréée:

```python
client.customer_invoices.send_to_pa(invoice.id)                  # emit through the PA
client.supplier_invoices.import_e_invoice(file="factur-x.pdf")   # ingest Factur-X/UBL/CII
```

## Complete API coverage

| API | Operations | Resources |
|---|---|---|
| Company v2 | 165/165 | customer and supplier invoices, quotes, customers, products, billing subscriptions, banking and reconciliation, journals, ledger entries, lettering, trial balance, analytics, FEC/GL/AGL exports, SEPA/GoCardless/Pro mandates, e-invoicing, changelogs, webhooks |
| Firm v1 | 48/48 | client portfolio, accounting, DMS, exports, invoicing (read), banking, analytics, changelogs |

Coverage is not a promise: `scripts/check_coverage.py` verifies in CI that every operation in the vendored official OpenAPI specs exists in both the sync and async clients.

## Learn more

- [Getting started](https://goatandcow7.github.io/pennylane-sdk/getting-started/)
- [Guides](https://goatandcow7.github.io/pennylane-sdk/guides/authentication/): authentication, pagination and filtering, errors and retries, invoicing lifecycle, e-invoicing 2026, accounting, Firm API, webhooks, OAuth apps
- [API reference](https://goatandcow7.github.io/pennylane-sdk/api/clients/)
- [Examples](examples/)
- [Contributing](CONTRIBUTING.md)

## License

[MIT](LICENSE). Build whatever you want with it.
