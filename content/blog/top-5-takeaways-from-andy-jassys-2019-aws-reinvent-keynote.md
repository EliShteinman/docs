---
title: "Top 5 Takeaways from Andy Jassy’s 2019 AWS re:Invent Keynote"
linkTitle: "Top 5 Takeaways from Andy Jassy’s 2019 AWS re:Invent Keynote"
url: "/blog/top-5-takeaways-from-andy-jassys-2019-aws-reinvent-keynote/"
description: "AWS re:Invent really is the Super Bowl for cloud computing and enterprise software. Every company—including AWS—brings their latest and greatest innovations to the show."
date: 2019-12-12
blogCategories:
- "Company"
authors:
- "Ryan Powers"
lastmod: 2025-03-27
hidden: true
---

*By Ryan Powers · Published 12 December 2019 · updated 27 March 2025*

![Blog tile image](/images/blog/4671a538f6957cd279ee1a2035a90d620e01aa75-811x479.webp)

AWS re:Invent really is the Super Bowl for cloud computing and enterprise software. Every company—including AWS—brings their latest and greatest innovations to the show.

This year, AWS CEO Andy Jassy made a ton of announcements in his highly anticipated keynote address, which focused on the need to adopt cloud-native architectures for shifting infrastructure to the cloud. He also shared a lot of information on where the cloud giant is heading, as well as benchmarks for where AWS customers are on their cloud journey. Thousands of attendees visited the Redis booth at the show, and not surprisingly many of them wanted to talk about issues raised in Jassy’s keynote. They wanted to know how to future-proof their data layer strategy as they modernize their infrastructure architectures. And many wanted to understand how they could utilize Redis beyond caching and make it their primary database. You can watch Jassy’s entire keynote here, but this post will address our top five takeaways from the almost three-hour talk, and how they affect Redis users.

