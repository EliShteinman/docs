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

COPY . .

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

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]

# ============================================================
# Final stage: select variant via build arg
# ============================================================
FROM runtime-${VARIANT} AS final
