---
title: "From zero to RAG: Building your first RAG pipeline with RedisVL"
linkTitle: "From zero to RAG: Building your first RAG pipeline with RedisVL"
url: "/blog/from-zero-to-rag-building-your-first-rag-pipeline-with-redisvl/"
description: "You know that mix of excitement and uncertainty when you’re starting something new? That’s exactly how I felt when I set out to build a Retrieval Augmented Generation (RAG) pipeline using the Redis..."
date: 2025-02-03
blogCategories:
- "How To and Tutorials"
- "Tech"
authors:
- "Rini Vasan"
lastmod: 2025-06-13
hidden: true
---

*By Rini Vasan, AI Product Marketing Manager · Published 3 February 2025 · updated 13 June 2025*

![Blog tile image](/images/blog/35fa1e78ad65887c9aa3b5969c3792f98487822b-772x552.webp)

You know that mix of excitement and uncertainty when you’re starting something new? That’s exactly how I felt when I set out to build a Retrieval Augmented Generation (RAG) pipeline using the Redis Vector Library.

RAG might sound like just another buzzword, but it’s really about using the power of semantic search and large language models to create smarter, more efficient ways of finding and using information. For someone like me, who’s constantly searching for ways to sharpen my technical skills, this was the perfect challenge.

What followed was a rollercoaster of wins, setbacks, and “aha!” moments. From understanding how to preprocess data for semantic search to learning about vector embeddings and schema design, this project was as much about discovery as it was about building.

This is my way of sharing the full experience—wins, challenges, and everything in between. If you’re interested in Redis, RedisVL, RAG, or just curious about tackling technical projects, this is for you.

## Who am I? A PMM who speaks developer

I’m Rini, and my journey into tech has been anything but straightforward. I started out as a backend software engineer, burying myself in code and solving tricky technical problems. But over time, I found myself drawn to a different kind of problem-solving: understanding the needs of developers and bringing technical products to life in ways that truly resonate with users. That is what led me to my current role as a Product Marketing Manager (PMM) for AI at Redis.

Even though I’ve traded daily coding for marketing strategies, my curiosity for the technical side hasn’t faded. As a PMM, understanding our products inside out is key to helping users get the most out of them. That is why I rolled up my sleeves and built out my first RAG pipeline.

This Redis Vector Library felt like a great starting point. It’s at the forefront of intelligent search and AI-driven apps, and it gave me a chance to explore RAG—a technology I’ve been hearing so much about.

**What was my goal here?**

