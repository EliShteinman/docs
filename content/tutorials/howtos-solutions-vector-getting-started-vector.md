---
title: "How to Perform Vector Similarity Search Using Redis in NodeJS"
linkTitle: "How to Perform Vector Similarity Search Using Redis in NodeJS"
url: "/tutorials/howtos/solutions/vector/getting-started-vector/"
description: "In the context of machine learning, a vector is a mathematical representation of data. It is an ordered list of numbers that encode the features or attributes of a piece of data."
group: "For developers"
aliases:
- "/tutorials/howtos-solutions-vector-getting-started-vector/"
date: 2026-02-25
lastmod: 2026-02-25
hidden: true
mirrored: true
---

*Published 25 February 2026*

> **TL;DR:**
>
> To perform vector similarity search with Redis, store your data as JSON documents, generate vector embeddings (using models like Hugging Face Transformers), index them with `FT.CREATE` using FLAT or HNSW algorithms, and query with KNN (`FT.SEARCH` with `[KNN ...]`) or range queries (`VECTOR_RANGE`). Redis supports L2, cosine, and inner product distance metrics out of the box.

## What you'll learn

- What vectors, vector databases, and vector similarity are
- How to generate text and image embeddings using Hugging Face Transformers and TensorFlow
- How to store vector data in Redis JSON documents
- How to create a Redis vector index with FLAT and HNSW algorithms
- How to run KNN (k-Nearest Neighbors) queries to find the most similar vectors
- How to run range queries to retrieve vectors within a given distance
- How Euclidean distance, cosine similarity, and inner product calculations work

## Prerequisites

