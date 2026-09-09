---
title: "Announcing LangChain RAG Template Powered by Redis"
linkTitle: "Announcing LangChain RAG Template Powered by Redis"
url: "/blog/announcing-langchain-rag-template-powered-by-redis/"
description: "The recent launch of LangChain Templates introduces a transformative approach for developers to create and deploy generative AI APIs. LangChain Templates, including the new Redis Retrieval..."
date: 2023-12-18
blogCategories:
- "Announcements"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 18 December 2023 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/c2f238b00e7a4cc7b0cc257cddb4b21ad302d21e-772x552.webp)

**The recent launch of **[**LangChain Templates**](https://blog.langchain.dev/langchain-templates/)** introduces a transformative approach for developers to create and deploy generative AI APIs. LangChain Templates, including the new Redis Retrieval Augmented Generation (RAG) template, provide deployable reference architectures that blend efficiency with adaptability.**

AI developers today face a deluge of technology choices between model providers, databases, and development frameworks such as [LangChain](https://github.com/langchain-ai/langchain). Additionally, getting to production requires significant investment beyond Jupyter notebooks and fancy Streamlit demos.

To reduce the friction in deploying APIs, LangChain offers a [hub of deployable architectures](https://templates.langchain.com/). These templates encompass tool-specific chains, Large Language Model (LLM)-specific chains, and technique-specific chains, ensuring comprehensive developer options. Central to their deployment is [LangServe](https://github.com/langchain-ai/langserve), which uses [FastAPI](https://fastapi.tiangolo.com/) to transform LLM-based [Chains](https://python.langchain.com/v0.1/docs/modules/chains/) or [Agents](https://python.langchain.com/v0.1/docs/modules/agents/) into operational REST APIs, enhancing accessibility and production-readiness.

Redis partnered with LangChain to produce the [Redis RAG template](https://github.com/langchain-ai/langchain/tree/master/templates/rag-redis), a package optimized for creating factually consistent, LLM-powered chat applications. By using Redis as the [vector database](/blog/vector-databases-101/), this template ensures rapid context retrieval and grounded prompt construction, crucial for responsive and precise AI responses.

## Getting started with our RAG template

The Redis RAG template serves a REST API for developers to chat with public financial PDF documents such as Nike’s 10k filings. The application uses:

- [FastAPI](https://fastapi.tiangolo.com/) and [Uvicorn](https://www.uvicorn.org/) to serve client requests via HTTP
- [UnstructuredFileLoader](https://python.langchain.com/resources/integrations/document_loaders/unstructured_file) to parse the PDF documents into raw text
- [RecursiveCharacterTextSplitter](https://python.langchain.com/resources/modules/data_connection/document_transformers/text_splitters/recursive_text_splitter) to split the text into smaller chunks
- ‘all-MiniLM-L6-v2’ sentence transformer from [HuggingFace](https://huggingface.co/) to embed text chunks into vectors
- [Redis](/solutions/vector-database) as the vector database for realtime context retrieval
- [OpenAI](https://platform.openai.com) ‘gpt-3.5-turbo-16k’ LLM to generate answers to user queries

![LangChain_RAG_Redis.drawio](/images/site-mirror/fdbd29997e875472c14bf2fa1f3af41b081ace7f-934x491.webp)

To run the RAG application with the template, you will need two things:

1. a running Redis instance ([Redis Cloud](/try-free) or local [Redis Stack](https://redis.io/resources/install/install-stack/))
1. an [OpenAI API](https://platform.openai.com) key

As always, refer to the official [project README](https://github.com/langchain-ai/langchain/tree/master/templates#readme) for the latest details. Here’s a step-by-step guide to build with the template locally:

1. **Environment Setup**: Set your OpenAI API key and Redis environment variables:

```javascript
export OPENAI_API_KEY> export REDIS_HOST> export REDIS_PORT> export REDIS_USER> export REDIS_PASSWORD>
```

Alternatively, you can set the REDIS_URL environment variable instead of the individual components.

2. **Create and activate a Python3.9 virtual environment** (best practice). We will use [venv](https://docs.python.org/3/library/venv.html):

```javascript
python3.9 -m venv lc-template
source lc-template/bin/activate
 
```

3. **Install the LangChain CLI** and Pydantic:

```javascript
pip install -U langchain-cli pydantic==1.10.13
```

3. **Create a new LangChain project**:

```javascript
langchain app new test-rag --package rag-redis>
```

Running the LangChain CLI command shown above will create a new directory named test-rag.

**When prompted to install the template, select the yes option, **y**.** This step will download the rag-redis template contents under the ./test-rag/packages directory and attempt to install Python requirements.

4. Enter the new project directory:

```javascript
cd test-rag

```

Looking at the directory tree, we should see the following structure:

![directory tree](/images/site-mirror/46d89eea40328c17dfdacdbc878cf38db68dd4db-237x423.webp)

5. To use the rag-redis package, **add the following snippet** to your app/server.py file:

```javascript
from rag_redis.chain import chain as rag_redis_chain
add_routes(app, rag_redis_chain, path="/rag-redis")
```

6. **Ingest source data** for demo app:

```javascript
cd packages/rag-redis
python ingest.py
```

This may take a few minutes. The ingest.py script executes a pipeline, as visualized below, that loads the source PDF docs, converts text into smaller chunks, creates text embeddings using a [HuggingFace](https://huggingface.co/) sentence transformer model, and loads data into Redis.

![ ingest.py script executes a pipeline](/images/site-mirror/c07ea38c9cdd188f2ff7d03ad4f834f5b6cd9588-715x170.webp)

7. **Serve the FastAPI** app with LangServe:

```javascript
cd ../ && cd ../
langchain serve
```

8. **Access the API **on port 8000. After spinning up, you should see the following output:

![Langserve](/images/site-mirror/5a1af31646367f2f4507247967e3bfd579fee2af-690x355.webp)

Navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to see documentation.

Visit [http://127.0.0.1:8000/rag-redis/playground](http://127.0.0.1:8000/rag-redis/playground) to use the testing playground, seen below:

![LangServ Playground](/images/site-mirror/318de9c226f7912baef975e1bd259e373ce88561-644x439.webp)

Use the playground to test your API by asking a question. The LangChain application responds with an answer that combines rich context from the Nike company PDF, retrieved from Redis, with the generative abilities of the OpenAI LLM.

## Advance AI innovation with LangChain and Redis

Our ongoing partnership with LangChain reflects a commitment to continual innovation in AI. This collaboration fosters the development of tools such as the [LangChain RAG template](/blog/explore-the-new-multimodal-rag-template-from-langchain-and-redis/) and supports initiatives such as the [OpenGPTs project](/blog/powering-langchain-opengpts-with-redis-cloud/). The partnership also fuels our work in maintaining the [Redis <> LangChain integrations](https://python.langchain.com/resources/integrations/providers/redis), as well Redis’ own AI-native client, [redisvl](https://github.com/RedisVentures/redisvl).

Redis is dedicated to equipping AI developers with the latest resources for creating performant and production-ready applications.

## Next steps

The LangChain RAG template, powered by Redis’ vector database, simplifies the creation of AI applications. Build with this template and leverage these tools to create AI solutions that drive progress in the field.

## Related resources

Powering LangChain

OpenGPTs With Redis Cloud open-source framework for building custom AI agents

Learn more

Vector database

Making it easy to build generative AI applications with Redis Enterprise.

Learn more

RedisVL client

Redis Vector Library (RedisVL) enables Redis as a realtime vector database for LLM Applications.

Learn more