The main focus of my project was to build a RAG pipeline from scratch using the Redis Vector Library. I worked my way through this [Redis tutorial](https://colab.research.google.com/github/redis-developer/redis-ai-resources/blob/main/python-recipes/RAG/01_redisvl.ipynb) to get started with RedisVL. RAG is an exciting technology that pairs semantic search with large language models (LLMs) to retrieve relevant information and generate accurate, context-aware answers. By tackling this project, I aimed to understand both the fundamentals of RAG and how Redis can power such applications.

The Redis Vector Library was an essential tool for this project. It simplifies working with vector embeddings, making fast and precise semantic search possible, which is key to building a functional RAG pipeline. RedisVL makes it easy to store, search, and get important data.

I ended up building a working AI assistant that can answer queries about a recent Nike earnings call. It pulls relevant context from Nike’s earnings report and generates accurate, context-aware responses using an LLM.

I learned how easy it can be to set up an AI assistant using RAG and Redis. Beyond the technical implementation, this project highlights how tools like Redis and RAG can have real-world impact. Scale this to industries like finance, healthcare, or education, and you’ve got AI assistants providing instant insights and making critical information easy to act on.

**First, I set up the basics**

To follow along, you can use [this tutorial](https://colab.research.google.com/github/redis-developer/redis-ai-resources/blob/main/python-recipes/RAG/01_redisvl.ipynb) located on our [AI resources dev hub](https://redis.io/docs/latest/develop/ai/).

Set up your environment

Clone the necessary GitHub repository to access datasets and resources

```python
!git clone https://github.com/redis-developer/redis-ai-resources.git temp_repo 
!mv temp_repo/python-recipes/RAG/resources . 
!rm -rf temp_repo


```

Install Python dependencies, including redis, redisVL, and LangChain.

```python
!pip install -q redis redisvl langchain_community pypdf sentence-transformers langchain openai

```

Install and configure Redis

Set up a Redis Stack instance locally for storing, indexing, querying vector embeddings.

```python
%%sh
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
sudo apt-get update  > /dev/null 2>&1
sudo apt-get install redis-stack-server  > /dev/null 2>&1
redis-stack-server --daemonize yes


```

Configure the Redis connection URL to work with either a local or cloud instance.

```python
import os
import warnings
#warnings.filterwarnings('ignore')

# Replace values below with your own if using Redis Cloud instance
REDIS_HOST = os.getenv("REDIS_HOST", "localhost") # ex: "redis-18374.c253.us-central1-1.gce.cloud.redislabs.com"
REDIS_PORT = os.getenv("REDIS_PORT", "6379")      # ex: 18374
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")  # ex: "1TNxTEdYRDgIDKM2gDfasupCADXXXX"

# If SSL is enabled on the endpoint, use rediss:// as the URL prefix
REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"


```

Prepare the dataset

Load a financial 10k PDF document using LangChain’s *PyPDFLoader.*

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

# Load list of pdfs from a folder
data_path = "resources/"
docs = [os.path.join(data_path, file) for file in os.listdir(data_path)]

print("Listing available documents ...", docs)


```

```python
# pick out the Nike doc for this exercise
doc = [doc for doc in docs if "nke" in doc][0]

# set up the file loader/extractor and text splitter to create chunks
text_splitter = RecursiveCharacterTextSplitter(
   chunk_size=2500, chunk_overlap=0
)
loader = PyPDFLoader(doc, headers = None)
# extract, load, and make chunks
chunks = loader.load_and_split(text_splitter)

print("Done preprocessing. Created", len(chunks), "chunks of the original pdf", doc)


```

This is what the output should look like in the Colab.

![](/images/blog/3006a2ad1a4e8fdc793bb74482570fe9659d2c1c-1521x78.webp)

Preprocess the document by splitting it into manageable chunks using *RecursiveCharacterTextSplitter.*

```python
from redisvl.utils.vectorize import HFTextVectorizer
import pandas as pd
from tqdm.auto import tqdm

hf = HFTextVectorizer("sentence-transformers/all-MiniLM-L6-v2")
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Embed each chunk content
embeddings = hf.embed_many([chunk.page_content for chunk in chunks])

# Check to make sure we've created enough embeddings, 1 per document chunk
len(embeddings) == len(chunks)


```

Define schema & create index

Design a Redis index schema with fields for text, tags, and vector embeddings.

```python
from redis import Redis
from redisvl.index import SearchIndex

index_name = "redisvl"

schema = {
 "index": {
   "name": index_name,
   "prefix": "chunk"
 },
 "fields": [
   {
       "name": "chunk_id",
       "type": "tag",
       "attrs": {
           "sortable": True
       }
   },
   {
       "name": "content",
       "type": "text"
   },
   {
       "name": "text_embedding",
       "type": "vector",
       "attrs": {
           "dims": 384,
           "distance_metric": "cosine",
           "algorithm": "hnsw",
           "datatype": "float32"
       }
   }
 ]
}


```

Configure the index in Redis to make semantic searches work efficiently.

```python
# connect to redis
client = Redis.from_url(REDIS_URL)
# create an index from schema and the client
index = SearchIndex.from_dict(schema)
index.set_client(client)
index.create(overwrite=True, drop=True)


```

```python
# use the RedisVL CLI tool to list all indices
!rvl index listall
# get info about the index
!rvl index info -i redisvl


```

Load data into Redis

Process and load the preprocessed chunks and their embeddings into the Redis index.

```python
# load expects an iterable of dictionaries
from redisvl.redis.utils import array_to_buffer

data = [
   {
       'chunk_id': i,
       'content': chunk.page_content,
       # For HASH -- must convert embeddings to bytes
       'text_embedding': array_to_buffer(embeddings[i], dtype='float32')
   } for i, chunk in enumerate(chunks)
]

# RedisVL handles batching automatically
keys = index.load(data, id_field="chunk_id")


```

Query the database

Construct vector queries to find text chunks semantically similar to user queries.

```python
from redisvl.query import VectorQuery
query = "Nike profit margins and company performance"
query_embedding = hf.embed(query)
vector_query = VectorQuery(
   vector=query_embedding,
   vector_field_name="text_embedding",
   num_results=3,
   return_fields=["chunk_id", "content"],
   return_score=True
)

# show the raw redis query
str(vector_query)

```

```python
# execute the query with RedisVL
result=index.query(vector_query)

# view the results
pd.DataFrame(result)


```

These are the results outputted in Colab notebook.


![Colab notebook.
](/images/blog/8583a8f2b7778f1c43ed1c3ac5160ed0eab7c0ec-1567x322.webp)

```python
​​# paginate through results
for result in index.paginate(vector_query, page_size=1):
   print(result[0]["chunk_id"], result[0]["vector_distance"], flush=True)


```

This is what pagination through the results looked like in the Colab notebook.

![ pagination](/images/blog/35e8362a1bfe46251d9944119c334800097b265a-410x155.webp)

Perform similarity searches, pull relevant results, and explore additional filtering/sorting options.

```python
# Sort by chunk_id field after vector search limits to topK
vector_query = VectorQuery(
   vector=query_embedding,
   vector_field_name="text_embedding",
   num_results=4,
   return_fields=["chunk_id"],
   return_score=True
)

# Decompose vector_query into the core query and the params
query = vector_query.query
params = vector_query.params

# Pass query and params direct to index.search()
result = index.search(
   query.sort_by("chunk_id", asc=True),
   params
)

pd.DataFrame([doc.__dict__ for doc in result.docs])

```

```python
from redisvl.query.filter import Text

vector_query = VectorQuery(
   vector=query_embedding,
   vector_field_name="text_embedding",
   num_results=4,
   return_fields=["content"],
   return_score=True
)

# Set a text filter
text_filter = Text("content") % "profit"

vector_query.set_filter(text_filter)

result=index.query(vector_query)
pd.DataFrame(result)

```

These are the results of the query from the Colab notebook.

![results of the query](/images/blog/e478b484a4f215f7b2aaa7aa992e51382e752b45-1463x394.webp)

```python
from redisvl.query import RangeQuery
range_query = RangeQuery(
   vector=query_embedding,
   vector_field_name="text_embedding",
   num_results=4,
   return_fields=["content"],
   return_score=True,
   distance_threshold=0.8  # find all items with a semantic distance of less than 0.8
)

result=index.query(range_query)
pd.DataFrame(result)


```

```python
# Add filter to range query
range_query.set_filter(text_filter)

index.query(range_query)
pd.DataFrame(result)


```

These are the results of the range query from the Colab notebook.

![range query from the Colab notebook](/images/blog/f45de83562536362d738a34744e3ffa427b29525-1456x390.webp)

Build the RAG pipeline

Setup RedisVL AsyncSearchIndex. This is a tool for creating and managing search indices in an asynchronous environment, which enables non-blocking operations for high-concurrency applications. It allows you to define data schemas, load and query data, and perform vector-based searches efficiently, making it ideal for scalable AI workflows like RAG pipelines.

```python
from redis.asyncio import Redis as AsyncRedis
from redisvl.index import AsyncSearchIndex

client = AsyncRedis.from_url(REDIS_URL)
async_index = AsyncSearchIndex.from_dict(schema)
await async_index.set_client(client)

```

Integrate OpenAI’s GPT model (gpt-3.5-turbo-0125) to generate context-aware responses based on retrieval results.

```python
import openai
import os
import getpass
CHAT_MODEL = "gpt-3.5-turbo-0125"

if "OPENAI_API_KEY" not in os.environ:
   os.environ["OPENAI_API_KEY"] = getpass.getpass("OPENAI_API_KEY :")


```

Use a structured prompt to combine user questions and relevant document context for optimal responses.

```python
async def answer_question(index: AsyncSearchIndex, query: str):
   """Answer the user's question"""

   SYSTEM_PROMPT = """You are a helpful financial analyst assistant that has access
   to public financial 10k documents in order to answer users questions about company
   performance, ethics, characteristics, and core information.
   """

   query_vector = hf.embed(query)
   # Fetch context from Redis using vector search
   context = await retrieve_context(index, query_vector)
   # Generate contextualized prompt and feed to OpenAI
   response = await openai.AsyncClient().chat.completions.create(
       model=CHAT_MODEL,
       messages=[
           {"role": "system", "content": SYSTEM_PROMPT},
           {"role": "user", "content": promptify(query, context)}
       ],
       temperature=0.1,
       seed=42
   )
   # Response provided by LLM
   return response.choices[0].message.content


async def retrieve_context(async_index: AsyncSearchIndex, query_vector) -> str:
   """Fetch the relevant context from Redis using vector search"""
   results = await async_index.query(
       VectorQuery(
           vector=query_vector,
           vector_field_name="text_embedding",
           return_fields=["content"],
           num_results=3
       )
   )
   content = "\n".join([result["content"] for result in results])
   return content


def promptify(query: str, context: str) -> str:
   return f'''Use the provided context below derived from public financial
   documents to answer the user's question. If you can't answer the user's
   question, based on the context; do not guess. If there is no context at all,
   respond with "I don't know".

   User question:

   {query}

   Helpful context:

   {context}

   Answer:
   '''

```

Now that we have everything set up, we can ask questions about the earnings report.

Test the pipeline

Ask financial questions (e.g. revenue trends, ESG practices) to test the RAG pipeline.

```python
# Generate a list of questions
questions = [
   "What is the trend in the company's revenue and profit over the past few years?",
   "What are the company's primary revenue sources?",
   "How much debt does the company have, and what are its capital expenditure plans?",
   "What does the company say about its environmental, social, and governance (ESG) practices?",
   "What is the company's strategy for growth?"
]

```

```python
import asyncio

results = await asyncio.gather(*[
   answer_question(async_index, question) for question in questions
])

```

View the results

Retrieve accurate, context-based responses showcasing the pipeline’s effectiveness.

```python
for i, r in enumerate(results):
   print(f"Question: {questions[i]}")
   print(f"Answer: \n {r}", "\n-----------\n")

```

Here we can finally see some of the answers to our questions from the Colab notebook.

![answers to our questions from the Colab notebook.](/images/blog/d577f6f661dec6664dd41fb76364b624790b0f06-2035x623.webp)

**Highlights of my journey**

Many parts of this project were surprisingly intuitive and enjoyable. Exploring the PyPDFLoader and RecursiveCharacterTextSplitter documentation was a highlight as it showed me how easy it was to preprocess and structure text from PDF documents into meaningful chunks.

RedisVL stood out for its simplicity and efficiency. Tasks like generating text embeddings with HFTextVectorizer and integrating Hugging Face models felt seamless. RedisVL’s ability to handle vector search made it easy to store, index, and retrieve relevant data, which was crucial for building the RAG pipeline.

Additionally, defining the schema, loading data into Redis, and querying the database went smoothly. Watching everything work together was rewarding and showed how powerful and user-friendly the tools were. It made the whole process both informative and fun.

**Where the road got bumpy**

I also ran into some hiccups with the project and I had to learn some new things to complete my AI assistant. First, I had to get up to speed on some unique technical concepts, like Hugging Face models, vector embeddings, and semantic search. These were new to me, so it required additional reading and experimentation to fully grasp how everything worked together.

Another hurdle came when I encountered an OpenAI API rate limit while testing the RAG pipeline. Each query to the API returned a “quota exceeded” error, effectively blocking progress. To resolve this, I considered introducing a delay between API requests to avoid exceeding the rate limit. However, the other solution I chose was changing to a different OpenAI API key that was part of a business plan. This allowed me to keep testing and finish the pipeline successfully.

**Key learnings**

Working through the project and building a RAG pipeline using RedisVL helped me learn a lot. RedisVL stood out as a powerful tool, making vector search and embedding management straightforward and efficient. Its seamless integration with Hugging Face models highlighted how well it supports complex AI workflows, and its role in powering semantic search for the RAG pipeline was invaluable. This project also deepened my understanding of RAG pipelines and their ability to combine semantic search with large language models to deliver precise, context-aware answers.

Another key lesson was the importance of effective data preprocessing. Using tools like PyPDFLoader and RecursiveCharacterTextSplitter made structuring data intuitive and ensured the rest of the pipeline worked smoothly.

Ultimately, this hands-on exploration reinforced the importance of approaching tools like Redis with a developer’s mindset, even in my role as a PMM. It was a rewarding journey that demonstrated the potential of Redis and RAG pipelines while leaving me eager to try more advanced use cases.

**What’s next**

If you are as intrigued by the possibilities of Redis and RAG pipelines as I am, the best way to get started is to try it yourself. Hands-on experience is invaluable, and to follow what I did, you can use this [Colab notebook](https://colab.research.google.com/github/redis-developer/redis-ai-resources/blob/main/python-recipes/RAG/01_redisvl.ipynb) to build the same RAG pipeline I did.

For more in-depth guidance, be sure to explore the[ RedisVL documentation](https://docs.redisvl.com/en/latest/). It’s a rich resource filled with detailed guides and examples that can help you understand the full range of capabilities RedisVL offers.

You can also consider using RedisVL to help enhance your current projects or inspire new ones. From powering search engines to optimizing recommendation systems, the applications are limitless. RedisVL can help you solve real-world challenges in your work.

Finally, if you are looking for more inspiration, check the [Redis for AI docs](https://redis.io/docs/latest/develop/ai/). It features additional use cases, tutorials, and hands-on projects to help you explore other ways to leverage RedisVL.
