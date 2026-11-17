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

ממלאים שתי תיקיות:
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

ממלאים:
- `mirrors_dir` ו-`transfer_dir`.
- `gitlab_url`: הכתובת של GitLab.
- לכל repo, את `gitlab_path`: הנתיב של ה-project ב-GitLab, למשל `redis/mirrors/redis`.
- `ca_file`: רק אם התעודה של GitLab חתומה על ידי ה-CA של החברה.
- `git_remote_base`: רק אם רוצים לדחוף ב-SSH במקום ב-HTTPS.

הטוקן של GitLab לא נכתב בקובץ. צריך טוקן עם הרשאת `api`, של משתמש שהוא Maintainer ב-projects, ומגדירים אותו לפני כל ריצה:

```bash
export GITLAB_TOKEN=<token>
```

**לפני ה-import הראשון:** כל project צריך להיות קיים ב-GitLab וריק לגמרי, בלי README.

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

לכל repo ב-`external.toml` אפשר לקבוע אילו releases יורדו עם הקבצים שלהם. ההערות של ה-release עוברות תמיד.

- `assets = "all"`: כל ה-releases. זו ברירת המחדל.
- `assets = "none"`: בלי קבצים.
- `assets = "latest:3"`: רק שלושת ה-releases האחרונים.
- `assets = "since:2026-01-01"`: רק releases מהתאריך הזה והלאה.
- `asset_filter = ["win", "linux"]`: רק קבצים שהשם שלהם מכיל אחת מהמילים. כך למשל מדלגים על קבצי macOS של Redis Insight.

ב-GitLab, כל קובץ נשמר ב-package registry של ה-project ומקבל כתובת קבועה: `<project>/-/releases/<tag>/downloads/<file>`. לכתובת הזו ה-chart מפנה את קישורי ההורדה בתיעוד.

הגודל המקסימלי של קובץ נקבע בהגדרה `generic_packages_max_file_size` של GitLab, וברירת המחדל שלה היא 5 GB.

## מה עושים כשמשהו נכשל

- **הפקודה מסתיימת בקוד 2:** קובץ ההגדרות שגוי. ההודעה מציינת איזה שדה.
- **הפקודה מסתיימת בקוד 1:** repo אחד או יותר נכשל. ה-repos האחרים בכל זאת עברו, ושם ה-repo שנכשל מופיע בשורה האחרונה. אפשר להריץ שוב את אותה פקודה: מה שכבר עבר יידלג.
- **ההודעה "builds on an earlier transfer that never arrived":** סבב קודם לא הגיע ל-GitLab. מעבירים אותו, או מריצים export עם `--full`.
- **ההודעה "GitLab has no project":** צריך ליצור את ה-project ב-GitLab, ריק.
- **כדי לראות כל פקודת git וכל קריאת HTTP:** משנים את `level` ל-`"DEBUG"` ב-`config/logging.toml`.

## הפעלת ההפניה ב-Helm

אחרי שה-repos נמצאים ב-GitLab, מפעילים את ההפניה ב-`values.yaml`. השמות זהים לשמות ב-`internal.toml`:

```yaml
externalLinks:
  gitMirrors:
    redis:
      enabled: true
      to: https://gitlab.<your-company>.example/redis/mirrors/redis
    RediSearch:
      enabled: true
      to: https://gitlab.<your-company>.example/redis/mirrors/RediSearch
```

לא צריך לבנות image מחדש: השינוי מעדכן ConfigMap בלבד.

## הוספת repo

1. מוסיפים entry ב-`helm/redis-docs/files/external-links.yaml`, תחת `git-mirrors:`. ב-`repo` שמים את השם הנוכחי ב-GitHub, וב-`aliases` שמות ישנים שעדיין מפנים אליו.
2. מוסיפים בלוק `[[repos]]` עם אותו `name` לשני קבצי ה-`.toml.example` ולשני קבצי ה-`.toml` האמיתיים.
3. יוצרים project ריק ב-GitLab.

הבדיקה ב-`helm/tools/test_git_mirrors_catalog.py` מוודאת ששלוש הרשימות זהות.

## מגבלות

- קישורים בתוך בלוקי קוד, כמו `git clone` או `kubectl apply -f https://raw.githubusercontent.com/...`, לא משתנים. ההפניה חלה רק על קישורים לחיצים.
- אם Redis עושים force push ל-branch הראשי, GitLab ידחה אותו, כי ה-branch הראשי מוגן מפני force push. ה-repo ייכשל בסבב הזה, והשאר ימשיכו.
- branches של submodules לא מועתקים. הם לא נחוצים בשביל הקישורים, רק בשביל בנייה מקוד מקור.
