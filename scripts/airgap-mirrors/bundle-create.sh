#!/usr/bin/env bash
# bundle-create.sh — EXTERNAL (online) machine.
#
# For every mirror in mirrors.conf:
#   1. fetch upstream GitHub with --prune (incremental — Git protocol delta)
#   2. create a `git bundle` of objects newer than the last confirmed sync
#      point ($MIRRORS_DIR/<name>.git's `git config sync.synced`)
#   3. record the bundled HEAD as `git config sync.bundled` (pending until
#      bundle-confirm.sh promotes it)
#   4. write a sidecar JSON with metadata next to each bundle
#
# Output goes to $TRANSFER_DIR/bundles/. Copy that whole subdir to USB.
#
# First run for a repo (no `sync.synced` yet) creates a FULL bundle (--all).
# Subsequent runs create DELTA bundles (synced..HEAD --all).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
source "$SCRIPT_DIR/lib/common.sh"
load_config

require_cmd git
require_cmd jq

OUT_DIR="$TRANSFER_DIR/bundles"
mkdir -p "$OUT_DIR"

STAMP="$(iso_stamp)"

bundle_one() {
  local name="$1" gh_path="$2" gl_path="$3"
  local repo="$MIRRORS_DIR/$name.git"
  local upstream="https://github.com/$gh_path"

  [[ -d "$repo" ]] || die "$name: bare mirror not found at $repo (run initial clone first)"

  log_info "$name: fetching upstream"
  git -C "$repo" fetch --prune

  local head synced bundle_kind bundle_path
  head="$(git -C "$repo" rev-parse HEAD)"
  synced="$(git_local_get "$repo" sync.synced)"

  if [[ -n "$synced" ]] && [[ "$synced" == "$head" ]]; then
    log_info "$name: no new commits since last sync — skipping"
    return 0
  fi

  if [[ -n "$synced" ]]; then
    bundle_kind="delta"
    bundle_path="$OUT_DIR/${name}.${STAMP}.delta.bundle"
    log_info "$name: bundling $synced..HEAD"
    git -C "$repo" bundle create "$bundle_path" "$synced..HEAD" --all
  else
    bundle_kind="full"
    bundle_path="$OUT_DIR/${name}.${STAMP}.full.bundle"
    log_info "$name: bundling --all (first run, no prior sync state)"
    git -C "$repo" bundle create "$bundle_path" --all
  fi

  # Mark this HEAD as "bundled but not yet confirmed". bundle-confirm.sh
  # promotes sync.bundled → sync.synced after the inner side reports success.
  git_local_set "$repo" sync.bundled "$head"

  jq -n \
    --arg name "$name" \
    --arg upstream "$upstream" \
    --arg gitlab "$gl_path" \
    --arg head "$head" \
    --arg from "${synced:-}" \
    --arg kind "$bundle_kind" \
    --arg created "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
    '{name:$name, upstream:$upstream, gitlab_path:$gitlab,
      head:$head, from:$from, kind:$kind, created_at:$created}' \
    > "${bundle_path%.bundle}.meta.json"

  log_info "$name: → $(basename "$bundle_path") ($(du -h "$bundle_path" | cut -f1))"
}

for_each_mirror bundle_one

log_info "all bundles ready in: $OUT_DIR"
log_info "next step: copy '$OUT_DIR' to USB → run bundle-import.sh on the inner machine"
