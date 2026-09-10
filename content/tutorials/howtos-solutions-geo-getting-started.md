---
title: "Redis Geo Commands Tutorial: Location-Based Queries and Search"
linkTitle: "Redis Geo Commands Tutorial: Location-Based Queries and Search"
url: "/tutorials/howtos/solutions/geo/getting-started/"
description: "Redis GEO commands let you store latitude/longitude coordinates and run proximity queries entirely in memory. Use GEOADD to index locations, GEOSEARCH to find items within a radius, and GEODIST to..."
group: "For developers"
aliases:
- "/tutorials/howtos-solutions-geo-getting-started/"
date: 2026-02-25
lastmod: 2026-02-25
hidden: true
---

*Published 25 February 2026*

Redis GEO commands let you store latitude/longitude coordinates and run proximity queries entirely in memory. Use `GEOADD` to index locations, `GEOSEARCH` to find items within a radius, and `GEODIST` to calculate distances — all with sub-millisecond latency. This tutorial walks through a complete e-commerce example: indexing store locations, querying nearby inventory, and exposing the results through a REST API.

## What you will learn in this tutorial

- How to store and index geospatial data in Redis using GEO commands
- How to perform radius-based proximity searches with `FT.SEARCH` and `FT.AGGREGATE`
- How to set up Redis OM for geospatial indexing in a Node.js project
- How to build a REST API endpoint for location-based product search
- How to sort and filter results by distance from a user's location

## What does the demo application look like?

> **GITHUB CODE**
>
> Below is a command to the clone the source code for the application used in this tutorial
>
> git clone --branch v10.1.0 https://github.com/redis-developer/redis-microservices-ecommerce-solutions

The demo application uses a microservices architecture:

`1. products service`: handles querying products from the database and returning them to the frontend

`2. orders service`: handles validating and creating orders

`3. order history service`: handles querying a customer's order history

`4. payments service`: handles processing orders for payment

`5. api gateway`: unifies the services under a single endpoint

`6. mongodb/ postgresql`: serves as the write-optimized database for storing orders, order history, products, etc.

> **TIP**
>
> You don't need to use MongoDB/ Postgresql as your write-optimized database in the demo application; you can use other [prisma supported databases](https://www.prisma.io/docs/reference/database-reference/supported-databases) as well. This is just an example.

