#!/usr/bin/env python3
"""
Check the vendored redis-cli widget against the upstream canonical copy.

Upstream (PR #3642) stopped shipping the full interactive redis-cli widget in
this repo: `static/js/cli.js` is now a thin shim that loads the canonical script
from the /cli backend at `https://redis.io/cli/static/js/cli.js`. The airgap fork
cannot load that at runtime, so it VENDORS the canonical script locally at
`static/cli-playground/assets/cli.js` and points both the docs shim and the
playground shell at the vendored copy.

Because upstream no longer tracks the widget in git, there is no PR/diff signal
when Redis updates it. This checker is the compensating control: it fetches the
canonical copy and compares it to the vendored one, so a rebuild can detect drift.

MANDATORY: run this on every docs image rebuild. A non-zero exit means the
upstream widget changed and the vendored copy must be refreshed and re-reviewed.

Usage:
    python build/check_cli_js_drift.py [--vendored PATH] [--url URL] [--quiet]

Exit status: 0 if identical, 1 on drift, 2 if the canonical copy can't be fetched
(so CI can tell "changed" apart from "couldn't check"). Stdlib only; run from the
repo root.
"""

import argparse
import hashlib
import sys
import urllib.request

CANONICAL_URL = "https://redis.io/cli/static/js/cli.js"
VENDORED_PATH = "static/cli-playground/assets/cli.js"
FETCH_TIMEOUT = 15

# redis.io sits behind Cloudflare, which 403s the default urllib user agent.
# Present as a normal browser, matching the link checker's .lychee.toml.
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=FETCH_TIMEOUT) as response:
        return response.read()


def check_drift(vendored_path: str, url: str, quiet: bool) -> int:
    try:
        with open(vendored_path, "rb") as handle:
            local = handle.read()
    except OSError as error:
        print(f"ERROR: cannot read vendored copy {vendored_path}: {error}", file=sys.stderr)
        return 2

    try:
        canonical = _fetch(url)
    except (urllib.error.URLError, OSError) as error:
        print(f"ERROR: cannot fetch canonical copy {url}: {error}", file=sys.stderr)
        return 2

    if _sha256(local) == _sha256(canonical):
        if not quiet:
            print(f"OK: {vendored_path} matches {url} ({len(local)} bytes)")
        return 0

    print(
        f"DRIFT: vendored {vendored_path} ({len(local)} bytes, {_sha256(local)[:12]}) "
        f"differs from canonical {url} ({len(canonical)} bytes, {_sha256(canonical)[:12]}). "
        f"Re-vendor and re-review before building the image.",
        file=sys.stderr,
    )
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vendored", default=VENDORED_PATH)
    parser.add_argument("--url", default=CANONICAL_URL)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    return check_drift(args.vendored, args.url, args.quiet)


if __name__ == "__main__":
    sys.exit(main())
