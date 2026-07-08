# Opérations comptables

Au-delà de la facturation, l'API expose le cœur comptable : journaux, plan comptable, écritures, lettrage, balance générale et exports légaux.

## Plan comptable et journaux

```python
# Chart of accounts (plan comptable)
for account in client.ledger_accounts.list():
    print(account.number, account.label)

client.ledger_accounts.create(number="706100", label="Prestations de services")

# Journals
for journal in client.journals.list():
    print(journal.code, journal.label)
```

## Écritures comptables (écritures)

Une écriture est un ensemble équilibré de lignes de débit/crédit :

```python
from decimal import Decimal

entry = client.ledger_entries.create(
    date="2026-07-08",
    journal_id=12,
    label="Vente prestation",
    ledger_entry_lines=[
        {"ledger_account_id": 411, "debit": Decimal("120.00"), "credit": Decimal("0.00")},
        {"ledger_account_id": 706, "debit": Decimal("0.00"), "credit": Decimal("100.00")},
        {"ledger_account_id": 445, "debit": Decimal("0.00"), "credit": Decimal("20.00")},
    ],
)
```

Si les lignes ne s'équilibrent pas, l'API répond 422 et le SDK lève `ValidationError` avec les totaux dans `err.details`.

!!! warning "Pas d'idempotence sur les créations"
    Poster deux fois la même écriture crée un doublon : l'API ne déduplique pas. Le SDK ne relance jamais automatiquement un POST après une erreur serveur pour cette raison. Dédupliquez de votre côté si votre pipeline peut rejouer les appels.

## Lettrage (lettrage)

Le lettrage relie des lignes d'écriture qui se soldent mutuellement, typiquement une ligne de facture avec sa ligne de paiement :

```python
client.ledger_entry_lines.letter(
    unbalanced_lettering_strategy="none",
    ledger_entry_lines=[{"id": 111}, {"id": 222}],
)
client.ledger_entry_lines.unletter(
    unbalanced_lettering_strategy="none",
    ledger_entry_lines=[{"id": 111}, {"id": 222}],
)
client.ledger_entry_lines.list_lettered_lines(111)
```

## Balance générale (balance générale)

```python
for row in client.trial_balance.list(
    period_start="2026-01-01",
    period_end="2026-06-30",
):
    print(row.number, row.debits, row.credits)
```

## Catégories analytiques

L'analytique de Pennylane permet de tagger presque tout (factures, transactions, lignes d'écriture) avec des catégories organisées en groupes (axes) :

```python
groups = client.category_groups.list()
client.categories.create(label="Agence Lyon", category_group_id=3)

client.customer_invoices.categorize(
    invoice_id,
    categories=[{"id": 42, "weight": "1.0"}],
)
```

## Exports légaux : FEC, grand livre

Les exports s'exécutent de façon asynchrone : créez l'export, puis interrogez-le jusqu'à ce que le fichier soit prêt.

```python
import time

export = client.exports.fecs.create(
    period_start="2026-01-01", period_end="2026-12-31"
)
while export.status not in ("done", "failed"):
    time.sleep(5)
    export = client.exports.fecs.get(export.id)
print(export.file_url)   # download link
```

Même logique pour `client.exports.general_ledgers` et `client.exports.analytical_general_ledgers`.

## Données bancaires

```python
for account in client.bank_accounts.list():
    ...

for tx in client.transactions.list(filter=[filters.gte("date", "2026-01-01")]):
    ...

# Reconcile: which invoices does this transaction settle?
client.transactions.list_matched_invoices(tx.id)
```
