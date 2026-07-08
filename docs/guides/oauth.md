# OAuth 2.0 apps

Building an app that other Pennylane companies install? Pennylane supports the standard authorization-code flow. Ask Pennylane for partner credentials (`client_id`, `client_secret`) first.

## The flow

```python
from pennylane_sdk.oauth import OAuthApp

app = OAuthApp(
    client_id="...",
    client_secret="...",
    redirect_uri="https://yourapp.example.com/oauth/callback",
)

# 1. Send the user to Pennylane's consent screen
url = app.authorization_url(
    scopes=["customer_invoices:all", "customers:all"],
    state=anti_csrf_token,
)

# 2. Pennylane redirects back with ?code=...; exchange it
tokens = app.exchange_code(code)

# 3. Use the access token like a regular API token
from pennylane_sdk import Pennylane
client = Pennylane(api_token=tokens.access_token)
```

`AsyncOAuthApp` offers the same methods as coroutines.

## Token lifetime and refresh

Access tokens live **24 hours** (`tokens.expires_in == 86400`). Refresh before expiry:

```python
new_tokens = app.refresh(stored_refresh_token)
save(new_tokens.access_token, new_tokens.refresh_token)  # persist IMMEDIATELY
```

!!! danger "Refresh Token Rotation"
    Pennylane rotates refresh tokens: **every refresh invalidates both previous tokens**. Two rules follow:

    1. Never run two refreshes concurrently for the same connection. The SDK serializes refreshes within one process; across processes, use your own lock.
    2. Persist the new pair before using it. If you crash after refreshing but before saving, the stored refresh token is dead and the user must re-authorize.

When a refresh token is invalid (revoked, rotated away, expired), the token endpoint answers 401 `invalid_grant` and the SDK raises `AuthenticationError`: send the user through the authorization flow again.

## The 2026 scopes migration

In January 2026, Pennylane replaced the legacy `ledger` scope with granular scopes and auto-added the new scopes to existing OAuth apps. If your app was created before that, re-authenticating your users once ensures their consents match the new scope model.
