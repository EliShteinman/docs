---
title: "Building a RAG application with Redis and Spring AI"
linkTitle: "Building a RAG application with Redis and Spring AI"
url: "/blog/building-a-rag-application-with-redis-and-spring-ai/"
description: "Vector databases frequently act as memory for AI apps. This is especially true for those powered by large language models (LLMs). Vector databases allow you to perform semantic search, which..."
date: 2024-04-16
blogCategories:
- "Tech"
authors:
- "Julien Ruaux"
lastmod: 2025-06-11
hidden: true
---

*By Julien Ruaux, Principal Field Engineer at Redis · Published 16 April 2024 · updated 11 June 2025*

![Blog tile image](/images/site-mirror/3264129fe6e554bf443dfe688faf3ab27fca6c6d-1200x628.webp)

Vector databases frequently act as memory for AI apps. This is especially true for those powered by large language models (LLMs). Vector databases allow you to perform semantic search, which provides relevant context for prompting the LLM.

Until recently, there weren’t many options for building AI apps with Spring and Redis. Now, Redis has gained traction as a high-performance vector database. And the Spring community introduced a new project called [Spring AI](https://docs.spring.io/spring-ai/reference/index.html), which aims to simplify the development of AI-powered apps, including those that leverage vector databases.

Let’s see how we can build a Spring AI app that uses Redis as its vector database, focusing on implementing a Retrieval Augmented Generation (RAG) workflow.

## Retrieval Augmented Generation

Retrieval Augmented Generation (RAG) is a technique used to integrate data with AI models. In a RAG workflow, the first step involves loading data into a vector database, such as Redis. When a user query is received, the vector database retrieves a set of documents similar to the query. These docs then serve as the context for the user’s question and are used in conjunction with the user’s query to generate a response, typically through an AI model.

In this example, we’ll use a dataset containing information about beers, including attributes such as name, Alcohol By Volume (ABV), International Bitterness Units (IBU), and a description for each beer. This dataset will be loaded into Redis to demonstrate the RAG workflow.

## Code and Dependencies

You can find all [code for the Spring AI and Redis demo on Github](https://github.com/redis-developer/spring-ai-redis-demo).

This project makes use of the usual Spring Boot starter dependencies for web apps as well as Azure OpenAI and [Spring AI Redis](https://github.com/redis-developer/spring-ai-redis-demo/blob/fce5e4004aceec875c2a585f38b57b6549781f02/pom.xml#L41).

## Data Load

The data we will use for our app consists of JSON documents providing information about beers. Each doc has the following structure:

```javascript
{
  "id": "00gkb9",
  "name": "Smoked Porter Ale",
  "description": "The Porter Pounder Smoked Porter is a dark rich flavored ale that is made with 5 malts that include smoked and chocolate roasted malts. It has coffee and mocha notes that create a long finish that ends clean with the use of just a bit of dry hopping",
  "abv": 8,
  "ibu": 36
}
```

To load this beer dataset into Redis, we will use the RagDataLoader class. This class contains a run method that is executed at app startup. Within this method, we use a JsonReader to parse the dataset and then insert the documents into Redis using the [autowired VectorStore](https://github.com/redis-developer/spring-ai-redis-demo/blob/fce5e4004aceec875c2a585f38b57b6549781f02/src/main/java/com/redis/demo/spring/ai/RagDataLoader.java#L32).

```
// Create a JSON reader with fields relevant to our use 
caseJsonReader loader = new JsonReader(file, "name", "abv", "ibu", "description");
// Use the autowired VectorStore to insert the documents into 
RedisvectorStore.add(loader.get());
```

What we have at this point is a dataset of about 22,000 beers with their corresponding embeddings.

## RAG Service

The RagService class implements the RAG workflow. When a user prompt is received, the retrieve method is called, which performs the following steps:

- Computes the vector of the user prompt
- Queries the Redis database to retrieve the most relevant documents
- Constructs a prompt using the retrieved documents and the user prompt
- Calls a ChatClient with the prompt to generate a response

```
public Generation retrieve(String message) { 
  SearchRequest request = SearchRequest.query(message).withTopK(topK); 
// Query Redis for the top K documents most relevant to the input message 
  List<Document> docs = store.similaritySearch(request); Message systemMessage = getSystemMessage(docs); UserMessage userMessage = new UserMessage(message); 
  // Assemble the complete prompt using a template 
  Prompt prompt = new Prompt(List.of(systemMessage, userMessage)); // Call the autowired chat client with the prompt
  ChatResponse response = client.call(prompt); return response.getResult();}
```

## Controller

Now that we have implemented our RAG service, we can wrap it in a HTTP endpoint.

The RagController class exposes the service as a POST endpoint:

```
@PostMapping("/chat/{chatId}")
@ResponseBody
public Message chatMessage(@PathVariable("chatId") String chatId, @RequestBody Prompt prompt) { 
  // Extract the user prompt from the body and pass it to the autowired RagService 
  Generation generation = ragService.retrieve(prompt.getPrompt()); 
  // Reply with the generated message 
  return Message.of(generation.getOutput().getContent());}
```

## User Interface

For the user interface, we have created a simple React front end that allows users to ask questions about beers. The front end interacts with the Spring back end by sending HTTP requests to the /chat/{chatId} endpoint and displaying the responses.

![Redis](/images/site-mirror/08194d211eff6d49f1a69aa53398b006052213fb-1600x793.webp)

And done–with just a few classes, we have implemented a RAG application with Spring AI and Redis.

To take the next step, we encourage you to [check out the example code on Github](https://github.com/redis-developer/spring-ai-redis-demo). And if you have any questions or issues, don’t hesitate to [open a ticket](https://github.com/redis-developer/spring-ai-redis-demo/issues/new). Combining Redis’ speed and ease of use with the handy abstractions provided by Spring AI makes it so much easier for Java developers to build responsive AI applications with Spring. We can’t wait to see what you build.

## Related Resources

- The code presented in this article is available on [GitHub](https://github.com/redis-developer/spring-ai-redis-demo.git).
- The documentation for Spring AI Redis is available [here](https://docs.spring.io/spring-ai/reference/api/vectordbs/redis.html).
- For more information about Spring AI, visit the [project homepage](https://docs.spring.io/spring-ai/reference).
- Learn more about the Redis vector search API in the [Redis vector documentation](https://redis.io/docs/interact/search-and-query/advanced-concepts/vectors/).
