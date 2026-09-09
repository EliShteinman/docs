---
title: "Getting Started on Feast With Redis: Machine Learning Feature Store Quickstart Tutorial"
linkTitle: "Getting Started on Feast With Redis: Machine Learning Feature Store Quickstart Tutorial"
url: "/blog/feast-with-redis-tutorial-for-machine-learning/"
description: "This tutorial provides a step-by-step Feast for Redis quickstart that walks you through an end-to-end example of using Feast with Redis as its online feature store for machine learning. It’s based..."
date: 2021-12-15
blogCategories:
- "How To and Tutorials"
- "Tech"
authors:
- "Nava Levy"
lastmod: 2026-05-26
hidden: true
---

*By Nava Levy, Developer Advocate, Data Science & ML Operations · Published 15 December 2021 · updated 26 May 2026*

![Blog tile image](/images/site-mirror/b73e4626f6815193f0b427cbc85f81df61bdb262-772x550.webp)

This tutorial provides a step-by-step **Feast for Redis quickstart **that walks you through an end-to-end example of using Feast with Redis as its online [feature store for machine learning](/solutions/feature-store/). It’s based on the [Feast Quickstart tutorial](https://docs.feast.dev/getting-started/quickstart), but instead of using the default online store, it uses the Redis online store for delivering real-time predictions at scale. If you’re not familiar with Feast or Redis, then the fastest way to get started with Feast using Redis is through this tutorial. Please refer to this [Feature Stores and Feast using Redis](/blog/building-feature-stores-with-redis-introduction-to-feast-with-redis/) blog article for a high-level introduction. More detailed information on Redis and Feast, as well as additional resources, are available at the end of this tutorial.

In this tutorial you will:

1. Deploy a local feature store with a Parquet file offline store and Redis online store.
1. Build a training dataset using the demo time series features from the Parquet files.
1. Materialize (load) feature values from the offline store into the Redis online store.
1. Read the latest features from the Redis online store for inference.

You can run the tutorial on [Google Colab](https://colab.research.google.com/drive/1MzieQE7h2BlVO6LT0IZGY9AozmhG1K9J?usp=sharing) or on your localhost following the guided steps below.

## Feast in a nutshell:

Feast (**Fea**ture **st**ore) is an open source feature store and is part of the [Linux Foundation AI & Data Foundation](https://lfaidata.foundation/blog/2020/11/10/feast-joins-lf-ai-data-as-new-incubation-project/). It can serve feature data to models from a low-latency online store (for real-time serving) or an offline store (for model training or batch serving). It also provides a central registry so **machine learning engineers** and **data scientists** can discover the relevant features for ML use cases. Below is a high-level architecture of Feast:

![](/images/site-mirror/dfd2b2b5996ae7d280b9f69b92590b53ad223007-1024x489.webp)

Feast is a Python library + optional CLI. You can install Feast using pip, as will be described soon in this tutorial.

Feast with Redis solves several common issues in this flow:

1. **Training-serving skew and complex data joins**: Feature values often exist across multiple tables. Joining these datasets can be complicated, slow, and error-prone.
  - Feast joins these tables with battle-tested logic that ensures point-in-time correctness so future feature values don’t leak to models.

1. **Online feature availability with low latency and at scale:** At inference time, models often need access to features that aren’t readily available and need to be precomputed from other data sources in real-time.
  - By deploying Feast with Redis you ensure the necessary features are consistently available and freshly computed at inference time, with low latency and high throughput.

1. **Feature reusability and model versioning: **Different teams within an organization are often unable to reuse features across projects, resulting in duplicate feature creation logic. Models have data dependencies that need to be versioned, like when running A/B tests on model versions.
  - Feast enables discovery of and collaboration on previously used features and enables versioning of sets of features (via feature services).
  - Feast enables feature transformation so users can reuse transformation logic across online / offline use cases and models.

## Feast with Redis Tutorial Overview

In this tutorial, we use feature stores to generate training data and power online model inference for a ride-sharing driver satisfaction prediction model. In the demo data scenario:

- We’ve surveyed some drivers to determine how satisfied they are with their experience using a ride-sharing app.
- We want to generate predictions for driver satisfaction for the rest of the users so we can reach out to potentially dissatisfied users.

## Tutorial Steps:

1. Install Redis and run Redis-Server in the background
1. Install Feast with Redis
1. Create a feature repository and define Redis as the online store
1. Register feature definitions and deploy your feature store
1. Generate training data
1. Load features into your Redis online store
1. Fetch feature vectors for inference

## Step 1: Install Redis and run Redis server in the background

To install Redis follow one of the alternatives below:

Ubuntu:

```javascript
$ sudo snap install redis
```

Docker:

```javascript
$ docker run --name redis --rm -p 6379:6379 -d redis
```

Mac (Homebrew):

```javascript
$ brew install redis
```

Additional information on alternative ways for installing Redis can be found [here](https://redis.io/download#installation). Additional configuration information can be found in the [Redis Quick Start](https://redis.io/topics/quickstart) guide.

## Step 2: Install Feast with Redis

Install the Feast SDK and CLI using pip:

```javascript
$ pip install 'feast[redis]'
```

## Step 3: Create a feature repository and configure Redis as the online store

A feature repository is a directory that contains the configuration of the feature store and individual features.

### Step 3a: Create a feature repository

The easiest way to create a new feature repository is to use the feast init command. This creates a scaffolding with initial demo data.

```javascript
$ feast init feature_repo
$ cd feature_repo
```

Output:

```javascript
Creating a new Feast repository in /Users/nl/dev_fs/feast/feature_repo
```

Let’s take a look at the resulting demo repo itself. It breaks down into:

- feature_store.yaml contains a demo setup configuring data sources and the online store
- example.py contains demo feature definitions
- data/ contains raw demo parquet data

### Step 3b: Configure Redis as the online store in the YAML configuration file

To configure Redis as the online store we need to set the type and connection_string values for online_store in feature_store.yaml as follows:

| project: my_projectregistry: data/registry.dbprovider: localonline_store: type: redis  connection_string: localhost:6379 |
|---|

The provider defines where the raw data exists (for generating training data and feature values for serving) in this demo, locally. The online_storedefines where to materialize ( load) feature values in the online store database (for serving).

Note that the above configuration is different from the default YAML file provided for the tutorial that instead uses the default online store :

| project: my_projectregistry: data/registry.dbprovider: localonline_store: path: data/online_store.db |
|---|

So by adding these two lines for online_store (type: redis, connection_string: localhost:6379) in the YAML file per the above, Feast is then able to read and write from Redis as its online store. Redis Online Store is part of the Feast core code, and as such, Feast knows how to use Redis out-of-the-box.

### Step 3c: Inspecting demo feature definitions at example.py

Let’s take a look at the demo feature definitions at example.py (to view it in your terminal you can run cat example.py ).

Example.py

```
# This is an example feature definition file

from google.protobuf.duration_pb2 import Duration

from feast import Entity, Feature, FeatureView, FileSource, ValueType

# Read data from parquet files. Parquet is convenient for local development mode. For
# production, you can use your favorite DWH, such as BigQuery. See Feast documentation
# for more info.
driver_hourly_stats = FileSource(
    path="/content/feature_repo/data/driver_stats.parquet",
    event_timestamp_column="event_timestamp",
    created_timestamp_column="created",
)

# Define an entity for the driver. You can think of entity as a primary key used to
# fetch features.
driver = Entity(name="driver_id", value_type=ValueType.INT64, description="driver id",)

# Our parquet files contain sample data that includes a driver_id column, timestamps and
# three feature column. Here we define a Feature View that will allow us to serve this
# data to our model online.
driver_hourly_stats_view = FeatureView(
    name="driver_hourly_stats",
    entities=["driver_id"],
    ttl=Duration(seconds=86400 * 1),
    features=[
        Feature(name="conv_rate", dtype=ValueType.FLOAT),
        Feature(name="acc_rate", dtype=ValueType.FLOAT),
        Feature(name="avg_daily_trips", dtype=ValueType.INT64),
    ],
    online=True,
    batch_source=driver_hourly_stats,
    tags={},
)

```

### 

### Step 3d: Inspect the raw data

Finally, let’s inspect the raw data. The raw data we have in this demo is stored in a local parquet file. The dataset captures the hourly stats of a driver in a ride-sharing app.

![](/images/site-mirror/d8cefcac22715f7192da47802a94a91ecc45b8ea-836x403.webp)

## Step 4: Register feature definitions and deploy your feature store

Now we run feast apply to register the feature views and entities defined in example.py. The apply command scans Python files in the current directory for feature view/entity definitions, registers the objects, and deploys infrastructure. In this example, it reads example.py (shown above) and sets up the Redis online store.

$ feast apply

Output:

| Registered entity driver_idRegistered feature view driver_hourly_statsDeploying infrastructure for driver_hourly_stats |
|---|

## Step 5: Generating training data

To train a model, we need features and labels. Often, this label data is stored separately (e.g. you have one table storing user survey results and another set of tables with feature values).

The user can query that table of labels with timestamps and pass that into Feast as an entity dataframe for training data generation. In many cases, Feast will also intelligently join relevant tables to create the relevant feature vectors.


- Note that we include timestamps because we want the features for the same driver at various timestamps to be used in a model.

Python

(*Copy the code below into a file gen_train_data.py and then run it):*

```python
from datetime import datetime, timedelta
import pandas as pd

from feast import FeatureStore

# The entity dataframe is the dataframe we want to enrich with feature values
entity_df = pd.DataFrame.from_dict(
    {
        "driver_id": [1001, 1002, 1003],
        "label_driver_reported_satisfaction": [1, 5, 3], 
        "event_timestamp": [
            datetime.now() - timedelta(minutes=11),
            datetime.now() - timedelta(minutes=36),
            datetime.now() - timedelta(minutes=73),
        ],
    }
)

store = FeatureStore(repo_path=".")

training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "driver_hourly_stats:conv_rate",
        "driver_hourly_stats:acc_rate",
        "driver_hourly_stats:avg_daily_trips",
    ],
).to_df()

print("----- Feature schema -----\n")
print(training_df.info())

print()
print("----- Example features -----\n")
print(training_df.head())

```

Output:

| ----- Feature schema -----<class 'pandas.core.frame.DataFrame'>Int64Index: 3 entries, 0 to 2Data columns (total 6 columns):# Column Non-Null Count Dtype --- ------ -------------- ----- 0 event_timestamp 3 non-null datetime64[ns, UTC]1 driver_id 3 non-null int64 2 label_driver_reported_satisfaction 3 non-null int64 3 conv_rate 3 non-null float32 4 acc_rate 3 non-null float32 5 avg_daily_trips 3 non-null int32 dtypes: datetime64[ns, UTC](1), float32(2), int32(1), int64(2)memory usage: 132.0 bytesNone----- Example features ----- event_timestamp driver_id ... acc_rate avg_daily_trips0 2021-08-23 15:12:55.489091+00:00 1003 ... 0.120588 9381 2021-08-23 15:49:55.489089+00:00 1002 ... 0.504881 6352 2021-08-23 16:14:55.489075+00:00 1001 ... 0.138416 606[3 rows x 6 columns] |
|---|

## Step 6: Load features into your Redis online store

We will now load or materialize feature data into your Redis online store so we can serve the latest features to models for online prediction. The materialize command allows users to materialize features over a specific historical time range into the online store. It will query the batch sources for all feature views over the provided time range, and load the latest feature values into the configured online store. materialize–incremental command will only ingest new data that has arrived in the offline store, since the last materialize call.

$ CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%S")
$ feast materialize-incremental $CURRENT_TIME

Output:

| Materializing 1 feature views to 2021-08-23 16:25:46+00:00 into the redis online store.driver_hourly_stats from 2021-08-22 16:25:47+00:00 to 2021-08-23 16:25:46+00:00:100%\|████████████████████████████████████████████\| 5/5 [00:00<00:00, 592.05it/s] |
|---|

## Step 7: Fetching feature vectors for inference

At inference time, we need to quickly read the latest feature values for different drivers (which otherwise might have existed only in batch sources) from Redis online feature store, using get_online_features(). These feature vectors can then be fed to the model.

Python

(*Copy the code below into a file get_feature_vectors.py and then run it):*

```python
from pprint import pprint
from feast import FeatureStore

store = FeatureStore(repo_path=".")

feature_vector = store.get_online_features(
    features=[
        "driver_hourly_stats:conv_rate",
        "driver_hourly_stats:acc_rate",
        "driver_hourly_stats:avg_daily_trips",
    ],
    entity_rows=[
        {"driver_id": 1004},
        {"driver_id": 1005},
    ],
).to_dict()

pprint(feature_vector)

```

Output

| {'acc_rate': [0.5732735991477966, 0.7828438878059387],'avg_daily_trips': [33, 984],'conv_rate': [0.15498852729797363, 0.6263588070869446],'driver_id': [1004, 1005]} |
|---|

Congratulations! You have reached the end of the tutorial. To shut down the Redis server that is running in the background you can use the redis-cli shutdown command.

## Tutorial recap:

In this tutorial you’ve deployed a local feature store with a Parquet file offline store and Redis online store. You then built a training dataset using time series features from Parquet files. Then, you materialized feature values from the offline store into the Redis online store. Finally, you read the latest features from the Redis online store for inference. With Redis as the online store you can read the latest feature very quickly for real-time ML use cases, with low latency and high throughput at scale.

## What’s next?

- Read the Feast [Concepts](https://docs.feast.dev/getting-started/concepts) page to understand the Feast data model, and read the Feast [Architecture](https://docs.feast.dev/getting-started/architecture-and-components) page.
- Read the full [configuration](https://rtd.feast.dev/en/master/#module-feast.infra.online_stores.redis) guide for Feast with Redis, and the [data model](https://github.com/feast-dev/feast/blob/master/docs/specs/online_store_format.md) used to store feature values in Redis.
- Case studies – learn from your peers: Learn how companies are using Features Stores with Redis as the online store ([Wix](https://youtu.be/E8839ENL-WY), [Swiggy](https://bytes.swiggy.com/enabling-data-science-at-scale-at-swiggy-the-dsp-story-208c2d85faf9), [Comcast](https://cdn.oreillystatic.com/en/assets/1/event/300/Automating%20ML%20model%20training%20and%20deployments%20via%20metadata-driven%20data%2C%20infrastructure%2C%20feature%20engineering%2C%20and%20model%20management%20Presentation.pdf), [Zomato](https://www.zomato.com/blog/elements-of-scalable-machine-learning), [AT&T](https://youtu.be/AXQt_oW9JEc), [DoorDash](https://doordash.engineering/2020/11/19/building-a-gigascale-ml-feature-store-with-redis/), [iFood](https://databricks.com/session_na20/building-a-real-time-feature-store-at-ifood)), and specifically how they are using Feast with Redis for their online store ([Gojek](https://youtu.be/DaNv-Wf1MBA?t=836), [Udaan](https://hasgeek.com/fifthelephant/mlops-conference/schedule/managed-feature-store-improving-data-reusability-providing-a-means-for-low-latency-real-time-prediction-at-udaan-HsZnfC4VUNdWUyJXXwfp5m), [Robinhood](https://www.applyconf.com/agenda/how-robinhood-built-a-feature-store-using-feast/)).
- Read about [Azure Managed Feature Store with Feast and Redis](https://github.com/Azure/feast-azure) and follow the [Getting started with Feast on Azure ](https://github.com/Azure/feast-azure/tree/main/provider/tutorial)tutorial as well as other Feast tutorials
- You can also look for more info on Feast or Redis in the general product introduction pages on [Feast](https://docs.feast.dev/) and [Redis](https://redis.io/topics/introduction) respectively.

Join other Feast users and contributors in[ Slack](https://slack.feast.dev) and become part of the community!
