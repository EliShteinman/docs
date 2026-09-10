---
title: "Triggers and Functions: Bring Code Closer to Your Data"
linkTitle: "Triggers and Functions: Bring Code Closer to Your Data"
url: "/blog/introducing-triggers-and-functions/"
description: "Developers can use Redis to build and maintain real-time applications. You can create JavaScript functions that automatically execute code on data changes directly in the Redis database, and thus..."
date: 2023-08-15
blogCategories:
- "Uncategorized"
authors:
- "Thomas Caudron"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Thomas Caudron, Contributor · Published 15 August 2023 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/47332548fb454cdc2f83aefd5a0b6701156b5b58-772x550.webp)

**Developers can use Redis to build and maintain real-time applications. You can create JavaScript functions that automatically execute code on data changes directly in the Redis database, and thus ensure a lower latency.**

In general, applications handle business logic operation, sending code for execution to the database. This is a slow process, because code flows from a client into the server each time a function is executed. The developer is responsible for maintaining code consistency across all applications that access the same database, whether the code is simple requests or complex data operations, and many times code is repeated across applications.

Following the Redis manifesto guideline, *We are against complexity, *we had to take action and to find a solution to those challenges.

Four years ago, we introduced RedisGears, our first programmability model within the platform. Developers wrote and executed scripts where data lived. However, the scripts were ephemeral, provided by each client, and that could lead to inconsistencies.

Following that direction, in Redis 7.0 we introduced the initial implementation of the scripting method with *functions*. Functions boosted usability and durability because they are part of the database, inheriting the level of replication and persistence of the data.

And now, we are proud to present the next step in programmability. With Redis 7.2, we introduce *triggers and functions*. These enhance Redis’ programmability, expand server-side capabilities, improve how and when functions are executed in the database, and facilitate the execution of complex business logic directly where the data lives.

## The basics of triggers and functions

Triggers and functions is a new generation of programmability available through Redis Stack. It allows developers to program, store, and automatically execute JavaScript code on data changes directly in a Redis database.

This capability lets developers define events (called triggers) to execute functions closer to the data. That is, developers define business logic that executes in response to database events or commands. That speeds up the code and related interactions, because there is no wait to bring code from clients into the database.

It also speeds up reaction time to other events in Redis, such as keyspace notifications that are not handled in real time with other means such as [Publish and Subscribe](https://redis.io/docs/interact/pubsub/) (Pub/Sub) events.

Triggers and functions handle the distribution within a clustered database, installing the libraries on each shard and executing the functions based on where the key lives.

We are also introducing *remote functions*. Remote functions allow you to perform read actions that can access data from any slot, even in a clustered database, so all your data is accessible from each function.

### It uses JavaScript, the most popular programming language

Redis uses Lua for scripting and functions. There are [many benefits](https://opensource.com/article/22/11/lua-worth-learning) to Lua, such as code reusability, but it is not a commonly used language among professional developers. According to the [2022 StackOverflow developer survey](https://survey.stackoverflow.co/2022#most-popular-technologies-language-prof), only 3.2% of developers use Lua in a professional capacity.

In contrast, two thirds of developers use JavaScript. Using a well-known language lowers the adoption barrier for new Redis developers. It’s one less thing to learn.

### Application code is easier to support and maintain

Another benefit of triggers and functions is that it reduces the complexity of managing business logic across multiple applications.

When multiple applications access the same database, developers have to coordinate how applications process data in a consistent manner. It is common to duplicate code in each application to validate data, to enrich search results, or to update the database when another application makes changes.

With triggers and functions, there is no longer a need to duplicate code on multiple applications. Code always executes in the same way, on-demand or initiated by an event in the database.

### Database events process in real time

Until now, reacting to database events within Redis required developers to rely on the Pub/Sub mechanism. While Pub/Sub has a lot of advantages, it isn’t always the right choice. In particular, Pub/Sub is not real-time. A client has to actively listen to the events; if the client is not listening, the events are lost.

Now developers can register keyspace triggers that execute based on a key prefix and event type. The trigger can be executed in an atomic way so that no other Redis event is processed between the event and the business logic.

## Show me how it’s done

It’s always easier to understand things with a practical example. Here, we introduce registering a function and a trigger. A function is executed when it is called via the TFCALL command; a trigger is executed based on the events in Redis.

The prologue defines that we use the js engine, the library name is lib, and the minimum required Triggers and Functions API is version 1.0.

```javascript
#!js name=lib api_version=1.0

```

Next, we create a function that returns the result of a Redis command. The client gives access to execute Redis commands within our function. The data event contains the keys and arguments that can be provided when running the function.

```javascript
function answer(client, data) {
	return client.call(“ping”);
}

```

The Redis global variable allows you to register triggers and functions, and to log to the log file. We register the function with a name with which we call it when it executes.

```javascript
redis.registerFunction(‘playPingPong’, answer);

```

The full JavaScript file looks like this.

```javascript
#!js name=lib api_version=1.0

function answer(client, data) {
	return client.call(‘ping’);
}

redis.registerFunction(‘playPingPong’, answer);


```

Save this as lib.js.

Then we register our function in triggers and functions using the TFUNCTION LOAD command. The TFUNCTION LOAD command also distributes the library in a clustered database.

```bash
> redis-cli  -x TFUNCTION LOAD < ./lib.js
OK

```

Now we can execute the function using the TFCALL command. The command gets the library name and the function name separated by a period.

```bash
>redis-cli TFCALL lib.playPingPong 0
“PONG”

```

By doing so, you successfully created, registered, and triggered a function in the Redis database.

We can extend this example with a keyspace trigger. We add a new registration that reacts to keys that are prefixed with 'fellowship:'. Add this code at the end of the lib.js file.

```javascript
function addLastUpdatedField(client, data) {
	if(data.event == ‘hset’) {
	var currentDateTime = Date.now();
	client.call(‘hset’, data.key, ‘last_updated’, currentDateTime.toString());
}
}

redis.registerKeySpaceTrigger(‘addLastUpdated’, 'fellowship:', addLastUpdatedField);

```

Use the TFUNCTION LOAD command with the REPLACE argument to update an existing library. The TFUNCTION LOAD REPLACE command immediately updates all the clients using the Redis database, and they start using the new business logic.

```bash
>redis-cli -x TFUNCTION LOAD REPLACE . < ./lib.js
OK

```

To test the new keyspace trigger, create a new key starting with fellowship: and check the fields using RedisInsight. The keyspace trigger is executed with the command, so the *last_updated* field is already added when the key is created.

![Check the results in RedisInsight](/images/site-mirror/7f2b152e653ab173627df483dd76531df3c35ae5-1577x1045.webp)

*Check the results in RedisInsight*

## Sound cool? Try it for yourself

Join the public preview of triggers and functions with Redis Stack 7.2. Get started with Redis Stack in the cloud by creating a database on [Redis Enterprise Cloud](/try-free/) in the fixed tier within the Google Cloud/Asia Pacific (Tokyo) or AWS/Asia Pacific (Singapore) region, or deploy a self-managed instance from our [download center](/downloads/).

The General Availability for triggers and functions is planned for Redis 8. This will include feedback received from the preview users, as well as additional features, such as timed triggers and more debugging options.

Comments and feedback are welcome on the [Redis mailing list](https://groups.google.com/g/redis-db?pli=1).
