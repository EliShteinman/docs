import subprocess
from pathlib import Path


def git(*arguments: str, cwd: Path | None = None) -> str:
    completed = subprocess.run(["git", *arguments], cwd=cwd, capture_output=True, text=True, check=True)
    return completed.stdout.strip()


class UpstreamRepository:
    """Stands in for a GitHub repository: a bare repository served over file://, plus a clone to commit from."""

    def __init__(self, root: Path, owner: str, name: str, default_branch: str = "main") -> None:
        self.bare: Path = root / owner / name
        self.work: Path = root / "_work" / owner / name
        self.bare.mkdir(parents=True)
        git("init", "--bare", "--quiet", f"--initial-branch={default_branch}", str(self.bare))
        self.work.mkdir(parents=True)
        git("init", "--quiet", f"--initial-branch={default_branch}", str(self.work))
        git("config", "user.email", "test@example.com", cwd=self.work)
        git("config", "user.name", "Test", cwd=self.work)
        git("remote", "add", "origin", str(self.bare), cwd=self.work)
        self.commit(default_branch, "README.md", "first")

    def commit(self, branch: str, file_name: str, content: str) -> str:
        if git("branch", "--list", branch, cwd=self.work):
            git("checkout", "--quiet", branch, cwd=self.work)
        else:
            git("checkout", "--quiet", "-b", branch, cwd=self.work)
        (self.work / file_name).write_text(content)
        git("add", file_name, cwd=self.work)
        git("commit", "--quiet", "-m", f"{branch}: {file_name}", cwd=self.work)
        git("push", "--quiet", "--force", "origin", branch, cwd=self.work)
        return git("rev-parse", "HEAD", cwd=self.work)

    def tag(self, name: str, *, annotated: bool = True) -> None:
        if annotated:
            git("tag", "-a", name, "-m", name, cwd=self.work)
        else:
            git("tag", name, cwd=self.work)
        git("push", "--quiet", "origin", f"refs/tags/{name}", cwd=self.work)

    def delete_branch(self, branch: str) -> None:
        git("push", "--quiet", "origin", f":refs/heads/{branch}", cwd=self.work)

    def set_default_branch(self, branch: str) -> None:
        git("symbolic-ref", "HEAD", f"refs/heads/{branch}", cwd=self.bare)

    def pull_request_ref(self, number: int, object_id: str) -> None:
        git("update-ref", f"refs/pull/{number}/head", object_id, cwd=self.bare)

    def refs(self) -> dict[str, str]:
        output: str = git("for-each-ref", "--format=%(objectname) %(refname)", "refs/heads", "refs/tags", cwd=self.bare)
        return {name: object_id for object_id, name in (line.split(" ", 1) for line in output.splitlines())}
