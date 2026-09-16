---
title: "How to Search Movies Database with Redis"
linkTitle: "How to Search Movies Database with Redis"
url: "/tutorials/howtos-search-movies-database-with-redis/"
description: "In this tutorial, you'll learn how to use Redis Search to index and query a movies database. You'll start with basic data modeling, create search indexes, run queries, and work your way up to..."
group: "For developers"
date: 2026-02-25
lastmod: 2026-02-25
hidden: true
mirrored: true
---

*Published 25 February 2026*

> **TL;DR:**
>
> You can search data in Redis by creating a secondary index with [`FT.CREATE`](https://redis.io/docs/latest/commands/ft.create/) and querying it with [`FT.SEARCH`](https://redis.io/docs/latest/commands/ft.search/). Redis Search supports full-text search, numeric range filters, TAG exact-match filters, fuzzy matching, and aggregations — all running in-memory for sub-millisecond response times.

In this tutorial, you'll learn how to use Redis Search to index and query a movies database. You'll start with basic data modeling, create search indexes, run queries, and work your way up to advanced aggregations and a sample application.

### What you'll learn

- How to model data in Redis Hashes for search
- How to create a search index with `FT.CREATE`
- How to run full-text, numeric, and TAG queries with `FT.SEARCH`
- How to use fuzzy matching and negation in queries
- How to manage indexes (inspect, alter, drop)
- How to aggregate data with `FT.AGGREGATE` (grouping, sorting, filtering)
- How to create filtered indexes for specialized queries

## Prerequisites

Before starting, make sure you have Redis running. You can follow the [Redis quick start](/tutorials/howtos/quick-start/#setup-redis) guide to set up Redis using Docker, Redis Cloud, or other methods.

For this tutorial, the quickest way is to use Docker:

```bash
docker run -it --rm --name redis \
   -p 6379:6379 \
   redis:latest
```

> **Note:** The container will automatically be removed when it exits (`--rm` parameter).

---

## How should I model movie data in Redis?

### Sample Dataset

In this tutorial, you'll work with a simple dataset describing movies. A movie is represented by the following attributes:

- **`movie_id`**: The unique ID of the movie, internal to this database
- **`title`**: The title of the movie
- **`plot`**: A summary of the movie
- **`genre`**: The genre of the movie (single genre per movie for simplicity)
- **`release_year`**: The year the movie was released as a numerical value
- **`rating`**: A numeric value representing the public's rating for this movie
- **`votes`**: Number of votes
- **`poster`**: Link to the movie poster
- **`imdb_id`**: ID of the movie in the [IMDB](https://imdb.com) database

### Key Structure

A common way of defining keys in Redis is to use specific patterns. For this application, we'll use:

- `business_object:key`

For example:

- `movie:001` for the movie with the id 001
- `user:001` for the user with the id 001

### Data Structure

For movie information, we'll use a Redis [Hash](https://redis.io/docs/latest/develop/data-types/hashes/). A Redis Hash allows the application to structure all the movie attributes in individual fields, and Redis Search will index these fields based on the index definition.

---

## How do I insert movie data into Redis?

Let's add some movies to the database using `redis-cli` or [Redis Insight](https://redis.io/insight/).

Connect to your Redis instance and run the following commands:

```bash
HSET movie:11002 title "Star Wars: Episode V - The Empire Strikes Back" plot "After the Rebels are brutally overpowered by the Empire on the ice planet Hoth, Luke Skywalker begins Jedi training with Yoda, while his friends are pursued by Darth Vader and a bounty hunter named Boba Fett all over the galaxy." release_year 1980 genre "Action" rating 8.7 votes 1127635 imdb_id tt0080684

HSET movie:11003 title "The Godfather" plot "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son." release_year 1972 genre "Drama" rating 9.2 votes 1563839 imdb_id tt0068646

HSET movie:11004 title "Heat" plot "A group of professional bank robbers start to feel the heat from police when they unknowingly leave a clue at their latest heist." release_year 1995 genre "Thriller" rating 8.2 votes 559490 imdb_id tt0113277

HSET movie:11005 title "Star Wars: Episode VI - Return of the Jedi" genre "Action" votes 906260 rating 8.3 release_year 1983 plot "The Rebels dispatch to Endor to destroy the second Empire's Death Star." imdb_id tt0086190
```

Now you can retrieve information from the hash using the movie ID:

```bash
HMGET movie:11002 title rating
```

Output:

```bash
1) "Star Wars: Episode V - The Empire Strikes Back"
2) "8.7"
```

You can also increment the rating:

```bash
HINCRBYFLOAT movie:11002 rating 0.1
```

Output:

```bash
"8.8"
```

But how do you find movies by year of release, rating, or title? This is where Redis Search comes in.

---

## How do I create a search index in Redis?

Redis Search provides a simple and automatic way to create secondary indices on Redis Hashes. For background on indexing strategies in Redis, see the [Indexing and Querying guide](/tutorials/guides/indexing/).

![Diagram showing how Redis Search indexes Hash fields into a secondary index for full-text and numeric queries](/images/site-mirror/7e9c592ad77640349f2fff82c400c628832b7291-1027x508.webp)

When using Redis Search, you must first index the fields you want to query. Let's index:

- Title
- Release Year
- Rating
- Genre

### Creating the index with FT.CREATE

```bash
FT.CREATE idx:movie ON hash PREFIX 1 "movie:" SCHEMA title TEXT SORTABLE release_year NUMERIC SORTABLE rating NUMERIC SORTABLE genre TAG SORTABLE
```

Let's break down this command:

- **`FT.CREATE`**: Creates an index with the given spec
- **`idx:movie`**: The name of the index
- **`ON hash`**: The type of structure to be indexed
- **`PREFIX 1 "movie:"`**: Index all keys starting with `movie:`. You can specify multiple prefixes, e.g., `PREFIX 2 "movie:" "tv_show:"`
- **`SCHEMA ...`**: Defines the schema with [field types](https://redis.io/docs/latest/develop/interact/search-and-query/indexing/):
    - `TEXT`: Full-text searchable fields (tokenized and stemmed)
    - `NUMERIC`: Numeric fields for range queries
    - `TAG`: Exact match fields
    - `SORTABLE`: Enables sorting on the field

Inspect the index:

```bash
FT.INFO idx:movie
```

> **Warning: Do not index all fields**
>
> Indexes take space in memory and must be updated when the primary data is updated. Create indexes carefully and only for fields you need to query.

---

## How do I query data with FT.SEARCH?

Now let's run some queries using [FT.SEARCH](https://redis.io/docs/latest/commands/ft.search/).

### Text Search

Find all movies containing "war":

```bash
FT.SEARCH idx:movie "war"
```

Output:

```bash
1) (integer) 2
2) "movie:11005"
3)  1) "title"
    2) "Star Wars: Episode VI - Return of the Jedi"
    ...
4) "movie:11002"
5)  1) "title"
    2) "Star Wars: Episode V - The Empire Strikes Back"
    ...
```

The movie "Star Wars" is found even though you searched for "war" because the title is indexed as TEXT, meaning it's [tokenized](https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/escaping/) and [stemmed](https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/stemming/).

### Limiting Returned Fields

Use `RETURN` to specify which fields to return:

```bash
FT.SEARCH idx:movie "war" RETURN 2 title release_year
```

Output:

```bash
1) (integer) 2
2) "movie:11005"
3) 1) "title"
   2) "Star Wars: Episode VI - Return of the Jedi"
   3) "release_year"
   4) "1983"
4) "movie:11002"
5) 1) "title"
   2) "Star Wars: Episode V - The Empire Strikes Back"
   3) "release_year"
   4) "1980"
```

### Field-Specific Search

Use `@field:` syntax to search specific fields:

```bash
FT.SEARCH idx:movie "@title:war" RETURN 2 title release_year
```

### Negation

Use `-` to exclude terms:

```bash
FT.SEARCH idx:movie "war -jedi" RETURN 2 title release_year
```

Output:

```bash
1) (integer) 1
2) "movie:11002"
3) 1) "title"
   2) "Star Wars: Episode V - The Empire Strikes Back"
   3) "release_year"
   4) "1980"
```

### Fuzzy Matching

Use `%` for [fuzzy matching](https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/query_syntax/#fuzzy-matching) based on [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance):

```bash
FT.SEARCH idx:movie "%gdfather%" RETURN 2 title release_year
```

Output:

```bash
1) (integer) 1
2) "movie:11003"
3) 1) "title"
   2) "The Godfather"
   3) "release_year"
   4) "1972"
```

### TAG Filters

The `genre` field is indexed as a TAG for exact match queries:

```bash
FT.SEARCH idx:movie "@genre:{Thriller}" RETURN 2 title release_year
```

Output:

```bash
1) (integer) 1
2) "movie:11004"
3) 1) "title"
   2) "Heat"
   3) "release_year"
   4) "1995"
```

Multiple TAG values (OR):

```bash
FT.SEARCH idx:movie "@genre:{Thriller|Action}" RETURN 2 title release_year
```

Learn more about [Tag filters](https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/tags/).

### Combined Conditions

Thriller or Action movies without "Jedi" in the title:

```bash
FT.SEARCH idx:movie "@genre:{Thriller|Action} @title:-jedi" RETURN 2 title release_year
```

### Numeric Range Queries

Movies released between 1970 and 1980:

Using FILTER parameter:

```bash
FT.SEARCH idx:movie * FILTER release_year 1970 1980 RETURN 2 title release_year
```

Using query string:

```bash
FT.SEARCH idx:movie "@release_year:[1970 1980]" RETURN 2 title release_year
```

Exclude a value with `(`:

```bash
FT.SEARCH idx:movie "@release_year:[1970 (1980]" RETURN 2 title release_year
```

---

## How do I manage Redis Search indexes?

### List All Indexes

```bash
FT._LIST
```

Output:

```bash
1) "idx:movie"
```

### Inspect an Index

```bash
FT.INFO "idx:movie"
```

This returns detailed information about the index including field definitions and document count.

### Add Fields to an Index

Use `FT.ALTER` to add new fields:

```bash
FT.ALTER idx:movie SCHEMA ADD plot TEXT WEIGHT 0.5
```

The `WEIGHT` parameter declares the importance of this field when calculating result accuracy (default is 1). Here, the plot is weighted less than the title.

Now you can search the plot field:

```bash
FT.SEARCH idx:movie "empire @genre:{Action}" RETURN 2 title plot
```

### Drop an Index

```bash
FT.DROPINDEX idx:movie
```

> **Note:** Dropping an index does not delete the underlying data. The movie hashes remain in the database.

Verify the data still exists:

```bash
SCAN 0 MATCH movie:*
```

Output:

```bash
1) "0"
2) 1) "movie:11002"
   2) "movie:11004"
   3) "movie:11003"
   4) "movie:11005"
```

> **Tip:** Add the `DD` parameter to `FT.DROPINDEX` to also delete the indexed documents.

---

## How does Redis Search handle document changes?

Redis Search automatically indexes new, updated, and deleted documents.

### Insert and Auto-Index

```bash
FT.SEARCH idx:movie "*" LIMIT 0 0
```

Output: `1) (integer) 4`

```bash
HSET movie:11033 title "Tomorrow Never Dies" plot "James Bond sets out to stop a media mogul's plan to induce war between China and the U.K in order to obtain exclusive global media coverage." release_year 1997 genre "Action" rating 6.5 votes 177732 imdb_id tt0120347
```

```bash
FT.SEARCH idx:movie "*" LIMIT 0 0
```

Output: `1) (integer) 5`

The new movie is automatically indexed:

```bash
FT.SEARCH idx:movie "never" RETURN 2 title release_year
```

### Update Documents

```bash
HSET movie:11033 title "Tomorrow Never Dies - 007"

FT.SEARCH idx:movie "007" RETURN 2 title release_year
```

Output:

```bash
1) (integer) 1
2) "movie:11033"
3) 1) "title"
   2) "Tomorrow Never Dies - 007"
   3) "release_year"
   4) "1997"
```

### Document Expiration

When a document expires (TTL), it's automatically removed from the index:

```bash
EXPIRE "movie:11033" 20
```

After 20 seconds:

```bash
FT.SEARCH idx:movie "007" RETURN 2 title release_year
```

Output: `1) (integer) 0`

> **Tip:** This is useful for "[Ephemeral Search](https://redis.io/blog/the-case-for-ephemeral-search/)" use cases like caching, session content, etc.

---

## How do I import a full movies dataset?

Now let's import a larger dataset to explore more advanced features.

### Dataset Overview

We'll import three datasets:

| Dataset  | Records | Description                                        |
| -------- | ------- | -------------------------------------------------- |
| Movies   | 922     | Movie hashes with title, plot, genre, rating, etc. |
| Theaters | 117     | New York theater locations with geospatial data    |
| Users    | 5,996   | User profiles with demographics and login data     |

- **Movie fields:** `movie:id` (key), `title`, `plot`, `genre`, `release_year`, `rating`, `votes`, `poster`, `imdb_id`
- **Theater fields:** `theater:id` (key), `name`, `address`, `city`, `zip`, `phone`, `url`, `location` (longitude,latitude for geo queries)
- **User fields:** `user:id` (key), `first_name`, `last_name`, `email`, `gender`, `country`, `country_code`, `city`, `longitude`, `latitude`, `last_login` (EPOC timestamp), `ip_address`

### Import the Data

First, flush the database:

```bash
FLUSHALL
```

Then import using `redis-cli`:

```bash
curl -s https://raw.githubusercontent.com/RediSearch/redisearch-getting-started/master/sample-app/redisearch-docker/dataset/import_movies.redis | redis-cli -h localhost -p 6379 --pipe

curl -s https://raw.githubusercontent.com/RediSearch/redisearch-getting-started/master/sample-app/redisearch-docker/dataset/import_theaters.redis | redis-cli -h localhost -p 6379 --pipe

curl -s https://raw.githubusercontent.com/RediSearch/redisearch-getting-started/master/sample-app/redisearch-docker/dataset/import_users.redis | redis-cli -h localhost -p 6379 --pipe
```

Verify the import:

```bash
HMGET "movie:343" title release_year genre
```

Output:

```bash
1) "Spider-Man"
2) "2002"
3) "Action"
```

```bash
HMGET "theater:20" name location
```

Output:

```bash
1) "Broadway Theatre"
2) "-73.98335054631019,40.763270202723625"
```

```bash
HMGET "user:343" first_name last_name last_login
```

Output:

```bash
1) "Umeko"
2) "Castagno"
3) "1574769122"
```

Use `DBSIZE` to see the total number of keys.

### Create Production Indexes

Movies Index:

```bash
FT.CREATE idx:movie ON hash PREFIX 1 "movie:" SCHEMA title TEXT SORTABLE plot TEXT WEIGHT 0.5 release_year NUMERIC SORTABLE rating NUMERIC SORTABLE votes NUMERIC SORTABLE genre TAG SORTABLE
```

Verify with `FT.INFO "idx:movie"` - should show 922 documents.

Theaters Index (with Geospatial):

```bash
FT.CREATE idx:theater ON hash PREFIX 1 "theater:" SCHEMA name TEXT SORTABLE location GEO
```

Verify with `FT.INFO "idx:theater"` - should show 117 documents.

Users Index:

```bash
FT.CREATE idx:user ON hash PREFIX 1 "user:" SCHEMA gender TAG country TAG SORTABLE last_login NUMERIC SORTABLE location GEO
```

---

## How do I write advanced search queries?

With the full dataset, let's explore more advanced query techniques.

### Conditions

Find all movies containing "heat" (in title or plot):

```bash
FT.SEARCH "idx:movie" "heat" RETURN 2 title plot
```

This returns 4 movies because:

- It searches all TEXT fields (title and plot)
- It finds related words like "heated" due to stemming
- Results are sorted by score (title has weight 1.0, plot has 0.5)

Search only in title:

```bash
FT.SEARCH "idx:movie" "@title:heat" RETURN 2 title plot
```

Returns only 2 movies.

Title contains "heat" but NOT "california":

```bash
FT.SEARCH "idx:movie" "@title:(heat -california)" RETURN 2 title plot
```

Returns 1 movie ("Heat").

> **Note:** Without parentheses, `-california` applies to ALL text fields:

```bash
# Searches for -woman only in title
FT.SEARCH "idx:movie" "@title:(heat -woman)" RETURN 2 title plot

# Searches for -woman in ALL text fields
FT.SEARCH "idx:movie" "@title:heat -woman" RETURN 2 title plot
```

---

## How do I aggregate data with FT.AGGREGATE?

Beyond retrieving documents, you often need to aggregate data. Redis provides [FT.AGGREGATE](https://redis.io/docs/latest/commands/ft.aggregate/) for this.

### Group By & Sort By

Number of movies by year:

```bash
FT.AGGREGATE "idx:movie" "*" GROUPBY 1 @release_year REDUCE COUNT 0 AS nb_of_movies
```

Number of movies by year (descending):

```bash
FT.AGGREGATE "idx:movie" "*" GROUPBY 1 @release_year REDUCE COUNT 0 AS nb_of_movies SORTBY 2 @release_year DESC
```

Movies by genre with total votes and average rating:

```bash
FT.AGGREGATE idx:movie "*" GROUPBY 1 @genre REDUCE COUNT 0 AS nb_of_movies REDUCE SUM 1 votes AS nb_of_votes REDUCE AVG 1 rating AS avg_rating SORTBY 4 @avg_rating DESC @nb_of_votes DESC
```

Count female users by country:

```bash
FT.AGGREGATE idx:user "@gender:{female}" GROUPBY 1 @country REDUCE COUNT 0 AS nb_of_users SORTBY 2 @nb_of_users DESC
```

### Apply Functions

Number of logins per year and month:

```bash
FT.AGGREGATE idx:user * APPLY year(@last_login) AS year APPLY "monthofyear(@last_login) + 1" AS month GROUPBY 2 @year @month REDUCE count 0 AS num_login SORTBY 4 @year ASC @month ASC
```

Logins by day of week:

```bash
FT.AGGREGATE idx:user * APPLY "dayofweek(@last_login) + 1" AS dayofweek GROUPBY 1 @dayofweek REDUCE count 0 AS num_login SORTBY 2 @dayofweek ASC
```

### Filter Expressions

Use [FILTER](https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/aggregations/#filter-expressions) to filter results after aggregation.

Female users by country (except China, with more than 100 users):

```bash
FT.AGGREGATE idx:user "@gender:{female}" GROUPBY 1 @country REDUCE COUNT 0 AS nb_of_users FILTER "@country!='china' && @nb_of_users > 100" SORTBY 2 @nb_of_users DESC
```

Logins per month for year 2020:

```bash
FT.AGGREGATE idx:user * APPLY year(@last_login) AS year APPLY "monthofyear(@last_login) + 1" AS month GROUPBY 2 @year @month REDUCE count 0 AS num_login FILTER "@year==2020" SORTBY 2 @month ASC
```

---

## How do I create filtered indexes?

You can create indexes with FILTER expressions to index only a subset of documents.

Create an index for Drama movies from the 1990s:

```bash
FT.CREATE idx:drama ON Hash PREFIX 1 "movie:" FILTER "@genre=='Drama' && @release_year>=1990 && @release_year<2000" SCHEMA title TEXT SORTABLE release_year NUMERIC SORTABLE
```

Run `FT.INFO idx:drama` to see the index definition and statistics.

> **Notes:**
>
> - The `PREFIX` is required even when using FILTER
> - This index is useful for specialized queries but may be redundant with `idx:movie`

Verify both indexes return the same count:

```bash
# On idx:drama
FT.SEARCH idx:drama "@release_year:[1990 (2000]" LIMIT 0 0
```

Output: `1) (integer) 24`

```bash
# On idx:movie
FT.SEARCH idx:movie "@genre:{Drama} @release_year:[1990 (2000]" LIMIT 0 0
```

Output: `1) (integer) 24`

---

## How do I build an application with Redis Search?

Now let's run a complete sample application that demonstrates Redis Search in action.

### Clone the Repository

```bash
git clone https://github.com/RediSearch/redisearch-getting-started.git
cd redisearch-getting-started
```

### Run with Docker Compose

```bash
cd sample-app
docker-compose up --force-recreate --build
```

This starts:

1. **Redis** on port 6380 with all data and indexes
2. **Java REST Service** on port 8085
3. **Node REST Service** on port 8086
4. **Python REST Service** on port 8087
5. **Frontend** on port 8084

### Access the Application

- **Frontend**: http://localhost:8084
- **Java API**: http://localhost:8085/api/1.0/movies/search?q=star&offset=0&limit=10
- **Node API**: http://localhost:8086/api/1.0/movies/search?q=star&offset=0&limit=10
- **Python API**: http://localhost:8087/api/1.0/movies/search?q=star&offset=0&limit=10

### Cleanup

Stop and remove all containers:

```bash
docker-compose down -v --rmi local --remove-orphans
```

---

## Next steps

Now that you know how to search structured data with Redis, explore these related topics:

- [Indexing and Querying patterns in Redis](/tutorials/guides/indexing/) — learn about indexing strategies using core data structures
- [Vector Similarity Search with Redis](/tutorials/howtos/solutions/vector/getting-started-vector/) — go beyond full-text search with vector embeddings
- [Semantic Text Search with LangChain and Redis](/tutorials/howtos/solutions/vector/semantic-text-search/) — combine LLMs and Redis for semantic search
- [Getting started with vector sets](/tutorials/howtos/vector-sets-basics/) — learn the basics of Redis vector sets for similarity search

## References

- [FT.CREATE command reference](https://redis.io/docs/latest/commands/ft.create/)
- [FT.SEARCH command reference](https://redis.io/docs/latest/commands/ft.search/)
- [FT.AGGREGATE command reference](https://redis.io/docs/latest/commands/ft.aggregate/)
- [Query syntax documentation](https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/query_syntax/)
- [Aggregation documentation](https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/aggregations/)
- [Indexing guide](https://redis.io/docs/latest/develop/interact/search-and-query/indexing/)
