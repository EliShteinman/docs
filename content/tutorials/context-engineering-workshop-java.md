---
title: "Context Engineering Workshop for Java Developers"
linkTitle: "Context Engineering Workshop for Java Developers"
url: "/tutorials/context-engineering-workshop-java/"
description: "Welcome to this hands-on workshop, where you'll learn to implement sophisticated context-engineering patterns. Context Engineering is the practice of strategically designing, structuring, and..."
group: "For AI"
date: 2026-02-25
lastmod: 2026-05-08
hidden: true
---

*Published 25 February 2026 · updated 8 May 2026*

> **TL;DR:**
>
> Context engineering is the discipline of designing and optimizing the full information pipeline feeding an LLM — memory, retrieval, ranking, caching, and token budgets — so the model consistently produces accurate, relevant responses. This workshop teaches it hands-on across 9 labs: you'll build a Java AI application with LangChain4J and Redis that progresses from a stateless chatbot to a production-ready system with short- and long-term memory, RAG, query compression, content reranking, few-shot prompting, token management, and semantic caching.

## Introduction

Welcome to this hands-on workshop, where you'll learn to implement sophisticated context-engineering patterns. Context Engineering is the practice of strategically designing, structuring, and optimizing the information provided to AI models (particularly LLMs) to achieve desired outputs. It goes beyond simple prompt engineering by considering the entire context window and how data is organized, presented, and sequenced to maximize model performance. In this workshop, you will learn how to implement this using [Java](https://www.java.com/en/), [LangChain4J](https://github.com/langchain4j/langchain4j), and [Redis](https://redis.io/).

## Why context engineering?

LLMs have limited context windows and no inherent memory between conversations. Without proper context engineering:

- Models lose track of conversation history
- Responses lack relevant domain knowledge
- Token limits are exceeded, causing failures
- Repeated API calls increase costs

This workshop teaches you patterns to solve these challenges systematically.

## What you'll build

By the end of this workshop, you'll have built a complete AI application featuring:

- LLM integration using OpenAI, Spring Boot, and LangChain4J
- Vector embeddings for semantic search with a chunking strategy
- RAG (Retrieval-Augmented Generation) with knowledge bases
- Dual-layer memory architecture (short-term and long-term memory)
- Query compression techniques for efficient context retrieval
- Content Reranking to optimize the relevance of retrieved information
- Few-shot learning pattern for improved generated responses
- Dynamic context window management based on token limits
- Semantic caching to optimize performance and reduce LLM costs

## Prerequisites

### Required knowledge

- Basic understanding of Java programming — if you're new to Redis with Java, start with the [Java getting-started tutorial](/tutorials/develop/java/getting-started/)
- Basic knowledge of LLMs and AI concepts — for a gentler intro to RAG, see the [AI-powered chatbot tutorial](/tutorials/howtos/solutions/vector/gen-ai-chatbot/)
- Familiarity with command-line interfaces
- Basic understanding of Docker and Git
- Familiarity with RESTful APIs

### Required software

