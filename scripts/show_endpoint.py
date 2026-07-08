"""Pretty-print the resolved schema of one endpoint from the vendored specs.

Made for SDK implementers: dumps the query parameters, request body and
response schema of an operation in a compact, readable form, with $refs
resolved inline.

Usage (leading slash optional: omit it in Git Bash on Windows, which would
otherwise rewrite the argument into a filesystem path):
    python scripts/show_endpoint.py company products get
    python scripts/show_endpoint.py company "customer_invoices/{id}/finalize" put
    python scripts/show_endpoint.py firm "companies/{company_id}/ledger_entries" post
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

SPEC_FILES = {"company": "company_v2.json", "firm": "firm_v1.json"}
PREFIXES = {"company": "/api/external/v2", "firm": "/api/external/firm/v1"}

_MAX_DEPTH = 12


def _resolve(spec: dict[str, Any], node: Any, depth: int = 0) -> Any:
    if depth > _MAX_DEPTH:
        return "<max depth>"
    if isinstance(node, dict):
        if "$ref" in node:
            target: Any = spec
            for part in node["$ref"].split("/")[1:]:
                target = target[part]
            return _resolve(spec, target, depth + 1)
        return {key: _resolve(spec, value, depth + 1) for key, value in node.items()}
    if isinstance(node, list):
        return [_resolve(spec, item, depth + 1) for item in node]
    return node


def _describe(schema: dict[str, Any], indent: int = 0) -> None:
    pad = "  " * indent
    for combinator in ("allOf", "anyOf", "oneOf"):
        if combinator in schema:
            for i, variant in enumerate(schema[combinator]):
                title = variant.get("title", f"variant {i}")
                print(f"{pad}[{combinator} {i}: {title}]")
                _describe(variant, indent + 1)
            return
    required = set(schema.get("required", []))
    for name, prop in schema.get("properties", {}).items():
        if not isinstance(prop, dict):
            continue
        kind = prop.get("type", "?")
        marks = []
        if name in required:
            marks.append("REQUIRED")
        if prop.get("nullable"):
            marks.append("nullable")
        if prop.get("deprecated"):
            marks.append("deprecated")
        enum = prop.get("enum")
        if enum and len(enum) <= 15:
            marks.append(f"enum={enum}")
        elif enum:
            marks.append(f"enum[{len(enum)} values, first={enum[:3]}]")
        if "default" in prop:
            marks.append(f"default={prop['default']!r}")
        description = str(prop.get("description", ""))[:90].replace("\n", " ")
        suffix = (": " + description) if description else ""
        flags = (" [" + ", ".join(marks) + "]") if marks else ""
        if kind == "object":
            print(f"{pad}{name}: object{flags}{suffix}")
            _describe(prop, indent + 1)
        elif kind == "array":
            items = prop.get("items", {})
            item_kind = items.get("type", "?") if isinstance(items, dict) else "?"
            print(f"{pad}{name}: array<{item_kind}>{flags}{suffix}")
            if isinstance(items, dict) and items.get("type") == "object":
                _describe(items, indent + 1)
        else:
            print(f"{pad}{name}: {kind}{flags}{suffix}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", choices=("company", "firm"))
    parser.add_argument("path", help="endpoint path WITHOUT the API prefix, e.g. /products")
    parser.add_argument("method", choices=("get", "post", "put", "patch", "delete"))
    args = parser.parse_args()

    spec = json.loads((ROOT / "specs" / SPEC_FILES[args.spec]).read_text(encoding="utf-8"))
    # Tolerate Git Bash (MSYS) path mangling and missing leading slashes.
    endpoint = args.path.replace("\\", "/")
    for marker in (PREFIXES[args.spec] + "/", ":/Program Files/Git/"):
        if marker in endpoint:
            endpoint = endpoint.split(marker, 1)[1]
    full_path = PREFIXES[args.spec] + "/" + endpoint.lstrip("/")
    item = spec["paths"].get(full_path)
    if item is None or args.method not in item:
        known = [p for p in spec["paths"] if args.path.split("/")[1] in p]
        print(f"Operation not found: {args.method.upper()} {full_path}")
        if known:
            print("Close matches:")
            for match in known[:20]:
                print(f"  {match}")
        return 1

    op = _resolve(spec, item[args.method])
    print(f"=== {args.method.upper()} {full_path}")
    print(f"operationId: {op.get('operationId')}")
    print(f"summary: {op.get('summary')}")
    if op.get("deprecated"):
        print("DEPRECATED: yes")
    if "Hidden" in op.get("tags", []):
        print("HIDDEN (beta / undocumented): yes")
    security = op.get("security")
    if security:
        print(f"scopes: {security[0].get('oauth2')}")

    params = [p for p in op.get("parameters", []) if isinstance(p, dict)]
    query = [p for p in params if p.get("in") == "query"]
    if query:
        print("\n--- query parameters:")
        for param in query:
            schema = param.get("schema", {})
            required = " [REQUIRED]" if param.get("required") else ""
            default = f" default={schema.get('default')!r}" if "default" in schema else ""
            print(f"  {param['name']}: {schema.get('type', '?')}{required}{default}")

    body = op.get("requestBody", {})
    for ctype, content in body.get("content", {}).items():
        print(f"\n--- request body [{ctype}]" + (" [REQUIRED]" if body.get("required") else ""))
        _describe(content.get("schema", {}), 1)

    for status, response in sorted(op.get("responses", {}).items()):
        content = response.get("content", {}) if isinstance(response, dict) else {}
        if not content:
            print(f"\n--- response {status}: (no body)")
            continue
        for ctype, body_schema in content.items():
            print(f"\n--- response {status} [{ctype}]:")
            _describe(body_schema.get("schema", {}), 1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
