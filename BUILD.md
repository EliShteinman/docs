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

כל שחרור מייצר **4 תגים** על **2 פלטפורמות** (linux/amd64 + linux/arm64):

| תג | Variant | פורט | שימוש |
|-----|---------|------|-------|
| `<HASH>` | privileged (nginx:alpine) | 80 | גרסה מתויגת — `docker run` |
| `latest` | privileged (nginx:alpine) | 80 | rolling tag — `docker run` |
| `<HASH>-unprivileged` | unprivileged (nginx-unprivileged) | 8080 | גרסה מתויגת — Kubernetes / OpenShift |
| `unprivileged` | unprivileged (nginx-unprivileged) | 8080 | rolling tag — Kubernetes / OpenShift |

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

שתי דרכים — בענן או מקומית. שתיהן מייצרות את אותם **4 תגים** ב-DockerHub.

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
- `helm/redis-docs/Chart.yaml` — `version` (לפי הטבלה) ו-`appVersion` (להחליף ל-HASH החדש)
- `helm/redis-docs/README.md` — דוגמת `tag:`
- `helm/redis-docs/README-he.md` — אותו דבר
- `helm/redis-docs/examples/values-openshift-airgapped.yaml` — `tag:` + ההערה למעלה

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
   - awk מסיר את ה-prefix של הגרסה מ-`relref`-ים בתוך תוכן הגרסה
   - `rsync -a --delete-after content/<product>/<version>/ content/<product>/` — דורסים את התוכן הראשי של המוצר בתוכן של הגרסה
   - `sed` מחזיר `linkTitle` ב-`_index.md` של ההורה לתווית המוצר ("Redis for Kubernetes" וכו')
   - `sed` משנה את תווית כפתור הדרופ-דאון מ-"latest" ל-"v<version>"
   - inject ל-`meta-links.html` שמתקן את "Edit on GitHub" כך שיצביע לתיקיית הגרסה
   - hugo
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
| `mermaid.min.js` | v11.16.0 | cdn.jsdelivr.net | דיאגרמות (flowcharts, sequence) |
| `redoc.standalone.js` | v2.5.3 | cdn.redoc.ly | תצוגת OpenAPI/Swagger |
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
ושני הצרכנים מצביעים אליו: ה-shim של הטרמינל המוטמע (`static/js/cli.js`) ו-shell של הפלייגראונד
(`static/cli-playground/index.html`). שניהם POST ל-`/cli` (ה-cli-proxy בקלאסטר).

מכיוון ש-upstream כבר לא עוקב אחרי הקובץ ב-git, **אין סיגנל PR/diff** כשרדיס מעדכנת אותו.
לכן **חובה, בכל בנייה מחדש של ה-image**, להריץ את בדיקת ה-drift:

```bash
python3 build/check_cli_js_drift.py
# exit 0 = תואם ל-redis.io  |  exit 1 = השתנה → לרה-וונדר ולסקור מחדש  |  exit 2 = לא ניתן למשוך (בדקו רשת)
```

> לרה-וונדור: `curl -s https://redis.io/cli/static/js/cli.js -o static/cli-playground/assets/cli.js`,
> להריץ שוב את הבדיקה עד exit 0, ולסקור את ה-diff לפני commit.

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
- ה-`__DOCS_BASE_URL__` מוטמע **רק על ידי 7 השורות** ב-`process-markdown-content.html`: שתיים ל-`relref`, שתיים ל-`image`, ושלוש לקישורי Markdown בצורה `](/content/....md)` שנוספה ב-DOC-6909. כל אחת מהן מטפלת בהפניה פנימית שמצביעה על תוכן באתר. כתובות חיצוניות שמשתמש כתב ידנית ב-MD לא נוגעים בהן.
- לוגו ה-header וה-footer מצביעים תמיד ל-`/` — לא תלויים ב-`canonicalURL`.
