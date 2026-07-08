"""Audit SDK coverage of the Pennylane OpenAPI specifications.

For every operation (method + path) declared in the vendored specs, this
script verifies that the SDK implements it in BOTH the sync and async
resource classes. It also flags SDK calls that do not match any spec
operation (typos, removed endpoints).

Convention enforced: resource methods perform requests through helpers named
``self._get/_post/_put/_patch/_delete`` (or ``self._client.request("GET", ...)``)
with the endpoint path as a plain or f- string literal starting with ``/``.
Path parameters may use any placeholder name: ``f"/customer_invoices/{invoice_id}"``
matches the spec path ``/customer_invoices/{id}``.

Usage:
    python scripts/check_coverage.py [--quiet]

Exit code 0 when coverage is complete and no unknown calls exist, 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "pennylane_sdk"

SUITES = [
    # (label, spec file, spec path prefix, resources directory)
    ("Company v2", "company_v2.json", "/api/external/v2", "resources/company"),
    ("Firm v1", "firm_v1.json", "/api/external/firm/v1", "resources/firm"),
]

HTTP_METHODS = ("get", "post", "put", "patch", "delete")

# self._get("/x") | self._post(f"/x/{id}") | self._client.request("GET", "/x")
CALL_RE = re.compile(
    r"self\._(?:(get|post|put|patch|delete)|client\.request\(\s*\"(GET|POST|PUT|PATCH|DELETE)\",)"
    r"\(?\s*f?\"(/[^\"]*)\"",
)

PLACEHOLDER_RE = re.compile(r"\{[^}]*\}")


def normalize(path: str) -> str:
    """Replace every {placeholder} with {} so param names don't matter."""
    return PLACEHOLDER_RE.sub("{}", path)


@dataclass
class Operation:
    method: str
    path: str  # spec path without the API prefix
    summary: str
    hidden: bool
    deprecated: bool
    sync_hits: int = 0
    async_hits: int = 0

    @property
    def key(self) -> tuple[str, str]:
        return (self.method, normalize(self.path))


@dataclass
class SuiteReport:
    label: str
    operations: list[Operation] = field(default_factory=list)
    unknown_calls: list[tuple[str, str, str]] = field(default_factory=list)  # (file, method, path)


def load_operations(spec_file: Path, prefix: str) -> list[Operation]:
    spec = json.loads(spec_file.read_text(encoding="utf-8"))
    operations: list[Operation] = []
    for raw_path, item in spec["paths"].items():
        if not raw_path.startswith(prefix):
            raise ValueError(f"Spec path {raw_path!r} does not start with expected prefix {prefix!r}")
        path = raw_path[len(prefix):]
        for method in HTTP_METHODS:
            if method in item:
                op = item[method]
                operations.append(
                    Operation(
                        method=method.upper(),
                        path=path,
                        summary=op.get("summary", op.get("operationId", "")),
                        hidden="Hidden" in op.get("tags", []),
                        deprecated=bool(op.get("deprecated")),
                    )
                )
    return operations


def scan_calls(resources_dir: Path) -> list[tuple[str, str, str, bool]]:
    """Return (file, METHOD, normalized_path, is_async_context) for each request call."""
    calls: list[tuple[str, str, str, bool]] = []
    for py_file in sorted(resources_dir.rglob("*.py")):
        text = py_file.read_text(encoding="utf-8")
        # Split the file into class bodies so we can tell sync from async:
        # convention is class Foo / class AsyncFoo in the same module.
        for class_match in re.finditer(r"^class\s+(\w+)[^\n]*:\n(.*?)(?=^class\s|\Z)", text, re.S | re.M):
            class_name, body = class_match.group(1), class_match.group(2)
            is_async = class_name.startswith("Async")
            for m in CALL_RE.finditer(body):
                method = (m.group(1) or m.group(2)).upper()
                calls.append((py_file.name, method, normalize(m.group(3)), is_async))
    return calls


def run_suite(label: str, spec_name: str, prefix: str, resources_rel: str) -> SuiteReport:
    report = SuiteReport(label=label)
    report.operations = load_operations(ROOT / "specs" / spec_name, prefix)
    by_key = {op.key: op for op in report.operations}

    resources_dir = SRC / resources_rel
    if resources_dir.exists():
        for file, method, path, is_async in scan_calls(resources_dir):
            op = by_key.get((method, path))
            if op is None:
                report.unknown_calls.append((file, method, path))
            elif is_async:
                op.async_hits += 1
            else:
                op.sync_hits += 1
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiet", action="store_true", help="only print the summary lines")
    args = parser.parse_args()

    ok = True
    for suite_args in SUITES:
        report = run_suite(*suite_args)
        total = len(report.operations)
        covered = [op for op in report.operations if op.sync_hits and op.async_hits]
        missing = [op for op in report.operations if not (op.sync_hits and op.async_hits)]

        print(f"{report.label}: {len(covered)}/{total} operations covered (sync + async)")
        if missing and not args.quiet:
            for op in missing:
                halves = []
                if not op.sync_hits:
                    halves.append("sync")
                if not op.async_hits:
                    halves.append("async")
                tags = "".join(
                    f" [{t}]" for t, cond in (("hidden", op.hidden), ("deprecated", op.deprecated)) if cond
                )
                print(f"  MISSING ({'+'.join(halves)}) {op.method} {op.path}{tags} — {op.summary}")
        if report.unknown_calls:
            ok = False
            for file, method, path in report.unknown_calls:
                print(f"  UNKNOWN CALL in {file}: {method} {path} (not in spec)")
        if missing:
            ok = False

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
