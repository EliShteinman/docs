---
title: "How to Create a Powerful Text Ranker Using Redis"
linkTitle: "How to Create a Powerful Text Ranker Using Redis"
url: "/blog/how-to-create-a-powerful-text-ranker-using-redis/"
description: "Living in a world where most people struggle to leave the house without their smartphone has meant Google is never too far away from us. In an instant, we can find an answer to almost any question..."
date: 2021-12-16
blogCategories:
- "How To and Tutorials"
- "Tech"
authors:
- "Growth Team"
lastmod: 2026-09-01
hidden: true
---

*By Growth Team · Published 16 December 2021 · updated 1 September 2026*

![Blog tile image](/images/blog/c86e373facc81f65cd92d14c045b1e2c546ed4be-772x550.webp)

Living in a world where most people struggle to leave the house without their smartphone has meant Google is never too far away from us. In an instant, we can find an answer to almost any question through a search query on Google’s search engine.

Search engines (and their access to infinite information) have been integrated into everyday life, making many of us incredibly reliant on them. And for one to be optimal, answers to queries need to be retrieved instantly due to the high standards set by Google and other tech giants.

Any lags, delays, or drags will hamper the user’s experience, which is why this Launchpad App, Alexis, has used Redis as the main database to overcome this obstacle.

The founder of this application, Bobby Donchev, has leveraged the power of RedisAI and RediSearch to retrieve information from a corpus in response to a query with maximum efficiency. Users are able to index PDFs and use a simple UI to extract information from their documents.

Without Redis, the entire search process would be sluggish, hampering the functionality of Alexis. Let’s take a look at how Bobby put this application together.


