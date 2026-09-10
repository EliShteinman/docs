---
title: "On Types and Transactions"
linkTitle: "On Types and Transactions"
url: "/blog/on-types-and-transactions/"
description: "Transactions in any database are intimidating. It requires a level of understanding beyond just what is stored, but also when it is stored. Unlike the happy world that results when countless layers..."
date: 2019-06-04
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2026-09-01
hidden: true
mirrored: true
---

*By Redis   · Published 4 June 2019 · updated 1 September 2026*

![Blog tile image](/images/site-mirror/2e1bd5ff6bc43ba94c881be573ca73aa2a3b6997-1384x924.webp)

Transactions in any database are intimidating. It requires a level of understanding beyond just what is stored, but also when it is stored. Unlike the happy world that results when countless layers of abstraction can shield you from complexity, transactions require you to go deeper. Redis is not unusual in this regard. In fact, its entirely different way of thinking about transactions causes a lot of people to say it doesn’t have transactions at all. Redis has them, just with an approach that’s totally different from the rollbacks you’ve probably grown up with.

To view transactions at 10,000 ft, you have to understand a few things about Redis. One is that it is single-threaded (well, with a list of exceptions that is perhaps continuing to grow). This means that if it’s doing something, that’s all it’s doing. Of course with Redis, “doing something” is best measured in milli- or nano-seconds. Second, keep in mind that Redis has tunable durability, with some options providing very good durability and some that are totally ephemeral. This obviously has an effect on transactions. Third, it lacks rollbacks, but can fail a transaction if a key changes before it starts. This inverted way of controlling transactions lets you pull data back to the client, and evaluate it logically to ensure that the data did not change before the transaction started.

The biggest tripping point for most people is that individual commands in transactions can have errors. This can create situations where each command is executed but one or more of the command executions has errors. Knowing this is key to understanding and controlling for these situations.

First, let’s take a look at the distinction between a syntax error and a semantic error in Redis. A syntax error is just that – the syntax is wrong in a way that is known without access to the data. For example, sending a command that doesn’t exist or violating the argument key/value sequence. Syntax errors result in a transaction never starting.

Take this example:

127.0.0.1:6379> MULTI

OK

127.0.0.1:6379> STE foo bar

(error) ERR unknown command `STE`, with args beginning with: `foo`, `bar`,

127.0.0.1:6379> EXEC

(error) EXECABORT Transaction discarded because of previous errors.

Redis knows that STE is not a command, so it can throw the whole thing out without ever even having to evaluate the underlying data, and will reject the entire MULTI/EXEC block. Other syntactical errors that are caught immediately by Redis include argument count and (some) argument pattern problems. These transaction errors are very safe — with [MULTI](https://redis.io/commands/multi), all subsequent commands are queued up to run when the [EXEC](https://redis.io/commands/exec) is called, so anything that triggered an EXECABORT was never run.

The next, and more expansive, category is semantic transaction errors, which behave differently than syntactical errors. They come about when Redis cannot catch the error statically, generally requiring Redis to evaluate the underlying data. A classic example of this behavior is this:

127.0.0.1:6379> SET foo "hello world"

OK

127.0.0.1:6379> MULTI

OK

127.0.0.1:6379> INCR foo

QUEUED

127.0.0.1:6379> SET bar baz

QUEUED

127.0.0.1:6379> EXEC

1) (error) ERR value is not an integer or out of range

2) OK

