# בנייה אופליינית — Redis Docs

## דרישות

- Docker עם BuildKit (Docker Desktop 4.x+)
- `docker buildx` עם תמיכה ב-multi-platform
- קובץ `PRIVATE_ACCESS_TOKEN` בשורש הפרויקט שמכיל GitHub token (ל-API rate limit)

## סכמת תגים

כל שחרור מייצר **4 תגים** על **2 פלטפורמות** (linux/amd64 + linux/arm64):

| תג | Variant | פורט | שימוש |
|-----|---------|------|-------|
| `<HASH>` | privileged (nginx:alpine) | 80 | גרסה מתויגת — `docker run` |
| `latest` | privileged (nginx:alpine) | 80 | rolling tag — `docker run` |
| `<HASH>-unprivileged` | unprivileged (nginx-unprivileged) | 8080 | גרסה מתויגת — Kubernetes / OpenShift |
| `unprivileged` | unprivileged (nginx-unprivileged) | 8080 | rolling tag — Kubernetes / OpenShift |

> `<HASH>` = commit hash בן 9 תווים (`git rev-parse --short=9 HEAD`).
> ברשת סגורה מומלץ להשתמש בתג עם hash (Artifactory דורש תג שאינו `latest`).

## בנייה

שתי הפקודות רצות במקביל:

```bash
# Privileged variant (פורט 80)
docker buildx build --platform linux/amd64,linux/arm64 \
  --target final --build-arg VARIANT=privileged \
  --secret id=PRIVATE_ACCESS_TOKEN \
  -t a0533057932/redis-docs:<HASH> \
  -t a0533057932/redis-docs:latest \
  --push .

# Unprivileged variant (פורט 8080)
docker buildx build --platform linux/amd64,linux/arm64 \
  --target final --build-arg VARIANT=unprivileged \
  --secret id=PRIVATE_ACCESS_TOKEN \
  -t a0533057932/redis-docs:<HASH>-unprivileged \
  -t a0533057932/redis-docs:unprivileged \
  --push .
```

## מה הבנייה עושה

1. **Builder stage** (משותף לשני ה-variants):
   - Base image: `node:24-trixie` (Node 24 + Python 3.13)
   - התקנת Hugo 0.143.1
   - התקנת dependencies (npm + pip)
   - שינוי `baseURL` ל-`"/"` (תמיכה בכל דומיין)
   - יצירת קבצי version selector (kubernetes, rs, rdi, redisvl)
   - הרצת `make components && make ndjson` (שליפת דוגמאות + בניית Hugo + יצירת NDJSON)
   - דחיסת gzip מראש לכל הקבצים הסטטיים

2. **Runtime stage** (לפי VARIANT):
   - `privileged`: `nginx:alpine` על פורט 80
   - `unprivileged`: `nginx-unprivileged:alpine` על פורט 8080 (non-root)

## הבדלים מול CI של Redis

| | CI (redis.io) | Docker |
|---|---|---|
| baseURL | `/docs/latest` | `/` |
| גרסאות | בילד נפרד לכל גרסה | הכל בבילד אחד |
| פלט | GCS bucket | nginx container |
| gzip | GCS עושה compression | gzip_static מראש |
| GitHub token | לא נדרש | אופציונלי (rate limit) |

## מיפוי URLs

משתמש שרואה לינק ב-redis.io:
```
https://redis.io/docs/latest/commands/set/
```

אצלך:
```
https://my-internal.com/commands/set/
```

**הכלל: החליפו `https://redis.io/docs/latest` ב-`https://<DOMAIN>`.**

## הרצה מקומית

```bash
docker run -p 8080:8080 a0533057932/redis-docs:unprivileged
# פתחו http://localhost:8080
```

או עם ה-privileged variant:

```bash
docker run -p 80:80 a0533057932/redis-docs:latest
# פתחו http://localhost
```

## קבצי Vendor (מחליפי CDN)

האתר המקורי טוען סקריפטים מ-CDN חיצוניים. לצורך פריסה אופליינית, כל הקבצים הוכנסו לתיקייה `static/vendor/`:

