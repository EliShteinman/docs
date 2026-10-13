"""Each Redis command's ACL categories, read from its page under content/commands.

The page is the one place a new command's categories exist before the Redis
that runs it does, which is what lets try_it_gate.py judge an upstream change
on the day it lands.
"""

import re

import yaml

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---", re.DOTALL)


class CommandCatalog:
    def __init__(self, categories: dict[str, frozenset[str]]) -> None:
        self._categories = categories

    @classmethod
    def from_pages(cls, pages: list[str]) -> "CommandCatalog":
        categories: dict[str, frozenset[str]] = {}
        for page in pages:
            match = FRONTMATTER.match(page)
            if not match:
                continue
            try:
                frontmatter = yaml.safe_load(match.group(1))
            except yaml.YAMLError:
                continue
            if not isinstance(frontmatter, dict) or "acl_categories" not in frontmatter:
                continue
            title = str(frontmatter.get("title") or "").strip().upper()
            if title:
                categories[title] = frozenset(frontmatter["acl_categories"] or [])
        return cls(categories)

    def resolve(self, command_line: str) -> str | None:
        """The command a line runs, with its subcommand when it has one."""
        words = command_line.upper().split()
        if len(words) > 1 and f"{words[0]} {words[1]}" in self._categories:
            return f"{words[0]} {words[1]}"
        if words and words[0] in self._categories:
            return words[0]
        return None

    def categories(self, command: str) -> frozenset[str]:
        return self._categories[command]