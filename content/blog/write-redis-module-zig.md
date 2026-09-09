---
title: "How to Write a Redis Module in Zig"
linkTitle: "How to Write a Redis Module in Zig"
url: "/blog/write-redis-module-zig/"
description: "Update (May 9th 2019): Changed the code to account for the new release of Zig version 0.4.0"
date: 2019-01-23
blogCategories:
- "How To and Tutorials"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 23 January 2019 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/2a71332a0c21e631f3c2b4fc81cdfbdfed3eb41d-1600x840.webp)

***Update (May 9th 2019):**** Changed the code to account for the new release of Zig version 0.4.0*

Everybody has a Redis instance somewhere in their stack or at the very least knows Redis. However not everybody knows that Redis supports modules: custom extensions that add new commands, data types, and functionalities to a Redis database.

Need a new data structure? Full-text search? Want to store graph data in Redis?

All of this is already possible with [existing modules](https://redis.io/modules) that are being actively developed by the Redis community.

If you have a specific use case that is not yet covered and you need the performance that Redis offers, you might be interested in learning how to write a module.

The default way of building a module is using C and compiling it as a shared dynamic library.

If you know C, then all is good, but if you don’t, setting up a brand new C project can feel a bit overwhelming. It’s easy to forget one small detail about the compilation process and end up with a binary that segfaults for no apparent reason.

It can get even more frustrating when you have to deal with cross-platform compilation, for example when you’re developing on macOS or Windows, and you intend to deploy on Linux.

### Introducing Zig

[Zig](https://ziglang.org) is a brand new language developed by [Andrew Kelley](https://twitter.com/andy_kelley?lang=en) that puts a lot of emphasis in bringing modern comfort to the C way of writing programs. The result is a language that allows you to build fully C ABI compatible binaries while having access to language features such as advanced error checking by the compiler, better metaprogramming facilities, generics, optionals, error types, and more.

### How modules interact with Redis

Redis modules are object files that can be dynamically loaded by Redis at runtime. A module expects access to a few functions exposed by Redis that allow it to operate in the Redis ecosystem. The only interface that the module is required to implement, is a function called RedisModule_OnLoad(), which is generally used to register in Redis all the new commands that the module offers.

This means that you can use any language that can be compiled to a C-compatible dynamic library, and Zig makes it particularly easy while allowing you to use more modern abstractions in your private code.

Let’s write a very simple module called testmodule that implements a test.hello command, which only sends “Hello World!” to the client when called.

### Writing modules – The C Way

In C, the most straightforward way of writing a Redis module is to download a copy of the redismodule.h header file from [Redis’ official repository (unstable branch)](https://github.com/antirez/redis/blob/unstable/src/redismodule.h), include it at the beginning of your code, and write the module.

A header file is the C way of describing the interface of another piece of code that won’t actually be part of the compilation phase, letting the compiler know if any unimplemented symbols are being used incorrectly.

This is how our module code looks like in C:

```python
#include "redismodule.h"

int HelloWorld_Command(RedisModuleCtx *ctx, RedisModuleString **argv, int argc) {
    RedisModule_ReplyWithSimpleString(ctx, "Hello World!");
    return REDISMODULE_OK;
}

int RedisModule_OnLoad(RedisModuleCtx *ctx, RedisModuleString **argv, int argc) {
    if (RedisModule_Init(ctx,"testmodule",1,REDISMODULE_APIVER_1)
        == REDISMODULE_ERR){
        return REDISMODULE_ERR;
    }
    
    if (RedisModule_CreateCommand(ctx,"test.hello", HelloWorld_Command, 
        "readonly", 0, 0, 0) == REDISMODULE_ERR){
        return REDISMODULE_ERR;
    }
    
    return REDISMODULE_OK;
}

```

Other than the header file import, the script only contains two function implementations: HelloWorld_Command() and RedisModule_OnLoad().

As mentioned before, RedisModule_OnLoad() is invoked by Redis when loading the module, while HelloWorld_Command() is our sample command

Now that we have written a simple HelloWorld module in C, let’s look at how can we do this in Zig.

### Writing modules – The Zig Way

Before we start writing in Zig, you may be wondering, how do you import all the definitions of a C header file if you’re not writing in C?

That already seems a big blocker, but Zig makes integrating with C projects a priority and so it offers two ways of quickly importing a header file.

The fastest method is to just call [@cInclude()](https://ziglang.org/documentation/master/#Import-from-C-Header-File), which allows to import a header file directly, while the second is to use a compiler command to translate the C code to Zig (which is what @cInclude() does under the hood).

While immediate, in our case the first option is not the best for a few reasons, the most important being that Zig is a safe language, and automatic translation of the header file results in Zig assuming that every pointer could be null, and thus requiring the user to explicitly check before any operation can be done.

### Null values in Zig

According to many, [null pointers are one of the worst things to happen to computer science](https://www.lucidchart.com/techblog/2015/08/31/the-worst-mistake-of-computer-science/).

In Zig, values that can be null are wrapped in a generic container type called [Optional](https://ziglang.org/documentation/master/#Optionals).

Optional types are becoming very widespread: [Swift](https://developer.apple.com/documentation/swift/optional), [Kotlin](https://kotlinlang.org/docs/reference/null-safety.html), [Rust](https://doc.rust-lang.org/std/option/), all have them, just to name a few.

When you have an optional value (be it a pointer or anything else), before being able to access it, you have to [unwrap](https://ziglang.org/documentation/master/#Attempt-to-Unwrap-Null) it. This enforces explicit checks over any potential null value without having to check indiscriminately or risk an unhandled exception.

Unfortunately, null is a valid value for pointers in C, and because of that there is no way of specifying if a pointer is allowed to be null or not. This means that when importing function signatures from a header file, every formal argument that is a pointer, is going to be translated in a Zig optional pointer, which is the correct and safe choice, but makes using the imported symbols unnecessarily verbose, if you know for certain that a given pointer is never going to be null.

To show you explicitly, this is what HelloWorld_Command() would look like when importing the header file directly:

```python
export fn HelloWorld_Command(ctx: ?*redis.RedisModuleCtx, argv: ?[*]?*redis.RedisModuleString, argc: c_int) c_int {
    _ = redis.RedisModule_ReplyWithSimpleString.?(ctx, c"Hello World!");
    return redis.REDISMODULE_OK;
}

```

Making sure we don’t try to dereference a null pointer is very good, but it is a bit verbose if we know that a pointer will never be null, as it is the case with formal arguments of Redis commands, for example.

The solution is to use:

$ zig translate-c redismodule.h

This will obtain a Zig file equivalent to the header file and change a few type signatures to spare ourselves some unnecessary optional unwrapping.

To make it easier, you can [download an already cleaned up copy of redismodule.zig ](https://github.com/kristoff-it/zig-redismodule)(compatible with Zig 0.4.0 and Redis 5.0). Just know that is not officially supported and that you might have to get your hands dirty in case something doesn’t work.

This is then what the module looks like when written in Zig:

```python
const redis = @import("./redismodule.zig");

export fn HelloWorld_Command(ctx: *redis.RedisModuleCtx, argv: [*c]*redis.RedisModuleString, argc: c_int) c_int {
    _ = redis.RedisModule_ReplyWithSimpleString(ctx, c"Hello World!");

    return redis.REDISMODULE_OK;
}

export fn RedisModule_OnLoad(ctx: *redis.RedisModuleCtx, argv: [*c]*redis.RedisModuleString, argc: c_int) c_int {
    if (redis.RedisModule_Init(ctx, c"testmodule", 1, redis.REDISMODULE_APIVER_1) 
        == redis.REDISMODULE_ERR) {
        return redis.REDISMODULE_ERR;
    } 

    if (redis.RedisModule_CreateCommand(ctx, c"test.hello", HelloWorld_Command, 
        c"readonly", 0, 0, 0) == redis.REDISMODULE_ERR) {
        return redis.REDISMODULE_ERR;
    }

    return redis.REDISMODULE_OK;

}

```

As you can see, the translation is very straightforward, the main difference being that the symbols imported are stored inside the redis constant.

Another thing of note is that C often has unwieldy interop with other languages because of inconsistencies in how strings are represented in memory. In C, strings are pointers to null-terminated byte arrays, while other languages have a variety of different representations. Zig itself does not use C-style strings but it makes easy to produce them by prefixing `c` to a string literal, as you can see in our Zig code.

This simple example shows that C code has a mostly straightforward translation to Zig, but don’t think that you then end up with a “C with extra steps”. There are many features that you will surely appreciate when you move into writing a real module that moves data around.

Consult the [official Zig documentation](https://ziglang.org/documentation/master/) for a complete list of features.

### Building a Zig module

Zig has a dedicated build command for shared libraries:

$ zig build-lib -dynamic module.zig

If you need to cross-compile for 64-bit Linux:

$ zig build-lib -dynamic module.zig –target-os linux –target-arch x86_64

To try out your module you can use the following commands in redis-cli or through the [Redis Enterprise GUI](https://docs.redis.com/latest/rs/developing/modules/installing/):

> MODULE LOAD /path/to/module.so.0 (or libmodule.0.0.0.dylib on macOS)


OK

> test.hello

Hello World!

### In conclusion

We saw how Zig makes integrating with the C ecosystem a reasonably enjoyable experience. You have great shortcuts such as @cInclude() and c”Hello World” as well as very practical escape hatches for when you need more control, like with the translate-c compiler command.

The result is a language that gives you more safety guarantees and a dead simple building process that even supports cross-compilation in a single command.

The only thing that now remains to know, is what you can actually do inside a Redis module.

The official website contains a [list of published modules](https://redis.io/modules) and the [full module API reference](https://redis.io/docs/latest/develop/reference/modules/modules-api-ref/).

If you want to share a Redis module written by you that you think the community would appreciate, send a pull request to [antirez/redis-doc](https://github.com/antirez/redis-doc) to have it added to the list.

Happy hacking!