| קובץ | גרסה | מקור מקורי | תיאור |
|------|-------|-----------|-------|
| `highlight.min.js` | v11.11.1 | cdnjs.cloudflare.com | הדגשת תחביר בדוגמאות קוד |
| `marked.min.js` | v9.1.6 | cdn.jsdelivr.net | פרסור Markdown (Agent Builder) |
| `mathjax-tex-mml-chtml.js` | v3.x | cdn.jsdelivr.net | נוסחאות מתמטיות |
| `mermaid.min.js` | v11.14.0 | cdn.jsdelivr.net | דיאגרמות (flowcharts, sequence) |
| `redoc.standalone.js` | latest | cdn.redoc.ly | תצוגת OpenAPI/Swagger |
| `thebe.js` | 0.9.0-rc.12 | unpkg.com | הרצת קוד אינטראקטיבית (Jupyter) |
| `thebe.css` | 0.9.0-rc.12 | unpkg.com | עיצוב Thebe |
| `codemirror-javascript.js` | 5.65.16 | unpkg.com | מצב הדגשת תחביר JavaScript ל-Thebe (mode/javascript/javascript.js) |

> לעדכון: הורידו את הגרסה החדשה מהמקור המקורי, החליפו את הקובץ ב-`static/vendor/`, ועדכנו טבלה זו.

## ניהול לינקים חיצוניים

האתר מכיל עשרות לינקים ל-`redis.io` — בדף הבית, בתפריט העליון, בתפריטי ה-dropdown ובפוטר. רוב הלינקים האלו לא יעבדו בפריסה airgap. הצ'ארט מספק מנגנון **היררכי** של חמש שכבות לניהול שלהם.

### מבנה היררכי

הקטלוג מסודר ב-**משפחות** וב-**תתי-משפחות**:

```
externalLinks.enabled                    ← master kill-switch
└── families
    ├── home                              ← קישורים בגוף עמוד הבית
    │   └── links: { sandbox, tutorials, ... }
    └── header                            ← תפריט עליון
        └── sub-families
            ├── main-nav: { Redis for AI, Docs, Pricing }
            ├── cta: { Login, Book a meeting, Try Redis }
            ├── search: { search button }
            ├── products-dropdown
            ├── resources-dropdown
            └── mobile: { hamburger + drawer }
```

(`footer` נוספת בקומיט בנפרד.)

### שכבה 1 — קטלוג ברירות המחדל

`helm/redis-docs/files/external-links.yaml` — רשימת **כל הלינקים** מאורגנים במשפחות ותתי-משפחות, עם ה-URL המקורי, תיאור, ו-`enabled: true` ברירת מחדל. אין לערוך אותו עבור deployment ספציפי.

### שכבות 2-5 — קונפיג מ-`values.yaml`

#### שכבה 2: Kill-switch גלובלי

```yaml
externalLinks:
  enabled: false   # מסתיר את הכל בבת אחת
```

#### שכבה 3: רמת משפחה

```yaml
externalLinks:
  enabled: false
  families:
    home:
      enabled: true   # להפעיל רק את משפחת home
```

#### שכבה 4: רמת תת-משפחה

```yaml
externalLinks:
  enabled: false
  families:
    header:
      sub-families:
        main-nav:
          enabled: true   # רק main-nav של header פעיל
```

#### שכבה 5: Override פר-לינק

```yaml
externalLinks:
  enabled: false
  overrides:
    tutorials:
      enabled: true
    github:
      enabled: true
      url: "https://gitlab.internal.company.com/redis-docs"
```

### סדר עדיפויות עבור `enabled` (הגבוה דורס)

1. `overrides.<key>.enabled` — פר-לינק (תמיד הכי חזק)
2. `families.<fam>.sub-families.<sub>.enabled` — תת-משפחה
3. `families.<fam>.enabled` — משפחה
4. `externalLinks.enabled` — global kill-switch
5. catalog default — תמיד true

