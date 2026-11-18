# העתקת ה-repos של Redis מ-GitHub ל-GitLab פנימי

## מה זה עושה

התיעוד מכיל אלפי קישורים ל-GitHub: לקוד של Redis, לספריות הלקוח, לקבצי התקנה. ברשת סגורה (airgap) הדפדפן לא מגיע ל-GitHub, והקישורים האלה נשברים.

הפתרון מורכב משני חלקים:

1. **העתקה.** הכלי ב-`scripts/airgap-mirrors/` מעתיק את ה-repos מ-GitHub ל-GitLab הפנימי, דרך דיסק און קי.
2. **הפניה.** ה-Helm chart מחליף בדפדפן כל קישור ל-GitHub בקישור לעותק ב-GitLab.

## התמונה הכללית

```
 מחשב חיצוני (עם אינטרנט)        דיסק און קי          מחשב פנימי (ליד GitLab)
 ─────────────────────────        ───────────          ────────────────────────
 1. export   ──── תיקיית העברה ────────────────────►   2. import  → GitLab
 3. confirm  ◄─── receipt.json ─────────────────────   (נכתב אוטומטית ב-import)
```

סבב אחד נראה כך:

1. **export** (במחשב החיצוני): מוריד מ-GitHub רק את מה שהשתנה מאז הסבב הקודם, וכותב אותו לתיקיית ההעברה.
2. מעתיקים את תיקיית ההעברה לדיסק און קי, ומשם למחשב הפנימי.
3. **import** (במחשב הפנימי): טוען את התיקייה ל-GitLab, וכותב קובץ קבלה (`receipt.json`) שמפרט מה נטען.
4. מעתיקים את `receipt.json` חזרה למחשב החיצוני.
5. **confirm** (במחשב החיצוני): מסמן שהמצב הזה כבר נמצא ב-GitLab, כך שהסבב הבא יעביר רק את מה שבא אחריו.

**אם דיסק און קי הלך לאיבוד או ש-confirm לא רץ, לא קורה כלום רע.** ה-export הבא פשוט כולל שוב את כל מה שעוד לא אושר.

## מה עובר ומה לא

**עובר:**
- כל ה-branches וכל ה-tags.
- ה-branch הראשי (default branch), בדיוק כמו ב-GitHub.
- דפי ה-releases: הכותרת וההערות.
- קבצי ה-releases, לפי מדיניות שנקבעת לכל repo בנפרד.

**לא עובר:**
- Pull requests, issues, discussions, security advisories, wiki ו-Actions. הם לא חלק מ-git אלא מסד נתונים של GitHub, ולכן קישורים אליהם נשארים מצביעים ל-GitHub.

## איך ה-branch הראשי נשמר (main נשאר main)

ב-GitHub לכל repo יש branch ראשי. ב-`redis` למשל הוא נקרא `unstable`, לא `main`. אם דוחפים repo ל-project ריק ב-GitLab, GitLab בוחר branch ראשי לבד. לכן הכלי לא משאיר לו את הבחירה:

1. ב-export הכלי שואל את GitHub מה ה-branch הראשי, ורושם את התשובה בקובץ ה-manifest שעובר בדיסק און קי.
2. ב-import הכלי דוחף **קודם רק את ה-branch הראשי**, ומיד מגדיר אותו ב-GitLab כראשי.
3. רק אחרי זה הוא דוחף את כל שאר ה-branches וה-tags.

זה קורה בכל סבב, לא רק בפעם הראשונה. לכן אם Redis ישנו את ה-branch הראשי ב-GitHub, GitLab יתעדכן בסבב הבא. במקרה כזה הכלי גם מסיר את ההגנה מה-branch הראשי הישן, כדי שאפשר יהיה למחוק אותו כמו ב-GitHub.

## התקנה

הכלי כתוב ב-Python, וצריך Python 3.11 ומעלה, `git`, ושתי ספריות: `pydantic` ו-`pydantic-settings`.

### במחשב החיצוני

```bash
cd scripts/airgap-mirrors
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

באותו מחשב מורידים גם את הספריות בשביל המחשב הפנימי, שאין לו אינטרנט. מתאימים את `--python-version` לגרסה שמותקנת במחשב הפנימי:

```bash
.venv/bin/pip download -r requirements.txt -d wheels \
  --only-binary=:all: --platform manylinux2014_x86_64 --python-version 3.11