However, before moving on, we’d like to highlight that we also have an awesome range of applications for you to check out on the [Redis Launchpad](https://launchpad.redis.com/). So make sure to check it out!

[Click here to view video](https://www.youtube.com/embed/0L8gvs7whhk)

1. What will you build?
1. What will you need?
1. Architecture
1. Getting started
1. How the data is stored
1. How the data is accessed
1. How it works

## 1. What will you build?

You’ll build an efficient text ranker capable of retrieving search queries at maximum speed. Users will be able to leverage this application to index important PDFs and extract answers from their documents with ease.

We’ll go through each step in chronological order and highlight what components are required to build the application.

![](/images/blog/7deee83f3410ab224c9a5ad15bca645702f88066-1328x968.webp)

![](/images/blog/ee452ee1d5c1973854ffe720522e41a670019ef5-1356x468.webp)

## 2. What will you need?

- [**RediSearch**](https://oss.redis.com/redisearch/index.html)**: **indexes, querying and full-text search engine
- [**RedisAI**](https://docs.redis.com/latest/modules/redisai/redisai-quickstart/)**: **executes deep learning/machine learning models to manage data and decrease latency
- [**Redis Streams**](https://redis.io/docs/latest/develop/)**: **manages data consumption
- [**NodeJS**](https://nodejs.org/en/)**: **used as an open-source, cross-platform that executes JavaScript code outside a web browser
- [**RedisJSON**](https://oss.redis.com/redisjson/)**: **implements ECMA-404 The JSON Data Interchange Standard as a native data type.

## 3. Architecture

Providing an answer to the searcher’s query happens in two steps:

1. Firstly, you select the text that’s likely to contain the answers. You’ll have to use RediSearch with the BM25 ranking function for this step.
1. You can use a Transformer AI model loaded into RedisAI to identify the answer spans in the text.

By using RediSearch in the first step, you’ll drastically reduce the search space. This will make the app’s overall experience faster. After this, you’ll need to use NodeJS with typescript in the backend and React with typescript in the frontend.

Besides using RedisAI and RediSearch, you’ll be leveraging RedisJSON for your user model as well as an asynchronous worker implemented with Redis Streams.

The webserver is exposed with the express framework that has the following endpoints:

```python
POST /v1/users
POST /v1/login
POST /v1/logout
GET /v1/me

POST /pdf  (pdfUpload)
POST /v1/query

```

Once you register and log into the app, you’ll be able to start adding documents to the indexed library. When a PDF is uploaded, an event will be written into Redis Streams. Afterwards, somebody from the consumer group will pick up the event for async processing.

You can then process the PDF, apply some cleaning and store the PDF in a Redis hash that’s indexed with RediSearch. You’ll now be able to send natural queries to the server and won’t be confined to basic keyword searches such as ‘kubernetes deployments,’ ‘DDD root aggregate’ etc.

Instead, you’ll be able to query more relevant searches.

**Flowchart**

Below is a general overview of how Alexis functions.

![](/images/blog/81fb5403295b6a863ccbbce1b174f27bee553635-1600x200.webp)

Now let’s break down how the *Upload PDFs & Index PDF Content *and the *Answer Query *parts of the flowchart operate.

### Answer Query

![](/images/blog/a35403ec9a238b73efdae7793ae2b0c42ae2c142-1600x612.webp)

- The user enters a query on the UI which is then sent to RediSearch
- Both RediSearch and the BM25 function are then activated using keywords to find the most meaningful content.
- This content is then transmitted to RedisAI, along with the query, for it to compare and decide which answer is the most relevant to the user’s query.

### Upload PDFs & Index PDF Content

![](/images/blog/e644f7bdeb41bac9f9caa5d8ad77994167231057-1600x587.webp)

- A user types in a question into the search engine.
- RediSearch indexes the PDF(s) and searches for an answer to this query.
- RedisAI runs an inference and pulls a number of possible answers.
- RedisAI then compares each answer and decides which one is most relevant to the query.
- The answer is finally displayed to the user.

## 4. Getting started

### Step 1: Install the prerequisites

- Node - v12.x.x
- NPM - v6.x.x
- Docker and Docker-compose

### Step 2. Clone the repository

```python
git clone https://github.com/redis-developer/alexis

```

### Step 3: Install the dependencies

Change the directory to alexis and run the below command:

npm install

### Step 4. Setting up frontend and backend

The below command will bootstrap server and client app and also it will initialize Redis server as well as RedisInsight GUI:

npm run bootstrap

### Step 5. Start the application

npm start

### Step 6. Accessing the application

Open [http://localhost:3000](http://localhost:3000) to access the application

### Step 7. Accessing RedisInsight

RedisInsight is a visual tool that lets you do both GUI- and CLI-based interactions with your Redis database, and so much more when developing your Redis based application. It is a fully-featured pure Desktop GUI client that provides capabilities to design, develop and optimize your Redis application. [Click Here to learn more about RedisInsight](https://redis.io/docs/connect/insight/)

The RedisInsight GUI is accessible via the following link: [http://localhost:8001](http://localhost:8001)

## 5. How the data is stored

**Step 1: **The user data is stored in a RedisJSON

```python
{
 firstName: string
 lastName: string
 email: string
 password: string
 pdfs: Array<{id: string, fileName: string}>
}

```

**Step 2: **A RediSearch index is created for each user with the code below

```python
FT.CREATE ax:idx:<userId> on HASH PREFIX 1 ax:pdfs:<userId> SCHEMA content TEXT PHONETIC dm:en

```

**Step 3: **Once a user uploads a PDF we update his pdfs array with RedisJSON

```python
JSON.ARRAPPEND ax:users:<userId> .pdfs {id: pdfId, fileName: <uploadedPdf>}

```

**Step 4: **The file upload also triggers an event that’s being written to the **ax:stream:pdf-processing** stream. The payload of the stream is:

```python
{
  id: string,
  fileName: string
}

```

**Step 5: **A consumer within a consumer group picks the event from the stream and processes the file, also writing the content in a hash.

```python
HSET ax:pdfs:<userId>.<paragraph> content <cleanedParagraphBlock> fileName <pdfFileName>

```

## 6. How the data is accessed

In this application, there’s a RediSearch index for each user that indexes the above hash. This provides lookup capabilities to match relevant content to a user’s query. Content is analyzed with the below code:

```python
FT.SEARCH ax:idx:<userId> '@content:<userQuery>' SCORER BM25 WITHSCORES LIMIT 0 4

```

The content that’s retrieved by RediSearch is then transmitted to RedisAI to be analyzed.

## 7. How it works

**Create an account**

When you open the Alexis app, you’ll be directed to the portal for you to log in (see image below). If you haven’t already got an account, you’ll have the opportunity to create a new one from the hyperlink at the bottom.

![](/images/blog/90b22ea31e75d19bb2568972509f17933100c5ad-1122x386.webp)

Once you’ve logged in, you’ll be taken to another page on the portal. If this is your first time on the portal, you won’t have any documents in the library. The next step will be to import them into the application.

**Import documents into your library**

To begin this procedure, you can either drag and drop documents into the box in the centre of the screen or manually pull them up by clicking on the cloud icon.

Once you’ve uploaded a document, you’ll receive confirmation of its storage through the display of its title on the left-hand side of the screen (see below).

![](/images/blog/f1da14bd4fa4202329141f5915dc5c8d7d8c1acf-1408x756.webp)

When this happens, the PDF is uploaded to the server and is also cleaned in the background. This process is efficient due to the advanced capabilities of Redis.

**Make your query**

![](/images/blog/ac7d79bde6e4c1f5febad6f518c2818673f1df47-1408x756.webp)

As you can see from the image above, you simply have to type in the query you want the application to retrieve. In this example, the user has directly enquired what the content of the file is about by typing in ‘What is the journey about?’

When you’ve submitted your query, you’ll instantly be provided with a few answers, each ranked hierarchically based on their relevancy (see example below).

![](/images/blog/37d2d6656fea06802da22fd706bbb0ed189ee132-1600x1030.webp)

## Conclusion: making search easy with Redis

When it boils down to it, everyone expects search queries to be instant with no delays *whatsoever. *This is the digital age, after all, and any lags will only push users away and towards something that’s more optimal.

By using Redis, Alexis was powered to operate at a premium standard. Gathering the most meaningful content across different locations was fast and efficient thanks to RediSearch. And the hyper-advanced capabilities of RedisAI were able to sift through this content and provide users with the most relevant and accurate answers to their query.

If you want to discover more about how this application was made then you should check out [Bobby’s YouTube video](https://youtu.be/0L8gvs7whhk). We also have a wide variety of applications for you to get inspired on the [Redis Launchpad](https://launchpad.redis.com/).

From creating [real-time bus tracking systems in Helsinki](https://launchpad.redis.com/?id=project%3Aexpert-garbanzo) to [protecting crop insurers in developing nations](https://launchpad.redis.com/?id=project%3ACropInsurRedis), programmers from all around the world are tapping into the wonders of Redis to make a difference in everyday lives. And you can too!

[Watch the video](https://launchpad.redis.com/)

## Who created this application?

### Bobby Donchev

![](/images/blog/8fe71456295610b5424189b3942795512ed52905-800x800.webp)

Bobby is a dynamic programming engineer who’s had over twelve years of experience designing and implementing systems for clients.

Make sure to take a peek at his [GitHub page](https://github.com/neurocode-io/alexis) to stay up to date with all of the projects he’s been involved in.
