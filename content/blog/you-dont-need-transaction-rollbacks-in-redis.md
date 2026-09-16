---
title: "You Don’t Need Transaction Rollbacks in Redis"
linkTitle: "You Don’t Need Transaction Rollbacks in Redis"
url: "/blog/you-dont-need-transaction-rollbacks-in-redis/"
description: "Redis features two main mechanisms for executing multiple operations atomically: MULTI/EXEC transactions and Lua scripts. One peculiarity of transactions in Redis that often trips up newcomers is..."
date: 2020-05-04
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Redis   · Published 4 May 2020 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

Redis features two main mechanisms for executing multiple operations atomically: MULTI/EXEC transactions and Lua scripts. One peculiarity of transactions in Redis that often trips up newcomers is the absence of a rollback mechanism. In my tenure as a Developer Advocate at Redis, I’ve talked to a few engineers with traditional SQL backgrounds who found this troubling, so with this blog I want to share my opinion on the subject, and argue that you don’t need rollbacks in Redis.

## MULTI/EXEC transactions

Transactions in Redis start with the MULTI command. Once it’s sent, the connection switches mode and all subsequent commands sent through the connection will be queued by Redis instead of being immediately executed, with the exception of DISCARD and EXEC (which will instead cause the transaction to abort or commit, respectively). Committing the transaction means executing the previously queued commands.

MULTI

SET mykey hello

INCRBY counter 10

EXEC

Transactions (and Lua scripts) ensure two important things:

