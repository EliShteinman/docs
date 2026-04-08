# Redis Docs Helm Chart

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

All containers in this pod communicate over `localhost`.

### Runtime Configuration

The `configmap-runtime.yaml` file injects a JS file into nginx, containing dynamic settings:
- `aiServices.litellm` — LiteLLM endpoint URL (instead of external CloudFront)
- `aiServices.binder.url` — BinderHub / JupyterHub URL
- `externalLinks` — control over external links on the homepage

### External Links (externalLinks)

The homepage contains 7 links to external services that are not part of the documentation site:

| ID | Default | Description |
|------|-----------|-------|
| `sandbox` | `https://redis.io/try/sandbox/` | Interactive Redis Sandbox |
| `tutorials` | `https://redis.io/tutorials/` | Tutorials (external site) |
| `university` | `https://university.redis.io/academy` | Redis University |
| `blog` | `https://redis.io/blog/` | Blog (external site) |
| `support` | `https://support.redislabs.com/hc/en-us` | Support portal (Zendesk) |
| `github` | `https://github.com/redis/docs/` | GitHub repository |
| `chatbot` | `https://redis.io/chat` | AI chatbot |

Each link supports:
- **`enabled`** — `true` / `false` — show or hide the link
- **`url`** — override the URL with an alternative internal service

In air-gapped networks, you can hide inaccessible links or redirect them to an equivalent internal service.

## Docker images

| Image | Tag | Port | Usage | Required? |
|---|---|---|---|---|
| `a0533057932/redis-docs` | `<HASH>` / `latest` | 80 | Standard run with `docker run` (privileged) | Yes — one of the two |
| `a0533057932/redis-docs` | `<HASH>-unprivileged` / `unprivileged` | 8080 | Kubernetes / OpenShift (non-root) | Yes — one of the two |
| `quay.io/martinhelmich/prometheus-nginxlog-exporter` | `v1.11.0` | 4040 | Prometheus metrics (including response times) | No — only if `metrics.enabled=true` |
| `a0533057932/redis-docs-cli` | `latest` / `0.2.0` | 8090 | CLI playground proxy (Flask) | No — only if `cli.enabled=true` |
| `redis` | `8-alpine` | 6379 | Redis sidecar for CLI playground | No — only if `cli.enabled=true` |
| `quay.io/jupyter/minimal-notebook` | `2026-04-02` | 8888 | Jupyter kernel server for interactive code execution | No — only if `cli.jupyter.enabled=true` |

> For Kubernetes/OpenShift use the `unprivileged` or `<HASH>-unprivileged` tag.
> For standard `docker run` use the `latest` or `<HASH>` tag.
> In air-gapped networks it is recommended to use a hash-based tag (Artifactory requires a tag other than `latest`).
> For image build documentation see `BUILD.md` in the project root.

## Installation

### Basic usage

```bash
helm install redis-docs redis-docs-0.11.0.tgz
```

### Installation with a values file

The recommended approach - a custom `values.yaml` file:

```bash
helm install redis-docs redis-docs-0.11.0.tgz -f my-values.yaml
```

Below is an example of a typical deployment scenario. See also ready-made example files in the `examples/` directory.

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
  tag: "79955fdb5-unprivileged"

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

# --- External links ---
externalLinks:
  github:
    url: "https://gitlab.internal.company.com/infra/redis-docs"
  support:
    url: "https://support.internal.company.com"
  sandbox:
    enabled: false
  tutorials:
    enabled: false
  university:
    enabled: false
  blog:
    enabled: false
  chatbot:
    enabled: false
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
docker pull redis:8-alpine
docker save redis:8-alpine -o redis.tar

# Jupyter kernel server (optional)
docker pull quay.io/jupyter/minimal-notebook:2026-04-02
docker save quay.io/jupyter/minimal-notebook:2026-04-02 -o jupyter.tar
```

### Step 2: Package the Helm chart

```bash
helm package helm/redis-docs/
# Produces: redis-docs-0.11.0.tgz
```

### Step 3: Transfer files to the air-gapped network

Transfer the following files:
- `redis-docs-0.11.0.tgz`
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
docker tag a0533057932/redis-docs-cli:latest REGISTRY/redis-docs-cli:0.2.0
docker push REGISTRY/redis-docs-cli:0.2.0

docker load -i redis.tar
docker tag redis:8-alpine REGISTRY/redis:8-alpine
docker push REGISTRY/redis:8-alpine

# Load Jupyter (optional)
docker load -i jupyter.tar
docker tag quay.io/jupyter/minimal-notebook:2026-04-02 REGISTRY/jupyter/minimal-notebook:2026-04-02
docker push REGISTRY/jupyter/minimal-notebook:2026-04-02
```

