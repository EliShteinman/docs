---
title: "Distributed Events"
linkTitle: "Distributed Events"
url: "/glossary/distributed-events/"
description: "The Pub/Sub messaging of Redis can be extended to create interesting distributed events. Let’s say we have a structure that is stored in a hash but we want to update clients of it only when a..."
lastmod: 2025-06-30
---

*updated 30 June 2025*

The Pub/Sub messaging of Redis can be extended to create interesting distributed events. Let’s say we have a structure that is stored in a hash but we want to update clients of it only when a particular field exceeds a numerical value as defined by the subscriber. We’ll listen to a pattern of channels, and only then, fetch the hash at *status*. In this example, we’re only interested in update_status when it is between 5 and 9.

To change the value of *status/error_level*, we’ll have a subroutine that runs two commands sequentially or in a [MULTI/EXEC block](https://redis.io/topics/transactions). The first command sets the level and the second command publishes the notice, with the value encoded in the channel itself.

When a message is received our client application switches to an alternate client and issues the [HGETALL](https://redis.io/commands/hgetall) command:

We can then use this to, say, update a local variable of a long-running process. This can allow multiple instances of the same process to “share” data in live way.

What’s nice about this pattern vs. just using Pub/Sub is that when the process restarts, it can simply grab the entire status hash and start listening. The changes will then be synchronized across any number of processes. Should the instance become disconnected from the Redis server, as part of the reconnection the server can grab the status hash and re-start listening.
