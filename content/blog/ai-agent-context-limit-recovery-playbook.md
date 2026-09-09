---
title: "Your agent hit the context limit. Here's the playbook"
linkTitle: "Your agent hit the context limit. Here's the playbook"
url: "/blog/ai-agent-context-limit-recovery-playbook/"
description: "Your agent was humming along, then it stopped mid-task and declared the job done when it wasn't. One common cause is the AI context limit, a hard ceiling on how many tokens a model can hold in its..."
date: 2026-06-15
blogCategories:
- "Tech DE"
authors:
- "Jim Allen Wallace"
lastmod: 2026-06-17
hidden: true
---

*By Jim Allen Wallace, Sr. Product Marketing Manager · Published 15 June 2026 · updated 17 June 2026*

![Your agent hit the context limit: a six-step recovery playbook](/images/site-mirror/3799b0c8735fe5bc78a6aa47d4887367681c48f1-2400x1256.webp)

Your agent was humming along, then it stopped mid-task and declared the job done when it wasn't. One common cause is the AI context limit, a hard ceiling on how many tokens a model can hold in its working memory at once. The frustrating part: this often isn't a model problem you can prompt your way out of. It's an architecture problem.

The good news is that recovery follows a fairly predictable path. You start by cutting the worst offenders out of the window, then work your way toward moving durable state into external storage where it belongs. This guide walks through six steps to help bring an agent back under its context limit, in roughly the order you should try them, and where a fast external store fits into the picture.

## First, what's actually filling the window?

Before you start cutting, it helps to know what a context window holds and why it fills up. The context window is all the text a model can reference when generating a response, measured in tokens. It acts like a model's short-term memory: it can only hold so much new information at one time before earlier details start to fade. The window holds your system prompt, the conversation history, tool definitions, tool results, and any retrieved content you inject.

Bigger windows haven't made this go away. Even with a very large window, quality can degrade as you fill it. As token count grows, accuracy and recall degrade, a phenomenon known as [context rot](https://docs.anthropic.com/en/docs/build-with-claude/context-windows). Models can also favor tokens at the beginning and end of long inputs, which creates lost-in-the-middle behavior when important details sit in the center. Recovery isn't only about fitting under the limit. It's about keeping the window small and high-signal so the agent actually reasons well. With that framing, here's the playbook.

## Step 1: Trim tool outputs before they enter the window

