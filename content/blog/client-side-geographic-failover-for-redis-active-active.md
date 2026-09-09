---
title: "Client-side geographic failover for Redis Active-Active"
linkTitle: "Client-side geographic failover for Redis Active-Active"
url: "/blog/client-side-geographic-failover-for-redis-active-active/"
description: "The Redis Active-Active architecture supports geographically distributed applications, providing real-time performance when apps are co-located with an Active-Active database member and ensuring..."
date: 2026-04-23
blogCategories:
- "Tech"
authors:
- "Mirko Ortensi"
lastmod: 2026-05-12
hidden: true
---

*By Mirko Ortensi, Sr. Product Manager, Products · Published 23 April 2026 · updated 12 May 2026*

![Client-side geographic failover for Redis Active-Active](/images/blog/680873d3c389456b657fc5608b61e5276baa5dee-1200x628.webp)

The [Redis Active-Active](https://redis.io/docs/latest/operate/rs/databases/active-active/) architecture supports **geographically distributed applications**, providing real-time performance when apps are co-located with an Active-Active database member and ensuring strong eventual consistency through the [Conflict-Free Replicated Datatype (CRDT)](/blog/diving-into-crdts/) based conflict resolution.

In addition to this unique support, Redis Active-Active can be used for disaster recovery, with many use cases successfully developed thanks to its strong eventual consistency model. Several options exist for designing a [disaster recovery strategy](https://redis.io/docs/latest/operate/rs/databases/active-active/disaster-recovery/) to ensure that the application can connect to an available Active-Active database member and execute workloads at any time. Load balancing solutions, global traffic managers, or software proxy solutions connect apps to a healthy dataset replica, increase application resiliency, and maximize service availability, especially for multi-region deployments.

Alongside infrastructure-based approaches such as load balancers, DNS routing, and proxies, failover can also be handled in the client. In Redis, this is supported through [client-side geographic failover](https://redis.io/docs/latest/develop/clients/failover/), which lets a client library monitor multiple Active-Active member endpoints and switch to the next healthy endpoint when the current one becomes unavailable.

With client-side geographic failover, client libraries can detect database failures based on a combination of the [circuit breaker pattern](https://en.wikipedia.org/wiki/Circuit_breaker_design_pattern) and a configurable health check mechanism, and redirect the workload to the next healthy endpoint. The overall experience is that the application does not perceive any disruption and connects to the desired Redis A-A database member.

![Redis](/images/blog/f8fe12b2bd4f66ceb9f3afef87b2d275b7bc2aaf-960x540.webp)

[Jedis](https://redis.io/docs/latest/develop/clients/jedis/failover/) and [redis-py support client-side geographic failover, and now it has been added to Lettuce as well.](https://redis.io/docs/latest/develop/clients/redis-py/failover/) See the [Lettuce 7.4.0](https://github.com/redis/lettuce/releases/tag/7.4.0.RELEASE) release notes to learn more.

## Features

The client-side geographic failover feature includes the following components and configurations:

- **Weighted endpoints**. The user can specify a list of endpoints with associated integer priorities. When the application starts, the client library monitors all endpoints according to the configured health check criteria and routes traffic to the highest-priority healthy endpoint.
- **Circuit breaker**. The active endpoint health is monitored. If the workload starts failing, the circuit breaker kicks in and raises an alert (depending on the sensitivity of the circuit breaker configuration).
- **Health check**. By default, client libraries set up a simple health check mechanism using the [PING](https://redis.io/docs/latest/commands/ping/) command. [REST API availability requests](https://redis.io/docs/latest/operate/rs/references/rest-api/requests/bdbs/availability/) can be configured for more control, and a custom health check can also be designed and configured (e.g., relying on a different logic or external service).
- **Failover**. When either the circuit breaker or the health check detects a failure, failover to the next healthy endpoint on the priority list is triggered, minimizing the downtime and making the switch transparent to the application.
- **Failback**. The client library continuously monitors all A-A database members, including those currently marked as unhealthy. If the highest-priority instance becomes healthy again, the client automatically fails back to it.
- **Manual failover/failback**. Client libraries expose an API to perform a manual failover or failback to the desired replica at any time.
- **Custom actions**. The client library can execute a custom action when failovers or failbacks happen.

Client-side geographic failover complements existing mechanisms for handling disconnections, latency spikes, and unstable connectivity. It maximizes availability while abstracting the underlying complexity from the application.

## Testing client-side geographic failover

To test, first choose the desired client library: Jedis, Lettuce, or redis-py (more official client libraries will be supported soon), and [read the docs](https://redis.io/docs/latest/develop/clients/failover/) to get started. Testing the feature is as easy as configuring the endpoints and using the default configuration. A quick example using redis-py follows.

1. To test the feature, you can configure a Redis Software test deployment on your machine using the official [Redis Software Docker image](https://hub.docker.com/r/redislabs/redis). You can follow instructions to setup two clusters on your laptop or testing environment. Follow the instructions to run [Redis Software on Docker](https://redis.io/docs/latest/integrate/docker-redis-enterprise/) and [create an Active-Active database](https://redis.io/docs/latest/operate/rs/databases/active-active/create/). To test the feature, you can create two [single-node](https://redis.io/docs/latest/operate/rs/installing-upgrading/quickstarts/docker-quickstart/#single-node) clusters (not recommended for production environments)
1. Create a Python virtual environment, then install redis-py and the circuit breaker library
`python3 -m venv testvenv`
`source testvenv/bin/activate`
`pip install redis`
`pip install pybreaker`
1. Consider the Python script below and configure the desired endpoints for the two Active-Active database members. For simplicity, the script relies on the default health check mechanism, the [PingHealthCheck](https://redis.io/docs/latest/develop/clients/redis-py/failover/#pinghealthcheck-default) (available in both Redis Software and Redis Cloud). For advanced users, the [LagAwareHealthCheck](https://redis.io/docs/latest/develop/clients/redis-py/failover/#lag-aware-health-check) is available (Redis Software only) and offers control over the consistency of the member databases in a failback scenario.
1. Then, start the script: as you can see, the first endpoint points to a Redis database running on port 15000, and has a higher priority (weight=1.0) than the database running on port 15001.
1. Now, let’s simulate a failure on the first Active-Active database member. In Redis Software, you can achieve this by [stopping services on the cluster](https://redis.io/faq/doc/1x3gqrydeo/how-do-i-simulate-a-redis-software-cluster-failure).
1. Wait a few seconds, the failure and subsequent automatic failover will be reported by the log.

Restart the services on the cluster and observe the log.

```python
import logging
import time
from redis.multidb.client import MultiDBClient
from redis.multidb.config import MultiDbConfig, DatabaseConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    cfg = MultiDbConfig(
        # Configure two databases with different weights
        databases_config=[
            # Primary database (higher weight = preferred)
            DatabaseConfig(
                from_url="redis://127.0.0.1:15000",
                weight=1.0,
                client_kwargs={"socket_timeout": 5,
                            "socket_connect_timeout": 5}
            ),
            # Secondary database (lower weight = secondary)
            DatabaseConfig(
                from_url="redis://127.0.0.1:15001",
                weight=0.5,
                client_kwargs={"socket_timeout": 5,
                                "socket_connect_timeout": 5}
            ),
        ],
        auto_fallback_interval=10.0,
    )

    client = MultiDBClient(cfg)
    
    counter = 0
    while True:
        counter += 1
        
        try:
            # Perform Redis operations
            key = f"demo:counter:{counter}"
            client.set(key, counter)
            client.get(key)
            logger.info(f"✓ Operation #{counter} successful")
        except Exception as e:
            logger.error(f"✗ Operation #{counter} failed: {e}")
        
        time.sleep(2)
            

if __name__ == "__main__":
    main()

```

This simple test application will log the two main events. First, the failure is detected, and a failover to the Redis Server instance running on port 15001 is done. When the former database member is operational again, the health check detects it, and failback is executed.

```python
2026-04-15 09:40:29,538 - INFO - ✓ Operation #1 successful
2026-04-15 09:40:31,543 - INFO - ✓ Operation #2 successful
2026-04-15 09:40:33,550 - INFO - ✓ Operation #3 successful
2026-04-15 09:40:35,560 - INFO - ✓ Operation #4 successful
...
2026-04-15 09:48:14,231 - INFO - ✓ Operation #229 successful
2026-04-15 09:48:16,235 - INFO - ✓ Operation #230 successful
2026-04-15 09:48:17,561 - WARNING - Database Database(client=<redis.client.Redis(<redis.connection.ConnectionPool(<redis.connection.Connection(socket_timeout=5,socket_connect_timeout=5,retry=<redis.retry.Retry object at 0x1068a6d50>,host=127.0.0.1,port=15000)>)>)>, weight=1.0) is unreachable. Failover has been initiated.
2026-04-15 09:48:18,288 - INFO - ✓ Operation #231 successful
2026-04-15 09:48:20,311 - INFO - ✓ Operation #232 successful
2026-04-15 09:48:22,316 - INFO - ✓ Operation #233 successful
2026-04-15 09:48:24,330 - INFO - ✓ Operation #234 successful
...
2026-04-15 09:48:56,727 - INFO - ✓ Operation #250 successful
2026-04-15 09:48:58,746 - INFO - ✓ Operation #251 successful
2026-04-15 09:48:59,817 - INFO - Database Database(client=<redis.client.Redis(<redis.connection.ConnectionPool(<redis.connection.Connection(socket_timeout=5,socket_connect_timeout=5,retry=<redis.retry.Retry object at 0x1068a6d50>,host=127.0.0.1,port=15000)>)>)>, weight=1.0) is reachable again.
2026-04-15 09:49:00,953 - INFO - ✓ Operation #252 successful
2026-04-15 09:49:03,001 - INFO - ✓ Operation #253 successful
```

Remember that when using client-side geographic failover, you can achieve a more refined failback strategy by configuring the [lag-aware health check](https://redis.io/docs/latest/develop/clients/redis-py/failover/#lag-aware-health-check), which offers the desired data consistency on failback.

## Getting started with client-side geographic failover

Learn more about this feature from the docs:

- [High-level explanation](https://redis.io/docs/latest/develop/clients/failover/) of client-side geographic failover
- [Jedis documentation](https://redis.io/docs/latest/develop/clients/jedis/failover/)
- [Lettuce documentation](https://redis.io/docs/latest/develop/clients/lettuce/failover/)
- [redis-py documentation](https://redis.io/docs/latest/develop/clients/redis-py/failover/)

And stick around, as we’re launching this feature for other client libraries.
