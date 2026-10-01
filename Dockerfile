# syntax=docker/dockerfile:1

ARG VARIANT=privileged

# ============================================================
# Stage: deps (apt + hugo + npm + pip)
# ============================================================
# Force builder-side stages to run on the host's native platform — the output
# is static HTML/CSS/JS that's identical regardless of target arch, so there's
# no point running Hugo + npm + pip twice under QEMU emulation. Each target's
# runtime stage COPYs the same /site/public out of the final builder stage.
FROM --platform=$BUILDPLATFORM node:24-trixie AS deps

ARG HUGO_VERSION=0.143.1
ARG BUILDARCH

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    git \
    make \
    wget \
    rsync \
    && rm -rf /var/lib/apt/lists/*

RUN wget -O /tmp/hugo.deb \
    "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-${BUILDARCH}.deb" \
    && dpkg -i /tmp/hugo.deb \
    && rm /tmp/hugo.deb

WORKDIR /site

COPY package.json ./
RUN npm install

COPY requirements.txt ./
RUN python3 -m venv /venv && /venv/bin/pip install -r requirements.txt

# ============================================================
# Stage: components (COPY workspace + make components)
# ============================================================
FROM deps AS components

# Everything but mirror/site: 3.4 GB the Hugo build never reads. The mirror
# stages below copy it straight from the build context.
COPY --exclude=mirror . .

ENV PATH="/venv/bin:$PATH"

RUN sed -i 's#baseURL = "https://redis.io"#baseURL = "/"#g' config.toml
# Hugo per-partial timeout: upstream sets 75s, which fits CI but not multi-platform
# Docker builds where dynacache is constantly evicted under memory pressure.
RUN sed -i 's/timeout="75"/timeout="600"/' config.toml

# Fetch external client repos (clones into examples/). Cannot move into the
# multi-build below because each version build resets the workspace; we want
# examples/ in the snapshot.
RUN --mount=type=secret,id=PRIVATE_ACCESS_TOKEN,env=PRIVATE_ACCESS_TOKEN \
    make components

# ============================================================
# Stage: builder (multi-version Hugo build + gzip pre-compression)
# ============================================================
FROM components AS builder

# Multi-build pipeline: latest + one Hugo invocation per (product, version),
# then merged into a single public/ tree. See airgap-multibuild.sh.
#
# The cache mount preserves per-version Hugo outputs across builds. The script
# computes a content-hash per version and reuses cached outputs when the hash
# matches — so a merge that only touches one version's content rebuilds only
# that version, not the other 27.
RUN --mount=type=cache,target=/var/cache/airgap-versions \
    bash airgap-multibuild.sh

# Pre-compress static assets that nginx serves via gzip_static. Skips .md and
# .json because nginx runs sub_filter on those at request time (gzip_static is
# OFF for those locations — pre-compressing them would be wasted CPU).
RUN find /site/public -type f \( -name "*.html" -o -name "*.css" -o -name "*.js" -o -name "*.xml" -o -name "*.svg" -o -name "*.txt" \) \
    -exec gzip -9 -k {} \;

# ============================================================
# Runtime: privileged variant (nginx:alpine, port 80)
# ============================================================
FROM nginx:alpine AS runtime-privileged

ARG GIT_COMMIT=unknown
ARG BUILD_DATE=unknown

LABEL org.opencontainers.image.source="https://github.com/redis/docs"
LABEL org.opencontainers.image.revision="${GIT_COMMIT}"
LABEL org.opencontainers.image.created="${BUILD_DATE}"
LABEL org.opencontainers.image.variant="privileged"

COPY --from=builder /site/public /usr/share/nginx/html

# Kept in step with Dockerfile.runtime, which the airgap workflow uses. The
# download bundles are packed at pod start so they carry the deployment's own
# base URL; see the note there.
RUN apk add --no-cache python3
COPY --from=builder /site/build/make_doc_bundles.py /opt/redis-docs/build/make_doc_bundles.py
COPY --from=builder /site/data/doc_bundles.json /opt/redis-docs/data/doc_bundles.json

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

# ============================================================
# Runtime: unprivileged variant (nginx-unprivileged, port 8080)
# ============================================================
FROM nginxinc/nginx-unprivileged:alpine AS runtime-unprivileged

ARG GIT_COMMIT=unknown
ARG BUILD_DATE=unknown

LABEL org.opencontainers.image.source="https://github.com/redis/docs"
LABEL org.opencontainers.image.revision="${GIT_COMMIT}"
LABEL org.opencontainers.image.created="${BUILD_DATE}"
LABEL org.opencontainers.image.variant="unprivileged"

COPY --from=builder --chown=nginx:nginx /site/public /usr/share/nginx/html

# See the note on the privileged variant. apk needs root; drop straight back to
# the image's own unprivileged uid so nothing else runs elevated.
USER root
RUN apk add --no-cache python3
COPY --from=builder /site/build/make_doc_bundles.py /opt/redis-docs/build/make_doc_bundles.py
COPY --from=builder /site/data/doc_bundles.json /opt/redis-docs/data/doc_bundles.json
USER 101

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]

# ============================================================
# The mirror: redis.io's marketing site, as captured by build.marketing_mirror
# ============================================================
# Built with `--target mirror-unprivileged`. The pages are committed under
# mirror/site and copied as they are: nothing here renders them. Kept in step
# with Dockerfile.runtime, which the airgap workflow uses.

# The mirror's pages: 1,705 of them, 2.5 GB, mostly the same Next.js markup
# page after page. gzip, one file at a time, cannot see across pages (650 MB);
# one zstd stream with a 32 MB window can (13 MB). The image carries that one
# archive, and 05-unpack-mirror-pages.sh unpacks it into /usr/share/nginx/pages
# when the container starts (under a second, 37 MB of memory; --long=25 keeps
# it well inside the chart's 256Mi limit). Every other file stays a plain file:
# the search service's init container reads mirror.ndjson from the image.
# A stage of its own, on the build platform: compressed once, not under QEMU.
FROM --platform=$BUILDPLATFORM alpine:3 AS mirror-pages
RUN apk add --no-cache zstd
COPY --exclude=sanity --exclude=_next --exclude=.git --exclude=.gitattributes mirror/site /site
RUN cd /site \
    && find . -name '*.html' | sort > /tmp/pages \
    && tar -cf - -T /tmp/pages | zstd -19 --long=25 -T0 -q -o /mirror-pages.tar.zst \
    && find . -name '*.html' -delete

FROM nginx:alpine AS mirror-privileged

ARG GIT_COMMIT=unknown
ARG BUILD_DATE=unknown

LABEL org.opencontainers.image.source="https://github.com/redis/docs"
LABEL org.opencontainers.image.revision="${GIT_COMMIT}"
LABEL org.opencontainers.image.created="${BUILD_DATE}"
LABEL org.opencontainers.image.variant="mirror-privileged"

# Writable by any user: the chart mounts an emptyDir here, and a plain
# `docker run` unpacks into the container's own layer.
RUN apk add --no-cache zstd && install -d -m 1777 /usr/share/nginx/pages

COPY build/marketing_mirror/runtime/nginx.conf /etc/nginx/conf.d/default.conf
# Assets first, in layers of their own: images and Next.js chunks change far
# less often than the pages that name them.
COPY mirror/site/sanity /usr/share/nginx/html/sanity
COPY mirror/site/_next /usr/share/nginx/html/_next
COPY --from=mirror-pages /site /usr/share/nginx/html
COPY build/marketing_mirror/runtime/*.js /usr/share/nginx/html/_mirror/
COPY --chmod=755 build/marketing_mirror/runtime/05-unpack-mirror-pages.sh /docker-entrypoint.d/
COPY --from=mirror-pages /mirror-pages.tar.zst /usr/share/nginx/mirror-pages.tar.zst

EXPOSE 8081

CMD ["nginx", "-g", "daemon off;"]

FROM nginxinc/nginx-unprivileged:alpine AS mirror-unprivileged

ARG GIT_COMMIT=unknown
ARG BUILD_DATE=unknown

LABEL org.opencontainers.image.source="https://github.com/redis/docs"
LABEL org.opencontainers.image.revision="${GIT_COMMIT}"
LABEL org.opencontainers.image.created="${BUILD_DATE}"
LABEL org.opencontainers.image.variant="mirror-unprivileged"

USER root
RUN apk add --no-cache zstd && install -d -m 1777 /usr/share/nginx/pages
USER 101

COPY build/marketing_mirror/runtime/nginx.conf /etc/nginx/conf.d/default.conf
COPY --chown=nginx:nginx mirror/site/sanity /usr/share/nginx/html/sanity
COPY --chown=nginx:nginx mirror/site/_next /usr/share/nginx/html/_next
COPY --from=mirror-pages --chown=nginx:nginx /site /usr/share/nginx/html
COPY --chown=nginx:nginx build/marketing_mirror/runtime/*.js /usr/share/nginx/html/_mirror/
COPY --chmod=755 build/marketing_mirror/runtime/05-unpack-mirror-pages.sh /docker-entrypoint.d/
COPY --from=mirror-pages /mirror-pages.tar.zst /usr/share/nginx/mirror-pages.tar.zst

EXPOSE 8081

CMD ["nginx", "-g", "daemon off;"]

# ============================================================
# Final stage: select variant via build arg
# ============================================================
FROM runtime-${VARIANT} AS final
