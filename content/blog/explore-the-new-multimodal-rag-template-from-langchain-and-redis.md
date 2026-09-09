---
title: "Explore the new Multimodal RAG template from LangChain and Redis"
linkTitle: "Explore the new Multimodal RAG template from LangChain and Redis"
url: "/blog/explore-the-new-multimodal-rag-template-from-langchain-and-redis/"
description: "Large language models (LLMs) are trained on massive sets of public data and excel at generating human-like text based on that information. However, they don’t have access to private or corporate..."
date: 2024-05-16
blogCategories:
- "Tech"
authors:
- "Tyler Hutcherson"
- "Lance Martin"
lastmod: 2026-08-13
hidden: true
---

*By Tyler Hutcherson, Lance Martin · Published 16 May 2024 · updated 13 August 2026*

![Blog tile image](/images/site-mirror/3b9140d0db061972cbc22ce08e2f391a58e4d30d-772x552.webp)

Large language models (LLMs) are trained on massive sets of public data and excel at generating human-like text based on that information. However, they don’t have access to private or corporate data, which limits how effective they are for enterprise use cases. Retrieval-augmented generation (RAG) is a popular approach to connect LLMs to this specialized data, broadening their knowledge bases beyond their initial training data. With RAG, companies are using LLMs to answer questions about their unique documents and data.

RAG works by integrating a retrieval component into the generative process. An application first retrieves relevant documents based on an input query and then synthesizes this information to generate a response. This approach not only provides a deeper context but also enhances the model’s responses with the most current information, delivering more accurate and relevant responses compared to traditional LLMs.

