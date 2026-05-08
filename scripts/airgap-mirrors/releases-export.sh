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
# Asset-download policy is per-repo, set via the optional 3rd field in
# each MIRRORS entry in mirrors.conf:
#
#   (omitted) | all          download every release's assets    [default]
#   none                     metadata only — no asset downloads
#   latest:N                 only the N most recent releases
#   since:YYYY-MM-DD         only releases published on/after this date
#
# Releases metadata (releases.json) is always fetched in full regardless
# of policy — it's small and the inner side needs the complete list to
# decide which Releases to create on GitLab. Only ASSET downloads are
# filtered.
#
# Repeat-run behavior: the JSON is re-fetched every time (cheap), and
# already-downloaded assets are reused as-is (`-s` size check). The
# inner-side `releases-import.sh` is idempotent — releases whose tag
# already exists on GitLab are skipped.
#
# CLI flags:
#   --no-assets       force `none` policy globally (overrides per-repo)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
source "$SCRIPT_DIR/lib/common.sh"
load_config

require_cmd gh
require_cmd jq
require_cmd curl

GLOBAL_NO_ASSETS=0
for arg in "$@"; do
  case "$arg" in
    --no-assets) GLOBAL_NO_ASSETS=1 ;;
    *) die "unknown flag: $arg" ;;
  esac
done

OUT_DIR="$TRANSFER_DIR/releases"
mkdir -p "$OUT_DIR"

# Decide which slice of the releases list gets its assets downloaded.
# Echoes a JSON array (subset of $1) on stdout. $1 is the full releases
# JSON file; $2 is the policy string.
filter_for_assets() {
  local releases_file="$1" policy="$2"

  case "$policy" in
    ''|all)
      cat "$releases_file"
      ;;
    none)
      echo '[]'
      ;;
    latest:*)
      local n="${policy#latest:}"
      [[ "$n" =~ ^[0-9]+$ ]] || die "invalid latest:N policy '$policy' (N must be a positive integer)"
      jq ".[0:$n]" "$releases_file"
      ;;
    since:*)
      local d="${policy#since:}"
      [[ "$d" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] \
        || die "invalid since: policy '$policy' (expected YYYY-MM-DD)"
      jq --arg d "${d}T00:00:00Z" \
        '[.[] | select(.published_at >= $d)]' "$releases_file"
      ;;
    *)
      die "unknown asset policy: '$policy'"
      ;;
  esac
}

export_one() {
  local name="$1" gh_path="$2" policy="${3:-all}" asset_filter="${4:-}"
  [[ "$GLOBAL_NO_ASSETS" -eq 1 ]] && policy="none"

  # Build a jq-compatible regex from the comma-separated keyword list
  # (e.g. "win,linux" → "win|linux"). Empty filter means accept all.
  local asset_regex=""
  if [[ -n "$asset_filter" ]]; then
    asset_regex="${asset_filter//,/|}"
  fi

  local repo_out="$OUT_DIR/$name"
  mkdir -p "$repo_out"

  local policy_desc="$policy"
  [[ -n "$asset_filter" ]] && policy_desc="$policy, assets matching: $asset_filter"
  log_info "$name: listing releases via gh API ($policy_desc)"
  gh api --paginate "repos/$gh_path/releases" > "$repo_out/releases.json"

  local count
  count="$(jq 'length' "$repo_out/releases.json")"
  log_info "$name: $count release(s) recorded"

  [[ "$count" -gt 0 ]] || return 0

  local to_assetize asset_count
  to_assetize="$(filter_for_assets "$repo_out/releases.json" "$policy")"
  asset_count="$(jq 'length' <<<"$to_assetize")"

  if [[ "$asset_count" -eq 0 ]]; then
    log_info "$name: policy excluded all releases — no assets to fetch"
    return 0
  fi
  log_info "$name: downloading assets for $asset_count release(s)"

  jq -c '.[]' <<<"$to_assetize" | while read -r rel; do
    local tag asset_dir
    tag="$(jq -r '.tag_name' <<<"$rel")"
    asset_dir="$repo_out/assets/$tag"
    mkdir -p "$asset_dir"

    # Apply asset name filter if set, otherwise take all assets.
    local asset_list
    if [[ -n "$asset_regex" ]]; then
      asset_list="$(jq -r --arg re "$asset_regex" \
        '.assets[]? | select(.name | test($re;"i")) | "\(.name)\t\(.browser_download_url)"' \
        <<<"$rel")"
    else
      asset_list="$(jq -r '.assets[]? | "\(.name)\t\(.browser_download_url)"' <<<"$rel")"
    fi

    while IFS=$'\t' read -r asset_name asset_url; do
      [[ -z "$asset_url" ]] && continue
      local target="$asset_dir/$asset_name"
      if [[ -s "$target" ]]; then
        log_info "$name: $tag/$asset_name (cached)"
      else
        log_info "$name: downloading $tag/$asset_name"
        curl -fsSL "$asset_url" -o "$target"
      fi
    done <<< "$asset_list"
  done
}

for_each_mirror export_one

log_info "all releases exported to: $OUT_DIR"
log_info "next step: copy '$OUT_DIR' to USB → run releases-import.sh on the inner machine"
