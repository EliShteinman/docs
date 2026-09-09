---
title: "Dynamic endpoints: Migrate databases without changing your endpoint"
linkTitle: "Dynamic endpoints: Migrate databases without changing your endpoint"
url: "/blog/dynamic-endpoints-migrate-databases-without-changing-your-endpoint/"
description: "Most teams don’t move Redis databases often. But when they do, the complexity is rarely in Redis itself. It’s in coordinating endpoint changes across apps, services, and jobs."
date: 2026-05-12
blogCategories:
- "Tech"
authors:
- "Noam Stern"
lastmod: 2026-05-12
hidden: true
---

*By Noam Stern, Sr. Product Manager, Products · Published 12 May 2026*

![Dynamic endpoints: Migrate databases without changing your endpoint](/images/site-mirror/99020b3bed5da7413bdf7a5d1d6bb282d1ac858c-1200x628.webp)

Most teams don’t move Redis databases often. But when they do, the complexity is rarely in Redis itself. It’s in coordinating endpoint changes across apps, services, and jobs.

Redis Cloud now supports **dynamic endpoints**, a stable hostname you can redirect between databases. Instead of changing the app configuration every time you move, you redirect once. It’s a controlled cutover from database A to database B, with your apps continuing to connect to the same endpoint. Dynamic endpoint **redirection** is currently available in public preview.

Customers can change their infrastructure without forcing coordinated app changes.

## Why database moves become operationally expensive

Moves aren’t daily work, but they’re common enough in production:

- Upgrading your database from Essentials to Pro
- Switching to a different Redis solution, like moving from Redis on RAM to Redis Flex (RAM and Flash)
- Standardizing or consolidating environments
- Migrating your database to a different region or cloud provider (for example, AWS to GCP)
- Handling disaster recovery scenarios

Some moves include **data migration**. Others involve redirecting traffic to a pre-provisioned database. In both cases, static endpoints are the constraint.

When apps connect directly to a database’s **static endpoint**:

- Endpoints are scattered across services, jobs, environments, and config systems
- Cutovers require coordinated redeploys across multiple owners
- Changes often need to be synchronized “all at once.”

The move itself may be simple. Updating the clients is not.

What should be a controlled infrastructure change can quickly become a cross-team operational event.

## What dynamic endpoints provide

Dynamic endpoints introduce a stable Redis Cloud hostname that can be redirected from one database to another. Instead of updating endpoints across multiple services and environments, you redirect the dynamic endpoint, allowing traffic to shift from the source database to the target.

Unlike a customer-managed DNS change or load balancer, dynamic endpoints are managed within Redis Cloud, so customers can keep the same app endpoint without operating an additional routing layer.

Redirection is explicit and controlled, and once apps adopt the dynamic endpoint, future moves do not require repeated endpoint changes. Dynamic endpoints handle traffic redirection only; data migration remains a separate operation.

For example, a company may need to move its Redis database to another region because of infrastructure realignment, proximity to dependent services, or disaster recovery planning. With dynamic endpoints, the app continues to use the same hostname while the backing database changes beneath it.

![Dynamic endpoints](/images/site-mirror/6165c964fbf4e33cf5aa170e2e3094b79bdc1c2a-1306x601.webp)

## Example: Upgrade from Redis Cloud Essentials to Redis Cloud Pro with private connectivity

**Scenario:** Your app connects to an **Essentials database via** **public access**. You want to **upgrade to Pro **and have your app use [**private connectivity**](https://redis.io/docs/latest/operate/rc/security/vpc-peering/)** without having to repeat** endpoint changes across all clients.

1. **Create the Pro database** and set up private connectivity in your environment.
1. **Migrate data if required** (for example, using replica-of)
  1. Optional: Based on your app requirements, pause writes for a strict cutover (if needed) and then stop** **replica-of
1. **Redirect the dynamic endpoint** to the Pro database.
  1. In this example, you can choose to redirect the source’s public endpoint to be your target’s private endpoint.
1. **Monitor and validate until stable**.

The app continues using the same hostname throughout the move; the infrastructure changes underneath it.

## Learn more

Dynamic endpoint redirection is currently available in **public preview** for supported database moves within the same account, including transitions such as Essentials to Pro and Pro to Pro. During the initial rollout, access will begin with a portion of new accounts before gradually expanding to more new and existing accounts over the coming weeks.

Support depends on factors such as port compatibility, networking, and allow list configuration, and the source and target deployment types. Some combinations, such as Active-Active databases or Pro-to-Essentials moves, are not supported.

For detailed requirements, configuration constraints, and implementation guidance, read our [official docs](https://redis.io/docs/latest/operate/rc/databases/redirect-endpoints/).
