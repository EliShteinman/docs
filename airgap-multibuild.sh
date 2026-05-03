#!/usr/bin/env bash
# Air-gap multi-build pipeline.
# Mirrors .github/workflows/main.yml's parallel matrix as a sequential bash loop.
#
# Produces a single public/ tree containing:
#   - "latest" content rooted at /operate/<product>/, /develop/ai/redisvl/, etc.
#     (with all version directories removed before Hugo runs)
#   - For each (product, version), a self-contained subtree at
#     /operate/<product>/<version>/ built from a Hugo invocation where the
#     version's content has been rsync'd over the parent directory.
#
# Run inside the Docker builder stage AFTER `make components` (so /site/examples/
# is populated from external clones).

set -euo pipefail

readonly SITE=/site
readonly SNAPSHOT=/tmp/site-snapshot
readonly FINAL=/tmp/public-final

cd "$SITE"

# ---- Airgap-only source-tree patches (applied once, before snapshot) ---------
# These changes flow into every per-version build via the snapshot.
#
# 1. Relax the JS regex that gates the version-selector dropdown. Upstream
#    requires URL prefix /docs/(latest|staging/.+)/, which never matches when
#    baseURL=/. Replace with a path-only check so the dropdown shows on any
#    deployment.
python3 <<'PYEOF'
import re, pathlib
p = pathlib.Path("layouts/partials/scripts.html")
text = p.read_text()
text, n_op  = re.subn(r"new RegExp\('/docs/\(latest\|staging\\/\.\+\)/operate/(\w+)/\.\*'\)",
                      r"new RegExp('/operate/\1/')", text)
text, n_dev = re.subn(r"new RegExp\('/docs/\(latest\|staging\\/\.\+\)/develop/ai/(\w+)/\.\*'\)",
                      r"new RegExp('/develop/ai/\1/')", text)
p.write_text(text)
assert n_op + n_dev == 3, f"expected 3 regex relaxations, got {n_op + n_dev}"
print(f"airgap: relaxed {n_op + n_dev} version-selector regex(es) in scripts.html")
PYEOF

# 2. Strip hardcoded https://redis.io/docs/latest/ from all content .md files,
#    so markdown links resolve against the local deployment instead of redis.io.
#    Also strip the bare "redis.io/docs/latest/" link-text occurrences (e.g.
#    inside bannerText) so the visible text isn't misleading.
echo "airgap: stripping hardcoded redis.io/docs/latest links from content/*.md..."
find content -type f -name '*.md' -print0 | xargs -0 sed -i \
  -e 's|https://redis.io/docs/latest/|/|g' \
  -e 's|redis\.io/docs/latest/|/|g'

# ---- Snapshot the prepared workspace -----------------------------------------
# Captures content + layouts + components output. Excludes Hugo's own outputs.
rm -rf "$SNAPSHOT"
mkdir -p "$SNAPSHOT"
rsync -a --delete \
  --exclude=public --exclude=resources --exclude=.git \
  "$SITE/" "$SNAPSHOT/"

mkdir -p "$FINAL"

# ---- Discover version directories from the snapshot --------------------------
discover() {
  local dir=$1
  if [ -d "$SNAPSHOT/$dir" ]; then
    ls -1 "$SNAPSHOT/$dir" | grep -E '^[0-9]+\.[0-9]+(\.[0-9]+)?$' || true
  fi
}

K8S_VERSIONS=$(discover content/operate/kubernetes)
RS_VERSIONS=$(discover content/operate/rs)
REDISVL_VERSIONS=$(discover content/develop/ai/redisvl)

echo ">>> Discovered versions:"
echo "    Kubernetes: $(echo "$K8S_VERSIONS" | tr '\n' ' ')"
echo "    RS:         $(echo "$RS_VERSIONS" | tr '\n' ' ')"
echo "    RedisVL:    $(echo "$REDISVL_VERSIONS" | tr '\n' ' ')"

# ---- Helpers -----------------------------------------------------------------
write_version_files() {
  echo "$K8S_VERSIONS"     > "$SITE/kubernetes-versions"
  echo "$RS_VERSIONS"      > "$SITE/rs-versions"
  echo "$REDISVL_VERSIONS" > "$SITE/redisvl-versions"
  : > "$SITE/rdi-versions"
}

reset_workspace() {
  rsync -a --delete \
    --exclude=public --exclude=resources --exclude=.git \
    "$SNAPSHOT/" "$SITE/"
}

# ---- 1. Build "latest" -------------------------------------------------------
# Latest = current site with ALL version dirs removed.
echo ">>> Building latest"
reset_workspace
cd "$SITE"

for v in $K8S_VERSIONS;     do rm -rf "content/operate/kubernetes/$v"; done
for v in $RS_VERSIONS;      do rm -rf "content/operate/rs/$v"; done
for v in $REDISVL_VERSIONS; do rm -rf "content/develop/ai/redisvl/$v"; done

write_version_files
hugo --logLevel info

rsync -a "$SITE/public/" "$FINAL/"

