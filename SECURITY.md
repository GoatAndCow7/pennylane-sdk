# Security policy

## Reporting a vulnerability

If you find a security issue in this SDK (token leakage, signature bypass, injection...), please do NOT open a public issue. Use GitHub's private vulnerability reporting on this repository ("Security" tab > "Report a vulnerability"). You will get an answer within a week.

Issues in the Pennylane API or platform itself should go to Pennylane directly (https://www.pennylane.com), not to this project.

## Scope and design notes

- The SDK never logs or serializes API tokens; they live only in the `Authorization` header.
- Webhook signatures are compared in constant time (`hmac.compare_digest`).
- OAuth refresh is serialized to avoid refresh-token-rotation races.
- Dependencies are minimal (httpx, pydantic, anyio) and pinned by a lockfile for development; the published package uses permissive ranges.

## Supported versions

Only the latest released minor version receives security fixes.
