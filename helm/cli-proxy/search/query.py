"""Turning the modal's query string into FT.SEARCH, and the reply back into JSON.

What the modal sends was measured against the live service, not guessed:

  * one request per keystroke, no debounce, with `*` appended to the whole
    string -- so the last token is a prefix and the rest are exact;
  * multiple words are ANDed (vector 382, search 728, "vector search" 316),
    which is the query engine's default for space-separated terms;
  * `p` filters server-side, and an unknown value answers total 0 rather than
    an error -- a TAG filter on a value nothing carries does the same;
  * `site` is accepted and ignored: the live service returns identical results
    with and without it.
"""

import json

from search.product import ALL_PRODUCTS

HIGHLIGHT_OPEN = "<b>"
HIGHLIGHT_CLOSE = "</b>"


def _escape(term: str) -> str:
    """Backslash-escape everything the query parser would otherwise read as syntax."""
    return "".join(character if character.isalnum() else "\\" + character for character in term)


def _tokenize(raw: str) -> list[str]:
    """Return the escaped query tokens, keeping the prefix marker the modal sent.

    A token the modal marked as a prefix keeps its `*`; the escape runs on the
    bare word so the marker is not escaped into a literal asterisk.
    """
    tokens = []
    for word in raw.split():
        is_prefix = word.endswith("*")
        escaped = _escape(word.rstrip("*") if is_prefix else word)
        if not escaped:
            continue
        tokens.append(escaped + "*" if is_prefix else escaped)
    return tokens


def build_query(raw: str, product: str) -> str:
    """Return the FT.SEARCH query for `raw`, or "" when there is nothing to search for."""
    tokens = _tokenize(raw)
    if not tokens:
        return ""
    query = " ".join(tokens)
    if product and product != ALL_PRODUCTS:
        query += " @product:{%s}" % _escape(product)
    return query


def search_command(index: str, query: str, limit: int) -> list[str]:
    """Return the FT.SEARCH argument vector for `query`."""
    return [
        "FT.SEARCH",
        index,
        query,
        "LIMIT",
        "0",
        str(limit),
        "RETURN",
        "4",
        "title",
        "body",
        "url",
        "hierarchy",
        "HIGHLIGHT",
        "FIELDS",
        "2",
        "title",
        "body",
        "TAGS",
        HIGHLIGHT_OPEN,
        HIGHLIGHT_CLOSE,
        "SUMMARIZE",
        "FIELDS",
        "1",
        "body",
        "FRAGS",
        "1",
        "LEN",
        "30",
        "SEPARATOR",
        " ... ",
        "DIALECT",
        "2",
    ]


def parse_reply(reply: object) -> tuple[int, list[dict[str, str]]]:
    """Split an FT.SEARCH reply into its total and its documents' field maps."""
    if not isinstance(reply, list) or not reply:
        return 0, []
    total = reply[0] if isinstance(reply[0], int) else 0
    documents = []
    # The reply alternates key, field-list, key, field-list. The key itself is
    # not needed -- `url` is stored on the document -- so only the field lists
    # are read.
    for item in reply[1:]:
        if not isinstance(item, list):
            continue
        documents.append(dict(zip(item[::2], item[1::2])))
    return total, documents


def to_results(documents: list[dict[str, str]]) -> list[dict]:
    """Map indexed documents onto the response records the modal expects."""
    results = []
    for document in documents:
        results.append(
            {
                "title": document.get("title", ""),
                # Always empty, matching the live service: every one of the 30
                # results sampled from redis.io carried an empty section_title.
                "section_title": "",
                "hierarchy": _decode_hierarchy(document.get("hierarchy")),
                "body": document.get("body", ""),
                "url": document.get("url", ""),
            }
        )
    return results


def _decode_hierarchy(stored: str | None) -> list[str]:
    if not stored:
        return []
    try:
        crumbs = json.loads(stored)
    except json.JSONDecodeError:
        return []
    return crumbs if isinstance(crumbs, list) else []
