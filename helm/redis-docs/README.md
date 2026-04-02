# Redis Docs Helm Chart

Helm chart להתקנת אתר הדוקומנטציה של Redis על Kubernetes / OpenShift.
מותאם לרשת סגורה (air-gapped) - ללא תלויות חיצוניות.

## דרישות מקדימות

- Kubernetes 1.26+ / OpenShift 4.x+
- Helm 3.x
- Private Docker registry (ברשת סגורה)

## ארכיטקטורה

הצ'ארט פורס שני פודים עיקריים:

### פוד 1 — `redis-docs` (אתר הדוקומנטציה)

| Container | תיאור | פורט |
|---|---|---|
| `nginx` | שרת האתר הראשי (unprivileged) | 8080 |
| `metrics` (אופציונלי) | sidecar — prometheus-nginxlog-exporter | 4040 |

nginx משמש גם כ-reverse proxy:
- `/cli` → מופנה ל-CLI proxy בפוד השני (פורט 8090)
- `/jupyter/` → מופנה ל-Jupyter בפוד השני (פורט 8888), כולל תמיכה ב-WebSocket

### פוד 2 — `redis-docs-cli` (CLI playground)

נוצר רק כאשר `cli.enabled=true`.

| Container | תיאור | פורט |
|---|---|---|
| `cli-proxy` | Flask proxy להרצת פקודות Redis | 8090 |
| `redis` | Redis sidecar — מקומי ל-pod (localhost) | 6379 |
| `jupyter` (אופציונלי) | Jupyter kernel server להרצת קוד אינטראקטיבי | 8888 |

כל הקונטיינרים בפוד זה מתקשרים על `localhost`.

### הגדרות Runtime

קובץ `configmap-runtime.yaml` מזריק קובץ JS לתוך nginx, המכיל הגדרות דינמיות:
- `aiServices.litellm` — כתובת LiteLLM endpoint (במקום CloudFront חיצוני)
- `aiServices.binder.url` — כתובת BinderHub / JupyterHub

## Docker images

| Image | תג | פורט | שימוש | חובה? |
|---|---|---|---|---|
| `a0533057932/redis-docs` | `latest` | 80 | הרצה רגילה עם `docker run` (privileged) | כן - אחד מהשניים |
| `a0533057932/redis-docs` | `unprivileged` | 8080 | Kubernetes / OpenShift (non-root) | כן - אחד מהשניים |
| `quay.io/martinhelmich/prometheus-nginxlog-exporter` | `v1.11.0` | 4040 | מטריקות Prometheus (כולל זמני תגובה) | לא - רק אם `metrics.enabled=true` |
| `a0533057932/redis-docs-cli` | `latest` / `0.2.0` | 8090 | CLI playground proxy (Flask) | לא - רק אם `cli.enabled=true` |
| `redis` | `8-alpine` | 6379 | Redis sidecar ל-CLI playground | לא - רק אם `cli.enabled=true` |
| `jupyter/minimal-notebook` | `latest` | 8888 | Jupyter kernel server להרצת קוד אינטראקטיבי | לא - רק אם `cli.jupyter.enabled=true` |
> ל-Kubernetes/OpenShift השתמשו בתג `unprivileged`. ל-`docker run` רגיל השתמשו בתג `latest`.

## התקנה

### שימוש בסיסי

```bash
helm install redis-docs redis-docs-0.9.0.tgz
```

### התקנה עם קובץ values

הדרך המומלצת - קובץ `values.yaml` מותאם:

```bash
helm install redis-docs redis-docs-0.9.0.tgz -f my-values.yaml
```

להלן דוגמאות לקבצי values לתרחישים שונים.

### רשת פתוחה — OpenShift

