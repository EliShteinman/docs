---
title: "Computing Jaccard Similarity with Redis"
linkTitle: "Computing Jaccard Similarity with Redis"
url: "/blog/computing-jaccard-similarity-with-redis/"
description: "Many things in the world have fancy-sounding names, but are actually really simple ideas. Jaccard similarity is one of those things. It’s a simple calculation—created by botanist Paul Jaccard in..."
date: 2020-04-13
blogCategories:
- "Tech"
authors:
- "Guy Royse"
lastmod: 2025-03-27
hidden: true
---

*By Guy Royse, Developer Advocate · Published 13 April 2020 · updated 27 March 2025*

![Blog tile image](/images/blog/fe64cf78ffcb607f90acf514709db241042355a2-1000x1000.webp)

Many things in the world have fancy-sounding names, but are actually really simple ideas. [Jaccard similarity](https://en.wikipedia.org/wiki/Jaccard_index) is one of those things. It’s a simple calculation—created by botanist Paul Jaccard in 1901—that you can make with sets to determine how similar they are.

Finding similar things is useful—you might want to find people with similar tastes as part of a matchmaking (romantic or otherwise) process or to find similar documents to detect plagiarism.

Redis, with its [Set data structure](https://redis.io/topics/data-types-intro#sets), has most of what you need to calculate Jaccard similarity. But before we get to the Redis bits, let’s look at how to calculate it.

## Cardinality, unions, and intersections, oh my!

If you have even the slightest background in set theory, this will be a review. We’ll start with sets. A *set* is a collection of unique objects. In mathematical notation, they are represented with curly braces and a list of the members of the set. Here’s a simple set of movies I like:

![](/images/blog/7b81e382175235e9e0c24f3fc257b8eea9e499a2-300x218.webp)

You can count a set’s members. This is the *cardinality* of the set. The above set has a cardinality of 6.

Of course, you can have more than one set. Here is a simple set of movies that my wife likes:

![](/images/blog/2642b3bdc95f128b59f87456bd53754f13d444eb-300x245.webp)

You can see that she and I have some movie preferences in common, but she also has several that I’m not as fond of. And vice versa. You can also see that her set has a cardinality of 7.

Now that we have two sets we can start doing some interesting stuff. First, we can combine the sets. This is called the *union*. The union is itself a set, and like all sets, has a cardinality (in this case 9). We can write the union of these two sets as an equation using the union symbol as shown below:

![](/images/blog/6585d0e153195cbf1badf6ee3252cadbc1a7a19e-1024x340.webp)

We can also determine what the sets have in common. This is called the *intersection*. The intersection is also a set and also has a cardinality—which is 4—just like a union. We can write the intersection of our two sets as an equation using the intersection symbol as shown below:

![](/images/blog/ab54b53a330727422af7e7f8b103b93d4b90c31a-1024x272.webp)

There’s lots more to set theory, but this is all we need to know to understand and calculate a Jaccard similarity.

## A simple calculation

The Jaccard similarity is the ratio of the cardinality of the intersection to the cardinality of the union. In our example, my wife and I have 4 movies in common and 9 movies between us. 4 divided by 9 yields approximately 0.444 or 44.4%. So, our taste in movies is 44.4% similar.

And that’s it. That’s all a Jaccard similarity is.

Let’s calculate it using Redis [Set commands](https://redis.io/commands#set).

## Using Redis and the X-Files

Instead of using movies that my wife and I like, this time I’m going to use states in which Scully and Mulder have seen UFOs. (This data is totally made up. I’m pretty sure they saw UFOs in every state.)

First, we need to create a couple of sets for Scully and Mulder:

> SADD ufos:scully "California" "Nevada" "Oregon"

> SADD ufos:scully "Wyoming" "New Mexico" "Ohio"

[Nevada](https://en.wikipedia.org/wiki/Area_51), [New Mexico](https://en.wikipedia.org/wiki/Roswell_UFO_incident), [Ohio](https://en.wikipedia.org/wiki/Hangar_18). Sounds legit:

> SADD ufos:mulder "Florida" "Kansas" "South Carolina"

> SADD ufos:mulder "West Virginia" "New Mexico" "Ohio"

New Mexico and Ohio again.

Now we need to create some new sets that are the intersection and union of these two sets. We’ll need to store them so we can get their cardinality:

> SINTERSTORE ufos:intersection ufos:scully ufos:mulder

(integer) 2

> SUNIONSTORE ufos:union ufos:scully ufos:mulder

(integer) 10

Now that we have the intersection and the union we can get their respective cardinalities:

> SCARD ufos:intersection

(integer) 2

> SCARD ufos:union

(integer) 10

Or, we can skip that call and just use the results of the SINTERSTORE and SUNIONSTORE commands. Either way, we just divide these two numbers and get the result. Which is 20%.

## SINTERSTORE and SUNIONSTORE

You might not be super familiar with the [SINTERSTORE](https://redis.io/commands/sinterstore) and [SUNIONSTORE](https://redis.io/commands/sunionstore) commands and their possible consequences, so I thought some education might be in order.

SINTERSTORE and SUNIONSTORE do the same basic thing as SINTER and SUNION except they store the result at a key (hence the STORE at the end). Using them is easy. Just pass in the desired key of the set to be created and one or more keys containing sets you want to operate against:

> SUNIONSTORE destination_key key1 key2 key2 …

(integer) 51

While SINTER and SUNION return the intersection and union of the sets they are handed, SINTERSTORE and SUNIONSTORE create new sets (and return the size of said sets). These sets could be quite large and will be written out to the AOF and replicated (if you’re doing those things.)

In our example, they are intended to be intermediate values. So, if they are big and they need to be written to the AOF and replicated, this could be a significant performance hit.

SINTER and SUNION don’t have this problem. They just return the set they create without the storing of it. We could have built our solution using them and just counted the members returned to get the cardinality. Of course, these sets could also be quite large, and returning them to the client could be a rather expensive operation.

There’s often more complexity hidden within once you dive into a problem. We could have solved our Jaccard similarity problem with SINTER and SUNION, or we could have chosen SINTERSTORE and SUNIONSTORE. Size, writing to the AOF, and replication are all factors here. So which is the right approach? As usual, the answer is “it depends.”

## A couple of notes

First and foremost, remember that we are using sets. More significantly, we are using intersection and union commands. The key names above would work only on a single instance without clustering. If you are using clustering, you need to be sure to slot your keys so they all go to the same shard. For more information, check out Kyle Davis’ great blog post on [Redis Clustering Best Practices with Keys](/blog/redis-clustering-best-practices-with-keys/).

Second: It’s not terribly satisfying to have to do the final computation outside of Redis. If we’re going to use Redis to compute Jaccard similarity then we want to use Redis, not Redis and client-side code. We can accomplish this with Lua.

If you just want to use Lua for the last mile of this calculation, the code below will work without a problem:

> EVAL "local inter_card = redis.pcall('scard', KEYS[1]); local union_card = redis.pcall('scard', KEYS[2]); local similarity = inter_card / union_card; return tostring(similarity)" 2 ufos:intersection ufos:union

However, if you want to avoid creating the intermediate sets using SUNIONSTORE and SINTERSTORE, there are other ways to do this. But there are tradeoffs. I have a [GitHub repo](https://github.com/guyroyse/jaccard-similarity) with a couple of ways of solving this that you can explore if you want to go deeper. (It’s in JavaScript. I hope you’ll forgive me.)

## Go make something

And just like that, you can now calculate Jaccard similarity and use it for all sorts of cool things. Looking for some fun data to try it against? Check out this [large dataset of UFO sightings](https://github.com/timothyrenner/nuforc_sightings_data)!
