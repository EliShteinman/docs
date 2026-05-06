# הגדרת Mirrors של GitHub ל-GitLab עבור airgap

## רקע

האתר הזה מכיל ~3,000 קישורים ל-GitHub ברחבי הדוקומנטציה. בסביבת airgap הקישורים נשברים — הדפדפן של הלקוח לא מגיע ל-`github.com`. המנגנון `gitMirrors` ב-`configmap-runtime.yaml` משכתב את הקישורים בזמן ריצה ל-mirror פנימי ב-GitLab, **בתנאי שה-mirror קיים שם, מסונכרן, ומכיל את כל ה-branches וה-tags המקוריים**.

המסמך הזה מתאר איך להכין את 12 ה-mirrors הנדרשים: **2 שכבר קיימים אצלך** (יש לעדכן את שיטת הסנכרון שלהם), ו-**10 חדשים** שצריך להוסיף.

## הזרימה הכללית (חלה על כל 12 ה-repos)

```
┌─────────────────────────┐                     ┌─────────────────────────┐
│  מחשב חיצוני (אינטרנט)  │                     │  מחשב פנימי (חברה)      │
│                         │                     │                         │
│  תיקייה A (mirror bare) │  ──── USB ────►     │  תיקייה A (עותק)        │
│  git fetch --prune      │   (ה-IT מעבירים)    │                         │
│                         │                     │  תיקייה B (mirror bare) │
│                         │                     │  fetch upstream-mirror  │
│                         │                     │  push --mirror origin   │
│                         │                     │  ↓                      │
│                         │                     │  GitLab של החברה        │
└─────────────────────────┘                     └─────────────────────────┘
```

**שינוי מהותי לעומת השיטה הישנה:**
- A ו-B שניהם `--mirror` clones (bare, ללא working tree).
- במקום `git fetch + git merge + git push` משתמשים ב-`git fetch + git push --mirror`.
- כך מסונכרנים **כל** ה-branches ו-**כל** ה-tags — לא רק זה שעובדים עליו.

**`git push --mirror` הוא destructive** — הוא מוחק ב-GitLab כל ref שלא קיים ב-A. אם שמרתם ב-GitLab branches ידניים שאינם ב-GitHub, יימחקו. עבור 12 ה-repos האלה זה התנהגות רצויה (mirror טהור).

## הסבר על URL ה-GitLab בכל סקציה

לאורך המסמך מופיע ה-placeholder:

```
https://gitlab.your-company.example/your-group/<repo-name>
```

- `gitlab.your-company.example` — ה-host של GitLab בחברה (להחליף בערך האמיתי).
- `your-group/...` — הקבוצה (יכולה להיות nested: `group/sub1/sub2/...`).
- `<repo-name>` — **שם ה-repo זהה לשם ב-GitHub**. שמור על האותיות בדיוק כפי שהן ב-GitHub כדי שלא תיווצרנה התנגשויות.

לאחר ההגדרה, מעדכנים את `values.yaml` של ה-Helm chart עם ה-`to` URL הנכון לכל entry ב-`externalLinks.gitMirrors`.

---

## 1. redis-enterprise-k8s-docs (כבר קיים אצלך)

| | URL |
|---|---|
| GitHub | `https://github.com/RedisLabs/redis-enterprise-k8s-docs` |
| GitLab (פיקטיבי) | `https://gitlab.your-company.example/your-group/redis-enterprise-k8s-docs` |

⚠️ ה-mirror הזה כבר קיים ב-GitLab, אבל סוכן בשיטה הישנה (clone רגיל + merge). יש להגדיר מחדש.

### במחשב החיצוני — חד-פעמי
```bash
rm -rf ~/mirrors/redis-enterprise-k8s-docs.git
git clone --mirror https://github.com/RedisLabs/redis-enterprise-k8s-docs ~/mirrors/redis-enterprise-k8s-docs.git
```

### במחשב החיצוני — כל פעם לפני USB
```bash
cd ~/mirrors/redis-enterprise-k8s-docs.git
git fetch --prune
```