```yaml
# my-values.yaml

# --- Replicas / Autoscaling ---
replicaCount: 2
# או לחלופין HPA:
# autoscaling:
#   enabled: true
#   minReplicas: 2
#   maxReplicas: 10
#   targetCPUUtilizationPercentage: 80

# --- תמונה ראשית (nginx) ---
image:
  registry: a0533057932
  name: redis-docs
  tag: unprivileged

# --- Resources - תמונה ראשית ---
resources:
  requests:
    cpu: 250m
    memory: 256Mi
  limits:
    cpu: "1"
    memory: 512Mi

# --- Route (OpenShift) ---
route:
  enabled: true
  # host: docs.apps.example.com  # ריק = אוטומטי

# --- מטריקות ---
metrics:
  enabled: true
  route:
    enabled: true
    # host: docs-metrics.apps.example.com
  image:
    registry: quay.io/martinhelmich
    name: prometheus-nginxlog-exporter
    tag: "v1.11.0"
  resources:
    requests:
      cpu: 10m
      memory: 16Mi
    limits:
      cpu: 50m
      memory: 32Mi

# --- CLI playground ---
cli:
  enabled: true
  image:
    registry: a0533057932
    name: redis-docs-cli
    tag: "latest"
  resources:
    requests:
      cpu: 50m
      memory: 64Mi
    limits:
      cpu: 200m
      memory: 128Mi
  redis:
    image:
      registry: docker.io
      name: redis
      tag: "8-alpine"
    resources:
      requests:
        cpu: 50m
        memory: 64Mi
      limits:
        cpu: 200m
        memory: 128Mi
```

> Route נפרד ייווצר עבור endpoint המטריקות על פורט 4040 בנתיב `/metrics`.
>
> ייווצר פוד נפרד עם Flask proxy + Redis sidecar. ה-CLI יהיה זמין בנתיב `/cli`.

### רשת פתוחה — Kubernetes עם Ingress

```yaml
# my-values.yaml
ingress:
  enabled: true
  hosts:
    - host: docs.company.internal
      paths:
        - path: /
          pathType: Prefix

metrics:
  enabled: true

cli:
  enabled: true
```

### רשת סגורה — דוגמה מלאה

```yaml
# my-values.yaml
global:
  registry: registry.internal.company.com

imagePullSecrets:
  - name: regcred

replicaCount: 2

# --- תמונה ראשית ---
image:
  name: redis-docs
  tag: unprivileged

# --- Route ---
route:
  enabled: true

# --- מטריקות ---
metrics:
  enabled: true
  route:
    enabled: true
  image:
    name: prometheus-nginxlog-exporter
    tag: "v1.11.0"

# --- CLI + Jupyter ---
cli:
  enabled: true
  image:
    name: redis-docs-cli
    tag: "0.2.0"              # ברשת סגורה: תג אמיתי (Artifactory דורש)
  redis:
    image:
      name: redis
      tag: "8-alpine"
  jupyter:
    enabled: true
    image:
      name: jupyter/minimal-notebook
      tag: "latest"

# --- שירותי AI (אופציונלי) ---
aiServices:
  litellm:
    enabled: true
    url: "http://litellm.internal:4000/v1/chat/completions"
    model: "gpt-3.5-turbo"
    apiKey: "sk-internal-key"
  binder:
    url: "https://redis.io/binder/"
```

> `global.registry` משנה את ה-registry לכל התמונות. אין צורך לציין registry לכל תמונה בנפרד.
>
> ברשת סגורה יש לתייג את CLI proxy כ-`0.2.0` (Artifactory דורש תג שאינו `latest`).
>
> כשהJupyter מופעל, הוא רץ כcontainer נוסף בפוד ה-CLI ומשתמש ב-Redis על localhost.
>
> `aiServices.litellm` מפנה את צ'אט ה-AI ב-Agent Builder ל-LiteLLM פנימי במקום CloudFront חיצוני. כש-`apiKey` מוגדר, המשתמש לא יתבקש להזין מפתח.

### תעודת אבטחה (TLS)

הצ'ארט תומך בשתי דרכים לספק תעודת אבטחה:

