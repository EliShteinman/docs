---
title: "Build fast, production-worthy AI apps with Spring AI and Redis"
linkTitle: "Build fast, production-worthy AI apps with Spring AI and Redis"
url: "/blog/build-fast-production-worthy-ai-apps-with-spring-ai-and-redis/"
description: "This post was co-written by Josh Long, an Spring Developer Advocate at Broadcom and Brian Sam-Bodden, an Applied AI Engineer at Redis. This post was written to show how you can use Redis in Spring..."
date: 2025-05-19
blogCategories:
- "Partners"
- "Tech"
authors:
- "Brian Sam-Bodden"
- "Josh Long"
lastmod: 2025-07-03
hidden: true
---

*By Brian Sam-Bodden, Josh Long · Published 19 May 2025 · updated 3 July 2025*

![Blog tile image](/images/site-mirror/e7c11c6b6ee952abae32b822e87df5f56fd8d5c7-772x554.webp)

*This post was co-written by Josh Long, an Spring Developer Advocate at Broadcom and Brian Sam-Bodden, an Applied AI Engineer at Redis. This post was written to show how you can use Redis in *[*Spring AI 1.0*](https://spring.io/blog/2025/05/20/spring-ai-1-0-GA-released)*, which was announced GA today.*

[Spring AI 1.0](https://spring.io/blog/2025/05/20/spring-ai-1-0-GA-released) is a comprehensive solution for AI engineering in Java. It’s now available after a significant development period influenced by rapid advancements in the AI field. The release includes numerous essential new features for AI engineers. Redis is a native vector store for Spring AI, helping you build fast AI apps.

Java and Spring are in a prime spot for AI right now. Tons of companies are running on Spring Boot, which makes it easy to plug AI into what you’re already doing. You can simply link up your business logic and data right to AI models without too much hassle.

![](/images/site-mirror/ab00325afd9559929412a316c16acaf0645d4535-1600x900.webp)

*(The picture shown is used with permission from the Spring AI team lead Dr. Mark Pollack)*

Spring AI provides support for various AI models and technologies. **Image models** can generate images given text prompts. **Transcription models** can take audio and convert them to text. **Embedding models **are models that convert arbitrary data into vectors, which are data types optimized for semantic similarity search. **Chat models **should be familiar. You’ve no doubt even had a brief conversation with one before. Chat models are where most of the fanfare seems to be in the AI space. You can get them to help you correct a document or write a poem (just don’t ask them to tell a joke … yet). They’re incredibly powerful, but they have some issues.

![](/images/site-mirror/f19a00a81fed5ced7412f6127dd7f709393ee50f-1600x900.webp)

*(The picture shown is used with permission from the Spring AI team lead Dr. Mark Pollack)*

Let’s go through some of these problems and their solutions in Spring AI. Chat models are open-minded and can easily be distracted. You need to give them a **system prompt **to govern their response shape and structure.

AI models don’t have memory. It’s up to you to help them connect one message from a given user to another by giving them **memory**.

Next, AI models live in isolated sandboxes, but they can do powerful things if you give them access to tools — functions that they can invoke when they deem it necessary. Spring AI supports **tool calling,** which lets you tell the AI model about tools in its environment, which it can then ask you to invoke. This multi-turn interaction is all handled transparently for you.

Additionally, AI models are smart but they’re not omniscient. They don’t know what’s in your proprietary databases—nor I think, would you want them to. So you need to inform their responses by **augmenting the prompts** – basically using the mighty string concatenation operator to put text in the request that the model considers *before* it looks at the question being asked. It’s similar to adding background information if you like.

Lastly, you can augment it with a lot of data, but not infinite amounts. How do you decide what should be sent and what shouldn’t? Use a vector store to select only the relevant data and send it in onward. This is called **retrieval augmented generation**, or **RAG**.

AI chat models like to, well, chat. Sometimes they do it so confidently that they can make up things. So, you need to use evaluation — using one model to check the results of another—to make sure the results are fair.

Of course, no AI app is an island. Today, modern AI systems and services work best when integrated with other systems and services. **Model Context Protocol **(MCP) lets it connect your AI apps with other MCP-based services, regardless of what language they’re written in. You can assemble all of this into **agentic **workflows that drive towards a larger goal.

You can do all this while building on the familiar idioms and abstractions any Spring Boot developer will have come to expect: Convenient starter dependencies for basically everything are available on the [**Spring Initializr**](https://start.spring.io)**. **Spring AI provides convenient Spring Boot autoconfigurations that give you the convention-over-configuration setup you’ve come to know and expect. And Spring AI supports observability with Spring Boot’s Actuator and the Micrometer project. It plays well with GraalVM and virtual threads, too, allowing you to build fast and efficient AI apps that scale.

### RAG should stand for “Redis Augmented Generation”

You’ve probably already installed Redis, and you know what a workhorse it is. You probably already know that it’s second to none for key-value storage.

But did you know that:

- It can also handle session storage, with key expirations, and distribution across multiple nodes.
- It can manage distributed locks with mutual exclusion in distributed environments thanks to features like Redlock.
- It can do feature flagging and configuration with fast read/write and TTL support.
- It can store real-time event logging and stream processing with the amazing STREAMS support.
- It can sort rankings for things like leaderboards with the sorted set (ZSET) structure.
- It can be handy for message queuing and pub-sub with things like LIST, STREAM, and PUBSUB.
- It can do search and autocompletion with things like ZSET or TRIE.
- It can manage real-time analytics and counters with things like atomic counters.

It can do *all* of this while being the fastest database on the market. So would it surprise you to learn it can also handle vector storage? RAG is a key part of today’s AI use cases. Sure, with today’s models, you *could* send huge amounts of data on each request, but that can be slow and costly. Instead, you send a selection of the most pertinent data. The faster you can determine what that pertinent data is, the better. Here’s where Redis makes the difference: It’s durable and also *fast*.

Let’s look at a simple app.

To create this app, we went to the [Spring Initializr](https://start.spring.io), specified Redis vector database, Docker compose, OpenAI, GraalVM, Actuator, and Web. We’re using Java 24 and Apache Maven as the build tool. We hit Generate and got a zip file that, once unzipped, gives us a project we can import into our IDE of choice.

The first thing’s first: We need to connect to a Redis database. The Spring Initialize generated a project with a valid compose.yml that will give you a fully functioning Redis instance, and Spring Boot will automatically start and stop that Redis instance each time you start the application. I find it annoying to have to restart the instance each time, so I tell (with configuration in application.properties) the Spring Boot Docker Compose support to just start it if it’s not already running.

```
spring.docker.compose.lifecycle-management=start_only

```

The generated compose.yml gives us most of what we want, but during development we find it highly useful to login to the Redis instance to inspect what’s been done as wemake changes. We like using the redis-cli for command line access or the fantastically intuitive [Redis Insight](https://redis.io/insight/) tool. It’s a visual tool with lots of quality-of-life improvements. We installed it using Homebrew: brew install –cask redis-insight.

We’re going to build an application that looks at the wide and wonderful world of beer. We’ll need some schema initialized in Redis too.

```java
spring.ai.vectorstore.redis.initialize-schema=true

spring.ai.vectorstore.redis.index-name=beers

spring.ai.vectorstore.redis.prefix=beer:

```

Let’s now build our RAG app. We want folks to be able to ask about certain recommended pairings and about beer. What beer you ask? Well, the beer described in this 26mb gzip-compressed archive in the sample code called beers.json.gz. Let’s load that into the vector store using Spring AI’s JsonReader and some basic I/O. We’ll do this when the application starts up in a bean of type ApplicationRunner.

```java
private static final Resource BEERS_DATA = new ClassPathResource("/beers.json.gz");

@Bean

ApplicationRunner vectorStoreInitializer(
       RedisVectorStoreProperties properties,
       RedisVectorStore vectorStore) {
   return _ -> {
       var indexInfo = vectorStore.getJedis().ftInfo(properties.getIndexName());
       var numDocs = (Long) indexInfo.getOrDefault("num_docs", 0L);
       if (numDocs != 0)
           return;
       System.out.println("Creating Embeddings... (this may take a while)");
       try (var inputStream = new GZIPInputStream(BEERS_DATA.getInputStream())) {
           var resource = new InputStreamResource(inputStream, "beers.json.gz");
           var loader = new JsonReader(resource, "name,abv,ibu,description".split(","));
           vectorStore.add(loader.get());
           System.out.println("Embeddings created!");
       }
   };
}

```

Run this and wait a while—it took several minutes on our machine. But it will finish, eventually.

Let’s inspect the data via the redis-cli:

```
~ redis-cli

127.0.0.1:6379> ft._list

1) beers

```

You can also get the details on the index:

```
127.0.0.1:6379> ft.info beers

1) index_name
2) beers
3) index_options
4) (empty array)
5) index_definition
6) 1) key_type
   2) JSON
   3) prefixes
   4) 1) beer:
   5) default_score
   6) "1"
7) attributes
8) 1) 1) identifier
      2) $.content
      3) attribute
      4) content
....

```

Nice. I love looking at the data itself in Redis Insight though.

![](/images/site-mirror/955e29cdaa1f1103efa52c6d2094ca007433f6bb-1600x1102.webp)

So much beer. So little time. How’s somebody supposed to know which beer to choose and when and why? That’s why we’re going to build an assistant to help people make the right decisions. We’ll pair Spring AI with all the data hosted in ‌Redis vector storage to make a winning combo.

Now let’s build that beer assistant as a Spring MVC controller:

```java
@Controller
@ResponseBody

class BeerController {
   private final ChatClient ai;
   BeerController(ChatClient.Builder ai, VectorStore vectorStore) {
       var defaultSystemPrompt = """
               You're assisting with questions about products in a beer catalog.
               Use the information from the DOCUMENTS section to provide accurate answers.
               The answer involves referring to the ABV or IBU of the beer, include the beer name in the response.
               If unsure, simply state that you don't know.
               """;
       this.ai = ai
               .defaultAdvisors(new QuestionAnswerAdvisor(vectorStore))
               .defaultSystem(defaultSystemPrompt)
               .build();
   }

   @GetMapping("/beers")

   String beers(@RequestParam String question) {
       return this.ai
               .prompt()
               .user(question)
               .call()
               .content();
   }
}

```

This controller exposes one endpoint, /beers, to which you can send requests with questions. In the constructor of the controller, we build and configure the Spring AI ChatClient by first specifying a *system prompt*. A system prompt governs the overall tone and tenor of the responses from the model. The model needs to know about the data in Redis’ vector store, so we’ll configure an advisor (an interceptor that can pre- and post-process requests to the model) with a `QuestionAnswerAdvisor`. To get this type on the classpath, we added the following dependency:

```java
<dependency>
   <groupId>org.springframework.ai</groupId>
   <artifactId>spring-ai-advisors-vector-store</artifactId>
</dependency>

```

And that’s it. Run the program and hit the endpoint like this:

```java
http :8080/beers question=="what beer pairs best with meats?"     

```

On one run, we got the following response:

```java
HTTP/1.1 200 
Connection: keep-alive
Content-Length: 215
Content-Type: text/plain;charset=UTF-8
Date: Sat, 03 May 2025 20:07:42 GMT
Keep-Alive: timeout=60

For pairing with meats, I recommend the Swabian Hall, which has an ABV of 4.7 and an IBU of 30. It's a Smoked Brown Ale that's perfect for hog roasts, making it an excellent choice to complement various meat dishes.

```

Nice. Can you imagine making beer somehow even *more* convenient?

## Production-worthy AI

Now, it’s time to turn our eyes toward production.

### Scalability

We want this code to be scalable. Remember, each time you make an HTTP request to an LLM (or many SQL databases), you’re doing *blocking* I/O. I/O that sits on a thread and makes that thread available to any other demand in the system until the I/O has completed. This is a waste of a perfectly good thread. Threads aren’t meant to just sit idle, waiting. Java 21 and later gives us virtual threads, which—for sufficiently I/O bound services—can *dramatically* improve scalability. That’s why you set up spring.threads.virtual.enabled=true in the application.properties file.

### GraalVM native images

GraalVM is a compiler that is ready for use. You can use it through the GraalVM Community Edition open source project or through the very powerful (and free) Oracle GraalVM distribution.

GraalVM requires that you stipulate what dynamic behavior will happen in the application, things like JNI proxies, resource loading, serialization, reflection, etc. The Java Redis driver we’re using here loads a few things at runtime, so we need to account for them. Add the following to your main application class:

```java
static class Hints implements RuntimeHintsRegistrar {

   @Override

   public void registerHints(RuntimeHints hints, ClassLoader classLoader) {
       hints.resources().registerPattern("redis/clients/jedis/pom.properties");
       hints.resources().registerPattern("redis/clients/jedis/LICENSE");
       hints.resources().registerResource(BEERS_DATA);
   }
}

```

If you’ve got that setup as your SDK, you can turn this Spring AI app into an operating system and architecture specific native image with ease:

```java
./mvnw -DskipTests -Pnative native:compile

```

This takes a minute or so on most machines, but once it’s done, you can run the binary with ease.

```java
./target/redis

```

This program will start up in a fraction of the time that it did on the JVM. You might want to comment on the ApplicationRunner we created earlier since it’s going to do I/O on startup time, significantly delaying that startup. On my machine, it starts up in less than a tenth of a second.

Even better, you should observe that the app takes a very small fraction of the RAM it would’ve otherwise taken on the JVM.

That’s all very well and good, you might say, but I need to get this running on a cloud platform and that means getting it into the shape of a Docker image. Easy.

```java
./mvnw -DskipTests -Pnative spring-boot:build-image

```

Stand back. This might take another minute still. When it finishes, you’ll see it printed out the name of the Docker image that’s been generated.

You can run it, remembering to override the hosts and ports of things it would’ve referenced on your host.

```
docker run docker.io/library/redis:0.0.1-SNAPSHOT

```

We’re on macOS, and amazingly, this application when run in a macOS virtual machine emulating Linux, runs *even faster*—and right from the jump than it would’ve on macOS directly.

### Observability

You’re well advised to keep an eye on your system resources and importantly the token count. All requests to an LLM have a cost—at least one of complexity, if not dollars and cents. Thankfully, Spring AI has your back. Launch a few requests to the model, and then up the Spring Boot Actuator metrics endpoint (powered by Micrometer.io):

```
http://localhost:8080/actuator/metrics 

```

You’ll see some metrics related to token consumption. Nice. You can use Micrometer to forward those metrics to your time-series database of choice to get a single pane of glass, a dashboard.

## Next steps

You’ve just built a production-worthy, AI-ready Spring AI and Redis database powered app in no time at all. We’ve only begun to scratch the surface. We could add conversational memory. We could export the beer functionality as an Model Context Protocol (MCP) service using Spring AI’s class-leading MCP support (the Spring AI team wrote the Java MCP SDK that underpins every other MCP integration out there could integrate security for encryption at rest. The possibilities are endless. In the meantime, check out Spring AI 1.0 at the [Spring Initializr](https://start.spring.io) today and learn more about [Redis](https://redis.io).
