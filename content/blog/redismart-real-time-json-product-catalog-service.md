---
title: "Building a Fast, Flexible, and Searchable Product Catalog with RedisJSON"
linkTitle: "Building a Fast, Flexible, and Searchable Product Catalog with RedisJSON"
url: "/blog/redismart-real-time-json-product-catalog-service/"
description: "RedisJSON powered by RediSearch is now out in public preview. In this blog post, we’ll dive into getting you started using RedisJSON’s new JSON indexing, querying, and full-text search capabilities..."
date: 2021-11-16
blogCategories:
- "How To and Tutorials"
- "New Product Announcements"
- "Tech"
authors:
- "Adi Wabisabi"
lastmod: 2025-03-27
hidden: true
---

*By Adi Wabisabi, Principal Software Architect, Demo Engineering · Published 16 November 2021 · updated 27 March 2025*

![Blog tile image](/images/blog/f7a57fc0de33ea1c22e48549024343b15110fc8e-929x628.webp)

RedisJSON powered by RediSearch is [now out in public preview](/blog/redisjson-public-preview-performance-benchmarking/). In this blog post, we’ll dive into getting you started using RedisJSON’s new JSON indexing, querying, and full-text search capabilities by looking at how it was used to build RedisMart’s product catalog service. In case you missed it, RedisMart is the fully-functional [real-time retail](/industries/retail/) store we demoed during the [RedisConf 2021 keynote presentation](https://www.youtube.com/watch?v=Q6LfMTNbQOs). We also published a [blog](/blog/redismart-retail-application-with-redis/) with a deep-dive into the main requirements and architecture of the RedisMart retail application.

## Getting started

[RedisJSON](/json/) is a high-performance document store built on top of Redis open source and available as a source-available license. Its primary goal is to allow you to take the JSON objects you’re likely already using in your application and make them accessible and searchable within Redis. It also offers a more sophisticated data API than the simple hash API, allowing you to expand your data model without having to use multiple keys.

There are a few ways that you can get started using RedisJSON:

- Try it out on [Redis Cloud](/try-free/) or in your Redis Enterprise Installation
- Pull the RedisJSON Docker container, and spin up a copy locally
- Build RedisJSON from source, and run Redis open source with it

For this post, we’re going to be using the Docker container option:

```javascript
$ docker run -d -p 6379:6379 redislabs/rejson:preview
```

Once you have that running, you can connect to it using redis-cli:

```javascript
$ redis-cli json.set foo . '{"hello" : "json"}'
OK
$ redis-cli json.get foo hello
"\"json\""
```

RedisMart is built in Python, so we’ll connect using the recently simplified developer tools.

## Connect to Redis and insert data

At Redis, we tend to prefer using [Poetry](https://python-poetry.org/) for dependency management, but the process for adding redis-py to your application is roughly the same for both:

```javascript
poetry add redis
```

Or, of course:

```javascript
pip install redis
```

Once we have redis-py added to our Python environment, we can connect to our Docker container and do a simple “hello world” application:

```javascript
from redis import Redis
R = Redis()
R.json().set('key', '.', {'hello':'json'})
print(R.json().get('key'))
```

Now that we have the basics in place, let’s create our data model and index.

## Using RedisJSON for document data model

To paraphrase the great Carl Sagan, if you wish to make a RedisJSON product catalog service from scratch, you must first create a search index. For RedisMart, we used a realistic, but straightforward, data model. (See the [full Gist here](https://gist.github.com/timeartist/9b967100a63b5df6fb5209642b5b17e6).)

```javascript
SAMPLE_DATA = [{'SKU': '43214563', 'categories': 'electronics,headphones', 'long_description': 'Monocle ipsum dolor sit amet k-pop smart bespoke, alluring wardrobe espresso Zürich charming Nordic ANA destination elegant bureaux handsome Melbourne. ', 'name': 'Craniumcandy - Wireless Over-the-Ear Headphones - Crazy Tropical', 'price': 100, 'rating': 1, 'short_description': 'Toto, K-pop sharp the highest quality sleepy boutique joy.'}, {'SKU': '431553432', 'name': 'Doodle - Sprite Buds True Wireless In-Ear Headphones - Night Black', 'short_description': 'Beams the highest quality remarkable Swiss concierge. Cosy signature the best extraordinary.', 'long_description': 'Discerning airport first-class, elegant conversation artisanal Beams flat white ryokan Helsinki Boeing 787 K-pop concierge soft power iconic. Toto Melbourne pintxos, joy destination global craftsmanship St Moritz smart premium boutique. Boeing 787 premium first-class extraordinary the best Zürich discerning elegant. Charming impeccable emerging sophisticated international Airbus A380 efficient Beams cosy Marylebone Muji Asia-Pacific. Charming uniforms Beams airport, essential Zürich global Nordic extraordinary Boeing 787 iconic vibrant.', 'price': 180, 'rating': 5, 'categories': 'electronics,headphones'}, {'SKU': '8743153432', 'name': 'Doodle - Sprite 6 Expert', 'short_description': 'Beams the highest quality remarkable Swiss concierge. Cosy signature the best extraordinary.', 'long_description': 'Discerning airport first-class, elegant conversation artisanal Beams flat white ryokan Helsinki Boeing 787 K-pop concierge soft power iconic. Toto Melbourne pintxos, joy destination global craftsmanship St Moritz smart premium boutique. Boeing 787 premium first-class extraordinary the best Zürich discerning elegant. Charming impeccable emerging sophisticated international Airbus A380 efficient Beams cosy Marylebone Muji Asia-Pacific. Charming uniforms Beams airport, essential Zürich global Nordic extraordinary Boeing 787 iconic vibrant.', 'price': 899, 'rating': 5, 'categories': 'cell phone,electronics'}, {'SKU': '4316647899', 'name': 'Blues Banjo Songs for Noobs - Gal Nimoy', 'short_description': 'The best Boeing 787 Lufthansa Toto. Destination Singapore efficient Nordic craftsmanship.', 'long_description': 'Wardrobe Fast Lane exclusive perfect delightful extraordinary Melbourne K-pop classic Airbus A380 elegant the highest quality. Emerging boutique concierge quality of life finest, punctual elegant delightful pintxos airport tote bag Muji flat white Swiss.', 'price': 23, 'rating': 3, 'categories': 'books,music'}, {'SKU': '84836424542', 'name': 'Be Here Now - Richard Alpert', 'short_description': 'The best Boeing 787 Lufthansa Toto. Destination Singapore efficient Nordic craftsmanship.', 'long_description': 'Wardrobe Fast Lane exclusive perfect delightful extraordinary Melbourne K-pop classic Airbus A380 elegant the highest quality. Emerging boutique concierge quality of life finest, punctual elegant delightful pintxos airport tote bag Muji flat white Swiss.', 'price': 42, 'rating': 3, 'categories': 'books'}]
```

Taking it and creating an index is pretty straightforward:

```javascript
  definition = IndexDefinition(prefix=[PRODUCTS_KEY.format('')], index_type=IndexType.JSON)

    ## Categories implemented as Tags - allows for more complex searching
    ctg_field = TagField('$.categories', as_name='categories')
    ctg_field_params = list(ctg_field.args)
    ctg_field.args = tuple(ctg_field_params)

    ## actually create the index
    client.create_index((
        TagField("$.SKU", as_name='SKU'),
        TextField("$.name", as_name='name'),
        TextField("$.short_description", as_name='short_description'),
        TextField("$.long_description", as_name='long_description'),
        NumericField("$.price", sortable=True, as_name='price'),
        NumericField("$.rating", sortable=True, as_name='rating'),
        ctg_field),
        definition=definition)
```

Notice how, for each field, we’re using the as_name argument to set an alias for the full path. This is helpful for two reasons: one, you don’t have to specify the full path when you’re using that attribute in your query. And two, it allows you to change the underlying path of that attribute without having to change the code that calls it.

Once the index is created, you’ll use the same object to search it. Best practice is to first check to see if the index is created by using the .info() method, and if it isn’t, to do so. Let’s expand our search index creation code to add those cases:

```javascript
 client = SearchClient(PRODUCTS_INDEX_KEY, conn=R)
    try:
        client.info()
        return client
    except ResponseError:
        print("index doesn't exist, creating")
```

A nice thing about using RedisJSON is that you can easily add new fields to your index with the [FT.ALTER](https://redis.io/docs/stack/search/commands/) command.

Next, we’ll make this search functionality accessible to the rest of the application.

## Using RedisJSON for querying the product catalog

One requirement for this project was that we’d be able to query the product catalog using different attributes. Querying by name of the product is an obvious choice, but we also implemented filtering by price, rating, and category as well. In the faceted navigation menu, you can use it to quickly find what you are looking for.

![](/images/blog/0ca9abe257ee49d6c6c4af11853ea5932d88f99b-1024x596.webp)

The category also shows up in the autocomplete drop-down powered by the fuzzy search feature of RedisJSON:

![](/images/blog/6e3b0f203c11e1aeaf69176cf78e67f6292f3f4a-640x342.webp)

Fuzzy search is easy to do using the Suggestions feature, which we can add to any data that we’re adding to the catalog:

```javascript
def add_products():
    '''
    Ingests the sample data into the DB
    '''
    with R.pipeline(transaction=False) as pipeline:
        for product in SAMPLE_DATA:
            key = PRODUCTS_KEY.format(product['SKU'])
            pipeline.jsonset(key, Path.rootPath(), product)
            
            ac = AutoCompleter(AUTOCOMPLETE_KEY, conn=pipeline)
            categories = product['categories'].split(',')
            suggestions = [Suggestion(product['name'])]
            suggestions.extend([Suggestion(category) for category in categories])
            ac.add_suggestions(*suggestions)

        pipeline.execute()
```

Now that we have our index and suggestions setup, let’s build a search query function for our product microservice:

```javascript
def search_products(name=None, categories=None, price=None, rating=None, fields=None,
                     paging=None, sort_by='name', ascending=True, **kwargs):
    '''
    Search the product catalog
    name - name of the product 
    categories - comma delimited category list (category1,category2)
    price - price range, hyphen delimited (price_low-price_high)
    rating - rating range, hyphen delmited (rating_low-rating_high)
    fields - object fields to return in response
    paging - comma delimited, show item range in this page (paging_start,paging_end)
    sort_by - field to sort by
    ascending - ascending or descending
    '''
    ## for non-numeric search terms, we'll build the term query
    search_terms = []
    if name:
        search_terms.append(f'@name:{name}')
    if categories:
        _categories = categories.split(',')
        search_terms.append(f'@categories:{{{"|".join(_categories)}}}') ## tag search uses {} vs () for compounds

    if search_terms:
        ## join the non-numeric terms together to create the query object
        terms_query = ' '.join(search_terms)
    else:
        ## no non-numeric ones were set, wildcard
        terms_query = '*'

    ## create and configure query object
    query = Query(terms_query)
    query.sort_by(sort_by, asc=ascending)
    if paging is not None:
        query.paging(*paging.split(','))
    if fields is not None:
        query.return_fields(*fields.split(','))

    ## numeric terms and other query parameters
    if price:
        price_low, price_high = price.split('-')
        query.add_filter(NumericFilter('price', price_low, price_high))
    if rating:
        rating_low, rating_high = rating.split('-')
        query.add_filter(NumericFilter('rating', rating_low, rating_high))

    ## execute search
    result = product_index().search(query)
    return [loads(doc.json) for doc in result.docs] # in order to get these all into one json obj, we'll need to transerialze them
```

Last, but not least, we’ll need to add the ability to add and modify items from the rest of the application.

## RedisJSON for CRUD operations

For RedisMart, we put the product catalog inside of a microservice.

![](/images/blog/5b9b9020b28f62858e7a020a2128fd97070060f1-1024x664.webp)

In order to complete the REST API, we’ll need to add our creation, update and delete flows.

```javascript
ALLOWED_FIELDS = ['SKU', 'name', 'categories', 'short_description', 'long_description', 'price', 'rating']

@app.route('/')
def get_search():
    '''
    Search the product catalog
    URL Args:
    name - name of the product 
    categories - comma delimited category list (category1,category2)
    price - price range, hyphen delimited (price_low-price_high)
    rating - rating range, hyphen delmited (rating_low-rating_high)
    fields - object fields to return in response
    paging - tuple of item range to show in this page (beginning, end)
    sort_by - field to sort by
    ascending - ascending or descending
    '''
    return jsonify(search_products(**request.args))    

@app.route('/suggestions/<string:stem>')
def get_suggestions(stem):
    '''
    Get autocomplete suggestions for a given stem
    '''
    return jsonify(get_suggestions(escape(stem)))

@app.route('/product', methods=['POST'])
def post_product():
    '''
    HTTP POST request to create/update a product
    '''
    product = {}
    for k, v in request.form.items():
        if k not in ALLOWED_FIELDS:
            return f'{k} not allowed in product POST request', 403
        product[k] = v

    key = PRODUCTS_KEY.format(product['SKU'])
    R.jsonset(key, Path.rootPath(), product)
    return Response(status=200)

@app.route('/product/<string:sku>')
def get_product(sku):
    '''
    Get the JSON object for a product from its SKU
    '''
    key = PRODUCTS_KEY.format(sku)
    return jsonify(R.jsonget(key))

@app.route('/product/<string:sku>', methods=['DELETE'])
def delete_product(sku):
    '''
    Remove a product from the catalog
    '''
    key = PRODUCTS_KEY.format(sku)
    key_deleted = R.delete(key)
    if key_deleted:
        return Response(status=200)
    else:
        return Response(status=404)
```

## Where can I go from here?

By now, you can see how to easily take your JSON-based product data and make it searchable and accessible to any modern application by using a microservice. In addition to indexing, searching, and full-text search features on JSON documents, RedisJSON powered by RediSearch also includes powerful [data aggregation ](https://redis.io/docs/stack/search/reference/aggregations/)capabilities (see [tutorial](https://github.com/RediSearch/redisearch-getting-started) and [online course](https://university.redis.com/courses/ru201/)). Here’s some links to get you started

- [RedisJSON web page](/json/)
- [RedisJSON ](https://redis.io/docs/data-types/json/)tutorial
- [Indexing, Querying, and Full-Text Search of JSON Documents with Redis](/blog/index-and-query-json-docs-with-redis/)

### See the full GitHub Gist

```python
Prerequisites:
Python 3.9+
Redis & RedisJSON 2.0
To run:
## if you want to run the container locally
docker run -d -p 6379:6379 redislabs/rejson:preview
pip3 install poetry
poetry install
poetry run python3 redismart_product_catalog.py
Access by navigating to
http://localhost:5000

```

```python
[tool.poetry]
name = "redismart_product_catalog"
version = "0.1.0"
description = "Accompanying Code for RedisMart Blog Pt. 2"
authors = []
license = "BSD"

[tool.poetry.dependencies]
python = "^3.9"
redis = "^3.5.3"
rejson = "^0.5.4"
redisearch = {git = "https://github.com/RediSearch/redisearch-py", rev = "master"}
Flask = "^2.0.2"

[tool.poetry.dev-dependencies]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

```

```python
# Copyright 2021 Redis Ltd.
#
# Redistribution and use in source and binary forms, with or without modification, 
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, 
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, 
# this list of conditions and the following disclaimer in the documentation and/or 
# other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors 
# may be used to endorse or promote products derived from this software without 
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING 
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from json import JSONDecoder, loads

from flask import Flask, request, Response, escape, jsonify
from rejson import Client, Path
from redis import ResponseError
from redisearch.client import IndexType
from redisearch import (Client as SearchClient, 
                        NumericField, 
                        TextField, 
                        TagField, 
                        IndexDefinition, 
                        Suggestion,
                        AutoCompleter,
                        NumericFilter,
                        Query)

class RedisJsonDecoder(JSONDecoder):
    def decode(self, s, *args, **kwargs):
        if isinstance(s, bytes):
            s = s.decode('UTF-8')
        elif isinstance(s, list):
            return s[0]
        return super(RedisJsonDecoder, self).decode(s, *args, **kwargs)

R = Client(decode_responses=True,
           encoding_errors='ignore',
           decoder=RedisJsonDecoder())

assert R.ping()

app = Flask(__name__)

                                    #########
                                    ## API ##
                                    #########

ALLOWED_FIELDS = ['SKU', 'name', 'categories', 'short_description', 'long_description', 'price', 'rating']

@app.route('/')
def get_search():
    '''
    Search the product catalog
    URL Args:
    name - name of the product 
    categories - comma delimited category list (category1,category2)
    price - price range, hyphen delimited (price_low-price_high)
    rating - rating range, hyphen delmited (rating_low-rating_high)
    fields - object fields to return in response
    paging - tuple of item range to show in this page (beginning, end)
    sort_by - field to sort by
    ascending - ascending or descending
    '''
    return jsonify(search_products(**request.args))    

@app.route('/suggestions/<string:stem>')
def get_suggestions(stem):
    '''
    Get autocomplete suggestions for a given stem
    '''
    return jsonify(get_suggestions(escape(stem)))

@app.route('/product', methods=['POST'])
def post_product():
    '''
    HTTP POST request to create/update a product
    '''
    product = {}
    for k, v in request.form.items():
        if k not in ALLOWED_FIELDS:
            return f'{k} not allowed in product POST request', 403
        product[k] = v

    key = PRODUCTS_KEY.format(product['SKU'])
    R.jsonset(key, Path.rootPath(), product)
    return Response(status=200)

@app.route('/product/<string:sku>')
def get_product(sku):
    '''
    Get the JSON object for a product from its SKU
    '''
    key = PRODUCTS_KEY.format(sku)
    return jsonify(R.jsonget(key))

@app.route('/product/<string:sku>', methods=['DELETE'])
def delete_product(sku):
    '''
    Remove a product from the catalog
    '''
    key = PRODUCTS_KEY.format(sku)
    key_deleted = R.delete(key)
    if key_deleted:
        return Response(status=200)
    else:
        return Response(status=404)

                                    ########
                                    ## DB ##
                                    ########

PRODUCTS_KEY = 'prod:{}'
PRODUCTS_INDEX_KEY = 'idx:prod'
AUTOCOMPLETE_KEY = 'ac:prods&cats'

SAMPLE_DATA = [{'SKU': '43214563',
 'categories': 'electronics,headphones',
 'long_description': 'Monocle ipsum dolor sit amet k-pop smart bespoke, alluring wardrobe espresso Zürich charming Nordic ANA destination elegant bureaux handsome Melbourne. ',
 'name': 'Craniumcandy - Wireless Over-the-Ear Headphones - Crazy Tropical',
 'price': 100,
 'rating': 1,
 'short_description': 'Toto, K-pop sharp the highest quality sleepy boutique joy.'},
 {'SKU': '431553432',
 'name': 'Doodle - Sprite Buds True Wireless In-Ear Headphones - Night Black',
 'short_description': 'Beams the highest quality remarkable Swiss concierge. Cosy signature the best extraordinary.',
 'long_description': 'Discerning airport first-class, elegant conversation artisanal Beams flat white ryokan Helsinki Boeing 787 K-pop concierge soft power iconic. Toto Melbourne pintxos, joy destination global craftsmanship St Moritz smart premium boutique. Boeing 787 premium first-class extraordinary the best Zürich discerning elegant. Charming impeccable emerging sophisticated international Airbus A380 efficient Beams cosy Marylebone Muji Asia-Pacific. Charming uniforms Beams airport, essential Zürich global Nordic extraordinary Boeing 787 iconic vibrant.',
 'price': 180,
 'rating': 5,
 'categories': 'electronics,headphones'},
  {'SKU': '8743153432',
 'name': 'Doodle - Sprite 6 Expert',
 'short_description': 'Beams the highest quality remarkable Swiss concierge. Cosy signature the best extraordinary.',
 'long_description': 'Discerning airport first-class, elegant conversation artisanal Beams flat white ryokan Helsinki Boeing 787 K-pop concierge soft power iconic. Toto Melbourne pintxos, joy destination global craftsmanship St Moritz smart premium boutique. Boeing 787 premium first-class extraordinary the best Zürich discerning elegant. Charming impeccable emerging sophisticated international Airbus A380 efficient Beams cosy Marylebone Muji Asia-Pacific. Charming uniforms Beams airport, essential Zürich global Nordic extraordinary Boeing 787 iconic vibrant.',
 'price': 899,
 'rating': 5,
 'categories': 'cell phone,electronics'},
 {'SKU': '4316647899',
 'name': 'Blues Banjo Songs for Noobs - Gal Nimoy',
 'short_description': 'The best Boeing 787 Lufthansa Toto. Destination Singapore efficient Nordic craftsmanship.',
 'long_description': 'Wardrobe Fast Lane exclusive perfect delightful extraordinary Melbourne K-pop classic Airbus A380 elegant the highest quality. Emerging boutique concierge quality of life finest, punctual elegant delightful pintxos airport tote bag Muji flat white Swiss.',
 'price': 23,
 'rating': 3,
 'categories': 'books,music'},
  {'SKU': '84836424542',
 'name': 'Be Here Now - Richard Alpert',
 'short_description': 'The best Boeing 787 Lufthansa Toto. Destination Singapore efficient Nordic craftsmanship.',
 'long_description': 'Wardrobe Fast Lane exclusive perfect delightful extraordinary Melbourne K-pop classic Airbus A380 elegant the highest quality. Emerging boutique concierge quality of life finest, punctual elegant delightful pintxos airport tote bag Muji flat white Swiss.',
 'price': 42,
 'rating': 3,
 'categories': 'books'}]

def get_suggestions(stem):
    '''
    Get a list of auto complete suggestions from a given stem
    '''
    ac = AutoCompleter(AUTOCOMPLETE_KEY, conn=R)
    return [str(sugg) for sugg in ac.get_suggestions(stem)]

def search_products(name=None, categories=None, price=None, rating=None, fields=None,
                     paging=None, sort_by='name', ascending=True, **kwargs):
    '''
    Search the product catalog
    name - name of the product 
    categories - comma delimited category list (category1,category2)
    price - price range, hyphen delimited (price_low-price_high)
    rating - rating range, hyphen delmited (rating_low-rating_high)
    fields - object fields to return in response
    paging - comma delimited, show item range in this page (paging_start,paging_end)
    sort_by - field to sort by
    ascending - ascending or descending
    '''
    ## for non-numeric search terms, we'll build the term query
    search_terms = []
    if name:
        search_terms.append(f'@name:{name}')
    if categories:
        _categories = categories.split(',')
        search_terms.append(f'@categories:{{{"|".join(_categories)}}}') ## tag search uses {} vs () for compounds

    if search_terms:
        ## join the non-numeric terms together to create the query object
        terms_query = ' '.join(search_terms)
    else:
        ## no non-numeric ones were set, wildcard
        terms_query = '*'

    ## create and configure query object
    query = Query(terms_query)
    query.sort_by(sort_by, asc=ascending)
    if paging is not None:
        query.paging(*paging.split(','))
    if fields is not None:
        query.return_fields(*fields.split(','))

    ## numeric terms and other query parameters
    if price:
        price_low, price_high = price.split('-')
        query.add_filter(NumericFilter('price', price_low, price_high))
    if rating:
        rating_low, rating_high = rating.split('-')
        query.add_filter(NumericFilter('rating', rating_low, rating_high))

    ## execute search
    result = product_index().search(query)
    return [loads(doc.json) for doc in result.docs] # in order to get these all into one json obj, we'll need to transerialze them

def product_index():
    '''
    Get or Create the product search index
    '''
    ## check to see if the client exists, otherwise create it
    client = SearchClient(PRODUCTS_INDEX_KEY, conn=R)
    try:
        client.info()
        return client
    except ResponseError:
        print("index doesn't exist, creating")

    ## Index Defn Base
    definition = IndexDefinition(prefix=[PRODUCTS_KEY.format('')], index_type=IndexType.JSON)

    ## Categories implemented as Tags - allows for more complex searching
    ctg_field = TagField('$.categories', as_name='categories')
    ctg_field_params = list(ctg_field.args)
    ctg_field.args = tuple(ctg_field_params)

    ## actually create the index
    client.create_index((
        TagField("$.SKU", as_name='SKU'),
        TextField("$.name", as_name='name'),
        TextField("$.short_description", as_name='short_description'),
        TextField("$.long_description", as_name='long_description'),
        NumericField("$.price", sortable=True, as_name='price'),
        NumericField("$.rating", sortable=True, as_name='rating'),
        ctg_field),
        definition=definition)

    return client

def add_products():
    '''
    Ingests the sample data into the DB
    '''
    with R.pipeline(transaction=False) as pipeline:
        for product in SAMPLE_DATA:
            key = PRODUCTS_KEY.format(product['SKU'])
            pipeline.jsonset(key, Path.rootPath(), product)
            
            ac = AutoCompleter(AUTOCOMPLETE_KEY, conn=pipeline)
            categories = product['categories'].split(',')
            suggestions = [Suggestion(product['name'])]
            suggestions.extend([Suggestion(category) for category in categories])
            ac.add_suggestions(*suggestions)

        pipeline.execute()

if __name__ == '__main__':
    product_index()
    add_products()
    app.run(debug=True)

```
