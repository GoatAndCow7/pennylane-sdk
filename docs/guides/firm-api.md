# Firm API (accounting firms)

Accounting firms (cabinets d'expertise comptable) get a dedicated API to work across their whole client portfolio: list the companies they manage, read and post accounting entries, upload documents, run exports, all per client company.

## Clients and token

```python
from pennylane_sdk import PennylaneFirm, AsyncPennylaneFirm

firm = PennylaneFirm()   # reads PENNYLANE_FIRM_API_TOKEN
```

The token is generated from your firm account (no sandbox needed). The Firm API is rate limited at 5 requests per second; the SDK throttles accordingly.

## Iterate your portfolio

```python
for company in firm.companies.list():
    print(company.id, company.name, company.siren)
```

Every other resource takes the company id as its first argument:

```python
company_id = 4217

# Fiscal years
for fy in firm.fiscal_years.list(company_id):
    print(fy.start, fy.finish)

# Trial balance over a period
for row in firm.trial_balance.list(
    company_id, period_start="2026-01-01", period_end="2026-06-30"
):
    print(row.number, row.debits, row.credits)
```

## Post accounting entries

```python
from decimal import Decimal

firm.ledger_entries.create(
    company_id,
    date="2026-07-08",
    journal_id=12,
    label="OD de régularisation",
    ledger_entry_lines=[
        {"ledger_account_id": 411, "debit": Decimal("120.00")},
        {"ledger_account_id": 706, "credit": Decimal("120.00")},
    ],
)
```

## Documents (DMS)

The firm-only DMS resource manages the document library of each client company:

```python
firm.dms.folders.list(company_id)
firm.dms.files.create(company_id, file="path/to/piece.pdf", ...)
```

## Exports

```python
export = firm.exports.fecs.create(
    company_id, period_start="2026-01-01", period_end="2026-12-31"
)
export = firm.exports.fecs.get(company_id, export.id)   # poll until done
```

## Mass synchronization

Changelogs let you sync many client companies incrementally without re-reading everything:

```python
for company in firm.companies.list():
    for event in firm.changelogs.ledger_entry_lines(company.id):
        ...
```

!!! note "Company vs Firm scopes"
    The Firm API is read-write on accounting (entries, accounts, journals, banking) but read-only on invoicing (customer and supplier invoices, in beta). Invoice creation happens through each company's own Company API.
