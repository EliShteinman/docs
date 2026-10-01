# Upgrading to 3.0: two pods, four images

> **[גרסה בעברית](UPGRADE-3.0-he.md)**

This covers the move from 2.x to 3.0 only. Everything else is in [README.md](README.md).

## What changed

| | 2.x | 3.0 |
|---|---|---|
| **Pods** | up to 4: site, CLI, search, mirror | up to 2: the site (with the mirror), and services (CLI and search) |
| **Search image** | inside `redis-docs-cli` | its own `redis-docs-search` |
| **Mirror image** | `redis-docs:<hash>-mirror-unprivileged` | `redis-docs-mirror:<hash>-unprivileged` |
| **Mirror port** | 8080 | 8081 — it now sits next to the site's nginx |
| **Search Redis** | 6379, in its own pod | 6380, in the services pod beside the CLI's Redis (6379) |
| **Jupyter** (`cli.jupyter`) | optional sidecar | removed |
| **Metrics** (`metrics`) | nginxlog-exporter sidecar, Route, ServiceMonitor, Grafana dashboard | removed. nginx logs go to stdout/stderr (`oc logs`) |

## Step 1: Mirror the images into the internal registry

Skip the mirror line if you do not deploy the mirror, and `redis-docs-search` if you do
not deploy search.

```bash
REG=registry.internal.company.com
HASH=<hash>          # the site's tag
MIRROR=<mirror-tag>  # the mirror's own tag; it changes only when the mirror does

skopeo copy docker://a0533057932/redis-docs:$HASH-unprivileged          docker://$REG/redis-docs:$HASH-unprivileged
skopeo copy docker://a0533057932/redis-docs-mirror:$MIRROR-unprivileged docker://$REG/redis-docs-mirror:$MIRROR-unprivileged
skopeo copy docker://a0533057932/redis-docs-cli:<cli-tag>             docker://$REG/redis-docs-cli:<cli-tag>
skopeo copy docker://a0533057932/redis-docs-search:<search-tag>       docker://$REG/redis-docs-search:<search-tag>
```

Take every tag from `helm show chart` for the chart version you install: its
`artifacthub.io/images` annotation lists each image pinned. `redis:8.10.0-alpine` did
not change.

**The new mirror image is required.** The old one listens on 8080, the same port as the
site. In 3.0 both are in one pod, so the container fails with
`nginx: [emerg] still could not bind()`. In testing, the rolling update kept the previous
site pod serving, so the site stayed up, but the upgrade does not complete.

## Step 2: Update your values file

**Keys whose value changes:**

| Key | Old | New |
|---|---|---|
| `mirror.image.name` | `redis-docs` | `redis-docs-mirror` |
| `mirror.image.tag` | `<hash>-mirror-unprivileged` | `<hash>-unprivileged` |
| `search.image.name` | `redis-docs-cli` | `redis-docs-search` |
| `search.image.tag` | same as `cli.image.tag` | its own tag, for example `0.1.0` |

**Keys that were removed.** Helm ignores them, and in testing an upgrade with an old
values file that still had them went through without errors. Delete them anyway, so the
file describes what actually runs.

| Key | Why it was removed |
|---|---|
| `metrics.*` (the whole block: `enabled`, `image`, `resources`, `route`, `serviceMonitor`) | the exporter was not used |
| `cli.jupyter.*` (the whole block) | a Jupyter server with no token, no password and no XSRF protection. Every link sent to it was a BinderHub launch path, which a plain Jupyter server does not answer |
| `mirror.replicas` | the mirror is a container in the site's pod and scales with it (`replicaCount` / `autoscaling`) |
| `mirror.containerPort` | fixed at 8081 in both image variants |
| `search.replicas` | the services pod always runs one replica, because the CLI keeps sessions in memory |

## Step 3: Upgrade

```bash
helm upgrade redis-docs oci://$REG/redis-docs --version 3.0.1 -f my-values.yaml  # the first 3.0 release published; a later 3.0.x works the same
```

**Do not rely on `--reuse-values` alone.** It keeps the old `mirror.image.name: redis-docs`
and `search.image.name: redis-docs-cli`. If you use it, add the four keys from the table
in step 2 with `--set`.

**What happens during the upgrade:**
- The `redis-docs-cli`, `redis-docs-search` and `redis-docs-mirror` deployments are deleted.
- So are the `redis-docs-mirror` Service, the metrics ConfigMap, the metrics Route and the
  ServiceMonitor.
- `redis-docs-services` is created and starts building the search index.
- The site updates with a rolling update, without downtime.
- The PodDisruptionBudget now covers the site's pods only. Before, it covered every pod
  in the release.
- The CLI and search are unavailable for a minute or two, until the services pod finishes
  indexing. With `Recreate` this happens on every upgrade, not only this one.

## Step 4: Verify

```bash
kubectl get deploy,pods
# redis-docs            2/2 (1/1 without the mirror)
# redis-docs-services   4/4 (2/2 with only the CLI or only search)

kubectl rollout status deploy/redis-docs-services
kubectl exec deploy/redis-docs-services -c cli-redis    -- redis-cli ACL DRYRUN docsandbox FT._LIST   # OK
kubectl exec deploy/redis-docs-services -c search-redis -- redis-cli -p 6380 FT._LIST                 # docs
```

In a browser: a documentation page, `/blog/` (if the mirror is on), a search, and Try it.

## Rolling back

```bash
helm history redis-docs
helm rollback redis-docs <revision-before-3.0>
```

In testing, the rollback brought back the four old deployments. There is no data to keep:
the index is rebuilt on every start, and the CLI's Redis is disposable.

## Recommended resources per pod

Measured per container in kind and local Docker, on the full corpus: 7,554 documents, 6,136
documentation and 1,418 mirrored. On OpenShift, once indexed, the site pod used 28Mi and the
services pod 222Mi in all.

| Container | Measured | Default (requests → limits) | Recommendation |
|---|---|---|---|
| **Pod 1: `redis-docs`** | | | |
| `redis-docs` (nginx) | 22Mi | `250m/256Mi → 1/512Mi` | the default. The `canonicalURL` and downloads init containers run with the same resources |
| `mirror` | 11Mi | `50m/64Mi → 500m/256Mi` | the default |
| **Pod 1 total** | | `300m/320Mi → 1.5/768Mi` | |
| **Pod 2: `redis-docs-services`** | | | |
| `cli-proxy` | 39Mi | `50m/64Mi → 200m/128Mi` | the default |
| `cli-redis` | 7Mi empty, grows with what readers write | `50m/64Mi → 200m/128Mi` | the default. The limit is what stops a reader from filling the sandbox |
| `search-api` | 40Mi, peaking at 125Mi and one core while indexing | `100m/128Mi → 500m/512Mi` | the default. With a `500m` limit, indexing just takes a little longer |
| `search-redis` | 135–156Mi after indexing | `100m/512Mi → 500m/1Gi` | can drop to `100m/256Mi → 500m/512Mi`. Otherwise keep it, since the corpus grows with every documentation release |
| **Pod 2 total (defaults)** | | `300m/768Mi → 1.4/1.75Gi` | |

In total, with everything on: requests of `600m` and `~1.1Gi`, limits of `2.9` cores and
`~2.5Gi`.

**Pod quota:** during an upgrade, the site (rolling update) briefly runs one extra pod. The
services pod (`Recreate`) does not. So with `replicaCount: 1` and everything on, you need a
quota of 3 pods: two permanent, plus one temporary for the site.
