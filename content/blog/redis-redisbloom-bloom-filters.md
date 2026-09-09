---
title: "Probably and No: Redis, Probabilistic, and Bloom Filters"
linkTitle: "Probably and No: Redis, Probabilistic, and Bloom Filters"
url: "/blog/redis-redisbloom-bloom-filters/"
description: "I’ve got a problem. I have tens of millions of players in my online game World of EverCraft (Not a real game. But if it was, it would be from Blizzards of the Coast!). This is a great problem to..."
date: 2020-03-26
blogCategories:
- "Tech"
authors:
- "Guy Royse"
lastmod: 2025-03-27
hidden: true
---

*By Guy Royse, Developer Advocate · Published 26 March 2020 · updated 27 March 2025*

![Blog tile image](/images/blog/a175d9db7cf27152144914a4d7021ab80b3fdf3f-644x437.webp)

I’ve got a problem. I have tens of millions of players in my online game World of EverCraft (Not a real game. But if it was, it would be from Blizzards of the Coast!). This is a great problem to have. So many gamers!

But when a new user signs up, it takes forever to determine if their desired username is taken or not. It’s a simple enough query but the vast amount of data makes it slow.

Switching to Redis helped. Instead of a simplistic but slow SQL query:

> SELECT COUNT(*) FROM Users WHERE UserName = 'EricTheCleric'

We ended up with a simplistic but fast Redis command:

> SISMEMBER Users 'EricTheCleric'

Win!

But all these users are still taking up a mountain of memory. Tens of millions of users will do that. Is there some way to make our data smaller, more compact?

Yes. I present to you the Bloom filter.

## What the heck’s a Bloom filter?

A Bloom filter is a type of probabilistic data structure. We’ve [talked](/blog/count-min-sketch-the-art-and-science-of-estimating-stuff/) [about](/blog/count-min-sketch-the-art-and-science-of-estimating-stuff/) [them](/blog/count-min-sketch-the-art-and-science-of-estimating-stuff/) [before](/blog/count-min-sketch-the-art-and-science-of-estimating-stuff/). In short, a [probabilistic data structure](/blog/streaming-analytics-with-probabilistic-data-structures/) uses hashes to give you faster and smaller data structures in exchange for a bit of uncertainty. Think of a Bloom filter as a set with limited capabilities. We can only add things to it and check if specific things are in it. But the responses to that checking is a little weird. A Bloom filter has two possible responses:

1. *No*—that thing is definitely not in the set.
1. *Probably*—that thing might be in the set.

Might. That’s the weird part, the uncertainty. But fear not. The degree of uncertainty is small and completely under your control using the Bloom filter in the [Probabilistic feature](/modules/redis-bloom/) . I’m going to show you how to use it and control the uncertainty.

## Using Bloom filters with Probabilistic

Let’s go back to World of EverCraft. I have tens of millions of unique usernames for my game that I need to check before I create a new user.

Before, I was doing this:

> SISMEMBER Users 'EricTheCleric'

And then this if the username was available:

> SADD Users 'EricTheCleric'

Let’s look at this process with a Bloom filter. There are two possible scenarios here:

1. Scenario A: the username is available.
1. Scenario B: the username is probably taken.

## Scenario A: Username is available

Alice the Allomancer wants to create a World of EverCraft account. We check to see if her username is in the Bloom filter:

> BF.EXISTS UserFilter 'AliceTheAllomancer'

BF.EXISTS returns 0, indicating that AliceTheAllomancer is not in the set and is available. We add her:

> BF.ADD UserFilter 'AliceTheAllomancer'

> SADD Users 'AliceTheAllomancer'

Easy peasy.

## Scenario B: Username is probably taken

Bob the Barbarian also wants to create an account. We look to see if *his* desired username is in the Bloom filter:

> BF.EXISTS UserFilter 'BobTheBarbarian'

BF.EXISTS returns 1. The username is probably taken. Pick a new one.

Now, I know what you’re thinking. What if it actually* isn’t *taken. Shouldn’t we check? What if we have callously denied Bob the Barbarian his desired username when it was actually available?

While I can appreciate not wanting to make a barbarian wielding a large battleaxe angry, this is the essential tradeoff being made. We are gaining performance and compactness at the cost of a limited amount of uncertainty. In this case (especially since the battleaxe is virtual) this is a good deal.

## Controlling the uncertainty

If you just call BF.ADD and allow it to create a Bloom filter for you, you’ll end up with default values. These are fine for small Bloom filters of dozens of items, but for the above example, they are entirely inappropriate.

