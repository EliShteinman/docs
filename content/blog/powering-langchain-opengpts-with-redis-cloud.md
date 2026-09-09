---
title: "Powering LangChain OpenGPTs With Redis Cloud"
linkTitle: "Powering LangChain OpenGPTs With Redis Cloud"
url: "/blog/powering-langchain-opengpts-with-redis-cloud/"
description: "OpenGPTs is a low-code, open-source framework for building custom AI agents. Because of Redis’ speed and reliability, LangChain chose Redis Cloud as the default vector database for this exciting..."
date: 2023-11-27
blogCategories:
- "Redis-Cloud"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 27 November 2023 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/a6c1a69440f0d8df0ce9c5f1b61d18a8b10de815-772x552.webp)

[**OpenGPTs**](/press/redis-cloud-powers-langchain-opengpts-project/)** is a low-code, open-source framework for building custom AI agents. Because of Redis’ speed and reliability, LangChain chose Redis Cloud as the default vector database for this exciting new project.**

In the constantly-evolving world of generative AI, crafting an AI-powered chatbot or agent is like assembling a complex jigsaw puzzle. That’s why [LangChain](https://github.com/langchain-ai/langchain) has evolved as one of the leading open source frameworks for streamlining application development with LLMs. OpenAI’s recent announcement of [OpenAI GPTs](https://openai.com/blog/new-models-and-developer-products-announced-at-devday) (a kind of no-code “app store” for building custom AI agents) inspired LangChain to develop a similar open-source tool called OpenGPTs.

[OpenGPTs](https://github.com/langchain-ai/opengpts/tree/main) lets you select your ideal LLM provider, system prompt, and enabled tools. Redis is the default vector database. As LangChain founder Harrison Chase [said](/press/redis-cloud-powers-langchain-opengpts-project/):

*“We’re using Redis Cloud for everything persistent in OpenGPTs including as a vector store for retrieval and as a database to store messages and agent configurations. The fact that you can do all of those in one database from Redis is really appealing.”*

​​Let’s jump right in and learn how to build an intelligent AI agent with OpenGPTs and Redis.

## Introducing OpenGPTs

With a few configuration steps, we can use [OpenGPTs](https://opengpts-example-vz4y4ooboq-uc.a.run.app/) to build a *RedisGuru* bot that acts as a “wise sage” who has mastered all there is to know about Redis.

Below you can see our choice of LLM, System Message (the primary behavior-influencing prompt), and Tools, including DuckDuckGo search, Wikipedia search, and access to public press releases thanks to [Kay.ai](https://www.kay.ai/).

![ChatGpt-01](/images/site-mirror/80e9f5c2ce2b8278ba0e774cbd971a5ebe66fb72-950x640.webp)

With RedisGuru configured and deployed, we can now test the agent:

![bot-initial-convo](/images/site-mirror/8925f5935df900300fa6c953ca26a47f7e67d31d-796x488.webp)

We can also ask questions about Redis data structures. Notice that RedisGuru remembers my name when prompted:

![bot-initial-convo](/images/site-mirror/7718121c96f12d251c4d1cb5be7711c25165fbe1-795x701.webp)

I constructed this RedisGuru agent in a matter of minutes. The possibilities are endless for what you might build next: an email copy editor, an intelligent research assistant, a code reviewer, and more.

## Redis Cloud’s role in OpenGPTs

Behind the scenes of this OpenGPTs demo, Redis Cloud provides a robust, high-performance data layer, integral to the OpenGPTs stack.

Redis Cloud persists user chat sessions (threads), agent configurations, and embedded document chunks for [vector database](/solutions/vector-database) retrieval.

- **User Chat Sessions**: To maintain “state” in the conversation, Redis Cloud provides OpenGPTs with persistent chat threads between a user and the AI agent. The chat sessions are also fed into the LLM to provide context about the current conversational state.
- **Agent Configurations**: To power a multi-tenant agent architecture, Redis Cloud provides OpenGPTs with a remote, low-latency storage layer. When the application spins up, it reads specified agent settings and configurations from Redis before serving requests.
- **Vector Database for RAG**: To ground the conversation in truth, OpenGPTs lets us upload “knowledge” sources for the LLM to mix in with its generated answers. Using a process known as Retrieval Augmented Generation (RAG), OpenGPTs stores uploaded documents in Redis and provides real-time vector search to retrieve relevant context for the LLM.

These capabilities (and more) are part of the Redis Cloud platform and made available with our [LangChain + Redis integration](https://python.langchain.com/docs/integrations/providers/redis).

Redis Cloud’s integration with LangChain’s OpenGPTs brings essential adaptability, scalability, and real-time processing and search. Its capacity to handle diverse data structures uniquely positions Redis Cloud as the go-to solution for OpenGPTs’ memory.

## Using OpenGPTs Locally

Interested in kicking the tires yourself? Running OpenGPTs locally is a straightforward process. More detailed instructions can be found in the [project’s README](https://github.com/langchain-ai/opengpts/blob/main/README.md). Here’s a quick rundown:

1. **Install Backend Requirements**: Clone the repo. Navigate to the backend directory and install the necessary Python dependencies.

cd backend
pip install -r requirements.txt

2. **Connect to Redis Cloud and OpenAI**: OpenGPTs uses Redis Cloud for LLM memory and OpenAI for LLM generation and embeddings. Set the REDIS_URL and OPENAI_API_KEY environment variables to connect to your [deployed Redis instance](/cloud-partners/google/) and your [OpenAI account](https://platform.openai.com).

export OPENAI_API_KEY=your-openai-api-key
export REDIS_URL=redis: //your-redis-url

3. **Start the Backend Server**: Run the LangChain server to serve the application on your local machine.

langchain serve –port=8100

4. **Start the Frontend**: In the frontend directory, use [yarn](https://classic.yarnpkg.com/en/docs/cli/) to start the development server.

cd frontend
yarn
yarn dev

5. Navigate to [http://localhost:5173/](http://localhost:5173/) to interact with your local OpenGPTs deployment.

## Using OpenGPTs in the Cloud

For those interested in building with OpenGPTs without a local setup, try [deploying the stack on Google Cloud](https://github.com/langchain-ai/opengpts/tree/main#deployment). Alternatively, visit the hosted [research preview deployment](https://opengpts-example-vz4y4ooboq-uc.a.run.app/), powered by LangChain, LangServe, and Redis Cloud. This deployment showcases OpenGPTs’ customizability and ease of use.

## Driving Innovation with Redis and LangChain

[Redis Cloud](/try-free) stands out as an enterprise-grade, low-latency vector database, uniquely poised to power your generative AI projects. It goes beyond mere vector search, offering versatile data structures that efficiently feed into the application state of LLMs. This robust platform ensures optimal scalability and performance, making Redis an indispensable tool in the realm of generative AI.

Dive into LangChain’s [OpenGPTs](https://github.com/langchain-ai/opengpts) today elevate your projects, blending speed, versatility, and innovation.
