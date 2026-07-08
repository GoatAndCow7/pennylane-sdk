# French e-invoicing (2026 reform)

France mandates electronic invoicing for domestic B2B transactions:

- **September 2026**: every company must be able to **receive** e-invoices; large companies and mid-caps must also **emit** them.
- **September 2027**: emission becomes mandatory for SMEs and micro-companies.

B2B invoices must transit through a **Plateforme Agréée (PA)**, a government-accredited platform, in a structured format: **Factur-X** (PDF with embedded XML), **UBL** or **CII**. Pennylane is itself an accredited PA, so Pennylane users need no third-party platform. The API exposes the whole flow, and this SDK covers all of it.

## Check your PA registrations

```python
for registration in client.pa_registrations.list():
    print(registration)
```

## Send an invoice through the PA network

Finalize the invoice, then hand it to the platform:

```python
invoice = client.customer_invoices.finalize(draft.id)
client.customer_invoices.send_to_pa(invoice.id)
```

Track the delivery status either on the invoice's e-invoicing fields, via the change feed, or with the webhook event `customer_invoice.e_invoicing_status_updated` (see the [webhooks guide](webhooks.md)).

## Receive supplier e-invoices

Invoices arriving through the network land in Pennylane automatically. If you receive structured invoices through another channel, import them:

```python
client.supplier_invoices.import_e_invoice(file="invoice.xml")
```

The Factur-X or XML data is parsed structurally (no OCR), so supplier, amounts and lines are reliable.

## Import sales e-invoices from another tool

If you invoice from an external ERP but keep Pennylane as your accounting system and PA, push your sales invoices as e-invoices:

```python
client.customer_invoices.import_e_invoice(
    file="factur-x.pdf",
    # invoice_options can pre-fill customer and lines, see the docstring
)
```

## Update e-invoice status (advanced)

Purchase-side workflows can update the lifecycle status of a received e-invoice (approved, refused, payment sent...):

```python
client.supplier_invoices.update_e_invoice_status(invoice_id, ...)
```

!!! tip "Deadlines are business-critical"
    If you integrate invoicing for September 2026, test the PA flow early in a sandbox. The SDK raises `ValidationError` with the API's details when a document does not meet the format requirements.
