#!/usr/bin/env bash
# releases-export.sh — EXTERNAL (online) machine.
#
# For every mirror in mirrors.conf, dumps the upstream GitHub Releases
# (title + body + tag + prerelease flag) plus the binary assets attached
# to each release to $TRANSFER_DIR/releases/<name>/.
#
# Layout per repo:
#   $TRANSFER_DIR/releases/<name>/releases.json    — full GH API response
#   $TRANSFER_DIR/releases/<name>/assets/<tag>/*   — downloaded asset files
#
# `gh` CLI handles auth + pagination automatically. Run `gh auth login`
# once before first use.
#
# This is a full snapshot each time (no incremental marker) — Releases are
# small in count (tens-to-hundreds per repo) and the inner-side import is
# idempotent (skips releases that already exist), so re-exporting is cheap
# for everything except the asset downloads. To skip asset re-download on
# repeat runs, pass --no-assets.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
source "$SCRIPT_DIR/lib/common.sh"
load_config

require_cmd gh
require_cmd jq
require_cmd curl

WITH_ASSETS=1
for arg in "$@"; do
  case "$arg" in
    --no-assets) WITH_ASSETS=0 ;;
    *) die "unknown flag: $arg" ;;
  esac
done

OUT_DIR="$TRANSFER_DIR/releases"
mkdir -p "$OUT_DIR"

export_one() {
  local name="$1" gh_path="$2" _gl_path="$3"
  local repo_out="$OUT_DIR/$name"
  mkdir -p "$repo_out"

  log_info "$name: listing releases via gh API"
  gh api --paginate "repos/$gh_path/releases" > "$repo_out/releases.json"

  local count
  count="$(jq 'length' "$repo_out/releases.json")"
  log_info "$name: $count release(s) recorded"

  [[ "$WITH_ASSETS" -eq 1 ]] || return 0
  [[ "$count" -gt 0 ]] || return 0

  jq -c '.[]' "$repo_out/releases.json" | while read -r rel; do
    local tag asset_dir
    tag="$(jq -r '.tag_name' <<<"$rel")"
    asset_dir="$repo_out/assets/$tag"
    mkdir -p "$asset_dir"

    jq -r '.assets[]? | "\(.name)\t\(.browser_download_url)"' <<<"$rel" \
      | while IFS=$'\t' read -r asset_name asset_url; do
        [[ -z "$asset_url" ]] && continue
        local target="$asset_dir/$asset_name"
        if [[ -s "$target" ]]; then
          log_info "$name: $tag/$asset_name (cached)"
        else
          log_info "$name: downloading $tag/$asset_name"
          curl -fsSL "$asset_url" -o "$target"
        fi
      done
  done
}

for_each_mirror export_one

log_info "all releases exported to: $OUT_DIR"
log_info "next step: copy '$OUT_DIR' to USB → run releases-import.sh on the inner machine"