- [Java 21+](https://www.oracle.com/java/technologies/downloads)
- [Maven 3.9+](https://maven.apache.org/install.html)
- [Docker](https://docs.docker.com/get-docker/)
- [Git](https://git-scm.com/install/)
- [Node.js](https://nodejs.org/en/download/)

### Required accounts

| Account                                          | Description                                              | Cost                  |
| :----------------------------------------------- | :------------------------------------------------------- | :-------------------- |
| [OpenAI](https://auth.openai.com/create-account) | LLM that will power the responses for the AI application | Free trial sufficient |
| [Redis Cloud](https://redis.io/try-free)         | Semantic caching service powered by Redis LangCache      | Free tier sufficient  |

> **NOTE**
>
> **Note on OpenAI costs:** While OpenAI occasionally offers free trial credits to new accounts, this workshop assumes pay-as-you-go pricing. The estimated cost of $1-3 covers all 9 labs. You can monitor your usage in the [OpenAI dashboard](https://platform.openai.com/usage) to track costs in real-time.

## Workshop structure

This workshop has an estimated duration of 2 hours and is organized into 9 progressive labs, each building on the previous one. Each lab introduces a specific context engineering challenge, which is then addressed in the subsequent lab.

| Lab | Topic                                                  | Duration | Branch          |
| :-- | :----------------------------------------------------- | :------- | :-------------- |
| 1   | Set up and deploy the AI application                   | 25 mins  | `lab-1-starter` |
| 2   | Enabling short-term memory with chat memory            | 10 mins  | `lab-2-starter` |
| 3   | Knowledge base with embeddings, parsers, and splitters | 10 mins  | `lab-3-starter` |
| 4   | Implementing basic RAG with knowledge base data        | 15 mins  | `lab-4-starter` |
| 5   | Enabling on-demand context management for memories     | 10 mins  | `lab-5-starter` |
| 6   | Implementing query compression and context reranking   | 15 mins  | `lab-6-starter` |
| 7   | Implementing a few-shot into the system prompt design  | 05 mins  | `lab-7-starter` |
| 8   | Enabling token management to handle token limits       | 05 mins  | `lab-8-starter` |
| 9   | Implementing semantic caching for conversations        | 25 mins  | `lab-9-starter` |

Each lab also contains a corresponding `lab-X-solution` branch with the completed code for reference. You can use this branch to compare your current implementation using `git diff {lab-X-solution}`. Alternatively, you can switch to the solution branch at any time during the lab if you are falling behind or to get unstuck.

## Getting started

### Step 1: Clone the repository

```bash
git clone https://github.com/redis-developer/context-engineering-workshop-java.git
```

### Step 2: Verify your environment

Ensure you have Java, Maven, Node.js, Docker, and Git installed. You can check their versions with:

```bash
java -version
mvn -version
npm --version
docker --version
git --version
```

### Step 3: Begin your first lab

Navigate to the cloned repository.

```bash
cd context-engineering-workshop-java
```

---

## Lab 1: Set up and deploy the AI application

### Learning objectives

By the end of this lab, you will:

- Set up a complete AI application development environment with LangChain4J
- Deploy the base Spring Boot application with OpenAI integration
- Deploy the base Node.js frontend application for testing purposes
- Understand the core architecture for LangChain4J-based AI applications
- Play with the AI application to verify correct LLM connectivity

**Estimated Time: 25 minutes**

### What you're building

In this foundational lab, you'll deploy a basic AI chat application that will serve as the platform for implementing context engineering patterns throughout the workshop. This includes:

- **Node.js Frontend**: Simple chat interface for testing purposes
- **Spring Boot Application**: RESTful API backend for AI interactions
- **LangChain4J Integration**: Framework for LLM orchestration
- **OpenAI Connection**: GPT model for generating responses

#### Architecture overview

![Lab 1 architecture diagram showing Spring Boot backend, Node.js frontend, and OpenAI](/images/site-mirror/48eb774d064eaab7225366ebca542798a3e7b01b-3277x320.webp)

### Prerequisites check

Before starting, ensure you have:

- [ ] Java 21+ properly installed
- [ ] Maven 3.9+ installed
- [ ] Docker up and running
- [ ] Git configured and authenticated
- [ ] Node.js 18+ and npm installed
- [ ] OpenAI API key ready
- [ ] Your IDE (IntelliJ IDEA, VS Code, or Eclipse)

### Setup instructions

#### Step 1: Switch to the lab 1 branch

```bash
git checkout lab-1-starter
```

#### Step 2: Create an environment file

```bash
cp .env.example .env
```

#### Step 3: Define your OpenAI API key

```bash
OPENAI_API_KEY=your-openai-api-key
```

#### Step 4: Build the backend application

```bash
cd backend-layer
```

```bash
mvn clean package
```

#### Step 5: Execute the backend application

```bash
mvn spring-boot:run
```

#### Step 6: Install the NPM dependencies

```bash
cd frontend-layer
```

```bash
npm install
```

#### Step 7: Start the frontend application

```bash
npm start
```

### Testing your setup

#### API health check

Test the health endpoint

```bash
curl http://localhost:8080/actuator/health
```

Expected response:

```json
{ "status": "UP" }
```

#### Basic chat test

Test basic chat functionality

```bash
curl -X GET "http://localhost:8080/ai/chat/string?query=Hello"
```

You should receive a streaming response.

#### Frontend verification

1. Open http://localhost:3000 in your browser
2. Type "Hi, my name is {{your-name}}" in the chat
3. Verify you receive a response from the AI
4. Type "Can you tell me my name?" in the chat
5. Verify if the AI don't remember your name

![Chat interface showing conversation with the AI assistant](/images/site-mirror/9ea30c0da002add71267f860d9a71da6546c2a1d-2026x1498.webp)

### Understanding the code

#### 1. `BasicChatAssistant.java`

- Simple AI Service interface using LangChain4J
- Uses Reactive Flux for streaming responses

#### 2. `ChatController.java`

- REST endpoint for chat interactions
- Currently returns simple string responses

#### 3. `GeneralConfig.java`

- Provides CORS configuration for web frontend

#### 4. `application.properties`

- Leverages the Spring Boot starter for LangChain4J
- Set the OpenAI API key and model parameters

### What's missing? (Context engineering perspective)

At this stage, your application lacks:

- **No Short Memory**: Each conversation is isolated
- **No Context Awareness**: No previous message history

**This is intentional.** We'll add these capabilities in the next lab.

### Lab 1 troubleshooting

**Error: "API key not valid" from OpenAI**

Solution:

- Verify your API key in the `.env` file
- Ensure the key has proper permissions
- Check if you have credits in your OpenAI account

**Error: "Connection refused" on localhost:8080**

Solution:

- Ensure the Spring Boot application is running
- Check if port 8080 is already in use
- Review application logs for startup errors

**Error: "npm: command not found"**

Solution:

- Install Node.js from nodejs.org
- Verify installation: `node --version`
- Restart your terminal after installation

### Lab 1 completion

Congratulations. You've successfully:

- Set up the development environment
- Deployed the base AI application
- Verified LLM integration is working

### Additional resources

- [LangChain4J docs](https://docs.langchain4j.dev/)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [Spring Boot](https://docs.spring.io/spring-boot/index.html)

---

## Lab 2: Enabling short-term memory with chat memory

### Learning objectives

By the end of this lab, you will:

- Set up the Redis Agent Memory using Docker
- Implement short-term memory using LangChain4J's ChatMemory
- Enable conversation continuity within a single chat session
- Understand how chat memory stores maintain conversation context
- Test memory retention across multiple message exchanges

**Estimated Time: 10 minutes**

### What you're building

In this lab, you'll enhance the basic chat application with short-term memory capabilities, allowing the AI to remember previous messages within a conversation session. This includes:

- **ChatMemoryStore**: LangChain4J implementation for the Agent Memory
- **Context Preservation**: Maintaining conversation flow across messages
- **Memory Configuration**: Setting up memory boundaries and constraints

#### Architecture overview

![Lab 2 architecture with Redis Agent Memory](/images/site-mirror/1c266638d126e75f07e27e59444604128b179b88-3277x994.webp)

### Prerequisites check

Before starting, ensure you have:

- [ ] Completed Lab 1 successfully
- [ ] Backend application running without errors
- [ ] Frontend application accessible at http://localhost:3000
- [ ] OpenAI API key configured and working

### Setup instructions

#### Step 1: Switch to the lab 2 branch

```bash
git checkout lab-2-starter
```

#### Step 2: Define the Redis Agent Memory URL

```bash
AGENT_MEMORY_SERVER_URL=http://localhost:8000
```

#### Step 3: Start Redis Agent Memory

```bash
docker compose up -d
```

#### Step 4: Verify if the containers are running

```bash
docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}\t{{.Names}}"
```

You should see something like this:

```bash
CONTAINER ID   IMAGE                                  STATUS                   PORTS                                         NAMES
48df24537047   redislabs/agent-memory-server:0.12.7   Up 2 minutes (healthy)   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp   redis-agent-memory-server
33aade92ddbd   redis/redisinsight:3.0.2               Up 2 minutes (healthy)   0.0.0.0:5540->5540/tcp, [::]:5540->5540/tcp   redis-insight
3c449915bb35   redis:8.4.0                            Up 2 minutes (healthy)   0.0.0.0:6379->6379/tcp, [::]:6379->6379/tcp   redis-database
```

#### Step 5: Review the ChatMemoryStore implementation

Open `backend-layer/src/main/java/io/redis/devrel/workshop/extensions/WorkingMemoryStore.java` and review the code.

This is a wrapper around the Redis Agent Memory REST APIs implemented using the support for chat memory stored from LangChain4J.

#### Step 6: Implement the ChatMemoryStore bean

Open `backend-layer/src/main/java/io/redis/devrel/workshop/memory/ShortTermMemory.java` and implement the method `chatMemoryStore()`.

Change from this:

```java
@Bean
public ChatMemoryStore chatMemoryStore() {
    // TODO: Implement a WorkingMemoryStore that connects to the agentMemoryServerUrl
    return null;
}
```

To this:

```java
@Bean
public ChatMemoryStore chatMemoryStore() {
    return WorkingMemoryStore.builder()
            .agentMemoryServerUrl(agentMemoryServerUrl)
            .storeAiMessages(true)
            .build();
}
```

This bean will provide the persistence layer for the chat memory, taking care of storing and retrieving messages from the Redis Agent Memory.

#### Step 7: Implement the ChatMemory bean

Open `backend-layer/src/main/java/io/redis/devrel/workshop/memory/ShortTermMemory.java` and implement the method `chatMemory()`.

Change from this:

```java
@Bean
public ChatMemory chatMemory(ChatMemoryStore chatMemoryStore) {
    // TODO: Implement a WorkingMemoryChat that uses the WorkingMemoryStore
    return null;
}
```

To this:

```java
@Bean
public ChatMemory chatMemory(ChatMemoryStore chatMemoryStore) {
    return WorkingMemoryChat.builder()
            .id(userId)
            .chatMemoryStore(chatMemoryStore)
            .build();
}
```

This bean will manage the chat memory for each user session, using the `WorkingMemoryStore` to persist messages.

#### Step 8: Rebuild and run the backend

```bash
cd backend-layer
mvn clean package
mvn spring-boot:run
```

#### Step 9: Keep the frontend running

The frontend should still be running from Lab 1. If not:

```bash
cd frontend-layer
npm start
```

### Testing your memory implementation

#### Memory retention test

1. Open http://localhost:3000 in your browser
2. Clear any previous conversations (refresh the page)
3. Type "Hi, my name is {{your-name}}" in the chat
4. Verify you receive a response acknowledging your name
5. Type "What is my name?" in the chat
6. **Verify the AI now remembers your name** (unlike in Lab 1)

![Chat demonstrating memory retention across messages](/images/site-mirror/5aac522b38d10491b04f74f8893556864782bb7f-2026x1498.webp)

As you can see, the AI now remembers your name within the same session, demonstrating that short-term memory is functioning correctly. This is possible because now the code is leveraging the Redis Agent Memory to store and retrieve conversation history.

If you want to verify the stored messages, you can use Redis Insight to connect to the Redis database and inspect the stored keys and values. Open your browser and type the following:

http://localhost:5540

Click on the database `redis-database:6379` and expand the `Keys` section to see the stored messages. You should see the following key:

![Redis Insight keys view showing working memory keys](/images/site-mirror/c5574f116124501fc78c6a7840d9774574dc9f08-2778x1644.webp)

If you click on the key, you can see the stored messages in JSON format.

![Redis Insight key detail view with stored message JSON](/images/site-mirror/3fef18cfd485eb69c868dd95518858be35829997-2780x1644.webp)

With this implementation of short-term memory, your chat application can now maintain context within a session, providing a more natural and engaging UX. This will happen even if the backend layer is restarted.

However, keep in mind that these messages are still short-term, meaning that they are shorted-lived. By default, the implementation of the ChatMemoryStore updates the working memory to be active for 5 minutes. This is controlled by the TTL property of the key.

### Understanding the code

#### 1. `ChatMemoryStore`

- Storage implementation for the Agent Memory
- Session-based memory isolation with dedicated namespace
- Temporary storage for conversations (up to 5 minutes)

#### 2. `ChatMemory`

- Pass-through implementation of a chat memory
- Always keeps all the messages in-memory
- Implemented for testing purposes (not production)

#### 3. Memory integration

- Automatically injected into the AI service
- Maintains conversation context transparently
- No changes needed to `BasicChatAssistant`

### What's still missing? (Context engineering perspective)

Your application now has short-term memory, but still lacks:

- ❌ **No Long-term Memory**: Memory is lost between sessions
- ❌ **No Knowledge Base**: No knowledge besides the conversation
- ❌ **No Semantic Search**: Cannot retrieve relevant information

**Next labs will address these limitations.**

### Lab 2 troubleshooting

**Error: "ChatMemory bean not found"**

Solution:

- Ensure `@Configuration` annotation is present on ShortTermMemory class
- Verify all `@Bean` methods are properly annotated
- Check that component scanning includes the memory package

**AI still doesn't remember previous messages**

Solution:

- Verify ChatMemoryStore bean is properly configured
- Check that the same userId is being used across messages
- Check if the Agent Memory is running and accessible

**Memory seems to cut off too early**

Solution:

- Check if you are not having network issues (unlikely with local setup)
- Review token limit configuration in your OpenAI account
- Consider the model's token limit (gpt-3.5-turbo has 4096 tokens)

### Lab 2 completion

Congratulations. You've successfully:

- ✅ Implemented short-term chat memory
- ✅ Enabled conversation continuity within sessions
- ✅ Tested memory retention across messages

### Additional resources

- [Redis Agent Memory](https://redis.github.io/agent-memory-server/)
- [LangChain4J Chat Memory](https://docs.langchain4j.dev/tutorials/chat-memory)

---

## Lab 3: Knowledge base with embeddings, parsers, and splitters

### Learning objectives

By the end of this lab, you will:

- Configure document parsing for PDF files using Apache PDFBox
- Implement document splitting strategies for optimal chunk sizes
- Create vector embeddings for semantic search capabilities
- Store processed documents in the Redis Agent Memory
- Understand how document processing enables knowledge-augmented AI

**Estimated Time: 10 minutes**

### What you're building

In this lab, you'll add document processing capabilities to your AI application, allowing it to ingest PDF documents and create a searchable knowledge base. This includes:

- **Document Parser**: Apache PDFBox for extracting text from PDFs
- **Document Splitter**: Paragraph-based splitting for optimal chunks
- **Embeddings Generation**: Converting text to vector representations
- **Knowledge Storage**: Persisting document chunks for semantic retrieval

#### Architecture overview

![Lab 3 architecture adding PDF files](/images/site-mirror/806a3c3461953e515244e8b6e312aa675fb15384-3277x1672.webp)

### Prerequisites check

Before starting, ensure you have:

- [ ] Completed Lab 2 successfully
- [ ] Redis Agent Memory running (from Lab 2)
- [ ] Backend application configured with memory support
- [ ] Sample PDF documents ready for testing

### Setup instructions

#### Step 1: Switch to the lab 3 branch

```bash
git checkout lab-3-starter
```

#### Step 2: Configure the knowledge base input directory

Add to your `.env` file:

```bash
KNOWLEDGE_BASE_INPUT_FILES=/data/input-files
```

#### Step 3: Add sample PDF documents

Place at least one or more PDF files in the `KNOWLEDGE_BASE_INPUT_FILES` directory. For testing, you can use any PDF document that has multiple pages and paragraphs.

#### Step 4: Review the FilesProcessor implementation

Open `backend-layer/src/main/java/io/redis/devrel/workshop/services/FilesProcessor.java` and review the document processing logic:

```java
@Service
public class FilesProcessor {
    // Automatic PDF scanning every 5 seconds
    @Scheduled(fixedRate = 5000)
    public void scanForPdfFiles() {
        // Scans for new PDF files
    }
}
```

As you can see, the `scanForPdfFiles()` method is scheduled to run every 5 seconds to check for new PDF files in the input directory. Once a file is detected, it calls the `processFile()` method to handle the document.

#### Step 5: Implement the document processing

Open `backend-layer/src/main/java/io/redis/devrel/workshop/services/FilesProcessor.java` and implement the PDF file processing behavior. You won't need to implement everything, just the parts that are pending.

In the `processFile()` method, change from this:

```java
private void processFile(File file) {
    // TODO: Initialize these objects properly
    final DocumentParser documentParser = null;
    final DocumentSplitter documentSplitter = null;
```

To this:

```java
private void processFile(File file) {
    final DocumentParser documentParser = new ApachePdfBoxDocumentParser();
    final DocumentSplitter documentSplitter = new DocumentByParagraphSplitter(1000, 100);
```

In the `scanForPdfFiles()` method, change from this:

```java
@Scheduled(fixedRate = 5000)
public void scanForPdfFiles() {
    File dir = new File(knowledgeBaseInputFiles);
    if (dir.exists() && dir.isDirectory()) {
        File[] pdfFiles = dir.listFiles((d, name) -> name.toLowerCase().endsWith(".pdf"));
        if (pdfFiles != null) {
            for (File pdf : pdfFiles) {
                // TODO: Uncomment the line below to enable file processing
                // processFile(pdf);
            }
        }
    }
}
```

To this:

```java
@Scheduled(fixedRate = 5000)
public void scanForPdfFiles() {
    File dir = new File(knowledgeBaseInputFiles);
    if (dir.exists() && dir.isDirectory()) {
        File[] pdfFiles = dir.listFiles((d, name) -> name.toLowerCase().endsWith(".pdf"));
        if (pdfFiles != null) {
            for (File pdf : pdfFiles) {
                processFile(pdf);
            }
        }
    }
}
```

With these changes, your application is now set up to automatically detect and process PDF files placed in the specified input directory. The parser and the splitter implementations used here were provided by the LangChain4J framework.

#### Step 6: Rebuild and run the backend

```bash
cd backend-layer
mvn clean package
mvn spring-boot:run
```

#### Step 7: Monitor document processing

Watch the console logs to see your PDFs being processed:

```bash
INFO  FilesProcessor : Processing file /path/to/your-document.pdf
INFO  FilesProcessor : Processed your-document.pdf - 15 segments stored out of 18 total
```

### Testing your knowledge base

#### Document processing verification

1. Place a PDF file in the `KNOWLEDGE_BASE_INPUT_FILES` directory
2. Wait 5-10 seconds for the scheduled scanner to detect it
3. Check the logs for processing confirmation
4. Verify the file is renamed to `.processed`

```bash
ls -la knowledge-base-input-files/
# You should see: your-document.processed
```

#### Verify knowledge base storage

Using Redis Insight (http://localhost:5540):

1. Connect to the Redis database
2. Look for keys with the pattern `knowledge.entry.*`
3. Inspect the stored document segments

![Redis Insight showing processed document keys in knowledge base](/images/site-mirror/ceaff1c45cf012e0a44d7fa7717ec25edd02f05c-3274x1964.webp)

#### Test document chunks

Each chunk should contain:

- Document metadata (filename, section number)
- The actual text content from the created chunk
- An embedding field containing the vector data

![Redis Insight detail view of document chunk with embeddings](/images/site-mirror/a3586137a161bae2f8d8877ee408c7e5c5f2cdea-3020x1900.webp)

#### Processing multiple documents

1. Add 2-3 PDF files to the input directory
2. Monitor the logs to see batch processing
3. Verify all documents are processed and renamed
4. Check Redis for multiple knowledge entries

### Understanding the code

#### 1. `ApachePdfBoxDocumentParser`

- Extracts text content from PDF files
- Preserves document structure and formatting
- Handles various PDF encodings and formats

#### 2. `DocumentByParagraphSplitter`

- Splits documents into manageable chunks (1000 chars)
- Maintains 100-character overlap for context continuity
- Preserves paragraph boundaries when possible

#### 3. `MemoryService.createKnowledgeBaseEntry()`

- Stores document chunks in dedicated namespace
- Creates vector embeddings for semantic search
- Mark the document as semantic data for retrieval

#### 4. Automatic processing

- Scheduled task runs every 5 seconds
- Processes new PDFs automatically
- Renames files to `.processed` to avoid reprocessing

### What's still missing? (Context engineering perspective)

Your application now has a knowledge base, but still lacks:

- ❌ **No Retrieval**: Can't search or retrieve relevant documents
- ❌ **No RAG Integration**: Knowledge isn't used in responses
- ❌ **No Query Routing**: Can't determine when to use knowledge

**Next lab will implement RAG to use this knowledge.**

### Lab 3 troubleshooting

**PDF files not being detected**

Solution:

- Verify the `KNOWLEDGE_BASE_INPUT_FILES` path is correct
- Ensure PDF files have `.pdf` extension (lowercase)
- Check file permissions for read access
- Review logs for directory scanning errors

**Document parsing fails**

Solution:

- Ensure PDF is not corrupted or password-protected
- Check if PDF contains extractable text (not just images)
- Verify Apache PDFBox dependencies are properly included
- Try with a simpler PDF document first

**Segments not being stored**

Solution:

- Verify Redis Agent Memory is running
- Check network connectivity to Redis
- Ensure segments meet minimum length (50 characters)
- Review logs for storage errors

### Lab 3 completion

Congratulations. You've successfully:

- ✅ Configured document parsing for PDFs
- ✅ Implemented intelligent document splitting
- ✅ Created a searchable knowledge base
- ✅ Stored document embeddings for semantic retrieval

### Additional resources

- [LangChain4J Document Loaders](https://docs.langchain4j.dev/tutorials/rag/#document-loader)
- [Apache PDFBox docs](https://pdfbox.apache.org/)
- [Document Splitting Strategies](https://docs.langchain4j.dev/tutorials/rag/#document-splitter)
- [Vector Embeddings Explained](https://redis.io/glossary/vector-embeddings/)

---

## Lab 4: Implementing basic RAG with knowledge base data

### Learning objectives

By the end of this lab, you will:

- Implement Retrieval-Augmented Generation (RAG) using your knowledge base
- Implement a content retriever to search for data in your knowledge base
- Set up a retrieval augmentor to inject relevant context
- Enable the AI to answer questions using document knowledge
- Test RAG functionality with document-specific queries

**Estimated Time: 20 minutes**

### What you're building

In this lab, you'll connect your knowledge base to the chat interface, enabling the AI to retrieve and use relevant document information when answering questions. This includes:

- **Content Retriever**: Searches the knowledge base for relevant information
- **Content Injection**: Formats retrieved documents for optimal LLM understanding
- **RAG Pipeline**: Complete flow from query to augmented response using query routing

#### Architecture overview

![Lab 4 architecture with RAG pipeline and knowledge base retriever](/images/site-mirror/5f1502efa8148de732782e4a7e32e1e2827d7ffd-3277x1672.webp)

### Prerequisites check

Before starting, ensure you have:

- [ ] Completed Lab 3 successfully
- [ ] At least one PDF processed in your knowledge base
- [ ] Redis Agent Memory running with stored documents
- [ ] Backend application with document processing enabled

### Setup instructions

#### Step 1: Switch to the lab 4 branch

```bash
git checkout lab-4-starter
```

#### Step 2: Review the LongTermMemory configuration

Open `backend-layer/src/main/java/io/redis/devrel/workshop/memory/LongTermMemory.java` and review the RAG configuration structure:

```java
@Configuration
public class LongTermMemory {

    @Autowired
    private MemoryService memoryService;

    @Bean
    public RetrievalAugmentor getRetrievalAugmentor() {
        // TODO: Implement a content injector and a query router to build the
        // RetrievalAugmentor correctly.
        return DefaultRetrievalAugmentor.builder()
                .build();
    }

    private ContentRetriever getGeneralKnowledgeBase() {
        // TODO: Implement a ContentRetriever to retrieve the knowledge base
        return null;
    }
}
```

#### Step 3: Implement the knowledge base content retriever

In `LongTermMemory.java`, locate and implement the `getGeneralKnowledgeBase()` method.

Change from this:

```java
private ContentRetriever getGeneralKnowledgeBase() {
    // TODO: Implement retriever that searches the knowledge base
    return null;
}
```

To this:

```java
private ContentRetriever getGeneralKnowledgeBase() {
    return query -> memoryService.searchKnowledgeBase(query.text())
            .stream()
            .map(Content::from)
            .toList();
}
```

#### Step 4: Configure the RAG pipeline

In the `getRetrievalAugmentor()` method, implement the content injector configuration.

Change from this:

```java
@Bean
public RetrievalAugmentor getRetrievalAugmentor() {
    // TODO: Implement a content injector and a query router to build the
    // RetrievalAugmentor correctly.
    return DefaultRetrievalAugmentor.builder()
            .build();
}
```

To this:

```java
@Bean
public RetrievalAugmentor getRetrievalAugmentor() {
    ContentInjector contentInjector = DefaultContentInjector.builder()
            .promptTemplate(PromptTemplate.from("{{userMessage}}\n\n[Context]\n{{contents}}"))
            .build();

    QueryRouter queryRouter = new DefaultQueryRouter(List.of(getGeneralKnowledgeBase()));

    return DefaultRetrievalAugmentor.builder()
            .contentInjector(contentInjector)
            .queryRouter(queryRouter)
            .build();
}
```

#### Step 5: Rebuild and run the backend

```bash
cd backend-layer
mvn clean package
mvn spring-boot:run
```

#### Step 6: Keep the frontend running

The frontend should still be running. If not:

```bash
cd frontend-layer
npm start
```

### Testing your RAG implementation

#### Basic RAG test

1. Open http://localhost:3000 in your browser
2. Ask a question about content from your uploaded PDF
3. Verify the AI uses document information in its response

Example test queries (adjust based on your PDF content):

- "What does the document say about [specific topic]?"
- "Can you summarize the main points from the uploaded documents?"
- "What information is available about [specific term from PDF]?"

For example, consider the following text from a sample PDF:

```txt
The garage door has a wireless touchpad mounted on the doorjamb, left side facing the door.
It is battery operated with a 5 digit code of 70170. It will raise and lower the garage door from
the outside. You should also reprogram your garage door opener in your car. I would guess
the directions are in your car's manual and on the side of the lift motor in the garage. (I think I
would program the car first and then reprogram the push button touchpad.)

Mounted inside the garage on the right side of the door into the kitchen is a lock box. It
contains a key to that door and all the other exterior doors of the house. The code is 1389.
Push the buttons to enter the code and then push down and hold the slider button and pull off
the front of the box. This slider button is also a reset so if you enter an incorrect code, reset
the lock and try again. You must unlock it again to reinstall it onto the lockbox. If you remove
the piece of cardboard inside the lock, it will expose the code and allow you to change it,
using the cardboard "edge" that is there to make the code selections.
```

This is how you can interact with the AI:

![Chat response using RAG with document context](/images/site-mirror/df3c6abf036541025b0349d36fb2518185d05763-2026x1500.webp)

### Understanding the code

#### 1. `ContentRetriever`

- Searches the knowledge base using semantic similarity
- Returns only relevant document chunks for the query
- Leverages vector embeddings for accurate retrieval

#### 2. `DefaultContentInjector`

- Formats retrieved content for LLM consumption
- Uses template to structure context and query
- Maintains clear separation between context and user message

#### 3. `QueryRouter`

- Determines which retriever to use for queries
- Routes to knowledge base for factual questions
- Can be extended for multiple knowledge sources

#### 4. `DefaultRetrievalAugmentor`

- Orchestrates the complete RAG pipeline
- Combines retrieval, injection, and generation
- Manages the flow from query to response

#### 5. `ChatController`

- Contains an optimized version of the system prompt
- Provides instructions about how to read the context
- Provides guidelines for generating accurate responses

### What's still missing? (Context engineering perspective)

Your application now has basic RAG, but still lacks:

- ❌ **No User Memories**: Can't store personal preferences
- ❌ **No Query Optimization**: No compression or transformation
- ❌ **No Content Reranking**: Retrieved content isn't prioritized
- ❌ **No Dynamic Routing**: Can't choose between memory types

**Next labs will add these advanced features.**

### Lab 4 troubleshooting

**AI doesn't use document knowledge**

Solution:

- Verify PDFs were successfully processed (check `.processed` files)
- Ensure knowledge base entries exist in Redis
- Check retriever configuration in LongTermMemory
- Review logs for retrieval errors

**Retrieved content seems irrelevant**

Solution:

- Check if embeddings were properly generated
- Verify the semantic search is working
- Try with more specific queries
- Ensure document chunks are meaningful

**Response time is slow**

Solution:

- Check Redis connection latency
- Verify number of retrieved documents (may be too many)
- Monitor OpenAI API response times
- Consider implementing caching (coming in Lab 9)

### Lab 4 completion

Congratulations. You've successfully:

- ✅ Implemented Retrieval-Augmented Generation
- ✅ Connected your knowledge base to the chat interface
- ✅ Enabled document-aware AI responses
- ✅ Tested RAG with real document queries

### Additional resources

- [LangChain4J RAG Tutorial](https://docs.langchain4j.dev/tutorials/rag)
- [Understanding RAG Systems](https://redis.io/glossary/retrieval-augmented-generation/)
- [Content Retriever Concepts](https://docs.langchain4j.dev/tutorials/rag/#content-retriever)
- [Content Injection Strategies](https://docs.langchain4j.dev/tutorials/rag/#content-injector)

---

## Lab 5: Enabling on-demand context management for memories

### Learning objectives

By the end of this lab, you will:

- Implement long-term memory storage for user-specific information
- Enable users to explicitly store personal preferences and facts
- Use the LLM to route queries between knowledge base and user memories
- Integrate user memories with the RAG pipeline for personalized responses
- Test memory persistence across different chat sessions

**Estimated Time: 10 minutes**

### What you're building

In this lab, you'll add long-term memory capabilities that allow users to explicitly store personal information, preferences, and important facts that persist across sessions. This includes:

- **Long-term Memory Storage**: Persistent user-specific memories
- **Memory Management**: Ability to create and retrieve user memories
- **Personalized RAG**: Integrating user memories with knowledge retrieval

#### Architecture overview

![Lab 5 architecture with dual-layer memory (user memories and knowledge base)](/images/site-mirror/295313b92976fa2d0165435a7831876fe3aaa3a3-3277x1622.webp)

### Prerequisites check

Before starting, ensure you have:

- [ ] Completed Lab 4 successfully
- [ ] RAG pipeline working with knowledge base
- [ ] Redis Agent Memory running
- [ ] Basic chat memory functioning from Lab 2

### Setup instructions

#### Step 1: Switch to the lab 5 branch

```bash
git checkout lab-5-starter
```

#### Step 2: Review the memory service

Open `backend-layer/src/main/java/io/redis/devrel/workshop/services/MemoryService.java` and review the method to search long-term memories.

```java
public List<String> searchUserMemories(String userId, String memory) {
    var searchRequest = Map.of(
            "session_id", Map.of("eq", userId),
            "namespace", Map.of("any",
                    List.of(SHORT_TERM_MEMORY_NAMESPACE,
                            LONG_TERM_MEMORY_NAMESPACE)),
            "text", memory,
            "limit", 5
    );

    return extractTexts(executeSearch(searchRequest));
}
```

#### Step 3: Implement user memory retriever

Open `backend-layer/src/main/java/io/redis/devrel/workshop/memory/LongTermMemory.java` and implement the `getLongTermMemories()` method.

Change from this:

```java
private ContentRetriever getLongTermMemories(String userId) {
  // TODO: Implement a content retriever that fetches user-specific memories
    return null;
}
```

To this:

```java
private ContentRetriever getLongTermMemories(String userId) {
    return query -> memoryService.searchUserMemories(userId, query.text())
            .stream()
            .map(Content::from)
            .toList();
}
```

#### Step 4: Update the query router for dual memory

In the `getRetrievalAugmentor()` method, update the query router to include both knowledge base and user memories.

Change from this:

```java
QueryRouter queryRouter = null;
```

To this:

```java
Map<ContentRetriever, String> retrieversToDesc = Map.of(
        getLongTermMemories(userId), "User specific memories like preferences, events, and interactions",
        getGeneralKnowledgeBase(), "General knowledge base with facts and data from documents"
);

QueryRouter queryRouter = LanguageModelQueryRouter.builder()
        .chatModel(chatModel)
        .retrieverToDescription(retrieversToDesc)
        .fallbackStrategy(LanguageModelQueryRouter.FallbackStrategy.ROUTE_TO_ALL)
        .build();
```

#### Step 5: Add ChatModel parameter

Update the `getRetrievalAugmentor()` method signature to accept a ChatModel:

```java
@Bean
public RetrievalAugmentor getRetrievalAugmentor(ChatModel chatModel) {
    // Existing implementation with updated query router
}
```

#### Step 6: Rebuild and run the backend

```bash
cd backend-layer
mvn clean package
mvn spring-boot:run
```

#### Step 7: Keep the frontend running

The frontend should still be running. If not:

```bash
cd frontend-layer
npm start
```

### Testing your long-term memory

#### Store personal information

Use curl to store a new personal memory directly into the Redis Agent Memory:

```bash
curl -X POST http://localhost:8000/v1/long-term-memory/ \
  -H "Content-Type: application/json" \
  -d '{
    "memories": [
      {
        "id": "id-123456789",
        "session_id": "user-2bfc7e6e-452f-40d6-b7e7-29855518B052",
        "text": "My favorite programming language is Java",
        "namespace": "long-term-memory",
        "memory_type": "semantic"
      }
    ]
  }'
```

Alternatively, you can use the sample HTTP request available in the `rest-api-calls` folder. There are examples for IDEs (IntelliJ and VS Code) and Postman.

#### Test memory retrieval

1. Open http://localhost:3000 in your browser
2. Ask "Which programming language do I enjoy coding in?"
3. Verify the AI recalls "Java" from stored memory

![Chat showing stored long-term user memories](/images/site-mirror/631145dd8e42570ae93369030207edd28a277022-2028x1498.webp)

One interesting aspect of this lab is how the short-term chat memory (from Lab 2) and the long-term user memory (from this lab) work together. But you may notice that now the context provided to the LLM may be filled with multiple memories. For instance:

![Redis Insight showing multiple memories for context](/images/site-mirror/c35824f80c3cb075d984e30d0eba0f973e7b41c9-3024x1900.webp)

The LLM will then receive multiple memories in the context, which may be beneficial for answering more complex questions. But sometimes it may lead to a larger context filled with irrelevant data. Don't worry, we will fix this in the next lab.

#### Store multiple memories

Store various types of personal information:

```bash
# Store preference
curl -X POST http://localhost:8000/v1/long-term-memory/ \
  -H "Content-Type: application/json" \
  -d '{
    "memories": [
      {
        "id": "id-987654321",
        "session_id": "user-2bfc7e6e-452f-40d6-b7e7-29855518B052",
        "text": "I prefer black coffee with no milk or sugar",
        "namespace": "long-term-memory",
        "memory_type": "semantic"
      }
    ]
  }'

# Store personal fact
curl -X POST http://localhost:8000/v1/long-term-memory/ \
  -H "Content-Type: application/json" \
  -d '{
    "memories": [
      {
        "id": "id-112233445",
        "session_id": "user-2bfc7e6e-452f-40d6-b7e7-29855518B052",
        "text": "My birthday is on October 5th",
        "namespace": "long-term-memory",
        "memory_type": "semantic"
      }
    ]
  }'

# Store work information
curl -X POST http://localhost:8000/v1/long-term-memory/ \
  -H "Content-Type: application/json" \
  -d '{
    "memories": [
      {
        "id": "id-111222333",
        "session_id": "user-2bfc7e6e-452f-40d6-b7e7-29855518B052",
        "text": "I work as a software engineer at a startup",
        "namespace": "long-term-memory",
        "memory_type": "semantic"
      }
    ]
  }'
```

#### Test context combination

Ask questions that require both memories and knowledge base:

- "Based on what you know about me, what coffee would you recommend?"
- "Given my interests, what information from the documents might be relevant?"

![Chat showing memory retrieval by context](/images/site-mirror/50665ee30281e7423de7f8281c388ccbe0b9a97a-2028x1496.webp)

#### Verify memory persistence

1. Stop and restart the backend application
2. Ask about previously stored information
3. Confirm memories persist across sessions

### Understanding the code

#### 1. `MemoryService.searchUserMemories()`

- Searches user memories using semantic similarity
- Filters by user ID for privacy and isolation
- Returns relevant memories based on query
- Combines multiple memory types (preferences, facts, events)

#### 2. `LanguageModelQueryRouter`

- Intelligently routes queries to appropriate retrievers
- Uses LLM to determine if query needs user memory or knowledge
- Falls back to searching all sources when uncertain
- Provides descriptions to help routing decisions

#### 3. Dual-layer memory architecture

- Short-term: Recent conversation context (Lab 2)
- Long-term: Persistent user memories (this lab)
- Knowledge base: Document information (Lab 3-4)
- All layers work together for comprehensive context

### What's still missing? (Context engineering perspective)

Your application now has dual-layer memory, but still lacks:

- ❌ **No Query Compression**: Queries aren't optimized
- ❌ **No Content Reranking**: Retrieved content isn't prioritized
- ❌ **No Few-shot Learning**: No examples in prompts
- ❌ **No Token Management**: No handling of context limits

**Next labs will add these optimization features.**

### Lab 5 troubleshooting

**Memories not being stored**

Solution:

- Check Redis Agent Memory is running
- Verify the POST request format is correct
- Check if the `id` field is not being duplicated
- Ensure memory text is not empty

**AI doesn't recall stored memories**

Solution:

- Verify memories exist in Redis using Redis Insight
- Check the userId matches between storage and retrieval
- Ensure query router is properly configured
- Test with more specific memory-related questions

**Wrong retriever being used**

Solution:

- Check LanguageModelQueryRouter configuration
- Verify retriever descriptions are clear
- Review fallback strategy settings
- Monitor logs to see routing decisions

### Lab 5 completion

Congratulations. You've successfully:

- ✅ Implemented long-term user memory storage
- ✅ Enabled explicit memory management
- ✅ Integrated user memories with RAG pipeline
- ✅ Created a dual-layer memory architecture

### Additional resources

- [Query Routing Strategies](https://docs.langchain4j.dev/tutorials/rag/#query-router)
- [Content Aggregation Strategies](https://docs.langchain4j.dev/tutorials/rag/#content-aggregator)

---

## Lab 6: Implementing query compression and context reranking

### Learning objectives

By the end of this lab, you will:

- Implement query compression to optimize retrieval queries
- Configure content reranking to prioritize relevant information
- Set up ONNX scoring models for semantic similarity
- Reduce context noise by filtering low-relevance content
- Test the impact of compression and reranking on response quality

**Estimated Time: 15 minutes**

### What you're building

In this lab, you'll optimize the RAG pipeline by adding query compression and content reranking, ensuring that only the most relevant information reaches the LLM. This includes:

- **Query Compression**: Simplifying queries while preserving intent
- **Content Reranking**: Scoring and ordering retrieved content by relevance
- **ONNX Scoring Model**: Using pre-trained models for similarity scoring
- **Context Optimization**: Filtering out low-scoring content

#### Architecture overview

![Lab 6 architecture with query compression and reranking](/images/site-mirror/10d2acc10c10fa6c19e446fd54ea2d9cca65093c-3277x2195.webp)

### Prerequisites check

Before starting, ensure you have:

- [ ] Completed Lab 5 successfully
- [ ] Dual-layer memory working (short-term and long-term)
- [ ] RAG pipeline functioning with knowledge base
- [ ] Multiple memories and documents stored for testing

### Setup instructions

#### Step 1: Switch to the lab 6 branch

```bash
git checkout lab-6-starter
```

#### Step 2: Review the ModelManager configuration

Open `backend-layer/src/main/java/io/redis/devrel/workshop/config/ModelManager.java` and review how ONNX models are extracted and managed:

```java
@Configuration
public class ModelManager {

  private String modelPath;
  private String tokenizerPath;

  @PostConstruct
  public void extractModels() throws IOException {
    Path tempDir = Files.createTempDirectory("onnx-models");

    Path modelFile = tempDir.resolve("model.onnx");
    try (InputStream is = getClass().getClassLoader()
            .getResourceAsStream("ms-marco-MiniLM-L-6/model.onnx")) {
      Files.copy(is, modelFile);
    }

    Path tokenizerFile = tempDir.resolve("tokenizer.json");
    try (InputStream is = getClass().getClassLoader()
            .getResourceAsStream("ms-marco-MiniLM-L-6/tokenizer.json")) {
      Files.copy(is, tokenizerFile);
    }

    this.modelPath = modelFile.toAbsolutePath().toString();
    this.tokenizerPath = tokenizerFile.toAbsolutePath().toString();
  }

  public String getModelPath() {
    return modelPath;
  }

  public String getTokenizerPath() {
    return tokenizerPath;
  }
}
```

#### Step 3: Implement query compression

Open `backend-layer/src/main/java/io/redis/devrel/workshop/memory/LongTermMemory.java` and add query compression.

Change from this:

```java
QueryTransformer queryTransformer = null; // TODO: Add query compression
```

To this:

```java
QueryTransformer queryTransformer = new CompressingQueryTransformer(chatModel);
```

#### Step 4: Implement content reranking

Still in `LongTermMemory.java`, add the content aggregator with reranking.

Change from this:

```java
ContentAggregator contentAggregator = null; // TODO: Add content reranking
```

To this:

```java
ScoringModel scoringModel = new OnnxScoringModel(
        modelManager.getModelPath(),
        modelManager.getTokenizerPath()
);
ContentAggregator contentAggregator = ReRankingContentAggregator.builder()
        .scoringModel(scoringModel)
        .minScore(0.8)
        .build();
```

#### Step 5: Rebuild and run the backend

```bash
cd backend-layer
mvn clean package
mvn spring-boot:run
```

#### Step 6: Keep the frontend running

The frontend should still be running. If not:

```bash
cd frontend-layer
npm start
```

### Testing query compression and reranking

#### Test query compression

1. Open http://localhost:3000 in your browser
2. Ask a verbose question: "Can you please tell me what my favorite programming language is based on what you remember about me?"
3. Check the short-memory details using Redis Insight
4. Verify the response still uses the correct memory

![Chat showing compressed query and reranked results](/images/site-mirror/020dfeb7ffdc82c379547177390caa599c00f5ab-2022x1500.webp)

![Redis Insight showing short-term memory with reranked context](/images/site-mirror/ab382392c46164337578874f082e3744cae5d95c-3016x1902.webp)

#### Test content reranking

1. Ask a question that might retrieve multiple memories
2. Observe that only the most relevant content appears in the context
3. Check that low-relevance content is filtered out

Besides checking the context details using Redis Insight, you can use one of the HTTP requests available in the `rest-api-calls` folder. It will reproduce the same query sent to the Agent Memory, so you can have an idea about what context was retrieved, and how it compares to the one reranked.

### Understanding the code

#### 1. `CompressingQueryTransformer`

- Uses the ChatModel to simplify verbose queries
- Preserves query intent while removing redundancy
- Reduces tokens sent to retrieval system
- Improves retrieval accuracy with focused queries

#### 2. `OnnxScoringModel`

- Pre-trained model for semantic similarity scoring
- Compares query against retrieved content
- Provides relevance scores (0-1 range)
- Lightweight and fast for real-time scoring

#### 3. `ReRankingContentAggregator`

- Scores all retrieved content against the query
- Orders content by relevance score
- Filters out content below minimum threshold (0.8)
- Ensures only high-quality context reaches LLM

#### 4. Model files

- `model.onnx`: The scoring model weights
- `tokenizer.json`: Tokenization configuration
- Extracted to temp directory at startup
- MS MARCO MiniLM model for cross-encoder scoring

### What's still missing? (Context engineering perspective)

Your application now has optimized retrieval, but still lacks:

- ❌ **No Few-shot Learning**: No examples in prompts
- ❌ **No Token Management**: No handling of context limits
- ❌ **No Semantic Caching**: Redundant queries still hit LLM

**Next labs will add these final optimizations.**

### Lab 6 troubleshooting

**ONNX model loading fails**

Solution:

- Verify model files exist in resources folder
- Check temp directory permissions
- Ensure sufficient disk space for extraction
- Review ModelManager initialization logs

**All content filtered out (empty context)**

Solution:

- Lower the minScore threshold (try 0.6 or 0.7)
- Check if queries are too specific
- Verify content is being retrieved before reranking
- Test with more general queries

**Query compression removing important terms**

Solution:

- Check the ChatModel configuration
- Review compression prompts in logs
- Consider adjusting the CompressingQueryTransformer
- Test with simpler initial queries

### Lab 6 completion

Congratulations. You've successfully:

- ✅ Implemented query compression for optimized retrieval
- ✅ Added content reranking with ONNX scoring models
- ✅ Filtered low-relevance content from context
- ✅ Improved overall response quality and relevance

### Additional resources

- [Query Compression Techniques](https://docs.langchain4j.dev/tutorials/rag/#query-transformer)
- [ONNX Runtime docs](https://onnxruntime.ai/docs/)
- [MS MARCO Models](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L-6-v2)

---

## Lab 7: Implementing few-shot learning in system prompts

### Learning objectives

By the end of this lab, you will:

- Understand few-shot learning patterns for LLMs
- Implement example-based prompting in system messages
- Improve response consistency with structured examples
- Guide the AI's output format and style through demonstrations
- Test the impact of few-shot learning on response quality

**Estimated Time: 5 minutes**

### What you're building

In this lab, you'll enhance the system prompt with few-shot examples to guide the AI's responses more effectively. This includes:

- **Few-shot Examples**: Adding input-output pairs to demonstrate desired behavior
- **Format Consistency**: Ensuring responses follow a predictable structure
- **Context Handling**: Teaching the AI how to use retrieved context properly
- **Style Guidelines**: Establishing consistent tone and personality

#### Architecture overview

![Lab 7 architecture with few-shot examples in system prompt](/images/site-mirror/0c1164a612425c72c16f08bcf3ac555824a8b44e-3277x1773.webp)

### Prerequisites check

Before starting, ensure you have:

- [ ] Completed Lab 6 successfully
- [ ] Query compression and reranking working
- [ ] System prompt accessible in ChatController
- [ ] Test queries ready for comparison

### Setup instructions

#### Step 1: Switch to the lab 7 branch

```bash
git checkout lab-7-starter
```

#### Step 2: Review the current system prompt

Open `backend-layer/src/main/java/io/redis/devrel/workshop/controller/ChatController.java` and locate the `SYSTEM_PROMPT` constant:

```java
private static final String SYSTEM_PROMPT = """
            You are an AI assistant that should act, talk, and behave as if you were J.A.R.V.I.S AI
            from the Iron Man movies...
            """;
```

#### Step 3: Add few-shot examples to the system prompt

Replace the existing `SYSTEM_PROMPT` with an enhanced version that includes few-shot examples.

Change from the current prompt to:

```java
private static final String SYSTEM_PROMPT = """
            You are an AI assistant that should act, talk, and behave as if you were J.A.R.V.I.S AI
            from the Iron Man movies. Be formal but friendly, and add personality. You are going to
            be the brains behind this AI project. While providing answers, be informative but maintain
            the J.A.R.V.I.S personality.

            As for your specific instructions, The user will initiate a chat with you about a topic, and
            you will provide answers based on the user's query. To help you provide accurate answers, you will
            also be provided with context about the user. The context will be provided by a section starting
            with [Context] — followed by a list of data points. The data points will be structured in two sections:

            - Chat memory: everything the user has said so far during the conversation. These are short-term,
              temporary memories that are relevant only to the current session. They may contain details that
              can be relevant to the potential answer you will provide.

            - User memories: This will be a list of memories that the user asked to be stored, explicitely.
              They are long-term memories that persist across sessions. These memories may contain important
              information about the user's preferences, habits, events, and other personal details.

            IMPORTANT: You don't need to consider all data points while answering. Pick the ones that are
            relevant to the user's query and discard the rest. The context must be used to provide accurate
            answers. Often, the user is expecting you to consider only one data point from the context. Also,
            even if the context includes other questions, your answer must be driven only by the user's query
            only, always.

            Also, make sure to:

            1. Keep your answer concise with three sentences top. Avoid listing items and bullet points.
            2. Use gender-neutral language - avoid terms like 'sir' or 'madam'.
            3. When talking about dates, use the format Month Day, Year (e.g., January 1, 2020).

            Few-shot examples:

            [Example 1 - Using only relevant context]
            User: "What's my favorite color?"
            Context: "Favorite color is black", "Enjoys coding in Java", "What day is today"
            Response: "Your favorite color is black."

            [Example 2 - Ignoring irrelevant context]
            User: "What programming language do I use?"
            Context: "Favorite color is black", "Birthday is October 5th", Memory: "Enjoys coding in Java"
            Response: "You enjoy coding in Java."

            [Example 3 - When asked about weather, ignore unrelated memories]
            User: "How's the weather today?"
            Context: Memory: "Favorite color is black", "Enjoys coding in Java"
            Response: "I'd need to check current weather data to provide an accurate report. The memories available don't contain weather information."

            [Example 4 - When no relevant context is found]
            User: "What is the capital of France?"
            Context: "Enjoys coding in Java", Memory: "Favorite color is black"
            Response: "The capital of France is Paris. This is general knowledge not requiring personal context."

            [Example 5 - Combining multiple relevant memories]
            User: "Tell me about my work preferences"
            Context: "Works as software engineer", "Favorite language is Java", "Prefers remote work", "Birthday October 5th"
            Response: "You work as a software engineer with a preference for Java programming. You also prefer remote work arrangements."

            [Example 6 - Handling document knowledge]
            User: "What does the document say about garage door codes?"
            Context: Document: "The garage door code is 70170"
            Response: "According to the document, the garage door code is 70170."
            """;
```

#### Step 4: Rebuild and run the backend

```bash
cd backend-layer
mvn clean package
mvn spring-boot:run
```

#### Step 5: Keep the frontend running

The frontend should still be running. If not:

```bash
cd frontend-layer
npm start
```

### Testing few-shot learning impact

#### Test context selection

1. Open http://localhost:3000 in your browser
2. Test with queries that have mixed relevant/irrelevant context
3. Verify the AI focuses only on relevant information

Example test:

- Ask: "What's my favorite programming language?"
- The response should mention only Java, ignoring other stored memories

![Chat showing few-shot examples in system message](/images/site-mirror/8ad693b86821b9f2982610365fc5edde840b2251-2024x1500.webp)

As you can see, this is a very objective response. Even though the context created was this:

![Redis Insight comparison of context with few-shot examples applied](/images/site-mirror/3db3aa286bd6c7a18cb36094aacb01b5292f03fc-2938x1840.webp)

#### Test response conciseness

1. Ask questions that previously generated long responses
2. Verify responses now stay within 3 sentences
3. Check that responses maintain clarity despite brevity

#### Test edge cases

Test scenarios from the few-shot examples:

- Ask about information not in context (should acknowledge limitation)
- Ask about weather or current events (should explain lack of real-time data)
- Ask for multiple pieces of information (should combine relevant memories)

#### Compare before and after

Notice improvements in:

- **Consistency**: More predictable response format
- **Relevance**: Better focus on pertinent information
- **Brevity**: Shorter, more direct answers
- **Accuracy**: Improved context interpretation

### Understanding the code

#### 1. Few-shot learning pattern

- Provides concrete examples of desired behavior
- Shows input-output pairs for different scenarios
- Teaches context selection through demonstration
- Establishes response format expectations

#### 2. Example categories

- **Relevant context usage**: Shows how to use available information
- **Irrelevant context filtering**: Demonstrates ignoring noise
- **Missing information handling**: How to acknowledge limitations
- **Multiple context combination**: Merging related information

#### 3. Impact on AI behavior

- More consistent response structure
- Better context discrimination
- Improved handling of edge cases
- Maintained personality while following guidelines

#### 4. Prompt engineering best practices

- Clear instructions before examples
- Diverse example scenarios
- Consistent format across examples
- Balance between guidance and flexibility

### What's still missing? (Context engineering perspective)

Your application now has few-shot learning, but still lacks:

- ❌ **No Token Management**: No handling of context limits
- ❌ **No Semantic Caching**: Redundant queries still hit LLM

**Next labs will add these final optimizations.**

### Lab 7 troubleshooting

**AI not following few-shot examples**

Solution:

- Verify the system prompt is properly updated
- Check that examples are clear and consistent
- Ensure no conflicting instructions in the prompt
- Test with simpler queries first

**Responses too rigid or robotic**

Solution:

- Balance examples with personality instructions
- Don't over-constrain with too many examples
- Allow some flexibility in response format
- Maintain the J.A.R.V.I.S personality guidance

**Context still being misused**

Solution:

- Add more specific examples for your use case
- Make context labels clearer in examples
- Verify context is properly formatted
- Check RAG pipeline is working correctly

### Lab 7 completion

Congratulations. You've successfully:

- ✅ Implemented few-shot learning in system prompts
- ✅ Added concrete examples for better guidance
- ✅ Improved response consistency and relevance
- ✅ Enhanced context selection accuracy

### Additional resources

- [Few-shot Prompting Guide](https://www.promptingguide.ai/techniques/fewshot)
- [OpenAI Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)
- [In-context Learning Research](https://arxiv.org/abs/2005.14165)

---

## Lab 8: Enabling token management to handle token limits

### Learning objectives

By the end of this lab, you will:

- Implement token window management for context optimization
- Configure dynamic message pruning based on token limits
- Use OpenAI token count estimation for accurate measurement
- Handle long conversations within model constraints
- Test token overflow scenarios and automatic pruning

**Estimated Time: 10 minutes**

### What you're building

In this lab, you'll implement token management to ensure your application handles context window limits effectively, maintaining conversation quality even in lengthy exchanges. This includes:

- **Token Window Management**: Automatic pruning of older messages
- **Token Count Estimation**: Accurate measurement of context size
- **Dynamic Context Adjustment**: Keeping most relevant messages within limits
- **Overflow Handling**: Graceful degradation when approaching limits

#### Architecture overview

![Lab 8 architecture with token-based memory management](/images/site-mirror/9d042fc49357b427f9c2d560fb94083a5b9d9f8b-3277x2112.webp)

### Prerequisites check

Before starting, ensure you have:

- [ ] Completed Lab 7 successfully
- [ ] Few-shot learning system prompt in place
- [ ] Understanding of token limits (GPT-3.5: 4096 tokens)
- [ ] Redis Agent Memory running

### Setup instructions

#### Step 1: Switch to the lab 8 branch

```bash
git checkout lab-8-starter
```

#### Step 2: Review token configuration

Open `backend-layer/src/main/java/io/redis/devrel/workshop/memory/ShortTermMemory.java` and review the token-related configuration:

```java
@Value("${langchain4j.open-ai.streaming-chat-model.model-name}")
private String modelName;

@Value("${chat.memory.max.tokens}")
private int maxTokens;
```

#### Step 3: Implement token window chat memory

In `ShortTermMemory.java`, update the `chatMemory()` method to use token-based memory management.

Change from this:

```java
@Bean
public ChatMemory chatMemory(ChatMemoryStore chatMemoryStore) {
    return WorkingMemoryChat.builder()
            .id(userId)
            .chatMemoryStore(chatMemoryStore)
            .build();
}
```

To this:

```java
@Bean
public ChatMemory chatMemory(ChatMemoryStore chatMemoryStore) {
    return TokenWindowChatMemory.builder()
            .id(userId)
            .chatMemoryStore(chatMemoryStore)
            .maxTokens(maxTokens, new OpenAiTokenCountEstimator(modelName))
            .build();
}
```

#### Step 4: Configure token limits

Include the following property to your `.env` file:

```bash
CHAT_MEMORY_MAX_TOKENS=768
```

The `max-tokens` value of `768` is very low for production environments but is suitable for testing token management behavior. This will give you a good testing experience so you won't have to create lenghty conversations with the AI to see the message pruning in action.

#### Step 5: Rebuild and run the backend

```bash
cd backend-layer
mvn clean package
mvn spring-boot:run
```

#### Step 6: Keep the frontend running

The frontend should still be running. If not:

```bash
cd frontend-layer
npm start
```

### Testing token management

#### Test token window behavior

1. Open http://localhost:3000 in your browser
2. Have a long conversation (1-5 messages)
3. Notice older messages being automatically pruned
4. Verify recent context is preserved

Example long message test:

```text
Tell me everything you know about software engineering best practices,
including design patterns, testing strategies, deployment methods,
and team collaboration techniques. Be as detailed as possible.
```

![Chat interface demonstrating token window behavior](/images/site-mirror/66d300279f88d1d28e49c51e37c1915860f5fcd4-2022x1500.webp)

With Redis Insight, you will see a couple of messages there:

![Redis Insight view of token-managed chat memory](/images/site-mirror/8c36034bb5640bca2aeab91042c463fff514acb9-2934x1838.webp)

#### Verify context preservation

Using Redis Insight:

1. Check the working memory before token limit
2. Send more messages to exceed the limit
3. Verify older messages are removed
4. Confirm recent messages remain

#### Test with different token limits

Temporarily adjust `CHAT_MEMORY_MAX_TOKENS` in .env:

- Try 100 tokens (more aggressive pruning)
- Try 3000 tokens (less frequent pruning)
- Observe behavior differences

### Understanding the code

#### 1. `TokenWindowChatMemory`

- Maintains conversation within token limits
- Automatically removes oldest messages when limit approached
- Preserves most recent and relevant context
- Uses sliding window approach

#### 2. `OpenAiTokenCountEstimator`

- Accurately estimates tokens for OpenAI models
- Accounts for special tokens and formatting
- Model-specific tokenization rules
- Helps prevent context overflow

#### 3. Token budget allocation

- **System Prompt**: ~500 tokens (including few-shot)
- **Chat History**: 2000 tokens (configured limit)
- **Retrieved Context**: ~500 tokens (from RAG)
- **Response Space**: ~1000 tokens
- **Total**: Within 4096 token limit

#### 4. Pruning strategy

- First-In-First-Out (FIFO) approach
- Removes complete message pairs (user + assistant)
- Maintains conversation coherence
- Keeps most recent exchanges

### What's still missing? (Context engineering perspective)

Your application now has token management, but still lacks:

- ❌ **No Semantic Caching**: Redundant queries still hit LLM

**The final lab will add this last optimization.**

### Lab 8 troubleshooting

**Messages disappearing too quickly**

Solution:

- Increase max-tokens value in application.properties
- Check if messages are unusually long
- Verify token estimation is accurate
- Consider using a model with larger context window

**Token limit exceeded errors**

Solution:

- Reduce max-tokens to leave more buffer
- Check total of all token consumers
- Monitor actual token usage
- Adjust system prompt length if needed

**Conversation losing important context**

Solution:

- Store critical information in long-term memory
- Adjust token window size
- Consider message importance weighting
- Use summary techniques for older messages

### Lab 8 completion

Congratulations. You've successfully:

- ✅ Implemented token window management
- ✅ Configured automatic message pruning
- ✅ Added token count estimation
- ✅ Handled long conversations within limits

### Additional resources

- [Understanding Tokenization](https://platform.openai.com/tokenizer)
- [LangChain4J Memory Eviction Policy](https://docs.langchain4j.dev/tutorials/chat-memory#eviction-policy)
- [LLMs Context Windows](https://redis.io/blog/llm-context-windows/)

---

## Lab 9: Implementing semantic caching for conversations

### Learning objectives

By the end of this lab, you will:

- Set up Redis LangCache for semantic caching of LLM responses
- Implement cache lookup before making LLM calls
- Store AI responses with semantic similarity matching
- Reduce costs and latency through intelligent caching
- Measure cache hit rates and performance improvements

**Estimated Time: 25 minutes**

### What you're building

In this final lab, you'll implement semantic caching to avoid redundant LLM calls when users ask similar questions, significantly reducing costs and improving response times. This includes:

- **Redis LangCache Integration**: Cloud-based semantic caching service
- **Similarity Matching**: Finding cached responses for similar queries
- **Cache Management**: TTL-based expiration and user isolation
- **Performance Optimization**: Instant responses for cached queries

#### Architecture overview

![Lab 9 architecture with LangCache semantic search](/images/site-mirror/6306cfb4e17ae18cb1248b17c79bf9e932af4c1e-3277x2580.webp)

### Prerequisites check

Before starting, ensure you have:

- [ ] Completed Lab 8 successfully
- [ ] Token management configured and working
- [ ] Redis Cloud account (free tier is sufficient)
- [ ] Understanding of semantic similarity concepts

### Setup instructions

#### Step 1: Switch to the lab 9 branch

```bash
git checkout lab-9-starter
```

#### Step 2: Review the LangCacheService

Open `backend-layer/src/main/java/io/redis/devrel/workshop/services/LangCacheService.java` and review the caching methods:

```java
public class LangCacheService {
    // Stores new responses in cache
    public void addNewResponse(String prompt, String response) {...}

    // Searches for similar cached responses
    public Optional<String> searchForResponse(String prompt) {...}
}
```

Key configuration values:

- **TTL**: 60 seconds (for testing, production would be higher)
- **Similarity Threshold**: 0.7 (70% similarity required for cache hit)

#### Step 3: Create Redis LangCache service

1. Go to [Redis Cloud Console](https://cloud.redis.io)
2. Navigate to the LangCache section in the left menu
3. Create a new service with `Quick service creation`
4. Note down:
    - **Base URL**
    - **API Key**
    - **Cache ID**

#### Step 4: Configure LangCache properties

Add to your `.env` file:

```bash
REDIS_LANGCACHE_SERVICE_BASEURL=your-redis-langcache-service-baseurl
REDIS_LANGCACHE_SERVICE_APIKEY=your-api-key-here
REDIS_LANGCACHE_SERVICE_CACHEID=your-cache-id-here
```

#### Step 5: Implement cache check in ChatController

Open `backend-layer/src/main/java/io/redis/devrel/workshop/controller/ChatController.java` and update the `chat()` method.

Change from this:

```java
@GetMapping("/ai/chat/string")
public Flux<String> chat(@RequestParam("query") String query) {
    // TODO: Implement semantic caching with the LangCacheService
    return assistant.chat(SYSTEM_PROMPT, query);
}
```

To this:

```java
@GetMapping("/ai/chat/string")
public Flux<String> chat(@RequestParam("query") String query) {
    return langCacheService.searchForResponse(query)
            .map(Flux::just)
            .orElseGet(() -> assistant.chat(SYSTEM_PROMPT, query)
                    .collectList()
                    .map(responses -> String.join("", responses))
                    .doOnNext(response -> langCacheService.addNewResponse(query, response))
                    .flux()
            );
}
```

#### Step 6: Rebuild and run the backend

```bash
cd backend-layer
mvn clean package
mvn spring-boot:run
```

#### Step 7: Keep the frontend running

The frontend should still be running. If not:

```bash
cd frontend-layer
npm start
```

### Testing semantic caching

#### Test cache miss and store

1. Open http://localhost:3000 in your browser
2. Ask a unique question: "What is my favorite programming language?"
3. Note the response time (first call hits LLM)

![First query resulting in cache miss and LLM call](/images/site-mirror/9ca463c93201f2aee047613d24f1055ba05a3adf-2022x1500.webp)

#### Test exact match cache hit

1. Ask the exact same question: "What is my favorite programming language?"
2. Notice the instant response (now served from cache)

![Similar query resulting in cache hit and fast response](/images/site-mirror/4a80112784eb7085ac336e7ca16830a3060f15b1-2022x1496.webp)

#### Test semantic similarity

Test with similar but not identical queries:

**Original**: "What's my favorite programming language?"
**Variations to test**:

- "Which programming language do I prefer?"
- "Tell me my preferred coding language"
- "What language do I like to program in?"

![Another cache hit for semantically similar question](/images/site-mirror/6cb6a6a01f9ddad8537f64273224cbaf3f59c4cd-2018x1494.webp)

Each should return cached response if similarity > 70%

#### Test cache expiration

1. Ask a question and get a response
2. Wait 60+ seconds (TTL expiration)
3. Ask the same question again
4. Verify it hits the LLM again (cache expired)

#### Monitor cache performance

Using the `Metrics` tab of your LangCache service, observe these metrics:

- **Cache Hit Ratio**: Cache hits vs total requests
- **Cache Search Requests**: Number of cache lookups
- **Cache Latency**: Time taken for cache searches

![LangCache service metrics showing cache performance](/images/site-mirror/8c0e88a94f67755302acf443cb2bbb07a4fa66ed-2840x2188.webp)

### Understanding the code

#### 1. `LangCacheService`

- HTTP client for Redis LangCache API
- Semantic search using vector embeddings
- TTL-based automatic expiration

#### 2. Cache search process

- Converts query to embedding
- Searches for similar cached prompts
- Returns response if similarity > threshold
- Falls back to LLM if no match

#### 3. Cache storage process

- After LLM generates response
- Stores prompt-response pair
- Sets TTL for automatic cleanup

#### 4. Similarity threshold

- 0.7 (70%) - Good balance for testing
- Higher values = more exact matches required
- Lower values = more cache hits but less accuracy
- Production typically uses 0.8-0.9

### Performance impact

#### Before semantic caching

- Every query hits OpenAI API
- ~2-3 seconds response time
- ~$0.002 per query cost
- No redundancy optimization

#### After semantic caching

- Similar queries served from cache
- ~50ms response time for cache hits
- Zero cost for cached responses
- 40-60% typical cache hit rate

### Lab 9 troubleshooting

**Cache always misses**

Solution:

- Verify Redis LangCache credentials
- Check network connectivity to Redis Cloud
- Lower similarity threshold (try 0.6)
- Ensure cache ID is correct
- Check TTL hasn't expired

**Wrong responses from cache**

Solution:

- Increase similarity threshold (try 0.8 or 0.9)
- Clear cache and rebuild
- Verify user isolation is working
- Check cache entries in Redis Cloud console

**Cache service connection errors**

Solution:

- Verify API key and base URL
- Check Redis Cloud service status
- Review firewall/proxy settings
- Test with curl directly to API

### Lab 9 completion

Congratulations. You've successfully:

- ✅ Implemented semantic caching with Redis LangCache
- ✅ Reduced redundant LLM calls
- ✅ Improved response times dramatically
- ✅ Added cost optimization through caching

### Additional resources

- [What is Semantic Caching?](https://redis.io/blog/what-is-semantic-caching/)
- [Redis LangCache docs](https://redis.io/docs/latest/develop/ai/langcache/)
- [Vector search](https://redis.io/docs/latest/develop/ai/search-and-query/vectors/)

---

## Congratulations

You've successfully completed the Context Engineering Workshop for Java Developers and built a sophisticated AI application that demonstrates industry-leading practices in context management for Large Language Models (LLMs). This complete implementation showcases how to architect, optimize, and scale AI applications using Java, LangChain4J, and Redis.

### What you've built

#### Complete context engineering system

Your application now implements a comprehensive context engineering solution with:

![Complete context engineering workshop architecture overview](/images/site-mirror/c0f1bd30da8784e639dee4acb520f475bd3e9598-3015x2287.webp)

### Context engineering techniques implemented

#### 1. Memory architectures (Labs 2 & 5)

- **Technique**: Hierarchical Memory Systems
- **Implementation**: Dual-layer memory with short-term (conversation) and long-term (persistent) storage
- **Reference**: [Memory-Augmented Neural Networks](https://arxiv.org/abs/1410.3916)
- **Benefits**:
    - Maintains conversation coherence
    - Preserves user preferences across sessions
    - Enables personalized interactions

#### 2. Retrieval-augmented generation (RAG) (Labs 3 & 4)

- **Technique**: Dynamic Context Injection
- **Implementation**: Vector-based semantic search with document chunking
- **Reference**: [RAG: Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- **Benefits**:
    - Access to external knowledge
    - Reduced hallucination
    - Up-to-date information retrieval

#### 3. Query optimization (Lab 6)

- **Technique**: Query Compression and Expansion
- **Implementation**: LLM-based query reformulation for better retrieval
- **Reference**: [Query Expansion Techniques](https://dl.acm.org/doi/10.1145/3397271.3401075)
- **Benefits**:
    - Improved retrieval accuracy
    - Reduced noise in search results
    - Better semantic matching

#### 4. Content reranking (Lab 6)

- **Technique**: Cross-Encoder Reranking
- **Implementation**: ONNX-based similarity scoring with MS MARCO models
- **Reference**: [Dense Passage Retrieval](https://arxiv.org/abs/2004.04906)
- **Benefits**:
    - Higher relevance in retrieved content
    - Reduced context pollution
    - Better answer quality

#### 5. Few-shot learning (Lab 7)

- **Technique**: In-Context Learning (ICL)
- **Implementation**: Example-based prompting in system messages
- **Reference**: [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165)
- **Benefits**:
    - Consistent output format
    - Better instruction following
    - Reduced prompt engineering effort

#### 6. Token management (Lab 8)

- **Technique**: Sliding Window Attention
- **Implementation**: Dynamic pruning with token count estimation
- **Reference**: [Efficient Transformers](https://arxiv.org/abs/2009.06732)
- **Benefits**:
    - Prevents context overflow
    - Maintains conversation flow
    - Optimizes token usage

#### 7. Semantic caching (Lab 9)

- **Technique**: Vector Similarity Caching
- **Implementation**: Redis LangCache with embedding-based matching
- **Reference**: [Semantic Caching for LLMs](https://arxiv.org/html/2504.02268v1)
- **Benefits**:
    - 40-60% reduction in LLM calls
    - Sub-100ms response times for cached queries
    - Significant cost savings

### Technology stack mastered

#### Core technologies

- **Java 21**: Modern Java with virtual threads and records
- **Spring Boot 3.x**: Reactive programming with WebFlux
- **LangChain4J**: Comprehensive LLM orchestration

#### AI/ML components

- **OpenAI GPT-3.5/4**: Large language model integration
- **ONNX Runtime**: Cross-platform model inference
- **Vector Embeddings**: Semantic similarity search
- **MS MARCO**: State-of-the-art reranking models

#### Infrastructure

- **Docker**: Containerized deployment
- **Redis Cloud**: Semantic caching via LangCache service
- **Agent Memory**: Distributed memory management

### Advanced concepts learned

1. **Context Window Optimization**: Balancing information density with token limits
2. **Semantic Similarity**: Understanding and implementing vector-based search
3. **Prompt Engineering**: Crafting effective system prompts with examples
4. **Memory Hierarchies**: Designing multi-tier memory systems
5. **Query Understanding**: Reformulating user intent for better retrieval
6. **Cache Strategies**: Implementing intelligent caching with semantic matching
7. **Token Economics**: Optimizing cost vs. performance in LLM applications

### Next steps for your journey

#### Continue learning with Redis tutorials

- [Java getting-started tutorial](/tutorials/develop/java/getting-started/) — deepen your Redis + Java fundamentals
- [Build an AI-powered chatbot](/tutorials/howtos/solutions/vector/gen-ai-chatbot/) — explore a complementary RAG architecture with Redis vector search

#### Immediate enhancements

**1. Implement Conversation Summarization**

```java
// Add conversation summary when token limit approached
public String summarizeConversation(List<ChatMessage> messages) {
    // Use LLM to create concise summary
    // Store as long-term memory
    // Clear short-term memory
}
```

**2. Add Multi-Modal Support**

- Integrate image processing with LangChain4J
- Add support for PDF charts and diagrams
- Implement audio transcription for voice queries

**3. Enhance Memory Management**

- Implement memory importance scoring
- Add memory consolidation strategies
- Create user-controlled memory editing

#### Advanced features

**1. Implement Agents and Tools**

```java
@Tool("Search the web for current information")
public String webSearch(String query) {
    // Integrate with search APIs
    // Add to context dynamically
}

@Tool("Execute calculations")
public String calculate(String expression) {
    // Math expression evaluation
    // Return formatted results
}
```

**2. Implement Hybrid Search**

- Combine vector search with keyword search
- Add metadata filtering for better precision
- Implement BM25 + dense retrieval fusion

#### Production considerations

**1. RAG Observability and Monitoring**

```java
public class MyEmbeddingModelListener implements EmbeddingModelListener {

    @Override
    public void onRequest(EmbeddingModelRequestContext requestContext) {
        requestContext.attributes().put("startNanos", System.nanoTime());
    }

    @Override
    public void onResponse(EmbeddingModelResponseContext responseContext) {
        long startNanos = (long) responseContext.attributes().get("startNanos");
        long durationNanos = System.nanoTime() - startNanos;
        // Do something with duration and/or responseContext.response()
    }

    @Override
    public void onError(EmbeddingModelErrorContext errorContext) {
        // Do something with errorContext.error()
    }
}
```

LangChain4J provides a comprehensive [observability framework](https://docs.langchain4j.dev/tutorials/observability) to monitor LLM and embedding model calls.

**2. Security and Privacy**

- Implement PII detection and masking
- Add conversation encryption
- Create audit logs for compliance
- Implement user consent management

**3. Scale and Performance**

- Implement distributed caching with Redis Cluster
- Add connection pooling for LLM calls
- Use async processing for document ingestion
- Implement circuit breakers for resilience

### Learning resources

#### Research papers

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [BERT: Pre-training of Deep Bidirectional Transformers](https://arxiv.org/abs/1810.04805)
- [Constitutional AI](https://arxiv.org/abs/2212.08073)

#### Online courses

- [CS324 - Large Language Models (Stanford)](https://stanford-cs324.github.io/winter2022/)
- [Full Stack LLM Bootcamp](https://fullstackdeeplearning.com/llm-bootcamp/)
- [Semantic Caching for AI Agents](https://www.deeplearning.ai/short-courses/semantic-caching-for-ai-agents/)

### Community and contribution

#### Join the community

- [LangChain4J Discord](https://discord.com/invite/JzTFvyjG6R)
- [Redis Developer Community](https://discord.gg/redis)

#### Contribute back

- Share your improvements as PRs
- Write blog posts about your learnings
- Create video tutorials
- Help others in community forums

### Certification of completion

You've demonstrated proficiency in:

- ✅ Context Window Management
- ✅ Memory System Architecture
- ✅ Retrieval-Augmented Generation
- ✅ Query Optimization Techniques
- ✅ Semantic Caching Strategies
- ✅ Token Economics and Management
- ✅ Production-Ready AI Applications

### Acknowledgments

This workshop was made possible by:

- The LangChain4J community
- Redis Developer Relations team
- All workshop participants and contributors

### Feedback and support

- **Workshop Issues**: [GitHub Issues](https://github.com/redis-developer/context-engineering-workshop-java/issues)
- **Improvements**: PRs are welcome.

---

**Thank you for joining us on this context engineering journey.**

You're now equipped with the knowledge and tools to build sophisticated, production-ready AI applications. The future of context-aware AI is in your hands. Go forth and build amazing things.

---
