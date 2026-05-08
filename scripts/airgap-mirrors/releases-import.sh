#!/usr/bin/env bash
# releases-import.sh — INTERNAL (airgap) machine.
#
# Reads $TRANSFER_DIR/releases/<name>/ and re-creates each Release in the
# corresponding GitLab project via the v4 API. Idempotent — releases whose
# tag_name already exists on GitLab are skipped.
#
# PREREQUISITES (all required before first run):
#   1. GITLAB_TOKEN exported — PAT with `api` scope.
#      Used for Release creation AND file uploads AND release links.
#   2. Git tags already pushed (run bundle-import.sh first). GitLab returns
#      422 if you try to create a Release for a tag that doesn't exist.
#   3. GitLab Generic Package Registry enabled for each project.
#      Admin: Settings → CI/CD → Package registry. Enabled by default on
#      most enterprise GitLab installations.
#   4. Package upload size limit sufficient for your largest asset.
#      Admin: Settings → General → Account and limit settings →
#      "Maximum artifacts size". Default is 1 GiB.
#
# File upload strategy: assets are uploaded to the project's Generic Package
# Registry (PUT /packages/generic/release-assets/<tag>/<filename>) rather
# than the /uploads API. The /uploads endpoint has a 10 MiB default limit
# which is insufficient for GUI installers (80–130 MiB each). The package
# registry limit is governed by max_artifacts_size and defaults to 1 GiB.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
source "$SCRIPT_DIR/lib/common.sh"
load_config

require_cmd curl
require_cmd jq

: "${GITLAB_HOST:?GITLAB_HOST not set in mirrors.conf}"
: "${GITLAB_TOKEN:?export GITLAB_TOKEN=<PAT with api scope> before running this script}"

IN_DIR="$TRANSFER_DIR/releases"
[[ -d "$IN_DIR" ]] || die "no releases dir at $IN_DIR — copy USB contents first"

# ── HTTP helpers ────────────────────────────────────────────────────────────

# GET/POST/PUT with JSON body. Echoes response body; sets LAST_HTTP_CODE.
gitlab_api() {
  local method="$1" path="$2"; shift 2
  local body
  body="$(mktemp)"
  trap 'rm -f "$body"' RETURN
  LAST_HTTP_CODE="$(curl -sS -o "$body" -w '%{http_code}' \
    --request "$method" \
    --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "$GITLAB_HOST/api/v4/$path" "$@")"
  cat "$body"
}

# PUT a binary file to the Generic Package Registry.
# Returns the full download URL on success, empty string on failure.
# Uses PUT + --upload-file (raw binary body) — correct for this endpoint.
upload_to_package_registry() {
  local proj_path="$1" tag="$2" file="$3"
  local filename encoded_proj pkg_url code
  filename="$(basename "$file")"
  encoded_proj="$(urlencode_path "$proj_path")"
  pkg_url="$GITLAB_HOST/api/v4/projects/${encoded_proj}/packages/generic/release-assets/${tag}/${filename}"

  code="$(curl -sS -o /dev/null -w '%{http_code}' \
    --request PUT \
    --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    --upload-file "$file" \
    "$pkg_url")"

  if [[ "$code" == "201" ]]; then
    echo "$pkg_url"
  else
    log_warn "upload failed for $filename (HTTP $code) — check max_artifacts_size admin setting"
    echo ""
  fi
}

# ── Release operations ───────────────────────────────────────────────────────

create_release() {
  local proj_path="$1" tag="$2" rel_name="$3" body_file="$4"
  local description payload
  # Use --arg (jq 1.5+) rather than --rawfile (jq 1.6+ only).
  description="$(cat "$body_file")"
  payload="$(jq -n \
    --arg t "$tag" \
    --arg n "$rel_name" \
    --arg d "$description" \
    '{tag_name:$t, name:$n, description:$d}')"

  gitlab_api POST "projects/$(urlencode_path "$proj_path")/releases" \
    --header "Content-Type: application/json" \
    --data "$payload" >/dev/null
}

link_release_asset() {
  local proj_path="$1" tag="$2" asset_name="$3" full_url="$4"
  local encoded_proj encoded_tag
  encoded_proj="$(urlencode_path "$proj_path")"
  encoded_tag="$(urlencode_path "$tag")"

  gitlab_api POST \
    "projects/${encoded_proj}/releases/${encoded_tag}/assets/links" \
    --data-urlencode "name=$asset_name" \
    --data-urlencode "url=$full_url" >/dev/null
}

# ── Per-repo import ──────────────────────────────────────────────────────────

import_one() {
  local name="$1" gl_path="$2"
  local repo_in="$IN_DIR/$name"
  local releases_file="$repo_in/releases.json"

  [[ -f "$releases_file" ]] || { log_warn "$name: no releases.json — skipping"; return 0; }

  local count
  count="$(jq 'length' "$releases_file")"
  log_info "$name: importing $count release(s) → $gl_path"

  jq -c '.[]' "$releases_file" | while read -r rel; do
    local tag rel_name body_tmp
    tag="$(jq -r '.tag_name' <<<"$rel")"
    rel_name="$(jq -r '.name // .tag_name' <<<"$rel")"

    # Skip if release already exists on GitLab (idempotency).
    gitlab_api GET \
      "projects/$(urlencode_path "$gl_path")/releases/$(urlencode_path "$tag")" \
      >/dev/null
    if [[ "$LAST_HTTP_CODE" == "200" ]]; then
      log_info "$name: $tag already exists — skipping"
      continue
    fi

    # Create the Release (title + body). Requires tag to exist in GitLab.
    body_tmp="$(mktemp)"
    jq -r '.body // ""' <<<"$rel" > "$body_tmp"
    create_release "$gl_path" "$tag" "$rel_name" "$body_tmp"
    rm -f "$body_tmp"

    if [[ "$LAST_HTTP_CODE" != "201" ]]; then
      log_warn "$name: $tag — create_release returned HTTP $LAST_HTTP_CODE (tag may not exist yet; run bundle-import.sh first)"
      continue
    fi
    log_info "$name: created $tag"

    # Upload binary assets (if any were downloaded on the external side).
    local asset_dir="$repo_in/assets/$tag"
    [[ -d "$asset_dir" ]] || continue
    for asset in "$asset_dir"/*; do
      [[ -f "$asset" ]] || continue
      local download_url
      download_url="$(upload_to_package_registry "$gl_path" "$tag" "$asset")"
      if [[ -z "$download_url" ]]; then
        log_warn "$name: $tag — skipped asset $(basename "$asset") (upload failed)"
        continue
      fi
      link_release_asset "$gl_path" "$tag" "$(basename "$asset")" "$download_url"
      log_info "$name: $tag ← $(basename "$asset")"
    done
  done
}

for_each_mirror import_one

log_info "all releases imported"
