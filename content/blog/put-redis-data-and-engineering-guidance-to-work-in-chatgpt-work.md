---
title: "Put Redis data and engineering guidance to work in ChatGPT Work"
linkTitle: "Put Redis data and engineering guidance to work in ChatGPT Work"
url: "/blog/put-redis-data-and-engineering-guidance-to-work-in-chatgpt-work/"
description: "Redis has launched a development plugin that brings current Redis engineering guidance into ChatGPT Work and Codex. It helps teams write, review, and troubleshoot Redis code without switching..."
date: 2026-09-11
blogCategories:
- "Tech"
authors:
- "Olga Lopaci"
lastmod: 2026-09-11
hidden: true
mirrored: true
---

*By Olga Lopaci · Published 11 September 2026*

![Put Redis data and engineering guidance to work in ChatGPT Work](/images/site-mirror/2e1e681fd898b86cfefcccac13e3a1aa95325215-1200x628.webp)

Redis has launched a development plugin that brings current Redis engineering guidance into ChatGPT Work and Codex. It helps teams write, review, and troubleshoot Redis code without switching between documentation and development tools.

Alongside OpenAI's new Data agent in ChatGPT Work, teams can also explore connected Redis data in plain language, investigate what changed, and understand why.

## One place to build and investigate

Teams are always looking for ways to build better apps. What can we make more efficient? What should we build next? How do we scale without creating another problem to solve later?

Connect Redis data to the Data agent in ChatGPT Work, and your team can design, build, review, and troubleshoot Redis apps with guidance grounded in your data. Get help with data structures, connections, Redis Search, semantic caching, clustering, security, observability, and Redis Iris agent memory.

Less time digging for answers. More time building.

## Bring Redis engineering guidance into the tools you use

For developers building the applications behind that data, the Redis Development plugin puts Redis-specific guidance directly into the agent’s context.

If you installed our agent skills using `npx skills add`, that still works. The skills are now also available through a plugin you can install in ChatGPT Work and Codex.

Each skill provides instructions the agent loads when it encounters relevant work, so the guidance is available when it's needed.

## What's in the plugin

`redis-core`: Choosing data structures, hashes versus JSON, and consistent key naming.

`redis-connections`: Connection pooling, multiplexing, pipelining, client-side caching, timeouts, and slow commands.

`redis-search`: Schema design, search and aggregation, vector similarity, hybrid retrieval, and RAG pipelines.

`redis-semantic-cache`: LLM response caching with LangCache, similarity tuning, and separate caches for different tasks.

`redis-clustering`: Hash tags for multi-key operations, avoiding CROSSSLOT errors, and replica reads.

`redis-security`: Authentication, TLS, ACL policies, network binding, and firewall configuration.

`redis-observability`: Key metrics, triage commands, and Redis Insight.

`iris-development`: Redis Agent Memory provisioning, SDK authentication, session events, long-term memory search, and asynchronous promotion.

## Why install it?

Ask an agent to build a cache, and it will often recognize Redis as a familiar option. Ask it to configure Redis Agent Memory or build a hybrid retrieval pipeline, and it may reach for older patterns.

The plugin gives the agent current Redis engineering guidance for that work, including newer capabilities such as LangCache and Redis Agent Memory.

We evaluated each skill using prompts written the way developers ask questions, comparing results with and without the skill across multiple models. Pass rates improved in every suite we ran, and responses became more direct.

## Get started

For Redis development work, find Redis Development in the plugin browser in supported ChatGPT Work and Codex interfaces.

For other supported agents, the skills CLI remains available:

```
npx skills add redis/agent-skills
```

To analyze Redis data, use the Data agent in ChatGPT Work with your organization's approved Redis data connection. Once the connection is configured, start a conversation with @Data and ask your question.

## What's next

We'll keep refining the skills, adding guidance where it helps and removing what proves redundant.

The repository is MIT licensed and open to contributions. If an agent gives you bad Redis advice, open an issue with your prompt and the response. That feedback helps us improve the skills.
