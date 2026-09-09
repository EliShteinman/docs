---
title: "What’s new in two – October edition"
linkTitle: "What’s new in two – October edition"
url: "/blog/whats-new-in-two-october-25-edition/"
description: "Click here to view video"
date: 2025-10-31
blogCategories:
- "Tech"
authors:
- "Talon Miller"
lastmod: 2025-10-31
hidden: true
---

*By Talon Miller, Principal Technical Marketer · Published 31 October 2025*

![What’s new in two October](/images/site-mirror/321bfa4ddab6c03f5d9c28a6bc134922a018a3a5-1200x628.webp)

[Click here to view video](https://www.youtube.com/embed/eZgTtMguUPU?si=FlHfjN9l8b-zCEu9)

Welcome to “What’s new in two,” your quick hit of Redis releases you might have missed in the past month. We’re covering the latest developments from October and expanding on what I covered in our latest video. Press play above if you’d rather watch than read. Let’s get started.

## New AI Integrations

### Redis + Microsoft Agent Framework integration

In early October, Microsoft introduced its new Agent Framework, and at the same time, [Redis announced](https://www.globenewswire.com/news-release/2025/10/01/3159741/0/en/Redis-expands-partnership-with-Microsoft-announces-integration-of-Azure-Managed-Redis-into-Microsoft-Agent-Framework.html) its integration with this framework. This collaboration empowers developers on Azure to build scalable, resilient, and intelligent agentic applications. With the [Agent Framework](https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview) acting as the pluggable memory architecture, Redis serves as the high-performance, low-latency data store that powers those agents.

### Redis MCP Server integration in Gemini CLI

Redis also released our Redis MCP Server in the [Gemini CLI extensions](https://geminicli.com/extensions/). Our Redis MCP Server is a natural language interface designed for agentic applications to efficiently manage and search data in Redis. This enables direct access to the data stored in Redis, so you can verify the stored data, create test data samples, and more, all from the same place you are creating things, the Gemini CLI. You can check out the [project here](https://github.com/redis/mcp-redis).

### Redis vector node integration on n8n

We’ve contributed a new Redis Vector Store Node to the open-source n8n automation platform, now available since version 1.116 (for both cloud and self-hosted deployments). Built on the LangChain.js Redis implementation, this new node enables seamless vector storage and retrieval directly within n8n workflows. It includes advanced features such as index validation, client reuse, TTL and overwrite options, and metadata filtering for efficient vector management. This contribution strengthens Redis’ position as a high-performance vector database and expands developer access to native AI workflow integrations across the n8n ecosystem. [Check out the docs here](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.vectorstoreredis/) to learn more.

## Redis Software 7.22.2

Redis released [Redis Software version 7.22.2](https://redis.io/docs/latest/operate/rs/release-notes/rs-7-22-releases/rs-7-22-2-14/), featuring an important security enhancement. With this update, Redis Enterprise customers can now provide their own trusted certificates for internode encryption, replacing the default self-signed certificates. This improvement strengthens compliance with customer security policies, many of which restrict or prohibit the use of self-signed certificates. Get the latest [download here](https://redis.io/downloads/#Redis_Software).

## New Redis Insight UI on Redis Cloud

Introducing the new Redis Insight Cloud UI - a sleeker, more intuitive way to explore and work with your Redis Cloud data. The refreshed interface offers a unified look and smoother navigation. With Browser and Workbench now front and center in the top menu, it’s easier than ever to visually interact with your data, run commands, and learn through built-in tutorials. Whether you’re just getting started with Redis or optimizing production workloads, Redis Insight helps you move faster and get more out of Redis Cloud. Available now on the Essentials and Free tiers.

## Metrics Engine 2.0 and Observability tutorial

In October, Redis announced the general availability of the new [Metrics Stream Engine](https://redis.io/docs/latest/operate/rs/monitoring/metrics_stream_engine/) for Redis Software version 8.0. Built on an exporter-based architecture, this next-generation monitoring system delivers more accurate, real-time data for improved observability and faster incident response. The Metrics Stream Engine introduces the new /v2 Prometheus scraping endpoint, enabling seamless integration with external monitoring tools like Grafana, DataDog, New Relic, and Dynatrace. By exporting raw rather than aggregated data, it provides greater accuracy and scalability for large deployments, along with full visibility during maintenance events such as shard failovers and scaling operations.

Alongside the new Metrics Stream Engine, Redis has released a comprehensive [Observability Quick Start Tutorial](https://redis.io/learn/operate/observability/redis-software-prometheus-and-grafana) to help users deploy a full monitoring stack for Redis Software in under an hour. The tutorial walks system administrators and DevOps professionals through setting up Prometheus and Grafana with preconfigured dashboards using the new v2 metrics engine, enabling real-time visibility, alerting, and deeper insights into cluster performance. It also covers transitioning from v1 to v2 metrics, interpreting key dashboards, and customizing monitoring for production environments, providing a fast path to enhanced observability and proactive system health management.

## Redis acquires Featureform

On October 9th [Redis announced](https://www.globenewswire.com/news-release/2025/10/09/3164211/0/en/Redis-Acquires-Featureform-to-Help-Developers-Deliver-Real-time-Structured-Data-into-AI-Agents.html) the acquisition of [FeatureForm](https://www.featureform.com/), a robust framework for managing, defining, and orchestrating machine learning features. This acquisition strengthens Redis’ ability to address one of the most significant challenges in production AI: delivering structured data to models quickly, reliably, and with complete visibility.

That’s a wrap on October updates. And if you missed [last month’s update](https://youtu.be/80gBENktz6c), two minutes is all you need to catch up. Whether you prefer watching or reading, catch more valuable updates in my next two-minute episode. See you next time.
