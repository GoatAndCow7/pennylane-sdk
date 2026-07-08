# Cycle de vie de la facturation

Ce guide parcourt toute la vie d'une facture client : brouillon, finalisation, envoi, encaissement, rapprochement.

## Créer un brouillon

```python
from pennylane_sdk import Pennylane

client = Pennylane()

invoice = client.customer_invoices.create(
    customer_id=123,
    date="2026-07-08",
    deadline="2026-08-07",
    invoice_lines=[
        # Avec un produit : le prix unitaire, la TVA et le libellé viennent du catalogue
        {"product_id": 45, "quantity": "2"},
        # Ou une ligne libre
        {
            "label": "On-site setup",
            "quantity": "1",
            "raw_currency_unit_price": "500.00",
            "unit": "day",
            "vat_rate": "FR_200",
        },
    ],
)
print(invoice.status)   # draft
```

Les brouillons peuvent être modifiés (`update`) et supprimés (`delete`) librement.

!!! note "Les montants sont des chaînes ou des Decimal"
    L'API transporte les montants sous forme de chaînes pour éviter les arrondis liés aux flottants. Passez `Decimal("500.00")` ou `"500.00"` : le SDK sérialise correctement les deux formes, et convertit les champs monétaires de la réponse en `Decimal`.

## Finaliser

La finalisation attribue à la facture son numéro légal définitif. Il n'y a pas de retour en arrière (règles comptables), seulement des avoirs.

```python
invoice = client.customer_invoices.finalize(invoice.id)
print(invoice.invoice_number)   # ex. F-2026-0042
```

## Envoyer

```python
client.customer_invoices.send_by_email(invoice.id)
```

Ou via le réseau français de facturation électronique pour le B2B, voir le [guide de facturation électronique](e-invoicing.md) :

```python
client.customer_invoices.send_to_pa(invoice.id)
```

## À partir d'un devis

```python
quote = client.quotes.create(customer_id=123, invoice_lines=[...])
client.quotes.send_by_email(quote.id)
# une fois accepté :
invoice = client.customer_invoices.create_from_quote(quote_id=quote.id, draft=True)
```

## Encaisser et rapprocher

```python
# Marquer comme payée manuellement
client.customer_invoices.mark_as_paid(invoice.id)

# Ou rapprocher une transaction bancaire réelle avec la facture
client.customer_invoices.match_transaction(invoice.id, transaction_id=987)
client.customer_invoices.list_matched_transactions(invoice.id)

# Paiements enregistrés sur la facture
client.customer_invoices.list_payments(invoice.id)
```

## Avoirs

Un avoir (credit note) est une facture client à montants négatifs. Reliez-le à la facture qu'il corrige :

```python
credit_note = client.customer_invoices.create(
    customer_id=123,
    invoice_lines=[{"product_id": 45, "quantity": "-2"}],
)
client.customer_invoices.finalize(credit_note.id)
client.customer_invoices.link_credit_note(invoice.id, credit_note_id=credit_note.id)
```

## Importer des factures existantes

Les factures produites en dehors de Pennylane (un autre outil, une marketplace) peuvent être importées. Pour un simple PDF, téléversez d'abord le fichier, puis référencez-le :

```python
# 1. Téléverser le PDF en tant que pièce jointe
attachment = client.file_attachments.create(file="path/to/invoice.pdf")

# 2. Importer la facture en la référençant
imported = client.customer_invoices.import_from_file(
    file_attachment_id=attachment.id,
    date="2026-07-01",
    deadline="2026-07-31",
    customer_id=123,
    currency_amount_before_tax="100.00",
    currency_amount="120.00",
    currency_tax="20.00",
    invoice_lines=[...],
)

# Les factures électroniques structurées (Factur-X, UBL, CII) se téléversent directement
imported = client.customer_invoices.import_e_invoice(file="path/to/factur-x.pdf")
```

## Factures récurrentes

`client.billing_subscriptions` crée des abonnements de facturation qui génèrent des factures selon un calendrier (hebdomadaire, mensuel, annuel...). Consultez la référence de l'API pour les options de récurrence.

## Synchroniser les changements de façon incrémentale

Plutôt que de tout relister, interrogez le flux de changements :

```python
for event in client.changelogs.customer_invoices():
    ...
```
