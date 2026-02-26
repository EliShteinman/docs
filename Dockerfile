# syntax=docker/dockerfile:1
FROM node:22-bookworm AS builder

ARG HUGO_VERSION=0.143.0
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

RUN --mount=type=secret,id=github_token \
    PRIVATE_ACCESS_TOKEN=$(cat /run/secrets/github_token) \
    make components && make hugo

FROM nginxinc/nginx-unprivileged:alpine

ARG GIT_COMMIT=unknown
ARG BUILD_DATE=unknown

LABEL org.opencontainers.image.source="https://github.com/redis/docs"
LABEL org.opencontainers.image.revision="${GIT_COMMIT}"
LABEL org.opencontainers.image.created="${BUILD_DATE}"

COPY --from=builder --chown=nginx:nginx /site/public /usr/share/nginx/html

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
