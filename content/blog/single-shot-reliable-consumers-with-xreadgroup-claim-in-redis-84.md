---
title: "Single-shot reliable consumers with XREADGROUP CLAIM in Redis 8.4"
linkTitle: "Single-shot reliable consumers with XREADGROUP CLAIM in Redis 8.4"
url: "/blog/single-shot-reliable-consumers-with-xreadgroup-claim-in-redis-84/"
description: "In Redis 8.4, we extended XREADGROUP with a new optional CLAIM parameter that lets a single command both consume new stream entries and reclaim idle pending ones. In this blog post, we'll cover:"
date: 2026-05-26
blogCategories:
- "Tech"
authors:
- "Sergey Georgiev"
lastmod: 2026-05-26
hidden: true
mirrored: true
---

*By Sergey Georgiev, Principal Software Engineer · Published 26 May 2026*

![Single-shot reliable consumers with XREADGROUP CLAIM in Redis 8.4](/images/site-mirror/2db85d7f16c2fdfe52efef73cdb74c60913f89a4-1200x628.webp)

In Redis 8.4, we extended `XREADGROUP` with a new optional `CLAIM` parameter that lets a single command both consume new stream entries and reclaim idle pending ones. In this blog post, we'll cover:

- Why reliable Redis Streams consumers historically required multiple commands per loop iteration
- How the new `CLAIM` option collapses that loop into a single round trip
- The performance gains it delivers — up to 22.5x faster than `XAUTOCLAIM`
- The data structures that make it efficient, and how we made them even leaner with a follow-up optimization

**Should I care?** If you use Redis Streams consumer groups and want workers to automatically recover messages abandoned by crashed, slow, or unhealthy consumers, then yes. Before Redis 8.4, that recovery usually required a loop combining `XPENDING`, `XCLAIM` or `XAUTOCLAIM`, and `XREADGROUP`. Now a single `XREADGROUP` call can first reclaim idle pending messages and then read new ones. You still need to XACK messages after successful processing — `CLAIM` simplifies recovery, but it does not replace acknowledgements.

## A quick primer on the Pending Entries List

Redis Streams is an append-only log data structure introduced in Redis 5.0. On top of it, consumer groups give you the building blocks for reliable, at-least-once message processing across a fleet of workers.

The mechanism that makes this reliability possible is the **Pending Entries List (PEL)**. Here's how it works.

