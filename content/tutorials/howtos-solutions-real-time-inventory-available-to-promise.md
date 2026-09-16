---
title: "Available to Promise in Real-time Inventory Using Redis"
linkTitle: "Available to Promise in Real-time Inventory Using Redis"
url: "/tutorials/howtos/solutions/real-time-inventory/available-to-promise/"
description: "The major requirement in a retail inventory system is presenting an accurate, real-time view of inventory to shoppers and store associates enabling buy-online-pickup-in-store (BOPIS). Optimizing..."
group: "For AI"
aliases:
- "/tutorials/howtos-solutions-real-time-inventory-available-to-promise/"
date: 2026-02-25
lastmod: 2026-02-25
hidden: true
mirrored: true
---

*Published 25 February 2026*

> **TL;DR:**
>
> Available-to-promise (ATP) is the projected inventory available to sell after accounting for existing allocations and expected supply. Redis enables real-time ATP by providing sub-millisecond reads and atomic inventory updates across all sales channels, so every customer sees accurate stock levels instantly.

> **GITHUB CODE**
>
> Below is a command to the clone the source code for the application used in this tutorial
>
> git clone [https://github.com/redis-developer/redis-real-time-inventory-solutions](https://github.com/redis-developer/redis-real-time-inventory-solutions)

## What you'll learn

- What available-to-promise (ATP) means and how to calculate it
- Why traditional inventory systems struggle with real-time accuracy
- How Redis delivers sub-millisecond inventory checks across omnichannel sales
- How to implement SKU retrieval, update, increment, and decrement operations with Redis
- How to handle bulk inventory operations for multi-product orders

## What is available-to-promise (ATP)?

The major requirement in a **retail inventory system** is presenting an accurate, real-time view of inventory to shoppers and store associates enabling buy-online-pickup-in-store (BOPIS). Optimizing fulfillment from multiple inventory locations.

**Available to promise (ATP)** is the projected amount of inventory left available to sell, not including allocated inventory. It allows businesses to control distribution to their customers and predict inventory. The ATP model helps retailers keep inventory costs down such as ordering costs, carrying costs and stock-out costs. ATP is helpful as long as consumer buying forecasts remain correct. Implementing ATP processes effectively for retailers can mean the difference between sustained growth and an inventory that repeatedly runs out of customer's favorite products missing sales opportunities and harming customer experience.

### How do you calculate available-to-promise?

Calculating available-to-promise is a relatively simple undertaking. Complete the following formula for an accurate breakdown of available-to-promise capabilities:

```txt
Available-to-promise = QuantityOnHand + Supply - Demand
```

This formula includes the following elements:

- QuantityOnHand: the total number of products that are immediately available to a company
- Supply: the total stock of a product available for sale
- Demand: the amount of a specific product that consumers are willing to purchase

## What are the current challenges in real-time inventory?

- **Over and under-stocking**: While adopting a multi-channel business model (online & in store), lack of inventory visibility results in over and under-stocking of inventory in different regions and stores.
- Consumers **seek convenience**: The ability to search across regional store locations and pickup merchandise **immediately** rather than wait for shipping is a key differentiator for retailers. See how Redis powers [local inventory search](/tutorials/howtos/solutions/real-time-inventory/local-inventory-search) to enable this.
- Consumers **seek speed**: All retailers, even small or family-run, must compete against the **customer experience** of large online retailers like Alibaba, FlipKart, Shopee, and Amazon.
- **High inventory costs**: Retailers seek to lower inventory costs by eliminating missed sales from out-of-stock scenarios which also leads to higher "inventory turnover ratios."
- **Brand value**: Inaccurate store inventory counts lead to frustrated customers and lower sales. The operational pain will **impact the status quo**.

## Why should you use Redis for available-to-promise?

- **Increased inventory visibility**: Redis Cloud provides highly scalable, real-time inventory synchronization between stores providing views into what stock is Available-To-Promise. Customers want to buy from a retailer who can check stock across multiple locations and provide real-time views on what's available locally.
- **Enhanced customer experience**: Sub-millisecond latency means online customers can easily get real-time views of shopping carts, pricing, and in stock availability. Redis Cloud built-in search engine delivers full text and aggregated faceted search of inventory in real time, scaling performance to instantly search inventories with millions of product types helping customers fill their shopping carts faster, keeping them engaged and loyal.
- **Cost efficiency at scale**: Redis Cloud offers real-time, bi-directional consistency between stores and data integration capabilities with enterprise systems without the complexity and costs of managing message brokers, auditing, and reconciliation.

## How does real-time inventory work with Redis?

![Architecture diagram showing how Redis synchronizes inventory data in real time across warehouses, stores, and online channels to calculate available-to-promise quantities](/images/site-mirror/dfc8747e956e584f05dfa96b3ad50d7896ffd080-1624x1100.webp)

Using Redis, the system delivers real-time synchronization of inventory across stores, in transit and warehouses. It provides retailers the most accurate, timely data on inventory across their entire store network and gives consumers positive customer experiences searching and locating inventory.

Redis Data Integration (RDI) capabilities enable accurate real-time inventory management and system of record synchronization. Redis advanced inventory search and query capabilities provide accurate available inventory information to multichannel and omnichannel customers and store associates. For a detailed walkthrough of searching inventory by location, see the [Real-time Local Inventory Search](/tutorials/howtos/solutions/real-time-inventory/local-inventory-search) tutorial.

This solution increases inventory turnover ratios resulting in lower inventory costs, higher revenue and profits. It also reduces the impact of customer searches on Systems of Record and Inventory Management Systems (IMS).

### Customer proof points

- Redis Cloud on Google Cloud Platform enables [**Ulta Beauty to build a "digital store of the future"**](https://redis.io/customers/ulta-beauty/)

## How do you manage SKU inventory operations with Redis?

> **GITHUB CODE**
>
> Below is a command to the clone the source code for the application used in this tutorial
>
> git clone [https://github.com/redis-developer/redis-real-time-inventory-solutions](https://github.com/redis-developer/redis-real-time-inventory-solutions)

Managing inventory or a **SKU (stock keeping unit)** process contains some activities like :

1.  RetrieveSKU : Fetch the current quantity of a product
2.  UpdateSKU : Update the latest quantity of a product
3.  IncrementSKU : Increment the quantity by a specific value (Say, when more products are procured)
4.  DecrementSKU : Decrement the quantity by a specific value (Say, after order fulfillment of the product)
5.  RetrieveManySKUs : Fetch the current quantity of **multiple** products (Say, to verify products in stock before payment)
6.  DecrementManySKUs: Decrement the quantity of **multiple** products (Say, after an order fulfillment with multiple products)

### How do you retrieve a single SKU?

The code that follows shows an example API request and response for retrieveSKU activity.

#### retrieveSKU API Request

```bash
GET http://localhost:3000/api/retrieveSKU?sku=1019688
```

#### retrieveSKU API Response

```json
{
    "data": {
        "sku": 1019688,
        "name": "5-Year Protection Plan - Geek Squad",
        "type": "BlackTie",
        "totalQuantity": 10
    },
    "error": null
}
```

When you make a request, it goes through the API gateway to the inventory service. Ultimately, it ends up calling a `retrieveSKU` function which looks as follows:

```js
static async retrieveSKU(_productId: number): Promise<IProduct> {
    /**
    Get current Quantity of a Product.

    :param _productId: Product Id
    :return: Product with Quantity
    */
    const repository = ProductRepo.getRepository();
    let retItem: IProduct = {};

    if (repository && _productId) {
        //fetch product by ID (using redis om library)
        const product = <IProduct>await repository.fetch(_productId.toString());

        if (product) {
            retItem = {
                sku: product.sku,
                name: product.name,
                type: product.type,
                totalQuantity: product.totalQuantity
            }
        }
        else {
            throw `Product with Id ${_productId} not found`;
        }
    }
    else {
        throw `Input params failed !`;
    }

    return retItem;
}
```

### How do you update a SKU quantity?

The code that follows shows an example API request and response for updateSKU activity.

#### updateSKU API Request

```bash
POST http://localhost:3000/api/updateSKU
{
    "sku":1019688,
    "quantity":25
}
```

#### updateSKU API Response

```json
{
    "data": {
        "sku": 1019688,
        "name": "5-Year Protection Plan - Geek Squad",
        "type": "BlackTie",
        "totalQuantity": 25 //updated value
    },
    "error": null
}
```

When you make a request, it goes through the API gateway to the inventory service. Ultimately, it ends up calling a `updateSKU` function which looks as follows:

```js
 static async updateSKU(_productId: number, _quantity: number): Promise<IProduct> {
        /**
        Set Quantity of a Product.

        :param _productId: Product Id
        :param _quantity: new quantity
        :return: Product with Quantity
        */
        const repository = ProductRepo.getRepository();
        let retItem: IProduct = {};

        if (repository && _productId && _quantity >= 0) {
            //fetch product by ID (using redis om library)
            const product = <IProduct>await repository.fetch(_productId.toString());

            if (product) {
                //update the product fields
                product.totalQuantity = _quantity;

                // save the modified product
                const savedItem = <IProduct>await repository.save(<RedisEntity>product);

                retItem = {
                    sku: savedItem.sku,
                    name: savedItem.name,
                    type: savedItem.type,
                    totalQuantity: savedItem.totalQuantity
                }
            }
            else {
                throw `Product with Id ${_productId} not found`;
            }
        }
        else {
            throw `Input params failed !`;
        }

        return retItem;
    }
```

### How do you increment a SKU quantity?

The code that follows shows an example API request and response for incrementSKU activity.

#### incrementSKU API Request

```bash
POST http://localhost:3000/api/incrementSKU
{
    "sku":1019688,
    "quantity":2
}
```

#### incrementSKU API Response

```json
{
    "data": {
        "sku": 1019688,
        "name": "5-Year Protection Plan - Geek Squad",
        "type": "BlackTie",
        "totalQuantity": 12 //previous value 10
    },
    "error": null
}
```

When you make a request, it goes through the API gateway to the inventory service. Ultimately, it ends up calling a `incrementSKU` function which looks as follows:

```js
static async incrementSKU(_productId: number, _incrQuantity: number, _isDecrement: boolean, _isReturnProduct: boolean): Promise<IProduct> {
        /**
        increment quantity of a Product.

        :param _productId: Product Id
        :param _incrQuantity: new increment quantity
        :return: Product with Quantity
        */

        const redisOmClient = getRedisOmClient();
        let retItem: IProduct = {};

        if (!_incrQuantity) {
            _incrQuantity = 1;
        }
        if (_isDecrement) {
            _incrQuantity = _incrQuantity * -1;
        }
        if (redisOmClient && _productId && _incrQuantity) {

            const updateKey = `${ProductRepo.PRODUCT_KEY_PREFIX}:${_productId}`;

            //increment json number field by specific (positive/ negative) value
            await redisOmClient.redis?.json.numIncrBy(updateKey, '$.totalQuantity', _incrQuantity);

            if (_isReturnProduct) {
                retItem = await InventoryServiceCls.retrieveSKU(_productId);
            }

        }
        else {
            throw `Input params failed !`;
        }

        return retItem;
    }
```

### How do you decrement a SKU quantity?

The code that follows shows an example API request and response for decrementSKU activity.

#### decrementSKU API Request

```bash
POST http://localhost:3000/api/decrementSKU
{
    "sku":1019688,
    "quantity":4
}
```

#### decrementSKU API Response

```json
{
    "data": {
        "sku": 1019688,
        "name": "5-Year Protection Plan - Geek Squad",
        "type": "BlackTie",
        "totalQuantity": 16 //previous value 20
    },
    "error": null
}
```

When you make a request, it goes through the API gateway to the inventory service. Ultimately, it ends up calling a `decrementSKU` function which looks as follows:

```js
static async decrementSKU(_productId: number, _decrQuantity: number): Promise<IProduct> {
        /**
        decrement quantity of a Product.

        :param _productId: Product Id
        :param _decrQuantity: new decrement quantity
        :return: Product with Quantity
        */
        let retItem: IProduct = {};

        //validating if product in stock
        let isValid = await InventoryServiceCls.validateQuantityOnDecrementSKU(_productId, _decrQuantity);

        if (isValid) {
            const isDecrement = true; //increments with negative value
            const isReturnProduct = true;
            retItem = await InventoryServiceCls.incrementSKU(_productId, _decrQuantity, isDecrement, isReturnProduct);
        }

        return retItem;
    }

    static async validateQuantityOnDecrementSKU(_productId: number, _decrQuantity?: number): Promise<boolean> {
        let isValid = false;

        if (!_decrQuantity) {
            _decrQuantity = 1;
        }

        if (_productId) {
            const product = await InventoryServiceCls.retrieveSKU(_productId);
            if (product && product.totalQuantity && product.totalQuantity > 0
                && (product.totalQuantity - _decrQuantity >= 0)) {

                isValid = true;
            }
            else {
                throw `For product with Id ${_productId},  available quantity(${product.totalQuantity}) is lesser than decrement quantity(${_decrQuantity})`;
            }

        }
        return isValid;
    }
```

### How do you retrieve multiple SKUs at once?

The code that follows shows an example API request and response for retrieveManySKUs activity.

#### retrieveManySKUs API Request

```bash
POST http://localhost:3000/api/retrieveManySKUs
[{
    "sku":1019688
},{
    "sku":1003622
},{
    "sku":1006702
}]
```

#### retrieveManySKUs API Response

```json
{
    "data": [
        {
            "sku": 1019688,
            "name": "5-Year Protection Plan - Geek Squad",
            "type": "BlackTie",
            "totalQuantity": 24
        },
        {
            "sku": 1003622,
            "name": "Aquarius - Fender Stratocaster 1,000-Piece Jigsaw Puzzle - Black/Red/White/Yellow/Green/Orange/Blue",
            "type": "HardGood",
            "totalQuantity": 10
        },
        {
            "sku": 1006702,
            "name": "Clash of the Titans [DVD] [2010]",
            "type": "Movie",
            "totalQuantity": 10
        }
    ],
    "error": null
}
```

When you make a request, it goes through the API gateway to the inventory service. Ultimately, it ends up calling a `retrieveManySKUs` function which looks as follows:

```js
static async retrieveManySKUs(_productWithIds: IProductBodyFilter[]): Promise<IProduct[]> {
        /**
        Get current Quantity of specific Products.

        :param _productWithIds: Product list with Id
        :return: Product list
        */
        const repository = ProductRepo.getRepository();
        let retItems: IProduct[] = [];

        if (repository && _productWithIds && _productWithIds.length) {

            //string id array
            const idArr = _productWithIds.map((product) => {
                return product.sku?.toString() || ""
            });

           //fetch products by IDs (using redis om library)
            const result = await repository.fetch(...idArr);

            let productsArr: IProduct[] = [];

            if (idArr.length == 1) {
                productsArr = [<IProduct>result];
            }
            else {
                productsArr = <IProduct[]>result;
            }

            if (productsArr && productsArr.length) {

                retItems = productsArr.map((product) => {
                    return {
                        sku: product.sku,
                        name: product.name,
                        type: product.type,
                        totalQuantity: product.totalQuantity
                    }
                });
            }
            else {
                throw `No products found !`;
            }
        }
        else {
            throw `Input params failed !`;
        }

        return retItems;
    }
```

### How do you decrement multiple SKUs at once?

The code that follows shows an example API request and response for decrementManySKUs activity.

#### decrementManySKUs API Request

```bash
POST http://localhost:3000/api/decrementManySKUs
[{
    "sku":1019688,
    "quantity":4
},{
    "sku":1003622,
     "quantity":2
},{
    "sku":1006702,
    "quantity":2
}]
```

#### decrementManySKUs API Response

```json
{
    "data": [
        {
            "sku": 1019688,
            "name": "5-Year Protection Plan - Geek Squad",
            "type": "BlackTie",
            "totalQuantity": 28 //previous value 32
        },
        {
            "sku": 1003622,
            "name": "Aquarius - Fender Stratocaster 1,000-Piece Jigsaw Puzzle - Black/Red/White/Yellow/Green/Orange/Blue",
            "type": "HardGood",
            "totalQuantity": 8 //previous value 10
        },
        {
            "sku": 1006702,
            "name": "Clash of the Titans [DVD] [2010]",
            "type": "Movie",
            "totalQuantity": 8 //previous value 10
        }
    ],
    "error": null
}
```

When you make a request, it goes through the API gateway to the inventory service. Ultimately, it ends up calling a `decrementManySKUs` function which looks as follows:

```js
 static async decrementManySKUs(_productsFilter: IProductBodyFilter[]): Promise<IProduct[]> {
        /**
        decrement quantity  of specific Products.

        :param _productWithIds: Product list with Id
        :return: Product list
        */
        let retItems: IProduct[] = [];

        if (_productsFilter && _productsFilter.length) {
            //validation only
            const promArr: Promise<boolean>[] = [];
            for (let p of _productsFilter) {
                if (p.sku) {
                  //validating if all products in stock
                    const promObj = InventoryServiceCls.validateQuantityOnDecrementSKU(p.sku, p.quantity);
                    promArr.push(promObj)
                }
            }
            await Promise.all(promArr);

            //decrement only
            const promArr2: Promise<IProduct>[] = [];
            for (let p of _productsFilter) {
                if (p.sku && p.quantity) {
                    const isDecrement = true; //increments with negative value
                    const isReturnProduct = false;
                    const promObj2 = InventoryServiceCls.incrementSKU(p.sku, p.quantity, isDecrement, isReturnProduct);
                    promArr2.push(promObj2)
                }
            }
            await Promise.all(promArr2);

            //retrieve updated products
            retItems = await InventoryServiceCls.retrieveManySKUs(_productsFilter);
        }
        else {
            throw `Input params failed !`;
        }

        return retItems;
    }
```

## Next steps

Now that you understand how to build an available-to-promise inventory system with Redis, here are some ways to go further:

- **Add location-based inventory search**: Learn how to let customers find products at nearby stores with the [Real-time Local Inventory Search](/tutorials/howtos/solutions/real-time-inventory/local-inventory-search) tutorial.
- **Explore Redis Insight**: Use [Redis Insight](https://redis.io/insight/) to visualize your inventory data and test raw Redis commands in the workbench.
- **Try Redis Cloud**: Get started with a free instance on [Redis Cloud](https://redis.io/try-free/) to deploy your inventory system.
- **Learn more about Redis clients**: Explore clients like [Node Redis](https://github.com/redis/node-redis) and [Redis OM for Node.js](https://github.com/redis/redis-om-node) used in this tutorial.
- **Watch and learn**: Visit the [Redis YouTube channel](https://www.youtube.com/c/Redisinc) for video walkthroughs and architecture deep dives.
