---
title: "ElastiCache to Azure Managed Redis (AMR)"
linkTitle: "ElastiCache to Azure Managed Redis (AMR)"
url: "/tutorials/learn/migration/elasti-cache-to-azure-managed-redis/"
description: "Migrate from AWS ElastiCache to Azure Managed Redis (AMR) using an offline S3 export-and-import workflow. Export your ElastiCache data as an RDB file, transfer it through an S3 bucket to Azure Blob..."
group: "For developers"
aliases:
- "/tutorials/learn-migration-elasti-cache-to-azure-managed-redis/"
date: 2026-02-24
lastmod: 2026-02-27
hidden: true
---

*Published 24 February 2026 · updated 27 February 2026*

Migrate from AWS ElastiCache to Azure Managed Redis (AMR) using an offline S3 export-and-import workflow. Export your ElastiCache data as an RDB file, transfer it through an S3 bucket to Azure Blob storage, and import it into a new AMR instance.

## What you'll learn

- How to create an S3 bucket with the correct permissions for ElastiCache backups
- How to export an RDB backup from ElastiCache to S3
- How to upload the RDB file to Azure Blob storage
- How to create and size an Azure Managed Redis instance
- How to import the RDB data into Azure Managed Redis

## Prerequisites

- An AWS account with an existing ElastiCache instance
- An Azure subscription with permissions to create storage accounts and Azure Managed Redis instances
- Familiarity with the AWS and Azure consoles

Before migrating to Azure Managed Redis, evaluate your migration options and choose the best strategy. Read this guide to [determine which migration strategy is right for you](/tutorials/migration). If you're considering Redis Cloud instead, see the [ElastiCache to Redis Cloud migration guide](/tutorials/migration/elasticache-to-redis-cloud/). Reach out to our team for support on live migrations.

## How do you perform an offline data migration from ElastiCache to Azure Managed Redis?

The offline migration process involves exporting your ElastiCache data as an RDB file to Amazon S3, transferring that file to Azure Blob storage, and importing it into your new Azure Managed Redis instance.

### How do you create an S3 bucket with the right permissions for ElastiCache backups?

Open Amazon S3 and create a new bucket. The ElastiCache backup and the Amazon S3 bucket that you create must be in the same AWS Region.

![AWS console showing the Create bucket dialog in Amazon S3](/images/site-mirror/89ae8c8192f1d8c1c12f3cdc518e83d42a13c416-940x603.webp)

Navigate to your new S3 bucket and go to the Permissions tab.

![S3 bucket Permissions tab with options for ACL and bucket policy](/images/site-mirror/2efa949269dda36688929698558e615add5963bb-1030x178.webp)

1.  Under Access Control List (ACL), choose Edit. Select Add grantee.

- ElastiCache canonical ID (paste this in under Grantee): 540804c33a284a299d2547575ce1010f2312ef3da9b3a053c8bc45bf233e4353
- Select Objects > List & Write
- Select Bucket ACL > Read & Write

![S3 bucket ACL editor showing the ElastiCache grantee with List, Write, and Read permissions](/images/site-mirror/8cf92273df6018651f7a01440b90d64fb24a2cc8-1128x647.webp)

Under the Permissions tab still, add the following JSON to the Bucket Policy section. Replace UNIQUE-BUCKET-NAME with the name of your S3 bucket:

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

![S3 bucket policy editor with the JSON policy granting Redis Cloud backup access](/images/site-mirror/e9c9b20b58f7c9edcf02636b2468cd3bffbc21e0-1218x679.webp)

### How do you create and export a backup from ElastiCache?

1.  Navigate back to your ElastiCache instance.
2.  Select the Actions button, and create a Backup.

![ElastiCache console with the Actions dropdown showing the Create Backup option](/images/site-mirror/bf5b0d8ed2eea7aca03fec652fbebce7426f5689-1433x202.webp)

### How do you export the ElastiCache backup to an S3 bucket?

1.  Navigate to the Backup page within ElastiCache and select the Backup you created.
2.  Within the Backup, select Export.

![ElastiCache Backups page with the Export option highlighted](/images/site-mirror/d1fbed417e951d1ebf7ffd99e63320ac93367aac-1433x463.webp)

Select the Target S3 location as the S3 bucket you created earlier.

![Export dialog showing the Target S3 bucket location selector](/images/site-mirror/17108b53f315ee1ab7ad68080ef702c53872b194-1433x362.webp)

Return to the S3 bucket and download the .rdb file that was created.

![S3 bucket file listing showing the exported .rdb backup file ready for download](/images/site-mirror/06450b7fb7927dc901633f31bf49b0aff958271f-1433x332.webp)

### How do you upload the RDB file to Azure Blob storage?

1.  In the Microsoft Azure console, navigate to Storage Accounts.
2.  Create an Azure Blob instance.

![Azure portal Create Storage Account form with fields for resource group and instance details](/images/site-mirror/d1f6f7b3f43c26990621c921fa13133e8e8da414-840x905.webp)

Upload your .rdb file into the Blob container.

![Azure Blob container view showing the uploaded .rdb backup file](/images/site-mirror/9577e11ed1604dff5f3f7bf0dff6030e8afb3448-1120x799.webp)

### How do you create and size an Azure Managed Redis instance?

1.  Navigate to Azure Managed Redis.
2.  Select a size that fits your data set size captured from your ElastiCache instance. The rough estimate for sizing is your \[current data set size \* 1.2\] = AMR data size (round up to the nearest size).

![Azure Managed Redis creation page showing the available cache size tiers](/images/site-mirror/cbaa044b2d5b1d498f06649f3122de969ae24027-771x887.webp)

Select the data modules that you used within your ElastiCache instance (RediSearch, RedisJSON, RedisTimeSeries, RedisBloom).

![Azure Managed Redis module selection with RediSearch, RedisJSON, RedisTimeSeries, and RedisBloom options](/images/site-mirror/9db3d576d55546e77389fd994b3feecfaf02f462-777x827.webp)

Create your instance.

### How do you import the RDB file into Azure Managed Redis?

1.  Navigate to your instance once it's been created.
2.  Go to Administration > Import Data.

![Azure Managed Redis Administration panel with the Import Data option selected](/images/site-mirror/dfda59b6c990e322f853b564469a86cdf14abfab-651x755.webp)

NOTE: Importing will delete existing cache data.

1.  Choose your storage account which has the .rdb blob.
2.  Select the .rdb file you wish to import.

![Azure import dialog showing the storage account and .rdb file selector](/images/site-mirror/47de8d806ffbdcb48dee84f8d205dca8d95fd343-550x859.webp)

Import your data.

### How do you validate the migration and update your application?

After the import completes, verify the data in your new Azure Managed Redis instance:

1.  Connect to the AMR instance using `redis-cli` or your preferred Redis client.
2.  Run `DBSIZE` to confirm the key count matches your source ElastiCache instance.
3.  Spot-check a few keys with `GET`, `HGETALL`, or other commands relevant to your data structures.
4.  Update your application's Redis connection strings to point to the new Azure Managed Redis endpoint.

## Next steps

- [Determine which migration strategy is right for you](/tutorials/migration)
- [Migrate ElastiCache to Redis Cloud](/tutorials/migration/elasticache-to-redis-cloud/)
