# Webhooks

!!! warning "Bêta"
    Les webhooks Pennylane sont en bêta. Pennylane recommande elle-même de conserver les [endpoints changelog](#repli-changelogs) en solution de repli pendant que la fonctionnalité se stabilise. Types d'événements connus à ce jour : `customer_invoice.e_invoicing_status_updated` et `dms_file.created`.

## S'abonner

```python
subscription = client.webhook_subscriptions.create(
    callback_url="https://example.com/webhooks/pennylane",  # must be HTTPS
    events=["customer_invoice.e_invoicing_status_updated"],
)
print(subscription.secret)
```

!!! danger "Stockez le secret immédiatement"
    Le `secret` utilisé pour vérifier les livraisons n'est renvoyé **qu'une seule fois**, à la création. Stockez-le immédiatement dans votre gestionnaire de secrets ; vous ne pourrez plus le récupérer ensuite.

Gérez les abonnements avec `list()`, `get(id)`, `update(id, ...)` et `delete(id)`.

## Recevoir et vérifier les livraisons

Pennylane signe les livraisons avec un HMAC du corps brut à l'aide de votre secret. Vérifiez avant de faire confiance :

```python
from fastapi import FastAPI, Header, HTTPException, Request
from pennylane_sdk.webhooks import parse_event, WebhookSignatureError

app = FastAPI()
SECRET = "..."  # from your secret manager

@app.post("/webhooks/pennylane")
async def pennylane_webhook(request: Request, x_pennylane_signature: str = Header(None)):
    raw = await request.body()   # le corps BRUT, ne pas le re-sérialiser
    try:
        event = parse_event(raw, signature=x_pennylane_signature, secret=SECRET)
    except WebhookSignatureError:
        raise HTTPException(status_code=400, detail="bad signature")
    if event.event == "customer_invoice.e_invoicing_status_updated":
        ...
    return {"ok": True}
```

!!! note "En-tête de signature"
    À la mi-2026, Pennylane ne documente pas encore précisément le nom ni l'encodage de l'en-tête de signature. `verify_signature` est volontairement tolérant : il accepte les encodages HMAC-SHA256 en hexadécimal comme en base64, avec ou sans préfixe `sha256=`, comparés en temps constant. Inspectez vos premières livraisons réelles pour confirmer l'en-tête (généralement `X-Pennylane-Signature`) et figez votre intégration en conséquence.

Vous pouvez aussi vérifier manuellement :

```python
from pennylane_sdk.webhooks import verify_signature

is_valid = verify_signature(raw_body, signature_header, SECRET)
```

## Repli : changelogs

Pour une synchronisation à livraison garantie, interrogez les endpoints changelog. Ils renvoient des événements de changement par ressource, paginés par curseur, ce qui rend triviale une boucle de synchronisation incrémentale :

```python
for event in client.changelogs.customer_invoices():
    ...  # chaque événement référence la facture modifiée
```

Des changelogs existent pour les factures clients, les factures fournisseurs, les clients, les fournisseurs, les produits, les lignes d'écriture, les transactions et les devis.
