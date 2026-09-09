---
title: "How To Build a Real-Time Product Recommendation System Using Redis and DocArray"
linkTitle: "How To Build a Real-Time Product Recommendation System Using Redis and DocArray"
url: "/blog/real-time-product-recommendation-docarray/"
description: "This tutorial helps you build a real-time product recommendation system for an e-commerce system using content-based filtering and vector similarity search. Follow along to learn the essential..."
date: 2022-11-08
blogCategories:
- "How To and Tutorials"
- "Tech"
authors:
- "Alaeddine Abdessalem"
lastmod: 2026-06-01
hidden: true
---

*By Alaeddine Abdessalem, Contributor · Published 8 November 2022 · updated 1 June 2026*

![Blog tile image](/images/site-mirror/5a4a696217f9bb0f3a70359401a425b309192048-772x550.webp)

**This tutorial helps you build a real-time product recommendation system for an e-commerce system using content-based filtering and vector similarity search. Follow along to learn the essential steps and how it works.**

Recommendation systems are an important technology for most online businesses and for [e-commerce sites](/industries/retail/) in particular. They’re an essential element in generating good conversion and maintaining customer loyalty.

A recommendation system typically shows items to users based on their profiles and preferences and by observing their actions (such as buying, liking, or viewing items).

![diagram of a phone app](/images/site-mirror/d2548071c5c85870f580233d5f09c9c385c494ec-720x434.webp)

Consider the challenges involved in building a recommendation system for a modern e-commerce site. This is just a subset of the issues to consider:

- **Customization:** Customers want to filter results, such as by price range, brand, and size. Our system should recommend products only within these parameters.
- **Multiple modalities:** A product listing is more than a text description. It can also contain images, video, audio, and 3D mesh, for example. All available data modalities should be exploited when making recommendations.
- **Latency:** Customers expect recommendations to appear quickly. If the system’s recommendations aren’t returned immediately, they’re irrelevant.
- **Data volume:** The more products and customers the site has, the harder it is to recommend products efficiently. Computing recommendations should stay fast even with big datasets.

