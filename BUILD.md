# בנייה אופליינית — Redis Docs

## דרישות

יש שתי דרכי בנייה — בענן (GitHub Actions) ובמחשב המקומי. שלב 3 שלמטה מתעד את שתיהן.

**משותף:**
- חשבון DockerHub עם הרשאת write ל-`a0533057932/redis-docs`

**לבנייה בענן (אופציה A — מומלץ):**
- Repository ב-GitHub עם 3 secrets/vars (כבר מוגדרים אצלך):
  - Variable `DOCKERHUB_USERNAME` = `a0533057932`
  - Secret `DOCKERHUB_TOKEN` = DockerHub Access Token עם הרשאת write
  - Secret `PRIVATE_ACCESS_TOKEN` = GitHub PAT עם scope `repo` (ל-`make components`)

**לבנייה מקומית (אופציה B):**
- Docker עם BuildKit (Docker Desktop 4.x+)
- `docker buildx` עם תמיכה ב-multi-platform
- קובץ `PRIVATE_ACCESS_TOKEN` בשורש הפרויקט שמכיל GitHub PAT (ל-API rate limit + clone של repos פרטיים)

## סכמת תגים

כל שחרור מייצר **8 תגים** על **2 פלטפורמות** (linux/amd64 + linux/arm64) — ארבעה
לאתר וארבעה לתמונת המירור:

| תג | Variant | פורט | שימוש |
|-----|---------|------|-------|
| `<HASH>` | privileged (nginx:alpine) | 80 | גרסה מתויגת — `docker run` |
| `latest` | privileged (nginx:alpine) | 80 | rolling tag — `docker run` |
| `<HASH>-unprivileged` | unprivileged (nginx-unprivileged) | 8080 | גרסה מתויגת — Kubernetes / OpenShift |
| `unprivileged` | unprivileged (nginx-unprivileged) | 8080 | rolling tag — Kubernetes / OpenShift |

למירור (`a0533057932/redis-docs-mirror`) יש תג משלו, `<MIRROR>` = ‏`<commit של mirror/site, 9 תווים>-<hash של Dockerfile.runtime ו-build/marketing_mirror/runtime, 8 תווים>`,
באותן ארבע צורות (`<MIRROR>`, ‏`latest`, ‏`<MIRROR>-unprivileged`, ‏`unprivileged`). הוא נבנה רק כשהתג הזה
עוד לא קיים עם כל הפלטפורמות. ה-chart פורס את `<MIRROR>-unprivileged` כש-`mirror.enabled=true`,
ו-`helm show chart` מציג אותו (וכל image אחר של אותה גרסה) תחת `artifacthub.io/images`.

> `<HASH>` = commit hash בן 9 תווים (`git rev-parse --short=9 HEAD`).
> ברשת סגורה מומלץ להשתמש בתג עם hash (Artifactory דורש תג שאינו `latest`).

## תהליך עדכון מקצה לקצה

תהליך התחזוקה הסטנדרטי בכל פעם ש-upstream של redis מפרסם תוכן/תיקונים חדשים. הסדר חשוב — אל תדלג על שלבים.

### שלב 1 — סקירה לפני מיזוג (5-10 דק)

המטרה: לוודא ש-upstream לא הכניס דבר ש"שוקע מתחת לרדאר" של מנגנוני ה-airgap (קטלוג `externalLinks`, vendored CDN, sed של `redis.io/docs/latest/`).

```bash
git fetch origin
MERGE_BASE=$(git merge-base HEAD origin/main)
git log --oneline $MERGE_BASE..origin/main          # מה מגיע (כותרות הקומיטים)
git diff --stat $MERGE_BASE..origin/main | tail     # היקף השינוי

# בדיקה 1 — לינקים חיצוניים חדשים בתבניות שלא מטופלים ע"י externalLinks:
git diff $MERGE_BASE..origin/main -- layouts/ \
  | grep -E '^\+' | grep -E 'href=["'"'"']https?://' | grep -v data-external-link
# שורות יוצאות = יש לינק שיצטרך להיכנס ל-helm/redis-docs/files/external-links.yaml

# בדיקה 2 — סקריפטים חיצוניים חדשים (cdn.*, unpkg.*, fonts.googleapis וכו'):
git diff $MERGE_BASE..origin/main \
  | grep -E '^\+' | grep -oE '(cdn\.[a-z]+|jsdelivr|unpkg|fonts\.googleapis|googletagmanager)[^ "]*' | sort -u
# שורות יוצאות = יש סקריפט שיצטרך לוונדור ל-static/vendor/

# בדיקה 3 — aliases חדשים שמצביעים לנתיבי גרסאות (יוצרים artifacts ב-airgap-multibuild):
git diff $MERGE_BASE..origin/main -- 'content/**.md' \
  | grep -E '^\+aliases:' | grep -oE '/(operate|develop)/[^ ,\]"]+/[0-9]+\.[0-9]+(\.[0-9]+)?/' | sort -u
# שורות יוצאות = ייתכן ש-airgap-multibuild.sh יצטרך התאמה (כרגע יש rm -rf לפני cp -a שמטפל ברוב המקרים)

# בדיקה 4 — תיקיות גרסה חדשות (כל תיקייה תחת content/operate/{rs,kubernetes}/ או content/develop/ai/redisvl/ עם שם של מספר):
git diff --diff-filter=A --name-only $MERGE_BASE..origin/main \
  | grep -E '^content/(operate/(rs|kubernetes)|develop/ai/redisvl)/[0-9]+\.[0-9]+(\.[0-9]+)?/_index\.md$'
# שורות יוצאות = airgap-multibuild.sh יגלה אותן אוטומטית, לא נדרש שינוי
```

אם אחת מבדיקות 1-3 מחזירה שורות → טיפלו לפני המיזוג (עדכון catalog, וונדור קובץ, או שינוי בסקריפט).

### שלב 2 — מיזוג

```bash
git merge origin/main
# auto-merge ברוב המקרים. במקרה של conflict — ידני
```

### שלב 3 — בנייה

> **לפני כל בנייה — בדיקת drift של `cli.js`** (חובה): `python3 build/check_cli_js_drift.py`.
> exit 1 = הקובץ הקנוני של רדיס השתנה → לרה-וונדר ולסקור לפני הבנייה. פירוט בסעיף
> "widget ה-redis-cli האינטראקטיבי" למטה.

שתי דרכים — בענן או מקומית. שתיהן מייצרות את אותם תגים ב-DockerHub.

#### אופציה A — בנייה בענן (GitHub Actions, מומלץ)

GHA workflow מקבילי: phase 1 setup → phase 2 הוא 29 ריצות Hugo במקביל (latest + 28 גרסאות) → phase 3 assemble → phase 4 push.

**הרצה:**
1. `git push fork feature/docker-support` (או הbranch הרצוי) — לוודא שהcommit נמצא ב-GitHub
2. https://github.com/EliShteinman/docs/actions/workflows/airgap-build.yml → **Run workflow**
3. בחר branch, השאר את ה-inputs כברירת מחדל (אם רוצים build רגיל)

**Inputs אופציונליים** (לבדיקות):

