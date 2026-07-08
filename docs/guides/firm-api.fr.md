# Firm API (cabinets d'expertise comptable)

Les cabinets d'expertise comptable (cabinets d'expertise comptable) disposent d'une API dédiée pour travailler sur l'ensemble de leur portefeuille de dossiers clients : lister les sociétés qu'ils gèrent, lire et poster des écritures comptables, téléverser des documents, lancer des exports, le tout pour chaque dossier client.

## Dossiers clients et jeton

```python
from pennylane_sdk import PennylaneFirm, AsyncPennylaneFirm

firm = PennylaneFirm()   # reads PENNYLANE_FIRM_API_TOKEN
```

Le jeton est généré depuis votre compte cabinet (aucun bac à sable nécessaire). La Firm API est soumise à une limite de débit de 5 requêtes par seconde ; le SDK applique une régulation de débit en conséquence.

## Parcourir votre portefeuille

```python
for company in firm.companies.list():
    print(company.id, company.name, company.siren)
```

Toute autre ressource prend l'identifiant du dossier client comme premier argument :

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

## Poster des écritures comptables

```python
from decimal import Decimal

firm.ledger_entries.create(
    company_id,
    date="2026-07-08",
    journal_id=12,
    label="OD de régularisation",
    ledger_entry_lines=[
        {"ledger_account_id": 411, "debit": Decimal("120.00"), "credit": Decimal("0.00")},
        {"ledger_account_id": 706, "debit": Decimal("0.00"), "credit": Decimal("120.00")},
    ],
)
```

## Documents (DMS)

La ressource DMS, réservée aux cabinets, gère la bibliothèque documentaire de chaque dossier client :

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

## Synchronisation de masse

Les changelogs permettent de synchroniser de nombreux dossiers clients de façon incrémentale, sans tout relire :

```python
for company in firm.companies.list():
    for event in firm.changelogs.ledger_entry_lines(company.id):
        ...
```

!!! note "Scopes Company vs Firm"
    La Firm API est en lecture-écriture sur la comptabilité (écritures, comptes, journaux, banque) mais en lecture seule sur la facturation (factures clients et fournisseurs, en bêta). La création de factures se fait via l'API Company propre à chaque dossier client.
