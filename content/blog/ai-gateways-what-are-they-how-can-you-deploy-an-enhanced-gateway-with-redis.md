---
title: "AI gateways: What are they & how can you deploy an enhanced gateway with Redis?"
linkTitle: "AI gateways: What are they & how can you deploy an enhanced gateway with Redis?"
url: "/blog/ai-gateways-what-are-they-how-can-you-deploy-an-enhanced-gateway-with-redis/"
description: "As more and more companies deploy GenAI apps in production, we’re hearing about a new set of challenges that are different from the initial “POC phase of GenAI.” These new challenges are driven..."
date: 2024-11-13
blogCategories:
- "Uncategorized"
authors:
- "Manvinder Singh"
lastmod: 2025-07-03
hidden: true
---

*By Manvinder Singh, VP of AI Products · Published 13 November 2024 · updated 3 July 2025*

![Blog tile image](/images/blog/14857a9f0a96421af91a7f823b569fe715c991c6-772x552.webp)

As more and more companies deploy GenAI apps in production, we’re hearing about a new set of challenges that are different from the initial “POC phase of GenAI.” These new challenges are driven more by the need to scale and secure usage, especially when they’re deploying apps that interface with users outside of the organization. Because of this, companies are starting to use AI gateways (or “LLM gateways” or “GenAI gateways”) as a key component in their AI infrastructure.

## What’s an AI gateway?

An **AI Gateway** is a service that simplifies, secures, and governs access to Large Language Models (LLMs) within an enterprise setting. It acts as a centralized platform for managing AI workflows, giving developers a consistent interface (or endpoint) to interact with models from different providers. The gateway optimizes and secures LLM usage with features like rate-limiting, PII redaction, caching, guardrails, usage tracking, chargebacks, fallbacks, and routing.

Here are a few popularly quoted examples of GenAI gateways already used in the industry:

