---
title: "Redis Developer Hub Expands to Support the Needs of DevOps Teams"
linkTitle: "Redis Developer Hub Expands to Support the Needs of DevOps Teams"
url: "/blog/redis-developer-hub-expansion/"
description: "The Redis Developer Hub has always been a great resource for developers looking to build with Redis. With more than 200+ free tutorials, which were accessed by millions of developers over the last..."
date: 2022-04-06
blogCategories:
- "News"
- "Tech"
authors:
- "Talon Miller"
- "Ajeet Raina"
lastmod: 2025-07-03
hidden: true
---

*By Talon Miller, Ajeet Raina · Published 6 April 2022 · updated 3 July 2025*

![Blog tile image](/images/site-mirror/56871e62057cfe57b336bb7ec1197244597ed75a-772x550.webp)

![redis developer home page](/images/site-mirror/91a0ac8565dffccfdd1382326eef2ad2a8c83ccc-600x244.webp)

The [Redis Developer Hub](/learn/) has always been a great resource for developers looking to build with Redis. With more than 200+ free tutorials, which were accessed by millions of developers over the last year, it offers invaluable training and instruction for developers looking to [**Create**](/learn/create/)**, **[**Develop**](/learn/develop/)**,** and [**Explore**](/learn/explore/)**.**

However, Redis recognizes that DevOps teams must focus on different things than developers do—issues such as stability, maintainability, and keeping a consistent flow of applications improved and deployed. Your job as a DevOps professional requires you to think holistically, deploying and maintaining many apps on your infrastructure frequently at a worldwide scale. Recognizing the specific challenges of DevOps, we have now expanded the Redis Developer Hub to specifically address the needs of DevOps professionals.

## Welcome to the new DevOps Hub

Today, with the addition of [**Operate,**](/learn/operate/) we are announcing an exciting milestone for developers, DevOps engineers, and SREs seeking to learn how to easily integrate Redis into their DevOps cycle to accelerate application deployment.

### What’s new in “Operate”?

![what's new in operate](/images/site-mirror/96ac9ebc003edd0c44df50056a4344f4f5fc209a-1024x226.webp)

Redis has become a [popular database choice](https://insights.stackoverflow.com/survey/2021#most-loved-dreaded-and-wanted-database-love-dread/), not only for developers but among DevOps teams, due to its unmatched simplicity and exceptionally high performance. In [Datadog’s 2021 Container Report](https://www.datadoghq.com/container-report/) Redis was the most popular container image running in Kubernetes [StatefulSets.](https://docs.redis.com/latest/platforms/kubernetes/kubernetes-with-operator/) Redis fits very well into the DevOps model due to its ease of deployment, reduced management toil, and low overhead. Redis Enterprise offers uninterrupted high availability, low latency, and automated linear scalability—all crucial features for DevOps teams.

![bar chart of top containers](/images/site-mirror/b4bf273b4d4a2b72bc9f9987c48411e3a5124d43-1024x582.webp)

Here at Redis, we know that rapid deployment is key to a successful DevOps approach. Therefore, in [this new section of our Developer Hub](/learn/operate/), we have introduced a collection of rich technical content to help DevOps and development teams operate Redis at a faster pace.

### Continuous integration and continuous deployment

Databases are now part of the continuous integration and continuous deployment (CI/CD) pipeline. If a DevOps pipeline doesn’t include the database, it becomes a bottleneck that slows down the delivery of new features. In fact, DevOps teams integrate databases not only in the development pipeline but also in the overall release pipeline. To address this reality, we have included tutorials to help you embed Redis easily into your [CI/CD](/learn/operate/continuous-integration-continuous-deployment/)[ pipeline](/blog/how-to-embed-redis-into-your-continuous-integration-and-continuous-deployment-ci-cd-process/).

One method to embed Redis into your CI/CD pipeline is through Argo CD. We have a tutorial that goes through what Argo CD is, how it works, and ultimately how to deploy an application with Redis Enterprise inside of an Argo CD pipeline.

### Observability

Observability goes significantly beyond basic monitoring and is a key capability for high-performing DevOps teams. Therefore, we’ve introduced tutorials around the tools and techniques that enable DevOps teams to observe key indicators to operate Redis at scale, such as throughput, latency, and capacity.

An example of how you can stay on top of key service level objectives (SLOs) on your Redis Enterprise database and/or cluster is through our integration with[ Datadog](https://docs.datadoghq.com/integrations/redisenterprise/). We have a [tutorial](/learn/operate/observability/datadog/) that goes through crucial Redis service level agreements (SLAs), key performance indicators to watch, and how to get started with this integration to improve observability.

### Provisioning

DevOps teams strive to provision and manage their databases just like they do with application code. Changes to databases are recognized as just another code deployment to be managed, tested, updated, automated, and improved with the same kind of seamless, robust, reliable methodologies applied to application code.

An example of how you can efficiently provision Redis Enterprise is through Azure Cache using [Terraform](https://docs.redis.com/latest/rc/cloud-integrations/terraform/). We now have a [tutorial](/learn/operate/provisioning/azure-cache-terraform-private/) that dives into the key features of Azure Resource Manager to manage your Redis Enterprise cluster and instructs you on how to get started withthe [**Azure Cache for Redis Enterprise using Terraform with Private Link**](https://docs.redis.com/latest/rc/cloud-integrations/terraform/)**.**

### Orchestration

Orchestrating databases is a unique challenge for DevOps teams. Rapid release of new application features and reduction in deployment time are the two primary concerns for most DevOps teams today. That’s why we address orchestration in our new DevOps resources to help you quickly and efficiently provision Redis and accelerate app deployment.

An example of orchestrating a Redis Enterprise database and/or cluster is learning about how to run a [Node.js application](/learn/operate/docker/nodejs-nginx-redis/) using Nginx, Docker, and Redis as the database with a detailed step-by-step tutorial.

Does our new DevOps journey sound exciting? We invite you to check it out today and we welcome your feedback and comments. Feel free to [contribute](https://github.com/redis-developer/redis-developer.github.io#how-to-contribute) by [raising a Pull Request](https://github.com/redis-developer/redis-developer.github.io/pulls/).
