import logging

from airgap_mirrors.exceptions import ConfigurationError
from airgap_mirrors.internal.gitlab_client import GitLabClient, GitLabGroup, GitLabProject
from airgap_mirrors.settings import InternalRepoSpec, ProjectVisibility

logger: logging.Logger = logging.getLogger(__name__)


class ProjectProvisioner:
    """Makes sure a repository has its GitLab project before anything is pushed to it.

    A missing project is created empty and read-only in spirit: no issues, merge requests, wiki or
    snippets, since everything in it comes from GitHub. Missing subgroups on the way are created too.
    The top group itself must already exist: creating a top-level group is an administrator's call."""

    def __init__(self, gitlab: GitLabClient, visibility: ProjectVisibility | None) -> None:
        self._gitlab: GitLabClient = gitlab
        self._visibility: str | None = visibility.value if visibility else None
        self._groups: dict[str, GitLabGroup] = {}

    def ensure_project(self, spec: InternalRepoSpec, upstream_url: str) -> GitLabProject:
        existing: GitLabProject | None = self._gitlab.project(spec.gitlab_path)
        if existing is not None:
            return existing
        group_path, _, project_name = spec.gitlab_path.rpartition("/")
        group: GitLabGroup = self._ensure_group(group_path)
        created: GitLabProject = self._gitlab.create_project(
            group.id, project_name, f"Copy of {upstream_url}, kept in sync from outside", self._visibility
        )
        logger.info("%s: created GitLab project %s", spec.name, spec.gitlab_path)
        return created

    def _ensure_group(self, group_path: str) -> GitLabGroup:
        if group_path in self._groups:
            return self._groups[group_path]
        group: GitLabGroup | None = self._gitlab.group(group_path)
        if group is None:
            group = self._create_group(group_path)
        self._groups[group_path] = group
        return group

    def _create_group(self, group_path: str) -> GitLabGroup:
        parent_path, _, name = group_path.rpartition("/")
        if not parent_path:
            raise ConfigurationError(
                f"GitLab has no group {group_path!r}. Create it (or ask a GitLab administrator to), "
                "then run import again; subgroups and projects inside it are created automatically."
            )
        parent: GitLabGroup = self._ensure_group(parent_path)
        created: GitLabGroup = self._gitlab.create_group(name, parent.id, self._visibility)
        logger.info("created GitLab group %s", group_path)
        return created