Every time an agent calls a tool, whatever comes back gets written into the context window: search results, an API response, file contents, a log dump. That raw payload sits alongside the conversation and counts against the same token budget, and it can quietly eat more tokens than the entire exchange. In Model Context Protocol (MCP) connected agents, tool definitions and results can [consume 50,000+ tokens](https://www.anthropic.com/engineering/code-execution-with-mcp) before the agent even reads a request.

A few practical techniques help here, and you can stack them. Start with the tool surfaces most likely to balloon.

- **Hard token caps and pagination:** Set a ceiling on any tool response that could run long. For Claude Code, the default [25,000-token cap](https://www.anthropic.com/engineering/writing-tools-for-agents) works with pagination, range selection, and filtering.
- **Dynamic tool filtering:** Load only the tools relevant to the current task. Tool lists are context too, so a smaller tool surface keeps the prompt cleaner.
- **Reference, don't inline:** If an agent writes a 500-line file, the chat history should contain the file path only, not the file content.

Trimming tool noise often buys back enough room to keep going. When it doesn't, the next lever is compressing the conversation itself.

## Step 2: Summarize & compact older turns

Once tool outputs are under control, the conversation history is usually the next thing to grow unwieldy. Compaction means [summarizing older turns](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) as the conversation nears the limit, then reinitializing a new window with that summary. Some frameworks trigger this automatically; for example, Deep Agents compact at [85% of the window](https://docs.langchain.com/oss/python/deepagents/context-engineering).

There's a real benefit beyond saving space. Summaries can act as clean rooms that correct prior mistakes, which helps avoid [context poisoning](https://developers.openai.com/cookbook/examples/agents_sdk/session_memory), where a hallucinated fact gets referenced turn after turn.

But compaction is lossy, and you should know what you're trading. A summary is a smaller, rewritten version of the original turns, so it keeps the gist while dropping specifics: exact file paths, error strings, the precise wording of an earlier decision. Think of three tiers of fidelity. Raw history keeps everything but costs the most tokens. A compacted version trims redundancy while keeping most detail. A summary is the most compact and the lossiest. The further you compress, the more the agent has to work from a paraphrase of what happened rather than the record itself.

That loss has a practical cost. When the summary drops the specifics an agent needed to finish a task, the agent can lose the thread: it looks at the partial progress in front of it, assumes the rest is done, and [declares the job complete](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) before it actually is. To guard against this, some frameworks write the full conversation to a file before compacting, so the summary stays in the window for day-to-day reasoning while the complete record sits in storage the agent can pull from when it needs an exact detail. That move, keeping the working version small and the durable version external, is the real fix, and it's the next step.

## Step 3: Move durable state out of the window

If you're summarizing the same facts over and over, that's a sign they shouldn't live in the window at all. The context window is working memory, not storage. Treating it as persistent storage by appending every fact, preference, and tool result asks working memory to do the job of a [persistent database](https://redis.io/glossary/databases/).

The model itself is stateless by design: every inference call starts fresh, with no record of what came before. You can't give the model memory; you build memory infrastructure around it. The standard way to do that is to split memory in two: keep only the active working set in the context window, and put everything durable, past decisions, user preferences, prior results, in an [external store](https://arxiv.org/html/2603.07670v1) that a retrieval step reads from each turn. Any agent that has to remember across a long task or multiple sessions ends up here, whether it's a coding assistant tracking a refactor or a support bot recalling an account. This is the baseline architecture for production agents, not a workaround.

This also explains why bigger windows don't make external storage obsolete. A longer context enlarges working memory but doesn't provide persistent cross-session storage, structured knowledge organization, or selective retrieval from months of history. Agents can read their own notes after a context reset and continue multi-hour tasks, preserving coherence across summarization steps in a way that's hard to maintain by holding everything in the window alone. The external store is what makes that pattern practical.

## Step 4: Retrieve on demand instead of carrying everything

Once durable state lives outside the window, the next move is to stop dragging the full history forward every turn. The pattern is just-in-time retrieval: pull the relevant working set per step rather than loading everything upfront. In practice, the agent decides mid-task what it needs, fetches just those records from the external store, uses them, and lets them drop out of the window again on the next step, so active context stays scoped to the work in front of it rather than the entire history.

This is where [retrieval-augmented generation pipelines](https://redis.io/glossary/retrieval-augmented-generation/) (RAG) fit. RAG converts a query into vector embeddings, the numerical representations of meaning that let you search by similarity, then retrieves only semantically similar documents to bundle with the prompt. In a RAG pipeline, the app embeds the query, the vector store returns the most relevant chunks, and the app passes those as context. The store retrieves; the app orchestrates.

A few best practices keep per-step retrieval lean. The goal is to keep the model focused, not to turn an awareness playbook into a tuning guide.

- **Budget the window:** Treat context as a limited compute and cognitive budget. Keep each step focused on the information the model needs now.
- **Check relevance before injection:** Review retrieved documents for relevance before they reach the model. Weak matches add noise even when they technically fit.
- **Load large payloads incrementally:** For SQL-assistant-style workloads, don't treat [roughly 5–10% of the window](https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant) as a universal cutoff. The broader pattern is to load large content through search or pagination rather than injecting it all at once.

That on-demand pattern reduces the odds that old, irrelevant material crowds out the current task. It also sets up the next move: isolating work that still needs a lot of tokens.

## Step 5: Isolate context-heavy subtasks

Some tasks are just token-hungry no matter how well you trim. For those, delegate to scoped subagents that run in their own isolated context windows, keeping the main window clean. The orchestrator holds a high-level plan while subagents do the deep work and return a condensed summary rather than the full working context. This pattern is often called context quarantine: isolating contexts in their own dedicated threads.

This pattern can pay off when work divides cleanly, but isolation isn't free. It works best for parallelizable, read-only tasks like research, where subtasks can run independently and return concise findings. For tightly coupled tasks like coding, the coordination overhead and risk of conflicting changes can create more problems than it solves.

Worth knowing: context pressure has its own behavioral tell. Agents can show [context anxiety](https://www.anthropic.com/engineering/managed-agents), where they wrap up tasks prematurely as the limit approaches. Keeping subtask context well below the ceiling helps reduce the risk of that failure mode.

## Step 6: Right-size the storage layer so recovery isn't a cost spike

Here's the catch with steps 3 through 5: moving state external only helps if the store is low-latency and cost-efficient for your workload. If every agent step kicks off a slow round of fetches, you've traded a context problem for a latency problem. Tools, memory, retrieval, and state often don't live in one place, and [agent context](/blog/ai-agent-context/) can't land until the slowest piece arrives. Small retrieval failures compound quickly across multi-step workflows.

This is where Redis Iris fits. [Redis Iris](https://redis.io/docs/latest/develop/ai/context-engine/) is a suite of fully-managed services that give AI agents the context engine they need to reliably act on business data, bundling capabilities that enterprises have typically had to stitch together from separate tools. Instead of bolting a separate vector database onto a separate cache onto a separate memory server, you keep the context layer in one place. Redis Iris brings together four services:

- **Context Retriever:** turns business data into structured tools agents can safely reuse.
- **Agent Memory:** a persistent memory service that maintains short-term session memory and long-term memory across agent interactions.
- **LangCache:** a semantic caching service that stores and reuses LLM responses for similar queries to reduce API costs and improve latency.
- **Data Integration (RDI):** syncs live data from existing relational databases into Redis Cloud so agents always have access to fresh, accurate business data.

All of it runs on Redis Cloud via REST API, with no database setup or management required, and [hybrid retrieval](/blog/from-demo-to-dependable-ai-in-context/) sits underneath in the Redis Query Engine.

Cost is the other half of right-sizing, since keeping a large external store hot can get expensive fast. Redis Flex, the SSD-based tiered storage engine underneath Iris, can reduce memory costs by [up to 80%](/blog/introducing-another-era-of-fast/) via tiered RAM and SSD storage, depending on hot and cold data distribution. That keeps retrieval fast while making it cheaper to maintain larger context windows and longer agent memories, which matters when bloated context multiplies the bill.

## The window is working space; your storage layer helps address the root cause

The through-line across all six steps is simple. Trim what you can, compact what's left, then stop treating the context window as a place to keep things. The window is working space for the current step. Durable state, long-term memory, and anything you'll need to retrieve later belong in a fast external store the agent pulls from on demand. Recovery is mostly about drawing that line in the right place and instrumenting your context usage so you act proactively before the window fills instead of reacting at 100%.

That external layer is where Redis Iris can fit in an agent stack. It brings real-time retrieval, semantic caching, agent memory, and data integration together in one system, so agents get fast context retrieval without managing separate stores, and Redis Flex keeps the cost reasonable as you scale. If you're untangling an agent that keeps hitting its context limit, you can [try Redis Iris](https://redis.io/try-free/?rcplan=iris) to see how a unified context layer behaves with your workload, or [talk to our team](https://redis.io/meeting/) about right-sizing the storage layer for your agents.
