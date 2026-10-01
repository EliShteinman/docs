<!-- short: The redis.io blog and tutorials and other marketing sections mirrored for the air-gapped Redis docs -->
# redis.io sections, mirrored

The parts of redis.io the air-gapped
[`a0533057932/redis-docs`](https://hub.docker.com/r/a0533057932/redis-docs) site links
out to — the blog, tutorials, customer stories, comparisons, solutions, technology pages
and architecture diagrams — captured as redis.io renders them and served by nginx, with
no internet access. About 1,400 pages and the 238 MB of pictures they use.

They ship apart from the documentation so a deployment that does not want them does not
carry them. `mirror.ndjson`, the same feed shape as the site's `docs.ndjson`, lets the
search service index them next to the documentation.

## Tags

| Tag | What it is | Port |
|-----|------------|------|
| `latest`, `<commit-sha>` | privileged (`nginx:alpine`) | 80 |
| `unprivileged`, `<commit-sha>-unprivileged` | unprivileged (non-root) | 8080 |

The same commit builds this image and the site's, so `<commit-sha>` names a matching
pair. Every tag is built for `linux/amd64` and `linux/arm64`, and carries its one-line
description as the `org.opencontainers.image.description` label.

## Use

The Helm chart deploys it next to the site with `mirror.enabled=true`; the site's nginx
sends the mirrored paths to it. The chart is published alongside the site image as an
OCI artifact:

```bash
helm pull oci://registry-1.docker.io/a0533057932/redis-docs --version 3.0.4
```

Its values are documented in the
[source repository](https://github.com/EliShteinman/docs/tree/feature/docker-support/helm/redis-docs).