Obviously, a real-world competent developer would never intentionally try to increment the string “hello world.” But when you think about an end-to-end application where user input is accepted, expecting a number but not validated as a number, this example becomes more realistic. The other insidious thing about this is that the second [SET](https://redis.io/docs/latest/commands/set/) command was executed but the [INCR](https://redis.io/commands/incr) was not. This is not what most developers want nor expect from the transaction. The good news is that this type of error can be controlled for with the use of the [WATCH](https://redis.io/commands/watch) command. WATCH enables you to observe keys for changes, and if they occur, it will immediately send an error to the client. This is very powerful and allows you to bring data to the client and evaluate it. In this case, you can evaluate if foo is able to be incremented (a.k.a. a whole number).

Take a look at this pseudocode:

1 > SET foo 1234

2 > WATCH foo

3 If watchError goto 2 else continue

4 > GET foo

5 If the result of line 4 is a not a number, throw an error, otherwise continue

6 > MULTI

7 > INCR foo

8 > SET bar baz

9 > EXEC

Now, if foo is changed by any connected client between lines 3 and 9 (but not during 9, which allows for the transaction itself to change watched data), the process will jump back to 2. After line 4, it will look at the contents of foo in the application and determine if it is possible to increment. Because it will immediately retry if a change happens, this ensures that you won’t get any errors due to the contents of foo being wrong.

This relates to how Redis works with whole numbers/integers vs. floating point numbers. [I’ve talked about this a little before](/blog/set-command-strange-beast/), but basically if your data is a floating point number then you have to use [INCRBYFLOAT](https://redis.io/commands/incrbyfloat) instead of INCR or [INCRBY](https://redis.io/commands/incrby). However, if the value is ever exactly equal to a whole number, then you can use INCR or INCRBY once again. It’s important to note that you can increment non-floating point numbers by non-floating point numbers using INCRBYFLOAT and it doesn’t affect anything. In essence, the INCR family of commands will never create a “1.0.” In a MULTI / EXEC situation, it’s safer to use INCRBYFLOAT over INCR or INCRBY, as it won’t create errors. The only reason to use INCR or INCRBY in this case is to ensure an error is thrown if you have a floating number – in that case, you have to use WATCH anyway.

One note about evaluating the data in this way: it’s not free. If you’re pulling numbers to the client side, the evaluation is minimal. But let’s say you have an unknown key and you evaluate it for suitability, but instead of 5-7 bytes that make up a number, you have a 500 MB binary blob. That’s going to take a while to push over the wire and evaluate. It’s an edge case, but it’s something to keep in mind.

This same pattern (WATCH / MULTI / EXEC) can be useful to guard against command / type mismatches (a.k.a. WRONGTYPE), turning up in the results of your transaction. With the INCR problem, you had to track if a String contained data that could be INCR’ed or INCRBYFLOAT’ed using some sort of client-side evaluation of the data. Alternatively, you can be much more straightforward and just use the TYPE command to evaluate the data’s type instead of the data itself (nicely avoiding the unexpected 500 MB evaluation).

Let’s take a look at how this might work:

1 > HSET foo bar 1234

2 > WATCH foo

3 If watchError goto 2 else continue

4 > TYPE foo

5 If the result of line 4 is a not “hash”, throw an error, otherwise continue

6 > MULTI

7 > HSET foo baz helloworld

8 > HLEN foo

9 > EXEC

In this case, you know that your [HSET](https://redis.io/commands/hset) and HLEN commands will work, since you’ve verified the type and it hasn’t changed by the time you run the EXEC. Of course, there is the matter of the [HINCRBY/HINCRBYFLOAT](https://redis.io/commands/hincrbyfloat) command, where you’ll need to combine the previous technique using [HGET](https://redis.io/commands/hget) instead of [GET](https://redis.io/docs/latest/commands/get/) to evaluate the field for INCR-ability.

Interestingly, [BITFIELD](https://redis.io/commands/bitfield) has controls for handling out-of-bounds values. You can either wrap around or saturate based on the type declared in the command itself, or you can use the FAIL option. This, strangely, doesn’t produce an error but ignores the INCR, leaving the value as before. BITFIELD, however, does have another gotcha. The command is quite complex and Redis only does some basic syntax checking, so if you pass it the wrong syntax, this will not be evaluated at the time it’s added to the transaction, but when the command is executed inside the transaction. This results in a syntax error that doesn’t cancel the transaction and is returned in the values. The only way to guard against these types of errors is to ensure that your syntax is correct at the client level before you throw it into a transaction.

By and large, Redis requires no initialization step for data. To some, this is alarming, but for most people, they get it. If a key is blank and you add data to it, the newly created data structure is defined by the command used to add data. This has slowly started to change with the advent of modules, which make this convention less definite. For example, RedisGraph requires you to add some nodes and relationships before you can query the graph.

Take this example:

> MULTI

OK

> GRAPH.QUERY mygraph "MATCH (r:Rider)-[:rides]->(t:Team) WHERE t.name = 'Yamaha' RETURN r,t"

QUEUED

> LPUSH teamqueries Yamaha

QUEUED

> EXEC

1) (error) key doesn't contains a graph object.

2) (integer) 1

Indeed, you can see this behavior as well with Redis Streams. For example:

> MULTI

OK

> XGROUP CREATE my-stream my-consumer-group $

QUEUED

> LPUSH my-stream-groups my-consumer-group

QUEUED

> EXEC

1) (error) ERR The XGROUP subcommand requires the key to exist. Note that for CREATE you may want to use the MKSTREAM option to create an empty stream automatically.

2) (integer) 1

Thankfully, these issues are resolved rather simply, by using the WATCH, TYPE, MULTI/EXEC pattern described above. You would just check the type matches (with these examples) and match graphdata or stream.

Redis transactions with MULTI and EXEC are really not that complicated. However, you do need to watch out for a few gotchas to make sure your transaction behaves as expected. If you take anything away from this article, remember that you can make bulletproof Redis transactions by assuming nothing about the type, contents or existence of the referenced keys.
