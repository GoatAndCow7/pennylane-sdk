from __future__ import annotations

import pytest

from pennylane_sdk import (
    AsyncPennylane,
    AsyncPennylaneFirm,
    Pennylane,
    PennylaneError,
    PennylaneFirm,
)
from pennylane_sdk._client import DEFAULT_COMPANY_BASE_URL, DEFAULT_FIRM_BASE_URL


class TestTokenResolution:
    def test_explicit_token(self) -> None:
        with Pennylane(api_token="tok") as client:
            assert client._client._api_token == "tok"

    def test_env_var_token(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("PENNYLANE_API_TOKEN", "env-tok")
        with Pennylane() as client:
            assert client._client._api_token == "env-tok"

    def test_missing_token_raises_helpful_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("PENNYLANE_API_TOKEN", raising=False)
        with pytest.raises(PennylaneError, match="PENNYLANE_API_TOKEN"):
            Pennylane()

    def test_firm_uses_separate_env_var(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("PENNYLANE_FIRM_API_TOKEN", raising=False)
        monkeypatch.setenv("PENNYLANE_API_TOKEN", "company-tok")
        with pytest.raises(PennylaneError, match="PENNYLANE_FIRM_API_TOKEN"):
            PennylaneFirm()


class TestConfiguration:
    def test_default_base_urls(self) -> None:
        with Pennylane(api_token="t") as company, PennylaneFirm(api_token="t") as firm:
            assert company._client.base_url == DEFAULT_COMPANY_BASE_URL
            assert firm._client.base_url == DEFAULT_FIRM_BASE_URL

    def test_base_url_override_and_trailing_slash(self) -> None:
        with Pennylane(api_token="t", base_url="https://proxy.local/v2/") as client:
            assert client._client.base_url == "https://proxy.local/v2"

    def test_throttle_enabled_by_default_with_official_limits(self) -> None:
        with Pennylane(api_token="t") as company, PennylaneFirm(api_token="t") as firm:
            company_throttle = company._client._throttle
            firm_throttle = firm._client._throttle
            assert company_throttle is not None
            assert (company_throttle.max_requests, company_throttle.period) == (25, 5.0)
            assert firm_throttle is not None
            assert (firm_throttle.max_requests, firm_throttle.period) == (5, 1.0)

    def test_throttle_can_be_disabled(self) -> None:
        with Pennylane(api_token="t", auto_throttle=False) as client:
            assert client._client._throttle is None


class TestAsyncClients:
    async def test_async_context_manager(self) -> None:
        async with AsyncPennylane(api_token="t") as client:
            assert client._client.base_url == DEFAULT_COMPANY_BASE_URL

    async def test_async_firm_context_manager(self) -> None:
        async with AsyncPennylaneFirm(api_token="t") as firm:
            assert firm._client.base_url == DEFAULT_FIRM_BASE_URL