# ---- 2. Build each version ---------------------------------------------------
# Per version: reset workspace, delete other versions, awk-fix relrefs,
# rsync version content INTO parent (so version becomes "the product"),
# tweak templates/frontmatter, run Hugo, extract /<product>/<version>/ subtree.
build_version() {
  local product_path=$1     # e.g. operate/kubernetes
  local product_label=$2    # e.g. "Redis for Kubernetes"
  local product_pascal=$3   # e.g. Kubernetes (matches docs-nav.html selector id suffix)
  local version=$4
  local all_versions=$5     # newline-separated version list for this product

  echo ">>> Building ${product_path} v${version}"
  reset_workspace
  cd "$SITE"

  # Remove all OTHER versions of this product
  for v in $all_versions; do
    if [ "$v" != "$version" ]; then
      rm -rf "content/$product_path/$v"
    fi
  done

  # Strip the version prefix from relrefs in the version's own content
  # (because after rsync the content moves up one level).
  find "content/$product_path/$version" -type f -name '*.md' | while read -r f; do
    awk -v pp="$product_path" -v ver="$version" '
      { gsub("\\(\\{\\{< ?relref \"/" pp "/" ver, "({{< relref \"/" pp); print }
    ' "$f" > "$f.tmp" && mv "$f.tmp" "$f"
  done

  # rsync the version content INTO the parent dir, replacing latest's content
  # for this product. --delete-after removes any latest files not in the version.
  rsync -a --delete-after \
    "content/$product_path/$version/" \
    "content/$product_path/"

  # Restore parent linkTitle (the rsync brought in the version's _index.md
  # whose linkTitle is "<version>", e.g. "7.8.6"; restore the product label).
  sed -i "s/^linkTitle: $version$/linkTitle: $product_label/" \
    "content/$product_path/_index.md" || true

  # Update the version-selector button label in the nav from "latest" to "v<version>".
  sed -i "s/id=\"versionSelector${product_pascal}Value\" class=\"version-selector-control\">latest/id=\"versionSelector${product_pascal}Value\" class=\"version-selector-control\">v${version}/" \
    layouts/partials/docs-nav.html

  # Inject Edit-on-GitHub path rewrite so it points at the version dir on GH.
  local pp_esc="${product_path//\//\\/}"
  sed -i "12i \\{{ \$gh_path = replaceRE \`^${pp_esc}/\` \"${pp_esc}/${version}/\" \$gh_path }}" \
    layouts/partials/meta-links.html

  # NOTE: the redis.io/docs/latest/ banner link is already rewritten globally
  # at the top of this script (before the snapshot), so we don't need a
  # per-version sed here.

  write_version_files
  hugo --logLevel info

  if [ ! -d "$SITE/public/$product_path/$version" ]; then
    echo "!!! ERROR: hugo did not produce public/$product_path/$version/" >&2
    exit 1
  fi

  mkdir -p "$FINAL/$product_path"
  # Latest's aliases (e.g. content/operate/rs/monitoring/_index.md has
  # `aliases: [..., /operate/rs/7.4/clusters/monitoring/]`) cause Hugo to
  # emit redirect HTMLs *inside* the version's URL prefix during the latest
  # build. Those land in $FINAL via the rsync after latest, and would make
  # `cp -a` nest the version's tree (creating $version/$version/index.html
  # and serving 403 at /<version>/). Wipe the dest first so the version's
  # tree fully replaces whatever was there.
  rm -rf "$FINAL/$product_path/$version"
  cp -a "$SITE/public/$product_path/$version" "$FINAL/$product_path/$version"

  # Mirror upstream's #3166/#3177 fix: per-version Hugo builds produce a
  # different /css/index.min.<hash>.css than the latest build (Tailwind purges
  # by classes seen in rendered HTML, which differs across versions). Without
  # this, version pages 404 on their CSS. Copy css/scss additively so each
  # build's hash coexists alongside latest's.
  for d in css scss; do
    if [ -d "$SITE/public/$d" ]; then
      mkdir -p "$FINAL/$d"
      cp -an "$SITE/public/$d/." "$FINAL/$d/"
    fi
  done

  rm -rf "$SITE/public"
}

for v in $K8S_VERSIONS; do
  build_version operate/kubernetes "Redis for Kubernetes" Kubernetes "$v" "$K8S_VERSIONS"
done
for v in $RS_VERSIONS; do
  build_version operate/rs "Redis Software" Rs "$v" "$RS_VERSIONS"
done
for v in $REDISVL_VERSIONS; do
  build_version develop/ai/redisvl "RedisVL" Redisvl "$v" "$REDISVL_VERSIONS"
done

# ---- 3. Replace site public with the merged final tree -----------------------
rm -rf "$SITE/public"
mv "$FINAL" "$SITE/public"

# ---- 4. Generate ndjson over the merged tree ---------------------------------
echo ">>> Generating ndjson..."
cd "$SITE"
python3 build/generate_ndjson.py
gzip -kf public/docs.ndjson

echo ">>> Multi-build complete. public/ summary:"
echo "    $(find public -type f | wc -l) files, $(du -sh public | cut -f1) total"
