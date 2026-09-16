---
title: "Writing Redis Modules"
linkTitle: "Writing Redis Modules"
url: "/blog/writing-redis-modules/"
description: "I’ve been using Redis for about six years now, and over the years I’ve exploited its few data types to do some pretty versatile things such as geographical queries, text search, machine learning..."
date: 2016-08-02
blogCategories:
- "Tech"
authors:
- "Dvir Dukhan"
lastmod: 2025-03-04
hidden: true
mirrored: true
---

*By Dvir Dukhan · Published 2 August 2016 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

![Redis Enterprise modules around a database](/images/site-mirror/6a121721b932e0aff48482412da0ec13ddda1114-300x200.webp)

I’ve been using Redis for about six years now, and over the years I’ve exploited its few data types to do some pretty versatile things such as geographical queries, text search, machine learning and more.

But over the years, I can’t even count the number of times I’ve found myself (as did many other users) wishing that Redis would have this or other data structure, command or capability it is lacking. Not having them forced user to resort to less elegant or less efficient methods to achieve our goals with Redis. And while Lua was a step in the right direction, it has its limitations.

But all that is changing, since Redis now has a (not yet stable) module system that allows developers to write C libraries, which add new capabilities and data structures to Redis – in speeds similar to normal Redis commands.

I personally think this is the most exciting new feature to hit Redis in a long time, and it will go beyond an API – dramatically shaping the dynamics and the usage of Redis in the years to come.

Over the past couple of months, while Salvatore has been working on the pretty big Modules API, we here at Redis have been busy experimenting with it, creating modules that add things like authentication, [probabilistic data structures](/blog/streaming-analytics-with-probabilistic-data-structures/) and full-text search — all using new data structures and adding new commands to Redis.

