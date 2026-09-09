---
title: "Mastering RediSearch / Part I"
linkTitle: "Mastering RediSearch / Part I"
url: "/blog/mastering-redisearch-part/"
description: "I’ve been working with the RediSearch module quite a bit lately — it’s one of the more fascinating developments in the Redis ecosystem and it deserves it’s own series."
date: 2017-09-22
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-04
hidden: true
---

*By Redis   · Published 22 September 2017 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/979210462f1d193a00f5897d3b403c8b62486991-1272x1688.webp)

I’ve been working with the [RediSearch](/search/) module quite a bit lately — it’s one of the more fascinating developments in the Redis ecosystem and it deserves it’s own series.

If you’ve built an application with Redis as a primary data store, you’ve likely experienced both the elation and confusion of the native data types. When you understand the data types, you realize that much of your data fits neatly into one of them. However, many common application patterns require both indexing (“what key has *x* value?”) and search (“what key contains* some text string*?”). While these questions can be answered by leveraging the native datatypes in creative ways, the code can be complex and has speed and/or space efficiency trade offs. The RediSearch module fills in these blanks with few trade offs. In this first installment we’re going to be exploring the very basics of the module as a gentle introduction.

#### What are modules?

Modules are add-ons for your Redis server. At their most basic level, they implement new commands, but they can also implement new data types. Modules are written in systems programming languages; C/C++, Rust and Golang have been used but other languages are possible. Since they’re written in compiled languages, extreme high performance is possible.

Modules are distinct from Redis scripting (Lua) in that they are first-class commands in the system and can interface storage directly, enabling the creation of their own datatypes. The only thing that sets them apart from in-built commands is that module commands are namespaced by a prefix, often two letters, and a dot (ex: XX.SOMECOMMAND).

Modules can be loaded either on the fly with MODULE LOAD, in the redis.conf file with *loadmodule, *or through the command line argument “loadmodule”. My personal preference is to load them via the conf file as it ensures that it’s always available and the configuration is portable.

#### What is RediSearch?

I’ve asked myself the question what *isn’t* RediSearch — but I’ll attempt to answer it without inverting. RediSearch is a module that provides three main features:

- Full Text Search,
- Secondary Indexing,
- Suggestion/auto-complete engine.

RediSearch utilizes both it’s own datatype and the in-built Redis data types. In this way, it’s more of a solution that uses Redis and also resides with Redis. That may seem confusing now, but stay with me.

Let’s evaluate each of the features from above. First, consider [full-text searching](/glossary/full-text-search/). With RediSearch you can index text that hasn’t already been processed. Let’s say that you have a list of one million client comments and you want to find all that mention “rendering.” Before RediSearch, you could certainly store those comments in Redis (in, say, a hash), but finding a specific word inside those comments was a struggle at best. Even if you managed to build your own index of words to comments (which involves splitting each comment into words at the app level), matching would need to be exact — “render,” “rendering,” and “rendered” would not match one another. Instead, by storing the data with RediSearch you could find all the comments without having to do anything special at your application level and it would match “rendered” to “rendering” automatically since it smartly processes both the index and the query.

Obviously, if it’s possible to do the above, it’s also possible to do it without the language processing smarts — as you start to think of this, you start to realize that RediSearch can be used as a general purpose secondary index. But it’s also possible to go beyond text matches — RediSearch can do numeric and geo indexes on a single item (termed “document”). It is possible to have multiple fields on each document — each with individual attributes.

Finally, somewhat separately, RediSearch provides a suggestion engine that can drive auto-complete-like services. This allows you to take known valid values and provide users “hints.” It’s based on a prefix model, so if a user starts to type “Hamb” the suggestion engine would provide, say, “Hamburger,” “Hambone,” and “Hamburg.” It’s important to note these suggestions aren’t integrated with the search results directly, so it’s up to your application to add or delete them from this suggestion store.

#### Hands on

As a hands on exercise, let’s install the module:

```python
$ git clone https://github.com/RedisLabsModules/RediSearch.git
$ cd RediSearch
$ make all
$ cd src
$ redis-cli
> MODULE LOAD ./redisearch.so

```

(or install it in your redis.conf file and restart redis-server)

After your module is loaded, go ahead and run this command in redis-cli to verify the module is running:

```python
> module list
1) 1) "name"
   2) "ft"
   3) "ver"
   4) (integer) 2000

```

In the results to this command you should see an entry for each module you have installed (likely just one). The name field of one of the entries should read “ft” (meaning *full text*). That’s how RediSearch is identified and the command prefix. Your version number will likely be different from mine, progress on this module is moving fast.

Now that the module is up and running it’s best to start with a clean database for these exercises (*flushdb *or a clean database/instance). To start let’s create an index and add an item:

```python
> FT.CREATE shakespeare SCHEMA line TEXT SORTABLE play TEXT NOSTEM speech NUMERIC SORTABLE speaker TEXT NOSTEM entry TEXT location GEO

```

This might look a tad complicated, especially if you’re used to commands with 1 or 2 arguments. Let’s break it down:

