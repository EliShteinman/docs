---
title: "Getting Started with Redis, Apache Spark and Python"
linkTitle: "Getting Started with Redis, Apache Spark and Python"
url: "/blog/getting-started-redis-apache-spark-python/"
description: "Apache Spark is one of the most popular frameworks for creating distributed data processing pipelines and, in this blog, we’ll describe how to use Spark with Redis as the data repository for..."
date: 2019-02-12
blogCategories:
- "How To and Tutorials"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 12 February 2019 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/50cfe8b569c3ff43a96baacca7496b571d4761a9-1200x1000.webp)

[Apache Spark](https://spark.apache.org/) is one of the most popular frameworks for creating distributed data processing pipelines and, in this blog, we’ll describe how to use Spark with Redis as the data repository for compute. Spark’s main feature is that a pipeline (a Java, Scala, Python or R script) can be run both locally (for development) and on a cluster, without having to change any of the source code.

Spark allows this flexibility by cleverly using delayed computation or, as it is called in some contexts, laziness. Everything starts with the classes RDD, DataFrame and the more recent Dataset, which are each distributed lazy representations of your data. They use distributed file systems, databases or other similar services as actual storage backend. Their operations — such as map/select, filter/where and reduce/groupBy — do not really make the computation happen. Rather, every operation adds a step to an execution plan that is eventually run when an actual result is needed (e.g., when trying to print it to screen).

When launching the script locally, all computations happen on your machine. Alternately, when launching on a distributed cluster, your data is partitioned to different nodes; the same operation happens (mostly) in parallel within the Spark cluster.

### About RDD, DataFrame, and Dataset

Over time, Spark developed three different APIs to deal with distributed data sets. While each new addition added more capabilities over the previous ones, no single API is a complete replacement of what came before. In order of creation (oldest to newest), here’s an overview:

- **RDD** offers low-level ways to apply compile-time, type-safe operations to your data. Using RDD, you express in your code “how” you want things to happen as opposed to a more declarative approach.
- **DataFrame** introduces a SQL-like approach to expressing computations (it even supports actual SQL queries). Its declarative syntax allows Spark to build optimized query plans, resulting in generally faster code compared to RDD.
- **Dataset** is an improvement of DataFrame for Java Virtual Machine (JVM) languages. It introduces the compile-time type safety that DataFrame lacks, as well as an optimized representation for rows that greatly reduces memory usage. It doesn’t really do anything for dynamic languages (Python, R) because of their dynamic nature, so from those you will still use DataFrame (which, in the meantime, was internally re-implemented as a Dataset).

For more details, check out “[A Tale of Three Apache Spark APIs](https://databricks.com/blog/2016/07/14/a-tale-of-three-apache-spark-apis-rdds-dataframes-and-datasets.html)” by Jules Damji.

### About spark-redis

[spark-redis](https://github.com/RedisLabs/spark-redis) is an open source connector that allows you to use Redis to store your data.

Three main reasons to use Redis as a backend are:

- **DataFrame/set and Redis-specific RDDs:** spark-redis implements both the more general purpose interfaces, as well as RDDs that expose the [data structures](https://redis.io/docs/manual/data-types/) Redis is famous for. This means you can very easily deploy your existing scripts on Redis and make use of Redis-specific functionality when you need full control.
- **Redis Cluster:** The connector speaks the [Redis Cluster API](https://docs.redis.com/latest/rs/concepts/data-access/oss-cluster-api/) and makes full use of a sharded database, including re-sharding and failovers. With your data in a Redis Cluster, you’ll greatly improve performance, since your pipeline will spin up multiple consumers for your data.
- **Redis Streams:** [Spark Streaming](https://spark.apache.org/streaming/) is a perfect match for the new [Redis Streams](/blog/use-redis-streams-apps/) data structure. Redis Streams also uses consumer groups that allow you to elegantly tune the level of parallelism.

In this article we will focus on getting started with Python and how to use the DataFrame API. At time of writing, Scala which can be considered the “native” language of Spark, has access to some of the more advanced features of the integration, like Redis RDDs and Streams. Since Scala is a JVM language, by extension Java can also use these features. With Python, we’ll need to stick to DataFrames.

### Setting up

Our first step is to install [pyspark](https://pypi.org/project/pyspark/) using [pip](https://pypi.org/project/pip/). You will also need [Java 8 installed on your machine](https://www.oracle.com/java/technologies/downloads/#java8).

$ pip install pyspark

Next, we’ll need Maven to build spark-redis. You can get it from the [official website](https://maven.apache.org/) or by using a package manager (e.g. homebrew on macOS).

[Download spark-redis from GitHub](https://github.com/RedisLabs/spark-redis) (either git clone or download as a zip), and build it using Maven.

$ cd spark-redis
$ mvn clean package -DskipTests

In the target/ subdirectory, you’ll find the compiled jar file.

If you don’t have it already, you will need a running Redis server to connect to. You can download it in a number of ways: from the [official website](https://redis.io/download/), package manager (apt-get or brew install redis) or [Docker Hub](https://hub.docker.com/_/redis) (psst, this might be a good moment to try out [Redis Enterprise](https://hub.docker.com/_/redis)).

Once you have it up and running, you can launch pyspark. Note that you’ll need to change VERSION to reflect the version you downloaded from GitHub.

$ pyspark –jars target/spark-redis-VERSION-jar-with-dependencies.jar

If your Redis server is in a container or has authentication enabled, add these switches to the previous invocation (and change the values to fit your situation).

–conf “spark.redis.host=localhost” –conf “spark.redis.port=6379” –conf “spark.redis.auth=passwd”

## Playing with a sample dataset

Now that we have a functioning pyspark shell that can store data on Redis, let’s play around with [this famous people data set](https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/28201/VEG34D&version=1.0).

### Getting started

After downloading the TSV file, let’s load it as a Spark DataFrame.

```python
>>> full_df = spark.read.csv("pantheon.tsv", sep="\t", quote="", header=True, inferSchema=True)
>>> full_df.dtypes
[('en_curid', 'int'), ('name', 'string'), ('numlangs', 'int'), ('birthcity', 'string'), ('birthstate', 'string'), ('countryName', 'string'), ('countryCode', 'string'), ('countryCode3', 'string'), ('LAT', 'double'), ('LON', 'double'), ('continentName', 'string'), ('birthyear', 'string'), ('gender', 'string'), ('occupation', 'string'), ('industry', 'string'), ('domain', 'string'), ('TotalPageViews', 'int'), ('L_star', 'double'), ('StdDevPageViews', 'double'), ('PageViewsEnglish', 'int'), ('PageViewsNonEnglish', 'int'), ('AverageViews', 'double'), ('HPI', 'double')]


```

Now, invoking .dtypes shows a list of all the columns (and relative types) in the data set. There are many things that could be interesting to investigate in this data set, but for the purpose of this example let’s focus on **finding, for each country, the most frequent occupation of its famous people**.

Let’s start by keeping only the columns relevant to our goal.

```python
>>> data = full_df.select("en_curid", "countryCode", "occupation")
>>> data.show(2)
+--------+-----------+-----------+
|en_curid|countryCode| occupation|
+--------+-----------+-----------+
|     307|         US| POLITICIAN|
|     308|         GR|PHILOSOPHER|
+--------+-----------+-----------+
only showing top 2 rows

```

This will create a copy of the original DataFrame that only contains three columns: the unique ID of each person, their country and their occupation.

We started by downloading a small data set for the purpose of this blog post, but in real life, if you were using Spark, the data set would likely be much bigger and hosted remotely. For this reason, let’s try to make the situation more realistic in the next step by loading the data into Redis:

```python
>>> data.write.format("org.apache.spark.sql.redis").option("table", "people").option("key.column", "en_curid").save()


```

This command will load our data set into Redis. The two options we specified help define the data layout in Redis, as we’ll now see.

### DataFrames on Redis

Let’s jump for a moment in [redis-cli](https://redis.io/docs/manual/cli/) to see how our DataFrame is stored on Redis:

```python
$ redis-cli
> SCAN 0 MATCH people:* COUNT 3
1) "2048"
2) 1) "people:2113653"
   2) "people:44849"
   3) "people:399280"
   4) "people:101393"

```

[SCAN](https://redis.io/commands/scan/) shows us some of the keys we loaded to Redis. You can immediately see how the options we gave before were used to define the key names:

- “table”, “people” defined a common prefix for the keys representing this DataFrame, and
- “key.column”, “en_curid” defined the primary key for our DataFrame.

Let’s take a look at the content of a random key:

```python
> HGETALL people:2113653
1) "countryCode"
2) "DE"
3) "occupation"
4) "SOCCER PLAYER"

```

As you can see, each row of our DataFrame became a [Redis Hash](https://redis.io/docs/manual/data-types/#hashes) containing countryCode and occupation. As stated earlier, en_curid was used as primary key, so it became part of the key name.

Now that we’ve seen how the data is stored on Redis, let’s jump back into pyspark and see how we would actually write a pipeline to get the most common occupation for the famous people of each country.

### Performing computations from a Redis DataFrame

Even though we should have the data still loaded into memory, let’s load it from Redis in order to write code that’s more similar to what you would do in real life.

```python
>>> df = spark.read.format("org.apache.spark.sql.redis").option("table", "people").option("key.column", "en_curid").load()
>>> df.show(2)
+--------+-----------+----------+
|en_curid|countryCode|occupation|
+--------+-----------+----------+
|  915950|         ZW|   SWIMMER|
|  726159|         UY|POLITICIAN|
+--------+-----------+----------+
only showing top 2 rows

```

This is how your Spark pipeline would start, so let’s finally do the computation!

```python
>>> counts = df.groupby("countryCode", "occupation").agg({"en_curid": "count"})
>>> counts.show(2)
+-----------+-------------+---------------+
|countryCode|   occupation|count(en_curid)|
+-----------+-------------+---------------+
|         FR|MATHEMATICIAN|             34|
|         IT|SOCCER PLAYER|             81|
+-----------+-------------+---------------+
only showing top 2 rows

```

Now each row represents the count of all the present (country, occupation) combinations. For the next step, we need to select only the occupation with the highest count for each country.

Let’s start by importing a few new modules we need, and then defining, using [windows](/events/unlocking-power-sorted-sets/), the code to select the most frequent occupations:

```python
>>> from pyspark.sql.window import Window
>>> from pyspark.sql.functions import count, col, row_number
>>> w = Window().partitionBy("countryCode").orderBy(col("count(en_curid)").desc())
>>> result = counts.withColumn("rn", row_number().over(w)).where(col("rn") == 1).select("countryCode", "occupation")
>>> result.show(5)
+-----------+-------------+
|countryCode|   occupation|
+-----------+-------------+
|         DZ|   POLITICIAN|
|         LT|   POLITICIAN|
|         MM|   POLITICIAN|
|         CI|SOCCER PLAYER|
|         AZ|   POLITICIAN|
+-----------+-------------+
only showing top 5 rows

```

This code grouped the original rows by countryCode, ordered the content of each group by count(en_curid)in descending order, and took only the first element. As you can see, within this small sample, politician seems a very common occupation.

Let’s see for how many countries this is true:

```python
>>> result.where(col("occupation") == "POLITICIAN").count()
150

```

Wow, that’s a lot, considering there are 195 countries in the world as of today. Now, let’s just save the remaining countries in Redis:

```python
>>> no_pol = result.where(col("occupation") != "POLITICIAN")
>>> no_pol.write.format("org.apache.spark.sql.redis").option("table", "occupation").option("key.column", "countryCode").save()


```

If you now jump into redis-cli, you will be able to see the new data:

```python
$ redis-cli
> HGETALL occupation:IT
1) "occupation"
2) "RELIGIOUS FIGURE"
> HGETALL occupation:US
1) "occupation"
2) "ACTOR"

```

If you want to practice more, inspect the original data set and see if you find other details that pique your interest.

### An afterword on Spark data types and the Redis Cluster API

A very important point worth reiterating is that every operation on a RDD or DataFrame/set object will be distributed on multiple nodes. If our example was not just about *famous* people, we’d have had tens of millions of rows at the beginning. In that case, Spark would scale out the computation. But if you only had one Redis instance in place, you’d have *N* nodes hammering on it, most probably bottlenecking your network bandwidth.

To get the most out of Redis, you’ll need to scale it appropriately using the Redis Cluster API. This will ensure that all your computing nodes are not starved when reading, or choked when writing.

### Conclusion

In this post, we explored how to download, compile and deploy spark-redis in order to use Redis as a backend for your Spark DataFrames. Redis offers full support for the DataFrame API, so it should be very easy to port existing scripts and start enjoying the added speed Redis offers. If you want to learn more, take a look at the [documentation for spark-redis on GitHub](https://github.com/RedisLabs/spark-redis).
