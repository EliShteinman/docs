---
title: "Introducing Model Context Protocol (MCP) for Redis"
linkTitle: "Introducing Model Context Protocol (MCP) for Redis"
url: "/blog/introducing-model-context-protocol-mcp-for-redis/"
description: "Model Context Protocol (MCP) is a standard developed by Anthropic that lets AI agentic apps use external data and tools. Think of it like a universal adapter that helps AI go beyond its training by..."
date: 2025-05-22
blogCategories:
- "Tech"
authors:
- "Mirko Ortensi"
lastmod: 2026-06-01
hidden: true
mirrored: true
---

*By Mirko Ortensi, Sr. Product Manager, Products · Published 22 May 2025 · updated 1 June 2026*

![Blog tile image](/images/site-mirror/f2a64afcd972d20eff117808d729658934ce2301-772x552.webp)

Model Context Protocol (MCP) is a standard [developed by Anthropic](https://www.anthropic.com/news/model-context-protocol) that lets AI agentic apps use external data and tools. Think of it like a universal adapter that helps AI go beyond its training by tapping into real-time info and capabilities, like pulling weather forecasts, live stock prices or checking your calendar.

MCP is built to solve common pain points around how AI accesses and works with information.

1. **Static knowledge limitations**: Most AI models are trained once and can’t access new or real-time data. MCP lets them connect to live data sources, making their responses more current and valuable.
1. **Tool interoperability**: AI models often need external tools (like search engines, databases, calculators), but there’s no universal way to connect. MCP provides a standardized interface so models can interact with tools more easily.
1. **Fragmented ecosystems**: Every integration between an AI and a tool must be custom-built without a standard protocol. MCP cuts the overhead by creating a plug-and-play system.
1. **Context switching**: AI agents often struggle to maintain and manage context when switching between different tools or data. MCP helps maintain a coherent model of context across different sources and tools.
1. **Scalability**: Scaling AI systems is difficult when each tool integration is a one-off. MCP makes it easy to scale by breaking the tight link between your models and the tools or data they rely on.

MCP integrations are available on Claude Desktop and extended to platforms like GitHub Copilot, Cursor, Augment, the OpenAI Agents SDK, and more.

That’s why we’re excited to introduce Redis’ MCP servers through two open-source projects:[mcp-redis](https://github.com/redis/mcp-redis) and [mcp-redis-cloud](https://github.com/redis/mcp-redis-cloud).

## The Redis MCP server

The [mcp-redis](https://github.com/redis/mcp-redis) project is a natural language interface designed to manage and search data in Redis. It integrates with [MCP clients](https://modelcontextprotocol.io/docs/concepts/architecture), enabling AI-driven workflows to interact with structured and unstructured data in Redis. The MCP Server makes it easy to work with everything Redis supports: strings, hashes, JSON documents, lists, sets, sorted sets, vector embeddings, etc. The server also makes available server management tools to perform a Redis database health check. Using the Redis MCP Server, the MCP client app can resort to Redis for popular use cases such as session management, conversation history, real-time caching, rate limiting, recommendations, or semantic search for retrieval augmented generation (RAG).

You can integrate this MCP Server in a few clicks using registries like the popular [Smithery platform](https://smithery.ai/server/@redis/mcp-redis), using the [pre-built Docker image](https://hub.docker.com/r/mcp/redis) made available on Docker Hub. You can also build your Docker image or clone the project and run the server locally.

MCP works with the tools you already use. IDEs like VS Code with GitHub Copilot, Cursor, and Claude Desktop support it out of the box—so you can talk to your Redis server no matter where it’s running: local, Docker, or Redis Cloud. Just connect the server you want and you’re ready to go.

![The Redis MCP server](/images/site-mirror/1bbaa95c23c006f53f6e85d9e99e88dc321b8900-1404x937.webp)

Integrating natural language processing into your IDE opens up new possibilities to boost user experience when working with app data. But MCP is much more. You can build powerful agentic apps in SDKs such as the OpenAI Agents SDK. The [SDK supports MCP](https://openai.github.io/openai-agents-python/mcp/) so that you can provide your MCP tools to agents.

Building complex apps is much easier by plugging in the desired functionalities exposed by the many existing MCP servers. You can find an [example](https://github.com/redis/mcp-redis/blob/main/examples/redis_assistant.py) in the mcp-redis repository. Provide as many MCP servers as you’d like, customize the agent’s instructions, and you’re ready to interact with it.

![The Redis MCP server Table](/images/site-mirror/8f60aa4b42d1e3d68a255b7d2441489e1a96e8a7-1600x854.webp)

## Redis Cloud API MCP server

The [mcp-redis-cloud](https://github.com/redis/mcp-redis-cloud) gives your AI agents direct access to your Redis Cloud subscription, so they can manage it without extra tooling. With the Redis Cloud API MCP server, you can use tools like Claude Desktop, Cursor, or any MCP-compatible IDE to manage your Redis Cloud account using natural language. For example:

- “Create a new Redis database in AWS”
- “What are my current subscriptions?”
- “Help me choose the right Redis database for my e-commerce app.”

This MCP server exposes the [Redis Cloud REST API](https://redis.io/docs/latest/operate/rc/api/) so you can bridge natural language instructions with programmatic Redis Cloud subscription management.

![Redis Cloud API MCP server](/images/site-mirror/a9b3ca8927152e18e7088c5d17b908fbb6e5b426-1600x709.webp)

If you want the ability to spin up databases for testing, manage your subscription, learn about the metrics of interest, or overload an existing app with the ability to create databases on demand, take a look at this server.

## Build smarter AI with MCP

From startups to enterprises, teams are looking at MCP to make their AI apps smarter:

- **Customer support bots**: Maintaining conversation history for more coherent interactions
- **Content generation**: Providing relevant reference materials to LLMs for accurate content creation
- **Personalized recommendations**: Incorporating user preferences and history into AI recommendations

MCP standardizes how tools bring in relevant context for GenAI, making it simpler to add new components and manage context effectively.

Built on Redis’ speed and flexibility, MCP offers a solid base for creating AI apps that are more capable, responsive, and context-aware. Try these MCP servers in your AI agentic app or integrate them into your development tools today; you’ll find instructions in the repositories. You can explore these projects, contribute to their development, and join us in shaping the future of AI agentic apps with Redis.
