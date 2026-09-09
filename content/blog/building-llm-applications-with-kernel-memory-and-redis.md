---
title: "Building LLM Applications with Kernel Memory and Redis"
linkTitle: "Building LLM Applications with Kernel Memory and Redis"
url: "/blog/building-llm-applications-with-kernel-memory-and-redis/"
description: "Redis now integrates with Kernel Memory, allowing any dev to build high-performance AI apps with Semantic Kernel."
date: 2024-05-21
blogCategories:
- "Tech"
authors:
- "Steve Lorello"
lastmod: 2025-07-03
hidden: true
---

*By Steve Lorello, Developer Advocate · Published 21 May 2024 · updated 3 July 2025*

![Blog tile image](/images/blog/5d463137a2025e41a24063a3e2cdd3732edbe744-772x552.webp)

**Redis now integrates with Kernel Memory, allowing any dev to build high-performance AI apps with Semantic Kernel.**

[Semantic Kernel](https://github.com/microsoft/semantic-kernel) is Microsoft’s developer toolkit for integrating LLMs into your apps. You can think of Semantic Kernel as a kind of operating system, where the LLM is the CPU, the LLM’s context window is the L1 cache, and your vector store is what’s in RAM. [Kernel Memory](https://github.com/microsoft/kernel-memory) is a component project of Semantic Kernel that acts as the memory-controller, and this is where Redis steps in, acting as the physical memory.

As an AI service, Kernel Memory lets you index and retrieve unstructured multimodal data. You can use KM to easily implement common LLM design patterns such as retrieval-augmented generation (RAG). Redis is a natural choice as the back end for Kernel Memory when your apps require high performance and reliability.

In this post, we’ll see how easily we can build an AI chat app using Semantic Kernel and Redis.

## Modes of Operation

There are two ways you can run Kernel Memory:

1. Directly within your app
1. As a standalone service

If you run Kernel Memory directly within your app, you’re limiting yourself to working within the .NET ecosystem (no great issue for this .NET dev), but the beauty of running Kernel Memory as a standalone service is that it can be addressed by any language that can make HTTP requests.

## Running the sample

To illustrate the platform neutrality of Kernel Memory, we’ve provided two samples, one in Python and one in .NET. In practice, any language that can run an HTTP server can easily be substituted to run with this example.

### Clone the sample

To clone the .NET sample, run the following:

```python
git clone --recurse-submodules https://github.com/redis-developer/redis-rag-chat-dotnet

```

To clone the python sample, run:

```python
git clone --recurse-submodules https://github.com/redis-developer/redis-rag-chat-python

```

### Running the samples

These example apps rely on OpenAI’s completion and embedding APIs. To start, obtain an OpenAI API key. Then pass the API key to docker-compose. This will start:

1. The front-end’s service (written in react)
1. The back-end’s web service—written in .NET or Python, depending on the repository you are using
1. Redis Stack
1. Kernel Memory as its own standalone service

```python
OpenAIApiKey=<YOUR_OPENAI_API_KEY> docker compose up

```

### Add data to Kernel Memory

We have a pre-built dataset of beer information that we can add to Kernel Memory (and ask it for recommendations). To add that dataset, just run:

```python
./common/scripts/setup_beers.sh

```

### Accessing the front end

To access the front end, navigate to http://localhost:3000., From there, you can ask the bot for recommendations:

![](/images/blog/c7ec83c94dff21be83a477e030d9bcb15f143b46-1775x1016.webp)

## How does this all work?

There are several parts of this demo:

1. Redis
1. Our React front end, which provides a simple chat interface
1. Kernel Memory
1. The back end, which maintains the chat session, searches Kernel Memory, and crafts the prompts for the LLM

Redis has vector database enabled, which is a feature provided by Redis, [Redis Cloud](https://redis.com/cloud/overview/), and [Azure Cache for Redis (Enterprise Tier)](https://redis.com/cloud-partners/microsoft-azure/). Any of these options will work. Our front end is a simple React app. Kernel Memory requires some configuration, which we’ll cover below. Plugins and HTTP calls drive our back end, so we’ll cover that, too.

## Configuring Kernel Memory

To get Kernel Memory up and running with Redis, you need to make some minor updates to the

```python
common/kernel-memory/appsettings.json file. Start with the template 

```

```python
common/kernel-memory/appsettings.json. 

```

```python
Rename this file to appsettings.json. 

```

Notice in this file that there is a Retrieval object:

```python
"Retrieval": {
 "MemoryDbType": "Redis",
 "EmbeddingGeneratorType": "OpenAI",
 "SearchClient": {
   "MaxAskPromptSize": -1,
   "MaxMatchesCount": 100,
   "AnswerTokens": 300,
   "EmptyAnswer": "INFO NOT FOUND"
 }
}


```

This tells the retriever which Embedding Generator to use (OpenAI) and which MemoryDbType to use (Redis).

There’s also a Redis Object:

```python
"Redis": {
 "Tags": {
   "user": ",",
   "email": "|"
 },
 "ConnectionString": "redis-km:6379",
 "AppPrefix":"redis-rag-chat-"
}


```

This Redis object maps out the important configuration parameters for the Redis connector in Kernel Memory:

- The** ConnectionString** is a [StackExchange.Redis connection string](https://stackexchange.github.io/StackExchange.Redis/Configuration#basic-configuration-strings), which tells it how to connect to Redis.
- **Tags** tells Kernel Memory which possible tags you might want to filter on and provides optional separators for you to allow you to follow [Redis Tag Semantics](https://redis.io/docs/interact/search-and-query/advanced-concepts/tags/).
- **AppPrefix** lets you provide an app prefix for Kernel Memory, so you can have multiple Kernel Memory apps working with the same Redis Database.

## Interacting with Kernel Memory

There are fundamentally two things we want to do with Kernel Memory:

1. Add Memories
1. Query Memories

To be sure, Kernel Memory has a lot more functionality, including information extraction, partitioning, pipelining, embedding generation, summarization, and more, but we’ve configured all of that already and they’re all in service of those two goals.

To interact with Kernel Memory, you use the HTTP interface. There are a few front ends for this interface:

1. Within a Semantic Kernel Plugin
1. With the IKernelMemory interface (in .NET)
1. Directly with the Http endpoints

## Adding documents to Kernel Memory

To upload a document, invoke one of the **IKernelMemory’s** Import functions. In the .NET example, we used a simple Document import with a file stream, but you can import web pages and text as well:

```python
[HttpPost("upload")]
public async Task<IActionResult> AddDocument(IFormFile file)
{
   await using var fileStream = file.OpenReadStream();
   var document = new Document().AddStream(file.FileName, fileStream);
   var res = await _kernelMemory.ImportDocumentAsync(document);
   return Ok(res);
}


```

In Python, there’s no KernelMemory client (yet), but you can simply use the Upload endpoint:

```python
@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
   file_content = await file.read()


   data = {
       "index": "km-py",
       "id": str(uuid.uuid4())
   }
   files = {'file': (file.filename, file_content, file.content_type)}


   response = requests.post(f"{kernel_memory_url}/upload", files=files, data=data)
   response.raise_for_status()
   return {"status": response.status_code, "response_data": response.text}


```

## Querying Kernel Memory

To query Kernel Memory, you can use either the Search or the Ask endpoint. The search endpoint does a search of the index, and returns the most relevant documents to you, whereas the ask endpoint performs the search and then pipes the results into an LLM.

### Invoke from a prompt

The Kernel Memory .NET client comes with its own plugin, which allows you to invoke it from a prompt:

```python
{{$systemPrompt}}


The following is the answer generated by kernel memory, put it into your own words:


Result:{{memory.ask $intent}}


```

The prompt above will summarize a response to Kernel Memory’s ask endpoint given the provided system prompt (and the intent generated from the chat history and the most recent message earlier in the pipeline). To get the plugin itself working, you’ll need to add the Memory Plugin to the kernel. The following are clipped portions from the Program.cs of the .NET project:

```python
var kmEndpoint = builder.Configuration["KernelMemoryEndpoint"];  
var kernelMemory = new MemoryWebClient(kmEndpoint);
builder.Services.AddSingleton(kernelMemory);
var kernelBuilder = builder.Services.AddKernel();
kernelBuilder.AddOpenAIChatCompletion(builder.Configuration["OpenAICompletionModelId"]!, builder.Configuration["OpenAIApiKey"]!);
kernelBuilder.Plugins.AddFromObject(new MemoryPlugin(kernelMemory), "memory");


```

This injects Kernel Memory into the DI container, then adds Semantic Kernel, and finally adds the MemoryPlugin from the Kernel Memory Client to Semantic Kernel.

### Invoking from an HTTP Endpoint

Naturally, you can also invoke these query functions from an HTTP endpoint. In the Python sample, we just invoke the search endpoint (and then format the results):

```python
def get_memories(question: str) -> str:
   data = {
       "index": "km-py",
       "query": question,
       "limit": 5
   }


   response = requests.post(f"{kernel_memory_url}/search", json=data)


   if response.status_code == 200:
       response_json = response.json()
       memories = response_json.get('results',[])

```

```python
   res = ""
       for memory in memories:
           res += "memory:"
           for partition in memory['partitions']:
               res += partition['text']
           res += '\n'
       print(res)
       return res


   raise Exception(response.text)

```

These memories can then be fed into our LLM to give it more context when answering a question.

## Wrapping Up

Semantic Kernel provides a straightforward way of managing the building blocks of the semantic computer, and Kernel Memory provides an intuitive and flexible way to interface with the memory layer of the Semantic Kernel. As we’ve observed here, integrating Kernel Memory with Redis is as simple as a couple of lines in a config file.
