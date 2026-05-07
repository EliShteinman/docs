#!/usr/bin/env bash
# bundle-confirm.sh — EXTERNAL (online) machine.
#
# Promotes the "pending" sync marker (`sync.bundled`) to confirmed
# (`sync.synced`) for each mirror that the inner side reports as
# successfully imported.
#
# Input: $TRANSFER_DIR/import-success.list, copied back from the inner
# machine. Each line: "<mirror-name> <imported-head-sha>".
#
# Why two-phase? If a USB transfer is lost or the inner-side push fails
# midway, sync.synced stays where it was, so the next bundle-create.sh
# regenerates the missing range — no objects fall through the cracks.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
source "$SCRIPT_DIR/lib/common.sh"
load_config

require_cmd git

SUCCESS_LIST="${1:-$TRANSFER_DIR/import-success.list}"
[[ -f "$SUCCESS_LIST" ]] || die "success list not found: $SUCCESS_LIST"

while IFS=' ' read -r name head; do
  [[ -z "$name" || "$name" =~ ^# ]] && continue

  repo="$MIRRORS_DIR/$name.git"
  [[ -d "$repo" ]] || die "$name: bare mirror not found at $repo"

  bundled="$(git_local_get "$repo" sync.bundled)"
  if [[ -z "$bundled" ]]; then
    log_warn "$name: no sync.bundled recorded — was bundle-create.sh run?"
    continue
  fi

  if [[ "$bundled" != "$head" ]]; then
    log_warn "$name: pending HEAD ($bundled) != imported HEAD ($head) — skipping"
    log_warn "$name: re-run bundle-create.sh to align state"
    continue
  fi

  git_local_set "$repo" sync.synced "$head"
  log_info "$name: confirmed → sync.synced=$head"
done < "$SUCCESS_LIST"

log_info "done. next bundle-create.sh will start from each repo's new sync.synced"
