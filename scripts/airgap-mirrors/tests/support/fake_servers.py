import json
import re
import subprocess
import threading
import urllib.parse
from collections.abc import Callable
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

Route = tuple[str, re.Pattern[str], Callable[..., tuple[int, object, dict[str, str]]]]


class FakeServer:
    """A real HTTP server on localhost, so the code under test goes through urllib exactly as in production."""

    def __init__(self) -> None:
        self.routes: list[Route] = []
        self.requests: list[tuple[str, str, dict[str, str]]] = []
        owner: FakeServer = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_: object) -> None:
                return

            def _dispatch(self) -> None:
                owner.requests.append((self.command, self.path, dict(self.headers)))
                length: int = int(self.headers.get("Content-Length") or 0)
                body: bytes = self.rfile.read(length) if length else b""
                split = urllib.parse.urlsplit(self.path)
                path: str = split.path
                query: dict[str, str] = dict(urllib.parse.parse_qsl(split.query))
                for method, pattern, handler in owner.routes:
                    match = pattern.fullmatch(path)
                    if method == self.command and match:
                        status, payload, headers = handler(
                            *match.groups(), body=body, headers=dict(self.headers), query=query
                        )
                        self._reply(status, payload, headers)
                        return
                self._reply(404, {"message": "404 Not Found"}, {})

            def _reply(self, status: int, payload: object, headers: dict[str, str]) -> None:
                data: bytes = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
                self.send_response(status)
                for name, value in headers.items():
                    self.send_header(name, value)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            do_GET = do_PUT = do_POST = do_DELETE = _dispatch  # noqa: N815

        self._server: ThreadingHTTPServer = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url: str = f"http://127.0.0.1:{self._server.server_address[1]}"
        self._thread: threading.Thread = threading.Thread(target=self._server.serve_forever, daemon=True)

    def route(self, method: str, pattern: str, handler: Callable[..., tuple[int, object, dict[str, str]]]) -> None:
        self.routes.append((method, re.compile(pattern), handler))

    def __enter__(self) -> "FakeServer":
        self._thread.start()
        return self

    def __exit__(self, *_: object) -> None:
        self._server.shutdown()
        self._server.server_close()


@dataclass
class FakeProject:
    id: int
    path: str
    repository: Path
    default_branch: str | None = None
    releases: dict[str, dict[str, object]] = field(default_factory=dict)
    links: dict[str, list[dict[str, str]]] = field(default_factory=dict)
    packages: dict[str, bytes] = field(default_factory=dict)
    protected: set[str] = field(default_factory=set)