### במחשב הפנימי — חד-פעמי
```bash
rm -rf ~/mirrors/redis-enterprise-k8s-docs.git
git clone --mirror https://gitlab.your-company.example/your-group/redis-enterprise-k8s-docs ~/mirrors/redis-enterprise-k8s-docs.git
cd ~/mirrors/redis-enterprise-k8s-docs.git
git remote add upstream-mirror /path/to/usb-copy/redis-enterprise-k8s-docs.git
git config remote.upstream-mirror.fetch '+refs/heads/*:refs/heads/*'
git config --add remote.upstream-mirror.fetch '+refs/tags/*:refs/tags/*'
```

### במחשב הפנימי — כל פעם אחרי USB
```bash
cd ~/mirrors/redis-enterprise-k8s-docs.git
git fetch --prune upstream-mirror
git push --mirror origin
```

---

## 2. redis-enterprise-observability (כבר קיים אצלך)

| | URL |
|---|---|
| GitHub | `https://github.com/redis-field-engineering/redis-enterprise-observability` |
| GitLab (פיקטיבי) | `https://gitlab.your-company.example/your-group/redis-enterprise-observability` |

⚠️ קיים אצלך, סוכן בשיטה הישנה — להגדיר מחדש.

### במחשב החיצוני — חד-פעמי
```bash
rm -rf ~/mirrors/redis-enterprise-observability.git
git clone --mirror https://github.com/redis-field-engineering/redis-enterprise-observability ~/mirrors/redis-enterprise-observability.git
```

### במחשב החיצוני — כל פעם לפני USB
```bash
cd ~/mirrors/redis-enterprise-observability.git
git fetch --prune
```

### במחשב הפנימי — חד-פעמי
```bash
rm -rf ~/mirrors/redis-enterprise-observability.git
git clone --mirror https://gitlab.your-company.example/your-group/redis-enterprise-observability ~/mirrors/redis-enterprise-observability.git
cd ~/mirrors/redis-enterprise-observability.git
git remote add upstream-mirror /path/to/usb-copy/redis-enterprise-observability.git
git config remote.upstream-mirror.fetch '+refs/heads/*:refs/heads/*'
git config --add remote.upstream-mirror.fetch '+refs/tags/*:refs/tags/*'
```

### במחשב הפנימי — כל פעם אחרי USB
```bash
cd ~/mirrors/redis-enterprise-observability.git
git fetch --prune upstream-mirror
git push --mirror origin
```

---

## 3. redis (706 קישורים)

| | URL |
|---|---|
| GitHub | `https://github.com/redis/redis` |
| GitLab (פיקטיבי) | `https://gitlab.your-company.example/your-group/redis` |

### במחשב החיצוני — חד-פעמי
```bash
git clone --mirror https://github.com/redis/redis ~/mirrors/redis.git
```

### במחשב החיצוני — כל פעם לפני USB
```bash
cd ~/mirrors/redis.git
git fetch --prune
```

### במחשב הפנימי — חד-פעמי
```bash
git clone --mirror https://gitlab.your-company.example/your-group/redis ~/mirrors/redis.git
cd ~/mirrors/redis.git
git remote add upstream-mirror /path/to/usb-copy/redis.git
git config remote.upstream-mirror.fetch '+refs/heads/*:refs/heads/*'
git config --add remote.upstream-mirror.fetch '+refs/tags/*:refs/tags/*'
```

### במחשב הפנימי — כל פעם אחרי USB
```bash
cd ~/mirrors/redis.git
git fetch --prune upstream-mirror
git push --mirror origin
```

---

## 4. RediSearch (1,067 קישורים — כולל וריאציה lowercase)

| | URL |
|---|---|
| GitHub | `https://github.com/RediSearch/RediSearch` |
| GitLab (פיקטיבי) | `https://gitlab.your-company.example/your-group/RediSearch` |

### במחשב החיצוני — חד-פעמי
```bash
git clone --mirror https://github.com/RediSearch/RediSearch ~/mirrors/RediSearch.git
```

### במחשב החיצוני — כל פעם לפני USB
```bash
cd ~/mirrors/RediSearch.git
git fetch --prune
```

