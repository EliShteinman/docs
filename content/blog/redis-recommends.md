---
title: "Redis Recommends…"
linkTitle: "Redis Recommends…"
url: "/blog/redis-recommends/"
description: "You just finished watching Narcos, season 2 and are about to slip into the post-binge-watching doldrums, when up pops a recommendation from Netflix. “Because you liked Narcos, you should watch..El..."
date: 2016-09-25
blogCategories:
- "Company"
authors:
- "Leena Joshi"
lastmod: 2026-08-13
hidden: true
mirrored: true
---

*By Leena Joshi, VP Product Marketing · Published 25 September 2016 · updated 13 August 2026*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

![Redis and Golang](/images/site-mirror/cc8701037f89c4639145a9cf9635920dafe54aba-300x250.webp)

You just finished watching Narcos, season 2 and are about to slip into the post-binge-watching doldrums, when up pops a recommendation from Netflix. “Because you liked Narcos, you should watch..El Patron De Mal.”

Its not just Netflix. The New York Times does it, Amazon does it, Google does it, even your teenager’s school’s application has recommendations.

Applications are getting smarter every day and it is no secret that they rely on extremely smart developers and technologies to pull out the insights to make these recommendations. What makes for an effective recommendation? Something you are likely to act on!

How do you get such a recommendation? While there are many algorithms that can crunch hundreds of different variables to get you the right article to read on a Sunday morning, there are some very simple ones too. People who share the same characteristics – geography, demographic, past preferences, past dislikes- make for a rich pool of potential recommenders. Some very simple approaches include just plain old comparisons. Computing which users have the most in common with you, who have done things in the same order as you, which items have they liked that you haven’t looked at yet, gives us a very simple path to generating the next set of recommendations for you.

In developer terms, implementing comparisons can be done in many different ways – but why take the trouble to write complex code to perform these comparisons, when you can use a database with built in set operations, that does it for you?

Redis is one of the few databases in the world that has sophisticated set operations. [Redis Sorted Sets](https://redis.io/topics/data-types) are beloved, powerful and adept at solving a multitude of problems. Built-in set operations are good for many things like time-series data, bid management, scoring, ranking and more. They are also a really simple way of implementing recommendation algorithms.
Conceptually, it is quite simple – you have hundreds and thousands of users- to find the most similar users, you compare users. Simple set intersection operations will get you users who rated the same item, simple set union operations to find all users who rated a group of items. Based on who rated common items similarly, you generate a similarity score and based on this score (Sorted set operations like ZRANGE to extract top similar by range of score), you find the top users similar to the user in question. Performing similar steps to find items they ranked highly, but that have not been purchased/seen by your current user, should give you the top recommendation to make to your user!

The cool thing about Redis Sorted Sets is that they maintain an ordered view of each member by score automatically and in-memory. This, combined with set operations makes for blazing fast retrieval times, which means you can implement a simple, extremely high performance recommendation engine with very little effort. We did just this! We recently [published (on github)](https://github.com/RedisLabs/redis-recommend) the code for a simple Recommendations engine written in Go, and using Redis. The other cool thing about this engine is that it is easily extensible. It is implemented with user scores as its only criterion for calculating similarity, but it is easy to add location, demographic and other characteristics too! [This whitepaper ](/docs/ultra-fast-recommendations-engine-using-redis-go/)describes how it works – so download it along with the code!
