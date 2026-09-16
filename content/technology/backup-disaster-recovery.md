---
title: "Backup & restore"
linkTitle: "Backup & restore"
url: "/technology/backup-disaster-recovery/"
description: "In addition to data-persistence functionality, Redis Enterprise provides out-of-the-box support for backup and restore services."
lastmod: 2026-02-21
mirrored: true
---

*updated 21 February 2026*

In addition to data-persistence functionality, Redis Enterprise provides out-of-the-box support for backup and restore services.

## Backup

Redis Enterprise allows you to backup a snapshot of your database (across all shards) to one of the major public cloud storage solutions (Amazon S3, Azure Blob Storage, or Google Cloud Storage) as well as FTP or Swift services. Before executing the snapshot, Redis Enterprise confirms that there are no outstanding requests in the cluster, thus ensuring consistency. This figure illustrates the backup process:

![Redis Backup & Restore](/images/site-mirror/643c1e76fc90a6fe077d0ed972783d177933b0dc-1240x1040.svg)

## Restore

The restore process is useful in the following cases:

- If you have lost all in-memory copy (or copies) of your data as well as your data persistence files (Note: The likelihood of this scenario is very low if you have deployed Redis Enterprise in a multi-AZ manner with replication and data persistence enabled.)
- When you need to regress your dataset ()Note: In this case, you can seamlessly return to a previous point in time by creating a second database, importing data and switching endpoints once the data loading is complete. This ensures that you can continue to access your data even while the backup is being loaded.)

## Cluster recovery

Cluster recovery is an independent tool that launches a Redis Enterprise cluster from scratch when the cluster reaches an irrecoverable state—when a majority of the cluster nodes are down, for instance. If you use Redis Enterprise as a fully managed service in the cloud (hosted or in your virtual private cloud), the cluster recovery process is executed automatically and governed by our DevOps team.

If you deploy on a Redis Enterprise cluster using Redis Enterprise software, you control the recovery process.

While it’s rare to encounter an irrecoverable cluster state, especially for clusters deployed across multiple availability zones, in order to avoid downtime in these situations we recommend that you use Active-Passive or Active-Active Geo-Distribution deployment.

The cluster recovery process is based on the information written in the Common Cluster Storage (CCS) file—which is constantly backed up during the operation of the cluster—and includes the following steps:

1. Rebuild the cluster, nodes, and storage

![Rebuild the cluster, nodes, and storage](/images/site-mirror/318bf5e8c32047814d591c2c1892bb2de076117e-1408x576.svg)

2. Transfer backup files to local/persistent storage

![Transfer backup files to local/persistent storage](/images/site-mirror/fa73b6e4139d407524430a86f1ccb05d22db5940-1400x762.svg)

3. Load the backup files to DRAM

![Load the backup files to DRAM](/images/site-mirror/a6343db7af1efa9d00713d4449d7e84c5f6bb16a-1400x743.svg)

4. Create replicas and start opening the cluster

![Create replicas and start opening the cluster](/images/site-mirror/9f4e18340fd91311e4b772da846f807dc35acabd-1400x746.svg)
