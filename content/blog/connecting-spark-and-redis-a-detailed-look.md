---
title: "Connecting Spark and Redis: A Detailed Look"
linkTitle: "Connecting Spark and Redis: A Detailed Look"
url: "/blog/connecting-spark-and-redis-a-detailed-look/"
description: "The spark-redis package on github is our1 first step in the Spark-Redis journey. Spark has captured the public imagination around the real-time possibilities of big data and we1 hope to contribute..."
date: 2016-02-02
blogCategories:
- "Tech"
authors:
- "Itamar Haber"
lastmod: 2025-03-27
hidden: true
---

*By Itamar Haber, Technology Evangelist · Published 2 February 2016 · updated 27 March 2025*

![Blog tile image](/images/blog/821a3948c41937b5cb942d6274be60848ebb619f-635x200.webp)

The [spark-redis package](https://github.com/RedisLabs/spark-redis) on github is our[1](#Sun He) first step in the Spark-Redis journey. Spark has captured the public imagination around the real-time possibilities of big data and we[1](#Sun He) hope to contribute in making this possibility a reality.

The spark-redis package is a Redis connector for Apache Spark that provides read and write access to all of Redis’ core data structures (RcDS) as RDDs (Resilient Distributed Datasets, not to be confused with RDBs).

I thought it would be fun to take the new connector for a test run and show off some of its capabilities. The following is my journey’s log. First things first…

## Setting up

There are a few prerequisites you need before you can actually use spark-redis, namely: [Apache Spark](http://spark.apache.org/), [Scala](http://www.scala-lang.org), [Jedis](https://github.com/xetorthio/jedis) and [Redis](https://redis.io/). While the package specifically states version requirements for each piece, I actually used later versions with no discernible ill effects (v1.5.2, v2.11.7, v2.8 and unstable respectively).

I fumbled quite a lot trying to get it all working. Just after I finished putting everything in place, friend and fellow Redis-eur [Tim Spann @PaaSDev](https://twitter.com/PaaSDev) published a step-by-step on [“Setting up a Standalone Apache Spark Cluster”](https://dzone.com/refcardz/apache-spark) over at [@DZone](https://twitter.com/DZoneinc). That should get you through the hairiest parts if you’re on Ubuntu like me.

Once you’ve fulfilled all the requirements, you can just git clone https://github.com/RedisLabs/spark-redis, build it by running [sbt](http://www.scala-sbt.org/) (oh, yeah, install that one too) or just use the package from [spark-packages.org ()](http://spark-packages.org/package/RedisLabs/spark-redis) and you should be all ready to go… but go where exactly?

## Mission statement

With this being an educational exercise, I needed a problem that could be solved with an advanced Directed Acyclic Graph engine and the fastest NoSQL Data Structure Store. After [extensive research](https://www.google.com/?q=spark+example1), I managed to identify perhaps the biggest challenge of contemporary data science – the counting of words. Since the word count challenge is the de-facto “Hello, World!” equivalent in Spark core, I elected to use it as my basis for tentative exploration and see how it could be adapted for use with Redis.

## Reading the data

The first thing you need when counting words is, of course, words. Being the single-minded individual I am, I decided on counting the words in Redis’ source code files ([this commit](https://github.com/antirez/redis/commit/fceaa46dda37a2d4db4e0a48cc1dab3fe208cb2c) specifically), also hoping to reveal some interesting data-sciency facts in the process. With everything ready, I started by jumping into spark-shell:

```javascript
itamar@ubuntu:~/src$ ./spark-1.5.2/bin/spark-shell --jars spark-redis/target/spark-redis-0.5.1.jar,jedis/target/jedis-2.8.0.jar
Spark context available as sc.
SQL context available as sqlContext.
Welcome to
____              __
/ __/__  ___ _____/ /__
_ / _ / _ `/ __/  '_/
/___/ .__/_,_/_/ /_/_   version 1.5.2
/_/
Using Scala version 2.11.7 (OpenJDK 64-Bit Server VM, Java 1.7.0_91)
Type in expressions to have them evaluated.
Type :help for more information.
scala>
```

The blinking cursor meant that the world was ready for my first line of Scala, and so I typed in:

```javascript
scala> val wtext = sc.wholeTextFiles("redis/src/*.[ch]")
wtext: org.apache.spark.rdd.RDD[(String, String)] = redis/src/*.[ch]
WholeTextFileRDD[0] at wholeTextFiles at :24
scala> wtext.count
res0: Long = 100
```

That’s awesome! I barely got started and already data science proved to be useful: there are exactly 100 Redis source files! Of course, doing

```javascript
ls -1 redis.src/*.[ch] | wc -l
```

Encouraged by my success, I rushed forward intent on getting the contents of the files transformed to words (that could later be counted). Unlike the usual examples that use the TextFileRDD, the WholeTextFilesRDD consists of file URLs and their contents, so it turned out that the following snippet did the work needed for splitting and cleaning the data (the call to the cache() method is strictly optional, but I try to follow best practices and expected to use that RDD later on again).

```javascript
val fwds = wtext.
flatMap{ case (filename, contents) =>
val fname = filename.substring(filename.lastIndexOf("/") + 1)
contents.
split("W+").
filter(!_.isEmpty).
map( word => (fname, word))
}
fwds.cache()
```

A note about variable names: I like them meaningful and short, so naturally wtf means WholeTextFiles, fwds is FileWords and so forth.

Once the fwds RDD had clean filenames and all the words were neatly split, I was off for some serious counting. First, I recreated the ubiquitous word counting example:

```javascript
val wcnts = fwds.
map{ case (fname, word) => (word, 1) }.
reduceByKey(_ + _).
map{ case (word, count) => (word, count.toString) }
```

Pasting the above into the spark-shell and following with take confirmed success:

```javascript
wcnts: org.apache.spark.rdd.RDD[(String, String)] = MapPartitionsRDD[5] at map at :31
```

```javascript
scala> wcnts.take(10)res1: Array[(String, String)] = Array((requirepass,15), (mixdigest,2), (propagte,1), (used_cpu_sys,1), (rioFdsetRead,2), (0x3e13,1), (preventing,1), (been,12), (modifies,1), (geoArrayCreate,3))
```

```javascript
scala> wcnts.count()
res2: Long = 12657
```

A note about the results: take isn’t supposed to be deterministic, but given that “requirepass” keeps surfacing these days, it may well be fatalistic. Also, 12657 must have some meaning but I’ve yet to find it.

## Writing RDDs to Redis

Now comes the really fun stuff, a.k.a Redis. I wanted to make sure that the results were stored somewhere safe (like my non-persisted, unbound, password-less Redis server ;)) so I could use them in later computations. Redis’ Sorted Sets are a perfect match for the word-count pairs and would also allow me to query the data like I’m used to. It took only one line of Scala code to do that (actually three lines, but the first two don’t count):

```javascript
import com.redis.provider.redis._
val redisDB = ("127.0.0.1", 6379)
sc.toRedisZSET(wcnts, "all:words", redisDB)
```

With the data where I was comfortable examining it, I fired up the cli and did a few quick reads:

```javascript
itamar@ubuntu:~/src$ ./redis/src/redis-cli127.0.0.1:6379> DBSIZE(integer) 1127.0.0.1:6379> ZCARD all:words(integer) 12657127.0.0.1:6379> ZSCORE all:words requirepass"15"127.0.0.1:6379> ZREVRANGE all:words 0 4 WITHSCORES1) "the"2) "8164"3) "if"4) "6657"5) "0"6) "5396"7) "c"8) "4524"9) "1"10) "4293"127.0.0.1:6379> ZRANGE all:words 6378 63791) "mbl"2) "mblen"
```

Nice! What else can I keep in Redis? Why, everything of course. The filenames themselves are perfect candidates, so I made another RDD and stored it in a regular Set:

```javascript
val fnames = fwds.map{ case (fname, word) => fname }.distinct()sc.toRedisSET(fnames, "all:files", redisDB)
```

Despite being very useful for science purposes, the contents fnames Set is pretty mundane and I wanted something more… so how about storing the word count for each file in its very own Sorted Set? With a few transformations/actions/RDDs I was able to do just that:

```javascript
fwds.groupByKey.collect.foreach{ case(fname, contents) =>val zsetcontents = contents.groupBy( word => word ).map{ case(word, list) => (word, list.size.toString) }.toArraysc.toRedisZSET(sc.parallelize(zsetcontents), "file:" + fname, redisDB)}
```

Back to redis-cli:

```javascript
127.0.0.1:6379> dbsize(integer) 102127.0.0.1:6379> ZREVRANGE file:scripting.c 0 4 WITHSCORES1) "lua"2) "366"3) "the"4) "341"5) "if"6) "227"7) "1"8) "217"9) "0"10) "197"
```

## Reding RDDs from Redis

I could have danced (stored word-count data) all night, but if you only write and never read you’d be better off using a spark-/dev/null connector. So to make practical use of the data in Redis, I ran the following code that took the per-file word counts and reduced them to basically the same output of the classic WC challenge:

```javascript
val rwcnts = sc.fromRedisKeyPattern(redisDB, "file:*").getZSet().map{ case (member, count) => (member, count.toFloat.toInt) }.reduceByKey(_ + _)
```

Then back to spark-shell to test this code and get a grand total of all words:

```javascript
scala> rwcnts.count()res8: Long = 12657scala> val total = rwcnts.aggregate(0)(| (acc, value) => acc + value._2,| (acc1, acc2) => acc1 + acc2)total: Int = 27265
```

To wrap things up, I couldn’t just take Spark’s result for granted, so I double checked using a Lua script:

```javascript
local tot1, tot2, cursor = 0, 0, 0
repeat
local rep1 = redis.call('SCAN', cursor, 'MATCH', 'file:*')
cursor = tonumber(rep1[1])
for _, ssk in pairs(rep1[2]) do
local rep2 = redis.call('ZRANGE', ssk, 0, -1, 'WITHSCORES')
for i = 2, #rep2, 2 do
tot1 = tot1 + tonumber(rep2[i])
end
end
until cursor == 0
local rep = redis.call('ZRANGE', 'all:words', 0, -1, 'WITHSCORES')
for i = 2, #rep, 2 do
tot2 = tot2 + tonumber(rep[i])
end
return { tot1, tot2 } itamar@ubuntu:~/src$ ./redis/src/redis-cli --eval /tmp/wordcount.lua 1) (integer) 272655 2) (integer) 272655
```

## Closing notes

Back in the days when data was small, you could get away with counting words using a simple wc -w. As data grows, we find new ways to abstract solutions and in return gain flexibility and scalability. While I’m no data scientist (yet), Spark is an exciting tool to have – I’ve always liked DAGs – and its core is extremely useful. And that’s even without going into its integration with the Hadoop ecosystem and extensions for SQL, streaming, graphs processing and machine learning… yum.

Redis quenches Spark’s thirst for data. [spark-redis](http://spark-packages.org/package/RedisLabs/spark-redis) lets you marry RDDs and RcDSs with just a line of Scala code. The first release already provides straightforward RDD-parallelized read/write access to all core data structures and a polite (i.e.SCAN-based) way to fetch key names. Furthermore, the connector carries considerable hidden punch as it is actually (Redis) cluster-aware and maps RDD partitions to hash slots to reduce inter-engine shuffling. This is just the first release for the connector, and there’s another release coming Soon(tm) which may break and change a few things, so take that into consideration. Of course, since the package is [open source](https://github.com/RedisLabs/spark-redis) you’re more than welcome to use/extend/fix/complain about it 🙂

1. ‘we’ being Redis and the talented Sun He @sunheehnus of the Redis community