### במחשב הפנימי — חד-פעמי
```bash
git clone --mirror https://gitlab.your-company.example/your-group/RediSearch ~/mirrors/RediSearch.git
cd ~/mirrors/RediSearch.git
git remote add upstream-mirror /path/to/usb-copy/RediSearch.git
git config remote.upstream-mirror.fetch '+refs/heads/*:refs/heads/*'
git config --add remote.upstream-mirror.fetch '+refs/tags/*:refs/tags/*'
```

### במחשב הפנימי — כל פעם אחרי USB
```bash
cd ~/mirrors/RediSearch.git
git fetch --prune upstream-mirror
git push --mirror origin
```

---

## 5. RedisGraph (578 קישורים — כולל וריאציה lowercase)

| | URL |
|---|---|
| GitHub | `https://github.com/RedisGraph/RedisGraph` |
| GitLab (פיקטיבי) | `https://gitlab.your-company.example/your-group/RedisGraph` |

### במחשב החיצוני — חד-פעמי
```bash
git clone --mirror https://github.com/RedisGraph/RedisGraph ~/mirrors/RedisGraph.git
```

### במחשב החיצוני — כל פעם לפני USB
```bash
cd ~/mirrors/RedisGraph.git
git fetch --prune
```

### במחשב הפנימי — חד-פעמי
```bash
git clone --mirror https://gitlab.your-company.example/your-group/RedisGraph ~/mirrors/RedisGraph.git
cd ~/mirrors/RedisGraph.git
git remote add upstream-mirror /path/to/usb-copy/RedisGraph.git
git config remote.upstream-mirror.fetch '+refs/heads/*:refs/heads/*'
git config --add remote.upstream-mirror.fetch '+refs/tags/*:refs/tags/*'
```

### במחשב הפנימי — כל פעם אחרי USB
```bash
cd ~/mirrors/RedisGraph.git
git fetch --prune upstream-mirror
git push --mirror origin
```

---

## 6. RedisInsight (430 קישורים — כולל וריאציה `redis/RedisInsight`)

| | URL |
|---|---|
| GitHub | `https://github.com/RedisInsight/RedisInsight` |
| GitLab (פיקטיבי) | `https://gitlab.your-company.example/your-group/RedisInsight` |

### במחשב החיצוני — חד-פעמי
```bash
git clone --mirror https://github.com/RedisInsight/RedisInsight ~/mirrors/RedisInsight.git
```

### במחשב החיצוני — כל פעם לפני USB
```bash
cd ~/mirrors/RedisInsight.git
git fetch --prune
```

### במחשב הפנימי — חד-פעמי
```bash
git clone --mirror https://gitlab.your-company.example/your-group/RedisInsight ~/mirrors/RedisInsight.git
cd ~/mirrors/RedisInsight.git
git remote add upstream-mirror /path/to/usb-copy/RedisInsight.git
git config remote.upstream-mirror.fetch '+refs/heads/*:refs/heads/*'
git config --add remote.upstream-mirror.fetch '+refs/tags/*:refs/tags/*'
```

### במחשב הפנימי — כל פעם אחרי USB
```bash
cd ~/mirrors/RedisInsight.git
git fetch --prune upstream-mirror
git push --mirror origin
```

---

## 7. RedisTimeSeries (221 קישורים — כולל וריאציה lowercase)

| | URL |
|---|---|
| GitHub | `https://github.com/RedisTimeSeries/RedisTimeSeries` |
| GitLab (פיקטיבי) | `https://gitlab.your-company.example/your-group/RedisTimeSeries` |

### במחשב החיצוני — חד-פעמי
```bash
git clone --mirror https://github.com/RedisTimeSeries/RedisTimeSeries ~/mirrors/RedisTimeSeries.git
```

### במחשב החיצוני — כל פעם לפני USB
```bash
cd ~/mirrors/RedisTimeSeries.git
git fetch --prune
```

### במחשב הפנימי — חד-פעמי
```bash
git clone --mirror https://gitlab.your-company.example/your-group/RedisTimeSeries ~/mirrors/RedisTimeSeries.git
cd ~/mirrors/RedisTimeSeries.git
git remote add upstream-mirror /path/to/usb-copy/RedisTimeSeries.git
git config remote.upstream-mirror.fetch '+refs/heads/*:refs/heads/*'
git config --add remote.upstream-mirror.fetch '+refs/tags/*:refs/tags/*'
```

