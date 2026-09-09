---
title: "Lua Helpers"
linkTitle: "Lua Helpers"
url: "/glossary/lua-helpers/"
description: "Redis can do amazing things just from redis-cli—and even more between Redis and your language of choice. But occasionally there are behaviors that cannot be efficiently or safely achieved with a..."
lastmod: 2025-06-30
---

*updated 30 June 2025*

Redis can do amazing things just from redis-cli—and even more between Redis and your language of choice. But occasionally there are behaviors that cannot be efficiently or safely achieved with a client/server architecture—the logic needs to be run on the database layer. This is where [Lua](https://www.lua.org/) comes in. Lua is baked into Redis as a scripting language. With Lua you can execute code atomicly in Redis without transmission overhead to and from the client.

An example of task like this is appending a value to a hash field. While Redis can easily append a value to a string key with APPEND, no such command exists to append a value to hash field. While you could try to achieve by fetching the value of the field with the client, appending the new string to the value and resetting the hash field, it’s a bad idea. As this is not atomic, the possibility exists that the during the time you are appending a value to the hash field another client could swoop in and change it and then the original client would write over the new update.

As you can see in line 2, the update to “goodbye” is lost. We can use a Lua helper to get around this issue and eliminate the send/receive overhead of moving the value to the client.

In any text editor, we need to create the Lua script. We’ll name it ‘happend.lua’:

In the first line, we’re creating a local variable called original that will store the current value of the hash key stored at the first passed key with the field being the first non-key argument. It’s important to understand that Lua scripts make a differentiation between keys and non-key arguments when executing.

In the second line, we’re calling HSET on the same key and field then concatenating the original value with the second non-key argument. This is being returned back to Redis, so we’ll retain the original return value of HSET.

While you can directly execute Lua scripts with the EVAL command, this can get rather messy and inefficient. Redis has a built-in script cache that allows for pre-loading the script then referencing it via the SHA1 hash digest of the script. To load the script from the command line we’ll use cat and redis-cli.

*(Note: if your script is even different by one character, you’ll have an entirely different hash string)*

Now, in redis-cli we can use EVALSHA to invoke our script and do an append:

Let’s break down the EVALSHA command. The first argument is the SHA1 digest of the script we created with SCRIPT LOAD. The second argument is the number of keys. In this case we are manipulating a single key, so it’s 1. The third argument is the key we’re manipulating. The third argument is the field we want to manipulate and finally the fourth argument is the value we’re appending to the field.

Because the append is happening inside the Lua script, our scenario from above cannot happen Lua scripts are executed in a fully synchronous and atomic fashion.

While Lua can be a very useful problem-solver, it should be undertaken with care. Scripts do block the server and can yield an unresponsive database. In sharded situations, the scripts try to keep all operations to a single server to avoid cross lot errors.
