<!-- short: CLI playground proxy and docs search API for the air-gapped Redis docs -->
# CLI playground and docs search

Two services for the air-gapped
[`a0533057932/redis-docs`](https://hub.docker.com/r/a0533057932/redis-docs) site, in
one image:

- **CLI playground proxy** (`main:app`, port 8090) runs the commands a reader types
  into the terminal on a documentation page. Each browser session gets its own slice
  of the keyspace and its own connection, and every command goes through a
  restricted ACL user, so one reader cannot reach another reader's keys or the
  server itself.
- **Docs search API** (`search.main:app`, port 8091) indexes the `docs.ndjson` feed
  the site image ships into the Redis 8 query engine, and answers the search box on
  the site. Without it that search reaches a service on redis.io, which an
  air-gapped network cannot.

They share an image because they share the same Flask, the same gunicorn and the
same RESP client, and a third image would be a third thing to carry through the air
gap. The Helm chart runs each from its own deployment with its own command, so
enabling one does not enable the other.

## Tags

`X.Y.Z` — what the chart pins — and `latest`. Every tag is built for `linux/amd64`
and `linux/arm64`, and a new one is published whenever the source changes. `0.6.0` is
the first tag carrying the search service; an older tag has no `search` module and
the search pod crash-loops.

## Use

This image is not meant to be run on its own: both services expect a Redis 8 (the
query engine is required for search) reachable in the same pod, and the search
service also expects the site's feed. The Helm chart wires all of that up, and is
published alongside the site image as an OCI artifact:

```bash
helm pull oci://registry-1.docker.io/a0533057932/redis-docs --version 2.0.5
```

Its values are documented in the
[source repository](https://github.com/EliShteinman/docs/tree/feature/docker-support/helm/redis-docs).