### במחשב הפנימי — כל פעם אחרי USB
```bash
cd ~/mirrors/RedisTimeSeries.git
git fetch --prune upstream-mirror
git push --mirror origin
```

---

## 8. RedisGears (152 קישורים)

| | URL |
|---|---|
| GitHub | `https://github.com/RedisGears/RedisGears` |
| GitLab (פיקטיבי) | `https://gitlab.your-company.example/your-group/RedisGears` |

### במחשב החיצוני — חד-פעמי
```bash
git clone --mirror https://github.com/RedisGears/RedisGears ~/mirrors/RedisGears.git
```

### במחשב החיצוני — כל פעם לפני USB
```bash
cd ~/mirrors/RedisGears.git
git fetch --prune
```

### במחשב הפנימי — חד-פעמי
```bash
git clone --mirror https://gitlab.your-company.example/your-group/RedisGears ~/mirrors/RedisGears.git
cd ~/mirrors/RedisGears.git
git remote add upstream-mirror /path/to/usb-copy/RedisGears.git
git config remote.upstream-mirror.fetch '+refs/heads/*:refs/heads/*'
git config --add remote.upstream-mirror.fetch '+refs/tags/*:refs/tags/*'
```

### במחשב הפנימי — כל פעם אחרי USB
```bash
cd ~/mirrors/RedisGears.git
git fetch --prune upstream-mirror
git push --mirror origin
```

---

## 9. RedisJSON (187 קישורים — כולל וריאציה lowercase)

| | URL |
|---|---|
| GitHub | `https://github.com/RedisJSON/RedisJSON` |
| GitLab (פיקטיבי) | `https://gitlab.your-company.example/your-group/RedisJSON` |

### במחשב החיצוני — חד-פעמי
```bash
git clone --mirror https://github.com/RedisJSON/RedisJSON ~/mirrors/RedisJSON.git
```

### במחשב החיצוני — כל פעם לפני USB
```bash
cd ~/mirrors/RedisJSON.git
git fetch --prune
```

### במחשב הפנימי — חד-פעמי
```bash
git clone --mirror https://gitlab.your-company.example/your-group/RedisJSON ~/mirrors/RedisJSON.git
cd ~/mirrors/RedisJSON.git
git remote add upstream-mirror /path/to/usb-copy/RedisJSON.git
git config remote.upstream-mirror.fetch '+refs/heads/*:refs/heads/*'
git config --add remote.upstream-mirror.fetch '+refs/tags/*:refs/tags/*'
```

### במחשב הפנימי — כל פעם אחרי USB
```bash
cd ~/mirrors/RedisJSON.git
git fetch --prune upstream-mirror
git push --mirror origin
```

---

## 10. RedisBloom (164 קישורים — כולל וריאציה lowercase)

| | URL |
|---|---|
| GitHub | `https://github.com/RedisBloom/RedisBloom` |
| GitLab (פיקטיבי) | `https://gitlab.your-company.example/your-group/RedisBloom` |

### במחשב החיצוני — חד-פעמי
```bash
git clone --mirror https://github.com/RedisBloom/RedisBloom ~/mirrors/RedisBloom.git
```

### במחשב החיצוני — כל פעם לפני USB
```bash
cd ~/mirrors/RedisBloom.git
git fetch --prune
```

### במחשב הפנימי — חד-פעמי
```bash
git clone --mirror https://gitlab.your-company.example/your-group/RedisBloom ~/mirrors/RedisBloom.git
cd ~/mirrors/RedisBloom.git
git remote add upstream-mirror /path/to/usb-copy/RedisBloom.git
git config remote.upstream-mirror.fetch '+refs/heads/*:refs/heads/*'
git config --add remote.upstream-mirror.fetch '+refs/tags/*:refs/tags/*'
```

### במחשב הפנימי — כל פעם אחרי USB
```bash
cd ~/mirrors/RedisBloom.git
git fetch --prune upstream-mirror
git push --mirror origin
```

---

## 11. redis-py (100 קישורים)

| | URL |
|---|---|
| GitHub | `https://github.com/redis/redis-py` |
| GitLab (פיקטיבי) | `https://gitlab.your-company.example/your-group/redis-py` |

