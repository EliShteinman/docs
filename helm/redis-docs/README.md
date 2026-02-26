# Redis Docs Helm Chart

Helm chart להתקנת אתר הדוקומנטציה של Redis על Kubernetes.
מותאם לרשת סגורה (air-gapped) - ללא תלויות חיצוניות.

## דרישות מקדימות

- Kubernetes 1.26+
- Helm 3.x
- Private Docker registry (ברשת סגורה)

## Docker images

| Image | שימוש | חובה? |
|---|---|---|
| `a0533057932/redis-docs` | אתר הדוקומנטציה (nginx + תוכן) | כן |
| `nginx/nginx-prometheus-exporter:1.4.0` | מטריקות Prometheus | לא - רק אם `metrics.enabled=true` |

## העברה לרשת סגורה

### שלב 1: שמירת Docker images

```bash
# אימג' ראשי (חובה)
docker pull a0533057932/redis-docs:unprivileged
docker save a0533057932/redis-docs:unprivileged -o redis-docs.tar

# מטריקות (אופציונלי)
docker pull nginx/nginx-prometheus-exporter:1.4.0
docker save nginx/nginx-prometheus-exporter:1.4.0 -o nginx-exporter.tar
```

### שלב 2: אריזת Helm chart

```bash
helm package helm/redis-docs/
# ייצור: redis-docs-0.1.0.tgz
```

### שלב 3: העברת קבצים לרשת הסגורה

העבירו את הקבצים הבאים:
- `redis-docs-0.1.0.tgz`
- `redis-docs.tar`
- `nginx-exporter.tar` (אופציונלי)

### שלב 4: טעינה ל-private registry

```bash
# טעינת אימג' ראשי
docker load -i redis-docs.tar
docker tag a0533057932/redis-docs:unprivileged REGISTRY/redis-docs:unprivileged
docker push REGISTRY/redis-docs:unprivileged

# טעינת מטריקות (אופציונלי)
docker load -i nginx-exporter.tar
docker tag nginx/nginx-prometheus-exporter:1.4.0 REGISTRY/nginx-prometheus-exporter:1.4.0
docker push REGISTRY/nginx-prometheus-exporter:1.4.0
```

> החליפו `REGISTRY` בכתובת ה-registry שלכם, לדוגמה: `registry.internal.company.com`

## התקנה

### בסיסי

```bash
helm install redis-docs redis-docs-0.1.0.tgz \
  --set image.repository=REGISTRY/redis-docs
```

### עם מטריקות

```bash
helm install redis-docs redis-docs-0.1.0.tgz \
  --set image.repository=REGISTRY/redis-docs \
  --set metrics.enabled=true \
  --set metrics.image.repository=REGISTRY/nginx-prometheus-exporter
```

### עם Ingress

```bash
helm install redis-docs redis-docs-0.1.0.tgz \
  --set image.repository=REGISTRY/redis-docs \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host=docs.company.internal \
  --set ingress.hosts[0].paths[0].path=/ \
  --set ingress.hosts[0].paths[0].pathType=Prefix
```

### אם ה-registry דורש הרשאות

```bash
# יצירת secret
kubectl create secret docker-registry regcred \
  --docker-server=REGISTRY \
  --docker-username=USER \
  --docker-password=PASS

# התקנה עם secret
helm install redis-docs redis-docs-0.1.0.tgz \
  --set image.repository=REGISTRY/redis-docs \
  --set imagePullSecrets[0].name=regcred
```

## עדכון גרסה

לעדכון תמונת Docker בלבד (ללא שינוי ב-chart):

```bash
helm upgrade redis-docs redis-docs-0.1.0.tgz \
  --set image.repository=REGISTRY/redis-docs \
  --set image.tag=NEW_TAG
```

> ה-repository וה-tag מפוצלים - אפשר לשנות רק את ה-tag בעת עדכון.

## גישה לאתר

לאחר התקנה:

```bash
kubectl port-forward svc/redis-docs 8080:80
# פתחו http://localhost:8080
```

## ערכים עיקריים

| ערך | ברירת מחדל | תיאור |
|---|---|---|
| `image.repository` | `a0533057932/redis-docs` | כתובת Docker image |
| `image.tag` | `unprivileged` | תג Docker image |
| `replicaCount` | `2` | מספר pods |
| `ingress.enabled` | `false` | הפעלת Ingress |
| `autoscaling.enabled` | `false` | הפעלת HPA (2-10 pods) |
| `metrics.enabled` | `false` | הפעלת Prometheus metrics |
| `metrics.serviceMonitor.enabled` | `false` | הפעלת ServiceMonitor (דורש Prometheus Operator) |
| `podDisruptionBudget.enabled` | `true` | הגנה בזמן rolling updates |
| `nginx.workerConnections` | `2048` | מספר חיבורים מקבילים per worker |
| `nginx.keepaliveTimeout` | `15` | timeout לחיבורים idle (שניות) |
