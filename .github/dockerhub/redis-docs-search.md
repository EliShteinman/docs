<!-- short: Docs search API for the air-gapped Redis docs — indexes the site's feed into the Redis query engine -->
# Docs search API

The search service behind the search box of the air-gapped
[`a0533057932/redis-docs`](https://hub.docker.com/r/a0533057932/redis-docs) site
(`search.main:app`, port 8091). At startup it indexes the `docs.ndjson` feed the site
image ships — and the mirrored redis.io sections' `mirror.ndjson`, when they are
deployed — into the Redis 8 query engine, then answers the site's searches. Without
it the search box reaches a service on redis.io, which an air-gapped network cannot.

Documentation results come first; the mirrored sections are grouped under Blog,
Tutorials and More from Redis.

## Tags

`X.Y.Z` — what the chart pins — and `latest`. Every tag is built for `linux/amd64`
and `linux/arm64`, and a new one is published whenever the source changes. Each
image carries its one-line description as the `org.opencontainers.image.description`
label, so a version keeps the text it was built with:

```bash
docker buildx imagetools inspect a0533057932/redis-docs-search:<tag> \
  --format '{{json .Image}}' | jq '.["linux/amd64"].config.Labels'
```

## Use

This image is not meant to be run on its own: it expects a Redis 8 with the query
engine next to it and the site's feed on disk. The Helm chart wires that up with
`search.enabled`, and is published alongside the site image as an OCI artifact:

```bash
helm pull oci://registry-1.docker.io/a0533057932/redis-docs --version 2.0.5
```

Its values are documented in the
[source repository](https://github.com/EliShteinman/docs/tree/feature/docker-support/helm/redis-docs).
