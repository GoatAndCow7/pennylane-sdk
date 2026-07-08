# Pagination and filtering

## Cursor pagination (almost everywhere)

List endpoints return a page object. The simplest way to use it: iterate, and let the SDK fetch the following pages lazily, under the client throttle.

```python
for invoice in client.customer_invoices.list(limit=100):
    ...  # walks EVERY page transparently
```

Async flavor:

```python
page = await client.customer_invoices.list(limit=100)
async for invoice in page:
    ...
```

To control pages yourself:

```python
page = client.customer_invoices.list(limit=100)
page.items        # items of the current page only
page.has_more     # whether a next page exists
page.next_cursor  # opaque cursor for the next page
next_page = page.next_page()        # or None on the last page

for page in page.iter_pages():      # page by page
    print(len(page.items))
```

`limit` accepts 1 to 100 (the API default is 20). Fewer requests with `limit=100` means faster bulk reads under the rate limit.

!!! warning "Filters are not encoded in the cursor"
    When you paginate a filtered query, the API requires the same `filter` and `sort` on every page request. The SDK does this for you in `next_page()` and during iteration.

## Page-number pagination (a few Firm endpoints)

Three Firm API endpoints (`companies`, `fiscal_years`, `trial_balance`) paginate with `page` and `per_page` instead of a cursor. Same experience:

```python
for company in firm.companies.list(per_page=50):
    ...
```

These return `SyncNumberedPage` / `AsyncNumberedPage` with `total_pages` and `current_page` attributes.

## Filtering

The `filter` parameter is a JSON array of conditions. Build it with the typed helpers:

```python
from pennylane_sdk import filters

client.customer_invoices.list(
    filter=[
        filters.gte("date", "2026-01-01"),
        filters.lt("date", "2026-07-01"),
        filters.eq("status", "upcoming"),
        filters.in_("customer_id", [42, 43]),
    ],
)
```

Available helpers: `eq`, `not_eq`, `lt`, `lte`, `gt`, `gte`, `in_`, `not_in`, and `where(field, operator, value)` for anything else. Values can be strings, numbers, `Decimal`, `date` or `datetime` (encoded automatically).

Which fields and operators each endpoint supports is listed in the [official reference](https://pennylane.readme.io/reference) per endpoint.

You can also pass a raw JSON string if you already have one; the SDK sends it as-is.

## Sorting

```python
client.customer_invoices.list(sort="-date")   # descending by date
client.customer_invoices.list(sort="id")      # ascending by id
```

Since the 2026 API changes, the default sort is `-id` (newest first) on all endpoints.

## Side-loading with include

Some list endpoints support an experimental `include` parameter to embed related records in one call:

```python
page = client.customer_invoices.list(include="invoice_lines")
page.included   # raw list of side-loaded records
```
