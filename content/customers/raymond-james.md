---
title: "Redis enables fast, scalable hybrid search for RAG pipelines at top financial services firm"
linkTitle: "Redis enables fast, scalable hybrid search for RAG pipelines at top financial services firm"
url: "/customers/raymond-james/"
description: "Watch the video"
lastmod: 2026-03-30
hidden: true
---

*updated 30 March 2026*

###### Watch the case study video

[Watch the video](https://redis-1.wistia.com/medias/3vvq5ovxwt)

###### Challenge

### From keyword search to trusted AI answers

Raymond James employees need fast and intuitive ways to access trusted internal knowledge.

To meet this need, Raymond James built a GenAI–powered search and chat platform designed to give advisors and employees direct, contextual answers grounded in enterprise-approved documents.

Raymond James initially relied on a traditional keyword-based search experience based on Apache Solr. With the rise of GenAI and retrieval-augmented generation (RAG), the data science team saw an opportunity to deliver **direct answers with clear source attribution**—while maintaining the governance and risk controls required in financial services.

In their V1, the initial RAG architecture focused on vector similarity search over chunked internal documents. While promising, it surfaced two key limitations:

1. **Older or less reliable documents** sometimes ranked too highly
1. **Keyword search still mattered**, especially for domain-specific terms with precise meanings

These insights made it clear that Raymond James needed **hybrid search**, not solely vector search, while remaining fast.

> We wanted a solution that could do both keyword search and vector search, without compromising on performance, especially latency.

At the same time, Raymond James’ data science team had to meet strict organizational and legal requirements to build and scale a compliant architecture.

###### SOLUTION

### Redis-powered hybrid search for RAG

In V2, Raymond James rebuilt the platform using Redis as the core retrieval engine. Redis now serves as the **central component of the V2 architecture**, enabling:

- **Hybrid search** combining keyword and vector similarity
- **Multi-vector search** across multiple embedding fields in parallel
- **Phrase boosting** based on user click behavior and engagement signals
- **Custom ranking logic**, including:
  - Fine-tuned embeddings on Raymond James data
  - LLM-generated query expansions
  - A document reliability score that penalizes outdated or low-value content

Raymond James uses Redis alongside Microsoft Azure and OpenAI models to provide an end-to-end RAG solution for their users. Working closely with their partners, they were able to fulfil their data privacy and production standards.

###### Why Redis

### Speed and scalability were critical

The speed of Redis allowed Raymond James to add more improvements inside of their latency window, while still providing instant responses to users.

> Redis allows us to do more within the same time budget. Because it’s fast, we can add more intelligence to the pipeline without slowing down the user experience.

Redis is “**extremely fast**”, which means they can handle more advanced workflows—like multi-vector searches and reranking—without slowing down the user experience. Redis also **scaled smoothly** for them, so as adoption grows across the firm, they know the system can keep up without sacrificing response times.

Beyond performance, two platform capabilities stood out to them: **the developer experience**, and Redis’ **flexibility**. First, the developer experience. Redis has invested in tools like RedisVL and integrations with LangChain, which accelerated their development process and allowed them to experiment quickly. Second, Redis’ flexibility—being able to combine hybrid search, metadata enrichment, and their own custom ranking logic all within one unified system—was a big advantage for their team.

###### Impact

### Happy users makes it all worth it

They validated the improvements of V2 in a couple of ways. First, they ran A/B testing and monitored several user experience metrics. These focused on how easy it was for users to find the right information.

One of the most important metrics they track is question coverage—essentially, the percentage of user questions that their chatbot is able to answer. Another key signal is user feedback, especially the percentage of answers that receive a thumbs up.

On the search side, they look closely at click behavior. Specifically, they track where in the ranked list users are clicking—in other words, how often they’re finding the right answer at the top versus having to dig deeper.

In V2 with Redis, user feedback had become noticeably more positive, including free-text comments highlighting satisfaction.

In fact, Raymond James had to switch back to V1 temporarily for operational reasons, and immediately Vicky’s team got feedback from users asking what happened and noticing that the search tool wasn’t working as well as before. Fortunately, they were quickly able to restore V2 and delight their users again.

###### What’s next

### Continue to evolve the platform with Redis at the center

The current system is a big step forward from where they started, but it’s not perfect. The team is constantly learning from metrics and, most importantly, from user feedback, and that continues to guide their roadmap.

They started working with RAG very early, back when GPT-3.5 was the new model, and today they’re on GPT-4o. One thing they’re excited about is experimenting with the GPT-5 model series, which has a much larger context window—up to 400k tokens. That opens the door to include more context in each query, potentially even the full content of the top few documents, which could make answers more complete and reliable.

They’re also looking at agent-based orchestration as another exciting direction. Redis integrates with LangChain and LangGraph and that will help them experiment and build quickly. Redis’ memory capabilities and integration with LangGraph enable smarter agents that can retain context, and its speed and flexibility will support more advanced workflows like multi-query routing, reranking, and query rewriting.

As they move toward agentic RAG, Redis will continue to be a key partner for them. We’re excited to see what they’ll build next.
