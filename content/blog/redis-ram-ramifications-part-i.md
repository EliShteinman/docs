---
title: "Redis RAM Ramifications – Part I"
linkTitle: "Redis RAM Ramifications – Part I"
url: "/blog/redis-ram-ramifications-part-i/"
description: "If there’s one most often repeated Redis question, it’s this one. It’s also one of the hardest to answer accurately because the answer depends on oh-so-many factors. In this post (and most likely a..."
date: 2015-04-16
blogCategories:
- "Tech"
authors:
- "Itamar Haber"
lastmod: 2026-08-13
hidden: true
---

*By Itamar Haber, Technology Evangelist · Published 16 April 2015 · updated 13 August 2026*

![Blog tile image](/images/blog/62f7c31d343148f296aebcf3372dacb4783ae801-140x92.webp)

![](/images/blog/39e0ae10ad81628baafd79df0a090abbfae056cf-635x200.webp)

> “…as we know, there are known knowns; there are things we know we know. We also know there are known unknowns; that is to say we know there are some things we do not know. But there are also unknown unknowns – the ones we don’t know we don’t know.”
United States Secretary of Defense Donald Rumsfeld, 2002

### How much RAM does Redis need?

If there’s one most often repeated Redis question, it’s this one. It’s also one of the hardest to answer accurately because the answer depends on oh-so-many factors. In this post (and most likely a few upcoming ones as I do tend to ramble while I rumble and mumble), I’ll try mapping out Redis’ RAM consumption. While I can’t guarantee an ultimate answer to everything, I hope it’ll help to:

- Repeat what we know about the known knowns (*KK*s)
- Turn known unknowns (*KU*s) into KKs when possible, or at least into known roughly-understood unknowns (*KRUU*s)
- Hopefully stumble on some unknown unknowns (*UU*s), and turn them into KUs, KRUUs or even KKs!

