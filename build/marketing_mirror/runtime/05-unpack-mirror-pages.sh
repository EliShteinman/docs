#!/bin/sh
# shellcheck shell=busybox
# Both mirror images are Alpine, whose sh (busybox ash) has pipefail.
# Run by the nginx image's entrypoint before nginx starts: unpacks the mirror's
# pages (one zstd archive, see Dockerfile.runtime) into the directory nginx
# serves them from. A restarted container keeps that directory, so it skips.
set -euo pipefail

archive=/usr/share/nginx/mirror-pages.tar.zst
pages=/usr/share/nginx/pages
marker="$pages/.unpacked"

if [ -f "$marker" ]; then
  echo "$0: pages already unpacked in $pages"
  exit 0
fi

zstd -d -q --long=25 -c "$archive" | tar -x -C "$pages"
touch "$marker"
echo "$0: unpacked $(find "$pages" -name '*.html' | wc -l) pages into $pages"
