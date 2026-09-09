---
title: "New Pricing for Redis Enterprise Cloud"
linkTitle: "New Pricing for Redis Enterprise Cloud"
url: "/blog/new-pricing-for-redis-enterprise-cloud/"
description: "For the last 12 months, we have been working closely with our cloud customers to better understand how our cloud service can meet their needs. Based on those discussions, today we are announcing a..."
date: 2021-02-03
blogCategories:
- "Company"
authors:
- "Aviad Abutbul"
lastmod: 2025-03-27
hidden: true
---

*By Aviad Abutbul, Senior Director of Product Management · Published 3 February 2021 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/13cb009a037331de1a5063b7df111df83bab98bb-1999x1040.webp)

For the last 12 months, we have been working closely with our cloud customers to better understand how our cloud service can meet their needs. Based on those discussions, today we are announcing a new pricing model for our Redis Enterprise Cloud service.

This new pricing model is designed to be as simple as possible, let our users scale up and down instantly, and pay only for the resources they need in a completely serverless fashion. Customers who choose our annual plan can enjoy significant discounts, and use their existing public cloud commits to pay for what we believe is the most advanced Redis cloud service in the market, created by the people behind open source Redis.

## How the new pricing works

[Redis Enterprise Cloud](/redis-enterprise-cloud/overview/) is a fully managed cloud service that allows you to use Redis for more than just simple caching use cases. It offers advanced capabilities like data persistence by default, five-nines (99.999%) availability, Active-Active multi-region deployment, and hosting large datasets on SSDs to dramatically reduce operating costs. With Redis Enterprise Cloud, you can design your real time applications using Redis features, including [Search and Query](/search/), [JSON](/json/), [Time Series](/timeseries/), [Probabilistic](/modules/redis-bloom/), and soon [more](/modules/get-started/).

Our new pricing mechanism also lets you use Redis Enterprise Cloud as a simple caching engine at a very attractive price point, with no operational overhead. You can start using the service with any of the four different plans, and you have the freedom and flexibility to move between plans according to your application needs:

[Watch the video](/redis-enterprise-cloud/pricing/)

### The Free plan

The Free plan lets you run a single non-highly available Redis database with up to 30MB and 30 connections, forever (or as long as you use it)! It lets you run Redis Enterprise Cloud in a selected region across all three major public clouds (Amazon Web Services, Microsoft Azure, and Google Cloud). You can use all available Redis features:[ Search and Query](/search/), [JSON](/json/), [Time Series](/timeseries/), and [Probabilistic](/modules/redis-bloom/). Best of all, it’s totally free, no credit card required.

[**Try our Free plan now**](/try-free/)**.**

### Fixed plans

Redis Enterprise Cloud’sFixed plans let you select anything from 100MB to 10GB of Redis memory; you can create multiple dedicated databases within the plan limit. In addition to supporting all Redis modules, the Fixed plans allow you to deploy your Redis database in a highly available manner over one or more availability zones, with instant failover times.

### The Flexible plan

As the name suggests, the Flexibleplan lets you consume Redis Enterprise Cloud resources in a fully flexible manner. You can create any number of databases, scale them to multiple-terabyte datasets with hundreds of millions of ops/sec, and support an unlimited number of connections, while deploying over a dedicated virtual private cloud (VPC) environment on AWS and Google Cloud.

Besides supporting single- or multi-availability zone deployments with instant failover and enriching your Redis functionality with Redis modules, the Flexible plan allows creating Redis on Flash databases. [Redis on Flash](/redis-enterprise/technology/redis-on-flash/) uses a combination of DRAM and SSD to store your datasets at up to 70% cost savings compared to a pure DRAM deployment.

Furthermore, with the Flexibleplan, you can deploy your Redis databases across multiple regions and clouds in an Active-Passive or an Active-Active manner, allowing you to run Redis with five-nines availability and instant failover across regions and clouds.

[Active-Active Redis](/active-active/) lets you deploy your application in a full globally distributed manner, as close as possible to where your users are located. It uses our conflict-free replicated data types ([CRDTs](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type))-based technology that enables read and write Redis operations from any location without worrying about conflict-resolution problems and maintains Redis’ sub-millisecond local latencies, even across global deployments. Finally, the Flexible plan lets you consume Redis in a serverless manner, without worrying about clusters and nodes, and to be charged only for the memory and throughput you provision.

