# יומן שינויים

> **[English version](CHANGELOG.md)**

מה השתנה בכל גרסה של ה-chart, ומה לשנות ב-values בזמן שדרוג.
ה-CI מפרסם כל גרסה עם העלאה של הספרה האחרונה. סדרת minor חדשה מתחילה ב-`.1`, כי ה-build
מעלה את הספרה האחרונה של הגרסה שכתובה ב-`Chart.yaml`.

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
