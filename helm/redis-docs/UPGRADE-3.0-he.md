# מעבר לגרסה 3.0: שני pods וארבעה images

> **[English version](UPGRADE-3.0.md)**

המסמך עוסק רק במעבר מ-2.x ל-3.0. את השאר מתאר [README-he.md](README-he.md).

## מה השתנה

| | 2.x | 3.0 |
|---|---|---|
| **pods** | עד 4: האתר, CLI, חיפוש, מירור | עד 2: האתר (עם המירור), ושירותים (CLI וחיפוש) |
| **image של החיפוש** | בתוך `redis-docs-cli` | `redis-docs-search` נפרד |
| **image של המירור** | `redis-docs:<hash>-mirror-unprivileged` | `redis-docs-mirror:<hash>-unprivileged` |
| **פורט המירור** | 8080 | 8081 (כי הוא יושב עכשיו ליד ה-nginx של האתר) |
| **Redis של החיפוש** | 6379 ב-pod משלו | 6380, ב-pod השירותים ליד ה-Redis של ה-CLI (6379) |
| **Jupyter** (`cli.jupyter`) | sidecar אופציונלי | הוסר |
| **metrics** (`metrics`) | sidecar ‏nginxlog-exporter, ‏Route, ‏ServiceMonitor, דשבורד Grafana | הוסר. לוגים של nginx יוצאים ל-stdout/stderr (`oc logs`) |

## שלב 1: להעביר את ה-images ל-registry הפנימי

אם המירור לא מופעל אצלכם, מדלגים על השורה שלו. אם החיפוש לא מופעל, מדלגים על `redis-docs-search`.

```bash
REG=registry.internal.company.com
HASH=<hash>          # התג של האתר
MIRROR=<mirror-tag>  # התג של המירור עצמו; משתנה רק כשהמירור משתנה

skopeo copy docker://a0533057932/redis-docs:$HASH-unprivileged        docker://$REG/redis-docs:$HASH-unprivileged
skopeo copy docker://a0533057932/redis-docs-mirror:$MIRROR-unprivileged docker://$REG/redis-docs-mirror:$MIRROR-unprivileged
skopeo copy docker://a0533057932/redis-docs-cli:<cli-tag>             docker://$REG/redis-docs-cli:<cli-tag>
skopeo copy docker://a0533057932/redis-docs-search:<search-tag>       docker://$REG/redis-docs-search:<search-tag>
```

את כל התגים לוקחים מ-`helm show chart` של גרסת ה-chart שמתקינים: ה-annotation ‏`artifacthub.io/images` מציג כל image עם התג המקובע שלו. ה-image ‏`redis:8.10.0-alpine` לא השתנה.

**חובה להשתמש ב-image המירור החדש.** ה-image הישן מאזין על 8080, אותו פורט כמו האתר. ב-3.0 שניהם באותו pod, ולכן הקונטיינר נופל עם `nginx: [emerg] still could not bind()`. בבדיקה ה-rolling update השאיר את ה-pod הקודם רץ, כך שהאתר לא נפל, אבל השדרוג לא הושלם.

## שלב 2: לעדכן את קובץ ה-values

**מפתחות שמשנים ערך:**

| מפתח | ישן | חדש |
|---|---|---|
| `mirror.image.name` | `redis-docs` | `redis-docs-mirror` |
| `mirror.image.tag` | `<hash>-mirror-unprivileged` | `<hash>-unprivileged` |
| `search.image.name` | `redis-docs-cli` | `redis-docs-search` |
| `search.image.tag` | זהה ל-`cli.image.tag` | תג משלו, למשל `0.1.0` |

**מפתחות שהוסרו:** Helm מתעלם מהם, ובבדיקה שדרוג עם קובץ values ישן שכולל אותם עבר בלי שגיאה. בכל זאת כדאי למחוק אותם, כדי שהקובץ ישקף את מה שבאמת רץ.

| מפתח | למה הוסר |
|---|---|
| `metrics.*` (כל הבלוק: `enabled`, ‏`image`, ‏`resources`, ‏`route`, ‏`serviceMonitor`) | ה-exporter לא היה בשימוש |
| `cli.jupyter.*` (כל הבלוק) | שרת Jupyter בלי token, בלי סיסמה ובלי הגנת XSRF. הקישורים שנשלחו אליו הם נתיבים של BinderHub, ששרת Jupyter רגיל לא עונה עליהם |
| `mirror.replicas` | המירור הוא קונטיינר ב-pod של האתר, וגדל איתו (`replicaCount` / `autoscaling`) |
| `mirror.containerPort` | קבוע 8081 בשני הווריאנטים של ה-image |
| `search.replicas` | ה-pod של השירותים תמיד replica אחת, בגלל ה-sessions של ה-CLI |

## שלב 3: לשדרג

```bash
helm upgrade redis-docs oci://$REG/redis-docs --version 3.0.1 -f my-values.yaml  # גרסת ה-3.0 הראשונה שפורסמה; כל 3.0.x מאוחרת יותר עובדת אותו דבר
```

