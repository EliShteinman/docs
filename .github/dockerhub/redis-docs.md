<!-- short: Air-gapped Redis documentation site — the nginx image and the Helm chart that deploys it -->
# Redis documentation, air-gapped

The Redis documentation site, built with Hugo and served by nginx, packaged to run
with no internet access at all. Every page, every documented product version and
every asset they need is inside the image.

## Tags

| Tag | What it is | Port | Use |
|-----|------------|------|-----|
| `latest`, `<commit-sha>` | image, privileged (`nginx:alpine`) | 80 | `docker run`, Docker Compose |
| `unprivileged`, `<commit-sha>-unprivileged` | image, unprivileged | 8080 | Kubernetes / OpenShift (non-root, read-only root filesystem) |
| `<commit-sha>-mirror`, `mirror` | image, the mirrored redis.io sections | 80 | Optional second pod (`mirror.enabled`) |
| `<commit-sha>-mirror-unprivileged`, `mirror-unprivileged` | the same, non-root | 8080 | Kubernetes / OpenShift |
| `X.Y.Z` | **the Helm chart**, as an OCI artifact | — | `helm pull` (see below) |

Every image tag is built for `linux/amd64` and `linux/arm64`. A plain `X.Y.Z` tag is
not an image: it is the chart that deploys these images, published to this same
repository.

## What is inside

- The documentation in full, including each versioned product tree.
- The glossary, and the documentation's own assets.
- The other redis.io sections the documentation links out to — blog, tutorials,
  customer stories, comparisons, solutions — are mirrored too, but ship in the
  `mirror` tags above rather than here, so a deployment that does not want 1,400
  extra pages and 238 MB of pictures does not carry them.
- `docs.ndjson`, the feed that the search service and RAG consumers read.

## Quick start

```bash
docker run -p 8080:80 a0533057932/redis-docs:latest
```

For Kubernetes or OpenShift, use the unprivileged variant:

```bash
docker run -p 8080:8080 a0533057932/redis-docs:unprivileged
```

## Search and the CLI playground

Both are optional and neither lives in this image: they run as their own pods from
[`a0533057932/redis-docs-cli`](https://hub.docker.com/r/a0533057932/redis-docs-cli),
and the Helm chart turns them on with `search.enabled` and `cli.enabled`.

## Helm chart

The chart deploys the site, and optionally the search and CLI pods, with metrics,
autoscaling, OpenShift Route support and hierarchical control over which external
links the pages keep. It is published here as an OCI artifact:

```bash
helm pull oci://registry-1.docker.io/a0533057932/redis-docs --version 2.0.2
helm install redis-docs oci://registry-1.docker.io/a0533057932/redis-docs --version 2.0.2
```

Its values, defaults and examples are documented in the
[source repository](https://github.com/EliShteinman/docs/tree/feature/docker-support/helm/redis-docs).

## Carrying this into an air-gapped network

The chart pulls more than this image, so mirror all of these into the internal
registry — the tags are the chart's defaults, and `helm show values` confirms them
for the version you took:

| Image | Needed for |
|-------|------------|
| `a0533057932/redis-docs` | the site itself |
| `a0533057932/redis-docs-cli` | search (`search.enabled`) and the CLI playground (`cli.enabled`) |
| `a0533057932/redis-docs` (`mirror-unprivileged`) | the mirrored redis.io sections (`mirror.enabled`) |
| `redis:8.10.0-alpine` | the Redis behind each of those two — the query engine search indexes into |
| `quay.io/martinhelmich/prometheus-nginxlog-exporter` | metrics (`metrics.enabled`) |
| `quay.io/jupyter/minimal-notebook` | the notebook sidecar (`cli.jupyter.enabled`) |

The chart itself travels the same way: `helm pull` it outside, then
`helm push` the `.tgz` to the internal registry.
