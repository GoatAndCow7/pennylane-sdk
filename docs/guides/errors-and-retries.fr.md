# Erreurs, nouvelles tentatives et limites de débit

## Hiérarchie des exceptions

Tout ce que le SDK lève dérive de `PennylaneError` :

```text
PennylaneError
├── APIConnectionError          la requête n'a jamais reçu de réponse HTTP
│   └── APITimeoutError
└── APIStatusError              l'API a répondu 4xx/5xx
    ├── BadRequestError         400  JSON malformé, mauvais types
    ├── AuthenticationError     401  jeton manquant/invalide/expiré
    ├── PermissionDeniedError   403  scope manquant
    ├── NotFoundError           404
    ├── ConflictError           409  ex. document en doublon
    ├── ValidationError         422  échec de validation métier
    ├── RateLimitError          429  inclut .retry_after
    └── ServerError             5xx
```

Chaque `APIStatusError` porte :

- `status_code` : le statut HTTP ;
- `error_code` : le champ `error` exploitable par un programme, quand l'API en envoie un (ex. `"unprocessable_entity"`) ;
- `message` : le meilleur message lisible disponible ;
- `details` : des détails structurés lorsqu'ils existent (ex. quels totaux ne s'équilibrent pas) ;
- `body` et `response` : la charge utile brute et l'objet `httpx.Response` pour tout le reste.

```python
from pennylane_sdk import Pennylane, ValidationError

try:
    client.ledger_entries.create(...)
except ValidationError as err:
    print(err.message)   # "Entry lines are not balanced"
    print(err.details)   # {"debit_total": "100.00", "credit_total": "80.00"}
```

!!! info "Pourquoi chaque champ est optionnel"
    Le format du corps d'erreur de l'API varie selon l'endpoint (parfois `{error, message, details}`, parfois `{error, status}`). Le SDK analyse la réponse de façon défensive afin de toujours vous fournir le maximum d'informations disponibles.

## Nouvelles tentatives automatiques

Le SDK relance les requêtes de façon transparente, avec un backoff exponentiel et du jitter, jusqu'à `max_retries` fois (3 par défaut). Cette politique est volontairement prudente car **l'API Pennylane n'a pas d'idempotence côté serveur** : renvoyer une requête de création que le serveur a peut-être déjà traitée pourrait produire une facture ou une écriture comptable en double.

| Situation | GET / PUT / DELETE | POST |
|---|---|---|
| 429 limite de débit atteinte | nouvelle tentative (respecte `retry-after`) | nouvelle tentative (la requête a été rejetée sans être traitée, sans risque) |
| 500 / 502 / 503 / 504 | nouvelle tentative | **pas de nouvelle tentative** (risque de doublon) |
| Échec de connexion avant envoi | nouvelle tentative | nouvelle tentative |
| Timeout / connexion perdue après envoi | nouvelle tentative | **pas de nouvelle tentative** |

Si vous avez besoin d'une sémantique "au moins une fois" sur les créations, dédupliquez de votre côté (par exemple avec des champs `external_reference`), comme Pennylane le recommande officiellement.

## Limites de débit

| API | Limite |
|---|---|
| Company API v2 | 25 requêtes par 5 secondes, par jeton |
| Firm API v1 | 5 requêtes par seconde |

Deux niveaux vous protègent :

1. **Régulation de débit côté client** (`auto_throttle=True` par défaut) : les requêtes sont cadencées pour que les pics, la pagination automatique et les imports massifs restent sous la limite. Désactivez avec `Pennylane(auto_throttle=False)` si vous gérez vous-même l'orchestration des limites.
2. **Gestion des 429** : si un 429 survient malgré tout (par exemple plusieurs processus partageant un même jeton), le SDK attend le délai indiqué par `retry-after` puis relance la requête, quelle que soit la méthode HTTP.

L'API indique le budget restant à chaque réponse ; le SDK expose les dernières valeurs :

```python
client.me.retrieve()
info = client.last_rate_limit
print(info.limit, info.remaining, info.reset)  # 25 24 1751980800
```

!!! tip "Un jeton par intégration"
    Les limites s'appliquent par jeton. Attribuez à chaque intégration son propre jeton afin qu'elles ne se privent pas mutuellement de quota.
