"""HTTP GET with retries. The only module here that touches the network."""

from __future__ import annotations

import gzip
import logging
import time
import urllib.error
import urllib.request
from email.message import Message
from typing import Protocol
from urllib.parse import urlsplit

from build.marketing_mirror import settings

LOGGER = logging.getLogger("marketing_mirror")

# Answers worth asking again: the origin was busy, not wrong.
_RETRYABLE_STATUS = frozenset({429, 500, 502, 503, 504})


class FetchError(RuntimeError):
    """A URL could not be read."""


class Moved(FetchError):
    """The URL redirects to a different page; its body is that page, not this one."""


def moved_to(requested: str, final: str) -> str | None:
    """The path `requested` was redirected to, or None if it answered itself.

    A trailing slash either way is the same page; anything else is not.
    """
    asked, got = urlsplit(requested).path, urlsplit(final).path
    return None if asked.rstrip("/") == got.rstrip("/") else got


class Fetcher(Protocol):
    def get(self, url: str) -> bytes: ...


def decode(body: bytes, headers: Message) -> bytes:
    """The body as the origin meant it. Pages are 1.5 MB and redis.io is slow
    to send them; asked for gzip, it sends a seventh of that."""
    if headers.get("Content-Encoding", "").lower() == "gzip":
        return gzip.decompress(body)
    return body


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
            url,
            headers={"User-Agent": settings.USER_AGENT, "Accept-Encoding": "gzip"},
        )
        for attempt in range(1, self._retries + 1):
            try:
                with urllib.request.urlopen(request, timeout=self._timeout) as response:
                    target = moved_to(url, response.geturl())
                    if target is not None:
                        raise Moved(f"{url}: moved to {target}")
                    return decode(response.read(), response.headers)
            except urllib.error.HTTPError as error:
                if error.code not in _RETRYABLE_STATUS or attempt == self._retries:
                    raise FetchError(f"{url}: HTTP {error.code}") from error
            except (urllib.error.URLError, TimeoutError, ConnectionError) as error:
                if attempt == self._retries:
                    raise FetchError(f"{url}: {error}") from error
            LOGGER.debug("retrying %s (attempt %d)", url, attempt + 1)
            time.sleep(self._backoff * attempt)
        raise FetchError(f"{url}: no attempts made")
