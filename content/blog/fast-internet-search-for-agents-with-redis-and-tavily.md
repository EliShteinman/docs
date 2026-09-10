---
title: "Fast internet search for agents with Redis & Tavily"
linkTitle: "Fast internet search for agents with Redis & Tavily"
url: "/blog/fast-internet-search-for-agents-with-redis-and-tavily/"
description: "Every AI agent sounds smart at first. But the cracks show fast. They don’t have the most recent information, lose track of the conversation, repeat themselves, and waste time (and money) hitting..."
date: 2025-09-12
blogCategories:
- "Tech"
authors:
- "Tyler Hutcherson"
- "Noah Nefsky"
- "Sofia Guzowski"
- "Jim Allen Wallace"
- "Rini Vasan"
lastmod: 2025-10-08
hidden: true
mirrored: true
---

*By Tyler Hutcherson, Noah Nefsky, Sofia Guzowski, Jim Allen Wallace, Rini Vasan · Published 12 September 2025 · updated 8 October 2025*

![Fast internet search for agents with Redis & Tavily](/images/site-mirror/8de567524f7bd95be797d4facb377de85b8e4599-772x552.webp)

Every AI agent sounds smart at first. But the cracks show fast. They don’t have the most recent information, lose track of the conversation, repeat themselves, and waste time (and money) hitting the same APIs over and over. You need to manage the data going into the context window for your agents. Enter Tavily & Redis to help streamline your context engineering.

- Tavily provides agents real-time, high-quality data from the web.
- Redis helps your agents actually remember what they’ve learned.

Put them together and you’ve got an agent that’s fast, sharp, and always on top of the latest.

## Tavily gives you the web

Tavily allows your agent to effectively access info from the internet by retrieving live, relevant, and high-quality data directly from online sources. It’s important to find the data, clean it, and process it intelligently so that agents and LLMs can use it effectively. Tavily automates this search and cleaning process. As your agents make more Tavily queries over time, the volume of data can grow quickly. By storing and reusing past data, you enable real-time reasoning and can continually enrich your knowledge with fresh Tavily calls, ensuring both historical context and up-to-date insights are always available.

To make the most of this data, it’s important to store it somewhere that allows for fast, low-latency search across relevant chunks.

## Redis lets your agents remember

Think of Redis as your agent’s RAM upgrade. It’s not just storage—it’s memory that works in real time. With sub-millisecond reads and writes, Redis can hold on to conversation history, state, and embeddings without slowing your agent down.

Beyond just storing data, [Redis Agent Memory Server](https://github.com/redis/agent-memory-server/) lets you intelligently add which pieces of info you’ll need later and summarize it in an efficient way. You can also store memories async after some reflection. Redis supports persistent memory across sessions, filtering, Automatic Entity Recognition, and memory deduplication and compaction. Redis also integrates with other AI tools and memory management systems like LangChain, Mem0, Cognee, and more.

With Redis Query Engine and vector search, Redis can retrieve just the information you need at the right time. Redis makes sure your agent remembers what matters, fast enough to feel real-time.

## Tavily + Redis = context superpowers

Tavily delivers fresh, high-quality insights from the web in real time, while Redis makes sure your agent doesn’t forget them. Tavily ensures your AI always has the most credible and up-to-date information, and Redis turns that information into durable, lightning-fast memory. With sub-millisecond reads and writes, LangGraph checkpointing on Redis captures and persists short-term conversation context as it happens.

For long-term recall, Redis vector database stores embeddings of past Tavily calls, conversations, and other documents, making retrieval instant whenever your agent needs it. Tavily keeps the knowledge stream flowing, Redis makes it stick. Together, they give your AI the kind of always-on context and speed that makes it feel less like a tool and more like a brain that never slows down.

Gathering the data and storing the data are both essential parts of making agents works, and Tavily and Redis have you covered.

## Let’s see it in action

We’ll walk through an example of how you can use Tavily and Redis together. You can [run the example yourself here](https://github.com/redis-developer/amr-autogen-travel-agent). Our example is a smart AI travel planning assistant showcasing AutoGen's advanced memory capabilities with dual-layer memory architecture: Redis-backed chat history and Mem0 based long term memory that remembers user preferences. Here are the components we’ll use:

- 🎯 **Dual-Layer Memory: **Short-term chat history (Redis) + Long-term learning (Mem0+Redis)
- 👥 **User Isolation: **Pre-seeded users get completely separate memory contexts
- 🔄 **Session Persistence: **Your conversations and preferences survive app restarts
- 📚 **Intelligent Learning: **The agent learns your travel preferences automatically
- 🌐 **Real-time Search: **Live travel information via Tavily search API
- 💬 **Clean Chat UI: **Gradio interface with user management
- 📅 **Calendar Export (ICS): **Generate a calendar file for your itinerary and open it directly in your default calendar app

## 🚀 Quick Setup (<5 minutes)

### Step 1: Get Your API Keys

You'll need three API keys:

- OpenAI API Key: Get from [platform.openai.com](https://platform.openai.com/api-keys)
- Tavily API Key: Get from [tavily.com](https://tavily.com/) (free tier available)
- Redis URL: See step two

### Step 2: Set Up Redis

You have 3 options for Redis:

#### Option A: Local Redis with Docker**

```
docker run --name redis -p 6379:6379 -d redis:8.0.3
```

#### Option B: Redis Cloud

Get a free db [here](https://redis.io/cloud).

#### Option C: Azure Managed Redis

Here's a quickstart guide to create Azure Managed Redis for as low as $12 monthly: [https://learn.microsoft.com/en-us/azure/redis/quickstart-create-managed-redis](https://learn.microsoft.com/en-us/azure/redis/quickstart-create-managed-redis)

### Step 3: Setup the Project

```python
# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
# Clone and install
git clone <repository-url>
cd amr-autogen-travel-agent
# Get uv env setup
uv sync

```

### Step 4: Configure Your Environment

Create a .env file with your API keys:

```
cp env.example .env
```

Edit the .env file as needed.

### Step 5: Launch the Application

```
uv run python gradio_app.py
```

🎉 Open [http://localhost:7860](http://localhost:7860/) to start chatting!

The application will:

- ✅ Validate your configuration and API connections
- ✅ Initialize the dual-layer memory system
- ✅ Load the user management interface
- ✅ Enable calendar export/open from finalized itineraries

![AI Travel Concierge](/images/site-mirror/725e708133ea69dfce8c8b0eaee79e7fffc5ddc4-844x649.webp)

## 👤 User Profile Configuration

The demo comes with pre-configured user profiles (Tyler, Purna, and Jan) that have distinct travel preferences. You can easily customize these or add new profiles by editing context/seed.json.
