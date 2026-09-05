# Redis Docs Helm Chart

> **[גרסה בעברית](README-he.md)**

Helm chart for installing the Redis documentation site on Kubernetes / OpenShift.
Designed for air-gapped networks - no external dependencies.

## Prerequisites

- Kubernetes 1.26+ / OpenShift 4.x+
- Helm 3.x
- Private Docker registry (in air-gapped networks)

## Architecture

The chart deploys two main pods:

### Pod 1 — `redis-docs` (documentation site)

| Container | Description | Port |
|---|---|---|
| `nginx` | Main web server (unprivileged) | 8080 |
| `metrics` (optional) | sidecar — prometheus-nginxlog-exporter | 4040 |

nginx also serves as a reverse proxy:
- `/cli` → routed to CLI proxy in the second pod (port 8090)
- `/jupyter/` → routed to Jupyter in the second pod (port 8888), including WebSocket support

### Pod 2 — `redis-docs-cli` (CLI playground)

Created only when `cli.enabled=true`.

| Container | Description | Port |
|---|---|---|
| `cli-proxy` | Flask proxy for executing Redis commands | 8090 |
| `redis` | Redis sidecar — local to pod (localhost) | 6379 |
| `jupyter` (optional) | Jupyter kernel server for interactive code execution | 8888 |

All containers in this pod communicate over `localhost`. Port 6379 is a container port
only — no Service exposes it — but any pod that can reach the pod IP can still reach Redis
directly, which is a NetworkPolicy question rather than something the chart settles.

#### CLI playground isolation

Every visitor shares one Redis database, so without this two readers working through the same
tutorial write to the same `product:1` and overwrite each other. Three mechanisms keep them
apart, all on by default:

| Mechanism | Value | What it does |
|---|---|---|
| Restricted user | `cli.redis.acl.enabled` | Commands run as `docsandbox`, whose rules live in `files/sandbox.acl`. Blocks `FLUSHALL`, `RANDOMKEY`, `SELECT`, `DUMP`, `CONFIG`, `MONITOR` and the rest of what would reach past a session. |
| Namespacing | `cli.namespace.enabled` | Each session gets a key prefix. Commands go out under it and replies come back without it, so a reader types `SET product:1` and `KEYS *` answers `product:1`. Search indexes are scoped the same way. |
| Session limits | `cli.session.*` | A session holds a Redis connection of its own so a `MULTI` survives between typed commands, so it is bounded: closed after `idleTtlSeconds`, and the least recently used goes first at `max`. |

`cli.namespace.cleanup.enabled` deletes a session's keys and indexes when it is reclaimed;
without it they accumulate, since the sidecar Redis has no eviction policy.

The ACL file cannot name module commands — Redis parses it before it registers the bundled
modules and aborts startup on an unknown command — so a `postStart` hook grants `FT._LIST`,
`FT.DROPINDEX` and `FT.TAGVALS` once the modules are up. To confirm it ran:

```bash
kubectl exec deploy/redis-docs-cli -c redis -- redis-cli ACL DRYRUN docsandbox FT._LIST
# OK
```

Turning any of these off is a deliberate downgrade: `namespace.enabled=false` puts every reader
back in one flat keyspace, and `acl.enabled=false` puts the proxy back on Redis's default user
with nothing between a typed `FLUSHALL` and everyone else's data.

### Runtime Configuration

Four ConfigMaps carry runtime configuration; two are always rendered, two follow their feature flag:

- **`configmap-runtime.yaml`** — produces `runtime-config.js`, loaded by every page. Holds:
  - `cli` — whether the CLI playground is deployed, and the URL the "Try it" buttons open. With `cli.enabled=false` the buttons are hidden instead of pointing at redis.io.
  - `aiServices.litellm` — LiteLLM endpoint URL (replaces external CloudFront)
  - `aiServices.binder.url` — BinderHub / JupyterHub URL, also used by the Jupyter cell buttons
  - `downloads` — whether the documentation download widget has archives to offer
  - `externalLinks` — the resolved enabled/url for every catalogued external link
  - `gitMirrors` — the resolved mirror host for every catalogued Git URL
