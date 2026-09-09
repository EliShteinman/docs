---
title: "Semantic caching & routing: two powerful patterns for vector classification"
linkTitle: "Semantic caching & routing: two powerful patterns for vector classification"
url: "/blog/semantic-caching-and-routing-two-powerful-patterns-for-vector-classification/"
description: "Redis’ vector datatype allows you to perform unsupervised classification in milliseconds. This core technology powers both semantic caching and semantic routing — two powerful optimization..."
date: 2026-03-13
blogCategories:
- "Tech"
authors:
- "Robert Shelton"
lastmod: 2026-03-13
hidden: true
---

*By Robert Shelton, AI Engineer at Redis · Published 13 March 2026*

![Semantic Caching and Routing](/images/site-mirror/9600db19abed34bce1585a956a614a9354070953-1200x628.webp)

Redis’ vector datatype allows you to perform unsupervised classification in milliseconds. This core technology powers both semantic caching and semantic routing — two powerful optimization techniques. Semantic caching answers the question “Have I seen something similar before?”, while semantic routing answers “Which path should this take?”. Together, they provide a highly cost-effective way to optimize systems for different use cases.

## The caching pattern

**Caching is an architectural pattern**: meaning Redis is not a cache but is a technology that can be used to implement caching.

The idea of a “cache” is to save the result of a process such that the next time you request the output of that process you can pull it from the cache quickly instead of re-running the whole process.

In a traditional cache, you classify a **cache hit** as a binary operator on a key. Key process_output_key_123 is either in the cache or it’s not. If it is grab if it’s not go calculate.

In a [semantic cache](/blog/what-is-semantic-caching/), we use vector math to classify a cache hit. If the input vector is below a configurable distance_threshold from the cached_input_vector then it is a hit and you should return the previously calculated response.

In [RedisVL](https://github.com/redis/redis-vl-python) this looks like:

```python
from redisvl.extensions.cache.llm import SemanticCache

sem_cache = SemanticCache(
    name="sem_cache",                    # underlying search index name
    redis_url="redis://localhost:6379",  # redis connection url string
    distance_threshold=0.5               # semantic cache distance threshold
)

link_key = sem_cache.store(prompt="how do I reset my password", response="See password reset <link>")

sem_cache.check("password reset?")

# returns
[
 {
  'entry_id': '21df46c0a6b534fdad84baece9623613bc7db1c9b2866db339df21f9129569e3',
  'prompt': 'how do I reset my password',
  'response': 'See password reset <link>',
  'vector_distance': 0.107770562172,
  'inserted_at': 1772737781.72,
  'updated_at': 1772737781.72,
  'key': 'sem_cache:21df46c0a6b534fdad84baece9623613bc7db1c9b2866db339df21f9129569e3'
 }
]

```

### Semantic caching architecture

The code above could be used in a system as shown below to avoid the latency and cost of invoking a more expensive LLM for duplicate similar questions.

![Semantic caching architecture](/images/site-mirror/ad2e9a04f92158f9f2ab372b363832f6c47de73e-1382x1056.webp)

Keep in mind that a “semantic cache” can be implemented at any phase in a process; it doesn't mean it can only be implemented in front of an LLM call. It could also be implemented in front of agent requests, tool calls, or within an agent workflow itself.

See also: [LangCache](https://redis.io/langcache/) for fully managed semantic caching service from Redis.

## The routing pattern

Often when writing intelligent applications you are not just trying to classify whether something is simply a **hit** or a **miss** but rather want to classify something as one of many potential labels. For example, let’s say you have a chat bot that gets asked many easy FAQ type questions that do not require spending money on the most advanced model to answer. Let’s also say that you have a known list of topics areas like politics that your bot is not designed to comment on that you want to stop execution for. In this case, it would be great if you had a tool that could quickly route FAQ type questions to the FAQ flow and blocked questions to the blocked flow. This is what a router does: A semantic router extends the idea of a semantic cache and helps you perform **generic classification** between an input and one of many potential labels in milliseconds.

If we were to implement our hypothetical example in RedisVL it would look like this:

```python
from redisvl.extensions.router import Route
from redisvl.extensions.router import SemanticRouter

# Define routes
faq = Route(
    name="faq",
    references=[
        "How do I reset my password?",
        "Where can I view my order history?",
        "How do I update my shipping address?"
    ],
    metadata={"category": "account_management", "priority": 1},
    distance_threshold=0.5
)

general = Route(
    name="general",
    references=[
        "I received the wrong item in my order, can you help?",
        "Can you recommend products that match my specific needs?",
        "The assembly instructions for my furniture are unclear",
        "I need help finding a product with particular specifications",
    ],
    metadata={"category": "customer_service", "priority": 2},
    distance_threshold=0.5
)

blocked = Route(
    name="blocked",
    references=[
        "What is your company's stance on the recent election?",
        "Do you support liberal or conservative policies?",
        "Can you tell me another customer's address?",
    ],
    metadata={"category": "prohibited", "priority": 3},
    distance_threshold=0.5
)

# Initialize the SemanticRouter
ecom_router = SemanticRouter(
    name="ecom-router",
    routes=[faq, general, blocked],
    redis_url="redis://localhost:6379",
    overwrite=True # Blow away any other routing index with this name
)

# invoke the router
route_match = ecom_router("Whatup how do i reset my password?")

# output
# RouteMatch(name='faq', distance=0.10850161314)

```

### Architectural example

In diagram form this code would power a system like this wherein at a very low latency and very low cost your system would be able to more appropriately respond to a variety of inputs.

![Architectural example](/images/site-mirror/421751a2a95b7040310f5eee38be970b5b792ce1-1600x820.webp)

More specifically, using a semantic router avoids the pitfall I see many developers fall into creating where they invoke an LLM to answer a prompt over and over again like:

“You are a labeling helper deciding to label something as Label A, B, or C return the correct label given the process”

This is a reasonable thing to ask an LLM and it would probably be pretty good at doing classification, however this is a very expensive way of solving this task in terms of latency and cost.

## In review

- Caching and routing are different architectural patterns that are both enabled through **vector based classification**.
- Vector based classification with Redis runs in milliseconds and does not take significant memory load.
- Each pattern can be implemented very easily using the corresponding classes from RedisVL.
- A semantic router can add a more deterministic and cheaper way of performing labeling tasks than an LLM.
- For more on how to optimize a [semantic cache](https://github.com/redis-developer/redis-ai-resources/blob/main/python-recipes/semantic-cache/02_semantic_cache_optimization.ipynb) or a [semantic router](https://github.com/redis-developer/redis-ai-resources/tree/main/python-recipes/semantic-router) check out the respective links.

As a final note, both the caching and routing patterns can be implemented **at any point** in an application where performance would be improved with quick classification. The examples shown above primarily consider these patterns as implemented in front of an LLM based system but they work for any vectors (images, audio, etc.) in any situation where you might be trying to reduce duplicate work or label.