| Input | ערכים | שימוש |
|--------|--------|--------|
| `variant` | both / privileged / unprivileged | לבנות רק וריאנט אחד |
| `platforms` | both / amd64 / arm64 | לבנות לrch ייעודי (חיסכון בזמן push) |
| `tag_override` | טקסט חופשי (e.g. `test1`) | תג זמני בלי לדרוס `:latest` / `:unprivileged` |

**זמן:** ~10-15 דק׳ first run, ~6-10 דק׳ אחרי שה-cache מאוכלס.

**ה-Summary page** של ה-run יציג בסוף פקודות `docker pull` ו-`docker run` להעתקה.

#### אופציה B — בנייה מקומית (Docker buildx)

ידני, על המק/לינוקס. משתמש ב-`Dockerfile` ובסקריפט `airgap-multibuild.sh` (28+1 ריצות Hugo ברצף בתוך container).

```bash
HASH=$(git rev-parse --short=9 HEAD)

# ראשון — unprivileged. בונה את builder stage המלא (~14 דק multi-arch).
docker buildx build --platform linux/amd64,linux/arm64 \
  --target final --build-arg VARIANT=unprivileged \
  --secret id=PRIVATE_ACCESS_TOKEN \
  -t a0533057932/redis-docs:${HASH}-unprivileged \
  -t a0533057932/redis-docs:unprivileged \
  --push .

# שני — privileged. מקבל cache מלא של builder stage (~3-5 דק).
docker buildx build --platform linux/amd64,linux/arm64 \
  --target final --build-arg VARIANT=privileged \
  --secret id=PRIVATE_ACCESS_TOKEN \
  -t a0533057932/redis-docs:${HASH} \
  -t a0533057932/redis-docs:latest \
  --push .
```

> **למה ברצף ולא במקביל?** שני ה-variants חולקים את אותו builder stage. כשהראשון מסתיים, ה-29 hugo runs נכנסים ל-cache של BuildKit. השני מקבל אותם CACHED ורץ רק את שלב ה-runtime (`COPY` + LABELs). במקביל — תחרות על משאבים בלי תועלת.

> **למה האותה פקודה לא מציינת `,src=`?** ה-default של `--secret id=NAME` ב-BuildKit הוא לקרוא מקובץ באותו שם ב-cwd. הקובץ `PRIVATE_ACCESS_TOKEN` מוגדר ב"דרישות" — לא נדרש `export` ולא `,src=` מפורש.

**זמן:** ~10-15 דק׳ build על Mac M-series + עד שעה+ push לDockerHub מאינטרנט ביתי.

#### השוואה בין האופציות

| | אופציה A (ענן) | אופציה B (מקומית) |
|---|------|------|
| היכן רץ | GitHub runners (ubuntu-24.04 amd64) | המחשב שלך |
| Parallelism | 29 ריצות hugo במקביל | רצף בתוך container |
| Build time | ~10-15 דק׳ | ~10-15 דק׳ |
| Push to DockerHub | ~2-5 דק׳ (network של Azure) | ~30 דק׳ עד שעה+ (אינטרנט ביתי) |
| **סה"כ wall-clock** | **~12-20 דק׳** | **~40-90 דק׳** |
| התערבות ידנית | אחת (לחיצה על Run) | להעקוב | 
| המחשב תפוס בזמן | לא | כן |
| קבצים מעורבים | `.github/workflows/airgap-build.yml` + `Dockerfile.runtime` | `Dockerfile` + `airgap-multibuild.sh` |

**המלצה:** אופציה A לעדכונים רגילים. אופציה B אם אין גישה ל-GitHub Actions, או לbuild שכולל שינויי Dockerfile/script שאתה בודק.

### מירור אתר השיווק של redis.io

הבלוג, המדריכים, סיפורי הלקוחות, ההשוואות, הפתרונות, עמודי הטכנולוגיה, מונחי המילון ודיאגרמות
הארכיטקטורה הם **אתר נפרד** מהתיעוד — גם ב-redis.io (‏Next.js + Sanity, מול Hugo של `/docs/`).
הם ממוררים **כפי ש-redis.io מרנדר אותם**, כדי שייראו בדיוק כמו שם, ו**מקובעים בגיט** כדי
שהבנייה לא תהיה תלויה ב-redis.io.

