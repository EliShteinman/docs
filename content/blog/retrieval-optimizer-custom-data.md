---
title: "Retrieval optimizer: Custom data"
linkTitle: "Retrieval optimizer: Custom data"
url: "/blog/retrieval-optimizer-custom-data/"
description: "In the previous blog posts on grid search and bayesian optimization with the retrieval optimizer we made things easy by pulling pre-defined and formatted data. However, let’s say you have custom..."
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

![Retrieval optimizer: Custom data](/images/site-mirror/f782aec472eb049411771b32bd0dbc76ec6ee4aa-772x552.webp)

In the previous blog posts on [grid search](https://docs.google.com/document/d/16ywR8VnbHrrgtQGB1r4gmpR6e3q3Z7E3fElRvJFUgfY/edit?tab=t.0) and [bayesian optimization](https://docs.google.com/document/d/1H_r3s9lYdnmExx1sGW7y2j8Xk-P_q7LL7pZNF3XZgQ0/edit?tab=t.0) with the retrieval optimizer we made things easy by pulling pre-defined and formatted data. However, let’s say you have custom data in a specific schema with a particular way of querying that you want to test, but it doesn’t fit under the pre-defined functions within the retrieval optimizer. What then? Luckily, the library was designed around this need and makes it very straightforward to define your own processing and search function to be used with the application.

In this blog post, we'll walk through how to define a custom corpus_processor function to transform raw source data into a format that can be efficiently indexed by Redis. We'll also demonstrate how to implement custom search_methods tailored to the specific fields within the dataset, allowing for more flexible and targeted querying. The dataset used in this example consists of text chunks and embeddings derived from car manuals for two different types of vehicles.

## Custom data example

📓A complete code notebook example is available [here](https://github.com/redis-applied-ai/redis-retrieval-optimizer/blob/main/docs/examples/grid_study/01_custom_grid_study.ipynb).

### Corpus

In the previous examples, the corpus data was defined as a large dictionary and only had fields for text and title. This data, however, is different and contains chunked data from a few different car manuals along with query_metadata.

```
[
{
'text': "Mazda3_8Y64-EA-08A_Edition1 Page1 Tuesday, November 27 2007 9:0 AM\n\nForm No.8Y64-EA-08A\n\nBlack plate (1,1)\n\nMazda3_8Y64-EA-08A_Edition1 Page2 Tuesday, November 27 2007 9:0 AM\n\nForm No.8Y64-EA-08A\n\nBlack plate (2,1)\n\nMazda3_8Y64-EA-08A_Edition1 Page3 Tuesday, November 27 2007 9:0 AM\n\nBlack plate (3,1)\n\nA Word to Mazda Owners\n\nThank you for choosing a Mazda. We at Mazda design and build vehicles with complete customer satisfaction in mind.\n\nTo help ensure enjoyable and trouble-free operation of your Mazda, read this manual carefully and follow its recommendations.\n\nAn Authorized Mazda Dealer knows your vehicle best. So when maintenance or service is necessary, that's the place to go.\n\nOur nationwide network of Mazda professionals is dedicated to providing you with the best possible service.\n\nWe assure you that all of us at Mazda have an ongoing interest in your motoring pleasure and in your full satisfaction with your Mazda product.\n\nMazda Motor Corporation HIROSHIMA, JAPAN\n\nImportant Notes About This Manual Keep this manual in the glove box as a handy reference for the safe and enjoyable use of your Mazda. Should you resell the vehicle, leave this manual with it for the next owner.\n\nAll specifications and descriptions are accurate at the time of printing. Because improvement is a constant goal at Mazda, we reserve the right to make changes in specifications at any time without notice and without obligation.\n\nEvent Data Recorder This vehicle is equipped with an event data recorder. In the event of a crash, this device records data related to vehicle dynamics and safety systems for a short period of time. These data can help provide a better understanding of the circumstances in which crashes and injuries occur and lead to the designing of safer vehicles.\n\nAir Conditioning and the Environment Your Mazda's genuine air conditioner is filled with HFC134a (R134a), a refrigerant that has been found not to damage the earth's ozone layer. If the air conditioner does not operate properly, consult an Authorized Mazda Dealer.\n\nPerchlorate Certain components of this vehicle such as [air bag modules, seat belt pretensioners, lithium batteries, ...] may contain Perchlorate Material– Special handling may apply for service or vehicle end of life disposal. See www.dtsc.ca.gov/hazardouswaste/perchlorate.\n\nPlease be aware that this manual applies to all models, equipment and options. As a result, you may find some explanations for equipment not installed on your vehicle.",
 'query_metadata': 
{
'make': 'mazda', 
'model': '3'
},
 'item_id': 'mazda_3:0'
},
...
]

```

### Queries

In addition to the corpus being different, we can also observe that the queries that we want to execute need to leverage additional data provided within the query_metadata attribute.

```
{
'query': 'At what speed should I shift from 2 to 3 with a manual transmission?',
 	'query_metadata': {
'make': 'mazda',
'model': '3'
}
}

```

### Qrels

**Qrels**, short for *query relevance judgments*, are structured annotations that map queries (in this case about cars) to documents (e.g., the chunk with id mazda_3:86) with binary or graded relevance labels. They’e a standard evaluation format from the information retrieval community (originating with TREC) used to assess how well a system retrieves relevant results. In this example, we use qrels to define which car parts are relevant to each car, allowing us to evaluate the performance of a retrieval model.

```
{'car-1': {'mazda_3:86': 1},
 'car-2': {'mazda_3:92': 1, 'mazda_3:93': 1},
 'car-3': {'mazda_3:84': 1, 'mazda_3:75': 1, 'mazda_3:105': 1},
 'car-4': {'mazda_3:188': 1},
 'car-5': {'mazda_3:68': 1, 'mazda_3:69': 1},
 'car-6': {'mazda_3:105': 1, 'mazda_3:83': 1},
 'car-7': {'mazda_3:195': 1, 'mazda_3:194': 1},
 'car-8': {'mazda_3:226': 1,
  'mazda_3:227': 1,
  'mazda_3:229': 1,
  'mazda_3:76': 1},
 'car-9': {'mazda_3:176': 1, 'mazda_3:175': 1},
 'car-10': {'mazda_3:179': 1,
  'mazda_3:209': 1,
  'mazda_3:211': 1,
  'mazda_3:212': 1,
  'mazda_3:213': 1,
  'mazda_3:210': 1}}

```

## Custom search methods

The retrieval optimizer can use any search method that the user has set up within the framework. It must take a SearchMethodInput and output a SearchMethodOutput (see schema definitions [here](https://github.com/redis-applied-ai/redis-retrieval-optimizer/blob/dfc36382efd7e5e06903482a8a23a32bc047f1e9/redis_retrieval_optimizer/schema.py#L14)). The user decides between those two points. You may want to set up many custom query re-writing steps, regex, and/or other ways to get the most out of your search.

The example uses two custom search techniques: one that uses default vector search and one that performs [hybrid search](https://github.com/redis-developer/redis-ai-resources/blob/main/python-recipes/vector-search/02_hybrid_search.ipynb). It uses the query_metadata available with the corpus and queries shown above.

```python
from ranx import Run
from redis_retrieval_optimizer.search_methods.base import run_search_w_time
from redisvl.query import VectorQuery
from redisvl.query.filter import Tag

from redis_retrieval_optimizer.schema import SearchMethodInput, SearchMethodOutput
from redis_retrieval_optimizer.search_methods.vector import make_score_dict_vec

def vector_query(query_info, num_results: int, emb_model) -> VectorQuery:
    vector = emb_model.embed(query_info["query"], as_buffer=True)

    return VectorQuery(
        vector=vector,
        vector_field_name="vector",
        num_results=num_results,
        return_fields=["_id", "make", "model", "text"],  # update to read from env maybe?
    )

def pre_filter_query(query_info, num_results, emb_model) -> VectorQuery:
    vec = emb_model.embed(query_info["query"])
    make = query_info["query_metadata"]["make"]
    model = query_info["query_metadata"]["model"]

    filter = (Tag("make") == make) & (Tag("model") == model)

    # Create a vector query
    query = VectorQuery(
        vector=vec,
        vector_field_name="vector",
        num_results=num_results,
        filter_expression=filter,
        return_fields=["_id", "make", "model", "text"]
    )

    return query

def gather_pre_filter_results(search_method_input: SearchMethodInput) -> SearchMethodOutput:
    redis_res_vector = {}

    for key in search_method_input.raw_queries:
        query_info = search_method_input.raw_queries[key]
        query = pre_filter_query(query_info, 10, search_method_input.emb_model)
        res = run_search_w_time(
            search_method_input.index, query, search_method_input.query_metrics
        )
        score_dict = make_score_dict_vec(res)

        redis_res_vector[key] = score_dict

    return SearchMethodOutput(
        run=Run(redis_res_vector),
        query_metrics=search_method_input.query_metrics,
    )


def gather_vector_results(search_method_input: SearchMethodInput) -> SearchMethodOutput:
    redis_res_vector = {}

    for key in search_method_input.raw_queries:
        text_query = search_method_input.raw_queries[key]
        vec_query = vector_query(text_query, 10, search_method_input.emb_model)
        res = run_search_w_time(
            search_method_input.index, vec_query, search_method_input.query_metrics
        )
        score_dict = make_score_dict_vec(res)
        redis_res_vector[key] = score_dict
        
    return SearchMethodOutput(
        run=Run(redis_res_vector),
        query_metrics=search_method_input.query_metrics,
    )

```

Once defined, you can make use of these functions in your study by creating a search_method_map. A search method map is a simple Python dictionary that maps the string provided in the study config to the user-defined function.

```python
CUSTOM_SEARCH_METHOD_MAP = {
    "basic_vector": gather_vector_results,
    "pre_filter_vector": gather_pre_filter_results,
}

```

## Custom corpus processor

Under the hood, the retrieval optimizer creates a Redis search index and populates it with the provided corpus data. For this process to work, the corpus data must be converted into a list of dictionaries that can be effectively indexed.

This function takes two arguments:

- **corpus** the data to be acted upon
- an **embedding model** since the retrieval optimizer is based around vector search

Note: the get_embedding_model function available with the [redis_retrieval_optimizer utilizes](https://github.com/redis-applied-ai/redis-retrieval-optimizer/blob/c5234185848f009c973b028b465f52ffb0fa3795/redis_retrieval_optimizer/utils.py#L94-L95) an embedding model dictionary and handles initializing the embedding model for you in a way that is usable in the application.

```python
def process_car_corpus(
    corpus, emb_model
):
    corpus_data = []
    corpus_texts = [c["text"] for c in corpus]

    text_embeddings = emb_model.embed_many(corpus_texts, as_buffer=True)

    for i, c in enumerate(corpus):
        corpus_data.append(
            {
                "_id": c["item_id"],
                "text": c["text"],
                "make": c["query_metadata"]["make"],
                "model": c["query_metadata"]["model"],
                "vector": text_embeddings[i],
            }
        )

    return corpus_data

```

## Define study config

Note:

- The search method strings match those of our custom method map
- We’ve added additional fields that correspond to the data attributes we wish to index based on the results of our corpus processor function

```python
# paths to necessary data files
corpus: "data/car_corpus.json" # optional if from_existing
queries: "data/car_queries.json"
qrels: "data/car_qrels.json"

# vector field names
index_settings:
  name: "car"
  prefix: "car" # prefix for index name
  vector_field_name: "vector" # name of the vector field to search on
  text_field_name: "text" # name of the text field for lexical search
  from_existing: false
  additional_fields:
    - name: "make"
      type: "tag"
    - name: "model"
      type: "tag"
  vector_dim: 384 # should match first embedding model or from_existing

# will run all search methods for each embedding model and then iterate
embedding_models: # embedding cache would be awesome here.
# if from_existing is true, first record is assumed to be the one used to create the index
  - type: "hf"
    model: "sentence-transformers/all-MiniLM-L6-v2"
    dim: 384
    embedding_cache_name: "vec-cache" # avoid names with including 'ret-opt' as this can cause collisions

search_methods: ["basic_vector", "pre_filter_vector"] # must match what is passed in search_method_map

```

## Run the study

Now that we have defined our custom search methods and our corpus processor, we can run a study with our custom data.

```python
import os
from redis_retrieval_optimizer.grid_study import run_grid_study
from dotenv import load_dotenv

CUSTOM_SEARCH_METHOD_MAP = {
    "basic_vector": gather_vector_results,
    "pre_filter_vector": gather_pre_filter_results,
}

# load environment variables containing necessary credentials
load_dotenv()

redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

metrics = run_grid_study(
    config_path="custom_grid_study_config.yaml",
    redis_url=redis_url,
    corpus_processor=process_car_corpus,
    search_method_map=CUSTOM_SEARCH_METHOD_MAP,
)

```

## Example output

From this simple study we see that we greatly increased our retrieval performance by making use of our custom query_metadata fields.

![Example output](/images/site-mirror/c919c2a68f77c41182c8905c0c74c83630fb8891-710x74.webp)

## Next steps

In this example you learned:

- How to define a custom corpus processor to leverage source data of arbitrary format in the retrieval optimizer.
- How to define custom search methods to test specific retrieval methods against each other for your app.

You can find a complete notebook example [here](https://github.com/redis-applied-ai/redis-retrieval-optimizer/blob/main/docs/examples/grid_study/01_custom_grid_study.ipynb).
