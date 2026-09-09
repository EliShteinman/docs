---
title: "Context windows in AI: why every token is a budget decision"
linkTitle: "Context windows in AI: why every token is a budget decision"
url: "/blog/context-window-ai/"
description: "Some of today's most capable LLMs now support very large context windows. That doesn't mean you should fill them. Context windows have grown fast, but the underlying cost and quality tradeoffs..."
date: 2026-06-10
blogCategories:
- "Tech DE"
authors:
- "Jim Allen Wallace"
lastmod: 2026-06-10
hidden: true
---

*By Jim Allen Wallace, Sr. Product Marketing Manager · Published 10 June 2026*

![Context window in AI: why every token is a budget decision](/images/site-mirror/4ba6c8382f068d07fe669c56c1b3e223a170c31b-2400x1256.webp)

Some of today's most capable LLMs now support very large context windows. That doesn't mean you should fill them. Context windows have grown fast, but the underlying cost and quality tradeoffs haven't gone away. They've just gotten easier to ignore.

Every token you put into a context window can add cost, and longer contexts can also hurt reasoning quality. Treating the window as a hard limit to fill misses the point. It's a budget, and what you leave out matters as much as what you put in.

This guide covers what context windows actually are, why filling them can degrade both cost and model performance, and how to keep your context lean without losing the information that matters.

## What is an AI context window?

A context window is the total number of tokens an LLM can process in a single inference pass. It covers both what you send and what the model generates back. On the input side, that means the system prompt, conversation history, any retrieved documents, and your tool definitions and their outputs; on the output side, the model's own response. Every window has a fixed size limit, and anything that doesn't fit is invisible to the model. It can't reach back for a document you left out, so what you omit shapes the answer as much as what you include.

One common misconception is that the context window and the max output limit are the same thing. They aren't. The total window covers both input and output, while output limits can still cap how much the model returns.

Here's a rough sense of scale for English text:

- **1,000 tokens:** about 750 words, or 3 pages
- **128,000 tokens:** roughly 96,000 words, or 384 pages
- **1,000,000 tokens:** around 750,000 words, or roughly 3,000 pages

Numbers like 384 pages or 3,000 pages sound like more room than any single prompt could ever need, which is why large windows feel so spacious in practice. But that intuition hides the tradeoff: every extra page still competes for cost and attention inside the same finite budget, and models don't always use the extra space as well as the headline number suggests.

That size limit exists because of self-attention: in a standard transformer, every token has to relate to every other token in the window, so the work grows fast as the window fills. A bigger window costs you twice. It costs more to run, and it can cost you reasoning quality.

## The two costs of every token: dollars & degraded reasoning

Start with the part you can see on your bill. You pay by the token, so a longer prompt costs more, every time you send it. The exact rates differ between providers, but the direction never changes: more tokens in, more money out.

Bigger context windows also don't guarantee better reasoning. Several long-context studies report accuracy slipping as context length grows, though the size of the drop depends on the model, the task, the retrieval setup, and where the relevant information sits in the prompt.

Three patterns show up across that research. The first is raw volume. In one study, Llama 3's HumanEval coding accuracy [dropped by about half](https://aclanthology.org/2025.findings-emnlp.1264.pdf) at 30,000 tokens compared to its baseline, with similar declines on GSM8K math reasoning and variable summation. The telling detail: it wasn't where the relevant content sat in the prompt that hurt performance, it was the sheer amount of input.

