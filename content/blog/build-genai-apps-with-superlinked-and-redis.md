---
title: "Build GenAI apps with Superlinked and Redis"
linkTitle: "Build GenAI apps with Superlinked and Redis"
url: "/blog/build-genai-apps-with-superlinked-and-redis/"
description: "It’s no secret. GenAI apps can boost operations, enhance customer experience, and cut costs. But many enterprise tech teams get stuck in the proof-of-concept (POC) phase, struggling to move these..."
date: 2024-08-07
blogCategories:
- "Tech"
authors:
- "Jim Allen Wallace"
- "Ben Gutkovich"
lastmod: 2026-09-01
hidden: true
---

*By Jim Allen Wallace, Ben Gutkovich · Published 7 August 2024 · updated 1 September 2026*

![Blog tile image](/images/site-mirror/6a71a9acaec9d96e208bc95c752c9e3aee943d5f-772x552.webp)

## Build smarter and faster GenAI apps with Superlinked and Redis

It’s no secret. GenAI apps can boost operations, enhance customer experience, and cut costs. But many enterprise tech teams get stuck in the proof-of-concept (POC) phase, struggling to move these high-performing apps to production.

That’s where Redis’ blazing-fast vector database and Superlinked’s vector compute framework come in handy. For complex data, it just might be the solution you’ve been looking for.

### Overcome the challenge of GenAI recommenders

Real data is complex, and large language models (LLMs) are notoriously bad at understanding and handling structured data types like prices, dates, product categories, and popularity metrics. These data types are critical for high-quality information retrieval across multiple use cases, and in particular in recommender systems, and personalized semantic search.

Recommenders that only use unstructured data might work well on a small scale, but they often underperform in production. Customers want fast recommendations that match their recent behavior, category, and price range. To make this happen, tech teams often develop and train custom embedding and re-ranking models, a challenging endeavor for most enterprise tech teams. That’s why most GenAI-powered recommender systems get stuck in the POC phase and rarely deliver on their promise.

### Redis and Superlinked is a winning combination

