---
title: "Deploy GenAI apps faster with Redis and NVIDIA NIM"
linkTitle: "Deploy GenAI apps faster with Redis and NVIDIA NIM"
url: "/blog/use-redis-with-nvidia-nim-to-deploy-genai-apps-faster/"
description: "Accelerate your GenAI app development with Redis–the world’s fastest data platform for real-time data and AI apps. Now, with Redis and NVIDIA NIM inference microservices, you can build and deploy..."
date: 2024-06-02
blogCategories:
- "Tech"
authors:
- "Jim Allen Wallace"
- "Tyler Hutcherson"
lastmod: 2025-07-03
hidden: true
---

*By Jim Allen Wallace, Tyler Hutcherson · Published 2 June 2024 · updated 3 July 2025*

![Blog tile image](/images/site-mirror/46e437a8e582c611148582d926192488f4c8e7b9-772x552.webp)

Accelerate your GenAI app development with Redis–the world’s fastest data platform for real-time data and AI apps. Now, with Redis and [NVIDIA NIM](https://www.nvidia.com/en-us/ai/) inference microservices, you can build and deploy GenAI apps faster.

Companies are looking for ways to bring their GenAI apps to production, so they can apply recent advances and provide a better experience for their customers. Building GenAI apps has all the usual challenges of software development–integrations, testing, and scaling, but AI takes it to another level. To stay ahead, companies need a simple and reliable infrastructure that adapts with technology.

To help companies bring GenAI apps to production faster, Redis is using NVIDIA NIM to provide ready-made infrastructure for fast data access and AI models. NIM, part of the NVIDIA AI Enterprise software platform for GenAI development and deployment, can be combined with Redis for fast and flexible deployment.

Devs rely on Redis for their real-time data and AI needs, for everything ranging from customer support agents, to fraud and anomaly detection, to real-time product recommendations. With NIM, you can skip the setup and maintenance of full-stack infrastructure to run the latest GenAI models. NIM streamlines AI model deployment with pre-built, cloud-native microservices that are maintained to deliver optimized inference on NVIDIA accelerated infrastructure.

You can use NIM alongside your existing data in Redis to use the latest Redis features like vector database and semantic caching. Use Redis as your [vector database](/blog/vector-databases-101/) for faster information access using Retrieval Augmented Generation (RAG) with models from NIM. Plus, use Redis semantic caching to cache the LLM responses for your GenAI apps. With both, you can reduce costs and speed up responses to provide the real-time experience that users expect.

To show how easy it is to get started with Redis and NVIDIA NIM, we’ll walk through this demo to build a simple chatbot that uses RAG with a Redis vector database and NIM for the model and inferencing for fast responses. In this example, we’ll ask it questions about the Chevy Colorado user manual. Let’s get started. You can follow along using [this notebook](https://github.com/redis-developer/redis-ai-resources/blob/main/python-recipes/RAG/05_nvidia_ai_rag_redis.ipynb).

First, connect to the NVIDIA-hosted LLM and embedding models. You can use your existing API key or [get one here](https://build.nvidia.com/explore/discover). We’ll use NIM for its simple and fast access to the latest models and LangChain to create embeddings.

```python
from langchain_core.messages import ChatMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_nvidia_ai_endpoints import ChatNVIDIA

# Create LLM instance with the Mistral model
llm = ChatNVIDIA(
    model="mistralai/mixtral-8x22b-instruct-v0.1",
    temperature=0.1,
    top_p=1.0,
)

```

```python
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings

emb = NVIDIAEmbeddings()

```

We’ll be working with a pdf of the Chevy Colorado truck user manual. It’s full of qualitative and quantitative information about the Chevy vehicle. Once the data is imported into the notebook, we’ll prepare the document for RAG using LangChain.

```python
from langchain.text_splitter import SentenceTransformersTokenTextSplitter
from langchain.document_loaders import UnstructuredFileLoader

# Load list of pdfs from a folder
data_path = f"data/"
docs = [os.path.join(data_path, file) for file in os.listdir(data_path)]

text_splitter = SentenceTransformersTokenTextSplitter()

```

```python
loader = UnstructuredFileLoader(
    docs[0], mode="single", strategy="fast"
)

# extract, load, and make chunks
chunks = loader.load_and_split(text_splitter)

```

We’ll take those chunks of data from the Chevy Colorado brochure and load them into Redis vector database for fast retrieval.

```python
from langchain_community.vectorstores.redis import Redis

vectordb = Redis.from_documents(
    documents=chunks,
    embedding=emb,
    redis_url="redis://localhost:6379"
  )

```

```python
retriever = vectordb.as_retriever(
    search_type="similarity_distance_threshold",
    search_kwargs={"distance_threshold":0.4}
)

```

To set up our RAG to get the most out of the NIM model, we’ll design a RAG prompt that describes the dataset and how we want the LLM to respond.

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    """You are an intelligent assistant specializing in the Chevy Colorado
    2022. You have access to the car manual and production information and should help
    answer users questions based on provided context below. Be truthful and honest --
    do not make anything up if it's not clearly provided in the context below.

    User Question: {question}

    Context:\n{context}
   Answer:"""
)

```

Let’s set up our RAG chain using LangChain Expression Language (LCEL).

```python
# Build the RAG chain using LCEL
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.pydantic_v1 import BaseModel

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

chain = (
    RunnableParallel({"context": retriever | format_docs, "question": RunnablePassthrough()})
    | prompt
    | llm
    | StrOutputParser()
)

# Add typing for input
class Question(BaseModel):
    __root__: str

chain = chain.with_types(input_type=Question)

```

Once everything is set up, we can go ahead and ask it our question. The chatbot will send the question and relevant information provided from Redis vector database to the LLM with NIM to generate a response.

```python
chain.invoke("What models are available for the chevy colorado?")

```

The app sends back an appropriate response from the source documents that matches our request.

```
The 2022 Chevy Colorado is available in four models: WT, LT, Z71, and ZR2. These models can come in either an extended cab or crew cab configuration. The engines available are a 2.5L 4-cylinder, a 3.6L V6, and a Duramax 2.8L turbo-diesel engine. The Duramax engine provides up to 7,700 lbs. of towing capacity and can deliver up to 30 mpg on the highway. The ZR2 model is an off-road beast with the capability to conquer tough trails. Additionally, there is an available ZR2 Bison Edition which includes 17-inch AEV.

```

Let’s go one step further and make the application add sources to the response. This helps users explore the docs and verify the information themselves.

```python
rag_chain_from_docs = (
    RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
    | prompt
    | llm
    | StrOutputParser()
)

rag_chain_with_source = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}
).assign(answer=rag_chain_from_docs)

