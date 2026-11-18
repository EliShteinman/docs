import logging
import urllib.parse
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from airgap_mirrors.http import HttpClient, HttpResponse
from airgap_mirrors.models import ReleaseRecord

logger: logging.Logger = logging.getLogger(__name__)


class GitLabProject(BaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True)

    id: int
    path_with_namespace: str
    default_branch: str | None = None
    web_url: str | None = None


class GitLabGroup(BaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True)

    id: int
    full_path: str


READ_ONLY_COPY: dict[str, object] = {
    "initialize_with_readme": False,
    "issues_access_level": "disabled",
    "merge_requests_access_level": "disabled",
    "wiki_access_level": "disabled",
    "snippets_access_level": "disabled",
    "package_registry_access_level": "enabled",
}


class GitLabClient:
    """The few GitLab REST calls the import needs. Projects are addressed by their path."""

    def __init__(self, http: HttpClient) -> None:
        self._http: HttpClient = http

    def project(self, project_path: str) -> GitLabProject | None:
        response: HttpResponse | None = self._http.get_or_none(_project(project_path))
        return GitLabProject.model_validate(response.json()) if response else None

    def group(self, group_path: str) -> GitLabGroup | None:
        response: HttpResponse | None = self._http.get_or_none(f"groups/{_segment(group_path)}")
        return GitLabGroup.model_validate(response.json()) if response else None

    def create_group(self, name: str, parent_id: int, visibility: str | None) -> GitLabGroup:
        payload: dict[str, object] = {"name": name, "path": name, "parent_id": parent_id}
        if visibility:
            payload["visibility"] = visibility
        return GitLabGroup.model_validate(self._http.send_json("POST", "groups", payload).json())

    def create_project(self, namespace_id: int, name: str, description: str, visibility: str | None) -> GitLabProject:
        payload: dict[str, object] = {
            "name": name,
            "path": name,
            "namespace_id": namespace_id,
            "description": description,
            **READ_ONLY_COPY,
        }
        if visibility:
            payload["visibility"] = visibility
        return GitLabProject.model_validate(self._http.send_json("POST", "projects", payload).json())

    def set_default_branch(self, project_path: str, branch: str) -> None:
        self._http.send_json("PUT", _project(project_path), {"default_branch": branch})

    def unprotect_branch(self, project_path: str, branch: str) -> bool:
        return self._http.delete_if_present(f"{_project(project_path)}/protected_branches/{_segment(branch)}")

    def tag_exists(self, project_path: str, tag: str) -> bool:
        return self._http.get_or_none(f"{_project(project_path)}/repository/tags/{_segment(tag)}") is not None

    def release_exists(self, project_path: str, tag: str) -> bool:
        return self._http.get_or_none(f"{_project(project_path)}/releases/{_segment(tag)}") is not None

    def create_release(self, project_path: str, release: ReleaseRecord) -> None:
        payload: dict[str, object] = {
            "tag_name": release.tag_name,
            "name": release.title,
            "description": release.body or "",
        }
        if release.published_at:
            payload["released_at"] = release.published_at.isoformat()
        self._http.send_json("POST", f"{_project(project_path)}/releases", payload)

    def release_link_names(self, project_path: str, tag: str) -> set[str]:
        response: HttpResponse = self._http.get(
            f"{_project(project_path)}/releases/{_segment(tag)}/assets/links", {"per_page": 100}
        )
        links: object = response.json()
        return {link["name"] for link in links} if isinstance(links, list) else set()

    def upload_package_file(self, project_path: str, package: str, version: str, source: Path) -> str:
        path: str = (
            f"{_project(project_path)}/packages/generic/{_segment(package)}/{_segment(version)}/{_segment(source.name)}"
        )
        self._http.upload_file(path, source)
        return self._http.url(path)

    def link_release_file(self, project_path: str, tag: str, file_name: str, url: str) -> None:
        self._http.send_json(
            "POST",
            f"{_project(project_path)}/releases/{_segment(tag)}/assets/links",
            {"name": file_name, "url": url, "direct_asset_path": f"/{file_name}", "link_type": "package"},
        )


def _project(project_path: str) -> str:
    return f"projects/{_segment(project_path)}"


def _segment(value: str) -> str:
    return urllib.parse.quote(value, safe="")
