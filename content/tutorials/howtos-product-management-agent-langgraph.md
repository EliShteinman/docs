---
title: "Building a product management agent (PM Maestro) with Redis and LangGraph"
linkTitle: "Building a product management agent (PM Maestro) with Redis and LangGraph"
url: "/tutorials/howtos/product-management-agent-langgraph/"
description: "PM Maestro is an AI-powered demonstration agent built using LangGraph.js, Redis and Tavily, designed to automate common Product Management tasks. Redis is used for memory management—including..."
group: "For developers"
aliases:
- "/tutorials/howtos-product-management-agent-langgraph/"
date: 2026-02-25
lastmod: 2026-02-25
hidden: true
---

*Published 25 February 2026*

> **TL;DR:**
>
> PM Maestro is an AI product management agent built with LangGraph.js and Redis. It automates market research and PRD generation using Redis as a checkpointer for short-term memory, a semantic or JSON cache for LLM responses, and a vector database for document retrieval.

## What you'll learn

- How to build a multi-tool AI agent with [LangGraph.js](https://langchain-ai.github.io/langgraphjs/) and [Redis](https://redis.io/learn)
- How to use Redis as a checkpointer for agent short-term memory
- How to implement semantic caching and JSON caching with Redis to reduce LLM costs
- How to orchestrate multi-step AI workflows for market research and PRD generation
- How to integrate optional data sources (Salesforce, Jira) and trigger workflows via Slack

## Prerequisites

- [Node.js](https://nodejs.org/) (v18+)
- A [Redis Cloud](https://redis.io/try-free/) instance or local Redis server
- An [OpenAI API key](https://platform.openai.com/signup)
- A [Tavily API key](https://tavily.com/) for web search
- Basic familiarity with TypeScript and AI agent concepts

## Introduction

PM Maestro is an AI-powered demonstration agent built using [LangGraph.js](https://langchain-ai.github.io/langgraphjs/), [Redis](https://redis.io/learn) and [Tavily](https://tavily.com/), designed to automate common Product Management tasks. **Redis** is used for memory management—including **checkpointers**, **vector databases**, and a **LLM cache**—demonstrating how developers can build robust, AI-driven workflows for real-world scenarios.

Product Managers frequently spend substantial time on repetitive yet essential tasks, such as collecting customer feedback, performing market research, estimating effort, and drafting product requirements. **PM Maestro**, powered by LangGraph JS, illustrates how these tasks can be effectively automated using AI agents. This repository serves as a practical demonstration of integrating LangGraph with advanced memory management features provided by **Redis**, including checkpointers, LLM caching, and vector databases, to create reliable, modular AI workflows. If you're interested in vector-powered retrieval, see also [How to Build a RAG GenAI Chatbot Using Vector Search with LangChain and Redis](/tutorials/howtos/solutions/vector/gen-ai-chatbot/).

## Tech stack

- **Language**: TypeScript (NodeJS)

- **Framework**: [LangGraph JS](https://langchain-ai.github.io/langgraphjs/) (Workflow orchestration)

- **Database**: [Redis](https://redis.io/learn) (Checkpointer and LLM cache)

- **LLM Provider**: OpenAI

- **Search Tool**: Tavily (Web search)

- **Slack Bot Integration (Optional)**: Trigger workflows via Slack

- **Salesforce Data Integration (Optional)**: Enrich context with Salesforce CRM data

- **Jira Data Integration (Optional)**: Enrich context with Jira data

## Project setup

### Clone the repository

```bash
git clone https://github.com/redis-developer/langgraph-pm-maestro.git
cd langgraph-pm-maestro
```

### Install dependencies

```bash
npm install
```

### Configure environment variables

Create your own configuration by copying the example environment file:

```bash
cp .env.example .env
```

Set the following key environment variables:

```bash
# .env
# OpenAI API
OPENAI_API_KEY=""
OPENAI_MODEL_NAME="gpt-4o-mini"

# Tavily Search API
TAVILY_API_KEY=""

# Redis
REDIS_URL=""
```

Note :

- Obtain your `OPENAI_API_KEY` from [OpenAI](https://platform.openai.com/signup)

- Obtain your `TAVILY_API_KEY` from [Tavily](https://tavily.com/)

### Run the application

```bash
npm run dev
```

This command starts the agent locally. Open the LangGraph Studio interface in your browser using the following URL:

```bash
https://smith.langchain.com/studio?baseUrl=http://localhost:2024
```

(Testing in Chrome browser is recommended)

## What workflows does PM Maestro support?

**PM Maestro** supports two primary workflows that demonstrate the capabilities of LangGraph and Redis. These workflows can be adapted easily to various domains or roles:

### 1. Market research workflow

This workflow performs competitor analysis through web searches and generates a PDF containing a feature comparison matrix of various market players.

### 2. PRD generation workflow

This workflow generates a comprehensive Product Requirements Document (PRD) by integrating market research data with information from Jira and Salesforce. The PRD includes MVP scope, effort estimations, technical considerations, and prioritized requirements.

## How does the market research workflow work?

Below is the workflow graph illustrating the market research process:

![Market research workflow graph showing feature extraction and competitor analysis](/images/site-mirror/0e9d44c01afb57d7ead31a10de480cf709779b16-570x708.webp)

The **competitorSubgraph** includes additional nodes to retrieve competitor lists and detailed feature information.

![Competitor subgraph workflow diagram for identifying and analyzing market players](/images/site-mirror/7520719af451de3ce646b60daf2b47e907a4bc24-610x668.webp)

Let's examine each node in the workflow:

- **extractProductFeature**: Extracts the specific product feature from the user's input.

```json
// Input: "Create PRD for stored procedures feature"
// Output
{
    "productFeature": "stored procedures"
}
```

- **fetchCompetitorList**: Uses the **Tavily** web search to identify competitors associated with the given product feature.

```json
// Output
{
    "competitorList": ["SQL Server", "Oracle", "MySQL", "PostgreSQL"]
}
```

- **fetchCompetitorFeatureDetails**: Retrieves detailed information about each competitor's implementation of the feature using **Tavily**.

```json
// Output
{
    "competitorFeatureDetailsList": [
        {
            "competitorName": "SQL Server",
            "featureDetails": "Stored procedures in Microsoft SQL Server are a powerful feature that allows users to encapsulate a group of one or more Transact-SQL (T-SQL) statements into a single callable unit..."
        },
        {
            "competitorName": "Oracle",
            "featureDetails": "Oracle Database provides a robust stored procedures feature that allows developers to encapsulate business logic within the database. This feature enhances performance, security, and code reuse, making it a powerful tool for building maintainable database apps...."
        }
    ]
}
```

- **createCompetitorTableMatrix**: Compiles competitors' feature details into a structured comparison table.

- **createCompetitorAnalysisPdf**: Generates a PDF containing the competitors' feature details and the comparison matrix.

![Animated demo of the market research workflow running in LangGraph Studio, showing each node executing in sequence](/images/site-mirror/345e63839e5676ba31fdaaa4fc06e8c51ae0109a-500x530.webp)

After running the workflow in LangGraph Studio, the generated PDF is saved in the **./prd-files** folder as **competitor-analysis-<date-time>.pdf**.

**Note**: You can customize the prompts located in the **src/agent/prompts/** directory as required.

## How does the PRD generation workflow work?

Below is the graph depicting the PRD (Product Requirements Document) generation workflow:

![PRD generation workflow graph integrating Jira and Salesforce data](/images/site-mirror/353e1ea07b3c2b7c1f56c95a49d8eb04420fa84a-452x688.webp)

Expanded **prdGenerationSubgraph :**

![Expanded PRD generation subgraph detailing customer demand analysis and effort estimation](/images/site-mirror/7d325277711e2556a563c8f5777629aeb2a54769-416x1048.webp)

The nodes **extractProductFeature** and **competitorSubgraph** are identical to those in the Market Research workflow.

Additional nodes are described below:

- **customerDemandAnalysis**: Aggregates customer demand data from Jira and Salesforce related to the requested product feature.

- **effortEstimation**: Estimates the implementation complexity and effort based on competitor analyses and optional customer demand data.

```json
// Output
{
    "tshirtSize": {
        "size": "M",
        "personMonths": 4.5, //over all effort
        "rationale": "Medium complexity with existing infrastructure support"
    },
    "components": [
        // sub tasks effort
        {
            "name": "Backend API",
            "description": "Implement REST endpoints for data processing",
            "effortMonths": 2,
            "customerImpact": "Enables real-time data access for FinTech Solutions",
            "technicalComplexity": "Medium"
        }
        //...
    ]
}
```

- **prdGenerationSubgraph**: Creates PRD sections including executive summary, customer analysis, market research, product strategy, and implementation strategy.

- **markdownToPdf**: Converts the PRD markdown content into a PDF document.

![Animated demo of the PRD generation workflow running in LangGraph Studio, showing competitor analysis and document creation steps](/images/site-mirror/172fc02514f80dde1ba784b2a216811096b8f928-500x530.webp)

After executing the workflow in LangGraph Studio, the resulting PDF is saved in the **./prd-files** directory with the filename **mini-prd-<date-time>.pdf**.

**Note:** You can adjust the prompts in the **src/agent/prompts/** folder to suit your specific needs.

## Salesforce integration (optional)

To integrate Salesforce, sign up at [Salesforce Developer](https://developer.salesforce.com/signup) to obtain your **SF_USERNAME** and **SF_PASSWORD**. You'll also need a **SF_SECURITY_TOKEN**, which you can get from your Salesforce account by navigating to **Settings -> Personal Information -> Reset Security Token**.

Configure the following environment variables:

```bash
# .env
# ==============================================
# SALESFORCE CONFIGURATION
# ==============================================
SF_USERNAME="your Salesforce username"
SF_PASSWORD="your Salesforce password"
SF_SECURITY_TOKEN="your Salesforce security token"
SF_LOGIN_URL="https://login.salesforce.com"

# Example Search Query (SEARCH_FIELD will be dynamically replaced with the requested feature)
SF_SEARCH_FEATURE_QUERY="FIND {SEARCH_FIELD} IN ALL FIELDS RETURNING TechnicalRequest(Id, Name, painPoint, featureRequestDetails, potentialDealSize, industry, priority, currentWorkaround, businessImpact)"
```

Note: Customize **SF_SEARCH_FEATURE_QUERY** according to your Salesforce organization's structure and objects. Restart the application after updating the environment variables.

## Jira integration (optional)

To integrate Jira, create an account on [Atlassian](https://id.atlassian.com/signup) and set up a Jira Cloud instance. Generate your API token from your Atlassian account's security settings.

Configure the following environment variables:

```bash
# .env
# signed up profile
JIRA_BASE_URL=https://yourdomain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your_api_token
# Sample JQL Query - SEARCH_FIELD will be automatically replaced with requested feature
JIRA_JQL_QUERY="project = 'CPG' AND textfields ~ 'SEARCH_FIELD' ORDER BY created DESC"
```

Note: Adjust the **JIRA_JQL_QUERY** to fit your specific Jira project and data structure. Restart the application after updating the environment variables.

## Slack bot integration

Follow the [Slack integration guide](https://github.com/redis-developer/langgraph-pm-maestro/blob/main/docs/how-tos/slack.md) to create and configure your Slack app. After setup, configure the following environment variables in your .env file:

```bash
# .env
SLACK_SIGNING_SECRET="your signing secret"
SLACK_BOT_TOKEN="your bot token"
SLACK_APP_TOKEN="your app token"
SLACK_BOT_PORT=8080
```

Start your Slack bot locally with:

```bash
npm run start-slack-bot
# (console output) ⚡️ Slack bot is running and connected!
```

You can trigger the workflows using these Slack slash commands:

- **/pm-market-research**: Executes the market research workflow.

- **/pm-prd**: Executes the PRD generation workflow.

In your Slack workspace, test the bot commands with messages like:

```bash
/pm-market-research stored procedures feature
# OR
/pm-prd stored procedures feature
```

The Slack channel displays intermediate messages and final results.

![Animated demo of the PM Maestro Slack bot responding to a market research slash command with intermediate results](/images/site-mirror/746c7f1e596eab26ba2a166ddcf2059b34ecde4a-500x356.gif)

## How does Redis provide short-term memory for AI agents?

In AI agents, short-term memory refers to the temporary storage of recent information or states that an agent needs immediate access to, enabling it to maintain context and continuity throughout its workflow execution.

LangGraph utilizes a checkpointer to implement short-term memory, allowing the agent to persist intermediate states and recover seamlessly in case of interruptions. In this demonstration, **Redis** serves as the **checkpointer**, providing robustness, reliability, and resilience to the agent's workflow execution. For a deeper dive into how agent memory works with Redis, see [What is Agent Memory? Example using LangGraph and Redis](/tutorials/what-is-agent-memory-example-using-langgraph-and-redis/).

Below is a screenshot illustrating checkpointer data stored in [Redis Insight](https://redis.io/insight/):

![Redis Insight showing checkpointer data stored as Redis hashes](/images/site-mirror/bbc0e449c49ac9fd4fefbb26c0324c552fd74a85-1825x987.webp)

**Note**: In this demo, a custom Redis checkpointer is implemented, as an official JavaScript integration is not yet available. For the official `Python` Redis checkpointer and store integration with LangGraph, refer to the [Python integration repository.](https://github.com/redis-developer/langgraph-redis)

## How does Redis caching reduce LLM costs in agent workflows?

Caching is employed to **speed up repeated queries** and **reduce costs**. When you rerun a workflow, cached responses are retrieved directly from Redis, eliminating redundant LLM calls and enhancing overall performance.

### Semantic cache (Redis Langcache)

- Utilizes vector embeddings (such as OpenAI embeddings) to store and retrieve cache entries based on semantic similarity rather than exact textual matches.

- When a new prompt is processed, its embedding is compared against cached entries. If a sufficiently similar entry exists, based on a configurable similarity threshold, the cached response is returned.

- Enables the retrieval of relevant cached results even when the wording of prompts changes, as long as the underlying meaning remains similar.

- Managed by Redis, Langcache is a service that handles embeddings, similarity search, and metadata within Redis.

- Ideal for scenarios where prompts may differ in phrasing but share the same intent or meaning.

### JSON cache

- Stores and retrieves cached entries using exact matches on prompt text along with associated metadata (e.g., feature, node name, user).

- Leverages Redis JSON capabilities for rapid lookups.

- Returns cached responses only if the prompt and metadata match exactly. Semantic similarity is not considered.

- Simpler and faster for identical, repeat queries but less adaptable to natural language variations. Recommended for workflows where agent node inputs remain static or predictable.
  Below is a screenshot illustrating cache data in [Redis Insight](https://redis.io/insight/):

![Redis Insight displaying JSON cache data for workflow optimization](/images/site-mirror/14ea83e7de266ca49449125a75683f1c6b39ef26-1825x999.webp)

**Note:** By default, JSON cache is enabled in this demo, since after the product feature is extracted, most subsequent node inputs are predictable keywords and well-suited for exact-match caching. However, you can enable semantic caching (Langcache) by configuring the following environment variables:

```bash
# .env
LANGCACHE_URL="http://localhost:8080"
LANGCACHE_CACHE_ID="cacheUUID1"
LANGCACHE_ENABLED=""
```

## Conclusion

PM Maestro demonstrates the practical capabilities of combining **LangGraph JS, Redis, Tavily**, and modern AI techniques to create efficient and robust workflows tailored for Product Management. You can further customize and expand these workflows to suit your specific requirements.

## Next steps

Now that you've seen how to build a product management AI agent with Redis and LangGraph, here are some ways to go further:

- **Explore agent memory in depth:** Learn how short-term and long-term memory work for AI agents in [What is Agent Memory? Example using LangGraph and Redis](/tutorials/what-is-agent-memory-example-using-langgraph-and-redis/).
- **Build a RAG chatbot:** See how Redis vector search powers retrieval-augmented generation in [How to Build a RAG GenAI Chatbot with Redis](/tutorials/howtos/solutions/vector/gen-ai-chatbot/).
- **Try Redis Cloud for free:** Spin up a managed Redis instance at [redis.io/try-free](https://redis.io/try-free/).
- **Visualize your data:** Use [Redis Insight](https://redis.io/insight/) to inspect checkpointer state, cached responses, and vector embeddings.
- **Check out the Python integration:** See the official [Redis LangGraph checkpointer and store](https://github.com/redis-developer/langgraph-redis) for Python projects.