#### אופציה 1: הדבקת תעודה ישירות

הדביקו את הטקסט של התעודה, המפתח, וה-CA (אופציונלי) ישירות ב-values:

```yaml
# my-values.yaml
tls:
  enabled: true
  certificate: |
    -----BEGIN CERTIFICATE-----
    MIIDxTCCAq2gAwIBAgIQAqxcJmoLQJuPC3nyrkYldzANBgkqhkiG9w0BAQUFAMDx
    ... (הדביקו כאן את כל הטקסט של התעודה)
    -----END CERTIFICATE-----
  privateKey: |
    -----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC7o4qne60TB3pq
    ... (הדביקו כאן את כל הטקסט של המפתח)
    -----END PRIVATE KEY-----
  caCertificate: |
    -----BEGIN CERTIFICATE-----
    MIIDrzCCApegAwIBAgIQCDvgVpBCRrGhdWrJWZHHSjANBgkqhkiG9w0BAQUFADBh
    ... (אופציונלי — הדביקו כאן את כל הטקסט של ה-CA)
    -----END CERTIFICATE-----

route:
  enabled: true
  host: docs.apps.example.com
  tls:
    enabled: true
    termination: edge
```

> **שימו לב:** השדות `certificate` ו-`privateKey` הם חובה. השדה `caCertificate` אופציונלי.
>
> אם קיבלתם קובץ PFX, חלצו ממנו את הטקסטים:
>
> ```bash
> openssl pkcs12 -in my-cert.pfx -clcerts -nokeys    # → certificate
> openssl pkcs12 -in my-cert.pfx -nocerts -nodes      # → privateKey
> openssl pkcs12 -in my-cert.pfx -cacerts -nokeys     # → caCertificate
> ```

#### אופציה 2: שימוש ב-Secret קיים

```yaml
# my-values.yaml
tls:
  enabled: true
  existingSecret: "my-tls-secret"

route:
  enabled: true
  host: docs.apps.example.com
```

> ה-Secret צריך להכיל `tls.crt` ו-`tls.key` (סוג `kubernetes.io/tls`).

### אם ה-registry דורש הרשאות

```bash
kubectl create secret docker-registry regcred \
  --docker-server=REGISTRY \
  --docker-username=USER \
  --docker-password=PASS
```

הוסיפו ל-values:

```yaml
imagePullSecrets:
  - name: regcred
```

## העברה לרשת סגורה

### שלב 1: שמירת Docker images

```bash
# אימג' ראשי (חובה)
docker pull a0533057932/redis-docs:unprivileged
docker save a0533057932/redis-docs:unprivileged -o redis-docs.tar

# מטריקות (אופציונלי)
docker pull quay.io/martinhelmich/prometheus-nginxlog-exporter:v1.11.0
docker save quay.io/martinhelmich/prometheus-nginxlog-exporter:v1.11.0 -o nginx-exporter.tar

# CLI playground (אופציונלי)
docker pull a0533057932/redis-docs-cli:latest
docker save a0533057932/redis-docs-cli:latest -o redis-docs-cli.tar
docker pull redis:8-alpine
docker save redis:8-alpine -o redis.tar

# Jupyter kernel server (אופציונלי)
docker pull jupyter/minimal-notebook:latest
docker save jupyter/minimal-notebook:latest -o jupyter.tar
```

### שלב 2: אריזת Helm chart

```bash
helm package helm/redis-docs/
# ייצור: redis-docs-0.9.0.tgz
```

### שלב 3: העברת קבצים לרשת הסגורה

העבירו את הקבצים הבאים:
- `redis-docs-0.9.0.tgz`
- `redis-docs.tar`
- `nginx-exporter.tar` (אופציונלי - מטריקות)
- `redis-docs-cli.tar` (אופציונלי - CLI)
- `redis.tar` (אופציונלי - CLI)
- `jupyter.tar` (אופציונלי - Jupyter)

### שלב 4: טעינה ל-private registry

