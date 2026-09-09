---
title: "Building a Two Tower Recommendation System with RedisVL"
linkTitle: "Building a Two Tower Recommendation System with RedisVL"
url: "/tutorials/building-a-two-tower-recommendation-system-with-redis-vl/"
description: "Recommendation systems are a common application of machine learning and are widely used across industries, from e-commerce to music streaming platforms."
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> A two-tower recommendation system uses separate neural networks for users and items, training on interaction data to produce embedding vectors. Once trained, you store those embeddings in Redis and use [vector similarity search](/tutorials/howtos-solutions-vector-getting-started-vector) for real-time, personalized recommendations — no model inference at query time. This tutorial walks through building one with PyTorch and RedisVL, including location-aware filtering.

Recommendation systems are a common application of machine learning and are widely used across industries, from e-commerce to music streaming platforms.

## What will you learn?

- What the two-tower recommendation architecture is and why it outperforms content-based and collaborative filtering alone
- How to build and train a two-tower model using PyTorch
- How to generate user and item embeddings from raw features
- How to store embeddings in Redis and use [RedisVL](https://github.com/redis/redis-vl-python) for vector similarity search
- How to apply geo, time, and attribute filters on top of vector search for location-aware recommendations
- How to visualize recommendations on an interactive map

## What is the two-tower architecture?

A two-tower model (also called a dual-encoder model) is a deep learning architecture for recommendation systems. It uses two separate neural networks — one "tower" for users and one for items — that each learn to map raw features into a shared embedding space. During training, the model learns from user-item interaction data (views, purchases, ratings) so that users and items likely to interact end up with similar embeddings. At inference time, finding recommendations is just a nearest-neighbor vector search — which is exactly what Redis excels at.

The key advantage over simpler approaches: the model can generate embeddings for brand-new users or items using only their raw features, without retraining.

## Prerequisites

- Python 3.9+ with [PyTorch](https://pytorch.org/), [scikit-learn](https://scikit-learn.org/), [pandas](https://pandas.pydata.org/), and [Faker](https://faker.readthedocs.io/)
- [RedisVL](https://github.com/redis/redis-vl-python) Python client (`pip install redisvl`)
- A running Redis instance (local or [Redis Cloud](https://redis.io/cloud/))
- Familiarity with [vector search concepts](/tutorials/howtos-solutions-vector-getting-started-vector)

There are several architectures for building recommendation systems. In our previous blog posts we showed how to build two popular approaches that use different techniques. The first went over [content filtering with RedisVL](https://redis.io/blog/what-is-content-based-filtering/), where recommendations are based on an item's underlying features. Next, we showed [how RedisVL can be applied to build a collaborative filtering recommender](https://redis.io/blog/collaborative-filtering-how-to-build-a-recommender-system/), which uses user ratings to create personalized suggestions. If you haven't checked those out yet they're great places to start your journey into building recommender systems.

## What are the drawbacks of content filtering and collaborative filtering?

Content filtering is perhaps the most straightforward recommender architecture to get started with as all that is needed is data of the products you want to recommend. This means you can get started quickly, and results will be mostly what you expect. Users will be recommended items similar to what they've consumed before. The problem is that with this approach users can get trapped in content silos. In our previous example of using IMDB movies this means that once someone watches one action movie they may only be shown other action movies. They may have really enjoyed a good classic horror film too, but they'll never be recommended it until after they watch something similar. This chicken-and-egg problem is hard for content filtering systems to escape from.

Collaborative systems don't have this silo problem as they leverage other users' behaviors to make personalized recommendations. But they suffer from a different challenge, and that is, '_How do you recommend items to new users, or how do you consider new items that no one has seen yet?'_ Collaborative filters rely on existing user-item interactions to generate features for users and items, which means they can't naturally handle new entries. With each new interaction their ground truth interaction data changes so model retraining is needed often.

What we want is a way to simultaneously learn from existing user behaviors, but still be able to handle new users and items being added to the system. Two tower models can do just this.

In this post we 'll cover how to build a [two-tower recommendation system](https://cloud.google.com/blog/products/ai-machine-learning/scaling-deep-retrieval-tensorflow-two-towers-architecture) and compare it to other methods. We'll cover its strengths and how it solves the shortcomings of other approaches. To mix things up a bit, instead of using our movies dataset like the previous two examples, we'll look at brick & mortar restaurants in San Francisco as our items to recommend.

## How do you prepare the restaurant data?

This tutorial walks through how to build this architecture. You can check out a [notebook with these steps here](https://github.com/redis-developer/redis-ai-resources/blob/main/python-recipes/recommendation-systems/02_two_towers.ipynb). Be sure to have your Redis instance running. First, define some constants and helper methods to load our restaurant data into a pandas DataFrame. We'll be using a set of restaurant reviews in San Francisco. See the [original dataset](https://www.kaggle.com/datasets/jkgatt/restaurant-data-with-100-trip-advisor-reviews-each).

```python
import os
import requests
import pandas as pd
import json

# Replace values below with your own if using Redis Cloud instance
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"

def fetch_data(file_name):
    dataset_path = 'datasets/two_towers/'
    try:
        with open(dataset_path + file_name, 'r') as f:
            return json.load(f)
    except:
        url = 'https://redis-ai-resources.s3.us-east-2.amazonaws.com/recommenders/datasets/two-towers/'
        r = requests.get(url + file_name)
        if not os.path.exists(dataset_path):
            os.makedirs(dataset_path)
        with open(dataset_path + file_name, 'wb') as f:
            f.write(r.content)
        return json.loads(r.content.decode('utf-8'))

restaurant_data = fetch_data('factual_tripadvisor_restaurant_data_all_100_reviews.json')
restaurant_data = restaurant_data["restaurants"] # ignore count fields

df = pd.DataFrame(restaurant_data)
df.fillna('', inplace=True)
df.drop(columns=['region', 'country', 'tel','fax', 'email', 'website', 'address_extended', 'chain_name','trip_advisor_url'], inplace=True)
df['unique_name'] = df['name'] +' ' + df['address'] # some restaurants are chains or have more than one location
df.head()
```

Here's a peak at the data we're working with.

| name                                | address           | locality      | latitude  | longitude    | cuisine                                            | price | rating |
| ----------------------------------- | ----------------- | ------------- | --------- | ------------ | -------------------------------------------------- | ----- | ------ |
| 21st Amendment Brewery & Restaurant | 563 2nd St        | San Francisco | 37.782448 | \-122.392576 | \[Cafe, Pub Food, American, Burgers, Pizza\]       | 2     | 4.0    |
| Absinthe Brasserie & Bar            | 398 Hayes St      | San Francisco | 37.777083 | \-122.422882 | \[French, Californian, Mediterranean, Cafe, Ame... | 3     | 4.0    |
| Amber India Restaurant              | 25 Yerba Buena Ln | San Francisco | 37.785772 | \-122.404401 | \[Indian, Chinese, Vegetarian, Asian, Pakistani\]  | 2     | 4.5    |
| Americano                           | 8 Mission St      | San Francisco | 37.793620 | \-122.392915 | \[Italian, American, Californian, Pub Food, Cafe\] | 3     | 3.5    |
| Anchor & Hope                       | 83 Minna St       | San Francisco | 37.787848 | \-122.398812 | \[Seafood, American, Cafe, Chowder, Californian\]  | 3     | 4.0    |

If you wanted to build a content filtering system now would be a good time to extract the text from the reviews, join them together and generate semantic embeddings from them [like we did in our previous post](https://redis.io/blog/what-is-content-based-filtering/).

This would be a great approach, but to demonstrate the two tower architecture we won't use a pre-trained embedding model like we did with content filtering. Instead we'll use the other columns as our raw features — but first we will extract the numerical ratings from the reviews.

```python
import numpy as np

df['min_rating'] = df['reviews'].apply(lambda x: np.min([r["review_rating"] for r in x]))
df['max_rating'] = df['reviews'].apply(lambda x: np.max([r["review_rating"] for r in x]))
df['avg_rating'] = df['reviews'].apply(lambda x: np.mean([r["review_rating"] for r in x]))
df['stddev_rating'] = df['reviews'].apply(lambda x: np.std([r["review_rating"] for r in x]))
df['price'] = df['price'].astype(int)

# now take all the features we have and build a raw feature vector for each restaurant
numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
boolean_cols = df.select_dtypes(include=['bool']).columns
df[boolean_cols] = df[boolean_cols].astype(int)

df['feature_vector'] = df[numerical_cols.tolist() + boolean_cols.tolist()].values.tolist()
```

We now have feature vectors with 30 features for each restaurant. The next step is to construct our raw feature vectors for our users.

## How do you generate user features and interaction data?

We don't have publicly available user data to correspond with this list of restaurants, so instead we'll generate some using the popular testing tool Faker.

```python
from faker import Faker
from uuid import uuid4

fake = Faker()

def generate_user():
    return {
        "user_id": str(uuid4()),
        "name": fake.name(),
        "username": fake.user_name(),
        "email": fake.email(),
        "address": fake.address(),
        "phone_number": fake.phone_number(),
        "birthdate": fake.date_of_birth().isoformat(),
        "likes": fake.random_elements(elements=['burgers', 'shakes', 'pizza', 'italian', 'mexican', 'fine dining', 'bbq', 'cocktails', 'breweries', 'ethiopian', 'pasta', 'brunch','fast food'], unique=True),
        "account_created_on": fake.date() ,
        "price_bracket": fake.random_element(elements=("low", "middle", "high")),
        "newsletter": fake.boolean(),
        "notifications": fake.boolean(),
        "profile_visibility": fake.random_element(elements=("public", "private", "friends-only")),
        "data_sharing": fake.boolean()
    }

users = [generate_user() for _ in range(1000)]
users_df = pd.DataFrame(users)
```

| user_id                              | name            | username        | email                        | address                                          | phone_number       | birthdate  | likes                                              | account_created_on | price_bracket | newsletter | notifications | profile_visibility | data_sharing |
| ------------------------------------ | --------------- | --------------- | ---------------------------- | ------------------------------------------------ | ------------------ | ---------- | -------------------------------------------------- | ------------------ | ------------- | ---------- | ------------- | ------------------ | ------------ |
| 2d72a59b-5b12-430f-a5c3-49f8b093cb3d | Kayla Clark     | debbie11        | teresa54@example.net         | 8873 Thompson Cape Osborneport, NV 34895         | 231.228.4452x008   | 1982-06-10 | \[pizza, pasta, shakes, brunch, bbq, ethiopian,... | 2017-04-18         | middle        | True       | True          | public             | True         |
| 034b2b2f-1949-478d-abd6-add4b3275efe | Leah Hopkins    | williamsanchez  | darryl77@example.net         | 353 Kimberly Green Roachfort, FM 34385           | 4669094632         | 1999-03-07 | \[brunch, ethiopian, breweries\]                   | 1970-06-21         | low           | False      | True          | public             | False        |
| 5d674492-3026-4cc9-b216-be675cf8d360 | Mason Patterson | jamescurtis     | lopezchristopher@example.com | 945 Bryan Locks Suite 200 Valenzuelaburgh, MI... | 885-983-4573       | 1914-02-14 | \[cocktails, fine dining, pizza, shakes, ethiop... | 2013-03-10         | high          | False      | False         | friends-only       | False        |
| 61e17d13-9e18-431f-8f06-208bd0469892 | Aaron Dixon     | marshallkristen | becky20@example.org          | 42388 Russell Harbors Suite 340 North Andrewc... | 448.270.3034x583   | 1959-05-01 | \[breweries, cocktails, fine dining\]              | 1973-12-11         | middle        | False      | True          | private            | True         |
| 8cc208b6-0f4f-459c-a8f5-31d3ca6deca6 | Loretta Eaton   | phatfield       | aaustin@example.org          | PSC 2899, Box 5115 APO AE 79916                  | 663-371-4597x72295 | 1923-07-02 | \[brunch, italian, bbq, mexican, burgers, pizza\]  | 2023-04-29         | high          | True       | True          | private            | True         |

Now, create our raw user feature vectors.

```python
from sklearn.preprocessing import MultiLabelBinarizer

# use a MultiLabelBinarizer to one-hot encode our user's 'likes' column, which has a list of users' food preferences
mlb = MultiLabelBinarizer()

likes_encoded = mlb.fit_transform(users_df['likes'])
likes_df = pd.DataFrame(likes_encoded, columns=mlb.classes_)

users_df = pd.concat([users_df, likes_df], axis=1)

categorical_cols = ['price_bracket', 'profile_visibility']
users_df = pd.get_dummies(users_df, columns=categorical_cols)

boolean_cols = users_df.select_dtypes(include=['boolean']).columns
users_df[boolean_cols] = users_df[boolean_cols].astype(int)

# combine all numerical columns into a single feature vector
numerical_cols = users_df.select_dtypes(include=['int64', 'uint8']).columns
users_df['feature_vector'] = users_df[numerical_cols].values.tolist()
```

Because two tower models are also trained on interaction data like our SVD collaborative filtering model we need to generate some purchases. This will be a 1 or -1 to indicate if a user has eaten at this restaurant before. Once again we're generating random labels for this example to go along with our random users.

```python
import random

user_ids = users_df['user_id'].tolist()
restaurant_names = df["unique_name"].tolist()

# generate purchases by randomly selecting users and businesses
purchases = [
    (user_ids[random.randrange(0, len(user_ids))],
     restaurant_names[random.randrange(0, len(restaurant_names))]
    )
    for _ in range(200)
]

positive_labels = []
for i in range(len(purchases)):
    user_index = users_df[users_df['user_id'] == purchases[i][0]].index.item()
    restaurant_index = df[df['unique_name'] == purchases[i][1]].index.item()
    positive_labels.append((user_index, restaurant_index, 1.))

# generate an equal number of negative examples
negative_labels = []
for i in range(len(purchases)):
    user_index = random.randint(0, len(user_ids)-1)
    restaurant_index = random.randint(0, len(restaurant_names)-1)
    negative_labels.append((user_index, restaurant_index, -1.))

labels = positive_labels + negative_labels
```

Now we have all of our data. The next steps are to define the model and train it.

## How does a two-tower model work?

Two tower models consider the item features as well as user features to make recommendations. They also are trained on user/item interactions like views, likes, or purchases, but once trained are still able to make personalized recommendations to brand new users and with brand new items. They can do this because they are deep learning models that learn embedding representations of users and content by being trained on a subsample of data. They are inductive ML models, which means they can form general rules from samples of data and apply those rules to never-before-seen data. With a trained model you can take a brand new set of users and a brand new set of items and predict their likelihood of interaction. It doesn't matter if your model has seen this exact user or item before.

A typical two tower model architecture can look like this:

![Architecture diagram of a two-tower recommendation system showing separate user and item neural network towers that produce embeddings compared via cosine similarity](/images/site-mirror/be5b5fa034b62eb79df8c582ec1ad50bbe3abcad-1254x680.webp)

Now that we're familiar with the ideas behind two tower modes we can build our model using Pytorch. We'll start by defining a custom data loader which we'll use during training. This just packages our user and item features together with our label inside of a torch tensor ready for use. Our model definition will include the required `forward(...)` method and also two helper methods, `get_user_embedding(...)` and `get_item_embedding(...)` so that we can generate new embeddings after training.

```python
import torch
from torch.utils.data import DataLoader, Dataset

import torch.nn as nn
import torch.optim as optim

class PurchaseDataset(Dataset):
    def __init__(self, user_features, restaurant_features, labels):
        self.user_features = user_features
        self.restaurant_features = restaurant_features
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        user_index, restaurant_index, label = self.labels[idx]
        return self.user_features[user_index], self.restaurant_features[restaurant_index], torch.tensor(label, dtype=torch.float32)

class TwoTowerModel(nn.Module):
    def __init__(self, user_input_dim, restaurant_input_dim, hidden_dim):
        super(TwoTowerModel, self).__init__()
        self.user_tower = nn.Sequential(
            nn.Linear(user_input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(p=0.5),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(p=0.5),
            nn.Linear(hidden_dim, hidden_dim),
        )
        self.restaurant_tower = nn.Sequential(
            nn.Linear(restaurant_input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(p=0.5),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(p=0.5),
            nn.Linear(hidden_dim, hidden_dim),
        )

    def get_user_embeddings(self, user_features):
        return nn.functional.normalize(self.user_tower(user_features), dim=1)

    def get_restaurant_embeddings(self, restaurant_features):
        return nn.functional.normalize(self.restaurant_tower(restaurant_features), dim=1)

    def forward(self, user_features, restaurant_features):
        user_embedding = self.get_user_embeddings(user_features)
        restaurant_embedding = self.get_restaurant_embeddings(restaurant_features)
        return user_embedding, restaurant_embedding
```

With our model defined the next step is to prepare our dataset and pass it to our data loader class.

```python
user_features = torch.tensor(users_df['feature_vector'].tolist(), dtype=torch.float32)
restaurant_features = torch.tensor(df['feature_vector'].tolist(), dtype=torch.float32)

dataset = PurchaseDataset(user_features, restaurant_features, labels)
dataloader = DataLoader(dataset, batch_size=64, shuffle=True)
```

## How do you train the two-tower model?

At last we're ready to train our model. We'll train it via back propagation like any other deep learning model. We've chosen cosine as our loss criteria to match with our architecture diagram and [Adam](https://arxiv.org/pdf/1412.6980) as our optimizer. We've chosen some reasonable defaults for the training steps and model hidden dimensions. Given the randomization of our data your mileage may differ.

```python
# initialize the model, loss function and optimizer
model = TwoTowerModel(user_input_dim=user_features.shape[1], restaurant_input_dim=restaurant_features.shape[1], hidden_dim=128)
cosine_criterion = nn.CosineEmbeddingLoss()

optimizer = optim.Adam(model.parameters(), lr=0.001)

# train model
num_epochs = 200
losses = []
for epoch in range(num_epochs):
    for user_batch, restaurant_batch, label_batch in dataloader:
        optimizer.zero_grad()
        user_embeddings, restaurant_embeddings = model(user_batch, restaurant_batch)
        loss = cosine_criterion(user_embeddings, restaurant_embeddings, label_batch)
        loss.backward()
        optimizer.step()
    if epoch % 10 == 0:
        print(f'epoch [{epoch+1}/{num_epochs}], loss: {loss.item()}')
    losses.append(loss.item())
```

## Why use two towers instead of content or collaborative filtering?

This all seems rather complicated compared to other recommender system architectures, so why go through with all of this effort? The best way to answer this is to compare with other recommendation system approaches.

### What are the shortcomings of content filtering?

The simplest machine learning approach to recommendations is content filtering. It's also an approach that doesn't take into account user behaviors beyond finding similar content. This may not sound too bad, but can quickly lead to users getting trapped into content bubbles, where once they interact with a certain item - even if it was just randomly - they only see similar items.

### What are the shortcomings of collaborative filtering?

Collaborative filtering approaches like Singular Value Decomposition (SVD) take the opposite approach and _only_ consider user behaviors to make recommendations. This has clear advantages, but one major drawback; SVD can't handle brand new users or brand new content. Each time a new user joins, or a new content is added to your library they won't have associated vectors. There also won't be meaningful new interaction data to re-train a model and generate vectors. It can be bad enough that a model needs frequent re-training; it can be an even bigger issue if you can't make recommendations for new users and content.

## How do two towers separate training, embedding creation, and inference?

Once we have a trained model we can use each tower in our two tower model to generate embeddings for users and items. Unlike SVD, we don't have to retrain our model to get these vectors. We also don't need new interaction data for new users or content. Even the step of embedding creation only needs to happen once.

```python
user_embeddings = model.get_user_embeddings(user_features=torch.tensor(users_df['feature_vector'].tolist(), dtype=torch.float32))
restaurant_embeddings = model.get_restaurant_embeddings(restaurant_features=torch.tensor(df['feature_vector'].tolist(), dtype=torch.float32))
```

## How does the two-tower model combine the best of both worlds?

Two tower models are a triple whammy when it comes to solving the above problems:

- They are trained on interaction data, aka our labels, so learn not to fall into content bubbles
- They directly consider the user features _and_ content features to create personalized recommendations
- they can handle brand new users and content that don't yet have interaction data. No retraining necessary

While we need some interaction data to train our model initially, it's totally fine if not all users or restaurants are included in our labeled data. Only a sample is needed. This is why we can handle new users and content without retraining. Only their raw features are needed to generate embeddings.

## How do you load embeddings into Redis?

With two sets of vectors we'll load the restaurant metadata into a Redis vector store to search over, and the user vectors into a regular key look up for quick access. We'll want to include our restaurants' opening and closing hours, as well as their location in longitude and latitude in our schema so transform them into a usable format. This requires some data transformations. These steps and a sample of the transformed data are shown below.

```python
#  extract opening and closing times from the 'hours' column
def extract_opening_closing_times(hours, day):
    if day in hours:
        return int(hours[day][0][0].replace(':','')), int(hours[day][0][1].replace(':',''))
    else:
        #assume a reasonable default of 9:00am to 8:00pm
        return 900, 2000

# create new columns for open and closing times for each day of the week
for day in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']:
    df[f'{day}_open'], df[f'{day}_close'] = zip(*df['hours'].apply(lambda x: extract_opening_closing_times(x, day)))

# combine 'longitude' and 'latitude' into a single 'location' column
df['location'] = df.apply(lambda row: f"{row['longitude']},{row['latitude']}", axis=1)
df.drop(columns=['hours', 'latitude', 'longitude'], inplace=True)

# ensure the 'embedding' column is in the correct format (list of floats)
df['embedding'] = restaurant_embeddings.detach().numpy().tolist()

# ensure all columns are in the correct order as defined in the schema
df = df[['name', 'address', 'locality', 'location', 'cuisine', 'price', 'rating', 'sunday_open', 'sunday_close', 'monday_open', 'monday_close', 'tuesday_open', 'tuesday_close', 'wednesday_open', 'wednesday_close', 'thursday_open', 'thursday_close', 'friday_open', 'friday_close', 'saturday_open', 'saturday_close', 'embedding']]
```

Here's one sample restaurant record ready to be loaded into our Redis vector store.

```json
{'name': '21st Amendment Brewery & Restaurant', 'address': '563 2nd St', 'locality': 'San Francisco', 'location': '-122.392576,37.782448', 'cuisine': ['Cafe', 'Pub Food', 'American', 'Burgers', 'Pizza'], 'price': 2, 'rating': 4.0, 'sunday_open': 1000, 'sunday_close': 2359, 'monday_open': 1130, 'monday_close': 2359, 'tuesday_open': 1130, 'tuesday_close': 2359, 'wednesday_open': 1130, 'wednesday_close': 2359, 'thursday_open': 1130, 'thursday_close': 2359, 'friday_open': 1130, 'friday_close': 2359, 'saturday_open': 1130, 'saturday_close': 2359, 'embedding': [0.04085610806941986, -0.07978134602308273, ... ]}
```

The schema we're using to index our restaurant embeddings will also include location and opening and closing times so that we can use them in our search filters. We'll define it from a dictionary, create the index in Redis, and load our restaurant data into it. We'll get back a list of keys.

```python
from redis import Redis
from redisvl.schema import IndexSchema
from redisvl.index import SearchIndex

client = Redis.from_url(REDIS_URL)

restaurant_schema = IndexSchema.from_dict({
    'index': {
        'name': 'restaurants',
        'prefix': 'restaurant',
        'storage_type': 'json'
    },
    'fields': [
        {'name': 'name', 'type': 'text'},
        {'name': 'address', 'type': 'text'},
        {'name': 'locality', 'type': 'tag'},
        {'name': 'location', 'type': 'geo'},
        {'name': 'cuisine', 'type': 'tag'},
        {'name': 'price', 'type': 'numeric'},
        {'name': 'rating', 'type': 'numeric'},
        {'name': 'sunday_open', 'type': 'numeric'},
        {'name': 'sunday_close', 'type': 'numeric'},
        {'name': 'monday_open', 'type': 'numeric'},
        {'name': 'monday_close', 'type': 'numeric'},
        {'name': 'tuesday_open', 'type': 'numeric'},
        {'name': 'tuesday_close', 'type': 'numeric'},
        {'name': 'wednesday_open', 'type': 'numeric'},
        {'name': 'wednesday_close', 'type': 'numeric'},
        {'name': 'thursday_open', 'type': 'numeric'},
        {'name': 'thursday_close', 'type': 'numeric'},
        {'name': 'friday_open', 'type': 'numeric'},
        {'name': 'friday_close', 'type': 'numeric'},
        {'name': 'saturday_open', 'type': 'numeric'},
        {'name': 'saturday_close', 'type': 'numeric'},
        {
            'name': 'embedding',
            'type': 'vector',
            'attrs': {
                'dims': 128,
                'algorithm': 'flat',
                'datatype': 'float32',
                'distance_metric': 'cosine'
            }
        }
    ]
})

restaurant_index = SearchIndex(restaurant_schema, redis_client=client)
restaurant_index.create(overwrite=True, drop=True)

restaurant_keys = restaurant_index.load(df.to_dict(orient='records'))
```

With our search index created and the restaurant data loaded it's time to load the user vectors into a regular redis space. Our user vectors are the ones used to search with so they don't need an index like our restaurant vectors do. Just keep the user_key handy.

```python
from redis.commands.json.path import Path

with client.pipeline(transaction=False) as pipe:
    for user_id, embedding in zip(users_df['user_id'], user_embeddings):
        user_key = f"user:{user_id}"

        user_data = {
            "user_embedding": embedding.tolist(),
        }
        pipe.json().set(user_key, Path.root_path(), user_data)
    pipe.execute()
```

## Why is Redis fast enough for real-time recommendations?

I can hear you say it, "deep learning is cool and all, but I need my system to be fast. I don't want to call a deep neural network to get recommendations."

Well not to fear my friend, you won't have to! While training our model may take a while, you won't need to do this often. And if you look closely you'll see that both the user and content embedding vectors can be generated once and reused again and again. Only the vector search is happening when generating recommendations. These embeddings will only change if your user or content features change and if you select your features wisely this won't be often.

![Architecture diagram showing Redis as both a feature store for user and item embeddings and the inference layer that replaces the final neural network layer with vector similarity search](/images/site-mirror/842fc7e74af1078455170550c03a855cde11a26d-1240x698.webp)

Redis is operating both as a feature store for your user and content embeddings, and also as the final inference layer for lightning fast real time recommendations. This means all the heavy lifting of storing embeddings and performing vector comparisons is handled by your Redis DB and not your app. We used Pytorch to train our embedding model and we need it to generate new embeddings from time to time, but when it comes time to get recommendations all that we need are the user and item vectors. This is why you can have as deep of a neural network as you like when training and generating embeddings and it won't impact inference. We've replaced the last layer of our Pytorch model with Redis vector search.

## How do you add location-aware recommendations?

We've shown how Redis can apply filters on top of [vector similarity search](/tutorials/howtos-solutions-vector-getting-started-vector) to further refine results, but did you know it can also refine search results by location? Using the `Geo` field type on our index definition we can apply a `GeoRadius` filter to find only places nearby, which seems mighty useful for a restaurant recommendation system.

Combining `GeoRadius` with `Num` tags we can find places that are personally relevant to us, nearby _and_ open for business right now. We have all our data and vectors ready to go. Now let's put it all together with query logic.

```python
from redisvl.query.filter import Tag, Num, Geo, GeoRadius
import datetime

def get_filter(user_long,
               user_lat,
               current_date_time,
               radius=1000,
               low_price=0.0,
               high_price=5.0,
               rating=0.0,
               cuisines=[]):

    geo_filter = Geo("location") == GeoRadius(user_long, user_lat, radius, unit="m") # use a distance unit of meters

    open_filter = Num(f"{current_date_time.strftime('%A').lower()}_open") < current_date_time.hour*100 + current_date_time.minute
    close_filter = Num(f"{current_date_time.strftime('%A').lower()}_close") > current_date_time.hour*100 + current_date_time.minute
    time_filter = open_filter & close_filter

    price_filter = (Num('price') >= low_price) & (Num('price') <= high_price)

    rating_filter = Num('rating') >= rating

    cuisine_filter = Tag('cuisine') == cuisines

    return geo_filter & time_filter & price_filter & rating_filter & cuisine_filter

from redisvl.query import VectorQuery

random_user = random.choice(users_df['user_id'].tolist())
user_vector = client.json().get(f"user:{random_user}")["user_embedding"]

# get a location for this user. Your app may call an API, here we'll set one randomly to within San Francisco in the longitude and latitude bounding box of:
# Lower corner: (-122.5137, 37.7099) in (longitude, latitude) format
# Upper corner: (-122.3785, 37.8101)

longitude = random.uniform(-122.5137, -122.3785)
latitude = random.uniform(37.7099, 37.8101)
longitude, latitude = -122.439, 37.779
radius = 1500

full_filter = get_filter(user_long=longitude,
                         user_lat=latitude,
                         radius=radius,
                         current_date_time=datetime.datetime.today())

query = VectorQuery(vector=user_vector,
                    vector_field_name='embedding',
                    num_results=5,
                    return_score=False,
                    return_fields=['name', 'address', 'location', 'distance'],
                    filter_expression=full_filter,
                    )

results = restaurant_index.query(query)
```

## How do you visualize the recommendations on a map?

With our vectors loaded and helper functions defined we can get some nearby recommendations. That's all well and good, but don't you wish you could see these recommendations? I sure do. So let's visualize them on an interactive map.

```python
import folium
from IPython.display import display

# create a map centered around San Francisco
figure = folium.Figure(width=700, height=600)
sf_map = folium.Map(location=[37.7749, -122.4194],
               zoom_start=13,
               max_bounds=True,
                min_lat= 37.709 - 0.1,
                max_lat= 37.8101 + 0.1,
                min_lon= -122.3785 - 0.3,
                max_lon= -122.5137 + 0.3,
    )

sf_map.add_to(figure)

# add markers for each restaurant in blue
for idx, row in df.iterrows():
    lat, lon = map(float, row['location'].split(','))
    folium.Marker([lon, lat], popup=row['name']).add_to(sf_map)

user = users_df['user_id'].tolist()[42]
user_vector = client.json().get(f"user:{user}")["user_embedding"]

# get a location for this user. Your app may call an API, here we'll set one randomly to within San Francisco
# lower corner: (-122.5137, 37.7099) in (longitude, latitude) format
# upper corner: (-122.3785, 37.8101)
longitude, latitude = -122.439, 37.779
num_results = 25
radius = 2000

# draw a circle centered on our user
folium.Circle(
    location=[latitude, longitude],
    radius=radius,
    color="green",
    weight=3,
    fill=True,
    fill_opacity=0.3,
    opacity=1,
).add_to(sf_map)

full_filter = get_filter(user_long=longitude,
                         user_lat=latitude,
                         radius=radius,
                         current_date_time=datetime.datetime.today()
                         )

query = VectorQuery(vector=user_vector,
                    vector_field_name='embedding',
                    num_results=num_results,
                    return_score=False,
                    return_fields=['name', 'address', 'location', 'rating'],
                    filter_expression=full_filter,
                    )

results = restaurant_index.query(query)

# now show our recommended places in red
for restaurant in results:
    lat, lon = map(float, restaurant['location'].split(','))
    folium.Marker([lon, lat], popup=restaurant['name'] + ' ' + restaurant['rating'] + ' stars', icon=folium.Icon(color='red')).add_to(sf_map)

display(sf_map)
```

![Interactive map of San Francisco with blue markers for all restaurants and red markers highlighting personalized recommendations within a green radius circle around the user's location](/images/site-mirror/cee8f51e2475896f6bf71cf36e1a1d6f447cdc19-1242x1066.webp)

Here you can see all the restaurants in our San Francisco dataset. The points in red are our personalized recommendations for our user. They're also narrowed down to being open right now and within our set maximum radius of 2km. Just what you want when you need a quick late night bite or are desperate for an early morning coffee.

## Summary

That's it! You've built a deep learning restaurant recommendation system with Redis. It's personalized, location aware, adaptable, and fast. Redis handles the scale and speed so you can focus on everything else.

And that concludes our three part series on building recommendation systems with Redis and RedisVL. Along the way we've explored vector search, different similarity metrics - cosine and inner product - different ways to generate user and content embeddings, crafting filters, adding location and time awareness, separating training from inference, and even some deep learning mixed in for good measure.

## Next steps

- Get started with [vector search in Redis](/tutorials/howtos-solutions-vector-getting-started-vector) if you're new to vector similarity search
- Try [semantic text search with Redis](/tutorials/howtos-solutions-vector-semantic-text-search) for another vector search use case
- Build a [generative AI chatbot with Redis](/tutorials/howtos-solutions-vector-gen-ai-chatbot) using vector search for retrieval-augmented generation
- Explore [image search with Redis](/tutorials/howtos-solutions-vector-image-summary-search) for multimodal vector similarity
- Browse [RedisVL on GitHub](https://github.com/redis/redis-vl-python) for the full client library documentation
- See our other [AI resources and recipes](https://github.com/redis-developer/redis-ai-resources) for more recommendation system examples
