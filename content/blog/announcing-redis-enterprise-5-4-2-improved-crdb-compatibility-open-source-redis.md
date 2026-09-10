---
title: "Announcing Redis Enterprise 5.4.2 with Improved CRDB Compatibility for Open Source Redis"
linkTitle: "Announcing Redis Enterprise 5.4.2 with Improved CRDB Compatibility for Open Source Redis"
url: "/blog/announcing-redis-enterprise-5-4-2-improved-crdb-compatibility-open-source-redis/"
description: "We just released a new version of Redis Enterprise – v5.4.2 and are happy to announce that we’ve added a much requested feature. One of the big highlights of this release is improved compatibility..."
date: 2019-04-16
blogCategories:
- "Company"
- "Tech"
authors:
- "Paz Yanover"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Paz Yanover, Principal Product Manager · Published 16 April 2019 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

We just released a new version of [Redis Enterprise – v5.4.2](/redis-enterprise/software/downloads/) and are happy to announce that we’ve added a much requested feature. One of the big highlights of this release is improved compatibility for active-active Redis (through CRDBs, or conflict-free replicated databases) COUNTER operations with open source Redis.

Redis Enterprise 5.4.2 also contains other new features and capabilities, such as:

- Support for [geospatial data](https://redis.io/commands/GEOADD) in CRDBs
- [SFTP and Mount Point backup locations](https://docs.redis.com/latest/rs/administering/database-operations/database-backup/)
- [Email alerts](https://docs.redis.com/latest/rs/clusters/monitoring/#:~:text=Send%20alerts%20by%20email,for%20the%20database%2C%20click%20Edit.) for team members per database
- [Optional client authentication with TLS](https://docs.redis.com/latest/rs/administering/designing-production/security/tls-configuration/)
- Node [maintenance mode](https://docs.redis.com/latest/rs/clusters/maintenance-mode/)

## Active-active Redis’ compatibility in Redis Enterprise 5.4.2

Prior to version 5.4.2, we treated COUNTERs as a different data type in Redis. In some scenarios, this created conflicts with the way users were used to working with Redis. For instance, unlike SETting a value and then incrementing it using the INCR command in open source Redis, with CRDBs, once you SET a value you couldn’t increment it because it was not treated as a COUNTER.

Since one of the main ideas behind CRDBs is to allow applications to smoothly migrate from a standard Redis deployment to an active-active deployment, we realized that this design must be changed. From now on, any CRDB COUNTER operations will be treated in the exact same manner they are treated in Redis. For example, Redis will check the encoding of the data before applying an operation, so an INCR operation will only succeed if the value is encoded as an integer. CRDBs will now follow this same algorithm.

The above CRDB improvement also applies to other Redis data types, such as Redis Hashes that contain and use Strings.

In order to update String data type behavior for CRDBs, we made changes to its internal structure and the communication protocol between CRDB instances. To enjoy these improvements, you’ll need to install Redis Enterprise version 5.4.2 and then [upgrade](https://docs.redis.com/latest/rs/installing-upgrading/upgrading/) your existing CRDB deployment. This will automatically execute the required Redis server restart. Newly created CRDBs will benefit from active-active compatibility.

## Upgrading a CRDB

The CRDB protocol is backward-compatible, which means that Redis Enterprise 5.4.2 CRDB instances that use the new protocol can understand write operations from instances on versions below 5.4.2. However, it is not forward-compatible, so CRDB instances with the old protocol cannot understand write operations of instances with the newer protocol version. As a result, after you upgrade the CRDB protocol on one instance, other instances that are not yet upgraded may not be able to sync from the upgraded instance, although the upgraded instance will receive updates from both upgraded and non-upgraded instances.

**Therefore, we highly recommend that you upgrade all instances of a specific CRDB within a reasonable time frame to avoid temporary inconsistencies between them.**

Note that:

- After you upgrade an instance to use the new protocol version, it will sync automatically with any missing write operations.
- This process is only required for CRDB protocol upgrades that change basic CRDB behavior. This is an exceptional case and we don’t expect it to be needed for future upgrades.

In order to upgrade the protocol of your CRDBs, follow these [upgrade instructions](https://docs.redis.com/latest/rs/installing-upgrading/upgrading/).

If you’re interested in a more detailed view of what else is new in Redis Enterprise 5.4.2, take a look at our [technical documentation](https://docs.redis.com/latest/index.html) or check out our [release notes](https://docs.redis.com/latest/rs/release-notes/legacy-release-notes/rs-5-4-2-april-2019/).

For any questions, don’t hesitate to drop us a line at pm.group@redis.com!
