---
title: "Supporting critical workloads with smart client handoffs"
linkTitle: "Supporting critical workloads with smart client handoffs"
url: "/blog/supporting-critical-workloads-with-smart-client-handoffs/"
description: "Planned software maintenance shouldn’t break apps. That’s the simple idea behind Redis Software’s and Redis Cloud’s new smart client handoffs feature—a capability that keeps apps online during..."
date: 2025-12-02
blogCategories:
- "Tech"
authors:
- "Mirko Ortensi"
lastmod: 2026-01-05
hidden: true
mirrored: true
---

*By Mirko Ortensi, Sr. Product Manager, Products · Published 2 December 2025 · updated 5 January 2026*

![Redis title card ](/images/site-mirror/ff8c864fb67e16fb977e98f342411eec3c8bdd02-1200x628.webp)

Planned software maintenance shouldn’t break apps. That’s the simple idea behind Redis Software’s and Redis Cloud’s new **smart client handoffs** feature—a capability that keeps apps online during scheduled upgrades. It coordinates connectivity and timeouts directly from the official Redis client libraries, so your apps continue running even while maintenance operations are in progress.

Designed for Redis Cloud and Redis Software, the feature requires no special orchestration in application code and works with the official Redis clients. Its goal: a low‑friction way to upgrade servers without hard disconnects, unfinished requests, or timeout storms.

#### How does it work?

[Upgrading](https://redis.io/docs/latest/operate/rs/installing-upgrading/upgrading/) to the latest Redis versions lets you take advantage of enhanced capabilities, improved stability, stronger security, and better performance. However, upgrades can also disrupt active connections—forcing apps to retry, back off, or fail altogether—unless clients are designed to smoothly handle the transition.

Normally, client libraries must handle these disruptions by building in resiliency through careful timeout configurations, reconnection strategies, and retry logic to ensure continuity during disconnects.

With smart client handoffs, Redis shifts that burden away from your apps. Redis' official client libraries understand the phases of a maintenance operation (e.g., [cluster](https://redis.io/docs/latest/operate/rs/installing-upgrading/upgrading/upgrade-cluster/) or database version upgrades, shard [migrations](https://redis.io/docs/latest/operate/rs/references/rest-api/requests/shards/actions/migrate/), or [failovers](https://redis.io/docs/latest/operate/rs/references/rest-api/requests/shards/actions/failover/)), and proactively reconnect to the correct endpoints, while adjusting timeouts as the transition completes. All this happens transparently to your app.

![Redis](/images/site-mirror/f657eeaae9c12560d7cdde5911628a2846d9c25a-1951x1097.webp)

The feature introduces two coordinated behaviors in official Redis client libraries:

- **Transparent endpoint rebinds:** Clients receive proactive notifications, disconnect from the old endpoint, and reconnect to the new one before the old server goes offline. No manual failover logic, DNS gymnastics, or custom retry loops. The handoff completes with in‑flight requests intact and avoids hard disconnects.
- **Adaptive timeouts:** During upgrades, planned shard migrations, or failovers, clients temporarily relax command timeouts to give pending requests more time to complete. After the operation finishes, timeouts automatically revert to their normal values.

Together, these behaviors transform scheduled maintenance into a routine event, rather than a risk for disconnection and loss of availability.

## Enabling the smart client handoffs feature

You can use the smart client handoffs feature in both Redis Software and Redis Cloud.

#### Redis Cloud

Smart client handoffs are enabled **by default** for Redis Cloud Essentials and Pro databases. Supported clients simply opt in and take advantage of maintenance notifications and handoff behavior.

#### Redis Software

To enable smart client handoffs in Redis Software, upgrade to Redis Software 8.0.2 and enable the feature on the cluster via the [REST API](https://redis.io/docs/latest/develop/clients/sch/#enable-sch). Once enabled on the server, clients can opt in and control their behavior.

## Working with the client libraries

Here’s a minimal Python example using the [redis-py](http://github.com/redis/redis-py) client library that opts into proactive reconnect and adaptive timeout behavior. Refer to the [documentation](https://redis.io/docs/latest/develop/clients/sch/) for additional examples using other official Redis client libraries, such as [Lettuce](https://redis.io/docs/latest/develop/clients/lettuce/connect/#connect-using-smart-client-handoffs-sch), [redis-py](https://redis.io/docs/latest/develop/clients/redis-py/connect/#connect-using-smart-client-handoffs-sch), [go-redis](https://redis.io/docs/latest/develop/clients/go/connect/#connect-using-smart-client-handoffs-sch), and [node-redis](https://redis.io/docs/latest/develop/clients/nodejs/connect/#connect-using-smart-client-handoffs-sch).

```python
r = redis.Redis(
    decode_responses=True,
    protocol=3,
    maint_notifications_config = MaintNotificationsConfig(
        enabled=True,
        proactive_reconnect=True,
        relaxed_timeout=10,
        endpoint_type=EndpointType.EXTERNAL_IP
    ),
    ...
)
```

If you run Redis for critical workloads, you need upgrades that don’t disrupt your team or end users, even during the quietest maintenance window. Smart client handoffs bring that reliability to Redis Software and Redis Cloud, delivering smooth endpoint transitions, adaptive timeouts, and clients that simply keep your app running.

## Learn more

You can learn more about the feature, as well as how to enable and configure it, in our [docs](https://redis.io/docs/latest/develop/clients/sch/).
