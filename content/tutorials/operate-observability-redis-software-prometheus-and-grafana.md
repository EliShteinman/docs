---
title: "Redis Software Observability with Prometheus and Grafana"
linkTitle: "Redis Software Observability with Prometheus and Grafana"
url: "/tutorials/operate/observability/redis-software-prometheus-and-grafana/"
description: "How do you monitor Redis Software with Prometheus and Grafana? Deploy a turnkey observability stack that scrapes Redis metrics via the v2 Metrics Stream Engine, visualizes them in pre-built Grafana..."
group: "For operators"
aliases:
- "/tutorials/operate-observability-redis-software-prometheus-and-grafana/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

How do you monitor Redis Software with Prometheus and Grafana? Deploy a turnkey observability stack that scrapes Redis metrics via the v2 Metrics Stream Engine, visualizes them in pre-built Grafana dashboards, and alerts you to issues before they impact your applications.

This tutorial walks you through the full setup in about an hour and is aimed at system administrators and DevOps professionals running Redis Software.

## What you'll learn

- How to deploy a Prometheus and Grafana monitoring stack for Redis Software
- How to read and interpret Redis Software v2 metrics and dashboards
- How to configure alerting rules in Prometheus for Redis performance and availability
- How to build custom Grafana dashboards with advanced Redis metrics