```

We’ll ask our question once and get the following response.

```python
rag_chain_with_source.invoke("What models are available for the chevy colorado?")

```

```
{'context': [Document(page_content='2022 colorado choose your adventure. the 2022 colorado delivers everything you could ask for in a midsize pickup. engine choices that are powerful and efficient, including an available gm - exclusive duramax(r) 2. 8l turbo - diesel engine that provides up to 7, 700 lbs. of towing1, 2 muscle. a zr2 off - road beast with the capability to conquer tough trails. and a comfortable interior filled with convenience and technology features. so go ahead. choose your best life in colorado. colorado crew cab zr2 in sand dune metallic with available zr2 dusk special edition. vehicle shown can tow up to 5, 000 lbs. 2, 3 1 requires colorado crew cab short box lt 2wd with available trailering package, lt convenience package and safety package. 2 maximum trailering ratings are intended for comparison purposes only. before you buy a vehicle or use it for trailering, carefully review the trailering section of the owner ' s manual. the trailering capacity of your specific vehicle may vary. the weight of passengers, cargo and options or accessories may reduce the amount you can trailer. 3 requires available trailering package and automatic locking rear differential on lt ; requires available trailering package on z71. due to current supply chain shortages, certain features shown have limited or late availability, or are no longer available. see the window label or a dealer regarding the features on an individual vehicle. introducing colorado colorado at a glance. four models : wt, lt, z71 and zr2 extended cab or crew cab three engines 2. 5l 4 - cylinder 3. 6l v6 duramax 2. 8l turbo - diesel 30 mpg highway 1 with available diesel engine 7, 700 lbs. maximum trailering weight2 with available diesel engine apple carplay(r)3 and android autoTM4 compatibility available zr2 bison edition includes 17 - inch aev', metadata={'id': 'doc:5313bad541f24eb58d856c7ca8f04fc4:17319c587eaa4dd69eacd57b50ff1a5e', 'source': 'data/2022-chevrolet-colorado-ebrochure.pdf'})],
 'question': 'What models are available for the chevy colorado?',
 'answer': ' The 2022 Chevy Colorado is available in four models: WT, LT, Z71, and ZR2. These models can come in either an extended cab or crew cab configuration. The engines available are a 2.5L 4-cylinder, a 3.6L V6, and a Duramax 2.8L turbo-diesel. The Colorado can achieve up to 30 mpg on the highway with the available diesel engine. The maximum trailering weight is 7,700 lbs with the available diesel engine. The Colorado also offers Apple CarPlay(r) and Android AutoTM compatibility. Additionally, there is an available ZR2 Bison Edition which includes 17-inch AEV.'}

```

We hope you enjoyed the demo. You can now use Redis and NVIDIA NIM for your own apps.

To get started:

- [Check out this notebook on the Redis Developer repo](https://github.com/redis-developer/redis-ai-resources/blob/main/python-recipes/RAG/05_nvidia_ai_rag_redis.ipynb)
- [Get started with Redis](https://redis.io/try-free/)
- [Learn more about how to use Nvidia NIM for your applications](https://www.nvidia.com/en-us/ai/)
