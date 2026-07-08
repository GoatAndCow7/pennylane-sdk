# Authentication

Pennylane supports three authentication modes. All of them end up as a `Bearer` token in the `Authorization` header, which the SDK sets for you.

## Company API token

For integrations that manage a single company (the most common case).

Created in **Settings > Connectivity > Developers** by a company admin. Tokens carry:

- a set of **scopes** (permissions): read only, or read and write, per resource domain;
- an **expiration date**: plan the renewal, an expired token raises `AuthenticationError`.

```python
from pennylane_sdk import Pennylane

client = Pennylane()                      # PENNYLANE_API_TOKEN env var
client = Pennylane(api_token="tok...")    # explicit
```

## Firm API token

For accounting firms operating across their client portfolio. Generated from the firm account, no sandbox needed. Use the dedicated clients:

```python
from pennylane_sdk import PennylaneFirm

firm = PennylaneFirm()                    # PENNYLANE_FIRM_API_TOKEN env var
```

The Firm and Company tokens are not interchangeable: they authenticate against different base URLs with different scopes.

## OAuth 2.0 (partner apps)

If you build an app that other Pennylane companies install, use the authorization-code flow. The SDK ships helpers for the whole dance, see the [OAuth guide](oauth.md).

Once you hold an access token, use it like a company token:

```python
client = Pennylane(api_token=tokens.access_token)
```

## Scopes

Each endpoint requires a scope, documented in every SDK method docstring (for example `customer_invoices:all` to create invoices, `customer_invoices:readonly` to list them). When the token lacks the scope, the API answers 403 and the SDK raises `PermissionDeniedError` whose message names the missing scope:

```text
pennylane_sdk.PermissionDeniedError: Missing scope: customer_invoices:all
```

Main v2 scopes: `customers`, `products`, `customer_invoices`, `quotes`, `customer_mandates`, `billing_subscriptions`, `commercial_documents`, `suppliers`, `supplier_invoices`, `purchase_requests`, `journals`, `ledger_accounts`, `ledger_entries`, `categories`, `transactions`, `bank_accounts`, `file_attachments` (each as `:readonly` or `:all`), plus `trial_balance:readonly`, `fiscal_years:readonly`, `bank_establishments:readonly` and `exports:fec`, `exports:agl`, `exports:gl`.

## Good practices

- Never commit a token. Use environment variables or a secret manager.
- Prefer read-only tokens for reporting integrations.
- Give each integration its own token, so you can revoke one without breaking the others, and so the `ratelimit` budget (which is per token) is not shared.