***Side note:**** you can track my progress on this series by subscribing to the RSS feed. Alternatively, sign up to *[*Redis Watch*](/redis-watch-archive)* and get weekly updates delivered to your inbox. Lastly, but only if you’re up to it, *[*follow us*](https://twitter.com/redis)* on Twitter for real-time action.*

So, Redis is a piece of software and as such it requires RAM to operate. But Redis is not just any software, it is an in-memory database, which means that every piece of data Redis manages is kept in RAM too. Lets call the RAM that Redis needs to operate the *Operational RAM*, and name the RAM used for data storage the *User Data RAM*.

### What is the airspeed velocity of an unladen swallow?

![](/images/blog/c53e21b844ac8a18c3135490778acf3f9e170ecc-300x165.webp)

We’ll begin our journey with a quick peek at Redis’ Operational RAM.

It is used for many purposes and tasks that Redis performs, and one way to think of that chunk of RAM is as all the memory that’s used by Redis for everything that isn’t the user’s data (I’ll probably waddle knee-deep into this later on) Redis’ RAM footprint is influenced by a myriad of deployment factors, including:

- The server processor’s architecture
- The operating system
- Redis’ version and configuration
- Probably a lot moar KKs, KUs and UUs

We can easily, however, set a baseline for Redis’ operational RAM requirements by examining it at rest on a typical server. For example, the memory footprint of [unladen African swallow](http://www.imdb.com/title/tt0071853/quotes) v3.0.0 instance on a virtualized Ubuntu 14 64-bit server is 7995392 bytes (or about 7.6MB). You can quickly determine how much total RAM your Redis instance has allocated from the command line with ps‘ RSS column, or with Redis’ [INFO](https://redis.io/commands/info) command:

```javascript
foo@bar:~$ uname -a
Linux bar 3.13.0-49-generic #81-Ubuntu SMP Tue Mar 24 19:29:48 UTC 2015 x86_64 x86_64 x86_64 GNU/Linux
foo@bar:~$ ps aux | grep redis-server
foo 20139 0.0 0.1 42304 7808 pts/1 Sl+ 19:18 0:00 ./redis-server *:6379
foo 20143 0.0 0.0 15940 944 pts/9 S+ 19:18 0:00 grep --color=auto redis-server
foo@bar:~$ redis-cli INFO memory | grep used_memory_rss
used_memory_rss:7995392
```

***Side note:**** the results of from the two methods above and others may not always be the same. Also, note that used_memory_rss differs greatly from Redis’ used_memory as we’ll see.*

Since this is a freshly initialized Redis instance, we can assume that this figure is a fair representation of our operational baseline. Redis’ operational RAM can grow, even significantly, but lets not worry about that for now.

### What? A swallow carrying a coconut?

[Redis is beautiful](/blog/red-is-beautiful-a-visualization-of-redis-commands), but you don’t keep it around just for its pretty face, do you? No, you make Redis manage your data because you need the fastest NoSQL database on the planet today. You let it carry your coconut and depend on it to keep beating its wings forty-three times (so close!) every second. So how much RAM does user data take? That depends on the coconut 🙂

Redis’ schemaless schema* is based on the Key-Value model. Every user datum that Redis manages is primarily a KV pair. It doesn’t take a genius to understand that the longer/bigger your keys and values are, the more RAM Redis will need to store it. But Redis does have a few ingenious tricks designed to keep data compacted and organized.

** There is no such as a schemaless database – at most it can have only an implicit one.*

Let’s jump right into it with an example concerning the simplest Redis data type – consider the following:

```javascript
127.0.0.1:6379> SET swallow coconut
OK
```

How much RAM did we just use? Since all data is organized by keys, the key’s name is the first element we’ll examine. We know that Redis key names are binary safe strings that can be up to 512MB long. Cool. String values in Redis are also binary safe and up to 0.5GB, so in our example above we can assume 7 bytes for “swallow” and another 7 bytes for the “coconut”… and we’d be wrong, at least partially. Here, let me show you:

```javascript
127.0.0.1:6379> STRLEN swallow
(integer) 7
127.0.0.1:6379> DEBUG SDSLEN swallow
key_sds_len:7, key_sds_avail:0, val_sds_len:7, val_sds_avail:0

```

As shown above with [STRLEN](https://redis.io/commands/strlen), Redis insists that the length of the value (“coconut”) that’s stored under the “swallow” key is 7 bytes long. Even more so, the “secret” DEBUG SDSLEN command also makes the same claims, but what both don’t account for is the datum’s overhead, and every Redis data structure comes with its own baggage. That means that besides the actual strings (“swallow” and “coconut”), Redis also needs some RAM to manage them.

Since every key-value tuple in Redis uses additional RAM for its internal bookkeeping, and because the amount of that RAM depends on the data structure and the data itself, I consider this overhead, while meta, a part of the user data. Put differently, if for every X bytes string Redis requires X + Y bytes, then Y is definitely a KU that I’d like to make into a KK.

### String theory

Strings in Redis are largely implemented by one of **Salvatore Sanfilippo @antirez**‘s sub-projects, called [sds](https://github.com/antirez/sds) (or Simple Dynamic Strings library for C). While sds strings bring a lot of power and ease of use to Redis internally, they do carry some overhead with them as an sds string is made up of:

```javascript
+--------+-------------------------------+-----------+
| Header | Binary safe C alike string... | Null term |
+--------+-------------------------------+-----------+
         |
         `-> Pointer returned to the user.

```

(diagram courtesy of antirez, [https://github.com/antirez/sds/blob/master/README.md](https://github.com/antirez/sds/blob/master/README.md))

The size of an sds string’s header ([at the moment](https://github.com/antirez/redis/pull/2509)) is 8 bytes and the null character is an additional byte, which give us a total of 9 bytes overhead per string. The 7 byte long “swallow” suddenly takes more than twice that amount – 16 bytes of RAM – to store in Redis!

***Side note:**** It actually uses moar. The reference to every key is also stored in Redis’ keyspace hash table, which in turn requires even more RAM… And there’s also the robj “object” that Redis uses to facilitate some stuff like LRU… But let’s just keep the key’s management RAM overhead as a KU and throw it into the operational RAM side of the house for now 🙂*

### …four really, if they had the coconut on a line between them

Back to our swallows and coconuts – so now we know that Redis will use 36 bytes for storing the two strings that make up the key and value in the example above, but is that all? Let’s take a closer look at our coconut:

```javascript
127.0.0.1:6379> OBJECT ENCODING swallow
"embstr"

```

The plot thickens (or maybe it’s the coconut growing hair?). This cryptic response begs an explanation, but are all coconuts encoded the same? Let’s try carrying a few different shapes of string coconuts and see:

```javascript
127.0.0.1:6379> SET swallow:0 "0"
OK
127.0.0.1:6379> SET swallow:1 "An oversized and thickly-haired coconut"
OK
127.0.0.1:6379> SET swallow:2 "Ok, this is the mother of all coconuts - it is something that would make Donkey Kong run back to his mama in tears"
OK
127.0.0.1:6379> OBJECT ENCODING swallow:0
"int"
127.0.0.1:6379> OBJECT ENCODING swallow:1
"embstr"
127.0.0.1:6379> OBJECT ENCODING swallow:2
"raw"

```

Each of our coconuts is different, so Redis uses different encodings. The “int” encoding is used to efficiently store integer values between *LONG_MIN* and *LONG_MAX* (as defined in your environment’s *limits.h*) and also leverages the shared.integers construct to avoid duplicating data. Consequently, these take up less space. On the other hand, strings longer than 39 bytes are stored as “raw”, whereas shorter ones use the “embstr” encoding (the magic number is defined by *REDIS_ENCODING_EMBSTR_SIZE_LIMIT* in *redis.h*).

### Going (coco)nuts

![](/images/blog/dc12d3345c5177c53e35caf7ff3a5eaeab06e5d5-300x200.webp)

What about other coconut structures? Strings are the simplest data structure that Redis offers and they are used internally to make other, more advanced structures. The Hash is made of a bunch of Strings (fields & values) added with a dictionary data structure, in which each entry is a linked list… BUT they could be encoded entirely as a ziplist. And speaking of lists, we have the linked lists and ziplists (and perhaps even **Matt Stancliff @mattsta**‘s [quicklists](https://matt.sh/redis-quicklist-visions) soon) that are also used by Sets and Sorted Sets…

I could go on, **indefinitely**, into the delicate intricacies of data encoding in Redis and how they affect memory consumption. I fear, however, that it will bore all of us to death pretty soon. Alternatively, you can *git checkout* the [source code](https://github.com/antirez/redis) and start reading it – I know a few people who have done it, but you’ll need a certain level of programming skills for that.

Which still leaves the big KU – *How much RAM does Redis need?* – and its little brother KU – *How much RAM do coconuts need?* – pretty much unanswered. But where there’s a will there’s a way. Feel free to interact with me via the usual channels – I’m Highly-Available 🙂

***Side note:**** to be continued.*
