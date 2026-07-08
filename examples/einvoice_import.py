"""French e-invoicing: import a Factur-X invoice and track PA delivery.

Run with: PENNYLANE_API_TOKEN=... python examples/einvoice_import.py invoice.pdf
"""

import sys

from pennylane_sdk import Pennylane

path = sys.argv[1] if len(sys.argv) > 1 else "invoice.pdf"

with Pennylane() as client:
    # Check the company's Plateforme Agréée registrations
    for registration in client.pa_registrations.list():
        print("PA registration:", registration)

    # Import a structured e-invoice (Factur-X PDF, UBL or CII XML).
    # The XML is parsed structurally, no OCR involved.
    result = client.customer_invoices.import_e_invoice(file=path)
    print("Imported:", result)
