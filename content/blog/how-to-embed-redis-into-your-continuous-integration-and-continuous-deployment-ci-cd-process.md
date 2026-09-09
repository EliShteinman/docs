---
title: "How to Embed Redis into Your Continuous Integration and Continuous Deployment (CI/CD) Process"
linkTitle: "How to Embed Redis into Your Continuous Integration and Continuous Deployment (CI/CD) Process"
url: "/blog/how-to-embed-redis-into-your-continuous-integration-and-continuous-deployment-ci-cd-process/"
description: "Earlier this week, I wrote about how Redis can benefit distributed development teams by helping them release new features safely and roll them back with minimal impact when required. Today, I’ll..."
date: 2019-04-26
blogCategories:
- "How To and Tutorials"
authors:
- "Shabih Syed"
lastmod: 2025-03-27
hidden: true
---

*By Shabih Syed, Shabih is a Sr. Director of Product Marketing at Redis Labs. He has 13+ years of experience with software development, product management and marketing of cloud-based data management & application integration platforms. Most recently he led product marketing at Liaison Technologies (now OpenText) and has worked for HP and IBM before that. Shabih is based out of NYC. · Published 26 April 2019 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/67a983cf6c2345801a976ed72c2ff177da42df14-512x574.webp)

Earlier this week, I wrote about how Redis can benefit distributed development teams by helping them release new features safely and roll them back with minimal impact when required. Today, I’ll dive into specific details about how feature toggles, feature context and error logs can enhance your continuous integration and continuous deployment (CI/CD) process.

### Feature Toggling with Redis

“Feature toggling” is a set of patterns that help you deliver new functionality to application users rapidly but safely. Feature toggles are also referred to as feature flags, feature bits or feature flippers.

![Redis - Figure 5: Feature toggles stored in redis_ent_1](/images/site-mirror/27c2c020572c51bc1088ea7555801f5c8da53de8-300x239.webp)

*Figure 5: Feature toggles stored in redis_ent_1*

In Redis Enterprise, it’s very easy to structure a toggle strategy using the native [Redis HASH](/redis-best-practices/data-storage-patterns/object-hash-storage/) data structure.

