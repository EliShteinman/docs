---
title: "How to Ace the Redis Certified Developer Exam"
linkTitle: "How to Ace the Redis Certified Developer Exam"
url: "/blog/how-to-ace-the-redis-certified-developer-exam/"
description: "As you may have heard, we recently announced the Redis Certified Developer program. Anyone can sign up for this certification program for free, but only engineers who take and pass the..."
date: 2019-11-19
blogCategories:
- "Company"
authors:
- "Kyle Banker"
lastmod: 2025-03-27
hidden: true
---

*By Kyle Banker, Sr. Director, Field Engineering · Published 19 November 2019 · updated 27 March 2025*

![Blog tile image](/images/blog/66b143b50dd2c2ca21c79b07ade1ce7594f29c66-286x275.webp)

As you may have heard, we recently announced the [Redis Certified Developer program](/blog/redis-developer-certification-is-here/). Anyone can [sign up for this certification program for free](https://university.redis.com/certification/), but only engineers who take and pass the certification exam will become Redis Certified Developers.

So, how do you prepare for the exam? How do you maximize your chances of passing and earning this coveted designation? Whether you’re already a veteran Redis expert or are still earning your spurs, there’s a process to put you on the right path and help ensure that you’re ready for your exam.

To begin, you’ll want to study the study guide and spend time working directly with Redis. Once you think you’re up to speed, take the practice exam to see how you do. If you need more background, Redis University courses are a great way to boost your knowledge. Let’s take a look at all four of these areas:

## Start with the study guide

Not surprisingly, the best way to prepare for the Redis Certified Developer exam is to start with the [study guide](https://university.redis.com/certification/). This comprehensive document covers all of the Redis topics you’ll encounter in the exam and includes many suggestions for study and practice. The guide is divided into seven sections. To give you a sense of what’s in store, check out this brief overview of each section:

**1. General computer science, database, and Redis knowledge**

You don’t need a Computer Science degree to pass this exam, but there is some required foundational knowledge. This includes knowing the difference between a bit and a byte; recognizing that Redis is an in-memory database that supports persistence; and understanding [time-complexity and Big-O notation](https://www.freecodecamp.org/news/time-complexity-of-algorithms/) (note that these topics are also covered in [RU101: An Introduction to Redis Data Structures](https://university.redis.com/courses/ru101/)).

**2. Redis keys**

What is a Redis key? What kinds of operations can you perform on keys? How many keys exist in your Redis database? What’s the TTL on a given key? These are a few of the questions you should be comfortable answering.

**3. Data structures**

Data structures are the crown jewels of Redis—so the exam expects you to know the available data structures and what they do. While we don’t expect you to memorize every command, we do want you to be able to recognize the most common operations for each data structure.

The exam also requires an understanding of the time complexity of these operations. Developers need to be aware of these time complexities to write efficient code against Redis.

**4. Data modeling**

How do you store a domain object in Redis? What about creating unique IDs for these objects? How do you create a leaderboard? Or a queue? Or a stream of unique events?

Being an effective Redis developer means knowing how to use the built-in data structures to solve a variety of domain problems. Since there’s often [more than one way to do it](https://en.wikipedia.org/wiki/There%27s_more_than_one_way_to_do_it), the study guide outlines a set of specific solutions for you to learn from.

**5. Debugging**

All good Redis developers need to know how to debug their code, and this section covers a few of those techniques and commands, such as [MONITOR](https://redis.io/commands/MONITOR). We also intro the Redis protocol, known as [RESP](https://redis.io/topics/protocol).

**6. Performance and correctness**

“Make it work, make it right, make it fast.”

If you’re familiar with Redis data structures, patterns, and debugging, then you can probably “make it work.” But getting everything right and making your code fast requires another level of understanding. In this section of the study guide, we review pipelines, transactions, and eviction policies. We also address the commands that you might want to avoid in production.

**7. Working with Redis clusters**

Writing code against a clustered Redis deployment, such as Redis Enterprise, requires you to understand [shards, hash slots, and hash tags](/blog/redis-clustering-best-practices-with-keys/) (and, no, we’re not talking about the [awkward social networking thingy](https://en.wikipedia.org/wiki/Hashtag)). As you may know, most [multi-key operations](https://docs.redis.com/latest/rs/concepts/high-availability/clustering/#multikey-operations) can be executed against a clustered Redis deployment *only if* all of the keys involved exist on the same shard. This section teaches you the techniques required to run such operations, including Lua scripts, transactions, and GEO commands.

## Get hands-on with Redis

As you’re working through the study guide, it helps to have the Redis CLI at hand. Running Redis commands, and experimenting with the data structures themselves, is one of the best ways to absorb the knowledge you need.

It’s also extremely helpful to write some actual code against Redis. Choose the programming language you’re most comfortable with (note: apart from Lua, there are no language-specific questions on the exam). Try to use *all* of the data structures. Go beyond the basics.

Wondering what to try first? Experiment with [key expiry](https://redis.io/commands/expire). Make sure you’re comfortable with blocking commands (e.g., [BRPOP](https://redis.io/commands/brpop)), [Pub/Sub](https://redis.io/topics/pubsub), and [Redis](https://redis.io/commands/xadd) [Streams](https://redis.io/commands/xread). Try iterating over the keys using [SCAN and a cursor](https://redis.io/commands/scan). And see about [writing Lua script or two](/ebook/part-3-next-steps/chapter-11-scripting-redis-with-lua/).

## Take the practice exam

Once you’ve reviewed the study guide and gotten some hands-on experience, you should be ready to tackle the practice exam. This is an *essential* part of your preparation for the actual certification test. Taking the practice exam will show you the kinds of questions to expect on the certification exam. And as you get your results, you’ll also be able to identify any knowledge gaps and areas of weakness.

Each practice exam question includes an explanation. It’s important to study these explanations as you go through the exam. The explanations often elaborate on the core concepts being tested.

## Take a Redis University course (or three!)

Let’s be clear: Redis University courses are *not* required to take the certification exam. And not all of the topics covered in the exam are discussed in our online courses. Still, taking a few of these courses can go a long way towards making you a Redis expert and preparing you to pass the exam. We recommend starting with the two data structures courses, plus one of our language courses:

**Data structures courses**

1. [RU101: Introduction to Redis Data Structures](https://university.redis.com/courses/ru101/)
1. [RU202: Redis Streams](https://university.redis.com/courses/ru202/)

**Language courses**

*Choose one:*

- [RU102J: Redis for Java Developers](https://university.redis.com/courses/ru102j/)
- [RU102JS: Redis for JavaScript Developers](https://university.redis.com/courses/ru102js/)

![](/images/blog/9610f901229efe6061f3e5360d3e426c4dd4383a-1024x496.webp)

## Final thoughts

If you follow all of the suggestions in the post, you’ll have a great chance of passing your certification exam. Of course, on the day of the exam, be sure that you’re relaxed and well rested. And if you have any questions during your exam preparation process, please don’t hesitate to [send us a note](mailto:certification@redis.com).

Again, we wish you the best of luck!
