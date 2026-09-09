---
title: "Real-time context: keeping agent inputs fresh on every step"
linkTitle: "Real-time context: keeping agent inputs fresh on every step"
url: "/blog/real-time-context-ai-agents-fresh-inputs/"
description: "Your AI agent issued the refund. It read the customer's tier, checked the return window, confirmed the policy, and processed it in seconds. The problem: the return window had closed four minutes..."
date: 2026-07-15
blogCategories:
- "Tech DE"
authors:
- "Jeff Mills"
lastmod: 2026-07-16
hidden: true
---

*By Jeff Mills, Director, Product Marketing · Published 15 July 2026 · updated 16 July 2026*

![Real-time context: keeping agent inputs fresh on every step](/images/site-mirror/6ad50b5e966a6873a3183e0eb95c1c4eb94a435c-2400x1256.webp)

Your AI agent issued the refund. It read the customer's tier, checked the return window, confirmed the policy, and processed it in seconds. The problem: the return window had closed four minutes earlier when a batch job updated the order status, and the agent was reading a snapshot from before the change. Now you have a refund you can't reverse, a policy exception you didn't approve, and no error log to point at.

This is the shift that catches teams off guard as they move from [agentic systems](/blog/ai-agent-orchestration-platforms/) that answer questions to ones that take actions. A stale answer is embarrassing. A stale action writes to your database, calls your payment provider, or triggers a downstream workflow that another agent will read as ground truth ten seconds later. Staleness stops being a quality issue and becomes a state-management issue, and it compounds fastest in the systems you're most likely to build next: multi-step agents whose outputs feed other agents' inputs. This article covers why agents act on outdated information even when retrieval succeeds, which parts of an agent's context have to stay current between steps, why getting fresh data in is only half the problem, and where a real-time context engine fits underneath the agent loop.

## Why agents act on stale data even when retrieval "worked"

The failure starts with a simple mismatch: retrieval working and context being fresh aren't the same thing. One agent-memory [diagnostic study](https://arxiv.org/html/2605.06527v1) tested how well long-term memory systems surface up-to-date information when facts change over time, measuring whether retrieval prioritizes the latest version of an entry or serves whatever ranks highest by similarity. The top-3 recalled memory entries still contained old evidence 60.5% of the time, and only 3.3% of those old entries were flagged as needing an update. Stale and updated memories sit side by side with nothing telling the agent which one to trust, which means outdated evidence stays visible even after newer evidence shows up.

That's one way stale context sneaks in. There are several more, and they stack on top of each other:

- **Cached answers skip the live tool.** Session memory can return a previous answer without re-invoking the tool that was supposed to fetch live data, so the agent responds from a snapshot while believing it checked. Cache invalidation is hard enough in apps; in agents, a cached answer also skips a decision point.
- **Prompt caching keeps its own clock.** Anthropic prompt caching entries have a cache lifetime of about five minutes, refreshed each time the cached content is used, so cached context gets re-served even if the underlying data changed a second later.
- **Early errors turn into ground truth.** Agents build each step on the history of previous steps, so a stale fact absorbed early gets integrated into state instead of isolated, and every later step builds on it as if it were fact.
- **Truncation drops context silently.** When the prompt exceeds the token limit, many frameworks trim older content with no error raised, and the model answers from an incomplete picture.

None of these are retrieval bugs in the classic sense. The retriever did what it was asked. The system just wasn't given a reliable way to separate fresh information from stale information, or it never asked for fresh information to begin with.

## Freshness is a context engineering problem, not just a RAG problem

These failure modes point to a bigger idea: the fix lives above retrieval, in how the whole context window gets managed. Context engineering is the practice of [curating and maintaining](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) the right set of tokens during LLM inference, meaning everything that lands in the context window, not just the prompt. Those strategies fall into four categories:

- **Write:** saving context outside the window so it can be recalled later.
- **Select:** pulling the right context into the window at the right time.
- **Compress:** keeping only what's needed as context accumulates.
- **Isolate:** splitting context across sub-agents or scoped memory.

Retrieval-augmented generation (RAG) mostly handles the select step. You can have a perfectly tuned retriever and still ship stale context, because freshness failures happen in what gets written, what gets kept, and what conflicts with what. Staleness is what makes those failures show up as recognizable patterns:

- Context poisoning is when a bad fact keeps getting referenced.
- Context distraction is when long history pulls focus away from the current task.
- Context confusion is when irrelevant content degrades the response.
- Context clash is when a fresh fact and a stale fact sit together with no trust signal.

[Context-length tests](/blog/context-rot/) show a related effect: as token count grows, accuracy and recall degrade well before you hit the window limit, and stale entries add to that pressure when they stick around in the prompt.

## What has to update in real time

If freshness is a context engineering problem, the next question is which parts of an agent's context actually need to stay current between steps. It's more than the vector index. Six components carry freshness requirements:

