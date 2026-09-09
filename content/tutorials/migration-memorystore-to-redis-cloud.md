---
title: "Memorystore to Redis Cloud"
linkTitle: "Memorystore to Redis Cloud"
url: "/tutorials/migration/memorystore-to-redis-cloud/"
description: "Before migrating to Redis Cloud, you should evaluate the migration and consider the best option. Read this guide to determine which migration strategy is right for you."
aliases:
- "/tutorials/migration-memorystore-to-redis-cloud/"
date: 2026-02-25
lastmod: 2026-02-27
hidden: true
---

*Published 25 February 2026 · updated 27 February 2026*

> **TL;DR:**
>
> You can migrate from Google Cloud Memorystore to Redis Cloud using either an offline RDB export through Google Cloud Storage or a live replication with [RIOT-X](https://redis.github.io/riotx/replication). Offline migration is simpler but requires downtime; live migration minimizes downtime but does not guarantee full consistency.

## What you'll learn

- How to export an RDB backup from Memorystore and import it into Redis Cloud
- How to set up live replication from Memorystore to Redis Cloud using RIOT
- How to validate your migration and redirect application traffic

## Prerequisites

- A Google Cloud Platform (GCP) account with an active Memorystore for Redis instance
- A [Redis Cloud account](https://cloud.redis.io/) with a target database provisioned
- For live migration: a Compute Engine instance in the same region and network as your Memorystore instance

Before migrating to Redis Cloud, you should evaluate the migration and consider the best option. Read this guide to [determine which migration strategy is right for you](/tutorials/migration).

## How do I perform an offline migration from Memorystore to Redis Cloud?

### Create a Google Cloud Storage bucket with proper permissions

1.  Open [Google Cloud Storage bucket](https://console.cloud.google.com/storage/browser).
2.  Create a new bucket to store Memorystore backups.
3.  Under **Choose how to control access to objects**, uncheck **Enforce public access prevention on this bucket**
4.  In the Google Cloud Storage bucket, under the **Permissions** tab, click **Grant Access.**
5.  In the Grant access menu under **Add principals**, enter: `service@redislabs-prod-clusters.iam.gserviceaccount.com`
6.  Under **Assign roles**, select **Cloud Storage ⇒ Storage Object User**
7.  Click **Save**.

![Google Cloud Grant Access dialog showing the Add principals field and Assign roles dropdown](/images/site-mirror/bd10278821cff373ae0bc2d100577239ffb24a10-580x717.webp)

### Import RDB file from Google Cloud Storage to Redis Cloud

1.  In the [Redis Cloud console](https://cloud.redis.io/), select the target database from the database list.
2.  Click **Import**.
3.  Enter the details for the RDB file:
4.  Source type - Select **Google Cloud Storage**.
5.  Source path - Enter the URL for the RDB file: `gs://bucketname/[path/]filename.rdb`
6.  For sharded databases with multiple RDB files, select **Add source** to add another RDB file.
7.  Select **Import**.
8.  Validate your migration and redirect your application's traffic to the new Redis Cloud endpoint.

![Redis Cloud console Import dialog with Google Cloud Storage selected as the source type](/images/site-mirror/4beb4c56a19e8bd57abca2b4ec8a944a54a2c0f0-868x776.webp)

## How do I perform a live migration from Memorystore to Redis Cloud?

Your Memorystore instance must be accessed from a Compute Engine instance with proper permissions. The following guide assumes that your Memorystore instance is reachable from the internet via a Compute Engine instance.

### Enable notify-keyspace-events in Memorystore

1.  Go to the [Memorystore for Redis](https://console.cloud.google.com/memorystore/redis/instances) page in the Google Cloud console.
2.  Click the Instance ID of your migration source.
3.  Click **Edit**.
4.  The **Configurations** section is now visible. Click **Add Configuration** to add a new configuration.
5.  In the configuration dropdown, select **notify-keyspace-events**
6.  For the **Value**, enter KEA
7.  Click **Save**.

![Google Cloud Memorystore configuration page showing notify-keyspace-events set to KEA](/images/site-mirror/efadb5d2eb05831c2711882ab5f94f7b338317a6-551x512.webp)

### Create a Compute Engine instance

1.  Go to the [Google Cloud Compute Engine console](https://console.cloud.google.com/compute/instances).
2.  Click **Create Instance**
3.  For the operating system, Ubuntu is preferred.
4.  Ensure that the Compute Engine instance is created in the same region as your Memorystore instance
5.  Ensure that the Compute Engine instance uses the same **Authorized network**.
6.  Click **Create**.

### Install redis-tools, Java, and RIOT

1.  In the [Google Cloud Compute Engine console](https://console.cloud.google.com/compute/instances), click **SSH** to connect to your instance.
2.  Install the redis-cli tool:

```bash
sudo apt update && sudo apt install -y redis-tools
```

3\. Verify the connectivity with the Memorystore instance, replace MEMORYSTORE_ENDPOINT with your Memorystore endpoint.

```bash
redis-cli -h MEMORYSTORE_ENDPOINT -p 6379
```

4\. Install Java, we recommended using OpenJDK 21 or later:

```bash
sudo apt install -y openjdk-21-jdk
```

5\. Install RIOT. Download the desired [release](https://github.com/redis/riotx/releases). Then, unzip the package and make sure the RIOT binaries are in place, as shown here:

```bash
wget https://github.com/redis/riotx/releases/download/v1.7.8/riotx-1.7.8.tar && tar -xvf riotx-1.7.8.tar && cd riotx-1.7.8/bin/
```

6\. You can check the version of RIOT-X by running the command below:

```bash
./riotx --version
```

```bash
------------------------------------------------------------
riotx 1.7.8
------------------------------------------------------------
Build time:   2025-02-16 18:35:57Z
Revision: 	d7a319522e4e72a2b5277e5a15bd715d557dedb6
JVM:      	21.0.6 (Ubuntu 21.0.6+7-Ubuntu-120.04.1)
------------------------------------------------------------
```

### Replicate Memorystore to Redis Cloud

Once Java and RIOT are installed, you are all set to begin the migration process which replicates data directly from the source (Memorystore) to the target (Redis Cloud).

1.  Log into the [Redis Cloud console](https://cloud.redis.io/).
2.  Click on your migration target and take note of the **public endpoint, username, and password**
3.  You can replicate the data from Memorystore to Redis Cloud by running the below command: `sudo ./riot replicate redis://MEMORYSTORE_ENDPOINT:port redis://username:password@REDIS_CLOUD_ENDPOINT:port --mode live`
4.  If you are migrating from a Memorystore cluster, you must include the --source-cluster option
5.  If you are migrating to a Redis Cloud cluster, you must include the --target-cluster option.
6.  Validate your migration and redirect your application's traffic to the new Redis Cloud endpoint.

## What are the risks of live replication?

The live replication mechanism does not guarantee data consistency. Redis sends keyspace notifications over pub/sub which does not provide guaranteed delivery. It is possible that RIOT can miss some notifications in case of network failures for example.

Also, depending on the type, size, and rate of change of data structures on the source it is possible that RIOT cannot keep up with the change stream. For example if a big set is repeatedly updated, RIOT will need to read the whole set on each update and transfer it over to the target database. With a big-enough set, RIOT could fall behind and the internal queue could fill up leading up to updates being dropped.

For those potentially problematic migrations it is recommended to perform some preliminary sizing using Redis statistics and bigkeys/memkeys in tandem with --mem-limit. If you need assistance please contact your Redis account team.

## Next steps

- [Redis Cloud Migration overview](/tutorials/migration) — compare migration strategies and choose the right approach
- [Migrate ElastiCache to Redis Cloud](/tutorials/migration/elasticache-to-redis-cloud/) — follow a similar migration path from AWS ElastiCache
- [Migrate Memorystore to Azure Managed Redis](/tutorials/learn/migration/memorystore-to-azure-managed-redis/) — migrate Memorystore to Azure Managed Redis instead
- [Redis Input/Output Tools (RIOT)](https://redis.github.io/riotx/replication) — learn more about RIOT replication
- [RIOT Live Replication](https://redis.github.io/riotx/replication/modes#_replication_mode_live) — deep dive into RIOT live replication mode