When a client reads messages from a stream with `XREADGROUP`, it identifies itself with a **consumer group** and a **consumer name**. For every message that gets delivered, Redis creates a *pending entry* inside the group. Internally, each pending entry is a small C struct called `streamNACK` (short for "negative acknowledgment" — it represents a message that *hasn't yet* been acknowledged). Each `streamNACK` records:

- Which message it refers to (the stream ID)
- Which consumer received it
- When it was delivered (delivery timestamp)
- How many times it has been delivered (delivery count)

You'll see `streamNACK` referenced throughout this post; whenever it appears, just read it as "the record for one pending entry."

The pending entry sits in the PEL until the client confirms it has finished processing the message by calling `XACK`. Once acknowledged, the entry is removed and Redis considers that message done.

This is what makes Streams suitable for work queues and event pipelines: if a consumer crashes mid-processing — or simply takes too long — its pending entries stay in the PEL. Another consumer in the same group can then take ownership of those entries with `XCLAIM` and pick up the work. To find out which entries are eligible for this kind of takeover, clients use `XPENDING`, which can filter pending entries by how long they've been idle.

There's an important corollary: **a pending entry that nobody acknowledges never goes away.** It stays in the PEL forever and continues to consume memory. Correct consumer-group usage isn't just about making sure every message gets processed — it's about making sure every message gets *acknowledged*, even if processing fails. The PEL is the heart of fault tolerance in Streams, and it's also where the operational complexity lives.

## The reliable consumer loop, before Redis 8.4

To build a correct consumer that handles both fresh messages and orphaned pending ones, you need three commands working together:

- `XREADGROUP` with the special > ID, which means "give me messages never delivered to any consumer in this group"
- `XPENDING` to discover entries that have been idle long enough to be considered abandoned
- `XCLAIM` or `XAUTOCLAIM` to take ownership of those idle entries

A typical loop looks something like this:

```
loop forever:
    # 1. Find orphaned messages
    pending = XPENDING mystream mygroup IDLE 30000 - + 100

    # 2. Claim them for this consumer
    if pending:
        claimed = XCLAIM mystream mygroup consumer1 30000 <ids...>
        process(claimed)

    # 3. Read new messages
    new_msgs = XREADGROUP GROUP mygroup consumer1 COUNT 100 BLOCK 5000 STREAMS mystream >
    process(new_msgs)

```

This pattern works, but it has real costs:

1. **Extra round trips.** Every iteration of every consumer makes two or three calls to Redis even when nothing needs to be claimed.
1. **Implementation burden.** Each application reimplements the same orchestration logic — often subtly wrong. Multi-stream consumers compound the complexity.
1. **Inefficient scans.** `XAUTOCLAIM` walks the PEL in stream-ID order and checks idle time per entry. With a large PEL and few idle entries, most of that scan is wasted work.

We wanted to give Streams users a single command that does the right thing.

## Introducing the CLAIM option

At a high level, `CLAIM` tells `XREADGROUP` to do two things in one call: first sweep up any pending messages that have been sitting idle in the group for longer than a threshold you specify, then read new messages as usual. The reclaimed entries are returned alongside the new ones, with extra metadata so the consumer can tell them apart and decide how to handle them.

That single command does the same job the old recovery loop did, but with a few properties that are hard to get right by hand: it runs in one round trip, it prioritizes orphaned work over new arrivals, it blocks reactively on both new messages and aging pending entries, and it returns the metadata clients need to build retry caps and dead-letter logic. We'll cover each of those below. In Redis 8.4, `XREADGROUP` accepts an optional `CLAIM` parameter:

```
XREADGROUP GROUP group consumer [COUNT count] [BLOCK milliseconds] [NOACK]
           [CLAIM min-idle-time]
           STREAMS key [key ...] id [id ...]

```

When `CLAIM min-idle-time` is specified, the command does two things in order, sharing a single `COUNT` budget:

1. **Claim first.** It scans for pending entries across the requested streams that have been idle for at least `min-idle-time` milliseconds, claims them for the calling consumer, and adds them to the response — up to `COUNT` entries total.
1. **Then read.** If the claim step filled the `COUNT` budget, the command returns immediately with only reclaimed entries. Otherwise it spends the remaining budget reading new entries from the streams, exactly as a normal `XREADGROUP` would.

So `COUNT` is a cap on the total number of entries , not on each step independently. Reclaimed entries always get priority — a consumer never starts processing new work while there's old work it could be picking up instead.

The consumer loop above collapses to this:

```
loop forever:
    msgs = XREADGROUP GROUP mygroup consumer1 COUNT 100 BLOCK 5000 \
           CLAIM 30000 STREAMS mystream >
    process(msgs)

```

One command. One round trip. Idle pending entries are prioritized so that no message gets indefinitely stuck behind a backlog of new arrivals.Response format with CLAIM

When `CLAIM` is in use, each returned entry carries two extra fields so the client can make informed decisions without going back to Redis:

```
127.0.0.1:6379> XREADGROUP GROUP mygroup consumer1 CLAIM 30000 STREAMS mystream >
1) 1) "mystream"
   2) 1) 1) "1609459200000-0"
         2) 1) "field1"
            2) "value1"
         3) (integer) 15000   ; idle time in ms
         4) (integer) 3        ; delivery count

```

- **Idle time (ms)** — milliseconds since this entry was last delivered. A value greater than zero means the entry was reclaimed; zero means it's freshly delivered.
- **Delivery count** — how many times this entry has been delivered. `0` for new messages, 1 or more for claimed ones.

These two fields are what make this useful for building **self-healing consumers**. With them in hand, a client can implement retry caps, route poison messages to a dead-letter stream, escalate critically delayed work, and detect stuck processing — all without an `XPENDING` call.

If the client passes a specific message ID instead of > — meaning "replay my own pending history from this point" rather than "give me new messages" — `CLAIM` is ignored and the response uses the standard format.

### Behavior with BLOCK

BLOCK is more interesting. A reliable consumer that blocks on new messages also wants to wake up the moment a pending entry crosses the `min-idle-time` threshold — otherwise the whole point of `CLAIM` is defeated during quiet periods.

To handle this, Redis tracks, per stream, the earliest timestamp at which the next pending entry will become claimable. A small bookkeeping function called from the `blockedBeforeSleep` hook checks that timestamp against the wall clock and wakes the relevant blocked clients exactly when needed. When multiple blocked clients are watching the same stream with different `min-idle-time` values, Redis keeps the minimum of their wakeup times so the earliest interested consumer is served first.

The result is reactive blocking: clients sleep efficiently and wake up as soon as either condition becomes true — new entries arrive, or pending entries age into eligibility.

## Performance impact

The whole reason to add this option — beyond ergonomics — is that it can be implemented far more efficiently than the multi-command alternative. The bottleneck in the old approach is finding which pending entries are idle. `XAUTOCLAIM` solves this by scanning the PEL in stream-ID order, which has no relationship to delivery time, so it ends up checking many entries that aren't yet eligible.

We took a different approach: maintain a separate, time-ordered index of the PEL so finding idle entries is a range query rather than a scan.

### When this helps most

The speedup is largest when your PEL is large but only a small number of messages are actually idle enough to reclaim. That's common when consumers are mostly healthy and only a few messages get stuck because a worker crashed or timed out. In that case `XAUTOCLAIM` may scan many pending entries to find a few reclaimable ones, while `XREADGROUP` `CLAIM` can go directly to the idle entries. If your PEL is small, or most pending messages are already idle, the speedup will be smaller.

### Latency benchmarks

To compare the two approaches, we designed a test that stresses the case where `XAUTOCLAIM` does the most wasted work: a large PEL where only a small fraction of entries are actually idle enough to claim. This is a realistic production scenario — a backlog of recently-delivered work where a handful of stragglers have timed out — and it's exactly the shape that the time-ordered index is designed to handle well.

**Test setup:**

1. Insert 20,000 messages into a stream
1. Read all of them with `XREADGROUP` to fully populate the PEL
1. Set idle time to 1100 ms on 1,000 randomly selected pending messages (the **5%** that are eligible to claim)
1. Set idle time to 50 ms on the remaining 19,000 (ineligible)
1. Execute the target command with `min-idle-time=1000` and `COUNT=1000` to claim the eligible entries
1. Repeat steps 3–5 for 1,000 iterations

| Metric | XAUTOCLAIM | XREADGROUP CLAIM | Improvement |
|---|---|---|---|
| Average | 54.671 ms | 2.426 ms | 95.6% lower |
| Median | 53.582 ms | 2.571 ms | 95.2% lower |
| P95 | 62.536 ms | 3.370 ms | 94.6% lower |
| P99 | 68.800 ms | 4.212 ms | 93.9% lower |
| Max | 71.596 ms | 4.653 ms | — |

That's **up to 22.5x faster on average** on this workload, with a much tighter tail. The improvement isn't a constant-factor win from removing a round trip — it's algorithmic. The new index turns a per-entry scan into an O(log n + k) range query, where k is the number of idle entries actually returned. (As we'll see further down, a follow-up optimization brought this even lower — to O(k) — by replacing the index with a simpler structure.)

