"""Before an upstream merge: the Try it commands the sandbox would newly refuse.

    python3 helm/tools/try_it_gate.py [<commit>]

Reads content/ at <commit>, or the working tree when it is left out, and the
sandbox ACL from the working tree. Lists every Try it command the ACL refuses
that DELIBERATELY_BLOCKED (try_it.py) does not already name, each with the
redis.io page that runs it. Open that page and press Try it:

  - "no permissions" there: redis.io refuses it too. Add it to
    DELIBERATELY_BLOCKED, and the sandbox behaves exactly as redis.io does.
  - A real answer there: grant it in helm/redis-docs/files/sandbox.acl, as
    +role was, so the reader's button works as it does on redis.io.

Both in the same merge, so the tests never meet a command nobody has checked.
Also lists DELIBERATELY_BLOCKED entries no Try it runs any more. Exits 1 when
either list has anything in it.
"""

import os
import sys
from dataclasses import dataclass, field

sys.path.insert(0, os.path.dirname(__file__))

from command_catalog import CommandCatalog  # noqa: E402
from sandbox_acl import SandboxAcl  # noqa: E402
from source_tree import GitTree, WorkingTree  # noqa: E402
from try_it import DELIBERATELY_BLOCKED, SHORTCODE_NAMES, try_it_lines  # noqa: E402

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ACL_FILE = os.path.join(REPO, "helm", "redis-docs", "files", "sandbox.acl")
SANDBOX_USER = "docsandbox"
REDIS_IO_DOCS = "https://redis.io/docs/latest/"


@dataclass
class GateReport:
    newly_refused: dict[str, set[str]] = field(default_factory=dict)
    stale: set[str] = field(default_factory=set)

    @property
    def clean(self) -> bool:
        return not self.newly_refused and not self.stale


def evaluate(pages: dict[str, str], catalog: CommandCatalog, acl: SandboxAcl) -> GateReport:
    refused: dict[str, set[str]] = {}
    for path, text in pages.items():
        for line in try_it_lines(text):
            command = catalog.resolve(line)
            if command and not acl.allows(command, catalog.categories(command)):
                refused.setdefault(command, set()).add(path)

    return GateReport(
        newly_refused={c: p for c, p in refused.items() if c not in DELIBERATELY_BLOCKED},
        stale=set(DELIBERATELY_BLOCKED) - set(refused),
    )


def redis_io_url(path: str) -> str:
    page = path.removeprefix("content/").removesuffix(".md")
    for index in ("_index", "index"):
        if page == index or page.endswith("/" + index):
            page = page[: -len(index)]
    page = page.rstrip("/")
    return REDIS_IO_DOCS + (page + "/" if page else "")


def render(report: GateReport) -> str:
    if report.clean:
        return "Try it gate: every Try it command the sandbox refuses is one redis.io refuses too."

    lines: list[str] = []
    if report.newly_refused:
        lines.append("The sandbox would refuse these Try it commands, and nobody has checked redis.io:")
        for command in sorted(report.newly_refused):
            lines.append(f"  {command}")
            for path in sorted(report.newly_refused[command]):
                lines.append(f"    {redis_io_url(path)}  ({path})")
        lines.append("Press Try it on each page. \"no permissions\" there: add the command to")
        lines.append("DELIBERATELY_BLOCKED in helm/tools/try_it.py. A real answer there: grant it")
        lines.append("in helm/redis-docs/files/sandbox.acl.")
    if report.stale:
        lines.append("No Try it runs these any more; remove them from DELIBERATELY_BLOCKED:")
        lines.extend(f"  {command}" for command in sorted(report.stale))
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    tree = GitTree(REPO, argv[0]) if argv else WorkingTree(REPO)
    catalog = CommandCatalog.from_pages(list(tree.markdown("content/commands").values()))
    with open(ACL_FILE, encoding="utf-8") as handle:
        acl = SandboxAcl.from_acl_file(handle.read(), SANDBOX_USER)

    report = evaluate(tree.markdown("content", containing=SHORTCODE_NAMES), catalog, acl)
    print(render(report))
    return 0 if report.clean else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
