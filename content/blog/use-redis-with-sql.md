---
title: "Use Redis with SQL"
linkTitle: "Use Redis with SQL"
url: "/blog/use-redis-with-sql/"
description: "Yes, you heard that right. Query Redis with SQL. No LLMs needed."
date: 2026-05-06
blogCategories:
- "Tech"
authors:
- "Nitin Kanukolanu"
- "Robert Shelton"
lastmod: 2026-05-06
hidden: true
---

*By Nitin Kanukolanu, Robert Shelton · Published 6 May 2026*

![Use Redis with SQL](/images/site-mirror/ee9a2aa0641e22180c118d2d3ae29bd78de3a790-1200x628.webp)

Yes, you heard that right. Query Redis with SQL. No LLMs needed.

Most data science teams already speak SQL fluently, and for many (including LLMs and agents), it’s still the most intuitive way to express queries. At the same time, teams often need the speed and flexibility of Redis at scale.

Luckily the Redis API already provides nearly all the primitives required to express rich, SQL-like queries against a single index, but translating between the two can be cumbersome.

To help close this gap, we released the [`sql-redis`](https://github.com/redis-developer/sql-redis) library to PyPi and added the [`SQLQuery`](https://github.com/redis/redis-vl-python/blob/main/docs/user_guide/12_sql_to_redis_queries.ipynb) class to [redisvl](https://github.com/redis/redis-vl-python) so you can run SQL-like queries at Redis speed.

## Quick start with RedisVL

Install:

```
pip install "redisvl[sql-redis]"

```

Setup index:

```python
from redisvl.index import SearchIndex
from redis import Redis

data = [
{
        'user': 'john',
        'age': 34,
        'job': 'software engineer',
        'region': 'us-west',
        'job_description': 'Designs, develops, and maintains software.'
	  'job_embedding': [0 * 768]
},
...
]

schema = {
    "index": {

        "name": "user_simple",
        "prefix": "user_simple_docs",
        "storage_type": "json",
    },
    "fields": [
        {"name": "user", "type": "tag"},
        {"name": "region", "type": "tag"},
        {"name": "job", "type": "tag"},
        {"name": "job_description", "type": "text"},
        {"name": "age", "type": "numeric"},
        {
            "name": "job_embedding",
            "type": "vector",
            "attrs": {
                "dims": 768,
                "distance_metric": "cosine",
                "algorithm": "flat",
                "datatype": "float32"
            }
        }
    ]
}


client = Redis.from_url("redis://localhost:6379")
index = SearchIndex.from_dict(schema, redis_client=client, validate_on_load=True)

index.create(overwrite=True, drop=True)
index.load(data)

```

Query:

```python
from redisvl.query import SQLQuery

sql_str = """
    SELECT user, region, job, age
    FROM user_simple
    WHERE age > 17
    """

sql_query = SQLQuery(sql_str)
results = index.query(sql_query)

```

Output:

```
[{'user': 'john',
  'region': 'us-west',
  'job': 'software engineer',
  'age': '34'},
 {'user': 'bill', 'region': 'us-central', 'job': 'engineer', 'age': '54'},
 {'user': 'mary', 'region': 'us-central', 'job': 'doctor', 'age': '24'},
 {'user': 'joe', 'region': 'us-east', 'job': 'dentist', 'age': '27'},
 {'user': 'stacy', 'region': 'us-west', 'job': 'project manager', 'age': '61'}]

```

## Under the hood

The `SQLQuery` class converts a sql-like statement such as:

```sql
SELECT user, region, job, age
FROM user_simple
WHERE age > 17

```

into an equivalent Redis query.

```
FT.SEARCH user_simple "@age:[(17 +inf] @region:{us\-west}" RETURN 4 user region job age DIALECT 2

```

Conveniently, you can preview the Redis query to be executed via the `.redis_query_string()` available on the `SQLQuery` class:

```python
sql_str = """
    SELECT user, region, job, age
    FROM user_simple
    WHERE age > 17 and region = 'us-west'
"""

sql_query = SQLQuery(sql_str)
redis_query = sql_query.redis_query_string(redis_url="redis://localhost:6379")
print("Resulting redis query: ", redis_query)
# FT.SEARCH user_simple "@age:[(17 +inf] @region:{us\-west}" RETURN 4 user region job age DIALECT 2

```

The `SQLQuery` class accomplishes this deterministically, without an LLM, with the help of [sqlglot](https://sqlglot.com/sqlglot.html) and the parser within `sql-redis`. Check out the [source code](https://github.com/redis-developer/sql-redis) for more details.

## More than simple selects

The core translation engine already handles aggregations, full-text search, geo queries, and async execution.

### Conditional operators

Natural language intent

```
Find all users in the user_simple dataset who are located in either the us-west or us-central region, and return their user, region, job, and age fields.

```

SQL

```sql
SELECT user, region, job, age
FROM user_simple
WHERE region = 'us-west' OR region = 'us-central'

```

Redis

```
FT.SEARCH user_simple "((@region:{us\-west})|(@region:{us\-central}))" RETURN 4 user region job age

```

### Vector search

Natural language intent

```
Find the users whose job embeddings are most similar to a given query vector, and return their user, job, job description, along with the similarity (distance) score, sorted from most similar to least similar.
  
```

SQL

```sql
SELECT user, job, job_description, cosine_distance(job_embedding, :vec) AS vector_distance
FROM user_simple
ORDER BY vector_distance ASC

```

Redis

```
FT.SEARCH user_simple "*=>[KNN 10 @job_embedding $vector AS vector_distance]" PARAMS 2 vector $vector DIALECT 2 RETURN 4 user job job_description vector_distance SORTBY vector_distance ASC

```

### Aggregations

Natural language intent

```
Group users by region, and for each region compute summary statistics on age—including total count, distinct count, minimum, maximum, average, standard deviation, first observed value, full list of ages, and the 99th percentile.

```

SQL

```sql
SELECT
   user,
   COUNT(age) AS count_age,
   COUNT_DISTINCT(age) AS count_distinct_age,
   MIN(age) AS min_age,
   MAX(age) AS max_age,
   AVG(age) AS avg_age,
   STDEV(age) AS std_age,
   FIRST_VALUE(age) AS first_value_age,
   ARRAY_AGG(age) AS to_list_age,
   QUANTILE(age, 0.99) AS quantile_age
FROM user_simple
GROUP BY region

```

Redis

```
FT.AGGREGATE user_simple "*" LOAD 3 @age @region @user GROUPBY 1 @region REDUCE COUNT 0 AS count_age REDUCE COUNT_DISTINCT 1 @age AS count_distinct_age REDUCE MIN 1 @age AS min_age REDUCE MAX 1 @age AS max_age REDUCE AVG 1 @age AS avg_age REDUCE STDDEV 1 @age AS std_age REDUCE FIRST_VALUE 1 @age AS first_value_age REDUCE TOLIST 1 @age AS to_list_age REDUCE QUANTILE 2 @age 0.99 AS quantile_age

```

Check out the redisvl [user guide](https://docs.redisvl.com/en/latest/user_guide/12_sql_to_redis_queries.html) for a full demo of queries available.

## To wrap things up

- You can now query Redis indexes with familiar SQL syntax
- Under the hood, `sql-redis` parses your SQL into an AST (Abstract Syntax Tree), checks it against your index schema, and emits the right FT.SEARCH or FT.AGGREGATE command.
- Beyond basic filters, it already supports aggregations, full-text search, geo queries, date functions, parameterized queries, and async execution.
- It runs fast. Schema metadata is cached so translation overhead stays in the low milliseconds.

### Try it out now

```
pip install "redisvl[sql-redis]"

```