class FakeGitLab:
    """Answers the GitLab REST calls the import makes. Tags are read from the project's real bare repository,
    the way GitLab reads them from the pushed repository."""

    def __init__(self, server: FakeServer) -> None:
        self.server: FakeServer = server
        self.projects: dict[str, FakeProject] = {}
        project: str = r"/api/v4/projects/([^/]+)"
        server.route("GET", project, self._get_project)
        server.route("PUT", project, self._put_project)
        server.route("GET", project + r"/repository/tags/([^/]+)", self._get_tag)
        server.route("DELETE", project + r"/protected_branches/([^/]+)", self._unprotect)
        server.route("GET", project + r"/releases/([^/]+)", self._get_release)
        server.route("POST", project + r"/releases", self._post_release)
        server.route("GET", project + r"/releases/([^/]+)/assets/links", self._get_links)
        server.route("POST", project + r"/releases/([^/]+)/assets/links", self._post_link)
        server.route("PUT", project + r"/packages/generic/([^/]+)/([^/]+)/([^/]+)", self._put_package)

    def add_project(self, path: str, repository: Path) -> FakeProject:
        subprocess.run(["git", "init", "--bare", "--quiet", str(repository)], check=True)
        created: FakeProject = FakeProject(id=len(self.projects) + 1, path=path, repository=repository)
        self.projects[path] = created
        return created

    def _project(self, encoded: str) -> FakeProject | None:
        return self.projects.get(urllib.parse.unquote(encoded))

    def _get_project(self, encoded: str, **_: object) -> tuple[int, object, dict[str, str]]:
        project: FakeProject | None = self._project(encoded)
        if project is None:
            return 404, {"message": "404 Project Not Found"}, {}
        if project.default_branch is None:
            head: str = subprocess.run(
                ["git", "symbolic-ref", "--quiet", "HEAD"], cwd=project.repository, capture_output=True, text=True
            ).stdout.strip()
            has_branch: bool = (
                subprocess.run(
                    ["git", "rev-parse", "--verify", "--quiet", head], cwd=project.repository, capture_output=True
                ).returncode
                == 0
            )
            if has_branch:
                project.default_branch = head.removeprefix("refs/heads/")
        return (
            200,
            {"id": project.id, "path_with_namespace": project.path, "default_branch": project.default_branch},
            {},
        )

    def _put_project(self, encoded: str, body: bytes, **_: object) -> tuple[int, object, dict[str, str]]:
        project: FakeProject = self.projects[urllib.parse.unquote(encoded)]
        project.default_branch = json.loads(body)["default_branch"]
        subprocess.run(
            ["git", "symbolic-ref", "HEAD", f"refs/heads/{project.default_branch}"], cwd=project.repository, check=True
        )
        return 200, {"id": project.id, "default_branch": project.default_branch}, {}

    def _unprotect(self, encoded: str, branch: str, **_: object) -> tuple[int, object, dict[str, str]]:
        project: FakeProject = self.projects[urllib.parse.unquote(encoded)]
        name: str = urllib.parse.unquote(branch)
        if name not in project.protected:
            return 404, {"message": "404 Not found"}, {}
        project.protected.discard(name)
        return 204, b"", {}

    def _get_tag(self, encoded: str, tag: str, **_: object) -> tuple[int, object, dict[str, str]]:
        project: FakeProject = self.projects[urllib.parse.unquote(encoded)]
        name: str = urllib.parse.unquote(tag)
        found: bool = (
            subprocess.run(
                ["git", "rev-parse", "--verify", "--quiet", f"refs/tags/{name}"],
                cwd=project.repository,
                capture_output=True,
            ).returncode
            == 0
        )
        return (200, {"name": name}, {}) if found else (404, {"message": "404 Tag Not Found"}, {})

    def _get_release(self, encoded: str, tag: str, **_: object) -> tuple[int, object, dict[str, str]]:
        release: dict[str, object] | None = self.projects[urllib.parse.unquote(encoded)].releases.get(
            urllib.parse.unquote(tag)
        )
        return (200, release, {}) if release else (404, {"message": "404 Not Found"}, {})

    def _post_release(self, encoded: str, body: bytes, **_: object) -> tuple[int, object, dict[str, str]]:
        release: dict[str, object] = json.loads(body)
        self.projects[urllib.parse.unquote(encoded)].releases[str(release["tag_name"])] = release
        return 201, release, {}

    def _get_links(self, encoded: str, tag: str, **_: object) -> tuple[int, object, dict[str, str]]:
        return 200, self.projects[urllib.parse.unquote(encoded)].links.get(urllib.parse.unquote(tag), []), {}

    def _post_link(self, encoded: str, tag: str, body: bytes, **_: object) -> tuple[int, object, dict[str, str]]:
        link: dict[str, str] = json.loads(body)
        self.projects[urllib.parse.unquote(encoded)].links.setdefault(urllib.parse.unquote(tag), []).append(link)
        return 201, link, {}

    def _put_package(
        self, encoded: str, package: str, version: str, file_name: str, body: bytes, **_: object
    ) -> tuple[int, object, dict[str, str]]:
        key: str = "/".join(urllib.parse.unquote(part) for part in (package, version, file_name))
        self.projects[urllib.parse.unquote(encoded)].packages[key] = body
        return 201, {"message": "201 Created"}, {}


class FakeGitHub:
    """Answers the releases listing (two to a page, to exercise pagination) and serves the release files."""

    def __init__(self, server: FakeServer) -> None:
        self.server: FakeServer = server
        self.releases: dict[str, list[dict[str, object]]] = {}
        self.files: dict[str, bytes] = {}
        server.route("GET", r"/repos/([^/]+)/([^/]+)/releases", self._list)
        server.route("GET", r"/files/(.+)", self._file)

    def add_release(
        self, repository: str, tag: str, published_at: str, files: dict[str, bytes], *, draft: bool = False
    ) -> None:
        assets: list[dict[str, object]] = []
        for name, content in files.items():
            self.files[f"{tag}/{name}"] = content
            assets.append(
                {"name": name, "size": len(content), "browser_download_url": f"{self.server.url}/files/{tag}/{name}"}
            )
        self.releases.setdefault(repository, []).append(
            {
                "tag_name": tag,
                "name": f"Release {tag}",
                "body": f"notes for {tag}",
                "published_at": published_at,
                "draft": draft,
                "assets": assets,
            }
        )

    page_size: int = 2

    def _list(self, owner: str, name: str, query: dict[str, str], **_: object) -> tuple[int, object, dict[str, str]]:
        page: int = int(query.get("page", "1"))
        everything: list[dict[str, object]] = self.releases.get(f"{owner}/{name}", [])
        start: int = (page - 1) * self.page_size
        headers: dict[str, str] = {}
        if start + self.page_size < len(everything):
            headers["Link"] = f'<{self.server.url}/repos/{owner}/{name}/releases?page={page + 1}>; rel="next"'
        return 200, everything[start : start + self.page_size], headers

    def _file(self, key: str, **_: object) -> tuple[int, object, dict[str, str]]:
        content: bytes | None = self.files.get(key)
        return (200, content, {}) if content is not None else (404, b"", {})
