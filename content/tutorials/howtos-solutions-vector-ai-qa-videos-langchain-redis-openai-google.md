---
title: "Building an AI-Powered Video Q&A Application with Vector Search, Redis and LangChain"
linkTitle: "Building an AI-Powered Video Q&A Application with Vector Search, Redis and LangChain"
url: "/tutorials/howtos/solutions/vector/ai-qa-videos-langchain-redis-openai-google/"
description: "In this tutorial you will build an AI-powered Q&A engine that lets users ask natural-language questions about video content. Along the way you will learn how to:"
group: "For AI"
aliases:
- "/tutorials/howtos-solutions-vector-ai-qa-videos-langchain-redis-openai-google/"
date: 2026-02-25
lastmod: 2026-03-20
hidden: true
---

*Published 25 February 2026 · updated 20 March 2026*

> **TL;DR:**
>
> To build a Q&A system for video content, transcribe videos using the YouTube Data API, summarize transcripts with an LLM (OpenAI or Google Gemini) via LangChain, generate vector embeddings of those summaries, and store them in Redis. When a user asks a question, convert it to a vector, perform a similarity search in Redis, and pass the matching video context to the LLM to generate an answer. Use Redis as a semantic vector cache to avoid redundant LLM calls for similar questions.

## What you'll learn

In this tutorial you will build an AI-powered Q&A engine that lets users ask natural-language questions about video content. Along the way you will learn how to:

- Retrieve and transcribe YouTube videos using the YouTube Data API and SearchAPI.io
- Summarize transcripts and generate sample questions with OpenAI ChatGPT or Google Gemini through LangChain
- Generate vector embeddings and store them in Redis for fast similarity search
- Build a search pipeline that converts user questions into vectors and finds relevant videos
- Implement semantic vector caching in Redis to avoid redundant LLM calls and speed up responses

> **GITHUB CODE**
>
> Below is a command to the clone the source code for the application used in this tutorial
> `git clone https://github.com/redis-developer/video-qa-semantic-vector-caching`

## What concepts do you need to understand before building a GenAI video Q&A app?

Before we dive into the details of this tutorial, let's go over a few concepts that are important to understand when building GenAI apps.

