import os

import pytest

from sandbox_acl import SandboxAcl

ACL_FILE = os.path.join(os.path.dirname(__file__), "..", "redis-docs", "files", "sandbox.acl")

ADMIN = frozenset({"@admin", "@dangerous"})
PLAIN = frozenset({"@read", "@fast"})


@pytest.fixture(scope="module")
def sandbox() -> SandboxAcl:
    with open(ACL_FILE, encoding="utf-8") as handle:
        return SandboxAcl.from_acl_file(handle.read(), "docsandbox")


@pytest.mark.parametrize(
    "rules,command,categories,expected",
    [
        (["+@all"], "GET", PLAIN, True),
        (["+@all", "-@admin"], "ROLE", ADMIN, False),
        (["+@all", "-@admin", "+role"], "ROLE", ADMIN, True),
        (["+@all", "-@admin", "+hotkeys"], "HOTKEYS START", ADMIN, True),
        (["+@all", "-script|flush"], "SCRIPT FLUSH", PLAIN, False),
        (["+@all", "-script|flush"], "SCRIPT LOAD", PLAIN, True),
        (["-@all"], "GET", PLAIN, False),
        (["+@all"], "RESET", PLAIN, False),
    ],
    ids=["all", "category-deny", "name-grant", "parent-grant", "subcommand-deny",
         "sibling-untouched", "nothing", "proxy-denied"],
)
def test_allows(rules, command, categories, expected):
    assert SandboxAcl(rules).allows(command, categories) is expected


def test_unknown_user_is_an_error():
    with pytest.raises(ValueError):
        SandboxAcl.from_acl_file("user default on +@all", "docsandbox")


def test_the_real_file_grants_role(sandbox):
    assert sandbox.allows("ROLE", ADMIN)


def test_the_real_file_refuses_hotkeys(sandbox):
    assert not sandbox.allows("HOTKEYS START", ADMIN)


def test_the_real_file_grants_the_module_commands(sandbox):
    assert sandbox.allows("FT.DROPINDEX", frozenset({"@dangerous", "@search"}))
