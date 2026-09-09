---
title: "Vector Semantic Image Based Queries Using LangChain (OpenAI) and Redis"
linkTitle: "Vector Semantic Image Based Queries Using LangChain (OpenAI) and Redis"
url: "/tutorials/howtos/solutions/vector/image-summary-search/"
description: "LangChain is an innovative library for building language model apps. It offers a structured way to combine different components like language models (e.g., OpenAI's models), storage solutions (like..."
aliases:
- "/tutorials/howtos-solutions-vector-image-summary-search/"
date: 2026-02-25
lastmod: 2026-02-25
hidden: true
---

*Published 25 February 2026*

> **TL;DR:**
>
> Use OpenAI to generate text descriptions of product images, store those descriptions as vector embeddings in Redis, and then search images by meaning using natural language queries. Redis handles the vector similarity search, returning products whose images best match the search text.

## What you'll learn

- How to generate AI-powered text summaries from product images using OpenAI's vision model
- How to create vector embeddings from image summaries and store them in Redis
- How to build a semantic search API that finds products by image content
- How to integrate LangChain, OpenAI, and Redis into an e-commerce application

## Terminology

[**LangChain**](https://js.langchain.com/) is an innovative library for building language model apps. It offers a structured way to combine different components like language models (e.g., OpenAI's models), storage solutions (like Redis), and custom logic. This modular approach facilitates the creation of sophisticated AI apps.

[**OpenAI**](https://openai.com/) provides advanced language models like GPT-3, which have revolutionized the field with their ability to understand and generate human-like text. These models form the backbone of many modern AI apps including vector text/ image search and chatbots.

## What does the e-commerce application architecture look like?

> **GITHUB CODE**
>
> Below is a command to the clone the source code for the application used in this tutorial
>
> git clone --branch v9.2.0 [https://github.com/redis-developer/redis-microservices-ecommerce-solutions](https://github.com/redis-developer/redis-microservices-ecommerce-solutions)

Lets take a look at the architecture of the demo application:

1.  `products service`: handles querying products from the database and returning them to the frontend
2.  `orders service`: handles validating and creating orders
3.  `order history service`: handles querying a customer's order history
4.  `payments service`: handles processing orders for payment
5.  `api gateway`: unifies the services under a single endpoint
6.  `mongodb/ postgresql`: serves as the write-optimized database for storing orders, order history, products, etc.

> **NOTE**
>
> You don't need to use MongoDB/ Postgresql as your write-optimized database in the demo application; you can use other [prisma supported databases](https://www.prisma.io/docs/reference/database-reference/supported-databases) as well. This is just an example.

## How is the e-commerce frontend built?

The e-commerce microservices app consists of a frontend, built using [Next.js](https://nextjs.org/) with [TailwindCSS](https://tailwindcss.com/). The app backend uses [Node.js](https://nodejs.org/). The data is stored in [Redis](https://redis.io/try-free/) and either MongoDB or PostgreSQL, using [Prisma](https://www.prisma.io/docs/reference/database-reference/supported-databases). Below are screenshots showcasing the frontend of the e-commerce app.

- **Dashboard:** Displays a list of products with different search functionalities, configurable in the settings page.

![E-commerce app dashboard showing a grid of product cards with search bar and navigation](/images/site-mirror/54bcaae53cb07e6f133be9943f428c60aa8e675a-2000x912.webp)

- **Settings:** Accessible by clicking the gear icon at the top right of the dashboard. Control the search bar, chatbot visibility, and other features here.

![Settings page with toggles for search type, chatbot visibility, and feature configuration](/images/site-mirror/6e84fb287f08e3c0b3e6db7ab772d40aa8702f3d-1822x956.webp)

- **Dashboard (Semantic Text Search):** Configured for semantic text search, the search bar enables natural language queries. Example: "pure cotton blue shirts."

![Dashboard with semantic text search enabled, showing results for natural language query pure cotton blue shirts](/images/site-mirror/e1fd780b43c0263d7c2c5fbdb4ef320c352beb73-1920x900.webp)

- **Dashboard (Semantic Image-Based Queries):** Configured for semantic image summary search, the search bar allows for image-based queries. Example: "Left chest nike logo."

![Dashboard with semantic image search enabled, showing product results for the query Left chest nike logo](/images/site-mirror/5c693202572f6afa32e14a43a521e28a217d172d-2000x933.webp)

- **Chat Bot:** Located at the bottom right corner of the page, assisting in product searches and detailed views.

![Chatbot widget open in the bottom right corner, showing a product search conversation](/images/site-mirror/2dee7a4bac41cf8176863e0cd577f96245b40f37-1920x911.webp)

Selecting a product in the chat displays its details on the dashboard.

![Product detail view on the dashboard after selecting a product from the chatbot results](/images/site-mirror/60779b88a709ba21d36afd0dbf3ec342e0990edf-2000x954.webp)

- **Shopping Cart:** Add products to the cart and check out using the "Buy Now" button.

![Shopping cart page listing selected items with quantities, prices, and a Buy Now checkout button](/images/site-mirror/21f76ca6a23b4c6d40e992a95305bc0f2fb83c0e-2000x948.webp)

- **Order History:** Post-purchase, the 'Orders' link in the top navigation bar shows the order status and history.

![Order history page displaying a table of past orders with status indicators and timestamps](/images/site-mirror/19d3f14bb7ac470c1081b0cf9fb0d29c1808494e-2000x517.webp)

- **Admin Panel:** Accessible via the 'admin' link in the top navigation. Displays purchase statistics and trending products.

![Admin panel dashboard showing purchase statistics charts and summary metrics](/images/site-mirror/ed9f7669fc0fd22a168b23d8da20e3da812099dd-2000x945.webp)

![Admin panel section showing trending products ranked by popularity](/images/site-mirror/41190173b54aa983dc6ad3bf7293fde8cdd0944c-2000x658.webp)

## How do you set up the database for image search?

> **NOTE**
>
> Sign up for an [OpenAI account](https://platform.openai.com/) to get your API key to be used in the demo (add OPEN_AI_API_KEY variable in .env file). You can also refer to the [OpenAI API docs](https://platform.openai.com/docs/api-reference/introduction) for more information.

> **GITHUB CODE**
>
> Below is a command to the clone the source code for the application used in this tutorial
>
> git clone --branch v9.2.0 [https://github.com/redis-developer/redis-microservices-ecommerce-solutions](https://github.com/redis-developer/redis-microservices-ecommerce-solutions)

### What does the sample data look like?

In this tutorial, we'll use a simplified e-commerce dataset. Specifically, our JSON structure includes `product` details and a key named `styleImages_default_imageURL`, which links to an image of the product. This image will be the focus of our AI-driven semantic search.

```js
// database/fashion-dataset/001/products/*.json
const products = [
    {
        productId: '11000',
        price: 3995,
        productDisplayName: 'Puma Men Slick 3HD Yellow Black Watches',
        variantName: 'Slick 3HD Yellow',
        brandName: 'Puma',
        // Additional product details...
        styleImages_default_imageURL:
            'http://host.docker.internal:8080/images/11000.jpg',
        // Other properties...
    },
    // Additional products...
];
```

### How do you generate image summaries with OpenAI?

The following code segment outlines the process of generating a text summary for a product image using OpenAI's capabilities. We'll first convert the image URL to a base64 string using `fetchImageAndConvertToBase64` function and then utilize OpenAI to generate a summary of the image using `getOpenAIImageSummary` function.

```js
// database/src/open-ai-image.ts
import {
  ChatOpenAI,
  ChatOpenAICallOptions,
} from "langchain/chat_models/openai";
import { HumanMessage } from "langchain/schema";
import { Document } from "langchain/document";
import { OpenAIEmbeddings } from "langchain/embeddings/openai";
import { RedisVectorStore } from "langchain/vectorstores/redis";

let llm: ChatOpenAI<ChatOpenAICallOptions>;

// Instantiates the LangChain ChatOpenAI instance
const getOpenAIVisionInstance = (_openAIApiKey: string) => {
  //OpenAI supports  images with text in input messages with their gpt-4-vision-preview.
  if (!llm) {
    llm = new ChatOpenAI({
      openAIApiKey: _openAIApiKey,
      modelName: "gpt-4-vision-preview",
      maxTokens: 1024,
    });
  }
  return llm;
};

const fetchImageAndConvertToBase64 = async (_imageURL: string) => {
  let base64Image = "";
  try {
    const response = await axios.get(_imageURL, {
      responseType: "arraybuffer",
    });
    // Convert image to Base64
    base64Image = Buffer.from(response.data, "binary").toString("base64");
  } catch (error) {
    console.error(
      `Error fetching or converting the image: ${_imageURL}`,
      error
    );
  }
  return base64Image;
};

// Generates an OpenAI summary for a given base64 image string
const getOpenAIImageSummary = async (
  _openAIApiKey: string,
  _base64Image: string,
  _product: Prisma.ProductCreateInput
) => {
  /*
     Reference : https://js.langchain.com/docs/integrations/chat/openai#multimodal-messages

    - This function utilizes OpenAI's multimodal capabilities to generate a summary from the image.
    - It constructs a prompt that combines the product description with the image.
    - OpenAI's vision model then processes this prompt to generate a detailed summary.

   */
  let imageSummary = "";

  try {
    if (_openAIApiKey && _base64Image && _product) {
      const llmInst = getOpenAIVisionInstance(_openAIApiKey);

      const text = `Below are the product details and image of an e-commerce product for reference. Please conduct and provide a comprehensive analysis of the product depicted in the image .

            Product Details:
            ${_product.productDescriptors_description_value}

            Image:
        `;
      // Constructing a multimodal message combining text and image
      const imagePromptMessage = new HumanMessage({
        content: [
          {
            type: "text",
            text: text,
          },
          {
            type: "image_url",
            image_url: {
              url: `data:image/jpeg;base64,${_base64Image}`,
              detail: "high", // low, high (if you want more detail)
            },
          },
        ],
      });

      // Invoking the LangChain ChatOpenAI model with the constructed message
      const response = await llmInst.invoke([imagePromptMessage]);
      if (response?.content) {
        imageSummary = <string>response.content;
      }
    }
  } catch (err) {
    console.log(
      `Error generating OpenAIImageSummary for product id ${_product.productId}`,
      err
    );
  }
  return imageSummary;
};
```

### What does a generated image summary look like?

The following section demonstrates the result of the above process. We'll use the image of a Puma T-shirt and generate a summary using OpenAI's capabilities.

![Black Puma T-shirt with yellow cat logo on a model, used as input for OpenAI image summary generation](/images/site-mirror/8b5955f282dd78976fc6c343e27c361442b5af11-1125x1500.webp)

Comprehensive summary generated by the OpenAI model is as follows:

```text
This product is a black round neck T-shirt featuring a design consistent with the Puma brand aesthetic, which includes their iconic leaping cat logo in a contrasting yellow color placed prominently across the chest area. The T-shirt is made from 100% cotton, suggesting it is likely to be breathable and soft to the touch. It has a classic short-sleeve design with a ribbed neckline for added texture and durability. There is also mention of a vented hem, which may offer additional comfort and mobility.

The T-shirt is described to have a 'comfort' fit, which typically means it is designed to be neither too tight nor too loose, allowing for ease of movement without being baggy. This could be ideal for casual wear or active use.

Care instructions are also comprehensive, advising a gentle machine wash with similar colors in cool water at 30 degrees Celsius, indicating it is relatively easy to care for. However, one should avoid bleaching, tumble drying, and dry cleaning it, but a warm iron is permissible.

Looking at the image provided:

- The T-shirt appears to fit the model well, in accordance with the described 'comfort' fit.
- The color contrast between the T-shirt and the graphic gives the garment a modern, sporty look.
- The model is paired with denim jeans, showcasing the T-shirt's versatility for casual occasions. However, the product description suggests it can be part of an athletic ensemble when combined with Puma shorts and shoes.
- Considering the model's statistics, prospective buyers could infer how this T-shirt might fit on a person with similar measurements.

Overall, the T-shirt is positioned as a versatile item suitable for both lifestyle and sporting activities, with a strong brand identity through the graphic, and is likely comfortable and easy to maintain based on the product details provided.
```

### How do you store image summary embeddings in Redis?

The `addImageSummaryEmbeddingsToRedis` function plays a critical role in integrating AI-generated image summaries with Redis. This process involves two main steps:

1.  **Generating Vector Documents**: Utilizing the `getImageSummaryVectorDocuments` function, we transform image summaries into vector documents. This transformation is crucial as it converts textual summaries into a format suitable for Redis storage.
2.  **Seeding Embeddings into Redis**: The `seedImageSummaryEmbeddings` function is then employed to store these vector documents into Redis. This step is essential for enabling efficient retrieval and search capabilities within the Redis database.

```js
// Function to generate vector documents from image summaries
const getImageSummaryVectorDocuments = async (
  _products: Prisma.ProductCreateInput[],
  _openAIApiKey: string
) => {
  const vectorDocs: Document[] = [];

  if (_products?.length > 0) {
    let count = 1;
    for (let product of _products) {
      if (product) {
        let imageURL = product.styleImages_default_imageURL; //cdn url
        const imageData = await fetchImageAndConvertToBase64(imageURL);
        imageSummary = await getOpenAIImageSummary(
          _openAIApiKey,
          imageData,
          product
        );
        console.log(
          `openAI imageSummary #${count++} generated for product id: ${
            product.productId
          }`
        );

        if (imageSummary) {
          let doc = new Document({
            metadata: {
              productId: product.productId,
              imageURL: imageURL,
            },
            pageContent: imageSummary,
          });
          vectorDocs.push(doc);
        }
      }
    }
  }
  return vectorDocs;
};

// Seeding vector documents into Redis
const seedImageSummaryEmbeddings = async (
  vectorDocs: Document[],
  _redisClient: NodeRedisClientType,
  _openAIApiKey: string
) => {
  if (vectorDocs?.length && _redisClient && _openAIApiKey) {
    const embeddings = new OpenAIEmbeddings({
      openAIApiKey: _openAIApiKey,
    });
    const vectorStore = await RedisVectorStore.fromDocuments(
      vectorDocs,
      embeddings,
      {
        redisClient: _redisClient,
        indexName: "openAIProductImgIdx",
        keyPrefix: "openAIProductImgText:",
      }
    );
    console.log("seeding imageSummaryEmbeddings completed");
  }
};

const addImageSummaryEmbeddingsToRedis = async (
  _products: Prisma.ProductCreateInput[],
  _redisClient: NodeRedisClientType,
  _openAIApiKey: string
) => {
  const vectorDocs = await getImageSummaryVectorDocuments(
    _products,
    _openAIApiKey
  );

  await seedImageSummaryEmbeddings(vectorDocs, _redisClient, _openAIApiKey);
};
```

The image below shows the JSON structure of **openAI image summary** within Redis Insight.

![Redis Insight GUI displaying the stored OpenAI image summary as a JSON document with vector embedding fields](/images/site-mirror/65dcd57c3b5baa03ace340df1a80e0434622091f-2000x1228.webp)

> **TIP**
>
> Download [Redis Insight](https://redis.io/insight/) to visually explore your Redis data or to engage with raw Redis commands in the workbench.

## How do you build the image search API?

### What does the search API endpoint look like?

This section covers the API request and response structure for `getProductsByVSSImageSummary`, which is essential for retrieving products based on semantic search using image summaries.

#### Search API request format

The example request format for the API is as follows:

```js
POST http://localhost:3000/products/getProductsByVSSImageSummary
{
   "searchText":"Left chest nike logo",

   //optional
   "maxProductCount": 4, // 2 (default)
   "similarityScoreLimit":0.2, // 0.2 (default)
}
```

#### Search API response structure

The response from the API is a JSON object containing an array of product details that match the semantic search criteria:

```json
{
    "data": [
        {
            "productId": "10017",
            "price": 3995,
            "productDisplayName": "Nike Women As The Windru Blue Jackets",
            "brandName": "Nike",
            "styleImages_default_imageURL": "http://host.docker.internal:8080/products/01/10017/product-img.webp",
            "productDescriptors_description_value": " Blue and White jacket made of 100% polyester, with an interior pocket ...",
            "stockQty": 25,
            "similarityScore": 0.163541972637,
            "imageSummary": "The product in the image is a blue and white jacket featuring a design consistent with the provided description. ..."
        }
    ],
    "error": null,
    "auth": "SES_fd57d7f4-3deb-418f-9a95-6749cd06e348"
}
```

### How does the vector similarity search work?

The backend implementation of this API involves following steps:

1.  `getProductsByVSSImageSummary` function handles the API Request.
2.  `getSimilarProductsScoreByVSSImageSummary` function performs semantic search on image summaries. It integrates with OpenAI's semantic analysis capabilities to interpret the searchText and identify relevant products from Redis vector store.

```js
// server/src/services/products/src/open-ai-prompt.ts
const getSimilarProductsScoreByVSSImageSummary = async (
  _params: IParamsGetProductsByVSS
) => {
  let {
    standAloneQuestion,
    openAIApiKey,

    //optional
    KNN,
    scoreLimit,
  } = _params;

  let vectorDocs: Document[] = [];
  const client = getNodeRedisClient();

  KNN = KNN || 2;
  scoreLimit = scoreLimit || 1;

  const embeddings = new OpenAIEmbeddings({
    openAIApiKey: openAIApiKey,
  });

  // create vector store
  const vectorStore = new RedisVectorStore(embeddings, {
    redisClient: client,
    indexName: "openAIProductImgIdx",
    keyPrefix: "openAIProductImgText:",
  });

  // search for similar products
  const vectorDocsWithScore = await vectorStore.similaritySearchWithScore(
    standAloneQuestion,
    KNN
  );

  // filter by scoreLimit
  for (let [doc, score] of vectorDocsWithScore) {
    if (score <= scoreLimit) {
      doc["similarityScore"] = score;
      vectorDocs.push(doc);
    }
  }

  return vectorDocs;
};
```

```js
// server/src/services/products/src/service-impl.ts
const getProductsByVSSImageSummary = async (
  productsVSSFilter
) => {
  let { searchText, maxProductCount, similarityScoreLimit } = productsVSSFilter;
  let products: IProduct[] = [];

  const openAIApiKey = process.env.OPEN_AI_API_KEY || "";
  maxProductCount = maxProductCount || 2;
  similarityScoreLimit = similarityScoreLimit || 0.2;

  //VSS search
  const vectorDocs = await getSimilarProductsScoreByVSSImageSummary({
    standAloneQuestion: searchText,
    openAIApiKey: openAIApiKey,
    KNN: maxProductCount,
    scoreLimit: similarityScoreLimit,
  });

  if (vectorDocs?.length) {
    const productIds = vectorDocs.map((doc) => doc?.metadata?.productId);

    //get product with details
    products = await getProductByIds(productIds, true);
  }

  //...

  return products;
};
```

### How do you use the image search in the frontend?

- **Settings configuration**: Initially, ensure that the `Semantic image summary search` option is enabled in the settings page.

![Settings page with the Semantic image summary search toggle highlighted and enabled](/images/site-mirror/30d093b44c0618cd2f0a78c5b80c4d1da550b21f-1758x956.webp)

- **Performing a search**: On the dashboard page, users can conduct searches using image-based queries. For example, if the query is `Left chest nike logo`, the search results will display products like a Nike jacket, characterized by a logo on its left chest, reflecting the query.

![Dashboard showing image-based search results for the query Left chest nike logo with matching Nike products](/images/site-mirror/5c693202572f6afa32e14a43a521e28a217d172d-2000x933.webp)

- **Viewing image summaries**: Users can click on any product image to view the corresponding image summary generated by OpenAI. This feature offers an insightful glimpse into how AI interprets and summarizes visual content.

![Product detail modal showing the AI-generated image summary text alongside the product image](/images/site-mirror/7801745c6e3e1c2aaf2cf0e3a4add781cf8284e7-1274x998.webp)

## Next steps

Now that you've built semantic image search with Redis, explore these related tutorials:

- [How to perform vector similarity search using Redis in NodeJS](/tutorials/howtos/solutions/vector/getting-started-vector) -- learn the fundamentals of vector search with Redis
- [Semantic text search using LangChain (OpenAI) and Redis](/tutorials/howtos/solutions/vector/semantic-text-search/) -- apply similar techniques to text-based semantic search
- [LangChain JS](https://js.langchain.com/docs/get_started/quickstart)
- [Learn LangChain](https://scrimba.com/learn/langchain)
- [LangChain Redis integration](https://js.langchain.com/docs/integrations/vectorstores/redis)
