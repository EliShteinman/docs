---
title: "Introducing the ChatGPT Memory Project"
linkTitle: "Introducing the ChatGPT Memory Project"
url: "/blog/chatgpt-memory-project/"
description: "ChatGPT Memory responds to context length limitations in large language models (LLMs) used in AI applications. The ChatGPT package uses Redis as a vector database to cache historical user..."
date: 2023-05-02
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2026-06-01
hidden: true
mirrored: true
---

*By Redis   · Published 2 May 2023 · updated 1 June 2026*

![Blog tile image](/images/site-mirror/df61308923a1454a2ba0d3fa61b56a5ca44b9ad3-772x550.webp)

**ChatGPT Memory responds to context length limitations in large language models (LLMs) used in AI applications. The ChatGPT package uses Redis as a vector database to cache historical user interactions per session, which provides an adaptive prompt creation mechanism based on the current context.**

[ChatGPT](https://chat.openai.com/), the AI chatbot created by [OpenAI](https://openai.com/), has revolutionized the realm of intelligent chat-based applications. Its human-like responses and capabilities, derived from the sophisticated GPT-3.5 and GPT-4 large language models (LLMs) and fine-tuned using [reinforcement learning through human feedback](https://huggingface.co/blog/rlhf) (RLHF), took the world by storm since its launch in November 2022. The hype machine is in full force.

Some [ChatGPT interactions are entertainingly silly](https://www.boredpanda.com/here-are-chatgpts-funniest-responses/), some [uses are worrisome](https://www.tomshardware.com/news/google-bard-plagiarizing-article), and they raise [ethical](https://arstechnica.com/gadgets/2023/04/googlers-say-bard-ai-is-worse-than-useless-ethics-concerns-were-ignored/) concerns that affect many professions.

However, everyone takes for granted that this technology inevitably will have a significant impact. For example, Microsoft is already using these models to provide an AI-based coding assistant ([GitHub Copilot](https://www.infoworld.com/article/3692530/visual-studio-code-177-previews-github-copilot-chat.html)) as well as to support its search engine ([Bing](https://www.zdnet.com/article/how-to-use-the-new-bing-and-how-its-different-from-chatgpt/)). [Duolingo and Khan Academy](https://www.makeuseof.com/apps-integrate-use-gpt4/) are using them to power new learning experiences. And [Be My Eyes](https://www.bemyeyes.com/) uses these tools to offer an AI assistant that [helps visually impaired people](https://www.businesswire.com/news/home/20230314005425/en/Be-My-Eyes-Announces-New-Tool-Powered-by-OpenAI%E2%80%99s-GPT-4-to-Improve-Accessibility-for-People-Who-are-Blind-or-Have-Low-Vision).

Despite the success of these language models, they have technical limitations. In particular, software developers who are exploring what they can accomplish with ChatGPT are discovering issues with the amount of *context* they can keep track of in an ongoing conversation.

The *context length* is the amount of information from a previous conversation that a language model can use to understand and respond to. One analogy is [the number of books that an advisor has read](https://towardsdatascience.com/how-to-use-large-language-models-llm-in-your-own-domains-b4dff2d08464) and from which they can offer practical advice. Even if the library is huge, it is not infinite.

It is important to make good use of the context length to create truly powerful LLM-based applications. You need to make clever use of the available context length of the model. That’s especially so because of cost, latency, and model reliability, all of which are influenced by the amount of text sent and received to an [LLM API](https://platform.openai.com/docs/api-reference) such as OpenAI’s.

To resolve the issues with limited context length in AI models like ChatGPT and GPT-4, we can attach an external source of memory for the model to use. This can significantly boost the model’s effective context length and is particularly important for advanced applications powered by [transformer](https://en.wikipedia.org/wiki/Transformer_(machine_learning_model))-based LLM models. Here, we share how we used [Redis’ vector database](/solutions/vector-search/) in our [chatgpt-memory](https://github.com/continuum-llms/chatgpt-memory) project to create an intelligent memory management method.

## Why context length matters

Let’s start by taking a deeper look into why context length matters.

ChatGPT’s context length increased from 4,096 tokens to 32,768 tokens with the advent of GPT-4. The costs for using OpenAI’s APIs for ChatGPT or GPT-4 are calculated based on the number of conversations; you can find more details on its [pricing page](https://openai.com/pricing). Hence, there is a tradeoff between using more tokens to process longer documents and using relatively smaller prompts to minimize cost.

However, truly powerful applications require a large amount of context length.

Theoretically, integrating memory by caching historical interactions in a [vector database](/blog/vector-databases-101/) (i.e. Redis vector database) with the LLM chatbot can provide an infinite amount of context. [Langchain](https://github.com/hwchase17/langchain), a popular library for building intelligent LLM-based applications, already provides such memory implementations. However, these are currently heuristic-based, using either all the conversation history or only the last k messages.

While this behavior may change, the approach is non-adaptive. For example, if the user changes a topic mid-conversation but then comes back to the subject, the simplistic ChatGPT memory approaches might fail to provide the true relevant context from past interactions. One possible cause for such a scenario is token overflow. Precisely, the historic interactions relevant to the current message lie so far back in the conversational history that it isn’t possible to fit them into the input text. Furthermore, since the simplistic ChatGPT memory approaches require a value of k to adhere to the input text limit of ChatGPT, such interactions are more likely fall outside the last k messages.

The range of topics in which ChatGPT can provide helpful personalized suggestions is limited. A more expansive and diverse range of topics would be desirable for a more effective and versatile conversational system.

To tackle this problem, we present the ChatGPT Memory project. ChatGPT Memory uses the Redis vector database to store an embedded conversation history of past user-bot interactions. It then uses vector search inside the embedding space to “intelligently” look up historical interactions related to the current user message. That helps the chatbot recall essential prior interactions by incorporating them into the current prompt.

This approach is more adaptive than the current default behavior because it only retrieves the previous *k* messages relevant to the current message from the entire history. We can add more relevant context to the prompt and never run out of token length. ChatGPT Memory provides adaptive memory, which overcomes the token limit constraints of heuristic buffer memory types. This implementation implicitly optimizes the prompt quality by only incorporating the most relevant history into the prompt; resulting in an implicit cost-efficient approach while also preserving the utility and richness of ChatGPT responses.

## The architecture of the ChatGPT memory project

ChatGPT Memory employs Redis as a vector database to cache historical user interactions per session. Redis provides semantic search based on [K-nearest neighbors](https://scikit-learn.org/stable/modules/neighbors.html) (KNN) search and range filters with distance metrics including L2, Inner Product (IP), and COSINE. These enable adaptive prompt creation by helping to retrieve the semantically-related historical user interactions using one of the distance metrics.

Furthermore, the ChatGPT Memory project takes advantage of the vector indexing algorithms that Redis supports, including the FLAT index (which employs a brute-force approach) and the optimized hierarchical navigable small world (HNSW) index. Redis supports real-time embedding creation/update/delete (CRUD) operations for managing this process in production.

In addition to mitigating the shortcomings of the heuristic memory limitation, ChatGPT Memory allows real-time management of concurrent conversational sessions. It segregates the history of each session, which relates to the user’s past interactions with the chatbot, for each chat session. Once the ChatGPT assistant responds to a user query, both the query and the assistant’s response are embedded using OpenAI’s embedding service. Then the generated embeddings are indexed in a Redis index for later retrieval.

The subsequent interactions are carried out as follows:

1. The user sends a new message to the ChatGPT bot.
1. ChatGPT Memory embeds the user message using the embedding API to obtain the query vector, and it queries the Redis vector database to obtain the top *k* semantically related historic interactions.
1. ChatGPT Memory incorporates the retrieved interactions into the current prompt alongside the current user message, and it sends the prompt to ChatGPT.
1. Once it has ChatGPT’s response, the current interaction is vectorized and cached in the Redis vector database.

This empowers users to get better, personalized answers because the system has more information to draw on.

![an illustration with arrows, a redis logo, and a human head icon dead center](/images/site-mirror/021b5f9335e3e19f26de0fb1ef969602b6f940bd-593x471.webp)

*ChatGPT offers a powerful mechanism for automatic retrieval-based prompt augmentation.*

## Code walkthrough

Before you use ChatGPT Memory, you need to clone the repo and install the dependencies. You also need an [OpenAI API key ](https://platform.openai.com/signup)and access to the Redis cloud-based vector database (which you can [try for free](/try-free/)).

Once you obtain these credentials, set them as environment variables named OPENAI_API_KEY, REDIS_HOST, REDIS_PASSWORD, and REDIS_PORT by plugging in the value in the following bash script.

```bash
# OPENAI API key
EXPORT OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Redis cloud database's credentials
EXPORT REDIS_HOST=localhost
EXPORT REDIS_PORT=1234
EXPORT REDIS_PASSWORD=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

```

After that, you can start using ChatGPT Memory by writing just a few lines of code.

Create an instance of the Redis datastore connection.

```python
from chatgpt_memory.datastore import RedisDataStoreConfig, RedisDataStore


redis_datastore_config = RedisDataStoreConfig(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
)
redis_datastore = RedisDataStore(config=redis_datastore_config)

```

Instantiate the OpenAI embedding client for vectorizing conversation history.

```python
from chatgpt_memory.llm_client import EmbeddingConfig, EmbeddingClient

embedding_config = EmbeddingConfig(api_key=OPENAI_API_KEY)
embed_client = EmbeddingClient(config=embedding_config)

```

Create the memory manager for orchestrating semantic prompt creation based on the current context.

```python
from chatgpt_memory.memory.manager import MemoryManager

memory_manager = MemoryManager(
    datastore=redis_datastore,
    embed_client=embed_client,
    topk=1
)

```

Then connect to the ChatGPT API.

```python
from chatgpt_memory.llm_client import ChatGPTClient, ChatGPTConfig

chat_gpt_client = ChatGPTClient(
    config=ChatGPTConfig(api_key=OPENAI_API_KEY, verbose=True),
    memory_manager=memory_manager
)

```

Finally, you are all set to interact with the ChatGPT client with an infinite contextual and adaptive memory powered by the GPT and the Redis datastore.

```
conversation_id = None
while True:
    user_message = input("\n Please enter your message: ")
    response = chat_gpt_client.converse(
        message=user_message,
        conversation_id=conversation_id
    )
    conversation_id = response.conversation_id
    print(response.chat_gpt_answer)

```

## Example interactions

So, what’s it look like? Consider these two examples of conversations with ChatGPT. They illustrate the difference in performance between the two modes of operation.

### Without ChatGPT memory

![A chatgpt conversation without memory](/images/site-mirror/15d22487cfe780544547d8075caa919b3916d68d-1999x1214.webp)

*The ChatGPT user told the system his name and age in this low-context example… but it doesn’t remember it even a sentence or two later.*

When the memory feature is not activated, the ChatGPT model can’t retrieve any information provided by the user in previous interactions – even from only a few sentences back.

### With ChatGPT memory

![a chatgpt conversation](/images/site-mirror/be5461d11077e5c3f661da52afa8cb660460d878-1999x1165.webp)

*With ChatGPT enabled, the information provided by the user goes into the system to be accessed in later parts of the conversation.*

The two conversations presented have a similar message flow. However, the conversation where the memory feature was not enabled showed that the ChatGPT model could not recall any information that the user had provided. In contrast, when the memory feature was enabled, the model remembered specific details about the user and offered a personalized and customizable conversational experience.

## Next steps

We believe that ChatGPT Memory is a valuable addition to the growing ecosystem of tools designed to improve LLMs’ capabilities. It presents a great opportunity for developers to build powerful and contextually intelligent AI applications.

ChatGPT Memory’s solution also highlights the essential nature of the Redis vector database, which caters to a multitude of AI use cases, including but not limited to LLMs.

To try ChatGPT Memory yourself, head to our GitHub repository and follow the instructions in this post. You should be able to spin up an instance within minutes. Finally, if you’re interested in learning more about building LLM apps with Redis and tools like LangChain, [register for this upcoming RedisDays virtual session](/redisdays/virtual/).
