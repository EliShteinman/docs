---
title: "Redis 8.2 streams and bitmap enhancements"
linkTitle: "Redis 8.2 streams and bitmap enhancements"
url: "/blog/redis-82-streams-bitmap/"
description: "Redis 8.2 delivers powerful new enhancements to the streams and bitmap data structures that solve real challenges devs face every day."
date: 2025-08-12
blogCategories:
- "Tech"
authors:
- "Lior Kogan"
lastmod: 2025-08-12
hidden: true
mirrored: true
---

*By Lior Kogan, Contributor · Published 12 August 2025*

![Redis 8.2 streams and bitmap enhancements](/images/site-mirror/2ae9bb3778f80a0e9ce155dc54a9faad5d7d87b8-772x552.webp)

Redis 8.2 delivers powerful new enhancements to the streams and bitmap data structures that solve real challenges devs face every day.

Based on years of community feedback, we're introducing 2 powerful new commands XACKDEL and XDELEX then also extending 2 existing commands that dramatically simplify working with multi-consumer groups. We’re also adding 4 new logical operators to the BITOP command to enable more sophisticated set operations.

Let's dive into how these enhancements make apps built with Redis even better.

## Streams

## Intro to Redis Streams and consumer groups

Streams is a Redis data structure often used to process real-time streaming messages or events. Streams let users respond to events as they happen, making it easier to identify and react to patterns, trends, or anomalies as they occur. Streams allows multiple applications or many instances of the same application to process data in parallel, making it much more efficient to deal with high volumes of data. Redis Streams adopts the concept of consumer groups. Each consumer group allows multiple consumers to collaboratively process messages from a single stream. Each consumer in a group gets a unique subset of the messages, ensuring that each message is processed only once within that group.

When a consumer group is used to read messages (“Stream entries”) from a Redis Stream using the XREADGROUP command, the entry ID and the consumer's name are added to the Pending Entries List (PEL) of that consumer group. This signifies that the entry has been delivered to a consumer but not yet acknowledged as fully processed. After a consumer successfully processes a message, it should acknowledge it using the XACK command, which removes the entry reference from the PEL of that consumer group. Then, the consumer can call XDEL to delete the entry from the stream.

## Working with multiple consumer groups

We can associate a stream with multiple consumer groups. Each entry is delivered to all the stream’s consumer groups, and within each consumer group, each consumer handles only a portion of the entries, as described above.

Once a consumer processes a message, it acknowledges it using the XACK command. After an entry is acknowledged on all consumer groups, the entry needs to be deleted from the stream using XDEL, XTRIM, or XADD with trimming.

## What problem do we solve in 8.2?

As described above, the application needs to implement the logic that delete entries from the stream only after that entries are acknowledged on all consumer groups. Determining the right time can be quite complex. Over the years, many community members have pointed out the complexity of this logic:

