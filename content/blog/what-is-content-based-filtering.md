---
title: "What is content-based filtering? A guide to building recommender systems"
linkTitle: "What is content-based filtering? A guide to building recommender systems"
url: "/blog/what-is-content-based-filtering/"
description: "Users like options, but too many options can lead to analysis paralysis."
date: 2025-01-31
blogCategories:
- "Benchmarks"
- "Tech"
authors:
- "Justin Cechmanek"
lastmod: 2026-06-01
hidden: true
---

*By Justin Cechmanek, Senior Applied AI Engineer · Published 31 January 2025 · updated 1 June 2026*

![Blog tile image](/images/site-mirror/6b2b5fbe2b0b0c19fef73a666f13fe2a6bdad876-772x552.webp)

Users like options, but too many options can lead to analysis paralysis.

That’s where recommender systems come in. These tools have come a long way, making it easier for businesses to offer plenty of options without overwhelming their users. It’s the best of both worlds: variety without the decision fatigue.

Let’s unpack content-based filtering (a core part of many types of recommender systems), explain the data science techniques that make it work, dig into its advantages and disadvantages, and walk through a tutorial that will show you how to build personalized recommendations with Redis. [You can clone the repo here](https://github.com/redis-developer/redis-ai-resources/blob/main/python-recipes/recommendation-systems/00_content_filtering.ipynb).

## What is content-based filtering?

Content-based filtering is a recommendation technique that uses machine learning to suggest items to users based on the features (i.e., the content) of those items. A recommender system using content-based filtering analyzes item features and user preferences to build a user profile that the system can match to new items that suit the user profile.

Content-based filtering methods break users and items down into metadata. IMDB’s recommender system might, for example, break out movies by genre tags, such as comedy, horror, or romance. It also captures information on user behavior, like the movies you click on or the search terms you’re using right now, building a user profile to keep those recommendations relevant and to support ongoing recommendations.

Metadata is the foundation of content-based filtering, but recommender algorithms are where the magic happens.

Many recommender systems rely on a k-Nearest Neighbors (k-NN) model. This machine learning model finds the nearest data points (i.e., neighbors) to a given input and makes predictions based on the properties of those neighbors. In the IMDB example, a k-NN model would know that a given user clicked on a movie listing with “fast-paced,” “ensemble cast,” and “PG rating” and then recommend a new movie listing with similar attributes.

Of course, this basic data science approach isn’t just for movies:

- An ecommerce clothing retailer might recommend joggers because a user previously bought sweatpants.
- A social media network might recommend posts on a given topic because a user clicked through and engaged with similar posts.
- A data analytics dashboard might recommend a new template because a business user has downloaded similar ones in the past.

Content-based filtering isn’t without its limitations, so it’s often combined with collaborative filtering.

## Content-based filtering vs. collaborative filtering

Recommender systems that exclusively use content-based filtering techniques tend to be limited by the scope and quality of available metadata.

When the metadata is limited, even the best algorithm can fall flat. Recommendations might miss the mark, feeling unconvincing or irrelevant. And if the metadata lacks depth, the system will likely serve up overly similar suggestions that leave users bored and uninspired.

For these reasons (among others, which we’ll get into in the next section), companies turn to collaborative filtering — either to replace content-based filtering or to complement it.

Collaborative filtering methods rely on user interactions, such as user ratings, user likes, or purchases, to make recommendations. The recommender system allows users to “collaborate” with each other via implicit feedback. It then leverages feedback from other users to make informed recommendations.

For example, if someone rates a movie highly or consistently buys and reviews certain clothing brands, a collaborative filtering system will recommend those movies and brands to similar users.

## Why content-based filtering works—and where it falls short

Content-based filtering comes with its own set of tradeoffs, but many of these can be balanced out by combining it with a hybrid recommender system that adds collaborative filtering. Either way, if you’re building a recommender system, you need to know how to leverage the advantages and get ahead of the disadvantages.

### Advantages

Content-based filtering has numerous advantages that make it a core part of many recommender systems:

- Personalized recommendations tailored to individual user preferences–including likes and dislikes–can help companies create a better user experience that leads to higher conversion rates.
- Recommending items based on the content of the items addresses what’s known as the cold-start problem, allowing even new users to receive personalized recommendations.
- These recommendations can still happen independent of any particular user data or user behaviors.

Content-based filtering often succeeds or struggles depending on the quality and breadth of your metadata. The richer the metadata, the easier it is to implement content-based filtering and the better the results.

### Disadvantages

Content-based filtering has a few limitations, some of which are harder to get around than others.

- Content-based filtering can sometimes create “filter bubbles,” (as they’re called on social media), where recommendations feel repetitive or overly narrow because the system focuses too much on the small set of items a user has interacted with.
- Sparse or poor-quality metadata can limit the effectiveness of content-based filtering because the recommendations can only be as good or as diverse as the metadata.
- Unlike collaborative filtering, content-based filtering doesn’t benefit from network effects or social proof.

Content-based filtering can also struggle in domains with complex or unstructured content, such as images, music, or videos. But if you have feature extraction methods, such as computer vision or vision-based LLM models, you can turn this disadvantage into an advantage using tools such as [RedisVL](https://github.com/redis/redis-vl-python).

## Use cases for content-based filtering

Content-based filtering is widely used across industries and use cases because the benefit of near-infinite options risks becoming a burden without personalized filtering and recommendations. That’s why, when you look closely, you can find content-based filtering almost everywhere you look online. Let’s explore a few use cases:

- **Ecommerce platforms**: Online retailers (whether on their own platform or a platform like Amazon or Shopify) often use content-based filtering to [recommend users new products](/blog/real-time-product-recommendation-docarray/) based on the products they’ve previously purchased.
- **Media streaming services**: Streaming services, such as Netflix, benefit from engaging users on their platforms for as long as possible, so these services often use content-based filtering to suggest movies, TV shows, or music based on the genres and artists users have already enjoyed.
- **Educational platforms**: With the rise of massive open online courses (MOOCs) and the popularity of industry-specific boot camps, such as coding boot camps, content-based filtering has become a useful way for educational platforms to recommend courses and resources based on a user’s learning history and preferences.
- **Healthcare applications**: There’s a huge variety of treatments, diets, and exercises available online, but not all of them work for all bodies, healthcare apps use the information they have on user preferences to recommend new exercise regimens or recipes.

In a physical store, business owners have limited space to show customers new products. Online, companies can show many more options as long as they use the right recommender system to help users find the choices that suit them best.

## How to build a content-based filtering recommendation engine with Redis

With Redis, building a content-based filtering system is easy. Here, we’ll walk through how to build a movie recommendation system supported by content-based filtering using [RedisVL](https://redis.io/docs/latest/integrate/redisvl/) and the IMDB movie dataset. [You can clone the repo here](https://github.com/redis-developer/redis-ai-resources/blob/main/python-recipes/recommendation-systems/00_content_filtering.ipynb).

At a high level, we’ll use RedisVL to generate a semantic embedding vector from each movie’s title, description, and keywords and then store and query vectors with vector similarity search to find semantically similar movies. We’ll then use additional fields, such as genre and release year, to enhance the results.

### Set up your environment

Start by importing the needed libraries and defining your Redis URL.

Python

```python
import pandas as pd
import ast
import os
import pickle
import requests

# Replace values below with your own if using Redis Cloud instance
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

# If SSL is enabled on the endpoint, use rediss:// as the URL prefix
REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"


```

### Load and preprocess the dataset

We’re using a dataset of approximately 25,000 movies from IMDB. As with any data task, the first step is to clean our data. This includes filling in missing values, converting certain fields into lists, and removing unnecessary columns.

Python

```python
try:
   df = pd.read_csv("datasets/content_filtering/25k_imdb_movie_dataset.csv")
except:
   # download the file
   url = 'https://redis-ai-resources.s3.us-east-2.amazonaws.com/recommenders/datasets/content-filtering/25k_imdb_movie_dataset.csv'
   r = requests.get(url)

   #save the file as a csv
   if not os.path.exists('./datasets/content_filtering'):
       os.makedirs('./datasets/content_filtering')
   with open('./datasets/content_filtering/25k_imdb_movie_dataset.csv', 'wb') as f:
       f.write(r.content)
   df = pd.read_csv("datasets/content_filtering/25k_imdb_movie_dataset.csv")


```

Python

```python
roman_numerals = ['(I)','(II)','(III)','(IV)', '(V)', '(VI)', '(VII)', '(VIII)', '(IX)', '(XI)', '(XII)', '(XVI)', '(XIV)', '(XXXIII)', '(XVIII)', '(XIX)', '(XXVII)']

def replace_year(x):
   if x in roman_numerals:
       return 1998 # the average year of the dataset
   else:
       return x

df.drop(columns=['runtime', 'writer', 'path'], inplace=True)


```

Python

```python
df['year'] = df['year'].apply(replace_year)             # replace roman numerals with average year
df['genres'] = df['genres'].apply(ast.literal_eval)     # convert string representation of list to list
df['keywords'] = df['keywords'].apply(ast.literal_eval) # convert string representation of list to list
df['cast'] = df['cast'].apply(ast.literal_eval)         # convert string representation of list to list
df = df[~df['overview'].isnull()]                       # drop rows with missing overviews
df = df[~df['overview'].isin(['none'])]                 # drop rows with 'none' as the overview


```

### Generate vector embeddings to recommend similar content

The heart of our recommendation system is determining the similarity between movies based on their descriptions. To do this, we use [a pre-trained language model from HuggingFace](https://huggingface.co/sentence-transformers/paraphrase-MiniLM-L6-v2) to generate [vector embeddings](https://redis.io/glossary/vector-embeddings/) for each movie’s overview and keywords. This step will take a while, but it only needs to be done once for your entire dataset.

If you don’t want to wait, you can skip this cell and load the vectors we’ve gone ahead and pre-generated to a file for you.

Python

```python
# add a column to the dataframe with all the text we want to embed
df["full_text"] = df["title"] + ". " + df["overview"] + " " + df['keywords'].apply(lambda x: ', '.join(x))

from redisvl.utils.vectorize import HFTextVectorizer

vectorizer = HFTextVectorizer(model = 'sentence-transformers/paraphrase-MiniLM-L6-v2')

df['embedding'] = df['full_text'].apply(lambda x: vectorizer.embed(x, as_buffer=False))
pickle.dump(df['embedding'], open('datasets/content_filtering/text_embeddings.pkl', 'wb'))


```

Python

```python
try:
    with open('datasets/content_filtering/text_embeddings.pkl', 'rb') as vector_file:
        df['embedding'] = pickle.load(vector_file)
except:
    embeddings_url = 'https://redis-ai-resources.s3.us-east-2.amazonaws.com/recommenders/datasets/content-filtering/text_embeddings.pkl'
    r = requests.get(embeddings_url)
    with open('./datasets/content_filtering/text_embeddings.pkl', 'wb') as f:
        f.write(r.content)
    with open('datasets/content_filtering/text_embeddings.pkl', 'rb') as vector_file:
        df['embedding'] = pickle.load(vector_file)


```

### Define our Redis Search schema

Next, we define a schema for RedisVL to specify the fields that each movie will have, including the vector dimensions, distance metric, and any additional fields like year, genre, or rating. We’ll load this from a yaml file, content_filtering_schema.yaml.

Unset

```
index:
    name: movies_recommendation
    prefix: movie
    storage_type: json

fields:
    - name: title
      type: text
    - name: rating
      type: numeric
    - name: rating_count
      type: numeric
    - name: genres
      type: tag
    - name: overview
      type: text
    - name: keywords
      type: tag
    - name: cast
      type: tag
    - name: writer
      type: text
    - name: year
      type: numeric
    - name: full_text
      type: text

    - name: embedding
      type: vector
      attrs:
          dims: 384
          distance_metric: cosine
          algorithm: flat
          dtype: float32

```

Python

```python
movie_schema = IndexSchema.from_yaml("content_filtering_schema.yaml")
index = SearchIndex(movie_schema, redis_client=client)
index.create(overwrite=True, drop=True)

data = df.to_dict(orient='records')
keys = index.load(data)

```

### Look for movie recommendations with vector similarity search

Now that our data is stored in Redis, we can use vector similarity search to find movies that are similar to one another. For example, to find movies similar to the classic “*20,000 Leagues Under the Sea*”, we retrieve its vector embedding and use it to search for similar movies.

Python

```python
from redisvl.query import RangeQuery

query_vector = df[df['title'] == '20,000 Leagues Under the Sea']['embedding'].values[0]

query = RangeQuery(vector=query_vector,
                    vector_field_name='embedding',
                    num_results=3,
                    distance_threshold=0.7,
                    return_fields = ['title', 'overview', 'vector_distance'])

results = index.query(query)


```

Here’s what the query results will look like.


Python

```python
[{'id': 'movie:b64fc099d6af440a891e1dd8314e5af7',
 'vector_distance': '0.584870040417',
 'title': 'The Odyssey',
 'overview': 'The aquatic adventure of the highly influential and fearlessly ambitious pioneer, innovator, filmmaker, researcher, and conservationist, Jacques-Yves Cousteau, covers roughly thirty years of an inarguably rich in achievements life.'},

{'id': 'movie:2fbd7803b51a4bf9a8fb1aa79244ad64',
 'vector_distance': '0.63329231739',
 'title': 'The Inventor',
 'overview': 'Inventing flying contraptions, war machines and studying cadavers, Leonardo da Vinci tackles the meaning of life itself with the help of French princess Marguerite de Nevarre.'},

{'id': 'movie:224a785ca7ea4006bbcdac8aad5bf1bc',
 'vector_distance': '0.658123672009',
 'title': 'Ruin',
 'overview': 'The film follows a nameless ex-Nazi captain who navigates the ruins of post-WWII Germany determined to atone for his crimes during the war by hunting down the surviving members of his former SS Death Squad.'}]

```

### Add filters to improve recommendations

In real-world recommendation systems, users often like to apply their own filters—like narrowing down by genre or searching with specific keywords. We can easily expand our system to include filters for these (or any other fields) set up in our schema.

There’s no one-size-fits-all approach to adding these filters because every content recommendation app will have different fields, which is why Redis supports a full host of filter types, including [tags](https://www.redisvl.com/api/filter.html#:~:text=%7C%20None)-,Tag,-%23), [text fuzzy matching](https://www.redisvl.com/api/filter.html#:~:text=str-,Text,-%23), [numeric ranges](https://www.redisvl.com/api/filter.html#:~:text=str-,Num,-%23), and [geo radius](https://www.redisvl.com/api/filter.html#:~:text=str-,GeoRadius,-%23). Try playing around with adding filters to other fields defined in our schema to see how the results change.

Python

```python
from redisvl.query.filter import Tag, Num, Text

def make_filter(genres=None, release_year=None, keywords=None):
    flexible_filter = (
        (Num("year") > release_year) &  # only show movies released after this year
        (Tag("genres") == genres) &     # only show movies that match at least one in list of genres
        (Text("full_text") % keywords)  # only show movies that contain at least one of the keywords
    )
    return flexible_filter

def get_recommendations(movie_vector, num_results=5, distance=0.6, filter=None):
    query = RangeQuery(vector=movie_vector,
                        vector_field_name='embedding',
                        num_results=num_results,
                        distance_threshold=distance,
                        return_fields = ['title', 'overview', 'genres'],
                        filter_expression=filter,
                        )

    recommendations = index.query(query)
    return recommendations


```

## Get started with RedisVL

Now, you know the basics of content-based filtering, the advantages and disadvantages of this technique, a range of use cases for adopting it, and how to build a content-based recommendation system yourself using RedisVL.

With the power of Redis as a vector database, you can generate relevant recommendations that improve the user experience and boost conversion rates (among many other benefits). Whether you’re recommending products, music, movies, or books, the flexibility and performance of RedisVL make it an excellent choice for building scalable recommender systems.

[Try Redis for free.](https://redis.io/try-free/)
