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

שני ConfigMaps מזריקים תצורת זמן-ריצה לתוך nginx:

- **`configmap-runtime.yaml`** — מייצר `runtime-config.js` שנטען בכל עמוד. מכיל:
  - `aiServices.litellm` — כתובת LiteLLM endpoint (במקום CloudFront חיצוני)
  - `aiServices.binder.url` — כתובת BinderHub / JupyterHub
  - `externalLinks` — `enabled`/`url` יעיל לכל לינק חיצוני בקטלוג
- **`configmap.yaml`** — קובץ ה-`default.conf` של nginx, שמשתמש ב-`canonicalURL` כדי להחליף את ה-placeholder `__DOCS_BASE_URL__` בתוך תגובות `.md` / `.json` בזמן הגשת הבקשה.

### לינקים חיצוניים (externalLinks)

האתר מכיל ~87 לינקים חיצוניים פזורים בגוף עמוד הבית, בתפריט העליון (לוגו, ניווט שיווקי, תפריטי dropdown), ובפוטר התחתון. כמעט אף אחד מהם לא יעבוד בהתקנה airgap. ההגדרה היא היררכית בת חמש שכבות:

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

הקטלוג המלא (כל מפתח עם תיאור ו-URL מקורי) נשלח עם הצ'ארט בקובץ `files/external-links.yaml`. אין לערוך אותו עבור deployment ספציפי — לזה מיועד `values.yaml`.

**סדר עדיפויות עבור `enabled`** (הגבוה דורס):

1. `overrides.<key>.enabled` — override פר-לינק
2. `families.<fam>.sub-families.<sub>.enabled` — kill-switch של תת-משפחה
3. `families.<fam>.enabled` — kill-switch של משפחה
4. `externalLinks.enabled` — master kill-switch
5. catalog default — תמיד `true`

עבור `url` הסדר פשוט יותר: ברירת מחדל מהקטלוג, אלא אם `overrides.<key>.url` דורס.

**ברירת המחדל של הצ'ארט היא `enabled: false`** — כל הלינקים החיצוניים מוסתרים מתוך הקופסה. הפעלה מחדש בכל רמה מתאימה ל-deployment:

```yaml
externalLinks:
  enabled: false             # master kill-switch (default)
  families:
    home:
      enabled: true          # כל הלינקים בעמוד הבית פעילים
    header:
      sub-families:
        main-nav:
          enabled: true      # רצועת ההדר: רק Redis-for-AI / Docs / Pricing
  overrides:
    tutorials:
      enabled: true          # להפעיל לינק ספציפי
    github:
      enabled: true
      url: "https://gitlab.internal.company.com/redis-docs"  # גם להחליף URL
    nav-search:
      enabled: false         # להשאיר מוסתר במפורש
```

שני הלוגואים (פינה שמאלית עליונה של ההדר ושל הפוטר) תמיד מקושרים ל-`/` (בית הדוקס המקומי) ואינם חלק מהקטלוג — הם מוצגים תמיד ולא ניתנים לקנפוג ל-deployment.

### מירורי Git (`externalLinks.gitMirrors`)