- [https://github.com/redis/redis/issues/5774](https://github.com/redis/redis/issues/5774)
- [https://github.com/redis/redis/issues/6415](https://github.com/redis/redis/issues/6415)
- [https://github.com/redis/redis/issues/13314](https://github.com/redis/redis/issues/13314)
- [https://github.com/redis/redis/issues/6399](https://github.com/redis/redis/issues/6399)
- [https://github.com/redis/redis/issues/6315](https://github.com/redis/redis/issues/6315)

In Redis 8.2, we introduce a way to greatly simplify the application’s logic.

## New command: XACKDEL

XACKDEL combines the functionality of XACK and XDEL in Redis Streams. It acknowledges the specified entries in the specified consumer group and conditionally deletes the corresponding entries from the stream.

```
XACKDEL key group [KEEPREF | DELREF | ACKED] IDS numids id [id ...]

```

XACKDEL acknowledges the specified entries for the specified consumer group, and based on the specified option, conditionally deletes entries from the stream and removes references to these entries for the consumer groups' PELs:

| Option | Behavior |
|---|---|
| KEEPREF | Deletes the specified entries from the stream. Preserves the existing references to these entries in all consumer groups' PELs. |
| DELREF | Deletes the specified entries from the stream. Removes all references to these entries from all the consumer groups' PELs, effectively cleaning up all traces of these entries. If an entry ID is not in the stream, but there are dangling references, these references would still be removed. |
| ACKED | Deletes only the specified entries that were read and acknowledged on all consumer groups. If an entry was not yet read or not yet acknowledged on some consumer group, it will not be deleted. |

Users are encouraged to use XACKDEL with the ACKED option instead of using XACK and XDEL. This will simplify the application logic considerably.

## New command: XDELEX

XDELEX is an XDEL extension that provides more control over when entries are deleted and their references are removed from the consumer groups' PELs.

```
XDELEX key [KEEPREF | DELREF | ACKED] IDS numids id [id ...]

```

XDELEX accepts the same three options as XACKDEL (see the table above). With KEEPREF, the behavior is similar to that of XDEL.Also here, users can use XDELEX with the ACKED option to safely delete entries, i.e., delete only those entries that were read and acknowledged on all the consumer groups.

## Commands extensions: XTRIM and XADD

Since both XTRIM and XADD can delete entries, we extend both commands with the [KEEPREF | DELREF | ACKED] options as well:

```
XTRIM key <MAXLEN | MINID> [= | ~] threshold [LIMIT count] [KEEPREF | DELREF | ACKED]

XADD key [NOMKSTREAM] [<MAXLEN | MINID> [= | ~] threshold [LIMIT count]] [KEEPREF | DELREF | ACKED] <* | id> field value [field value ...]

```

The specified entries are deleted from the stream according to the specified strategy (MAXLEN or MINID). The behavior is as specified in the table above.

KEEPREF is the default behavior of XTRIM and XADD, hence we introduce no breaking change. While KEEPREF is provided for backward compatibility, DELREF is a better way to completely delete messages that should not be further processed. Also here, users can use the ACKED option to safely delete entries, i.e., delete only those entries that were read and acknowledged on all the consumer groups.

## Bitmap

Redis users often use bitmaps to store information about individuals:

- Multiple bitmaps, all of the same length, are used.
- Each bitmap is associated with one property.
- Each bit index , across all these bitmaps, is associated with a given individual.
- A bit is set if and only if an individual has some property.

Examples:

- Game engines often hold a bitmap per game segment. A bit index corresponds to a certain player (same index on all these bitmaps). A bit is set if a player is located within that segment.
- Adtech engines hold bitmaps to store campaign memberships. Each bitmap represents a campaign. A bit index corresponds to a certain person (same index on all these bitmaps). A bit is set if a specific person should be exposed (or was already exposed) to a given campaign.

The BITOP command is often used to create new bitmaps (or refresh existing ones) based on a set of existing bitmaps and a logical operator.

```
BITOP operator destkey key [key ...]

```

Before Redis 8.2, BITOP supported 4 logical operators: AND, OR, XOR and NOT.These covered basic logic, but complex targeting required scripts or using multiple commands. To address those needs, we introduce four new BITOP operators that simplify complex operations and enable more advanced logic in a single command:

- BITOP DIFF destkey X [Y1 Y2 ...]A bit in destkey is set if it is set in X but not in any of Y1, Y2, … 
- BITOP DIFF1 destkey X [Y1 Y2 ...]A bit in destkey is set if it is set on one or more Y1, Y2, … but not on X
- BITOP ANDOR destkey X [Y1 Y2 ...]
- A bit in destkey is set if it is set in X and also in one or more of Y1, Y2, …
- BITOP ONE destkey X1 [X2 X3 ...]
- A bit in destkey is set if it is set in exactly one of X1, X2, …

In other words, we can now construct the following bitmaps in a single command:

- DIFF: members of X but not of any of Y1, Y2, …
- DIFF1: members of one or more of Y1, Y2, … but not of X
- ADNOR: members of X and also of one or more of Y1, Y2, …
- ONE: members of exactly one of the given bitmaps

Lets look at a specific example: suppose we want to expose people to a specific ad. The target audience is people who love to read books, and are interested in fantasy, adventure, or science fiction. Assume we have the following bitmaps:

- LRB - people who love to read books
- B:F -people interested in fantasy
- B:A - people interested in adventure
- B:SF - people interested in science fiction

To create a bitmap representing the target audience, we can use the following command:

BITOP ANDOR newkey LRB B:F B:A B:SF

## Getting started

These enhancements are generally available on Redis 8.2 today. Learn more about Redis 8.2 in our [GA for open source blog post](/blog/redis-82-ga/).

Start using these new commands by [downloading Redis 8.2](https://redis.io/downloads/).

Have feedback or questions? Join the discussion on our [Discord server](https://discord.gg/redis) or reach out to your account manager.