> Replace `REGISTRY` with your registry address, for example: `registry.internal.company.com`

## Version Upgrade

```bash
helm upgrade redis-docs redis-docs-0.11.0.tgz -f my-values.yaml
```

Or with a single value override:

```bash
helm upgrade redis-docs redis-docs-0.11.0.tgz -f my-values.yaml \
  --set image.tag=NEW_TAG
```

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
| `route.enabled` | `false` | Enable Route (OpenShift) |
| `route.annotations` | `{}` | Route annotations |
| `route.host` | `""` | Route hostname (auto-generated if empty) |
| `route.path` | `/` | Route path |
| `route.tls.termination` | `edge` | TLS termination type |
| `route.tls.insecureEdgeTerminationPolicy` | `Redirect` | Policy for unencrypted traffic |
| `nginx.workerConnections` | `2048` | Number of concurrent connections per worker |
| `nginx.keepaliveTimeout` | `15` | Idle connection timeout (seconds) |
| `resources.requests.cpu` | `250m` | Minimum CPU request |
| `resources.requests.memory` | `256Mi` | Minimum memory request |
| `resources.requests.ephemeral-storage` | `128Mi` | Ephemeral storage request |
| `resources.limits.cpu` | `1` | CPU limit |
| `resources.limits.memory` | `512Mi` | Memory limit |
| `resources.limits.ephemeral-storage` | `256Mi` | Ephemeral storage limit |
| `livenessProbe` | `httpGet /healthz` | Liveness probe (initialDelay: 5s, period: 10s) |
| `readinessProbe` | `httpGet /healthz` | Readiness probe (initialDelay: 3s, period: 5s) |
| `autoscaling.enabled` | `false` | Enable HPA |
| `autoscaling.minReplicas` | `1` | Minimum pods in HPA |
| `autoscaling.maxReplicas` | `10` | Maximum pods in HPA |
| `autoscaling.targetCPUUtilizationPercentage` | `80` | CPU threshold for scaling up |
| `autoscaling.targetMemoryUtilizationPercentage` | `80` | Memory threshold for scaling up |
| `podDisruptionBudget.enabled` | `true` | Protection during rolling updates |
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
| `cli.image.registry` | `a0533057932` | CLI proxy image registry |
| `cli.image.name` | `redis-docs-cli` | CLI proxy image name |
| `cli.image.tag` | `latest` | CLI proxy image tag (in air-gapped networks: `0.2.0`) |
| `cli.image.pullPolicy` | `IfNotPresent` | CLI image pull policy |
| `cli.resources` | requests: 50m/64Mi, limits: 200m/128Mi | CLI proxy resources |
| `cli.redis.image.registry` | `docker.io` | Redis image registry |
| `cli.redis.image.tag` | `8-alpine` | Redis sidecar image tag |
| `cli.redis.image.pullPolicy` | `IfNotPresent` | Redis image pull policy |
| `cli.redis.resources` | requests: 50m/64Mi, limits: 200m/128Mi | Redis sidecar resources |
| `cli.jupyter.enabled` | `false` | Enable Jupyter kernel server (additional container in CLI pod) |
| `cli.jupyter.securityContext.allowPrivilegeEscalation` | `false` | Prevent privilege escalation (Jupyter) |
| `cli.jupyter.securityContext.runAsNonRoot` | `true` | Block running as root (Jupyter) |
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
| `externalLinks.sandbox.enabled` | `true` | Show Redis Sandbox link |
| `externalLinks.sandbox.url` | `https://redis.io/try/sandbox/` | Redis Sandbox URL |
| `externalLinks.tutorials.enabled` | `true` | Show tutorials link |
| `externalLinks.tutorials.url` | `https://redis.io/tutorials/` | Tutorials URL |
| `externalLinks.university.enabled` | `true` | Show Redis University link |
| `externalLinks.university.url` | `https://university.redis.io/academy` | Redis University URL |
| `externalLinks.blog.enabled` | `true` | Show blog link |
| `externalLinks.blog.url` | `https://redis.io/blog/` | Blog URL |
| `externalLinks.support.enabled` | `true` | Show support portal link |
| `externalLinks.support.url` | `https://support.redislabs.com/hc/en-us` | Support portal URL |
| `externalLinks.github.enabled` | `true` | Show GitHub link |
| `externalLinks.github.url` | `https://github.com/redis/docs/` | GitHub repository URL |
| `externalLinks.chatbot.enabled` | `true` | Show chatbot link |
| `externalLinks.chatbot.url` | `https://redis.io/chat` | AI chatbot URL |
| `nodeSelector` | `{}` | Node selector for pod scheduling |
| `tolerations` | `[]` | Tolerations for pod scheduling |
| `affinity` | `{}` | Affinity rules for pod scheduling |
