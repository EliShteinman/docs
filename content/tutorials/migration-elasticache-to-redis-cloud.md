---
title: "ElastiCache to Redis Cloud"
linkTitle: "ElastiCache to Redis Cloud"
url: "/tutorials/migration/elasticache-to-redis-cloud/"
description: "Redis Cloud offers several advantages over AWS ElastiCache, including access to the full Redis stack (Search, JSON, Time Series, and more), Active-Active geo-replication, predictable pricing..."
aliases:
- "/tutorials/migration-elasticache-to-redis-cloud/"
date: 2026-02-25
lastmod: 2026-02-27
hidden: true
---

*Published 25 February 2026 · updated 27 February 2026*

> **TL;DR:**
>
> You can migrate from AWS ElastiCache to Redis Cloud using either an offline approach (export an RDB snapshot to S3 and import it) or a live approach (replicate data in real time using [RIOT](https://redis.github.io/riot/)). The offline method is simpler but requires downtime; live replication minimizes downtime but does not guarantee full consistency.

## What you'll learn

- How to export an ElastiCache backup to S3 and import it into Redis Cloud
- How to set up live replication from ElastiCache to Redis Cloud using RIOT
- How to configure AWS permissions, parameter groups, and networking for migration
- How to validate your data after migration

## Prerequisites

- An **AWS account** with access to your ElastiCache instance and the S3 console
- A **Redis Cloud account** with a target database already provisioned ([sign up free](https://redis.io/try-free/))
- For live migration: an **EC2 instance** in the same VPC as your ElastiCache cluster

## Why migrate from ElastiCache to Redis Cloud?

Redis Cloud offers several advantages over AWS ElastiCache, including access to the full Redis stack (Search, JSON, Time Series, and more), [Active-Active geo-replication](https://redis.io/docs/latest/operate/rc/databases/configuration/active-active-redis/), predictable pricing without per-node fees, and a fully managed experience across any cloud provider. If you are looking for an AWS ElastiCache alternative with more flexibility and lower operational overhead, Redis Cloud is a strong option.

## What are my migration options?

You have two primary migration strategies:

1. **Offline migration (S3 export/import):** Create a manual backup of your ElastiCache cluster, export the RDB file to an S3 bucket, and import it into Redis Cloud. This is the simplest path but requires a maintenance window.
2. **Live migration (RIOT replication):** Use the [RIOT-X](https://redis.github.io/riotx/) tool to replicate data from ElastiCache to Redis Cloud in real time. This minimizes downtime but requires additional setup and is not supported by ElastiCache Serverless.

Before migrating to Redis Cloud, you should evaluate the migration and consider the best option. Read the [Redis Cloud Migration Guide](/tutorials/migration/) to determine which migration strategy is right for you.

## Offline data migration

### Create S3 bucket with proper permissions

1.  Open the [Amazon S3 console](https://console.aws.amazon.com/s3/).
2.  Create a new S3 bucket to store Elasticache backups.
3.  Choose **Permissions**.
4.  Under **Access control list (ACL)**, choose **Edit**.
5.  Click **Add grantee**, and then enter the following Elasticache canonical ID (this allows the Elasticache service to write backups to this S3 bucket):

```bash
540804c33a284a299d2547575ce1010f2312ef3da9b3a053c8bc45bf233e4353
```

6\. For Objects, select List and Write.

7\. For Bucket ACL, select Read and Write.

8\. Click Save changes.

9\. Add the following JSON to the Bucket policy. Replace UNIQUE-BUCKET-NAME with the name of your bucket:

```json
{
    "Version": "2012-10-17",
    "Id": "MyBucketPolicy",
    "Statement": [
        {
            "Sid": "RedisCloudBackupsAccess",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::168085023892:root"
            },
            "Action": ["s3:PutObject", "s3:getObject", "s3:DeleteObject"],
            "Resource": "arn:aws:s3:::UNIQUE-BUCKET-NAME/*"
        }
    ]
}
```

10\. Disable “block all public access” at the account level and at the bucket level.

11\. While still in the Permissions tab, edit **Block public access (bucket settings)**.

12\. Uncheck **Block all public access.**

13\. Disable “block all public access” at the account level.

14\. In the S3 navigation pane, click on [Block Public Access settings for this account](https://console.aws.amazon.com/s3/settings).

15\. Uncheck **Block all public access.**

### Create manual Elasticache backup and export to S3

1.  Open the [ElastiCache console](https://console.aws.amazon.com/elasticache/).
2.  From the navigation pane, choose **Redis OSS caches.**
3.  Select your Redis database
4.  In the Actions dropdown button, select **Backup**.
5.  Input a name for your backup and click **Create Backup**.
6.  In the navigation pane, under **Resources**, choose **Backups**.
7.  From the list of backups, select your backup.
8.  From the Actions dropdown menu, choose **Export**.
9.  In **Target S3 location** dropdown list, select the S3 bucket that you created.
10. Click **Export**.
11. Locate your backup RDB file in S3 and edit the permissions.
12. In the **Permissions** tab click **Edit**
13. ﻿For **Authenticated users group (anyone with an AWS account)**, under **Object** check **Read.**

![AWS S3 bucket permissions dialog showing Read access enabled for authenticated users on the RDB backup object](/images/site-mirror/3b41dfebefffdccc3e7479983732cd436269a43c-1008x584.webp)

### Import RDB file into Redis Cloud

1.  In the [Redis Cloud console](https://cloud.redis.io/), select the target database from the database list.
2.  Select **Import**.
3.  Enter the details for the RDB file:
4.  Source type - Select **AWS S3**.
5.  Source path - Enter the **S3 URI** for the RDB file from the previous step: s3://bucketname/\[path/\]filename.rdb
6.  For sharded databases with multiple RDB files, select **Add source** to add another RDB file.
7.  Select **Import**.
8.  Validate your migration and redirect your app's traffic to the new Redis Cloud endpoint.

![Redis Cloud console import dialog with AWS S3 selected as the source type and an S3 URI entered for the RDB file](/images/site-mirror/52570473a6f8443bdc5d918fc498a4b9ca0f6772-671x589.webp)

## Live data migration

AWS does not allow direct access to ElastiCache instances. Your ElastiCache instance must be accessed from an EC2 instance with proper permissions. The following guide assumes that your ElastiCache instance is reachable from the internet via an EC2 instance.

> **Note:** Live data migration is not supported by ElastiCache serverless.

### Modify your ElastiCache parameter group

By default, ElastiCache has keyspace notifications disabled. This feature is required for RIOT live mode. You will need to create a custom parameter group in order to modify configuration values for your ElastiCache. If your ElastiCache already has a custom parameter group, you can skip to step 5 to edit the **notify-keyspace-events** parameter.

1. Open the [ElastiCache console](https://console.aws.amazon.com/elasticache/) and select **Parameter groups**.
2. Click **Create parameter group.**
3. Name your parameter group, give it a description, and select the Redis version under **Family**.
4. Click **Create**.
5. From the **Parameter groups** page, click on the parameter group you just created, click **Edit parameter values**.
6. Type in keyspace in Find parameters to filter for the **notify-keyspace-events** parameter.
7. For **Value,** enter KEA.
8. If your ElastiCache has cluster mode enabled, you will also need to modify the **cluster-enabled** parameter.
9. Click **Save changes**.

![AWS ElastiCache parameter group editor showing the notify-keyspace-events parameter set to KEA](/images/site-mirror/fc97125cfe88f9e6f24a05bea7bcf892bb50fb17-975x294.webp)

10\. In the left navigation pane, click on **Redis OSS caches** and select your ElastiCache instance.

11\. Click **Modify**, under **Parameter groups** select your new parameter group.

12\. Click **Preview changes**, then click **Modify** to confirm changes.

### Set up compute connection to ElastiCache

1.  Open the [ElastiCache console](https://console.aws.amazon.com/elasticache/) and select your open source Redis cache.
2.  From the **Actions** dropdown button, select **Set up compute connection**.
3.  Create a new EC2 instance or select an existing one in the same VPC.
4.  Ubuntu is preferred, additional steps might be required if using Amazon Linux.
5.  Click **Setup**, this will create a new ENI and security groups to allow your instance access to ElastiCache.

### Install redis-tools, Java, and RIOT

1\. Use Instance Connect or SSH to connect to the new EC2 instance:

```bash
ssh -i “public key” AWS_EC2_INSTANCE
```

2\. Install the redis-cli tool:

```bash
sudo apt update && sudo apt install -y redis-tools
```

3\. Verify the connectivity with the ElastiCache instance, replace ELASTICACHE_ENDPOINT with your ElastiCache endpoint. Remove the --tls option if TLS is not enabled.

```bash
redis-cli --tls -h ELASTICACHE_ENDPOINT -p 6379
```

4\. Install Java, we recommended using OpenJDK 21 or later:

```bash
sudo apt install -y openjdk-21-jdk
```

5\. Install RIOT. Download the desired release. Then, unzip the package and make sure the RIOT binaries are in place, as shown here:

```bash
wget https://github.com/redis/riot/releases/download/v4.2.3/riot-4.2.3.tar && tar -xvf riot-4.2.3.tar && cd riot-4.2.3/bin/﻿
```

6\. You can check the version of RIOT by running the command below:

```bash
./riot --version
```

```bash
------------------------------------------------------------
riot 4.2.3
------------------------------------------------------------
Build time:   2025-02-16 18:35:57Z
Revision: 	d7a319522e4e72a2b5277e5a15bd715d557dedb6
JVM:      	21.0.6 (Ubuntu 21.0.6+7-Ubuntu-124.04.1)
------------------------------------------------------------
```

### Replicate ElastiCache to Redis Cloud

Once Java and RIOT are installed, you are all set to begin the migration process which replicates data directly from the source (ElastiCache) to the target (Redis Cloud). 

1.  Log into the [Redis Cloud console](https://cloud.redis.io/).
2.  Click on your migration target and take note of the: public endpoint, username, and password
3.  Back in your EC2 instance run the command below:

`sudo ./riot replicate rediss://ELASTICACHE_ENDPOINT:port redis://username:password@REDIS_CLOUD_ENDPOINT:port --mode live`

1. If you are migrating from an ElastiCache cluster, you must include the --source-cluster option
2. If you are migrating to a Redis Cloud cluster, you must include the --target-cluster option.
3. If TLS is not enabled in your ElastiCache cluster, replace rediss:// with redis://
4. Validate your migration and redirect your application's traffic to the new Redis Cloud endpoint.

The live replication mechanism does not guarantee data consistency. Redis sends keyspace notifications over pub/sub which does not provide guaranteed delivery. It is possible that RIOT can miss some notifications in case of network failures for example.

Also, depending on the type, size, and rate of change of data structures on the source it is possible that RIOT cannot keep up with the change stream. For example if a big set is repeatedly updated, RIOT will need to read the whole set on each update and transfer it over to the target database. With a big-enough set, RIOT could fall behind and the internal queue could fill up leading up to updates being dropped.

For those potentially problematic migrations it is recommended to perform some preliminary sizing using Redis statistics and bigkeys/memkeys in tandem with --mem-limit. If you need assistance please contact your Redis account team.

For more information, see:

- [Redis Input/Output Tools (RIOT-X)](https://redis.github.io/riotx/replication)
- [RIOT Live Replication](https://redis.github.io/riotx/replication/modes#_replication_mode_live)

## Next steps

Now that you've migrated from ElastiCache to Redis Cloud, consider exploring these resources:

- [Redis Cloud Migration Guide](/tutorials/migration/) — Compare migration strategies and plan your next move.
- [Migrate Memorystore to Redis Cloud](/tutorials/migration/memorystore-to-redis-cloud/) — Follow a similar process to migrate from Google Cloud Memorystore.
- [Migrate ElastiCache to Azure Managed Redis](/tutorials/learn/migration/elasti-cache-to-azure-managed-redis/) — Learn how to migrate from ElastiCache to Azure Managed Redis instead.
- [Migrate Redis Open Source to Redis Cloud](/tutorials/migration/redis-open-source-to-redis-cloud/) — Move your self-hosted Redis instance to Redis Cloud.
