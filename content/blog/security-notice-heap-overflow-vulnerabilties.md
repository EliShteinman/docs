---
title: "Redis Security Notice: Heap Overflow Vulnerabilities"
linkTitle: "Redis Security Notice: Heap Overflow Vulnerabilities"
url: "/blog/security-notice-heap-overflow-vulnerabilties/"
description: "Here’s what you need to do about the CVE-2022-24834 and CVE-2023-36824 vulnerabilities, as well as the updates available for affected customers."
date: 2023-07-10
blogCategories:
- "Uncategorized"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 10 July 2023 · updated 27 March 2025*

![Blog tile image](/images/blog/2ce9bd4a215451a1158557748bc4ca2727cac706-720x508.webp)

**Here’s what you need to do about the CVE-2022-24834 and CVE-2023-36824 vulnerabilities, as well as the updates available for affected customers.**

We were made aware that Redis was affected by two security vulnerabilities, CVE-2022-24834 and CVE-2023-36824. CVE-2022-24834 uses a specially crafted Lua script in Redis that can trigger a heap overflow in the cJSON and cmsgpack libraries, resulting in heap corruption and potentially remote code execution. CVE-2023-36824 extracts key names from a command and a list of arguments that can also trigger a heap overflow and result in reading heap memory, heap corruption, and potentially remote code execution.

Redis has, of course, taken action to prevent everyone from harm.

Here’s the current situation, so we can bring the Redis community up to date about [CVE-2022-24834](https://github.com/redis/redis/security/advisories/GHSA-p8x2-9v9q-c838) and [CVE-2023-36824](https://github.com/redis/redis/security/advisories/GHSA-4cfx-h9gq-xpx3). The fix for these vulnerabilities are available in the following releases:

- Redis Enterprise Cloud:
  - CVE-2022-24834: Patched
  - CVE-2023-36824: Patched (Redis 7.0 Preview locations only)
- Redis Enterprise:
  - CVE-2022-24834: 6.2.12-82 and above, 6.2.18-1 and above, 6.4 all minor versions, 7.2.0 and above
  - CVE-2023-36824: Unaffected
- Redis Open Source:
  - CVE-2022-24834: 6.0.20, 6.2.13, 7.0.12, 7.2 RC3
  - CVE-2023-36824: 7.0.12, 7.2 RC3
- Redis Stack:
  - CVE-2022-24834: 6.2.6-v8, 7.2 RC3
  - CVE-2023-36824: 7.2 RC3

CVE-2023-36824 only affects 7.X versions.

No action is needed by Redis Enterprise Cloud customers. However, we encourage all [Redis Enterprise](https://docs.redis.com/latest/rs/installing-upgrading/), [Redis Open Source](https://redis.io/docs/getting-started/installation/), and [Redis Stack](https://redis.io/docs/getting-started/install-stack/) customers to upgrade to a supported and patched version immediately.

We thank the security research community for helping us to keep Redis secure!
