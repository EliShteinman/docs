---
title: "How to Use Redis at Least x1000 More Efficiently"
linkTitle: "How to Use Redis at Least x1000 More Efficiently"
url: "/blog/how-to-use-redis-at-least-x1000-more-efficiently/"
description: "The recent Redis’ v2.8.9 was “the strangest beast” in its history of releases. Unlike previous versions, this release solely introduced new Redis functionality rather than defect fixes. As we are..."
date: 2014-05-23
blogCategories:
- "Tech"
authors:
- "Itamar Haber"
lastmod: 2026-08-13
hidden: true
mirrored: true
---

*By Itamar Haber, Technology Evangelist · Published 23 May 2014 · updated 13 August 2026*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

![](/images/site-mirror/04d1bc57de5ba3542613f13dbe995fe3794a53de-625x200.webp)

The [recent Redis’ v2.8.9](https://groups.google.com/forum/#!msg/redis-db/32VPw9X46Sg/GxHLzKeqRc0J) was “the strangest beast” in its history of releases. Unlike previous versions, this release solely introduced new Redis functionality rather than defect fixes. As we are nearing the completion of 2.8.9’s rollout in our Redis Cloud service, I wanted to use this chance to briefly summarize these updates for our users.

### The HyperLogLog Data Structure

First is the addition of the new HyperLogLog data structure to Redis. HyperLogLog allows you to estimate the cardinality of a set or, put differently, get an approximate count of unique items. Even before HLL’s addition, you could use Redis for counting stuff but HLL’s raison d’être is to let you do that using a **fixed amount of memory and constant complexity**. Since there are no free lunches, the tradeoff is that HLL’s count has a standard error of up to 0.81%. If you want to learn more, check out [this post](http://antirez.com/news/75) in which antirez has provided an amazing overview of the HyperLogLog algorithm and some of the challenges in implementing it. Besides Phillipe Flajolet’s [original paper](http://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf), the web has [several](http://stackoverflow.com/questions/12327004/how-does-the-hyperloglog-algorithm-work) [other](http://static.googleusercontent.com/media/research.google.com/en//pubs/archive/40671.pdf) [resources](http://blog.notdot.net/2012/09/Dam-Cool-Algorithms-Cardinality-Estimation) that [explain](http://research.neustar.biz/2012/10/25/sketch-of-the-day-hyperloglog-cornerstone-of-a-big-data-infrastructure/) HLL, including [this nifty visualization](http://www.aggregateknowledge.com/science/blog/hll.html).

Let’s see how HLL can be put to good use, for example by adding a sprinkle of real-time analytics to your application. Assume you want to keep track of how many unique users are using your app throughout the day, hour by hour. Before HyperLogLog, one simple way that you could do that in Redis was by storing the IDs of your users (e.g. their emails) in an hourly set, so for each request you’d do something like:

SADD users:<date>:<hour> <email>


This way, the result of [SCARD](https://redis.io/commands/scard) for any such set would be the number of unique users for that hour. The problem with that approach is that it can consume a lot of memory. If your application is seeing 50K users per hour on average, and assuming each identifier is 25 bytes on average, the average size of any hourly set would be about 12MB. HLL lets you do the same thing using only 12KB, so you could say it is **three orders of magnitude more efficient 😛**

When using HLL we’d count the users with:

PFADD users:<date>:<hour> <email>


And use [PFCOUNT](https://redis.io/commands/pfcount) to obtain the hourly count. But what if you wanted (and you usually do) to have aggregates for different time periods, like 3h, 6h, 12h and 24h? With the SADD/SCARD approach, you’ll either need to dedicate a few more counter sets for each resolution or execute on-demand/periodic [SUNION](https://redis.io/commands/sunion)s, costing RAM and CPU. You could, as shown above, gain considerably by using HLL but there’s actually another big saving with it. Since HLLs can be merged very efficiently, you don’t need to save a counter for each of time resolution and just [PFMERGE](https://redis.io/commands/pfmerge) the relevant counters to get the sums.

### Lexicographical Ordering

Second, there’s lexicographical ordering of sorted sets. When the scores of the sorted sets’ members are identical, the [ZRANGEBYLEX](https://redis.io/commands/ZRANGEBYLEX) command will return a requested range of members using lexical sorting. Compared to the incumbent [SORT](https://redis.io/commands/sort) command with the ALPHA option, the new lexical commands are not only more performant, but also allow the straightforward implementation of [autocomplete-like](https://autocomplete.redis.io/) functionality (although RAM-wise, such sorted sets are more expensive).

Despite the ingenuity of Flajolet’s contraption and all the hard work that went into putting it into Redis, I prefer lexicographical ordering (and not only because of the way it rolls off your tongue). I have two reasons for that specific bias and both are entirely subjective. For starters,[this](https://groups.google.com/d/msg/redis-db/KMKIPtyoJ-w/F0FQJ1EqbkkJ) and [that](https://groups.google.com/d/msg/redis-db/GrCM183WkxM/X8tdr3BG7jwJ) thread from the Redis mailing list unfold the story behind the feature. Besides all the juicy technical details in these correspondences, they give a brilliant demonstration of how much teamwork goes into the making of an open source project — a shining example of Redis’ great community. On top of that, it’s just more practical and screams to be used.

I mean, consider HLL – it lets you count (and [I love to count!](https://twitter.com/CountVonCount)) but that’s basically it. Sure, you want to count lots of different things in the #IoT but that’s about as exciting as it gets. On the other hand, the ability to lexicographically rank members in a set opens up a world of possibilities, like so many other Redis commands. Here’s one neat use – imagine you have a set of email addresses and you need find all the addresses from a certain domain. By indexing (i.e. ZADDing) the reversed version of each address, this becomes just matter of a ZRANGEBYLEX. To index an email address you can use the following Lua:

```python
redis.call("zadd", KEYS[1], 1, ARGV[1]:reverse())

```

And the Lua script to search for addresses in a domain:

```python
local res = redis.call("zrangebylex", KEYS[1], "\[" .. ARGV[1]:reverse(), "\[" .. ARGV[1]:reverse() .. "\\xff")
for k, v in pairs(res) do
  res[k] = v:reverse()
end
return res

```

It’s going to be very interesting to see more ways these new features will be put to use. To start using Redis v2.8.9 with Redis Cloud immediately, just [create a new database](/?login=1). Questions? Feedback? [Email](mailto:itamar@redis.com) or [tweet](https://twitter.com/@itamarhaber) me – I’m highly available 🙂
