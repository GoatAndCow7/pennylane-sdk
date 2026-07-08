from __future__ import annotations

import time

import pytest

from pennylane_sdk._throttle import AsyncRateThrottle, RateThrottle


class TestRateThrottle:
    def test_burst_within_limit_is_instant(self) -> None:
        throttle = RateThrottle(5, 1.0)
        start = time.monotonic()
        for _ in range(5):
            throttle.acquire()
        assert time.monotonic() - start < 0.2

    def test_exceeding_limit_waits_for_window(self) -> None:
        throttle = RateThrottle(2, 0.3)
        start = time.monotonic()
        for _ in range(3):
            throttle.acquire()
        elapsed = time.monotonic() - start
        assert elapsed >= 0.25  # 3rd request had to wait for the window

    def test_slots_free_up_after_period(self) -> None:
        throttle = RateThrottle(1, 0.1)
        throttle.acquire()
        time.sleep(0.12)
        start = time.monotonic()
        throttle.acquire()
        assert time.monotonic() - start < 0.05

    @pytest.mark.parametrize(("requests", "period"), [(0, 1.0), (1, 0.0), (1, -1.0)])
    def test_rejects_invalid_configuration(self, requests: int, period: float) -> None:
        with pytest.raises(ValueError, match="must be"):
            RateThrottle(requests, period)


class TestAsyncRateThrottle:
    async def test_burst_within_limit_is_instant(self) -> None:
        throttle = AsyncRateThrottle(5, 1.0)
        start = time.monotonic()
        for _ in range(5):
            await throttle.acquire()
        assert time.monotonic() - start < 0.2

    async def test_exceeding_limit_waits_for_window(self) -> None:
        throttle = AsyncRateThrottle(2, 0.3)
        start = time.monotonic()
        for _ in range(3):
            await throttle.acquire()
        elapsed = time.monotonic() - start
        assert elapsed >= 0.25

    @pytest.mark.parametrize(("requests", "period"), [(0, 1.0), (1, 0.0)])
    async def test_rejects_invalid_configuration(self, requests: int, period: float) -> None:
        with pytest.raises(ValueError, match="must be"):
            AsyncRateThrottle(requests, period)