When setting up a Bloom filter, use BF.RESERVE to control the settings:

> BF.RESERVE UserFilter 0.001 100000000

This sets up a Bloom filter under the key UserFilter with an error rate of 0.001 or 0.1% and a capacity of 100,000,000 usernames.

## So how does a Bloom filter work?

The implementation of a Bloom filter is surprisingly easy for the power they contain. In preparation for writing this blog post, I (and [others at Redis](https://code.tutsplus.com/articles/understanding-the-magic-of-bloom-filters-with-nodejs-redis--cms-25397)) wrote a Bloom filter in [JavaScript](https://github.com/guyroyse/understanding-probabilistic-data-structures/tree/master/code/bloom-filter/javascript) using Node.js and another in [C#](https://github.com/guyroyse/understanding-probabilistic-data-structures/tree/master/code/bloom-filter/c%23) using .NET Core. Mind you, I wrote these Bloom filters for education and not for performance, so don’t use them in production.

At heart, a Bloom filter is an array of bits of a specified width. When an entry is added to the filter, it is run through a specified number of hashing functions (typically the same hashing algorithm with differing seeds). The results of these hashes are used to generate indices for the bit array. For each index, put a 1 in the array.

An example may make this more understandable. Let’s create a tiny filter with a bit width of 8 bits:

| Bit | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
|---|---|---|---|---|---|---|---|---|
| Index | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |

We use a hashing function with two different seeds. When we add an entry, we will call the hashing function twice to get two numbers. We will [modulo](https://en.wikipedia.org/wiki/Modulo_operation) those numbers by the bit width to generate our indices. Here it is in pseudocode:

index = some_hash_function('AliceTheAllomancer', seed) % 8

Let’s say that for Alice the Allomancer, this yields us the numbers 2 and 6. We then update our bit array by placing a 1 in positions 2 and 6.

| Bit | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 |
|---|---|---|---|---|---|---|---|---|
| Index | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |

Let’s add Bob the Barbarian. We put him through our hash functions and get a 3 and a 6 back. Our bit array now looks like this:

| Bit | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 0 |
|---|---|---|---|---|---|---|---|---|
| Index | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |

Great. Note that Alice and Bob both ended up setting bit 6 to a 1. A hash collision. Not a problem. This is why we use more than one hashing function.

Now let’s see if something is in the Bloom filter. We do this by running the entry we want to check through the same hashing functions. If we run Alice the Allomancer we get 2 and 6, just like before and if we run Bob the Barbarian we get 3 and 6, just like before. This is expected because hashing functions are deterministic.

For Alice we check bits 2 and 6. They are both 1 so Alice is probably in the Bloom filter. For Bob we check bits 3 and 6. Same result.

Let’s check for someone we know is not in the filter, Eric the Cleric. Eric’s hash yields a 0 and a 6. Since all of the bits are not set to 1 for Eric, he is definitely not in the Bloom filter.

But what about Fritz the Fighter? We haven’t seen him yet. His hash yields a 2 and a 3. Bits 2 and 3 are both set to 1, 2 by Alice and 3 by Bob. Fritz wasn’t added but he is probably in the filter. Hmm.

This is the source of the uncertainty of a Bloom filter. It can be ameliorated by increasing the bit width and/or the number of hashes. Doing either of these consumes more memory, so there is always a trade-off to be made. Such is life.

You can calculate the error rate using some algebra and the following formula, where *p* is the error rate, *k* is the number of hashes, *m* is the bit width, and *n* is the maximum number elements you expect to insert:

*p=*(1 – *e-kn/m*)*k*

Or you can just use an online calculator like [this one](https://hur.st/bloomfilter/).

## Just beginning with Bloom filters

There’s a lot more to Bloom filters that we haven’t gone into.

We explored a simple use case, but there are many many more. If you have a lot of data and don’t need perfection, Bloom filters are there for you. You could use a Bloom filter to track URLs that a web crawler has crawled or to remember suggested friends on social media so the user doesn’t keep seeing the same “Perhaps You Know” suggestions when they already said they didn’t. Or maybe just feed it all the words in a dictionary and use it as a spellchecker.

We also didn’t perform any benchmarks with Redis to compare sets and Bloom filters. But [we’ve blogged on that before](/blog/use-redis-content-filtering/) so no need!

If you want to more deeply explore Bloom filters, check out the Redis [documentation](https://docs.redis.com/latest/modules/redisbloom/) on Bloom filters to see everything you can do with them. And if you want to really internalize how they work, write your own Bloom filter in your language of choice. And please share it with me on [Twitter](https://twitter.com/guyroyse)!
