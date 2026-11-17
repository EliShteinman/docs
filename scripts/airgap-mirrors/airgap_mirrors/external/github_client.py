import logging
import re
from pathlib import Path

from pydantic import TypeAdapter

from airgap_mirrors.http import HttpClient, HttpResponse
from airgap_mirrors.models import ReleaseRecord

logger: logging.Logger = logging.getLogger(__name__)

_NEXT_PAGE = re.compile(r'<([^>]+)>;\s*rel="next"')
_RELEASES = TypeAdapter(list[ReleaseRecord])
PAGE_SIZE: int = 100


class GitHubClient:
    def __init__(self, http: HttpClient) -> None:
        self._http: HttpClient = http

    def published_releases(self, repository: str) -> list[ReleaseRecord]:
        releases: list[ReleaseRecord] = []
        response: HttpResponse = self._http.get(f"repos/{repository}/releases", {"per_page": PAGE_SIZE})
        while True:
            releases += _RELEASES.validate_python(response.json())
            next_page: str | None = _next_page(response)
            if next_page is None:
                break
            response = self._http.get(next_page)
        published: list[ReleaseRecord] = [release for release in releases if not release.draft]
        logger.debug("%s: %d releases", repository, len(published))
        return published

    def download(self, url: str, target: Path) -> None:
        self._http.download(url, target)


def _next_page(response: HttpResponse) -> str | None:
    link: str = response.headers.get("Link") or ""
    match: re.Match[str] | None = _NEXT_PAGE.search(link)
    return match.group(1) if match else None
