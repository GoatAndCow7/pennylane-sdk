# Errors, retries and rate limits

## Exception hierarchy

Everything the SDK raises derives from `PennylaneError`:

```text
PennylaneError
├── APIConnectionError          the request never got an HTTP response
│   └── APITimeoutError
└── APIStatusError              the API answered 4xx/5xx
    ├── BadRequestError         400  malformed JSON, wrong types
    ├── AuthenticationError     401  missing/invalid/expired token
    ├── PermissionDeniedError   403  missing scope
    ├── NotFoundError           404
    ├── ConflictError           409  e.g. duplicate document
    ├── ValidationError         422  business validation failed
    ├── RateLimitError          429  includes .retry_after
    └── ServerError             5xx
```

Every `APIStatusError` carries:

- `status_code`: the HTTP status;
- `error_code`: the machine-readable `error` field when the API sends one (e.g. `"unprocessable_entity"`);
- `message`: the best human-readable message available;
- `details`: structured details when present (e.g. which totals do not balance);
- `body` and `response`: the raw payload and `httpx.Response` for anything else.

```python
from pennylane_sdk import Pennylane, ValidationError

try:
    client.ledger_entries.create(...)
except ValidationError as err:
    print(err.message)   # "Entry lines are not balanced"
    print(err.details)   # {"debit_total": "100.00", "credit_total": "80.00"}
```

!!! info "Why every field is optional"
    The API's error body format varies by endpoint (sometimes `{error, message, details}`, sometimes `{error, status}`). The SDK parses defensively so you always get the most information available.

## Automatic retries

The SDK retries transparently, with exponential backoff and jitter, up to `max_retries` times (3 by default). The policy is deliberately conservative because **the Pennylane API has no server-side idempotency**: re-sending a create request that the server may have already processed could produce a duplicate invoice or ledger entry.

| Situation | GET / PUT / DELETE | POST |
|---|---|---|
| 429 rate limited | retried (honors `retry-after`) | retried (the request was rejected unprocessed, safe) |
| 500 / 502 / 503 / 504 | retried | **not retried** (duplicate risk) |
| Connection failed before sending | retried | retried |
| Timeout / connection lost after sending | retried | **not retried** |

If you need at-least-once semantics on creations, deduplicate on your side (for instance with `external_reference` fields) as Pennylane officially recommends.

## Rate limits

| API | Limit |
|---|---|
| Company API v2 | 25 requests per 5 seconds, per token |
| Firm API v1 | 5 requests per second |

Two layers keep you safe:

1. **Client-side throttle** (`auto_throttle=True` by default): requests are paced so bursts, auto-pagination and mass imports stay under the limit. Disable with `Pennylane(auto_throttle=False)` if you orchestrate limits yourself.
2. **429 handling**: if a 429 still happens (e.g. several processes sharing one token), the SDK waits for `retry-after` and retries, for every HTTP method.

The API reports the remaining budget on every response; the SDK exposes the latest values:

```python
client.me.retrieve()
info = client.last_rate_limit
print(info.limit, info.remaining, info.reset)  # 25 24 1751980800
```

!!! tip "One token per integration"
    Limits apply per token. Give each integration its own token and they will not starve each other.
