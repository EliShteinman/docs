# Redis Docs Helm Chart

> **[English version](README.md)**

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
- `externalLinks` — שליטה על לינקים חיצוניים בדף הבית

### לינקים חיצוניים (externalLinks)

דף הבית מכיל 7 לינקים לשירותים חיצוניים שאינם חלק מאתר הדוקומנטציה:

| מזהה | ברירת מחדל | תיאור |
|------|-----------|-------|
| `sandbox` | `https://redis.io/try/sandbox/` | Redis Sandbox אינטראקטיבי |
| `tutorials` | `https://redis.io/tutorials/` | טוטוריאלים (אתר חיצוני) |
| `university` | `https://university.redis.io/academy` | Redis University |
| `blog` | `https://redis.io/blog/` | בלוג (אתר חיצוני) |
| `support` | `https://support.redislabs.com/hc/en-us` | פורטל תמיכה (Zendesk) |
| `github` | `https://github.com/redis/docs/` | מאגר קוד ב-GitHub |
| `chatbot` | `https://redis.io/chat` | צ'אטבוט AI |

כל לינק תומך ב:
- **`enabled`** — `true` / `false` — הצגה או הסתרה של הלינק
- **`url`** — דריסת הכתובת לשירות פנימי חלופי

ברשת סגורה, ניתן להסתיר לינקים שלא נגישים או להפנות אותם לשירות פנימי מקביל.

## Docker images

| Image | תג | פורט | שימוש | חובה? |
|---|---|---|---|---|
| `a0533057932/redis-docs` | `<HASH>` / `latest` | 80 | הרצה רגילה עם `docker run` (privileged) | כן — אחד מהשניים |
| `a0533057932/redis-docs` | `<HASH>-unprivileged` / `unprivileged` | 8080 | Kubernetes / OpenShift (non-root) | כן — אחד מהשניים |
| `quay.io/martinhelmich/prometheus-nginxlog-exporter` | `v1.11.0` | 4040 | מטריקות Prometheus (כולל זמני תגובה) | לא — רק אם `metrics.enabled=true` |
| `a0533057932/redis-docs-cli` | `latest` / `0.2.0` | 8090 | CLI playground proxy (Flask) | לא — רק אם `cli.enabled=true` |
| `redis` | `8-alpine` | 6379 | Redis sidecar ל-CLI playground | לא — רק אם `cli.enabled=true` |
| `quay.io/jupyter/minimal-notebook` | `2026-04-02` | 8888 | Jupyter kernel server להרצת קוד אינטראקטיבי | לא — רק אם `cli.jupyter.enabled=true` |

> ל-Kubernetes/OpenShift השתמשו בתג `unprivileged` או `<HASH>-unprivileged`.
> ל-`docker run` רגיל השתמשו בתג `latest` או `<HASH>`.
> ברשת סגורה מומלץ להשתמש בתג עם hash (Artifactory דורש תג שאינו `latest`).
> לתיעוד בניית האימג'ים ראו `BUILD.md` בשורש הפרויקט.

## התקנה

### שימוש בסיסי

```bash
helm install redis-docs redis-docs-0.11.0.tgz
```

### התקנה עם קובץ values

הדרך המומלצת - קובץ `values.yaml` מותאם:

```bash
helm install redis-docs redis-docs-0.11.0.tgz -f my-values.yaml
```

להלן דוגמה לתרחיש פריסה טיפוסי.

קבצי values מוכנים לשימוש ישיר נמצאים בתיקייה `examples/`:

```bash
helm install redis-docs ./helm/redis-docs -f helm/redis-docs/examples/values-openshift-airgapped.yaml
```

### OpenShift — רשת סגורה עם מטריקות

