---
title: "Redis Observability: Monitoring, Metrics, and Troubleshooting"
linkTitle: "Redis Observability: Monitoring, Metrics, and Troubleshooting"
url: "/tutorials/operate/redis-at-scale/observability/"
description: "This tutorial is part of the Running Redis at Scale course. You can jump to any section:"
group: "For operators"
aliases:
- "/tutorials/operate-redis-at-scale-observability/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> Monitor Redis in production using the built-in `INFO` command for real-time metrics (memory, clients, throughput), `SLOWLOG` to catch slow queries, the latency monitoring framework for spike detection, and external tools like [Datadog](/tutorials/operate/observability/datadog/) or [Prometheus with Grafana](/tutorials/operate/observability/redis-software-prometheus-and-grafana/) for dashboards and alerting.

## Course Structure

This tutorial is part of the **Running Redis at Scale** course. You can jump to any section:

1. [Introduction to Running Redis at Scale](/tutorials/operate/redis-at-scale/)
2. [Talking to Redis](/tutorials/operate/redis-at-scale/talking-to-redis/) - CLI, clients, and tuning
3. [Persistence and Durability](/tutorials/operate/redis-at-scale/persistence-and-durability/) - RDB and AOF
4. [High Availability](/tutorials/operate/redis-at-scale/high-availability/) - Replication and Sentinel
5. [Scalability](/tutorials/operate/redis-at-scale/scalability/) - Redis Cluster
6. **Observability** ← You are here
7. [Course Conclusion](/tutorials/operate/redis-at-scale/course-wrap-up/)

---

## What you'll learn

- How to use the Redis `INFO` command to inspect server, memory, replication, and keyspace metrics
- How to measure latency with `redis-cli` options like `--latency`, `--latency-history`, and `--latency-dist`
- How to configure and query the Redis Slow Log to find expensive commands
- How to enable the latency monitoring framework and interpret its output
- How to identify problematic keys with `--bigkeys`, `--memkeys`, and `--hotkeys`
- How to set up Redis log files and forward them to a remote logging server
- How to connect Redis metrics to external monitoring tools for production dashboards

---

