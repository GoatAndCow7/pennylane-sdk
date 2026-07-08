# Accounting operations

Beyond invoicing, the API exposes the accounting core: journals, chart of accounts, entries, lettering, trial balance and legal exports.

## Chart of accounts and journals

```python
# Chart of accounts (plan comptable)
for account in client.ledger_accounts.list():
    print(account.number, account.label)

client.ledger_accounts.create(number="706100", label="Prestations de services")

# Journals
for journal in client.journals.list():
    print(journal.code, journal.label)
```

## Ledger entries (écritures)

An entry is a balanced set of debit/credit lines:

```python
from decimal import Decimal

entry = client.ledger_entries.create(
    date="2026-07-08",
    journal_id=12,
    label="Vente prestation",
    ledger_entry_lines=[
        {"ledger_account_id": 411, "debit": Decimal("120.00")},
        {"ledger_account_id": 706, "credit": Decimal("100.00")},
        {"ledger_account_id": 445, "credit": Decimal("20.00")},
    ],
)
```

If the lines do not balance, the API answers 422 and the SDK raises `ValidationError` with the totals in `err.details`.

!!! warning "No idempotency on creations"
    Posting the same entry twice creates a duplicate: the API does not deduplicate. The SDK never auto-retries a POST after a server error for this reason. Deduplicate on your side if your pipeline can replay.

## Lettering (lettrage)

Lettering links entry lines that settle each other, typically an invoice line with its payment line:

```python
client.ledger_entry_lines.letter(ledger_entry_line_ids=[111, 222])
client.ledger_entry_lines.unletter(ledger_entry_line_ids=[111, 222])
client.ledger_entry_lines.list_lettered_lines(111)
```

## Trial balance (balance générale)

```python
for row in client.trial_balance.list(
    period_start="2026-01-01",
    period_end="2026-06-30",
):
    print(row.number, row.debits, row.credits)
```

## Analytical categories

Pennylane's analytics let you tag almost everything (invoices, transactions, entry lines) with categories organized in groups (axes):

```python
groups = client.category_groups.list()
client.categories.create(label="Agence Lyon", category_group_id=3)

client.customer_invoices.categorize(
    invoice_id,
    categories=[{"id": 42, "weight": "1.0"}],
)
```

## Legal exports: FEC, general ledger

Exports run asynchronously: create the export, then poll until the file is ready.

```python
import time

export = client.exports.fecs.create(fiscal_year_id=7)
while export.status not in ("done", "failed"):
    time.sleep(5)
    export = client.exports.fecs.get(export.id)
print(export.url)   # download link
```

Same pattern for `client.exports.general_ledgers` and `client.exports.analytical_general_ledgers`.

## Bank data

```python
for account in client.bank_accounts.list():
    ...

for tx in client.transactions.list(filter=[filters.gte("date", "2026-01-01")]):
    ...

# Reconcile: which invoices does this transaction settle?
client.transactions.list_matched_invoices(tx.id)
```