- **Working memory:** the active state inside the context window during a run. LangGraph reads this state [at each step](https://docs.langchain.com/oss/python/langchain/short-term-memory) and updates it when the step completes, so anything stale at the start of a step stays stale for that step.
- **Session state:** the saved conversation thread across turns. The OpenAI Agents SDK [prepends session history](https://openai.github.io/openai-agents-python/sessions) to the input before each run and stores new items after, so whatever sits in that store is what the agent sees.
- **Long-term memory:** the facts and preferences carried across sessions. Combining a memory tool with context editing [improved performance by 39%](https://www.anthropic.com/news/context-management) over baseline in an internal agentic search evaluation, which suggests actively managing this tier pays off.
- **Tool results:** the live external data pulled in at invocation time. Clearing already-used tool results is a common light-touch form of compaction, because a result that's already been consumed is noise on the next step.
- **Retrieved documents:** the RAG index that snapshots your sources at last ingestion. Many batch pipelines refresh on hourly or daily schedules, so teams often turn to [change data capture](/blog/knowledge-graph-rag-structured-retrieval-ai-agents/) and incremental, near-real-time updates instead of periodic rebuilds.
- **Machine learning (ML) features:** the pre-computed signals about users, products, or devices. Online feature stores often serve dozens of features per inference call inside a [millisecond request budget](https://redis.io/docs/latest/develop/use-cases/feature-store), depending on workload, while batch and streaming pipelines update those same features on very different cadences.

Each component fails differently when it goes stale. Stale working memory buries the current task. Stale session state serves yesterday's answer. Stale features leave a fast model reasoning over a slow-moving view of the world. Treating all six as one undifferentiated "context" is how freshness problems hide.

## Getting fresh data in is only half the problem

Keeping those six components updated is the write path, and a lot of teams stop there. But a system can have a fast ingestion pipeline and still fail the agent, because the agent needs to read fresh state before each step, and [read latency](/blog/database-performance-optimization-guide/) compounds in a way single-query systems never prepared us for.

To see why read latency matters, look at how often agents actually read. Every iteration of an agent loop re-reads context, memory, and tool results before deciding the next action, and the iteration count adds up fast. One data-question-agent benchmark measured [6.1 iterations](https://arxiv.org/html/2603.20576v1) and 7.3 tool calls per request for GPT-5.2, with the hardest queries pushing that to 17.6 tool calls and one model averaging over 60 tool calls on its hardest query. That's dozens of reads per user request, and each one has to hit fresh state to be worth doing.

Those reads dominate the latency budget, and the numbers show why freshness checks can't be a free operation. One benchmark measured an agentic RAG pipeline at [4.72 seconds](https://arxiv.org/html/2607.07858v1) end-to-end against a 1.64-second single-LLM baseline, with the loop itself driving the difference. In another analysis, tool execution alone accounted for [60% of latency](https://arxiv.org/html/2603.18897v1) in coding tasks. Both point to the same thing: the read path, not the model, is where agent time goes.

That's the trap. An agent that reads session context and long-term knowledge at every step pays that retrieval latency multiplied by the iteration count, so a read path that's "fast enough" for a single query becomes the bottleneck when the agent hits it dozens of times per task. Teams notice the slowdown and respond by caching more aggressively or skipping freshness checks—which is exactly how stale context sneaks back in. Fast reads aren't a nice-to-have; they're what makes checking for fresh state on every step affordable in the first place.

So real-time context has two halves. Fresh data has to flow in continuously, and reads have to be fast enough that checking for fresh data on every step doesn't blow the latency budget. Skip the first half and you get confident wrong answers. Skip the second and teams start caching aggressively or skipping reads, which quietly reintroduces the staleness they were trying to fix.

## Where Redis Iris fits: the read path underneath the agent loop

[Redis Iris](https://redis.io/iris/) is built for exactly this problem. Iris is a unified, real-time context engine built on Redis that keeps agent context fresh on the write path and fast on the read path, so checking for current state on every step stays affordable. Its components sit in one memory-first system instead of three or four separate ones, which matters because of the compounding math above: when session state, vector search, and cached responses live in separate systems, each agent step pays multiple network hops.

- **Redis Data Integration** streams changes from your systems of record into Redis in near real time through change data capture, so agents work from current business state instead of stale exports.
- **Redis Context Retriever** gives agents a schema-first path through business entities like customers, orders, and tickets, backed by [vector and hybrid search](https://redis.io/docs/latest/develop/ai/search-and-query/) with metadata filtering. In one [billion-vector benchmark](/blog/searching-1-billion-vectors-with-redis-8/), Redis reported 90% precision at roughly 200ms median latency retrieving the top 100 neighbors under 50 concurrent queries.
- **Redis Agent Memory** provides working and long-term memory tiers with deduplication, summarization, and background consolidation, so context compounds across sessions instead of going stale. Agent Memory is in public preview.
- **Redis LangCache** serves repeated and semantically similar LLM queries from cache, with [up to 15x faster](/blog/context-window-management-llm-apps-developer-guide/) responses on cache hits and [up to 73% lower](/blog/llm-token-optimization-speed-up-apps/) inference costs in high-repetition workloads. Time-to-live (TTL) and eviction controls bound how stale a cached answer can get. LangCache is in public preview.

For the ML features component, [Redis Feature Form](https://redis.io/docs/latest/develop/ai/featureform/), currently in preview, lets teams define, manage, and materialize feature definitions while Redis serves them as the low-latency online store. And if your app team already runs Redis for caching or sessions, this is the same Redis. Iris is built on the platform you may already operate, not a separate stack to procure.

**Redis keeps agent context fresh where it matters most: the read path**

That context layer matters because agents often fail even when retrieval appears to work. They fail because stale and fresh information coexist with no adjudication, because cached answers skip live tools, and because errors made early get treated as ground truth later. Fixing that means treating freshness as a context engineering problem across the whole agent context stack, not only a RAG indexing schedule. And it means recognizing the second half of the problem: an agent that makes dozens of reads per task needs a read path fast enough that checking for current state on every step is affordable.

Redis Iris sits underneath that loop as the real-time context layer. It keeps data continuously written through change data capture and fast to read through retrieval, memory, and semantic caching. Everything lives in one memory-first system. [Try Redis Iris](https://redis.io/try-free/?rcplan=iris) to see how it handles your agent's read path, or [talk to us](https://redis.io/meeting/) about keeping context fresh across your AI stack.
