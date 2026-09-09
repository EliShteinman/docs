---
title: "Redis Security Course Is Now Live at Redis University"
linkTitle: "Redis Security Course Is Now Live at Redis University"
url: "/blog/redis-security-course-is-now-live-at-redis-university/"
description: "For the past few months, the Redis education team has been working hard on a new course covering Redis security. Today, we’re pleased to announce the general availability of RU330: Redis Security!..."
date: 2020-08-18
blogCategories:
- "Company"
authors:
- "Kyle Banker"
lastmod: 2025-03-27
hidden: true
---

*By Kyle Banker, Sr. Director, Field Engineering · Published 18 August 2020 · updated 27 March 2025*

![Blog tile image](/images/blog/41bfbde67a28d594c783f244ddfa4da403e597ba-1999x1158.webp)

For the past few months, the Redis education team has been working hard on a new course covering Redis security. Today, we’re pleased to announce the general availability of [RU330: Redis Security](https://university.redis.com/courses/ru330/)! If you run Redis in production, then you’ll definitely want to [sign up](https://university.redis.com/courses/ru330/).

If you need more persuasion, then please read on.

## Why Redis Security?

It is a universal truth that any database worth its salt must be secure. But how *do* you secure Redis? If we’re being completely honest, the early development of Redis generally prioritized utility and stability over security.

That’s changed in recent years, though, especially with [the release of Redis 6](/blog/diving-into-redis-6/). Now, you can implement the [principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege) by taking advantage of access control lists ([ACLs](/blog/getting-started-redis-6-access-control-lists-acls/)), and you can secure your Redis connections by [enabling TLS](https://redis.io/topics/encryption) (Transport Layer Security) encryption.

Building on this momentum, we wanted to create the definitive guide to Redis security, and, well, [RU330: Redis Security](https://university.redis.com/courses/ru330/) is the fruit of that effort.

So, who’s teaching this course? Why should you take it? And what are you going to learn?

## Course instructors

The idea for Redis Security started with [Jamie Scott](/author/jamiescott/), a Redis Product Manager focused on security. Speaking daily with our customers about security, Jamie has been deeply involved in the security feature development for open source Redis 6, Redis Enterprise, and Redis Enterprise Cloud. Needless to say, Jamie was the perfect person to spearhead this effort, and Jamie is the lead teacher for most of the Security Course.

I am Jamie’s co-teacher. As a longtime software engineer, technical author, and experienced Redis University [curriculum](https://university.redis.com/courses/ru102j/) [developer](https://university.redis.com/courses/ru202/), I’ve helped Jamie to create what we hope is an engaging, informative course that’s well worth your time.

## What you’ll learn

Our course takes a holistic approach to security education.

Before delving into any Redis-specific topics, we start with some general security principles that we think everyone should know. We cover the basics of information security, including the [CIA triad](https://whatis.techtarget.com/definition/Confidentiality-integrity-and-availability-CIA#:~:text=Confidentiality%2C%20integrity%20and%20availability%2C%20also,with%20the%20Central%20Intelligence%20Agency.) (confidentiality, integrity, and availability), [defense in depth](https://en.wikipedia.org/wiki/Defense_in_depth_(computing)), and the [principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege). This sets the stage for a tour of Redis’ basic security controls. Later in the course, we provide a thorough introduction to encryption and public key cryptography before showing you exactly how to implement TLS in your Redis deployment.

In explaining the reasoning behind Redis’ security features, our goal is to help you make the best decisions when you go to production. For example, we want you to think hard about what level of Redis access your applications actually need. If you’re running a service whose sole job is to return search queries run against [RediSearch](https://oss.redis.com/redisearch/), then you’ll want to create a specific ACL user for that service. The ACL user you define might look something like this:

user searchservice on &gt;secret +FT.SEARCH ~*

This ACL directive creates a user capable of running exactly one Redis command: FT.SEARCH, which queries a RediSearch index. This is a good practice because it reduces the likelihood that your application will do any damage if it’s ever compromised. For instance, your application won’t be able to call FLUSHDB, a command that would drop all Redis data and likely cause your users some discomfort.

## Horror stories

You can think of this course as a series of techniques for avoiding a Redis horror story. In fact, because Redis is deployed so widely, it can be a target for [hackers](https://en.wikipedia.org/wiki/Hacker#Black_hat_hacker) (the bad kind) and [script kiddies](https://en.wikipedia.org/wiki/Script_kiddie). As a kind of motivation, Jamie and I had the idea of featuring a different Redis horror story each week in the course. You’ll learn about some infamous Redis exploits and what might’ve been done to avoid them.

![](/images/blog/904be32ba34695896e498a694e825481ce14a3b8-1024x578.webp)

## Open source Redis

This course focuses on open source Redis, so it’s broadly applicable to most Redis users. Occasionally we’ll point out a feature of [Redis Enterprise](/redis-enterprise/) or [Redis Enterprise Cloud](/redis-enterprise-cloud/), which you might need as you scale the use in Redis in your organization. But Redis is fully committed to open source Redis users as well, so we emphasize open source Redis in this course, just as we do in the other [six Redis University courses](https://university.redis.com/#courses) available today.

## Secure your Redis deployments

You *can* learn Redis security, and you can also thwart most attackers by making the right security decisions. [RU330: Redis Security](https://university.redis.com/courses/ru330/) teaches you all of this, plus a number of principles that you can apply to any system you need to secure.

The course is instructor-paced, lasting three weeks, with one more week for the final exam. Along the way, I will be available in the [course Discord channel](https://discord.com/invite/z2N7Hgz) to answer all your questions or to just say, “Hi.” We hope you’ll [join us](https://university.redis.com/courses/ru330/)!

[Click here to view video](https://www.youtube.com/embed/8TnwCftUfkM)
