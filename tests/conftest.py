from __future__ import annotations

import pytest

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient

BASE_URL = "https://app.pennylane.com/api/external/v2"


@pytest.fixture
def sync_client() -> SyncAPIClient:
    return SyncAPIClient(api_token="test-token", base_url=BASE_URL, max_retries=3)


@pytest.fixture
def async_client() -> AsyncAPIClient:
    return AsyncAPIClient(api_token="test-token", base_url=BASE_URL, max_retries=3)


@pytest.fixture(autouse=True)
def _no_retry_delay(monkeypatch: pytest.MonkeyPatch) -> None:
    """Zero out retry backoff delays so retry tests run instantly.

    Patching ``_retry_delay`` (rather than ``time.sleep`` globally) keeps the
    throttle tests, which rely on real timing, unaffected.
    """
    from pennylane_sdk._base_client import BaseAPIClient

    monkeypatch.setattr(
        BaseAPIClient, "_retry_delay", lambda self, attempt, response: 0.0
    )
