# Authentification

Pennylane prend en charge trois modes d'authentification. Tous se traduisent par un jeton `Bearer` dans l'en-tête `Authorization`, que le SDK définit pour vous.

## Jeton Company API

Pour les intégrations qui gèrent une seule société (le cas le plus courant).

Créé dans **Paramètres > Connectivité > Développeurs** par un administrateur de la société. Les jetons portent :

- un ensemble de **scopes** (permissions) : lecture seule, ou lecture et écriture, par domaine de ressources ;
- une **date d'expiration** : anticipez le renouvellement, un jeton expiré déclenche une `AuthenticationError`.

```python
from pennylane_sdk import Pennylane

client = Pennylane()                      # variable d'environnement PENNYLANE_API_TOKEN
client = Pennylane(api_token="tok...")    # explicite
```

## Jeton Firm API

Pour les cabinets d'expertise comptable opérant sur l'ensemble de leur portefeuille de dossiers clients. Généré depuis le compte cabinet, sans besoin de bac à sable. Utilisez les clients dédiés :

```python
from pennylane_sdk import PennylaneFirm

firm = PennylaneFirm()                    # variable d'environnement PENNYLANE_FIRM_API_TOKEN
```

Les jetons Firm et Company ne sont pas interchangeables : ils s'authentifient sur des URL de base différentes, avec des scopes différents.

## OAuth 2.0 (applications partenaires)

Si vous développez une application que d'autres sociétés Pennylane installent, utilisez le flux authorization-code. Le SDK fournit des fonctions d'aide pour tout le processus, voir le [guide OAuth](oauth.md).

Une fois un jeton d'accès obtenu, utilisez-le comme un jeton de société :

```python
client = Pennylane(api_token=tokens.access_token)
```

## Scopes

Chaque endpoint requiert un scope, documenté dans la docstring de chaque méthode du SDK (par exemple `customer_invoices:all` pour créer des factures, `customer_invoices:readonly` pour les lister). Lorsque le jeton n'a pas le scope requis, l'API répond 403 et le SDK lève une `PermissionDeniedError` dont le message précise le scope manquant :

```text
pennylane_sdk.PermissionDeniedError: Missing scope: customer_invoices:all
```

Principaux scopes v2 : `customers`, `products`, `customer_invoices`, `quotes`, `customer_mandates`, `billing_subscriptions`, `commercial_documents`, `suppliers`, `supplier_invoices`, `purchase_requests`, `journals`, `ledger_accounts`, `ledger_entries`, `categories`, `transactions`, `bank_accounts`, `file_attachments` (chacun en `:readonly` ou `:all`), ainsi que `trial_balance:readonly`, `fiscal_years:readonly`, `bank_establishments:readonly` et `exports:fec`, `exports:agl`, `exports:gl`.

## Bonnes pratiques

- Ne committez jamais un jeton. Utilisez des variables d'environnement ou un gestionnaire de secrets.
- Privilégiez les jetons en lecture seule pour les intégrations de reporting.
- Donnez à chaque intégration son propre jeton, afin de pouvoir en révoquer un sans casser les autres, et pour que le budget de `ratelimit` (attribué par jeton) ne soit pas partagé.
