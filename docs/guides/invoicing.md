# Invoicing lifecycle

This guide walks the full life of a customer invoice: draft, finalize, send, get paid, reconcile.

## Create a draft

```python
from pennylane_sdk import Pennylane

client = Pennylane()

invoice = client.customer_invoices.create(
    customer_id=123,
    date="2026-07-08",
    deadline="2026-08-07",
    invoice_lines=[
        # With a product: unit price, VAT and label come from the catalog
        {"product_id": 45, "quantity": "2"},
        # Or a free line
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

Drafts can be edited (`update`) and deleted (`delete`) freely.

!!! note "Amounts are strings or Decimals"
    The API transports amounts as strings to avoid float rounding. Pass `Decimal("500.00")` or `"500.00"`; the SDK serializes both correctly, and parses monetary response fields into `Decimal`.

## Finalize

Finalizing gives the invoice its final legal number. There is no undo (accounting rules), only credit notes.

```python
invoice = client.customer_invoices.finalize(invoice.id)
print(invoice.invoice_number)   # e.g. F-2026-0042
```

## Send

```python
client.customer_invoices.send_by_email(invoice.id)
```

Or through the French e-invoicing network for B2B, see the [e-invoicing guide](e-invoicing.md):

```python
client.customer_invoices.send_to_pa(invoice.id)
```

## From a quote

```python
quote = client.quotes.create(customer_id=123, invoice_lines=[...])
client.quotes.send_by_email(quote.id)
# once accepted:
invoice = client.customer_invoices.create_from_quote(quote_id=quote.id)
```

## Get paid and reconcile

```python
# Mark as paid manually
client.customer_invoices.mark_as_paid(invoice.id)

# Or match a real bank transaction against it
client.customer_invoices.match_transaction(invoice.id, transaction_id=987)
client.customer_invoices.list_matched_transactions(invoice.id)

# Payments recorded on the invoice
client.customer_invoices.list_payments(invoice.id)
```

## Credit notes

A credit note (avoir) is a customer invoice with negative amounts. Link it to the invoice it corrects:

```python
credit_note = client.customer_invoices.create(
    customer_id=123,
    invoice_lines=[{"product_id": 45, "quantity": "-2"}],
)
client.customer_invoices.finalize(credit_note.id)
client.customer_invoices.link_credit_note(invoice.id, credit_note_id=credit_note.id)
```

## Import existing invoices

Invoices produced outside Pennylane (another tool, a marketplace) can be imported:

```python
# From a PDF file
imported = client.customer_invoices.import_from_file(
    file="path/to/invoice.pdf",
    # + invoice fields, see the docstring
)

# From a structured e-invoice (Factur-X, UBL, CII)
imported = client.customer_invoices.import_e_invoice(file="path/to/factur-x.pdf")
```

## Recurring invoices

`client.billing_subscriptions` creates subscriptions that generate invoices on a schedule (weekly, monthly, yearly...). See the API reference for the recurrence options.

## Sync changes incrementally

Instead of re-listing everything, poll the change feed:

```python
for event in client.changelogs.customer_invoices():
    ...
```
