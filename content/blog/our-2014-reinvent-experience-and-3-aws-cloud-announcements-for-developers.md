---
title: "Our 2014 re:Invent Experience and 3 AWS Cloud Announcements for Developers"
linkTitle: "Our 2014 re:Invent Experience and 3 AWS Cloud Announcements for Developers"
url: "/blog/our-2014-reinvent-experience-and-3-aws-cloud-announcements-for-developers/"
description: "AWS re:Invent 2014 turned out to be an exciting three days for us at Redis. Amazon revealed a considerable amount of announcements this year that are especially exciting for the developers among us..."
date: 2014-11-24
blogCategories:
- "Company"
authors:
- "Leena Joshi"
lastmod: 2025-03-27
hidden: true
---

*By Leena Joshi, VP Product Marketing · Published 24 November 2014 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

![](/images/site-mirror/7deb15dbe677284dee592e01279e2b35418b272a-300x200.webp)

AWS re:Invent 2014 turned out to be an exciting three days for us at Redis. Amazon revealed a considerable amount of announcements this year that are especially exciting for the developers among us (we’ll discuss the highlights in our summary below). As seasoned AWS re:Invent sponsors and exhibitors, having taken part in all three conferences, we highly enjoyed it, as always, and learned quite a lot from the keynotes, breakout sessions, and interactions with the impressive attendees.

We were delighted that Bleacher Reports and Hotel Tonight, both of whom use Redis to support their vast needs for excellent Redis performance and availability, collaborated with us at our booth. We’d like to thank them for sharing their stories with those who visited us. We also gave away various goodies this year, including Redis Geek baby swag, which was catalogued by Carmen Barr, wife of the AWS evangelist, Jeff Barr, in her [tour of re:Invent swag](http://instagram.com/carmenzbarr). We are happy to see that so many toddlers are going to be future Redis Geeks 🙂

## 3 AWS re:Invent Announcements

Three major announcements, of many, were made by Amazon’s Andy Jassy and Werner Vogels in the keynotes on the last two days of the event.

### 1. Lambda – An Event Driven Service

The most prominent announcement of the event was the introduction of Lambda. It is an interesting new AWS service that helps developers code on top of AWS’ infrastructure, which we see as a big step towards Amazon’s pure PaaS (Platform-as-a-Service) model. With Lambda, developers don’t need to manage their underlying compute resources. It runs code written in JavaScript, and is powered by a server-side Node.js, while performing general requests, like image uploading, or custom requests in backend services. Amazon then bills by the amount of computing that was consumed in order to run the code. We recommend that you check out [the tests](http://alestic.com/2014/11/aws-lambda-environment) done by [@esh](https://twitter.com/esh) that explore the AWS Lambda file system and runtime environment. As a developer, this service can become your best friend, since you won’t need to waste time building a new VM to run your code.

### 2. EC2 Container Service

Amazon knows that developers love Docker containers, and accordingly introduced the EC2 Container Service. Containers separate applications from their underlying infrastructure, easing IT operations like portability and environment replication, making Docker container support essential to easily run a distributed application. This new Amazon service facilitates container management aspects such as cluster management, authentication, firewalling, and movement between different availability zones. Amazon provides this service for free which makes sense as it facilitates infrastructure provisioning for every application.

### 3. Amazon RDS for Aurora

The third notable announcement was AWS’ launch of Amazon Aurora. In today’s web applications and mobile apps, such as online games, we see users increase from hundreds to millions in a matter of months, which isn’t truly supported by any of the current relational database offerings. According to Jeff Barr, the principles that these databases were built upon are old, all database operations start and end on one single server. However, according to Andy Jassy, Amazon recognized this and came up with Aurora, the second generation of RDS, built by the RDS team over the last 3 years. The team rewrote the MySQL engine, the most popular open source database. Amazon used their cloud capacity and scale in order to support an enhanced read replica mechanism, that, relies on a scalable infrastructure to achieve better performance than in RDS. In addition, with Aurora, a master database is replicated in 3 AZs parallelly, and all of the replicas are directly linked to the master server, allowing for higher availability and durability.

## Final note

It was remarkable to see that the conference tripled itself in all dimensions, including the amount of exhibitors, attendees, and even tweets. We expect this conference to grow even more next year, just like AWS. This year’s announcements have demonstrated Amazon’s amazing innovation, positively disrupting the IT industry time and time again. Needless to say, we’re excited for next year’s AWS re:Invent!