[YouTube: https://www.youtube.com/watch?v=hO1AGE3I_bU](https://www.youtube.com/watch?v=hO1AGE3I_bU)

The last thing you want to do after successfully deploying and scaling Redis is to be stuck working on the weekend because performance is down or the service is unavailable!

If you're running a managed service like Redis Cloud, you won't have to worry about these questions as much. But even then, it's still worthwhile to know about certain key Redis metrics.

Some of the questions you always want to be able to answer include:

- Is Redis up and running right now?
- Where is my Redis capacity at?
- Is Redis accessible at this moment?
- Is Redis performing the way we expect?
- When failures occur… what exactly happened to Redis?

Then of course you must ask...

- **How can I find this out ahead of time?**

Let's dig into these questions and more as we look into observability with Redis.

---

## What metrics does Redis expose for monitoring?

There are several Redis metrics that can be viewed through `redis-cli`.

### How do I use the Redis INFO command?

Running the `INFO` command provides many of the metrics available in a single view.

```bash
127.0.0.1:6379> INFO
# Server
redis_version:6.0.1
redis_git_sha1:00000000
redis_git_dirty:0
redis_build_id:e02d1d807e41d65
redis_mode:standalone
os:Linux 4.19.121-linuxkit x86_64
…
```

There are several sections that can be pulled individually. For example, if you wanted to just get the CLIENTS section you can pass that section as an argument to the `INFO` command.

```bash
127.0.0.1:6379> INFO CLIENTS
# Clients
connected_clients:1
client_recent_max_input_buffer:2
client_recent_max_output_buffer:0
blocked_clients:0
tracking_clients:0
clients_in_timeout_table:0
```

### INFO Sections

### Server\*\*: the current Redis server inf

Metrics of note:

- `redis_version`
- `process_id`
- `config_file`
- `uptime_in_seconds`
- `uptime_in_days`

### Clients\*\*: available data on clients connected or failed connection

Metrics of note:

- `connected_clients`
- `blocked_clients`

### Memory\*\*: memory usage and sta

Metrics of note:

- `used_memory`
- `mem_fragmentation_ratio`

### Persistence\*\*: RDB or AOF metri

Metrics of note:

- `rdb_last_save_time`
- `rdb_changes_since_last_save`
- `aof_rewrite_in_progress`

### Stats\*\*: some general statisti

Metrics of note:

- `keyspace_hits`
- `keyspace_misses`
- `expired_keys`
- `evicted_keys`
- `instantaneous_ops_per_sec`

### Replication\*\*: replication data including primary/replica identifiers and offse

Metrics of note:

- `master_link_down_since`
- `connected_slaves`
- `master_last_io_seconds_ago`

### CPU\*\*: compute consumption sta

Metrics of note:

- `used_cpu_sys`
- `used_cpu_user`

### Modules\*\*: data from any loaded modul

Metrics of note (per module):

- `ver`
- `options`

### Cluster\*\*: whether cluster is enabl

Metric of note:

- `cluster_enabled`

### Keyspace\*\*: keys and expiration da

Metrics of note (per db):

- `keys`
- `expires`
- `avg_ttl`

The output can be read from the results or piped into a file.

```bash
127.0.0.1:6379> redis-cli INFO STATS > redis-info-stats
```

This could be done at intervals and consumed by a local or third party monitoring service.

Some of the data returned by `INFO` are going to be static. For example the Redis version which won't change until an update is made. Other data is dynamic, for `keyspace_hits ÷ keyspace_misses`. The latter could be taken to compute a hit ratio and observed as a long term metric. The replication section field `master_link_down_since` could be a metric to connect an alert.

Some examples of possible alerts that could be setup for a given metric:

| **Metric**               | Example Alert                                            |
| ------------------------ | -------------------------------------------------------- |
| `uptime_in_seconds`      | < 300 seconds: to ensure the server is staying up        |
| `connected_clients`      | < minimum number of expected application connections     |
| `master_link_down_since` | \> 30 seconds: replication should be operational         |
| `rdb_last_save_time`     | \> maximum acceptable interval without taking a snapshot |

> **NOTE**
>
> This is not an exhaustive list, but just to give you an idea of how the metrics in INFO could be used.

### How do I measure Redis latency and stats from the command line?

The redis-cli client has some built-in options that allow you to pull some real-time latency and stats data.

> **NOTE**
>
> These are not available as commands from Redis but as options in redis-cli.

### Latency options

Continuously sample latency:

```bash
$ redis-cli --latency
min: 1, max: 17, avg: 4.03 (927 samples)
```

The `raw` or `csv` output flag can be added:

```bash
$ redis-cli --latency --csv
1,4,1.94,78
```

In order to sample for longer than one second you can use `latency-history` which has a default interval of 15 seconds but can be specified using the `-i` param.

```bash
$ redis-cli --latency-history -i 60
min: 1, max: 30, avg: 4.84 (328 samples)
```

This can also be combined with the `csv` or `raw` output format flag.

```bash
$ redis-cli --latency-history -i 60 --csv
13,13,13.00,1
5,13,9.00,2
3,13,7.00,3
...
```

Both of these could be piped to a file as well.

The `latency-dist` option shows latency as a spectrum. The default interval is one second but can be changed using the `-i` param.

![Screenshot of redis-cli --latency-dist output showing latency distribution spectrum](/images/site-mirror/c7b75c9edb89ec237ed5c86c210ca51dd57a0859-603x771.webp)

### Stats option

Get rolling stats from the server using the `stat` flag.

```bash
$ redis-cli --stat
------- data ------ --------------------- load -------------------- - child -
keys       mem      clients blocked requests            connections
4          9.98M    51      0       8168035 (+0)        4132
4          9.98M    51      0       8181542 (+13507)    4132
4          9.98M    51      0       8196100 (+14558)    4132
4          9.98M    51      0       8209794 (+13694)    4132
...
```

### How do I check Redis memory usage?

Redis includes a `MEMORY` command that includes a subcommand to get stats.

```bash
127.0.0.1:6379> memory stats
 1) "peak.allocated"
 2) (integer) 11912984
 3) "total.allocated"
 4) (integer) 8379168
 5) "startup.allocated"
 6) (integer) 5292168
 7) "replication.backlog"
 8) (integer) 0
 9) "clients.slaves"
10) (integer) 0
11) "clients.normal"
12) (integer) 16986
13) "aof.buffer"
14) (integer) 0
```

These values are available in the `INFO MEMORY` command as well, but here they are returned in a typical Redis `RESP` Array reply.

There is also a `LATENCY DOCTOR` subcommand with an analysis report of the current memory metrics.

### How do I enable Redis latency monitoring?

As we know Redis is fast and as a result is often used in very extreme scenarios where low latency is a must. Redis has a feature called Latency Monitoring which allows you to dig into possible latency issues. Latency monitoring is composed of the following conceptual parts:

- Latency hooks that sample different latency sensitive code paths.
- Time series recording of latency spikes split by different events.
- A reporting engine to fetch raw data from the time series.
- Analysis engine to provide human readable reports and hints according to the measurements.

By default this feature is disabled because most of the time it is not needed. In order to enable it you can update the threshold time in milliseconds that you want to monitor in your Redis configuration. Events that take longer than the threshold will be logged as latency spikes. The threshold configuration should be set accordingly if the requirement is to identify all events blocking the server for a time of 10 milliseconds or more.

```bash
latency-monitor-threshold 10
```

If the debugging session is intended to be temporary the threshold can be set via redis-cli.

```bash
127.0.0.1:6379> CONFIG SET latency-monitor-threshold 10
```

To disable the latency framework the threshold should be set back to 0.

```bash
127.0.0.1:6379> CONFIG SET latency-monitor-threshold 0
```

The latency data can be viewed using the LATENCY command with it's subcommands:

- `LATENCY LATEST` - latest samples for all events
- `LATENCY HISTORY` - latest time series for a given event
- `LATENCY RESET` - resets the time series data
- `LATENCY GRAPH` - renders an ASCII-art graph
- `LATENCY DOCTOR` - analysis report

| **Event**          | Description                                                              |
| ------------------ | ------------------------------------------------------------------------ |
| `command`          | regular commands                                                         |
| `fast-command`     | `O(1)` and `O(log N)` commands                                           |
| `fork`             | the `fork(2)` system call                                                |
| `aof-write`        | writing to the AOF                                                       |
| `aof-fsync-always` | the `fsync(2)` system call when invoked by the appendfsync always policy |
| `expire-cycle`     | the expiration cycle                                                     |
| `eviction-cycle`   | the eviction cycle                                                       |

For example, you can use the `LATENCY LATEST` subcommand and you may see some data like this:

```bash
127.0.0.1:6379> latency latest
1) 1) "command"
   2) (integer) 1616372606
   3) (integer) 600
   4) (integer) 600
2) 1) "fast-command"
   2) (integer) 1616372434
   3) (integer) 12
   4) (integer) 12
```

The results of this command provide the timestamp, latency and max latency for this event.

While the cost of enabling latency monitoring is near zero and memory requirements are very small it will raise your baseline memory usage so if you are getting the required performance out of Redis there is no need to leave this enabled.

### What tools can I use to monitor Redis in production?

There are many open source monitoring tools and services to visualize your Redis metrics - some of which also provide alerting capabilities.

One example of this is the [Redis Data Source for Grafana](https://grafana.com/grafana/plugins/redis-datasource/). It is a [Grafana](https://grafana.com/) plug-in that allows users to connect to the Redis database and build dashboards to easily observe Redis data. It provides an out-of-the-box predefined dashboard but also lets you build customized dashboards tuned to your specific needs.

For step-by-step setup guides, see:

- [Redis Monitoring with Datadog](/tutorials/operate/observability/datadog/) — integrate Redis metrics into Datadog dashboards with alerting
- [Redis Software Observability with Prometheus and Grafana](/tutorials/operate/observability/redis-software-prometheus-and-grafana/) — scrape Redis metrics with Prometheus and visualize them in Grafana

---

## Exercise: Working with Redis Metrics

Change into the `observability-stats` directory.

### Requirements

- docker
- docker compose
- internet connection

### Starting Environment

```bash
docker compose up -d
```

### Connect to the Environment

In a terminal run this command to get a shell prompt inside the running Docker container:

```bash
docker compose exec redis_stats bash
```

### Generate load

A simple way to to generate some load is to open another terminal and run:

```bash
docker compose exec redis_stats redis-benchmark
```

### Explore INFO

Since most of the stats data comes from the INFO command you should first run this to view that there.

```bash
redis-cli INFO
```

Try piping this output to a file.

### Memory usage

Since we generally recommend setting the `maxmemory` size, it is possible to calculate the percentage of memory in use and alert based on results of the `maxmemory` configuration value and the `used_memory` stat.

First set the `maxmemory`.

```bash
redis-cli config set maxmemory 100000
```

Then you can pull the two data points to see how that could be used to calculate memory usage.

```bash
redis-cli INFO | grep used_memory:
redis-cli CONFIG GET maxmemory
```

### Client data

You can pull the `clients` section of the `INFO` command

```bash
redis-cli info clients
```

or maybe a particular metric you would want to track:

```bash
redis-cli info clients | grep connected_clients
```

### Stats section

Use `redis-cli` to list the full 'stats' section.

### Hit ratio

A cache hit/miss ratio could be generated using two data points in the stats section.

```bash
redis-cli INFO stats | grep keyspace
```

### Evicted keys

Eviction occurs when Redis has reached its maximum memory and `maxmemory-policy` in `redis.conf` is set to something other than `volatile-lru.`

```bash
redis-cli INFO stats | grep evicted_keys
```

### Keyspace

The following data could be used for graphing the size of the keyspace as a quick drop or spike in the number of keys is a good indicator of issues.

```bash
redis-cli INFO keyspace
```

### Workload (connections received, commands processed)

The following stats are a good indicator of workload on the Redis server.

```bash
redis-cli INFO stats | egrep "^total_"
```

---

## How do I troubleshoot Redis performance issues?

Besides the metrics from the data points from info, memory and the latency framework in the sections above, you may need to pull data from other sources when troubleshooting.

### How do I check if Redis is running?

The Redis server will respond to the PING command when running properly:

```bash
$ redis-cli -h redis.example.com -p 6379 PING
PONG
```

### How do I use the Redis Slow Log to find slow queries?

Redis Slow Log is a system to log queries that exceed a specific execution time which does not include I/O operations like client communication. It is enabled by default with two configuration parameters.

```bash
slowlog-log-slower-than 1000000
```

This indicates if there is an execution time longer than the time in microseconds, in this case one second, it will be logged. The slow log can be disabled using a value of -1. It can also be set to log every command with a value of 0.

```bash
slowlog-max-len 128
```

This sets the length of the slow log. When a new command is logged the oldest one is removed from the queue.

These values can also be changed at runtime using the `CONFIG SET` command.

You can view the current length of the slow log using the `LEN` subcommand:

```bash
redis.cloud:6379> slowlog len
(integer) 11
```

Entries can be pulled off of the slow log using the `GET` subcommand.

```bash
redis.cloud:6379> slowlog get 2
1) 1) (integer) 10
   2) (integer) 1616372606
   3) (integer) 600406
   4) 1) "debug"
      2) "sleep"
      3) ".6"
   5) "172.17.0.1:60546"
   6) ""
2) 1) (integer) 9
   2) (integer) 1616372602
   3) (integer) 600565
   4) 1) "debug"
      2) "sleep"
      3) ".6"
   5) "172.17.0.1:60546"
   6) ""
```

The slow log can be reset using the `RESET` subcommand.

```bash
redis.cloud:6379> slowlog reset
OK
redis.cloud:6379> slowlog len
(integer) 0
```

### How do I find large or hot keys in Redis?

There are a few options that can be passed to redis-cli that will trigger a keyspace analysis. They use the `SCAN` command so they should be safe to run without impacting operations.

### Key Stats (--keystats):\*\* This option will scan the dataset for keys based on memory size and lengt

```bash
redis-cli --keystats
```

### Big Keys (--bigkeys):\*\* This option will scan the dataset for big keys and provide information about the

### Mem Keys (--memkeys):\*\* Similarly to big keys, mem keys will look for the biggest keys but also report on the average size

### Hot Keys (--hotkeys):\*\* The hot keys scan is only available when the `maxmemory-policy` is set to `volatile-lfu` or `allkeys-lfu`. If you need to identity hot keyyou can add this argument to `redis-cli`

```bash
redis-cli --hotkeys
```

### How do I watch live Redis commands with MONITOR?

The `MONITOR` command allows you to see a stream of every command running against your Redis instance.

```bash
127.0.0.1:6379 > monitor
OK
1616541192.039933 [0 127.0.0.1:57070] "PING"
1616541276.052331 [0 127.0.0.1:57098] "set" "user:2398423hu" "KutMo"
```

> **CAUTION**
>
> Since `MONITOR` streams back all commands, its use comes at a cost. It has been known to reduce performance by up to 50% so use with caution!

### How do I configure Redis logging?

The Redis log file is the other important log you need to be aware of. It contains useful information for troubleshooting configuration and deployment errors. If you don't configure Redis logging, troubleshooting will be significantly harder.

Redis has four logging levels, which you can configure directly in `redis.conf` file.

Log Levels:

- `WARNING`
- `NOTICE`
- `VERBOSE`
- `DEBUG`

Redis also supports sending the log files to a remote logging server through the use of syslog.

Remote logging is important to many security professionals. These remote logging servers are frequently used to monitor security events and manage incidents. These centralized log servers perform three common functions: ensure the integrity of your log files, ensure that logs are retained for a specific period of time, and to correlate logs against other system logs to discover potential attacks on your infrastructure.

Let's set up logging on our Redis deployment. First we'll open our `redis.conf` file:

```bash
sudo vi /etc/redis/redis.conf
```

The `redis.conf` file has an entire section dedicated to logging.

First, find the logfile directive in the `redis.conf` file. This will allow you to define the logging directory. For this example lets use `/var/log/redis/redis.log`.

If you'd like to use a remote logging server, then you'll need to uncomment the lines `syslog-enabled`, `syslog-ident` and `syslog-facility`, and ensure that `syslog-enabled` is set to yes.

Next, we'll restart the Redis server.

You should see the log events indicating that Redis is starting.

```bash
sudo tail -f /var/log/redis/redis.log
```

And next let's check that we are properly writing to syslog. You should see these same logs.

```bash
less /var/log/syslog | grep redis
```

Finally, you'll need to send your logs to your remote logging server to ensure your logs will be backed up to this server. To do this, you'll also have to modify the rsyslog configuration. This configuration varies depending on your remote logging server provider.

---

## Next steps

Now that you understand Redis observability fundamentals, explore these resources to deepen your monitoring setup:

- **[Redis Monitoring with Datadog](/tutorials/operate/observability/datadog/)** — set up Datadog integration to track Redis KPIs with dashboards and alerts
- **[Redis Software Observability with Prometheus and Grafana](/tutorials/operate/observability/redis-software-prometheus-and-grafana/)** — collect metrics with Prometheus and build Grafana dashboards for Redis
- **[Course Conclusion →](/tutorials/operate/redis-at-scale/course-wrap-up/)** — wrap up the Running Redis at Scale course
