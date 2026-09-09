---
title: "Redis Enterprise Cloud Releases Terraform Version 1.0.0"
linkTitle: "Redis Enterprise Cloud Releases Terraform Version 1.0.0"
url: "/blog/redis-enterprise-cloud-terraform-1-0-0/"
description: "Redis is investing in its Terraform registry, helping developers manage their databases across multiple modules easily. Let’s see what new updates Redis Enterprise Cloud’s Terraform version 1.0.0..."
date: 2022-08-31
blogCategories:
- "Product Releases"
authors:
- "Noam Stern"
lastmod: 2025-03-27
hidden: true
---

*By Noam Stern, Sr. Product Manager, Products · Published 31 August 2022 · updated 27 March 2025*

![Blog tile image](/images/blog/e52cffc4ae0ae4a941d16aec9562a67df2a9536b-772x550.webp)

**Redis is investing in its Terraform registry, helping developers manage their databases across multiple modules easily. Let’s see what new updates Redis Enterprise Cloud’s Terraform version 1.0.0 brings, how to implement it, and what to consider before upgrading.**

[Terraform](https://www.terraform.io/) is an infrastructure as code (IaC) tool that enables users to manage, build, change, and version their infrastructure safely and efficiently. [Redis Enterprise Cloud ](/redis-enterprise-cloud/overview/)solutions support multiple Terraform resources, such as accounts, subscriptions, and databases for a different [cloud provider](/cloud-partners/microsoft-azure/). Let’s see what changes you can expect with Terraform 1.0.0.

Create a Terraform subscription.

## Introducing Terraform version 1.0.0

The most significant difference between prior versions and version 1.0.0 is that the database resource is extracted from the subscription resource. Until now, the database was a nested block inside the subscription resource.


Now, we are introducing a new resource called **‘rediscloud_subscription_database**,’ which will allow users to manage their databases on a separate logical resource and even by different configuration files if required. It can decrease provisioning time, improve the user experience, and even increase security in scenarios where other team members have different permissions on the databases within a subscription.

Redis has also improved some of the functionalities in its resources. One critical implementation is users can create or modify a database with multiple [modules](/modules/get-started/). You can read about the changes in the Terraform Redis Cloud Provider [CHANGELOG](https://github.com/RedisLabs/terraform-provider-rediscloud/blob/main/CHANGELOG.md).

## How to upgrade to Terraform version 1.0.0 using Redis

[Click here to view video](https://www.youtube.com/embed/2IV2unjQqd8)

The new version contains breaking changes. If you’re already using Terraform for Redis resources with a version prior to version 1.0.0, you must import your existing configuration file to a new directory before upgrading the version.

The process is straightforward. It usually won’t take more than 10 minutes (depending on the number of resources in your TF configuration file). Watch the video above for a quick walkthrough of how the importing process works.

[Follow the four steps guide in the Redis registry in Terraform.](https://registry.terraform.io/providers/RedisLabs/rediscloud/latest/docs/guides/migration-guide-v1.0.0)