```yaml
# my-values.yaml

# --- רפליקה אחת ---
replicaCount: 1

# --- דריסת registry גלובלי ---
global:
  registry: registry.internal.company.com

# --- הרשאות משיכה ---
imagePullSecrets:
  - name: regcred

# --- תמונה ראשית (דריסת תג ספציפי) ---
image:
  name: redis-docs
  tag: "79955fdb5-unprivileged"

# --- מטריקות (דריסת תמונה ותג) ---
metrics:
  enabled: true
  image:
    name: prometheus-nginxlog-exporter
    tag: "v1.11.0"
  route:
    enabled: true
    # host ריק = OpenShift מייצר hostname אוטומטי + תעודה אוטומטית

# --- Route (בחרו אחת מ-3 האפשרויות) ---

# אפשרות א: Route אוטומטי + TLS אוטומטי של OpenShift
route:
  enabled: true
  tls:
    enabled: true
    termination: edge

# אפשרות ב: Route אוטומטי ללא TLS (HTTP בלבד)
# route:
#   enabled: true

# אפשרות ג: Route מותאם אישית + תעודה שלכם
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
#     ... (הדביקו כאן את התעודה)
#     -----END CERTIFICATE-----
#   privateKey: |
#     -----BEGIN PRIVATE KEY-----
#     ... (הדביקו כאן את המפתח)
#     -----END PRIVATE KEY-----
#   caCertificate: |
#     -----BEGIN CERTIFICATE-----
#     ... (אופציונלי — תעודת CA)
#     -----END CERTIFICATE-----

# --- לינקים חיצוניים ---
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

> `global.registry` דורס את ה-registry לכל התמונות. דריסת `image.name` ו-`image.tag` מאפשרת שליטה מלאה על כל תמונה.
>
> ברשת סגורה מומלץ להשתמש בתג עם commit hash (Artifactory דורש תג שאינו `latest`).
>
> **Route — 3 אפשרויות:**
> - **אפשרות א** — OpenShift מייצר hostname ותעודת TLS אוטומטית. הדרך הפשוטה ביותר.
> - **אפשרות ב** — HTTP בלבד, ללא הצפנה.
> - **אפשרות ג** — hostname מותאם + תעודה שלכם. דורש הגדרת `tls.certificate` ו-`tls.privateKey`.
>
> המטריקות מקבלות Route אוטומטי עם TLS של OpenShift תמיד (ללא תלות באפשרות שנבחרה לאתר).
>
> `externalLinks` — ניתן לדרוס URL לשירות פנימי חלופי (`url:`) או להסתיר (`enabled: false`).

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
docker pull quay.io/jupyter/minimal-notebook:2026-04-02
docker save quay.io/jupyter/minimal-notebook:2026-04-02 -o jupyter.tar
```

### שלב 2: אריזת Helm chart

```bash
helm package helm/redis-docs/
# ייצור: redis-docs-0.11.0.tgz
```

### שלב 3: העברת קבצים לרשת הסגורה

העבירו את הקבצים הבאים:
- `redis-docs-0.11.0.tgz`
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
docker tag quay.io/jupyter/minimal-notebook:2026-04-02 REGISTRY/jupyter/minimal-notebook:2026-04-02
docker push REGISTRY/jupyter/minimal-notebook:2026-04-02
```

> החליפו `REGISTRY` בכתובת ה-registry שלכם, לדוגמה: `registry.internal.company.com`

## עדכון גרסה

```bash
helm upgrade redis-docs redis-docs-0.11.0.tgz -f my-values.yaml
```

או עם דריסת ערך בודד:

```bash
helm upgrade redis-docs redis-docs-0.11.0.tgz -f my-values.yaml \
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
| `cli.jupyter.image.registry` | `quay.io` | registry לתמונת Jupyter |
| `cli.jupyter.image.name` | `jupyter/minimal-notebook` | שם תמונת Jupyter |
| `cli.jupyter.image.tag` | `2026-04-02` | תג תמונת Jupyter |
| `cli.jupyter.image.pullPolicy` | `IfNotPresent` | מדיניות משיכת תמונת Jupyter |
| `cli.jupyter.resources` | requests: 100m/256Mi, limits: 500m/512Mi | משאבי Jupyter |
| `aiServices.litellm.enabled` | `false` | הפעלת LiteLLM endpoint (במקום CloudFront חיצוני) |
| `aiServices.litellm.url` | `""` | URL ל-LiteLLM (OpenAI-compatible) |
| `aiServices.litellm.model` | `gpt-3.5-turbo` | שם המודל לשליחה |
| `aiServices.litellm.apiKey` | `""` | API key צד שרת (דילוג על שאלת המשתמש) |
| `aiServices.binder.url` | `https://redis.io/binder/` | URL ל-BinderHub / JupyterHub |
| `externalLinks.sandbox.enabled` | `true` | הצגת לינק ל-Redis Sandbox |
| `externalLinks.sandbox.url` | `https://redis.io/try/sandbox/` | כתובת Redis Sandbox |
| `externalLinks.tutorials.enabled` | `true` | הצגת לינק לטוטוריאלים |
| `externalLinks.tutorials.url` | `https://redis.io/tutorials/` | כתובת טוטוריאלים |
| `externalLinks.university.enabled` | `true` | הצגת לינק ל-Redis University |
| `externalLinks.university.url` | `https://university.redis.io/academy` | כתובת Redis University |
| `externalLinks.blog.enabled` | `true` | הצגת לינק לבלוג |
| `externalLinks.blog.url` | `https://redis.io/blog/` | כתובת הבלוג |
| `externalLinks.support.enabled` | `true` | הצגת לינק לפורטל תמיכה |
| `externalLinks.support.url` | `https://support.redislabs.com/hc/en-us` | כתובת פורטל תמיכה |
| `externalLinks.github.enabled` | `true` | הצגת לינק ל-GitHub |
| `externalLinks.github.url` | `https://github.com/redis/docs/` | כתובת מאגר GitHub |
| `externalLinks.chatbot.enabled` | `true` | הצגת לינק לצ'אטבוט |
| `externalLinks.chatbot.url` | `https://redis.io/chat` | כתובת צ'אטבוט AI |
| `nodeSelector` | `{}` | node selector לתזמון פודים |
| `tolerations` | `[]` | tolerations לתזמון פודים |
| `affinity` | `{}` | affinity rules לתזמון פודים |
