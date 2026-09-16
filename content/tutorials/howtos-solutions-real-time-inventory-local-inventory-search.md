---
title: "Real-time Local Inventory Search Using Redis"
linkTitle: "Real-time Local Inventory Search Using Redis"
url: "/tutorials/howtos/solutions/real-time-inventory/local-inventory-search/"
description: "Real-time local inventory search is a method of utilizing advanced product search capabilities across a group of stores or warehouses in a region or geographic area by which a retailer can enhance..."
group: "For developers"
aliases:
- "/tutorials/howtos-solutions-real-time-inventory-local-inventory-search/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
mirrored: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> Build a local inventory search with Redis by storing product quantities per store as JSON documents with geospatial coordinates, then querying them with Redis's geo-radius search. Customers search by SKU and location, and Redis returns matching stores within a given radius — optionally sorted by distance — enabling buy-online-pickup-in-store (BOPIS) experiences.

> **GITHUB CODE**
>
> Below is a command to the clone the source code for the application used in this tutorial
>
> git clone [https://github.com/redis-developer/redis-real-time-inventory-solutions](https://github.com/redis-developer/redis-real-time-inventory-solutions)

## What you'll learn

- What real-time local inventory search is and why it matters for omnichannel retail
- How to model store inventory data with geospatial coordinates in Redis
- How to query nearby store product availability using Redis geo-spatial search
- How to sort inventory results by distance from the customer's location
- How to build `inventorySearch` and `inventorySearchWithDistance` APIs with Redis

## What is real-time local inventory search?

**Real-time local inventory search** is a method of utilizing advanced product search capabilities across a group of stores or warehouses in a region or geographic area by which a retailer can enhance the customer experience with a localized view of inventory while fulfilling orders from the closest store possible.

Geospatial search of merchandise local to the consumer helps sell stock faster, lowers inventory levels, and thus increases inventory turnover ratio. Consumers locate a product online, place the order in their browser or mobile device, and pick up at nearest store location. This is called "buy-online-pickup-in-store" (BOPIS)

## What are the current challenges in real-time inventory?

- **Over and under-stocking**: While adopting a multi-channel business model (online & in store), lack of inventory visibility results in over and under-stocking of inventory in different regions and stores.
- Consumers **seek convenience**: The ability to search across regional store locations and pickup merchandise **immediately** rather than wait for shipping is a key differentiator for retailers.
- Consumers **seek speed**: All retailers, even small or family-run, must compete against the **customer experience** of large online retailers like Alibaba, FlipKart, Shopee, and Amazon.
- **High inventory costs**: Retailers seek to lower inventory costs by eliminating missed sales from out-of-stock scenarios which also leads to higher "inventory turnover ratios."
- **Brand value**: Inaccurate store inventory counts lead to frustrated customers and lower sales. The operational pain will **impact the status quo**.

## Why should you use Redis for local inventory search?

- **Accurate location/regional inventory search**: Redis geospatial search capabilities enable retailers to provide local inventories by store location across geographies and regions based on a consumer's location. This enables a real-time view of store inventory and a seamless BOPIS shopping experience.
- **Consistent and accurate inventory view across multichannel and omnichannel experiences**: Accurate inventory information no matter what channel the shopper is using, in-store, kiosk, online, or mobile. Redis provides a single source of truth for inventory information across all channels.
- **Real-time search performance at scale**: Redis's real-time search and query engine allows retailers to provide instant application and inventory search responses and scale performance effortlessly during peak periods.

If you're new to geospatial data in Redis, see the [Getting Started with Geo](/tutorials/howtos/solutions/geo/getting-started/) tutorial for foundational concepts.

## How does real-time local inventory search work with Redis?

![Architecture diagram showing how Redis geo-spatial queries connect a customer's location to nearby store inventory across multiple retail locations](/images/site-mirror/077ed4f9330fd511c5b1577d7bd8d570d430224f-1024x520.webp)

Redis provides geospatial search capabilities across a group of stores or warehouses in a region or geographic area allowing a retailer to quickly show the available inventory local to the customer.

Redis processes event streams, keeping store inventories up-to-date in real-time. This enhances the customer experience with localized, accurate search of inventory while fulfilling orders from the nearest and fewest stores possible.

This solution lowers days sales of inventory (DSI), selling inventory faster and carrying less inventory for increased revenue generation and profits over a shorter time period.

It also reduces fulfillment costs to home and local stores enhancing a retailer's ability to fulfill orders with the lowest delivery and shipping costs.

> **CUSTOMER PROOF POINTS**
>
> Redis on Google Cloud Platform enables [**Ulta Beauty to build a "digital store of the future"**](https://redis.io/customers/ulta-beauty/)

## How do you build a real-time local inventory search with Redis?

> **GITHUB CODE**
>
> Below is a command to the clone the source code for the application used in this tutorial
>
> git clone [https://github.com/redis-developer/redis-real-time-inventory-solutions](https://github.com/redis-developer/redis-real-time-inventory-solutions)

### How do you set up the data?

Once the application source code is downloaded, run following commands to populate data in Redis:

```bash
# install packages
npm install

# Seed data to Redis
npm run seed
```

The demo uses two collections:

- **Product collection**: Stores product details like `productId`, `name`, `price`, `image`, and other details

![Redis Insight screenshot displaying product JSON documents with fields for productId, name, price, and image URL](/images/site-mirror/dc982240c01773e038de4e94f150750eda39f392-2000x611.webp)

> **TIP**
>
> Download [Redis Insight](https://redis.io/insight/) to view your Redis data or to play with raw Redis commands in the workbench.

- **StoresInventory collection**: Stores product quantity available at different local stores.

For demo purpose, we are using the below regions in New York, US as store locations. Products are mapped to these location stores with a storeId and quantity.

![Map of New York State highlighting ten demo store locations used for geo-spatial inventory search](/images/site-mirror/1d330a39940a70cfba618b17d23bf6d9a711d118-1272x998.webp)

![Redis Insight screenshot showing StoresInventory JSON documents with storeId, SKU, quantity, and geo-coordinates per store](/images/site-mirror/1f7113d222bfa29dd28361ef20b4f3ac089335fb-2000x656.webp)

Let's build the following APIs to demonstrate geospatial search using Redis:

- **InventorySearch API**: Search Products in local stores within a search radius.
- **InventorySearchWithDistance API**: Search Product in local stores within search radius and sort results by distance from current user location to store.

### How does the InventorySearch API work?

The code that follows shows an example API request and response for the `inventorySearch` API:

#### inventorySearch API Request

```bash
{
    "sku":1019688,
    "searchRadiusInKm":500,
    "userLocation": {
        "latitude": 42.880230,
        "longitude": -78.878738
    }
}
```

#### inventorySearch API Response

```bash
{
  "data": [
    {
      "storeId": "02_NY_ROCHESTER",
      "storeLocation": {
        "longitude": -77.608849,
        "latitude": 43.156578
      },
      "sku": 1019688,
      "quantity": 38
    },
    {
      "storeId": "05_NY_WATERTOWN",
      "storeLocation": {
        "longitude": -75.910759,
        "latitude": 43.974785
      },
      "sku": 1019688,
      "quantity": 31
    },
    {
      "storeId": "10_NY_POUGHKEEPSIE",
      "storeLocation": {
        "longitude": -73.923912,
        "latitude": 41.70829
      },
      "sku": 1019688,
      "quantity": 45
    }
  ],
  "error": null
}
```

When you make a request, it goes through the API gateway to the `inventory service`. Ultimately, it ends up calling an `inventorySearch` function which looks as follows:

```js
/**
 * Search Product in stores within search radius.
 *
 * :param _inventoryFilter: Product Id (sku), searchRadiusInKm and current userLocation
 * :return: Inventory product list
 */
static async inventorySearch(_inventoryFilter: IInventoryBodyFilter): Promise<IStoresInventory[]> {
    const nodeRedisClient = getNodeRedisClient();

    const repository = StoresInventoryRepo.getRepository();
    let retItems: IStoresInventory[] = [];

    if (nodeRedisClient && repository && _inventoryFilter?.sku
        && _inventoryFilter?.userLocation?.latitude
        && _inventoryFilter?.userLocation?.longitude) {

        const lat = _inventoryFilter.userLocation.latitude;
        const long = _inventoryFilter.userLocation.longitude;
        const radiusInKm = _inventoryFilter.searchRadiusInKm || 1000;

        const queryBuilder = repository.search()
            .where('sku')
            .eq(_inventoryFilter.sku)
            .and('quantity')
            .gt(0)
            .and('storeLocation')
            .inRadius((circle) => {
                return circle
                    .latitude(lat)
                    .longitude(long)
                    .radius(radiusInKm)
                    .kilometers
            });

        console.log(queryBuilder.query);
        /* Sample queryBuilder query
          ( ( (@sku:[1019688 1019688]) (@quantity:[(0 +inf]) ) (@storeLocation:[-78.878738 42.88023 500 km]) )
        */

        retItems = <IStoresInventory[]>await queryBuilder.return.all();

        /* Sample command to run query directly on CLI
          FT.SEARCH StoresInventory:index '( ( (@sku:[1019688 1019688]) (@quantity:[(0 +inf]) ) (@storeLocation:[-78.878738 42.88023 500 km]) )'
        */

        if (!retItems.length) {
            throw `Product not found with in ${radiusInKm}km range!`;
        }
    }
    else {
        throw `Input params failed !`;
    }
    return retItems;
}
```

### How does the InventorySearchWithDistance API work?

The code that follows shows an example API request and response for `inventorySearchWithDistance` API:

#### inventorySearchWithDistance API request

```bash
{
  "sku": 1019688,
  "searchRadiusInKm": 500,
  "userLocation": {
    "latitude": 42.88023,
    "longitude": -78.878738
  }
}
```

#### inventorySearchWithDistance API response

```bash
{
  "data": [
    {
      "storeId": "02_NY_ROCHESTER",
      "storeLocation": {
        "longitude": -77.608849,
        "latitude": 43.156578
      },
      "sku": "1019688",
      "quantity": "38",
      "distInKm": "107.74513"
    },
    {
      "storeId": "05_NY_WATERTOWN",
      "storeLocation": {
        "longitude": -75.910759,
        "latitude": 43.974785
      },
      "sku": "1019688",
      "quantity": "31",
      "distInKm": "268.86249"
    },
    {
      "storeId": "10_NY_POUGHKEEPSIE",
      "storeLocation": {
        "longitude": -73.923912,
        "latitude": 41.70829
      },
      "sku": "1019688",
      "quantity": "45",
      "distInKm": "427.90787"
    }
  ],
  "error": null
}
```

When you make a request, it goes through the API gateway to the inventory service. Ultimately, it ends up calling an `inventorySearchWithDistance` function which looks as follows:

```js
/**
 * Search Product in stores within search radius, Also sort results by distance from current user location to store.
 *
 * :param _inventoryFilter: Product Id (sku), searchRadiusInKm and current userLocation
 * :return: Inventory product list
 */
static async inventorySearchWithDistance(_inventoryFilter: IInventoryBodyFilter): Promise<IStoresInventory[]> {
    const nodeRedisClient = getNodeRedisClient();

    const repository = StoresInventoryRepo.getRepository();
    let retItems: IStoresInventory[] = [];

    if (nodeRedisClient && repository && _inventoryFilter?.sku
        && _inventoryFilter?.userLocation?.latitude
        && _inventoryFilter?.userLocation?.longitude) {

        const lat = _inventoryFilter.userLocation.latitude;
        const long = _inventoryFilter.userLocation.longitude;
        const radiusInKm = _inventoryFilter.searchRadiusInKm || 1000;

        const queryBuilder = repository.search()
            .where('sku')
            .eq(_inventoryFilter.sku)
            .and('quantity')
            .gt(0)
            .and('storeLocation')
            .inRadius((circle) => {
                return circle
                    .latitude(lat)
                    .longitude(long)
                    .radius(radiusInKm)
                    .kilometers
            });

        console.log(queryBuilder.query);
        /* Sample queryBuilder query
            ( ( (@sku:[1019688 1019688]) (@quantity:[(0 +inf]) ) (@storeLocation:[-78.878738 42.88023 500 km]) )
        */

        const indexName = `${StoresInventoryRepo.STORES_INVENTORY_KEY_PREFIX}:index`;
        const aggregator = await nodeRedisClient.ft.aggregate(
            indexName,
            queryBuilder.query,
            {
                LOAD: ["@storeId", "@storeLocation", "@sku", "@quantity"],
                STEPS: [{
                    type: AggregateSteps.APPLY,
                    expression: `geodistance(@storeLocation, ${long}, ${lat})/1000`,
                    AS: 'distInKm'
                }, {
                    type: AggregateSteps.SORTBY,
                    BY: "@distInKm"
                }]
            });

        /* Sample command to run query directly on CLI
            FT.AGGREGATE StoresInventory:index '( ( (@sku:[1019688 1019688]) (@quantity:[(0 +inf]) ) (@storeLocation:[-78.878738 42.88023 500 km]) )' LOAD 4 @storeId @storeLocation @sku @quantity  APPLY "geodistance(@storeLocation,-78.878738,42.88043)/1000" AS distInKm SORTBY 1 @distInKm
        */

        retItems = <IStoresInventory[]>aggregator.results;

        if (!retItems.length) {
            throw `Product not found with in ${radiusInKm}km range!`;
        }
        else {
            retItems = retItems.map((item) => {
                if (typeof item.storeLocation == "string") {
                    const location = item.storeLocation.split(",");
                    item.storeLocation = {
                        longitude: Number(location[0]),
                        latitude: Number(location[1]),
                    }
                }
                return item;
            })
        }
    }
    else {
        throw `Input params failed !`;
    }
    return retItems;
}
```

## Next steps

Now that you've seen how to build a local inventory search with Redis geo-spatial queries, here are some ways to go further:

- **Add available-to-promise logic**: Combine local inventory search with [Available to Promise (ATP)](/tutorials/howtos/solutions/real-time-inventory/available-to-promise/) to show customers real-time reservable quantities, not just raw stock counts.
- **Learn geospatial fundamentals**: If you haven't already, work through the [Getting Started with Geo](/tutorials/howtos/solutions/geo/getting-started/) tutorial to deepen your understanding of Redis GEOSEARCH and related commands.
- **Build an omnichannel store finder**: Extend the search API to return store hours, curbside pickup availability, and shipping estimates alongside inventory data.
- **Add real-time stock updates**: Use [Redis Streams](https://redis.io/docs/latest/develop/data-types/streams/) to process point-of-sale events and keep store inventory counts accurate in real time.

### Additional resources

Real time inventory with Redis

- [Available to Promise in Real-time Inventory](/tutorials/howtos/solutions/real-time-inventory/available-to-promise/)

General

- [Redis YouTube channel](https://www.youtube.com/c/Redisinc)
- Clients like [Node Redis](https://github.com/redis/node-redis) and [Redis om Node](https://github.com/redis/redis-om-node) help you to use Redis in Node.js apps.
- [Redis Insight](https://redis.io/insight/) : To view your Redis data or to play with raw Redis commands in the workbench
- [Try Redis Cloud for free](https://redis.io/try-free/)