With [Redis-cli](https://redis.io/download) or any [Redis client](https://redis.io/docs/latest/develop/connect/clients/) for the language of your choice, you can create HASH keys (such as “useNewAlgorithm”) with values that set a toggle flag, release number, developer names, an override flag, etc.

Using this type of data structure, you can set up as many feature toggles in Redis as you need. Your application can then look these up at runtime to check the real-time flag status and metadata.

Using this type of data structure, you can set up as many feature toggles in Redis as you need. Your application can then look these up at runtime to check the real-time flag status and metadata.

```python
HSET useNewAlgorithm toggle "True" releaseNum "2.5" fingerprint "John S" override "fb-user"

```

```python
HGETALL useNewAlgorithm

```

Response:


```python
 1) "name"
 2) "John Smith"
 3) "email"
 4) "john.smith@jsmith.com"
 5) "phone"
 6) "718-111-2222"
 7) "authType"
 8) "fb-user"
 9) "creationTime"
10) "Fri Apr 5 09:51:05 GMT-5"

```

### Feature Context with Redis

“Feature context” is a dynamic routing decision based on certain context, such as which user is making the request. It can be read directly from session management, which is a popular use case for Redis.

![](/images/site-mirror/9b4facb00c0980759106ed64e410332b324785f9-300x255.webp)

*Figure 6: Feature context (session stores) stored in redis_ent_1*

Again, using the native [Redis HASH](/redis-best-practices/data-storage-patterns/object-hash-storage/) data structure and [Redis-cli](https://redis.io/download) (or any [Redis client](/resources/redis-clients/)), you can store session data in keys and look it up at runtime to read real-time values.

For example, in Figure 6, the ‘sessionAuthorized’ method checks if a user has logged in with Facebook using the ‘authType” value stored in the session key.

```python
HSET session:4156e021:1234 name "John Smith" email "john.smith@jsmith.com" phone "718-111-2222" authType "fb-user" creationTime "Fri Apr 5 09:51:05 GMT-5"


```

```python
HGETALL session:4156e021:1234

```

Response:


```python
 1) "name"
 2) "John Smith"
 3) "email"
 4) "john.smith@jsmith.com"
 5) "phone"
 6) "718-111-2222"
 7) "authType"
 8) "fb-user"
 9) "creationTime"
10) "Fri Apr 5 09:51:05 GMT-5"

```

Feel free to read up more on session stores [here](/blog/cache-vs-session-store/).

### Using Redis for a Fast, Searchable Error Database

An “error database” is a centralized data store for errors reported during runtime. Errors can be stored in [RediSearch](/redis-enterprise/technology/redis-search/), a powerful text search and secondary indexing engine, which provides a fast search for looking them up. The version of RediSearch that comes with Redis Enterprise supports scaling across many servers, allowing it to easily grow to billions of documents on hundreds of servers.

You can push any errors reported during runtime into RediSearch, along with other useful information from the feature toggle and feature context, which will help with the triage process.

Create search indexes with [Redis-cli](https://redis.io/download) or any [Redis client.](https://redis.io/docs/latest/develop/connect/clients/)

For example, let’s create a new index called “toggle_errors_db” to store all errors reported whenever a feature toggle is used.

```python
FT.CREATE toggle_errors_db SCHEMA toggleName TEXT toggleValue TEXT fingerPrint TEXT exceptionBody TEXT

```

Let’s add some data to this index with a new key using the format:useNewAlgorithm:03-12-19-10-32-05

```python
FT.ADD toggle_errors_db useNewAlgorithm:03-12-19-10-32-05 1.0 FIELDS toggleName 'useNewAlgorithm' toggleValue 'True' fingerPrint 'John S,Stephanie B' exceptionBody 'Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: 5 at Exceptions.Unchecked_Demo.main(Unchecked_Demo.java:8)'


```

Try a search on this index for any object with keywords, e.g. search for developer name: John

```python
FT.SEARCH toggle_errors_db John

```


Response:

```python
1) (integer) 1
2) "useNewAlgorithm:03-12-19-10-32-05"
3) 1) "fingerPrint"
   2) "John S,Stephanie B"
   3) "exceptionBody"
   4) "Exception in thread \"main\" java.lang.ArrayIndexOutOfBoundsException: 5 at Exceptions.Unchecked_Demo.main(Unchecked_Demo.java:8)"
   5) "toggleValue"
   6) "True"
   7) "toggleName"
   8) "useNewAlgorithm"

```

Search for feature toggle name: useNewAlgorithm

```python
FT.SEARCH toggle_errors_db useNewAlgorithm

```

Response:

```python
1) (integer) 1
2) "useNewAlgorithm:03-12-19-10-32-05"
3) 1) "fingerPrint"
   2) "John S,Stephanie B"
   3) "exceptionBody"
   4) "Exception in thread \"main\" java.lang.ArrayIndexOutOfBoundsException: 5 at Exceptions.Unchecked_Demo.main(Unchecked_Demo.java:8)"
   5) "toggleValue"
   6) "True"
   7) "toggleName"
   8) "useNewAlgorithm"

```

### Logs Database

A “logs database” is a centralized data store that tracks log messages. You can use Redis to store a recent list of log messages, which will give you a snapshot view of your logs at any time.

![Figure 8: Logs stored in redis_ent_3](/images/site-mirror/a15c28cd17a84c3ff063cfe76981f317dfcd088d-300x236.webp)

*Figure 8: Logs stored in redis_ent_3*

To keep a recent list of logs, you can [LPUSH](https://redis.io/commands/lpush) log messages to a LIST and then trim that LIST to a fixed size.

Later, if you want to read those log messages, just perform a simple LRANGE to fetch them.

SEVERITY = {

logging.DEBUG: 'debug',

logging.INFO: 'info',

logging.WARNING: 'warning',

logging.ERROR: 'error',

logging.CRITICAL: 'critical',

}

SEVERITY.update((name, name) for name in SEVERITY.values())
**//Set up a mapping that should help turn most logging severity levels into something consistent**

def log_recent(conn, name, message, severity=logging.INFO, pipe=None):

severity = str(SEVERITY.get(severity, severity)).lower()

**//Actually try to turn a logging level into a simple string.**

destination = 'recent:%s:%s'%(name, severity)

**//Create the key that messages will be written to.**

message = time.asctime() + ' ' + message

**//Add the current time so that we know when the message was sent.**

pipe = pipe or conn.pipeline()

pipe.lpush(destination, message)

**//Add the message to the beginning of the log list.**

pipe.ltrim(destination, 0, 99)

**//Trim the log list to only include the most recent 100 messages.**

pipe.execute()

### Get Started with Redis Enterprise

Each of these techniques brings an opportunity to take your continuous updates to the next level and minimize the time and headaches inherent in managing development for large-scale apps with frequent releases. Of course, Redis Enterprise is a great way to bring more power and flexibility to the whole CI/CD process. Thankfully, creating a Redis cluster with Redis Enterprise Pro (which includes the RediSearch module and features data persistence) is easy and free.

[Get Started with Redis Enterprise](/get-started/) today.