As these requirements evolve, approaches to building recommendation systems need to evolve as well. In this blog post, we show you how to build a real-time product recommendation system with respect to user-defined filters using the latest [vector search technology](https://redis.io/docs/stack/search/reference/vectors/). The tool suite includes Redis and DocArray, but the methodology is relevant no matter which tools you employ.

## Recommendation systems basics

As with any other computing problem, there are multiple approaches to building recommendation systems and tools to support each effort. They include:

- **Collaborative filtering:** The system predicts items relevant to the user based on the preferences of similar users.
- **Content-based filtering:** The system models the user’s interests as feature vectors and predicts relevant items based on the similarity between vectors.
- **Hybrid approaches:** The system combines collaborative filtering, content-based filtering, and other approaches.

This blog post focuses on improving the content-based filtering approach. If you’re new to this topic, it may help to read [Google’s overview](https://developers.google.com/machine-learning/recommendation/content-based/basics) of content-based filtering first.

There are two important considerations when implementing content-based filtering:

First, when you model the user and items as a feature vector, it’s important to exploit all modalities of the data. Simply relying on keywords or a set of engineered features might not efficiently represent complex data.

That’s why state-of-the-art [AI](/modules/redis-ai/) models are important, as they represent complex, multimodal data as vector embeddings.

One of the best-known models to represent both text and image data is[ CLIP](https://github.com/openai/CLIP). Therefore, in this tutorial, we use[ CLIP-as-service](https://clip-as-service.jina.ai/) as the inference engine that powers our recommendations.

Also, computing vector similarity can be slow and costly if not performed efficiently. Our application requirements (to respect user filters and deliver low-latency recommendations) make it impractical to pre-compute similarity between items and user profiles in batch jobs. That’s why it’s crucial to compute vector similarity in real-time, using efficient techniques such as Hierarchical Navigable Small World[ (HNSW)](https://arxiv.org/abs/1603.09320).

These techniques are implemented in vector databases. Redis offers vector search capabilities in[ RediSearch](/search/) 2.4. And since Redis is an in-memory database, recommending items is both fast and performed in a real-time context.

With feature representation and computing vector similarity covered, we still need a data structure to bridge the gap between our multimodal data and the vector database. For that, we use[ DocArray](http://docarray.jina.ai/). Think of DocArray as a universal [vector database](/solutions/vector-search/) client with support for multimodal data. It has a Pythonic interface that makes it easy to build a recommendation system in just a few lines of code.

![docarray ingestion](/images/site-mirror/69c9122d6498e657187e0413a4fcc99819e6fe7e-1999x1220.webp)

## Designing the solution

We have assembled the tools for this application: Redis for Vector Similarity Search, CLIP-as-service to encode visual data, and DocArray to represent multimodal documents and connect to Redis. In this tutorial, we apply these technologies to build a content-based filtering recommendation system.

The procedure is as follows:

- Load the dataset into DocArray format.
- Model products by encoding product images using CLIP-as-service.
- Model the user profile by computing the weighted average of the last *k* viewed products’ embeddings.
- Use DocArray to load the product data.
- Index the product data in Redis.
- Use [Redis Vector Similarity Search ](/blog/rediscover-redis-for-vector-similarity-search/)to recommend the most similar items to the user’s view history while also filtering those results to respect user preferences.

In the instruction that follows, the data we use for product recommendations comes from the[ Amazon Berkeley Objects Dataset](https://amazon-berkeley-objects.s3.amazonaws.com/index.html), a dataset of Amazon products with metadata, catalog images, and 3D models.

## Setup

The first step is to provision a Redis instance. You can create a local Redis instance using Docker:

```bash
docker run -d -p 6379:6379 redis/redis-stack:latest

```

Next, we need to install DocArray, [Jina](https://docs.jina.ai/), and clip-client:

```bash
pip install docarray[redis] jina clip-client

```

That’s all the setup we need. Now we’re ready to start exploring with data.

## Dataset exploration

The Amazon Berkeley Objects Dataset consists of product items accompanied by images and metadata such as brand, country, and color. It represents the inventory of an e-commerce website.

![nia and nicole womens wallet](/images/site-mirror/8abe311e50e090c3a19bd0067bca6713c4901eeb-697x268.webp)

For the purposes of this tutorial, we can download a subset of this dataset from Jina Cloud, pre-processed in DocArray format.

First, authenticate to Jina Cloud using the terminal:

```bash
jina auth login

```

Next, download the dataset:

```python
from docarray import DocumentArray, Document
da = DocumentArray.pull('amazon-berkeley-objects-dataset', show_progress=True)

```

This returns a[ DocumentArray](https://docarray.jina.ai/fundamentals/documentarray/) object containing samples from the Amazon Berkeley Objects dataset. We get an overview using the summary() method:

```
da.summary()

```

```
╭────────────────────── Documents Summary ──────────────────────╮
│                                                               │
│   Type                   DocumentArrayInMemory                │
│   Length                 **5809**                                 │
│   Homogenous Documents   *True*                                 │
│   Common Attributes      **(**'id', 'mime_type', 'uri', 'tags'**)**   │
│   Multimodal dataclass   *False*                                │
│                                                               │
╰───────────────────────────────────────────────────────────────╯
╭───────────────────── Attributes Summary ─────────────────────╮
│                                                              │
│   **Attribute**   **Data type**   **#Unique values**   **Has empty value**   │
│  ──────────────────────────────────────────────────────────  │
│   id          **(**'str',**)**    **5809**             *False*             │
│   mime_type   **(**'str',**)**    **1**                *False*             │
│   tags        **(**'dict',**)**   **5809**             *False*             │
│   uri         **(**'str',**)**    **4848**             *False*             │
│                                                              │
╰──────────────────────────────────────────────────────────────╯

```

Or we can display the images of the first items using the [plot_image_sprites()](<https://docarray.jina.ai/api/docarray.array.document/#docarray.array.document.DocumentArray.plot_image_sprites>) method.

```python
da[:12].plot_image_sprites()

```

![product catalog items](/images/site-mirror/1d6c8b44879dc456a12741bd9b8949f6d475a1ff-734x554.webp)

Each product contains the metadata information in the tags field.

Let’s take a look at the content of tags:

```python
da[0].tags

```

```
{'height': '1926',
 'country': 'CA',
 'width': '1650',
 'product_type': 'ACCESSORY',
 'color': 'Blue',
 'brand': 'Thirty Five Kent',
 'item_name': "Thirty Five Kent Men's Cashmere Zig Zag Scarf, Blue"}

```

Later, we use this metadata to filter recommendations according to the user’s preferences.

## Adding embeddings

To create the vector embeddings for our dataset, we first need a token for CLIP-as-service inference:

```
# Create a Jina token to be used for CLIP-as-service inference
jina auth token create fashion -e 30

```

Then we can start to encode the data. Be sure to pass the created token to the Client object:

```python
from clip_client import Client

c = Client(
    'grpcs://api.clip.jina.ai:2096', credential={'Authorization': 'your-auth-token'}
)

encoded_da = c.encode(da, show_progress=True)

```

Encoding the dataset takes a few minutes. When it’s done, we proceed with the next steps.

## Connecting to Redis

At this point, our data is encoded and ready to index.

To do so, we create a DocumentArray instance connected to our Redis server. It’s important to specify the correct embedding dimensions and filter columns:

```python
# Configure a new DocumentArray with a Redis document store
redis_da = DocumentArray(storage='redis', config={
    'n_dim': 768,
    'columns': {
        'color': 'str',
        'country': 'str',
        'product_type': 'str',
        'width': 'int',
        'height': 'int',
        'brand': 'str',
    }
})

# Index data
redis_da.extend(encoded_da

```

For more information, see[ Redis Document Store](https://docarray.jina.ai/advanced/document-store/redis/) in DocArray.

## Generating recommendations

In order to understand the recommendation logic, consider the following example: Eleanor decided to add a scarf to her wardrobe and looked into several ones in our shop. Her favorite color is navy, and she has to keep the budget under $25.

Our recommendation function should allow specifying those requirements and recommend items based on the view history, with emphasis on the most recently viewed items.

Thus, we combine embeddings of the latest viewed items by giving more weight to the recent items:

Let’s implement a function that recommends products based on a weighted average of the embeddings of recently-viewed items, taking user filters into account. That is, in recommended items, we want to emphasize the items the shopper viewed most recently.

Thus, we combine embeddings of the latest viewed items by giving more weight to the recent items:

```python
import numpy as np

def recommend(view_history, color=None, country=None):
    embedding = np.average(
        [doc.embedding for doc in view_history],
        weights=range(len(view_history), 0, -1),
        axis=0
    )

    user_filter = ''
    
    if color:
        user_filter += f'@color:{color} '
    
    if country:
        user_filter += f'@country:{country} '
    
    return redis_da.find(embedding, filter=user_filter)

```

## Adding recommendations to product views

To show relevant recommendations when a customer views a product, we need three steps:

1. Show the product’s image and description.
1. Add the product to the list of last *k* viewed products.
1. Show recommendations related to the last *k* viewed products.

We can achieve that with the following function:

```python
k = 5
view_history = []

def view(item: Document, view_history, color=None, country=None):
    print(item.tags['item_name'], ':')
    item.display()
    view_history.insert(0, item)
    view_history = view_history[:k]
    recommendations = recommend(view_history, color=color, country=country)
    recommendations.plot_image_sprites()
    return recommendations

```

## Viewing the results

Let’s try it out a few times. First, let’s view the first item in the store and the recommendations for it:

```python
recommended = view(redis_da[0], view_history

```

That displays an attractive scarf, labeled as ” Thirty-Five Kent Men’s Cashmere Zig Zag Scarf, Blue”:

![gray scarf](/images/site-mirror/a13e60b94e811b04133c0c983df7b5c9e1ba8ac0-219x256.webp)

… and the accompanying recommendations:

![assortment of scarves](/images/site-mirror/56d1cae73409ea14340c587e63745274200e72b7-734x590.webp)

How well do they meet the user’s filter?

Let’s check the third item in the recommendation list and apply a filter color=’Navy‘ to ensure a better match:

```python
recommended = view(recommended[2], view_history, color='Navy')

```

…which generates a better item display and recommendations:

Thirty-Five Kent Men’s Cashmere Zig Zag Scarf, Blue:

![navy scarf](/images/site-mirror/52693fc798e29395ead834d92eec79027b68abb2-166x256.webp)

![digital store clothing items](/images/site-mirror/fddecfdd35455a924398068102e2df46837cd71b-734x590.webp)

Now the recommendation function returns the most visually similar items to scarves that also satisfy the filter color='Navy'.

Success! And, possibly, a new e-commerce sale.

## Putting it all together

The instructions above are a brief overview to demonstrate the building blocks for a process to recommend products in an online store.

You’re welcome to take it further. We created a [GitHub repository](https://github.com/jina-ai/product-recommendation-redis-docarray) with source code for a product store interface with the same dataset and technique we just showed.

![vector similarity search](/images/site-mirror/e4c25f811826111c03db921bb245a1e512817d51-1322x620.webp)

This demonstration just showed you how Vector Similarity Search can offer low-latency real-time recommendations that respect user preferences and filter selection.

But how fast is it? Let’s look at the latency numbers for recommendation queries. You can find logs in the command line console:

```
Retrieving products ... Retrieving products takes 0 seconds (0.01s)

```

This means computing recommendations takes about 10 milliseconds!

Of course, there’s still room for improvement, especially when it comes to quality. For example, we can come up with more sophisticated ways to model the user’s profile and interests. We could also incorporate more types of data, such as 3D mesh and video. That’s left as an exercise to the reader.

## Shopping for better answers

Vector Similarity Search is an essential technique for implementing recommendations in a real-time context.

Your next steps:

- Use state-of-the-art AI models to encode multimodal data into vector representations.
- Use a [vector database](/blog/vector-databases-101/) to compute vector similarity in a real-time context. For low latency, an in-memory database like Redis is ideal.
- Consult the[ Redis documentation](https://redis.io/docs/) for more information.

Use DocArray as a convenient data structure for handling multimodal data as well as for interfacing with the vector database. Consult the[ DocArray documentation](https://docarray.jina.ai) to get started and get connected with the [Redis AI/ML team](https://docs.google.com/forms/d/e/1FAIpQLSf7tc5V4DCcwM8x4iQU36TAoBoKVM35xrKVZTw_wyXhaLO_Qg/viewform/) for more information on Redis Vector Search.

Get started with the[ Redis Cloud free tier](/try-free/).
