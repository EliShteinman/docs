# הגדרת Mirrors של GitHub ל-GitLab עבור airgap

## רקע

האתר מכיל ~3,000 קישורים ל-GitHub. בסביבת airgap הדפדפן לא מגיע ל-`github.com` — הקישורים נשברים.
המנגנון `gitMirrors` ב-`configmap-runtime.yaml` משכתב אותם בזמן ריצה ל-mirrors פנימיים ב-GitLab,
בתנאי שהם מסונכרנים ומכילים את כל ה-branches וה-tags המקוריים.

12 repos נדרשים — הם מפורטים בקטלוג `helm/redis-docs/files/external-links.yaml` תחת `git-mirrors:`.

---

## ייבוא ראשוני (חד-פעמי)

הייבוא הראשוני כבר בוצע. אם יש צורך להוסיף repo חדש בעתיד, ראה [הוספת repo חדש](#הוספת-repo-חדש).

---

## הגדרת הסקריפטים

כל הסקריפטים נמצאים ב-`scripts/airgap-mirrors/`.

### מחשב חיצוני (אונליין)

```bash
cd scripts/airgap-mirrors/
cp mirrors.external.conf.example mirrors.conf
# ערוך:
#   MIRRORS_DIR  — נתיב לתיקיית ה-bare mirrors (לדוגמה: ~/mirrors)
#   TRANSFER_DIR — תיקייה שממנה תעתיק ל-USB
# שאר הקובץ (רשימת ה-repos ו-policies) כבר מוגדר נכון
```

### מחשב פנימי (airgap)

```bash
cd scripts/airgap-mirrors/
cp mirrors.internal.conf.example mirrors.conf
# ערוך:
#   MIRRORS_DIR  — נתיב לתיקיית ה-bare mirrors
#   TRANSFER_DIR — תיקייה שאליה תעתיק מה-USB
#   GITLAB_HOST  — כתובת GitLab הפנימי
#   כל שורת MIRRORS — החלף "your-group" ב-path האמיתי של כל פרויקט ב-GitLab
```

> **הפרדת מידע:** `mirrors.conf` על המחשב החיצוני לא מכיל שום פרט על הרשת הפנימית.
> מידע על GitLab (host, paths, token) קיים **רק** על המחשב הפנימי.

### פעם אחת לאחר ה-bootstrap הראשוני — הגדרת נקודת ההתחלה

מאחר שהייבוא הראשוני כבר בוצע, יש לסמן לסקריפטים שה-state הנוכחי כבר סונכרן:

```bash
# במחשב החיצוני:
cd ~/mirrors    # או ה-MIRRORS_DIR שלך
for d in *.git; do
  ( cd "$d" && git config --local sync.synced "$(git rev-parse HEAD)" )
done
```

---

## זרימה שוטפת — סנכרון Git (תקופתי)

```
מחשב חיצוני                USB                מחשב פנימי
─────────────               ───                ────────────
bundle-create.sh  ──────►  bundles/  ──────►  bundle-import.sh
                                               (push --mirror origin → GitLab)
bundle-confirm.sh ◄──────  import-success.list
```

**1. מחשב חיצוני:**
```bash
./bundle-create.sh
# → TRANSFER_DIR/bundles/*.bundle  (delta קטן מאז הסנכרון האחרון)
```

**2. העתק `$TRANSFER_DIR/bundles/` ל-USB ומשם למחשב הפנימי.**

**3. מחשב פנימי:**
```bash
export GITLAB_TOKEN="glpat-xxxxx"
./bundle-import.sh
# → מוודא, טוען, דוחף --mirror origin לכל repo
# → TRANSFER_DIR/import-success.list
```

**4. העתק `$TRANSFER_DIR/import-success.list` חזרה ל-USB ומשם למחשב החיצוני.**

**5. מחשב חיצוני:**
```bash
./bundle-confirm.sh
# → מקדם sync.synced לריצה הבאה
```

> **שלב 4–5 חשוב:** `bundle-confirm.sh` מסמן את נקודת ההתחלה לבאנדל הבא.
> אם הוא לא רץ — הריצה הבאה תייצר bundle גדול יותר (מה שחסר), אבל לא תאבד נתונים.

---

## זרימה שוטפת — Releases (כשיש ריליסים חדשים)

כולל: metadata (title + body), binary assets לפי policy.

**Policy של assets מוגדר ב-`mirrors.conf` (שדה שלישי ורביעי בכל שורת MIRRORS):**

| Policy | משמעות |
|---|---|
| `all` (ברירת מחדל) | כל ה-assets |
| `none` | metadata בלבד |
| `latest:N` | assets של N הריליסים האחרונים בלבד |
| `since:YYYY-MM-DD` | assets של ריליסים שיצאו מתאריך זה |

שדה רביעי אופציונלי — סינון שמות קבצים (keywords מופרדים בפסיק):
```
"RedisInsight|RedisInsight/RedisInsight|all|win,linux"
# → מוריד כל ה-releases, אך רק קבצי Windows + Linux (ללא macOS .dmg)
```

גדלים מדודים של RedisInsight (48 ריליסים, win+linux בלבד): **~3.52 GiB ריצה ראשונה**, ~700–815 MiB לכל ריליס חדש מכאן ואילך.

**1. מחשב חיצוני:**
```bash
gh auth login   # פעם אחת בלבד
./releases-export.sh
# → TRANSFER_DIR/releases/<name>/releases.json
# → TRANSFER_DIR/releases/<name>/assets/<tag>/*  (לפי policy)
# קבצים שכבר הורדו בעבר — מדולגים אוטומטית (cache)
```

**2. העתק `$TRANSFER_DIR/releases/` ל-USB ומשם למחשב הפנימי.**

**3. מחשב פנימי** (לאחר `bundle-import.sh` — tag חייב להיות ב-GitLab קודם):
```bash
export GITLAB_TOKEN="glpat-xxxxx"
./releases-import.sh
# → idempotent: ריליס קיים ב-GitLab → מדולג
```

---

## הגדרת Default Branch (חד-פעמי)

`git push --mirror` לא מעביר את ה-default branch של ה-project — GitLab קובע אותו בנפרד.
לדוגמה, `redis/redis` משתמש ב-`unstable` ולא ב-`master`.

```bash
# מחשב פנימי, לאחר bundle-import.sh הראשון:
export GITLAB_TOKEN="glpat-xxxxx"
./default-branch-set.sh
# → קורא HEAD מכל bare mirror, מעדכן GitLab project settings
```

---

## מגבלות — מה לא מועבר

| משאב | סיבה | השפעה על docs |
|---|---|---|
| **Issues, Pull Requests** | DB של GitHub, לא Git | 2,220 קישורי PR + 648 Issues → יציגו ב-GitLab אבל תוכן לא יועבר |
| **Security Advisories** | DB של GitHub | 16 קישורים — יישארו שבורים |
| **Wiki** | repo נפרד (`<repo>.wiki.git`) | 2 קישורים — צריך mirror נפרד |
| **Release body של ריליסים ישנים** | לא בגיט | נוצרים דפי Release ריקים אם לא יובא ה-JSON |
| **Release assets היסטוריים** | לפי ה-policy | רק מה שה-policy מגדיר |
| **`curl`/`kubectl apply -f` ב-code blocks** | JS handler לא נוגע ב-code blocks | קישורים אלה לא משוכתבים בזמן ריצה |

---

## עדכון `values.yaml`

לאחר שכל ה-mirrors מוכנים ב-GitLab, מפעילים אותם ב-Helm:

```yaml
externalLinks:
  gitMirrors:

    k8s-docs:
      enabled: true
      to: https://gitlab.your-company.example/your-group/redis-enterprise-k8s-docs

    observability:
      enabled: true
      to: https://gitlab.your-company.example/your-group/redis-enterprise-observability

    redis:
      enabled: true
      to: https://gitlab.your-company.example/your-group/redis

    RediSearch:
      enabled: true
      to: https://gitlab.your-company.example/your-group/RediSearch

    RedisGraph:
      enabled: true
      to: https://gitlab.your-company.example/your-group/RedisGraph

    RedisInsight:
      enabled: true
      to: https://gitlab.your-company.example/your-group/RedisInsight

    RedisTimeSeries:
      enabled: true
      to: https://gitlab.your-company.example/your-group/RedisTimeSeries

    RedisGears:
      enabled: true
      to: https://gitlab.your-company.example/your-group/RedisGears

    RedisJSON:
      enabled: true
      to: https://gitlab.your-company.example/your-group/RedisJSON

    RedisBloom:
      enabled: true
      to: https://gitlab.your-company.example/your-group/RedisBloom

    redis-py:
      enabled: true
      to: https://gitlab.your-company.example/your-group/redis-py

    prometheus-operator:
      enabled: true
      to: https://gitlab.your-company.example/your-group/prometheus-operator
```

```bash
helm upgrade <release-name> helm/redis-docs/ -f your-values.yaml
# אין צורך ב-image rebuild — מנגנון ConfigMap בלבד
```

---

## הוספת repo חדש

```bash
# מחשב חיצוני:
git clone --mirror https://github.com/<owner>/<repo> ~/mirrors/<repo>.git

# העתק ~/mirrors/<repo>.git ל-USB → מחשב פנימי

# מחשב פנימי:
git clone --mirror https://gitlab.your-company.example/your-group/<repo> ~/mirrors/<repo>.git
cd ~/mirrors/<repo>.git
git remote add external /path/to/usb/<repo>.git
git fetch --prune external
git push --mirror origin

# אתחל state על המחשב החיצוני:
cd ~/mirrors/<repo>.git
git config --local sync.synced "$(git rev-parse HEAD)"
```

הוסף entry ל-`helm/redis-docs/files/external-links.yaml` תחת `git-mirrors:` ועדכן את `values.yaml`.