הסדר עבור `url`: קטלוג ברירת מחדל, ואופציונלית `overrides.<key>.url`.

### דוגמה: airgap עם re-enable היררכי

```yaml
externalLinks:
  enabled: false              # global off
  families:
    home:
      enabled: true           # אבל home דווקא כן יוצג
    header:
      sub-families:
        main-nav:
          enabled: true       # וגם main-nav של header
  overrides:
    nav-pricing:
      enabled: false          # חוץ מ-Pricing שדווקא יוסתר
    github:
      url: "https://gitlab.internal/redis-docs"  # github עם URL פנימי
```

### איך זה מגיע לדפדפן

`templates/configmap-runtime.yaml` הולך על העץ ההיררכי ב-`helm install/upgrade`, מחשב `enabled` יעיל לכל מפתח לפי סדר העדיפויות, ופולט מפה שטוחה ל-`window.RUNTIME_CONFIG.externalLinks`. ה-JS המשותף ב-`layouts/partials/external-links.html` מטפל בכל אלמנט שמסומן ב-`data-external-link="<key>"` (מסתיר אם `enabled === false`, מחליף `href` אם יש `url`).

## הזרקת URL קנוני בזמן ריצה (`canonicalURL`)

### הבעיה
כש-Hugo מייצר את גרסאות ה-`.md` וה-`.json` של עמודים (שמיועדות לצריכת AI/RAG), ה-shortcodes הפנימיים `{{< relref "..." >}}` ו-`{{< image filename="..." >}}` חייבים להפוך ל-URLs מלאים — אחרת LLM שמקבל את התוכן בלי הקשר של הדפדפן לא יודע מה ה-domain. אבל hardcoding של domain ספציפי (כמו `https://redis.io/docs/latest/`) פוגע בגמישות, ושינוי ל-domain פנימי דורש build נפרד לכל deployment.

### הפתרון
**Hugo כותב placeholder, nginx מחליף בזמן ריצה.**

1. **Build time** (`layouts/partials/process-markdown-content.html`): כל `{{< relref >}}` ו-`{{< image >}}` מומר ל-`__DOCS_BASE_URL__/<path>`. הקבצים נשמרים סטטית עם ה-placeholder.
2. **Helm value** (`values.yaml`): שדה `canonicalURL` (ברירת מחדל ריק).
3. **Runtime** (`templates/configmap.yaml` של ה-Helm chart): `nginx sub_filter` בלוקיישן של `.md`/`.json` מחליף את ה-placeholder. הערך:
   - אם `canonicalURL` הוגדר ב-`values.yaml` → תמיד אותו URL
   - אם ריק → `$scheme://$http_host` של הבקשה (auto-detect — אותה image על מספר דומיינים)

### דוגמה

```yaml
# values.yaml
canonicalURL: "https://docs.intranet.example.com"
```

המשתמש מבקש `GET /develop/foo/index.md`. הקובץ על הדיסק מכיל:
```markdown
ראו [את העמוד הבא](__DOCS_BASE_URL__/develop/bar) למידע נוסף
```

nginx מחליף ושולח:
```markdown
ראו [את העמוד הבא](https://docs.intranet.example.com/develop/bar) למידע נוסף
```

### גבולות
- ה-`sub_filter` פעיל **רק על `.md` ו-`.json`** — לא על HTML/CSS/JS. אין סיכון להחלפה לא צפויה ב-content אחר.
- `gzip_static` כבוי בלוקיישן הזה (כי `sub_filter` לא יכול לפעול על תוכן מכווץ); דחיסה דינמית פעילה במקום זאת.
- ה-`__DOCS_BASE_URL__` מוטמע **רק על ידי 4 השורות** ב-`process-markdown-content.html`, וכל אחת מהן מטפלת ב-shortcode פנימי שמצביע על תוכן באתר. כתובות חיצוניות שמשתמש כתב ידנית ב-MD לא נוגעים בהן.
- לוגו ה-header וה-footer מצביעים תמיד ל-`/` — לא תלויים ב-`canonicalURL`.
