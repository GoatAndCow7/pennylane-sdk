"""Download the official Pennylane OpenAPI specifications into specs/.

These vendored specs are the source of truth for the SDK: resource methods,
request/response models and the coverage audit (scripts/check_coverage.py)
are all validated against them.

Usage:
    python scripts/update_specs.py
"""

from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

SPECS = {
    "company_v2.json": "https://pennylane.readme.io/openapi/accounting.json",
    "firm_v1.json": "https://firm-pennylane.readme.io/openapi/referentials.json",
}

SPECS_DIR = Path(__file__).resolve().parent.parent / "specs"


def main() -> int:
    SPECS_DIR.mkdir(exist_ok=True)
    for filename, url in SPECS.items():
        target = SPECS_DIR / filename
        print(f"Downloading {url} -> {target}")
        # readme.io rejects requests without a browser-like User-Agent (403).
        request = urllib.request.Request(url, headers={"User-Agent": "pennylane-sdk-tools/1.0"})
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read()
        # Validate and pretty-print for readable diffs.
        spec = json.loads(raw)
        n_paths = len(spec.get("paths", {}))
        if n_paths == 0:
            print(f"ERROR: {filename} contains no paths: refusing to overwrite", file=sys.stderr)
            return 1
        target.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"  OK: {spec['info']['title']} v{spec['info']['version']}: {n_paths} paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
