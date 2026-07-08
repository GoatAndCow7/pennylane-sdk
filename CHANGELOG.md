# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-07-08

Initial release.

### Added

- Full coverage of the Pennylane **Company API v2**: 165 operations across 24 resource modules (customer and supplier invoicing, quotes, customers, products, billing subscriptions, banking, ledger, lettering, trial balance, analytics, FEC/GL/AGL exports, SEPA/GoCardless/Pro Account mandates, e-invoicing, changelogs, webhook subscriptions).
- Full coverage of the Pennylane **Firm API v1**: 48 operations (companies portfolio, accounting, DMS, exports, invoicing, banking, categories, changelogs).
- Sync (`Pennylane`, `PennylaneFirm`) and async (`AsyncPennylane`, `AsyncPennylaneFirm`) clients with identical surfaces.
- Typed Pydantic response models; monetary values as `Decimal` serialized to API-compliant strings.
- Auto-paginating cursor and page-number pages, re-sending filters across pages.
- Client-side throttling to the official rate limits, on by default.
- Conservative retry policy safe for a non-idempotent accounting API (POST never retried on 5xx).
- Defensive error parsing with a full exception hierarchy.
- Typed filter builders (`pennylane_sdk.filters`).
- OAuth 2.0 helpers with serialized refresh (Refresh Token Rotation safe).
- Webhook signature verification (constant-time HMAC) and payload parsing.
- Coverage audit script validating the SDK against the vendored official OpenAPI specs.
