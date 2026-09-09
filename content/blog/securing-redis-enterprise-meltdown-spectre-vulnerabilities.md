---
title: "Securing Redis Enterprise from Meltdown and Spectre Vulnerabilities"
linkTitle: "Securing Redis Enterprise from Meltdown and Spectre Vulnerabilities"
url: "/blog/securing-redis-enterprise-meltdown-spectre-vulnerabilities/"
description: "With the recent security vulnerabilities discovered — Meltdown (CVE-2017-5754) and Spectre (CVE-2017-5753 and CVE-2017-5715) — Redis’ engineering, devops and support teams have been working hard to..."
date: 2018-01-08
blogCategories:
- "Company"
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 8 January 2018 · updated 27 March 2025*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

With the recent security vulnerabilities discovered — [Meltdown](https://meltdownattack.com/meltdown.pdf) (CVE-2017-5754) and [Spectre](https://spectreattack.com/spectre.pdf) (CVE-2017-5753 and CVE-2017-5715) — Redis’ engineering, devops and support teams have been working hard to make sure our cloud services, [Redis Enterprise Cloud](/redis-enterprise-cloud/) (REC) and [Redis Enterprise VPC](/redis-enterprise-cloud/) (REV), are protected.

As of now, all our REC and REV clusters on AWS, Azure, GCP and IBM Cloud have been patched by our cloud partners against Meltdown. In addition, some cloud vendors have already managed to mitigate the [Spectre’s branch target injection](https://support.google.com/faqs/answer/7625886) (CVE-2017-5715).

**Redis Enterprise Software (RES) customers:**

- Customers who use RES on the public clouds mentioned above (and deployed RES on dedicated instances without sharing other applications on the same instances) can rely on the hypervisor security patch. An isolated Redis or Redis Enterprise instance cannot be affected by Meltdown or Spectre when Redis modules are disabled or when using Redis’ certified modules.
- Customers who use RES on-premises should deploy the Kernel Page Table Isolation (PKTI) patch. We are still waiting for the formal patch release from all major distributions (such as Amazon Linux, Red Hat Enterprise Linux, and Ubuntu), and will make additional recommendations available in the coming days.

**Performance implications:**

Redis’ engineering team has done a series of tests to validate the effect on the performance of our cloud services. We found that the patch has a negligible impact on our [Redis Enterprise VPC](/redis-enterprise-cloud/) service, between 2.5% – 5%, whereas the impact on our Redis Enterprise Cloud service is in the range of 5%-30%, with minor outliers, depending on the cluster instance types and cloud infrastructure. Our initial tests were performed on our Redis on RAM product, and we plan to extend these to our Redis on Flash product in the coming days and weeks.

We have successfully mitigated performance issues for several customers during the last few days.

**Snippets from our REV tests:**

We tested a 3-node REV cluster on AWS, here is what we found:

Before the Meltdown fix:

![Before-the-Meltdown-fix-graph](/images/blog/382b3fe6283b4df809228b627ffd270870afb33a-1600x674.webp)

After the Meltdown fix:

![After-the-Meltdown-fix-graph](/images/blog/8e5231f5abef3b9c2a6716d4904fa989c80652b2-1149x472.webp)

We observed a negligible impact of throughput (2.5%-5%) and almost no effect on latency.

*Test parameters*

===========

| Cluster |  |
|---|---|
| Cluster instance type | m4.16xlarge |
| Number of nodes in the cluster | 3 |
| Number of master shards | 60 |
| Number of items | 10M |
| Item size | 100B |
| Read/write ratio | 1:1 |
| Load simulation |  |
| Load generation tool | memtier_benchmark |
| memtier_benchmark instance type | c4.8xlarge |
| Number of memtier_benchmark instances | 3 |
| Connections | 1440 |
| Pipeline size | 9 |

The Redis Team
