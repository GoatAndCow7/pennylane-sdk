"""Receive Pennylane webhooks with FastAPI (pip install fastapi uvicorn).

1. Expose this app over HTTPS (e.g. behind a reverse proxy).
2. Subscribe:
     sub = client.webhook_subscriptions.create(
         callback_url="https://your.host/webhooks/pennylane",
         events=["customer_invoice.e_invoicing_status_updated"],
     )
     # STORE sub.secret NOW, it is shown only once
3. Run: uvicorn examples.webhook_receiver:app --port 8000
"""

import os

from fastapi import FastAPI, HTTPException, Request

from pennylane_sdk.webhooks import WebhookSignatureError, parse_event

SECRET = os.environ["PENNYLANE_WEBHOOK_SECRET"]

app = FastAPI()


@app.post("/webhooks/pennylane")
async def pennylane_webhook(request: Request) -> dict[str, bool]:
    raw = await request.body()  # raw bytes: never re-serialize before verifying
    # Pennylane does not document the signature header name yet (beta);
    # inspect your first deliveries and pin the right one.
    signature = request.headers.get("x-pennylane-signature", "")

    try:
        event = parse_event(raw, signature=signature, secret=SECRET)
    except WebhookSignatureError:
        raise HTTPException(status_code=400, detail="invalid signature") from None

    if event.event == "customer_invoice.e_invoicing_status_updated":
        print("e-invoicing status changed:", event.data)
    elif event.event == "dms_file.created":
        print("new document:", event.data)

    return {"ok": True}
