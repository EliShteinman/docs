---
title: "The SET command is a strange beast"
linkTitle: "The SET command is a strange beast"
url: "/blog/set-command-strange-beast/"
description: "The Helicoprion is a now extinct but strange animal that roamed the seas of the early Permian. It looks more or less similar in both size and shape to a contemporary Great White Shark. Most likely,..."
date: 2019-05-13
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2026-09-01
hidden: true
---

*By Redis   · Published 13 May 2019 · updated 1 September 2026*

![Blog tile image](/images/blog/c7af871aa5afedd94ab0d40e643e0aa4e1221a8b-1600x1116.webp)

The Helicoprion is a now extinct but strange animal that roamed the seas of the early Permian. It looks more or less similar in both size and shape to a contemporary Great White Shark. Most likely, it was a formidable predatory of the seas. The thing that set it apart was that it had a “Tooth-whorl,” which is somewhat akin to having a shark-toothed circular saw located inside the lower jaw. Seems like it would be a good idea, but evolution had a different idea and we don’t have any existent animals like that. An evolutionary dead end.

In some ways the Redis [SET](https://redis.io/docs/latest/commands/set/) command is like the Helicoprion, but it still roams the waters of Redis servers all over the globe. It is a very early command with some unusual features that seem like a good idea but can prove to be dangerous yet deeply useful when correctly used.

On the other hand, the SET command seems to be as plain and ordinary as anything. We use it as one of the first commands when learning and we use it for doing a simple test to make sure Redis is working properly. I can’t tell you how many times I’ve typed the command:

> SET foo bar

So, that is nothing exotic on the surface. But is it hiding something?

### SET: Destroyer of data

Coming back to our simple SET example. Let’s add some more context:

> UNLINK foo

(integer) 1

> HSET foo bar 123

(integer) 1

> SET foo bar

OK

Did you catch the weirdness here with SET? The existing key *foo* was of type hash (due to the [HSET](https://redis.io/commands/hset)), but when I ran SET immediately afterwards it still accepted the command. This is actually deeply weird compared to other Redis commands. Let’s take the same commands but flip the order of the last two:

> UNLINK foo

(integer) 1

> SET foo bar

OK

> HSET foo bar 123

(error) WRONGTYPE Operation against a key holding the wrong kind of value

You can see that SET disregards the existence or type of key and always writes. Hashes, on the other hand, throw an error when confronted with a non-empty key of a different type. The same holds true for all data types except for Strings and specifically the SET command and a few variants ([PSETEX](https://redis.io/commands/psetex), [SETEX](https://redis.io/commands/setex), [MSET](https://redis.io/commands/mset)). Take this, for example:

> HSET foo bar 123

(integer) 1

> APPEND foo bar

(error) WRONGTYPE Operation against a key holding the wrong kind of value

> INCR foo

(error) WRONGTYPE Operation against a key holding the wrong kind of value

> SETBIT foo 1 1

(error) WRONGTYPE Operation against a key holding the wrong kind of value

> BITFIELD foo SET u8 0 1

(error) WRONGTYPE Operation against a key holding the wrong kind of value

> INCRBY foo 1

(error) WRONGTYPE Operation against a key holding the wrong kind of value

> INCRBYFLOAT foo 1

(error) WRONGTYPE Operation against a key holding the wrong kind of value

> SETRANGE foo 1 barbar

(error) WRONGTYPE Operation against a key holding the wrong kind of value

SETNX and SET…NX (more on this later) are an interesting side note, they will SET if the key does not exist, returning a 1 if it was set and 0 if not. So, it doesn’t type check, but rather presence checks.

All in all, SET just doesn’t care about types. It always writes, very little can stand in its path.

### One TYPE three types.

If you’ve been around the block in Redis a few times you know that you can retrieve the type of data stored at a key by using the [TYPE](https://redis.io/commands/type) command. So, for example, let’s return to *foo*:

> SET foo bar

OK

> TYPE foo

string

Easy enough. You set the value “bar” at the key *foo*. Now, let’s see something else:

> SET foo 1234

OK

> TYPE foo

String

> GETRANGE foo 2 3

"34"

So, you might think that the number 1234 is being stored as characters, and you’d be more/less correct. However, there is more to this story:

> INCR foo

(integer) 1235

> GETRANGE foo 2 3

"35"

This illustrates that Redis understands characters as text and numbers – you can think of it as a form of loose typing. But it gets weird:

> SET foo "hello world"

OK

> INCR foo

(error) ERR value is not an integer or out of range

Obviously, Redis cannot increment a non-number. But there are more details to cover. Redis also understands float values. Take this example:

> SET foo 1.2

OK

> INCR foo

(error) ERR value is not an integer or out of range

> INCRBYFLOAT foo 0.8

"2"

> INCR foo

(integer) 3

You can see the initial value is put in as a float and therefore the [INCR](https://redis.io/commands/incr) (which is for integers) would not work. However, [INCRBYFLOAT](https://redis.io/commands/incrbyfloat) does work. This changes the value to a whole number that can be used by the previous not allowed INCR command.

### One command, many arguments

The other thing that is distinctive about the command is the ability to supply two categories of optional arguments: one category for expiration and the other for existence checking. Let’s take a look at the first category: expiration arguments.

For most commands, if you want to expire a key immediately, you need to issue the [EXPIRE](https://redis.io/commands/expire) or [PEXPIRE](https://redis.io/commands/pexpire) immediately afterwards, most often in a [MULTI](https://redis.io/commands/multi) / [EXEC](https://redis.io/commands/exec) transaction. For example:

> MULTI

OK

> SADD baz alpha beta gamma

QUEUED

> EXPIRE baz 10

QUEUED

> EXEC

1) (integer) 3

2) (integer) 1

This ensures that you cannot be interrupted between your [SADD](https://redis.io/commands/sadd) and your EXPIRE command. You know that immediately after the EXEC you’ll have a set that expires in 10 seconds. With SET, however, you can do this without a transaction.

> SET foo bar EX 10

OK

Alternately, you can use PX instead of EX to expire in units of milliseconds instead of seconds. It’s a handy shorthand that can also be expressed with SETEX and PSETEX. I think of these commands as shortcuts only – they exchange a few keystrokes in your application and a few bytes to and from the server for a little less readability and flexibility.

The other category of arguments, NX / XX, controls how SET works with existent or non-existent data. The NX key sets a value only if the key does not exist. So, take this example:

> UNLINK foo

(integer) 0

> SET foo 1234 NX

OK

> GET foo

"1234"

> SET foo 5678 NX

(nil)

> GET foo

"1234"

You can see that the 4th command actually doesn’t do anything because the key *foo* already exists. This has numerous uses: setting default values and without overwriting existing data, preventing accidental SETS when user input is part of a key, etc.

The inverse of this is the XX command. This only sets a value when the key already exists.

> UNLINK foo

(integer) 1

> SET foo 1234 XX

(nil)

> set foo 1234

OK

> SET foo 5678 XX

OK

This can be used to confine writes to expressly defined keys. One thing this doesn’t do is type check. So XX will still overwrite a key of another type, as long as it exists.

### So, is SET dangerous / bad / not suggested?

Absolutely not. SET is fundamental to the operation of many excellent patterns in Redis. However, it has a number of features that are fundamentally different from the rest of Redis. It is important to know how these features work in order to make proper assumptions about how to structure your keyspace and operate Redis in your application.
