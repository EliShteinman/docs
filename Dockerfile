# syntax=docker/dockerfile:1

ARG VARIANT=privileged

# ============================================================
# Builder stage (shared by both variants)
# ============================================================
FROM node:24-trixie AS builder

ARG HUGO_VERSION=0.143.1
ARG TARGETARCH
ARG GIT_COMMIT=unknown
ARG BUILD_DATE=unknown

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
    "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-${TARGETARCH}.deb" \
    && dpkg -i /tmp/hugo.deb \
    && rm /tmp/hugo.deb

WORKDIR /site

COPY package.json ./
RUN npm install

COPY requirements.txt ./
RUN python3 -m venv /venv && /venv/bin/pip install -r requirements.txt

COPY . .

ENV PATH="/venv/bin:$PATH"

RUN sed -i 's#baseURL = "https://redis.io"#baseURL = "/"#g' config.toml
# Hugo per-partial timeout: upstream sets 75s, which fits CI but not multi-platform
# Docker builds where dynacache is constantly evicted under memory pressure and
# QEMU-emulated amd64 plus parallel arm64 share a single host's resources.
RUN sed -i 's/timeout="75"/timeout="600"/' config.toml

RUN find content/operate/kubernetes -maxdepth 1 -type d -regex '.*[0-9]' -printf '%f\n' | sort > kubernetes-versions && \
    find content/operate/rs -maxdepth 1 -type d -regex '.*[0-9]' -printf '%f\n' | sort > rs-versions && \
    find content/integrate/redis-data-integration -maxdepth 1 -type d -regex '.*[0-9]' -printf '%f\n' | sort > rdi-versions && \
    find content/develop/ai/redisvl -maxdepth 1 -type d -regex '.*[0-9]' -printf '%f\n' | sort > redisvl-versions

# Air-gap nav alignment: applied at build time only so the source tree stays identical
# to upstream redis/docs (no merge conflicts on `git pull`).
#  1. Relax the version-selector URL regex in scripts.html so the dropdown shows on
#     any baseURL — upstream regex requires `/docs/latest/` or `/docs/staging/`.
#  2. Inject `hidden: true` into version-directory `_index.md` files so they stop
#     appearing as standalone nav items. Uses upstream's existing `Params.hidden`
#     filter (`docs-nav.html` line 6).
RUN python3 <<'PYEOF'
import re, glob, os, pathlib

scripts_path = pathlib.Path("layouts/partials/scripts.html")
text = scripts_path.read_text()
text, n_op = re.subn(
    r"new RegExp\('/docs/\(latest\|staging\\/\.\+\)/operate/(\w+)/\.\*'\)",
    r"new RegExp('/operate/\1/')",
    text,
)
text, n_dev = re.subn(
    r"new RegExp\('/docs/\(latest\|staging\\/\.\+\)/develop/ai/(\w+)/\.\*'\)",
    r"new RegExp('/develop/ai/\1/')",
    text,
)
scripts_path.write_text(text)
assert n_op + n_dev == 3, f"expected 3 regex relaxations, got {n_op + n_dev}"

VERSION_RE = re.compile(r"^\d+\.\d+(\.\d+)?$")
patched = 0
for pattern in ("content/operate/rs/*/_index.md",
                "content/operate/kubernetes/*/_index.md",
                "content/develop/ai/redisvl/*/_index.md"):
    for path in glob.glob(pattern):
        if not VERSION_RE.match(os.path.basename(os.path.dirname(path))):
            continue
        p = pathlib.Path(path)
        s = p.read_text()
        if not s.startswith("---"):
            continue
        try:
            _, frontmatter, body = s.split("---", 2)
        except ValueError:
            continue
        if re.search(r"^hidden:\s*true\s*$", frontmatter, re.M):
            continue
        if re.search(r"^hidden:", frontmatter, re.M):
            frontmatter = re.sub(r"^hidden:.*$", "hidden: true", frontmatter, count=1, flags=re.M)
        else:
            frontmatter = frontmatter.rstrip() + "\nhidden: true\n"
        p.write_text(f"---{frontmatter}---{body}")
        patched += 1
assert patched > 0, "no version _index.md files were patched"
print(f"airgap-nav: relaxed {n_op + n_dev} JS regex(es), hid {patched} version dir(s)")
PYEOF

RUN --mount=type=secret,id=PRIVATE_ACCESS_TOKEN,env=PRIVATE_ACCESS_TOKEN \
    make components && make ndjson

RUN find /site/public -type f \( -name "*.html" -o -name "*.css" -o -name "*.js" -o -name "*.json" -o -name "*.xml" -o -name "*.svg" -o -name "*.txt" \) \
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