#### Where does the 22.5x come from?

The arithmetic here is worth unpacking, because it tells you when to expect this kind of speedup in your own workload — and when not to.

`XAUTOCLAIM` walks the PEL in stream-ID order, which has no relationship to delivery time. To find the 1,000 eligible entries in this test, it has to examine roughly all 20,000 pending entries — that's O(n). `XREADGROUP` `CLAIM` uses the time-ordered index, so it visits only the 1,000 entries it actually returns — that's O(k). The theoretical ratio is `n / k = 20,000 / 1,000 = 20x`, and the measured 22.5x lines up cleanly with that.

So the speedup scales with **the ratio of total PEL size to actually-idle entries**. The bigger the gap, the bigger the win:

- **PEL mostly fresh, few stragglers** (this benchmark): large speedup, because `XAUTOCLAIM` wastes work on every ineligible entry.
- **PEL mostly idle** (e.g., 18,000 of 20,000 eligible): much smaller speedup. Both approaches end up touching most of the PEL, so they do similar amounts of work.
- **Small PEL**: the difference shrinks too; constants start to dominate.

The headline number isn't "every workload becomes 22.5x faster" — it's "the pathological case for `XAUTOCLAIM` stops being pathological." That case happens to be very common in production: a busy stream where consumers are mostly keeping up, with occasional stuck messages that need to be reclaimed. That's exactly the regime where reliability matters most, and where the old approach paid the highest cost.

