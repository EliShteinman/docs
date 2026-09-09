---
title: "Retrieval optimizer: Bayesian optimization"
linkTitle: "Retrieval optimizer: Bayesian optimization"
url: "/blog/retrieval-optimizer-bayesian-optimization/"
description: "In the last article, we introduced the retrieval optimizer, why it matters for eval driven development (EDD) and how to get started with a basic grid search. Often selecting the right search method..."
date: 2025-07-21
blogCategories:
- "Tech"
authors:
- "Robert Shelton"
lastmod: 2025-07-21
hidden: true
---

*By Robert Shelton, AI Engineer at Redis · Published 21 July 2025*

![Retrieval optimizer: Bayesian optimization](/images/blog/ea40e751f4c664465805827c525c17df7c8085c7-772x552.webp)

In the [last article](https://docs.google.com/document/d/16ywR8VnbHrrgtQGB1r4gmpR6e3q3Z7E3fElRvJFUgfY/edit?tab=t.0), we introduced the retrieval optimizer, why it matters for eval driven development (EDD) and how to get started with a basic grid search. Often selecting the right search method and embedding model are the most influential elements that need to be measured first. However, there are many search index settings that have a tangible impact on the performance of your information retrieval app.

The problem is that to test all the available permutations of these settings would take too much time. This is where Bayesian optimization comes in. Instead of testing every possible combination of hyperparameters, Bayesian optimization chooses the best ones to try next based on what it has already learned. This greatly reduces the number of experiments needed. You don’t need to dive into the math behind Gaussian processes. Just define what matters most to your app (e.g. recall, latency, or precision) as an objective function (see below), and the optimizer will guide the search toward configurations that maximize your chosen objective.

## Code example

Running a bayesian optimization study with the retrieval optimizer is very similar to running a grid study.

📓You can find the complete notebook example [here](https://github.com/redis-applied-ai/redis-retrieval-optimizer/blob/main/docs/examples/bayesian_optimization/00_bayes_study.ipynb).

### Gather dependencies

#### Install tool:

```
pip install redis-retrieval-optimizer

```

#### Run redis:

```
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest

```

### Pull and/or create study data

As we did in the grid study, we’ll pull the data for our experiment from the beir benchmarking IR datasets and save to respective files.

```python
# Load data
import json
from redis_retrieval_optimizer.corpus_processors import eval_beir

# check the link above for different datasets to try
beir_dataset_name = "nfcorpus"

# Load sample data
corpus, queries, qrels = eval_beir.get_beir_dataset(beir_dataset_name)

with open(f"{beir_dataset_name}_corpus.json", "w") as f:
    json.dump(corpus, f)

with open(f"{beir_dataset_name}_queries.json", "w") as f:
    json.dump(queries, f)

with open(f"{beir_dataset_name}_qrels.json", "w") as f:
    json.dump(qrels, f)

```

### Define study config

The study config determines the ranges and values that the optimization process can choose to select while it seeks to maximize the objective function.

The metric_weights define how much each parameter is weighted in the objective function. In the following example, the resulting objective function will be:

```
obj = (1 * f1_at_k) + (1 * total_indexing_time) + (0 * recall_at_k) + (0 * ndcg_at_k) 

* embedding_latency and total_index_time are normalized to a value between 0 and 1 when used in the objective function for optimization.

```

If a metric, such as recall_at_k isn’t indicated in the metrics weights, its assumed value will be 0. Therefore, in this hypothetical study, we’ll choose settings that equal weight improvements for f1_at_k and total_indexing_time.

```
# path to data files for easy read
corpus: "data/nfcorpus_corpus.json"
queries: "data/nfcorpus_queries.json"
qrels: "data/nfcorpus_qrels.json"

index_settings:
  name: "optimize"
  vector_field_name: "vector" # name of the vector field to search on
  text_field_name: "text" # name of the text field for lexical search
  from_existing: false
  vector_dim: 384 # should match first embedding model or from_existing
  additional_fields:
      - name: "title"
        type: "text"

# section for bayesian optimization
optimization_settings:
  # defines weight of each metric in optimization function
  metric_weights:
    f1_at_k: 1
    total_indexing_time: 1
  algorithms: ["hnsw"] # indexing algorithm to be included in the study
  vector_data_types: ["float16", "float32"] # data types to be included in the study
  distance_metrics: ["cosine"] # distance metrics to be included in the study
  n_trials: 10 # total number of trials to run
  n_jobs: 1
  ret_k: [1, 10] # potential range of value to be sampled during study
  ef_runtime: [10, 20, 30, 50] # potential values for ef_runtime to take
  ef_construction: [100, 150, 200, 250, 300] # potential values for ef_construction to take
  m: [8, 16, 64] # potential values for m to take

# potential values for search method
search_methods: ["vector", "hybrid"]

# potential values for embedding models
embedding_models:
  - type: "hf"
    model: "sentence-transformers/all-MiniLM-L6-v2"
    dim: 384
    embedding_cache_name: "vec-cache" # avoid names with including 'ret-opt' as this can cause collisions
    dtype: "float32"

```

### Execute study

```python
import os
from redis_retrieval_optimizer.bayes_study import run_bayes_study
from redis_retrieval_optimizer.corpus_processors import eval_beir
from dotenv import load_dotenv

# load environment variables containing necessary credentials
load_dotenv()

redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

metrics = run_bayes_study(
    config_path="bayes_study_config.yaml",
    redis_url=redis_url,
    corpus_processor=eval_beir.process_corpus
)

```

### Output example

As you can see from the output, the process selected options (such as a smaller m param and vector_data_type) to reduce footprint and bring down indexing_time while maintaining or improving the f1 score.

![Output example](/images/blog/1621d3f0b892eb501f756965e1205a6a5cf316a9-885x491.webp)

## Process schematics

The following diagram outlines the full process flow for how the retrieval optimizer completes bayesian optimization. The retrieval optimizer uses the [Redisvl embedding cache feature](https://docs.redisvl.com/en/latest/user_guide/10_embeddings_cache.html) and only re-indexes when needed. This makes it much faster to run later tests.

![Process schematics](/images/blog/ac827d8c6793d3d4d6d40856871fa583dae633f5-1600x1153.webp)

## Next steps

Hopefully you’re now well on your way to optimizing your retrieval process. You can see the full notebook example of this tutorial [here](https://github.com/redis-applied-ai/redis-retrieval-optimizer/blob/main/docs/examples/bayesian_optimization/00_bayes_study.ipynb) and the source code for the retrieval optimizer [here](https://github.com/redis-applied-ai/redis-retrieval-optimizer).
