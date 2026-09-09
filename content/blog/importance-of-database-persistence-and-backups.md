---
title: "The Importance of Database Persistence and Backups"
linkTitle: "The Importance of Database Persistence and Backups"
url: "/blog/importance-of-database-persistence-and-backups/"
description: "We recently had an opportunity to work with the Cohesity team to verify integration between Helios and Redis Enterprise as a step in onboarding into the Redis Technical Partner Program. Cohesity..."
date: 2022-06-17
blogCategories:
- "Uncategorized"
authors:
- "André Srinivasan"
lastmod: 2025-03-27
hidden: true
---

*By André Srinivasan, Solutions Architect · Published 17 June 2022 · updated 27 March 2025*

![Blog tile image](/images/blog/32fe174d68c8a5353ecbc90283702415b0cb8643-772x550.webp)

We recently had an opportunity to work with the [Cohesity](https://www.cohesity.com/) team to verify integration between Helios and Redis Enterprise as a step in onboarding into the [Redis Technical Partner Program](/partners/). Cohesity SmartFiles, a service that runs on Helios, provides a single view and global management of [unstructured data](/glossary/unstructured-data/), irrespective of where the data resides. In the context of Redis Enterprise, SmartFiles provides a single view of database snapshots.

Why do we bother with persistence and backup? It is true: If Redis is used as a cache and can be rehydrated from a backend database with minimal system impact, there is no need for either. On the other hand, consider when Redis is used as an operational database to provide fast access to slow data (think: transaction history, inventory count, customer lookup). The Redis database needs to quickly recover from hardware issues or even failover to another datacenter.

## Persistence

All data in a Redis database is stored and managed exclusively in either RAM or RAM + Flash Memory ([Redis on Flash](https://docs.redis.com/latest/rs/concepts/memory-performance/redis-flash/)); it is at risk of being lost upon a process or server failure. There are several strategies that can be followed to mitigate this risk: High Availability (HA) databases with primary and secondary [data shards](https://docs.redis.com/latest/rs/concepts/terminology/#redis-instance-shard), geo-distributed [active-active](https://docs.redis.com/latest/rs/concepts/intercluster-replication/) databases, and of course disk based persistence. From a performance perspective, it is always preferred to failover from a primary database shard to a synchronized secondary database shard, and this is how Redis Enterprise works; only when the primary and secondary shards are lost is the database restored from disk. Similarly, in the case of a datacenter failure, failing over to a synchronized active-active database in another data center will be faster than recovering from disk.

To the question of persistence, Redis supports append-only files (AOF) for better durability, though requires more resources, and snapshots (RDB), which are less durable while requiring fewer resources. As with all things, there are tradeoffs that can be further explored in the [Redis Enterprise documentation](https://docs.redis.com/latest/rs/concepts/memory-performance/persistence/). For the purposes of this article, we will assume we want AOF for better durability.

![illustration of data persistence](/images/blog/f68d2583b50107b83063d8fd472ae5d76e6f2628-1024x536.webp)

## Backup

Redis Enterprise relies on persistence for recovery when both the primary and secondary database shards are lost. If active-active is not used and the racks housing the databases along with attached storage are lost, then we are left with restoring from a backup. In the case of Redis Enterprise, a backup is always a snapshot, which, when coupled with AOF for persistence, creates a resilient and durable data platform.

This is where Cohesity SmartFiles comes into play; Redis Enterprise utilizes the S3 compatible endpoint conveniently provided by SmartFiles for managed backups across the clouds. To set this up, we use the [Redis Enterprise REST API](https://docs.redis.com/latest/rs/references/rest-api/) with the following assumptions:

- $S3_IP is set to the Cohesity S3 object store IP address and $BUCKET is set to the bucket name
- $USER and $PASS are set to the Redis Enterprise admin username and password, respectively
- $ACCESS_KEY and $SECRET_KEY are set the S3 object store access key and secret key, respectively

Enable [database persistence](/redis-enterprise/technology/durable-redis/).

```bash
curl -s -k -u $USER:$PASS -H content-type:application/json -XPUT 
https://localhost:9443/v1/bdbs/1 -d '{"data_persistence": "aof"}'

```

Configure the cluster to use the S3 object store by setting the S3 URL. Note the bucket name is not included in the S3 URL.

```bash
curl -s -k -u $USER:$PASS -H content-type:application/json -X PUT 
https://localhost:9443/v1/cluster -d '{"s3_url": '\"$S3_IP\"'}'

```

Configure the cluster S3 backup for privacy only.

```bash
curl -s -k -u $USER:$PASS -H content-type:application/json -X PUT 
https://localhost:9443/v1/cluster -d 
'{"s3_certificate_verification":false}'

```

Validate the backup location. Note the only response on success is an HTTP 200 OK.

```bash
curl -s -k -u $USER:$PASS -H content-type:application/json -X POST 
https://localhost:9443/v1/bdbs/actions/validate_backup_location -d 
'{"backup_location": {"type": "s3", "bucket_name": '\"$BUCKET\"', 
"subdir": "","access_key_id": '\"$ACCESS_KEY\"', "secret_access_key": 
'\"$SECRET_KEY\"'}}'

```

Create a backup. Note the only response on success is an HTTP 200 OK.

```bash
curl -s -k -u $USER:$PASS -H content-type:application/json -X POST 
https://localhost:9443/v1/bdbs/1/actions/export -d 
'{"export_location": {"type": "s3", "bucket_name": '\"$BUCKET\"', 
"subdir": "", "access_key_id": '\"$ACCESS_KEY\"', "secret_access_key": 
'\"$SECRET_KEY\"'}}'

```

Configure a recurring backup every 30 minutes. Note the only response on success is an HTTP 200 OK.

```bash
curl -s -k -u $USER:$PASS -H content-type:application/json -X PUT 
https://localhost:9443/v1/bdbs/1 -d '{"backup":true, 
"backup_interval":1800, "backup_interval_offset":360, 
"backup_location": {"type": "s3", "bucket_name": '\"$BUCKET\"', 
"subdir": "", "access_key_id": '\"$ACCESS_KEY\"', "secret_access_key": 
'\"$SECRET_KEY\"'}}'

```

## Final Thoughts

In a frictionless world, Redis Enterprise configured with HA and Active-Active saves you from worrying about persistence and backups. We don’t live in a frictionless world and we need both persistence and backups (along with HA) when Redis is expected to recover from system failures. It is common to see an S3 backup endpoint as can be seen by the appliance offerings from the likes of Dell EMC, NetApp, or Pure Storage. Fortunately, the verified integration with Cohesity SmartFiles makes it easy to utilize this endpoint and to include backups in operational strategies.
