---
title: "How Redis brings persistent memory to Snowflake Cortex Agents"
linkTitle: "How Redis brings persistent memory to Snowflake Cortex Agents"
url: "/blog/how-redis-brings-persistent-memory-to-snowflake-cortex-agents/"
description: "AI agents can reason and act, but without memory, every interaction starts from zero. Intelligent short-term memory and persistent context across conversations are what turns a capable model into a..."
date: 2026-08-06
blogCategories:
- "Tech"
authors:
- "Mike  Moss "
lastmod: 2026-08-12
hidden: true
mirrored: true
---

*By Mike  Moss , SVP, Worldwide Channels & Alliances · Published 6 August 2026 · updated 12 August 2026*

![How Redis brings persistent memory to Snowflake Cortex Agents](/images/site-mirror/0140510a3bf87b882cd63d1fbca3d6f9d4acc1e8-1200x628.webp)

AI agents can reason and act, but without memory, every interaction starts from zero. Intelligent short-term memory and persistent context across conversations are what turns a capable model into a truly useful agent. It should remember the useful details you have already shared, such as your goals and constraints, so it can act with more context and fewer repeated questions.

For example, if an agent is helping a sales ops team pull pipeline data, it should remember which region, fiscal quarter, and revenue definitions the team usually uses. That way, the next time someone asks for a pipeline update, the agent can retrieve the right data, apply the right assumptions, and give an answer that reflects the team's actual business context.

To supercharge your agentic analytics, we are excited to announce that Redis Agent Memory is now available on the Snowflake Marketplace, bringing persistent long-term memory to Cortex AI agents. Once you install the application from the Marketplace, Redis Agent Memory is launched inside your account using Snowpark Container Services, with no data egress outside of your data warehouse and no new infrastructure to manage.

![Snowflake Account Diagram](/images/site-mirror/8acffd0647ed03badf8308d94fad4591fb87317e-2406x978.webp)

## The memory gap in Cortex agents

Snowflake Cortex is a powerful foundation for building AI applications. Cortex Analyst queries structured data, Cortex Search retrieves unstructured documents, and Threads track context within a single conversation. When a conversation ends, carrying relevant context forward to future conversations requires a persistent memory layer.

Enterprises need context to compound over time, not disappear at session end. Redis Agent Memory fills that gap by giving Cortex agents a durable memory layer that persists across sessions.

## How Redis fills the gap

Redis Agent Memory gives agents a persistent context layer. Persistent context lets an agent pick up where it left off, remember what your business terms mean, and recall relevant history without being told twice. There are four memory types at work:

**Episodic memory** captures specific events and outcomes, for example, "last week's EMEA pipeline drop was tied to delayed renewals." These are timestamped facts that can be recalled later to explain patterns or avoid repeating mistakes.

**Semantic memory** holds reusable business knowledge: definitions, rules, and conventions like "stage 2+ opportunities count as pipeline." This is the shared understanding an analyst would have internalized after months on the job.

**User preference memory** tracks how individuals like to work — preferred metrics, reporting cadence, chart types, or how they phrase certain queries — so the agent adapts over time without being reconfigured.

**Procedural memory** encodes the *how* — workflows, calculation methods, and reasoning steps the agent has learned to follow reliably, like how to compute churn or which filters to apply for a board-level pipeline review.

These four types come together naturally in a business analytics context: semantic memory defines what pipeline means in your org, episodic memory explains why last quarter looked anomalous, user preference memory knows you always want results broken out by region, and procedural memory knows the exact steps to pull and format that report. Before the model responds to any of this, Redis Agent Memory has already done the work, pulling the right facts, the right history, the right preferences, and the right process steps, assembled and ready. The analyst doesn't brief the agent. The agent already knows.

Redis Agent Memory for Snowflake exposes functions like `store_memory()`, `search_memory()`, and `hydrate_prompt()`. The key interface is `hydrate_prompt()`: a single function call that combines relevant long-term memory with working memory for a given prompt. Instead of requiring developers to manually search, rank, merge, and format context, Redis Agent Memory assembles the context the model needs before it responds.

For enterprise deployments, memory is scoped by user and namespace, so teams can isolate context across users, applications, tenants, or environments. Redis Agent Memory brings that memory layer directly into the Snowflake ecosystem.

## Up & running in five minutes

Redis Agent Memory installs directly from the Snowflake Marketplace with no external infrastructure to manage and no configuration required. Search for "**Redis Agent Memory**," click **Get**, grant two privileges (**create compute pool and bind service endpoint**), and all four containers auto-provision on Snowflake's own Snowpark Container Services. Your first memory is stored in under five minutes.

Once installed, everything is accessible through pure SQL. Eight service functions plus five Cortex Agent tools cover the full memory lifecycle: `store_memory()` to save facts and preferences, `search_memory()` for semantic vector search across all stored memories, and `hydrate_prompt()` to assemble full context for your LLM in a single call. No new languages, no SDKs, no REST APIs to learn.

It is Capacity Drawdown eligible, meaning customers can apply existing Snowflake credits toward it. All compute run on your own SPCS compute pool, all AI calls go through Snowflake Cortex, and your data never leaves your Snowflake account.

## Agents that actually remember

As AI moves from experimentation into production, the quality of the experience depends on continuity. Users expect agents to know who they are, what they care about, and what happened last time. Redis Agent Memory brings that continuity to Snowflake, giving Cortex agents a persistent memory layer while keeping data governed, compliant, and close to where it already lives.

**Ready to give your Cortex agents a memory?**

- [Install Redis Agent Memory from the Snowflake Marketplace (14-day free trial)](https://app.snowflake.com/marketplace/listing/GZ2FQZ166PM6/redis-inc-redis-agent-memory-for-snowflake-agents)
- Run the getting started notebook in under 5 minutes
- Register Redis Agent Memory as a tool in your existing Cortex Agent

The future of AI is agents that learn and remember, and Redis is proud to power that on Snowflake.
