# pennylane-sdk

**Le SDK Python non officiel pour l'API [Pennylane](https://www.pennylane.com)**, la plateforme française de comptabilité et de facturation utilisée par des dizaines de milliers d'entreprises et de cabinets d'expertise comptable.

!!! note "Non affilié"
    Ce projet est communautaire, il n'est pas affilié à Pennylane SAS. Il n'a également aucun rapport avec le framework de calcul quantique PennyLane, qui possède le nom `pennylane` sur PyPI. Ce paquet s'appelle `pennylane-sdk`.

## Pourquoi ce SDK

- **Complet** : chaque opération de la Company API v2 (165 opérations) et de la Firm API v1 (48 opérations) est implémentée, en version synchrone comme asynchrone. La couverture est mesurée par rapport aux spécifications OpenAPI officielles grâce à un script d'audit exécuté en CI.
- **Typé** : chaque réponse est un modèle Pydantic. Les montants monétaires sont des `Decimal`, jamais des flottants, conformément au contrat de l'API (les montants transitent sous forme de chaînes pour éviter les erreurs d'arrondi).
- **Sûr pour les données comptables** : l'API Pennylane n'offre pas d'idempotence côté serveur, le SDK ne retente donc jamais un POST après une erreur serveur. Vous ne créerez pas de facture en double à cause d'un incident réseau.
- **Conscient des limites de débit** : les requêtes sont cadencées côté client selon les limites officielles (25 requêtes par 5 secondes pour les dossiers clients, 5 par seconde pour les cabinets), et les réponses 429 sont retentées en respectant `retry-after`. Les exports en masse fonctionnent sans effort.
- **Une pagination qui s'efface** : parcourez un appel de liste et le SDK récupère les pages suivantes pour vous, sous la limite de débit, en renvoyant vos filtres comme l'exige l'API.

## Installation

```bash
pip install pennylane-sdk
```

Nécessite Python 3.10 ou supérieur.

## Un aperçu

```python
from decimal import Decimal
from pennylane_sdk import Pennylane, filters

client = Pennylane()  # lit PENNYLANE_API_TOKEN

# Parcourt toutes les factures depuis janvier, les plus récentes en premier
for invoice in client.customer_invoices.list(
    filter=[filters.gte("date", "2026-01-01")],
    sort="-date",
):
    print(invoice.invoice_number, invoice.currency_amount)

# Crée et finalise une facture
invoice = client.customer_invoices.create(
    customer_id=123,
    date="2026-07-08",
    deadline="2026-08-07",
    invoice_lines=[{"product_id": 45, "quantity": "2"}],
)
client.customer_invoices.finalize(invoice.id)
client.customer_invoices.send_by_email(invoice.id)
```

Version asynchrone, même interface :

```python
from pennylane_sdk import AsyncPennylane

async with AsyncPennylane() as client:
    page = await client.customer_invoices.list(limit=100)
    async for invoice in page:
        ...
```

Les cabinets d'expertise comptable peuvent opérer sur l'ensemble de leur portefeuille de dossiers clients :

```python
from pennylane_sdk import PennylaneFirm

firm = PennylaneFirm()  # lit PENNYLANE_FIRM_API_TOKEN
for company in firm.companies.list():
    balance = firm.trial_balance.list(
        company.id, period_start="2026-01-01", period_end="2026-06-30"
    )
```

## Pour aller plus loin

- [Bien démarrer](getting-started.md) : jetons, premier appel, bac à sable.
- [Guides](guides/authentication.md) : authentification, pagination, gestion des erreurs, cycle de vie de la facturation, la réforme de la facturation électronique de 2026, webhooks.
- [Référence de l'API](api/clients.md) : chaque ressource et chaque modèle, générés à partir du code.
