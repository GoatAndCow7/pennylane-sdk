"""Audit sync/async parity across all resource modules.

Every resource module deliberately ships a sync class and its Async twin.
This script proves, mechanically, that each pair stays identical: same
methods, same signatures and defaults, and same normalized bodies (after
stripping ``async``/``await`` and Sync/Async name prefixes). A bug fixed in
one twin but not the other fails CI here.

Usage:
    python scripts/check_parity.py [--quiet]

Exit code 0 when every pair matches, 1 otherwise.
"""

from __future__ import annotations

import argparse
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESOURCE_DIRS = [
    ROOT / "src" / "pennylane_sdk" / "resources" / "company",
    ROOT / "src" / "pennylane_sdk" / "resources" / "firm",
]


class _Normalizer(ast.NodeTransformer):
    """Rewrite an async function body into its sync-equivalent form."""

    def visit_Await(self, node: ast.Await) -> ast.AST:
        return self.visit(node.value)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AST:
        self.generic_visit(node)
        return ast.FunctionDef(
            name=node.name,
            args=node.args,
            body=node.body,
            decorator_list=node.decorator_list,
            returns=node.returns,
            type_comment=node.type_comment,
            type_params=getattr(node, "type_params", []),
        )

    def visit_Name(self, node: ast.Name) -> ast.AST:
        node.id = _strip_variant_prefix(node.id)
        return node

    def visit_Attribute(self, node: ast.Attribute) -> ast.AST:
        self.generic_visit(node)
        node.attr = _strip_variant_prefix(node.attr)
        return node


def _strip_variant_prefix(name: str) -> str:
    if name.startswith("Async"):
        return name[len("Async"):]
    if name.startswith("Sync"):
        return name[len("Sync"):]
    return name


def _strip_docstrings(node: ast.AST) -> None:
    for child in ast.walk(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = child.body
            if (
                body
                and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)
            ):
                child.body = body[1:] or [ast.Pass()]


def _normalized_dump(cls: ast.ClassDef) -> dict[str, str]:
    """Map of method name -> normalized AST dump."""
    methods: dict[str, str] = {}
    for item in cls.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            _strip_docstrings(item)
            normalized = _Normalizer().visit(item)
            ast.fix_missing_locations(normalized)
            methods[item.name] = ast.dump(normalized, annotate_fields=False)
    return methods


def check_module(py_file: Path) -> list[str]:
    tree = ast.parse(py_file.read_text(encoding="utf-8"))
    classes = {n.name: n for n in tree.body if isinstance(n, ast.ClassDef)}
    problems: list[str] = []

    sync_names = [n for n in classes if not n.startswith("Async")]
    for sync_name in sync_names:
        async_name = f"Async{sync_name}"
        if async_name not in classes:
            problems.append(f"{py_file.name}: {sync_name} has no {async_name} twin")
            continue
        sync_methods = _normalized_dump(classes[sync_name])
        async_methods = _normalized_dump(classes[async_name])

        for missing in sorted(set(sync_methods) - set(async_methods)):
            problems.append(f"{py_file.name}: {async_name} is missing method {missing}()")
        for extra in sorted(set(async_methods) - set(sync_methods)):
            problems.append(f"{py_file.name}: {async_name} has extra method {extra}()")
        for name in sorted(set(sync_methods) & set(async_methods)):
            if sync_methods[name] != async_methods[name]:
                problems.append(
                    f"{py_file.name}: {sync_name}.{name}() and {async_name}.{name}() "
                    "diverge (signature, defaults or body)"
                )
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    pairs = 0
    problems: list[str] = []
    for directory in RESOURCE_DIRS:
        for py_file in sorted(directory.glob("*.py")):
            if py_file.name == "__init__.py":
                continue
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
            pairs += sum(
                1
                for n in tree.body
                if isinstance(n, ast.ClassDef) and not n.name.startswith("Async")
            )
            problems.extend(check_module(py_file))

    print(f"Sync/async parity: {pairs - len(problems)}/{pairs} class pairs identical")
    if problems and not args.quiet:
        for problem in problems:
            print(f"  DIVERGENCE {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
