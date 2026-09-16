---
title: "Getting started with vector sets"
linkTitle: "Getting started with vector sets"
url: "/tutorials/howtos/vector-sets-basics/"
description: "Vector sets are a Redis data type similar to sorted sets. However, instead of associating each element with a numerical score, elements in a vector set are associated with a vector—a list of..."
group: "For AI"
aliases:
- "/tutorials/howtos-vector-sets-basics/"
date: 2026-02-25
lastmod: 2026-03-20
hidden: true
mirrored: true
---

*Published 25 February 2026 · updated 20 March 2026*

> **TL;DR:**
>
> Redis vector sets are a native data type that stores elements with associated vectors for fast similarity search. Use [`VADD`](https://redis.io/docs/latest/commands/vadd/) to insert items with embeddings, and [`VSIM`](https://redis.io/docs/latest/commands/vsim/) to find the nearest neighbors by comparing vectors. Vector sets power use cases like semantic search, recommendation systems, and AI-powered retrieval directly inside Redis.

## What you'll learn

- What Redis vector sets are and when to use them
- How to add elements with vectors using the `VADD` command
- How to perform similarity search against existing elements or custom vectors using `VSIM`
- How to bulk import vector data via Redis Insight
- How to inspect vector sets with utility commands like `VCARD`, `VDIM`, and `VINFO`

## Prerequisites

- **Redis 8** or later with vector sets support enabled
- [Redis Insight](https://redis.io/insight/) (recommended for bulk import and exploring data)
- Familiarity with generating vector embeddings (e.g., via OpenAI, Sentence Transformers, or similar models)

## What are Redis vector sets?

Vector sets are a Redis data type similar to sorted sets. However, instead of associating each element with a numerical score, elements in a vector set are associated with a **vector**—a list of floating-point numbers representing the item in a multi-dimensional space.

This makes vector sets ideal for **similarity search** tasks such as:

- Retrieving the most similar items to the **vector of an existing element** already in the set.
- Retrieving the most similar items to a **specified vector** (e.g., a new embedding not yet in the set).

With these capabilities, vector sets are useful in semantic search, recommendation systems, face recognition, and other apps where vector similarity is important.

```yml

Vector set: "pg:sts"
├── Element ID: "s1"
│     ├── Vector: [-0.010130, -0.026101, …] (1536 dimensions)
│     └── Attributes:
│          {
│            "sentence": "A young child is riding a horse.",
│            "activityType": "people",
│            "wordCount": 7,
│            "charCount": 32
│          }
├── Element ID: "s2"
│     ├── Vector: [-0.011102, -0.034598, …]
│     └── Attributes: {...}
└── …
```

A vector set is a collection of elements, each associated with a vector and optional custom attributes.

In the above representation:

- **Vector set key** is `"pg:sts"`
- **Element IDs** are sentences identified by `"s1"`, `"s2"`, etc., each storing a vector and custom attributes required for future filtering or inspection.

## How do you add items to a Redis vector set?

You can add items to a vector set using the [`VADD`](https://redis.io/docs/latest/commands/vadd/) command.

### VADD syntax

```bash
VADD {vectorSetKey} VALUES {embeddingDimension} {embeddingValues...} {elementId} SETATTR {elementAttributesAsJSON}
```

Parameters:

- {vectorSetKey} – The name of your vector set.
- {embeddingDimension} – The length of the vector (number of dimensions).
- {embeddingValues...} – The vector values (space-separated floats).
- {elementId} – A unique identifier for this element in the set.
- {elementAttributesAsJSON} – A JSON object containing any metadata about the element, making it easy to filter or inspect later.

```bash
VADD "pg:sts" VALUES 1536 -0.010130 -0.026101 ... "s1" SETATTR '{"sentence":"A young child is riding a horse.","activityType":"people","wordCount":7,"charCount":32}'
```

### How do you bulk import vector data?

The full **Semantic Textual Similarity (STS) Development Set** used in this tutorial is [available here](https://github.com/redis-developer/redis-datasets/blob/master/core/vectorsets/sts-dev-ds/sts-dev-open-ai.redis).

Upload that file into [Redis Insight](https://redis.io/insight/):

- Click `**Bulk Actions**` -> choose `**Upload Data**` tab -> upload the file and click `**Upload**`

![Redis Insight Bulk Actions interface for uploading a data file](/images/site-mirror/678b51a2738449498d1e5f02aa83f8aefa798603-1038x567.webp)

- Post upload, you can see the status of the upload data

![Redis Insight displaying the status and success of a bulk data upload](/images/site-mirror/fd1c542dc1f76bd14b838dcbbdded52379b4d284-1038x570.webp)

## How do you search by similarity with existing elements?

The [`VSIM`](https://redis.io/docs/latest/commands/vsim/) command allows you to find elements in a vector set that are most similar to the vector of an **existing element** in the same set.

This is useful when you already have an element in your dataset and want to find others that are semantically or visually close to it—a common pattern in recommendation systems and "more like this" features.

### VSIM with existing elements

```bash
VSIM {vectorSetKey} ELE {elementId} WITHSCORES WITHATTRIBS
```

Parameters:

- {vectorSetKey} – The name of your vector set.
- ELE {elementId} – The ID of the element whose vector you want to use for similarity search.
- WITHSCORES – Returns the similarity score for each result.
- WITHATTRIBS – Returns the stored attributes (metadata) for each result.

```bash
# Retrieve elements similar to existing element 's4' (Sentence 4)
VSIM "pg:sts" ELE "s4" WITHSCORES WITHATTRIBS COUNT 5
```

```json
[
    "s4",
    "1",
    "{\"sentence\":\"The man is feeding a mouse to the snake.\",\"activityType\":\"people\",\"wordCount\":9,\"charCount\":40}",
    "s3",
    "0.9913436630740762",
    "{\"sentence\":\"A man is feeding a mouse to a snake.\",\"activityType\":\"people\",\"wordCount\":9,\"charCount\":36}",
    "s424",
    "0.9541677162051201",
    "{\"sentence\":\"The man is trying to feed the snake with a mouse.\",\"activityType\":\"people\",\"wordCount\":11,\"charCount\":49}",
    "s1585",
    "0.7106717228889465",
    "{\"sentence\":\"As mentioned in previous answers, rats and gerbils can be offered instead of mice or in a rotation with mice.\",\"activityType\":\"other\",\"wordCount\":20,\"charCount\":109}",
    "s431",
    "0.6881625354290009",
    "{\"sentence\":\"The cat tried to eat the corn on the cob.\",\"activityType\":\"animals\",\"wordCount\":10,\"charCount\":41}"
]
```

```yml
Query: "Find items similar to element 's4'"

pg:sts
 ├── s4  (query element)
 │     Vector: [...]
 │     Attributes: { "sentence": "The man is feeding a mouse to the snake.", ... }
 │
 ├── s3  (score: 0.9913)  → "A man is feeding a mouse to a snake."
 ├── s424 (score: 0.9541) → "The man is trying to feed the snake with a mouse."
 ├── s1585 (score: 0.7106) → "Rats and gerbils can be offered instead of mice..."
 └── s431  (score: 0.6881) → "The cat tried to eat the corn on the cob."
```

### Try element similarity in the Redis sandbox

You can experiment with [Element similarity queries](https://redis.io/try/sandbox?queryId=VECTOR_SETS_ELE_SIMILARITY_WITH_SCORES&catId=VECTOR_SETS_ELE_SIMILARITY) in the Redis Sandbox:

- Element similarity with scores and count example

![Redis Sandbox environment showing results for an element similarity search with VSIM ELE command](/images/site-mirror/6cff0e8a6a0dadf613eea3b5db3de4f9f82aac0e-1038x512.webp)

- Element similarity with logical filter

![Redis Sandbox showing VSIM element similarity results filtered by activityType attribute](/images/site-mirror/5d4e0ccec39c8d5fc3435b0aa0c27c0a397ca91f-1038x510.webp)

> **TIP**
>
> In the Redis sandbox, explore additional filter options in the left sidebar, including arithmetic filters, comparison filters, and containment filters.

## How do you search with a new vector (KNN query)?

The [`VSIM`](https://redis.io/docs/latest/commands/vsim/) command can also search for elements similar to a **vector you provide directly**, instead of using an existing element's vector. This is a K-nearest neighbor (KNN) query.

This is useful when:

- You have a **new piece of text, image, or audio** not in your dataset.
- You have already generated its vector embeddings using the **same model and dimensions** used when seeding the vector set.

### VSIM with specified vectors

```bash
VSIM {vectorSetKey} VALUES {embeddingDimension} {embeddingValues...} WITHSCORES WITHATTRIBS
```

Where:

- {vectorSetKey} – The name of your vector set.
- VALUES {embeddingDimension} {embeddingValues...} – The embedding vector to compare against.
- WITHSCORES – Returns the similarity score for each result.
- WITHATTRIBS – Returns the stored attributes (metadata) for each result.
- COUNT N (optional) – Limits the number of results returned.

```bash
# Retrieve the top 5 elements similar to the phrase "She is playing a guitar"
VSIM "pg:sts" VALUES 1536 0.000534 0.034054 ... WITHSCORES WITHATTRIBS COUNT 5
```

> **NOTE**
>
> Before running this query, convert your search text into vector embeddings using the same model (and dimensionality) as the one used to seed the dataset. For example, if the dataset was built using OpenAI's text-embedding-ada-002 model (1536 dimensions), use the same for the query.

```json
[
    "s292",
    "0.8956013321876526",
    "{\"sentence\":\"The girl is playing the guitar.\",\"activityType\":\"people\",\"wordCount\":6,\"charCount\":31}",
    "s117",
    "0.8890393897891045",
    "{\"sentence\":\"A woman is playing a guitar.\",\"activityType\":\"people\",\"wordCount\":6,\"charCount\":28}",
    "s5",
    "0.8769233152270317",
    "{\"sentence\":\"A woman is playing the guitar.\",\"activityType\":\"people\",\"wordCount\":6,\"charCount\":30}",
    "s232",
    "0.863240122795105",
    "{\"sentence\":\"A woman plays an electric guitar.\",\"activityType\":\"people\",\"wordCount\":6,\"charCount\":33}",
    "s271",
    "0.8623353093862534",
    "{\"sentence\":\"A person is playing a guitar.\",\"activityType\":\"people\",\"wordCount\":6,\"charCount\":29}"
]
```

```bash
Query Vector: [0.000534, 0.034054, ...]  (1536 dimensions)
Phrase: "She is playing a guitar"

pg:sts
 ├── s292  (score: 0.8956) → "The girl is playing the guitar."
 ├── s117  (score: 0.8890) → "A woman is playing a guitar."
 ├── s5    (score: 0.8769) → "A woman is playing the guitar."
 ├── s232  (score: 0.8632) → "A woman plays an electric guitar."
 └── s271  (score: 0.8623) → "A person is playing a guitar."
```

### Try value similarity in the Redis sandbox

Experiment with [Value similarity queries](https://redis.io/try/sandbox?queryId=VECTOR_SETS_VALUE_SIMILARITY_WITH_SCORES&catId=VECTOR_SETS_VALUE_SIMILARITY) in the Redis Sandbox:

Value similarity with scores and count example

![Redis Sandbox showing KNN similarity search results for a provided query vector using VSIM VALUES](/images/site-mirror/3161f5cf6b85b3aaf76d8c4b31948b9284c220f5-1038x514.webp)

Value similarity with logical filter

![Redis Sandbox showing VSIM value similarity results filtered with a logical attribute filter](/images/site-mirror/3065d99d7db5ec9b3ccccbc12ea60793d75e2863-1038x510.webp)

> **TIP**
>
> In the Redis sandbox, explore additional filter options in the left sidebar, including arithmetic filters, comparison filters, and containment filters.

## What other vector set commands are available?

Vector sets in Redis support several utility commands that let you inspect, debug, and retrieve metadata, attributes, or structure-related information.

- [`VCARD`](https://redis.io/docs/latest/commands/vcard/) – Count elements.
- [`VDIM`](https://redis.io/docs/latest/commands/vdim/) – Get vector dimensions.
- [`VEMB`](https://redis.io/docs/latest/commands/vemb/) – Get vector for an element.
- [`VGETATTR`](https://redis.io/docs/latest/commands/vgetattr/) – Get attributes for an element.
- [`VINFO`](https://redis.io/docs/latest/commands/vinfo/) – Get metadata about the vector set.
- [`VISMEMBER`](https://redis.io/docs/latest/commands/vismember/) – Check if an element exists.
- [`VLINKS`](https://redis.io/docs/latest/commands/vlinks/) – Get neighbors in the HNSW graph.
- [`VRANDMEMBER`](https://redis.io/docs/latest/commands/vrandmember/) – Get random elements.

### Commands

```bash
#  Retrieve number of elements in the vector set
VCARD 'pg:sts'

# Output
2898
```

```bash
# Retrieve number of dimensions of the vectors in the vector set
VDIM 'pg:sts'

# Output
1536
```

```bash
#  Retrieve the approximate vector associated with a given element in the vector set.
VEMB 'pg:sts' 's4'

# output
[
    -0.000534,
    -0.034054,
    ...
]
```

```bash
# Retrieve the JSON attributes associated with an element in a vector set.
VGETATTR 'pg:sts' 's4'

# Output
{
  "sentence": "The man is feeding a mouse to the snake.",
  "activityType": "people",
  "wordCount": 9,
  "charCount": 40
}
```

```bash
# Retrieve metadata and internal details about a vector set, including size, dimensions, quantization type, and graph structure.
VINFO 'pg:sts'

# output
[
    "quant-type",
    "int8",
    "hnsw-m",
    16,
    "vector-dim",
    1536,
    "projection-input-dim",
    0,
    "size",
    2898,
    "max-level",
    5,
    "attributes-count",
    2898,
    "vset-uid",
    1,
    "hnsw-max-node-uid",
    2898
]
```

```bash
# Check if an element exists in a vector set.
VISMEMBER 'pg:sts' 's4'

# Output
1
```

```bash
# Retrieve the neighbors of a specified element in a vector set. The command shows the connections for each layer of the HNSW graph.
VLINKS 'pg:sts' 's4' WITHSCORES

# Output
[
    [
        "s3",
        "0.9913524389266968",
        "s48",
        "0.6641438603401184",
        "s41",
        "0.6403481364250183",
        "s143",
        "0.6444393396377563",
        ....
    ]
]
```

```bash
# Retrieve one or more random elements from a vector set.
VRANDMEMBER 'pg:sts' 5

# Output
[
    "s2602",
    "s989",
    "s409",
    "s349",
    "s547"
]
```

### Try vector set commands in the Redis sandbox

Experiment with [other vector set commands](https://redis.io/try/sandbox?queryId=VECTOR_SETS_INSIGHTS_VCARD&catId=VECTOR_SETS_INSIGHTS) in the Redis sandbox:

![Redis Sandbox interface showing VCARD, VDIM, and other vector set utility commands with output](/images/site-mirror/b6546d3ae8b526fd46574ebb5f6e51042f01ee8c-1038x507.webp)

> **TIP**
>
> In the Redis sandbox, you can select a command from the left sidebar, click the Run button, and instantly see the output.

## How do vector sets compare to vector indexing with Redis Search?

Redis offers two ways to work with vectors:

| Feature           | Vector sets                                                                 | Redis Search vector indexing                                    |
| ----------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------- |
| **Data type**     | Native `VSET` type (Redis 8+)                                               | Vectors stored in hashes or JSON, indexed via `FT.CREATE`       |
| **Indexing**      | Built-in HNSW graph, automatic                                              | Requires explicit index creation with `FT.CREATE`               |
| **Query command** | `VSIM`                                                                      | `FT.SEARCH` with KNN syntax                                     |
| **Filtering**     | Attribute-based filters in `VSIM`                                           | Full-text, tag, numeric, and geo filters via query syntax       |
| **Best for**      | Lightweight similarity search, real-time recommendations, rapid prototyping | Complex queries combining vector search with structured filters |
| **Schema**        | Schema-free; attributes are arbitrary JSON                                  | Schema defined at index creation                                |

**Use vector sets** when you need a simple, fast path to nearest-neighbor search with minimal setup. **Use Redis Search** when you need to combine vector similarity with rich filtering, full-text search, or aggregation across structured data.

For a hands-on walkthrough using Redis Search for vector search, see the [Vector similarity search tutorial](/tutorials/howtos/solutions/vector/getting-started-vector/).

## Ready to use Redis vector sets?

You've learned how to:

- Add elements to a vector set with `VADD`.
- Run similarity searches using existing elements or custom query vectors with `VSIM`.
- Perform KNN queries against new embeddings.
- Use utility commands to inspect and explore your data.

Vector sets provide fast, scalable nearest-neighbor search natively in Redis — perfect for semantic search, recommendations, and AI-powered retrieval.

## Next steps

- Try the [Redis sandbox](https://redis.io/try/sandbox/) links throughout this guide.
- Import your own data and test queries.
- Explore the full [vector sets data type documentation](https://redis.io/docs/latest/develop/data-types/vector-sets/).
- Learn about [vector similarity search with Redis Search](/tutorials/howtos/solutions/vector/getting-started-vector/).
- Build a [semantic text search application](/tutorials/howtos/solutions/vector/semantic-text-search/) using Redis vectors.
- Dive into the [VADD](https://redis.io/docs/latest/commands/vadd/) and [VSIM](https://redis.io/docs/latest/commands/vsim/) command references.