**איפה הם יושבים:** `mirror/site` הוא **submodule** של המאגר הפרטי
[`EliShteinman/redis-docs-mirror`](https://github.com/EliShteinman/redis-docs-mirror). המאגר הזה
שומר רק מצביע לגרסה שלו, כך ש-3.4GB של עמודים לא נכנסים להיסטוריה שלו ולא מגיעים לאף job
ב-CI — `actions/checkout` לא מוריד submodules כברירת מחדל. רק `4e` ו-`4f` מבקשים אותו, עם
ה-secret ‏`PRIVATE_ACCESS_TOKEN` — אותו PAT קלאסי (הרשאת `repo`) שמשמש את `make components`, ולכן
קורא גם את מאגר המירור. `persist-credentials: false` מוציא אותו מהגדרות ה-git של ה-job אחרי ה-checkout.

```bash
git submodule update --init mirror/site   # פעם אחת, לפני make mirror או בנייה מקומית של ה-image
make mirror          # רק מה שהשתנה, ואחריו llms.txt
make mirror-rewrite  # כללי השכתוב של היום על העמודים שבדיסק, בלי להוריד אף עמוד (שניות)
make mirror-full     # כל העמודים מחדש (~1,700, כ-15–35 דקות); כמעט אף פעם לא נחוץ. תמונות ו-chunks עדיין מהדיסק
make mirror-check    # מה redis.io מפרסם ועוד לא אצלנו, בלי לכתוב כלום
make llms            # רק llms.txt, בלי לרענן את המירור

# שני commits: התוכן במאגר המירור, והמצביע אליו כאן
git -C mirror/site add -A && git -C mirror/site commit -m "chore: sync with redis.io" && git -C mirror/site push
git add mirror/site && git commit -m "chore(mirror): sync with redis.io"
```

**ריצה רגילה מורידה רק מה שהשתנה.** ה-sitemap של redis.io נותן לכל עמוד `lastmod`;
`mirror/site/manifest.json` זוכר את התאריך של כל עמוד מהריצה הקודמת, ועמוד שהתאריך שלו לא זז
נלקח מהדיסק. נכסים (chunks של Next.js ותמונות Sanity) נקראים לפי התוכן שלהם, ולכן **נכס שכבר
בדיסק לא יורד שוב אף פעם**. מה שנלקח מהדיסק מקושר (hard link), לא מועתק.

**שינוי בכללי השכתוב לא דורש הורדה.** עמוד שנלקח מהדיסק עובר את הכללים של היום (`rewrite_again`), וכך
גם chunks (`JS_PATCHES`). שינוי ב-`rewrite.py`, `settings.py` או `JS_PATCHES` → `make mirror-rewrite`.

**השלד של redis.io** — header ו-footer — חלק מכל עמוד, אבל לא מוצג: `docs-frame.js` מציג במקומו את
הכותרת והפוטר של התיעוד. לכן שינוי שלהם אצל redis.io לא מצריך הורדה מחדש.

הריצה כותבת לתיקייה זמנית ומחליפה את `mirror/site` רק אם הצליחה (עד 2% עמודים שנכשלו).

**עמוד שעבר מקום:** כתובת ב-sitemap ש-redis.io מפנה לעמוד אחר (למשל מדריכים שהופנו
ל-`/partners/aws/`) לא נשמרת — הריצה מדווחת עליה כ-moved ולא כותבת את גוף העמוד האחר תחת
הכתובת הלא נכונה. אותו דבר ל-`.md` שמפנה ל-HTML.

**מה נכלל:** רשימת העמודים היא ה-sitemap של redis.io, מסונן לסקשנים ב-`settings.SECTIONS`.
לכל עמוד: ה-HTML, ה-Markdown שלו (`<path>.md` — הכפתור "View as Markdown" והחיפוש), כל
ה-chunks של Next.js שהוא טוען (כולל כאלה שנטענים בזמן ריצה), ה-CSS, הפונטים והתמונות מ-Sanity.

**מה משתנה בדרך** (`build/marketing_mirror/rewrite.py`, `settings.py`):
- תמונות מ-`cdn.sanity.io` עוברות ל-`/sanity/...` מקומי.
- iframes: גרף סטטי מהוסט שב-`settings.LOCAL_EMBEDS` (גרפי ה-benchmark ב-S3) נשמר יחד עם הקבצים
  שהוא טוען, כולל ספרייה מ-CDN, ומוגש מ-`/_mirror/embeds/...` (`embeds.py`). כל iframe אחר הוא נגן
  (YouTube, פודקאסט, מצגת) שהמדיה שלו לא זמינה ברשת סגורה, והוא מציג את
  `/_mirror/embed-unavailable.html` — גם ב-HTML וגם ב-payload של Next.js. ה-CSP מתיר iframe מאותו דומיין בלבד.
- תגיות GTM, trustarc, Segment ו-Cloudflare Insights מוסרות, וגם רכיבי המעקב שה-layout של redis.io מרנדר מתוך
  ה-payload של Next.js (`settings.TRACKING_ELEMENTS`: GTM, Segment, Amplitude, TrustArc ופיקסלים) — כך שהדף לא
  מנסה לפנות אליהם בכלל. מחרוזת payload משתנה רק אם היא נקראת חזרה בדיוק כפי ש-Next.js כתב אותה.
  ‏chunks של Next.js מוגשים עם `no-cache` (בדיקה מול השרת, 304), כי `JS_PATCHES` משנה תוכן בלי לשנות שם. ונוספים שלושה סקריפטים: `/js/runtime-config.js` (המתג של
  Helm), `/_mirror/marketing-links.js` ו-`/_mirror/docs-frame.js` — שמסתיר מראש את הכותרת והפוטר של
  redis.io ומציג במקומם את אלה של התיעוד (נקראים מדף הבית, ב-shadow root). כפתור החיפוש מוביל ל-`/#search`.
- שלושה תיקונים ב-JS: next/image טוען תמונות ישירות (אין כאן שרת אופטימיזציה), ובונה ה-URL של
  Sanity פונה ל-`/sanity`. **אם redis.io ישנו את ה-JS כך שתיקון לא מתאים לכלום, הריצה נכשלת**
  ולא שומרת עמודים שבורים — וזה המקום לעדכן.

**מה נשאר בחוץ בזמן ריצה:** ה-JS של redis.io טוען בעצמו analytics, באנר עוגיות וצ'אט. ה-pod
מגיש את העמודים עם Content-Security-Policy שמתיר רק את אותו דומיין, כך ששום דבר מזה לא נטען.

**קישורים** (`build/marketing_mirror/runtime/marketing-links.js`): `/docs/latest/...` הופך
לנתיב המקומי של התיעוד, סקשן ממורר נשאר, וכל השאר יוצא מהאתר. המתג `marketing-offsite` בקטלוג
הקישורים החיצוניים קובע מה קורה ליוצאים: כבוי — מוסתרים בתפריטים, ב-footer ובכפתורים, והופכים
לטקסט רגיל בתוך פסקאות.

**`/glossary/`** הוא המילון של התיעוד; המונחים שמתחתיו (`/glossary/<term>/`) מגיעים מהמירור.

**רשימות הבלוג** (`feeds.py`): עמוד הבלוג, כל קטגוריה וכל מחבר מציגים 21 פוסטים וטוענים את
השאר בגלילה מ-`/api/blog/feed`, `/api/blog/category` ו-`/api/blog/author`. כל batch נשמר כקובץ
ב-`_feed/<רשימה>/<start>.json`, וה-nginx של ה-pod עונה לפי `start`. הן יורדות במקביל, ונלקחות
מהדיסק כשאף עמוד לא השתנה.

**חיפוש:** `mirror/site/mirror.ndjson`, באותו מבנה של הפיד של התיעוד (כולל `sections`, שממנו
שירות החיפוש מאנדקס). הטקסט הוא ה-Markdown של העמוד, ובסקשנים ש-redis.io לא מפרסם להם Markdown
(השוואות, לקוחות, טכנולוגיה, דיאגרמות) — הטקסט מתוך ה-HTML (`page_text.py`: רק `<main>` ובלוקי
ה-streaming, בלי header ו-footer). עמודי רשימה לא מאונדקסים. בחלון החיפוש: קבוצות **Blog**,
**Tutorials** ו-**More from Redis**, וה-docs תמיד ראשונים (`search.index.mirrorWeight` קובע כמה
עמודי מירור נכנסים לתוצאות).

**חיפוש בתוך הבלוג** (`blog_search.py`): תיבת החיפוש של הבלוג שולחת ל-`/blog/search/?s=...`,
עמוד ש-redis.io בונה בשרת לכל שאילתה. כאן זה עמוד הבלוג בלי ה-scripts של Next.js, ש-
`runtime/blog-search.js` ממלא משירות החיפוש (`source=blog`) בשורות באותו עיצוב, עם תאריך, קטגוריה
ומחברים מ-`_mirror/blog-posts.json`. ה-chart מפנה את `/en/...` של redis.io לנתיב בלי הקידומת.

**ניווט:** `layouts/partials/more-from-redis-menu.html` מוסיף ל-header העליון תפריט נפתח
"More from Redis" עם כל הסקשנים הממוררים. הסרגל הצדדי (`docs-nav.html`) נשאר זהה ל-upstream.
ה-partial נפרד וההוספה ל-`header.html` היא **שורה אחת**, כדי לצמצם התנגשות במיזוג upstream.
בלי קונטיינר ה-mirror, ה-runtime config מסיר את התפריט.

**קישורים ישנים בתיעוד (`build/doc_links.json`):** כתובות תיעוד ישנות — ‏`/docs/<מבנה ישן>/`
ו-`/topics/<עמוד>` — שעברו שתי רה-ארגונים; רק רדיס יודעת לאן, ולכן כל כתובת **נצפית** פעם אחת
ונרשמת במפה, והבנייה מפנה אותן לעמוד המקומי בלי רשת.

```bash
python3 -m build.doc_links --refresh   # דורש אינטרנט; לרענן ולקבע את המפה
python3 -m build.doc_links             # מה שהבנייה מריצה, בלי רשת
```

**‏`/llms.txt` (`static/llms.txt`, `static/llms-docs.txt`):** האינדקס לסוכני AI נכתב מה-llms.txt של
redis.io, באותה שיטה: `make llms` (דורש אינטרנט) מוריד אותו פעם אחת, משאיר רק קישורים שהאתר הזה
עונה עליהם, ושומר שני קבצים שנכנסים ל-commit. קישור לעמוד תיעוד שזז נבדק ב-redis.io לאן הוא מפנה,
ו-alias מוחלף בעמוד שהוא מפנה אליו. `llms.txt` כולל גם את הקטעים הממוררים ואת `/mirror.ndjson`;
‏`llms-docs.txt` בלעדיהם, ו-nginx מגיש אותו ב-`/llms.txt` כשהמירור כבוי. הקישורים כתובים עם
‏`__DOCS_BASE_URL__`, ש-nginx ממלא בזמן הבקשה. `make mirror` ו-`make mirror-full` מריצים אותו בסוף,
כי הוא בודק מה יש בדיסק של המירור; את `static/llms.txt` ו-`static/llms-docs.txt` מכניסים ל-commit
יחד עם המצביע של המירור.

**‏`/mirror.ndjson`:** העמודים הממוררים כפיד אחד, באותו מבנה כמו `/docs.ndjson`. הקובץ נמצא ב-image
של המירור, ו-nginx של האתר מעביר אליו את הבקשה (רק כש-`mirror.enabled`).

**פער מול המקור:** ה-job ‏`4e. Mirror drift report` מריץ `make mirror-check` ומדווח ב-summary,
בלי להכשיל כלום. הוא **כבוי כברירת מחדל** — הוא פונה ל-redis.io — ורץ רק כשמסמנים את
`mirror_drift` בהפעלת ה-workflow. **ה-CI אף פעם לא מוריד תוכן מ-redis.io**; זה קורה רק ב-`make mirror`
ידני. גם ה-image של המירור הוא כפתור (`mirror_image`, מסומן כברירת מחדל), ובלעדיו
`publish_chart` לא רץ, כי ה-chart מפרסם את ה-tag של המירור. גם `publish_chart` מסומן כברירת מחדל:
הרצה בלי לשנות כלום בטופס נותנת מוצר שלם — כל ה-images ו-chart שמצביע עליהם.

#### התיאורים ב-Docker Hub

הטקסט שמופיע בעמוד של כל image ב-Docker Hub נשמר ברפו, ב-`.github/dockerhub/<repo>.md`.
השורה הראשונה בכל קובץ היא `<!-- short: ... -->` והיא התקציר שמופיע בחיפוש; כל השאר הוא
גוף העמוד. התקציר מוגבל ל-100 תווים (מגבלה של Docker Hub) ובלי פסיקים (הוא נכנס גם ל-label של ה-image).
ה-job בודק את כל הקבצים לפני שהוא שולח משהו.

ה-job ‏`4d. Docker Hub descriptions` משווה כל קובץ לתיאור החי ומעדכן **רק אם יש הבדל** —
כלומר הטקסט זז רק כשעורכים את הקובץ. הוא רץ **רק מהבראנץ `feature/docker-support`**:
שני הבראנצ'ים דוחפים לאותם repositories, והתיאור שייך ל-repository ולא לתג.

> **ה-token של Docker Hub צריך הרשאת כתיבה** כדי לשנות תיאור. אם אין לו, רק ה-job הזה
> ייכשל — שום דבר אחר לא תלוי בו.

#### ה-image של המירור

‏`mirror/site` נארז כמו שהוא — אין כאן Hugo. ה-Dockerfile מעתיק את התמונות (`sanity/`) ואת
ה-chunks (`_next/`) בשכבות נפרדות מתחת לעמודים, כי הם משתנים לאט יותר. ה-nginx של ה-pod
(`build/marketing_mirror/runtime/nginx.conf`) מוסיף את ה-CSP ודוחס בזמן אמת.

**העמודים עצמם** (1,705 קבצי HTML, ‏2.5 GB) נכנסים ל-image כארכיון אחד, `mirror-pages.tar.zst`
(‏zstd ‏`-19 --long=25`, כ-13 MB). gzip לכל קובץ לחוד הגיע ל-650 MB, כי הוא לא רואה את החזרות
בין העמודים. כשהקונטיינר עולה, `build/marketing_mirror/runtime/05-unpack-mirror-pages.sh` פורס
אותם ל-`/usr/share/nginx/pages` (פחות משנייה, 37 MB זיכרון) ורק אז nginx עולה. ב-chart זה
emptyDir בשם `mirror-pages`, כלומר כ-2.5 GB של ephemeral storage לכל pod. כל קובץ שאינו
עמוד (`mirror.ndjson`, ‏`_feed/`, ‏`manifest.json`) נשאר קובץ רגיל ב-image.

```bash
docker buildx build --platform linux/amd64,linux/arm64 --target mirror-unprivileged \
  -t redis-docs-mirror:local .
```

ב-CI זה ה-job ‏`4f. Mirror image (build if changed)`. הוא לא מחכה לבניית האתר. קודם הוא מחשב את התג
`<MIRROR>` (מה-commit של `mirror/site` בעץ, בלי להוריד את ה-submodule) ובודק ב-Docker Hub אם התג כבר קיים
עם כל הפלטפורמות. אם כן — לא בונה, ורק מזיז את `latest` / `unprivileged` אליו אם צריך. אם לא — מוריד את
`mirror/site` ודוחף ל-`a0533057932/redis-docs-mirror` בתגים `<MIRROR>` ו-`<MIRROR>-unprivileged` (וגם
`latest` / `unprivileged`). ב-chart: `mirror.enabled`.

#### ה-images של ה-CLI ושל החיפוש (`redis-docs-cli`, `redis-docs-search`) — נבנים אוטומטית ב-`airgap-build.yml`

שני images נפרדים, כל אחד לשירות אחד:

| image | מקור | שירות | פורט |
|---|---|---|---|
| `redis-docs-cli` | `helm/cli-proxy/` | ה-proxy של ה-CLI playground (`main:app`) | 8090 |
| `redis-docs-search` | `helm/search/` | שירות החיפוש בדוקס (`search.main:app`) | 8091 |

`helm/common/resp.py` — לקוח ה-RESP ששניהם משתמשים בו — יושב פעם אחת ונכנס לשניהם. לכן
שני ה-`Dockerfile` נבנים מ-`helm/` (‏`-f cli-proxy/Dockerfile` / `-f search/Dockerfile`),
והבדיקות מוצאות אותו דרך `helm/pytest.ini`.

ה-jobs ‏`4b. CLI image` ו-`4b. Search image` רצים בכל הרצה של `airgap-build.yml`, במקביל לבניית
האתר. שניהם מריצים את אותה לוגיקה, ב-`.github/actions/service-image`:

1. מחשב hash של כל הקבצים במקור שלו ובתוספת `helm/common/`, חוץ מקבצי הבדיקות
   (`test_*.py`), שלא נכנסים ל-image.
2. מתחיל מהתג שב-`values.yaml` (‏`cli.image.tag` / `search.image.tag`) ובודק ב-Docker Hub:
   תג שקיים ומכיל את אותו hash (label ‏`redis-docs.<cli|search>.source-hash`) — נשאר, לא
   בונים. תג שקיים עם קוד אחר — עולים ב-patch (‏`0.6.0 → 0.6.1`) ובודקים שוב. תג פנוי —
   מריצים את הבדיקות, בונים amd64+arm64 ודוחפים אותו ואת `latest`.
3. עם `publish_chart`, שלב 5 מעדכן כל תג שהשתנה ב-`values.yaml`, בדוגמה
   `values-openshift-airgapped.yaml` וב-README-ים, ומפרסם את הצ'ארט.

אחרי הדחיפה כל job מוודא שה-image באמת עולה: מריץ בתוכו ייבוא של השירות, בשתי הארכיטקטורות.
זה תופס מודול שנוסף למקור ולא נוסף לרשימת ה-`COPY` שב-`Dockerfile` — הבדיקות רצות על הקוד
שברפו ולא רואות את זה.

כל image נושא גם את התיאור הקצר שלו — השורה הראשונה של `.github/dockerhub/<repository>.md`
— כ-label ‏`org.opencontainers.image.description`, וגם `org.opencontainers.image.version`. כך
כל גרסה שומרת את התיאור שהיה בזמן שנבנתה, גם אחרי שעמוד ה-repository ב-Docker Hub מתעדכן:

```bash
docker buildx imagetools inspect a0533057932/redis-docs-search:0.1.0 \
  --format '{{json .Image}}' | jq '.["linux/amd64"].config.Labels'
```

ה-job ‏`4c. Fork tests` רץ במקביל ומריץ את כל בדיקות הפורק (‏`helm/cli-proxy` כולל
`test_acl.py`, `helm/search` ו-`build/`). הוא לא עוצר את בניית ה-image-ים, אבל בלעדיו שלב 5
לא מפרסם chart. שלושה חריגים: `build/jupyterize` (דורש `nbformat` שאף קובץ requirements ברפו
לא מכריז עליו), `test_every_product_is_offered` (‏Radar חסר ב-`data/doc_bundles.json` של רדיס
עצמה, נכשל גם על main שלהם) ו-`build/test_cmd_tools.py` (‏#4107 של רדיס הסיר את
`FILTER_PREFIXES` מ-`cmd_tools.py` ולא מהבדיקה, שנכשלת בייבוא גם על main שלהם).

תג שפורסם אף פעם לא נדרס. הרצה שבנתה image בלי `publish_chart` לא משאירה עבודה: ההרצה
הבאה מוצאת את התג עם אותו hash ומפנה אליו את הצ'ארט. הרצת בדיקה עם `tag_override` דוחפת
כל אחד מהם רק תחת תג ה-override, בלי `latest` ובלי לגעת ברצף הגרסאות.

> **בנייה ידנית — לבדיקה מקומית בלבד.** לא לדחוף ידנית תג גרסה (`X.Y.Z`) או `latest`:
> image בלי ה-label ייראה ל-CI כקוד אחר, והוא יעלה גרסה סביבו.
>
> ```bash
> python3 -m pytest helm/cli-proxy helm/search -q
> docker buildx build --platform linux/amd64,linux/arm64 -f helm/cli-proxy/Dockerfile -t redis-docs-cli:local helm
> docker buildx build --platform linux/amd64,linux/arm64 -f helm/search/Dockerfile -t redis-docs-search:local helm
> ```
>
> `airgap-multibuild.sh` בונה רק את האתר ולא דוחף כלום, אז אין מה לשקף בו.

> **ה-image של Redis** (`redis:8.10.0-alpine`) משרת גם את ה-playground וגם את החיפוש —
> אותו image, שני פודים. אין מה לבנות; רק לוודא שהוא ממורר.

### שלב 4 — אימות deployment

```bash
# התקנה נקייה (כדי לוודא שהתמונה החדשה באמת עולה):
helm uninstall redis-docs -n redis-docs
helm install redis-docs ./helm/redis-docs -n redis-docs --set route.enabled=true

# (לחלופין, אם רק רוצים להחליף תמונה ב-deployment קיים:)
# helm upgrade redis-docs ./helm/redis-docs -n redis-docs --reuse-values

oc get pods,route -n redis-docs
```

בדיקות בדפדפן:
1. דף בית — לוגו ולינקים פנימיים עובדים
2. `/operate/kubernetes/` — דרופ-דאון גרסאות מופיע, התפריט נקי (בלי תיקיות גרסה)
3. `/operate/kubernetes/7.8.6/` — הכפתור מציג `v7.8.6 ▼`, התפריט מחליף לתוכן הגרסה
4. עמוד גרסה ישנה — באנר עם קישור יחסי ל-`/operate/.../`, לא ל-`redis.io/...`

### שלב 5 — עדכון Helm chart

לפי היקף השינויים מאז הגרסה הקודמת של ה-chart:

| מקרה | bump | פעולה |
|---|---|---|
| **תוכן upstream בלבד** (זה הרגיל) | patch (`1.1.0 → 1.1.1`) | עדכון `appVersion`, עדכון tag בדוגמאות |
| **תיקון/הוספה קטנה ב-airgap-multibuild.sh, ב-Dockerfile, ב-Dockerfile.runtime או ב-`.github/workflows/airgap-build.yml`** | minor (`1.1.0 → 1.2.0`) | אותו דבר |
| **שינוי במבנה ה-chart** (כניסה חדשה ל-catalog, configmap חדש, default values משופרים) | minor או major | + עיון בכל ה-templates שהתעדכנו |
| **שינוי breaking** (שיניתי `values.yaml` באופן שלא תואם לאחור) | major (`1.x → 2.0.0`) | + הערת migration ב-CHANGELOG |

קבצים לעדכן (4 בכל מקרה):
- `helm/redis-docs/Chart.yaml` — `version` (לפי הטבלה), `appVersion` (להחליף ל-HASH החדש), ורשימת
  `artifacthub.io/images` תחת `annotations` (כל image עם התג המקובע שלו; למירור — `<MIRROR>-unprivileged`)
- `helm/redis-docs/README.md` — דוגמת `tag:` ושם הקובץ `redis-docs-X.Y.Z.tgz` בפקודות ההתקנה
- `helm/redis-docs/README-he.md` — אותו דבר
- `helm/redis-docs/examples/values-openshift-airgapped.yaml` — `tag:` + ההערה למעלה, ו-`tag:` של המירור
  (התג שלו, `<MIRROR>-unprivileged`, לא ה-HASH של האתר)

```bash
git add helm/
git commit -m "chore(helm): bump chart X.Y.Z, appVersion ${HASH}"

# רענון מטא של ה-release (Pods לא נופלים אם templates זהים):
helm upgrade redis-docs ./helm/redis-docs -n redis-docs --reuse-values
```

### שלב 6 — פרסום ה-chart ל-OCI registry

מאז Helm 3.8, helm charts יכולים להיות מאוחסנים כ-OCI artifacts באותו registry שבו נמצאות תמונות Docker. ב-Docker Hub זה תומך מיידית — ה-chart ייגש לאותו account שבו ה-image (`a0533057932/redis-docs`), עם MediaType שונה אז אין התנגשות עם תגי image.

```bash
# אריזה של ה-chart ל-tgz (גרסת tar gzipped):
helm package helm/redis-docs/

# דחיפה ל-Docker Hub כ-OCI artifact:
helm push redis-docs-X.Y.Z.tgz oci://registry-1.docker.io/a0533057932

# ניקוי הקובץ המקומי (gitignored כבר):
rm redis-docs-*.tgz
```

לאימות שהדחיפה הצליחה:
```bash
helm show chart oci://registry-1.docker.io/a0533057932/redis-docs --version X.Y.Z | head
```

**לקוחות יכולים להתקין ישירות ב-pipeline אחד**, בלי לקלון את הריפו:
```bash
helm install my-deploy oci://registry-1.docker.io/a0533057932/redis-docs --version X.Y.Z \
  --set route.enabled=true
```

---

## בנייה

ראו "תהליך עדכון מקצה לקצה" — שלב 3 לפקודות (אופציה A לענן, אופציה B מקומית).

## מה הבנייה עושה (אופציה B — מקומית, ע"ב Dockerfile)

> אופציה A (GHA) עושה את **אותו דבר לוגית** אבל מפצלת ל-jobs מקבילים — phase 1 setup → phase 2 הוא 29 ריצות Hugo במקביל → phase 3 assemble → phase 4 nginx+push. ראה `.github/workflows/airgap-build.yml`.



1. **Builder stage** (משותף לשני ה-variants ולשתי הארכיטקטורות):
   - Base image: `node:24-trixie` (Node 24 + Python 3.13)
   - **רץ תמיד native על host platform** — ראו פרק "Builder native via BUILDPLATFORM" למטה
   - התקנת Hugo 0.143.1
   - התקנת dependencies (npm + pip)
   - שינוי `baseURL` ל-`"/"` (תמיכה בכל דומיין)
   - הרצת `make components` (שליפת דוגמאות מ-repos חיצוניים)
   - הרצת `airgap-multibuild.sh` — N+1 בילדי Hugo נפרדים: latest + אחד לכל גרסה. ראו פרק נפרד בהמשך.
   - דחיסת gzip מראש לכל הקבצים הסטטיים

2. **Runtime stage** (לפי VARIANT, רץ native לפי target platform):
   - `privileged`: `nginx:alpine` על פורט 80
   - `unprivileged`: `nginx-unprivileged:alpine` על פורט 8080 (non-root)
   - `COPY --from=builder /site/public /usr/share/nginx/html` + LABELs
   - `apk add python3` (13.5MB, stdlib בלבד) + העתקת `build/make_doc_bundles.py`
     ו-`data/doc_bundles.json` ל-`/opt/redis-docs/` — ראו פרק "חבילות ההורדה" למטה

### חבילות ההורדה (`downloads`)

הכפתור "Download documentation" בכל עמוד מציע כל מוצר כ-`.tar.gz` ב-Markdown,
HTML או JSON. upstream בונה את הארכיונים ב-CI ומגיש אותם מ-bucket; בפורק הם
**נארזים ב-init container בעליית הפוד**.

הסיבה: הארכיונים מכילים לינקים אבסולוטיים, ולכן הם נכונים רק אחרי שכתובת האתר
ידועה — וזו נקבעת ב-`helm install`, לא בבניית ה-image. אריזה מראש הייתה צורבת
את הכתובת הלא נכונה, ומוסיפה ~280MB לכל שכבה.

מה שהבנייה חייבת לספק ל-image כדי שזה יעבוד:

| רכיב | למה |
|---|---|
| `python3` | הפאקר הוא סקריפט Python (stdlib בלבד — בלי pip, בלי venv) |
| `/opt/redis-docs/build/make_doc_bundles.py` | הפאקר עצמו |
| `/opt/redis-docs/data/doc_bundles.json` | קטלוג המוצרים והפורמטים; הפאקר מוצא אותו בנתיב ברירת המחדל בזכות מבנה הספריות |

> **ב-`airgap-build.yml` שני הקבצים האלה חייבים להופיע ב-`sparse-checkout` של
> job ה-docker.** אותו job מושך רק את מה שהוא מפרט במפורש, ובלעדיהם ה-`COPY`
> נכשל. `airgap-multibuild.sh` לא בונה image ולכן לא מושפע.

**מדידה** (272MB, כל 4 הפורמטים, ליבה אחת): 148 שניות. פורמט `html` הוא ~89%
מהמשקל ומהזמן; `downloads.formats: "md,md-single,json"` מוריד ל-~30MB ולשניות.

תיקון צד-פורק בפאקר: Hugo כותב את הטוקן `__DOCS_BASE_URL__` לתוך פלטי ה-`.md`
וה-`.json`, ובאתר חי nginx מחליף אותו בכל בקשה. הפאקר קורא מהדיסק — nginx אף
פעם לא רץ — ולכן הטוקן היה נארז כמו שהוא. ההחלפה קורית עכשיו בזמן האריזה, מול
אותו `--url-base`.

### Builder native via `BUILDPLATFORM`

ה-builder stage מכריז `FROM --platform=$BUILDPLATFORM node:24-trixie AS builder`. זה כופה את ה-stage לרוץ על הארכיטקטורה של ה-host (arm64 על Mac M-class, amd64 על runner intel).

**למה זה חיוני:**

ה-builder מריץ ~26 קריאות Hugo, npm install, pip install, ו-make components. **הפלט שלו (`/site/public`) הוא HTML/CSS/JS — בייט-אידנטי בכל ארכיטקטורה.** לא היה שום טעם להריץ את כל הצינור פעמיים בבילד multi-arch (פעם native ופעם תחת QEMU emulation).

**לפני התיקון** (Dockerfile ללא `--platform=$BUILDPLATFORM`): multi-arch על Mac arm64 לקח ~85-100 דק כי amd64 רץ תחת QEMU emulation, וכל קריאת hugo הייתה איטית פי 6-9.

**אחרי התיקון**: ~14 דק. ה-builder רץ native פעם אחת, שני ה-runtime stages (`linux/arm64` ו-`linux/amd64`) משתמשים באותו `COPY --from=builder`.

**שימוש ב-`BUILDARCH` במקום `TARGETARCH`** להורדת Hugo binary: ה-Hugo רץ ב-builder, אז ה-binary צריך להתאים ל-host's arch, לא ל-target.

## פיפליין הבילד הרב-גרסתי (`airgap-multibuild.sh`)

הסקריפט בשורש הריפו, נקרא מ-Dockerfile בתוך builder stage. הוא משכפל את ההתנהגות של `.github/workflows/main.yml` של redis (matrix build לכל גרסה) — אבל ברצף בתוך container אחד, לא מקבילית ב-N runners.

### למה צריך פיפליין מיוחד

ב-redis.io כל גרסה ארכיונית (`/docs/latest/operate/kubernetes/7.8.6/...` למשל) מוגשת מבילד נפרד שבו תוכן הגרסה הוא **כל המוצר** (לא תת-תיקייה). זה גורם לכך שהניווט הצדדי בעמוד של 7.8.6 מציג את ה-children של הגרסה ישירות תחת "Redis for Kubernetes", בלי שכבת היררכיה נוספת של "7.8.6". בלי הפיפליין הזה, בילד יחיד של Hugo יציג גם את children של latest וגם את הגרסה כפריט-בן עם children מקוננים — UX מבולבל.

### זרימה

1. **`make components`** רץ פעם אחת (יקר, מסונכרן עם clones חיצוניים).
2. **תיקוני source חד-פעמיים** לפני snapshot:
   - הרפיית ה-regex של בורר הגרסה ב-`layouts/partials/scripts.html` כך שיוצג בכל baseURL (ולא רק `/docs/latest/`).
   - הסרה של `https://redis.io/docs/latest/` ושל הטקסט-של-קישור `redis.io/docs/latest/` מכל קבצי `content/*.md` (~150 קבצים), כך שלינקים markdown הופכים ליחסיים.
3. **Snapshot** של ה-workspace — נקודת ייחוס ש-`reset_workspace` חוזר אליה לפני כל בילד.
4. **גילוי גרסאות** דינמי מתוך `content/operate/kubernetes`, `content/operate/rs`, `content/develop/ai/redisvl`. גרסה חדשה ש-redis יוסיפו ב-upstream נתפסת אוטומטית.
5. **בילד "latest"** — מוחקים את כל תיקיות הגרסה מ-content, רצים hugo, פלט נכנס ל-`$FINAL`.
6. **בילד לכל (מוצר, גרסה)**:
   - `reset_workspace` (שחזור משלב 3)
   - מוחקים את שאר הגרסאות של אותו מוצר
   - awk מסיר את ה-prefix של הגרסה מ-`relref`-ים ומקישורי `](/content/<product>/<version>/` בתוך תוכן הגרסה
   - `rsync -a --delete-after content/<product>/<version>/ content/<product>/` — דורסים את התוכן הראשי של המוצר בתוכן של הגרסה
   - `sed` מחזיר `linkTitle` ב-`_index.md` של ההורה לתווית המוצר ("Redis for Kubernetes" וכו')
   - `sed` משנה את תווית כפתור הדרופ-דאון מ-"latest" ל-"v<version>"
   - inject ל-`meta-links.html` שמתקן את "Edit on GitHub" כך שיצביע לתיקיית הגרסה
   - hugo
   - **בדיקת קישורים:** קישור ש-Hugo לא מצא יוצא כ-`href="/content/..."`, שהוא 404. הבנייה נכשלת רק על
     קישור לגרסה עצמה (`/content/<product>/<version>/`), כי זה הסימן שהסרת ה-prefix לא עבדה. שאר
     הקישורים כאלה הם באגים בתוכן של Redis, שבורים גם ב-redis.io (issue ‏redis/docs#4155), ומודפסים
     כאזהרה בלבד
   - `rm -rf` היעד ב-`$FINAL/<product>/<version>` (חיוני — ראו "מלכודת aliases" למטה) ואז `cp -a` של תת-העץ לשם
7. **`mv $FINAL /site/public`** — מאחדים.
8. **`python3 build/generate_ndjson.py`** + gzip על התוצאה הסופית.

### מלכודת aliases

קובצי `_index.md` של תוכן latest לפעמים כוללים aliases לגרסאות ישנות, למשל ב-`content/operate/rs/monitoring/_index.md`:
```
aliases: [/operate/rs/clusters/monitoring/, /operate/rs/7.4/clusters/monitoring/]
```
בבילד latest, Hugo מייצר HTML של redirect במסלול ה-alias המלא — כולל `public/operate/rs/7.4/clusters/monitoring/`. בעת מיזוג, היעד `$FINAL/operate/rs/7.4/` כבר קיים מ-redirect הזה. בלי `rm -rf` לפני `cp -a`, ה-`cp` היה מקנן את עץ הגרסה (`$FINAL/operate/rs/7.4/7.4/index.html`) ו-nginx היה מחזיר 403 על `/operate/rs/7.4/`.

הפתרון בסקריפט: `rm -rf "$FINAL/$product_path/$version"` לפני ה-`cp -a`. תוכן הגרסה דורס לחלוטין כל artifact של alias מ-latest.

### עלויות

- **זמן wall-clock** (Mac M-class):
  - arm64-only: ~10-12 דק
  - multi-arch (amd64+arm64) **אחרי תיקון BUILDPLATFORM**: ~14 דק
  - variant שני ברצף אחרי הראשון: ~3-5 דק (cache מלא של builder stage)
  - ב-CI של redis המקבילי: ~5-10 דק בזכות N runners
- **disk peak**: snapshot (~2GB) + `$SITE/public` הנוכחי (~1.3GB) + `$FINAL` המצטבר (גדל עד ~1.3GB) ≈ ~5-7GB בתוך ה-container.
- **גודל image סופי**: ~1.5-2GB (כל הגרסאות בתוך אותו image).

### גרסה חדשה ב-upstream

כל מה שצריך לעשות אחרי `git pull origin main`: לבנות Docker מחדש. הסקריפט מגלה תיקיות גרסה חדשות אוטומטית. אין שום הגדרה ידנית לעדכן.

## הבדלים מול CI של Redis

| | CI (redis.io) | Docker airgap |
|---|---|---|
| baseURL | `/docs/latest` | `/` |
| בילדי גרסאות | מקבילית ב-N runners | רצף בתוך container אחד (`airgap-multibuild.sh`) |
| מיזוג | rsync ל-GCS לכל גרסה בנפרד | `cp -a` ל-`$FINAL` ו-`mv` בסוף |
| Multi-arch | runner נפרד לכל arch | builder native על host דרך `BUILDPLATFORM`; runtime לפי target |
| Cache בין variants | אין (כל variant build נפרד) | builder stage cached, variant שני רץ ~3-5 דק |
| פלט | GCS bucket | nginx container |
| gzip | GCS עושה compression | `gzip_static` מראש |
| לינקים `redis.io/docs/latest/` | תקפים (זה ה-canonical) | מותקנים ל-`/` ב-build time |
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
| `mermaid.min.js` | v12.0.0 | cdn.jsdelivr.net | דיאגרמות (flowcharts, sequence) |
| `redoc.standalone.js` | v2.5.4 | cdn.redoc.ly | תצוגת OpenAPI/Swagger |
| `thebe.js` | 0.9.0-rc.12 | unpkg.com | הרצת קוד אינטראקטיבית (Jupyter) |
| `thebe.css` | 0.9.0-rc.12 | unpkg.com | עיצוב Thebe |
| `codemirror-javascript.js` | 5.65.16 | unpkg.com | מצב הדגשת תחביר JavaScript ל-Thebe (mode/javascript/javascript.js) |
| `codemirror-ruby.js` | 5.65.16 | unpkg.com | מצב הדגשת תחביר Ruby ל-Thebe (mode/ruby/ruby.js) |
| `codemirror-clike.js` | 5.65.16 | unpkg.com | מצב הדגשת תחביר C/C++/Java ל-Thebe (mode/clike/clike.js, MIME text/x-csrc) |

> לעדכון: הורידו את הגרסה החדשה מהמקור המקורי, החליפו את הקובץ ב-`static/vendor/`, ועדכנו טבלה זו.

### widget ה-redis-cli האינטראקטיבי (`cli.js` וונדר) — בדיקת drift חובה

מ-upstream PR #3642, הדוקס **לא מחזיקים יותר** את הקוד המלא של ה-widget: `static/js/cli.js`
הוא shim דק שטוען את הסקריפט הקנוני מה-backend ב-`https://redis.io/cli/static/js/cli.js`.
ב-airgap הכתובת הזו לא נגישה, לכן ה-fork **וונדר** את הסקריפט הקנוני ל-`static/cli-playground/assets/cli.js`,
ושלושת הצרכנים מצביעים אליו: ה-shim של הטרמינל המוטמע (`static/js/cli.js`), shell של הפלייגראונד
(`static/cli-playground/index.html`), ומ-upstream #3862 גם ה-workbench (`static/js/redis-workbench.js`).
כולם POST ל-`/cli` (ה-cli-proxy בקלאסטר).

ב-shim, upstream מחזיק קבוע יחיד (`REDIS_CLI_BACKEND`) שממנו נגזרים גם ה-API וגם כתובת הסקריפט,
כי אצלם זה אותו origin. ב-fork אלו שני נתיבים שונים בקלאסטר, לכן הוא מפוצל ל-`REDIS_CLI_API`
(`/cli`) ו-`REDIS_CLI_SCRIPT` (`/cli-playground/assets/cli.js`). מיזוג upstream שנוגע ב-shim
יחזיר את האיחוד — צריך לפצל שוב.

ה-workbench הוא הסיבה שה-drift מסוכן יותר מבעבר: הוא בנוי על `window.RedisCli`, API שרק
הסקריפט הקנוני מפרסם. עותק וונדר ישן שלא מכיר אותו לא יישבר ברעש — המגירה פשוט לא תיפתח.

מכיוון ש-upstream כבר לא עוקב אחרי הקובץ ב-git, **אין סיגנל PR/diff** כשרדיס מעדכנת אותו.
לכן **חובה, בכל בנייה מחדש של ה-image**, להריץ את בדיקת ה-drift:

```bash
python3 build/check_cli_js_drift.py
# exit 0 = תואם ל-redis.io  |  exit 1 = השתנה → לרה-וונדר ולסקור מחדש  |  exit 2 = לא ניתן למשוך (בדקו רשת)
```

> לרה-וונדור: `curl -s https://redis.io/cli/static/js/cli.js -o static/cli-playground/assets/cli.js`,
> להריץ שוב את הבדיקה עד exit 0, ולסקור את ה-diff לפני commit.

### ניתוב ה-"Try it" (`openTryItCli`) — נקודת תיקון אחת

כפתור ה-Try it בונה URL עם הפקודות ב-base64 ופותח אותו. ב-upstream הבסיס קשיח
(`https://redis.io/cli`); ב-fork הוא מגיע מ-`RUNTIME_CONFIG.cli.url` (Helm), ו-cli מכובה
הופך את הכפתור ל-no-op. בהיעדר `RUNTIME_CONFIG` נשמרת התנהגות upstream, כדי שבנייה ציבורית
תמשיך לעבוד.

**עד #3862 הלוגיקה הייתה משוכפלת בשני קבצים** (`layouts/partials/tabs/wrapper.html`
ו-`layouts/shortcodes/redis-cli.html`), ותיקון של אחד בלבד הדליף את כל עמודי הפקודות החוצה —
קרה בפועל אחרי upstream #3608. upstream איחד את שתיהן ל-partial אחד, ולכן היום:

| קובץ | מה מתוקן |
|---|---|
| `layouts/partials/tryit-script.html` | `cliBase` מ-`RUNTIME_CONFIG.cli.url` — **נקודת התיקון היחידה** |
| `layouts/partials/tabs/wrapper.html` | `updateAllTryItButtons` מסתיר את הכפתור כש-`cli.enabled=false`; `updateAllBinderLinks` |
| `layouts/_default/baseof.html` | `RESOLVED_BINDER_URL` קורא מ-`RUNTIME_CONFIG` |
| `layouts/shortcodes/jupyter-example.html` | משכתב כל `[data-binder-url]` ל-hub הפנימי |

**אימות אחרי כל מיזוג שנוגע באחד מהם:** לבנות מקומית (`hugo`), ואז לסרוק
`public/commands/**/*.html` — כל עמוד עם `onclick="openTryItCli(this)"` חייב להכיל `cliBase`,
ולא את המחרוזת `'https://redis.io/cli?commands='` כבסיס פעיל.

> `baseof.html` הוא המסוכן שבהם: הוא נוטה למזג **בלי קונפליקט** בעוד ההשמה של upstream
> ל-`config.binderOptions.binderUrl` דורסת בשקט תיקון שמוצב לפניה. לכן התיקון יושב על
> הגדרת הקבוע ולא על אתרי ההשמה.

## ניהול לינקים חיצוניים

האתר מכיל עשרות לינקים ל-`redis.io` — בדף הבית, בתפריט העליון, בתפריטי ה-dropdown ובפוטר. רוב הלינקים האלו לא יעבדו בפריסה airgap. הצ'ארט מספק מנגנון **היררכי** של חמש שכבות לניהול שלהם.

### מבנה היררכי

הקטלוג מסודר ב-**משפחות** וב-**תתי-משפחות**:

```
externalLinks.enabled                    ← master kill-switch
└── families
    ├── home                              ← קישורים בגוף עמוד הבית
    │   └── links: { sandbox, tutorials, ... }
    ├── header                            ← תפריט עליון
    │   └── sub-families
    │       ├── main-nav: { Docs }
    │       ├── cta: { Login, Sign up }
    │       ├── search: { search button }
    │       └── mobile: { hamburger + drawer }
    └── footer                            ← פוטר תחתון
        └── sub-families: { social, legal, compare, company,
                            cloud-partners, services }
```

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
    nav-try-redis:
      enabled: false          # חוץ מכפתור Sign up שדווקא יוסתר
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
- ה-`__DOCS_BASE_URL__` מוטמע **רק במקומות האלה**, וכל אחד מהם מטפל בהפניה פנימית שמצביעה על תוכן באתר. כתובות חיצוניות שמשתמש כתב ידנית ב-MD לא נוגעים בהן.
  - ‏`process-markdown-content.html`: שתיים ל-`relref`, שלוש ל-`image` (כולל תמונות Markdown מ-DOC-7128), ושלוש לקישורי Markdown בצורה `](/content/....md)` שנוספה ב-DOC-6909.
  - ‏`markdown-command-group.html`: שתיים לטבלאות הפקודות, שנכתבו אצל Redis עם `https://redis.io/commands/`.
  - ‏`static/llms.txt` ו-`static/llms-docs.txt`, שנכתבים עם ה-placeholder (ראו `make llms`). ל-`/llms.txt` יש location משלו עם אותו `sub_filter`.
- לוגו ה-header וה-footer מצביעים תמיד ל-`/` — לא תלויים ב-`canonicalURL`.