### The cost we paid

The time-ordered index isn't free, and it's worth being explicit about what it costs — because some of those costs are paid even by consumers that don't use `CLAIM`.

**Extra work on the write path.** Every time `XREADGROUP` delivers a message, Redis now has to insert a `streamNACK` into `pel_by_time` in addition to the existing PEL structures. Every `XACK` has to remove it. Every `XCLAIM` and re-delivery has to update its position. Each of those rax-tree operations is O(log n) with a non-trivial constant — a 32-byte key traversal plus tree rebalancing. That's overhead on Redis's hot path, and it's paid whether or not anything ever queries the index.

For consumers that *do* use `CLAIM`, the trade is obviously worth it. For consumers that don't, they're paying a small tax for a feature they aren't using. We'll come back to this in a moment, because it's a big part of why the second optimization was worth doing.

**Memory footprint.** To measure the index's memory cost, we ran a separate test:

1. Insert 200,000 messages into a stream
1. Read them in blocks of 100 with `XREADGROUP`, populating the PEL
1. Wait 5 ms between blocks to simulate realistic processing delays
1. Compare memory used with and without the index

|  | Without index | With index |
|---|---|---|
| After insertion | 6.80 MB | 6.81 MB |
| After reading | 41.53 MB | 45.07 MB |
| Increase from reading | 34.72 MB | 38.27 MB |

The index added **3.55 MB across 200,000 pending entries**, or about **18.6 bytes per entry** — a roughly 8.7% overhead on total memory. The overhead only applies to entries that are actually pending; once a message is acknowledged, its index entry goes away with it.

For most workloads these costs are acceptable, but they're real, and they motivated the follow-up work we describe next.

## Under the hood

The rest of this post explains the internal Redis data structures that make `CLAIM` efficient. If you mainly want to use the feature, the key takeaway is that `XREADGROUP` `CLAIM` replaces the old multi-command recovery loop with a single command.

### The original design: A time-ordered rax tree

The first version of the feature introduced a new rax (radix) tree per consumer group called `pel_by_time`. Each entry in this tree is keyed by:

```
[ delivery_time (16 bytes) ][ streamId (16 bytes) ]   →   no value

```

The 32-byte composite key gives us three properties for free:

- **Uniqueness.** Two pending entries can share a delivery time, but they can never share a stream ID. The composite is globally unique.
- **Time ordering.** Rax trees sort lexicographically; with `delivery_time` as the prefix, that's equivalent to chronological order.
- **Range queries.** "Find all entries idle for at least N ms" becomes a range scan from the start of the tree up to `current_time - N`. That's O(log n + k).

No node values were needed — the stream ID is embedded in the key itself, so once we've located an idle entry we can immediately retrieve its full `streamNACK` from the existing PEL structures.

This design shipped in the first version of `XREADGROUP` `CLAIM` and is what powered the benchmarks above.

### The follow-up: From rax tree to linked list

Once we had the time-ordered index in production-shaped tests, we noticed something interesting about the workload.

**99% of ****`delivery_time`**** updates set the time to "now."**

This matters a lot, because — as we noted in the "cost we paid" section above — every `XREADGROUP` delivery, every `XCLAIM`, and every re-delivery is doing a rax-tree update on the hot path. Every time an entry is reclaimed or re-delivered, we were doing:

```c
raxRemovePelByTime(group->pel_by_time, old_time, &id);   // O(log n) tree op
nack->delivery_time = current_time;
raxInsertPelByTime(group->pel_by_time, current_time, &id); // O(log n) tree op

```

Two rax operations — each touching a 32-byte key, walking down a tree — for what is, fundamentally, an append to the tail of a time-ordered sequence. The rax tree was over-engineered for this access pattern, and it was making *every* consumer pay for it, even ones that never used `CLAIM`.

We replaced it with a **doubly-linked list embedded directly in each ****`streamNACK`** — that is, each pending-entry record now carries its own neighbors in the time-ordered sequence:

```c
typedef struct streamNACK {
    mstime_t delivery_time;
    uint64_t delivery_count;
    streamConsumer *consumer;
    listNode *cgroup_ref_node;
    streamID id;                     // NEW
    struct streamNACK *pel_prev;     // NEW
    struct streamNACK *pel_next;     // NEW
} streamNACK;

```

