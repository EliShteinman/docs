"""Markdown files read from the working tree or from a git commit, the same way.

A commit is how an upstream pull request is judged before it is merged: its
files are read straight out of git, so nothing is checked out or merged to look.
"""

import os
import re
import subprocess


class WorkingTree:
    def __init__(self, root: str) -> None:
        self._root = root

    def markdown(self, directory: str, containing: str | None = None) -> dict[str, str]:
        pattern = re.compile(containing) if containing else None
        files: dict[str, str] = {}
        for dirpath, _, names in os.walk(os.path.join(self._root, directory)):
            for name in names:
                if not name.endswith(".md"):
                    continue
                path = os.path.join(dirpath, name)
                with open(path, encoding="utf-8", errors="replace") as handle:
                    text = handle.read()
                if pattern is None or pattern.search(text):
                    files[os.path.relpath(path, self._root)] = text
        return files


class GitTree:
    def __init__(self, root: str, ref: str) -> None:
        self._root = root
        self._ref = ref

    def markdown(self, directory: str, containing: str | None = None) -> dict[str, str]:
        if containing:
            listed = self._git("grep", "-l", "-E", containing, self._ref, "--", directory)
            paths = [line.split(":", 1)[1] for line in listed.splitlines()]
        else:
            paths = self._git("ls-tree", "-r", "--name-only", self._ref, "--", directory).splitlines()
        return self._read([path for path in paths if path.endswith(".md")])

    def _read(self, paths: list[str]) -> dict[str, str]:
        if not paths:
            return {}
        request = "".join(f"{self._ref}:{path}\n" for path in paths).encode()
        output = subprocess.run(
            ["git", "-C", self._root, "cat-file", "--batch"],
            input=request, capture_output=True, check=True,
        ).stdout

        files: dict[str, str] = {}
        position = 0
        for path in paths:
            header_end = output.index(b"\n", position)
            size = int(output[position:header_end].split()[2])
            start = header_end + 1
            files[path] = output[start:start + size].decode("utf-8", errors="replace")
            position = start + size + 1
        return files

    def _git(self, *args: str) -> str:
        result = subprocess.run(
            ["git", "-C", self._root, *args], capture_output=True, text=True,
        )
        # git grep exits 1 when nothing matches, which is an answer, not a failure.
        if result.returncode not in (0, 1):
            raise RuntimeError(result.stderr.strip())
        return result.stdout