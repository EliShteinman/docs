#!/usr/bin/env bash
# default-branch-set.sh — INTERNAL (airgap) machine. One-time bootstrap.
#
# `git push --mirror` does NOT propagate the source repo's HEAD symref to
# GitLab — the project's default branch is a project-level setting that
# GitLab picks once on first push and never updates afterwards. For repos
# whose upstream default isn't `master`/`main` (e.g. redis/redis uses
# `unstable`) this leaves the GitLab project pointing at the wrong branch.
#
# This script reads each mirror's local HEAD, derives the branch name
# (e.g. "unstable"), and PUTs it as the GitLab project's default_branch.
# Run after the very first bundle-import.sh; idempotent thereafter.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
source "$SCRIPT_DIR/lib/common.sh"
load_config

require_cmd git
require_cmd curl
require_cmd jq

: "${GITLAB_HOST:?GITLAB_HOST not set in mirrors.conf}"
: "${GITLAB_TOKEN:?export GITLAB_TOKEN before running this script}"

set_one() {
  local name="$1" _gh_path="$2" gl_path="$3"
  local repo="$MIRRORS_DIR/$name.git"

  [[ -d "$repo" ]] || { log_warn "$name: bare mirror not found, skipping"; return 0; }

  # `symbolic-ref HEAD` resolves to e.g. `refs/heads/unstable`; strip prefix.
  local head_ref branch
  head_ref="$(git -C "$repo" symbolic-ref HEAD 2>/dev/null || true)"
  if [[ -z "$head_ref" ]]; then
    log_warn "$name: HEAD is detached — cannot determine default branch"
    return 0
  fi
  branch="${head_ref#refs/heads/}"

  log_info "$name: setting default_branch=$branch on $gl_path"
  local code
  code="$(curl -sS -o /dev/null -w '%{http_code}' \
    --request PUT \
    --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    --data-urlencode "default_branch=$branch" \
    "$GITLAB_HOST/api/v4/projects/$(urlencode_path "$gl_path")")"

  if [[ "$code" == "200" ]]; then
    log_info "$name: ok"
  else
    log_warn "$name: PUT returned HTTP $code"
  fi
}

for_each_mirror set_one
log_info "default branches set on all mirrors"
