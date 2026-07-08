# Bien démarrer

## 1. Installer le paquet

```bash
pip install pennylane-sdk
```

Ou avec uv :

```bash
uv add pennylane-sdk
```

Python 3.10 ou supérieur est requis. Le SDK ne dépend que de `httpx` et `pydantic`.

## 2. Obtenir un jeton d'API

Le SDK dialogue avec deux API Pennylane distinctes, chacune avec son propre jeton :

**Company API** (vous gérez la comptabilité et la facturation d'une seule société) :

1. Connectez-vous à Pennylane avec un compte administrateur.
2. Allez dans **Paramètres > Connectivité > Développeurs**.
3. Créez un jeton : donnez-lui un nom, choisissez les permissions (lecture seule, ou lecture et écriture) et une date d'expiration.
4. Copiez-le immédiatement : Pennylane ne l'affiche qu'une seule fois.

**Firm API** (vous êtes un cabinet d'expertise comptable travaillant sur plusieurs dossiers clients) : générez un jeton Firm depuis les paramètres de votre compte cabinet. Voir le [guide Firm API](guides/firm-api.md).

!!! tip "Bac à sable"
    Pennylane vous permet de créer un environnement de bac à sable pour développer avec des données de test. Voir le [guide officiel de démarrage](https://pennylane.readme.io/docs/api-overview) pour la configuration du bac à sable. Le SDK fonctionne à l'identique face à un bac à sable, limites de débit comprises.

## 3. Configurer le jeton

La méthode recommandée est une variable d'environnement, pour que le jeton ne se retrouve jamais dans votre code :

```bash
export PENNYLANE_API_TOKEN="your-token"        # Company API
export PENNYLANE_FIRM_API_TOKEN="your-token"   # Firm API
```

```python
from pennylane_sdk import Pennylane

client = Pennylane()  # récupère PENNYLANE_API_TOKEN
```

Vous pouvez aussi le passer explicitement, par exemple lorsqu'un même processus gère plusieurs sociétés :

```python
client = Pennylane(api_token="your-token")
```

## 4. Premier appel

```python
me = client.me.retrieve()
print(me)
```

Si le jeton est valide, vous récupérez le profil de votre société. Sinon, le SDK lève une `AuthenticationError` avec le message de l'API.

## 5. Explorer les ressources

Le client expose un attribut par ressource de l'API. Quelques exemples :

| Attribut | Ce qu'il gère |
|---|---|
| `client.customer_invoices` | Factures de vente et avoirs : création, finalisation, envoi, import de PDF et de factures électroniques |
| `client.quotes` | Devis, et leur transformation en factures |
| `client.customers` | Clients, avec `.companies` (B2B) et `.individuals` (B2C) |
| `client.products` | Catalogue produits |
| `client.supplier_invoices` | Factures d'achat, imports, statut de paiement |
| `client.transactions` | Transactions bancaires, rapprochement avec les factures |
| `client.ledger_entries` | Écritures comptables |
| `client.ledger_entry_lines` | Lignes d'écriture, lettrage |
| `client.trial_balance` | Balance générale |
| `client.exports` | Exports FEC, grand livre et analytiques |
| `client.changelogs` | Flux de modifications pour synchroniser les données de façon incrémentale |

La liste complète se trouve dans la [référence de l'API](api/clients.md).

## 6. Options du client

```python
client = Pennylane(
    api_token=None,        # par défaut : variable d'environnement PENNYLANE_API_TOKEN
    timeout=60.0,          # secondes, ou un httpx.Timeout
    max_retries=3,         # nouvelles tentatives automatiques (429, erreurs réseau transitoires)
    auto_throttle=True,    # cadence les requêtes à 25 par 5s pour ne jamais atteindre 429
    base_url=None,         # à surcharger pour les proxys
    http_client=None,      # utilisez votre propre httpx.Client
)
```

Utilisez le client comme gestionnaire de contexte (ou appelez `client.close()`) pour libérer les connexions :

```python
with Pennylane() as client:
    ...

async with AsyncPennylane() as client:
    ...
```
