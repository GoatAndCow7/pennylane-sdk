# pennylane-sdk

> Le SDK Python non officiel pour l'API de [Pennylane](https://www.pennylane.com), la plateforme française de comptabilité et de facturation.

🇬🇧 [English version](README.md)

**[Documentation complète](https://goatandcow7.github.io/pennylane-sdk/)** (en anglais)

## Pourquoi ce SDK

- **Complet** : la totalité des opérations de l'API Entreprise v2 (165) et de l'API Cabinet v1 (48), en synchrone et en asynchrone. La couverture est vérifiée automatiquement en CI contre les spécifications OpenAPI officielles de Pennylane.
- **Typé** : chaque réponse est un modèle Pydantic. Les montants sont des `Decimal`, jamais des floats, exactement comme l'API le demande (les montants circulent en chaînes pour éviter les erreurs d'arrondi).
- **Sûr pour la compta** : l'API Pennylane n'a pas d'idempotence côté serveur. Le SDK ne réessaie donc jamais un POST après une erreur serveur : impossible de créer une facture en double à cause d'un souci réseau.
- **Anti rate-limit** : les requêtes sont cadencées côté client aux limites officielles (25 requêtes / 5 s pour les entreprises, 5/s pour les cabinets), et les 429 sont réessayés en respectant `retry-after`. Vos exports de masse passent sans effort.
- **Pagination invisible** : itérez sur un `list()` et le SDK va chercher les pages suivantes tout seul, en renvoyant vos filtres comme l'API l'exige.

> Projet communautaire, non affilié à Pennylane SAS. Sans rapport avec le framework de calcul quantique PennyLane (qui possède le nom `pennylane` sur PyPI ; ce paquet s'appelle `pennylane-sdk`).

## Installation

```bash
pip install pennylane-sdk
```

Python 3.10 ou plus récent.

## Démarrage rapide

Créez un jeton API dans Pennylane (**Paramètres > Connectivité > Développeurs**), copiez-le immédiatement (il n'est affiché qu'une fois), puis :

```bash
export PENNYLANE_API_TOKEN="votre-jeton"
```

```python
from pennylane_sdk import Pennylane, filters

client = Pennylane()

# Lister et filtrer, pagination transparente
for facture in client.customer_invoices.list(
    filter=[filters.gte("date", "2026-01-01")],
    sort="-date",
):
    print(facture.invoice_number, facture.currency_amount)

# Créer un brouillon, le finaliser, l'envoyer
facture = client.customer_invoices.create(
    customer_id=123,
    date="2026-07-08",
    deadline="2026-08-07",
    invoice_lines=[{"product_id": 45, "quantity": "2"}],
)
client.customer_invoices.finalize(facture.id)
client.customer_invoices.send_by_email(facture.id)
```

La version asynchrone offre exactement la même surface :

```python
from pennylane_sdk import AsyncPennylane

async with AsyncPennylane() as client:
    page = await client.customer_invoices.list(limit=100)
    async for facture in page:
        ...
```

## Cabinets d'expertise comptable

L'API Cabinet permet de travailler sur tout le portefeuille de dossiers clients :

```python
from pennylane_sdk import PennylaneFirm

cabinet = PennylaneFirm()  # lit PENNYLANE_FIRM_API_TOKEN

for dossier in cabinet.companies.list():
    # Balance générale du dossier sur la période
    for ligne in cabinet.trial_balance.list(
        dossier.id, period_start="2026-01-01", period_end="2026-06-30"
    ):
        print(ligne.number, ligne.debits, ligne.credits)

    # Export FEC
    export = cabinet.exports.fecs.create(
        dossier.id, period_start="2026-01-01", period_end="2026-12-31"
    )
```

## Facturation électronique (réforme 2026)

Pennylane est Plateforme Agréée (PA) : l'API couvre l'émission et la réception des factures électroniques, et le SDK aussi.

```python
# Émettre une facture via la plateforme agréée
client.customer_invoices.send_to_pa(facture.id)

# Importer une facture fournisseur Factur-X / UBL / CII
client.supplier_invoices.import_e_invoice(file="facture.xml")

# Suivre vos immatriculations PA
client.pa_registrations.list()
```

## Ce que couvre le SDK

| Domaine | Ressources |
|---|---|
| Ventes | factures clients, avoirs, devis, abonnements récurrents, clients, produits, envoi par email ou par PA |
| Achats | fournisseurs, factures fournisseurs, bons de commande, statuts de paiement |
| Banque | comptes, transactions, rapprochement avec les factures |
| Comptabilité | journaux, plan comptable, écritures, lettrage, balance, exercices |
| Analytique | catégories et axes analytiques sur factures, transactions, écritures |
| Exports | FEC, grand livre, grand livre analytique |
| Mandats | SEPA, GoCardless, compte pro |
| Synchronisation | changelogs par ressource, webhooks (bêta), OAuth 2.0 pour les apps partenaires |
| Cabinet | dossiers clients, comptabilité, GED, exports, lecture des factures |

Gestion des erreurs : une hiérarchie d'exceptions claire (`AuthenticationError`, `ValidationError` avec les détails métier, `RateLimitError` avec `retry_after`...). Voir le [guide des erreurs](https://goatandcow7.github.io/pennylane-sdk/guides/errors-and-retries/).

## Contribuer

Les contributions sont bienvenues, en anglais de préférence pour le code et les issues. Voir [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

[MIT](LICENSE). Utilisez-le librement, y compris commercialement.
