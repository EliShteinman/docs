---
title: "Faster, deterministic answers for healthcare voice assistant with LangCache"
linkTitle: "Faster, deterministic answers for healthcare voice assistant with LangCache"
url: "/customers/mangoes-ai/"
description: "Mangoes.ai offers a voice-first assistant that helps caregivers analyze and address symptoms for their patients. Mangoes functions like a stethoscope for behavioral health, detecting symptoms..."
lastmod: 2026-01-03
hidden: true
---

*updated 3 January 2026*

###### Challenge

### Give caregivers trusted answers at low cost

Mangoes.ai offers a voice-first assistant that helps caregivers analyze and address symptoms for their patients. Mangoes functions like a stethoscope for behavioral health, detecting symptoms through voice AI before patients can articulate them—whether in-person or via Zoom/telehealth.

To deliver answers caregivers could trust, Mangoes.ai had three problems to solve:

- **Quality answers are a must:** In healthcare, answers can’t change from one interaction to the next. Clinicians need to trust that the system will respond consistently to the same question. And tool admins need to be able to review questions and answers to ensure reliability over time.
- **Caregivers require quick responses:** Because Mangoes.ai is voice-first, any delay is immediately obvious and erodes trust. Long pauses or “thinking” time can disrupt the flow of a sensitive conversation.
- **LLM costs pile up quickly:** While scaling in production, Mangoes.ai found that they wanted to invoke LLMs more often and with more context. This heavy demand led to unpredictable and fast-rising costs, which Mangoes.ai needed better control over.

Mangoes.ai needed a way to make LLM responses high-quality, fast, and affordable without building something new from scratch that would become obsolete next month.

###### SOLUTION

### Managed semantic caching with LangCache

To address these constraints, Mangoes.ai adopted Redis LangCache, a fully managed semantic cache designed for LLM and agentic applications.

Instead of sending every conversational query directly to an LLM, Mangoes.ai routes requests through LangCache:

1. **Cache first:** When a caregiver or patient speaks, the system converts the utterance to text and sends it to LangCache.
1. **Semantic lookup:** LangCache stores query–response pairs, and uses embeddings to detect *semantically similar* questions (not just exact string matches). 
  1. For example, “Does this clinic offer CBT?” and “Can I get cognitive behavioral therapy here?” can both map to the same trusted answer.
1. **Instant answer on hit:** If a similar question has been answered before, LangCache returns the cached response in milliseconds—no LLM call required.
1. **Fallback on miss:** If there’s no suitable match, the query goes to the LLM. The new answer can then be added to the cache for future use.

![Redis Mangoes.ai Case Study Diagram](/images/site-mirror/12f8cf53a786c8d60bb5bda9ee9b61e44f476953-842x585.svg)

Because Mangoes.ai’s domain includes a lot of repeated intents (e.g., services offered, clinic options, symptom explanations, care guidance), the hit rate is high—turning repeated LLM calls into fast cache lookups.

At the same time, Mangoes.ai uses guardrails and filtering to ensure that **patient-specific or PII-heavy content is not cached**, keeping the cache focused on reusable, generalizable knowledge (e.g., what services a clinic offers, how to handle a category of symptoms). With Redis concurrency and reliability, Mangoes's infrastructure autoscales seamlessly as client usage grows.

> Our voice app for patient care gets a lot of specific treatment questions, so it has to be absolutely accurate, and that's what LangCache does. I was worried about LLM costs for high usage, but with LangCache, we're getting a 70% cache hit rate, which saves 70% of our LLM spend. On top of that, it’s 4X faster, which makes a huge difference for real-time patient interactions.

### Why Redis LangCache?

Mangoes.ai considered building its own caching layer but quickly concluded that managed LangCache would get them to value much faster:

- **Time-to-value measured in hours, not months.** The core caching component—central to the entire app—was wired up in about an hour using Redis Cloud and LangCache APIs, instead of weeks spent designing, deploying, and tuning a homegrown cache.
- **Higher quality answers.** It became clear that Redis had several advantages in storing and retrieving cached answers compared to what Mangoes.ai had built themselves. LangCache offered a fine-tuned embedding model for only semantic caching and had tagging and hybrid search so that Mangoes.ai could filter out answers they didn’t want.
- **Predictable costs.** With LangCache’s built-in monitoring and clear pricing, it was much easier to see how much we were spending (and saving) on caching our LLM calls. It was a pretty clear win.

> We could have spent months building our own caching infrastructure. Instead, we had the central caching component of the app running in about an hour. LangCache let us focus on increasing the experience of our app, which is more central to what we do.

### LangCache resulted in high hit rates and a faster app

By adopting Redis LangCache, Mangoes.ai transformed both the **technical performance** and **clinical usability** of its voice-based behavioral health assistant:

- **70% hit rate.** Even with very nuanced healthcare terminology, most questions were repeats and could be answered quickly from cache.
- **4× faster answers.** By pulling most answers from cache, the overall user experience was improved with noticeably faster responses to caregivers.
- **Up and running in under an hour.** The managed service was easy to set up, populate with past questions, and connect to their existing application.

### Next up: Broader domain knowledge and more proactive guidance

With Redis LangCache in place, Mangoes.ai is now focused on expanding what its behavioral health assistant can do:

- **Deeper domain tuning.** The team can spend more time refining domain prompts, retrieval strategies, and escalation paths for different levels of risk—rather than worrying about infrastructure.
- **Smarter conversational flows.** Deterministic, low-latency responses enable more advanced conversational patterns, including proactive guidance, symptom tracking over time, and better post-visit summaries for providers.
- **Scalable, sustainable economics.** As adoption grows across clinics and populations, caching ensures that better outcomes don’t have to mean runaway LLM bills.

By combining voice AI, clinical expertise, and Redis LangCache, Mangoes.ai is redefining how behavioral health support can be delivered—faster, more predictably, and at scale.
