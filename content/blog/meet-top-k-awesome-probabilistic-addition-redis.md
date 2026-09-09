---
title: "Meet Top-K: an Awesome Probabilistic Addition to Redis Features"
linkTitle: "Meet Top-K: an Awesome Probabilistic Addition to Redis Features"
url: "/blog/meet-top-k-awesome-probabilistic-addition-redis/"
description: "You may find yourself wondering whether you should use more probabilistic data structures in your code. The answer is, as always, it depends. If your data set is relatively small and you have the..."
date: 2019-07-02
blogCategories:
- "Tech"
authors:
- "Ariel Shtul"
lastmod: 2025-03-27
hidden: true
---

*By Ariel Shtul · Published 2 July 2019 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/7d68123acde860f40ab8690e8cc5f1ea5ab76267-691x500.webp)

## Background

You may find yourself wondering whether you should use more probabilistic data structures in your code. The answer is, as always, it depends. If your data set is relatively small and you have the required memory available, keeping another copy of the data in an index might make sense. You’ll maintain 100% accuracy and get a fast execution time.

However, when the data set becomes sizeable, your current solution will soon turn into a slow memory hog as it stores an additional copy of the items or items’ identifiers. Therefore, when you deal with a large number of items, you might want to relax the requirement of 100% accuracy in order to gain speed and save memory space. In these instances, using the appropriate [probabilistic data structure](/blog/streaming-analytics-with-probabilistic-data-structures/) could work magic – supporting high accuracy, a predefined memory allowance and a time complexity that’s independent of your data set size.

## Top-K introduction

Finding the largest K elements (a.k.a. keyword frequency) in a data set or a stream is a common functionality requirement for many modern applications. This is often a critical task used to track network traffic for either marketing or cyber-security purposes, or serve as a [game leaderboard](/solutions/leaderboards/) or a simple word counter. The latest implementation of Top-K in our [Probabilistic feature](http://redisbloom.io/) uses an algorithm, called HeavyKeeper1, which was proposed by a group of researchers. They abandoned the usual ***count-all*** or ***admit-all-count-some*** strategies used by prior algorithms, such as Space-Saving or different Count Sketches. Instead, they opted for a ***count-with-exponential-decay*** strategy. The design of ***exponential decay*** is biased against mouse (small) flows, and has a limited impact on elephant (large) flows. This ensures high accuracy with shorter execution times than previous probabilistic algorithms allowed, while keeping memory utilization to a fraction of what is typically required by a Sorted Set.

An additional benefit of using this Top-K probabilistic data structure is that you’ll be notified in real time whenever elements enter into or expelled from your Top-K list. If an element add-command enters the list, the dropped element will be returned. You can then use this information to help prevent DoS attacks, interact with top players or discover changes in writing style in a book.

Initializing Top-K key in Probabilistic requires four parameters:

- K – the number of items in your list;
- Width – the number of counters at each array;
- Depth – the number of arrays; and
- Decay – the probability of a counter to be decreased in case of collision1.

As a rule of thumb, width of k*log(k), depth of log(k) or minimum of 5, and decay of 0.9, yield good results. You could run a few tests to fine tune these parameters to the nature of your data.

## Leaderboard benchmark using Sorted Set vs. Top-K

Redis’ Sorted Set data structure provides an easy and popular way to maintain a simple, accurate **leaderboard**2. With this approach, you can update members’ scores by calling [ZINCRBY](https://redis.io/commands/zincrby) and retrieve lists by calling [ZREVRANGE](https://redis.io/commands/zrevrange) with the desirable range. Top-K, on the other hand, is initialized with the [TOPK.RESERVE](https://redis.io/docs/stack/bloom/TopK_Commands/) command. Calling [TOPK.ADD](https://oss.redis.com/redisbloom/TopK_Commands/#topkadd) will update counters, and if your Top-K list has changed, the dropped item will be returned. Finally, [TOPK.LIST](https://redis.io/docs/data-types/probabilistic/top-k/), as you would expect, returns the current list of K items. To compare these two options, we ran a simple benchmark with the leaderboard use case.

[In this benchmark](https://github.com/RedisBloom/RedisBloom/tree/master/tests/benchmark.py), we extracted a list of the most common words in the book [War and Peace](https://en.wikipedia.org/wiki/War_and_Peace), which contains over 500,000 words. To accomplish this task, Redis Sorted Set took just under 6 seconds and required almost 4MB of RAM with guaranteed 100% accuracy. By comparison, Top-K took, on average, a quarter of that time and a fraction of the memory, especially for lower K values. Its accuracy was 100% in most cases, except for very high Ks where it ‘only’ achieved 99.9% accuracy3.

![](/images/site-mirror/2ca9d42f22b0d653946d485d4504f6c2e21d3d12-1456x2289.webp)

Some interesting takeaways from the results above include:

- Execution time was hardly affected by K value.
- Insufficient depth not only reduced accuracy, but also increased execution time. This might be due to frequent changes to the Top-K list and the processing time that entails.
- Space efficiency was great, and for any reasonable use case we’d expect a 99% RAM saving.

It is important to note that different types of data might be sensitive to different variables. In my experiments, some data sets’ execution time was more sensitive to ‘K.’ In other instances, lower decay values yielded higher accuracy for the same width and depth values.

The new Top-K probabilistic data structure in Probabilistic is fast, lean and super accurate. Consider it for any projects with streams or growing data sets that have a low memory usage requirement. Personally, this was my first project at Redis and I feel lucky to be given the opportunity to work on such a unique algorithm. I could not be more happy with the results!

If you have a use case you would like to discuss, or just want to share some ideas, please feel welcome to email me.

## Footnotes

[1] [HeavyKeeper](https://www.usenix.org/system/files/conference/atc18/atc18-gong.pdf): An Accurate Algorithm for Finding Top-K Elephant Flows by co-primary authors: Junzhi Gong and Tong Yang.

[2] [The Top 3 Game Changing Redis Use Cases](/blog/the-top-3-game-changing-redis-use-cases/).

[3] Lower results in the graph didn’t follow guidelines for width and depth.
