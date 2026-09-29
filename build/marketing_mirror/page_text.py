"""The prose of a captured page, for pages redis.io publishes no Markdown for.

redis.io serves `<path>.md` for the blog, tutorials, glossary and solutions,
but not for comparisons, customer stories, technology guides or architecture
diagrams. Their text is in the rendered HTML instead -- in <main>, or, where
Next.js streamed it, in the hidden `<div hidden id="S:n">` blocks it moves into
place in the browser. Both lie outside the header, menus and footer, so reading
only them reads the page and nothing around it.

The result is Markdown-shaped: ## before each h2 and h3, so feed.sections()
splits it the way it splits real Markdown.
"""

from __future__ import annotations

import html
import re
from html.parser import HTMLParser

_MAIN = re.compile(r"<main[^>]*>(.*?)</main>", re.DOTALL)
_STREAMED = re.compile(r'<div hidden id="S:[^"]*">(.*?)</div><script', re.DOTALL)
_TITLE = re.compile(r"<title>([^<]*)</title>")
_OG_TITLE = re.compile(r'<meta property="og:title" content="([^"]*)"')
_H1 = re.compile(r"<h1[^>]*>(.*?)</h1>", re.DOTALL)
_TAG = re.compile(r"<[^>]+>")
_BLANK_LINES = re.compile(r"[ \t]*\n[ \t\n]*")

_SKIPPED = frozenset(
    {"script", "style", "svg", "noscript", "template", "button", "select", "form"}
)
_VOID = frozenset(
    {
        "br",
        "img",
        "meta",
        "link",
        "input",
        "hr",
        "source",
        "wbr",
        "area",
        "col",
        "embed",
        "param",
        "track",
    }
)
_HEADINGS = frozenset({"h2", "h3"})
_BLOCKS = frozenset({"p", "li", "h1", "h4", "h5", "tr", "blockquote"})
_TITLE_SUFFIX = " | Redis"


class _TextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._open: list[str] = []
        self._skipping = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in _VOID:
            return
        self._open.append(tag)
        if tag in _SKIPPED:
            self._skipping += 1
        elif not self._skipping and tag in _HEADINGS:
            self.parts.append("\n\n## ")
        elif not self._skipping and tag in _BLOCKS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in _VOID:
            return
        while self._open:
            closed = self._open.pop()
            if closed in _SKIPPED:
                self._skipping -= 1
            if closed == tag:
                return

    def handle_data(self, data: str) -> None:
        if not self._skipping and data.strip():
            self.parts.append(" ".join(data.split()) + " ")


def content(page_html: str) -> str:
    """The page's own text, headings marked with ##; "" when it has none."""
    parser = _TextParser()
    parser.feed("".join(_MAIN.findall(page_html) + _STREAMED.findall(page_html)))
    return _BLANK_LINES.sub("\n", "".join(parser.parts)).strip()


def title(page_html: str) -> str:
    """The page's title: <title>, else og:title, else its first h1.

    Next.js streams the metadata of some pages into the browser after the
    body, so their saved HTML carries neither <title> nor og:title -- only
    the heading the reader sees.
    """
    for pattern in (_TITLE, _OG_TITLE):
        match = pattern.search(page_html)
        if match and match.group(1).strip():
            return html.unescape(match.group(1)).strip().removesuffix(_TITLE_SUFFIX)
    match = _H1.search(page_html)
    return (
        " ".join(html.unescape(_TAG.sub(" ", match.group(1))).split()) if match else ""
    )