- **Node.js** v18 or later installed
- A **Redis Cloud** instance (or local Redis Stack with the Search module) — [get started free](https://redis.io/try-free/)
- Basic familiarity with JavaScript/TypeScript and npm
- (Optional) [Redis Insight](https://redis.io/insight/) for visually exploring your data

## What are vectors and why do they matter?

### What is a vector in machine learning?

In the context of machine learning, a vector is a mathematical representation of data. It is an ordered list of numbers that encode the features or attributes of a piece of data.

Vectors can be thought of as points in a multi-dimensional space where each dimension corresponds to a feature. **For example**, consider a simple dataset about ecommerce `products`. Each product might have features such as `price`, `quality`, and `popularity`.

| **Id** | **Product**                              | Price ($) | Quality (1 - 10) | Popularity (1 - 10) |
| ------ | ---------------------------------------- | --------- | ---------------- | ------------------- |
| 1      | Puma Men Race Black Watch                | 150       | 5                | 8                   |
| 2      | Puma Men Top Fluctuation Red Black Watch | 180       | 7                | 6                   |
| 3      | Inkfruit Women Behind Cream Tshirt       | 5         | 9                | 7                   |

Now, product 1 `Puma Men Race Black Watch` might be represented as the vector `[150, 5, 8]`

In a more complex scenario, like natural language processing (NLP), words or entire sentences can be converted into dense vectors (often referred to as embeddings) that capture the semantic meaning of the text.Vectors play a foundational role in many machine learning algorithms, particularly those that involve distance measurements, such as clustering and classification algorithms.

### What is a vector database?

A vector database is a specialized system optimized for storing and searching vectors. Designed explicitly for efficiency, these databases play a crucial role in powering vector search apps, including recommendation systems, image search, and textual content retrieval. Often referred to as vector stores, vector indexes, or vector search engines, these databases employ vector similarity algorithms to identify vectors that closely match a given query vector.

> **TIP**
>
> [**Redis Cloud**](https://redis.io/try-free/) is a popular choice for vector databases, as it offers a rich set of data structures and commands that are well-suited for vector storage and search. Redis Cloud allows you to index vectors and perform vector similarity search in a few different ways outlined further in this tutorial. It also maintains a high level of performance and scalability.

### What is vector similarity?

Vector similarity is a measure that quantifies how alike two vectors are, typically by evaluating the `distance` or `angle` between them in a multi-dimensional space. When vectors represent data points, such as texts or images, the similarity score can indicate how similar the underlying data points are in terms of their features or content.

#### Use cases for vector similarity

- **Recommendation Systems**: If you have vectors representing user preferences or item profiles, you can quickly find items that are most similar to a user's preference vector.
- **Image Search**: Store vectors representing image features, and then retrieve images most similar to a given image's vector.
- **Textual Content Retrieval**: Store vectors representing textual content (e.g., articles, product descriptions) and find the most relevant texts for a given query vector.

> **CALCULATING VECTOR SIMILARITY**
>
> If you're interested in learning more about the mathematics behind vector similarity, scroll down to the [**How to calculate vector similarity?**](#how-is-vector-similarity-calculated) section.

## How do you generate vector embeddings?

In our scenario, our focus revolves around generating sentence (product description) and image (product image) embeddings or vectors. There's an abundance of AI model repositories, like GitHub, where AI models are pre-trained, maintained, and shared.

For sentence embeddings, we'll employ a model from [Hugging Face Model Hub](https://huggingface.co/models), and for image embeddings, one from [TensorFlow Hub](https://tfhub.dev/) will be leveraged for variety.

> **GITHUB CODE**
>
> Below is a command to the clone the source code used in this tutorial
>
> git clone [https://github.com/redis-developer/redis-vector-nodejs-solutions.git](https://github.com/redis-developer/redis-vector-nodejs-solutions.git)

### How do you generate sentence and text embeddings?

To generate sentence embeddings, we'll make use of a Hugging Face model titled [Xenova/all-distilroberta-v1](https://huggingface.co/Xenova/all-distilroberta-v1). It's a compatible version of [sentence-transformers/all-distilroberta-v1](https://huggingface.co/sentence-transformers/all-distilroberta-v1) for transformer.js with ONNX weights.

> **INFO**
>
> [Hugging Face Transformers](https://huggingface.co/docs/transformers.js/index) is a renowned open-source tool for Natural Language Processing (NLP) tasks. It simplifies the use of cutting-edge NLP models.
>
> The transformers.j library is essentially the JavaScript version of Hugging Face's popular Python library.

> **INFO**
>
> [ONNX (Open Neural Network eXchange)](https://onnx.ai/) is an open standard that defines a common set of operators and a common file format to represent deep learning models in a wide variety of frameworks, including PyTorch and TensorFlow

Below, you'll find a Node.js code snippet that illustrates how to create vector embeddings for any provided `sentence`:

```bash
npm install @xenova/transformers
```

```javascript
import * as transformers from "@xenova/transformers";

async function generateSentenceEmbeddings(_sentence): Promise<number[]> {
  let modelName = "Xenova/all-distilroberta-v1";
  let pipe = await transformers.pipeline("feature-extraction", modelName);

  let vectorOutput = await pipe(_sentence, {
    pooling: "mean",
    normalize: true,
  });

  const embeddings: number[] = Object.values(vectorOutput?.data);
  return embeddings;
}

export { generateSentenceEmbeddings };
```

Here's a glimpse of the vector output for a sample text:

```javascript
const embeddings = await generateSentenceEmbeddings('I Love Redis !');
console.log(embeddings);
/*
 768 dim vector output
 embeddings = [
    -0.005076113156974316,  -0.006047232076525688,   -0.03189406543970108,
    -0.019677048549056053,    0.05152582749724388,  -0.035989608615636826,
    -0.009754283353686333,   0.002385444939136505,   -0.04979122802615166,
    ....]
*/
```

### How do you generate image embeddings?

To obtain image embeddings, we'll leverage the [mobilenet](https://github.com/tensorflow/tfjs-models/tree/master/mobilenet) model from TensorFlow.

Below, you'll find a Node.js code snippet that illustrates how to create vector embeddings for any provided image:

```bash
npm i @tensorflow/tfjs @tensorflow/tfjs-node @tensorflow-models/mobilenet jpeg-js
```

```javascript
import * as tf from "@tensorflow/tfjs-node";
import * as mobilenet from "@tensorflow-models/mobilenet";

import * as jpeg from "jpeg-js";

import * as path from "path";
import { fileURLToPath } from "url";
import * as fs from "fs/promises";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function decodeImage(imagePath) {
  imagePath = path.join(__dirname, imagePath);

  const buffer = await fs.readFile(imagePath);
  const rawImageData = jpeg.decode(buffer);
  const imageTensor = tf.browser.fromPixels(rawImageData);
  return imageTensor;
}

async function generateImageEmbeddings(imagePath: string) {
  const imageTensor = await decodeImage(imagePath);

  // Load MobileNet model
  const model = await mobilenet.load();

  // Classify and predict what the image is
  const prediction = await model.classify(imageTensor);
  console.log(`${imagePath} prediction`, prediction);

  // Preprocess the image and get the intermediate activation.
  const activation = model.infer(imageTensor, true);

  // Convert the tensor to a regular array.
  const vectorOutput = await activation.data();

  imageTensor.dispose(); // Clean up tensor

  return vectorOutput; //DIM 1024
}
```

![Sample Puma watch product image used to generate image vector embeddings with TensorFlow MobileNet](/images/site-mirror/ab4615450410946af330b71965845ab6260db2b1-480x640.webp)

Below is an illustration of the vector output for a sample watch image:

```javascript
//watch image
const imageEmbeddings = await generateImageEmbeddings('images/11001.jpg');
console.log(imageEmbeddings);
/*
 1024 dim vector output
 imageEmbeddings = [
    0.013823275454342365,    0.33256298303604126,                     0,
    2.2764432430267334,    0.14010703563690186,     0.972867488861084,
    1.2307443618774414,      2.254523992538452,   0.44696325063705444,
    ....]

  images/11001.jpg (mobilenet model) prediction [
  { className: 'digital watch', probability: 0.28117117285728455 },
  { className: 'spotlight, spot', probability: 0.15369531512260437 },
  { className: 'digital clock', probability: 0.15267866849899292 }
]
*/
```

## How do you set up Redis as a vector database?

> **GITHUB CODE**
>
> Below is a command to the clone the source code used in this tutorial
>
> git clone [https://github.com/redis-developer/redis-vector-nodejs-solutions.git](https://github.com/redis-developer/redis-vector-nodejs-solutions.git)

### How do you seed sample data into Redis?

For the purposes of this tutorial, let's consider a simplified e-commerce context. The `products` JSON provided offers a glimpse into vector search functionalities we'll be discussing.

```javascript
const products = [
    {
        _id: '1',
        price: 4950,
        productDisplayName: 'Puma Men Race Black Watch',
        brandName: 'Puma',
        ageGroup: 'Adults-Men',
        gender: 'Men',
        masterCategory: 'Accessories',
        subCategory: 'Watches',
        imageURL: 'images/11002.jpg',
        productDescription:
            '<p>This watch from puma comes in a heavy duty design. The asymmetric dial and chunky casing gives this watch a tough appearance perfect for navigating the urban jungle.<br /><strong><br />Dial shape</strong>: Round<br /><strong>Case diameter</strong>: 32 cm<br /><strong>Warranty</strong>: 2 Years<br /><br />Stainless steel case with a fixed bezel for added durability, style and comfort<br />Leather straps with a tang clasp for comfort and style<br />Black dial with cat logo on the 12 hour mark<br />Date aperture at the 3 hour mark<br />Analog time display<br />Solid case back made of stainless steel for enhanced durability<br />Water resistant upto 100 metres</p>',
    },
    {
        _id: '2',
        price: 5450,
        productDisplayName: 'Puma Men Top Fluctuation Red Black Watches',
        brandName: 'Puma',
        ageGroup: 'Adults-Men',
        gender: 'Men',
        masterCategory: 'Accessories',
        subCategory: 'Watches',
        imageURL: 'images/11001.jpg',
        productDescription:
            '<p style="text-align: justify;">This watch from puma comes in a clean sleek design. This active watch is perfect for urban wear and can serve you well in the gym or a night of clubbing.<br /><strong><br />Case diameter</strong>: 40 mm&lt;</p>',
    },

    {
        _id: '3',
        price: 499,
        productDisplayName: 'Inkfruit Women Behind Cream Tshirts',
        brandName: 'Inkfruit',
        ageGroup: 'Adults-Women',
        gender: 'Women',
        masterCategory: 'Apparel',
        subCategory: 'Topwear',
        imageURL: 'images/11008.jpg',
        productDescription:
            '<p><strong>Composition</strong><br />Yellow round neck t-shirt made of 100% cotton, has short sleeves and graphic print on the front<br /><br /><strong>Fitting</strong><br />Comfort<br /><br /><strong>Wash care</strong><br />Hand wash separately in cool water at 30 degrees <br />Do not scrub <br />Do not bleach <br />Turn inside out and dry flat in shade <br />Warm iron on reverse<br />Do not iron on print<br /><br />Flaunt your pretty, long legs in style with this inkfruit t-shirt. The graphic print oozes sensuality, while the cotton fabric keeps you fresh and comfortable all day. Team this with a short denim skirt and high-heeled sandals and get behind the wheel in style.<br /><br /><em>Model statistics</em><br />The model wears size M in t-shirts <br />Height: 5\'7", Chest: 33"</p>',
    },
];
```

Below is the sample code to seed products data as JSON in Redis. The data also includes vectors of both product descriptions and images.

```javascript
async function addProductWithEmbeddings(_products) {
    const nodeRedisClient = getNodeRedisClient();

    if (_products && _products.length) {
        for (let product of _products) {
            console.log(
                `generating description embeddings for product ${product._id}`,
            );
            const sentenceEmbedding = await generateSentenceEmbeddings(
                product.productDescription,
            );
            product['productDescriptionEmbeddings'] = sentenceEmbedding;

            console.log(
                `generating image embeddings for product ${product._id}`,
            );
            const imageEmbedding = await generateImageEmbeddings(
                product.imageURL,
            );
            product['productImageEmbeddings'] = imageEmbedding;

            await nodeRedisClient.json.set(`products:${product._id}`, '$', {
                ...product,
            });
            console.log(`product ${product._id} added to redis`);
        }
    }
}
```

You can observe products JSON data in Redis Insight:

![Redis Insight showing JSON product documents with vector embeddings stored in Redis](/images/site-mirror/6599e41fc07a212ead73c979b5c0a4b17ddcc055-1024x557.webp)

> **TIP**
>
> Download [Redis Insight](https://redis.io/insight/) to visually explore your Redis data or to engage with raw Redis commands in the workbench.

### How do you create a vector index in Redis?

For searches to be conducted on JSON fields in Redis, they must be indexed. The methodology below highlights the process of indexing different types of fields. This encompasses vector fields such as `productDescriptionEmbeddings` and `productImageEmbeddings`.

```javascript
import {
  createClient,
  SchemaFieldTypes,
  VectorAlgorithms,
  RediSearchSchema,
} from "redis";

const PRODUCTS_KEY_PREFIX = "products";
const PRODUCTS_INDEX_KEY = "idx:products";
const REDIS_URI = "redis://localhost:6379";
let nodeRedisClient = null;

const getNodeRedisClient = async () => {
  if (!nodeRedisClient) {
    nodeRedisClient = createClient({ url: REDIS_URI });
    await nodeRedisClient.connect();
  }
  return nodeRedisClient;
};

const createRedisIndex = async () => {
  /*    (RAW COMMAND)
          FT.CREATE idx:products
          ON JSON
              PREFIX 1 "products:"
          SCHEMA
          "$.productDisplayName" as productDisplayName TEXT NOSTEM SORTABLE
          "$.brandName" as brandName TEXT NOSTEM SORTABLE
          "$.price" as price NUMERIC SORTABLE
          "$.masterCategory" as "masterCategory" TAG
          "$.subCategory" as subCategory TAG
          "$.productDescriptionEmbeddings" as productDescriptionEmbeddings VECTOR "FLAT" 10
                  "TYPE" FLOAT32
                  "DIM" 768
                  "DISTANCE_METRIC" "L2"
                  "INITIAL_CAP" 111
                  "BLOCK_SIZE"  111
          "$.productDescription" as productDescription TEXT NOSTEM SORTABLE
          "$.imageURL" as imageURL TEXT NOSTEM
          "$.productImageEmbeddings" as productImageEmbeddings VECTOR "HNSW" 8
                          "TYPE" FLOAT32
                          "DIM" 1024
                          "DISTANCE_METRIC" "COSINE"
                          "INITIAL_CAP" 111

      */
  const nodeRedisClient = await getNodeRedisClient();

  const schema: RediSearchSchema = {
    "$.productDisplayName": {
      type: SchemaFieldTypes.TEXT,
      NOSTEM: true,
      SORTABLE: true,
      AS: "productDisplayName",
    },
    "$.brandName": {
      type: SchemaFieldTypes.TEXT,
      NOSTEM: true,
      SORTABLE: true,
      AS: "brandName",
    },
    "$.price": {
      type: SchemaFieldTypes.NUMERIC,
      SORTABLE: true,
      AS: "price",
    },
    "$.masterCategory": {
      type: SchemaFieldTypes.TAG,
      AS: "masterCategory",
    },
    "$.subCategory": {
      type: SchemaFieldTypes.TAG,
      AS: "subCategory",
    },
    "$.productDescriptionEmbeddings": {
      type: SchemaFieldTypes.VECTOR,
      TYPE: "FLOAT32",
      ALGORITHM: VectorAlgorithms.FLAT,
      DIM: 768,
      DISTANCE_METRIC: "L2",
      INITIAL_CAP: 111,
      BLOCK_SIZE: 111,
      AS: "productDescriptionEmbeddings",
    },
    "$.productDescription": {
      type: SchemaFieldTypes.TEXT,
      NOSTEM: true,
      SORTABLE: true,
      AS: "productDescription",
    },
    "$.imageURL": {
      type: SchemaFieldTypes.TEXT,
      NOSTEM: true,
      AS: "imageURL",
    },
    "$.productImageEmbeddings": {
      type: SchemaFieldTypes.VECTOR,
      TYPE: "FLOAT32",
      ALGORITHM: VectorAlgorithms.HNSW, //Hierarchical Navigable Small World graphs
      DIM: 1024,
      DISTANCE_METRIC: "COSINE",
      INITIAL_CAP: 111,
      AS: "productImageEmbeddings",
    },
  };
  console.log(`index ${PRODUCTS_INDEX_KEY} created`);

  try {
    await nodeRedisClient.ft.dropIndex(PRODUCTS_INDEX_KEY);
  } catch (indexErr) {
    console.error(indexErr);
  }
  await nodeRedisClient.ft.create(PRODUCTS_INDEX_KEY, schema, {
    ON: "JSON",
    PREFIX: PRODUCTS_KEY_PREFIX,
  });
};
```

> **FLAT VS HNSW INDEXING**
>
> FLAT: When vectors are indexed in a "FLAT" structure, they're stored in their original form without any added hierarchy. A search against a FLAT index will require the algorithm to scan each vector linearly to find the most similar matches. While this is accurate, it's computationally intensive and slower, making it ideal for smaller datasets.
>
> HNSW (Hierarchical Navigable Small World): HNSW is a graph-centric method tailored for indexing high-dimensional data. With larger datasets, linear comparisons against every vector in the index become time-consuming. HNSW employs a probabilistic approach, ensuring faster search results but with a slight trade-off in accuracy.

> **INITIAL_CAP AND BLOCK_SIZE PARAMETERS**
>
> Both INITIAL_CAP and BLOCK_SIZE are configuration parameters that control how vectors are stored and indexed.
>
> INITIAL_CAP defines the initial capacity of the vector index. It helps in pre-allocating space for the index.
>
> BLOCK_SIZE defines the size of each block of the vector index. As more vectors are added, Redis will allocate memory in chunks, with each chunk being the size of the BLOCK_SIZE. It helps in optimizing the memory allocations during index growth.

## How does KNN vector search work in Redis?

KNN, or k-Nearest Neighbors, is an algorithm used in both classification and regression tasks, but when referring to "KNN Search," we're typically discussing the task of finding the "k" points in a dataset that are closest (most similar) to a given query point. In the context of vector search, this means identifying the "k" vectors in our database that are most similar to a given query vector, usually based on some distance metric like cosine similarity or Euclidean distance.

### How do you run a KNN query with Redis?

Redis allows you to index and then search for vectors [using the KNN approach](https://redis.io/docs/latest/develop/ai/search-and-query/vectors/).

Below, you'll find a Node.js code snippet that illustrates how to perform `KNN query` for any provided `search text`:

```javascript
const float32Buffer = (arr) => {
    const floatArray = new Float32Array(arr);
    const float32Buffer = Buffer.from(floatArray.buffer);
    return float32Buffer;
};
const queryProductDescriptionEmbeddingsByKNN = async (
    _searchTxt,
    _resultCount,
) => {
    //A KNN query will give us the top n documents that best match the query vector.

    /*  sample raw query

        FT.SEARCH idx:products
        "*=>[KNN 5 @productDescriptionEmbeddings $searchBlob AS score]"
        RETURN 4 score brandName productDisplayName imageURL
        SORTBY score
        PARAMS 2 searchBlob "6\xf7\..."
        DIALECT 2

    */
    //https://redis.io/docs/latest/develop/ai/search-and-query/

    console.log(`queryProductDescriptionEmbeddingsByKNN started`);
    let results = {};
    if (_searchTxt) {
        _resultCount = _resultCount ?? 5;

        const nodeRedisClient = getNodeRedisClient();
        const searchTxtVectorArr = await generateSentenceEmbeddings(_searchTxt);

        const searchQuery = `*=>[KNN ${_resultCount} @productDescriptionEmbeddings $searchBlob AS score]`;

        results = await nodeRedisClient.ft.search(
            PRODUCTS_INDEX_KEY,
            searchQuery,
            {
                PARAMS: {
                    searchBlob: float32Buffer(searchTxtVectorArr),
                },
                RETURN: [
                    'score',
                    'brandName',
                    'productDisplayName',
                    'imageURL',
                ],
                SORTBY: {
                    BY: 'score',
                    // DIRECTION: "DESC"
                },
                DIALECT: 2,
            },
        );
    } else {
        throw 'Search text cannot be empty';
    }

    return results;
};
```

Please find output for a KNN query in Redis **(A lower score or distance in the output signifies a higher degree of similarity.)**

```javascript
const result = await queryProductDescriptionEmbeddingsByKNN(
    'Puma watch with cat', //search text
    3, //max number of results expected
);
console.log(JSON.stringify(result, null, 4));

/*
{
    "total": 3,
    "documents": [
        {
            "id": "products:1",
            "value": {
                "score": "0.762174725533",
                "brandName": "Puma",
                "productDisplayName": "Puma Men Race Black Watch",
                "imageURL": "images/11002.jpg"
            }
        },
        {
            "id": "products:2",
            "value": {
                "score": "0.825711071491",
                "brandName": "Puma",
                "productDisplayName": "Puma Men Top Fluctuation Red Black Watches",
                "imageURL": "images/11001.jpg"
            }
        },
        {
            "id": "products:3",
            "value": {
                "score": "1.79949247837",
                "brandName": "Inkfruit",
                "productDisplayName": "Inkfruit Women Behind Cream Tshirts",
                "imageURL": "images/11008.jpg"
            }
        }
    ]
}
*/
```

> **NOTE**
>
> KNN queries can be combined with standard Redis search functionalities using [Hybrid queries](https://redis.io/docs/latest/develop/ai/search-and-query/query/combined/#pre-filter-for-a-knn--vector-query).

## How does vector range search work in Redis?

Range queries retrieve data that falls within a specified range of values. For vectors, a "range query" typically refers to retrieving all vectors within a certain distance of a target vector. The "range" in this context is a radius in the vector space.

### How do you run a range query with Redis?

Below, you'll find a Node.js code snippet that illustrates how to perform vector `range query` for any range (radius/ distance)provided:

```javascript
const queryProductDescriptionEmbeddingsByRange = async (_searchTxt, _range) => {
    /*  sample raw query

       FT.SEARCH idx:products
       "@productDescriptionEmbeddings:[VECTOR_RANGE $searchRange $searchBlob]=>{$YIELD_DISTANCE_AS: score}"
       RETURN 4 score brandName productDisplayName imageURL
       SORTBY score
       PARAMS 4 searchRange 0.685 searchBlob "A=\xe1\xbb\x8a\xad\x...."
       DIALECT 2
       */

    console.log(`queryProductDescriptionEmbeddingsByRange started`);
    let results = {};
    if (_searchTxt) {
        _range = _range ?? 1.0;

        const nodeRedisClient = getNodeRedisClient();

        const searchTxtVectorArr = await generateSentenceEmbeddings(_searchTxt);

        const searchQuery =
            '@productDescriptionEmbeddings:[VECTOR_RANGE $searchRange $searchBlob]=>{$YIELD_DISTANCE_AS: score}';

        results = await nodeRedisClient.ft.search(
            PRODUCTS_INDEX_KEY,
            searchQuery,
            {
                PARAMS: {
                    searchBlob: float32Buffer(searchTxtVectorArr),
                    searchRange: _range,
                },
                RETURN: [
                    'score',
                    'brandName',
                    'productDisplayName',
                    'imageURL',
                ],
                SORTBY: {
                    BY: 'score',
                    // DIRECTION: "DESC"
                },
                DIALECT: 2,
            },
        );
    } else {
        throw 'Search text cannot be empty';
    }

    return results;
};
```

Please find output for a range query in Redis

```javascript
const result2 = await queryProductDescriptionEmbeddingsByRange(
    'Puma watch with cat', //search text
    1.0, //with in range or distance
);
console.log(JSON.stringify(result2, null, 4));
/*
{
    "total": 2,
    "documents": [
        {
            "id": "products:1",
            "value": {
                "score": "0.762174725533",
                "brandName": "Puma",
                "productDisplayName": "Puma Men Race Black Watch",
                "imageURL": "images/11002.jpg"
            }
        },
        {
            "id": "products:2",
            "value": {
                "score": "0.825711071491",
                "brandName": "Puma",
                "productDisplayName": "Puma Men Top Fluctuation Red Black Watches",
                "imageURL": "images/11001.jpg"
            }
        }
    ]
}
*/
```

## Are image and text vector queries different?

> **IMAGE VS TEXT VECTOR QUERY**
>
> The syntax for vector KNN/ range queries is consistent, regardless of whether you're working with image vectors or text vectors. Just as there's a method for text vector queries named `queryProductDescriptionEmbeddingsByKNN`, there's a corresponding method for images titled `queryProductImageEmbeddingsByKNN` in the code base.

> **GITHUB CODE**
>
> Below is a command to clone the source code used in this tutorial
>
> git clone [https://github.com/redis-developer/redis-vector-nodejs-solutions.git](https://github.com/redis-developer/redis-vector-nodejs-solutions.git)

Hopefully this tutorial has helped you visualize how to use Redis for vector similarity search.

(Optional) If you want to also understand the math behind vector similarity search , then read following

## How is vector similarity calculated?

Several techniques are available to assess vector similarity, with some of the most prevalent ones being:

### Euclidean Distance (L2 norm)

**Euclidean Distance (L2 norm)** calculates the linear distance between two points within a multi-dimensional space. Lower values indicate closer proximity, and hence higher similarity.

For illustration purposes, let's assess `product 1` and `product 2` from the earlier ecommerce dataset and determine the `Euclidean Distance` considering all features.

As an example, we will use a 2D chart made with [chart.js](https://www.chartjs.org/) comparing the `Price vs. Quality` features of our products, focusing solely on these two attributes to compute the `Euclidean Distance`.

![2D chart plotting Price vs Quality to visualize Euclidean Distance (L2 norm) between product vectors](/images/site-mirror/9994a258997ea8a3a2a19bd78d2943633bf141fd-1250x624.webp)

### Cosine Similarity

**Cosine Similarity** measures the cosine of the angle between two vectors. The cosine similarity value ranges between -1 and 1. A value closer to 1 implies a smaller angle and higher similarity, while a value closer to -1 implies a larger angle and lower similarity. Cosine similarity is particularly popular in NLP when dealing with text vectors.

> **NOTE**
>
> If two vectors are pointing in the same direction, the cosine of the angle between them is 1. If they're orthogonal, the cosine is 0, and if they're pointing in opposite directions, the cosine is -1.

Again, consider `product 1` and `product 2` from the previous dataset and calculate the `Cosine Distance` for all features.

![Table of product feature values used for computing Cosine Similarity between two vectors](/images/site-mirror/1db18d9b032d4440b486bb2a524b04c3878a5086-1250x331.webp)

Using chart.js, we've crafted a 2D chart of `Price vs. Quality` features. It visualizes the `Cosine Similarity` solely based on these attributes.

![2D chart showing the angular difference between two product vectors for Cosine Similarity calculation](/images/site-mirror/f351e7ca377db106977821716a340279254ac6b9-1268x624.webp)

### Inner Product

**Inner Product (dot product)** The inner product (or dot product) isn't a distance metric in the traditional sense but can be used to calculate similarity, especially when vectors are normalized (have a magnitude of 1). It's the sum of the products of the corresponding entries of the two sequences of numbers.

> **NOTE**
>
> The inner product can be thought of as a measure of how much two vectors "align" in a given vector space. Higher values indicate higher similarity. However, the raw values can be large for long vectors; hence, normalization is recommended for better interpretation. If the vectors are normalized, their dot product will be `1 if they are identical` and `0 if they are orthogonal` (uncorrelated).

Considering our `product 1` and `product 2`, let's compute the `Inner Product` across all features.

![Table showing the dot product (Inner Product) calculation across all features for two product vectors](/images/site-mirror/ace383d483ffd5dfd06f66b8da831b5afe277b31-1210x105.webp)

> **TIP**
>
> Vectors can also be stored in databases in **binary formats** to save space. In practical applications, it's crucial to strike a balance between the dimensionality of the vectors (which impacts storage and computational costs) and the quality or granularity of the information they capture.

## Next steps

Now that you know how to perform vector similarity search with Redis and Node.js, explore these related tutorials and resources:

- [Semantic text search with Redis and LangChain](/tutorials/howtos/solutions/vector/semantic-text-search/) — combine vector embeddings with LangChain and OpenAI for full semantic search
- [Build a RAG GenAI chatbot with Redis](/tutorials/howtos/solutions/vector/gen-ai-chatbot/) — use vector search to power a retrieval-augmented generation chatbot
- [Vector query documentation](https://redis.io/docs/latest/develop/ai/search-and-query/vectors/) — full reference for Redis vector query syntax
- [Redis as a vector database](https://redis.io/solutions/vector-database/) — learn about production use cases
- [Redis VSS getting started](https://github.com/redis-applied-ai/redis-vss-getting-started) — additional sample code and notebooks