### במחשב החיצוני — חד-פעמי
```bash
git clone --mirror https://github.com/redis/redis-py ~/mirrors/redis-py.git
```

### במחשב החיצוני — כל פעם לפני USB
```bash
cd ~/mirrors/redis-py.git
git fetch --prune
```

### במחשב הפנימי — חד-פעמי
```bash
git clone --mirror https://gitlab.your-company.example/your-group/redis-py ~/mirrors/redis-py.git
cd ~/mirrors/redis-py.git
git remote add upstream-mirror /path/to/usb-copy/redis-py.git
git config remote.upstream-mirror.fetch '+refs/heads/*:refs/heads/*'
git config --add remote.upstream-mirror.fetch '+refs/tags/*:refs/tags/*'
```

### במחשב הפנימי — כל פעם אחרי USB
```bash
cd ~/mirrors/redis-py.git
git fetch --prune upstream-mirror
git push --mirror origin
```

---

## 12. prometheus-operator (44 קישורים)

| | URL |
|---|---|
| GitHub | `https://github.com/prometheus-operator/prometheus-operator` |
| GitLab (פיקטיבי) | `https://gitlab.your-company.example/your-group/prometheus-operator` |

### במחשב החיצוני — חד-פעמי
```bash
git clone --mirror https://github.com/prometheus-operator/prometheus-operator ~/mirrors/prometheus-operator.git
```

### במחשב החיצוני — כל פעם לפני USB
```bash
cd ~/mirrors/prometheus-operator.git
git fetch --prune
```

### במחשב הפנימי — חד-פעמי
```bash
git clone --mirror https://gitlab.your-company.example/your-group/prometheus-operator ~/mirrors/prometheus-operator.git
cd ~/mirrors/prometheus-operator.git
git remote add upstream-mirror /path/to/usb-copy/prometheus-operator.git
git config remote.upstream-mirror.fetch '+refs/heads/*:refs/heads/*'
git config --add remote.upstream-mirror.fetch '+refs/tags/*:refs/tags/*'
```

### במחשב הפנימי — כל פעם אחרי USB
```bash
cd ~/mirrors/prometheus-operator.git
git fetch --prune upstream-mirror
git push --mirror origin
```

---

## אחרי שכל 12 ה-mirrors מוכנים — עדכון `values.yaml`

עבור כל repo שהפעלת mirror אצלך, הוסף entry ב-`values.yaml`:

**שים לב:** המפתחות (`k8s-docs`, `observability` וכו') הם השמות מהקטלוג ב-`external-links.yaml` — לא שמות ה-repo המלאים מ-GitHub. הערך של `to` הוא ה-URL המלא ל-project ב-GitLab שלך (כן השם המלא של ה-repo).

העתק את כל הבלוק הבא ל-values.yaml בחברה, החלף רק את `gitlab.your-company.example/your-group` ב-URL האמיתי שלך:

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

**הערה:** ה-keys תחת `gitMirrors` ב-values.yaml חייבים להופיע גם ב-`helm/redis-docs/files/external-links.yaml` תחת `git-mirrors:` כקטלוג. כל 12 ה-entries כבר קיימים בקטלוג של ה-chart — אם מוסיפים repo חדש בעתיד יש להוסיף שם entry מתאים.

לאחר עדכון ה-values:
```bash
helm upgrade <release-name> helm/redis-docs/ -f your-values.yaml
```

**אין צורך ב-image rebuild** — המנגנון כולו ב-runtime ConfigMap.

## בדיקת תקינות

לאחר ה-deploy, פתח דפדפן בסביבה הפנימית, נווט לדף עם קישור ל-GitHub (למשל `content/operate/kubernetes/...`), פתח את ה-DevTools, וודא ש-`<a href>` של הקישור הומר ל-URL של GitLab הפנימי שלך. אם הקישור עדיין מצביע ל-`github.com` — בדוק:

1. ה-`enabled: true` קיים ב-values.yaml.
2. ה-`to` URL מצביע ל-mirror אמיתי (פתח אותו בדפדפן ידנית).
3. ה-key תחת `gitMirrors` תואם בדיוק ל-key בקטלוג `external-links.yaml`.