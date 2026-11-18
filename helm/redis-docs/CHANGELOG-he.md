# יומן שינויים

> **[English version](CHANGELOG.md)**

מה השתנה בכל גרסה של ה-chart, ומה לשנות ב-values בזמן שדרוג.
ה-CI מפרסם כל גרסה עם העלאה של הספרה האחרונה. סדרת minor חדשה מתחילה ב-`.1`, כי ה-build
מעלה את הספרה האחרונה של הגרסה שכתובה ב-`Chart.yaml`.

## 3.2.0

### נדרשת פעולה

- **רק אם הגדרתם את `externalLinks.gitMirrors`:** עד עכשיו, entry בשם שלא מופיע ב-`files/external-links.yaml`
  נבלע בשקט. עכשיו הוא מכשיל את ההתקנה עם הודעה, אלא אם ה-entry מציין `repo: <owner>/<name>`.
  entries עם שמות מהקטלוג ממשיכים לעבוד כמו קודם.
- **רק אם ערכתם את `files/external-links.yaml` בעותק של ה-chart:** ‏entry תחת `git-mirrors` מציין
  עכשיו את ה-repo עם `repo: <owner>/<name>` (ועם `aliases`), ולא עם כתובת `from`.

### שינויים

- **קישורי ה-mirrors מותאמים לפי שם ה-repo המלא.** קודם `redis/redis` תפס כל קישור שמתחיל בו, ולכן
  קישורים ל-`redis/redis-py`, ל-`redis/redis-om-*` ול-`redis/redisinsight` נשלחו לעותק של redis.
  עכשיו הם נשלחים לעותק שלהם, או נשארים ב-GitHub.
- **קישורים למה שאין בעותק ב-GitLab נשארים ב-GitHub:** ‏pull requests, ‏issues, ‏discussions,
  ‏security advisories, ‏wiki ו-Actions. קודם הם נשלחו לדף ב-GitLab שלא קיים.
- **קישורי releases מקבלים את הצורה של GitLab:** ‏`releases/latest` הופך ל-`/-/releases/permalink/latest`,
  ו-`releases/download/<tag>/<file>` הופך ל-`/-/releases/<tag>/downloads/<file>`. טווח שורות
  `#L10-L20` הופך ל-`#L10-20`.
- **גם קישורים שנוספים לדף אחרי שהוא נטען מקבלים את ההפניה.**

### נוסף

- **34 repos בקטלוג ה-mirrors** (במקום 12), כולם כבויים כברירת מחדל: ספריות הלקוח, ‏`redis/docs`,
  ‏redisctl, ‏RIOT-X, ה-tutorials של Redis Insight, שרת Arrow Flight, דרייבר ה-ADBC והפלאגין של Grafana.
  כל entry מזהה גם שמות ישנים ש-GitHub עדיין מפנה מהם, כמו `RedisInsight/RedisInsight`, שעבר
  ל-`redis/RedisInsight`.
- **את העותקים עצמם** יוצרים עם `scripts/airgap-mirrors`, שגם כותב בשבילכם את ה-values של
  `gitMirrors`. ראו `MIRRORS-SETUP-he.md`.

אין images חדשים ואין פורטים חדשים. ‏`appVersion` וכל ה-tags של ה-images לא השתנו.

## 3.1.1

### נדרשת פעולה

- **למחוק את `externalLinks.overrides.nav-mobile-menu` מה-values, אם הוא קיים.** המפתח כבר
  לא קיים. override עבורו לא נקרא, כך שהשארתו לא שוברת את ההתקנה, אבל הוא לא עושה כלום.
- **למחוק את `externalLinks.families.header.sub-families.mobile` מה-values, אם הוא קיים.**
  תת-המשפחה כבר לא קיימת, מאותה סיבה.

### שינויים

- **תפריט הנייד (ההמבורגר) מוצג תמיד.** קודם הוא היה חלק מקטלוג הקישורים החיצוניים בשם
  `nav-mobile-menu`, ולכן עם `externalLinks.enabled: false` הוא הוסתר, יחד עם הדפים הפנימיים
  שבתוכו. עכשיו הוא נפתח עם Redis Iris, ‏Redis install, ‏Data types, ‏Tools ו-Community. הפריטים
  החיצוניים שבתוכו (Docs, ‏Sign up, ‏Login) נשארים עם המפתחות שלהם (`nav-docs`,
  `nav-try-redis`, `nav-login`), ומוסתרים כל עוד המפתחות האלה כבויים.
- **התפריט העליון המלא מופיע מרוחב 1280 פיקסלים, לא מ-1024** (שינוי של upstream). מתחת ל-1280
  הכותרת מציגה את הלוגו ואת ההמבורגר. תפריט "More from Redis" של ה-fork עובר לאותה נקודת שבירה.

### נוסף

- **התיעוד של Redis Iris** (upstream): ‏Agent Memory, ‏Context Gateway, ‏Intent Router,
  ‏Agent Playbooks ו-Lens, תחת `/develop/ai/context-engine/` ו-`/operate/iris/`.
  LangCache עבר מ-`/develop/ai/context-engine/langcache/` ל-`/develop/ai/langcache/`.
  הכתובות הישנות מפנות לחדשות.

אין images, ‏values או פורטים חדשים.