The e-commerce microservices application consists of a frontend, built using [Next.js](https://nextjs.org/) with [TailwindCSS](https://tailwindcss.com/). The application backend uses [Node.js](https://nodejs.org/). The data is stored in [Redis](https://redis.io/try-free/) and either MongoDB or PostgreSQL, using [Prisma](https://www.prisma.io/docs/reference/database-reference/supported-databases). Below are screenshots showcasing the frontend of the e-commerce app.

Dashboard: Displays a list of products with different search functionalities, configurable in the settings page.

![E-commerce app dashboard showing a product grid with search bar, filters, and product cards displaying images, names, and prices](/images/site-mirror/b1e5ce258357daea2a38afd2f58a7e8a227b3070-1038x494.webp)

Settings: Accessible by clicking the gear icon at the top right of the dashboard. Control the search bar, chatbot visibility, and other features here.

![Settings page with toggle switches for enabling geo location search, vector search, and chatbot features](/images/site-mirror/40c0cdcab149bdf9fbc6829bb5f0f5da0638d1dc-1038x701.webp)

Dashboard (Geo Location Search): Configured for `Geo location search`, the search bar enables location queries.
_Note:_ In our demo, each zipCode location is mapped with lat long coordinates.

![Dashboard with geo location search enabled, showing a zip code input field and product results filtered by proximity](/images/site-mirror/ffc7137fbd3f1e95debf3f8db3c5af0be18aed84-1038x490.webp)

Shopping Cart: Add products to the cart and check out using the "Buy Now" button.

![Shopping cart sidebar showing selected products with quantities, individual prices, and a total order summary](/images/site-mirror/238c99139b76686098fe34e54f715a1093b248cb-1038x490.webp)

Order History: Post-purchase, the 'Orders' link in the top navigation bar shows the order status and history.

![Order history page listing past orders with order IDs, dates, statuses, and item summaries](/images/site-mirror/5fe6b87130a8f55286ba036fc005f9ba6067057c-1038x364.webp)

Admin Panel: Accessible via the 'admin' link in the top navigation. Displays purchase statistics and trending products.

![Admin panel with bar charts showing purchase statistics over time and a table of trending products](/images/site-mirror/cb43b75e3d2831cc3de2269b599475ebfafb7235-1038x490.webp)

## What are Redis GEO commands?

Redis GEO commands are a set of built-in commands for storing and querying geospatial data. They use a sorted set under the hood, encoding latitude and longitude pairs into [geohash](https://en.wikipedia.org/wiki/Geohash) values for efficient indexing. The core commands include:

- **`GEOADD`** — add members with longitude/latitude coordinates to a sorted set
- **`GEOSEARCH`** — find members within a given radius or bounding box
- **`GEODIST`** — calculate the distance between two members
- **`GEOPOS`** — retrieve the coordinates of one or more members
- **`GEOHASH`** — return the geohash string for one or more members

When combined with the [RediSearch](/docs/latest/develop/interact/search-and-query/) module, you can also use `FT.SEARCH` and `FT.AGGREGATE` to run geospatial queries alongside full-text search, numeric filtering, and aggregation — all in a single command.

## Why use Redis for geo location search?

Geo location search involves querying data based on geographical coordinates (latitude and longitude). Common use cases include finding nearby stores, tracking delivery drivers, building ride-sharing features, and powering "buy-online-pickup-in-store" (BOPIS) experiences.

Redis is well suited for geo location search because:

- **In-memory speed** — geospatial queries execute with sub-millisecond latency and high throughput
- **Combined queries** — RediSearch lets you filter by location, text, numeric ranges, and tags in a single query
- **Real-time updates** — inventory and location data can be updated and queried instantly
- **Simple API** — a few commands handle the entire lifecycle from indexing to querying

Consider a multi-store shopping scenario where consumers locate a product online and pick up at the nearest store. Redis enables a real-time view of store inventory and a seamless BOPIS shopping experience. For a deeper look at inventory-specific patterns, see the [Real-time Local Inventory Search](/tutorials/howtos/solutions/real-time-inventory/local-inventory-search/) tutorial.

## How do you set up the database for geo queries?

### What data collections are needed?

The demo application utilizes two primary data collections within Redis to simulate an e-commerce platform's inventory system:

`1. products` collection: This collection stores detailed information about each product, including name, description, category and price.

![Redis Insight browser view showing the products JSON collection with fields for productId, displayName, price, and category](/images/site-mirror/c258a3a79ec5022df07b1497bf6271b587fb496d-1038x641.webp)

> **TIP**
>
> Utilize [Redis Insight](https://redis.io/insight/) to interactively explore your Redis database and execute raw Redis commands in a user-friendly workbench environment.

`2. storeInventory` collection: This collection maintains the inventory status of products across different store locations. It records the quantity of each product available at various stores, facilitating inventory tracking and management.

![Redis Insight browser view showing the storeInventory JSON collection with fields for storeId, storeLocation, productId, and stockQty](/images/site-mirror/267e75fa9465963dbb598175cd54136c743e5317-1038x644.webp)

For the purpose of this demo, we simulate an e-commerce operation in various regions across New York (US), with each store location identified by a `storeId` and associated `stockQty` for products.

![Map of the New York region with pins marking each simulated store location used in the demo application](/images/site-mirror/f3a989d1cfd4a88c3bbe5294aebd297c1cfdbfa2-1038x814.webp)

### How do you index geospatial data in Redis?

To enable geo location searches within the storeInventory collection, you need to index the data appropriately. Redis offers multiple methods for creating indexes: using the Command Line Interface (CLI) or using client libraries like Redis OM, node redis, etc.

#### Using CLI command

To facilitate geo-spatial queries and other search operations on the `storeInventory` collection, follow these commands:

```bash
# Remove existing index
FT.DROPINDEX "storeInventory:storeInventoryId:index"

# Create a new index with geo-spatial and other field capabilities
FT.CREATE "storeInventory:storeInventoryId:index"
  ON JSON
  PREFIX 1 "storeInventory:storeInventoryId:"
  SCHEMA
    "$.storeId" AS "storeId" TAG SEPARATOR "|"
    "$.storeName" AS "storeName" TEXT
    "$.storeLocation" AS "storeLocation" GEO
    "$.productId" AS "productId" TAG SEPARATOR "|"
    "$.productDisplayName" AS "productDisplayName" TEXT
    "$.stockQty" AS "stockQty" NUMERIC
    "$.statusCode" AS "statusCode" NUMERIC
```

#### Using Redis OM

For applications leveraging the Node.js environment, Redis OM provides an elegant, object-mapping approach to interact with Redis. Below is an implementation example to set up the index using Redis OM:

```js
// File: server/src/common/models/store-inventory-repo.ts

import {
    Schema as RedisSchema,
    Repository as RedisRepository,
    EntityId as RedisEntityId,
} from 'redis-om';

import { getNodeRedisClient } from '../utils/redis/redis-wrapper';

const STORE_INVENTORY_KEY_PREFIX = 'storeInventory:storeInventoryId';
const schema = new RedisSchema(STORE_INVENTORY_KEY_PREFIX, {
    storeId: { type: 'string', indexed: true },
    storeName: { type: 'text', indexed: true },
    storeLocation: { type: 'point', indexed: true }, // Uses longitude,latitude format

    productId: { type: 'string', indexed: true },
    productDisplayName: { type: 'text', indexed: true },
    stockQty: { type: 'number', indexed: true },
    statusCode: { type: 'number', indexed: true },
});

/*
 A Repository is the main interface into Redis OM. It gives us the methods to read, write, and remove a specific Entity
 */
const getRepository = () => {
    const redisClient = getNodeRedisClient();
    const repository = new RedisRepository(schema, redisClient);
    return repository;
};

/*
we need to create an index or we won't be able to search.
Redis OM uses hash to see if index needs to be recreated or not
*/
const createRedisIndex = async () => {
    const repository = getRepository();
    await repository.createIndex();
};

export {
    getRepository,
    createRedisIndex,
    RedisEntityId,
    STORE_INVENTORY_KEY_PREFIX,
};
```

```js
// File: server/src/services/products/src/index.ts

import * as StoreInventoryRepo from '../../../common/models/store-inventory-repo';

app.listen(PORT, async () => {
    //...

    await StoreInventoryRepo.createRedisIndex();
    //...
});
```

## How do you build geo location search queries in Redis?

### How do you search for products within a radius?

Once the data is indexed, you can execute raw Redis queries to perform geo location searches. Here are two sample queries to demonstrate the capabilities:

**1. Searching products within a radius:** This query finds products within a `50-mile` radius of a specific location (`New York City`) with a particular product name (`puma`). It combines geo-spatial search with text search to filter results based on both location and product name.

```bash
FT.SEARCH "storeInventory:storeInventoryId:index" "( ( ( (@statusCode:[1 1]) (@stockQty:[(0 +inf]) ) (@storeLocation:[-73.968285 40.785091 50 mi]) ) (@productDisplayName:'puma') )"
```

This query leverages the `FT.SEARCH` command to perform a search within the `storeInventory:storeInventoryId:index`. It specifies a circular area defined by the center's longitude and latitude and a radius of `50 miles`. Additionally, it filters products by availability `(@stockQty:[(0 +inf]))` and `@statusCode` indicating an active status `([1 1])`, combined with a match on the product display name containing `puma`.

![Redis Insight workbench showing FT.SEARCH query results with matching store inventory entries within 50 miles of New York City](/images/site-mirror/795bb128212452da5d53c84a8e79e8a9dd7c8c44-1038x643.webp)

**2. Aggregate query for sorted results:** This aggregate query extends the first example by sorting the results based on geographical distance from the search location and limiting the results to the first 100.

```bash
FT.AGGREGATE "storeInventory:storeInventoryId:index"
          "( ( ( (@statusCode:[1 1]) (@stockQty:[(0 +inf]) ) (@storeLocation:[-73.968285 40.785091 50 mi]) ) (@productDisplayName:'puma') )"
          LOAD 6 "@storeId" "@storeName" "@storeLocation" "@productId" "@productDisplayName" "@stockQty"
          APPLY "geodistance(@storeLocation, -73.968285, 40.785091)/1609"
          AS "distInMiles"
          SORTBY 1 "@distInMiles"
          LIMIT 0 100
```

In this query, `FT.AGGREGATE` is used to process and transform search results. The `APPLY` clause calculates the distance between each store location and the specified coordinates, converting the result into miles. The `SORTBY` clause orders the results by this distance, and `LIMIT` caps the output to 100 entries, making the query highly relevant for applications requiring sorted proximity-based search results.

![Redis Insight workbench showing FT.AGGREGATE results with a distInMiles column calculated for each store entry](/images/site-mirror/1dde8551f91d7e9bdabbd8ed86547ce834186c38-1038x640.webp)

### How do you expose geo search through an API?

The `getStoreProductsByGeoFilter` API endpoint enables clients to search for store products based on geographical location and product name, demonstrating a practical application of Redis geo location search capabilities.

API Request

The request payload specifies the product name to search for, the search radius in miles, and the user's current location in latitude and longitude coordinates.

```bash
POST http://localhost:3000/products/getStoreProductsByGeoFilter
{
    "productDisplayName":"puma",

    "searchRadiusInMiles":50,
    "userLocation": {
        "latitude": 40.785091,
        "longitude": -73.968285
    }
}
```

API Response

The response returns an array of products matching the search criteria, including detailed information about each product and its distance from the user's location.

```json
{
    "data": [
        {
            "productId": "11000",
            "price": 3995,
            "productDisplayName": "Puma Men Slick 3HD Yellow Black Watches",
            "variantName": "Slick 3HD Yellow",
            "brandName": "Puma",
            "ageGroup": "Adults-Men",
            "gender": "Men",
            "displayCategories": "Accessories",
            "masterCategory_typeName": "Accessories",
            "subCategory_typeName": "Watches",
            "styleImages_default_imageURL": "http://host.docker.internal:8080/images/11000.jpg",
            "productDescriptors_description_value": "...",

            "stockQty": "5",
            "storeId": "11_NY_MELVILLE",
            "storeLocation": {
                "longitude": -73.41512,
                "latitude": 40.79343
            },
            "distInMiles": "46.59194"
        }
        //...
    ],
    "error": null
}
```

### How is the geo search API implemented?

This section outlines the implementation of the `getStoreProductsByGeoFilter` API, focusing on the `searchStoreInventoryByGeoFilter` function that executes the core search logic.

1. Function Overview: `searchStoreInventoryByGeoFilter` accepts an inventory filter object that includes optional product display name, search radius in miles, and user location. It constructs a query to find store products within the specified radius that match the product name.
2. Query Construction: The function builds a search query using Redis OM's fluent API, specifying conditions for product availability, stock quantity, and proximity to the user's location. It also optionally filters products by name if specified.
3. Executing the Query: The constructed query is executed against Redis using the ft.aggregate method, which allows for complex aggregations and transformations. The query results are processed to calculate the distance in miles from the user's location and sort the results accordingly.

4. Result Processing: The function filters out duplicate products across different stores, ensuring unique product listings in the final output. It then formats the store locations into a more readable structure and compiles the final list of products to return.

```js
import * as StoreInventoryRepo from '../../../common/models/store-inventory-repo';

interface IInventoryBodyFilter {
  productDisplayName?: string;

  searchRadiusInMiles?: number;
  userLocation?: {
    latitude?: number;
    longitude?: number;
  },
}

const searchStoreInventoryByGeoFilter = async (
  _inventoryFilter: IInventoryBodyFilter,
) => {
  // (1) ---
  const redisClient = getNodeRedisClient();
  const repository = StoreInventoryRepo.getRepository();
  let storeProducts: IStoreInventory[] = [];
  const trimmedStoreProducts: IStoreInventory[] = []
  const uniqueProductIds = {};

  if (repository
    && _inventoryFilter?.userLocation?.latitude
    && _inventoryFilter?.userLocation?.longitude) {

    const lat = _inventoryFilter.userLocation.latitude;
    const long = _inventoryFilter.userLocation.longitude;
    const radiusInMiles = _inventoryFilter.searchRadiusInMiles || 500;

    // (2) --- Query Construction
    let queryBuilder = repository
      .search()
      .and('statusCode')
      .eq(1)
      .and('stockQty')
      .gt(0)
      .and('storeLocation')
      .inRadius((circle) => {
        return circle
          .latitude(lat)
          .longitude(long)
          .radius(radiusInMiles)
          .miles
      });

    if (_inventoryFilter.productDisplayName) {
      queryBuilder = queryBuilder
        .and('productDisplayName')
        .matches(_inventoryFilter.productDisplayName)
    }

    console.log(queryBuilder.query);

    /* Sample queryBuilder.query to run on CLI
    FT.SEARCH "storeInventory:storeInventoryId:index" "( ( ( (@statusCode:[1 1]) (@stockQty:[(0 +inf]) ) (@storeLocation:[-73.968285 40.785091 50 mi]) ) (@productDisplayName:'puma') )"
            */

   // (3) --- Executing the Query
    const indexName = `storeInventory:storeInventoryId:index`;
    const aggregator = await redisClient.ft.aggregate(
      indexName,
      queryBuilder.query,
      {
        LOAD: ["@storeId", "@storeName", "@storeLocation", "@productId", "@productDisplayName", "@stockQty"],
        STEPS: [{
          type: AggregateSteps.APPLY,
          expression: `geodistance(@storeLocation, ${long}, ${lat})/1609`,
          AS: 'distInMiles'
        }, {
          type: AggregateSteps.SORTBY,
          BY: ["@distInMiles", "@productId"]
        }, {
          type: AggregateSteps.LIMIT,
          from: 0,
          size: 1000,
        }]
      });

    /* Sample command to run on CLI
        FT.AGGREGATE "storeInventory:storeInventoryId:index"
          "( ( ( (@statusCode:[1 1]) (@stockQty:[(0 +inf]) ) (@storeLocation:[-73.968285 40.785091 50 mi]) ) (@productDisplayName:'puma') )"
          "LOAD" "6" "@storeId" "@storeName" "@storeLocation" "@productId" "@productDisplayName" "@stockQty"
          "APPLY" "geodistance(@storeLocation, -73.968285, 40.785091)/1609"
          "AS" "distInMiles"
          "SORTBY" "1" "@distInMiles"
          "LIMIT" "0" "100"
    */

    storeProducts = <IStoreInventory[]>aggregator.results;

    if (!storeProducts.length) {
      // throw `Product not found with in ${radiusInMiles}mi range!`;
    }
    else {

     // (4) --- Result Processing
      storeProducts.forEach((storeProduct) => {
        if (storeProduct?.productId && !uniqueProductIds[storeProduct.productId]) {
          uniqueProductIds[storeProduct.productId] = true;

          if (typeof storeProduct.storeLocation == "string") {
            const location = storeProduct.storeLocation.split(",");
            storeProduct.storeLocation = {
              longitude: Number(location[0]),
              latitude: Number(location[1]),
            }
          }

          trimmedStoreProducts.push(storeProduct)
        }
      });
    }
  }
  else {
    throw "Mandatory fields like userLocation latitude / longitude missing !"
  }

  return {
    storeProducts: trimmedStoreProducts,
    productIds: Object.keys(uniqueProductIds)
  };
};
```

The implementation demonstrates a practical use case for Redis geo location search, showcasing how to perform proximity searches combined with other filtering criteria (like product name) and present the results in a user-friendly format.

### How do you enable geo search in the frontend?

Make sure to select `Geo location search` in settings page to enable the feature.

![Settings page with the Geo location search toggle switch highlighted and enabled](/images/site-mirror/40c0cdcab149bdf9fbc6829bb5f0f5da0638d1dc-1038x701.webp)

Within the dashboard, users have the option to select a random zip code and search for products (say titled "puma"). The search results are comprehensively displayed, including essential details such as the product name, available stock quantity, the name of the store, and the distance of the store from the user's selected location.

![Dashboard search results for "puma" showing product cards with store name, stock quantity, and distance in miles from the selected zip code](/images/site-mirror/a9c3256969f53411d1661c6ff10b598c22f5695f-1038x488.webp)

## Next steps

Now that you know how to build geo location search with Redis, here are some ways to go further:

- **[Real-time Local Inventory Search](/tutorials/howtos/solutions/real-time-inventory/local-inventory-search/)** — extend this pattern with real-time inventory availability across multiple store locations
- **[Redis GEO command reference](/docs/latest/commands/?group=geo)** — explore the full set of GEO commands including `GEOSEARCHSTORE` and bounding box queries
- **[Search and query documentation](/docs/latest/develop/interact/search-and-query/)** — learn more about combining geospatial filters with full-text search, numeric ranges, and aggregations
- **[Redis Insight](https://redis.io/insight/)** — visualize your Redis data and test geo queries interactively in the workbench
- **[Try Redis Cloud for free](https://redis.io/try-free/)** — get started with a managed Redis instance that supports all GEO commands and RediSearch

### References

- [Redis YouTube channel](https://www.youtube.com/c/Redisinc)
- Clients like [Node Redis](https://github.com/redis/node-redis) and [Redis OM Node](https://github.com/redis/redis-om-node) help you to use Redis in Node.js applications.
- [Redis Insight](https://redis.io/insight/): To view your Redis data or to play with raw Redis commands in the workbench
- [Try Redis Cloud for free](https://redis.io/try-free/)
