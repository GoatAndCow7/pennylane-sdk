# Contributing

Thanks for helping make pennylane-sdk better! Contributions of every size are welcome: bug reports, docs fixes, new endpoint coverage, ideas.

## Development setup

Requirements: Python 3.10+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/GoatAndCow7/pennylane-sdk
cd pennylane-sdk
uv sync
```

Run the checks the CI runs:

```bash
uv run pytest                              # tests (all mocked, no token needed)
uv run mypy --strict src                   # type checking
uv run ruff check src tests scripts       # lint
uv run python scripts/check_coverage.py    # every API operation implemented?
uv run python scripts/check_parity.py      # sync and Async twins identical?
uv run mkdocs serve                        # docs live preview
```

## Project layout

```
specs/                     vendored official OpenAPI specs (source of truth)
scripts/update_specs.py    refresh the specs from pennylane.readme.io
scripts/check_coverage.py  audits that every spec operation exists in sync + async
scripts/show_endpoint.py   inspect one endpoint's schema from the specs
src/pennylane_sdk/
  _base_client.py          HTTP engine: auth, retries, throttle, errors
  _pagination.py           cursor and page-number auto-paginating pages
  resources/company|firm/  one module per URL namespace, sync + Async classes
  types/company|firm/      Pydantic response models
tests/                     mirrors resources/, respx-mocked
docs/                      mkdocs-material site
```

## Adding or fixing an endpoint

1. Find the operation in the spec: `uv run python scripts/show_endpoint.py company "customer_invoices/{id}/finalize" put`
2. Follow the conventions in `docs/design/resource-map.md` (method naming, models, docstrings). `src/pennylane_sdk/resources/company/products.py` is the reference style.
3. Write the resource method (sync and async), the models, and tests.
4. Make the four checks above pass. `check_coverage.py` must report full coverage.

## Style rules

- English everywhere in code and docs.
- No em dashes or en dashes in text; use plain punctuation.
- Docstrings state the required scope and link the official reference page.
- Response model fields are optional (`| None = None`) except `id`; monetary strings use the `Money` type.

## Releasing (maintainers)

1. Update `CHANGELOG.md` and bump the version in `pyproject.toml` and `src/pennylane_sdk/_version.py`.
2. Tag: `git tag v0.x.y && git push --tags`.
3. The `release.yml` workflow tests, builds and publishes to PyPI via trusted publishing.

## When the API changes

Refresh the vendored specs and see what the coverage audit says:

```bash
uv run python scripts/update_specs.py
uv run python scripts/check_coverage.py
```

New operations show up as MISSING; removed ones as UNKNOWN CALL. Please open an issue even if you cannot fix it yourself.
