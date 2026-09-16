---
title: "Getting Started with RediSearch 2.0"
linkTitle: "Getting Started with RediSearch 2.0"
url: "/blog/getting-started-with-redisearch-2-0/"
description: "RediSearch 2.0 is now out in public preview! Most of the features in this major new release have been driven by your feedback, with a focus on improving the developer experience and enhanced..."
date: 2020-09-17
blogCategories:
- "Tech"
- "Tech Redis Modules"
authors:
- "Tugdual Grall"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Tugdual Grall, Technical Marketing Manager · Published 17 September 2020 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/982857fb3b57db29fbfe252734054aa84a79eaef-386x260.webp)

RediSearch 2.0 is now out in public preview! Most of the features in this major new release have been driven by your feedback, with a focus on improving the developer experience and enhanced scalability. But this blog post concentrates on helping you get started using RediSearch 2.0’s new data indexing capabilities and better ways to create an index.

Having a rich query and aggregation engine inside your Redis database opens the door to many new applications that go well beyond caching. You can use Redis as your primary database even when you need to access the data using complex queries, without adding complexity to the code to update and index data. All this with Redis’ famous speed, reliability, and scalability!

**For more on what’s new, see **[**Introducing RediSearch 2.0**](/blog/introducing-redisearch-2-0/)

## Getting started

**Prerequisites**

To get started with RediSearch 2.0, you’ll need:

