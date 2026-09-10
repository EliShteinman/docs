---
title: "C and Redis"
linkTitle: "C and Redis"
url: "/tutorials/develop/c/"
description: "Version 1.0.0 marks the first stable release of hiredis. Install the build tools you need, then download and compile hiredis from source."
group: "For developers"
aliases:
- "/tutorials/develop-c/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> Install [hiredis](https://github.com/redis/hiredis), the recommended C Redis client library, compile it with `make`, then use `redisConnect` and `redisCommand` to talk to your Redis server from any C program.

## What you'll learn

- How to install and compile the hiredis C client library
- How to connect to a Redis server from C
- How to execute Redis commands and handle replies
- Where to go next with async hiredis and Redis Cluster

## Prerequisites

- A C compiler (`gcc` or `clang`)
- `make` and `wget`
- Package manager: `brew` (macOS) or `apt` (Linux)
- A running Redis server

## How do I install hiredis?

Version 1.0.0 marks the first stable release of hiredis. Install the build tools you need, then download and compile hiredis from source.

Install the build prerequisites:

```bash
# macOS
brew install gcc make

# Debian / Ubuntu
sudo apt update && sudo apt install -y gcc make wget
```

Start a Redis server if you don't already have one running:

```bash
redis-server
```

Download and compile hiredis:

```bash
wget https://github.com/redis/hiredis/archive/master.zip
unzip master.zip
cd hiredis-master
make
sudo make install
```

## How do I connect to Redis from a C program?

Create a file called `redistest.c` with the following code. It opens a connection with `redisConnect`, sends a `PING` command, prints the reply, and cleans up.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <hiredis/hiredis.h>

int main(int argc, char **argv) {
    redisReply *reply;
    redisContext *c;

    c = redisConnect("127.0.0.1", 6379);
    if (c == NULL || c->err) {
        if (c) {
            printf("Connection error: %s\n", c->errstr);
            redisFree(c);
        } else {
            printf("Connection error: can't allocate redis context\n");
        }
        return 1;
    }

    /* PING the server */
    reply = redisCommand(c, "PING %s", "Hello World");
    printf("RESPONSE: %s\n", reply->str);
    freeReplyObject(reply);

    redisFree(c);
    return 0;
}
```

## How do I compile and run my C Redis program?

Compile the code with `gcc`, linking against hiredis:

```bash
gcc redistest.c -o redistest -I /usr/local/include/hiredis -lhiredis
```

Run the program:

```bash
./redistest
RESPONSE: Hello World
```

## What about async connections?

hiredis also provides an asynchronous API for non-blocking I/O. The async interface integrates with event loops such as `libevent`, `libev`, and `libuv`, making it suitable for high-throughput or embedded C applications that need to handle many concurrent Redis operations. See the [hiredis async documentation](https://github.com/redis/hiredis#asynchronous-api) for details.

## Next steps

- Explore [hiredis on GitHub](https://github.com/redis/hiredis) for the full API reference
- Try [hiredis-cluster](https://github.com/Nordix/hiredis-cluster), a C client library for Redis Cluster
- Check out [hiredispool](https://github.com/aclisp/hiredispool) for connection pooling and auto-reconnect
- Browse the [Redis command reference](https://redis.io/docs/latest/commands/) to see all available commands
