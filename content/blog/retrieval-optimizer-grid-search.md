---
title: "Retrieval optimizer: Grid search"
linkTitle: "Retrieval optimizer: Grid search"
url: "/blog/retrieval-optimizer-grid-search/"
description: "One of the most valuable pieces of feedback I’ve ever received as an engineer came as an intern. I was debugging some data issues and, truthfully, didn’t really know what was going on. When my..."
date: 2025-07-21
blogCategories:
- "Tech"
authors:
- "Robert Shelton"
lastmod: 2025-07-21
hidden: true
mirrored: true
---

*By Robert Shelton, AI Engineer at Redis · Published 21 July 2025*

![Retrieval optimizer: Grid search](/images/site-mirror/060d3e0b4b4f5e9edbd62c0a9b054b547dce190c-772x552.webp)

One of the most valuable pieces of feedback I’ve ever received as an engineer came as an intern. I was debugging some data issues and, truthfully, didn’t really know what was going on. When my manager asked me for an update, I responded with something vague like, “I think it happens when event A occurs, but not all the time—so maybe it’s a network thing?”

He looked at me, in the way senior engineers will look at junior engineers for the rest of eternity, smiled and said: **“Well don’t guess—measure the problem.”**

At the time, it felt like a small correction. But as I’ve grown in my career, I’ve seen over and over how much time and effort is wasted because we guess—about root causes, about what matters, about what’s better—without grounding those guesses in real measurements or clear goals. I’ve wasted countless hours of my life *debugging assumptions,* and when I’m stuck I will often find myself repeating the phrase “don’t guess” like a mantra. I suppose that’s sort of absurd, but it works for me.

Recently, I was working with a large financial services customer trying to improve the performance of a retrieval-augmented generation (RAG) system. They were chasing a “silver bullet”: a better model, a novel chunking strategy, a fancy retrieval trick they saw in a blog post. We tried a dozen things, and each had some effect, but no one could confidently say what was actually helping, and by how much. **We were optimizing vibes, not metrics**.

This isn’t unusual. Our team at Redis has interactions daily with devs and product teams who are asking similar kinds of questions: *What embedding model should I use? What’s the best retrieval method?* These are good questions—but the unfortunate (and unsatisfying) answer is almost always:** *****it depends****.* Everyone we talk to has slightly different business requirements, slightly different data, and while there are general best practices, it still feels more like name dropping than true engineering.

Eval Driven Development (EDD)

Traditional software is largely deterministic—click button A, get result B—and can be reliably tested with unit and integration tests. LLM-based apps, however, are probabilistic by nature, making consistent behavior harder to guarantee. This has led to the rise of *eval-driven development* (EDD), where teams define clear metrics and use structured evaluation sets to measure and iterate on model performance.

This is where the **Retrieval Optimizer** comes in. We built a way to flexibly **test the parts of their system that drive what *****depends***. The Retrieval Optimizer is an open source framework that makes it quick and easy to measure performance for your specific situation. It also compares configurations objectively, in their own setting, against the metrics that are important for your problem.

Specifically, with the retrieval optimizer you can try multiple embedding models, test different retrieval methods (BM25, hybrid, rerank, vector search, and more), and run evaluations on curated IR datasets or bring your own. The output of which is a meaningful profile of the options—grounded in actual data, not just intuition.

Ironically, once you’ve defined your goals clearly and made them measurable, *then* you can afford to guess. Try things out quickly. Iterate. Explore. **Because now, every guess becomes a test**—and every test gives you a signal of the right direction to go.