So I wanted to share the lessons I’ve learned as a sort of basic guide to writing modules. The [documentation of the API](https://redis.io/documentation#redis-modules-api) is very good, but also very long. So take this guide as a TL;DR guide to module writing.

## 1. Not Your Grandfather’s Lua Script

Let’s start with the basics: Modules are basically C shared libraries (.so files) that Redis can load at runtime or on startup. They can register new commands that Redis doesn’t support, and can access Redis’ data to do their thing. But there are a few key differences that make modules a lot more powerful:

- First of all, the execution of C code for computational functions is orders of magnitude faster, so unless what you’re doing is a small added-logic macro, you should see modules running as fast as Redis itself.
- While Lua scripts can only add functionality on top of existing data structures, modules can create new data types, using any data structure imaginable.
- Lua scripts can only be called with ***EVAL*** and ***EVALSHA***, which makes calling them a bit cumbersome without a proper client library. Modules add commands to Redis that can just be called directly. FOO BAR BAZ— that’s it!
- Unlike Lua, Modules can bind into third party libraries. Think for example about unicode processing, image manipulation or even execution of code on the GPU.
- The API exposed to Redis Modules is much richer than the minimalist API exposed to Lua.

## 2. What’s in a Module

What modules basically contain are command handlers. These are C functions with the following signature:

int MyCommand(RedisModuleCtx *ctx, RedisModuleString **argv, int argc)

The idea is pretty simple, as can be seen from the signature: The function returns an integer, either OK or ERR. Usually returning OK, even if returning an error to the user, is fine.

The command handler accepts a ***RedisModuleCtx**** object. This object is opaque to the module developer, but internally it contains the calling client’s state, and even internal memory management, which we’ll get to later.

Next it receives ***argv*** and ***argc*** which are basically the argument the user has passed to the command being called. The first argument is the name of the call itself, and the rest are simply parsed arguments from the Redis protocol.

Notice that they are received as ***RedisModuleString*** objects, which again, are opaque. They can be converted to normal C strings with zero copy if manipulation is needed.

To activate the module’s commands, the standard entry point for a module is a function called*** RedisModule_OnLoad***. This function tells Redis what commands are in the module and maps them to their handler.

## Let’s Write a Module

OK, let’s write a Redis Module. We’ll focus on a very simple example of a module that implements a new Redis command – ***HGETSET <key> <element> <new value>***. It’s basically a combination of ***HGET*** and ***HSET***, getting the current value in a hash object, and setting a new value instead of it atomically. This is pretty basic, and can be done with a simple transaction or a Lua script, but it has the advantage of being really simple.

**1. Let’s start with a bare command handler:**

int HGetSetCommand(RedisModuleCtx *ctx, RedisModuleString **argv, int argc) {
return REDISMODULE_OK;
}

Again, this currently does nothing, it just returns the OK code. So let’s give it some substance.

**2. Validate the arguments**

Remember, our command is ***HGETSET <key> <element> <new value>***, meaning it will always have four arguments in ***argv***. So let’s make sure this is indeed what happens:

/**
HGETSET <key> <element> <new value>
*/
int HGetSetCommand(RedisModuleCtx *ctx, RedisModuleString **argv, int argc) {
if (argc != 4) {
return RedisModule_WrongArity(ctx);
}
return REDISMODULE_OK;
}

***RedisModule_WrongArity*** will return a standard error to the client in the form of:

(error) ERR wrong number of arguments for ‘get’ command

**3. Activate AutoMemory**

One of the great features of the Redis Modules API is automatic resource and memory management. While the module author can allocate and free memory independently, creating Redis resources is managed, and Redis strings, keys and responses allocated during the handler’s lifecycle are freed automatically, if we call ***RedisModule_AutoMemory***.

RedisModule_AutoMemory(ctx);

**4. Performing a Redis call**

Now we’ll run the first of two Redis calls: ***HGET***. We pass ***argv[1]*** and ***argv[2]*** which are the key and element as the arguments. We use the generic ***RedisModule_Call*** command, which simply allows the module developer to call any existing Redis commands, much like a Lua script.

RedisModuleCallReply *rep =
RedisModule_Call(ctx, “HGET”, “ss”, argv[1], argv[2]);
// And let’s make sure it’s not an error
if (RedisModule_CallReplyType(rep) == REDISMODULE_REPLY_ERROR) {
RedisModule_ReplyWithCallReply(ctx, rep);
return REDISMODULE_ERR;
}

Notice that ***RedisModule_Call***’s third argument, *“ss”*, denotes how Redis should treat the passed variadic arguments to the function. *“ss”* means “two RedisModuleString objects.” Other specifiers are *“c”* for a c-string, *“d”* for double, *“l”* for long, and *“b”* for a c-buffer (a string followed by its length).

Now let’s perform the second Redis call, ***HSET***:

RedisModuleCallReply *srep =
RedisModule_Call(ctx, “HSET”, “sss”, argv[1], argv[2], argv[3]);
if (RedisModule_CallReplyType(srep) == REDISMODULE_REPLY_ERROR) {
RedisModule_ReplyWithCallReply(ctx, srep);
return REDISMODULE_ERR;
}

Which is done much like the ***HGET*** command, except we pass three arguments to it.

**5. Return the results**

In this simple case, we just need to return the result of ***HGET***, or the value before we changed it. This is done using a simple function – ***RedisModule_ReplyWithCallReply***, which forwards the reply object to the client:

RedisModule_ReplyWithCallReply(ctx, rep);
return REDISMODULE_OK;

And that’s it! Our command handler is ready; we just need to register our module and command handler properly.

**6. Initialize the module**

The entry point for all Redis Modules is a function called ***RedisModule_OnLoad***, which the developer has to implement. It registers and initializes the module, and registers its commands with Redis so that they can be called.

Initializing our module works like so:

int RedisModule_OnLoad(RedisModuleCtx *ctx) {
// Register the module itself – it’s called example and has an API version of 1
if (RedisModule_Init(ctx, “example”, 1, REDISMODULE_APIVER_1) == REDISMODULE_ERR) {
return REDISMODULE_ERR;
}

// register our command – it is a write command, with one key at argv[1]
if (RedisModule_CreateCommand(ctx, “example.hgetset”, HGetSetCommand,
“write”, 1, 1, 1) == REDISMODULE_ERR) {
return REDISMODULE_ERR;
}

return REDISMODULE_OK;
}

And that’s about it! Our module is done.

**7. A Word on module building**

All that’s left is to compile our module. I won’t go into the specifics of creating a makefile for it, but what you need to know is that Redis Modules require no special linking. Once you’ve included the “***redismodule.h***” file in your module’s files, and implemented the entry point function, that’s all Redis needs to load your module; any other linking is up to you.

Provided here are the commands needed to compile our basic module with gcc.

On Linux:

$ gcc -fPIC -std=gnu99 -c -o module.o module.c
$ ld -o module.so module.o -shared -Bsymbolic -lc

On OSX:

$ gcc -dynamic -fno-common -std=gnu99 -c -o module.o module.c
$ ld -o module.so module.o -bundle -undefined dynamic_lookup -lc

**8. Loading our module**

Once you’ve built your module, you need to load it. Assuming you’ve downloaded Redis v4 or above, you just run it with the ***loadmodule*** command-line argument:

$ redis-server --loadmodule /path/to/module.so

And that’s it! Redis is now running and has loaded our module. We can simply connect with ***redis-cli*** and run our commands!

## Getting the source

The full source code detailed here can be found in the *example* directory of [RedisModuleSDK](https://github.com/RedisLabsModules/RedisModulesSDK), which also includes a Module project template, makefile, and a utility library with functions automating some of the more boring stuff around writing modules, that are not included in the original API. You do not have to use it, but feel free to.
