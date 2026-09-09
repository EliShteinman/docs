---
title: "Redis quick start guide"
linkTitle: "Redis quick start guide"
url: "/tutorials/howtos/quick-start/"
description: "Welcome to the getting started for the official Redis Developer Hub!"
aliases:
- "/tutorials/howtos-quick-start/"
date: 2026-02-25
lastmod: 2026-09-01
hidden: true
---

*Published 25 February 2026 · updated 1 September 2026*

> **TL;DR:**
>
> Redis is an open-source, in-memory data store used as a database, cache, and message broker. To get started, install Redis via Docker or Redis Cloud, connect with `redis-cli` or a client library in your language of choice, and begin storing and retrieving data with simple `SET` and `GET` commands. Then go further based on what you want to do.

### What you'll learn

- How to install Redis (Docker, Cloud, or native)
- How to connect to Redis via the CLI or Redis Insight
- How to perform basic CRUD operations (SET, GET, DEL)
- How to work with Redis JSON documents
- How to create indexes and search your data
- How to use probabilistic data structures
- How to store and query time-series data

---

Welcome to the getting started for the official Redis Developer Hub!

If you are new to Redis, we recommend starting with the ["Get started with Redis" course on Redis University](https://university.redis.io/learningpath/14q8m6gilfwltm?tab=details). It is an introductory course, perfect for developers new to Redis. In this course, you'll learn about the data structures in Redis, and you'll see how to practically apply them in the real world.

If you have questions related to Redis, come join the [Redis Discord server](https://discord.gg/redis). Our Discord server is a place where you can learn, share, and collaborate about anything and everything Redis. Connect with users from the community and Redis University. Get your questions answered and learn cool new tips and tricks! Watch for notifications of the latest content from Redis and the community. And share your own content with the community.

## How do I install Redis?

There are essentially two ways you can use Redis:

### Redis Cloud

- **Cloud Redis**: A hosted and serverless Redis database-as-a-service (DBaaS). The fastest way to deploy Redis Cloud via Amazon AWS, Google Cloud Platform, or Microsoft Azure.
    - [Free Sign-up](https://redis.io/try-free/)
    - [Videos](https://www.youtube.com/playlist?list=PL83Wfqi-zYZG6uGxBagsbqjpsi2XBEj1K)
- **On-prem/local Redis**: Self-managed Redis using your own server and any operating system (Mac OS, Windows, or Linux).

If you choose to use local Redis we strongly recommend using Docker. If you choose not to use Docker, use the following instructions based on your OS:

### Docker

The `docker run` command below exposes redis-server on port 6379 and Redis Insight on port 8001. You can use Redis Insight by pointing your browser to `http://localhost:8001`.

```bash
# install
$ docker run -d --name redis -p 6379:6379 -p 8001:8001 redis:latest
```

You can use `redis-cli` to connect to the server at `localhost:6379`. If you don't have `redis-cli` installed locally, you can run it from the Docker container like below:

```bash
# connect
$ docker exec -it redis redis-cli
```

### Older methods

If you do not want to use Redis Cloud or Docker, see the [install archive](https://redis.io/docs/latest/operate/oss_and_stack/install/archive/) for how to run Redis natively.

## How do I connect to Redis?

### CLI

- Connect to Redis using CLI or [**Redis Insight**](https://redis.io/downloads/#Redis_Insight) (a GUI tool to visualize data and run commands, see below)

![Redis Insight GUI showing a connected Redis database with key browser](/images/site-mirror/bd01a8ef9031b45714908a30b4ea2b9e93c5ed56-806x486.svg)

```bash
# syntax 1 : connect using host & port, followed by password
$ redis-cli -h host -p port
> AUTH password
OK

# example 1
$ redis-cli -h redis15.localnet.org -p 6390
> AUTH myUnguessablePassword
OK

# syntax 2 : connect using uri
$ redis-cli -u redis://user:password@host:port/dbnum

# example 2
$ redis-cli -u redis://LJenkins:p%40ssw0rd@redis-16379.hosted.com:16379/0
```

- Basic CLI / Redis Insight workbench commands

```bash
# syntax : Check specific keys
> KEYS pattern

# example
> KEYS *

#------------
# syntax : Check number of keys in database
> DBSIZE

#------------
# syntax : set a key value
> SET key value EX expirySeconds

# example
> SET company redis EX 60

#------------
# syntax : get value by key
> GET key

# example
> GET company

#------------
# syntax : delete keys
> DEL key1 key2 key3 ... keyN

# example
> DEL company

#------------
# syntax : Check if key exists
> EXISTS key1

# example
> EXISTS company

#------------
# syntax : set expiry to key
> EXPIRE key seconds

# example
> EXPIRE lastname 60

#------------
# syntax : remove expiry from key
> PERSIST key

# example
> PERSIST lastname

#------------
# syntax : find (remaining) time to live of a key
> TTL key

# example
> TTL lastname

#------------
# syntax : increment a number
> INCR key

# example
> INCR counter

#------------
# syntax : decrement a number
> DECR key

# example
> DECR counter
```

- Detailed [CLI instructions](https://redis.io/docs/latest/develop/tools/cli/)
- [Redis commands](https://redis.io/docs/latest/commands/)

### Javascript

```bash
# install redis in the project
npm install redis --save
```

```js
//create client & connect to redis

import { createClient } from 'redis';

const client = createClient({
    //redis[s]://[[username][:password]@][host][:port][/db-number]
    url: 'redis://alice:foobared@awesome.redis.server:6380',
});

client.on('error', (err) => console.log('Redis Client Error', err));

await client.connect();
```

```js
// Check specific keys
const pattern = '*';
await client.keys(pattern);

//------------
// Check number of keys in database
await client.dbsize();

//------------
// set key value
await client.set('key', 'value');
await client.set('key', 'value', {
    EX: 10,
    NX: true,
});

//------------
// get value by key
const value = await client.get('key');

//------------
//syntax : delete keys
await client.del('key');
const keyArr = ['key1', 'key2', 'key3'];
await client.del(...keyArr);

//------------
// Check if key exists
await client.exists('key');

//------------
// set expiry to key
const expireInSeconds = 30;
await client.expire('key', expireInSeconds);

//------------
// remove expiry from key
await client.persist('key');

//------------
// find (remaining) time to live of a key
await client.ttl('key');

//------------
// increment a number
await client.incr('key');

//------------
// decrement a number
await client.decr('key');

//------------
// use the method below to execute commands directly
await client.sendCommand(['SET', 'key', 'value']);
```

```js
//graceful disconnecting
await client.quit();

//forceful disconnecting
await client.disconnect();
```

- See the [node-redis Github repo](https://github.com/redis/node-redis) for more information
- For a deeper dive, see [Getting Started with Node and Redis](/tutorials/develop/node/gettingstarted/)

### Python

```bash
# install redis in the project
pip install redis
```

```python
import redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)

# Check specific keys
r.keys('*')

#------------
# Check number of keys in database
r.dbsize()

#------------
# set key value
r.set('key', 'value')
r.set('key', 'value', ex=10, nx=True)

#------------
# get value by key
value = r.get('key')

#------------
# syntax : delete keys
r.delete('key')
r.delete('key1', 'key2', 'key3')

#------------
# Check if key exists
r.exists('key')

#------------
# set expiry to key
expireInSeconds = 30
r.expire('key', expireInSeconds)

#------------
# remove expiry from key
r.persist('key')

#------------
# find (remaining) time to live of a key
r.ttl('key')

#------------
# increment a number
r.incr('key')

#------------
# decrement a number
r.decr('key')

#------------
# use the method below to execute commands directly
r.execute_command('SET', 'key', 'value')
```

- See the [redis-py Github repo](https://github.com/redis/redis-py) for more information
- For a deeper dive, see [Getting Started with Redis OM for Python](/tutorials/develop/python/redis-om/) or [Using Redis with FastAPI](/tutorials/develop/python/fastapi/)

### C# / .NET

The .NET Community has built many [client libraries](https://redis.io/clients#c-sharp) to help handle requests to Redis Server. In this guide, we'll mostly be concerned with using the [StackExchange.Redis](https://github.com/StackExchange/StackExchange.Redis) client library. As the name implies the StackExchange client is developed by StackExchange for use on popular websites like [StackOverflow](https://stackoverflow.com/).

```bash
# install redis in the project
dotnet add package StackExchange.Redis
```

```csharp
// Impport the required namespace
using StackExchange.Redis;

// Initialize the connection
static readonly ConnectionMultiplexer _redis = ConnectionMultiplexer.Connect("localhost:6379");
```

```csharp
var redis = _redis.GetDatabase();

// Check specific keys
var server = _redis.GetServer(_redis.GetEndPoints()[0]);
server.Keys(pattern: "*");

//------------
// Check number of keys in database
server.DatabaseSize();

//------------
// set key value
redis.StringSet("key", "value");
redis.StringSet("key", "value", expiry: TimeSpan.FromSeconds(10), when: When.NotExists);

//------------
// get value by key
var value = redis.StringGet("key");

//------------
// syntax : delete keys
redis.KeyDelete("key");
redis.KeyDelete(new RedisKey[] { "key1", "key2", "key3"});

//------------
// Check if key exists
redis.KeyExists("key");

//------------
// set expiry to key
redis.KeyExpire("key", DateTime.Now.AddSeconds(30));

//------------
// remove expiry from key
redis.KeyPersist("key");

//------------
// find (remaining) time to live of a key
redis.KeyTimeToLive("key");

//------------
// increment a number
redis.StringIncrement("key");

//------------
// decrement a number
redis.StringDecrement("key");

//------------
// use the method below to execute commands directly
redis.Execute("SET", "key", "value");
```

- See the [StackExchange.Redis Github repo](https://github.com/StackExchange/StackExchange.Redis) for more information
- For a deeper dive, see [Using Redis OM .NET](/tutorials/redis-om-dotnet-getting-started/)

## How do I use Redis JSON and query data?

### CLI

Redis supports JSON.

```bash
# syntax : set an object value to a key
> JSON.SET objKey $ value

# example
> JSON.SET person $ '{"name":"Leonard Cohen","dob":1478476800,"isActive": true, "hobbies":["music", "cricket"]}'

#------------
# syntax : get object value of a key
> JSON.GET objKey $

# example
> JSON.GET person $

#------------
# syntax : find object key length
> JSON.OBJLEN objKey $

# example
> JSON.OBJLEN person $

#------------
# syntax : find object keys
> JSON.OBJKEYS objKey $

# example
> JSON.OBJKEYS person $

#------------
# syntax : update nested property
> JSON.SET objKey $.prop value

# example
> JSON.SET person $.name '"Alex"'

#------------
# syntax : update nested array
> JSON.SET objKey $.arrayProp fullValue
> JSON.SET objKey $.arrayProp[index] value

# example
> JSON.SET person $.hobbies '["music", "cricket"]'
> JSON.SET person $.hobbies[1] '"dance"'

#------------
# syntax : remove nested array item by index
> JSON.ARRPOP objKey $.arrayProp index

# example
> JSON.ARRPOP person $.hobbies 1
```

More details can be found in the [Redis docs](https://redis.io/docs/latest/develop/data-types/json/)

Redis has a query and indexing engine, providing secondary indexing, full-text search and aggregations capabilities.

- We have to create index on schema to be able to search on its data

```bash
# syntax
> FT.CREATE {index_name} ON JSON PREFIX {count} {prefix} SCHEMA {json_path} AS {attribute} {type}
# NOTE: attribute = logical name,  json_path = JSONPath expressions

# example
> FT.CREATE userIdx ON JSON PREFIX 1 users: SCHEMA $.user.name AS name TEXT $.user.hobbies AS hobbies TAG $.user.age as age NUMERIC
# NOTE: You can search by any attribute mentioned in the above index for keys that start with users: (e.g. users:1).
```

- More details on [indexing JSON](https://redis.io/docs/latest/develop/data-types/json/indexing_json/)

Once index is created, any pre-existing/ new/ modified JSON document is automatically indexed.

```json
//sample json document
{
    "user": {
        "name": "John Smith",
        "hobbies": "foo,bar",
        "age": 23
    }
}
```

```bash
# adding JSON document
> JSON.SET myDoc $ '{"user":{"name":"John Smith","hobbies":"foo,bar","age":23}}'
```

- Search

```bash
# search all user documents with name 'John'
> FT.SEARCH userIdx '@name:(John)'
1) (integer) 1
2) "myDoc"
3) 1) "$"
   2)  {"user":{"name":"John Smith","hobbies":"foo,bar","age":23}}"
```

- Search & project required fields

```bash
# search documents with name 'John' & project only age field
> FT.SEARCH userIdx '@name:(John)' RETURN 1 $.user.age
1) (integer) 1
2) "myDoc"
3) 1) "$.user.age"
   2) "23"
```

```bash
# project multiple fields
> FT.SEARCH userIdx '@name:(John)' RETURN 2 $.user.age $.user.name
1) (integer) 1
2) "myDoc"
3) 1) "$.user.age"
   2) "23"
   3) "$.user.name"
   4) "John Smith"

#------------
# project with alias name
> FT.SEARCH userIdx '@name:(John)' RETURN 3 $.user.age AS userAge

1) (integer) 1
2) "myDoc"
3) 1) "userAge"
   2) "23"
#------------

# multi field query
> FT.SEARCH userIdx '@name:(John) @hobbies:{foo | me} @age:[20 30]'
1) (integer) 1
2) "myDoc"
3) 1) "$"
   2)  {"user":{"name":"John Smith","hobbies":"foo,bar","age":23}}"
```

More details on [query syntax](https://redis.io/docs/latest/develop/data-types/json/indexing_json/)

- Drop index

```bash
> FT.DROPINDEX userIdx
```

1. [Redis and JSON explained (Revisited in 2022)](https://www.youtube.com/watch?v=I-ohlZXXaxs) video
2. [Redis University, Storing, Querying, and Indexing JSON at Speed](https://university.redis.io/learningpath/pdkbr7xdv3miym?tab=details)

### Javascript

The following example uses [Redis OM Node](https://github.com/redis/redis-om-node), but you can also use [Node Redis](https://github.com/redis/node-redis), [IO Redis](https://github.com/luin/ioredis), or any other supported [client](https://redis.io/resources/clients/)

```bash
# install RedisOM in the project
npm install redis-om --save
```

- create RedisOM Client & connect to redis

```js
//client.js file

import { Client } from 'redis-om';

// pulls the Redis URL from .env
const url = process.env.REDIS_URL;

const client = new Client();
await client.open(url);

export default client;
```

- Create Entity, Schema & Repository

```js
//person.js file

import { Entity, Schema } from 'redis-om';
import client from './client.js';

class Person extends Entity {}

const personSchema = new Schema(Person, {
    firstName: { type: 'string' },
    lastName: { type: 'string' },
    age: { type: 'number' },
    verified: { type: 'boolean' },
    location: { type: 'point' },
    locationUpdated: { type: 'date' },
    skills: { type: 'string[]' },
    personalStatement: { type: 'text' },
});

export const personRepository = client.fetchRepository(personSchema);

//creating index to make person schema searchable
await personRepository.createIndex();
```

```js
import { Router } from 'express';
import { personRepository } from 'person.js';
```

- Insert example

```js
const input = {
    firstName: 'Rupert',
    lastName: 'Holmes',
    age: 75,
    verified: false,
    location: {
        longitude: 45.678,
        latitude: 45.678,
    },
    locationUpdated: '2022-03-01T12:34:56.123Z',
    skills: ['singing', 'songwriting', 'playwriting'],
    personalStatement: 'I like piña coladas and walks in the rain',
};
let person = await personRepository.createAndSave(input);
```

- Read example

```js
const id = person.entityId;
person = await personRepository.fetch(id);
```

- Update example

```js
person = await personRepository.fetch(id);

person.firstName = 'Alex';

//null to remove that field
person.lastName = null;

await personRepository.save(person);
```

- Update location sample

```js
const longitude = 45.678;
const latitude = 45.678;
const locationUpdated = new Date();

const person = await personRepository.fetch(id);
person.location = { longitude, latitude };
person.locationUpdated = locationUpdated;
await personRepository.save(person);
```

- Search examples

```js
// Get all person records
const queryBuilder = personRepository.search();
const people = await queryBuilder.return.all();

// Multiple AND conditions example
const queryBuilder = personRepository
    .search()
    .where('verified')
    .eq(true) // ==
    .and('age')
    .gte(21) // >=
    .and('lastName')
    .eq(lastName);
//console.log(queryBuilder.query);
const people = await queryBuilder.return.all();

// Multiple OR conditions example
const queryBuilder = personRepository
    .search()
    .where('verified')
    .eq(true)
    .or((search) => search.where('age').gte(21).and('lastName').eq(lastName))
    .sortAscending('age');
const people = await queryBuilder.return.all();
```

- Delete example

```js
await personRepository.remove(id);
```

- [Redis OM Github repo](https://github.com/redis/redis-om-node)
- [Getting started video](https://www.youtube.com/watch?v=KUfufrwpBkM)
- [Getting started Source code](https://github.com/redis-developer/express-redis-om-workshop)

### Python

The following example uses [Redis OM Python](https://github.com/redis/redis-om-python), but you can also use [redis-py](https://github.com/redis/redis-py) or any other supported [client](https://redis.io/resources/clients/)

```bash
# install Redis OM in the project
pip install redis-om
```

Create a JSON model

```python
import datetime
import dateutil.parser
from typing import List, Optional

from redis_om import (
    EmbeddedJsonModel,
    JsonModel,
    Field,
    Migrator,
)

class Point(EmbeddedJsonModel):
    longitude: float = Field(index=True)
    latitude: float = Field(index=True)

class Person(JsonModel):
    first_name: str = Field(index=True)
    last_name: Optional[str] = Field(index=True)
    age: int = Field(index=True)
    verified: bool
    location: Point
    location_updated: datetime.datetime = Field(index=True)
    skills: List[str]
    personal_statement: str = Field(index=True, full_text_search=True)

# Before running queries, we need to run migrations to set up the
# indexes that Redis OM will use. You can also use the `migrate`
# CLI tool for this!
Migrator().run()
```

- Insert example

```python
person = Person(**{
    "first_name": "Rupert",
    "last_name": "Holmes",
    "age": 75,
    "verified": False,
    "location": {
        "longitude": 45.678,
        "latitude": 45.678
    },
    "location_updated": dateutil.parser.isoparse("2022-03-01T12:34:56.123Z"),
    "skills":  ["singing", "songwriting", "playwriting"],
    "personal_statement": "I like piña coladas and walks in the rain"
}).save()
```

- Read example

```python
id = person.pk
person = Person.get(id)
```

- Update example

```python
person = Person.get(id)
person.first_name = "Alex"
person.last_name = None
person.save()
```

- Update embedded JSON example

```python
person = Person.get(id)
person.location = Point(longitude=44.678, latitude=44.678)
person.location_updated = datetime.datetime.now()
person.save()
```

- Search examples

```python
# Get all Person records

all = Person.find().all()

# Multiple AND conditions example

people = Person.find(
    (Person.age > 21) &
    (Person.first_name == "Alex")
).all()

# Multiple OR conditions example

people = Person.find(
    (Person.age > 75) |
    (Person.first_name == "Alex")
).all()

# Multiple AND + OR conditions example

people = Person.find(
    ((Person.age > 21) &
     (Person.first_name == "Alex")) &
    ((Person.age > 75) |
     (Person.first_name == "Alex"))
).all()
```

- Delete example

```python
Person.get(id).delete()
```

- [Redis OM Python Github repo](https://github.com/redis/redis-om-python)
- [Getting started video](https://www.youtube.com/watch?v=PPT1FElAS84)
- [Getting started source code](https://github.com/redis-developer/redis-om-python-flask-skeleton-app)

### C# / .NET

The following example uses [Redis OM .NET](https://github.com/redis/redis-om-dotnet), but you can also use any other supported [client](https://redis.io/resources/clients/). The examples also use the synchronous methods of Redis OM .NET, but it is recommended that you use the asynchronous methods in a production application.

```bash
# install Redis OM in the project
dotnet add package Redis.OM
```

- Create a JSON model

```csharp
using Redis.OM.Modeling;

namespace RedisApp.Model
{
    [Document(StorageType = StorageType.Json, Prefixes = new[] { "Person" })]
    public class Person
    {
        [RedisIdField]
        public string Id { get; set; }

        [Indexed]
        public string FirstName { get; set; }

        [Indexed]
        public string? LastName { get; set; }

        [Indexed(Sortable = true)]
        public int Age { get; set; }

        [Indexed]
        public bool Verified { get; set; }

        [Indexed]
        public GeoLoc Location { get; set; }

        [Indexed]
        public string[] Skills { get; set; } = Array.Empty<string>();

        [Searchable]
        public string PersonalStatement { get; set; }
    }
}
```

- Setup your main program

```csharp
using System;
using System.Linq;
using Redis.OM;
using Redis.OM.Modeling;
using RedisApp.Model;

namespace RedisApp
{
    class Program
    {
        static void Main(string[] args)
        {

        }
    }
}
```

The rest of the code will be inside of `Main`.

- Create your provider used to call into Redis

```csharp
var provider = new RedisConnectionProvider("redis://localhost:6379");
```

- Conditionally create index necessary for searching

```csharp
var info = provider.Connection.Execute("FT._LIST").ToArray().Select(x => x.ToString());

if (info.All(x => x != "person-idx"))
{
    provider.Connection.CreateIndex(typeof(Person));
}
```

- Initialize your collection

```csharp
var people = provider.RedisCollection<Person>();
```

- Insert example

```csharp
var person = new Person
{
    FirstName = "Rupert",
    LastName = "Holmes",
    Age = 75,
    Verified = false,
    Location = new GeoLoc { Longitude = 45.678, Latitude = 45.678 },
    Skills = new string[] { "singing", "songwriting", "playwriting" },
    PersonalStatement = "I like piña coladas and walks in the rain"
};

var id = people.Insert(person);
```

- Read example

```csharp
person = people.FindById(id);
```

- Update example

```csharp
person = people.FindById(id);
person.FirstName = "Alex";
person.LastName = null;
people.Update(person);
```

- Update location example

```csharp
person = people.FindById(id);
person.Location = new GeoLoc { Longitude = 44.678, Latitude = 44.678 };
people.Update(person);
```

- Search examples

```csharp
// Multiple AND conditions example
people.Where(p => p.Age > 21 && p.FirstName == "Alex").ToList();

// Multiple OR conditions example
people.Where(p => p.Age > 75 || p.FirstName == "Alex").ToList();

// Multiple AND + OR conditions example
people.Where(p =>
            (p.Age > 21 && p.FirstName == "Alex") &&
            (p.Age > 75 || p.FirstName == "Alex")
).ToList();
```

- Delete example

```csharp
person = people.FindById(id);
people.Delete(person);
```

- [Redis OM .NET Github repo](https://github.com/redis/redis-om-dotnet)
- [Getting started video](https://www.youtube.com/watch?v=ZHPXKrJCYNA)
- [Getting started source code](https://github.com/redis-developer/redis-om-dotnet-skeleton-app)

## How do I use probabilistic data structures in Redis?

Redis supports probabilistic data types and queries. Below you will find a stock leaderboard example:

```bash
# Reserve a new leaderboard filter
> TOPK.RESERVE trending-stocks 12 50 4 0.9
"OK"

# Add a new entries to the leaderboard
> TOPK.ADD trending-stocks AAPL AMD MSFT INTC GOOG FB NFLX GME AMC TSLA
1) "null" ...

# Get the leaderboard
> TOPK.LIST trending-stocks
1) "AAPL"
2) "AMD"
2) "MSFT" ...

# Get information about the leaderboard
> TOPK.INFO trending-stocks
1) "k"
2) "12"
3) "width"
4) "50"
5) "depth"
6) "4"
7) "decay"
8) "0.90000000000000002"
```

More details in [docs](https://redis.io/docs/latest/develop/data-types/probabilistic/)

## How do I store and query time-series data in Redis?

Redis supports time-series use cases such as IoT, stock prices, and telemetry. You can ingest and query millions of samples and events at the speed of Redis. You can also use a variety of queries for visualization and monitoring with built-in connectors to popular tools like Grafana, Prometheus, and Telegraf.

The following example demonstrates how you might store temperature sensor readings in Redis:

```bash
# Create new time-series, for example temperature readings
> TS.CREATE temperature:raw DUPLICATE_POLICY LAST
"OK"

# Create a bucket for monthly aggregation
> TS.CREATE temperature:monthly DUPLICATE_POLICY LAST
"OK"

# Automatically aggregate based on time-weighted average
> TS.CREATERULE temperature:raw temperature:monthly AGGREGATION twa 2629800000
"OK"

# Add data to the raw time-series
> TS.MADD temperature:raw 1621666800000 52 ...
1) "1621666800000" ...

# View the monthly time-weighted average temperatures
> TS.RANGE temperature:monthly 0 +
1) 1) "1621666800000"
   2) "52" ...

# Delete compaction rule
> TS.DELETERULE temperature:raw temperature:monthly
"OK"

# Delete partial time-series
> TS.DEL temperature:raw 0 1621666800000
(integer) 1
```

More details in [docs](https://redis.io/docs/latest/develop/data-types/timeseries/)

## Next steps

Now that you have Redis up and running, explore these tutorials to go deeper:

- [Redis Quick Start Cheat Sheet](/tutorials/howtos/quick-start/cheat-sheet/) -- a handy reference for the most common Redis commands
- [Rate Limiting with Redis](/tutorials/howtos/ratelimiting/) -- learn how to build a rate limiter using Redis
- [Building a Leaderboard with Redis](/tutorials/howtos/leaderboard/) -- create a real-time leaderboard backed by Redis Sorted Sets
- [Getting Started with Node and Redis](/tutorials/develop/node/gettingstarted/) -- build your first Node.js app with Redis
- [Getting Started with Java and Redis](/tutorials/develop/java/getting-started/) -- connect Redis to a Java application
- [Getting Started with Redis OM for Python](/tutorials/develop/python/redis-om/) -- model and query Redis data with Python

## Additional Resources

- Join the [community](https://redis.io/community)
- [Redis Insight](https://redis.io/insight/)