> **NOTE**
>
> This tutorial relies on an existing Redis Software instance. You may follow our [quickstart guide](https://redis.io/docs/latest/operate/rs/installing-upgrading/quickstarts/docker-quickstart/) for testing environments or our [installation documentation](https://redis.io/docs/latest/operate/rs/installing-upgrading/) for production environments.

## Prerequisites

- A running Redis Software v7.8.2+ instance (required for v2 metrics support)
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed
- Network access to your Redis Software cluster (port 8070 must be reachable)
- Your Redis Software cluster FQDN
- Intermediate familiarity with Redis and enterprise-grade infrastructure

## How do you set up the Redis monitoring stack?

The Redis Field Engineering team provides a turnkey solution that sets up Prometheus + Grafana with pre-configured dashboards. You can quickly set it up by running the following commands:

```bash
# Clone the repository
git clone https://github.com/redis-field-engineering/redis-enterprise-observability.git

# Navigate to the v2 kickstart directory
cd redis-enterprise-observability/grafana_v2/kickstart_v2

# Run the setup script with your cluster FQDN, the dashboard directory, and password
./setup.sh your-cluster-fqdn.example.com ../dashboards/grafana_v9-11/software/basic very-secret-password
```

> **NOTE**
>
> You must use `very-secret-password` in the setup script above. If you use a different password, the script won't run properly. This password is configured in the `docker-compose.yml` file.

This script automatically:

- Configures Prometheus to scrape v2 metrics from your cluster
- Deploys Grafana with Redis Software dashboards
- Sets up the complete monitoring stack via Docker Compose

## How do you access the monitoring stack?

After the setup completes:

1.  **Grafana**: http://localhost:3000 (user: admin, pass: very-secret-password)
2.  **Prometheus**: http://localhost:9090

### How do you verify Prometheus is scraping Redis metrics?

1\. Check that Prometheus is collecting metrics:

- Go to http://localhost:9090/targets
- redis-v1 and redis-v2 should show as "UP"

![Prometheus targets page showing redis-v1 and redis-v2 endpoints with status UP and last scrape time](/images/site-mirror/1fa57157dd06fa18ff9904dcf0955a6d93c63007-1340x410.webp)

2\. View your dashboards in Grafana:

- Sign in using **user**: admin, **pass**: very-secret-password
- Navigate to Dashboards
- Open "Cluster Status Dashboard" or other dashboards
- Verify data is populating

To see the metrics as they start to come in, you may want to make the time range smaller in the top right of the dashboard, e.g. "Last 5 Minutes".

![Grafana Cluster Status Dashboard displaying ops/sec, latency, memory usage, and key count graphs with active data](/images/site-mirror/f3040798a5de11a3fbd38d38d4fcfe204d98f776-1374x537.webp)

### What is the difference between v1 and v2 Redis metrics?

This setup uses Redis Software Metrics Stream Engine. Below, you can compare features between the original Metrics v1 and v2.

| Feature                    | Metrics v1           | Metrics v2                       |
| -------------------------- | -------------------- | -------------------------------- |
| **Precision**              | Millisecond averages | Microsecond histograms           |
| **Real-time**              | Snapshot-based       | Stream-based                     |
| **Maintenance visibility** | Limited              | Full visibility during failovers |
| **Required version**       | Any                  | v7.8.2+                          |

**Why v2 matters**: Real-time monitoring with sub-millisecond precision and visibility during all operations, including maintenance windows.

### How do you calculate latency with v2 metrics?

**V1 approach** (snapshot-based):

```sql
# V1 provided pre-calculated averages
bdb_avg_latency
```

**V2 approach** (stream-based with PromQL):

```sql
# V2 requires calculation from histogram data per millisecond
histogram_quantile(0.95, sum by (le, db) (irate(endpoint_read_requests_latency_histogram_bucket[1m]))) / 1000
```

The metrics take a couple minutes to come into Prometheus. If you're seeing no data and you're sure you're getting read requests, wait a few minutes and refresh or increase the time window, e.g. 1m -> 5m.

The v2 metrics stream engine provides finer-grained control over metric queries, including the ability to filter or aggregate results by quantile — for example, extracting the p95 (95th percentile) latency metric for specific operations.

This update gives you greater flexibility and precision in querying metrics, leveraging [PromQL aggregation functions](https://prometheus.io/docs/prometheus/latest/querying/basics/) for powerful custom analysis.

![Prometheus query interface showing the p95 read latency PromQL formula with a result value of 0.127](/images/site-mirror/d56afe07851da77433600e396ccb658c23b7845c-1000x410.webp)

### How do you migrate from v1 to v2 metrics?

For a comparison of queries if you're looking to move from V1 to V2, check out our [Transition from Prometheus v1 to Prometheus v2 documentation](https://redis.io/docs/latest/operate/rs/references/metrics/prometheus-metrics-v1-to-v2/)

## How do you read and understand your Redis dashboards?

Let's dive into what the key metrics mean and how to interpret dashboard data for operational decision-making.

Your monitoring stack includes several pre-built dashboards. Here's what to focus on:

### Which dashboards should you monitor first?

Below are three important dashboards to get familiar with:

**Cluster status dashboard** - Your starting point for cluster health:

- Database count and status
- Overall resource utilization (used memory, memory usage)
- High-level performance indicators (total ops/sec, average latency, key count)

**Database status dashboard** - Application-focused metrics:

- Per-database performance (latency, throughput, error rates by database)
- Memory utilization
- Connection patterns (active connections, connection rate changes)

![Grafana Database Status Dashboard showing per-database latency, throughput, memory utilization, and connection graphs](/images/site-mirror/2d3365056e48b19382fec8bd041f39228aca3a51-1348x736.webp)

**Node dashboard** - Infrastructure details:

- Shard & database counts
- CPU, memory, and network per node (individual machine resource usage)
- System-level health indicators (OS metrics, file descriptors, disk I/O)

![Grafana Node Dashboard displaying per-node CPU, memory, network throughput, and shard count panels](/images/site-mirror/3c9ba9bff72e3e04f4c8cabd3eec27077e8dce92-1361x515.webp)

### What Redis metrics should you monitor?

#### Memory utilization

Memory utilization can be calculated using the following v2 [metrics](https://redis.io/docs/latest/operate/rs/references/metrics/prometheus-metrics-v2/) in Prometheus or Grafana.

```sql
# Memory utilization percentage per shard
avg by (cluster,db,redis)(redis_server_used_memory) / avg by (cluster,db,redis)(redis_server_maxmemory) * 100

# Database-level memory utilization (aggregated across shards)
sum by (cluster,db)(redis_server_used_memory{role="master"}) / (avg by(cluster,db)(db_memory_limit_bytes) / max by(cluster,db)(db_replication_factor))
```

What to look for:

- **Caching workloads**: Safe up to 100% (relies on evictions)
- **Non-caching workloads**: Alert at 80%, critical at 90%
- **Trend analysis:** Steady growth vs. sudden spikes

#### Latency performance

Latency performance can be calculated using the following [metrics](https://redis.io/docs/latest/operate/rs/references/metrics/prometheus-metrics-v2/) in Prometheus or Grafana.

```sql
# 95th percentile read latency (milliseconds)
histogram_quantile(0.95, sum by (le, db) (irate(endpoint_read_requests_latency_histogram_bucket[1m]))) / 1000

# 95th percentile write latency (milliseconds)
histogram_quantile(0.95, sum by (le, db) (irate(endpoint_write_requests_latency_histogram_bucket[1m]))) / 1000

# Combined 95th percentile latency for all operations (milliseconds)
histogram_quantile(0.95, sum by (le, db) (
  irate(endpoint_read_requests_latency_histogram_bucket[1m]) +
  irate(endpoint_write_requests_latency_histogram_bucket[1m]) +
  irate(endpoint_other_requests_latency_histogram_bucket[1m])
)) / 1000
```

Example performance targets

- **Excellent**: <0.5ms
- **Good**: 0.5-1ms
- **Investigate**: >1ms
- **Critical**: >4ms

> **NOTE**
>
> These targets are based on typical Redis Software performance. Your specific thresholds may vary based on network, hardware, and app requirements.

#### CPU utilization

Redis Software monitors CPU at three levels:

1.  The shard CPU which tracks individual Redis processes (single-threaded)
2.  The proxy CPU which monitors the multi-threaded connection routing processes
3.  The node CPU which shows overall system utilization.

Since Redis shards are single-threaded, a high shard CPU utilization often indicates hot keys or data distribution problems, while a high proxy CPU utilization suggests connection issues. You'll need to establish appropriate thresholds based on your specific environment and performance requirements.

### What should you watch out for?

**Hot keys** - One shard has a high CPU utilization while others are idle:

- **Symptom**: Uneven CPU distribution across shards
- **Impact**: Single-threaded bottleneck
- **Solution**: Distribute keys, implement app caching

**Large keys** - High network utilization with CPU spikes:

- **Symptom**: Network traffic spikes correlating with CPU
- **Impact**: Bandwidth and processing bottlenecks
- **Solution**: Break large values into smaller keys

**Slow operations** - Commands taking excessive time:

- **Symptom**: Latency spikes with specific operation types
- **Impact**: Overall performance degradation
- **Solution**: Optimize queries, avoid O(n) operations like `KEYS`

### How do you analyze cache performance?

For caching workloads, monitor:

```sql
# Cache read hit ratio (database level), can also be done for writes
(
  sum by (db) (irate(redis_server_keyspace_read_hits{role="master"}[1m])) /
  (sum by (db) (irate(redis_server_keyspace_read_hits{role="master"}[1m])) +
   sum by (db) (irate(redis_server_keyspace_read_misses{role="master"}[1m])))
) * 100
```

Suggested target ranges:

- **Excellent**: >90% hit ratio
- **Good**: 70-90%
- **Needs attention**: <70%

Resources:

If you're looking to dive deeper, the following resources explain these metrics in greater detail.

- [Redis Software developer observability playbook](/tutorials/redis-software-observability-playbook) - Comprehensive analysis techniques
- [Redis Software observability guide](https://redis.io/docs/latest/integrate/prometheus-with-redis-enterprise/observability/) - Detailed metric explanations

## How do you set up alerting for Redis?

We can also set up intelligent alerts that notify you before issues impact apps. The setup script that we ran earlier added Prometheus [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/) and it's been populated with Redis-specific alert rules.

There are three primary suggested areas of monitoring and alerting:

1.  **Performance alerts:** These alerts monitor latency, CPU utilization, and memory pressure to detect degradation before it impacts apps.
2.  **Availability alerts:** These alerts provide immediate notifications for critical failures like node outages or shard unavailability.
3.  **Capacity alerts:** These alerts use predictive monitoring to warn about approaching resource limits before they cause problems. They are designed to escalate from 'warning' to 'critical,' based on severity, giving you time to respond before issues affect your users.

Alerts will appear in the Prometheus console under the Alerts tab.

![Prometheus Alerts tab showing a firing RedisHighReadLatency alert with severity label and annotation details](/images/site-mirror/fa610c9ebfd80868bd7a6526cf726df9be23af54-1489x686.webp)

### How do you configure Redis alert rules?

The alerts used for this tutorial can be found at `redis-enterprise-observability/prometheus_v2/rules/alerts.yml`. If you'd like to test edits, you'll need to bring down the `dashboard` Docker container and run the setup script again.

Here's an example alert for high latency:

```yaml
# Example: High read latency alert
- alert: RedisHighReadLatency
  expr: histogram_quantile(0.95, sum by (le, db) (irate(endpoint_read_requests_latency_histogram_bucket[1m]))) / 1000 > 1
  for: 2m
  labels:
      severity: warning
  annotations:
      summary: 'Redis database {{ $labels.db }} has high read latency'
      description: '95th percentile read latency is {{ $value }}s'
```

Once you have an alert like the one above, you'll then need to add the file name to the `rule_files` section of the `prometheus.yml` file to see the alerts in action. See these in the Prometheus console under the Alerts tab.

### How do you send Redis alert notifications?

You can also configure Alertmanager for your notification channels, such as Slack, PagerDuty, Email, etc. Here's an example of what a notification might look like:

```yaml
# alertmanager.yml example
receivers:
- name: 'slack-alerts'
 slack_configs:
 - api_url: 'YOUR_SLACK_WEBHOOK'
   channel: '#redis-alerts'
   title: 'Redis Software Alert'
   text: 'Alert: {{ .GroupLabels.alertname }}'

- name: 'email-alerts'
 email_configs:
 - to: 'ops-team@company.com'
   subject: 'Redis Software Alert'
```

Prevent false positives

- Use appropriate `for` durations (2-5 minutes for most alerts)
- Set minimum traffic thresholds for meaningful alerts
- Use `avg_over_time()` for noisy metrics

Resources

To dive deeper, check out the following resources on alerting:

- [Prometheus Alerting docs](https://prometheus.io/docs/alerting/) - Complete alerting guide

## How do you build custom Redis dashboards?

Lastly, let's get familiar with what's possible with custom dashboards and v2 metrics for specialized monitoring needs.

### What v2 metrics are available for custom dashboards?

Redis Software v2 metrics (available in v7.8.2+) provide comprehensive monitoring capabilities. Note: V2 metrics are currently in preview with a partial list available.

You can test some of these queries in Prometheus to see their outputs.

Database endpoint monitoring

```sql
# Client connection tracking (rates for meaningful metrics)
irate(endpoint_client_connections[1m])
irate(endpoint_client_disconnections[1m])
irate(endpoint_client_connection_expired[1m])
irate(endpoint_client_establishment_failures[1m])

# Number of active connections to Redis database
endpoint_client_connections - endpoint_client_disconnections - endpoint_proxy_disconnections

# Request rates by type
irate(endpoint_read_requests[1m])
irate(endpoint_write_requests[1m])
```

Node resource monitoring

```sql
# Available system resources
node_available_flash_bytes
node_available_memory_bytes

# Node health and certificate monitoring
node_metrics_up
node_cert_expires_in_seconds

# Network throughput
irate(node_network_receive_bytes_total[1m])
```

Cluster status tracking

```sql
# Cluster health indicators
generation
has_quorum
is_primary
```

Replication monitoring

```sql
# Replication data flow
irate(database_syncer_ingress_bytes[1m])

# Sync status tracking
database_syncer_current_status{syncer_type="replicaof"}
```

Redis shard performance

```sql
# Memory and processing
redis_server_used_memory
irate(redis_server_total_commands_processed[5m])  # Commands per second

# Shard health
redis_server_up

# CPU usage (via node_exporter)
irate(namedprocess_namegroup_thread_cpu_seconds_total{mode=~"system|user"}[1m])
```

### What advanced Grafana features can you use with Redis?

Grafana provides several powerful features for creating sophisticated Redis Software dashboards:

- [**Template Variables**](https://grafana.com/docs/grafana/latest/dashboards/variables/)**:** These variables allow you to create dynamic dashboards that can filter by cluster, database, or time range.
- [**Heat Maps**](https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/heatmap/)**:** These maps can visualize latency distribution over time using v2 histogram metrics.
- [**Annotations**](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/annotate-visualizations/)**:** These let you mark deployment events or maintenance windows on your charts.

Resources

- [V2 Metrics Complete Reference](https://redis.io/docs/latest/integrate/prometheus-with-redis-enterprise/prometheus-metrics-definitions/) - All available v2 metrics
- [Grafana Dashboard Best Practices](https://grafana.com/docs/grafana/latest/dashboards/) - Dashboard design guidance
- [PromQL Tutorial](https://prometheus.io/docs/prometheus/latest/querying/basics/) - Query language reference

## Next steps

Throughout this tutorial, you deployed a complete Redis Software monitoring stack with Prometheus and Grafana, learned how to interpret key Redis metrics and dashboards, configured proactive alerting rules, and explored advanced monitoring with v2 metrics.

To continue building your Redis observability skills:

- [Monitor Redis with Datadog](/tutorials/operate/observability/datadog/) - Set up Redis monitoring using Datadog as an alternative to Prometheus and Grafana
- [Add Redis as a Grafana datasource](/tutorials/operate/observability/redisdatasource/) - Query Redis data directly from Grafana dashboards for custom analytics

### Additional resources

Official docs

- [Redis Software Monitoring Overview](https://redis.io/docs/latest/operate/rs/monitoring/) - Complete monitoring guide
- [Metrics Stream Engine](https://redis.io/docs/latest/operate/rs/monitoring/metrics_stream_engine/) - V2 metrics architecture
- [Transition from Prometheus v1 to Prometheus v2 documentation](https://redis.io/docs/latest/operate/rs/references/metrics/prometheus-metrics-v1-to-v2/)

Learning & certification

- [Redis University - Get Started with Redis Software](https://university.redis.io/learningpath/an0mgw5bjpjfbe?tab=details) - Free courses about all things Redis, including Redis Software
- [Redis Developer Hub](https://redis.io/dev) - Find other tutorials, client libraries, videos and dev events

Community support

- [Redis Discord](https://discord.gg/redis) - Active community discussions
- [GitHub Issues](https://github.com/redis-field-engineering/redis-enterprise-observability/issues) - Report bugs or request features for this repo

### Extending your setup

Production considerations

- Configure persistent storage for Prometheus data
- Set up high availability for monitoring infrastructure
- Implement proper authentication and TLS
- Plan retention policies for metrics data

Advanced integrations

- Connect to existing SIEM systems
- Integrate with incident management (PagerDuty, OpsGenie)
- Add business logic metrics and custom exporters
- Implement automated capacity scaling based on metrics

Your Redis Software observability foundation is now in place. The monitoring stack can grow with your deployment and provide continuous insights into your Redis operations.

[Reach out to the Redis team](https://redis.io/meeting/) if you're looking for help expanding further.
