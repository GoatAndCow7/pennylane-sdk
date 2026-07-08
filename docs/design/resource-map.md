# Resource map — SDK design contract

This document is the binding naming contract between the OpenAPI specs (`specs/`) and the
SDK surface. Every implementer MUST follow it exactly so that the whole
SDK stays coherent. `scripts/check_coverage.py` audits that every spec operation appears
in both the sync and async resource classes.

## Conventions

- One module per top-level URL namespace (grouped where noted). Each module contains the
  sync class and its `Async*` twin, e.g. `CustomerInvoices` / `AsyncCustomerInvoices`.
- Standard method names: `list` (GET collection → cursor page), `get` (GET one),
  `create` (POST), `update` (PUT), `delete` (DELETE). Custom actions follow the path
  segment (`finalize`, `send_by_email`, `mark_as_paid`, `update_status`, …).
  `/import` and `/e_invoices/imports` endpoints → `import_from_file` / `import_e_invoice`.
- Sub-resource endpoint naming (`<parent_id>` is the first positional argument):
  | Endpoint pattern | Method name |
  |---|---|
  | GET `.../{id}/categories` | `list_categories(parent_id)` |
  | PUT `.../{id}/categories` | `categorize(parent_id, categories=...)` |
  | GET `.../{id}/appendices` | `list_appendices(parent_id)` |
  | POST `.../{id}/appendices` | `add_appendix(parent_id, ...)` |
  | GET `.../{id}/invoice_lines` | `list_invoice_lines(parent_id)` |
  | GET `.../{id}/invoice_line_sections` | `list_invoice_line_sections(parent_id)` |
  | GET `.../{id}/payments` | `list_payments(parent_id)` |
  | GET `.../{id}/matched_transactions` | `list_matched_transactions(parent_id)` |
  | POST `.../{id}/matched_transactions` | `match_transaction(parent_id, transaction_id)` |
  | DELETE `.../{id}/matched_transactions/{tid}` | `unmatch_transaction(parent_id, transaction_id)` |
  | GET `.../{id}/contacts` | `list_contacts(parent_id)` |
  | GET `.../{id}/custom_header_fields` | `list_custom_header_fields(parent_id)` |
- Required query parameters (e.g. `period_start` on `/trial_balance`) become required
  keyword arguments; optional ones default to ``None``.
- ``anyOf`` request bodies (e.g. draft vs finalized invoice): expose the union of the
  variants' top-level fields as optional keyword arguments and document the variants.
- Resource methods call `self._get / _get_page / _post / _put / _delete` with the path as
  an (f-)string literal starting with `/` (enforced by `scripts/check_coverage.py`).
- List endpoints return `SyncCursorPage[T]` / `AsyncCursorPage[T]` via `self._get_page`.
- Response models live in `types/company/<module>.py` or `types/firm/<module>.py`, inherit
  `PennylaneModel`, declare every spec field as optional (`field: X | None = None`) except
  `id`, and use `Money` (Decimal) for monetary string fields and `datetime.date`/`datetime`
  for date fields.
- Docstrings: English, one summary line, `Args:`/`Returns:` sections, the required OAuth
  scope, and the official reference URL (`https://pennylane.readme.io/reference/...`).
- Beta endpoints (`Hidden` tag) and deprecated endpoints are implemented and documented
  as such ("Beta — subject to change" / a `.. deprecated::` note).

## Company API (`Pennylane` / `AsyncPennylane`) — spec `specs/company_v2.json`

Base URL `https://app.pennylane.com/api/external/v2` — throttle 25 req / 5 s.

