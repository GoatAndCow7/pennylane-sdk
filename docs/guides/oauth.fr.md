# Applications OAuth 2.0

Vous développez une application que d'autres sociétés Pennylane pourront installer ? Pennylane prend en charge le flux standard d'autorisation par code. Demandez d'abord à Pennylane des identifiants partenaire (`client_id`, `client_secret`).

## Le flux

```python
from pennylane_sdk.oauth import OAuthApp

app = OAuthApp(
    client_id="...",
    client_secret="...",
    redirect_uri="https://yourapp.example.com/oauth/callback",
)

# 1. Envoyer l'utilisateur vers l'écran de consentement Pennylane
url = app.authorization_url(
    scopes=["customer_invoices:all", "customers:all"],
    state=anti_csrf_token,
)

# 2. Pennylane redirige avec ?code=... ; échanger ce code
tokens = app.exchange_code(code)

# 3. Utiliser le jeton d'accès comme un jeton API classique
from pennylane_sdk import Pennylane
client = Pennylane(api_token=tokens.access_token)
```

`AsyncOAuthApp` propose les mêmes méthodes sous forme de coroutines.

## Durée de vie du jeton et rafraîchissement

Les jetons d'accès vivent **24 heures** (`tokens.expires_in == 86400`). Rafraîchissez-les avant expiration :

```python
new_tokens = app.refresh(stored_refresh_token)
save(new_tokens.access_token, new_tokens.refresh_token)  # à persister IMMÉDIATEMENT
```

!!! danger "Rotation du refresh token"
    Pennylane fait tourner les refresh tokens : **chaque rafraîchissement invalide les deux jetons précédents**. Deux règles en découlent :

    1. Ne jamais lancer deux rafraîchissements en parallèle pour la même connexion. Le SDK sérialise les rafraîchissements au sein d'un même processus ; entre plusieurs processus, utilisez votre propre verrou.
    2. Persister la nouvelle paire avant de l'utiliser. Si vous plantez après le rafraîchissement mais avant la sauvegarde, le refresh token stocké est mort et l'utilisateur doit se réauthentifier.

Quand un refresh token est invalide (révoqué, remplacé par la rotation, expiré), l'endpoint de jeton répond 401 `invalid_grant` et le SDK lève `AuthenticationError` : faites repasser l'utilisateur par le flux d'autorisation.

## La migration des scopes 2026

En janvier 2026, Pennylane a remplacé le scope historique `ledger` par des scopes granulaires et a automatiquement ajouté les nouveaux scopes aux applications OAuth existantes. Si votre application a été créée avant cette date, réauthentifier vos utilisateurs une fois permet d'aligner leurs consentements sur le nouveau modèle de scopes.
