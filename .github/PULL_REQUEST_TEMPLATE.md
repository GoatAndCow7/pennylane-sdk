<!-- Thanks for contributing! A few checks before review: -->

**What this changes**

**Checklist**

- [ ] `uv run pytest` passes
- [ ] `uv run mypy --strict src` passes
- [ ] `uv run ruff check src tests scripts` passes
- [ ] `uv run python scripts/check_coverage.py` still reports full coverage
- [ ] New endpoints follow `docs/design/resource-map.md` (sync + async + tests + docstrings with scope and reference)
