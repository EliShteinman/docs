---
title: "Memorystore to Azure Managed Redis (AMR)"
linkTitle: "Memorystore to Azure Managed Redis (AMR)"
url: "/tutorials/learn/migration/memorystore-to-azure-managed-redis/"
description: "Before migrating to Azure Managed Redis, you should evaluate the migration and consider the best option. Read this guide to determine which migration strategy is right for you. If you are..."
group: "For developers"
aliases:
- "/tutorials/learn-migration-memorystore-to-azure-managed-redis/"
date: 2026-02-25
lastmod: 2026-02-27
hidden: true
---

*Published 25 February 2026 · updated 27 February 2026*

> **TL;DR:**
>
> To migrate from Google Cloud Memorystore to Azure Managed Redis, export your Memorystore data as an RDB file to a Google Cloud Storage bucket, download it, upload it to Azure Blob Storage, then import it into a new Azure Managed Redis instance.

## What you'll learn

- How to export data from Google Cloud Memorystore as an RDB backup
- How to transfer an RDB file from Google Cloud Storage to Azure Blob Storage
- How to create and size an Azure Managed Redis instance for your workload
- How to import an RDB backup into Azure Managed Redis

## Prerequisites

- A Google Cloud Platform (GCP) account with an active Memorystore for Redis instance
- An Azure subscription with permissions to create storage accounts and Azure Managed Redis instances
- Access to both the [Google Cloud Console](https://console.cloud.google.com) and the [Microsoft Azure Portal](https://portal.azure.com)

## How do I choose the right migration strategy?

Before migrating to Azure Managed Redis, you should evaluate the migration and consider the best option. Read this guide to [determine which migration strategy is right for you](/tutorials/migration). If you are considering migrating to Redis Cloud instead, see [Migrate Memorystore to Redis Cloud](/tutorials/migration/memorystore-to-redis-cloud/).

NOTE: Reach out to our team for support on live migrations.

## How do I export data from Memorystore using offline migration?

### Create a Google Cloud Storage bucket with proper permissions

Open [Google Cloud Storage bucket](https://console.cloud.google.com/storage/browser).

![Creating a new Google Cloud Storage bucket for Memorystore backups](/images/site-mirror/4098de78f4f4d9a0facc2593d081e2d5479fe61c-830x389.webp)

1.  Create a new bucket to store Memorystore backups.
2.  Click Save.

### Export from Memorystore to Google Cloud Storage bucket

1.  Navigate to the Overview page of your Memorystore instance.

NOTE: Make note of the data size of your instance, you will need it when creating your Azure Managed Redis instance.

![Memorystore for Redis overview page showing instance details and data size](/images/site-mirror/066ed087cc22a09d86ee4a158da003a91517976d-1433x485.webp)

1.  Select Export in the top right.

![Selecting the Export option in the Google Cloud console for Memorystore](/images/site-mirror/a20607c5db14cc5b539e7eaba84dbea45ea38c8d-1433x485.webp)

1.  Find the Google Cloud Storage bucket created in the previous step.
2.  Select that bucket.
3.  Click Export.

### Download from the Google Cloud Storage bucket

1.  Navigate to the Google Cloud Storage bucket.
2.  Select the bucket you saved the .rdb file in.
3.  Download the .rdb file to your local machine.

![Downloading the exported .rdb backup file from Google Cloud Storage to your local machine](/images/site-mirror/b0dc8a0137bd83c3f0837358aad72ab3959e1546-1433x548.webp)

## How do I import data into Azure Managed Redis?

### Upload the RDB file to Azure Blob Storage

1.  In the Microsoft Azure portal, navigate to Storage Accounts.
2.  Create an Azure Blob storage instance.

![Creating an Azure Storage Account in the Microsoft Azure portal for RDB file upload](/images/site-mirror/7dd902436c60bd7134e9601aed1029fef49d6557-853x864.webp)

1.  Upload your .rdb file into the Blob container.

![Uploading the exported .rdb backup file to an Azure Blob storage container](/images/site-mirror/f2df2f1f10b0a39864b8e2c0064c60a9306b9d93-1253x593.webp)

### How do I create and size my Azure Managed Redis instance?

1.  Navigate to Azure Managed Redis in the Azure portal.
2.  Select a size that fits your data set size captured in the initial steps on Memorystore. The rough estimate for sizing is your \[current data set size \* 1.2\] = AMR data size (round up to the nearest size).

![Sizing the Azure Managed Redis instance to match the Memorystore data size](/images/site-mirror/47c212278f3f2b1b8c6d9faebf422756d7591105-874x864.webp)

1.  Select the data modules that you used within your Memorystore instance (RediSearch, RedisJSON, RedisTimeSeries, RedisBloom).

![Selecting relevant Redis data modules such as RediSearch and RedisJSON during Azure Managed Redis setup](/images/site-mirror/9db3d576d55546e77389fd994b3feecfaf02f462-777x827.webp)

1.  Create your instance.

### Import the RDB file into Azure Managed Redis

1.  Navigate to your instance once it's been created.
2.  Go to Administration > Import Data.

![Importing data from Azure Blob Storage into the new Azure Managed Redis instance](/images/site-mirror/8293fce27cd650ebafc738c65e7db8032441e1d0-832x798.webp)

NOTE: Importing will delete existing cache data.

1.  Choose your storage account which has the .rdb blob.
2.  Select the .rdb file you wish to import.

![Selecting the .rdb backup file from the Azure storage account for data import into Azure Managed Redis](/images/site-mirror/e302b052eef21a3d5d576a4013bc33be1d13bc63-801x825.webp)

1.  Import your data.

## Next steps

- [Determine the best migration strategy for your use case](/tutorials/migration)
- [Migrate Memorystore to Redis Cloud](/tutorials/migration/memorystore-to-redis-cloud/) for an alternative cloud destination
