# Pagination et filtrage

## Pagination par curseur (presque partout)

Les endpoints de liste renvoient un objet page. La façon la plus simple de l'utiliser : itérer, et laisser le SDK récupérer les pages suivantes de façon paresseuse, sous la régulation de débit du client.

```python
for invoice in client.customer_invoices.list(limit=100):
    ...  # parcourt TOUTES les pages de façon transparente
```

Version asynchrone :

```python
page = await client.customer_invoices.list(limit=100)
async for invoice in page:
    ...
```

Pour contrôler les pages vous-même :

```python
page = client.customer_invoices.list(limit=100)
page.items        # éléments de la page courante uniquement
page.has_more     # indique si une page suivante existe
page.next_cursor  # curseur opaque pour la page suivante
next_page = page.next_page()        # ou None sur la dernière page

for page in page.iter_pages():      # page par page
    print(len(page.items))
```

`limit` accepte des valeurs de 1 à 100 (la valeur par défaut de l'API est 20). Moins de requêtes avec `limit=100` signifie des lectures en masse plus rapides sous la limite de débit.

!!! warning "Les filtres ne sont pas encodés dans le curseur"
    Lorsque vous paginez une requête filtrée, l'API exige le même `filter` et le même `sort` à chaque requête de page. Le SDK s'en charge pour vous dans `next_page()` et pendant l'itération.

## Pagination par numéro de page (quelques endpoints Firm)

Trois endpoints de la Firm API (`companies`, `fiscal_years`, `trial_balance`) paginent avec `page` et `per_page` plutôt qu'avec un curseur. L'expérience reste la même :

```python
for company in firm.companies.list(per_page=50):
    ...
```

Ces endpoints renvoient des `SyncNumberedPage` / `AsyncNumberedPage`, avec les attributs `total_pages` et `current_page`.

## Filtrage { #filtering }

Le paramètre `filter` est un tableau JSON de conditions. Construisez-le avec les fonctions d'aide typées :

```python
from pennylane_sdk import filters

client.customer_invoices.list(
    filter=[
        filters.gte("date", "2026-01-01"),
        filters.lt("date", "2026-07-01"),
        filters.eq("status", "upcoming"),
        filters.in_("customer_id", [42, 43]),
    ],
)
```

Fonctions disponibles : `eq`, `not_eq`, `lt`, `lte`, `gt`, `gte`, `in_`, `not_in`, et `where(field, operator, value)` pour tout le reste. Les valeurs peuvent être des chaînes, des nombres, des `Decimal`, des `date` ou `datetime` (encodées automatiquement).

Les champs et opérateurs pris en charge par chaque endpoint sont listés dans la [référence officielle](https://pennylane.readme.io/reference), endpoint par endpoint.

Vous pouvez aussi passer une chaîne JSON brute si vous en avez déjà une ; le SDK l'envoie telle quelle.

## Tri

```python
client.customer_invoices.list(sort="-date")   # par date décroissante
client.customer_invoices.list(sort="id")      # par id croissant
```

Depuis les évolutions de l'API de 2026, le tri par défaut est `-id` (les plus récents en premier) sur tous les endpoints.

## Chargement conjoint avec include

Certains endpoints de liste prennent en charge un paramètre expérimental `include` pour intégrer des enregistrements liés en un seul appel :

```python
page = client.customer_invoices.list(include="invoice_lines")
page.included   # liste brute des enregistrements chargés conjointement
```
