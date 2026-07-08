"""Accounting firm: sweep the whole client portfolio.

Run with: PENNYLANE_FIRM_API_TOKEN=... python examples/firm_portfolio.py
"""

from pennylane_sdk import PennylaneFirm

with PennylaneFirm() as firm:
    for company in firm.companies.list(per_page=50):
        print(f"\n=== {company.name} (SIREN {company.siren})")

        # Fiscal years of this client
        for fy in firm.fiscal_years.list(company.id):
            print("  fiscal year:", fy.start, "->", fy.finish)

        # Incremental sync: what changed in the ledger recently?
        events = 0
        for _event in firm.changelogs.ledger_entry_lines(company.id):
            events += 1
            if events >= 100:
                break
        print(f"  {events} recent ledger changes")
