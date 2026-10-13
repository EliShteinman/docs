"""The sandbox user's rules from files/sandbox.acl, evaluated without a Redis.

Redis reads a user's rules left to right, and the last rule that reaches a
command decides: by its name, by its parent's name for a subcommand, or by a
category it belongs to. That is all this reproduces — enough to say, from a
command's ACL categories, whether the sandbox lets a reader run it.
test_acl.py holds the evaluation to a live Redis over every Try it command.
"""

# Granted by the deployment's postStart hook once the modules are loaded,
# because Redis parses the ACL file first and rejects any module command in it.
MODULE_GRANTS = ("+ft._list", "+ft.dropindex", "+ft.tagvals")

# Refused by the proxy itself, since no ACL rule can deny RESET. Mirrors
# PROXY_DENIED in helm/cli-proxy/main.py.
PROXY_DENIED = frozenset({"RESET"})


class SandboxAcl:
    def __init__(self, rules: list[str]) -> None:
        self._rules = [rule.lower() for rule in rules if rule[:1] in ("+", "-")]

    @classmethod
    def from_acl_file(cls, text: str, user: str) -> "SandboxAcl":
        for line in text.splitlines():
            words = line.split()
            if words[:2] == ["user", user]:
                return cls(words[2:] + list(MODULE_GRANTS))
        raise ValueError(f"no rules for user {user!r} in the ACL file")

    def allows(self, command: str, categories: frozenset[str]) -> bool:
        if command.upper() in PROXY_DENIED:
            return False
        name = command.lower().replace(" ", "|")
        parent = name.split("|")[0]
        lowered = {category.lower() for category in categories}

        allowed = False
        for rule in self._rules:
            target = rule[1:]
            if target == "@all" or target in lowered or target in (name, parent):
                allowed = rule.startswith("+")
        return allowed