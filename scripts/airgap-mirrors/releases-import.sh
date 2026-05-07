#!/usr/bin/env bash
# releases-import.sh — INTERNAL (airgap) machine.
#
# Reads $TRANSFER_DIR/releases/<name>/ and re-creates each Release in the
# corresponding GitLab project via the v4 API. Idempotent — releases whose
# tag_name already exists on GitLab are skipped (HTTP 409 path).
#
# Requires:
#   - GITLAB_HOST set in mirrors.conf
#   - GITLAB_TOKEN exported in the environment (PAT with `api` scope)
#   - The git mirror already pushed (tag must exist in GitLab before a
#     Release can attach to it — run bundle-import.sh first).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
source "$SCRIPT_DIR/lib/common.sh"
load_config

require_cmd curl
require_cmd jq

: "${GITLAB_HOST:?GITLAB_HOST not set in mirrors.conf}"
: "${GITLAB_TOKEN:?export GITLAB_TOKEN before running this script}"

IN_DIR="$TRANSFER_DIR/releases"
[[ -d "$IN_DIR" ]] || die "no releases dir at $IN_DIR — copy USB contents first"

# POST/PUT/GET helper. Echoes response body, sets $LAST_HTTP_CODE.
gitlab_api() {
  local method="$1" path="$2"; shift 2
  local body; body="$(mktemp)"
  local code
  code="$(curl -sS -o "$body" -w '%{http_code}' \
    --request "$method" \
    --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "$GITLAB_HOST/api/v4/$path" "$@")"
  LAST_HTTP_CODE="$code"
  cat "$body"
  rm -f "$body"
}

create_release() {
  local proj_path="$1" tag="$2" name="$3" body_file="$4"
  local payload
  payload="$(jq -n --arg t "$tag" --arg n "$name" --rawfile d "$body_file" \
    '{tag_name:$t, name:$n, description:$d}')"

  gitlab_api POST "projects/$(urlencode_path "$proj_path")/releases" \
    --header "Content-Type: application/json" \
    --data "$payload" >/dev/null
}

upload_asset() {
  local proj_path="$1" file="$2"
  local resp
  resp="$(gitlab_api POST "projects/$(urlencode_path "$proj_path")/uploads" \
    --form "file=@$file")"
  jq -r '.url' <<<"$resp"
}

link_asset_to_release() {
  local proj_path="$1" tag="$2" asset_name="$3" upload_path="$4"
  local full_url="$GITLAB_HOST/-/project/$(urlencode_path "$proj_path")$upload_path"
  gitlab_api POST \
    "projects/$(urlencode_path "$proj_path")/releases/$(urlencode_path "$tag")/assets/links" \
    --data-urlencode "name=$asset_name" \
    --data-urlencode "url=$full_url" >/dev/null
}

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
    body_tmp="$(mktemp)"
    jq -r '.body // ""' <<<"$rel" > "$body_tmp"

    gitlab_api GET \
      "projects/$(urlencode_path "$gl_path")/releases/$(urlencode_path "$tag")" \
      >/dev/null
    if [[ "$LAST_HTTP_CODE" == "200" ]]; then
      log_info "$name: $tag already exists — skipping"
      rm -f "$body_tmp"
      continue
    fi

    create_release "$gl_path" "$tag" "$rel_name" "$body_tmp"
    rm -f "$body_tmp"

    if [[ "$LAST_HTTP_CODE" != "201" ]]; then
      log_warn "$name: $tag create returned HTTP $LAST_HTTP_CODE"
      continue
    fi
    log_info "$name: created $tag"

    local asset_dir="$repo_in/assets/$tag"
    [[ -d "$asset_dir" ]] || continue
    for asset in "$asset_dir"/*; do
      [[ -f "$asset" ]] || continue
      local upload_path
      upload_path="$(upload_asset "$gl_path" "$asset")"
      link_asset_to_release "$gl_path" "$tag" "$(basename "$asset")" "$upload_path"
      log_info "$name: $tag ← $(basename "$asset")"
    done
  done
}

for_each_mirror import_one

log_info "all releases imported"
