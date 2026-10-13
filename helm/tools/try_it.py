"""What a reader can run from a docs page's "Try it" button.

Two shortcodes put the button on a page: clients-example, unless the author
marked it runnable="false", and redis-cli. Both run the lines that open with a
"> " or "redis> " prompt — the rule layouts/shortcodes/redis-cli.html and
layouts/partials/tabbed-clients-example.html apply. A command in a plain code
block is text a reader cannot run, so nothing here looks at one.
"""

import re

# A self-closing clients-example has no body and no button; the lookbehind keeps
# its opener from pairing with the next block's closing tag.
TRY_IT_BLOCK = re.compile(
    r"\{\{[<%]\s*(clients-example|redis-cli)\b([^{}]*?)(?<!/)\s*[>%]\}\}(.*?)\{\{[<%]\s*/\1\s*[>%]\}\}",
    re.DOTALL,
)
PROMPT_LINE = re.compile(r"^ *(?:redis> |> )(.+)$", re.MULTILINE)
SHORTCODE_NAMES = "clients-example|redis-cli"

# Try it commands the sandbox refuses on purpose, because redis.io's sandbox
# refuses them too. Each one was seen answering "no permissions" from the Try it
# button on its redis.io page; helm/tools/try_it_gate.py says how to check a new
# one before it is added.
DELIBERATELY_BLOCKED = frozenset({"HOTKEYS START", "HOTKEYS GET", "HOTKEYS STOP", "HOTKEYS RESET"})


def try_it_lines(markdown: str) -> list[str]:
    lines: list[str] = []
    for _, params, body in TRY_IT_BLOCK.findall(markdown):
        if 'runnable="false"' in params:
            continue
        lines.extend(line.strip() for line in PROMPT_LINE.findall(body))
    return lines
