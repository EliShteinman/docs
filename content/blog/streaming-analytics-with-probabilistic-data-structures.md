---
title: "Probabilistic Data Structures in Redis"
linkTitle: "Probabilistic Data Structures in Redis"
url: "/blog/streaming-analytics-with-probabilistic-data-structures/"
description: "Hello World! My name is Savannah, and I’m a new-ish Developer Advocate at Redis. I’ve hopped on livestream to talk about RedisJSON with our Senior Developer Advocates Justin and Guy to discuss..."
date: 2022-08-11
blogCategories:
- "Tech"
authors:
- "Savannah Norem"
lastmod: 2025-03-27
hidden: true
---

*By Savannah Norem, Contributor · Published 11 August 2022 · updated 27 March 2025*

![Blog tile image](/images/blog/3ace11fe856ce404c030cbd5fc1c7a2f92ca854a-772x550.webp)

Hello World! My name is Savannah, and I’m a new-ish Developer Advocate at Redis. I’ve hopped on livestream to talk about [RedisJSON ](https://www.youtube.com/watch?v=ZP2j7bmWfmU&list=PL83Wfqi-zYZHSnOXH3kCkgyfk3Rqo_wzH)with our Senior Developer Advocates Justin and Guy to discuss probabilistic data structures. That exploration with Guy is ephemeral on Twitch, but I recently did some coding using a few more probabilistic data structures that you can watch on [YouTube](https://www.youtube.com/watch?v=_TGJSXZvLT8&list=PL83Wfqi-zYZHSnOXH3kCkgyfk3Rqo_wzH&index=2). There can be some confusion about what a probabilistic data structure is, so I figured I’d take some time to write out the highlights of these data structures that take large datasets.

Google Chrome, Akami, and your ISP will likely use some types of probabilistic data structures to do things that improve your life as an end user. So if you’ve got large datasets, think data structures are cool, or want to see where those big names would use these things, read on!

Download our white paper “[Redis HyperLogLog: A Deep Dive](/docs/redis-hyperloglog-deep-dive/).”

Redis offers a few different probabilistic data structures – some in the [RedisBloom](/redis-best-practices/bloom-filter-pattern/) module (that’s included in redis-py, my language of choice) and one in core Redis, but [RedisBloom](https://redis.io/docs/stack/bloom/) is now included with all the client libraries, so there is no need to import anything else if you’re using [Redis Stack](https://redis.io/docs/stack/). In this post, I’ll tell you about [Bloom filters,](/blog/redis-redisbloom-bloom-filters/) cuckoo filters, [Top-K](/blog/meet-top-k-awesome-probabilistic-addition-redisbloom/), [Count-Min Sketch](/blog/count-min-sketch-the-art-and-science-of-estimating-stuff/), and [Hyperloglog. ](/redis-best-practices/counting/hyperloglog/)We’ll walk through what the probabilistic nature of each is, a high-leveloverview of how they work, and some key use cases. We’ll start with the following Redis connection and definition for these code examples.

```python
r = redis.Redis(
   host='localhost',
   port=6379,
   db=0,
   decode_responses=True
)

```

### Bloom filters

Named after the person that first wrote down the idea, Bloom filters can tell us probabilistic membership, that is, whether or not something has been added to the filter.

Bloom filters work as a bit array, where items are added, and certain bits are set. This can have overlap; however, multiple things could map to some of the same bits. These items are added with no issue to the filter unless all the bits they correspond to have already been set, in which case the response is that the item may have already been added to the filter. Since a not set bit means that an item has not been added, there are no false negatives.

However, because of the bit overlaps of different items and the fact that Bloom filters don’t store any information about *what* has been added, there is no deletion. We’ll show how to create our Bloom filter, a multi-add, and a multi-exists check. The output here is probabilistic and could be either a false positive or a true negative. In this case, with only adding three things to a filter set to store 1,000, it’s almost guaranteed to be a true negative.

```python
r.bf().create('Bloom', 0.01, 1000)
r.bf().madd('Bloom', foo, bar, baz)
r.bf().mexists('Bloom', foo, faz) #1 0 OR 1 1

```

Other commands are available to get information about the Bloom filter, save and load it, and a few others. But creating it, adding things to it, and checking if those things exist is all you need to accomplish the main purpose of the Bloom filter.

These filters can be used in place of testing set membership for large datasets quickly. For example, the Google Chrome browser maintains a Bloom filter of malicious URLs. When someone tries to go to a website in Chrome, the browser first checks the Bloom filter. Since there are no false negatives, if the filter returns that it’s not there, Chrome allows the user to go through to the URL quickly and without having to check a large dataset. Because Bloom filters are just bit arrays, they can often be stored in a browser cache, saving time against large and far away database lookups.

On top of the standard Bloom filter I’ve explained above, the Redis implementation has an option to become a Scaling Bloom filter. There are a couple of different things that people have tacked on to Bloom filters over the years, adding different functionality while mostly maintaining the core ideas. For instance, a Stable Bloom filter can deal better with unbounded data without the need to scale but can introduce false negatives. [Other types](https://en.wikipedia.org/wiki/Bloom_filter#Extensions_and_applications) of Bloom filters include Counting Bloom filters, Distributed Bloom filters, Layered Bloom filters, and more.

### Cuckoo filters

Named after a bird that famously pushes other birds’ eggs out of their nests and takes them over, cuckoo filters also tell us probabilistic membership, but in a very different way than Bloom filters.

Cuckoo filters keep hold of a fingerprint of each item that’s been added and store multiple fingerprints in each bucket. The length, in bits, of the fingerprints determines how quickly there are collisions, which helps determine the number of buckets you’ll need and what error rate you can get. When a collision occurs, one of the fingerprints in the bucket will get kicked out and put into a different bucket, hence the name.

Because a fingerprint is stored, cuckoo filters do support deletion. However, the collisions still exist, and you could end up deleting something that you didn’t mean to delete, which can lead to some false negatives. Like the Bloom filter, the main things we want to do are create one, add things to it, and check if they exist. However, we must use the `insert` command to add multiple things to the cuckoo filter. The cuckoo filter also has a [command](https://redis.io/commands/?group=cf) for adding an item if it doesn’t already exist: `addnx`.

However, because the `exists` command is probabilistic, attempting to delete an item added this way can cause false negatives. Here we’ll see the same probabilistic output of `mexists` as the Bloom filter.

```python
r.cf().create('cuckoo', 1000)
r.cf().addnx('cuckoo', foo)
r.cf().insert('cuckoo', bar, baz)
r.cf().delete('cuckoo', foo)
r.cf().mexists('cuckoo', foo, faz) #1 0 OR 1 1

```

The main draw of a cuckoo filter is the ability to delete entries, and aside from cases where that’s an essential requirement, Bloom filters are generally used.

### Count-Min Sketch

Like a sketch is a rough drawing, a Count-Min Sketch (aka CM Sketch) will return a rough guess of the minimum count of how many times an item was added to the sketch. This means, that this data structure answers item frequency questions. In some ways, CM Sketch is similar to HyperLogLog as they both count elements, with the crucial difference that CM Sketch doesn’t count unique elements but rather how many copies of each element you added to it.

Like a piece of the Top-K structure, the Count-Min Sketch is a table where each row represents a different hash function being used, and each item added gets a spot in each row. However, unlike the Top-K, this data structure is *just* the counts, with no regard for what the counts are attached to. So in the case of a collision, the count is simply incremented with no concern for the fact that the count is now the count of two different things combined. This is why when you query for the count of an item, the counts from each row are considered, and you get back the *minimum*.

For a Count-Min Sketch, we can either initialize it by the probabilities we want to maintain or the dimensions we want. This will be somewhat important because to merge two Count-Min Sketches, they must have the same dimensions.

Some important things to note (about the [commands](https://redis.io/commands/?group=cms) in the Python code below), you don’t actually add things to the Count-Min Sketch use `incrby` and increase the count by a specified amount. Even if you only increment one thing, it has to be passed in as a list. They can then be merged with specified weights, where the weights essentially multiply the counts in the respective Sketches. The merged Sketch is then queried.

In this code, I am no longer able to see what used to be in `cms1`, but I can still use the original `cms2`. I could have also created a new Count-Min Sketch `cms3` (with the same dimensions) and then merged `cms1` & `cms2` into `cms3`, preserving the original data of both `cms1` & `cms2`.

The output of querying for baz is 6 because we used `incrby` with 2 and then a weight of 3. However, once a significant number of things are added, this count will become less accurate.

```python
r.cms().initbydim('cms1', 2000, 5)
r.cms().initbydim('cms2', 2000, 5)
r.cms().incrby('cms1', [foo], [4])
r.cms().incrby('cms1', [bar, baz], [1, 2])
r.cms().incrby('cms2', [foo], [1])
r.cms().merge('cms1', 2, ['cms1', 'cms2'], weights=[3,1])
r.cms().query('cms1', baz) #6

```

This data structure can be used for large amounts of data when storing what each item becomes impractical because instead of storing whatever the item is, you’re only storing a table of numbers. You can then query how many times any given item has been added and get the minimum count of the spaces it maps to, which may still be slightly inflated depending on the number of collisions that have happened.

### Top-K

Named after its functionality, a Top-K data structure will give you back an approximation of the Top-K counts stored in it.

There are two data structures at play here; a table that keeps track of fingerprints and their counts and a min heap structure that keeps track of what the Top-K things in the table are. Each row in the table represents a different hash function being used, so each item added gets hashed to a spot in each row. Redis’ implementation, in particular, uses an algorithm called HeavyKeeper. With this algorithm, the basic idea is that whenever there’s a collision between fingerprints, there’s a probability that the count of what was already there will be decremented. This means that items that get added a lot have high counts and a low probability of being decayed, while items that don’t will be overwritten over time.

To learn more about available [Top-K commands](https://redis.io/commands/?group=topk), we’ll reserve the space for one, specifying first the number of top things we want to save and then the width, depth, and decay that we want (required by redis-py, but not in the Redis CLI, as you can watch me find out in one of our[ Redis Live](https://youtu.be/_TGJSXZvLT8?list=PL83Wfqi-zYZHSnOXH3kCkgyfk3Rqo_wzH&t=405) recordings. . We add things to Top-K we can add multiple things or just one with the same command. We can then get the count of any of the things we’ve added.

But when we use `query`, we only find out whether or not the thing we query for is in our specified Top-K items. So, for instance, we initialize ‘topk’ to only keep the top 1 item in the min heap. So querying for bar will return 0 since we add ‘foo’ multiple times. Querying for ‘foo’ will return 1. We can also get the list of the Top-K items. When a significant number of things are added and go through the probabilistic decay, this Top-K can lose some of its precision.

```python
r.topk().reserve('topk', 1, 8, 7, 0.9)
r.topk().add('topk', foo, bar, baz)
r.topk().add('topk', foo)
r.topk().add('topk', foo)
r.topk().count('topk', bar) #1
r.topk().count('topk', foo) #3
r.topk().query('topk', bar) #0
r.topk().query('topk', foo) #1
r.topk().list('topk') #[foo]

```

The more hash functions used, the less likely collisions are. In the Top-K structure, the maximum count for a single item is what will be checked against the min heap. So for an item to really have its count decreased, it has to have a hash collision on every row. This still means there’s a chance that the Top-K min heap will end up with, for example, the sixth most common thing added instead of the fifth. This data structure is often used to monitor network traffic and track what IP addresses are flooding a network and potentially trying to cause DDoS.

### HyperLogLog

After starting with linear counting, then moving to probabilistic counting, this name started with a [paper](http://algo.inria.fr/flajolet/Publications/DuFl03-LNCS.pdf) from 2003 proposing the LogLog algorithm and an improved version called Super-LogLog, and now we have HyperLogLog.

One of the first data structures available in Redis, HyperLogLog keeps a probabilistic count of how many unique items have been added. Like the Bloom filter, this data structure runs items through hash functions and then sets bits in a type of bitfield. Also, like a Bloom filter, this structure doesn’t retain information aboutthe individual items being added, so there is no deletion here. This data structure doesn’t have many commands available, making it easier to use than others. With only add, count, merge, and two testing commands, we can easily see what you can do. You can add things to it, get a count of how many *unique* things have been added, and merge them together. Merging them together will result in a HyperLogLog that only contains the unique items from each – that is – items that were in both will not be duplicated, and they’ll only be counted as one unique item in the merged HyperLogLog.

Because HyperLogLog is in core Redis – not the RedisBloom module – in the [commands](https://redis.io/commands/?group=hyperloglog) below, we don’t see the `r.hll().add`, nor do we have to actually create or reserve one; we just start adding things to it. We can merge multiple HyperLogLogs together and get a probabilistic count of how many unique things are in them. Again, as more things are added, the more likely this count is to lose some precision.

```python
r.pfadd('hll1', foo, bar, baz)
r.pfadd('hll2', foo)
r.pfmerge('hll3', 'hll1', 'hll2')
r.pfcount('hll1') #3
r.pfcount('hll2') #1
r.pfcount('hll3') #3

```

This data structure is useful for counting unique items in large datasets, for instance, unique IP addresses that hit websites, unique video viewers, etc.

## Why a probabilistic data structure?

Well, if you have a very large dataset or a big data application, you likely want some quick things from it that are okay with certain inaccuracies because those inaccuracies come with major space-saving. Knowing quickly that something is definitely not present might be worth the rate of false positives. Knowing that out of your top 10, you might have a few things that are really in the top 15 and missing a few of the 10, but depending on what you’re hoping to do with that information, that’s just fine. If you’re using [Chrome, Akami, or really any part of the internet](https://en.wikipedia.org/wiki/Bloom_filter#Examples), you’re probably benefitting from some probabilistic data structures.

I hope you learned something about why and when probabilistic data structures can help you get information about large datasets, all while not taking up as much space – granted, with a bit less precision in the information. I hope you check out the probabilistic data structures Redis has to offer for you. Should you have any questions, come find us on [discord](http://discord.gg/redis), or check out the Redis[YouTube channel ](https://www.youtube.com/c/Redisinc)and see what you can do with Redis.