- ‘[Uber’s GenAI gateway](https://www.uber.com/blog/genai-gateway/)’ gives developers one unified platform to access multiple LLMs—from OpenAI, Vertex AI, and Uber’s own models—through a single, consistent interface that mirrors OpenAI’s.
- ‘[Roblox’s ML gateway](https://corp.roblox.com/newsroom/2024/09/running-ai-inference-at-scale-in-the-hybrid-cloud)’ centralizes access to large AI models, combining both in-house and open-source options, to create a more efficient system for managing AI resources.
- ‘[BT’s GenAI gateway platform](https://press.aboutamazon.com/aws/2024/9/bt-groups-digital-unit-launches-genai-gateway-platform-powered-by-aws-accelerating-the-companys-safe-adoption-of-generative-ai-at-scale)’ lets the company securely and privately access different LLMs from providers. It also includes essential features like centralized privacy controls, use-case-based billing, and enterprise search.

In each of these examples, the gateway sits between the apps and the underlying LLMs, acting as a gatekeeper. It controls data access, enforces adherence to established rules, and monitors how GenAI apps behave. Plus, by abstracting away the different AI APIs, organizations can avoid locking into specific providers and stay flexible as the AI landscape evolves.

![](/images/blog/dc97157b9d39e1c0ed82632230c2ddba389e9684-3840x2160.webp)

## Eight key features every AI gateway needs

An AI gateway platform brings together a range of essential features, often customized to fit each enterprise’s needs. But there are eight key capabilities that every gateway should have—widely adopted across enterprise setups.

1. **Unified API**: Provides a single, consistent interface to access and interact with multiple AI models and providers, often using a widely used standard like the OpenAI API for ease of use and compatibility.
1. **Rate Limiting**: Lets you flexibly route AI requests to different models based on specific criteria to manage workloads. This may include load balancing for performance optimization, fallback mechanisms for handling failures or capacity limits per app.
1. **Routing **(based on intent)**: **Directs requests to the most appropriate model for each task, often on the basis of a semantic comparison of incoming request’s meaning against predefined routes. This is usually implemented a [Semantic Router](https://www.redisvl.com/user_guide/semantic_router_08.html).
1. **Caching: **Improves latency and cost for inference by caching LLM responses in a distributed in-memory database. With a [Semantic Cache](/blog/what-is-semantic-caching/), incoming queries can be semantically compared with cached queries for better hit-rates and smoother performance.
1. **PII Redaction: **Keeps sensitive information safe by masking or redacting data before it’s sent to external AI models. This prevents data leaks and ensures you’re staying compliant with privacy regulations.
1. **Guardrails:** Ensures responsible AI use by adding safety checks and guardrails to filter out harmful or inappropriate content, detect and block requests with sensitive data, and moderate AI-generated outputs for quality and compliance**.**
1. **Usage tracking **(and chargebacks): Keeps spending on AI services in check by tracking token usage, setting budget limits, cost chargebacks and analyzing usage patterns by app, user, or department.
1. **Credentials management:** Safeguards AI usage with centralized management of keys for external services like LLM & embedding generation providers, such as OpenAI, Anthropic, and Hugging Face.

![](/images/blog/512bdad4d40fbb47d47c3546c2c45d9830659e7c-3840x2160.webp)

## Build your AI gateway

New gateway solutions from Kong, Databricks, Portkey, and Cloudflare offer an easy deployment option for many teams. Still, plenty of enterprise customers are building custom platforms to fit their specific environments and needs.

Even teams building their own gateways can benefit from established open-source and enterprise solutions that provide essential components. Here is a list of commonly used technologies that can be used to construct GenAI gateways or Platforms:

- [LiteLLM](https://github.com/BerriAI/litellm): LiteLLM is a tool that provides a standardized way to access a wide array of large language models (LLMs) from different providers through a single API1. This simplifies the process of interacting with and comparing various LLMs.
- [Guardrails AI:](https://github.com/guardrails-ai/guardrails) A framework that helps build reliable AI apps by running Input/Output Guards in your app that detect, quantify and mitigate specific types of risks such as PII leakage, profanity, off-topic conversations etc.
- [Langfuse](https://github.com/langfuse/langfuse): Covers usage tracking with its open-source suite for LLM observability, metrics, evals, and prompt management. Langfuse integrates with LlamaIndex, Langchain, OpenAI SDK and LiteLLM.
- [Hashicorp vault](https://github.com/hashicorp/vault): Manages secure secrets, encryption as a service, and privileged access control management and can be used to manage credentials for AI API services. Redis is [one of the supported databases](https://developer.hashicorp.com/vault/docs/secrets/databases/redis) for Hashicorp Vault.
- [Redis](https://redis.io/): A high-performance, all-in-one data platform and vector search solution, that can power key AI Gateway services. Up next, we’ll explore why Redis is the ideal data stack for building scalable AI Gateways.

## Redis’ role in enhancing AI gateways:

Redis powers AI gateways with the speed and flexibility they need. With top-tier performance—including the [fastest vector search benchmarks](/blog/benchmarking-results-for-vector-databases/)—and versatile support for multiple data types, Redis seamlessly handles caching, routing, rate limiting, credentials management, guardrails, and PII redaction. Below are some useful links that describe how to use Redis for these use-cases:


- **Retrieval augmented generation (RAG): **Redis vector database offers the fastest vector search and data retrieval available to make GenAI apps faster. By combining fast data access with LLMs through AI gateways, teams get performant and accurate RAG. See [here](https://redis.io/docs/latest/develop/get-started/rag/) to get started with RAG with Redis.
- **Rate-limiting:** Redis supports a range of rate-limiting algorithms—like fixed window, sliding window, and token bucket—and can handle a large number of requests per second, making it ideal for rate-limiting. Teams can set limits per model, load-balance across models, or even create fallback routes if a model hits its limit. Check out this [guide](https://redis.io/learn/howtos/ratelimiting) to implementing rate-limiting in python with Redis.
- **Caching: **Redis is the top choice for caching model responses, with low latency and powerful caching features. By using a semantic cache that searches for similar queries and returns responses on cache hits, organizations can cut down on both latency and inference costs. Redis makes semantic caching easy with its [RedisVL](https://www.redisvl.com/) Python client library. Learn more [here](https://redis.io/docs/latest/integrate/redisvl/user-guide/semantic-caching/).
- **Router and guardrails:** Redis delivers high-performance vector search that’s perfect for building a fast, low-latency router. Developers can define routes based on sample queries, then use semantic search to direct incoming requests to the right models. This approach also allows blocking certain query types and adding guardrails for safety. Find a detailed guide on setting up a semantic router using Redis and RedisVL [here](https://www.redisvl.com/user_guide/semantic_router_08.html).
- **Other use-cases **(storing credentials, usage data, PII etc.): Redis’ versatility and support for multiple data types make it a solid choice as the database behind various gateway services. For example, Redis can be used as the storage layer for Hashicorp Vault’s secret manager, securely hold PII data retrieved during the masking process, and storing usage data as part of a custom observability platform. With Redis, developers get a single platform that covers multiple use cases—no juggling different databases required.

![](/images/blog/94fbb3d41f61f4a73ebd95d11a726bcd426e9f52-3840x2160.webp)

Finally, Redis is available across multiple platforms and can be deployed in both public cloud (as a managed service or self-managed software) and on-prem. This flexibility is key for organizations running ML models across both cloud and on-prem environments.

## Let’s start building

Using Redis to power your AI gateway lets you build a robust system that secures, controls, and optimizes your GenAI apps—all while supporting ethical practices. Check out the resources below to start building with Redis today, or connect with our team to chat about AI gateways.

- [Redis AI resources](https://github.com/redis-developer/redis-ai-resources): GitHub repo with code samples and notebooks to help you build AI apps.
- [Redis AI Docs :](https://redis.io/learn/vector/) Quickstarts and tutorials to get you up and running fast.
- [Redis Cloud](https://redis.io/try-free/): The easiest way to deploy Redis—try it free on AWS, Azure, or GCP.
