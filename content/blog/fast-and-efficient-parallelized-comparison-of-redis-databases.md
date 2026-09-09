---
title: "Fast and Efficient Parallelized Comparison of Redis Databases"
linkTitle: "Fast and Efficient Parallelized Comparison of Redis Databases"
url: "/blog/fast-and-efficient-parallelized-comparison-of-redis-databases/"
description: "The process of comparing two versions of a database is a fairly common practice, generally used for testing and development purposes, as well as supporting application updates and new releases...."
date: 2014-04-16
blogCategories:
- "Tech"
authors:
- "Yoav Steinberg"
lastmod: 2025-03-27
hidden: true
---

*By Yoav Steinberg · Published 16 April 2014 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/1b6fdc2e664fbb627d82768d4fe0ab77a6a1a7cd-270x225.webp)

The process of comparing two versions of a database is a fairly common practice, generally used for testing and development purposes, as well as supporting application updates and new releases. Comparing databases provides a number of advantages. Beginning by ensuring two databases are fully synced, then enabling users to assess the functionality of the backup setup and various processes, including verification of backup restoration or master-slave replication. This process is highly useful to anyone who uses a Redis database. As such, at Redis, we compare older versions of databases with our own newly developed ones, ensuring the replication mechanism between the different versions is satisfactory. In addition, we continuously validate our database synchronizations between different cloud zones and regions as a means to support customers with their [fully managed and highly available Redis databases](/redis-cloud). The following information expands upon the process I underwent to develop the Redis comparison tool.

![](/images/site-mirror/489fa71d38ddce27cb86c758812bb7ea531283ba-635x200.webp)

### The Redis RDB Tools

Initially, we used [Redis RDB Tools](https://github.com/sripathikrishnan/redis-rdb-tools), which is an open source project that provides libraries to efficiently parse Redis dump files (RDB). The Redis RDB Tools library also provides tools to compare two RDB files, analyzing the amount of memory that their operations require, among other useful capabilities. By means of the dump file of a given database, Redis RDB Tools prints a text file consisting of all existing key names and respective values sorted alphabetically. Once a file has been created for each database, the two files can be compared easily using a simple text comparison tool (e.g. [diff](https://man.cx/diff(1)) or [meld](https://meldmerge.org/)).

### The Drawbacks

Redis RDB Tools has proven to be very flexible and useful in the past, though over time, several drawbacks were discovered.

1. Redis includes several data types: strings, hashes, sorted sets, and lists. Unfortunately, Redis RDB Tools does not sufficiently dump sorted sets and frequently confuses the order of the sets, running the risk of harming a comparison. On the bright side, this is a minor obstacle that can be [easily resolved](https://github.com/yoav-steinberg/redis-rdb-tools/commit/f2352316c1283dd71eb6479ae722d7b1dc91bd55).
1. The Redis RDB Tools comparison process requires the creation of dump files. This may pose a challenge if remote access to the database solely exists. Additionally, since we often deal with large datasets, generating dump files can be cumbersome, costly and time consuming.
1. The RDB Tools method requires sorting text files, meaning the text files are held in RAM. This makes matters difficult when dealing with large datasets. For instance, in order to run the process on a Redis server that holds 60 GB of data in RAM, a development machine must be supplied with sufficient memory to hold the corresponding dump file. Using instances with these quantities of RAM for test and development is costly and therefore may render the entire comparison process impossible.

### Our Solution

Redis’ recent version 2.8 introduced [a family of commands](https://redis.io/commands/scan) (SCAN, HSCAN, SSCAN and ZSCAN) that are used to incrementally iterate a collection of keys. Using the SCAN function, it is possible to iterate through all of the keys in one database, and compare each key with the corresponding key type in a second database, if such a key, indeed, exists. This can provide a simple and efficient comparison solution that operates on the existing database and therefore does not require any additional compute resources or the creation of a local dump file.

Even with this fairly straightforward approach, we ran into performance issues when dealing with large datasets. Comparing millions of keys, one key type at a time, while using a single Redis connection is still a very slow process. In order to overcome this, I wrote a [script](https://gist.github.com/yoav-steinberg/10589500) which consists of a pool of processes using Python’s multiprocessing library. Through this method, the main process iterates all of the keys in the source database and subsequently sends several keys to the processes in the pool. Each process then compares the key it received with the second database. Since the comparisons are parallelized, the entire process is completed much faster.

### Further Improvement

The script currently prints *“Key X differs key Y”* when discrepancies are discovered between two databases. Improvements can be made to the tool by having a more detailed output, such as indicating the specific element that differs within a list type key.

Redis keys can be optionally set with expiration values. During a comparison, it is possible that a key read from the source database will have already expired in the target database (or vice versa), however, our tool will still indicate a difference. Since the key will soon expire this difference may be irrelevant to the overall database comparison, nonetheless, our current version does not take this factor into account. Setting a threshold for minimal expiration values and comparing between different expiration values is yet another useful improvement that would enhance the tool.

It should be noted that this solution could possibly fall short if the data is altered during the comparison process. This tool should be used for cases in which data is constant, or if real time data changes are tolerable.

I welcome you to [download](https://gist.github.com/yoav-steinberg/10589500) this Python script that will help perform a simple and quick comparison of your Redis database.
