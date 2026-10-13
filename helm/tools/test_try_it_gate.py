import os
import subprocess
import sys

import pytest

import try_it_gate
from command_catalog import CommandCatalog
from sandbox_acl import SandboxAcl

GATE = os.path.join(os.path.dirname(__file__), "try_it_gate.py")

CATALOG = CommandCatalog({
    "GET": frozenset({"@read"}),
    "ROLE": frozenset({"@admin", "@dangerous"}),
    "HOTKEYS START": frozenset({"@admin", "@dangerous"}),
    "HOTKEYS GET": frozenset({"@admin", "@dangerous"}),
    "HOTKEYS STOP": frozenset({"@admin", "@dangerous"}),
    "HOTKEYS RESET": frozenset({"@admin", "@dangerous"}),
})
ACL = SandboxAcl(["+@all", "-@admin", "-@dangerous"])

HOTKEYS_PAGE = """{{< clients-example set="h" step="h" >}}
> HOTKEYS START METRICS 1 NET
> HOTKEYS GET
> HOTKEYS STOP
> HOTKEYS RESET
{{< /clients-example >}}"""
ROLE_PAGE = "{{% redis-cli %}}\nredis> ROLE\n{{% /redis-cli %}}"
GET_PAGE = "{{% redis-cli %}}\nredis> GET k\n{{% /redis-cli %}}"


def test_a_command_redis_io_refuses_too_is_not_reported():
    report = try_it_gate.evaluate({"content/commands/hotkeys.md": HOTKEYS_PAGE}, CATALOG, ACL)

    assert report.clean


def test_an_unchecked_refused_command_is_reported_with_its_page():
    pages = {"content/commands/hotkeys.md": HOTKEYS_PAGE, "content/commands/role.md": ROLE_PAGE}

    report = try_it_gate.evaluate(pages, CATALOG, ACL)

    assert report.newly_refused == {"ROLE": {"content/commands/role.md"}}


def test_a_blocked_entry_no_page_runs_is_reported_as_stale():
    report = try_it_gate.evaluate({"content/commands/get.md": GET_PAGE}, CATALOG, ACL)

    assert report.stale == {"HOTKEYS START", "HOTKEYS GET", "HOTKEYS STOP", "HOTKEYS RESET"}


@pytest.mark.parametrize(
    "path,url",
    [
        ("content/commands/role.md", "https://redis.io/docs/latest/commands/role/"),
        ("content/develop/data-types/_index.md", "https://redis.io/docs/latest/develop/data-types/"),
        ("content/develop/reference/eviction/index.md",
         "https://redis.io/docs/latest/develop/reference/eviction/"),
    ],
)
def test_redis_io_url(path, url):
    assert try_it_gate.redis_io_url(path) == url


def test_the_report_names_the_page_to_check():
    pages = {"content/commands/hotkeys.md": HOTKEYS_PAGE, "content/commands/role.md": ROLE_PAGE}

    rendered = try_it_gate.render(try_it_gate.evaluate(pages, CATALOG, ACL))

    assert "https://redis.io/docs/latest/commands/role/" in rendered


def test_the_repository_has_no_unchecked_try_it_command():
    """End to end, as it runs before a merge: over this checkout's own content."""
    result = subprocess.run([sys.executable, GATE], capture_output=True, text=True)

    assert result.returncode == 0, result.stdout


def test_a_commit_is_read_without_checking_it_out():
    result = subprocess.run([sys.executable, GATE, "HEAD"], capture_output=True, text=True)

    assert result.returncode == 0, result.stdout