```bash
# טעינת אימג' ראשי
docker load -i redis-docs.tar
docker tag a0533057932/redis-docs:unprivileged REGISTRY/redis-docs:unprivileged
docker push REGISTRY/redis-docs:unprivileged

# טעינת מטריקות (אופציונלי)
docker load -i nginx-exporter.tar
docker tag quay.io/martinhelmich/prometheus-nginxlog-exporter:v1.11.0 REGISTRY/prometheus-nginxlog-exporter:v1.11.0
docker push REGISTRY/prometheus-nginxlog-exporter:v1.11.0

# טעינת CLI (אופציונלי)
docker load -i redis-docs-cli.tar
docker tag a0533057932/redis-docs-cli:latest REGISTRY/redis-docs-cli:0.2.0
docker push REGISTRY/redis-docs-cli:0.2.0

docker load -i redis.tar
docker tag redis:8-alpine REGISTRY/redis:8-alpine
docker push REGISTRY/redis:8-alpine

# טעינת Jupyter (אופציונלי)
docker load -i jupyter.tar
docker tag jupyter/minimal-notebook:latest REGISTRY/jupyter/minimal-notebook:latest
docker push REGISTRY/jupyter/minimal-notebook:latest
```

> החליפו `REGISTRY` בכתובת ה-registry שלכם, לדוגמה: `registry.internal.company.com`

## עדכון גרסה

```bash
helm upgrade redis-docs redis-docs-0.9.0.tgz -f my-values.yaml
```

או עם דריסת ערך בודד:

```bash
helm upgrade redis-docs redis-docs-0.9.0.tgz -f my-values.yaml \
  --set image.tag=NEW_TAG
```

## גישה לאתר

לאחר התקנה:

```bash
kubectl port-forward svc/redis-docs 8080:80
# פתחו http://localhost:8080
```

## דשבורד Grafana

קובץ דשבורד מוכן לייבוא נמצא בנתיב `helm/dashboards/redis-docs-nginx.json`.

### ייבוא הדשבורד

1. פתחו את Grafana ולחצו על **Dashboards** → **Import**
2. בחרו את הקובץ `redis-docs-nginx.json` או הדביקו את תוכנו
3. הגדירו את שני ה-inputs הנדרשים:

| Input | סוג | תיאור | דוגמה |
|---|---|---|---|
| `DS_PROMETHEUS` | datasource | מקור נתונים מסוג Prometheus | `Prometheus` |
| `VAL_JOB` | variable | שם ה-job ב-Prometheus | `redis-docs` |

> הדשבורד דורש שה-Prometheus datasource יהיה מוגדר מראש ב-Grafana.
>
> שם ה-job תלוי באופן שבו ServiceMonitor / scrape config מוגדרים בקלאסטר.

## ערכים עיקריים

