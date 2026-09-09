---
title: "3 Hackathon Winners Show What Generative AI Can Accomplish"
linkTitle: "3 Hackathon Winners Show What Generative AI Can Accomplish"
url: "/blog/lablab-ai-hackathon-review/"
description: "Redis has co-sponsored several AI hackathons. These three winners – from Memoiz, RedAGPT, and SmartHealth – may inspire you to add AI features to your own applications."
date: 2023-06-28
blogCategories:
- "Uncategorized"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 28 June 2023 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/977e093b32d94db37802f8221c97f8110882a183-772x550.webp)

**Redis has co-sponsored several AI hackathons. These three winners – from Memoiz, RedAGPT, and SmartHealth – may inspire you to add AI features to your own applications.**

AI has taken significant leaps forward, escaping from university laboratories and corporate research departments. In recent months, the rate of innovation has been staggering. Nvidia CEO, Jensen Huang, called it [the ”iPhone moment” of AI](https://www.youtube.com/watch?v=3O4OujSFwt8).

Whatever your opinion of its influence, there’s no denying that this pioneering technology is pushing boundaries and springing surprises. With the attention and engagement of developers worldwide, an array of new applications, solutions, and even businesses have been launched.

## Partnering to foster AI innovation

Over the past three months, [Redis and LabLab AI collaborated](https://lablab.ai/blog/redis) to fuel an ecosystem of AI-driven applications. This initiative integrated technologies from organizations including [OpenAI](https://platform.openai.com), [Cohere](https://cohere.ai/), [LangChain](https://langchain.readthedocs.io/), [LlamaIndex](https://gpt-index.readthedocs.io/en/latest/), [Vercel](https://vercel.com/), and, naturally, [Redis](https://redis.com). During the events, [LabLab’s platform](https://lablab.ai) fostered discovery, collaboration, and innovation. Redis was featured as a “[side quest](https://lablab.ai/side-quests)” technology, providing an extra challenge with additional prize opportunities for developers who integrated Redis into their hackathon applications.

Ultimately, 47 high-quality, Redis-powered submissions emerged from the [seven AI hackathons](https://lablab.ai/event). Given that Redis was not a mandatory requirement for any of these events, the sheer[ amount and caliber of the submissions](https://lablab.ai/apps/tech/redis) speaks volumes. We’ve seen and been a part of countless hackathons over the years, but the blend of groundbreaking technology and applicable business ideas from this event was truly remarkable.

Below, we examine the top three projects: Memoiz, RedAGPT, and SmartHealth. We distill the core problems the projects tackled and their creative solutions for the broader community’s benefit.

## Memoiz

In the wake of large language models (LLMs), we’ve seen a surge of applications that encourage users to chat with their notes, capitalizing on LLMs’ language comprehension and language generation capabilities. While the concept isn’t necessarily groundbreaking, its application to specialized use cases, like the one pursued by [Memoiz](https://lablab.ai/event/ai-startup-hackathon-episode-2/we-absolutely-have-no-idea/memoiz), is potentially transformative.

![Memoiz mood tracker interface](/images/site-mirror/b9ea437a941fc892ce4d0e9f4ec0812f12ddc3f5-1134x1182.webp)

*Memoiz mood tracker interface*

Memoiz is developing a platform for creating, storing, and interacting with personal diary content. It’s akin to having a personal librarian for your memories, thoughts, and moods. You write notes, recall memories, track your daily moods, and explore historical shifts over time. The novelty lies in the ability to “chat” with your personalized librarian as you access past reflections.

Our Redis team sees huge potential in an application like Memoiz to shift the way people, young and old, maintain thoughtful access to memories, plans, and personal experiences.

When the Redis judges (Brian Sam-Bodden, Paul Ford, Taimur Rashid, Sam Partee, and I) spoke with the Memoiz team, Thanasan Kumdee and Nutchanon Taechasuk, the two Japanese university students’ joy, humility, and honor were palpable. Now backed by the [NewNative](https://newnative.ai/) Slingshot AI Accelerator program, Kumdee’s and Taechasuk’s enthusiasm is obvious. The developers’ plans for the project include integrations with other note-taking applications, such as Notion or Obsidian, for broader access. They also intend to work on improving temporal understanding and querying of the underlying memories.

![Memoiz technical architecture including Redis and Cohere](/images/site-mirror/c5729d4fdd1ed044619d9c59edb9e46324b650ab-1390x736.webp)

*Memoiz technical architecture including Redis and Cohere*

Under the hood, Memoiz uses Redis Cloud for storing and searching through vector embeddings that symbolize the memories and queries. Married with a [Cohere LLM](http://cohere.ai), this enables users to delve into their past in a conversational way. The Redis-Cohere combination, an increasingly popular pattern in the generative AI boom, offers superior speed and semantic accuracy, which enhances Memoiz’s end-user experience.

The team is ready to build towards the future and has our full support to reach its goals.

## RedAGPT

The [RedAGPT](https://lablab.ai/event/autonomous-gpt-agents-hackathon/redteamagpt/redteamagpt) team’s AI-powered cybersecurity tool earned second place in the hackathon series. Designed to probe network vulnerabilities in residential and commercial environments, RedAGPT uses AutoGPT, Redis, and Langchain for efficient and effective security testing. Prioritizing rapid engineering and ease of integration, this toolkit perfectly complements security-focused Linux environments, making it an indispensable asset for security professionals.

At its core, RedAGPT conducts a series of tests to uncover network and system vulnerabilities, and it leverages Generative AI, specifically the GPT-3 LLM via the [Langchain](https://python.langchain.com/v0.1/docs/get_started/introduction/) library. The tool detects weaknesses and also quantifies their severity, along with providing actionable recommendations for remediation. The result? A comprehensive security report that transforms raw data into meaningful insights. RedAGPT stands as a testament to the revolutionary application of AI in cybersecurity.

## SmartHealth

[SmartHealth](https://lablab.ai/event/openai-hackathon/smarthealth/smart-health) is a personalized health assistant that delivers health advice tailored to unique needs. SmartHealth doesn’t just offer a symptom checker; it serves as a comprehensive health companion, sharing personalized tips that help users to take control of their health and well-being.

We were impressed with the team behind SmartHealth: a talented group of computer science, medical, arts, and business professionals.

![SmartHealth chat application UI](/images/site-mirror/d07d125864c9e4c51fe5727ec508604080ecf82e-1004x1072.webp)

*The SmartHealth chat application UI*

The tech stack includes GPT-3, Redis as a vector database, Python, and React. The team assembled a robust database of health conditions, symptoms, causes, and treatments, which, when paired with GPT-3, helps users understand their health status without needing an in-person doctor visit.

The team also went to great lengths to address security and privacy concerns — an area we initially flagged while reviewing its submission. However, we were impressed by the team’s extensive measures in this domain, reinforcing SmartHealth’s commitment to deliver a secure, effective, and personalized health platform.

We believe that products like SmartHealth are only the beginning of the ways generative AI can be applied in the medical industry, but there’s a long road ahead.

## Why Redis for generative AI projects?

The consistent thread running through these projects is their use of generative AI technologies and Redis. While Redis’ involvement may be unsurprising to some, others might find it new, even unexpected.

Redis has been stirring up the machine learning (ML) community with its commitment to real-time performance and versatile data structures. The objective is clear: to empower developers to focus on their application creation, minimizing fuss over the data layer. It also didn’t hurt that [OpenAI announced to the world that ChatGPT relies on Redis](https://openai.com/blog/march-20-chatgpt-outage) to effectively scale its end-user chatbot user experience.

With real-time interaction increasingly demanded in today’s apps, Redis emerges as a Swiss Army knife, solving an array of challenges. It can serve as a low-latency [feature store](/solutions/feature-store/) for ML model serving, a [vector database](/blog/vector-databases-101/) for LLM knowledge retrieval, or a [caching](/solutions/caching/) layer for ML model inference or LLM prompts. In the whirlwind of AI innovation, Redis’ adaptability and extensibility is crucial.

Choosing trustworthy tools from burgeoning new technologies and SaaS products can be overwhelming. Redis aims to be a reliable, multi-purpose tool in this intricate ecosystem.

Now, with a [suite of fresh projects](https://lablab.ai/apps/tech/redis) and ideas leveraging these capabilities**, **it’s your turn**. **Whether you’re an open-source developer, a startup, or an enterprise, there’s something for you in the Redis universe. Start exploring our curated list of AI [resources](https://github.com/RedisVentures/redis-ai-resources), join our [developer community on Discord](https://discord.gg/redis), or get started today in [Redis Cloud](/try-free/) for free.