[**Learn more about our Flexible pricing plan.**](#the-flexible-plan-pricing-model)

### The Annual plan

By committing to a predefined annual consumption in the Annualplan, you can get a significant discount compared to Flexible plan prices. The yearly commitment applies to all your workloads across multiple clouds and regions. The Annual plan lets you use your AWS or Google Cloud commits to consume Redis Enterprise Cloud resources.

[**Learn more about our Annual pricing plan.**](#the-annual-plan)

Let’s take a closer look at each of the new pricing models.

## The Flexible plan pricing model

Sizing your Flexible plan workloads is done using an [online calculator](/redis-enterprise-cloud/pricing/#calculator). Simply specify your database memorylimit (and if your database is highly available, make sure your memory limit takes into account the size of your replica), the expected throughput(in ops/sec) and the number of databases of this type. The screenshot below shows an example of a three-database deployment:

![](/images/site-mirror/1e247f99749598df16797a13ce073e3355fd288c-1024x349.webp)

We use a shard-based pricing model to size your deployment, in which a shard is composed of a Redis server plus the infrastructure needed to host Redis:

![](/images/site-mirror/29b19d5a9eeba6067b5dc55008787f0e3b11a828-1024x319.webp)

In order to provide the best prices across the majority of the Redis use cases, we defined five types of shards, each with a different memory and throughput characteristics and a different price per hour (Note: shard rates vary between cloud providers and regions). The diagram below shows how it works:

![](/images/site-mirror/679dd2e107d96c27efc089b141348c2bae56a232-1024x615.webp)

Here’s how this new shard-based pricing approach maps to the three-database deployment outlined above:

![](/images/site-mirror/548a1e240d43549b7c014dc2656fd0e67b72a06d-1024x623.webp)

As you can see:

- Database 1 is configured with a 1GB memory limit, no replication, and 1,000 ops/sec. It’s mapped to a single micro shard at $0.043/hr (according to AWS/us-east-1 region prices).
- Database 2 is configured with a 5GB memory limit (including the replica size) and 50,000 ops/sec. It’s mapped to 4 high-throughput shards at $0.792/hr.
- Database 3 is configured with a 200GB memory limit (including the replica size) and 25,000 ops/sec. It’s mapped to 8 large shards at $4.680/hr.

Note that we enforce memory and throughput limits per shard to better utilize the memory of underlying cloud instances with minimal overhead. This also lets us parallelize replication and data persistence processes. Enforcing the ops/sec limit helps customers better predict their Redis behavior when combining low and high computational commands. That said, we allow those users who know that a single instance of Redis can process more than 25K ops/sec for their use case to size their databases according to the number of shards rather than by ops/sec.

### A serverless approach: pay only for what you provision

The Flexible plan is built with the mindset of serverless computing, in which you pay only for the memory and the throughput limits you provision, without having to deal with the cloud infrastructure that runs behind the scenes. In other words, you can “forget clusters, forget nodes.”

Redis Enterprise Cloud will always choose the most attractive price/performance cloud infrastructure (instances, network, and storage) to meet your workload needs, and will place and balance your Redis databases across them. The beauty of this approach is that with a single API call you can scale your database up and down and your usage bill will be (instantly) adjusted accordingly. This lets you modify your Redis deployments to account for peak and slow periods in a matter of seconds, keeping your Redis operation as efficient as possible.

This example shows the power of this approach:

![](/images/site-mirror/fa2f58221ac500af658da4dfe66d5e401efb2fd2-1024x466.webp)

- Let’s assume that at time T0, you launch a highly available database with a 10GB memory limit and 10K ops/sec. This will be translated to 2 small shards, priced at $0.622/hr (on the AWS/us-east-1 region).
- Now let’s assume that at time T1 you decide to scale up your database to 100GB and 50K ops/sec to meet peak demand. This will immediately be translated to 4 large shards at a usage cost of $2.34/hr.
- If at time T3 you realize that you need only 50GB memory (while keeping the 50K ops/sec throughput limit), Redis Enterprise Cloud will translate this to 4 high-throughput shards with a usage cost of just $0.792/hr.

## The Annual plan

As noted, the Annual plan provides significant discounts compared to the Flexible plan prices, by committing to a predefined annual consumption. Signing up for an Annual plan requires a short, three-step interaction between you and a Redis sales representative:

![](/images/site-mirror/9335b21a06db08d0c555117d62d374939b34de05-1024x300.webp)

**Step 1:** Our sales representative will walk you through a sizing exercise to estimate your usage and annual spending.

**Step 2: **Establish your annual commit and discount level based on the sizing exercise. For instance, if your spending estimate is $100K/yr and you get a 10% discount, you will pay just $90K to consume $100K Redis Enterprise Cloud resources.

**Step 3:** Once you sign your annual agreement and start consuming your Redis Enterprise Cloud resources, we will monitor your usage on an hourly basis to help you to better understand how your actual consumption compares with your initial commitment.

An annual deal allows you to consume resources across any cloud (currently AWS and Google Cloud) or region. It also lets you consume Redis Enterprise Cloud resources using your existing cloud commits.

## In summary

We believe that our [new cloud pricing approach](/redis-enterprise-cloud/pricing/) is a key step towards improving the Redis Enterprise Cloud experience for both existing and new customers. It allows you to scale up and down instantly and pay only for the amount of data and throughput you were provisioned at any given time, all at an attractive price for memory and throughput.
