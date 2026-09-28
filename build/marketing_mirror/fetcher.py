"""HTTP GET with retries. The only module here that touches the network."""

from __future__ import annotations

import logging
import time
import urllib.error
import urllib.request
from typing import Protocol

from build.marketing_mirror import settings

LOGGER = logging.getLogger("marketing_mirror")

# Answers worth asking again: the origin was busy, not wrong.
_RETRYABLE_STATUS = frozenset({429, 500, 502, 503, 504})


class FetchError(RuntimeError):
    """A URL could not be read."""


class Fetcher(Protocol):
    def get(self, url: str) -> bytes: ...


class HttpFetcher:
    def __init__(
        self,
        timeout: float = settings.TIMEOUT_SECONDS,
        retries: int = settings.RETRIES,
        backoff_seconds: float = 2.0,
    ) -> None:
        self._timeout = timeout
        self._retries = retries
        self._backoff = backoff_seconds

    def get(self, url: str) -> bytes:
        request = urllib.request.Request(
            url, headers={"User-Agent": settings.USER_AGENT}
        )
        for attempt in range(1, self._retries + 1):
            try:
                with urllib.request.urlopen(request, timeout=self._timeout) as response:
                    return response.read()
            except urllib.error.HTTPError as error:
                if error.code not in _RETRYABLE_STATUS or attempt == self._retries:
                    raise FetchError(f"{url}: HTTP {error.code}") from error
            except (urllib.error.URLError, TimeoutError, ConnectionError) as error:
                if attempt == self._retries:
                    raise FetchError(f"{url}: {error}") from error
            LOGGER.debug("retrying %s (attempt %d)", url, attempt + 1)
            time.sleep(self._backoff * attempt)
        raise FetchError(f"{url}: no attempts made")
