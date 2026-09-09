"""Recovering the URLs redis.io answers with a redirect.

The documentation, and the mirrored content itself, link to paths that are not
where the page lives any more: /blog/connecting-spark-and-redis/ is really
/blog/connecting-spark-and-redis-a-detailed-look/, and redis.io answers the
first with a 301. Its redirect map is in the hosting layer, not in the dataset,
so it cannot be queried -- but it can be observed, one request per stale URL.

The observed map is written to redirects.json and committed, because the mirror
regenerates every markdown file from the source on each run: an alias worked
out at sync time would be lost on the next one. Refreshing it needs the public
internet and is therefore a deliberate step (`--refresh-redirects`), not part
of a normal run.
"""

from __future__ import annotations

import json
import logging
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

LOGGER = logging.getLogger("site_mirror.redirects")

SOURCE_HOST = "https://redis.io"
MAP_PATH = Path(__file__).with_name("redirects.json")
USER_AGENT = "Mozilla/5.0 (compatible; redis-docs-airgap-site-mirror/1.0)"


def load(path: Path = MAP_PATH) -> dict[str, list[str]]:
    """Return {destination path: [stale paths that redirect to it]}."""
    if not path.exists():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        LOGGER.warning("%s is not readable JSON; ignoring it", path)
        return {}
    return {k: list(v) for k, v in raw.items() if isinstance(v, list)}


def save(mapping: dict[str, list[str]], path: Path = MAP_PATH) -> None:
    ordered = {k: sorted(set(v)) for k, v in sorted(mapping.items())}
    path.write_text(json.dumps(ordered, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def resolve(path_: str, timeout: float = 30.0) -> str:
    """Return the path redis.io redirects `path_` to, or "" if it does not.

    A GET rather than a HEAD: the site answers some HEAD requests differently,
    and following the chain is the whole point.
    """
    url = SOURCE_HOST + path_ if path_.startswith("/") else path_
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            final = response.geturl()
    except (urllib.error.HTTPError, OSError) as error:
        LOGGER.debug("%s did not resolve: %s", path_, error)
        return ""
    if not final.startswith(SOURCE_HOST):
        return ""
    landed = final[len(SOURCE_HOST):].split("#")[0].split("?")[0]
    return "" if landed.rstrip("/") == path_.rstrip("/") else landed


def build_map(
    stale: list[str], known: set[str], timeout: float = 30.0
) -> tuple[dict[str, list[str]], list[str]]:
    """Follow every stale path. Returns (destination -> stale paths, unrecovered)."""
    mapping: dict[str, list[str]] = defaultdict(list)
    unrecovered = []
    for path_ in sorted(stale):
        landed = resolve(path_, timeout)
        if landed and landed.rstrip("/") + "/" in known:
            mapping[landed.rstrip("/") + "/"].append(path_.rstrip("/") + "/")
        else:
            unrecovered.append(path_)
    return dict(mapping), unrecovered


def aliases_for(pathname: str, mapping: dict[str, list[str]]) -> tuple[str, ...]:
    """Return the stale paths that should redirect to `pathname`."""
    return tuple(mapping.get(pathname.rstrip("/") + "/", ()))