[Click here to view video](https://www.youtube.com/embed/7-31KgImGgU)

## Takeaway #1: The vast majority of IT is still on premises

According to Jassy, **a whopping 97 percent** of [the $3.7 trillion IT market](https://www.gartner.com/en/newsroom/press-releases/2019-10-07-gartner-says-global-it-spending-to-grow-06-in-2019) is still on premises, in corporate servers and data centers, and not yet in the cloud! Despite the cloud’s undeniable momentum, it remains critical to build and purchase solutions that will work not only in the cloud but also on-premises. In that vein, the most common question from Redis booth visitors was, “How do I reconcile my data in the cloud with data on-premises, and even data in different geographies?”

At Redis, we see a lot of companies still maintaining applications on-premises even as they begin shifting workloads to the cloud. That makes it an absolute necessity to have a data layer that enables a hybrid and multi-cloud strategy.

And that’s only part of the equation. Not only are modern applications being built on hybrid infrastructure or even multiple clouds, they are also geo-distributed. In efforts to lower latency and comply with data regulations, many cloud-native companies are pushing instances across the US and even around the world. When it comes to supporting multi-geo applications with a scalable, geo-local, low-latency database [Redis Enterprises’ Active-Active](/docs/developing-apps-using-active-active-redis-enterprise/) features have you covered whether you’re using a hybrid or multi-cloud approach.

## Takeaway #2: Use the right database for the job

![](/images/blog/c8fd8df6eefab277f8e9da4d71e59b2b5b1a2d27-1024x313.webp)

In the prelude leading up to Jassy’s announcement of Amazon’s managed Cassandra service, he talked about AWS’ commitment to creating purpose-built databases that are the right tools for your job. The days of using your Oracle database for everything are over.

AWS is suggesting multiple databases because each one works with a particular data model, but here’s the thing: like Oracle, each one is a standalone product. Redis Enterprise, on the other hand, offers the best of both worlds: one cluster, multiple data models. That combination resonated powerfully for the many Redis booth visitors who were looking for a tool that could give them a unified view into their cache and database as well as support their myriad of use cases and data models.

Imagine a world where you have the right tools for the job, *and they all share one easy-to-learn and easy-to-use user interface. *The first step to this promised land is what you get with the newly announced [RedisInsight](/insight/), an open source tool that provides the visibility you need to reduce memory usage, track keys, monitor commands in real-time, and manage your Redis clusters. RedisInsight also gives you visibility into [Redis Enterprise’s modules](/modules/), such as RediSearch, RedisGraph, and RedisTimeSeries, which let our customers use the best data models for their needs—all within the unified Redis Enterprise interface. Teams can build real-time applications quickly, while reducing the operational complexity associated with developing across multiple databases with different UIs.

## Takeaway #3: AWS continues to build on top of the open source community

AWS’ announcement of a new managed Cassandra service is effectively building on top of the Cassandra OSS community and providing a managed solution. This is similar to what AWS has done with other open source projects, including ElasticSearch and even Redis. AWS claimed in a [press release](https://aws.amazon.com/blogs/opensource/contributing-cassandra-community/) accompanying the keynote that this move will actually help the Cassandra OSS community. We look forward to AWS making good on its promise to give back to the OSS community that it relies on for the foundation of many of its services.

At Redis, open source is core to our DNA. [Salvatore Sanfilippo](/press/redis-creator-salvatore-sanfilippo-antirez-joins-redis-labs/), the founder of open source Redis—the [world’s most popular database](/blog/redis-named-loved-database-third-consecutive-year/) with more than** 5.3 million container launches per day**—is part of the Redis team. We have helped guide open source Redis since the beginning, and the** vast majority of commits to the open source code have come from Redis.**

## Takeaway #4: AWS customers continue to rapidly adopt containers and Kubernetes

Like other cloud vendors, AWS is putting a lot of eggs in the Kubernetes basket. During his keynote, Jassy revealed that [AWS EKS will now be available on AWS Fargate](https://aws.amazon.com/blogs/aws/amazon-eks-on-aws-fargate-now-generally-available/). Containers and Kubernetes are becoming the de facto way of building cloud-native applications along with increasingly popular new serverless compute options. Cloud vendors are racing to create feature-rich experiences for their customers re-architecting their applications to take advantage of the new cloud-native stack.

Redis Enterprise is built with this stack in mind. You can seamlessly deploy, monitor, and administer Redis Enterprise containers as a cloud-native database service in your Kubernetes cluster to reduce deployment complexity, enhance operational readiness, and accelerate your application development and delivery. To learn more, download our free [Microservices with Redis Enterprise on Kubernetes whitepaper](/docs/microservices-on-kubernetes/).

## Takeaway #5: Cost reduction remains top of mind for AWS customers

![](/images/blog/1f918725e03439ef74001fe97487bc47ca2acd00-300x171.webp)

Jassy announced a number of new and upgraded AWS instances, including the [M6g, R6g, CRg EC2 instances](https://aws.amazon.com/about-aws/whats-new/2019/12/announcing-new-amazon-ec2-m6g-c6g-and-r6g-instances-powered-by-next-generation-arm-based-aws-graviton2-processors/), and [Inf1 EC2 instances](https://aws.amazon.com/about-aws/whats-new/2019/12/introducing-amazon-ec2-inf1-instances-high-performance-and-the-lowest-cost-machine-learning-inference-in-the-cloud/) for machine-learning use cases.

Fun fact: the largest cost factor in machine learning use cases comes in the work needed to make predictions (up to 90%, according to Jassy). Training the models can also be expensive, but the inferences needed to make predictions generates the bulk of costs. AWS developed the inf1 instances to help drive down the cost-per-inference.

The extensive amount of data from modern use cases like machine learning, AI—and the need for low latency data in conjunction with these use cases—was another big topic of conversation at the Redis booth. Inevitably, questions of scalability and performance quickly turn to cost effectiveness. Booth visitors wanted to understand how we compared to other cloud managed Redis services, and we were proud to note that we are objectively one of the most cost-effective and fastest options at scale. We understand the cloud’s promise to drive down costs and that is one of the core values we provide to our customers. Learn more about [Redis Enterprise’s advantages here](/enterprise/).

## Summary

As you build out your roadmap for 2020, don’t forget about the data layer. Can your primary database handle the scale and low-latency requirements of modern cloud-native applications for all your use cases while minimizing operational complexities and its associated costs?

If you missed us in Vegas, no worries, we’ve got you covered. To learn more about how your organization can leverage Redis Enterprise for hybrid and multi-cloud environments and cloud-native architectures with the highest performance at the lowest cost, visit the Redis Growth Happens page now!