1.  **GenAI** is a rapidly evolving field that focuses on creating content, whether it's text, images, or even video. It leverages deep learning techniques to generate new, unique outputs based on learned patterns and data.
2.  **Retrieval-Augmented Generation (RAG)** combines generative models with external knowledge sources to provide more accurate and informed responses. This technique is particularly useful in apps where context-specific information is critical.
3.  [**LangChain**](https://www.langchain.com/) is a powerful library that facilitates the development of apps involving language models. It simplifies tasks such as summarization, question answering, and interaction with generative models like ChatGPT or Google Gemini.
4.  **Google Gemini** and **OpenAI/ChatGPT** are generative models that can be used to generate text based on a given prompt. They are useful for apps that require a large amount of text generation, such as summarization or question answering.
5.  **Vector search** is a technique that uses vector embeddings to find similar items in a database. It is typically combined with RAG to provide more accurate responses to user queries.
6.  **Redis** is an in-memory database that can be used to store and search vector embeddings. It is particularly useful for apps that require fast responses.

Our app leverages these technologies to create a unique Q&A platform based on video content. Users can upload YouTube video URLs or IDs, and the app utilizes GenAI to summarize these videos, formulate potential questions, and create a searchable database. This database can then be queried to find answers to user-submitted questions, drawing directly from the video content.

If you're new to vector search with Redis, start with [Perform vector search using Redis](/tutorials/howtos/solutions/vector/getting-started-vector). For a text-focused RAG approach, see [Semantic text search with Redis](/tutorials/howtos/solutions/vector/semantic-text-search) or [Building a GenAI chatbot using Redis](/tutorials/howtos/solutions/vector/gen-ai-chatbot).

## How does the AI video Q&A app work at a high level?

Here's how our app uses AI and vector search to answer user questions based on video content:

1. **Uploading videos**: Users can upload YouTube videos either via links (e.g. `https://www.youtube.com/watch?v=LaiQFZ5bXaM`) or video IDs (e.g. `LaiQFZ5bXaM`). The application processes these inputs to retrieve necessary video information. For the purposes of this tutorial, the app is pre-seeded with a collection of videos from the [Redis YouTube channel](https://www.youtube.com/@Redisinc). However, when you run the application you can adjust it to cover your own set of videos.

![Video Q&A app upload form where users paste a YouTube URL or video ID to transcribe and index content in Redis](images/inline-1-aeaac3669030a208cae92cbd9858e7eb8d85c784-919x312.jpg)

1. **Video processing and AI interaction**: Using the [Youtube Data API](https://developers.google.com/youtube/v3), the application obtains video titles, descriptions, and thumbnails. It also uses [SearchAPI.io](https://searchapi.io/) to retrieve video transcripts. These transcripts are then passed to a large language model (LLM) - either Google Gemini or OpenAI's ChatGPT - for summarization and sample question generation. The LLM also generates vector embeddings for these summaries.

An example summary and sample questions generated by the LLM are shown below:

```text
Summary:
The video provides a walkthrough of building a real-time stock tracking application
using Redis, demonstrating its capability to handle multiple data models and
act as a message broker in a single integrated database. The application maintains
a watch list of stock symbols, along with real-time trading information and a chart
updated with live data from the Alpaca API. The presenter uses Redis features
such as sets, JSON documents, time series, Pub/Sub, and Top-K filter to store and
manage different types of data. An architecture diagram is provided, explaining the
interconnection between the front end, API service, and streaming service within
the application. Code snippets highlight key aspects of the API and streaming
service written in Python, highlighting the use of Redis Bloom, Redis JSON, Redis
Time Series, and Redis Search for managing data. The video concludes with a
demonstration of how data structures are visualized and managed in Redis Insight,
emphasizing how Redis can simplify the building of a complex real-time
application by replacing multiple traditional technologies with one solution.

Example Questions and Answers:

Q1: What is Redis and what role does it play in the application?
Q2: How is the stock watch list stored and managed within the application?
Q3: What type of data does the application store using time series capabilities of
Redis?
Q4: Can you explain the use of the Top-K filter in the application?
Q5: What methods are used to update the front end with real-time information in
the application?
Q6: How does the application sync the watch list with the streaming service?
Q7: What frontend technologies are mentioned for building the UI of the application?
Q8: How does Redis Insight help in managing the application data?
```

1. **Data storage with Redis**: All generated data, including video summaries, potential questions, and vector embeddings, are stored in Redis. The app utilizes Redis's diverse data types for efficient data handling, caching, and quick retrieval.

![Redis Insight showing stored video summaries, sample questions, and vector embeddings used for similarity search](images/inline-2-597682be14cbe0f672f89df90be50da2e1ff401d-1622x801.jpg)

1. **Search and answer retrieval**: The frontend, built with Next.js, allows users to ask questions. The application then searches the Redis database using semantic vector similarity to find relevant video content. It further uses the LLM to formulate answers, prioritizing information from video transcripts.

![Search bar where users type natural-language questions that are converted to vectors and matched against video content in Redis](images/inline-3-ad485885929706aa3894efbebfb23b47c80f4ed3-1061x389.jpg)

1. **Presentation of results**: The app displays the most relevant videos along with the AI-generated answers, offering a comprehensive and interactive user experience. It also displays cached results from previous queries using vector caching for fast response times.

![Video Q&A results dashboard showing an AI-generated answer alongside the most relevant YouTube video clips found via Redis vector search](images/inline-4-523089fd6eeaa3c67f6508af2c3ace0c2a19cebf-2000x855.jpg)

## How do you set up the development environment?

To get started with our AI-powered video Q&A application, you'll first need to set up your development environment. We'll follow the instructions outlined in the project's `README.md` file.

### Requirements

- [Node.js](https://nodejs.org/)
- [Docker](https://www.docker.com/)
- [SearchAPI.io API Key](https://www.searchapi.io/)
- This is used to retrieve video transcripts and free for up to 100 requests. The application will cache the results to help avoid exceeding the free tier.
- [Google API Key](https://console.cloud.google.com/apis/credentials)
- You must have the following APIs enabled:
- YouTube Data API v3
- Generative Language API
- This is used to retrieve video information and prompt the Google Gemini model. This is not free.
- [OpenAI API Key](https://platform.openai.com/api-keys)
- This is used to prompt the OpenAI ChatGPT model. This is not free.

## How do you set up Redis for vector storage?

Redis is used as our database to store and retrieve data efficiently. You can start quickly with a cloud-hosted Redis instance by signing up at [redis.io/try-free](https://redis.io/try-free/). This is ideal for both development and testing purposes. You can easily store the data for this application within the limitations of the Redis free tier.

### Cloning the Repository

First, clone the repository containing our project:

```bash
git clone https://github.com/redis-developer/video-qa-semantic-vector-caching
```

### Installing Dependencies

After setting up your Node.js environment, you'll need to install the necessary packages. Navigate to the root of your project directory and run the following command:

```bash
npm install
```

This command will install all the dependencies listed in the `package.json` file, ensuring you have everything needed to run the application.

### Configuration

Before running the application, make sure to configure the environment variables. There is a script to automatically generate the `.env` files for you. Run the following command:

```bash
npm run setup
```

This will generate the following files:

1.  `app/.env` - This file contains the environment variables for the Next.js application.
2.  `app/.env.docker` - This file contains overrides for the environment variables when running in Docker.
3.  `services/video-search/.env` - This file contains the environment variables for the video search service.
4.  `services/video-search/.env.docker` - This file contains overrides for the environment variables when running in Docker.

By default, you should not need to touch the environment files in the `app`. However, you will need to configure the environment files in the `services/video-search` directory.

The `services/video-search/.env` looks like this:

```bash
USE=<HF|OPENAI>

REDIS_URL=<redis[s]://[[username][:password]@][host][:port][/db-number]>
SEARCHAPI_API_KEY=<https://www.searchapi.io/>
YOUTUBE_TRANSCRIPT_PREFIX=<redis-transcript-prefix>
YOUTUBE_VIDEO_INFO_PREFIX=<redis-video-info-prefix>

GOOGLE_API_KEY=<https://console.cloud.google.com/apis/credentials>
GOOGLE_EMBEDDING_MODEL=<https://ai.google.dev/models/gemini#model_variations>
GOOGLE_SUMMARY_MODEL=<https://ai.google.dev/models/gemini#model_variations>

OPENAI_API_KEY=<https://platform.openai.com/api-keys>
OPENAI_ORGANIZATION=<https://platform.openai.com/account/organization>
OPENAI_EMBEDDING_MODEL=<https://platform.openai.com/account/limits>
OPENAI_SUMMARY_MODEL=<https://platform.openai.com/account/limits>
```

For Gemini models, you can use the following if you are not sure what to do:

```bash
GOOGLE_EMBEDDING_MODEL=embedding-001
GOOGLE_SUMMARY_MODEL=gemini-pro
```

For OpenAI models, you can use the following if you are not sure what to do:

```bash
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
OPENAI_SUMMARY_MODEL=gpt-4-1106-preview
```

NOTE: Depending on your OpenAI tier you may have to use a different summary model. `gpt-3.5` models will be okay.

The `_PREFIX` environment variables are used to prefix the keys in Redis. This is useful if you want to use the same Redis instance for multiple apps. They have the following defaults:

```bash
YOUTUBE_TRANSCRIPT_PREFIX=transcripts:
YOUTUBE_VIDEO_INFO_PREFIX=yt-videos:
```

If you're satisfied with the defaults, you can delete these values from the `.env` file.

Lastly, the `services/video-search/.env.docker` file contains overrides for the Redis URL when used in Docker. By default this app sets up a local Redis instance in Docker. If you are using a cloud instance, you can simply add the URL to your `.env` and delete the override in the `.env.docker` file.

## How do you run the video Q&A application?

After installing and configuring the application, run the following command to build the Docker images and run containers:

```bash
npm run dev
```

This command builds the app and the video service, and deploys them to Docker. It is all setup for hot reloading, so if you make changes to the code, it will automatically restart the servers.

Once the containers are up and running, the application will be accessible via your web browser:

- **Client**: Available at [http://localhost](http://localhost/) (Port 80).
- **Video search service**: Accessible at [http://localhost:8000](http://localhost:8000/api/healthcheck).

This setup allows you to interact with the client-side application through your browser and make requests to the video search service hosted on a separate port.

The video search service doesn't publish a client application. Instead, it exposes a REST API that can be used to interact with the service. You can validate that it is running by checking Docker or by visiting the following URL:

- [http://localhost:8000/api/healthcheck](http://localhost:8000/api/healthcheck)

You should be up and running now! The rest of this tutorial is focused on how the application works and how to use it, with code examples.

## How do you build a video Q&A application with Redis and LangChain?

### How are video uploads processed?

#### How do you retrieve video transcripts and metadata?

The backend is set up to handle YouTube video links or IDs. The relevant code snippet from the project demonstrates how these inputs are processed.

```js
export type VideoDocument = Document<{
  id: string;
  link: string;
  title: string;
  description: string;
  thumbnail: string;
}>;

export async function load(videos: string[] = config.youtube.VIDEOS) {
  // Parse the video URLs to get a list of video IDs
  const videosToLoad: string[] = videos.map(parseVideoUrl).filter((video) => {
    return typeof video === "string";
  }) as string[];

  // Get video title, description, and thumbnail from YouTube API v3
  const videoInfo = await getVideoInfo(videosToLoad);

  // Get video transcripts from SearchAPI.io, join the video info
  const transcripts = await mapAsyncInOrder(videosToLoad, async (video) => {
    return await getTranscript(video, videoInfo[video]);
  });

  // Return the videos as documents with metadata, and pageContent being the transcript
  return transcripts.filter(
    (transcript) => typeof transcript !== "undefined"
  ) as VideoDocument[];
}
```

In the same file you will see two caches:

```js
const cache = cacheAside(config.youtube.TRANSCRIPT_PREFIX);
const videoCache =
    jsonCacheAside < VideoInfo > config.youtube.VIDEO_INFO_PREFIX;
```

These caches are used to store the transcripts (as a `string`) and video metadata (as `JSON`) in Redis. The `cache` functions are helper functions that use Redis to store and retrieve data. They looks like this:

```js
export function cacheAside(prefix: string) {
  return {
    get: async (key: string) => {
      return await client.get(`${prefix}${key}`);
    },
    set: async (key: string, value: string) => {
      return await client.set(`${prefix}${key}`, value);
    },
  };
}

export function jsonCacheAside<T>(prefix: string) {
  return {
    get: async (key: string): Promise<T | undefined> => {
      return client.json.get(`${prefix}${key}`) as T;
    },
    set: async (key: string, value: RedisJSON) => {
      return await client.json.set(`${prefix}${key}`, "$", value);
    },
  };
}
```

You will see these functions used elsewhere in the app. They are used to prevent unnecessary API calls, in this case to SearchAPI.io and the YouTube API.

#### How do you summarize video content with LangChain and an LLM?

After obtaining the video transcripts and metadata, the transcripts are then summarized using LangChain and the LLMs, both Gemini and ChatGPT. There are a few interesting pieces of code to understand here:

1.  The `prompt` used to ask the LLM to summarize the video transcript and generate sample questions
2.  The `refinement chain` used to obtain the summarized video and sample questions
3.  The `vector embedding chain` that uses the LLM to generate text embeddings and store them in Redis

The LLM `summary prompt` is split into two parts. This is done to allow analyzing videos where the transcript length is larger than the LLM's accepted context.

```js
import { PromptTemplate } from 'langchain/prompts';

const summaryTemplate = `
You are an expert in summarizing YouTube videos.
Your goal is to create a summary of a video.
Below you find the transcript of a video:
--------
{text}
--------

The transcript of the video will also be used as the basis for a question and answer bot.
Provide some examples questions and answers that could be asked about the video. Make these questions very specific.

Total output will be a summary of the video and a list of example questions the user could ask of the video.

SUMMARY AND QUESTIONS:
`;

export const SUMMARY_PROMPT = PromptTemplate.fromTemplate(summaryTemplate);

const summaryRefineTemplate = `
You are an expert in summarizing YouTube videos.
Your goal is to create a summary of a video.
We have provided an existing summary up to a certain point: {existing_answer}

Below you find the transcript of a video:
--------
{text}
--------

Given the new context, refine the summary and example questions.
The transcript of the video will also be used as the basis for a question and answer bot.
Provide some examples questions and answers that could be asked about the video. Make
these questions very specific.
If the context isn't useful, return the original summary and questions.
Total output will be a summary of the video and a list of example questions the user could ask of the video.

SUMMARY AND QUESTIONS:
`;

export const SUMMARY_REFINE_PROMPT = PromptTemplate.fromTemplate(
    summaryRefineTemplate,
);
```

The `summary prompts` are used to create a `refinement chain` with LangChain. LangChain will automatically handle splitting the video transcript document(s) and calling the LLM accordingly.

```js
const videoSummarizeChain = loadSummarizationChain(llm, {
  type: "refine",
  questionPrompt: SUMMARY_PROMPT,
  refinePrompt: SUMMARY_REFINE_PROMPT,
});

const summaryCache = cacheAside(`${prefix}-${config.redis.SUMMARY_PREFIX}`);

async function summarizeVideos(videos: VideoDocument[]) {
  const summarizedDocs: VideoDocument[] = [];

  for (const video of videos) {
    log.debug(`Summarizing ${video.metadata.link}`, {
      ...video.metadata,
      location: `${prefix}.summarize.docs`,
    });
    const existingSummary = await summaryCache.get(video.metadata.id);

    if (typeof existingSummary === "string") {
      summarizedDocs.push(
        new Document({
          metadata: video.metadata,
          pageContent: existingSummary,
        })
      );

      continue;
    }

    const splitter = new TokenTextSplitter({
      chunkSize: 10000,
      chunkOverlap: 250,
    });
    const docsSummary = await splitter.splitDocuments([video]);
    const summary = await videoSummarizeChain.run(docsSummary);

    log.debug(`Summarized ${video.metadata.link}:\n ${summary}`, {
      summary,
      location: `${prefix}.summarize.docs`,
    });
    await summaryCache.set(video.metadata.id, summary);

    summarizedDocs.push(
      new Document({
        metadata: video.metadata,
        pageContent: summary,
      })
    );
  }

  return summarizedDocs;
}
```

Notice the `summaryCache` is used to first ask Redis if the video has already been summarized. If it has, it will return the summary and skip the LLM. This is a great example of how Redis can be used to cache data and avoid unnecessary API calls. Below is an example video summary with questions.

```text
Summary:
The video provides a walkthrough of building a real-time stock tracking application
using Redis, demonstrating its capability to handle multiple data models and
act as a message broker in a single integrated database. The application maintains
a watch list of stock symbols, along with real-time trading information and a chart
updated with live data from the Alpaca API. The presenter uses Redis features
such as sets, JSON documents, time series, Pub/Sub, and Top-K filter to store and
manage different types of data. An architecture diagram is provided, explaining the
interconnection between the front end, API service, and streaming service within
the application. Code snippets highlight key aspects of the API and streaming
service written in Python, highlighting the use of Redis Bloom, Redis JSON, Redis
Time Series, and Redis Search for managing data. The video concludes with a
demonstration of how data structures are visualized and managed in Redis Insight,
emphasizing how Redis can simplify the building of a complex real-time
application by replacing multiple traditional technologies with one solution.

Example Questions and Answers:

Q1: What is Redis and what role does it play in the application?
Q2: How is the stock watch list stored and managed within the application?
Q3: What type of data does the application store using time series capabilities of
Redis?
Q4: Can you explain the use of the Top-K filter in the application?
Q5: What methods are used to update the front end with real-time information in
the application?
Q6: How does the application sync the watch list with the streaming service?
Q7: What frontend technologies are mentioned for building the UI of the application?
Q8: How does Redis Insight help in managing the application data?
```

The `vector embedding chain` is used to generate vector embeddings for the video summaries. This is done by asking the LLM to generate text embeddings for the summary. The `vector embedding chain` is defined as follows:

```js
const vectorStore = new RedisVectorStore(embeddings, {
    redisClient: client,
    indexName: `${prefix}-${config.redis.VIDEO_INDEX_NAME}`,
    keyPrefix: `${prefix}-${config.redis.VIDEO_PREFIX}`,
    indexOptions: {
        ALGORITHM: VectorAlgorithms.HNSW,
        DISTANCE_METRIC: 'IP',
    },
});
```

The vector store uses the `RedisVectorStore` class from LangChain. This class is a wrapper around Redis that allows you to store and search vector embeddings. We are using the `HNSW` algorithm and the `IP` distance metric. For more information on the supported algorithms and distance metrics, see the [Redis vector store docs](https://redis.io/docs/latest/develop/ai/search-and-query/advanced-concepts/vectors/). We pass the `embeddings` object to the `RedisVectorStore` constructor. This object is defined as follows:

```js
new GoogleGenerativeAIEmbeddings({
    apiKey: config.google.API_KEY,
    modelName: modelName ?? config.google.EMBEDDING_MODEL,
    taskType: TaskType.SEMANTIC_SIMILARITY,
});
```

Or for OpenAI:

```js
new OpenAIEmbeddings({
    openAIApiKey: config.openai.API_KEY,
    modelName: modelName ?? config.openai.EMBEDDING_MODEL,
    configuration: {
        organization: config.openai.ORGANIZATION,
    },
});
```

The `embeddings` object is used to generate vector embeddings for the video summaries. These embeddings are then stored in Redis using the `vectorStore`.

```js
async function storeVideoVectors(documents: VideoDocument[]) {
  log.debug("Storing documents...", {
    location: `${prefix}.store.store`,
  });
  const newDocuments: VideoDocument[] = [];

  await Promise.all(
    documents.map(async (doc) => {
      const exists = await client.sIsMember(
        `${prefix}-${config.redis.VECTOR_SET}`,
        doc.metadata.id
      );

      if (!exists) {
        newDocuments.push(doc);
      }
    })
  );

  log.debug(`Found ${newDocuments.length} new documents`, {
    location: `${prefix}.store.store`,
  });

  if (newDocuments.length === 0) {
    return;
  }

  await vectorStore.addDocuments(newDocuments);

  await Promise.all(
    newDocuments.map(async (doc) => {
      await client.sAdd(
        `${prefix}-${config.redis.VECTOR_SET}`,
        doc.metadata.id
      );
    })
  );
}
```

Notice that we first check if we have already generated a vector using the Redis Set `VECTOR_SET`. If we have, we skip the LLM and use the existing vector. This avoids unnecessary API calls and can speed things up.

### How does Redis vector search power the video Q&A?

One of the key features of our application is the ability to search through video content using AI-generated queries. This section will cover how the backend handles search requests and interacts with the AI models.

#### How are user questions converted into vectors and matched to videos?

When a user submits a question through the frontend, the backend performs the following steps to obtain the answer to the question as well as supporting videos:

1.  We generate a semantically similar question to the one being asked. This helps to find the most relevant videos.
2.  We then use the `vectorStore` to search for the most relevant videos based on the semantic question.
3.  If we don't find any relevant videos, we search with the original question.
4.  Once we find videos, we call the LLM to answer the question.
5.  Finally, we return the answer and supporting videos to the user.

To answer a question, we first generate a semantically similar question to the one being asked. This is done using the `QUESTION_PROMPT` defined below:

```js
import { PromptTemplate } from 'langchain/prompts';

const questionTemplate = `
You are an expert in summarizing questions.
Your goal is to reduce a question down to its simplest form while still retaining the semantic meaning.
Below you find the question:
--------
{question}
--------

Total output will be a semantically similar question that will be used to search an existing dataset.

SEMANTIC QUESTION:
`;

export const QUESTION_PROMPT = PromptTemplate.fromTemplate(questionTemplate);
```

Using this prompt, we generate the `semantic question` and use it to search for videos. We may also need to search using the original `question` if we don't find any videos with the `semantic question`. This is done using the `ORIGINAL_QUESTION_PROMPT` defined below:

```js
async function getVideos(question: string) {
  log.debug(
    `Performing similarity search for videos that answer: ${question}`,
    {
      question,
      location: `${prefix}.search.search`,
    }
  );

  const KNN = config.searches.KNN;
  /* Simple standalone search in the vector DB */
  return await (vectorStore.similaritySearch(question, KNN) as Promise<
    VideoDocument[]
  >);
}

async function searchVideos(question: string) {
  log.debug(`Original question: ${question}`, {
    location: `${prefix}.search.search`,
  });

  const semanticQuestion = await prompt.getSemanticQuestion(question);

  log.debug(`Semantic question: ${semanticQuestion}`, {
    location: `${prefix}.search.search`,
  });
  let videos = await getVideos(semanticQuestion);

  if (videos.length === 0) {
    log.debug(
      "No videos found for semantic question, trying with original question",
      {
        location: `${prefix}.search.search`,
      }
    );

    videos = await getVideos(question);
  }

  log.debug(`Found ${videos.length} videos`, {
    location: `${prefix}.search.search`,
  });

  const answerDocument = await prompt.answerQuestion(question, videos);

  return [
    {
      ...answerDocument.metadata,
      question: answerDocument.pageContent,
      isOriginal: true,
    },
  ];
}
```

The code above shows the whole process for getting answers from the LLM and returning them to the user. Once relevant videos are identified, the backend uses either Google Gemini or OpenAI's ChatGPT to generate answers. These answers are formulated based on the video transcripts stored in Redis, ensuring they are contextually relevant to the user's query. The `ANSWER_PROMPT` used to ask the LLM for answers is as follows:

```js
import { PromptTemplate } from 'langchain/prompts';

const answerTemplate = `
You are an expert in answering questions about Redis and Redis.
Your goal is to take a question and some relevant information extracted from videos and return the answer to the question.

- Try to mostly use the provided video info, but if you can't find the answer there you can use other resources.
- Make sure your answer is related to Redis. All questions are about Redis. For example, if a question is asking about strings, it is asking about Redis strings.
- The answer should be formatted as a reference document using markdown. Make all headings and links bold, and add new paragraphs around any code blocks.
- Your answer should include as much detail as possible and be no shorter than 500 words.

Here is some extracted video information relevant to the question: {data}

Below you find the question:
--------
{question}
--------

Total output will be the answer to the question.

ANSWER:
`;

export const ANSWER_PROMPT = PromptTemplate.fromTemplate(answerTemplate);
```

That's it! The backend will now return the answer and supporting videos to the user.

## How can you speed up responses with semantic answer caching?

The application we've built in this tutorial is a great starting point for exploring the possibilities of AI-powered video Q&A. However, there are many ways to improve the application and make it more efficient. One such improvement is to use Redis as a semantic vector cache.

Note in the previous section, we discussed making a call to the LLM to answer every question. There is a performance bottleneck during this step, because LLM response times vary, but can take several seconds. What if there was a way we could prevent unnecessary calls to the LLM? This is where `semantic vector caching` comes in.

### What is semantic vector caching and why does it matter?

Semantic vector caching happens when you take the results of a call to an LLM and cache them alongside the vector embedding for the prompt. In the case of our application, we could generate vector embeddings for the questions and store them in Redis with the answer from the LLM. This would allow us to avoid calling the LLM for similar questions that have already been answered.

You might ask why store the question as a vector? Why not just store the question as a string? The answer is that storing the question as a vector allows us to perform semantic vector similarity searches. So rather than relying on someone asking the exact same question, we can determine an acceptable similarity score and return answers for similar questions

### How do you implement semantic vector caching in Redis?

If you're already familiar with storing vectors in Redis, which we have covered in this tutorial, semantic vector caching is an extension of that and operates in essentially the same way. The only difference is that we are storing the question as a vector, rather than the video summary. We are also using the [cache aside](https://www.youtube.com/watch?v=AJhTduDOVCs) pattern. The process is as follows:

1.  When a user asks a question, we perform a vector similarity search for existing answers to the question.
2.  If we find an answer, we return it to the user. Thus, avoiding a call to the LLM.
3.  If we don't find an answer, we call the LLM to generate an answer.
4.  We then store the question as a vector in Redis, along with the answer from the LLM.

In order to store the question vectors we need to create a new vector store. This will create an index specifically for the question and answer vector. The code looks like this:

```js
const answerVectorStore = new RedisVectorStore(embeddings, {
    redisClient: client,
    indexName: `${prefix}-${config.redis.ANSWER_INDEX_NAME}`,
    keyPrefix: `${prefix}-${config.redis.ANSWER_PREFIX}`,
    indexOptions: {
        ALGORITHM: VectorAlgorithms.FLAT,
        DISTANCE_METRIC: 'L2',
    },
});
```

The `answerVectorStore` looks nearly identical to the `vectorStore` we defined earlier, but it uses a different [algorithm and distance metric](https://redis.io/docs/latest/develop/ai/search-and-query/advanced-concepts/vectors/). This algorithm is better suited for similarity searches for our questions.

The following code demonstrates how to use the `answerVectorStore` to check if a similar question has already been answered.

```js
async function checkAnswerCache(question: string) {
  const haveAnswers = await answerVectorStore.checkIndexExists();

  if (!(haveAnswers && config.searches.answerCache)) {
    return;
  }

  log.debug(`Searching for closest answer to question: ${question}`, {
    location: `${prefix}.search.getAnswer`,
    question,
  });

  /**
   * Scores will be between 0 and 1, where 0 is most accurate and 1 is least accurate
   */
  let results = (await answerVectorStore.similaritySearchWithScore(
    question,
    config.searches.KNN
  )) as Array<[AnswerDocument, number]>;

  if (Array.isArray(results) && results.length > 0) {
    // Filter out results with too high similarity score
    results = results.filter(
      (result) => result[1] <= config.searches.maxSimilarityScore
    );

    const inaccurateResults = results.filter(
      (result) => result[1] > config.searches.maxSimilarityScore
    );

    if (Array.isArray(inaccurateResults) && inaccurateResults.length > 0) {
      log.debug(
        `Rejected ${inaccurateResults.length} similar answers that have a score > ${config.searches.maxSimilarityScore}`,
        {
          location: `${prefix}.search.getAnswer`,
          scores: inaccurateResults.map((result) => result[1]),
        }
      );
    }
  }

  if (Array.isArray(results) && results.length > 0) {
    log.debug(
      `Accepted ${results.length} similar answers that have a score <= ${config.searches.maxSimilarityScore}`,
      {
        location: `${prefix}.search.getAnswer`,
        scores: results.map((result) => result[1]),
      }
    );

    return results.map((result) => {
      return {
        ...result[0].metadata,
        question: result[0].pageContent,
        isOriginal: false,
      };
    });
  }
}
```

The `similaritySearchWithScore` will find similar questions to the one being asked. It ranks them from `0` to `1`, where `0` is most similar or "closest". We then filter out any results that are too similar, as defined by the `maxSimilarityScore` environment variable. If we find any results, we return them to the user. Using a max score is crucial here, because we don't want to return inaccurate results.

To complete this process, we need to apply the `cache aside` pattern and store the question as a vector in Redis. This is done as follows:

```js
async function searchVideos(
  question: string,
  { useCache = config.searches.answerCache }: VideoSearchOptions = {}
) {
  log.debug(`Original question: ${question}`, {
    location: `${prefix}.search.search`,
  });

  if (useCache) {
    const existingAnswer = await checkAnswerCache(question);

    if (typeof existingAnswer !== "undefined") {
      return existingAnswer;
    }
  }

  const semanticQuestion = await prompt.getSemanticQuestion(question);

  log.debug(`Semantic question: ${semanticQuestion}`, {
    location: `${prefix}.search.search`,
  });

  if (useCache) {
    const existingAnswer = await checkAnswerCache(semanticQuestion);

    if (typeof existingAnswer !== "undefined") {
      return existingAnswer;
    }
  }

  let videos = await getVideos(semanticQuestion);

  if (videos.length === 0) {
    log.debug(
      "No videos found for semantic question, trying with original question",
      {
        location: `${prefix}.search.search`,
      }
    );

    videos = await getVideos(question);
  }

  log.debug(`Found ${videos.length} videos`, {
    location: `${prefix}.search.search`,
  });

  const answerDocument = await prompt.answerQuestion(question, videos);

  if (config.searches.answerCache) {
    await answerVectorStore.addDocuments([answerDocument]);
  }

  return [
    {
      ...answerDocument.metadata,
      question: answerDocument.pageContent,
      isOriginal: true,
    },
  ];
}
```

When a question is asked, we first check the answer cache. We check both the question and the generated semantic question. If we find an answer, we return it to the user. If we don't find an answer, we call the LLM to generate an answer. We then store the question as a vector in Redis, along with the answer from the LLM. It may look like we're doing more work here than we were without the cache, but keep in mind the LLM is the bottleneck. By doing this, we are avoiding unnecessary calls to the LLM.

Below are a couple screenshots from the application to see what it looks like when you find an existing answer to a question:

![First query result from the AI video Q&A app showing an original LLM-generated answer with matched video thumbnails](images/inline-4-523089fd6eeaa3c67f6508af2c3ace0c2a19cebf-2000x855.jpg)

![Subsequent query result served from the Redis semantic vector cache, returning an existing answer without calling the LLM](images/inline-5-d5d535681f8015591cb636f54cccbbf4c54dc751-2000x831.jpg)

## Conclusion

In this tutorial, we've explored how to build an AI-powered video Q&A application using Redis, LangChain, and various other technologies. We've covered setting up the environment, processing video uploads, and implementing search functionality. You also saw how to use Redis as a `vector store` and `semantic vector cache`.

> **Note**
>
> Not included in this tutorial is an overview of the frontend `Next.js` app. However, you can find the code in the [GitHub repository](https://github.com/redis-developer/video-qa-semantic-vector-caching) in the `app` directory.

### Key takeaways

- GenAI can be leveraged to create powerful apps without writing a ton of code.
- Redis is highly versatile and efficient in handling AI-generated data and vectors.
- LangChain makes it easy to integrate AI models with vector stores.
- Semantic vector caching in Redis dramatically reduces LLM costs and latency for repeated or similar questions.

## Next steps

Now that you've built a video Q&A system, here are some ways to extend what you've learned:

- **Add more content sources** — Extend the app to index podcasts, webinars, or lecture recordings using the same transcription and embedding pipeline.
- **Explore different embedding models** — Experiment with newer OpenAI or open-source embedding models to improve search accuracy.
- **Build a text-based RAG chatbot** — Apply the same Redis vector search pattern to documents and web pages with [Building a GenAI chatbot using Redis](/tutorials/howtos/solutions/vector/gen-ai-chatbot).
- **Try semantic text search** — Learn how to search unstructured text data with [Semantic text search with Redis](/tutorials/howtos/solutions/vector/semantic-text-search).
- **Get started with Redis Cloud** — Sign up at [redis.io/try-free](https://redis.io/try-free/) to run your vector store in a managed environment.

## Further reading

- [Perform vector search using Redis](/tutorials/howtos/solutions/vector/getting-started-vector)
- [Building a GenAI chatbot using Redis](/tutorials/howtos/solutions/vector/gen-ai-chatbot)
- [Semantic text search with Redis](/tutorials/howtos/solutions/vector/semantic-text-search)
- [Redis vector search documentation](https://redis.io/docs/latest/develop/ai/search-and-query/advanced-concepts/vectors/)
- [LangChain JS](https://js.langchain.com/docs/get_started/quickstart)
- [LangChain Redis integration](https://js.langchain.com/docs/integrations/vectorstores/redis)
