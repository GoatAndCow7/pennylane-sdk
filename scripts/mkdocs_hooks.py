"""MkDocs build hooks.

Generates llms.txt and llms-full.txt (https://llmstxt.org) into the built
site, so AI tools can ingest the documentation efficiently:

- llms.txt: a compact index of every documentation page with absolute URLs.
- llms-full.txt: the entire documentation concatenated into one Markdown file.

Wired through the ``hooks:`` setting in mkdocs.yml; runs on every build.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

_TITLE_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
_BLURB_RE = re.compile(r"^(?!#|>|!|\||-|\s*$)(.+)$", re.MULTILINE)


def _page_meta(md_file: Path) -> tuple[str, str]:
    """Return (title, one-line blurb) for a Markdown page."""
    text = md_file.read_text(encoding="utf-8")
    title_match = _TITLE_RE.search(text)
    title = title_match.group(1).strip() if title_match else md_file.stem
    blurb_match = _BLURB_RE.search(text)
    blurb = blurb_match.group(1).strip() if blurb_match else ""
    blurb = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", blurb)  # strip md links
    blurb = re.sub(r"[*`]", "", blurb)
    if len(blurb) > 160:
        blurb = blurb[:157] + "..."
    return title, blurb


def _collect_pages(docs_dir: Path) -> list[Path]:
    """English pages only (translations mirror them), stable order."""
    ordered: list[Path] = []
    for pattern in ("index.md", "getting-started.md", "guides/*.md", "api/**/*.md"):
        for page in sorted(docs_dir.glob(pattern)):
            if ".fr.md" in page.name:
                continue
            ordered.append(page)
    return ordered


def on_post_build(config: dict[str, Any], **_kwargs: Any) -> None:
    docs_dir = Path(config["docs_dir"])
    site_dir = Path(config["site_dir"])
    site_url = str(config.get("site_url") or "").rstrip("/")

    pages = _collect_pages(docs_dir)

    index_lines = [
        "# pennylane-sdk",
        "",
        "> Unofficial Python SDK for the Pennylane API, the French accounting and "
        "invoicing platform. Complete coverage of the Company API v2 and Firm API v1, "
        "sync and async, typed with Pydantic.",
        "",
        f"Package: pip install pennylane-sdk | Repository: {config.get('repo_url', '')}",
        "",
        "## Documentation",
        "",
    ]
    full_parts = []
    for page in pages:
        title, blurb = _page_meta(page)
        rel = page.relative_to(docs_dir).as_posix()
        url_path = rel[: -len(".md")]
        url_path = "" if url_path == "index" else url_path + "/"
        url = f"{site_url}/{url_path}"
        suffix = f": {blurb}" if blurb else ""
        index_lines.append(f"- [{title}]({url}){suffix}")
        full_parts.append(f"<!-- source: {rel} -->\n\n{page.read_text(encoding='utf-8')}")

    index_lines += [
        "",
        "## Optional",
        "",
        f"- [Complete documentation in a single file]({site_url}/llms-full.txt)",
        "",
    ]

    (site_dir / "llms.txt").write_text("\n".join(index_lines), encoding="utf-8")
    (site_dir / "llms-full.txt").write_text("\n\n---\n\n".join(full_parts), encoding="utf-8")
