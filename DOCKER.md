# בניית Docker Image — Redis Docs

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