**However, most RAG approaches focus exclusively on text, leaving out information-rich images or charts contained in slide decks or reports**. With the rise of multi-modal models, such as [GPT4-V](https://openai.com/research/gpt-4v-system-card), it’s possible to pass images directly into LLMs for reasoning. Still, there’s been a gap in the development of RAG frameworks that seamlessly work with text and images.

[Redis ](https://redis.io/)and [LangChain](https://github.com/langchain-ai/langchain) go beyond text by introducing a [template for multimodal RAG](https://github.com/langchain-ai/langchain/tree/master/templates/rag-redis-multi-modal-multi-vector). By incorporating visual data, this template allows models to process and reason across both text and images, paving the way for more comprehensive and nuanced AI apps. We’re thrilled to present a system that not only reads text but also interprets images, effectively combining these sources to enhance understanding and response accuracy.

In this post, we’ll:

1. **Introduce multimodal RAG**
1. **Walk through template setup**
1. **Show a few sample queries and the benefits of using multimodal RAG**

## Go beyond simple RAG

The typical RAG pipeline involves indexing text documents with [vector embeddings](https://redis.io/glossary/vector-embeddings/) and metadata, retrieving relevant context from the database, forming a grounded prompt, and synthesizing an answer with an LLM. For more on this, see LangChain’s video series [RAG From Scratch](https://www.youtube.com/watch?v=wd7TZ4w1mSw).

![](/images/site-mirror/ef9a5fb5c5b346f30edb669e010a2907d75a4135-1327x626.webp)

*But what about non-textual data like images or graphics? *For these other data types, we have to extract semantics with a unique process. For example, consider analyzing a slide deck of the Nvidia Q3 FY24 investor presentation. The slides are a combination of text, images, tables, and charts. Standard PDF extraction techniques will only extract text, leaving information-rich images outside retrieval scope.

Fortunately, we can solve this using the flexible data structures in [Redis](https://redis.io) and the innovative capabilities of OpenAI’s combined text and vision model, [GPT4-V](https://platform.openai.com/docs/guides/vision). To setup the multi-modal RAG pipeline, we start with a few preprocessing steps:

1. **Extract slide summaries** as text using GPT4-V
1. **Embed text summaries **using [OpenAI’s embedding models](https://platform.openai.com/docs/guides/embeddings)
1. **Index text summary embeddings** in Redis hashes, referenced by a primary key
1. **Encode raw images** as base64 strings and store them in Redis hashes with a primary key

For this use case, LangChain provides the [MultiVector Retriever](https://python.langchain.com/docs/modules/data_connection/retrievers/multi_vector) to index documents and summaries efficiently. The benefit of this approach is that we can employ commonly used text embeddings to index image *summaries* just like any other text, avoiding the need for more specialized and less mature multimodal embeddings.

Now at runtime, when a user asks a question:

1. **Embed the user question** using OpenAI
1. **Retrieve relevant images** from Redis based on the embedded image summaries
1. **Look up the raw images** from Redis using the primary key
1. **Generate an informed answer** using GPT4-V with the raw images and original question


As RAG functionality continues to advance, many expect that processes like this will have more retrieval calls to databases and to LLMs, creating [compound AI systems](https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/). Each of these additional steps increases lag and cost. Redis [semantic caching](https://www.redisvl.com/user_guide/llmcache_03.html) reduces the number of calls to databases and LLMs for repeat questions, removing redundant work. Semantic caching works by storing responses from previously answered questions. Then, when a similar question is asked, the application retrieves that stored answer from the cache instead of initiating a duplicate call to the database and another costly call to the LLM. By removing additional steps for frequently-asked questions, apps can speed up responses and significantly reduce the cost of calling LLMs.

## Spin up with the RAG template

Before starting the app, you need a (free) [Redis Cloud instance](https://redis.com/try-free) and an [OpenAI API key](https://platform.openai.com).

1. Set your **OpenAI API key** and** Redis URL** environment variables:

```
export OPENAI_API_KEY=<your-openai-api-key>
export REDIS_URL=redis://:<redis-pwd>@<redis-host>:<redis-port>

```

2. **Install the LangChain CLI** in your Python environment:

```
pip install -U langchain-cli

```

3. **Create a new LangChain app**:

```
langchain app new my-app
cd my-app

```

This will create a new directory called my-app with two folders:

- app: Where LangServe code lives
- packages: Where your chains or agents live

4. **Add the multimodal rag package:**

```
langchain app add rag-redis-multi-modal-multi-vector

```

**When prompted to install the template, select the yes option, **y**.**

5. **Add the following snippet** to your app/server.py file:

```python
from rag_redis_multi_modal_multi_vector.chain import chain as rag_redis_chain

add_routes(
    app,
    rag_redis_chain,
    path="/rag-redis-multi-modal-multi-vector"
)

```

6. **Ingest source data** for demo app:

```
cd packages/rag-redis-multi-modal-multi-vector

poetry install
poetry run python ingest.py

```

This may take a few minutes. The ingest.py script executes a pipeline to load slide images, extract summaries with GPT4-V, and create text embeddings.

7. **Serve the FastAPI** app with LangServe:

```
cd . . /. . / 

langchain serve

```

8. **Access the API **at [http://127.0.0.1:8000](http://127.0.0.1:8000) and test your app via the playground at [http://127.0.0.1:8000/playground](http://127.0.0.1:8000/playground):

![](/images/site-mirror/fedc9163b36717b7f7f4b6b76aac486d63f944fb-1402x602.webp)

![](/images/site-mirror/21596ca289ca53d9d7c06761c878896d1c68336f-1432x988.webp)

Validate the answer from the RAG system by quickly checking the referenced PDF image from the slide deck.

![](/images/site-mirror/52860fb5b30dcbfec6f1461678bb72d833c36b51-1064x814.webp)

In addition to LangServe, LangChain also has an observability platform called [LangSmith](https://www.langchain.com/langsmith). This will log all generations performed by the template, allowing for inspection of the prompt and validation of the images passed to GPT-4V. For example, you can see a trace on [langchain.com](https://smith.langchain.com/public/d77b7b52-4128-4772-82a7-c56eb97e8b97/r/ed6726ad-b733-4cbe-bc9a-0e6378d80e24) on multi-modal data that shows extraction of information from financial charts.

## Wrapping up

With the new multimodal RAG template, devs can now build sophisticated AI apps that understand and leverage diverse data types powered by a single backend technology—Redis.

Get started by setting up a free [Redis Cloud instance](https://redis.io/try-free) and using the new[Redis <> LangChain](https://github.com/langchain-ai/langchain/tree/master/templates/rag-redis-multi-modal-multi-vector). For insights on other emerging RAG concepts, [explore the recent session](https://redis.io/events/the-future-of-rag-exploring-advanced-llm-architectures-with-langchain-and-redis/) with Lance Martin, Nuno Campos, and Tyler Hutcherson.

## Related Resources

- [RAG Multimodal Template](https://github.com/langchain-ai/langchain/tree/master/templates/rag-redis-multi-modal-multi-vector)
- [The Future of RAG: Exploring Advanced LLM Architectures with LangChain and Redis](https://redis.io/events/the-future-of-rag-exploring-advanced-llm-architectures-with-langchain-and-redis/)
