# Redis Docs - Nginx Metrics Reference

## Exporter

**Image:** `quay.io/martinhelmich/prometheus-nginxlog-exporter:v1.11.0`
**Port:** 4040
**Endpoint:** `/metrics`

## Available Metrics

| Metric | Type | Description | Labels |
|---|---|---|---|
| `nginx_http_response_count_total` | Counter | Total processed HTTP requests | `method`, `status` |
| `nginx_http_response_size_bytes` | Counter | Total transferred bytes (response) | `method`, `status` |
| `nginx_http_response_time_seconds` | Summary | Response time summary (quantiles p50/p90/p99) | `method`, `status` |
| `nginx_http_response_time_seconds_hist` | Histogram | Response time histogram (buckets) | `method`, `status` |
| `nginx_parse_errors_total` | Counter | Log lines that could not be parsed | — |

### Histogram Buckets

```
0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10, 15, 30, 60
```

## Grafana Dashboard

קובץ: `redis-docs-nginx.json`

בייבוא הדשבורד, Grafana תבקש:
- **Datasource** — מקור הנתונים (Prometheus / Thanos)
- **Job** — שם ה-job שמוגדר לגרידת המטריקות

### Overview (שורה עליונה)

| פאנל | סוג | תיאור |
|---|---|---|
| Requests / sec | Stat | קצב בקשות נוכחי (ירוק < 50, צהוב < 100, אדום > 100) |
| Avg Response Time | Stat | זמן תגובה ממוצע (ירוק < 0.5s, צהוב < 1s, אדום > 1s) |
| Error Rate (5xx) | Stat | אחוז שגיאות שרת (ירוק < 1%, צהוב < 5%, אדום > 5%) |
| Throughput | Stat | תעבורת תגובות (bytes/sec, סקאלה אוטומטית) |

### Response Time (שורה שנייה)

| פאנל | סוג | תיאור |
|---|---|---|
| Response Time (avg / p90 / p99) | Time series | שלושה קווים — ממוצע, אחוזון 90, אחוזון 99 |
| Response Time Distribution | Heatmap | התפלגות זמני תגובה לפי buckets (צבע כהה = יותר בקשות) |

### Requests (שורה שלישית)

| פאנל | סוג | תיאור |
|---|---|---|
| Requests / sec by Status Code | Time series | קצב בקשות מפוצל לפי קוד תגובה (200, 301, 404, 5xx) |
| Requests / sec by Method | Time series | קצב בקשות מפוצל לפי HTTP method (GET, POST) |

### Errors & Traffic (שורה תחתונה)

| פאנל | סוג | תיאור |
|---|---|---|
| Error Rate % | Time series | אחוז שגיאות לאורך זמן (5xx + 404 בנפרד) |
| Throughput | Time series | תעבורת תגובות לאורך זמן (bytes/sec) |
| Status Code Distribution (1h) | Pie chart | התפלגות קודי תגובה בשעה האחרונה (donut) |

## PromQL Queries

### Response Time

Average response time:
```promql
sum(rate(nginx_http_response_time_seconds_sum[5m])) / sum(rate(nginx_http_response_time_seconds_count[5m]))
```

P90 response time:
```promql
histogram_quantile(0.90, sum(rate(nginx_http_response_time_seconds_hist_bucket[5m])) by (le))
```

P99 response time:
```promql
histogram_quantile(0.99, sum(rate(nginx_http_response_time_seconds_hist_bucket[5m])) by (le))
```

### Requests

Requests per second (total):
```promql
sum(rate(nginx_http_response_count_total[1m]))
```

Requests per second by status code:
```promql
sum(rate(nginx_http_response_count_total[1m])) by (status)
```

### Errors

Error rate (5xx percentage):
```promql
sum(rate(nginx_http_response_count_total{status=~"5.."}[5m])) / sum(rate(nginx_http_response_count_total[5m])) * 100
```

404 rate (percentage):
```promql
sum(rate(nginx_http_response_count_total{status="404"}[5m])) / sum(rate(nginx_http_response_count_total[5m])) * 100
```

### Traffic

Throughput (bytes/sec):
```promql
sum(rate(nginx_http_response_size_bytes[5m]))
```

Average response size (bytes):
```promql
sum(rate(nginx_http_response_size_bytes[5m])) / sum(rate(nginx_http_response_count_total[5m]))
```

### Slow Responses

Requests slower than 5s (per second):
```promql
sum(rate(nginx_http_response_time_seconds_hist_count[5m])) - sum(rate(nginx_http_response_time_seconds_hist_bucket{le="5"}[5m]))
```

Percentage of requests slower than 1s:
```promql
(1 - sum(rate(nginx_http_response_time_seconds_hist_bucket{le="1"}[5m])) / sum(rate(nginx_http_response_time_seconds_hist_count[5m]))) * 100
```
