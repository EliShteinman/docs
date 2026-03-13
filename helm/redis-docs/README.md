# Redis Docs Helm Chart

Helm chart להתקנת אתר הדוקומנטציה של Redis על Kubernetes / OpenShift.
מותאם לרשת סגורה (air-gapped) - ללא תלויות חיצוניות.

## דרישות מקדימות

- Kubernetes 1.26+ / OpenShift 4.x+
- Helm 3.x
- Private Docker registry (ברשת סגורה)

## Docker images

| Image | תג | פורט | שימוש | חובה? |
|---|---|---|---|---|
| `a0533057932/redis-docs` | `latest` | 80 | הרצה רגילה עם `docker run` (privileged) | כן - אחד מהשניים |
| `a0533057932/redis-docs` | `unprivileged` | 8080 | Kubernetes / OpenShift (non-root) | כן - אחד מהשניים |
| `quay.io/martinhelmich/prometheus-nginxlog-exporter` | `v1.11.0` | 4040 | מטריקות Prometheus (כולל זמני תגובה) | לא - רק אם `metrics.enabled=true` |
| `a0533057932/redis-docs-cli` | `latest` / `0.1.0` | 8090 | CLI playground proxy (Flask) | לא - רק אם `cli.enabled=true` |
| `redis` | `8-alpine` | 6379 | Redis sidecar ל-CLI playground | לא - רק אם `cli.enabled=true` |

> ל-Kubernetes/OpenShift השתמשו בתג `unprivileged`. ל-`docker run` רגיל השתמשו בתג `latest`.

## התקנה

### שימוש בסיסי

```bash
helm install redis-docs redis-docs-0.4.0.tgz
```

### התקנה עם קובץ values

הדרך המומלצת - קובץ `values.yaml` מותאם:

```bash
helm install redis-docs redis-docs-0.4.0.tgz -f my-values.yaml
```

להלן דוגמאות לקבצי values לתרחישים שונים.

### רשת פתוחה — OpenShift עם מטריקות + CLI

```yaml
# my-values.yaml
route:
  enabled: true

metrics:
  enabled: true
  route:
    enabled: true

cli:
  enabled: true
```

> Route נפרד ייווצר עבור endpoint המטריקות על פורט 4040 בנתיב `/metrics`.
>
> מטריקות זמינות כוללות: `nginx_http_response_time_seconds` (histogram), `nginx_http_response_count_total`, `nginx_http_response_size_bytes`.
>
> ייווצר פוד נפרד עם Flask proxy + Redis sidecar. ה-CLI יהיה זמין בנתיב `/cli`.

### רשת פתוחה — OpenShift עם hostname מותאם

```yaml
# my-values.yaml
route:
  enabled: true
  host: docs.apps.example.com

metrics:
  enabled: true
  route:
    enabled: true
    host: docs-metrics.apps.example.com
```

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

route:
  enabled: true

metrics:
  enabled: true
  route:
    enabled: true

cli:
  enabled: true
  image:
    tag: "0.1.0"
```

> `global.registry` משנה את ה-registry לכל התמונות (ראשית + מטריקות + CLI).
>
> ברשת סגורה יש לתייג את CLI proxy כ-`0.1.0` (Artifactory דורש תג שאינו `latest`).

### רשת סגורה — דריסת registry לתמונה ספציפית

```yaml
# my-values.yaml
image:
  registry: my-registry.com

metrics:
  enabled: true
  image:
    registry: other-registry.com
```

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
```

### שלב 2: אריזת Helm chart

```bash
helm package helm/redis-docs/
# ייצור: redis-docs-0.4.0.tgz
```

### שלב 3: העברת קבצים לרשת הסגורה

העבירו את הקבצים הבאים:
- `redis-docs-0.4.0.tgz`
- `redis-docs.tar`
- `nginx-exporter.tar` (אופציונלי - מטריקות)
- `redis-docs-cli.tar` (אופציונלי - CLI)
- `redis.tar` (אופציונלי - CLI)

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
docker tag a0533057932/redis-docs-cli:latest REGISTRY/redis-docs-cli:0.1.0
docker push REGISTRY/redis-docs-cli:0.1.0

docker load -i redis.tar
docker tag redis:8-alpine REGISTRY/redis:8-alpine
docker push REGISTRY/redis:8-alpine
```

> החליפו `REGISTRY` בכתובת ה-registry שלכם, לדוגמה: `registry.internal.company.com`

## עדכון גרסה

```bash
helm upgrade redis-docs redis-docs-0.4.0.tgz -f my-values.yaml
```

או עם דריסת ערך בודד:

```bash
helm upgrade redis-docs redis-docs-0.4.0.tgz -f my-values.yaml \
  --set image.tag=NEW_TAG
```

## גישה לאתר

לאחר התקנה:

```bash
kubectl port-forward svc/redis-docs 8080:80
# פתחו http://localhost:8080
```

## ערכים עיקריים

| ערך | ברירת מחדל | תיאור |
|---|---|---|
| `global.registry` | `""` | דריסת registry לכל התמונות |
| `image.registry` | `a0533057932` | registry לתמונה הראשית |
| `image.name` | `redis-docs` | שם התמונה הראשית |
| `image.tag` | `unprivileged` | תג התמונה הראשית |
| `replicaCount` | `1` | מספר pods |
| `ingress.enabled` | `false` | הפעלת Ingress (Kubernetes) |
| `route.enabled` | `false` | הפעלת Route (OpenShift) |
| `route.host` | `""` | hostname ל-Route (אוטומטי אם ריק) |
| `route.tls.termination` | `edge` | סוג TLS termination |
| `autoscaling.enabled` | `false` | הפעלת HPA (1-10 pods) |
| `metrics.enabled` | `false` | הפעלת Prometheus metrics |
| `metrics.image.registry` | `quay.io/martinhelmich` | registry לתמונת מטריקות |
| `metrics.image.name` | `prometheus-nginxlog-exporter` | שם תמונת מטריקות |
| `metrics.image.tag` | `v1.11.0` | תג תמונת מטריקות |
| `metrics.route.enabled` | `false` | הפעלת Route למטריקות (OpenShift) |
| `metrics.route.host` | `""` | hostname ל-Route מטריקות (אוטומטי אם ריק) |
| `metrics.serviceMonitor.enabled` | `false` | הפעלת ServiceMonitor (דורש Prometheus Operator) |
| `podDisruptionBudget.enabled` | `true` | הגנה בזמן rolling updates |
| `nginx.workerConnections` | `2048` | מספר חיבורים מקבילים per worker |
| `nginx.keepaliveTimeout` | `15` | timeout לחיבורים idle (שניות) |
| `cli.enabled` | `false` | הפעלת CLI playground (פוד נפרד עם Flask + Redis) |
| `cli.image.registry` | `a0533057932` | registry לתמונת CLI proxy |
| `cli.image.name` | `redis-docs-cli` | שם תמונת CLI proxy |
| `cli.image.tag` | `latest` | תג תמונת CLI proxy (ברשת סגורה: `0.1.0`) |
| `cli.redis.image.tag` | `8-alpine` | תג תמונת Redis sidecar |
