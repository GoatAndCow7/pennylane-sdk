"""Integration tests against a real Pennylane sandbox.

These tests run ONLY when ``PENNYLANE_API_TOKEN`` is set (use a sandbox
token: some tests create real objects). They are automatically skipped in
CI and on contributor machines without a token.

Run them with:

    PENNYLANE_API_TOKEN=... uv run pytest tests/integration -q
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from pennylane_sdk import Pennylane

_TOKEN = os.environ.get("PENNYLANE_API_TOKEN")

pytestmark = pytest.mark.skipif(
    not _TOKEN, reason="PENNYLANE_API_TOKEN not set: integration tests need a sandbox token"
)


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    # This hook receives every collected item in the session, not only the
    # ones under this directory: scope the skip to the integration folder,
    # otherwise the whole unit suite gets skipped when no token is set.
    if _TOKEN:
        return
    here = Path(__file__).parent
    skip = pytest.mark.skip(reason="PENNYLANE_API_TOKEN not set")
    for item in items:
        if here in Path(str(item.fspath)).parents:
            item.add_marker(skip)


@pytest.fixture(scope="session")
def live_client() -> Pennylane:
    client = Pennylane()  # built-in throttle keeps us under 25 req / 5 s
    yield client
    client.close()