**לא להשתמש ב-`--reuse-values` לבד.** הוא שומר את `mirror.image.name: redis-docs` ואת `search.image.name: redis-docs-cli` הישנים. אם בכל זאת משתמשים בו, צריך להוסיף את ארבעת המפתחות מהטבלה של שלב 2 עם `--set`.

**מה קורה בזמן השדרוג:**
- ה-deployments ‏`redis-docs-cli`, ‏`redis-docs-search` ו-`redis-docs-mirror` נמחקים.
- נמחקים גם ה-Service ‏`redis-docs-mirror`, ה-ConfigMap של metrics, ה-Route של metrics וה-ServiceMonitor.
- ‏`redis-docs-services` נוצר, ומתחיל לבנות את אינדקס החיפוש.
- האתר מתעדכן ב-rolling update, בלי השבתה.
- ה-PodDisruptionBudget חל עכשיו רק על ה-pods של האתר. קודם הוא תפס את כל ה-pods של ה-release.
- ה-CLI והחיפוש לא זמינים לדקה-שתיים, עד שה-pod של השירותים מסיים לבנות את האינדקס. בפריסה עם `Recreate` זה קורה בכל שדרוג, לא רק בזה.

## שלב 4: לוודא

```bash
kubectl get deploy,pods
# redis-docs            ‏2/2 (או 1/1 בלי מירור)
# redis-docs-services   ‏4/4 (‏2/2 עם רק CLI או רק חיפוש)

kubectl rollout status deploy/redis-docs-services
kubectl exec deploy/redis-docs-services -c cli-redis    -- redis-cli ACL DRYRUN docsandbox FT._LIST   # OK
kubectl exec deploy/redis-docs-services -c search-redis -- redis-cli -p 6380 FT._LIST                 # docs
```

בדפדפן: דף תיעוד, ‏`/blog/` (אם המירור מופעל), חיפוש, ו-Try it.

## חזרה לאחור

```bash
helm history redis-docs
helm rollback redis-docs <revision-before-3.0>
```

בבדיקה ה-rollback החזיר את ארבעת ה-deployments הישנים. אין נתונים לשמור: האינדקס נבנה מחדש בכל עלייה, וה-Redis של ה-CLI זמני.

## משאבים מומלצים לכל pod

נמדד לכל קונטיינר ב-kind וב-Docker מקומי, על הקורפוס המלא: 7,554 מסמכים, מהם 6,136 תיעוד ו-1,418 מירור. ב-OpenShift, אחרי האינדוקס, ה-pod של האתר השתמש ב-28Mi וה-pod של השירותים ב-222Mi בסך הכל.

| קונטיינר | נמדד | ברירת המחדל (requests → limits) | המלצה |
|---|---|---|---|
| **pod 1: `redis-docs`** | | | |
| `redis-docs` (nginx) | ‏22Mi | ‏`250m/256Mi → 1/512Mi` | ברירת המחדל. ה-init containers של `canonicalURL` ושל ה-downloads רצים עם אותם משאבים |
| `mirror` | ‏11Mi | ‏`50m/64Mi → 500m/256Mi` | ברירת המחדל |
| **סה"כ pod 1** | | ‏`300m/320Mi → 1.5/768Mi` | |
| **pod 2: `redis-docs-services`** | | | |
| `cli-proxy` | ‏39Mi | ‏`50m/64Mi → 200m/128Mi` | ברירת המחדל |
| `cli-redis` | ‏7Mi ריק, גדל לפי מה שקוראים כותבים | ‏`50m/64Mi → 200m/128Mi` | ברירת המחדל. ההגבלה היא מה שעוצר קורא שממלא את ה-sandbox |
| `search-api` | ‏40Mi, ושיא של 125Mi וליבה אחת בזמן אינדוקס | ‏`100m/128Mi → 500m/512Mi` | ברירת המחדל. עם limit של `500m`, האינדוקס פשוט לוקח קצת יותר זמן |
| `search-redis` | ‏135–156Mi אחרי אינדוקס | ‏`100m/512Mi → 500m/1Gi` | אפשר להוריד ל-`100m/256Mi → 500m/512Mi`. אם לא, להשאיר, כי הקורפוס גדל עם כל גרסת תיעוד |
| **סה"כ pod 2 (ברירת מחדל)** | | ‏`300m/768Mi → 1.4/1.75Gi` | |

סך הכל, בפריסה עם הכל מופעל: ‏requests של `600m` ו-`~1.1Gi`, ו-limits של `2.9` ליבות ו-`~2.5Gi`.

**מכסת pods:** בזמן שדרוג, האתר (rolling update) מרים זמנית pod נוסף אחד. השירותים (`Recreate`) לא. לכן, עם `replicaCount: 1` והכל מופעל, צריך מכסה של 3 pods: שניים קבועים, ועוד אחד זמני לאתר.