| Client attribute | Module `resources/company/` | Classes (sync) | Endpoints (path prefix) |
|---|---|---|---|
| `customers` (+ `.companies`, `.individuals` sub-resources) | `customers.py` | `Customers`, `CompanyCustomers`, `IndividualCustomers` | `/customers*`, `/company_customers*`, `/individual_customers*` |
| `customer_invoices` | `customer_invoices.py` | `CustomerInvoices` | `/customer_invoices*` (list/create/get/update/delete, `import_from_file` = `/import`, `import_e_invoice` = `/e_invoices/imports`, `send_to_pa`, `create_from_quote`, `finalize`, `mark_as_paid`, `send_by_email`, `link_credit_note`, `update_imported`, categories, appendices, invoice_lines, invoice_line_sections, payments, matched_transactions, custom_header_fields) |
| `quotes` | `quotes.py` | `Quotes` | `/quotes*` (incl. `update_status`, `send_by_email`, appendices, invoice_lines, invoice_line_sections) |
| `commercial_documents` | `commercial_documents.py` | `CommercialDocuments` | `/commercial_documents*` |
| `customer_invoice_templates` | `customer_invoice_templates.py` | `CustomerInvoiceTemplates` | `/customer_invoice_templates` |
| `products` | `products.py` | `Products` | `/products*` |
| `billing_subscriptions` | `billing_subscriptions.py` | `BillingSubscriptions` | `/billing_subscriptions*` |
| `suppliers` | `suppliers.py` | `Suppliers` | `/suppliers*` |
| `supplier_invoices` | `supplier_invoices.py` | `SupplierInvoices` | `/supplier_invoices*` (incl. `import_from_file`, `import_e_invoice`, `validate_accounting`, `update_payment_status` = `/payment_status`, `update_e_invoice_status` = `/e_invoice_status`, `link_purchase_requests` = `/linked_purchase_requests`) |
| `purchase_requests` | `purchase_requests.py` | `PurchaseRequests` | `/purchase_requests*` (`import_from_file` = `/imports`) |
| `transactions` | `transactions.py` | `Transactions` | `/transactions*` (incl. categories, matched_invoices) |
| `bank_accounts`, `bank_establishments` | `bank_accounts.py` | `BankAccounts`, `BankEstablishments` | `/bank_accounts*`, `/bank_establishments` |
| `journals` | `journals.py` | `Journals` | `/journals*` |
| `ledger_accounts` | `ledger_accounts.py` | `LedgerAccounts` | `/ledger_accounts*` |
| `ledger_entries`, `ledger_attachments` | `ledger_entries.py` | `LedgerEntries`, `LedgerAttachments` | `/ledger_entries*`, `/ledger_attachments` (deprecated) |
| `ledger_entry_lines` | `ledger_entry_lines.py` | `LedgerEntryLines` | `/ledger_entry_lines*` (incl. `letter` = POST `/lettering`, `unletter` = DELETE `/lettering`, `lettered_ledger_entry_lines`, categories) |
| `trial_balance`, `fiscal_years` | `accounting.py` | `TrialBalance`, `FiscalYears` | `/trial_balance`, `/fiscal_years` |
| `categories`, `category_groups` | `categories.py` | `Categories`, `CategoryGroups` | `/categories*`, `/category_groups*` |
| `exports` (+ `.fecs`, `.general_ledgers`, `.analytical_general_ledgers` sub-resources) | `exports.py` | `Exports`, `FecExports`, `GeneralLedgerExports`, `AnalyticalGeneralLedgerExports` | `/exports/*` |
| `sepa_mandates`, `gocardless_mandates`, `pro_account` | `mandates.py` | `SepaMandates`, `GocardlessMandates`, `ProAccount` | `/sepa_mandates*`, `/gocardless_mandates*`, `/pro_account/*` |
| `e_invoices`, `pa_registrations` | `e_invoices.py` | `EInvoices`, `PaRegistrations` | `/e-invoices/imports` (deprecated beta), `/pa_registrations` |
| `file_attachments` | `file_attachments.py` | `FileAttachments` | `/file_attachments` (multipart) |
| `changelogs` | `changelogs.py` | `Changelogs` | `/changelogs/{resource}` — one method per resource: `customer_invoices()`, `supplier_invoices()`, `customers()`, `suppliers()`, `products()`, `ledger_entry_lines()`, `transactions()`, `quotes()` |
| `webhook_subscriptions` | `webhook_subscriptions.py` | `WebhookSubscriptions` | `/webhook_subscriptions*` (beta/hidden) |
| `me` | `me.py` | `Me` | `/me` (`retrieve()`) |

## Firm API (`PennylaneFirm` / `AsyncPennylaneFirm`) — spec `specs/firm_v1.json`

Base URL `https://app.pennylane.com/api/external/firm/v1` — throttle 5 req / 1 s.
Every method takes `company_id: int` as its first positional argument, except the
`companies` resource itself.

| Client attribute | Module `resources/firm/` | Classes (sync) | Endpoints |
|---|---|---|---|
| `companies` | `companies.py` | `FirmCompanies` | `/companies`, `/companies/{id}` |
| `fiscal_years`, `trial_balance`, `journals`, `ledger_accounts`, `ledger_entries`, `ledger_entry_lines` | `accounting.py` | `FirmFiscalYears`, `FirmTrialBalance`, `FirmJournals`, `FirmLedgerAccounts`, `FirmLedgerEntries`, `FirmLedgerEntryLines` | `/companies/{company_id}/fiscal_years*`, `/trial_balance`, `/journals*`, `/ledger_accounts*`, `/ledger_entries*`, `/ledger_entry_lines*` |
| `exports` (+ `.fecs`, `.analytical_general_ledgers`) | `exports.py` | `FirmExports`, `FirmFecExports`, `FirmAnalyticalGeneralLedgerExports` | `/companies/{company_id}/exports/*` |
| `dms`, `file_attachments` | `dms.py` | `FirmDms` (`.files`, `.folders` sub-resources), `FirmFileAttachments` | `/companies/{company_id}/dms/*`, `/file_attachments` |
| `customer_invoices`, `supplier_invoices`, `customers`, `suppliers` | `invoicing.py` | `FirmCustomerInvoices`, `FirmSupplierInvoices`, `FirmCustomers`, `FirmSuppliers` | `/companies/{company_id}/customer_invoices*`, `/supplier_invoices*`, `/customers`, `/suppliers` |
| `bank_accounts`, `transactions` | `banking.py` | `FirmBankAccounts`, `FirmTransactions` | `/companies/{company_id}/bank_accounts*`, `/transactions*` |
| `categories`, `category_groups` | `categories.py` | `FirmCategories`, `FirmCategoryGroups` | `/companies/{company_id}/categories*`, `/category_groups*` |
| `changelogs` | `changelogs.py` | `FirmChangelogs` | `/companies/{company_id}/changelogs/*` — methods `dms_files()`, `ledger_entry_lines()`, `supplier_invoices()`, `customer_invoices()` |