```

מעבירים את התיקייה `scripts/airgap-mirrors` כולה, כולל `wheels`, למחשב הפנימי.

### במחשב הפנימי

```bash
cd scripts/airgap-mirrors
python3 -m venv .venv
.venv/bin/pip install --no-index --find-links wheels -r requirements.txt
```

## הגדרה

לכל מחשב יש קובץ הגדרות משלו בתיקייה `config/`. ההפרדה מכוונת: הקובץ של המחשב החיצוני לא מכיל שום פרט על הרשת הפנימית.

### במחשב החיצוני

```bash
cp config/external.toml.example config/external.toml
```

הקובץ מוכן לשימוש כמו שהוא: רשימת ה-repos מלאה, והתיקיות מוגדרות ב-`~/airgap`. משנים רק אם רוצים מיקום אחר:
- `mirrors_dir`: כאן נשמר עותק של כל repo בין סבב לסבב. בזכותו כל העברה כוללת רק את מה שחדש.
- `transfer_dir`: התיקייה שעוברת בדיסק און קי.

אופציונלי, אבל מומלץ: טוקן של GitHub, שמעלה את מגבלת הקריאות מ-60 ל-5,000 בשעה.

```bash
export GITHUB_TOKEN=<token>
```

### במחשב הפנימי

```bash
cp config/internal.toml.example config/internal.toml
```

ממלאים רק שני שדות:
- `gitlab_url`: הכתובת של GitLab.
- `gitlab_group`: הקבוצה שאליה ייכנסו כל העותקים, למשל `redis/mirrors`. כל repo יהיה project בשם `<gitlab_group>/<name>`, למשל `redis/mirrors/redis`.

אין רשימת repos לתחזק. הכלי קורא מתיקיית ההעברה מה הגיע.

**מה הכלי עושה לבד ב-import הראשון:**
- **יוצר את ה-projects.** כל project נוצר ריק, בלי README, ובלי issues, merge requests, wiki ו-snippets, כי הכול מגיע מ-GitHub.
- **יוצר תתי-קבוצות חסרות.** למשל, את `mirrors` בתוך `redis`.
- **קובע בכל project את ה-branch הראשי** לפי GitHub.

הקבוצה העליונה (`redis` בדוגמה) חייבת להתקיים מראש, כי ליצור קבוצה עליונה זו החלטה של מנהל ה-GitLab.

**שדות אופציונליים:**
- `project_visibility`: ‏`"private"`, ‏`"internal"` או `"public"`. בלי השדה הזה GitLab קובע לפי ברירת המחדל שלו.
- `ca_file`: אם התעודה של GitLab חתומה על ידי ה-CA של החברה.
- `git_remote_base`: כדי לדחוף ב-SSH במקום ב-HTTPS.
- בלוק `[[repos]]`: רק אם רוצים ש-repo מסוים יישב במקום אחר.

**הטוקן:** הטוקן של GitLab לא נכתב בקובץ. מגדירים אותו לפני כל ריצה:
```bash
export GITLAB_TOKEN=<token>
```
צריך טוקן עם scope ‏`api` ותפקיד Maintainer על הקבוצה. מומלץ Group Access Token, שלא משויך לאף משתמש.

## סבב רגיל

**1. במחשב החיצוני:**
```bash
.venv/bin/python -m airgap_mirrors --config config/external.toml export
```

**2.** מעתיקים את תיקיית ההעברה (`transfer_dir`) לדיסק און קי, ומשם ל-`transfer_dir` של המחשב הפנימי.

**3. במחשב הפנימי:**
```bash
export GITLAB_TOKEN=<token>
.venv/bin/python -m airgap_mirrors --config config/internal.toml import
```

בסוף ה-import נכתב הקובץ `~/airgap/mirrors/helm-values-git-mirrors.yaml`. זה קובץ values מוכן ל-Helm, עם כתובת לכל repo שהגיע ל-GitLab (ראו [הפעלת ההפניה ב-Helm](#הפעלת-ההפניה-ב-helm)).

**4.** מעתיקים את `receipt.json`, שנמצא בתיקיית ההעברה, חזרה ל-`transfer_dir` של המחשב החיצוני.

**5. במחשב החיצוני:**
```bash
.venv/bin/python -m airgap_mirrors --config config/external.toml confirm
```

**6.** מרוקנים את תיקיית ההעברה בשני המחשבים. הסבב הבא ייצור אותה מחדש.

### אפשרויות נוספות

- `--repo <name>`: רק repo אחד. אפשר לחזור על האפשרות כדי לבחור כמה repos.
- `--skip-releases`: רק git, בלי releases.
- `--full` (ב-export בלבד): שולח הכול מחדש, ולא רק את מה שהשתנה.

## הורדת קבצי releases

הקוד עובר עם כל ההיסטוריה שלו: כל ה-branches וכל ה-tags. ההערות של כל ה-releases עוברות גם הן. רק **הקבצים** של ה-releases מסוננים, כי ההיסטוריה שלהם תופסת הרבה מקום: כל הקבצים של כל ה-releases ביחד שוקלים כ-14 GB.

הסינון נקבע פעם אחת, בראש `external.toml`, וחל על כל ה-repos:

```toml
default_assets = "latest-per-type"
default_platforms = ["windows", "linux", "redhat"]
default_architectures = ["x86_64"]
```

**`default_assets`: מאילו releases להוריד קבצים.**
- `"latest-per-type"`: האחרון מכל סוג שחרור. "סוג" נקבע לפי שני דברים:
  - **הקידומת של ה-tag.** ‏repo אחד יכול להפיץ כמה מוצרים. ב-`redisctl`, למשל, יש `redisctl-v0.14.0`, ‏`redisctl-mcp-v0.14.0` ו-`redisctl-core-v0.14.0`, וכל אחד מהם הוא סוג נפרד.
  - **יציב או pre-release.** יורד ה-release היציב האחרון, ובנוסף ה-pre-release האחרון (rc, beta, alpha), אבל רק אם הוא חדש יותר מה-release היציב. ב-`redis`, למשל, יורדים הקבצים של 8.10.3 ושל 8.12-rc3. release נחשב pre-release אם הוא מסומן ככזה ב-GitHub, או אם השם שלו נראה כמו pre-release.
- `"latest-stable"`: רק ה-release היציב האחרון מכל קידומת, בלי pre-releases.
- `"none"`: בלי קבצים.
- `"all"`: כל ה-releases.
- `"latest:3"`: שלושת ה-releases האחרונים.
- `"since:2026-01-01"`: מהתאריך הזה והלאה.

**`default_platforms`: לאילו פלטפורמות.**
- `windows`: קבצי ‎`.exe`, ‏`.msi`, ושמות שמכילים `win`.
- `linux`: קבצי ‎`.deb`, ‏`.AppImage`, ‏`.snap`, ושמות של הפצות כמו Ubuntu ו-Debian.
- `redhat`: קבצי ‎`.rpm`, ושמות שמכילים `el8`, ‏`el9`, ‏`el10`, ‏`rhel`, ‏`centos` או `rocky`.
- `amazon`: חבילות של Amazon Linux (`amzn`).
- `macos`: קבצי ‎`.dmg`, ושמות שמכילים `mac` או `darwin`.

**`default_architectures`: לאיזה מעבד.**
- `x86_64`: גם `amd64` ו-`x64`.
- `arm64`: גם `aarch64`.
- `arm32` ו-`x86_32`.

הפלטפורמה והמעבד מזוהים לפי שם הקובץ. קובץ שלא מציין פלטפורמה או מעבד תמיד עובר, כי הוא מתאים לכולם: קוד מקור, jar, YAML, installer של Windows, סקריפט התקנה. רשימה ריקה פירושה הכול.

**repo בודד** יכול לדרוס את ברירות המחדל עם `assets` ו-`platforms` משלו, ולצמצם עוד יותר עם `asset_filter`. במקרה כזה עוברים רק קבצים שהשם שלהם מכיל אחת מהמילים ברשימה.

עם ההגדרות האלה, ההורדה הראשונה של קבצי ה-releases היא כ-1.7 GB. בלי הסינון היא הייתה כ-14 GB. רוב הנפח מגיע משני repos:
- **RIOT-X:** כ-780 MB. כל קובץ שלו שוקל כ-390 MB, כי Java ארוזה בתוכו. לכן ב-config הוא מוגדר להוריד רק את ה-release היציב האחרון (`latest-stable`), ורק את הגרסה העצמאית ל-Linux x86_64 ול-Windows.
- **Redis Insight:** כ-650 MB.

ב-GitLab, כל קובץ נשמר ב-package registry של ה-project ומקבל כתובת קבועה: `<project>/-/releases/<tag>/downloads/<file>`. לכתובת הזו ה-chart מפנה את קישורי ההורדה בתיעוד. הגודל המקסימלי של קובץ נקבע בהגדרה `generic_packages_max_file_size` של GitLab, וברירת המחדל שלה היא 5 GB.

## אילו repos מועתקים

34 repos, שנבחרו מתוך 222 ה-repos שהתיעוד מקשר אליהם. נבחר כל repo של Redis שיש אליו קישורים רבים, וכל מוצר שהתיעוד שולח להוריד מ-GitHub. הרשימה המלאה נמצאת ב-`config/external.toml.example`.

**Redis והמודולים:** `redis`, ‏`RediSearch`, ‏`RedisJSON`, ‏`RedisTimeSeries`, ‏`RedisBloom`, ‏`RedisGears`, ‏`RedisGraph`.

**מוצרים וכלים להורדה:**
- `RedisInsight`
- `redisctl`
- `riotx`
- `memtier_benchmark`
- `redis-apache-arrow-flight`
- `redis-adbc-driver`
- `redisinsight-tutorials`
- `grafana-redis-datasource`

**Kubernetes וניטור:** `k8s-docs` (ה-operator), ‏`prometheus-operator`, ‏`observability`.

**קוד מקור וספריות לקוח:**
- `docs`
- `redis-py`, ‏`redis-vl-python`
- `jedis`, ‏`lettuce`
- `node-redis`, ‏`ioredis`
- `go-redis`, ‏`rueidis`
- `NRedisStack`
- `hiredis`
- `predis`
- `redis-om-python`, ‏`redis-om-node`, ‏`redis-om-spring`, ‏`redis-om-dotnet`

**לא נכללו:**
- **כלים של צד שלישי**, כמו node_exporter, ingress-nginx ו-Reloader. בסביבה סגורה מביאים אותם בערוצים שלהם.
- **repos שיש אליהם קישור בודד**, בלי מוצר להורדה.

מתוך כ-5,600 הקישורים לכל ה-repos האלה, כ-2,200 עוברים ל-GitLab. השאר הם קישורים ל-pull requests ול-issues ב-release notes של המודולים, ולכן נשארים ב-GitHub.

## מה עושים כשמשהו נכשל

- **הפקודה מסתיימת בקוד 2:** קובץ ההגדרות שגוי. ההודעה מציינת איזה שדה.
- **הפקודה מסתיימת בקוד 1:** repo אחד או יותר נכשל. ה-repos האחרים בכל זאת עברו, ושם ה-repo שנכשל מופיע בשורה האחרונה. אפשר להריץ שוב את אותה פקודה: מה שכבר עבר יידלג.
- **ההודעה "builds on an earlier transfer that never arrived":** סבב קודם לא הגיע ל-GitLab. מעבירים אותו, או מריצים export עם `--full`.
- **ההודעה "GitLab has no group":** הקבוצה העליונה שב-`gitlab_group` לא קיימת. יוצרים אותה, או מבקשים ממנהל ה-GitLab, ומריצים שוב.
- **שגיאת HTTP ‏403 ביצירת project:** לטוקן אין הרשאה ליצור projects בקבוצה. צריך תפקיד Maintainer.
- **כדי לראות כל פקודת git וכל קריאת HTTP:** משנים את `level` ל-`"DEBUG"` ב-`config/logging.toml`.

## הפעלת ההפניה ב-Helm

ה-import כותב את הקובץ `~/airgap/mirrors/helm-values-git-mirrors.yaml`, ובו כל ה-repos שכבר נמצאים ב-GitLab, עם הכתובת של כל אחד:

```yaml
externalLinks:
  gitMirrors:
    "redis":
      enabled: true
      to: "https://gitlab.<your-company>.example/redis/mirrors/redis"