- Docker
- A Redis command-line interface. Your two main options are:
  - [redis-cli](https://redis.io), provided with Redis
  - [RedisInsight](/insight/), a free GUI for streamlined Redis application development, that also includes a command–line interface.

**Get a Redis database with RediSearch enabled**

You can install and use RediSearch 2.0 in various ways:

- [Redis Enterprise Cloud](/try-redis-modules-for-free/)
- [Redis Enterprise Software](/try-free/)
- [RediS](https://oss.redis.com/redisearch/Quick_Start/#download_and_running_binaries)[e](https://oss.redis.com/redisearch/Quick_Start/#download_and_running_binaries)[arch binaries](https://oss.redis.com/redisearch/Quick_Start/#download_and_running_binaries)
- [RediSearch sources](https://oss.redis.com/redisearch/Quick_Start/#building_and_running_from_source)
- [Docker image](https://hub.docker.com/r/redislabs/redisearch/)

For simplicity, this blog post will use the Docker images. (If you have already installed RedisSearch 2.0, you can jump to the next section.) To start your Redis instance with Docker, open a terminal and run the following command:

```javascript
> docker run -it --rm --name redis-search-2 \
   -p 6379:6379 \
   redis/redisearch:2.0.0
```

**Note: **The container will automatically be removed when it exits (–rm parameter).

## Connect to Redis and insert data

Using your favorite Redis client, connect to the RediSearch database.

If you have started your Redis instance with Docker you can use the following command to use the redis-cli embedded in the container:

```javascript
> docker exec -it redis-search-2 redis-cli
```

If you want to use Redis Insight, [add your RediSearch instance](https://docs.redis.com/latest/ri/using-redisinsight/add-instance/) and go to the [CLI](https://docs.redis.com/latest/ri/using-redisinsight/cli/).

**Insert data**

You are now ready to insert some data. This example uses movie data stored as Redis Hashes, so let’s insert a couple of movies:

```javascript
> HSET movie:11002 title "Star Wars: Episode V - The Empire Strikes Back" plot "Luke Skywalker begins Jedi training with Yoda." release_year 1980 genre "Action" rating 8.7 votes 1127635

(integer) 6 

> HSET movie:11003 title "The Godfather" plot "The aging patriarch of an organized crime dynasty transfers control of his empire to his son." release_year 1972 genre "Drama" rating 9.2 votes 1563839 

(integer) 6
```

The database contains now two Hashes. It is simple to retrieve information using the following command, if you know the key of the movie (movie:11002):

```javascript
> HMGET movie:11002 title rating

1) "Star Wars: Episode V - The Empire Strikes Back"
2) "8.7"
```

But how can you query the database to get a list of movies based using the title, the genre, or the release_year?

With “core” Redis data structures, you have to manage your index yourself using Sets to associate the genre to the list of movie IDs, for example, and add a lot of code to your application to manage and query the index.

But with RediSearch you can simply define an index associated with your data and let the database manage them. You can then use the query engine to query/search the data using secondary indices.

## Create a RediSearch index for the movies

To create an index, you must define a schema to list the fields and their types that are indexed, and that you can use in your queries.

For this example you will be indexing four fields:

1. Title
1. Release year
1. Rating
1. Genre

Creating the index is done using the [FT.CREATE](https://redis.io/commands/ft.create/) command:

```javascript
> FT.CREATE idx:movie ON hash PREFIX 1 "movie:" SCHEMA title TEXT SORTABLE release_year NUMERIC SORTABLE rating NUMERIC SORTABLE genre TAG SORTABLE

OK
```

Before running queries, though, let’s take a closer look at the FT.CREATE command:

- idx:movie: the name of the index, which you will use when doing queries
- ON hash: the type of structure to be indexed. *(Note that RediSearch 2.0 supports only the Hash structure, but this parameter will allow RediSearch to index other structures in the future.)*
- PREFIX 1 “movie:”: the prefix of the keys that should be indexed. This is a list, so since we want to only index movie:* keys the number is 1. If you want to index movies and TV shows with the same fields, you could use: PREFIX 2 “movie:” “tv_show:”
- SCHEMA …: defines the schema, the fields, and their type to index. As you can see in the command, we are using TEXT, [NUMERIC](https://oss.redis.com/redisearch/Overview/#numeric_index), and [TAG](https://oss.redis.com/redisearch/Overview/#tag_index), and [SORTABLE](https://oss.redis.com/redisearch/Overview/#sortable_fields) parameters.

The RediSearch 2.0 engine will scan the database using the PREFIX values, and update the index based on the schema definition. This makes it **easy to add an index to an existing application** that uses Hashes, there’s no need to change your code.

You can see the index information with the following command:

```javascript
> FT.INFO idx:movie

 1) index_name
 2) idx:movie
... 
46) 1) global_idle
    2) (integer) 0
...
```

Now we’re ready to use the index and query the database.

## Query the movie database

For this section you will use the [FT.SEARCH](https://oss.redis.com/redisearch/Commands.html#ftsearch) command and its [syntax](https://redis.io/docs/stack/search/reference/query_syntax/); note that the goal of this blog post is to get you started, so we stick to the basics and don’t go into all the details. To learn more about RediSearch, look at the [documentation](https://oss.redis.com/redisearch/) and the [tutorial](https://github.com/RediSearch/redisearch-getting-started).

**Full-text search queries**

RediSearch is a full-text search engine, allowing the application to run powerful queries à la Google. For example, to search all movies that contain “*war*”-related information, you would run the following command:

```javascript
> FT.SEARCH idx:movie "war" RETURN 3 title release_year rating

1) (integer) 1
2) "movie:11002"
3) 1) "title"
   2) "Star Wars: Episode V - The Empire Strikes Back"
   3) "release_year"
   4) "1980"
   5) "rating"
   6) "8.7"
```

As you can see, the movie *Star Wars: Episode V—The Empire Strikes Back* is found, even though you used only the word “*war*” to match “*Wars*” in the title. This is because the title has been indexed as text, so the field is [tokenized](https://redis.io/docs/stack/search/reference/escaping/) and [stemmed](https://redis.io/docs/stack/search/reference/stemming/).

Also, the command does not specify a field, so the word “war” (*and related words*) is searched in all text fields of the index. If you want to search specific fields, you would use the @field notation, as shown here:

```javascript
> FT.SEARCH idx:movie "@title:war" RETURN 3 title release_year rating
```

You can run additional full-text search queries against this simple dataset, as demonstrated here *(Note: to keep the document short, the results of the queries are not shown):*

Prefix matches:

```javascript
> FT.SEARCH idx:movie "emp*" RETURN 3 title release_year rating
```

Fuzzy search:

```javascript
> FT.SEARCH idx:movie "%gdfather%" RETURN 3 title release_year rating
```

Unions:

```javascript
> FT.SEARCH idx:movie "war |  %gdfather% " RETURN 3 title release_year rating
```

You can find more information about the[ query syntax in the RediSearch documentation](https://redis.io/docs/stack/search/reference/query_syntax/).

**Tag field search**

Use the tag field “genre” to find all “drama” movies:

```javascript
> FT.SEARCH idx:movie "@genre:{Drama}" RETURN 3 title release_year rating

1) (integer) 1
2) "movie:11003"
3) 1) "title"
   2) "The Godfather"
   3) "release_year"
   4) "1972"
   5) "rating"
   6) "9.2"
```

The syntax @field:{value} indicates that you are searching in a tag field. You can find more information about the [tag filter in the RediSearch documentation](https://redis.io/docs/interact/search-and-query/advanced-concepts/tags/).

## Update the database and query

So far, all the data you are querying was created before the index and indexed during the index creation. Let’s change things up by adding a new movie:

```javascript
> HSET "movie:11005" title "Star Wars: Episode VI - Return of the Jedi"  plot "The Rebels destroy the Empire's Death Star." release_year 1983 genre "Action" rating 8.3 votes 906260 

(integer) 6
```

You can reuse the earlier queries:

```javascript
> FT.SEARCH idx:movie "war" RETURN 3 title release_year rating

1) (integer) 2
2) "movie:11005"
3) 1) "title"
   2) "Star Wars: Episode VI - Return of the Jedi"
   3) "release_year"
   4) "1983"
   5) "rating"
   6) "8.3"
4) "movie:11002"
5) 1) "title"
   2) "Star Wars: Episode V - The Empire Strikes Back"
   3) "release_year"
   4) "1980"
   5) "rating"
   6) "8.7"
```

As you can see, the new movie has been automatically indexed.

Similarly, if you delete or expire a movie, the index will be automatically updated, as shown here:

```javascript
> EXPIRE "movie:11002" 15

(integer) 1
```

If you wait 15 seconds and run the search query, you will see that the movie has been removed from the index.

This is quite powerful when you want to do ephemeral search and let the database manage the expiration of the data and indexes. You can find more information about ephemeral search in our blog post laying out [The Case for Ephemeral Search](/blog/the-case-for-ephemeral-search/).

[Click here to view video](https://www.youtube.com/embed/DJewW_qhpyk)

## Where can I go from here?

This post has shared some of the basics of RediSearch, and shown how indexing data is transparent from your application code. This functionality is new in RediSearch 2.0, since in RediSearch 1.x developers had to specifically use the FT.ADD command to index the data.

In addition to the search and indexing functionality discussed in this blog post, RediSearch also includes powerful [data aggregation](/blog/getting-started-with-redisearch-2-0/) capabilities, which are covered in the RediSearch documentation, [tutorial](https://github.com/RediSearch/redisearch-getting-started), and [online course](https://university.redis.com/courses/ru201/).

The [tutorial](https://github.com/RediSearch/redisearch-getting-started) contains the same data, but with a bigger dataset and more sample queries and aggregation. It also contains an application that shows how to use RediSearch with programming languages such as Java, Python, and Node.js. To learn more, check out these additional resources:

- [RediSearch web page](https://redisearch.io)
- [RediSearch 2.0 Tutorial](https://github.com/RediSearch/redisearch-getting-started)
- [Rediscover Use Cases and Projects](/rediscover/projects/)
