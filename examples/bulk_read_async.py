"""Read a large dataset fast and safely with the async client.

The built-in throttle keeps the whole run under the API rate limit
(25 requests / 5 s), so you can just iterate.

Run with: PENNYLANE_API_TOKEN=... python examples/bulk_read_async.py
"""

import asyncio
from collections import Counter

from pennylane_sdk import AsyncPennylane, filters


async def main() -> None:
    async with AsyncPennylane() as client:
        totals: Counter[str] = Counter()
        count = 0

        page = await client.customer_invoices.list(
            filter=[filters.gte("date", "2026-01-01")],
            limit=100,  # 100 per request = 5x fewer requests than the default
        )
        async for invoice in page:
            count += 1
            if invoice.status:
                totals[invoice.status] += 1

        print(f"{count} invoices since 2026-01-01")
        for status, n in totals.most_common():
            print(f"  {status}: {n}")


if __name__ == "__main__":
    asyncio.run(main())
