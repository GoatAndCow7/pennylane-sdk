# Getting started

## 1. Install the package

```bash
pip install pennylane-sdk
```

Or with uv:

```bash
uv add pennylane-sdk
```

Python 3.10 or newer is required. The SDK depends only on `httpx` and `pydantic`.

## 2. Get an API token

The SDK talks to two different Pennylane APIs, each with its own token:

**Company API** (you manage one company's accounting and invoicing):

1. Log into Pennylane with an admin account.
2. Go to **Settings > Connectivity > Developers**.
3. Create a token: give it a name, pick the permissions (read only, or read and write) and an expiration date.
4. Copy it immediately: Pennylane shows it only once.

**Firm API** (you are an accounting firm working across client companies): generate a Firm token from your firm account settings. See the [Firm API guide](guides/firm-api.md).

!!! tip "Sandbox"
    Pennylane lets you create a sandbox environment to develop against test data. See the [official getting started guide](https://pennylane.readme.io/docs/api-overview) for sandbox setup. The SDK works identically against a sandbox, including rate limits.

## 3. Configure the token

The recommended way is an environment variable, so the token never lands in your code:

```bash
export PENNYLANE_API_TOKEN="your-token"        # Company API
export PENNYLANE_FIRM_API_TOKEN="your-token"   # Firm API
```

```python
from pennylane_sdk import Pennylane

client = Pennylane()  # picks up PENNYLANE_API_TOKEN
```

You can also pass it explicitly, for instance when one process handles several companies:

```python
client = Pennylane(api_token="your-token")
```

## 4. First call

```python
me = client.me.retrieve()
print(me)
```

If the token is valid you get your company profile back. If not, the SDK raises `AuthenticationError` with the API's message.

## 5. Explore the resources

The client exposes one attribute per API resource. A few examples:

| Attribute | What it manages |
|---|---|
| `client.customer_invoices` | Sales invoices and credit notes: create, finalize, send, import PDFs and e-invoices |
| `client.quotes` | Quotes, and turning them into invoices |
| `client.customers` | Customers, with `.companies` (B2B) and `.individuals` (B2C) |
| `client.products` | Product catalog |
| `client.supplier_invoices` | Purchase invoices, imports, payment status |
| `client.transactions` | Bank transactions, matching with invoices |
| `client.ledger_entries` | Accounting entries |
| `client.ledger_entry_lines` | Entry lines, lettering (lettrage) |
| `client.trial_balance` | Trial balance (balance générale) |
| `client.exports` | FEC, general ledger and analytical exports |
| `client.changelogs` | Change feeds to sync data incrementally |

The full list is in the [API reference](api/clients.md).

## 6. Client options

```python
client = Pennylane(
    api_token=None,        # default: PENNYLANE_API_TOKEN env var
    timeout=60.0,          # seconds, or an httpx.Timeout
    max_retries=3,         # automatic retries (429, transient network errors)
    auto_throttle=True,    # pace requests to 25 per 5s so you never hit 429
    base_url=None,         # override for proxies
    http_client=None,      # bring your own httpx.Client
)
```

Use the client as a context manager (or call `client.close()`) to release connections:

```python
with Pennylane() as client:
    ...

async with AsyncPennylane() as client:
    ...
```