1. Other clients won’t see a partial state—meaning that all clients will see the state either before the transaction was applied, or after.
1. In case of a node failure, once Redis restarts, it will reload either the whole transaction or none of it from the [AOF file](https://redis.io/topics/persistence).

One last basic thing to keep in mind about transactions: Redis will continue to serve other clients even when a MULTI transaction has been initiated. Redis will stop applying other clients’ commands only briefly when the transaction gets committed by calling EXEC. This is very different from SQL databases, where transactions engage various mechanisms within the DBMS to provide varying degrees of isolation assurances, and where clients can read values from the database while performing the transaction. In Redis, transactions are “one shot”—in other words, just a sequence of commands that get executed all at once. So, how do you create a transaction that depends on the data present in Redis? For this purpose, Redis implements WATCH, a command for performing optimistic locking.

**Optimistic locking with WATCH**

Let me show you on a practical level why you can’t read values from Redis while in a transaction:

MULTI

SET counter 42

GET counter

EXEC

If you run this series of commands in redis-cli, the reply from “GET counter” will be “QUEUED”, and the value “42” will be returned only as a result of calling EXEC, alongside the “OK” returned from executing the SET command.

To write a transaction that depends on data read from Redis, you must use WATCH. Once run, the command will ensure that the subsequent transaction will be executed only if the keys being WATCHed have not changed before EXEC gets called.

For example, this is how you would implement an atomic increment operation if INCRBY did not exist:

WATCH counter

GET counter

MULTI

SET counter <the value obtained from GET + any increment>

EXEC

In this example, we first create a WATCH trigger over the “counter” key, then we GET its value. Notice how GET happens before we start the transaction’s body, meaning it will be executed immediately and it will return the key’s current value. At this point, we start the transaction using MULTI and apply the change by computing on the clientside what the new value of “counter” should be.

If multiple clients were trying to concurrently apply this same transaction to the “counter” key, some transactions would be automatically discarded by Redis. At this point it would usually be the client’s job to retry the transaction. This is similar to SQL transactions, where higher isolation levels will occasionally cause the transaction to abort, leaving the client the task of retrying it.

## Lua scripts

While WATCH can be very useful for performing articulated transactions, it’s usually easier and more efficient to use a Lua script when you need to perform multiple operations that depend on data in Redis. With a Lua script, you send the logic to Redis (in the form of the script itself) and have Redis execute the code locally, instead of pushing data to the client as we were doing in the example above. This is faster for several reasons, but here’s the big one: Lua scripts can read data from Redis without needing optimistic locking.

This how the previous transaction would be implemented as a Lua one-liner:

EVAL "redis.call('SET', KEYS[1], tonumber(redis.call('GET', KEYS[1]) or 0) + tonumber(ARGV[1]))" 1 counter 42

There are, in my opinion, a couple of reasonable situations where you might legitimately prefer transactions with optimistic locking over Lua:

1. The keys your transaction depends on are not modified frequently, meaning that you are confident optimistic locking will almost never abort transactions.
1. You depend on a lot of logic written on the client side—or maybe a third-party service—so there is no easy way to move that logic to a Lua script.

Unless both these points are true for your application, I recommend you choose Lua over WATCH.

## Errors in transactions

To recap: MULTI/EXEC transactions (without WATCH) and Lua scripts never get discarded by Redis, while MULTI/EXEC + WATCH will cause Redis to abort transactions that depend on values changed after the corresponding keys were WATCHed. Lua scripts are more powerful than simple (i.e. WATCH-less) transactions because they can also read values from Redis, and are more efficient than “WATCHed” transactions because they don’t require optimistic locking to read values.

The key point about optimistic locking is that when a WATCHed key is changed, the whole transaction is discarded immediately when the client commits it using EXEC. Redis has a main, single-threaded command execution loop, so when the transaction queue is being executed no other command will run. **This means that Redis transactions have a true **[**serializable isolation level**](https://en.wikipedia.org/wiki/Isolation_(database_systems)#Serializable), and also means that no rollback mechanism is required to implement WATCH.

But what happens when there’s an error in a transaction? The answer is that Redis will continue to execute all commands and report all errors that happened.

To be more precise, there are some types of errors that Redis can catch before the client calls EXEC. One basic example are blatant syntax errors:

MULTI

GOT key? *(NOTE: Redis has no GOT command and, after season 8, it never will)*

EXEC


But not all errors can be discovered by inspecting the command syntax, and those could cause the transaction to misbehave. As an example:

MULTI

SET counter banana

INCRBY counter 10

EXEC

The example above will be executed but the INCRBY command will fail because the “counter” key doesn’t contain a number. This type of error can be discovered only when running the transaction (nevermind that in this simplified example we are the ones setting the wrong initial value).

This is the moment where one might say that rollbacks would be nice to have. I might agree if not for two considerations:

1. The snapshotting mechanism required to implement rollbacks would have a considerable computational cost. That extra complexity wouldn’t sit well with Redis’ philosophy and ecosystem.
1. Rollbacks can’t catch all errors. In the example above, we set “counter” to “banana” in order to show a blatant error, but in the real world the process that used the “counter” key in the wrong way might instead have deleted it, or put in a credit-card number, for example. Rollbacks would add a considerable amount of complexity and would still not fully solve the problem.

The second point is particularly important because it also applies to SQL: SQL DBMSs offer many mechanisms to help protect data integrity, but even they can’t completely protect you from programming errors. **On both platforms, the burden of writing correct transactions remains on you.**

## Rollbacks in SQL DBMSs

If that seems to conflict with your experience using SQL databases, let’s look at the difference between relying on errors to enforce constraints vs. relying on errors to protect the data from bugs in your code.

It’s common practice in SQL to use indexes to implement constraints on the data and rely on those indexes on the client side for correctness. A common example would be to add a “UNIQUE” constraint to a “username” column to ensure that each user has a different username. At that point clients would try to insert new users and expect the insertion to fail when another user with the same name already exists.

This is a perfectly legitimate use of a SQL database, but relying on the constraint to implement application logic is very different than expecting rollbacks to protect you from mistakes in the transaction logic itself.

At [AWS re:Invent 2019](/blog/redis-labs-at-aws-reinvent-2019/), when an attendee asked me “Why doesn’t Redis have rollbacks?” my answer was based on enumerating why people use rollbacks in SQL. In my opinion, there are only two main reasons to do so:

**First reason to use rollbacks: concurrency**

Most common SQL databases are multithreaded applications, and when a client requests a high isolation level, the DBMS prefers to trigger an exception rather than stop serving all other clients. This makes sense for the SQL ecosystem because SQL transactions are “chatty”: a client locks a few rows, reads a few values, computes what changes to apply, and finally commits the transaction.

In Redis, transactions are not meant to be as interactive. The single-threaded nature of the main event loop in Redis ensures that while the transaction is running, no other command gets executed. This ensures that all transactions are truly serializable without violating the isolation level. When a transaction uses optimistic locking, Redis will be able to abort it before executing any command in the transaction queue—which doesn’t require a rollback.

**Second reason to use rollbacks: leveraging index constraints**

In SQL, it’s common to use index constraints to implement logic in the application. I mentioned UNIQUE, but the same applies to foreign key constraints and more. The premise is that the application relies on the database to have been properly configured and leverages index constraints to implement the logic in an efficient way. But I’m sure everyone has seen applications misbehave when somebody forgets to put in a UNIQUE constraint, for example.

While SQL DBMSs do a great job of protecting data integrity, you can’t expect to be protected from all errors in your transaction code. There is a significant class of errors that don’t violate type checking or index constraints.

Redis has no built-in index system (Redis modules are a different story and don’t apply here). To force uniqueness, for example, you would use a [Set](https://redis.io/commands#set) (or equivalent) data type. This means the correct way to express an operation in Redis looks different from the equivalent in SQL. Redis’ data model and execution model are different enough from SQL that the same logical operation would be expressed in different ways depending on the platform, but the application must always be in sync with the state of the database.

An application that tries to INCRBY a key that contains a non-numeric value is the same as an application that expects a SQL schema inconsistent with what’s on the database. If you have gremlins in your Redis database making unexpected changes, [lock them out using access control lists (ACLs](/blog/getting-started-redis-6-access-control-lists-acls/)).

## Redis vs. SQL

If you come from a SQL background, you might understandably be surprised by how transactions work in Redis. Given that NoSQL has demonstrated that relational databases are not the only valuable model for storing data, don’t make the mistake of assuming that any diversion from what SQL offers is inherently inferior. SQL transactions are chatty, based on a multi-threaded model and interoperate with other subsystems to leverage rollbacks in case of failures. In contrast, Redis transactions are more focused on performance and there is no indexing subsystem to leverage for enforcing constraints. Because of these differences, the transaction-writing “style” that you use in Redis is fundamentally different from the SQL one.

**This means that the lack of rollbacks in Redis doesn’t limit expressiveness**. All reasonable SQL transactions can be rewritten to a functionally equivalent Redis transaction, but it’s not always trivial to do in practice. Reasoning about a problem originally articulated in SQL in Redis requires you to think about your data in a different way, and you also need to account for the different execution model.

Finally,** it’s true that rollbacks can be useful to protect your data from programming errors, but they are not meant to be a solution to that problem**. As a [multi-model database](/redis-enterprise/multi-model/) based on a key-value structure, Redis doesn’t offer the same level of “type checking” ease that SQL does, but there are techniques to help with that, as Kyle Davis, Head of Developer Advocacy at Redis, explained in this recent blog post: [Bullet-Proofing Lua Scripts in RedisPy.](/blog/bullet-proofing-lua-scripts-in-redispy/)

That said, your applications need to be in sync with what’s in the database, both when using a relational database and when using Redis. For Redis, the utility of rollbacks would not outweigh the costs in terms of performance and additional complexity. If you ever wondered how Redis can be so much faster than other databases, here’s yet another reason why.