[Superlinked](https://www.superlinked.com/)‘s vector compute framework lets data science teams create custom vector embeddings that combine structured and unstructured data in one unified vector space. This aligns with user insights and delivers** custom model performance with pre-trained model convenience**.

Redis’ lightning-fast [vector database](https://redis.io/solutions/vector-database/), based on in-memory storage, is perfect for customer-facing use cases that need quick responses like real-time recommender systems. Users respond better to recommendations that match their interests now, not later, when they’ve moved on.

Superlinked’s framework also simplifies the route to production, saving time for data and ML engineering resources. Data scientists can build and test their solutions in a Python notebook and compile them directly to a cloud service. This seamless transition from development to deployment accelerates time-to-market and ensures robust, scalable solutions.

### See how this large e-commerce platform hit 4x AOV growth

A major e-commerce platform faced low engagement with product recommendations. The issue stemmed from their constantly changing product catalog and reliance on static, non-personalized recommendation methods, resulting in missed revenue opportunities.

Using Superlinked to generate the vector embeddings from structured and unstructured product data, and Redis to deliver the vector search results in real-time, the client was able to launch a real-time personalized recommender system within weeks. The system presented users with highly relevant and timely recommendations, taking into account their browsing behavior within seconds, resulting in a 4x uplift in Average Order Value (AOV) for exposed users.

### Get started with Superlinked and Redis

Below you’ll find a step-by-step guide for building your first simple application with Superlinked, using Redis as the vector database and search solution. This semantic search application allows users to perform a free text search within a database of product reviews and demonstrates how combining the unstructured text of the review with the star ratings of the product embedded as a numeric value in the same vector space delivers higher-quality and more relevant results.

You can try [a complete example of an app](https://links.superlinked.com/sl-repo-redis-app), and, as always, refer to the official [README](https://github.com/superlinked/superlinked) for the latest details. Once you master this example, explore [additional notebooks](https://github.com/superlinked/superlinked/tree/main/notebook), including an example of an [e-commerce recommender system](https://github.com/superlinked/superlinked/tree/main/notebook).

**Experiment in your Python notebook environment**

#### Step 1: Install Superlinked

```python
%pip install superlinked

```

#### Step 2: Define the data schema

```python
# we are going to create 2 representations of the data
## 1. separate text and ranking for multimodal superlinked embeddings
## 2. full_review_as_text for LLM embedding of stringified review and rating
@schema

class Review:
    id: IdField
    review_text: String
    rating: Integer    
    full_review_as_text: String


```

#### Step 3: Create the spaces to encode different parts of data

```python
# Embed review data separately
review_text_space = TextSimilaritySpace(
    text=review.review_text, model="all-MiniLM-L6-v2")

rating_maximizer_space = NumberSpace(review.rating, min_value=1, 
    max_value=5, mode=Mode.MAXIMUM)

## Embed the full review as text
full_review_as_text_space = TextSimilaritySpace(
    text=review.full_review_as_text, model="all-MiniLM-L6-v2"

# Combine spaces as vector parts to an index.
## Create one for the stringified review 
naive_index = Index([full_review_as_text_space])

## and one for the structured multimodal embeddings
advanced_index = Index([review_text_space, rating_maximizer_space])

```

#### Step 4: Define the query mapping to each index type

```python
openai_config = OpenAIClientConfig(api_key=userdata.get("openai_api_key"),     model="gpt-4o")

# Define your query using dynamic parameters for query text and weights.
## first a query on the naive index - using natural language
naive_query = (
    Query(
        naive_index,
        weights={
            full_review_as_text_space: Param('full_review_as_text_weight')
        },
    )
    .find(review)
    .similar(full_review_as_text_space.text, Param("query_text"))
    .limit(Param('limit'))
    .with_natural_query(Param("natural_query"), openai_config)
)
## and another on the advanced multimodal index - also using natural language
superlinked_query = (
    Query(
        advanced_index,
        weights={
            review_text_space: Param('review_text_weight'),
            rating_maximizer_space: Param('rating_maximizer_weight'),
        },
    )
    .find(review)
    .similar(review_text_space.text, Param("query_text"))
    .limit(Param('limit'))
    .with_natural_query(Param("natural_query"), openai_config)
)

```

**Note**: Superlinked supports two ways of setting weights for the different query parts:

1. “Natural language queries” – using .with_natural_query – dynamically and automatically parse user queries and set the weights
1. Pre-defined weights – developers can set weights for each part of the query based on business logic or known user preferences

#### Step 5: Load the data

```python
# Run the app
source: InMemorySource = InMemorySource(review, parser=DataFrameParser(schema=review))
executor = InMemoryExecutor(sources=[source], indices=[naive_index, advanced_index]])
app = executor.run()

# Download dataset
data = pd.read_json("https://storage.googleapis.com/superlinked-preview-test-data/amazon_dataset_1000.jsonl",lines=True)

# Ingest data to the framework.
source.put([data])

```

#### Step 6: Run experiments with different representations, until you are satisfied with the results

```python
# query that is based on the LLM embedded reviews
naive_positive_results = app.query(
    naive_query,
    natural_query='High rated quality products',
    limit=10)
naive_positive_results.to_pandas()


# query based on multimodal Superlinked embeddings
superlinked_positive_results = app.query(
    superlinked_query,
    natural_query='High rated quality products',
    limit=10)
superlinked_positive_results.to_pandas()

```

**See for yourself**

Notice how creating a multimodal vector using custom embeddings improves the quality of the results. Compare the top three results for the query “High rated quality products” in the table below, and you’ll see how the LLM “misinterprets” the query and fetches a clearly wrong result in the third position.

| Search for “High rated quality products” |  |  |  |
|---|---|---|---|
| Results based solely on the text | Results based on text and rating |  |  |
| Review text | Rating | Review text | Rating |
| Good Product Good Product | 5 | Good Product Good Product | 5 |
| Can’t beat this deal! Great amount of products for the price. A lot of sample sizes but the value on some of the products is insane. Loved trying so many things that I wouldn’t consider normally. | 5 | Can’t beat this deal! Great amount of products for the price. A lot of sample sizes but the value on some of the products is insane. Loved trying so many things that I wouldn’t consider normally. | 5 |
| Cheap product Not good | 1 | Good product Works great | 5 |

**Ready to deploy?**

#### Step 7: Install Superlinked server (refer to the server [README](https://github.com/superlinked/superlinked/blob/main/README.md) for the latest instructions)

```python
# Clone the repository
git clone https://github.com/superlinked/superlinked

cd <repo-directory>/server
./tools/init-venv.sh
cd runner
source "$(poetry env info --path)/bin/activate"
cd ..

# Make sure you have your docker engine running and activate the virtual environment
./tools/deploy.py up

```

#### Step 8: Connect to your Redis instance (refer to [Redis documentation](https://redis.io/docs/latest/operate/oss_and_stack/install/install-stack/) for instructions)

```python
from superlinked.framework.dsl.storage.redis_vector_database import RedisVectorDatabase

vector_database = RedisVectorDatabase(
# Your Redis URL without port or any extra fields 
    "<your_redis_host>",
# Port number, which should be an integer
    12315,     
# The params can be found here: https://redis.readthedocs.io/en/stable/connections.html 
    username="<username>",
    password="<password>"
)

```

#### Step 9: Configure the Superlinked server – add your configuration from the notebook (Steps 2, 3) and append the deployment setup

```python
# Copy your configuration to app.py
# ...

# Create a data source to bulk load your production data.
config = DataLoaderConfig("https://storage.googleapis.com/superlinked-sample-datasets/amazon_dataset_ext_1000.jsonl", DataFormat.JSON, pandas_read_kwargs={"lines": True, "chunksize": 100})
source = DataLoaderSource(review, config)

executor = RestExecutor(
    # Add your data source 
    sources=[source],
    # Add the indices that contains your configuration 
    indices=[index],
    # Create a REST endpoint for your query.
    queries=[RestQuery(RestDescriptor("naive_query"), naive_query),      
            RestQuery(RestDescriptor("superlinked_query"), superlinked_query)],

    # Connect to Redis 
    vector_database=RedisVectorDatabase()
)

SuperlinkedRegistry.register(executor)

```

#### Step 10: Test your deployment

```python
# Trigger the data load 
curl -X POST 'http://localhost:8080/data-loader/review/run'

# Check the status of the loader 
curl -X GET 'http://localhost:8080/data-loader/review/status'

# Send your first query
curl -X POST \
    'http://localhost:8080/api/v1/search/superlinked_query' \
    --header 'Accept: */*' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "natural_query": "High rated quality products",


        "limit": 10
    }'

```

Congratulations. You learned how to build your first solution that combines numeric and unstructured data in the same embedding space to deliver high-quality results. We’re excited to see the amazing applications that you’ll build with Superlinked and Redis — don’t hesitate to [share your work](mailto:contact@superlinked.com) with us.

### Conclusion

In the words of Ash Vijayakanthan, SVP of Cloud Sales and Partnerships at Redis: *“Redis is partnering with Superlinked to make vector databases easier to apply to complex data for use cases like RAG with LLMs and e-commerce recommendation systems”*. It’s a partnership that helps enterprises overcome the hurdles of moving from proof-of-concept to production and realize the full potential of their GenAI apps.

## Related resources

#### Solutions

### Redis vector database

Build real-time apps that exceed expectations for responsiveness and include complex processing with low latency.

#### Solutions

### Superlinked

Superlinked is a compute framework for your information retrieval and feature engineering systems, focused on turning complex data into vector embeddings.

#### Solutions

### Superlinked examples

Compute tooling for vector-powered apps.

![Close](/images/site-mirror/96e244338b2f3fee742526528445ee7fd0a56a5c-17x17.svg)

*(interactive chart, not available offline)*

*(interactive chart, not available offline)*

*(interactive chart, not available offline)*
