import json
import logging
import os
import shutil
import ssl
import tempfile
import urllib.parse
import urllib.request
from collections.abc import Mapping
from email.message import Message
from pathlib import Path
from urllib.error import HTTPError, URLError

from airgap_mirrors.exceptions import ApiError

logger: logging.Logger = logging.getLogger(__name__)

NOT_FOUND: int = 404
CHUNK_BYTES: int = 1024 * 1024


class HttpResponse:
    def __init__(self, status: int, body: bytes, headers: Message) -> None:
        self.status: int = status
        self.body: bytes = body
        self.headers: Message = headers

    def json(self) -> object:
        return json.loads(self.body) if self.body else None


class HttpClient:
    """A small JSON-over-HTTP client on the standard library, so the air-gapped machine needs no extra packages."""

    def __init__(
        self,
        base_url: str,
        headers: Mapping[str, str],
        error_type: type[ApiError],
        timeout_seconds: float,
        ssl_context: ssl.SSLContext | None = None,
    ) -> None:
        self._base_url: str = base_url.rstrip("/")
        self._headers: dict[str, str] = dict(headers)
        self._error_type: type[ApiError] = error_type
        self._timeout: float = timeout_seconds
        self._ssl_context: ssl.SSLContext | None = ssl_context

    def url(self, path: str, query: Mapping[str, str | int] | None = None) -> str:
        absolute: str = path if path.startswith(("http://", "https://")) else f"{self._base_url}/{path.lstrip('/')}"
        return f"{absolute}?{urllib.parse.urlencode(query)}" if query else absolute

    def get(self, path: str, query: Mapping[str, str | int] | None = None) -> HttpResponse:
        return self._send(urllib.request.Request(self.url(path, query), method="GET"))

    def get_or_none(self, path: str) -> HttpResponse | None:
        try:
            return self.get(path)
        except self._error_type as failure:
            if failure.status == NOT_FOUND:
                return None
            raise

    def delete_if_present(self, path: str) -> bool:
        try:
            self._send(urllib.request.Request(self.url(path), method="DELETE"))
        except self._error_type as failure:
            if failure.status == NOT_FOUND:
                return False
            raise
        return True

    def send_json(self, method: str, path: str, payload: Mapping[str, object]) -> HttpResponse:
        request: urllib.request.Request = urllib.request.Request(
            self.url(path),
            data=json.dumps(payload).encode(),
            method=method,
            headers={"Content-Type": "application/json"},
        )
        return self._send(request)

    def upload_file(self, path: str, source: Path) -> HttpResponse:
        with source.open("rb") as handle:
            request: urllib.request.Request = urllib.request.Request(
                self.url(path),
                data=handle,
                method="PUT",
                headers={"Content-Length": str(source.stat().st_size), "Content-Type": "application/octet-stream"},
            )
            return self._send(request)

    def download(self, url: str, target: Path) -> None:
        target.parent.mkdir(parents=True, exist_ok=True)
        request: urllib.request.Request = self._authorized(urllib.request.Request(url, method="GET"))
        descriptor, temporary = tempfile.mkstemp(dir=target.parent, prefix=f".{target.name}.")
        try:
            with self._open(request) as response, os.fdopen(descriptor, "wb") as handle:
                shutil.copyfileobj(response, handle, CHUNK_BYTES)
            os.replace(temporary, target)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    def _send(self, request: urllib.request.Request) -> HttpResponse:
        with self._open(self._authorized(request)) as response:
            return HttpResponse(response.status, response.read(), response.headers)

    def _authorized(self, request: urllib.request.Request) -> urllib.request.Request:
        for name, value in self._headers.items():
            request.add_unredirected_header(name, value)
        return request

    def _open(self, request: urllib.request.Request):  # noqa: ANN202 - urllib returns a private response type
        logger.debug("%s %s", request.get_method(), request.full_url)
        try:
            return urllib.request.urlopen(request, timeout=self._timeout, context=self._ssl_context)
        except HTTPError as failure:
            body: str = failure.read().decode(errors="replace")
            raise self._error_type(failure.code, request.full_url, body) from failure
        except URLError as unreachable:
            raise self._error_type(0, request.full_url, str(unreachable.reason)) from unreachable
