# Webhooks

!!! warning "Beta"
    Pennylane webhooks are in beta. Pennylane itself recommends keeping the [changelog endpoints](#fallback-changelogs) as a fallback while the feature stabilizes. Known event types so far: `customer_invoice.e_invoicing_status_updated` and `dms_file.created`.

## Subscribe

```python
subscription = client.webhook_subscriptions.create(
    callback_url="https://example.com/webhooks/pennylane",  # must be HTTPS
    events=["customer_invoice.e_invoicing_status_updated"],
)
print(subscription.secret)
```

!!! danger "Store the secret now"
    The `secret` used to verify deliveries is returned **only once**, at creation. Store it in your secret manager immediately; you cannot fetch it again.

Manage subscriptions with `list()`, `get(id)`, `update(id, ...)` and `delete(id)`.

## Receive and verify deliveries

Pennylane signs deliveries with an HMAC of the raw body using your secret. Verify before trusting:

```python
from fastapi import FastAPI, Header, HTTPException, Request
from pennylane_sdk.webhooks import parse_event, WebhookSignatureError

app = FastAPI()
SECRET = "..."  # from your secret manager

@app.post("/webhooks/pennylane")
async def pennylane_webhook(request: Request, x_pennylane_signature: str = Header(None)):
    raw = await request.body()   # the RAW body, do not re-serialize
    try:
        event = parse_event(raw, signature=x_pennylane_signature, secret=SECRET)
    except WebhookSignatureError:
        raise HTTPException(status_code=400, detail="bad signature")
    if event.event == "customer_invoice.e_invoicing_status_updated":
        ...
    return {"ok": True}
```

!!! note "Signature header"
    As of mid-2026 Pennylane does not document the exact signature header name or encoding. `verify_signature` is deliberately tolerant: it accepts hex and base64 HMAC-SHA256 encodings, with or without a `sha256=` prefix, compared in constant time. Inspect your first real deliveries to confirm the header (commonly `X-Pennylane-Signature`) and pin your integration accordingly.

You can also verify manually:

```python
from pennylane_sdk.webhooks import verify_signature

is_valid = verify_signature(raw_body, signature_header, SECRET)
```

## Fallback: changelogs

For guaranteed-delivery synchronization, poll the changelog endpoints. They return change events per resource, cursor-paginated, so an incremental sync loop is trivial:

```python
for event in client.changelogs.customer_invoices():
    ...  # each event references the changed invoice
```

Changelogs exist for customer invoices, supplier invoices, customers, suppliers, products, ledger entry lines, transactions and quotes.
