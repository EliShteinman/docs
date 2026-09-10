---
title: "Diving deep into Redis’s new array data type"
linkTitle: "Diving deep into Redis’s new array data type"
url: "/blog/diving-deep-into-rediss-new-array-data-type/"
description: "The most popular data types in Redis are strings, lists, hashes, sets, and sorted sets. Each is purpose-built around a specific way of organizing data, enabling developers to solve a wide range of..."
date: 2026-06-02
blogCategories:
- "Tech"
authors:
- "Ricardo Ferreira"
lastmod: 2026-06-02
hidden: true
mirrored: true
---

*By Ricardo Ferreira, Lead Developer Advocate at Redis · Published 2 June 2026*

![Diving deep into Redis’s new array data type](/images/site-mirror/0efa10bbf4c17f61f38abf3499bc59bcd75b05c0-1200x628.webp)

The most popular data types in Redis are [strings](https://redis.io/docs/latest/develop/data-types/strings/), [lists](https://redis.io/docs/latest/develop/data-types/lists/), [hashes](https://redis.io/docs/latest/develop/data-types/hashes/), [sets](https://redis.io/docs/latest/develop/data-types/sets/), and [sorted sets](https://redis.io/docs/latest/develop/data-types/sorted-sets/). Each is purpose-built around a specific way of organizing data, enabling developers to solve a wide range of technical problems. What none of them offer is effectively constant-time access to a specific position. A list gives you O(N) index access, a Hash has no position concept, and a sorted set uses scores as metadata, not as addresses. That gap matters on its own. It matters even more when the index itself is part of your data model. Where position 47, for example, isn't just the 47th item in a sequence. It means something. Maybe it's the 47th minute of the hour, the 47th line of a Markdown file, or the event number 47 in a machine log.

Redis 8.8 introduces the [array](https://redis.io/docs/latest/develop/data-types/arrays/) type, designed by [Salvatore Sanfilippo](https://github.com/antirez), the original creator of Redis, with a specific contract in mind: if you know the index, you get the value, and everything in between costs nothing.

This post walks through what you can build with it, why it works the way it does under the hood, and where it fits relative to the types you already know, including cases where it doesn't fit. Not everything needs to be an array, and knowing when to stop reaching for it matters as much as knowing when to use it.

## Why a new data type?

There are scenarios where the right data structure is an array. Where developers instinctively think in terms of a natural, navigable sequence of elements, where each position can be fetched directly, and their indices have a meaning. Until Redis 8.8, there was no native way to handle it. Here are a few examples where an array is the natural data model:

- **Document line indexing**. You're building a code review tool, a log viewer, or a diff engine. Lines are addressed by number. When an error points to line 4821, you fetch line 4821 directly. When a reviewer comments on lines 40–55, you fetch that range in one command. Using a list would require iterating over the dataset. A hash provides no range queries. Neither was built for this.
- **Stack or call trace analysis**. You're building a profiler or debugger where stack frames are indexed by depth: frame 0 is the bottom, frame 47 is where the exception was thrown. You need O(1) access to any frame by depth, range queries over a call window, and gap detection for frames with no annotations. No existing Redis type gives you all three: a hash has no range scan, a list traverses from one end, and a sorted set can't distinguish an empty frame from one never written.
- **A workflow with numbered steps**. Step 0 is "received", step 3 is "under review", step 5 is "approved". Steps 1, 2, and 4 were never executed; they were skipped intentionally. The gap between step 0 and step 3 is semantically significant. It tells you something about how this claim was processed differently from others. You need to be able to look at a range of steps and see exactly which ones fired and which didn't, in a single query.

In each of these scenarios, there is a workaround in Redis today, but none of them is clean. Each workaround costs developers something: either atomicity, performance, or the mental overhead of keeping a secondary structure in sync just to answer "what's at position X." And because Redis lives entirely in RAM, that secondary structure isn't just a code-maintenance burden. It's memory you're paying for on every instance, every replica, every deployment.

## What you can build with array

The array type solves a specific class of problems. The following examples cover three distinct patterns: positional range access, fixed-size bounded buffers, and server-side filtering across sparse data. Each one is a problem that Redis developers have been solving with workarounds, and each one becomes straightforward with the array type.

### Network port allocation

Let's say you're managing a fleet of network switches. Each switch has a fixed number of ports, and each port has a unique number that serves as its identity. Port 47 isn't the 47th item in a sequence; it is port 47. Some ports are active, some are reserved, and most are dark. The gaps carry meaning: a contiguous block of empty ports is a candidate for a new VLAN assignment, and a single active port surrounded by empty ones may be a behavior worth investigating.

The naive Redis approach is a Hash with the port number as the field name. Individual lookups work fine. But the moment you need a range query, show me all active ports between 24 and 48, or find dark ports in the uplink range, you're pulling the entire hash to your application and filtering there. There's no server-side range query on a hash, no gap detection without a round-trip, and no aggregation without fetching everything first.

Using an array, dark ports simply don't exist in memory. They cost nothing to store, and scanning over them is essentially free because the data structure skips past empty regions entirely. Only the active ports take up space.

Three commands do the work here. `ARGETRANGE` returns the full range, including dark ports, which is what you need when the screen position has to match the port number. `ARSCAN` returns only the occupied slots, skipping the gaps entirely. `ARCOUNT` gives you the total count of active ports in O(1), no scan required. Here's what that looks like:

```
ARSET switch:tor-01 47 "10GbE · trunk · VLAN 200"
ARSET switch:tor-01 48 "10GbE · trunk · VLAN 200"
ARSET switch:tor-01 96 "1GbE · access · VLAN 100"


# full range, nils where ports are dark
ARGETRANGE switch:tor-01 45 48
>  1) (nil)
   2) (nil)
   3) "10GbE · trunk · VLAN 200"
   4) "10GbE · trunk · VLAN 200"


# only the active ports in the range
ARSCAN switch:tor-01 24 48
> 1) 1) "47"
     2) "10GbE · trunk · VLAN 200"
  2) 1) "48"
     2) "10GbE · trunk · VLAN 200"

# total active ports on the device
ARCOUNT switch:tor-01
> (integer) 3

```

One nuance worth understanding: `ARCOUNT` and `ARLEN` answer different questions. The `ARCOUNT` command tells you how many ports are actually active. `ARLEN` tells you the highest port index currently set, plus one, which indicates how far into the port range the device has been configured. On a 96-port switch where only ports 1–48 have ever been touched, `ARLEN` is 49 (indices start at 0, so the length is the highest index plus one: 48 + 1 = 49), and `ARCOUNT` is the number of those ports that are currently active. When calculating utilization percentage, you want `ARCOUNT` over total capacity, not `ARLEN`. Both commands exist because both questions are real; the data structure gives you the right answer for each one directly, without needing to scan to find out.

### Fixed-sized event logs

Assume you're running a fleet of machines, and you want a per-machine log of the last 200 kernel events, the kind of thing you'd read with the `dmesg` command. If something goes wrong, you want the last 50. When your monitoring system flags a specific event by sequence number, you want to jump directly to it.

The classic Redis solution is using a list, with the `LPUSH` + `LTRIM commands`. It works. But it has two friction points that matter at scale: atomicity and access patterns. `LPUSH` and `LTRIM` are separate commands, so without a transaction, there's a window during which the list is longer than you want. In a fleet of hundreds of machines all writing continuously, that window isn't theoretical. And `LINDEX` to fetch a specific position has to traverse the list from whichever end is closer; for a 200-item list, fetching event 47 means walking 47 steps from the head every time, regardless of how recently you fetched event 46.

`ARRING` writes the new event and advances the head pointer, both steps in a single atomic operation. No read before the write, no two-step operation to make atomic. And because the capacity is fixed at 200, the memory footprint is fixed too; the array never grows beyond 200 populated slots, regardless of how many events come in. You know exactly how much RAM each machine's log consumes.

```
ARRING myring 200 "[141087.430123]: arm_cpu_init(): cpu 14 online"


ARLASTITEMS myring 50
> 1) "[141087.430123]: arm_cpu_init(): cpu 14 online"


ARGET myring 47
> (nil)

```

One thing to keep in mind: `ARRING` is designed to be called with a fixed capacity. If you shrink the ring size or grow it after the ring has already wrapped around, the implementation rebuilds the logical ring to retain the latest entries in the correct positions. That's a significant operation proportional to the ring capacity, not the quick per-insert write you'd normally expect. Growing the ring before it has wrapped requires no rebuild. Set the size once and leave it.

For example, here's what happens when a new event comes in, and the buffer is already full. In the diagram below, the buffer holds five entries — "a" through "e" — with "a" being the oldest at position 0 and "e" the newest at position 4. Writing "f" doesn't expand the array. It overwrites position 0 (where "a" was) and updates the head pointer. The buffer stays at five slots; only the oldest entry is gone.

![Redis](/images/site-mirror/3f64af432ade274f25118ea8ad8906b7680f54a1-950x383.svg)

Now the buffer holds "b" through "f". Reading the three most recent entries with the command `ARLASTITEMS myring 3` doesn't walk the list from the beginning. It uses the head pointer and modular arithmetic to calculate exactly which positions hold the three newest entries, then reads each one directly. In the diagram below, you can see it stepping back from position 0 to position 4 to position 3, returning "f", "e", "d" in newest-to-oldest order (or "d", "e", "f" oldest-first, which is the default).

![Redis](/images/site-mirror/d3b584e7fca166970d7aa60372f9f81603d54d61-950x240.svg)

`ARLASTITEMS` returns results oldest-first by default. If you want newest-first, you can add `REV`.

If you're currently using `LPUSH` + `LTRIM` and never need to access specific events by position, the list solution isn't wrong; it's simpler and well-understood. The array is the better fit when the sequence number of each event carries meaning, when predictable memory usage matters, and when you need position-based access alongside the recency view.

### Pattern search across sparse data

Now, let's say you're storing log entries in an array indexed by their sequence number. The array is sparse; maybe one in ten positions has a value, because you're only recording entries that passed a severity filter. At some point, you need to find all entries matching a pattern, like all errors, all warnings from a specific service, or all entries mentioning a particular host.

The alternatives aren't pretty. Pull a range to your application and filter there, which means transferring potentially thousands of values over the wire just to discard most of them. Or maintain a secondary data structure that indexes entries by type, which means every write updates two keys, and now you're paying RAM for two representations of the same data. With an array, you can handle this server-side with ARGREP. Say you enter the following values.

```
ARSET myarray 0 "ok:200"
ARSET myarray 2 "err:timeout"
ARSET myarray 3 "ok:204"
ARSET myarray 5 "err:404"

```

You can use the `ARGREP` command to scan only the occupied slots. Empty positions are skipped at the directory level; the code looks at the group pointer, sees null, and jumps the entire group of 4096 positions in one step. The cost is proportional to the number of entries, not to the size of the index space they span. Only the matching entries travel over the wire. There’s no secondary index or secondary RAM cost.

```
ARGREP myarray - + GLOB "err:*" WITHVALUES
> 1) 1) "2"
     2) "err:timeout"
  2) 1) "5"
     2) "err:404"

```

The diagram below shows exactly how the traversal works.

![Redis](/images/site-mirror/59b2604cdab730b0837048df23de2b38c510d9a2-950x420.svg)

`ARGREP` supports four matching modes: `EXACT` for literal equality, `MATCH` for substring search, `GLOB` for wildcard patterns using the same `*`, `?`, and `[...]` syntax as `KEYS` and SCAN, and RE for regular expressions. Predicates can be combined with `AND` or `OR` logic. The - and + range sentinels follow the same convention as sorted set range commands.

The regex support deserves a note of its own. It's backed by [TRE](https://github.com/laurikari/tre/), a POSIX regex library chosen specifically because it prevents pathological worst-case behavior from adversarial or unlucky patterns, the kind of thing you need to think about when regex runs inside a database server. Salvatore noted in his [write-up](https://www.antirez.com/news/164) on the array type's development that TRE's handling of alternation patterns, such as `ERR|WARN|FATAL`, was slow and required optimization before shipping. That's exactly the pattern you'd reach for in log monitoring and alerting.

One thing to understand about `ARGREP`: it's a scan, not an index lookup. The cost scales with the number of entries in the range, not the total size of the index space. For sparse data, this is fast; that's the whole point. For very dense arrays where you're running pattern searches at high frequency across millions of populated entries, you should benchmark against your latency requirements. `ARGREP` is designed for sparse-to-moderate-density data where position carries meaning. For purely search-driven workloads on dense data, a dedicated index with [Redis Search](https://redis.io/docs/latest/develop/ai/search-and-query/) is likely still the right architecture.

## How the array data type works internally

The scenarios discussed earlier have something in common: the memory model makes them practical. It's worth understanding it directly because once you see how the array data type stores data, the behavior of every command above stops being surprising and becomes obvious.

In most programming languages, an array works something like this:

```
arr := [5]string{"a", "b", "c", "d", "e"}
x := arr[3] // assigns "d" to variable x

```

Writing values at indices and reading them back is O(1). The index is the address. This contract is exactly what array preserves: `ARGET myarray 3` gives you "d" the same way `arr[3]` in your programming language does. What changes is the implementation underneath: how the data is laid out in memory, what happens when the array is sparse, and how it stays fast as it grows to tens of millions of entries without consuming RAM proportional to the index space.

The key difference from a typical array is that an array in Redis doesn't allocate memory for every position upfront. A plain C array of a million entries reserves space for all million slots upfront, whether they hold values or not. The array data type divides its index space into groups of 4096 slots and only allocates a slot block for a group when something is actually written to it. An empty group costs 8 bytes: one null pointer in the index table, nothing more. That single decision is what keeps gaps free, scanning fast, and large index spaces practical. Let's take a look at a few concrete scenarios.

### Writing data consecutively

When you write to positions 0, 1, and 2 of the array, only one slot block gets allocated, for group 0, which covers positions 0 through 4095. Every other group in the index table stays as an empty 8-byte null pointer. For example, with these entries:

```
ARSET myarray 0 "a"
ARSET myarray 1 "b"
ARSET myarray 2 "c"

```

The array will change its internal state from all groups empty and nothing allocated to creating one active slot block, and leaving three groups still costing just 8 bytes each.

![Redis](/images/site-mirror/2f6844d6375791b8882cb86e57937e92c53f43bd-950x473.svg)

Small integers, floats, and short strings are stored directly inside the pointer slot, with no separate heap allocation. The low bits of a pointer that would otherwise go unused due to memory alignment are used to encode the value and its type. A dense array of small values ends up with essentially the same memory footprint as a raw C array of pointers. For sensor readings, counters, or short status strings, you're allocating for the data and nothing else.

Executing `ARGET myarray 1` follows the path shown below: one step to find group 0 in the index table, then a binary search within that group to locate position 1. By default, this will always be two steps, except in scenarios where the array has more than 8M entries, as we will see later in this section. Because the number of steps is determined by the structure and not the amount of data, this is effectively constant-time access.

![Redis](/images/site-mirror/970a8a26e0d68b2cd2d4afc98ba44a4e5f93f0d1-950x240.svg)

### Writing data sparsely

Now, let's say you are importing data with gaps. When you write the position 2 and the position 8194, only two slot blocks are allocated, one for each group that received a write.

```
ARSET myarray 2 "a"
ARSET myarray 8194 "b"

```

The diagram below shows what the index table looks like after both writes. Group 0 holds position 2. Position 8194 lands in group 2 (because 8194 = 8192 + 2). Group 1, covering positions 4096 through 8191, never received a write; it exists only as a null pointer (8 bytes). A gap covering 4096 positions costs the same as a gap covering 40,960 positions: 8 bytes.

![Redis](/images/site-mirror/f542482affd38d436249dfafe14b399e0e738ba3-950x646.svg)

A job with a million input rows and 200 errors costs the memory of 200 stored values plus a handful of null pointers. And scanning with `ARSCAN` doesn't visit a million positions: it looks at the directory, finds the groups that have data, jumps the empty ones entirely, and returns just the occupied entries. The same design that makes gaps free also makes scanning fast.

Reading a specific index in a sparse array follows the same two-step path as before: the first hop identifies the group and relative position; the second hop reaches the sparse block; and then a binary search within that block locates the exact entry. The diagram below shows an example. The search is over a small bounded set, never more than 10 entries per block by default, so it stays fast regardless of how spread out the data is.

![Redis](/images/site-mirror/150b44d2e630e295216d628b056eb4030caab2e4-950x240.svg)

### When the array gets very large

When you write to an index of 8,388,608 or higher, the array promotes itself from a flat index table to a three-level structure: a top-level directory, known as superdir, pointing to blocks, each block pointing to the groups you already know about. That threshold isn't arbitrary. It's where the flat directory would need to grow beyond its hard internal limit of 2048 entries, so the structure upgrades itself instead.

```
ARSET myarray 50000000 "x"

```

This happens silently. You just write, and the structure adapts. `ARGET myarray 50000000` still works exactly like `arr[50000000]`; you will get "x" back. The diagram below shows the before and after: a flat directory at the top and the newly promoted three-level structure at the bottom, with the top-level `superdir` pointing to blocks, and blocks pointing to the slices that hold actual values.

![Redis](/images/site-mirror/e0b767e1dfb988cc83060ea3754f46bcde000f5a-950x850.svg)

After the upgrade, the structure always has exactly three levels: a top-level superdir, a block, and a slice. The depth is fixed; it will never grow to four or five levels, regardless of how much data you add. The diagram below shows a read for index 50,000,000 traversing those three levels: a binary search in the superdir to locate the right block, which runs efficiently because there are very few blocks, then a direct index into the block, then a lookup within the slice; a binary search for sparse data, or a direct index for dense data.

![Redis](/images/site-mirror/9848a2fe41cdff5cbf599775fba0411b72d4ff88-950x240.svg)

The lookup within the top level involves a binary search over the superdir entries, but the number of superdir blocks stays very small relative to the data. The search is over structured metadata, not your actual values, so in practice, the cost stays tight and predictable even at very large scales.

The upgrade itself is a one-time cost, not an ongoing one. Here's precisely what happens: the flat directory is capped at a hard maximum of 2048 entries before the upgrade ever triggers, a limit enforced by a constant in the source. So when it fires, the work is fixed: allocate a small superdir array, allocate one 2048-pointer block, copy at most 2048 pointers from the old flat directory, and free the old directory. That's roughly 16 KB of pointer copies, two small allocations, and a bounded copy. Fully synchronous within the triggering `ARSET` call, because Redis processes commands on a single thread. In practice, it's a handful of microseconds. The upgrade is permanent. Once the array is promoted to superdir, it stays there regardless of how many entries are later deleted.

There's no degraded period after. No background work, no second phase. The one slightly slower command is the entire price, and subsequent writes and reads continue to cost the same as before.

If you need tight latency guarantees on every individual write near the boundary, pre-warm: write a single sentinel value at an index above the threshold before your production traffic starts. The upgrade happens at setup time on your terms, not mid-traffic on a random write.

### Server-side aggregations

Now, let's say you're tracking per-device metrics like request counts, packet counts, and error rates stored in an array indexed by time bucket. At some point, you need the total for a time window, the peak value, or simply how many buckets had any activity.

The obvious approach may be to fetch the range using `ARGETRANGE` and aggregate it in your application. For a dense array with thousands of entries, that means transferring all the values over the wire to discard them after a single arithmetic pass. You could maintain a separate running counter in another key to avoid the transfer, but now every write touches two structures, and consistency becomes your problem.

`AROP` runs the aggregation on the server and returns a single value.

```
ARSET metrics:device-01 0 142
ARSET metrics:device-01 1 98
ARSET metrics:device-01 5 201
ARSET metrics:device-01 6 174

# total requests in the window
AROP metrics:device-01 0 8300 SUM
> "615"

# peak bucket in that window
AROP metrics:device-01 0 8300 MAX
> "201"

# how many buckets had any traffic
AROP metrics:device-01 0 8300 USED
> (integer) 4

```

`AROP` supports `SUM`, `MIN`, `MAX`, `AND`, `OR`, `XOR`, `USED`, and `MATCH`. Numeric operations like `SUM`, `MIN`, and `MAX` return their results as strings. `USED`, `AND`, `OR`, `XOR`, and `MATCH` return an integer. Worth accounting for in your client code.

Under the hood, `AROP` uses the same scan iterator as `ARSCAN` and `ARGREP`. The traversal starts at the first directory entry that overlaps the requested range and walks forward. For each group pointer in the directory, the iterator checks whether it is null. If it is, the entire group of 4096 positions is skipped in a single step, no values are touched, no slots are visited. Only groups that have been written to are entered. The diagram below shows this path for the example above: the range 0–8300 spans three groups. Group 0 has data and is entered. Groups 1 and 2 are null pointers and are each skipped in a single step.

![Redis](/images/site-mirror/137f49f13ca3f37f09ed8b3d681aba78ace92093-950x488.svg)

Once the iterator enters a group, it visits only the occupied slots within the requested range. For each slot, the stored value is extracted and fed into the accumulator. For `SUM`, each value is parsed as a number and added to a running total. For `MAX`, it replaces the current maximum if larger. For `USED`, the counter increments by one regardless of the value. At the end of the scan, the accumulated result is returned as a single reply.

The diagram below shows the accumulator receiving values from group 0: positions 0, 1, 5, and 6, the only four occupied slots in the range. Groups 1 and 2 were skipped at the directory level and contributed nothing.

![Redis](/images/site-mirror/fa6314ff56c41008d7c3e38c480efa5ee0cd93c9-950x446.svg)

`USED` is worth separating from `ARCOUNT`. `ARCOUNT` returns the total populated count across the entire array in O(1) because it reads a stored counter directly. `AROP USED` scans the range and counts what it finds, which makes it the range-scoped equivalent: useful when you need the active count within a specific window rather than across the whole array.

`MATCH` takes a predicate in the same form as `ARGREP` and returns a count of matching entries rather than their positions or values. If `ARGREP` answers the question "which entries match?", `AROP MATCH` answers "how many match?" with no values transferred.

### Deleting entries

`ARDEL` removes a single position. `ARDELRANGE` removes a range. Both operate in proportion to the number of entries touched, not to the size of the index space they span. To illustrate this, let's take a look at this example.

```
ARSET myarray 0 142
ARSET myarray 1 98
ARSET myarray 5 201

ARDEL myarray 5

ARGET myarray 5
> (nil)

ARCOUNT myarray
> (integer) 2

```

The memory behavior mirrors the write path exactly. When a deletion empties a slice entirely, the slice is freed immediately, and its slot in the directory is set back to null, the same 8-byte cost as a gap that was never written to. There's no deferred cleanup, no background pass. The memory is recovered within the same command that deleted the last entry.

![Redis](/images/site-mirror/f6e7c66d99df1a6f6382235a22be5d543c192aa6-950x646.svg)

`ARCOUNT` decrements immediately. It's a stored counter updated on every write and delete, so the cost is always O(1) and the answer is always exact. `ARLEN` updates dynamically as well. It always reflects the current highest occupied index plus one. Delete a position in the middle, and `ARLEN` is unchanged, because the highest occupied index didn't move. Delete the position at the top — the current highest — and `ARLEN` decreases to the next occupied position plus one. The source scans backward through the directory to find it.

This means `ARLEN` and `ARCOUNT` can diverge in arrays that see heavy deletions from the middle. If you're tracking utilization, `ARCOUNT` is the right number: it tells you how many positions are currently occupied. `ARLEN` tells you the current extent of the data, which is a different question.

## When other data types are still the right choice

The right question isn't "can I use an array here?" It's "Does the numeric index carry domain meaning?" If the position is part of your data model, if removing it would change what the data means, that's where arrays shine. If the index is an implementation detail, a mechanism for ordering or uniqueness that your application never reasons about directly, you almost certainly want something else.

Here's how that plays out across the types you already use.

### Array vs. list

Lists and arrays look superficially similar. Both are ordered, both hold string values, but they optimize for different access patterns. A list is a double-ended queue (deque): push and pop at either end are O(1), and positional access degrades from there. `LINDEX` can give you `arr[47]`-style access, but at O(N) cost as it traverses from whichever end is closer, so fetching position 47 means walking 47 steps from the head every time, regardless of how recently you fetched position 46. There's also no gap concept: a list is always dense, so there's no way to represent "slot 47 was intentionally left empty" without storing an explicit sentinel value and teaching your application to interpret it.

Use a list when insertion order is the meaning: queues, logs, feeds, where "what came first" is what matters. Use an array when position is the meaning: numbered steps, indexed events, anything where slot 47 **is** slot 47 in your domain.

The gray area is the `LPUSH` + `LTRIM` ring buffer pattern. If you never need to access events by sequence number, that pattern is simpler and perfectly correct. `ARRING` earns its place when you need both recency access and position-based access on the same data, or when you want a fixed memory budget enforced at the data structure level rather than maintained by application logic.

### Array vs. hash

Hashes are the natural choice when fields are named: user profiles, configuration objects, session data. The field names carry meaning, and there's no inherent ordering between them.

When field names are integers, the decision gets murkier. You can store port 47 in a Hash as field "47" and `HGET` works fine. The problem surfaces the moment you need range operations: show me all fields between 24 and 48, or find every field in the range 0–96 that is missing. The `HSCAN` command doesn't support that. You pull the entire hash and filter in your application, transferring potentially thousands of fields over the wire for every query.

A useful signal: if you'd ever call the field a "position" or an "index" rather than a "name", and if range queries or gap detection matter, that's an array.

### Array vs. set

Sets answer one question well: is this value a member? `SADD`, `SREM`, and `SISMEMBER` are all O(1), and set algebra (union, intersection, difference) is built in. For tracking unique visitors, active sessions, or feature flag enrollments, nothing is simpler.

What sets don't have is any concept of position. Members are unordered and unindexed; the only meaningful property is membership. `SMEMBERS` returns everything in arbitrary order, and there's no range query without pulling the full set to your application. There's also no way to ask "what's at slot 47?" because slots don't exist. Only presence or absence.

The distinction comes down to the question you're actually asking. A set tells you whether something is present. An array tells you what's at a specific position. If your data has natural numeric addresses, row 18552 of a file, step 3 of a workflow, port 47 on a switch, a set can't model that. You'd have to encode the position into the member value itself, at which point you've given up membership semantics and gained nothing over a hash.

Use a set when uniqueness is the constraint and order doesn't matter. Use the array when the position is the schema.

### Array vs. sorted set

Sorted sets are often used as a proxy for indexed data: store values with a numeric score and use `ZRANGEBYSCORE` for range queries. The pattern works, but the data model differs in a way that matters at the margins.

In a sorted set, the score is metadata you compute and attach to a member. Two members can share a score. The score and the member are separate things. With arrays, the index IS the address: writing to position 47 means the value lives at 47, not that you've tagged it with the number 47. There's no separate member identity.

The practical difference shows up around gaps. With a sorted set, you can't distinguish "nothing was ever written at score 47" from "this position was explicitly cleared." `ZRANGEBYSCORE` 47 47 just returns empty either way. The array gives you `ARCOUNT` versus `ARLEN`, `ARSCAN` versus `ARGETRANGE`: primitives that let you reason about density, utilization, and gaps at the data structure level, not in application code.

Use a sorted set when the score is the metadata, such as ranking, ratings, or priorities. Use an array when the index is the address in your data model.

### The decision in one question

If you find yourself explaining what a numeric index means in the context of your data, such as "index 47 is the 47th minute of the hour", "index 3 is the approval step", and "index 18552 is row 18552 of the import file", that's array territory. If the index is an internal mechanism you'd never expose to your application logic, the existing types are still the better fit for what they were built to do.

## Trying it

Array is available in Redis 8.8. To see it working in a realistic context, we built a demo that loads a Markdown document into an array and connects it to an AI agent. The agent decides at runtime whether a question is better answered by an exact array command or by performing a vector similarity search. A side panel shows which tool was selected, the exact Redis command executed, and the round-trip latency for each turn.

The demo runs as a web app or via CLI and requires only Docker Compose and an OpenAI API key. The GitHub repository with the setup instructions is available [here](https://github.com/redis-developer/redis-array-context-demo).
