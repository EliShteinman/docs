---
title: "Redis Commands Cheat sheet"
linkTitle: "Redis Commands Cheat sheet"
url: "/tutorials/howtos/quick-start/cheat-sheet/"
description: "What are the most common Redis commands? This cheat sheet gives you a quick reference for essential Redis commands across the CLI, node-redis, redis-py, NRedisStack, and Jedis. For full step-by-..."
aliases:
- "/tutorials/howtos-quick-start-cheat-sheet/"
date: 2026-02-24
lastmod: 2026-09-01
hidden: true
---

*Published 24 February 2026 · updated 1 September 2026*

What are the most common Redis commands? This cheat sheet gives you a quick reference for essential Redis commands across the CLI, [node-redis](https://github.com/redis/node-redis), [redis-py](https://github.com/redis/redis-py), [NRedisStack](https://github.com/redis/NRedisStack), and [Jedis](https://github.com/redis/jedis). For full step-by-step explanations, see the [Quick start guide](/tutorials/howtos/quick-start/). You can also browse the complete [Redis commands reference](https://redis.io/docs/latest/commands/).

**What you'll find here:**

- Connection examples (CLI, Redis Insight, and client libraries)
- String and number operations (SET, GET, MGET, INCR)
- Generic key operations (KEYS, EXISTS, EXPIRE, TTL, SCAN, DEL)
- Hashes (HSET, HGET, HGETALL, HMGET)
- Sets (SADD, SMEMBERS, SCARD, SDIFF)
- Sorted sets (ZADD, ZRANGE)
- Lists (LPUSH, RPUSH, LRANGE, LPOP, RPOP)
- Streams (XADD, XREAD, XRANGE, XLEN, XDEL, XTRIM)
- JSON (JSON.SET, JSON.GET, JSON.ARRAPPEND, JSON.ARRINDEX)
- Search and query (FT.CREATE, FT.SEARCH, FT.AGGREGATE)

## Connect

### CLI

```bash
# Syntax
redis-cli -u redis://host:port
redis-cli -u redis://username:password@host:port

# Examples
redis-cli
redis-cli -u redis://localhost:6379
redis-cli -u redis://myuser:mypassword@localhost:6379

# If you run Redis through Docker
docker exec -it <container-id-or-name> redis-cli
```

### Redis Insight

Download [Redis Insight](https://redis.io/insight/) to visually explore your Redis data or to engage with raw Redis commands in the workbench.

![Redis Insight workbench showing command results in the GUI query interface](/images/site-mirror/780038e210eeeef2f90aa5d608035d4bbaf283df-1896x954.webp)

### node-redis

```javascript
import { createClient } from 'redis';

let client = createClient({ url: 'redis://localhost:6379' });

await client.connect();

//await client.set('key', 'value');

await client.disconnect();
```

### redis-py

```python
import redis

r = redis.Redis(host='localhost', port=6379, db=0)
```

### NRedisStack

```csharp
using StackExchange.Redis;

ConnectionMultiplexer redis = ConnectionMultiplexer.Connect("localhost");
IDatabase db = redis.GetDatabase();
```

### Jedis

```java
import redis.clients.jedis.JedisPooled;

JedisPooled jedis = new JedisPooled("localhost", 6379);
```

> **NOTE**
>
> To setup Redis either locally or in the cloud, refer to the [tutorial](/tutorials/howtos/quick-start#setup-redis)

## Strings/Numbers

### CLI

| **Command** | **Syntax**           | **Example**                 | **Output**            | **Description**                                                                                                                                                         |
| :---------- | :------------------- | :-------------------------- | :-------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SET         | `SET key value`      | `SET myKey "Hello"`         | `"OK"`                | Set key to hold the string value. If key already holds a value, it is overwritten, regardless of its type. _Time Complexity: O(1)_                                      |
| GET         | `GET key`            | `GET myKey`                 | `"Hello"`             | Get the string value of key. If the key does not exist the special value nil is returned. _Time Complexity: O(1)_                                                       |
| MGET        | `MGET key [key ...]` | `MGET myKey nonExistentKey` | `1) "Hello" 2) (nil)` | Returns the values of all specified keys. For every key that does not hold a string value or does not exist, the special value nil is returned. _Time Complexity: O(N)_ |
| INCR        | `INCR key`           | `INCR myCounter`            | `(integer) 1`         | Increments the number stored at key by one. If the key does not exist, it is set to 0 before performing the operation. _Time Complexity: O(1)_                          |

### node-redis

```javascript
/*
  SET key value
  Set key to hold the string value. If key already holds a value, it is overwritten, regardless of its type.
  Time Complexity: O(1)
  */
const setResult = await client.set('myKey', 'Hello');
console.log(setResult); // "OK"

/*
  GET key
  Get the string value of key. If the key does not exist the special value nil is returned.
  Time Complexity: O(1)
  */
const getResult = await client.get('myKey');
console.log(getResult); // "Hello"

/*
  MGET key [key ...]
  Returns the values of all specified keys. For every key that does not hold a string value or does not exist, the special value nil is returned.
  Time Complexity: O(N)
  */
const mGetResult = await client.mGet(['myKey', 'nonExistentKey']);
console.log(mGetResult); // ["Hello", null]

/*
  INCR key
  Increments the number stored at key by one. If the key does not exist, it is set to 0 before performing the operation.
  Time Complexity: O(1)
  */
const incrResult = await client.incr('myCounter');
console.log(incrResult); // 1
```

### redis-py

```python
# SET key value
# O(1)
# Set key to hold the string value. If key already holds a value, it is overwritten, regardless of its type.
r.set('mykey', 'Hello')
r.set('mykey2', 'World')

# GET key
# O(1)
# Get the string value of key. If the key does not exist the special value nil is returned.
r.get('mykey')

# MGET key [key ...]
# O(N)
# Returns the values of all specified keys. For every key that does not hold a string value or does not exist, the special value nil is returned.
r.mget(['mykey', 'mykey2', 'nonexistantkey'])

# INCR key
# O(1)
# Increments the number stored at key by one. If the key does not exist, it is set to 0 before performing the operation.
r.delete('mykey')
r.incr('mykey', 1)
r.get('mykey')
```

### NRedisStack

```csharp
/*
 * SET key value
 * O(1)
 * Set key to hold the string value. If key already holds a value, it is
 * overwritten, regardless of its type.
 */
db.StringSet("mykey", "Hello");
db.StringSet("mykey2", "World");

/*
 * GET key
 * O(1)
 * Get the value of key. If the key does not exist the special value nil
 */
db.StringGet("mykey");

/*
 * MGET key [key ...]
 * O(N)
 * Returns the values of all specified keys. For every key that does not hold a
 * string value or does not exist, the special value nil is returned.
 */
db.StringGet(new RedisKey[] { "mykey", "mykey2", "nonexistantkey" });

/*
 * INCR key
 * O(1)
 * Increments the number stored at key by one. If the key does not exist, it is
 * set to 0 before performing the operation.
 */
db.KeyDelete("mykey");
db.StringIncrement("mykey");
db.StringGet("mykey");
```

### Jedis

```java
/*
 * SET key value
 * O(1)
 * Set key to hold the string value. If key already holds a value, it is
 * overwritten, regardless of its type.
 */
jedis.set("mykey", "Hello");
jedis.set("mykey2", "World");

/*
 * GET key
 * O(1)
 * Get the value of key. If the key does not exist the special value nil
 */
jedis.get("mykey");

/*
 * MGET key [key ...]
 * O(N)
 * Returns the values of all specified keys. For every key that does not hold a
 * string value or does not exist, the special value nil is returned.
 */
jedis.mget("mykey", "mykey2", "nonexistantkey");

/*
 * INCR key
 * O(1)
 * Increments the number stored at key by one. If the key does not exist, it is
 * set to 0 before performing the operation.
 */
jedis.del("mykey");
jedis.incr("mykey");
jedis.get("mykey");
```

## Generic

### CLI

| **Command** | **Syntax**                                  | **Example**                | **Output**                                  | **Description**                                                                                                                                                                                                                                              |
| :---------- | :------------------------------------------ | :------------------------- | :------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| KEYS        | `KEYS pattern`                              | `KEYS my*`                 | `1) "myKey" 2) "myCounter"`                 | Returns all keys matching pattern. _Time Complexity: O(N)_                                                                                                                                                                                                   |
| EXISTS      | `EXISTS key [key ...]`                      | `EXISTS myKey`             | `(integer) 1`                               | Checks if one or more keys exist. _Time Complexity: O(N)_                                                                                                                                                                                                    |
| EXPIRE      | `EXPIRE key seconds`                        | `EXPIRE myKey 120`         | `(integer) 1`                               | Set a timeout on a key. After the timeout has expired, the key will automatically be deleted. _Time Complexity: O(1)_                                                                                                                                        |
| TTL         | `TTL key`                                   | `TTL myKey`                | `(integer) 113`                             | Returns the remaining time to live of a key that has a timeout. _Time Complexity: O(1)_                                                                                                                                                                      |
| PERSIST     | `PERSIST key`                               | `PERSIST myKey`            | `(integer) 1`                               | Removes the expiration from a key. _Time Complexity: O(1)_                                                                                                                                                                                                   |
| SCAN        | `SCAN cursor [MATCH pattern] [COUNT count]` | `SCAN 0 MATCH my* COUNT 2` | `1) "3" 2) 1) "myCounter" 2) "myKey"`       | Iterates the set of keys in the currently selected Redis database. _Time Complexity: O(1) for every call. O(N) for a complete iteration._                                                                                                                    |
| DEL         | `DEL key [key ...]`                         | `DEL myKey`                | `(integer) 1`                               | Removes the specified keys. _Time Complexity: O(N)_                                                                                                                                                                                                          |
| INFO        | `INFO [section]`                            | `INFO keyspace`            | `# Keyspace db0:keys=2,expires=0,avg_ttl=0` | Returns information and statistics about the server, with the different sections like - server, clients, memory, persistence, stats, replication, cpu, commandstats, latencystats, sentinel, cluster, modules, keyspace, errorstats. _Time Complexity: O(1)_ |

### node-redis

```javascript
/*
    KEYS pattern
    Returns all keys matching pattern.
    Time Complexity: O(N)
    */
const keysResult = await client.keys('my*');
console.log(keysResult); // ["myKey", "myCounter"]

/*
    EXISTS key [key ...]
    Checks if one or more keys exist.
    Time Complexity: O(N)
    */
const existsResult = await client.exists('myKey');
console.log(existsResult); // 1

/*
    EXPIRE key seconds
    Set a timeout on a key. After the timeout has expired, the key will automatically be deleted.
    Time Complexity: O(1)
    */
const expireResult = await client.expire('myKey', 120);
console.log(expireResult); // true

/*
    TTL key
    Returns the remaining time to live of a key that has a timeout.
    Time Complexity: O(1)
    */
const ttlResult = await client.ttl('myKey');
console.log(ttlResult); // 113

/*
    PERSIST key
    Removes the expiration from a key.
    Time Complexity: O(1)
    */
const persistResult = await client.persist('myKey');
console.log(persistResult); // true

/*
    SCAN cursor [MATCH pattern] [COUNT count]
    Iterates the set of keys in the currently selected Redis database.
    Time Complexity: O(1) for every call. O(N) for a complete iteration.
    */
const scanOptions = {
    TYPE: 'string',
    MATCH: 'my*',
    COUNT: 2,
};
let cursor = 0;

// scan 1
let scanResult = await client.scan(cursor, scanOptions);
console.log(scanResult); // { cursor: 4, keys: [ 'myCounter', 'myKey' ] }

// scan 2
cursor = scanResult.cursor;
scanResult = await client.scan(cursor, scanOptions);
console.log(scanResult); //{ cursor: 12, keys: [ 'myOtherkey' ] }

// ... scan n

console.log('OR use any loop to continue the scan by cursor value');
cursor = 0;
do {
    scanResult = await client.scan(cursor, scanOptions);
    console.log(scanResult);
    cursor = scanResult.cursor;
} while (cursor != 0);

/*
    DEL key [key ...]
    Removes the specified keys.
    Time Complexity: O(N)
    */
const delResult = await client.del('myKey');
console.log(delResult); // 1

/*
    INFO [section]
    Returns information and statistics about the server, with the different sections
        like - server, clients, memory, persistence, stats, replication, cpu, commandstats,
        latencystats, sentinel, cluster, modules, keyspace, errorstats.
    Time Complexity: O(1)
    */
let infoResult = await client.info('keyspace');
console.log(infoResult); //# Keyspace \n db0:keys=2,expires=0,avg_ttl=0"
```

### redis-py

```python
# KEYS pattern
# O(N)
# Returns all keys matching pattern.
r.keys('*')

# EXPIRE key seconds
# O(1)
# Set a timeout on key. After the timeout has expired, the key will automatically be deleted.
r.expire('mykey', 10)

# SCAN cursor [MATCH pattern] [COUNT count]
# O(1) for every call. O(N) for a complete iteration, including enough command calls for the cursor to return back to 0.
# Iterates the set of keys in the currently selected Redis database.
r.delete('mykey', 'mykey2')
scanResult = r.scan(0, match='employee_profile:*')
r.scan(scanResult[0], match='employee_profile:*')

# DEL key [key ...]
# O(N)
# Removes the specified keys.
r.delete('employee_profile:viraj', 'employee_profile:terry',
         'employee_profile:sheera')

# TTL key
# O(1)
# Returns the remaining time to live of a key that has a timeout.
r.ttl('employee_profile:nicol')

# INFO [section ...]
# O(1)
# Returns information and statistics about the server, with the following sections: server, clients, memory, persistence, stats, replication, cpu, commandstats, latencystats, sentinel, cluster, modules, keyspace, errorstats
r.info('keyspace')
```

### NRedisStack

```csharp
/*
 * KEYS pattern
 * O(N)
 * Returns all keys matching pattern.
 */
redis.GetServer("localhost:6379").Keys();

/*
 * EXPIRE key seconds
 * O(1)
 * Set a timeout on key. After the timeout has expired, the key will be
 * automatically deleted.
 */
db.KeyExpire("mykey", TimeSpan.FromSeconds(10));

/*
 * SCAN cursor [MATCH pattern] [COUNT count]
 * O(1) for every call. O(N) for a complete iteration, including enough command
 * calls for the cursor to return back to 0.
 * Iterates the set of keys in the currently selected Redis database.
 */
db.KeyDelete(new RedisKey[] { "mykey", "mykey2" });
redis.GetServer("localhost:6379").Keys(-1, "employee_profile:*", 10);

/*
 * DEL key [key ...]
 * O(N)
 * Removes the specified keys.
 */
db.KeyDelete(new RedisKey[] { "employee_profile:viraj", "employee_profile:terry", "employee_profile:sheera" });

/*
 * TTL key
 * O(1)
 * Returns the remaining time to live of a key that has a timeout.
 */
db.KeyTimeToLive("employee_profile:nicol");
```

### Jedis

```java
/*
 * KEYS pattern
 * O(N)
 * Returns all keys matching pattern.
 */
jedis.keys("*");

/*
 * EXPIRE key seconds
 * O(1)
 * Set a timeout on key. After the timeout has expired, the key will be
 * automatically deleted.
 */
jedis.expire("mykey", 10);

/*
 * SCAN cursor [MATCH pattern] [COUNT count]
 * O(1) for every call. O(N) for a complete iteration, including enough command
 * calls for the cursor to return back to 0.
 * Iterates the set of keys in the currently selected Redis database.
 */
jedis.del("mykey", "mykey2");
ScanResult<String> scan = jedis.scan("0", new ScanParams() {
    {
        match("employee_profile:*");
    }
});
scan = jedis.scan(scan.getCursor(), new ScanParams() {
    {
        match("employee_profile:*");
    }
});

/*
 * DEL key [key ...]
 * O(N)
 * Removes the specified keys.
 */
jedis.del("employee_profile:viraj", "employee_profile:terry""employee_profile:sheera");

/*
 * TTL key
 * O(1)
 * Returns the remaining time to live of a key that has a timeout.
 */
jedis.ttl("employee_profile:nicol");
```

## Hashes

### CLI

| **Command** | **Syntax**                               | **Example**                                       | **Output**                              | **Description**                                                                                            |
| :---------- | :--------------------------------------- | :------------------------------------------------ | :-------------------------------------- | :--------------------------------------------------------------------------------------------------------- |
| HSET        | `HSET key field value [field value ...]` | `HSET h_employee_profile:101 name "Nicol" age 33` | `(integer) 2`                           | Sets the specified fields to their respective values in the hash stored at key. _Time Complexity: O(N)_    |
| HGET        | `HGET key field`                         | `HGET h_employee_profile:101 name`                | `"Nicol"`                               | Returns the value associated with field in the hash stored at key. _Time Complexity: O(1)_                 |
| HGETALL     | `HGETALL key`                            | `HGETALL h_employee_profile:101`                  | `1) "name" 2) "Nicol" 3) "age" 4) "33"` | Returns all fields and values of the hash stored at key. _Time Complexity: O(N)_                           |
| HMGET       | `HMGET key field1 [field2]`              | `HMGET h_employee_profile:101 name age`           | `1) "Nicol" 2) "33"`                    | Returns the values associated with the specified fields in the hash stored at key. _Time Complexity: O(N)_ |

### node-redis

```javascript
/*
    HSET key field value [field value ...]
    Sets the specified fields to their respective values in the hash stored at key.
    Time Complexity: O(N)
    */

const hSetResult = await client.hSet('h_employee_profile:101', {
    name: 'Nicol',
    age: 33,
});
console.log(hSetResult); // 2

/*
    HGET key field
    Returns the value associated with field in the hash stored at key.
    Time Complexity: O(1)
    */
const hGetResult = await client.hGet('h_employee_profile:101', 'name');
console.log(hGetResult); // "Nicol"

/*
    HGETALL key
    Returns all fields and values of the hash stored at key.
    Time Complexity: O(N)
    */
const hGetAllResult = await client.hGetAll('h_employee_profile:101');
console.log(hGetAllResult); // {name: "Nicol", age: "33"}

/*
    HMGET key field1 [field2]
    Returns the values associated with the specified fields in the hash stored at key.
    Time Complexity: O(N)
    */
const hmGetResult = await client.hmGet('h_employee_profile:101', [
    'name',
    'age',
]);
console.log(hmGetResult); // ["Nicol", "33"]
```

### redis-py

```python
# HSET key field value [field value ...]
# O(N)
# Sets the specified fields to their respective values in the hash stored at key.
r.hset('h_employee_profile:nicol', 'name', 'Nicol')

# HGETALL key
# O(N)
# Returns all fields and values of the hash stored at key.
r.hgetall('h_employee_profile:nicol')

# HGET key field
# O(1)
# Returns the value associated with field in the hash stored at key.
r.hget('h_employee_profile:nicol', 'name')
```

### NRedisStack

```csharp
/*
 * HSET key field value [field value ...]
 * O(N)
 * Sets the specified fields to their respective values in the hash stored at
 * key.
 */
db.HashSet("h_employee_profile:nicol", new HashEntry[] { new HashEntry("name"Nicol") });

/*
 * HGETALL key
 * O(N)
 * Returns all fields and values of the hash stored at key.
 */
db.HashGetAll("h_employee_profile:nicol");

/*
 * HGET key field
 * O(1)
 * Returns the value associated with field in the hash stored at key.
 */
db.HashGet("h_employee_profile:nicol", "name");
```

### Jedis

```java
/*
 * HSET key field value [field value ...]
 * O(N)
 * Sets the specified fields to their respective values in the hash stored at
 * key.
 */
jedis.hset("h_employee_profile:nicol", "name", "Nicol");

/*
 * HGETALL key
 * O(N)
 * Returns all fields and values of the hash stored at key.
 */
jedis.hgetAll("h_employee_profile:nicol");

/*
 * HGET key field
 * O(1)
 * Returns the value associated with field in the hash stored at key.
 */
jedis.hget("h_employee_profile:nicol", "name");
```

## Sets

### CLI

| **Command** | **Syntax**                           | **Example**                            | **Output**    | **Description**                                                                                                                         |
| :---------- | :----------------------------------- | :------------------------------------- | :------------ | :-------------------------------------------------------------------------------------------------------------------------------------- |
| SADD        | `SADD key member [member ...]`       | `SADD mySet "Hello"`                   | `(integer) 1` | Adds the specified members to the set stored at key. _Time Complexity: O(N)_                                                            |
| SMEMBERS    | `SMEMBERS key`                       | `SMEMBERS mySet`                       | `1) "Hello"`  | Returns all the members of the set value stored at key. _Time Complexity: O(N)_                                                         |
| SCARD       | `SCARD key`                          | `SCARD mySet`                          | `(integer) 1` | Returns the set cardinality (number of elements) of the set stored at key. _Time Complexity: O(1)_                                      |
| SISMEMBER   | `SISMEMBER key member`               | `SISMEMBER mySet "Hello"`              | `(integer) 1` | Returns if member is a member of the set stored at key. _Time Complexity: O(1)_                                                         |
| SDIFF       | `SDIFF key1 [key2]`                  | `SDIFF mySet myOtherSet`               | `1) "Hello"`  | Returns the members of the set resulting from the difference between the first set and all the successive sets. _Time Complexity: O(N)_ |
| SDIFFSTORE  | `SDIFFSTORE destination key1 [key2]` | `SDIFFSTORE myNewSet mySet myOtherSet` | `(integer) 1` | This command is equal to SDIFF, but instead of returning the resulting set, it is stored in destination. _Time Complexity: O(N)_        |
| SREM        | `SREM key member [member ...]`       | `SREM mySet "Hello"`                   | `(integer) 1` | Removes the specified members from the set stored at key.                                                                               |

### node-redis

```javascript
/*
    SADD key member [member ...]
    Adds the specified members to the set stored at key.
    Time Complexity: O(N)
    */
const sAddResult = await client.sAdd('mySet', 'Hello');
console.log(sAddResult); // 1

/*
    SMEMBERS key
    Returns all the members of the set value stored at key.
    Time Complexity: O(N)
    */
const sMembersResult = await client.sMembers('mySet');
console.log(sMembersResult); // ["Hello"]

/*
    SCARD key
    Returns the set cardinality (number of elements) of the set stored at key.
    Time Complexity: O(1)
    */
const sCardResult = await client.sCard('mySet');
console.log(sCardResult); // 1

/*
    SISMEMBER key member
    Returns if member is a member of the set stored at key.
    Time Complexity: O(1)
    */
const sIsMemberResult = await client.sIsMember('mySet', 'Hello');
console.log(sIsMemberResult); // true

/*
    SDIFF key1 [key2]
    Returns the members of the set resulting from the difference between the first set and all the successive sets.
    Time Complexity: O(N)
    */
const sDiffResult = await client.sDiff(['mySet', 'myOtherSet']);
console.log(sDiffResult); // ["Hello"]

/*
    SDIFFSTORE destination key1 [key2]
    This command is equal to SDIFF, but instead of returning the resulting set, it is stored in destination.
    Time Complexity: O(N)
    */
const sDiffStoreResult = await client.sDiffStore('myNewSet', [
    'mySet',
    'myOtherSet',
]);
console.log(sDiffStoreResult); // 1

/*
    SREM key member [member ...]
    Removes the specified members from the set stored at key.
    */
const sRemResult = await client.sRem('mySet', 'Hello');
console.log(sRemResult); // 1
```

### redis-py

```python
# SADD key member [member ...]
# O(N)
# Add the specified members to the set stored at key.
r.sadd('myset', 'Hello')
```

### NRedisStack

```csharp
/*
 * SADD key member [member ...]
 * O(N)
 * Add the specified members to the set stored at key.
 */
db.SetAdd("myset", "Hello");
```

### Jedis

```java
/*
 * SADD key member [member ...]
 * O(N)
 * Add the specified members to the set stored at key.
 */
jedis.sadd("myset", "Hello");
```

## Sorted sets

### CLI

| **Command** | **Syntax**                                 | **Example**                   | **Output**          | **Description**                                                                                                                                    |
| :---------- | :----------------------------------------- | :---------------------------- | :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| ZADD        | `ZADD key score member [score member ...]` | `ZADD myZSet 1 "one" 2 "two"` | `(integer) 2`       | Adds all the specified members with the specified scores to the sorted set stored at key. _Time Complexity: O(log(N))_                             |
| ZRANGE      | `ZRANGE key start stop [WITHSCORES]`       | `ZRANGE myZSet 0 -1`          | `1) "one" 2) "two"` | Returns the specified range of elements in the sorted set stored at key. _Time Complexity: O(log(N)+M) where M is the number of elements returned_ |

### node-redis

```javascript
/*
    ZADD key score member [score member ...]
    Adds all the specified members with the specified scores to the sorted set stored at key.
    Time Complexity: O(log(N))
    */
const zAddResult = await client.zAdd('myZSet', [
    {
        score: 1,
        value: 'one',
    },
    {
        score: 2,
        value: 'two',
    },
]);
console.log(zAddResult); // 2

/*
    ZRANGE key start stop [WITHSCORES]
    Returns the specified range of elements in the sorted set stored at key.
    Time Complexity: O(log(N)+M) where M is the number of elements returned
    */
const zRangeResult = await client.zRange('myZSet', 0, -1);
console.log(zRangeResult); // ["one", "two"]
```

### redis-py

```python
# ZADD key score member [score member ...]
# O(log(N))
# Adds all the specified members with the specified scores to the sorted set stored at key.
r.zadd('myzset', {'one': 1, 'two': 2, 'three': 3})

# ZRANGE key start stop [WITHSCORES]
# O(log(N)+M)
# Returns the specified range of elements in the sorted set stored at key.
r.zrange('myzset', 0, -1, withscores=True)
r.zrange('myzset', 0, -1)
```

### NRedisStack

```csharp
/*
 * ZADD key score member [score member ...]
 * O(log(N))
 * Adds all the specified members with the specified scores to the sorted set
 * stored at key.
 */
db.KeyDelete("myzset");
db.SortedSetAdd("myzset", new SortedSetEntry[] {
                            new SortedSetEntry("one", 1.0),
                            new SortedSetEntry("two", 2.0),
                            new SortedSetEntry("three", 3.0)
                          });

/*
 * ZRANGE key start stop [WITHSCORES]
 * O(log(N)+M)
 * Returns the specified range of elements in the sorted set stored at key.
 */
db.SortedSetRangeByRank("myzset", 0, -1);
db.SortedSetRangeByRankWithScores("myzset", 0, -1);
```

### Jedis

```java
/*
 * ZADD key score member [score member ...]
 * O(log(N))
 * Adds all the specified members with the specified scores to the sorted set
 * stored at key.
 */
jedis.del("myzset");
jedis.zadd("myzset", Map.of(
                            "one", 1.0,
                            "two", 2.0,
                            "three", 3.0
                            ));

/*
 * ZRANGE key start stop [WITHSCORES]
 * O(log(N)+M)
 * Returns the specified range of elements in the sorted set stored at key.
 */
jedis.zrange("myzset", 0, -1);
jedis.zrangeWithScores("myzset", 0, -1);
```

## Lists

### CLI

| **Command** | **Syntax**                    | **Example**            | **Output**              | **Description**                                                                                                                                                              |
| :---------- | :---------------------------- | :--------------------- | :---------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| LPUSH       | `LPUSH key value [value ...]` | `LPUSH myList "World"` | `(integer) 1`           | Inserts the specified values at the head of the list stored at key. _Time Complexity: O(N)_                                                                                  |
| RPUSH       | `RPUSH key value [value ...]` | `RPUSH myList "Hello"` | `(integer) 2`           | Inserts the specified values at the tail of the list stored at key. _Time Complexity: O(N)_                                                                                  |
| LRANGE      | `LRANGE key start stop`       | `LRANGE myList 0 -1`   | `1) "World" 2) "Hello"` | Returns the specified elements of the list stored at key. _Time Complexity: O(S+N) where S is the distance of start and N is the number of elements in the specified range._ |
| LLEN        | `LLEN key`                    | `LLEN myList`          | `(integer) 2`           | Returns the length of the list stored at key. _Time Complexity: O(1)_                                                                                                        |
| LPOP        | `LPOP key [count]`            | `LPOP myList`          | `"World"`               | Removes and returns the first element of the list stored at key. _Time Complexity: O(N)_                                                                                     |
| RPOP        | `RPOP key [count]`            | `RPOP myList`          | `"Hello"`               | Removes and returns the last element of the list stored at key. _Time Complexity: O(N)_                                                                                      |

### node-redis

```javascript
/*
    LPUSH key value [value ...]
    Inserts the specified values at the head of the list stored at key.
    Time Complexity: O(N)
    */
const lPushResult = await client.lPush('myList', 'World');
console.log(lPushResult); // 1

/*
    RPUSH key value [value ...]
    Inserts the specified values at the tail of the list stored at key.
    Time Complexity: O(N)
    */
const rPushResult = await client.rPush('myList', 'Hello');
console.log(rPushResult); // 2

/*
    LRANGE key start stop
    Returns the specified elements of the list stored at key.
    Time Complexity: O(S+N) where S is the distance of start and N is the number of elements in the specified range.
    */
const lRangeResult = await client.lRange('myList', 0, -1);
console.log(lRangeResult); // ["World", "Hello"]

/*
    LLEN key
    Returns the length of the list stored at key.
    Time Complexity: O(1)
    */
const lLenResult = await client.lLen('myList');
console.log(lLenResult); // 2

/*
    LPOP key [count]
    Removes and returns the first element of the list stored at key.
    Time Complexity: O(N)
    */
const lPopResult = await client.lPop('myList');
console.log(lPopResult); // "World"

/*
    RPOP key [count]
    Removes and returns the last element of the list stored at key.
    Time Complexity: O(N)
    */
const rPopResult = await client.rPop('myList');
console.log(rPopResult); // "Hello"
```

### redis-py

```python
# LPOP key [count]
# O(N)
# Removes and returns the first element(s) of the list stored at key.
r.rpush('mylist', 'one', 'two', 'three', 'four', 'five')
r.lpop('mylist')
r.lpop('mylist', 2)

# LRANGE key start stop
# O(S+N)
# Returns the specified elements of the list stored at key.
r.delete('mylist')
r.rpush('mylist', 'one', 'two', 'three', 'four', 'five')
r.lrange('mylist', 0, -1)
r.lrange('mylist', -3, 2)

# LPUSH key element [element ...]
# O(N)
# Inserts specified values at the head of the list stored at key.
r.delete('mylist')
r.lpush('mylist', 'world')
r.lpush('mylist', 'hello')
r.lrange('mylist', 0, -1)
```

### NRedisStack

```csharp
/*
 * LPOP key [count]
 * O(N)
 * Removes and returns the first elements of the list stored at key.
 */
db.ListLeftPush("mylist", new RedisValue[] { "one", "two", "three", "four", "five" });
db.ListLeftPop("mylist");
db.ListLeftPop("mylist", 2);

/*
 * LRANGE key start stop
 * O(S+N)
 * Returns the specified elements of the list stored at key.
 */
db.KeyDelete("mylist");
db.ListRightPush("mylist", new RedisValue[] { "one", "two", "three", "four", "five" });
db.ListRange("mylist", 0, -1);
db.ListRange("mylist", -3, 2);

/*
 * LPUSH key value [value ...]
 * O(N)
 * Insert all the specified values at the head of the list stored at key.
 */
db.KeyDelete("mylist");
db.ListLeftPush("mylist", new RedisValue[] { "world" });
db.ListLeftPush("mylist", new RedisValue[] { "hello" });
db.ListRange("mylist", 0, -1);
```

### Jedis

```java
/*
 * LPOP key [count]
 * O(N)
 * Removes and returns the first elements of the list stored at key.
 */
jedis.lpush("mylist", "one", "two", "three", "four", "five");
jedis.lpop("mylist");
jedis.lpop("mylist", 2);

/*
 * LRANGE key start stop
 * O(S+N)
 * Returns the specified elements of the list stored at key.
 */
jedis.del("mylist");
jedis.rpush("mylist", "one", "two", "three", "four", "five");
jedis.lrange("mylist", 0, -1);
jedis.lrange("mylist", -3, 2);

/*
 * LPUSH key value [value ...]
 * O(N)
 * Insert all the specified values at the head of the list stored at key.
 */
jedis.del("mylist");
jedis.lpush("mylist", "world");
jedis.lpush("mylist", "hello");
jedis.lrange("mylist", 0, -1);
```

## Streams

### CLI

| **Command** | **Syntax**                                                                   | **Example**                                          | **Output**                                                                                          | **Description**                                                                                                                                                                                                                                                             |
| :---------- | :--------------------------------------------------------------------------- | :--------------------------------------------------- | :-------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| XADD        | `XADD key field value [field value ...]`                                     | `XADD myStream * sensorId "1234" temperature "19.8"` | `1518951480106-0`                                                                                   | Appends the specified stream entry to the stream at the specified key. _Time Complexity: O(1) when adding a new entry._                                                                                                                                                     |
| XREAD       | `XREAD [COUNT count] [BLOCK milliseconds] STREAMS key [key ...] ID [ID ...]` | `XREAD COUNT 2 STREAMS myStream 0`                   | `1) 1) "myStream" 2) 1) 1) "1518951480106-0" 2) 1) "sensorId" 2) "1234" 3) "temperature" 4) "19.8"` | Read data from one or multiple streams, only returning entries with an ID greater than the last received ID reported by the caller.                                                                                                                                         |
| XRANGE      | `XRANGE key start end [COUNT count]`                                         | `XRANGE myStream 1518951480106-0 1518951480106-0`    | `1) 1) "1518951480106-0" 2) 1) "sensorId" 2) "1234" 3) "temperature" 4) "19.8"`                     | Returns the entries matching a range of IDs in a stream. _Time Complexity: O(N) with N being the number of elements being returned. If N is constant (e.g. always asking for the first 10 elements with COUNT), you can consider it O(1)._                                  |
| XLEN        | `XLEN key`                                                                   | `XLEN myStream`                                      | `(integer) 1`                                                                                       | Returns the number of entries of a stream. _Time Complexity: O(1)_                                                                                                                                                                                                          |
| XDEL        | `XDEL key ID [ID ...]`                                                       | `XDEL myStream 1518951480106-0`                      | `(integer) 1`                                                                                       | Removes the specified entries from a stream. _Time Complexity: O(1) for each single item to delete in the stream_                                                                                                                                                           |
| XTRIM       | `XTRIM key MAXLEN [~] count`                                                 | `XTRIM myStream MAXLEN 0`                            | `(integer) 0`                                                                                       | Trims the stream to a different length. _Time Complexity: O(N), with N being the number of evicted entries. Constant times are very small however, since entries are organized in macro nodes containing multiple entries that can be released with a single deallocation._ |

### node-redis

```javascript
/*
    XADD key field value [field value ...]
    Appends the specified stream entry to the stream at the specified key.
    O(1) when adding a new entry.
    */
const xAddResult = await client.xAdd(
    'myStream',
    '*', //dynamic id
    {
        sensorId: '1234',
        temperature: '19.8',
    },
);
console.log(xAddResult); // "1518951480106-0"

/*
    XREAD [COUNT count] [BLOCK milliseconds] STREAMS key [key ...] ID [ID ...]
    Read data from one or multiple streams, only returning entries with an ID greater than the last received ID reported by the caller.
    */
const xReadResult = await client.xRead(
    commandOptions({
        isolated: true,
    }),
    [
        {
            // XREAD can read from multiple streams, starting at a different ID for each.
            key: 'myStream',
            id: '0', //entries greater than id
        },
    ],
    {
        // Read 2 entries at a time, block for 5 seconds if there are none.
        COUNT: 2,
        BLOCK: 5000,
    },
);

console.log(JSON.stringify(xReadResult)); // [{"name":"myStream","messages":[{"id":"1518951480106-0","message":{"sensorId":"1234","temperature":"19.8"}}]}]

/*
    XRANGE key start end [COUNT count]
    Returns the entries matching a range of IDs in a stream.
    O(N) with N being the number of elements being returned. If N is constant (e.g. always asking for the first 10 elements with COUNT), you can consider it O(1).
    */
const xRangeResult = await client.xRange('myStream', xAddResult, xAddResult);
console.log(JSON.stringify(xRangeResult)); // [{"id":"1518951480106-0","message":{"sensorId":"1234","temperature":"19.8"}}]

/*
    XLEN key
    Returns the number of entries of a stream.
    O(1)
    */
const xLenResult = await client.xLen('myStream');
console.log(xLenResult); // 1

/*
    XDEL key ID [ID ...]
    Removes the specified entries from a stream.
    O(1) for each single item to delete in the stream
    */
const xDelResult = await client.xDel('myStream', xAddResult);
console.log(xDelResult); // 1

/*
    XTRIM key MAXLEN [~] count
    Trims the stream to a different length.
    O(N), with N being the number of evicted entries. Constant times are very small however, since entries are organized in macro nodes containing multiple entries that can be released with a single deallocation.
    */
const xTrimResult = await client.xTrim('myStream', 'MAXLEN', 0);
console.log(xTrimResult); // 0
```

### redis-py

```python
# XADD key field value [field value ...]
# O(1) for new entries, O(N) when trimming where N is the number of evicted values
# Appends the specified stream entry to the stream at the specified key.
r.xadd('temperatures:us-ny:10007',
       {'temp_f': 87.2, 'pressure': 29.69, 'humidity': 46})
r.xadd('temperatures:us-ny:10007',
       {'temp_f': 83.1, 'pressure': 29.21, 'humidity': 46.5})
r.xadd('temperatures:us-ny:10007',
       {'temp_f': 81.9, 'pressure': 28.37, 'humidity': 43.7})

# XREAD [COUNT count] [BLOCK milliseconds] STREAMS key [key ...] ID [ID ...]
# Read data from one or multiple streams, only returning entries with an ID greater than the last received ID reported by the caller.
r.xread({'temperatures:us-ny:10007': '0-0'})
```

### NRedisStack

```csharp
/*
 * XADD key ID field value [field value ...]
 * O(1) for new entries, O(N) when trimming where N is the number of evicted
 * values
 * Appends the specified stream entry to the stream at the specified key.
 */
db.StreamAdd("temperatures:us-ny:10007", new NameValueEntry[] { new NameValueEntry("temp_f", "87.2"), new NameValueEntry("pressure", "29.69"), new NameValueEntry("humidity", "46.0") });
db.StreamAdd("temperatures:us-ny:10007", new NameValueEntry[] { new NameValueEntry("temp_f", "83.1"), new NameValueEntry("pressure", "29.21"), new NameValueEntry("humidity", "46.5") });
db.StreamAdd("temperatures:us-ny:10007", new NameValueEntry[] { new NameValueEntry("temp_f", "81.9"), new NameValueEntry("pressure", "28.37"), new NameValueEntry("humidity", "43.7") });

/*
 * XREAD [COUNT count] [BLOCK milliseconds] STREAMS key [key ...] ID [ID ...]
 * Read data from one or multiple streams, only returning entries with an ID
 * greater than the last received ID reported by the caller.
 */
db.StreamRead("temperatures:us-ny:10007", "0-0");
```

### Jedis

```java
/*
 * XADD key ID field value [field value ...]
 * O(1) for new entries, O(N) when trimming where N is the number of evicted
 * values
 * Appends the specified stream entry to the stream at the specified key.
 */
jedis.xadd("temperatures:us-ny:10007", StreamEntryID.NEW_ENTRY,
        Map.of("temp_f", "87.2", "pressure", "29.69", "humidity", "46.0"));
jedis.xadd("temperatures:us-ny:10007", StreamEntryID.NEW_ENTRY,
        Map.of("temp_f", "83.1", "pressure", "29.21", "humidity", "46.5"));
jedis.xadd("temperatures:us-ny:10007", StreamEntryID.NEW_ENTRY,
        Map.of("temp_f", "81.9", "pressure", "28.37", "humidity", "43.7"));

/*
 * XREAD [COUNT count] [BLOCK milliseconds] STREAMS key [key ...] ID [ID ...]
 * Read data from one or multiple streams, only returning entries with an ID
 * greater than the last received ID reported by the caller.
 */
jedis.xread(XReadParams.xReadParams().count(5).block(1000),
        singletonMap("temperatures:us-ny:10007", new StreamEntryID(0, 0)));
```

## JSON

### CLI

| **Command**    | **Syntax**                                        | **Example**                                              | **Output**           | **Description**                                                                                                                                                                                                                                                         |
| :------------- | :------------------------------------------------ | :------------------------------------------------------- | :------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| JSON.SET       | `JSON.SET key path value`                         | `JSON.SET employee_profile:1 . '{"name":"Alice"}'`       | `OK`                 | Sets JSON value at path in key. _Time Complexity: O(M+N) where M is the original size and N is the new size_                                                                                                                                                            |
| JSON.GET       | `JSON.GET key [path [path ...]]`                  | `JSON.GET employee_profile:1`                            | `{"name":"Alice"}`   | Returns the JSON value at path in key. _Time Complexity: O(N) when path is evaluated to a single value where N is the size of the value, O(N) when path is evaluated to multiple values, where N is the size of the key_                                                |
| JSON.NUMINCRBY | `JSON.NUMINCRBY key path number`                  | `JSON.NUMINCRBY employee_profile:1 .age 5`               | `35`                 | Increments a number inside a JSON document. _Time Complexity: O(1) when path is evaluated to a single value, O(N) when path is evaluated to multiple values, where N is the size of the key_                                                                            |
| JSON.OBJKEYS   | `JSON.OBJKEYS key [path]`                         | `JSON.OBJKEYS employee_profile:1`                        | `1) "name" 2) "age"` | Return the keys in the object that's referenced by path. _Time Complexity: O(N) when path is evaluated to a single value, where N is the number of keys in the object, O(N) when path is evaluated to multiple values, where N is the size of the key_                  |
| JSON.OBJLEN    | `JSON.OBJLEN key [path]`                          | `JSON.OBJLEN employee_profile:1`                         | `(integer) 2`        | Report the number of keys in the JSON object at path in key. _Time Complexity: O(1) when path is evaluated to a single value, O(N) when path is evaluated to multiple values, where N is the size of the key_                                                           |
| JSON.ARRAPPEND | `JSON.ARRAPPEND key [path] value [value ...]`     | `JSON.ARRAPPEND employee_profile:1 .colors '"yellow"'`   | `(integer) 4`        | Append the json values into the array at path after the last element in it. _Time Complexity: O(1) for each value added, O(N) for multiple values added where N is the size of the key_                                                                                 |
| JSON.ARRINSERT | `JSON.ARRINSERT key path index value [value ...]` | `JSON.ARRINSERT employee_profile:1 .colors 2 '"purple"'` | `(integer) 5`        | Insert the json values into the array at path before the index (shifts to the right). _Time Complexity: O(N) when path is evaluated to a single value where N is the size of the array, O(N) when path is evaluated to multiple values, where N is the size of the key_ |
| JSON.ARRINDEX  | `JSON.ARRINDEX key path value [start [stop]]`     | `JSON.ARRINDEX employee_profile:1 .colors '"purple"'`    | `(integer) 2`        | Searches for the first occurrence of a JSON value in an array. _Time Complexity: O(N) when path is evaluated to a single value where N is the size of the array, O(N) when path is evaluated to multiple values, where N is the size of the key_                        |

### node-redis

```javascript
/*
      JSON.SET key path value
      Sets JSON value at path in key.
      O(M+N) where M is the original size and N is the new size
    */
const setResult = await client.json.set('employee_profile:1', '.', {
    name: 'Alice',
});
console.log(setResult); // OK

/*
       JSON.GET key [path [path ...]]
       Returns the JSON value at path in key.
       O(N) when path is evaluated to a single value where N is the size of the value, O(N) when path is evaluated to multiple values, where N is the size of the key
    */
const getResult = await client.json.get('employee_profile:1');
console.log(getResult); // { name: 'Alice' }

/*
      JSON.NUMINCRBY key path number
      Increments a number inside a JSON document.
      O(1) when path is evaluated to a single value, O(N) when path is evaluated to multiple values, where N is the size of the key
    */
await client.json.set('employee_profile:1', '.age', 30);
const incrementResult = await client.json.numIncrBy(
    'employee_profile:1',
    '.age',
    5,
);
console.log(incrementResult); // 35

/*
      JSON.OBJKEYS key [path]
      Return the keys in the object that's referenced by path
      O(N) when path is evaluated to a single value, where N is the number of keys in the object, O(N) when path is evaluated to multiple values, where N is the size of the key
    */
const objKeysResult = await client.json.objKeys('employee_profile:1');
console.log(objKeysResult); // [ 'name', 'age' ]

/*
      JSON.OBJLEN key [path]
      Report the number of keys in the JSON object at path in key
      O(1) when path is evaluated to a single value, O(N) when path is evaluated to multiple values, where N is the size of the key
    */
const objLenResult = await client.json.objLen('employee_profile:1');
console.log(objLenResult); // 2

/*
      JSON.ARRAPPEND key [path] value [value ...]
      Append the json values into the array at path after the last element in it
      O(1) for each value added, O(N) for multiple values added where N is the size of the key
    */
await client.json.set('employee_profile:1', '.colors', [
    'red',
    'green',
    'blue',
]);
const arrAppendResult = await client.json.arrAppend(
    'employee_profile:1',
    '.colors',
    'yellow',
);
console.log(arrAppendResult); // 4

/*
      JSON.ARRINSERT key path index value [value ...]
      Insert the json values into the array at path before the index (shifts to the right)
      O(N) when path is evaluated to a single value where N is the size of the array, O(N) when path is evaluated to multiple values, where N is the size of the key
    */
const arrInsertResult = await client.json.arrInsert(
    'employee_profile:1',
    '.colors',
    2,
    'purple',
);
console.log(arrInsertResult); // 5

/*
      JSON.ARRINDEX key path json [start [stop]]
      Searches for the first occurrence of a JSON value in an array.
      O(N) when path is evaluated to a single value where N is the size of the array, O(N) when path is evaluated to multiple values, where N is the size of the key
    */
const arrIndexResult = await client.json.arrIndex(
    'employee_profile:1',
    '.colors',
    'purple',
);
console.log(arrIndexResult); // 2
```

### redis-py

```python
# JSON.SET key path value
# O(M+N) where M is the original size and N is the new size
# Set the JSON value at path in key.
r.json().set('employee_profile:nicol', '.', {
    'name': 'nicol', 'age': 24, 'single': True, 'skills': []})
r.json().set('employee_profile:nicol', '$.name', 'Nicol')

# JSON.GET key [path [path ...]]
# O(N)
# Return the value at path in JSON serialized form
r.json().get('employee_profile:nicol', '.')

# JSON.ARRAPPEND key [path] value [value ...]
# O(1) for each value added, O(N) for multiple values added where N is the size of the key
# Append the value(s) to the array at path in key after the last element in the array.
r.json().set('employee_profile:nicol', '$.skills', [])
r.json().arrappend('employee_profile:nicol', '$.skills', 'python')
r.json().get('employee_profile:nicol', '$.skills')

# JSON.ARRINDEX key path value [start [stop]]
# O(N)
# Search for the first occurrence of a JSON value in an array.
r.json().arrindex('employee_profile:nicol', '$.skills', 'python')
r.json().arrindex('employee_profile:nicol', '$.skills', 'java')
```

### NRedisStack

```csharp
/*
 * JSON.SET key path value
 * O(M+N) where M is the original size and N is the new size
 * Set the JSON value at path in key.
 */
db.JSON().Set("employee_profile:nicol", ".", new
{
    name = "Nicol",
    age = 24,
    single = true,
    skills = new string[] { }
});
db.JSON().Set("employee_profile:nicol", "$.name", "\"Nicol\"");

/*
 * JSON.GET key [path [path ...]]
 * O(N)
 * Return the value at path in JSON serialized form
 */
db.JSON().Get("employee_profile:nicol", ".");

/*
 * JSON.ARRAPPEND key [path] value [value ...]
 * O(1) for each value added, O(N) for multiple values added where N is the size
 * of the key
 * Append the value(s) to the array at path in key after the last element in the
 * array.
 */
db.JSON().Set("employee_profile:nicol", "$.skills", "[]");
db.JSON().ArrAppend("employee_profile:nicol", "$.skills", "python");
db.JSON().Get("employee_profile:nicol", "$.skills");

/*
 * JSON.ARRINDEX key path value [start [stop]]
 * O(N)
 * Search for the first occurrence of a JSON value in an array.
 */
db.JSON().ArrIndex("employee_profile:nicol", "$.skills", "python");
db.JSON().ArrIndex("employee_profile:nicol", "$.skills", "java");
```

### Jedis

```java
/*
 * JSON.SET key path value
 * O(M+N) where M is the original size and N is the new size
 * Set the JSON value at path in key.
 */
jedis.jsonSet("employee_profile:nicol", Path2.ROOT_PATH,
        "{\"name\":\"nicol\",\"age\":24,\"single\":true,\"skills\":[]}");
jedis.jsonSet("employee_profile:nicol", Path2.of("$.name"),
        "\"Nicol\"");

/*
 * JSON.GET key [path [path ...]]
 * O(N)
 * Return the value at path in JSON serialized form
 */
jedis.jsonGet("employee_profile:nicol", Path2.ROOT_PATH);

/*
 * JSON.ARRAPPEND key [path] value [value ...]
 * O(1) for each value added, O(N) for multiple values added where N is the size
 * of the key
 * Append the value(s) to the array at path in key after the last element in the
 * array.
 */
jedis.jsonSet("employee_profile:nicol", Path2.of("$.skills"),
        "[]");
jedis.jsonArrAppend("employee_profile:nicol", Path2.of("$.skills"), "\"python\"");
jedis.jsonGet("employee_profile:nicol", Path2.of("$.skills"));

/*
 * JSON.ARRINDEX key path value [start [stop]]
 * O(N)
 * Search for the first occurrence of a JSON value in an array.
 */
jedis.jsonArrIndex("employee_profile:nicol", Path2.of("$.skills"), "\"python\"");
jedis.jsonArrIndex("employee_profile:nicol", Path2.of("$.skills"), "\"java\"");
```

## Search and Query

### CLI

| **Command**  | **Syntax**                                                                                                                        | **Example**                                                                                                | **Output**                      | **Description**                                                                                                                                      |
| :----------- | :-------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------- | :------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------- |
| FT.CREATE    | `FT.CREATE index [ON HASH / JSON] [PREFIX count prefix [prefix ...]] SCHEMA field_name [AS alias] TEXT / TAG / NUMERIC / GEO ...` | `FT.CREATE staff:index ON JSON PREFIX 1 staff: SCHEMA "$.name" AS name TEXT "$.age" AS age NUMERIC`        | `OK`                            | Create an index with the given specification. _Time Complexity: O(K) where K is the number of fields in the document, O(N) for keys in the keySpace_ |
| FT.SEARCH    | `FT.SEARCH index query [RETURN count identifier ...] [SORTBY sortby] [LIMIT offset num]`                                          | `FT.SEARCH staff:index "(@name:'alex')" RETURN 1 $ LIMIT 0 10`                                             | `Matching documents data`       | Search the index with a query, returning either documents or just ids. _Time Complexity: O(N)_                                                       |
| FT.AGGREGATE | `FT.AGGREGATE index query [GROUPBY nargs property ...] [REDUCE function nargs arg ...] [SORTBY nargs ...]`                        | `FT.AGGREGATE staff:index "(@age:[(18 +inf])" GROUPBY 1 @age REDUCE COUNT_DISTINCT 1 @name AS staff_count` | `Aggregated results by age`     | Run a search query on an index, and perform aggregate transformations on the results.                                                                |
| FT.INFO      | `FT.INFO index`                                                                                                                   | `FT.INFO staff:index`                                                                                      | `Index configuration and stats` | Return information and statistics on the index. _Time Complexity: O(1)_                                                                              |
| FT.DROPINDEX | `FT.DROPINDEX index [DD]`                                                                                                         | `FT.DROPINDEX staff:index`                                                                                 | `OK`                            | Dropping existing index. _Time Complexity: O(1) or O(N) if documents are deleted, where N is the number of keys in the keyspace_                     |

### node-redis

```javascript
const STAFF_INDEX_KEY = "staff:index";
const STAFF_KEY_PREFIX = "staff:";

try {
  /*
       FT.DROPINDEX index [DD]
       Dropping existing index
       O(1) or O(N) if documents are deleted, where N is the number of keys in the keyspace
      */
  await client.ft.dropIndex(STAFF_INDEX_KEY);
} catch (indexErr) {
  console.error(indexErr);
}

/*
   FT.CREATE index [ON HASH | JSON] [PREFIX n] SCHEMA [field type [field type ...]]
   Create an index with the given specification
   O(K) where K is the number of fields in the document, O(N) for keys in the keyspace
 */
const schema: RediSearchSchema = {
  "$.name": {
    type: SchemaFieldTypes.TEXT,
    AS: "name",
  },
  "$.age": {
    type: SchemaFieldTypes.NUMERIC,
    AS: "age",
  },
  "$.isSingle": {
    type: SchemaFieldTypes.TAG,
    AS: "isSingle",
  },
  '$["skills"][*]': {
    type: SchemaFieldTypes.TAG,
    AS: "skills",
    SEPARATOR: "|",
  },
};
await client.ft.create(STAFF_INDEX_KEY, schema, {
  ON: "JSON",
  PREFIX: STAFF_KEY_PREFIX,
});

//-------addStaffEntries for search
await client.json.set("staff:1", ".", {
  name: "Bob",
  age: 22,
  isSingle: true,
  skills: ["NodeJS", "MongoDB", "React"],
});
await client.json.set("staff:2", ".", {
  name: "Alex",
  age: 45,
  isSingle: true,
  skills: ["Python", "MySQL", "Angular"],
});
//------

/*
    FT.SEARCH index query
    Search the index with a query, returning either documents or just ids
    O(N)
    */

const query1 = "*"; //all records
const query2 = "(@name:'alex')"; // name == 'alex'
const query3 = "( (@isSingle:{true}) (@age:[(18 +inf]) )"; //isSingle == true && age > 18
const query4 = "(@skills:{NodeJS})";
const searchResult = await client.ft.search(
  STAFF_INDEX_KEY,
  query1, //query2, query3, query4
  {
    RETURN: ["name", "age", "isSingle"],
    LIMIT: {
      from: 0,
      size: 10,
    },
  }
);
console.log(JSON.stringify(searchResult));
//{"total":1,"documents":[{"id":"staff:2","value":{"name":"Alex","age":"45","isSingle":"1"}}]}

/*
    FT.AGGREGATE index query
    Run a search query on an index, and perform aggregate transformations on the results

    FT.AGGREGATE staff:index "(@age:[(10 +inf])"
      GROUPBY 1 @age
        REDUCE COUNT 0 AS userCount
      SORTBY 1 @age
      LIMIT 0 10
    */
const aggregateResult = await client.ft.aggregate(
  STAFF_INDEX_KEY,
  "(@age:[(10 +inf])",
  {
    STEPS: [
      {
        type: AggregateSteps.GROUPBY,
        properties: ["@age"],
        REDUCE: [
          {
            type: AggregateGroupByReducers.COUNT,
            AS: "userCount",
          },
        ],
      },
      {
        type: AggregateSteps.SORTBY,
        BY: "@age",
      },
      {
        type: AggregateSteps.LIMIT,
        from: 0,
        size: 10,
      },
    ],
  }
);
console.log(JSON.stringify(aggregateResult));
//{"total":2,"results":[{"age":"22","userCount":"1"},{"age":"45","userCount":"1"}]}
//----

/*
    FT.INFO index
    Return information and statistics on the index
    O(1)
    */
const infoResult = await client.ft.info(STAFF_INDEX_KEY);
console.log(infoResult);
/**
     {
        indexName: 'staff:index',
        numDocs: '2',
        maxDocId: '4',
        stopWords: 2
        ...
     }
     */
```

### redis-py

```python
try:
    r.ft('idx-employees').dropindex()
except:
    pass

# FT.CREATE index [ON HASH | JSON] [PREFIX count prefix [prefix ...]] SCHEMA field_name [AS alias] TEXT | TAG | NUMERIC | GEO | VECTOR | GEOSHAP [SORTABLE [UNF]] [NOINDEX] [ field_name [AS alias] TEXT | TAG | NUMERIC | GEO | VECTOR | GEOSHAPE [ SORTABLE [UNF]] [NOINDEX] ...]
# O(K) where K is the number of fields in the document, O(N) for keys in the keyspace
# Creates a new search index with the given specification.
schema = (TextField('$.name', as_name='name', sortable=True), NumericField('$.age', as_name='age', sortable=True),
          TagField('$.single', as_name='single'), TagField('$.skills[*]', as_name='skills'))

r.ft('idx-employees').create_index(schema, definition=IndexDefinition(
    prefix=['employee_profile:'], index_type=IndexType.JSON))

# FT.INFO index
# O(1)
# Return information and statistics on the index.
r.ft('idx-employees').info()

# FT.SEARCH index query
# O(N)
# Search the index with a textual query, returning either documents or just ids
r.ft('idx-employees').search('Nicol')
r.ft('idx-employees').search("@single:{false}")
r.ft('idx-employees').search("@skills:{python}")
r.ft('idx-employees').search(Query("*").add_filter(NumericFilter('age', 30, 40)))
r.json().arrappend('employee_profile:karol', '$.skills', 'python', 'java', 'c#')
r.ft('idx-employees').search(Query("@skills:{java}, @skills:{python}"))

# FT.AGGREGATE index query
# O(1)
# Run a search query on an index, and perform aggregate transformations on the results, extracting statistics etc from them
r.ft('idx-employees').aggregate(aggregations.AggregateRequest("*").group_by('@age',
                                                                            reducers.count().alias('count')).sort_by("@age")).rows

r.ft('idx-employees').aggregate(aggregations.AggregateRequest("@skills:{python}").group_by('@skills',
                                                                                           reducers.tolist('@name').alias('names'))).rows
```

### NRedisStack

```csharp
try
{
    /*
     * FT.DROPINDEX index [DD]
     * O(1)
     * Deletes an index and all the documents in it.
     */
    db.FT().DropIndex("idx-employees");
}
catch
{
    // Index not found
}

/*
 * FT.CREATE index [ON HASH | JSON] [PREFIX count prefix [prefix ...]] SCHEMA
 * field_name [AS alias] TEXT | TAG | NUMERIC | GEO | VECTOR | GEOSHAP [SORTABLE
 * [UNF]] [NOINDEX] [ field_name [AS alias] TEXT | TAG | NUMERIC | GEO | VECTOR
 * | GEOSHAPE [ SORTABLE [UNF]] [NOINDEX] ...]
 * O(K) where K is the number of fields in the document, O(N) for keys in the
 * keyspace
 * Creates a new search index with the given specification.
 */
db.FT().Create("idx-employees", new FTCreateParams()
                                    .On(IndexDataType.JSON)
                                    .Prefix("employee_profile:"),
                                new Schema()
                                    .AddTextField(new FieldName("$.name", "name"), sortable: true)
                                    .AddNumericField(new FieldName("$.age", "age"), sortable: true)
                                    .AddTagField(new FieldName("$.single", "single"))
                                    .AddTagField(new FieldName("$.skills[*]", "skills")));

/*
 * FT.INFO index
 * O(1)
 * Returns information and statistics on the index.
 */
db.FT().Info("idx-employees");

/*
 * FT._LIST
 * O(1)
 * Returns a list of all existing indexes.
 */
db.FT()._List();

/*
 * FT.SEARCH index query
 * O(N)
 * Search the index with a textual query, returning either documents or just ids
 */
db.FT().Search("idx-employees", new Query("@name:{nicol}"));
db.FT().Search("idx-employees", new Query("@single:{false}"));
db.FT().Search("idx-employees", new Query("@skills:{python}"));
db.FT().Search("idx-employees", new Query().AddFilter(new NumericFilter("@age", 30, 40)));
db.JSON().ArrAppend("employee_profile:karol", "$.skills", "python", "java", "c#");
db.FT().Search("idx-employees", new Query("@skills:{java}, @skills:{python}"));

/*
 * FT.AGGREGATE index query
 * O(1)
 * Run a search query on an index, and perform aggregate transformations on the
 * results, extracting statistics etc from them
 */
db.FT().Aggregate("idx-employees", new AggregationRequest("@age:[20 40]")
                                    .GroupBy("@age", Reducers.Count().As("count"))
                                    .SortBy(new SortedField("@age", SortedField.SortOrder.ASC)));
db.FT().Aggregate("idx-employees", new AggregationRequest("@skills:{python}")
                                    .GroupBy("@skills", Reducers.ToList("@name").As("names")));
```

### Jedis

```java
try {
    jedis.ftDropIndex("idx-employees");
} catch (Exception e) {
    // Index not found
}

/*
 * FT.CREATE index [ON HASH | JSON] [PREFIX count prefix [prefix ...]] SCHEMA
 * field_name [AS alias] TEXT | TAG | NUMERIC | GEO | VECTOR | GEOSHAP [SORTABLE
 * [UNF]] [NOINDEX] [ field_name [AS alias] TEXT | TAG | NUMERIC | GEO | VECTOR
 * | GEOSHAPE [ SORTABLE [UNF]] [NOINDEX] ...]
 * O(K) where K is the number of fields in the document, O(N) for keys in the
 * keyspace
 * Creates a new search index with the given specification.
 */
Schema schema = new Schema()
        .addSortableTextField("$.name", 1.0).as("name")
        .addSortableNumericField("$.age").as("age")
        .addTagField("$.single").as("single")
        .addTagField("$.skills[*]").as("skills");

IndexDefinition def = new IndexDefinition(IndexDefinition.Type.JSON)
        .setPrefixes("employee_profile:");

jedis.ftCreate("idx-employees", IndexOptions.defaultOptions().setDefinition(def), schema);

/*
 * FT.INFO index
 * O(1)
 * Returns information and statistics on the index.
 */
jedis.ftInfo("idx-employees");

/*
 * FT._LIST
 * O(1)
 * Returns a list of all existing indexes.
 */
jedis.ftList();

/*
 * FT.SEARCH index query
 * O(N)
 * Search the index with a textual query, returning either documents or just ids
 */
jedis.ftSearch("idx-employees", "Nicol");
jedis.ftSearch("idx-employees", "@single:{false}");
jedis.ftSearch("idx-employees", "@skills:{python}");
jedis.ftSearch("idx-employees", "*",
        FTSearchParams.searchParams().filter(new NumericFilter("age", 30, 40)));
jedis.jsonArrAppend("employee_profile:karol", Path2.of("$.skills"), "\"python\"", "\"java\"", "\"c#\"");
jedis.ftSearch("idx-employees", "@skills:{java}, @skills:{python}");

/*
 * FT.AGGREGATE index query
 * O(1)
 * Run a search query on an index, and perform aggregate transformations on the
 * results, extracting statistics etc from them
 */
jedis.ftAggregate("idx-employees", new AggregationBuilder()
        .groupBy("@age", Reducers.count().as("count")).sortBy(new SortedField("@age", SortOrder.ASC)))
        .getRows();
jedis.ftAggregate("idx-employees", new AggregationBuilder("@skills:{python}")
        .groupBy("@skills", Reducers.to_list("@name").as("names")))
        .getRows();
```