```

מוסיפים את הקובץ להתקנה של ה-chart עם `-f`:

```bash
helm install <release> <chart> -f your-values.yaml -f ~/airgap/mirrors/helm-values-git-mirrors.yaml
```

לא צריך לבנות image מחדש: השינוי מעדכן ConfigMap בלבד.

## הוספת repo

1. מוסיפים entry ב-`helm/redis-docs/files/external-links.yaml`, תחת `git-mirrors:`. ב-`repo` שמים את השם הנוכחי ב-GitHub, וב-`aliases` שמות ישנים שעדיין מפנים אליו.
2. מוסיפים בלוק `[[repos]]` עם אותו `name` ל-`config/external.toml.example`, ול-`external.toml` אם יצרתם עותק.

זה הכול: ה-project ב-GitLab ייווצר ב-import הבא. הבדיקה ב-`helm/tools/test_git_mirrors_catalog.py` מוודאת שהרשימה בכלי ובקטלוג זהות.

## מגבלות

- קישורים בתוך בלוקי קוד, כמו `git clone` או `kubectl apply -f https://raw.githubusercontent.com/...`, לא משתנים. ההפניה חלה רק על קישורים לחיצים.
- אם Redis עושים force push ל-branch הראשי, GitLab ידחה אותו, כי ה-branch הראשי מוגן מפני force push. ה-repo ייכשל בסבב הזה, והשאר ימשיכו.
- branches של submodules לא מועתקים. הם לא נחוצים בשביל הקישורים, רק בשביל בנייה מקוד מקור.