- **`configmap.yaml`** — the nginx `default.conf`. It uses `canonicalURL` to substitute `__DOCS_BASE_URL__` placeholders inside `.md` / `.json` responses at HTTP response time, and proxies `/cli` to the CLI playground service.
- **`configmap-metrics.yaml`** — the nginxlog-exporter configuration. Only with `metrics.enabled=true`.
- **`configmap-cli-acl.yaml`** — the Redis ACL file from `files/sandbox.acl`, mounted into the Redis sidecar. Only with `cli.redis.acl.enabled=true`; see [CLI playground isolation](#cli-playground-isolation).

### External Links (externalLinks)

The site contains ~87 external links scattered across the home-page body, the
top header (logo, marketing nav, dropdown menus), and the bottom footer.
Almost none of them work in an air-gapped install. Configuration is driven
by a five-layer hierarchy:

```
externalLinks.enabled                    ← master kill-switch
└── families
    ├── home          (7 keys)
    │   └── links: { sandbox, tutorials, university, blog, support, github, chatbot }
    ├── header        (5 keys, 4 sub-families)
    │   └── sub-families: { main-nav, cta, search, mobile }
    └── footer        (23 keys, 6 sub-families)
        └── sub-families: { social, legal, compare, company,
                            cloud-partners, services }
```

The full catalog (every key with its description and upstream URL) ships
inside the chart at `files/external-links.yaml`. Do not edit it for
per-deployment customization — that is what `values.yaml` is for.

**Precedence for `enabled`** (highest wins):

1. `overrides.<key>.enabled` — per-link override
2. `families.<fam>.sub-families.<sub>.enabled` — sub-family kill-switch
3. `families.<fam>.enabled` — family kill-switch
4. `externalLinks.enabled` — master kill-switch
5. catalog default — always `true`

`url` resolution is simpler: catalog default unless `overrides.<key>.url` replaces it.

**The chart default is `enabled: false`** — every external link is hidden out of
the box. Opt back in at whichever level fits the deployment:

```yaml
externalLinks:
  enabled: false             # master kill-switch (default)
  families:
    home:
      enabled: true          # all home-page links back on
    header:
      sub-families:
        main-nav:
          enabled: true      # header strip: only Redis-for-AI / Docs / Pricing
  overrides:
    tutorials:
      enabled: true          # opt one specific link back in
    github:
      enabled: true
      url: "https://gitlab.internal.company.com/redis-docs"  # also rewrite URL
    nav-search:
      enabled: false         # explicitly keep a link hidden
```

The two logos (top-left of the header, top-left of the footer) always link
to `/` (the local docs home) and are not part of the catalog — they are
shown unconditionally and not configurable per deployment.

### Git mirrors (`externalLinks.gitMirrors`)

A separate mechanism rewrites inline `<a href>` links inside markdown
content (Grafana dashboard URLs, Prometheus alert configs, repository
listings, etc.) from the upstream public Git host to an internal mirror.

It is **not** part of the `families` / `overrides` system above — those
target layout elements with `data-external-link="<key>"` attributes
(home page cards, header strip, footer columns). `gitMirrors` matches by
URL prefix on the rendered HTML, which is what inline content links need.

Catalog of available mirrors lives at `files/external-links.yaml` under
`git-mirrors:`. Each entry has a fixed upstream `from` URL — the chart
ships two entries today:

| Name | Upstream | Affected docs |
|---|---|---|
| `observability` | `https://github.com/redis-field-engineering/redis-enterprise-observability` | 36 inline links across `rs-observability.md`, `rs-prometheus-grafana-quickstart.md`, `prometheus-with-redis-cloud/_index.md` |
| `k8s-docs` | `https://github.com/RedisLabs/redis-enterprise-k8s-docs` | ~179 inline links across ~89 files under `content/operate/kubernetes/` (operator releases, API reference, manifests, vault, rack-awareness) |

Per-deployment activation is two fields in `values.yaml` per mirror:

```yaml
externalLinks:
  gitMirrors:
    observability:
      enabled: true
      to: "https://gitlab.internal.company.com/redis/group1/group2/observability"
    k8s-docs:
      enabled: true
      to: "https://gitlab.internal.company.com/redis/k8s/redis-enterprise-k8s-docs"
```

> The handler rewrites only `<a href>` URLs (clickable links). `curl` /
> `kubectl apply -f` commands inside fenced code blocks that reference
> `raw.githubusercontent.com/...` are not rewritten — those need a
> separate build-time substitution if required.

The `to` URL is treated as an opaque prefix — provide the full project
URL including any nested GitLab groups. The runtime handler translates
GitHub paths (`/blob/<ref>/<path>`, `/tree/<ref>/<path>`, `/raw`,
`/blame`, `/commits`, `/commit`, `/tags`, `/releases`, `/wiki`,
`/issues`) to their GitLab equivalents (`/-/blob/...`, `/-/tree/...`,
etc.) automatically.

**Activation is purely Helm-driven**: changing `values.yaml` regenerates
the runtime ConfigMap (`runtime-config.js`), and the
`checksum/runtime-config` annotation triggers a rolling restart. No
image rebuild is required, and the same image can serve different
mirror URLs per deployment.

**Adding a new mirror** (e.g. another upstream repo referenced from the
docs) is two steps: add an entry under `git-mirrors:` in the catalog
with its `from` URL, then opt in per-deployment with `enabled: true`
and `to: <mirror URL>` in `values.yaml`. No template, handler, or
Hugo / image change is needed.

### Canonical URL substitution (`canonicalURL`)

When Hugo builds the AI / RAG output formats (`.md`, `.json`) it expands
internal shortcodes like `{{< relref "..." >}}` and `{{< image filename="..." >}}`
into a placeholder, `__DOCS_BASE_URL__/<path>`. nginx substitutes the
placeholder at response time so consumers that ingest the markdown without
HTML context still see fully-qualified URLs:

```yaml
canonicalURL: "https://docs.intranet.example.com"
```

When `canonicalURL` is empty (default), nginx falls back to
`$scheme://$http_host` from the request — the same image deployed at
multiple internal hostnames yields per-host URLs.

The `sub_filter` is scoped to `.md` / `.json` only. HTML / CSS / JS responses
are never rewritten, and the placeholder is only emitted at four well-defined
points inside `process-markdown-content.html` (relref + image shortcodes),
so external URLs an author wrote by hand in markdown remain untouched.

### Documentation downloads (`downloads`)

Every documentation page carries a **Download documentation** button. It offers
each product as a `.tar.gz` in Markdown (one file per page, or one file per
product), offline-browsable HTML, or JSON.

The archives hold absolute links, so they are only correct once the site's base
URL is fixed. An init container therefore packs them at pod start, writing this
deployment's own `canonicalURL` into every one, and nginx serves them from a
per-pod `emptyDir`. Nothing is baked into the image, and nothing reaches
`redis.io`.

```yaml
canonicalURL: "https://docs.intranet.example.com"   # required
downloads:
  enabled: true
  formats: "md,md-single,json,html"
  sourceURL: "https://git.intranet.example.com/docs" # empty omits the line
```

Downloads need `canonicalURL`. Without it the base URL is resolved per request
from the `Host` header, which no file on disk can carry — so packing is skipped
and the button is removed from the page rather than left to return 404s. Setting
`downloads.enabled: false` removes it the same way.

**`html` costs far more than the other three formats.** It is roughly 89% of
both the packed size and the packing time, because every page is rewritten to
resolve from disk and its assets are collected alongside. Dropping it takes the
packed set from ~280 MB to ~30 MB and the pack from minutes to seconds:

```yaml
downloads:
  formats: "md,md-single,json"
```

Two settings follow from the size and the time:

- `resources.limits.ephemeral-storage` must hold the packed set. The chart
  defaults to `1Gi`, enough for all four formats.
- `progressDeadlineSeconds` defaults to `1800` here, because packing `html` on a
  throttled node can outrun Kubernetes' own 600-second default and fail a
  rollout that is in fact progressing normally.

Packing is CPU-bound and happens once per pod start. `downloads.resources`
overrides `resources` for that init container alone:

```yaml
downloads:
  resources:
    limits:
      cpu: "4"
```

**Raise the limit, not the request.** Kubernetes sets a pod's resource request to
`max(init containers, sum(containers))`, so a request set here becomes the whole
pod's request for its entire life — long after packing has finished and nginx is
the only thing running. A rolling update then has to fit that request twice at
once, which is enough to make the new pod unschedulable under a namespace quota.
A limit costs nothing until the container actually runs.

## Docker images

| Image | Tag | Port | Usage | Required? |
|---|---|---|---|---|
| `a0533057932/redis-docs` | `<HASH>` / `latest` | 80 | Standard run with `docker run` (privileged) | Yes — one of the two |
| `a0533057932/redis-docs` | `<HASH>-unprivileged` / `unprivileged` | 8080 | Kubernetes / OpenShift (non-root) | Yes — one of the two |
| `quay.io/martinhelmich/prometheus-nginxlog-exporter` | `v1.11.0` | 4040 | Prometheus metrics (including response times) | No — only if `metrics.enabled=true` |
| `a0533057932/redis-docs-cli` | `latest` / `0.4.0` | 8090 | CLI playground proxy (Flask) | No — only if `cli.enabled=true` |
| `redis` | `8.10.0-alpine` | 6379 | Redis sidecar for CLI playground | No — only if `cli.enabled=true` |
| `quay.io/jupyter/minimal-notebook` | `2026-04-02` | 8888 | Jupyter kernel server for interactive code execution | No — only if `cli.jupyter.enabled=true` |

> For Kubernetes/OpenShift use the `unprivileged` or `<HASH>-unprivileged` tag.
> For standard `docker run` use the `latest` or `<HASH>` tag.
> In air-gapped networks it is recommended to use a hash-based tag (Artifactory requires a tag other than `latest`).
> For image build documentation see `BUILD.md` in the project root.

## Installation

### Basic usage

```bash
helm install redis-docs redis-docs-1.9.0.tgz
```

### Installation with a values file

The recommended approach - a custom `values.yaml` file:

```bash
helm install redis-docs redis-docs-1.9.0.tgz -f my-values.yaml
```

Below is an example of a typical deployment scenario.

Ready-to-use values files are available in the `examples/` directory:

```bash
helm install redis-docs ./helm/redis-docs -f helm/redis-docs/examples/values-openshift-airgapped.yaml
```

### OpenShift — air-gapped network with metrics

```yaml
# my-values.yaml

# --- Single replica ---
replicaCount: 1

# --- Global registry override ---
global:
  registry: registry.internal.company.com

# --- Pull credentials ---
imagePullSecrets:
  - name: regcred

# --- Main image (specific tag override) ---
image:
  name: redis-docs
  tag: "4dfba535c-unprivileged"

# --- Metrics (image and tag override) ---
metrics:
  enabled: true
  image:
    name: prometheus-nginxlog-exporter
    tag: "v1.11.0"
  route:
    enabled: true
    # empty host = OpenShift generates an automatic hostname + automatic certificate

# --- Route (choose one of the 3 options) ---

# Option A: Automatic Route + automatic OpenShift TLS
route:
  enabled: true
  tls:
    enabled: true
    termination: edge

# Option B: Automatic Route without TLS (HTTP only)
# route:
#   enabled: true

# Option C: Custom Route + your own certificate
# route:
#   enabled: true
#   host: docs.apps.example.com
#   tls:
#     enabled: true
#     termination: edge
# tls:
#   enabled: true
#   certificate: |
#     -----BEGIN CERTIFICATE-----
#     ... (paste the certificate here)
#     -----END CERTIFICATE-----
#   privateKey: |
#     -----BEGIN PRIVATE KEY-----
#     ... (paste the private key here)
#     -----END PRIVATE KEY-----
#   caCertificate: |
#     -----BEGIN CERTIFICATE-----
#     ... (optional — CA certificate)
#     -----END CERTIFICATE-----

# --- Canonical public URL (used by nginx sub_filter for .md/.json) ---
# canonicalURL: "https://docs.intranet.company.com"   # leave empty to auto-detect from request

# --- External links ---
# Master kill-switch is on by default. Re-enable specific links via overrides.
externalLinks:
  enabled: false
  overrides:
    github:
      enabled: true
      url: "https://gitlab.internal.company.com/infra/redis-docs"
    support:
      enabled: true
      url: "https://support.internal.company.com"
```

> `global.registry` overrides the registry for all images. Overriding `image.name` and `image.tag` provides full control over each image.
>
> In air-gapped networks it is recommended to use a commit hash tag (Artifactory requires a tag other than `latest`).
>
> **Route — 3 options:**
> - **Option A** — OpenShift generates a hostname and automatic TLS certificate. The simplest approach.
> - **Option B** — HTTP only, no encryption.
> - **Option C** — Custom hostname + your own certificate. Requires setting `tls.certificate` and `tls.privateKey`.
>
> Metrics always get an automatic Route with OpenShift TLS (regardless of the option chosen for the site).

### TLS Certificate

The chart supports two ways to provide a TLS certificate:

#### Option 1: Paste the certificate directly

Paste the certificate text, private key, and CA (optional) directly in the values:

```yaml
# my-values.yaml
tls:
  enabled: true
  certificate: |
    -----BEGIN CERTIFICATE-----
    MIIDxTCCAq2gAwIBAgIQAqxcJmoLQJuPC3nyrkYldzANBgkqhkiG9w0BAQUFAMDx
    ... (paste the full certificate text here)
    -----END CERTIFICATE-----
  privateKey: |
    -----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC7o4qne60TB3pq
    ... (paste the full private key text here)
    -----END PRIVATE KEY-----
  caCertificate: |
    -----BEGIN CERTIFICATE-----
    MIIDrzCCApegAwIBAgIQCDvgVpBCRrGhdWrJWZHHSjANBgkqhkiG9w0BAQUFADBh
    ... (optional — paste the full CA certificate text here)
    -----END CERTIFICATE-----

route:
  enabled: true
  host: docs.apps.example.com
  tls:
    enabled: true
    termination: edge
```

> **Note:** The `certificate` and `privateKey` fields are required. The `caCertificate` field is optional.
>
> If you received a PFX file, extract the texts from it:
>
> ```bash
> openssl pkcs12 -in my-cert.pfx -clcerts -nokeys    # → certificate
> openssl pkcs12 -in my-cert.pfx -nocerts -nodes      # → privateKey
> openssl pkcs12 -in my-cert.pfx -cacerts -nokeys     # → caCertificate
> ```

#### Option 2: Use an existing Secret

```yaml
# my-values.yaml
tls:
  enabled: true
  existingSecret: "my-tls-secret"

route:
  enabled: true
  host: docs.apps.example.com
```

> The Secret must contain `tls.crt` and `tls.key` (type `kubernetes.io/tls`).

### If the registry requires authentication

```bash
kubectl create secret docker-registry regcred \
  --docker-server=REGISTRY \
  --docker-username=USER \
  --docker-password=PASS
```

Add to your values:

```yaml
imagePullSecrets:
  - name: regcred
```

## Air-Gapped Network Transfer

### Step 1: Save Docker images

```bash
# Main image (required)
docker pull a0533057932/redis-docs:unprivileged
docker save a0533057932/redis-docs:unprivileged -o redis-docs.tar

# Metrics (optional)
docker pull quay.io/martinhelmich/prometheus-nginxlog-exporter:v1.11.0
docker save quay.io/martinhelmich/prometheus-nginxlog-exporter:v1.11.0 -o nginx-exporter.tar

# CLI playground (optional)
docker pull a0533057932/redis-docs-cli:latest
docker save a0533057932/redis-docs-cli:latest -o redis-docs-cli.tar
docker pull redis:8.10.0-alpine
docker save redis:8.10.0-alpine -o redis.tar

# Jupyter kernel server (optional)
docker pull quay.io/jupyter/minimal-notebook:2026-04-02
docker save quay.io/jupyter/minimal-notebook:2026-04-02 -o jupyter.tar
```

### Step 2: Package the Helm chart

```bash
helm package helm/redis-docs/
# Produces: redis-docs-1.9.0.tgz
```

### Step 3: Transfer files to the air-gapped network

Transfer the following files:
- `redis-docs-1.9.0.tgz`
- `redis-docs.tar`
- `nginx-exporter.tar` (optional - metrics)
- `redis-docs-cli.tar` (optional - CLI)
- `redis.tar` (optional - CLI)
- `jupyter.tar` (optional - Jupyter)

### Step 4: Load into the private registry

```bash
# Load main image
docker load -i redis-docs.tar
docker tag a0533057932/redis-docs:unprivileged REGISTRY/redis-docs:unprivileged
docker push REGISTRY/redis-docs:unprivileged

# Load metrics (optional)
docker load -i nginx-exporter.tar
docker tag quay.io/martinhelmich/prometheus-nginxlog-exporter:v1.11.0 REGISTRY/prometheus-nginxlog-exporter:v1.11.0
docker push REGISTRY/prometheus-nginxlog-exporter:v1.11.0

# Load CLI (optional)
docker load -i redis-docs-cli.tar
docker tag a0533057932/redis-docs-cli:latest REGISTRY/redis-docs-cli:0.4.0
docker push REGISTRY/redis-docs-cli:0.4.0

docker load -i redis.tar
docker tag redis:8.10.0-alpine REGISTRY/redis:8.10.0-alpine
docker push REGISTRY/redis:8.10.0-alpine

# Load Jupyter (optional)
docker load -i jupyter.tar
docker tag quay.io/jupyter/minimal-notebook:2026-04-02 REGISTRY/jupyter/minimal-notebook:2026-04-02
docker push REGISTRY/jupyter/minimal-notebook:2026-04-02
```

> Replace `REGISTRY` with your registry address, for example: `registry.internal.company.com`

## Version Upgrade

```bash
helm upgrade redis-docs redis-docs-1.9.0.tgz -f my-values.yaml
```

Or with a single value override:

```bash
helm upgrade redis-docs redis-docs-1.9.0.tgz -f my-values.yaml \
  --set image.tag=NEW_TAG
```

> **A rebuilt image under the same tag will not be pulled.** Both images default to
> `pullPolicy: IfNotPresent`, so a node that already holds `latest` keeps serving the old
> layers and the upgrade appears to succeed while changing nothing. Push under a new tag and
> set it (`--set cli.image.tag=0.4.0`), or set `pullPolicy: Always`. This applies to
> `image.tag` and `cli.image.tag` alike.

## Accessing the Site

After installation:

```bash
kubectl port-forward svc/redis-docs 8080:80
# Open http://localhost:8080
```

## Grafana Dashboard

A ready-to-import dashboard file is located at `helm/dashboards/redis-docs-nginx.json`.

### Importing the Dashboard

1. Open Grafana and click **Dashboards** → **Import**
2. Select the `redis-docs-nginx.json` file or paste its contents
3. Configure the two required inputs:

| Input | Type | Description | Example |
|---|---|---|---|
| `DS_PROMETHEUS` | datasource | Prometheus data source | `Prometheus` |
| `VAL_JOB` | variable | Prometheus job name | `redis-docs` |

> The dashboard requires that the Prometheus datasource is pre-configured in Grafana.
>
> The job name depends on how ServiceMonitor / scrape config are configured in the cluster.

## Key Values

| Value | Default | Description |
|---|---|---|
| `global.registry` | `""` | Registry override for all images |
| `replicaCount` | `1` | Number of pods |
| `image.registry` | `a0533057932` | Registry for the main image |
| `image.name` | `redis-docs` | Main image name |
| `image.tag` | `unprivileged` | Main image tag |
| `image.pullPolicy` | `IfNotPresent` | Image pull policy |
| `imagePullSecrets` | `[]` | Secret names for image pulling |
| `nameOverride` | `""` | Chart name override |
| `fullnameOverride` | `""` | Chart full name override |
| `serviceAccount.create` | `true` | Create ServiceAccount |
| `serviceAccount.annotations` | `{}` | ServiceAccount annotations |
| `serviceAccount.name` | `""` | ServiceAccount name (auto-generated if empty) |
| `podAnnotations` | `{}` | Pod annotations |
| `podSecurityContext.runAsNonRoot` | `true` | Block running as root at the pod level |
| `podSecurityContext.seccompProfile.type` | `RuntimeDefault` | Seccomp profile |
| `securityContext.allowPrivilegeEscalation` | `false` | Prevent privilege escalation |
| `securityContext.readOnlyRootFilesystem` | `true` | Read-only root filesystem |
| `securityContext.runAsNonRoot` | `true` | Block running as root |
| `securityContext.capabilities.drop` | `[ALL]` | Linux capabilities dropped from the container |
| `service.type` | `ClusterIP` | Service type |
| `service.port` | `80` | Service port |
| `containerPort` | `8080` | Container port (nginx) |
| `tls.enabled` | `false` | Enable TLS certificate |
| `tls.existingSecret` | `""` | Name of existing Secret with certificate |
| `tls.certificate` | `""` | Certificate text (PEM) |
| `tls.privateKey` | `""` | Private key text (PEM) |
| `tls.caCertificate` | `""` | CA certificate text (optional) |
| `tls.nginxTermination` | `false` | TLS termination at nginx level (passthrough) |
| `tls.httpsPort` | `8443` | HTTPS port when nginxTermination is enabled |
| `ingress.enabled` | `false` | Enable Ingress (Kubernetes) |
| `ingress.className` | `""` | Ingress class name |
| `ingress.annotations` | `{}` | Ingress annotations |
| `ingress.hosts` | `redis-docs.local` at `/` | Hosts and paths the Ingress serves |
| `ingress.tls` | `[]` | Ingress TLS entries (secret name plus hosts) |
| `route.enabled` | `false` | Enable Route (OpenShift) |
| `route.annotations` | `{}` | Route annotations |
| `route.host` | `""` | Route hostname (auto-generated if empty) |
| `route.path` | `/` | Route path |
| `route.tls.termination` | `edge` | TLS termination type |
| `route.tls.enabled` | `true` | Enable TLS on the Route |
| `route.tls.insecureEdgeTerminationPolicy` | `Redirect` | Policy for unencrypted traffic |
| `nginx.workerConnections` | `2048` | Number of concurrent connections per worker |
| `nginx.keepaliveTimeout` | `15` | Idle connection timeout (seconds) |
| `progressDeadlineSeconds` | `1800` | Rollout timeout. Raised over the Kubernetes default of 600 because packing the `html` download bundles can outrun it. Empty leaves the default. |
| `downloads.enabled` | `true` | Pack the documentation download bundles at pod start. Needs `canonicalURL`; when inactive the download button is removed from the page. |
| `downloads.formats` | `md,md-single,json,html` | Bundle formats to pack. Dropping `html` takes the set from ~280 MB to ~30 MB. |
| `downloads.sourceURL` | `""` | Where the docs source lives, named in each bundle's README. Empty omits the line. |
| `downloads.resources` | `{}` | Resources for the packing init container alone. Empty inherits `resources`. |
| `resources.requests.cpu` | `250m` | Minimum CPU request |
| `resources.requests.memory` | `256Mi` | Minimum memory request |
| `resources.requests.ephemeral-storage` | `512Mi` | Ephemeral storage request |
| `resources.limits.cpu` | `1` | CPU limit |
| `resources.limits.memory` | `512Mi` | Memory limit |
| `resources.limits.ephemeral-storage` | `1Gi` | Ephemeral storage limit. Must hold the packed download bundles. |
| `livenessProbe` | `httpGet /healthz` | Liveness probe (initialDelay: 5s, period: 10s) |
| `readinessProbe` | `httpGet /healthz` | Readiness probe (initialDelay: 3s, period: 5s) |
| `autoscaling.enabled` | `false` | Enable HPA |
| `autoscaling.minReplicas` | `1` | Minimum pods in HPA |
| `autoscaling.maxReplicas` | `10` | Maximum pods in HPA |
| `autoscaling.targetCPUUtilizationPercentage` | `80` | CPU threshold for scaling up |
| `autoscaling.targetMemoryUtilizationPercentage` | `80` | Memory threshold for scaling up |
| `podDisruptionBudget.enabled` | `true` | Protection during rolling updates |
| `podDisruptionBudget.maxUnavailable` | `1` | Pods that may be unavailable during a disruption |
| `metrics.enabled` | `false` | Enable Prometheus metrics |
| `metrics.image.registry` | `quay.io/martinhelmich` | Metrics image registry |
| `metrics.image.name` | `prometheus-nginxlog-exporter` | Metrics image name |
| `metrics.image.tag` | `v1.11.0` | Metrics image tag |
| `metrics.image.pullPolicy` | `IfNotPresent` | Metrics image pull policy |
| `metrics.route.enabled` | `false` | Enable Route for metrics (OpenShift) |
| `metrics.route.annotations` | `{}` | Metrics Route annotations |
| `metrics.route.host` | `""` | Metrics Route hostname (auto-generated if empty) |
| `metrics.route.tls.enabled` | `true` | Enable TLS on metrics Route |
| `metrics.route.tls.termination` | `edge` | TLS termination type for metrics |
| `metrics.route.tls.insecureEdgeTerminationPolicy` | `Redirect` | Policy for unencrypted traffic (metrics) |
| `metrics.serviceMonitor.enabled` | `false` | Enable ServiceMonitor (requires Prometheus Operator) |
| `metrics.serviceMonitor.interval` | `30s` | Scraping interval |
| `metrics.serviceMonitor.labels` | `{}` | Additional ServiceMonitor labels |
| `cli.enabled` | `false` | Enable CLI playground (separate pod with Flask + Redis) |
| `cli.securityContext.allowPrivilegeEscalation` | `false` | Prevent privilege escalation (CLI) |
| `cli.securityContext.runAsNonRoot` | `true` | Block running as root (CLI) |
| `cli.securityContext.capabilities.drop` | `[ALL]` | Linux capabilities dropped (CLI) |
| `cli.image.registry` | `a0533057932` | CLI proxy image registry |
| `cli.image.name` | `redis-docs-cli` | CLI proxy image name |
| `cli.image.tag` | `latest` | CLI proxy image tag (in air-gapped networks: `0.4.0`) |
| `cli.image.pullPolicy` | `IfNotPresent` | CLI image pull policy |
| `cli.resources` | requests: 50m/64Mi, limits: 200m/128Mi | CLI proxy resources |
| `cli.session.idleTtlSeconds` | `1800` | Close a browser session after this long without a command |
| `cli.session.max` | `500` | Cap on live sessions; the least recently used is closed first |
| `cli.session.sweepIntervalSeconds` | `60` | How often idle sessions are looked for |
| `cli.namespace.enabled` | `true` | Give each session its own slice of the shared keyspace |
| `cli.namespace.scanMinCount` | `10000` | Floor on SCAN's COUNT, so a scan does not return an empty page |
| `cli.namespace.cleanup.enabled` | `true` | Delete a session's keys and indexes when it is closed |
| `cli.namespace.cleanup.batch` | `500` | Keys deleted per round trip during cleanup |
| `cli.redis.image.registry` | `docker.io` | Redis image registry |
| `cli.redis.image.name` | `redis` | Redis sidecar image name |
| `cli.redis.acl.enabled` | `true` | Run reader commands as a restricted Redis user (files/sandbox.acl) |
| `cli.redis.acl.username` | `docsandbox` | The restricted user the proxy authenticates as |
| `cli.redis.image.tag` | `8.10.0-alpine` | Redis sidecar image tag |
| `cli.redis.image.pullPolicy` | `IfNotPresent` | Redis image pull policy |
| `cli.redis.resources` | requests: 50m/64Mi, limits: 200m/128Mi | Redis sidecar resources |
| `cli.jupyter.enabled` | `false` | Enable Jupyter kernel server (additional container in CLI pod) |
| `cli.jupyter.securityContext.allowPrivilegeEscalation` | `false` | Prevent privilege escalation (Jupyter) |
| `cli.jupyter.securityContext.runAsNonRoot` | `true` | Block running as root (Jupyter) |
| `cli.jupyter.securityContext.capabilities.drop` | `[ALL]` | Linux capabilities dropped (Jupyter) |
| `cli.jupyter.image.registry` | `quay.io` | Jupyter image registry |
| `cli.jupyter.image.name` | `jupyter/minimal-notebook` | Jupyter image name |
| `cli.jupyter.image.tag` | `2026-04-02` | Jupyter image tag |
| `cli.jupyter.image.pullPolicy` | `IfNotPresent` | Jupyter image pull policy |
| `cli.jupyter.resources` | requests: 100m/256Mi, limits: 500m/512Mi | Jupyter resources |
| `aiServices.litellm.enabled` | `false` | Enable LiteLLM endpoint (instead of external CloudFront) |
| `aiServices.litellm.url` | `""` | LiteLLM URL (OpenAI-compatible) |
| `aiServices.litellm.model` | `gpt-3.5-turbo` | Model name to send |
| `aiServices.litellm.apiKey` | `""` | Server-side API key (skips user prompt) |
| `aiServices.binder.url` | `https://redis.io/binder/` | BinderHub / JupyterHub URL |
| `canonicalURL` | `""` | Public URL of this deployment, used by nginx sub_filter to replace `__DOCS_BASE_URL__` in `.md` / `.json`. Empty → auto-detect from `$http_host`. |
| `externalLinks.enabled` | `false` | Master kill-switch for every catalogued external link. Default hides everything (airgap-first). |
| `externalLinks.families.<fam>.enabled` | unset | Per-family kill-switch (e.g. `home`, `header`, `footer`). Set `true` to opt the whole family back in. |
| `externalLinks.families.<fam>.sub-families.<sub>.enabled` | unset | Per-sub-family kill-switch (e.g. `header.main-nav`, `footer.legal`). |
| `externalLinks.overrides.<key>.enabled` | unset | Per-link override. Wins over family / sub-family / master switches. |
| `externalLinks.overrides.<key>.url` | unset | Replace the upstream URL for a single link (typically with an internal mirror). |
| `nodeSelector` | `{}` | Node selector for pod scheduling |
| `tolerations` | `[]` | Tolerations for pod scheduling |
| `affinity` | `{}` | Affinity rules for pod scheduling |
