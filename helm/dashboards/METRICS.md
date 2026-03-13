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
| `nginx_http_request_size_bytes` | Counter | Total received bytes (request) | `method`, `status` |
| `nginx_http_response_time_seconds` | Summary | Response time summary (quantiles) | `method`, `status` |
| `nginx_http_response_time_seconds_hist` | Histogram | Response time histogram (buckets) | `method`, `status` |
| `nginx_http_upstream_time_seconds` | Summary | Upstream response time (reverse proxy only) | `method`, `status` |
| `nginx_http_upstream_time_seconds_hist` | Histogram | Upstream response time histogram (reverse proxy only) | `method`, `status` |

### Histogram Buckets

```
0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10, 15, 30, 60
```

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

Throughput (MB/s):
```promql
sum(rate(nginx_http_response_size_bytes[5m])) / 1024 / 1024
```

### Slow Responses

Requests slower than 5s (per second):
```promql
sum(rate(nginx_http_response_time_seconds_hist_bucket{le="5"}[5m])) - sum(rate(nginx_http_response_time_seconds_hist_bucket{le="60"}[5m]))
```

Percentage of requests slower than 1s:
```promql
(1 - sum(rate(nginx_http_response_time_seconds_hist_bucket{le="1"}[5m])) / sum(rate(nginx_http_response_time_seconds_hist_count[5m]))) * 100
```

Average response size (bytes):
```promql
sum(rate(nginx_http_response_size_bytes[5m])) / sum(rate(nginx_http_response_count_total[5m]))
```
