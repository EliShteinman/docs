---
title: "Indexing with Redis"
linkTitle: "Indexing with Redis"
url: "/blog/indexing-with-redis/"
description: "This article was originally posted on nosqlgeek.org"
date: 2017-08-10
blogCategories:
- "Company"
- "Tech"
authors:
- "David Maier"
lastmod: 2025-03-04
hidden: true
---

*By David Maier, Technical Enablement Mananger · Published 10 August 2017 · updated 4 March 2025*

![Blog tile image](/images/blog/d75b51f6d811874093f54bfd83f6615b7f728a6b-91x78.webp)

*This article was originally posted on *[*nosqlgeek.org*](http://www.nosqlgeek.org)

If you follow my news on Twitter then you might have realized that I just started to work more with Redis. Redis (=Remote Dictionary Server) is known as a Data Structure Store. This means that we can not just deal with Key-Value Pairs (called Strings in Redis) but in addition with data structures as Hashes (Hash-Maps), Lists, Sets or Sorted Sets. Further details about data structures can be found here:

- [https://redis.io/topics/data-types-intro](https://redis.io/topics/data-types-intro)

### Indexing in Key-Value Stores

With a pure Key-Value Store, you would typically maintain your index structures manually by applying some KV-Store patterns. Here some examples

- **Direct access via the primary key:** The key itself is semantically meaningful and so you can access a value directly by knowing how the key is structured (by using key patterns). An example would be to access an user profile by knowing the user’s id. The key looks like ‘user::<uid>’.
- **Exact match by a secondary key:** The KV-Store itself can be seen as a huge Hash-Map, which means that you can use lookup items in order to reference other ones. This gives you a kind of Hash Index. An example would be to find a user by his email address. The lookup item has the key ’email::<email_addr>’, whereby the value is the key of the user. In order to fetch the user with a specific email address you just need to do a Get operation on the key with the email prefix and then another one on the key with the user prefix.
- **Range by a secondary key:** This is where it is getting a bit more complicated with pure KV-Stores. Most of them allow you to retrieve a list of all keys, but doing a full ‘key space scan’ is not efficient (complexity of O(n), n=number of keys). You can indeed build your own tree structure by storing lists as values and by referencing between them, but maintaining these search trees on the application side is really not what you usually want to do.

### The Redis Way

So how is Redis addressing these examples? We are leveraging the power of data structures as Hashes and Sorted Sets.

##### Direct Access via the Primary Key

A Get operation already has a complexity of O(1). This is the same for Redis.

##### Exact Match by a Secondary Key

Hashes (as the name already indicates) can be directly used to build a hash index in order to support exact match ‘queries’. The complexity of accessing an entry in a Redis Hash is indeed O(1). Here an example:

HMSET idx_email david.maier@redis.com user::dmaier

HMSET idx_email max.mustermann@example.com user::mustermann

HGET idx_email david.maier@redis.com

"user::dmaier"

In addition Redis Hashes are supporting operations as HSCAN. This provides you a cursor based approach to scan hashes. Further information can be found here:

- [https://redis.io/commands/scan](https://redis.io/commands/scan)

Here an example:

HSCAN idx_email 0 match d*

1) "0"

2) 1) "david.maier@redis.com"

2) "user::dmaier"

##### Range by a Secondary Key

Sorted Sets can be used to support range ‘queries’. The way how this works is that we use the value for which we are searching as the score (order number). To scan such a Sorted Set has then a complexity of O(log(n)+m) whereby n is the number of elements in the set and m is the result set size. Here an example:

ZADD idx_age 37 user::david

ZADD idx_age 9 user::philip

ZADD idx_age 36 user::katrin

ZADD idx_age 13 user::robin

ZADD idx_age 0 user::samuel

ZRANGEBYSCORE idx_age 0 10

1) "user::samuel"

2) "user::philip"

If you add 2 elements with the same score then they are sorted lexicographically. This is interesting for non-numeric values. The command ZRANGEBYLEX allows you to perform range ‘queries’ by taking the lexicographic order into account.

### Modules

Redis supports now Modules (since v4.0). Modules are allowing you to extend Redis’ functionality. One module which perfectly matches the topic of this blog post is RediSearch. RediSearch is basically providing Full Text Indexing and Searching capabilities to Redis. It uses an Inverted Index behind the scenes. Further details about RediSearch can be found here:

- [http://redisearch.io](http://redisearch.io/)

Here a very basic example from the RediSearch documentation:

FT.CREATE myIdx SCHEMA title TEXT WEIGHT 5.0 body TEXT url TEXT

FT.ADD myIdx doc1 1.0 FIELDS title "hello world" body "lorem ipsum" url "http://redis.io"

FT.SEARCH myIdx "hello world" LIMIT 0 10

1) (integer) 1

2) "doc1"

3) 1) "title"

2) "hello world"

3) "body"

4) "lorem ipsum"

5) "url"

6) "http://redis.io"

As usual, I hope that you found this article useful and informative. Feedback is very welcome!
