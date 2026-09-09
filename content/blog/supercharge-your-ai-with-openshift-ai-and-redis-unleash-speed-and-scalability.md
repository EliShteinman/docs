---
title: "Supercharge Your AI with OpenShift AI and Redis: Unleash speed and scalability"
linkTitle: "Supercharge Your AI with OpenShift AI and Redis: Unleash speed and scalability"
url: "/blog/supercharge-your-ai-with-openshift-ai-and-redis-unleash-speed-and-scalability/"
description: "Since the birth of large language models (LLMs) and the release of ChatGPT, artificial intelligence (AI) has gone from being an out-of-reach concept to showing real promise in the business..."
date: 2025-05-02
blogCategories:
- "Tech"
authors:
- "Denis Abrantes"
- "Nick Schuetz"
lastmod: 2025-10-01
hidden: true
---

*By Denis Abrantes, Nick Schuetz · Published 2 May 2025 · updated 1 October 2025*

![Blog tile image](/images/blog/dce12404a5c7748ee68c6b81ad527ef3beff352a-772x552.webp)

Since the birth of [large language models](https://www.redhat.com/en/topics/ai/what-are-large-language-models) (LLMs) and the release of ChatGPT, [artificial intelligence](https://www.redhat.com/en/artificial-intelligence) (AI) has gone from being an out-of-reach concept to showing real promise in the business landscape for every industry and business. From personalized customer experiences to streamlined operations and increased security, the possibilities are endless.

The reality we encounter in many companies, however, shows a lack of robust and flexible infrastructure technologies that will allow the business to harness the full potential of these AI promises. Leaders see the potential of AI and want to adopt it, but the teams do not have access to the basic tooling that will allow them to explore it.

This is where [Red Hat OpenShift AI](https://www.redhat.com/en/technologies/cloud-computing/openshift/openshift-ai) and [Redis](https://redis.io/redis-for-ai/) come into play, offering a powerful environment for data scientists and machine learning (ML) engineers.

OpenShift AI provides organizations with an efficient way to deploy and manage a comprehensive set of AI/ML tools. Its ability to create custom environments ensures that data scientists and machine learning engineers always have the right resources at their fingertips.

Redis is the world’s fastest in-memory database. It’s a versatile solution that has evolved beyond a simple key-value data store to support a wide range of use cases, including:

- [Vector database](https://redis.io/solutions/vector-database/): Store and query vector data for similarity searches
- [Retrieval augmented generation (RAG)](/blog/using-redis-for-real-time-rag-goes-beyond-a-vector-database/): Enhance LLM accuracy and relevance by grounding searches in real-time data
- [LLM memory](/blog/langgraph-redis-build-smarter-ai-agents-with-memory-persistence/): Manage the context window of LLMs for more coherent and context-aware conversations
- [Semantic cache](/blog/what-is-semantic-caching/): Optimize performance and reduce LLM costs by caching semantically similar prompts and responses

## Better together: OpenShift AI and Redis

AI applications, especially those involving [generative AI (gen AI)](https://www.redhat.com/en/topics/ai/what-is-generative-ai), demand high performance and low latency. Users expect real-time responses and personalized experiences. The combination of OpenShift AI and Redis addresses these challenges head-on.

![Supercharge Your AI](/images/blog/a14553eaf6efcb3b5402264d642821ed6f7980a6-1122x641.webp)

OpenShift AI provides the environment where data scientists can use different tools, including embedding models, third-party frameworks like [LangChain](https://github.com/langchain-ai/langchain) or [LlamaIndex](https://github.com/run-llama/llama_index) and multiple LLMs to implement their gen AI use cases at scale. Redis delivers the sub-second latency that gen AI use cases need.

### Let’s dive into specific use cases:

**1. Retrieval augmented generation (RAG)**

[RAG](https://www.redhat.com/en/topics/ai/what-is-retrieval-augmented-generation) enhances the knowledge of LLMs by integrating external data sources. Instead of solely relying on their pretrained knowledge, LLMs can fetch relevant information from a database in real time to generate more accurate and contextually appropriate responses. Fine-tuning an LLM with business-specific data is traditionally a costly and time-consuming process, and it may not be viable, depending on how often the knowledge base changes (with new or updated records). Keeping the knowledge base external to the model provides more flexibility and makes it easier to ensure that the LLM always has the latest information to serve the users.

![Redis Technical Diagram RedHat Blog RAG](/images/blog/d66b79f31b61553ed3c309f79ba41ecd7a66c574-1700x1284.webp)

**The business benefit**: Improved accuracy, reduced hallucinations and access to up-to-date information for chatbots, content generation tools and more.

In this use case, Redis plays the role of the [vector database](https://redis.io/docs/latest/develop/get-started/vector-database/), while Openshift AI provides the compute resources and notebook environment with pipelines and model serving tools for the data scientists to prepare the vector data and test the quality and performance of semantic searches. OpenShift AI also provides advanced tooling like guardrails to improve LLM accuracy and monitor and better safeguard both user input interactions and model outputs.

By using [Redis as the vector database](https://redis.io/solutions/vector-database/), administrators can configure role-based access control (RBAC) and access control lists (ACLs) to separate vector data between different users, departments, etc. This allows vectors that contain sensitive information that can only be shared to certain users. Redis implements this control at the highest level, not only as a query parameter.

**2. Semantic cache**

LLMs can be expensive to run, especially for repetitive queries. A [semantic cache](/blog/what-is-semantic-caching/) stores LLM responses based on the meaning of the query, not just the exact text. When the user submits a new prompt, the system will look for similar prompts, and if it finds a match, it will retrieve the LLM response directly from the cache, saving a trip to the LLM server and the associated token cost (when using a hosted LLM service) or compute capacity (when self-hosting a model).

![Redis Technical Diagram RedHat Blog Semantic Cache](/images/blog/8a7a878ae4b31591089a1aee8dc7c6726336e589-1700x1284.webp)

**The business benefit:** Semantic caching can greatly reduce LLM costs, especially for use cases where users are expected to ask basic or generic questions (FAQs, etc). Other benefits include faster response times and improved scalability for [AI-powered applications](https://developers.redhat.com/products/red-hat-openshift-ai/overview).

In this use case, Redis will be used as the vector database and semantic cache. Some frameworks, like LangChain, are configured immediately to save prompts to the semantic cache and check automatically for each new prompt. This allows developers to quickly take advantage of this capability without having to write a lot of code, or control reads and writes to the cache. Data scientists can define the distance threshold for the cache based on the requirements and characteristics of the use case.

OpenShift AI provides the environment and tooling such as Jupyter and data science pipelines to create and run the code that will generate the vector data and load it. This can help data scientists not only generate the vector data, but also preload the semantic cache with thousands of questions and answers that can be generated with the help of a LLM. That way, when the first user asks a question, there is a good probability that a similar question is already in the cache, reducing the response time to milliseconds, potentially 15x faster than the traditional RAG pipeline.

If we can ensure a user experience where most of the prompts take only milliseconds to respond, how else can we enrich this user experience? What other data or services can we add to it, if we know that users won’t be waiting for seconds every time?

**3. LLM memory**

LLMs are, by definition, stateless. Meaning, they keep no record of any previous interaction with the user. As far as the model is aware, every prompt is an entirely new prompt, with no past or history to consider.

To get around this limitation, client applications (like chatbots) keep the conversation history between the user and the model (plus some additional information) and serve this data to the model every time the user submits a new prompt. The capacity to use this data is called the “context window,”’ and it makes it possible for the model to keep the answers within the context of the conversation that is happening.

![Redis Technical Diagram RedHat Blog LLM Memory](/images/blog/f3feee0203c38f8814df9d14146a4f3fd5b4066e-1600x1284.webp)

**The business benefit:** More engaging and context-aware chatbots, personalized customer experiences and improved ability to handle complex conversations.

Redis not only stores the context window data, but again provides immediate integrations with frameworks like LangChain, which allows developers to enable LLM memory using only 2 lines of code. Additionally, using Redis to store LLM memory has other impactful benefits, such as:

- It enables multichannel user experiences. Users can close the browser-based chatbot and open the voice assistant in their mobile application and continue the conversation exactly where they left off, because both clients are pulling the conversation history from Redis;
- In case a call center or some other internal team needs to review the conversation history between user and bot, it can very easily be retrieved from Redis. This allows internal staff to understand exactly what happened in that conversation and whether or not the information provided by the model was correct.

Additionally, OpenShift AI provides data scientists with an environment that can be customized to grant access to the conversation history within Redis to fine-tune the conversation model. Having access to a dataset that includes real questions and answers can be critical to ensure the continuous improvement of the LLM responses. With OpenShift AI, data scientists have the resources and tooling to analyse and prepare a dataset to use for fine-tuning the embedding model or the LLM (or to prepare new prompts to ‘pre-warm’ the semantic cache).

Now that we’ve covered the main use cases, let’s see how we can put these ideas into action.

## Getting started

Deploying Redis to [Red Hat OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift) can be greatly simplified using the OperatorHub. In the OpenShift web console, go to the OperatorHub page (in the Operators section of the left-side navigation panel).

From there, you can browse to the Database tab and look for Redis, or simply type Redis in the search bar.

![Supercharge Your AI](/images/blog/278c0d4cca528f42a17f0206499721234c3c91ce-1170x690.webp)

Then you can open the Details page and click on the Install button to deploy the Redis operator.

Once the Operator is deployed, Redis resources can be easily and quickly created through the OpenShift UI:

![Supercharge Your AI Blog](/images/blog/5547280821f6f9c04c6bda15d6e18b8b6ebab6d3-1170x443.webp)

There are 2 main resources for Redis: the cluster and the database (along with their active-active counterparts, which is outside the scope of this article).

The Redis cluster manages multiple databases, ensuring high availability and scalability. This is the first resource that needs to be created. Once the cluster is created, a new database can be created to serve the use cases discussed above. Make sure to enable the Search and JSON support capabilities, as they are necessary for vector search.

Once the database is created, users can access the Redis console to retrieve the connection information, check metrics and track the overall health of the database.

![Supercharge Your AI](/images/blog/0318f4947a4e3fab32078ab9278cbd3fbeb7866c-1513x758.webp)

Next, the OpenShift AI environment can be configured. Here, users can create a notebook environment, provision inference services for local LLMs, create and configure data science pipelines and much more.

![Supercharge Your AI](/images/blog/2b9bd16a0b3049b2fc4df08d570c5cbb11c0c954-1786x1029.webp)

Jupyter notebooks provide a very simple and convenient way to experiment with vector searches. Users can connect to the Redis database with only a few lines of code, and from there, they can take advantage of popular frameworks like LangChain and LlamaIndex, or they can use the [*redis-vl*](https://docs.redisvl.com/en/latest/) package, which allows them to use vector capabilities without requiring a specific framework.

![Supercharge Your AI Blog](/images/blog/287448ab5308b05cb3974387b41da2326ecb00e2-1625x920.webp)

## Conclusion

The increasing popularity of AI tools has unquestionably enabled a broad set of opportunities for companies that are looking to modernize, innovate and stay ahead of the competition.

Providing an environment with the resources and capabilities needed to take advantage of these AI tools is one of the greatest challenges companies face, as they try to understand the value AI could bring to their business.

OpenShift AI and Redis offer a powerful combination for organizations looking to use AI effectively. By providing a flexible gen AI development environment and a high-performance data platform, these technologies empower data scientists and machine learning engineers to build innovative AI solutions that create real business value. Whether it’s RAG, semantic caching or LLM memory, OpenShift AI and Redis provide the foundation for building intelligent applications that are fast, scalable and context-aware.
