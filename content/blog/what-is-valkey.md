---
title: "What is Valkey?"
linkTitle: "What is Valkey?"
url: "/blog/what-is-valkey/"
description: "Redis has been one of the most popular database technologies among devs for years. Companies like Airbnb, Hulu, and OpenAI rely on Redis for high-performance workloads across caching, real-time..."
date: 2026-03-11
blogCategories:
- "Tech"
authors:
- "James Tessier"
lastmod: 2026-06-01
hidden: true
mirrored: true
---

*By James Tessier, Senior Technical Product Marketing Manager, Competitive Intelligence · Published 11 March 2026 · updated 1 June 2026*

![Blog tile image](/images/site-mirror/73490f3b7bbcac67264436996fa2683cff9f1197-772x552.webp)

Redis has been one of the most popular database technologies among devs for years. Companies like Airbnb, Hulu, and OpenAI rely on Redis for high-performance workloads across caching, real-time data, and AI infrastructure.

In 2024, Redis shifted its [licensing ](https://redis.io/legal/licenses/)to a dual source-available model, and later added [AGPLv3 ](https://www.gnu.org/licenses/agpl-3.0.en.html)as an open-source option with Redis 8. [Valkey](https://valkey.io/) was created as a fork of Redis, backed by the Linux Foundation.

Though there's currently overlap between Redis and Valkey, the two projects have different teams, different roadmaps, and increasingly different feature sets. As Valkey maintainer Kyle Davis [put it](https://www.youtube.com/watch?v=3G6QgwIl-xs): "From this point forward, Redis and Valkey are two different pieces of software." This comparison covers what you need to know to make the right call for your architecture.

## How Valkey started & where it stands

Valkey is an open-source fork of Redis 7.2.4. Both started from the same codebase and share core in-memory data store and caching capabilities, storing data as key-value pairs in RAM, with optional disk persistence and replication for durability. But since the fork, the two projects have diverged significantly in data model, AI capabilities, and licensing.

Valkey launched in March 2024 with Linux Foundation governance. [Valkey 9](https://valkey.io/blog/introducing-valkey-9/) marked its biggest departure from the original fork, adding multiple logical database support in cluster mode, atomic slot migration, official modules for JSON, Bloom filters, and vector search, and demonstrating over one billion requests per second on a 2,000-node cluster in the project's own benchmarks.

Redis, meanwhile, has expanded well beyond the 7.2 feature set that Valkey forked from. The Redis 8 series, now at 8.6 with four major point releases in a year, integrates JSON, time series, probabilistic structures, vector sets, vector search, hybrid search, semantic caching, and AI tooling natively into the core, while compounding performance gains with each release.

## Valkey features & capabilities

Valkey is an [in-memory data store](https://redis.io/solutions/caching/) and cache that primarily serves data from RAM, with optional disk persistence and replication for durability. It shares Redis' core architecture and is fully compatible with the Redis 7.2 command set. For workloads that fit this model (i.e. database caching, real-time leaderboards, and message queuing) Valkey performs reliably.

### New capabilities since the fork

Since the fork, Valkey has added per-slot metrics for cluster observability, experimental Remote Direct Memory Access (RDMA) support, and in-progress Rust integration. Valkey 9.0 also added hash field expiration for granular time-to-live ([TTL](https://redis.io/docs/latest/commands/ttl/)) management at the individual hash field level, scaling clusters to as many as 2,000 nodes with automatic failover in the project's test configurations, and official BSD-licensed modules for JSON, Bloom filters, and search (including vector search), distributed together in the Valkey Bundle. [Replication](/blog/what-is-data-replication/) follows the familiar leader-replica model.

Where Redis 8 diverges is scope. Redis 8 supports hash field expiration too, and goes further with commands like HGETEX, HSETEX, and HGETDEL for combined get-and-expire and get-and-delete operations in a single call.

More importantly, Redis 8 integrates JSON, time series, additional probabilistic structures ([Cuckoo filters](https://redis.io/docs/latest/develop/data-types/probabilistic/cuckoo-filter/), [Count-Min Sketch](https://redis.io/docs/latest/develop/data-types/probabilistic/count-min-sketch/), [Top-k](https://redis.io/docs/latest/develop/data-types/probabilistic/top-k/), [t-digest](https://redis.io/docs/latest/develop/data-types/probabilistic/t-digest/)), vector sets, and Redis Search (including full text search, vector search and aggregations) into the core distribution, meaning no separate modules to install or manage. Time series, additional probabilistic structures, vector sets, semantic caching, and the Redis Query Engine remain gaps that Valkey hasn't addressed.

That gap has continued to widen. Redis 8.2 added [new streams commands](/blog/redis-82-ga/) for simplified multi-consumer-group workflows. Redis 8.4 introduced [hybrid search](/blog/redis-8-4-open-source-ga/) through the FT.HYBRID command (combining full-text and vector search with score fusion in a single query), atomic slot migration for safer cluster rebalancing, and atomic compare-and-set operations.

Redis 8.6 added [idempotent streams production](/blog/announcing-redis-86-performance-improvements-streams/) (duplicate-free message production, so producers can retry after failures without adding the same message twice), least recently modified (LRM) eviction policies, hot key detection and reporting, TLS certificate-based client authentication, and time series support for NaN values. None of these capabilities exist in Valkey today.

## Licensing & governance

The licensing split is the single biggest difference for many enterprise teams: Valkey uses permissive BSD 3-Clause, while Redis 8 offers a tri-license that includes copyleft AGPLv3.

### Licensing

Redis 8 is available under a tri-license: RSALv2, SSPLv1, and the OSI-approved AGPLv3, letting users choose which terms to adopt. (Earlier versions used BSD 3-Clause through 7.2.x, then dual RSALv2/SSPLv1 from 7.4.) AGPLv3 carries network copyleft obligations: if you modify Redis and offer it as a network service, AGPLv3 is generally interpreted to require disclosing those modifications.

Valkey is distributed under the BSD 3-Clause license, an OSI-approved permissive open-source license with no restrictions on commercial use, modification, or redistribution beyond attribution. The Linux Foundation's governance model means no single vendor can unilaterally change these terms.

### Governance

Redis Inc. controls the Redis project as a single-vendor effort, with a commitment to maintaining AGPLv3 as a permanent licensing option. Valkey uses the Linux Foundation's multi-vendor governance model, where decision-making is distributed across contributing organizations.

### Redis 7.2 end-of-life

Redis Open Source 7.2.4 was the last BSD-licensed Redis release. Separately, Redis Software 7.2 reached end-of-life on February 28, 2026. Teams still running 7.2 face an active migration decision: adopt Redis 8 under the tri-license, move to Redis Cloud or Redis Software for commercial licensing and enterprise support, or migrate to Valkey.

## Redis 8 through 8.6: performance & data structures

Redis 8 integrates capabilities that previously lived in separate Redis Stack modules directly into the core, adding eight new native data types: JSON, time series, five probabilistic structures (Bloom filter, Cuckoo filter, count-min sketch, top-k, t-digest), and vector sets (beta) for AI and semantic search. All are available in the Redis 8 open-source distribution under the Redis tri-license (RSALv2, SSPLv1, or AGPLv3), not only in paid enterprise tiers.

Redis has shipped four point releases in a year, each stacking performance and memory gains. Redis 8.6 reports [more than 5x throughput](/blog/announcing-redis-86-performance-improvements-streams/) versus Redis 7.2 on a single node. The 8.0 release reported [up to 87% lower latency](/blog/redis-8-ga/) compared to 7.2.5, and Redis 8.4 reported up to [92% memory reduction](/blog/redis-8-4-open-source-ga/) for JSON numeric arrays, with each subsequent release improving further.

The cumulative result in Redis 8.6: [more than 5x throughput](/blog/announcing-redis-86-performance-improvements-streams/) versus Redis 7.2 on a single node. Compared to 8.4 specifically, Redis 8.6 reported up to 35% lower latency on sorted set commands, up to 58% faster vector set queries, and up to 30.5% memory reduction for sorted sets. These are Redis-reported benchmarks, and real-world results will vary by workload.

For AI workloads, vector sets combined with the Redis Search's hybrid search capabilities let you mix vector search, full-text search, geospatial queries, and metadata filtering in a single query. Redis 8.4 added FT.HYBRID for unified score fusion across full-text and vector results. Redis LangCache delivers [up to 15× faster](/blog/context-window-management-llm-apps-developer-guide/) responses for cache hits and can cut LLM inference costs by recognizing semantically equivalent queries.

## Feature comparison: Redis vs Valkey

Redis maintains [well over a hundred](/blog/redis-elasticache-valkey-sprawl/) additional commands compared to Valkey, driven by its expanded data model.

| Capability | Redis Open Source | Valkey 9.0 |
|---|---|---|
| Core key-value & caching | ✓ | ✓ |
| Strings, lists, sets, hashes, sorted sets | ✓ | ✓ |
| Streams | ✓ | ✓ |
| Replication & clustering | ✓ | ✓ |
| JSON data type | ✓ (native) | Via official module |
| Time Series data type | ✓ | — |
| Probabilistic data structures | ✓ (native, 5 types) | Bloom filter via official module |
| Hash field expiration (field-level TTL) | ✓ | ✓ |
| Vector search | ✓ | Via official Valkey Search module |
| Hybrid search (FT.HYBRID) | ✓ | — |
| Atomic slot migration | ✓ | ✓ |
| Idempotent streams production | ✓ | — |
| Enhanced I/O multithreading | ✓ | ✓ |

On the enterprise tier, Redis has the most integrated first-party story across Redis Open Source, Redis Cloud, and Redis Software, with published SLAs up to 99.999% and enterprise features like Active-Active Geo Distribution with conflict-free replicated data type (CRDT) conflict resolution, Redis Flex for hybrid RAM and flash storage, Redis Data Integration for real-time sync from relational databases, role-based access control (RBAC), SAML integration, and audit logging for compliance-regulated environments.

## Similar origins but different futures

Each project's direction reflects how it's governed. Valkey's multi-vendor community prioritizes features that benefit a broad contributor base, with development velocity influenced by participating organizations' bandwidth. Redis' roadmap is driven by a single commercial entity with a clear strategic investment in AI infrastructure, bolstered by the return of creator [Salvatore "antirez" Sanfilippo](https://en.wikipedia.org/wiki/Salvatore_Sanfilippo), who developed the vector set data type. That focus enables faster innovation in specific capability areas.

The practical result: Redis has shipped four major point releases in under a year (8.0 through 8.6), moving aggressively into AI infrastructure with native vector sets, hybrid search, semantic caching, LRM evictions, and Redis Search—while reporting more than 5x throughput versus 7.2 in its latest benchmarks. Valkey has focused on core throughput, clustering, and extending capabilities through official modules. For basic caching, the two remain compatible at the application layer, but the gap in integrated capabilities widens with each elease.

## Which should you choose: Redis or Valkey?

The right answer depends on your workload, licensing constraints, and infrastructure requirements.

**Redis is the stronger choice when:**

- Your app uses or plans to use time series, multiple probabilistic structures, vector sets, or Redis Search for full text search or hybrid queries. Valkey doesn't currently offer these even through modules.
- You need hybrid search (FT.HYBRID) combining full-text and vector results with score fusion in a single query
- You want JSON, vector search, and Bloom filters integrated natively rather than managing separate modules
- You're building AI apps that benefit from semantic caching, vector embeddings, or the Redis for AI toolset
- You need operational features from the 8.x series like idempotent streams production, hot key detection, or atomic slot migration
- You need Active-Active Geo Distribution for multi-region writes with automatic conflict resolution
- Enterprise support with guaranteed SLAs, RBAC, or compliance documentation is a requirement

**Teams choose Valkey when:**

- Their workload fits Valkey's core plus its official modules (JSON, Bloom filters, search), and full Redis compatibility is not a concern
- Their organization has a blanket policy against AGPLv3 or source-available licenses, and the licensing constraint outweighs the feature and performance gap
- They need Linux Foundation governance and BSD licensing for long-term, community-governed terms, but can give up Redis' broader data model, AI capabilities, and the cumulative performance gains through 8.6

Some cloud providers now offer Valkey as a managed service alongside or instead of Redis. AWS ElastiCache supports Valkey with upgrade paths from some Redis OSS versions, and Google Cloud offers Memorystore for Valkey as a separate service. Confirming your engine version and command compatibility before enabling Redis 8-specific features is an important operational step.

## Build on the full Redis data platform

The question worth asking isn't what you're caching today, but what you'll need to build in the next 12 months. For apps that need time series, hybrid queries, AI inference pipelines, semantic caching, or the full depth of Redis' data model in a single integrated distribution, the Redis 8.x series through 8.6 offers a far richer platform—and one that's getting faster with every release. When you're ready for production at scale, Redis Cloud and Redis Software come with compliance documentation, SLAs, and managed operations that Valkey's ecosystem can't match today.

[Try Redis free](https://redis.io/try-free/) to explore Redis 8.6 and its full data platform capabilities, or [talk to the team](https://redis.io/meeting/) about the right deployment model for your workload.

## FAQs about Redis vs Valkey

### Redis 8.x (through 8.6) vs Valkey 9.0: key differences?

Redis 8 ships a broader feature set, and the gap has widened with each release through 8.6. The core integrates JSON, time series, five probabilistic structures (Bloom filter, Cuckoo filter, Count-Min Sketch, Top-k, t-digest), and vector sets (beta) natively, alongside the Redis Query Engine, hybrid search (FT.HYBRID), Redis LangCache for semantic caching, and well over a hundred additional commands. The 8.x series also added idempotent streams production, hot key detection, and atomic slot migration. Cumulative performance gains through 8.6 report more than 5x throughput versus Redis 7.2 in Redis' benchmarks. Valkey offers official modules for JSON, Bloom filters, and basic search, but time series, additional probabilistic structures, vector sets, semantic caching, hybrid search, and the Query Engine remain Redis-only. Both share core data structures and hash field expiration.

### Can I migrate from Valkey to Redis?

If you're running Valkey, migrating to Redis 8 is straightforward since both share the same RESP protocol and core command set. Existing client libraries work unchanged. Moving to Redis 8.6 gives you access to native JSON, time series, probabilistic structures, vector sets, the Redis Query Engine, hybrid search (FT.HYBRID), Redis LangCache for semantic caching, and idempotent streams production—without managing separate modules. If you're using Valkey's official modules for JSON, Bloom filters, or search, those capabilities are already built into the Redis 8 core.

### BSD 3-Clause vs AGPLv3 for enterprises?

Redis 8 gives users three license options: RSALv2, SSPLv1, or the OSI-approved AGPLv3. Using Redis unmodified as a backend database is generally understood not to trigger AGPLv3's copyleft obligations, and most production deployments fall into this category. Valkey uses BSD 3-Clause, which only requires attribution. For teams where licensing is the primary concern, the choice comes down to whether permissive licensing outweighs Redis 8's broader feature set and AI capabilities.

### Does Valkey support vector search & AI?

Redis 8 is the stronger option for vector search and AI. It integrates vector search natively through Redis Search and vector sets (beta), with hybrid search (FT.HYBRID) combining full-text and vector results through score fusion in a single query (added in 8.4). Redis LangCache provides semantic caching, and performance has improved through each 8.x release—with up to 58% faster queries in 8.6 versus 8.4. Valkey offers a Search module with vector search and structured filtering, but it doesn't match the Redis 8.x series' depth of integration or AI tooling.

### How to check if your provider switched to Valkey?

Connect via CLI and run INFO SERVER; Valkey identifies itself by name in the output. You can also check your cloud provider's console, where the engine type and version are usually in the instance details. For infrastructure-as-code users, check engine parameters in your Terraform or CloudFormation configs.
