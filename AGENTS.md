# Guide for AI coding tools

This file helps AI assistants work with pennylane-sdk, whether using the SDK in an application or contributing to it. Everything here is also true for humans.

## What this is

`pennylane-sdk` is the unofficial Python SDK for the Pennylane API (French accounting and invoicing platform, https://www.pennylane.com). Not related to the PennyLane quantum computing framework.

- PyPI package: `pennylane-sdk`, import name: `pennylane_sdk`, Python 3.10+.
- Machine-readable docs index: https://goatandcow7.github.io/pennylane-sdk/llms.txt (full docs in one file: llms-full.txt at the same location).

## Using the SDK in an application

Entry points and their token environment variables:

| Client | API | Env var |
|---|---|---|
| `Pennylane()` / `AsyncPennylane()` | Company API v2 (one company) | `PENNYLANE_API_TOKEN` |
| `PennylaneFirm()` / `AsyncPennylaneFirm()` | Firm API v1 (accounting firms) | `PENNYLANE_FIRM_API_TOKEN` |

Ground rules the SDK enforces, which your generated code should respect:

1. Resources hang off the client: `client.customer_invoices.list()`, `client.products.create(...)`, `firm.trial_balance.list(company_id, ...)`. Firm methods take `company_id` as first positional argument.
2. Monetary values are strings in the API; pass `Decimal` or `str`, never float. Response models expose them as `Decimal`.
3. Iterating a `list()` result walks ALL pages automatically. Do not write manual pagination loops unless you need page-level control (`.items`, `.next_page()`, `.iter_pages()`).
4. Filters are built with `pennylane_sdk.filters` helpers (`filters.gte("date", "2026-01-01")`), passed as `filter=[...]`.
5. Every method docstring states the required OAuth scope and links the official reference page. Every exception derives from `pennylane_sdk.PennylaneError`.
6. The API has NO idempotency: never wrap SDK create calls in blind retry loops; the SDK already retries what is safe to retry.
7. Rate limits (Company 25 req/5s, Firm 5 req/s) are handled by the built-in throttle; do not add sleeps.

Introspection shortcuts: all response models live in `pennylane_sdk.types.company` / `pennylane_sdk.types.firm`; the package ships `py.typed`, so type checkers and IDEs see everything.

## Contributing to the SDK

Read in this order:

1. `docs/design/resource-map.md`: the binding naming and style contract.
2. `specs/company_v2.json` and `specs/firm_v1.json`: the vendored official OpenAPI specs, source of truth.
3. `scripts/show_endpoint.py`: inspect any operation's exact schema, e.g. `uv run python scripts/show_endpoint.py company "customer_invoices/{id}/finalize" put`.

Verification loop (all must pass before any change is done):

```bash
uv run pytest                             # 550+ mocked tests
uv run mypy --strict src
uv run ruff check src tests scripts
uv run python scripts/check_coverage.py   # 213/213 operations, sync + async
```

Conventions that trip up newcomers: resource methods must call `self._get/_get_page/_get_numbered_page/_post/_put/_delete` with the path as an (f-)string literal (the coverage audit parses these); response model fields are all optional except `id`; classes named `list` methods shadow the builtin, use `builtins.list` in annotations there; no em dashes anywhere in text.