מנגנון נפרד שמשכתב לינקים מסוג `<a href>` בתוך תוכן Markdown (URLs של דשבורדי Grafana, קונפיגי alerts של Prometheus, listings של repositories וכו') מ-host ציבורי במעלה הזרם למירור פנימי.

המנגנון **אינו** חלק ממערכת ה-`families` / `overrides` שלמעלה — אלה מתמקדות באלמנטים של ה-layout עם `data-external-link="<key>"` (כרטיסי עמוד הבית, רצועת ההדר, עמודות הפוטר). `gitMirrors` מתאים לפי קידומת URL ב-HTML המרונדר, וזה מה שלינקים מתוך תוכן צריכים.

הקטלוג של המירורים הזמינים נמצא ב-`files/external-links.yaml` תחת `git-mirrors:`. לכל entry יש כתובת upstream (`from`) קבועה — הצ'ארט נשלח עם שני entries:

| שם | upstream | תיעוד מושפע |
|---|---|---|
| `observability` | `https://github.com/redis-field-engineering/redis-enterprise-observability` | 36 לינקים מוטמעים ב-`rs-observability.md`, `rs-prometheus-grafana-quickstart.md`, `prometheus-with-redis-cloud/_index.md` |
| `k8s-docs` | `https://github.com/RedisLabs/redis-enterprise-k8s-docs` | ~179 לינקים מוטמעים ב-~89 קבצים תחת `content/operate/kubernetes/` (releases של ה-operator, ה-API reference, manifests לדוגמה, vault, rack-awareness) |

הפעלה פר-deployment היא שני שדות ב-`values.yaml` לכל מירור:

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

> ה-handler משכתב רק כתובות `<a href>` (קישורים לחיצים). פקודות `curl` / `kubectl apply -f` בתוך code-blocks שמפנות ל-`raw.githubusercontent.com/...` **לא** עוברות שכתוב — הן דורשות החלפה build-time נפרדת אם נדרש.

ה-URL ב-`to` מטופל כקידומת אטומית — יש לספק את כתובת הפרויקט המלאה, כולל כל נסטינג של GitLab groups. ה-handler ב-runtime מתרגם נתיבי GitHub (`/blob/<ref>/<path>`, `/tree/<ref>/<path>`, `/raw`, `/blame`, `/commits`, `/commit`, `/tags`, `/releases`, `/wiki`, `/issues`) למקבילות שלהם ב-GitLab (`/-/blob/...`, `/-/tree/...`, וכו') באופן אוטומטי.

**ההפעלה היא Helm בלבד**: שינוי `values.yaml` מייצר מחדש את ה-ConfigMap של ה-runtime (`runtime-config.js`), וה-annotation `checksum/runtime-config` גורם ל-rolling restart. אין צורך לבנות מחדש את ה-image, ואותה image יכולה להגיש URLs שונים של מירור עבור deployments שונים.

**הוספת מירור חדש** (למשל repo נוסף שמוזכר בתיעוד) היא שני שלבים: הוספת entry תחת `git-mirrors:` בקטלוג עם כתובת ה-`from` שלו, ולאחר מכן opt-in פר-deployment עם `enabled: true` ו-`to: <כתובת המירור>` ב-`values.yaml`. אין צורך לשנות template, handler, Hugo, או image.

### החלפת URL קנוני (`canonicalURL`)

כש-Hugo בונה את פורמטי ה-AI / RAG (`.md`, `.json`), הוא מרחיב shortcodes פנימיים כמו `{{< relref "..." >}}` ו-`{{< image filename="..." >}}` ל-placeholder בצורת `__DOCS_BASE_URL__/<path>`. nginx מחליף את ה-placeholder בזמן ריצה כך שצרכנים שצורכים את ה-Markdown ללא הקשר של HTML עדיין רואים URLs מלאים:

```yaml
canonicalURL: "https://docs.intranet.example.com"
```

כש-`canonicalURL` ריק (ברירת מחדל), nginx משתמש ב-`$scheme://$http_host` של הבקשה — אותה image שנפרסת ב-hostnames פנימיים מרובים מקבלת URLs לכל host בנפרד.

ה-`sub_filter` מוגבל ל-`.md` / `.json` בלבד. תגובות HTML / CSS / JS לעולם לא נכתבות מחדש, וה-placeholder מוטמע רק בארבע נקודות מוגדרות היטב בתוך `process-markdown-content.html` (shortcodes של relref + image), כך שכתובות חיצוניות שמחבר כתב ידנית ב-Markdown נשארות ללא שינוי.

## Docker images

| Image | תג | פורט | שימוש | חובה? |
|---|---|---|---|---|
| `a0533057932/redis-docs` | `<HASH>` / `latest` | 80 | הרצה רגילה עם `docker run` (privileged) | כן — אחד מהשניים |
| `a0533057932/redis-docs` | `<HASH>-unprivileged` / `unprivileged` | 8080 | Kubernetes / OpenShift (non-root) | כן — אחד מהשניים |
| `quay.io/martinhelmich/prometheus-nginxlog-exporter` | `v1.11.0` | 4040 | מטריקות Prometheus (כולל זמני תגובה) | לא — רק אם `metrics.enabled=true` |
| `a0533057932/redis-docs-cli` | `latest` / `0.3.3` | 8090 | CLI playground proxy (Flask) | לא — רק אם `cli.enabled=true` |
| `redis` | `8-alpine` | 6379 | Redis sidecar ל-CLI playground | לא — רק אם `cli.enabled=true` |
| `quay.io/jupyter/minimal-notebook` | `2026-04-02` | 8888 | Jupyter kernel server להרצת קוד אינטראקטיבי | לא — רק אם `cli.jupyter.enabled=true` |

> ל-Kubernetes/OpenShift השתמשו בתג `unprivileged` או `<HASH>-unprivileged`.
> ל-`docker run` רגיל השתמשו בתג `latest` או `<HASH>`.
> ברשת סגורה מומלץ להשתמש בתג עם hash (Artifactory דורש תג שאינו `latest`).
> לתיעוד בניית האימג'ים ראו `BUILD.md` בשורש הפרויקט.

## התקנה

### שימוש בסיסי

```bash
helm install redis-docs redis-docs-1.0.0.tgz
```

### התקנה עם קובץ values

הדרך המומלצת - קובץ `values.yaml` מותאם:

```bash
helm install redis-docs redis-docs-1.0.0.tgz -f my-values.yaml
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
  tag: "30ecd868d-unprivileged"

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
# --- Canonical public URL (משמש את nginx sub_filter ב-.md/.json) ---
# canonicalURL: "https://docs.intranet.company.com"   # ריק = auto-detect מהבקשה

# --- External links ---
# Master kill-switch מופעל. הפעלה מחדש של לינקים ספציפיים דרך overrides.
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
# ייצור: redis-docs-1.0.0.tgz
```

### שלב 3: העברת קבצים לרשת הסגורה

העבירו את הקבצים הבאים:
- `redis-docs-1.0.0.tgz`
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
docker tag a0533057932/redis-docs-cli:latest REGISTRY/redis-docs-cli:0.3.3
docker push REGISTRY/redis-docs-cli:0.3.3

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
helm upgrade redis-docs redis-docs-1.0.0.tgz -f my-values.yaml
```

או עם דריסת ערך בודד:

```bash
helm upgrade redis-docs redis-docs-1.0.0.tgz -f my-values.yaml \
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
| `cli.image.tag` | `latest` | תג תמונת CLI proxy (ברשת סגורה: `0.3.3`) |
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
| `canonicalURL` | `""` | URL ציבורי של ה-deployment, משמש את nginx sub_filter להחלפת `__DOCS_BASE_URL__` ב-`.md` / `.json`. ריק → auto-detect מ-`$http_host`. |
| `externalLinks.enabled` | `false` | Master kill-switch לכל הלינקים החיצוניים בקטלוג. ברירת מחדל מסתירה הכל (airgap-first). |
| `externalLinks.families.<fam>.enabled` | unset | Kill-switch ברמת משפחה (למשל `home`, `header`, `footer`). הגדר `true` כדי להפעיל משפחה שלמה. |
| `externalLinks.families.<fam>.sub-families.<sub>.enabled` | unset | Kill-switch ברמת תת-משפחה (למשל `header.main-nav`, `footer.legal`). |
| `externalLinks.overrides.<key>.enabled` | unset | Override פר-לינק. דורס משפחה / תת-משפחה / master. |
| `externalLinks.overrides.<key>.url` | unset | החלפת URL של לינק יחיד (בדרך כלל למראה פנימי). |
| `nodeSelector` | `{}` | node selector לתזמון פודים |
| `tolerations` | `[]` | tolerations לתזמון פודים |
| `affinity` | `{}` | affinity rules לתזמון פודים |
