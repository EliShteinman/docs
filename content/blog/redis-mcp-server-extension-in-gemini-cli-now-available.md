---
title: "Redis MCP Server extension in Gemini CLI now available"
linkTitle: "Redis MCP Server extension in Gemini CLI now available"
url: "/blog/redis-mcp-server-extension-in-gemini-cli-now-available/"
description: "Following Gemini CLI’s recent support for extensions, the Redis MCP Server is now available in the Gemini CLI extensions gallery."
date: 2025-11-17
blogCategories:
- "Tech"
authors:
- "Mirko Ortensi"
- "Vasko Chomakov"
lastmod: 2025-11-17
hidden: true
---

*By Mirko Ortensi, Vasko Chomakov · Published 17 November 2025*

![Redis Redis MCP Server now available in Gemini CLI ](/images/blog/06d2a51ae0512d2e437147c2f1dd0165f3db101a-1200x628.webp)

Following [Gemini CLI](https://github.com/google-gemini/gemini-cli)’s [recent ](https://blog.google/technology/developers/gemini-cli-extensions/)support for extensions, the [Redis MCP Server](https://github.com/redis/mcp-redis) is now available in the Gemini CLI [extensions gallery](https://geminicli.com/extensions/).

The Redis Model Context Protocol (MCP) Server is a natural language interface designed for code assistants and agentic apps to manage and search data in Redis efficiently. Redis is a popular real-time data store across several use cases, leveraging data structures like hashes, sets, lists, and sorted sets. Starting with Redis 8, JSON data modeling, real-time indexing and search, probabilistic data structures, and time series are available in Redis Open Source, Redis Software, and Redis Cloud.

Redis fulfills a range of use cases in modern GenAI and app development, serving as both short-term and long-term memory as well as powering semantic search, semantic caching, and fast, scalable data access. Through the standard MCP specifications, the Redis MCP Server bridges these capabilities with GenAI tools, allowing code assistants and agentic apps to query, update, and reason over Redis data using natural language. Installing the Redis MCP Server extension in Gemini CLI is quick and straightforward.

## Installing the Redis MCP Server extension

If you haven’t already, install Gemini CLI on your machine using the following command:

```sql
npm install -g @google/gemini-cli
```

You can also follow the [Gemini CLI installation guide](https://geminicli.com/docs/get-started/deployment/) for environment-specific instructions.

Next, browse the Gemini CLI [extensions gallery](https://geminicli.com/extensions/), find Redis, and click the “Copy” icon to get the installation command for the **redis extension**. Alternatively, you can run the following in your terminal:

```sql
gemini extensions install https://github.com/redis/mcp-redis
```

This will install and instruct the MCP Server to connect to a local Redis instance on the default port 6379. To connect to another server, you can also specify a URL connection string by setting the REDIS_URL environment variable.

After installation, start Gemini CLI and verify that the Redis MCP Server extension is available:

```sql
/extensions list
```

Under the /mcp [slash command](https://geminicli.com/docs/cli/commands/#slash-commands), you get more control over the installed MCP extensions. So, as an example, you can inspect the server’s JSON schema for the tools and their parameters:

```sql
/mcp schema
```

You can also view all installed MCP servers and their tools in a compact format:

```sql
/mcp list
```

## Working with Redis using the Redis MCP Server extension

You can use the Gemini CLI to get started with new projects or edit existing ones. Several powerful tools enable control over the overall coding experience, allowing users to create custom commands, manage memories, revert to previous versions, and more.

Redis is a natural fit for modern apps, providing building blocks for session management, caching, queuing, and leaderboards. With the Redis MCP Server extension, devs can access Redis directly from Gemini CLI: the same place they build, debug, and refine their code. This integration simplifies development by unifying the data and code layers in one environment.

Let’s say you are working on an app and want to implement session management using Redis. Redis is a common solution for scalable, highly available, and real-time apps. You can instruct Gemini CLI to develop an integration with Redis and provide context in the GEMINI.md file to instruct the model with your preferences. This refers specifically to the GEMINI.md file in your **project directory** (e.g., ~/projects/my-app/GEMINI.md), which defines the context for that particular integration. Other GEMINI.md files may exist, such as a **global** one at ~/.gemini/GEMINI.md and an **extension-specific** one at ~/.gemini/extensions/mcp-redis/GEMINI.md.

```sql
## Session Management

The app uses Redis to store user session data in JSON format. Each session is stored under a key prefixed with `session:<uuid>`, where `<uuid>` is a unique identifier for the session. The JSON document for each session has the following structure:

*   **`visited`**: A JSON array of unique song IDs that the user has viewed during the session. Song IDs are deduplicated to ensure each song is listed only once.
*   **`created`**: A Unix timestamp (integer) indicating when the session was first created.
*   **`updated`**: A Unix timestamp (integer) indicating the last time the session was updated.
  
A session is created for each user, and the number of songs viewed is tracked in the "visited" array.
```

If you would like to customize your experience further, you can modify the prompt with additional instructions, such as avoiding anti-patterns or providing specific recommendations.

```sql
## Custom Prompts and Guidelines

1. Never flush a Redis database, neither in code nor running redis-cli
2. Never use the KEYS command in a project
3. Use the node-redis client library to connect to Redis
```

When working with data, you may want to verify the execution of a functionality and review the state of the database. You can use [Redis Insight](https://redis.io/insight/), the official Redis dev tool with an intuitive UI, to quickly browse your data, profile the flow of commands to Redis, inspect JSON files, and more. This is an invaluable source of truth during development.

Alternatively, the Redis MCP Server’s natural language interface helps you issue the right commands and inspect results directly from Gemini CLI while your app runs:

```sql
> count the existing sessions

✓  scan_all_keys (redis MCP Server) {"pattern":"session:*"}                                         session:31f2032da547230149ad4d57766a3152                                                         session:cYl7jUxkfGNAFOeVTRthWctMj69vgDf62cJsQmhwk64                                              session:4w5a8jOQO8Ro9zyyyA2LNYh-VDHfZynbPCKQUrULzD8                                              

✦ I found 3 sessions.
```

The Gemini CLI knows from the contextual preferences that the app should store sessions in Redis as JSON documents, prefixed with "session:". The Redis MCP Server exposes tools for working with JSON documents, enabling users to ask direct questions about the data:

```sql
> check if there are duplicate songs in the sessions

 ✓  json_get (redis MCP Server) {"name":"session:31f2032da547230149ad4d57766a3152","path":".visited"}  

[
    "0",
    "1",
    "3",
    "2",
    "4"
]

[...]

✦ I checked the JSON session and found no duplicate songs in the visited lists. The app has a mechanism to prevent adding duplicate songs to the session, so this is the expected behavior.
```

Peeking into the database isn’t the only way to speed up your coding experience. If you’d like to add some random test data, you can do so without code additions to your project:


```sql
> Create three sessions with fake data, visited song IDs should exist in the database

[...]

✦ I have successfully created three sessions with fake data: session:fake_user_001, session:fake_user_002, and session:fake_user_003

> read session session:fake_user_002
✓  json_get (redis MCP Server) {"path":"$","name":"session:fake_user_002"}

✦ The content of session session:fake_user_002 is:

1 [
2   {
3     "visited": [
4       "2",
5       "4",
6       "1",
7       "0"
8     ],
9     "created": 1697037000,
10     "updated": 1697296200
11   }
12 ]
```

You can formulate complex questions that are easily solved using Gemini CLI and the Redis MCP Server extension, as well as write and verify complex data structures. Additionally, you can create, merge, update, or delete data in Redis.

## Where to learn more

You can learn more about the Redis MCP Server’s capabilities in our [docs](https://redis.io/docs/latest/integrate/redis-mcp/). To discover the Gemini CLI’s integration with MCP servers and customize your experience, read the following Gemini CLI [docs](https://geminicli.com/docs/tools/mcp-server/).