The consumer group now keeps a `pel_time_head` and `pel_time_tail` pointer. Updating a NACK's delivery time becomes:

```c
pelListUpdate(group, nack, current_time);  // unlink + append to tail, both O(1)

```

For the typical case — "this entry was just delivered, push it to the tail" — we do a handful of pointer updates. For the rare case of `XCLAIM` with an explicit `IDLE` value in the past, `pelListInsertSorted()` scans backward from the tail; rare enough that its O(N) worst case doesn't matter in practice.

### Why this works

The linked list is a perfect fit because:

- **Idle-entry queries still start at the head.** The list is sorted by delivery time, so the oldest entries are at the front. Finding entries idle for at least N ms is a forward walk from the head until the condition stops holding — no lookup step needed, because we always begin at the head.
- **Updates are appends.** The 99% case sets delivery time to "now," which means moving the NACK to the tail. Both unlink and append are O(1).
- **No separate structure to maintain.** The previous design had a `streamNACK` in the PEL hash *and* a key in the rax tree. The list pointers live inside the `streamNACK` itself, so cache locality improves and we have one less allocation per entry.

Putting the algorithmic story side by side:

| Operation | XAUTOCLAIM (pre-CLAIM) | CLAIM with rax tree | CLAIM with linked list |
|---|---|---|---|
| Find idle entries | O(n) — scans the PEL in stream-ID order | O(log n + k) — locate range, then walk | O(k) — walk from head |
| Update delivery time | O(log n) — two tree operations | O(log n) — two tree operations | O(1) — unlink + append |

The first jump (scan → range query) is what gave us the headline speedup over `XAUTOCLAIM` on the stress workload — and as we saw, that ratio scales with `n / k`, the fraction of the PEL that's actually idle. The second jump (range query → head walk, plus O(1) updates) is what gave us the additional 28% throughput on top.

### Memory got better too

The arithmetic is straightforward:

|  | Per pending entry |
|---|---|
| Added by linked list (id + 2 pointers) | 32 bytes |
| Removed with rax tree (composite key + node overhead) | ~40–50 bytes |
| Net | Lower memory |

So we got better throughput, lower latency, *and* a smaller footprint.

### Throughput benchmarks for the optimization

We re-ran the workload after the switch to a linked list using `memtier_benchmark` with 2M messages.

| Implementation | XREADGROUP RPS | Avg latency | P99 latency |
|---|---|---|---|
| Rax tree | 4,935 ops/sec | 0.195 ms | 0.212 ms |
| Linked list | 6,321 ops/sec | 0.152 ms | 0.168 ms |

That's **+28% throughput, –22% average latency, –21% P99 latency**, on top of the original 22.5x improvement over `XAUTOCLAIM`. `XADD` performance was unchanged at ~69K ops/sec — the optimization is purely on the consumer path.

## Compatibility

The `CLAIM` option is fully optional. Consumers that don't use it see the same behavior and response format as before. Within a single consumer group, you can freely mix:

- Consumers that use `CLAIM` and process both new and orphaned entries
- Consumers that don't, and only handle new ones

The linked-list optimization is what makes this clean: the per-delivery bookkeeping is now O(1), so consumers that never touch `CLAIM` no longer pay a measurable performance cost for the feature's existence. And the optimization itself is fully internal — no protocol, RDB, or AOF format changes.

## Wrapping up

Reliable Streams consumers used to require stitching together `XPENDING`, `XCLAIM/XAUTOCLAIM`, and `XREADGROUP` per loop iteration. With Redis 8.4, a single `XREADGROUP` ... `CLAIM` ... `STREAMS` ... does the same job in one round trip, prioritizes orphaned work correctly, blocks reactively on both new arrivals and aging pending entries, and returns the metadata clients need to build retry caps and dead-letter logic.

Under the hood, a time-ordered index turns "find me the idle entries" from a scan into a range query, and a linked-list implementation of that index gives us O(1) updates for the overwhelmingly common case where delivery time advances to "now."

The end result is up to **22.5x faster claim latency**, **28% higher throughput**, and a substantially simpler consumer loop — with full backward compatibility for everyone who isn't ready to change.

We're excited to see what reliability patterns the community builds on top of this. Happy streaming.
