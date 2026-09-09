---
title: "Build an E-commerce Chatbot With Redis, LangChain, and OpenAI"
linkTitle: "Build an E-commerce Chatbot With Redis, LangChain, and OpenAI"
url: "/blog/build-ecommerce-chatbot-with-redis/"
description: "Given the recent surge of AI-enabling APIs and web development tools, it seems like everyone is building chatbots into their applications. Want to see what’s involved? Here’s an overview."
date: 2023-04-12
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2026-06-01
hidden: true
---

*By Redis   · Published 12 April 2023 · updated 1 June 2026*

![Blog tile image](/images/site-mirror/4827332eea928c40aba2fb92e94ae172db9b4c53-772x550.webp)

**Given the recent surge of AI-enabling APIs and web development tools, it seems like everyone is building chatbots into their applications. Want to see what’s involved? Here’s an overview.**

One new (and wildly popular) framework, [LangChain](https://github.com/hwchase17/langchain), makes it easy to develop applications that interact with a language model and external sources of data or computation. It does this by focusing on clear and modular abstractions for all the building blocks necessary to build; then it constructs commonly used “chains,” which are combinations of the building blocks. For example, the [Conversational Retrieval Chain](https://github.com/hwchase17/langchain/tree/master/langchain/chains/conversational_retrieval) enables users to have a “conversation” with their data in an external store.

How does it do this? [OpenAI](http://platform.openai.com) language models were not trained on your company’s specific data, or certainly not tuned for it. If you want the chatbot to rely on it, you need to provide OpenAI with your data at runtime. The retrieval step fetches relevant data to the user’s query from Redis using Vector Similarity Search (VSS) and then pipes the data into the language model along with the original question. It asks the model to use *only* the provided sources – what we in AI circles call “context” – to answer the question.

Most of the complexity in this chain comes down to the retrieval step. That is why we’re so excited to add an integration between LangChain and [Redis Enterprise as a vector database](/solutions/vector-search/). This combination makes it possible to bridge the gap between complex AI and product development – without breaking a sweat.

Don’t believe us? In this short tutorial we build a conversational retail shopping assistant that helps customers find items of interest that are buried in a product catalog. [You can follow along with the full code](https://github.com/RedisVentures/redis-langchain-chatbot).

## Building your chatbot

Before we jump in, we’d like to thank Fabian Stehle from [LabLab AI](https://lablab.ai/), who put together the initial prototype of this demo. We extended it and layered in additional LangChain components to give it more functionality.

First, let’s collect all the pieces we need for the project.

### Install Python requirements

This project needs a few Python libraries. These are stored in the requirements.txt file at the [github repo](https://github.com/RedisVentures/redis-langchain-chatbot).

```bash
pip install langchain==0.0.123
pip install openai==0.27.2
pip install redis==4.5.3
pip install numpy
pip install pandas
pip install gdown

```

### Fetch and prepare the products dataset

For the retail chatbot, we chose to work with the [Amazon Berkeley Objects](https://amazon-berkeley-objects.s3.amazonaws.com/index.html) dataset. This includes a large selection of Amazon products that are perfect for generating a retail assistant. Download the file from the link, or use the gdown command line interface to download the file from [a hosted link](https://drive.google.com/file/d/1tHWB6u3yQCuAgOYc-DxtZ8Mru3uV5_lj/view).

```bash
gdown --id 1tHWB6u3yQCuAgOYc-DxtZ8Mru3uV5_lj

```

We use the pandas Python library to load and preprocess the dataset. While it loads, we truncate the longer text fields. That’s to keep our dataset a bit leaner, which saves on memory and compute time.

```python
import pandas as pd

MAX_TEXT_LENGTH=1000  # Maximum num of text characters to use

def auto_truncate(val):

    """Truncate the given text."""

    return val[:MAX_TEXT_LENGTH]

# Load Product data and truncate long text fields

all_prods_df = pd.read_csv("product_data.csv", converters={

    'bullet_point': auto_truncate,

    'item_keywords': auto_truncate,

    'item_name': auto_truncate

})

```

With our products dataset fully loaded, we perform some final preprocessing steps to clean up the keywords field and to drop missing values.

```python
# Replace empty strings with None and drop

all_prods_df['item_keywords'].replace('', None, inplace=True)

all_prods_df.dropna(subset=['item_keywords'], inplace=True)

# Reset pandas dataframe index

all_prods_df.reset_index(drop=True, inplace=True)

```

If you’re following along with the code on github, take a peek at the dataframe with all_prods_df.head(). The full dataset contains over 100,000 products, but for this chatbot, we restrict it to a subset of 2,500.

```python
# Num products to use (subset)
NUMBER_PRODUCTS = 2500  

# Get the first 2500 products
product_metadata = ( 
    all_prods_df
     .head(NUMBER_PRODUCTS)
     .to_dict(orient='index')
)

# Check one of the products
product_metadata[0]

```

Here is an example of one of the product [JSON](/blog/learn-json-from-redis-experts/) objects we have to work with.

```javascript
{'item_id': 'B07T2JY31Y',
 'marketplace': 'Amazon',
 'country': 'IN',
 'main_image_id': '71vX7qIEAIL',
 'domain_name': 'amazon.in',
 'bullet_point': '3D Printed Hard Back Case Mobile Cover for Sony Xperia Z1 L39H Easy to put & take off with perfect cutouts for volume buttons, audio & charging ports. Stylish design and appearance, express your unique personality. Extreme precision design allows easy access to all buttons and ports while featuring raised bezel to life screen and camera off flat surface. Slim Hard Back Cover No Warranty',
 'item_keywords': 'mobile cover back cover mobile case phone case mobile panel phone panel LG mobile case LG phone cover LG back case hard case 3D printed mobile cover mobile cover back cover mobile case phone case mobile panel phone panel Sony Xperia mobile case Sony Xperia phone cover Sony Xperia back case hard case 3D printed mobile cover mobile cover back cover mobile case phone case mobile panel phone panel Sony Xperia mobile case Sony Xperia phone cover Sony Xperia back case hard case 3D printed mobile cover mobile cove',
 'material': 'Wood',
 'brand': 'Amazon Brand - Solimo',
 'color': 'others',
 'item_name': 'Amazon Brand - Solimo Designer Leaf on Wood 3D Printed Hard Back Case Mobile Cover for Sony Xperia Z1 L39H',
 'model_name': 'Sony Xperia Z1 L39H',
 'model_number': 'gz8056-SL40528',
 'product_type': 'CELLULAR_PHONE_CASE'}

```

## Set up Redis as a vector database

LangChain has a simple [wrapper around Redis](https://github.com/hwchase17/langchain/blob/master/langchain/vectorstores/redis.py) to help you load text data and to create [embeddings](https://platform.openai.com/docs/guides/embeddings) that capture “meaning.” In this code, we prepare the product text and metadata, prepare the text embeddings provider (OpenAI), assign a name to the search index, and provide a Redis URL for connection.

```python
import os

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.redis import Redis as RedisVectorStore

# set your openAI api key as an environment variable
os.environ['OPENAI_API_KEY'] = "YOUR OPENAI API KEY"

# data that will be embedded and converted to vectors
texts = [
    v['item_name'] for k, v in product_metadata.items()
]

# product metadata that we'll store along our vectors
metadatas = list(product_metadata.values())

# we will use OpenAI as our embeddings provider
embedding = OpenAIEmbeddings()

# name of the Redis search index to create
index_name = "products"

# assumes you have a redis stack server running on local host
redis_url = "redis://localhost:6379"

```

At this point, we’ve successfully processed the Amazon products dataset and loaded it into the Redis database with vector embeddings.

Then we bring it all together to create the Redis vectorstore.

```python
# create and load redis with documents
vectorstore = RedisVectorStore.from_texts(
    texts=texts,
    metadatas=metadatas,
    embedding=embedding,
    index_name=index_name,
    redis_url=redis_url
)

```

Now we’re ready to create a chatbot that uses the products’ data (stored in Redis) to inform conversations.

## Create the LangChain conversational chain

Chatbots are [hugely popular](https://bloggingwizard.com/chatbot-statistics/) because they can be immensely useful. In the scenario we build below, we assume that you need fashion advice. You can ask the bot for help in finding a pair of shoes suitable for both casual outings and work-related outings. You want something that pops, but doesn’t cause too much of a distraction. Given the data we fed it already, our chatbot should be able to recommend a few pairs of shoes that fit the requirements.

It’s time to bring in more LangChain functionality. To do so, we need to import several LangChain tools.

```python
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import (
    ConversationalRetrievalChain,
    LLMChain
)
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.prompts.prompt import PromptTemplate

```

As mentioned in the introduction, this project uses a ConversationalRetrievalChain to simplify chatbot development.

Redis holds our product catalog including metadata and OpenAI-generated embeddings that capture the semantic properties of the product content. Under the hood, using [Redis Vector Similarity Search](https://redis.io/docs/stack/search/reference/vectors/) (VSS), the chatbot queries the catalog for products that are most similar to or relevant to what the user is shopping for. No fancy keyword search or manual filtering is needed; VSS takes care of it.

The ConversationalRetrievalChain that forms the chatbot operates in three phases:

1. **Question creation** evaluates the input question and uses the OpenAI GPT model to combine it with knowledge from previous conversational interactions (if any).
1. **Retrieval** searches Redis for the best available products, given the items in which the shopper expressed interest.
1. **Question answering** gets the product results from the vector search query and uses the OpenAI GPT model to help the shopper navigate the options.

Even though LangChain and Redis greatly expedite this workflow, interacting with a large language model (LLM) like GPT requires a “prompt” for communication. We humans create a prompt (set of instructions) to steer the model’s behavior towards a desired outcome. To get the best results from the chatbot, further [prompt engineering](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api) may help.

See the two prompts we define for steps 1 and 3 above. You can always start with these and improve them for your own scenario.

```python
template = """Given the following chat history and a follow up question, rephrase the follow up input question to be a standalone question.
Or end the conversation if it seems like it's done.
Chat History:\"""
{chat_history}
\"""
Follow Up Input: \"""
{question}
\"""
Standalone question:"""

condense_question_prompt = PromptTemplate.from_template(template)

template = """You are a friendly, conversational retail shopping assistant. Use the following context including product names, descriptions, and keywords to show the shopper whats available, help find what they want, and answer any questions.

It's ok if you don't know the answer.
Context:\"""

{context}
\"""
Question:\"
\"""

Helpful Answer:"""

qa_prompt= PromptTemplate.from_template(template)

```

Next, we define two OpenAI LLMs and wrap them with chains for question generation and question answering respectively. The streaming_llm allows us to pipe the chatbot responses to stdout, token by token, giving it a charming, chatbot-like user experience.

```python
# define two LLM models from OpenAI
llm = OpenAI(temperature=0)

streaming_llm = OpenAI(
    streaming=True,
    callback_manager=CallbackManager([
        StreamingStdOutCallbackHandler()
    ]),
    verbose=True,
    max_tokens=150,
    temperature=0.2
)

# use the LLM Chain to create a question creation chain
question_generator = LLMChain(
    llm=llm,
    prompt=condense_question_prompt
)

# use the streaming LLM to create a question answering chain
doc_chain = load_qa_chain(
    llm=streaming_llm,
    chain_type="stuff",
    prompt=qa_prompt
)


```

Finally, we tie it all together with the ConversationalRetrievalChain that wraps all three steps.

```python
chatbot = ConversationalRetrievalChain(
    retriever=vectorstore.as_retriever(),
    combine_docs_chain=doc_chain,
    question_generator=question_generator
)

```

## Experiment with your friendly virtual shopping assistant

Keep in mind, this is *not* an all-intelligent being. But with the help of Redis, which stores the example’s entire product inventory knowledge base, we create a pretty neat experience.

```python
# create a chat history buffer
chat_history = []
# gather user input for the first question to kick off the bot
question = input("Hi! What are you looking for today?")

# keep the bot running in a loop to simulate a conversation
while True:
    result = chatbot(
        {"question": question, "chat_history": chat_history}
    )
    print("\n")
    chat_history.append((result["question"], result["answer"]))
    question = input()

```

The bot interacts with you in realtime, and helps you narrow in on interesting product choices based on what’s in the catalog. Here’s a simple example:

```
Hi! What are you looking for today?

>> gold-plated earrings

Hi there! I'm happy to help you find the perfect earrings. Do you have a preference for yellow gold plated sterling silver or platinum or gold-plated sterling silver?

>> My preference is the yellow gold plated sterling silver

Hi there! Are you looking for yellow gold-plated sterling silver earrings with Swarovski Zirconia or Topaz gemstones? We have a few options that might fit the bill. We have yellow gold-plated sterling silver Swarovski Zirconia fancy green stud earrings, yellow gold-plated sterling silver honey topaz stud earrings made with Swarovski Topaz gemstones, and yellow gold-plated sterling silver antique drop earrings set.

```

After the chatbot welcomes you with, “Hi! What are you looking for today?” try a few of these sample prompts, or make your own:

- Fancy earrings that are silver or gold
- Comfortable walking shoes
- A durable iPhone case

## Customize your chains for better performance

One of the best parts about LangChain is that each class abstraction is made so that you can extend or create your own. Below, we customize the BaseRetriever class to perform some document preprocessing before it returns the results.

```python
import json
from langchain.schema import BaseRetriever
from langchain.vectorstores import VectorStore
from langchain.schema import Document
from pydantic import BaseModel

class RedisProductRetriever(BaseRetriever, BaseModel):
    vectorstore: VectorStore

    class Config:
        arbitrary_types_allowed = True

    def combine_metadata(self, doc) -> str:
        metadata = doc.metadata
        return (
           "Item Name: " + metadata["item_name"] + ". " +
           "Item Description: " + metadata["bullet_point"] + ". " +
           "Item Keywords: " + metadata["item_keywords"] + "."
        )

    def get_relevant_documents(self, query):
        docs = []
        for doc in self.vectorstore.similarity_search(query):
            content = self.combine_metadata(doc)
            docs.append(Document(
                page_content=content,
                metadata=doc.metadata
            ))

        return docs

```

We need to update the retrieval class and chatbot to use the custom implementation above.

```python
redis_product_retriever = RedisProductRetriever(vectorstore=vectorstore)

chatbot = ConversationalRetrievalChain(
    retriever=redis_product_retriever,
    combine_docs_chain=doc_chain,
    question_generator=question_generator
)


```

Done! Now your chatbot can infuse more product information in your conversation as it steers you towards e-commerce glory! Here’s another short conversation example:

```
Hi! What are you looking for today?

>>> fancy footwear for going out

Hi there! We have a few great options for women's shoes and sandals. We have the Amazon Brand - The Fix Women's Giana Open Toe Bootie with Pearl Buckle, bright white leather, 9.5 B US, Flavia Women's Beige Fashion Sandals-7 UK (39 EU) (8 US) (FL/236/BEG), Flavia Women's Blue Fashion Sandals-8 UK (40 EU) (9 US) (FL/211/BLU), and The Fix Women's Faris Flat Slide Sandal with Pearls. All of these shoes feature a variety of styles and colors to choose from. Let me know if you have any questions about any of these items!

>>> These are nice. However, I am looking for men's shoes. Can you help me?

Hi there! We have a great selection of men's formal shoes available. We have Amazon Brand - Symbol Men's Formal Shoes, Amazon Brand - Symbol Men's Leather Formal Shoes, and more. All of our formal shoes are made from high quality materials and feature a variety of closure types, toe styles, and heel types. They also come with a manufacturer's warranty and care instructions to ensure they last. Let me know if you have any questions or need help finding the perfect pair of shoes for you!

>>>Can you show me some more men's options?

Hi there! I'm here to help you find the perfect item for you. We have a few options available for men's formal shoes. We have the Men's Stainless Steel Link Bracelet, the Amazon Brand - Arthur Harvey Men's Leather Formal Shoes, and the Amazon Brand - Symbol Men's Formal Derby shoes. All of these items feature a variety of features such as leather material, lace-up closure, pointed toe, block heel, and more. If you have any questions about any of these items, please let me know. I'm happy to help!

>>> Ok this looks great, thanks!

```

## Next steps

Building with LangChain and Redis is easy. Try building [this chatbot](https://github.com/RedisVentures/redis-langchain-chatbot) on your own, or customizing it for your use case. [Try Redis Enterprise for free](/try-free/) or pull our [Redis Stack docker container](https://redis.io/docs/stack/get-started/install/docker/) to get started.

Interested in getting your hands dirty with AI? Our partners at LabLab AI are hosting [a series of hackathons](https://lablab.ai/event) over the next month featuring Redis. Compete for prizes, hype, and fame. In fact, [there’s a hackathon with Stable Diffusion](https://lablab.ai/event/stable-diffusion-ai-hackathon) starting April 14th!

![Stable diffusion AI hackathon promo image](/images/site-mirror/3465e0a91ccc40732678364c9d6bfa3e7ff2d054-1600x900.webp)

Like what you’re hearing about Generative AI from Tyler and Harrison? See them share more practical examples during their joint session at [RedisDays Virtua](/redisdays/virtual/)l, a free virtual event on May 24th.

Learn more about [Vector Similarity Search](/solutions/vector-search/) in Redis. You may be amazed by what you can accomplish.
