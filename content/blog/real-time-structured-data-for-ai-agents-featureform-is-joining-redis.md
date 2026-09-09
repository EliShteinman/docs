---
title: "Real-time structured data for AI agents: Featureform is joining Redis"
linkTitle: "Real-time structured data for AI agents: Featureform is joining Redis"
url: "/blog/real-time-structured-data-for-ai-agents-featureform-is-joining-redis/"
description: "For developers building AI agents, context is everything."
date: 2025-10-09
blogCategories:
- "Tech"
authors:
- "Rowan Trollope"
lastmod: 2026-06-01
hidden: true
---

*By Rowan Trollope, CEO · Published 9 October 2025 · updated 1 June 2026*

![Real-time structured data for AI agents: Featureform is joining Redis](/images/site-mirror/0f1b7fc0da1a297112c1339e3a3760268e39cf10-1200x628.webp)

For developers building AI agents, context is everything.

AI agents need more than LLMs. They depend on real-time data, past interactions, and knowledge bases to deliver accurate results. Getting that context to models at the right time is one of the hardest challenges in production AI. Redis makes it simple by serving as the real-time data platform developers trust to power AI agents with memory, knowledge, and structured data.

That’s why we’re excited to announce that [Featureform](https://www.featureform.com/) is joining Redis. The acquisition adds a powerful framework for managing, defining, and orchestrating structured data signals to Redis’ speed and simplicity.

Together, Redis and Featureform will continue to serve AI developers. Featureform will be incorporated into Redis' feature store offerings within our real-time data platform for AI. It joins the fastest benchmarked vector database powered by [Redis Query Engine](https://redis.io/query-engine/), and the most advanced semantic caching service, [Redis LangCache](https://redis.io/langcache/).

## What is Featureform?

Featureform is a virtual feature store built on Apache Iceberg with out-of-the-box integrations with Snowflake, Clickhouse, Spark and more. It is designed to solve one of the hardest problems in production AI: getting structured data into models quickly, reliably, and with full observability.

At its core, Featureform isn’t just a place to store features. It’s a framework to:

- Define features as reusable, versioned pipelines
- Unify training and inference workflows across batch and streaming
- Maintain point-in-time correctness to support offline model training
- Serve low-latency features using caches like Redis in production
- Detect data drift and monitor changes to feature distributions over time

Simba Khadder, Featureform’s founder and CEO, describes the platform as a “motherboard” for AI infrastructure. It connects data sources, compute engines, and online stores into one cohesive system. Featureform integrates with the tools you already use, including Spark, Snowflake, Iceberg, Kafka, and of course, Redis.

## Redis + Featureform

Together, Redis and Featureform provide a complete end-to-end solution for managing and serving structured data in AI systems.

If you already use Redis as your online store, the acquisition of Featureform adds a flexible, declarative system for defining and orchestrating your features across training and inference. This means:

- No more disconnected pipelines for batch vs real-time
- No more manual rewrites from notebooks to production
- No more brittle glue code between Spark, Redis, and model APIs

With Redis + Featureform, you can:

- Define features once and use them everywhere
- Orchestrate batch, streaming, and real-time workflows in one framework
- Serve features instantly with Redis as the online store

This integration gives teams building GenAI, ML, and agentic systems a fully managed, Redis-native feature pipeline from raw data to low-latency inference.

And unlike traditional feature stores that tightly couple storage with logic, Featureform gives you orchestration without lock-in. It integrates with the tools you already use, while providing a simple, centralized way to manage the features that power your AI.

This work also connects to community efforts like [EnrichMCP](https://github.com/featureform/enrichmcp), which explores how agents can retrieve the right structured data on demand, and Featureform builds on this vision with a fully managed solution.

## Still flexible, still open

Redis and Featureform provide the easiest way to build an end-to-end structured data pipeline. But if you’re already using another feature store, Redis will continue to support you.

Redis remains committed to:

- Full support for existing integrations with [Feast](https://feast.dev/), [Tecton](https://www.tecton.ai/), and other popular feature stores
- Keeping Redis open and flexible as an online store for any feature store
- Offering Featureform’s capabilities as a Redis-native option, not a requirement

## Why now

The industry is moving beyond naive RAG and basic LLM orchestration. AI teams want to enrich prompts with user profile data, financial metrics, risk scores, and business logic. But those structured inputs live across different systems, and are often difficult to define, update, or govern at scale.

Featureform helps solve this by treating everything as a feature—not just tabular values, but embeddings, prompts, and model inputs. It gives you a shared language for defining and managing the building blocks of your AI system.

With Redis + Featureform, you can finally bridge the gap between fast vector search and rich structured context—delivering just the right information, at just the right time. You can serve both embeddings and features from the same platform. And you can do it with the speed, reliability, and simplicity you expect from Redis.

We are thrilled to welcome the Featureform team to Redis. We believe this combination will unlock a new level of performance and clarity for AI builders everywhere. If you would like to learn more about Redis and Featureform or how it can support your AI use case, please [get in touch with us](https://calendly.com/d/y5h-jpf-gj7/featureform-intro-call).
