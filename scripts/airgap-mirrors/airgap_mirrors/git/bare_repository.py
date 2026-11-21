import logging
from pathlib import Path

from airgap_mirrors.exceptions import GitCommandError
from airgap_mirrors.git.git_runner import GitRunner

logger: logging.Logger = logging.getLogger(__name__)

BRANCHES: str = "refs/heads/"
TAGS: str = "refs/tags/"
INCOMING: str = "refs/airgap-incoming/"
SEED_REMOTE: str = "gitlab"
BRANCHES_AND_TAGS: list[str] = ["+refs/heads/*:refs/heads/*", "+refs/tags/*:refs/tags/*"]


class BareRepository:
    """A bare git repository holding branches and tags only: no pull requests, no working tree."""

    def __init__(self, path: Path, git: GitRunner) -> None:
        self.path: Path = path
        self._git: GitRunner = git

    def exists(self) -> bool:
        return (self.path / "HEAD").is_file()

    def create(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._git.run(["init", "--bare", "--quiet", str(self.path)])
        logger.info("created %s", self.path)

    def track_upstream(self, url: str) -> None:
        if self._git.succeeds(["remote", "get-url", "origin"], cwd=self.path):
            self._run(["remote", "set-url", "origin", url])
        else:
            self._run(["remote", "add", "origin", url])
        self._run(["config", "--unset-all", "remote.origin.fetch"], tolerate_missing=True)
        for refspec in BRANCHES_AND_TAGS:
            self._run(["config", "--add", "remote.origin.fetch", refspec])
        self._run(["config", "remote.origin.tagOpt", "--no-tags"])

    def seed_tips_from(self, url: str) -> None:
        """Takes only the newest commit of each branch and tag, without file contents: enough for a bundle that
        builds on them to apply. Anything else a later step needs, git fetches from this remote on demand."""
        self._run(["remote", "add", SEED_REMOTE, url])
        for refspec in BRANCHES_AND_TAGS:
            self._run(["config", "--add", f"remote.{SEED_REMOTE}.fetch", refspec])
        self._run(["config", f"remote.{SEED_REMOTE}.tagOpt", "--no-tags"])
        self._run(["fetch", "--quiet", "--depth=1", "--filter=blob:none", SEED_REMOTE])

    def fetch_upstream(self) -> None:
        self._run(["fetch", "--prune", "--quiet", "origin"])

    def upstream_default_branch(self) -> str:
        for line in self._run(["ls-remote", "--symref", "origin", "HEAD"]).splitlines():
            if line.startswith("ref: ") and line.endswith("\tHEAD"):
                return line.removeprefix("ref: ").removesuffix("\tHEAD").removeprefix(BRANCHES)
        raise GitCommandError(["ls-remote", "--symref", "origin", "HEAD"], 0, "upstream did not name a default branch")

    def point_head_at(self, branch: str) -> None:
        self._run(["symbolic-ref", "HEAD", f"{BRANCHES}{branch}"])

    def branch_and_tag_tips(self) -> dict[str, str]:
        output: str = self._run(["for-each-ref", "--format=%(objectname) %(refname)", BRANCHES, TAGS])
        tips: dict[str, str] = {}
        for line in output.splitlines():
            object_id, ref_name = line.split(" ", 1)
            tips[ref_name] = object_id
        return tips

    def drop_refs_outside_branches_and_tags(self) -> None:
        stray: list[str] = [
            ref_name
            for ref_name in self._run(["for-each-ref", "--format=%(refname)"]).splitlines()
            if not ref_name.startswith((BRANCHES, TAGS))
        ]
        if stray:
            logger.info("%s: dropping %d refs that are not branches or tags", self.path.name, len(stray))
            self._run(["update-ref", "--stdin"], stdin="".join(f"delete {ref_name}\n" for ref_name in stray))

    def has_object(self, object_id: str) -> bool:
        return self._git.succeeds(["cat-file", "-e", object_id], cwd=self.path)

    def missing_objects(self, object_ids: set[str]) -> set[str]:
        return {object_id for object_id in object_ids if not self.has_object(object_id)}

    def has_objects_beyond(self, ref_names: list[str], known_object_ids: list[str]) -> bool:
        listing: str = self._run(["rev-list", "--objects", "--stdin"], stdin=_revisions(ref_names, known_object_ids))
        return bool(listing.strip())

    def create_bundle(self, target: Path, ref_names: list[str], known_object_ids: list[str]) -> None:
        target.parent.mkdir(parents=True, exist_ok=True)
        self._run(
            ["bundle", "create", "--quiet", str(target), "--stdin"], stdin=_revisions(ref_names, known_object_ids)
        )

    def verify_bundle(self, bundle: Path) -> None:
        self._run(["bundle", "verify", "--quiet", str(bundle)])

    def unpack_bundle(self, bundle: Path) -> None:
        self._run(["fetch", "--quiet", "--no-tags", str(bundle), f"+refs/*:{INCOMING}*"])
        incoming: list[str] = self._run(["for-each-ref", "--format=%(refname)", INCOMING]).splitlines()
        if incoming:
            self._run(["update-ref", "--stdin"], stdin="".join(f"delete {ref_name}\n" for ref_name in incoming))

    def set_branches_and_tags(self, tips: dict[str, str]) -> None:
        current: dict[str, str] = self.branch_and_tag_tips()
        commands: list[str] = [f"delete {ref_name}\n" for ref_name in current if ref_name not in tips]
        commands += [f"update {ref_name} {object_id}\n" for ref_name, object_id in tips.items()]
        self._run(["update-ref", "--stdin"], stdin="".join(commands))

    def push(self, url: str, refspecs: list[str], *, prune: bool = False) -> None:
        arguments: list[str] = ["push", "--quiet", "--porcelain"]
        if prune:
            arguments.append("--prune")
        self._run([*arguments, url, *refspecs])

    def _run(self, arguments: list[str], *, stdin: str | None = None, tolerate_missing: bool = False) -> str:
        try:
            return self._git.run(arguments, cwd=self.path, stdin=stdin)
        except GitCommandError as failure:
            if tolerate_missing and failure.returncode == 5:
                return ""
            raise


def _revisions(ref_names: list[str], known_object_ids: list[str]) -> str:
    return "".join(f"{name}\n" for name in ref_names) + "".join(f"^{object_id}\n" for object_id in known_object_ids)