Furthermore, as more and more code and processes integrate AI the new bottleneck in development will increasingly be *verification,* as [Andrej Karpathy](https://www.youtube.com/watch?v=LCEmiRjPEtQ) points out in his keynote at the AI startup school. Tools like the retrieval optimizer help reduce the bottleneck of verification by providing a framework for quicker evaluation, aka verification of a probabilistic process.

## Code or it didn’t happen

📓A complete example notebook is available [here](https://github.com/redis-applied-ai/redis-retrieval-optimizer/blob/main/docs/examples/grid_study/00_grid_study.ipynb).

The easiest way to get started with the retrieval optimizer is to run a grid study. With a grid study, you choose the embedding models and search methods you want to test. The retrieval optimizer runs them in a row like a grid search, which is why the name is given.

The retrieval optimizer will do the work of embedding, indexing, and searching against your provided corpus data. This will let you focus on the new search part of your problem.

## Steps

### Install tool:

```python
pip install redis-retrieval-optimizer
```

### Run redis:

```python
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
```

### Prepare dataset:

For ease of getting started we are going to use the nfcorpus dataset made easily available through [beir-cellar](https://github.com/beir-cellar/beir) for benchmarking IR. In this example, we’ll use the useful NF Corpus dataset (Non-factoid corpus). This dataset is a biomedical based dataset that is often used for testing longer answers that need understanding beyond simple fact-based queries.

```python
# helper functions for using the beir datasets
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

#### Corpus

The **Corpus** is the full set of documents you'll be searching against, i.e. what gets indexed into Redis. By default, this data will be processed by the corpus_processors.eval_beir.process_corpus function, which knows how to format data from these general IR benchmarks. You can also **define your own custom processors** to handle corpus data provided in a different structure. For an example, see [this blog](https://docs.google.com/document/d/1NDKQGkikEhW_qIC-pwxg04s9N9cGMyS7HCmBILMYyu0/edit?usp=sharing).

**General structure**:

```
{
    "corpus_id": {
        "text": "text to be searched or vectorized",
        "title": "optional associated title"
    }
}

```

**Real world example**:

```
{
    "MED-10": {
        "text": "Recent studies have suggested that statins, an established drug group in the prevention of cardiovascular mortality, could delay or prevent breast cancer recurrence...",
        "title": "Statin Use and Breast Cancer Survival: A Nationwide Cohort Study from Finland"
    }
}

```

#### Queries

**Queries** are the search inputs you'll evaluate against the corpus. Each query should have a unique ID and the query text. Like the corpus, **you can define your own query structure** and objects and use custom search methods. For an example, see [this blog](https://docs.google.com/document/d/1NDKQGkikEhW_qIC-pwxg04s9N9cGMyS7HCmBILMYyu0/edit?usp=sharing).

**General structure**:

```
{
    "query_id": "query text"
}

```

**Example**:

```
{
    "PLAIN-2": "Do Cholesterol Statin Drugs Cause Breast Cancer?",
    "PLAIN-12": "Exploiting Autophagy to Live Longer"
}

```

#### Qrels

**Qrels, **otherwise known as *query relevance judgments*, are a formalized way of defining the relevance of documents for each query under test. The format is used by many IR benchmarking tools and was first introduced by [TREC](https://trec.nist.gov/). For the retrieval optimizer, the format is required for evaluating retrieval performance using metrics like NDCG, recall, precision, and F1. In brief, **Qrels act as “ground truth” for the retrieval optimizer and must follow this structure for the optimization to work as expected.**

**Required** **structure**:

```
{
    "query_id": {
        "corpus_id": relevance_score
    }
}

```

**Example**:

```
{
    "PLAIN-2": {
        "MED-2427": 2,
        "MED-2440": 1,
        "MED-2434": 1,
        "MED-2435": 1,
        "MED-2436": 1
    },
    "PLAIN-12": {
        "MED-2513": 2,
        "MED-5237": 2
    }
}

```

### Define a study YAML

The study config is where you configure the parameters under test and looks like this:

```python
# source data from the step above
corpus: "nfcorpus_corpus.json"
queries: "nfcorpus_queries.json"
qrels: "nfcorpus_qrels.json"

# settings for the index
index_settings:
  name: "optimize"
  vector_field_name: "vector" # name of the vector field to search on
  text_field_name: "text" # name of the text field for lexical search
  from_existing: false
  additional_fields:
    - name: "title"
      type: "text"
  vector_dim: 1536 # should match first embedding model or from_existing

# the embedding models we want to test
embedding_models:
  - type: "openai"
    model: "text-embedding-3-small"
    dim: 1536
    embedding_cache_name: "openai-small-vec-cache"

  - type: "hf"
    model: "sentence-transformers/all-MiniLM-L6-v2"
    dim: 384
    embedding_cache_name: "hf-minilm-vec-cache"

  - type: "hf"
    model: "sentence-transformers/all-mpnet-base-v2"
    dim: 768
    embedding_cache_name: "hf-mpnet-vec-cache"

# the search methods we want to test
search_methods: ["bm25", "vector", "hybrid", "rerank", "weighted_rrf"]

```

### Run a grid study

Once the data is in place and the study_config file, executing the study becomes trivial. Simply import the function, pass the variables, and execute the function. From here, the retrieval optimizer will iteratively run each search method for each embedding model and collect the corresponding results.

```python
import os
from redis_retrieval_optimizer.grid_study import run_grid_study
from redis_retrieval_optimizer.corpus_processors import eval_beir
from dotenv import load_dotenv

# load environment variables containing necessary credentials
load_dotenv()

redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

metrics = run_grid_study(
    config_path="comparison_study_config.yaml",
    redis_url=redis_url,
    corpus_processor=eval_beir.process_corpus
)

```

### Output and analysis

Once complete the metrics variable, shown in the last code block, will be a dataframe containing key information about the average time for each query, overall indexing time, as well as recall, precision, and normalized discounted cumulative gain (ndcg).

From this grid study, we can say that the embedding model had more impact on the overall performance of our retrieval than did the search method. The top 3 results all used OpenAi’s text-embeeding-3-small over the hugging face alternatives. However, this is where the real engineering begins and we can start to offer informed opinions. For example, we can see that using weighted_rrf with the all-mpnet-base-v2 model had the same accuracy as the top 3. But maybe for the system we’re measuring that’s good enough to justify the cost savings of an open source model over hitting the OpenAI service.

![Output and analysis](/images/site-mirror/cdcfdf2131607b8e7457baec0e24f02d55d52696-1600x606.webp)

## Next steps

Hopefully in this blog I have effectively motivated the need for **Eval Driven Development **and highlighted the value that the retrieval optimizer can provide your team. Beyond this first use-case of determining our model and search method selection, the retrieval optimizer can also perform more complex index fine-tuning with bayesian optimization. To see how, when, and why to check that out, see [this blog](https://docs.google.com/document/d/1H_r3s9lYdnmExx1sGW7y2j8Xk-P_q7LL7pZNF3XZgQ0/edit?userstoinvite=rini.vasan@redis.com&sharingaction=manageaccess&role=writer&tab=t.0#heading=h.ptplu4l7fp2z).

A full notebook example of the code above is available [here](https://github.com/redis-applied-ai/redis-retrieval-optimizer/blob/main/docs/examples/grid_study/00_grid_study.ipynb). To follow more of what the Applied AI team is up to at Redis check out the [redis-ai-resources](https://github.com/redis-developer/redis-ai-resources/tree/main) repo.