| ערך | ברירת מחדל | תיאור |
|---|---|---|
| `global.registry` | `""` | דריסת registry לכל התמונות |
| `replicaCount` | `1` | מספר pods |
| `image.registry` | `a0533057932` | registry לתמונה הראשית |
| `image.name` | `redis-docs` | שם התמונה הראשית |
| `image.tag` | `unprivileged` | תג התמונה הראשית |
| `image.pullPolicy` | `IfNotPresent` | מדיניות משיכת תמונה |
| `imagePullSecrets` | `[]` | שמות Secrets למשיכת תמונות |
| `nameOverride` | `""` | דריסת שם הצ'ארט |
| `fullnameOverride` | `""` | דריסת השם המלא של הצ'ארט |
| `serviceAccount.create` | `true` | יצירת ServiceAccount |
| `serviceAccount.annotations` | `{}` | annotations ל-ServiceAccount |
| `serviceAccount.name` | `""` | שם ServiceAccount (אוטומטי אם ריק) |
| `podAnnotations` | `{}` | annotations לפודים |
| `podSecurityContext.runAsNonRoot` | `true` | חסימת הרצה כ-root ברמת הפוד |
| `podSecurityContext.seccompProfile.type` | `RuntimeDefault` | פרופיל seccomp |
| `securityContext.allowPrivilegeEscalation` | `false` | מניעת הסלמת הרשאות |
| `securityContext.readOnlyRootFilesystem` | `true` | מערכת קבצים לקריאה בלבד |
| `securityContext.runAsNonRoot` | `true` | חסימת הרצה כ-root |
| `service.type` | `ClusterIP` | סוג השירות |
| `service.port` | `80` | פורט השירות |
| `containerPort` | `8080` | פורט הקונטיינר (nginx) |
| `tls.enabled` | `false` | הפעלת תעודת אבטחה |
| `tls.existingSecret` | `""` | שם Secret קיים עם תעודה |
| `tls.certificate` | `""` | טקסט התעודה (PEM) |
| `tls.privateKey` | `""` | טקסט המפתח הפרטי (PEM) |
| `tls.caCertificate` | `""` | טקסט תעודת CA (אופציונלי) |
| `tls.nginxTermination` | `false` | TLS termination ברמת nginx (passthrough) |
| `tls.httpsPort` | `8443` | פורט HTTPS כש-nginxTermination מופעל |
| `ingress.enabled` | `false` | הפעלת Ingress (Kubernetes) |
| `ingress.className` | `""` | Ingress class name |
| `ingress.annotations` | `{}` | annotations ל-Ingress |
| `route.enabled` | `false` | הפעלת Route (OpenShift) |
| `route.annotations` | `{}` | annotations ל-Route |
| `route.host` | `""` | hostname ל-Route (אוטומטי אם ריק) |
| `route.path` | `/` | נתיב ל-Route |
| `route.tls.termination` | `edge` | סוג TLS termination |
| `route.tls.insecureEdgeTerminationPolicy` | `Redirect` | מדיניות לתעבורה לא מוצפנת |
| `nginx.workerConnections` | `2048` | מספר חיבורים מקבילים per worker |
| `nginx.keepaliveTimeout` | `15` | timeout לחיבורים idle (שניות) |
| `resources.requests.cpu` | `250m` | בקשת CPU מינימלית |
| `resources.requests.memory` | `256Mi` | בקשת זיכרון מינימלית |
| `resources.requests.ephemeral-storage` | `128Mi` | בקשת אחסון זמני |
| `resources.limits.cpu` | `1` | מגבלת CPU |
| `resources.limits.memory` | `512Mi` | מגבלת זיכרון |
| `resources.limits.ephemeral-storage` | `256Mi` | מגבלת אחסון זמני |
| `livenessProbe` | `httpGet /healthz` | בדיקת חיות (initialDelay: 5s, period: 10s) |
| `readinessProbe` | `httpGet /healthz` | בדיקת מוכנות (initialDelay: 3s, period: 5s) |
| `autoscaling.enabled` | `false` | הפעלת HPA |
| `autoscaling.minReplicas` | `1` | מינימום pods ב-HPA |
| `autoscaling.maxReplicas` | `10` | מקסימום pods ב-HPA |
| `autoscaling.targetCPUUtilizationPercentage` | `80` | סף CPU להגדלה |
| `autoscaling.targetMemoryUtilizationPercentage` | `80` | סף זיכרון להגדלה |
| `podDisruptionBudget.enabled` | `true` | הגנה בזמן rolling updates |
| `metrics.enabled` | `false` | הפעלת Prometheus metrics |
| `metrics.image.registry` | `quay.io/martinhelmich` | registry לתמונת מטריקות |
| `metrics.image.name` | `prometheus-nginxlog-exporter` | שם תמונת מטריקות |
| `metrics.image.tag` | `v1.11.0` | תג תמונת מטריקות |
| `metrics.image.pullPolicy` | `IfNotPresent` | מדיניות משיכת תמונת מטריקות |
| `metrics.route.enabled` | `false` | הפעלת Route למטריקות (OpenShift) |
| `metrics.route.annotations` | `{}` | annotations ל-Route מטריקות |
| `metrics.route.host` | `""` | hostname ל-Route מטריקות (אוטומטי אם ריק) |
| `metrics.route.tls.enabled` | `true` | הפעלת TLS ב-Route מטריקות |
| `metrics.route.tls.termination` | `edge` | סוג TLS termination למטריקות |
| `metrics.route.tls.insecureEdgeTerminationPolicy` | `Redirect` | מדיניות לתעבורה לא מוצפנת (מטריקות) |
| `metrics.serviceMonitor.enabled` | `false` | הפעלת ServiceMonitor (דורש Prometheus Operator) |
| `metrics.serviceMonitor.interval` | `30s` | מרווח scraping |
| `metrics.serviceMonitor.labels` | `{}` | labels נוספים ל-ServiceMonitor |
| `cli.enabled` | `false` | הפעלת CLI playground (פוד נפרד עם Flask + Redis) |
| `cli.securityContext.allowPrivilegeEscalation` | `false` | מניעת הסלמת הרשאות (CLI) |
| `cli.securityContext.runAsNonRoot` | `true` | חסימת הרצה כ-root (CLI) |
| `cli.image.registry` | `a0533057932` | registry לתמונת CLI proxy |
| `cli.image.name` | `redis-docs-cli` | שם תמונת CLI proxy |
| `cli.image.tag` | `latest` | תג תמונת CLI proxy (ברשת סגורה: `0.2.0`) |
| `cli.image.pullPolicy` | `IfNotPresent` | מדיניות משיכת תמונת CLI |
| `cli.resources` | requests: 50m/64Mi, limits: 200m/128Mi | משאבי CLI proxy |
| `cli.redis.image.registry` | `docker.io` | registry לתמונת Redis |
| `cli.redis.image.tag` | `8-alpine` | תג תמונת Redis sidecar |
| `cli.redis.image.pullPolicy` | `IfNotPresent` | מדיניות משיכת תמונת Redis |
| `cli.redis.resources` | requests: 50m/64Mi, limits: 200m/128Mi | משאבי Redis sidecar |
| `cli.jupyter.enabled` | `false` | הפעלת Jupyter kernel server (container נוסף בפוד CLI) |
| `cli.jupyter.securityContext.allowPrivilegeEscalation` | `false` | מניעת הסלמת הרשאות (Jupyter) |
| `cli.jupyter.securityContext.runAsNonRoot` | `true` | חסימת הרצה כ-root (Jupyter) |
| `cli.jupyter.image.registry` | `docker.io` | registry לתמונת Jupyter |
| `cli.jupyter.image.name` | `jupyter/minimal-notebook` | שם תמונת Jupyter |
| `cli.jupyter.image.tag` | `latest` | תג תמונת Jupyter |
| `cli.jupyter.image.pullPolicy` | `IfNotPresent` | מדיניות משיכת תמונת Jupyter |
| `cli.jupyter.resources` | requests: 100m/256Mi, limits: 500m/512Mi | משאבי Jupyter |
| `aiServices.litellm.enabled` | `false` | הפעלת LiteLLM endpoint (במקום CloudFront חיצוני) |
| `aiServices.litellm.url` | `""` | URL ל-LiteLLM (OpenAI-compatible) |
| `aiServices.litellm.model` | `gpt-3.5-turbo` | שם המודל לשליחה |
| `aiServices.litellm.apiKey` | `""` | API key צד שרת (דילוג על שאלת המשתמש) |
| `aiServices.binder.url` | `https://redis.io/binder/` | URL ל-BinderHub / JupyterHub |
| `nodeSelector` | `{}` | node selector לתזמון פודים |
| `tolerations` | `[]` | tolerations לתזמון פודים |
| `affinity` | `{}` | affinity rules לתזמון פודים |
