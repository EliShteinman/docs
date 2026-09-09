---
title: "Build on Redis with one-click using Augment Code’s Easy MCP"
linkTitle: "Build on Redis with one-click using Augment Code’s Easy MCP"
url: "/blog/build-on-redis-with-one-click-using-augment-codes-easy-mcp/"
description: "If you’re a developer or vibe coder you’re probably already familiar with AI-powered coding assistants like Augment Code. These tools have a number of features, but they are all working largely on..."
date: 2025-07-31
blogCategories:
- "Tech"
authors:
- "William Johnston"
lastmod: 2026-01-13
hidden: true
---

*By William Johnston, Head of Technical Marketing · Published 31 July 2025 · updated 13 January 2026*

![Build on Redis with one-click using Augment Code’s Easy MCP](/images/site-mirror/ceedade2096b58000647da0b5b60d2057904782b-772x552.webp)

If you’re a developer or vibe coder you’re probably already familiar with AI-powered coding assistants like [Augment Code](https://www.augmentcode.com/). These tools have a number of features, but they are all working largely on fine-tuning the “agent” experience. The term “agent” can have a ton of meanings depending upon who you ask, but in the case of Augment Code, the “agent” is what you use to interact with your codebase. Augment Agent indexes your codebase and with the help of tools helps you build new features, iterate on existing features, fix bugs, and more.

One of the interesting features of Augment Agent is the ability to add [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) servers. In fact, Augment Code just released [Easy MCP](https://www.augmentcode.com/blog/announcing-easy-mcp), its one-click connection to various services (including Redis) that let Augment Agent seamlessly interact with external systems as first-class tools through natural-language commands. You can tell Augment Agent, “Generate some sample data in Redis based on the schema defined in my project.” The agent will look at the code in your project as well as use the [Redis MCP server](https://github.com/redis/mcp-redis) to understand the existing data in your database. Then it will come up with a plan and execute a series of commands against your Redis database to generate the data.

As an example, on my computer I have the [Redis Chat app](https://github.com/redis-developer/redis-chat) code (screenshot below), and I’m going to use Augment Agent and Redis MCP server to generate some sample data.

![Redis Chat](/images/site-mirror/9d1dc9dbb76ea628db7d7670ce5dd4bd1bc5976c-1768x1962.webp)

I’ll get to the setup later, here are the results:

## Using Augment Agent with Redis MCP server

I started with the following prompt:

“Can you generate some sample data in Redis based on the schema defined in redis-chat?”

Using the “[Enhance Prompt](https://www.augmentcode.com/blog/prompt-enhancer-live-in-augment-chat)” feature of Augment Code I transformed my simple prompt into:

“””

Please analyze the redis-chat application's data schema and generate realistic sample data in Redis that follows the defined structure. Specifically:

1. First, examine the codebase to understand the data models, schema definitions, and Redis key patterns used in the redis-chat application

2. Identify the main data entities (such as users, chats, messages, etc.) and their required fields

3. Create a comprehensive set of sample data that includes:

- Multiple users
- A variety of messages with timestamps, different message types, and realistic content
- Any other entities defined in the schema (like user sessions, etc.)

4. Use the Redis MCP Server tools to populate the Redis database with this sample data, ensuring:

- Proper key naming conventions as defined in the application
- Correct data types (strings, json, streams, etc.) for each entity
- Realistic relationships between entities (message threads, etc.)
- Appropriate data volumes for testing (enough to be meaningful but not overwhelming)

The goal is to create a realistic dataset that would allow developers to test the redis-chat application's functionality with meaningful data rather than empty or minimal test data.

“””

This “Looked Good To Me™” so I clicked to run it with Augment Agent. Here is a [recording of the full output](https://drive.google.com/file/d/1f3G31uDP6d5pCKnw3auhrk2V2iYbNd0I/view?usp=drive_link).

Here are some screenshots with some interesting output from Augment Agent.

### Augment Agent looks at your codebase and Redis

Not only did Augment Agent look at my code to determine the structure of the data I wanted to generate, it also used Redis MCP server to understand the data:

![Augment Agent looks at your codebase and Redis](/images/site-mirror/340906b001901cbf6edcc9b854e1ce561e462c5c-1464x902.webp)

After running a few more Redis commands, Augment Agent spit out the following schema analysis:

![Redis Data Schema Analysis](/images/site-mirror/b48d809119c63b0a41020361fa3c0de5fbef02cb-1404x738.webp)

This was exactly how I expected the data to look, so I let Augment Agent keep going.

### With approval Augment Agent gets to work

After running several Redis commands using the Redis MCP server, Augment Agent summarized the results:

![Sample Data Generation Complete](/images/site-mirror/1b8e1a1129c5c3303f6c13138c12a11e70817cd4-1448x1136.webp)

![Summary](/images/site-mirror/bfbe0f1184bae8a6fa949a7107b6415930d2532c-1444x1178.webp)

But it’s not enough to simply trust that Augment Agent did the job. I used [Redis Insight](https://redis.io/insight/) to verify the results. I searched for “*alice*” in Redis Insight, since “alice” was one of the sample users generated by Augment Agent.

![Redis Insight Generated Data](/images/site-mirror/7b19e0050a74585f54a51158a08acdf6bf4aba87-966x1740.webp)

Using the Redis MCP server, Augment Agent was able to generate a session, chat stream, several messages, and a user_memory entry. Since you might not be familiar with the “user_memory” and “semantic_memory” features of the Redis Chat, here is an example of a “semantic_memory” generated by Augment Agent:

![Redis Insight Semantic Memory](/images/site-mirror/ad361d1f3e8ce92e53166f22bd59cfbb350b9c0d-1784x974.webp)

This is the exact data type that the Redis Chat application also stores, which makes the sample data fit nicely with the existing application. All of this is made possible because of Augment Agent and Redis MCP server, and it’s really easy to get started.

### Setting up Redis MCP server with Augment Code

The easiest way to [get setup with Redis MCP server and Augment Code](https://redis.io/docs/latest/integrate/redis-mcp/client-conf/#augment-code) is outlined in our docs.

## What’s Next

That’s all there is to it. Once you have the Redis MCP server connected to Augment Code you can prompt Augment Agent and do whatever you need to in Redis. You’ve already seen what it’s like to generate data, but here are some other use-cases:

1. Looking at existing data in Redis and using it to build out data structures and CRUD components in your code.
1. Generating example data to prove a concept in Redis, such as using sorted sets to keep track of trends at a large scale.
1. Debugging your code and Redis to understand why something isn’t working.

There’s so much more, I’ll let you play with it and figure out what works for you.

### More Resources

1. Explore [Redis Vector Sets](https://redis.io/docs/latest/develop/data-types/vector-sets/)
1. Learn how to use [Redis for AI](https://redis.io/docs/latest/develop/ai/)
1. Try before you buy with [Redis Sandbox](https://redis.io/try/sandbox/)