The second is position. Many transformer models studied so far show a [U-shaped attention pattern](https://arxiv.org/abs/2307.03172), attending more to content at the beginning and end of the context while underweighting the middle, the "lost in the middle" problem. If your retrieval-augmented generation (RAG) pipeline drops its most relevant chunks into the middle of a long context block, the model may be less likely to use them.

The third is diminishing returns. A study of 13 long-context models found that, in that benchmark, [most peaked](https://arxiv.org/html/2404.02060v2) around 20,000 tokens for in-context learning and got no better past that point. The advertised limit and the useful limit aren't the same number.

The takeaway is straightforward: longer contexts can mean higher token spend while also risking worse results, and both costs compound with unnecessary tokens.

## Where the budget goes: system prompt, history, retrieved data & tool output

If longer context costs more and reasons worse, it helps to know where that budget goes. The context window is [a rival resource](https://arxiv.org/html/2605.09104v1): every token you give to one component displaces a token from another. The budget usually includes at least six, though some providers add hidden system or routing tokens on top.

- **System prompt:** The standing instructions that define how the model behaves. It's part of the input, billed per token and often resent on every API call.
- **Tool schemas:** The definitions that tell the model which tools it can call and how. They scale with the number of tools you expose.
- **Conversation history:** The running transcript of the exchange so far. It grows every turn unless you trim or summarize it, a common cause of context overflow in long sessions.
- **RAG retrieved chunks:** The passages your retrieval step pulls in to ground the answer. Chunk size is a key lever, and sloppy formatting can eat a large share of tokens.
- **Tool call outputs:** Whatever a tool returns when the model calls it. These range from a few tokens to very large, and big responses can crowd out the rest of the prompt.
- **Output buffer:** The space reserved for the model's own response. Set it aside explicitly rather than treating it as whatever's left over.

Those are where most context pressure comes from. Seeing the budget line by line makes it much easier to decide what belongs in the window and what doesn't.

## Spend less by keeping context out of the window until you need it

With the budget mapped, the goal shifts to keeping as much of that material out of the window as possible until it's actually needed. Context engineering treats the context window as something you actively curate rather than passively fill, holding information outside the window until the moment it's relevant.

Several strategies are well-documented, but the common idea is simple: pull in only what the model needs for the current step.

### Sliding window

Keep only the most recent conversation turns and discard everything older. It's the simplest approach and a good starting point. The tradeoff is permanent information loss, but for short-task agents and customer service bots where recent context matters most, that's often acceptable.

### Lazy context loading

Load tool definitions and reference material only when a specific reasoning step requires them. [Dynamic tool gating](https://arxiv.org/html/2604.21816v1) reduces tool overhead by loading only the tools relevant to the current step, rather than listing every available tool on every call.

### Retrieval-on-demand

Keep your knowledge in an external store and retrieve only the top semantically relevant chunks at query time. The context window never sees the full corpus. Passing only related documents cuts the amount of irrelevant content in the prompt.

### External memory stores

For agents that need continuity across sessions, move long-term memory entirely outside the context window into a persistent store. Once a conversation ends, the context is gone. External memory systems retrieve only the relevant slice for each turn, preserving continuity across conversations without carrying the full history in context.

Most of these strategies need one thing: storage fast enough to fetch the right context mid-request without stalling the model. [Redis Iris](https://redis.io/iris/) is designed for exactly that. Iris is a real-time context engine, and its parts line up with the strategies above. [Context Retriever](https://redis.io/context-retriever/) (public preview) pulls the operational data an agent needs at query time. [Agent Memory](https://redis.io/agent-memory/) (public preview) keeps long-term recall outside the window and returns only the slice that matters each turn. [LangCache](https://redis.io/langcache/) catches repeated questions so they don't hit the model twice. All of it runs with sub-millisecond response times, fast enough that retrieval never becomes the bottleneck.

The common thread across these strategies is simple: context management is about selection, not stuffing everything into the prompt. You decide what earns a spot in the window for each call, and Iris keeps everything else close by.

## How semantic caching cuts repeat spend on the same intent

Curating context reduces input spend, but it doesn't address the other half of the bill: repeated calls for the same intent. Even with a tightly managed context strategy, your app can still make many LLM calls that are semantically identical to previous ones. Semantic caching catches those duplicates and returns the stored response instead of making another model call.

### How semantic caching differs from exact-match caching

Semantic caching stores LLM responses indexed by vector embeddings of the input prompt and returns a cached response when a new prompt clears a configured similarity threshold. Unlike [exact-match caching](https://redis.io/glossary/cache-invalidation/), which only catches identical strings, semantic caching works at the intent level. "What's the weather today?" and "Tell me today's temperature" can hit the same cache entry.

### Tuning the similarity threshold

The similarity threshold is the dial that decides what counts as "the same question." Set it too loose and unrelated prompts collide, so the cache hands back a wrong answer. Set it too tight and real matches slip through, so you pay for calls you could have cached. Most teams tune it against their own traffic, watching for false hits on one side and missed matches on the other, and settle on the point that catches the most repeats without serving bad answers.

### Where Redis LangCache fits

Redis LangCache is the [semantic caching service](https://redis.io/docs/latest/develop/ai/context-engine/langcache) in Iris, built on Redis' vector search to store and retrieve LLM responses at the speed Redis is known for. In Redis-reported results for high-repetition workloads, LangCache showed [73% lower inference costs](/blog/llm-token-optimization-speed-up-apps/) and, in separate Redis benchmarks, [up to 15x faster responses](/blog/context-window-management-llm-apps-developer-guide/) for cache hits.

### A caveat for multi-turn conversations

One caveat is worth keeping in mind: standard semantic caching works best for single-turn queries. Multi-turn conversations introduce more complexity because follow-up questions can be falsely matched to earlier, unrelated prompts. Production systems handling multi-turn interactions need to account for conversational context in their caching logic.

## The cheapest token is the one you never send

Filling a giant context window just because you can is like maxing out a credit card because the limit is high. Reasoning quality can degrade well before a model's nominal context limit, so reliable AI systems treat context as a finite resource: select what goes in, keep everything else in fast external storage, and avoid paying twice for repeated intent.

That's the pattern Redis Iris is built for. Context Retriever, Agent Memory, and LangCache all run on one real-time context engine with sub-millisecond response times, so the storage layer never becomes the reason your app feels slow. Iris retrieves only the relevant context for each call, LangCache returns a stored answer on a cache hit instead of calling the model again, and long-term memory stays outside the window until you need it.

[Try Redis free](https://redis.io/try-free/?rcplan=iris) to test semantic caching and context retrieval against your own workloads, or [talk to the team](https://redis.io/meeting/) about building context infrastructure that scales with your AI apps.
