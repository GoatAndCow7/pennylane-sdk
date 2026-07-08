"""Client-side rate throttling (sliding window).

The Pennylane API enforces strict rate limits: Company API: 25 requests per
5 seconds, Firm API: 5 requests per second: applied per token. Both clients
therefore throttle outgoing requests by default (``auto_throttle=True``) so
that bulk operations (auto-pagination, mass imports) never trip the limit.

The implementation is a sliding-window log: it keeps the monotonic timestamps
of the last ``max_requests`` sends and, when the window is full, waits until
the oldest one leaves the window.
"""

from __future__ import annotations

import asyncio
import threading
import time
from collections import deque

__all__ = ["AsyncRateThrottle", "RateThrottle"]


class RateThrottle:
    """Thread-safe sliding-window throttle for the sync client."""

    def __init__(self, max_requests: int, period: float) -> None:
        if max_requests < 1:
            raise ValueError("max_requests must be >= 1")
        if period <= 0:
            raise ValueError("period must be > 0")
        self.max_requests = max_requests
        self.period = period
        self._timestamps: deque[float] = deque()
        self._lock = threading.Lock()

    def acquire(self) -> None:
        """Block until a request slot is available, then consume it."""
        while True:
            with self._lock:
                now = time.monotonic()
                while self._timestamps and now - self._timestamps[0] >= self.period:
                    self._timestamps.popleft()
                if len(self._timestamps) < self.max_requests:
                    self._timestamps.append(now)
                    return
                wait = self._timestamps[0] + self.period - now
            # Sleep outside the lock so concurrent threads can queue fairly.
            time.sleep(max(wait, 0.001))


class AsyncRateThrottle:
    """Asyncio sliding-window throttle for the async client."""

    def __init__(self, max_requests: int, period: float) -> None:
        if max_requests < 1:
            raise ValueError("max_requests must be >= 1")
        if period <= 0:
            raise ValueError("period must be > 0")
        self.max_requests = max_requests
        self.period = period
        self._timestamps: deque[float] = deque()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Wait until a request slot is available, then consume it."""
        while True:
            async with self._lock:
                now = time.monotonic()
                while self._timestamps and now - self._timestamps[0] >= self.period:
                    self._timestamps.popleft()
                if len(self._timestamps) < self.max_requests:
                    self._timestamps.append(now)
                    return
                wait = self._timestamps[0] + self.period - now
            await asyncio.sleep(max(wait, 0.001))
