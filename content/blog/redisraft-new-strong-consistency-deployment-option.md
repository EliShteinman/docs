---
title: "Introducing RedisRaft, a New Strong-Consistency Deployment Option"
linkTitle: "Introducing RedisRaft, a New Strong-Consistency Deployment Option"
url: "/blog/redisraft-new-strong-consistency-deployment-option/"
description: "RedisRaft (under development) is a new module for open source Redis that makes it possible to operate a number of Redis servers as a single fault-tolerant, strongly consistent cluster. As its name..."
date: 2020-06-23
blogCategories:
- "Company"
authors:
- "Yossi Gottlieb"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Yossi Gottlieb, Chief Architect at Redis Labs · Published 23 June 2020 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/43c082ae3a08f3bc9087ca5c8b4b56a31dc51e47-368x260.webp)

[RedisRaft ](https://github.com/RedisLabs/redisraft)(under development) is a new module for open source Redis that makes it possible to operate a number of Redis servers as a single fault-tolerant, strongly consistent cluster. As its name suggests, it is based on the [Raft consensus algorithm](https://raft.github.io/) and an [open-source C library](https://github.com/willemt/raft) that implements it.

RedisRaft brings a new [strong-consistency with strict serialization](https://jepsen.io/consistency/models/strict-serializable#:~:text=Informally%2C%20strict%20serializability%20(a.k.a.%20PL,B%20in%20the%20serialization%20order) deployment option to Redis and the Redis ecosystem. The new module makes it possible to use Redis along with Redis’ existing clients, libraries, and data types in beyond-cache scenarios requiring a high level of reliability and consistency.

## RedisRaft’s beginnings

RedisRaft started as an experimental “side project” shortly before Redis 5 was released. The Redis module API was introduced in Redis 4, primarily designed to support modules that implement new data types and commands. We wanted to explore how far we could stretch the API, and use modules to extend Redis in even more radical ways. But we also wanted to end up with something useful—a strong consistency deployment option for Redis.

A RedisRaft cluster offers the same level of consistency and reliability expected from reliable, well-known data stores such as ZooKeeper or Etcd. In a nutshell, in RedisRaft:

- Acknowledged writes are guaranteed to be committed and never lost.
- Reads will always return the most up-to-date committed write.

As expected from reliable data stores offering this level of consistency, such guarantees bring trade-offs in performance and availability. In RedisRaft:

- Client operations depend on cluster nodes exchanging messages, so they become bound to network latency.
- Writes must be flushed to disk before completing, so they become bound to disk I/O latency.
- The cluster is available only as long as a majority of the nodes are up, healthy, and able to communicate with each other.

## How RedisRaft works

Once a RedisRaft module is loaded into Redis, it takes over communication between cluster nodes, replication of the Raft log or snapshots, persistence, and so on. The Redis core remains unaware of this and as far as it is concerned, it is operating as a standalone server with no clustering, persistence, or replication.

Setting up a three-node RedisRaft cluster is as easy as starting three Redis servers, as shown here:

redis-server --loadmodule /path/to/redisraft.so

This is how to connect to the first server and create the Raft cluster:

10.0.0.1:6379> RAFT.CLUSTER INIT

OK 989645460313dd2ddb051f033c791222

Then you connect to the other two servers and join them to the cluster:

10.0.0.2:6379> RAFT.CLUSTER JOIN 10.0.0.1:6379

OK

10.0.0.3:6379> RAFT.CLUSTER JOIN 10.0.0.1:6379

OK

## Accessing the cluster

Once RedisRaft is set up, we can write data to our cluster:

10.0.0.1:6379> INCR counter:1

(integer) 1

Receiving a reply shows that our write has been replicated to **at least **a majority of the cluster nodes (2 nodes in our case), and committed to their persistent storage.

Raft is based on a strong-leader concept, which means all client operations should go to the leader node and initiate from it. In this case, our client was indeed connected to the leader, but cluster leadership is dynamic and clients may not necessarily know who the leader is.

Trying the same operation on a follower (non-leader) node creates this response:

10.0.0.3:6379> INCR counter:1

(error) MOVED 10.0.0.1:6379

So as a client, we can now catch this error, re-establish a connection with the leader node as specified, and retry our command.

But what if we don’t want to modify our existing application? Luckily, RedisRaft can also be configured to automatically handle this for us. By enabling *follower proxy mode*, we can have cluster nodes automatically forward our request to the leader and provide the reply when it is available:

10.0.0.3:6379> RAFT.CONFIG SET follower-proxy yes

OK

10.0.0.3:6379> INCR counter:1

(integer) 2

This is much simpler, of course, but impacts latency and network load as hitting a non-leader node creates an extra network hop.

## Cluster changes

When setting up our cluster, we’ve actually performed three distinct operations:

1. Created the cluster on a single node.
1. Added the second node.
1. Added the third node.

RedisRaft cluster configuration is not static, and it is possible to add or remove additional nodes after the cluster has been created and while it’s active.

For example, we may need to replace our third node. First, we join a new node that’s going to replace it. Note that we “add-then-remove” rather than “remove-then-add” to avoid leaving the cluster and our precious data in a degraded redundancy state during the transition:

10.0.0.4:6379> RAFT.CLUSTER JOIN 10.0.0.1:6379

OK

Next, we look up the ID that was randomly assigned to our third node:

redis-cli -h 10.0.0.1 --raw RAFT.INFO | grep 10.0.0.3

node2:id=**1739451728**,state=connected,voting=yes,addr=10.0.0.3,port=6379,

last_conn_secs=3537,conn_errors=0,conn_oks=1

And then we remove it:

10.0.0.1:6379> RAFT.NODE REMOVE 1739451728

OK

## RedisRaft release status

As part of RedisRaft development work, we have been collaborating with Kyle Kingsbury (a.k.a [Aphyr](https://aphyr.com/about)) to analyze and test RedisRaft using [Jepsen](https://jepsen.io/), a well-known framework for testing the safety and correctness of distributed systems. This collaboration has so far resulted in [this published analysis](https://jepsen.io/analyses/redis-raft-1b3fbf6).

Though still under development, most of RedisRaft’s basic functionality is in place. We are currently working towards a first preview version, which is expected to be available in a couple of months. When generally available, RedisRaft will be released under a dual license, either GNU AGPLv3 or Redis Source Available License (RSAL).
