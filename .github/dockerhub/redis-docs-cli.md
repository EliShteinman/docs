<!-- short: CLI playground proxy for the air-gapped Redis docs — runs the commands readers type on a page -->
# CLI playground proxy

The proxy behind the in-page Redis terminal of the air-gapped
[`a0533057932/redis-docs`](https://hub.docker.com/r/a0533057932/redis-docs) site. It
runs the commands a reader types on a documentation page (`main:app`, port 8090).
Each browser session gets its own slice of the keyspace and its own connection, and
every command goes through a restricted ACL user, so one reader cannot reach another
reader's keys or the server itself.

The docs search API used to ship in this image. It has its own now:
[`a0533057932/redis-docs-search`](https://hub.docker.com/r/a0533057932/redis-docs-search).

## Tags

`X.Y.Z` — what the chart pins — and `latest`. Every tag is built for `linux/amd64`
and `linux/arm64`, and a new one is published whenever the source changes. Each
image carries its one-line description as the `org.opencontainers.image.description`
label, so a version keeps the text it was built with:

```bash
docker buildx imagetools inspect a0533057932/redis-docs-cli:<tag> \
  --format '{{json .Image}}' | jq '.["linux/amd64"].config.Labels'
```

## Use

This image is not meant to be run on its own: it expects a Redis reachable next to
it, holding the ACL user the chart creates. The Helm chart wires that up, and is
published alongside the site image as an OCI artifact:

```bash
helm pull oci://registry-1.docker.io/a0533057932/redis-docs --version 3.0.9
```

Its values are documented in the
[source repository](https://github.com/EliShteinman/docs/tree/feature/docker-support/helm/redis-docs).
