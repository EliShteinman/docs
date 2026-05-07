# Shared helpers for airgap mirror scripts. Sourced — not executed.

set -euo pipefail

log_info()  { printf '\033[0;32m[INFO]\033[0m  %s\n' "$*" >&2; }
log_warn()  { printf '\033[0;33m[WARN]\033[0m  %s\n' "$*" >&2; }
log_error() { printf '\033[0;31m[ERROR]\033[0m %s\n' "$*" >&2; }
die()       { log_error "$*"; exit 1; }

# Resolve the script directory of the caller and load mirrors.conf.
# Looks first for a real `mirrors.conf`, falls back to `mirrors.conf.example`
# only with a warning so first-time runs are obviously misconfigured.
load_config() {
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[1]}")" && pwd)"
  local config="$script_dir/mirrors.conf"

  if [[ ! -f "$config" ]]; then
    die "missing $config — copy the matching template (mirrors.external.conf.example on the online machine, mirrors.internal.conf.example on the airgap machine) to mirrors.conf and edit"
  fi

  # shellcheck source=/dev/null
  source "$config"

  : "${MIRRORS_DIR:?MIRRORS_DIR not set in mirrors.conf}"
  : "${TRANSFER_DIR:?TRANSFER_DIR not set in mirrors.conf}"
  : "${MIRRORS:?MIRRORS array not set in mirrors.conf}"
}

# Iterate over $MIRRORS and call $1 with (name, target).
#
# `target` is the side-specific second field of each entry — on the
# external machine it's `github_owner/repo`, on the internal machine it's
# `gitlab_path`. Each script knows which it expects based on the side it
# runs on; this helper stays side-agnostic.
#
# Exits on first failure to match `set -e` semantics.
for_each_mirror() {
  local callback="$1"
  local entry name target
  for entry in "${MIRRORS[@]}"; do
    IFS='|' read -r name target <<< "$entry"
    [[ -n "$name" && -n "$target" ]] \
      || die "malformed mirror entry: '$entry'"
    "$callback" "$name" "$target"
  done
}

# URL-encode a path while preserving forward slashes' usual meaning.
# GitLab's "path-as-id" addressing (/api/v4/projects/<group>%2F<repo>)
# requires `/` → `%2F` but no other characters appear in mirror paths.
urlencode_path() {
  local path="$1"
  printf '%s' "${path//\//%2F}"
}

# UTC ISO8601 timestamp suitable for filenames (no colons).
iso_stamp() {
  date -u +"%Y%m%dT%H%M%SZ"
}

# Read a `git config --local` value, returning empty string if unset.
# Wraps the non-zero-exit-on-missing behavior so callers can use `[[ -z ]]`.
git_local_get() {
  local repo="$1" key="$2"
  git -C "$repo" config --local --get "$key" 2>/dev/null || true
}

# Set a `git config --local` value (creates if absent, overwrites if present).
git_local_set() {
  local repo="$1" key="$2" value="$3"
  git -C "$repo" config --local "$key" "$value"
}

require_cmd() {
  local cmd="$1"
  command -v "$cmd" >/dev/null 2>&1 || die "missing required command: $cmd"
}