*FT.CREATE shakespeare*
This is just the command and the “key” (more on that later)

*SCHEMA*
This indicates that the following arguments will be about the fields in the search index.

*line TEXT SORTABLE*
Here we are creating a field named *line* that holds text values and will be sortable later on.

*play TEXT NOSTEM*
This is the field “play” that is for text values but it won’t be stemmed (e.g. *rendering* will not match *render*)

*speech NUMERIC SORTABLE*
We’re creating a field named “speech” that is numeric and sortable.

*speaker TEXT NOSTEM*
Just like the *play *field the *speaker* field will hold text that will only do exact, word-for-word matches.

*entry TEXT*
This field (*entry*) holds text values that are processed for exact or stemmed match.

*location GEO*
The *location* field holds a geographic coordinate.

See — it’s just a lot in one line, but not really complicated.

Now, let’s add a document to our index:

```python
> FT.ADD shakespeare 57956 1 FIELDS text_entry "Out, damned spot! out, I say!--One: two: why," line "5.1.31" play macbeth speech 15  speaker "LADY MACBETH" location -3.9264,57.5243

```

Comparing the two commands, you might notice that the FT.CREATE and FT.ADD commands are following a similar pattern. Let’s look at the command in more depth:

*FT.ADD shakespeare 57956 1*
We’re adding a document with an ID of *57956* to the index (*shakespeare*). Note that in this command the document ID is a number (just a feature of the dataset I’m using), but it can be any valid Redis key. The final argument in this section is the weight — we’ll get into this in a later part of the series, but, for now, you just need to know that it can be between 0 and 1 and 1 is a good default value.

*FIELDS …*
“FIELDS” indicates that we’re going to specifying the fields of the document in a [fieldname] [value] repeating pattern. Note that when the value is single word or number, you don’t need quotes, but if you’re using spaces or other odd characters, enclose your value in quotes. The other special one is the location field that includes a set of coordinates (*longitude*,*latitude*)

#### The curious case of RediSearch keys

Recall that we created an index with the key “shakespeare” (via the FT.CREATE command). Let’s do a quick experiment:

```python
> TYPE shakespeare
none

```

Strange, right? This is where we start departing from normal Redis behaviour and you’ll start seeing where RediSearch is a solution that is both using and integrated with Redis.

If you’re running this on a non-production database, let’s do *KEYS * *for debugging purposes:

```python
> KEYS *
1) "ft:shakespeare/1"
2) "ft:shakespeare/31"
3) "idx:shakespeare"
4) "ft:shakespeare/5"
5) "ft:shakespeare/macbeth"
6) "ft:shakespeare/lady"
7) "nm:shakespeare/speech"
8) "geo:shakespeare/location"
9) "57956"

```

Running two commands had yielded 9 keys. I want to highlight a few of these keys just to fill out the understanding of what is actually going on here:

```python
> TYPE idx:shakespeare
ft_index0

```

Here we can see that RediSearch has created a key with it’s own datatype (ft_index0). We can’t really do much with this key directly, but it’s important to know that it exists and how it was created.

Now, let’s look at key *57956*

```python
> TYPE 57956
hash

```

A hash! We can work with this — let’s look at this key directly:

```python
> HGETALL 57956
 1) "text_entry"
 2) "Out, damned spot! out, I say!--One: two: why,"
 3) "line"
 4) "5.1.31"
 5) "play"
 6) "macbeth"
 7) "speech"
 8) "15"
 9) "speaker"
10) "LADY MACBETH"
11) "location"
12) "-3.9264,57.5243"

```

This should look familiar as it’s your data from the FT.ADD command and the key is just your document ID. While it’s important to know how this is being stored, don’t manipulate this key directly with HASH commands.

```python
> TYPE nm:shakespeare/speech
numericdx

```

Interesting — the field *speech *in our dataset is a numeric index and the type is a “numericdx.” Again, since this is a RediSearch native datatype, we can’t manipulate this with any ‘normal’ Redis commands.

```python
> TYPE geo:shakespeare/location
zset

```

The key here gives you a hint — while the TYPE command returns that it’s a ZSET, Redis geohash sets are stored as ZSETs and will report as them when the type is queried. That being said, let’s look at a couple of GEO commands:

```python
> GEOHASH geo:shakespeare/location 1
1) "gfjpnxuzk40"
> GEOPOS geo:shakespeare/location 1
1) 1) "-3.92640262842178345"
   2) "57.52429905544970268"

```

Brilliant! RediSearch has stored the coordinates in a bog-standard GEO set. But, like the hash above, don’t modify these values directly with ZSET or GEO commands.

Finally, let’s take a look at one more key:

```python
> TYPE ft:shakespeare/lady
ft_invidx

```

Sharp readers might notice that the term “lady” was only indexed in a full-text field (speaker). Data stored *ft_invidx* keys are textual indexes.

Now that we know a little about how RediSearch is storing our data, we can start to load more substantial information into database and explore querying but that will have to wait to Part II of Mastering RediSearch coming in a few weeks.
