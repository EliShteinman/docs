#!/usr/bin/env bash
# bundle-import.sh — INTERNAL (airgap) machine.
#
# Walks every *.bundle file under $TRANSFER_DIR/bundles/ and, for each:
#   1. read the sidecar .meta.json to identify the mirror
#   2. `git bundle verify` (offline integrity check — catches broken USB)
#   3. fetch refs from the bundle into the local bare mirror
#   4. `git push --mirror` to GitLab (origin must be set to the GitLab URL)
#   5. record the imported HEAD in `git config sync.imported`
#   6. emit success line to $TRANSFER_DIR/import-success.list — that file
#      is what bundle-confirm.sh consumes back on the external machine
#
# Idempotent: re-running with the same bundles is safe. `git fetch` is a no-op
# for objects already present, and `push --mirror` re-pushes whatever's there.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
source "$SCRIPT_DIR/lib/common.sh"
load_config

require_cmd git
require_cmd jq

IN_DIR="$TRANSFER_DIR/bundles"
SUCCESS_LIST="$TRANSFER_DIR/import-success.list"

[[ -d "$IN_DIR" ]] || die "no bundles dir at $IN_DIR — copy USB contents first"

: > "$SUCCESS_LIST"   # truncate / start fresh

shopt -s nullglob
bundles=("$IN_DIR"/*.bundle)
shopt -u nullglob
[[ ${#bundles[@]} -gt 0 ]] || die "no *.bundle files found under $IN_DIR"

for bundle in "${bundles[@]}"; do
  meta="${bundle%.bundle}.meta.json"
  [[ -f "$meta" ]] || die "missing sidecar metadata for $bundle"

  name="$(jq -r '.name' "$meta")"
  head="$(jq -r '.head' "$meta")"
  repo="$MIRRORS_DIR/$name.git"

  [[ -d "$repo" ]] || die "$name: bare mirror not found at $repo"

  log_info "$name: verifying $(basename "$bundle")"
  git -C "$repo" bundle verify "$bundle" >/dev/null

  log_info "$name: fetching from bundle"
  git -C "$repo" fetch "$bundle" \
    '+refs/heads/*:refs/heads/*' \
    '+refs/tags/*:refs/tags/*'

  log_info "$name: pushing to GitLab (origin)"
  git -C "$repo" push --mirror origin

  git_local_set "$repo" sync.imported "$head"
  echo "$name $head" >> "$SUCCESS_LIST"
  log_info "$name: imported HEAD=$head"
done

log_info "all bundles imported → success list: $SUCCESS_LIST"
log_info "next step: copy '$SUCCESS_LIST' back to external machine → run bundle-confirm.sh"
