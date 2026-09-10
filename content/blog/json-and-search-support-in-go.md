---
title: "JSON and search support in Go"
linkTitle: "JSON and search support in Go"
url: "/blog/json-and-search-support-in-go/"
description: "You can now explore advanced data modeling, with support for secondary indexing, JSON documents, and the ability to search your data with the go-redis client library."
date: 2024-11-12
blogCategories:
- "Uncategorized"
authors:
- "Mirko Ortensi"
lastmod: 2026-05-26
hidden: true
mirrored: true
---

*By Mirko Ortensi, Sr. Product Manager, Products · Published 12 November 2024 · updated 26 May 2026*

![Blog tile image](/images/site-mirror/e305e79e49035a8237a6e0f7dc9735040feb5098-772x552.webp)

You can now explore advanced data modeling, with support for secondary indexing, JSON documents, and the ability to search your data with the go-redis client library.

With the latest addition, go-redis is getting closer to supporting all the capabilities offered by Redis Community Edition (Redis Stack and [Redis 8](/blog/redis-8-0-m01-released-one-redis-for-every-use-case/)), Redis Software, and Redis Cloud. JSON data modeling does not need many presentations: the most popular exchange format, supported by all Redis versions, allows for flexible data management to resolve many of the modern problems of storing hierarchical data in the database. However, only with the search features can you get the most out of your data. The Redis query engine supports indexing hash and JSON documents and simplifies the retrieval of any single piece of data.

Let’s look at some examples of recent additions. To test the samples proposed in this post, create a [free Redis Cloud account](https://redis.io/try-free/) on AWS, GCP, or Azure. If you’d rather run Redis on your laptop, look at Redis 8 (the M02 milestone is available) on [Docker Hub](https://hub.docker.com/_/redis), or install Redis Stack using the preferred [installation method](https://redis.io/docs/latest/operate/oss_and_stack/install/install-stack/).

# JSON support

Create a connection to Redis as usual (connect with the credentials from your Redis Cloud account. Docker images have an empty default password).

```javascript
client := redis.NewClient(&redis.Options{
    	Addr: 	"localhost:6379",
    	Password: "",
    	Protocol: 2,
})

```

Try to create simple JSON documents and execute standard commands as follows:

```javascript
client.JSONSet(ctx, "greeting", "$", `{"hello": "world"}`)
greeting := client.JSONGet(ctx, "greeting", "$.hello")
fmt.Println(greeting.Val())
// Output: ["world"]

expandedJSON, e := greeting.Expanded()
if e != nil {
	panic(e)
}
fmt.Println(expandedJSON.([]interface{})[0])
// Output: world

client.JSONSet(ctx, "data", "$", `{"a": 10, "b": {"a": [12, 13, 17, 23, 55]}}`)
res := client.JSONGet(ctx, "data", "$.b.a[0]")
fmt.Println(res.Val())
// Output: [12]


```

Let’s try something advanced. Imagine you’d like to model a shopping cart as a JSON document:


```javascript
{
	"lastAccessedTime": 1673354843,
	"creationTime": 1673354843,
	"cart":[
    	{
        	"id": "hp-printer",
        	"price": 59.90,
        	"quantity": 1
    	},
    	{
        	"id":" MacBook",
        	"price": 2990.99,
        	"quantity": 1
    	}
	],
	"location": "13.456260,43.300751",
	"visited": ["www.redis.io"]
}

```

You can create the document with the following command:

```javascript
session := `{"lastAccessedTime":1673354843, "creationTime":1673354843, "cart":[{"id":"hp-printer","price":59.90,"quantity":1}, {"id":"MacBook","price":2990.99,"quantity":1}], "location":"13.456260,43.300751", "visited":["www.redis.io"]}`

client.JSONSet(ctx, "session:3rf2iu23fu", "$", session)



```

Apart from reading or writing different items in your shopping cart selectively, you can search within the cart using the [JSONPath syntax](https://redis.io/docs/latest/develop/data-types/json/path/). So, if you want to check what items are cheaper than 2500 dollars in your cart, the solution is served:

```javascript
res = client.JSONGet(ctx, "session:3rf2iu23fu", "$.cart[?(@.price<2500)].id")
fmt.Println(res.Val())
// Output: ["hp-printer"]

```

The ability to model your data using the JSON format evolves the simple yet efficient hash data structure. Only the JSON format supports hierarchical data and internal search with JSONPath. But things get even more interesting because you can search across different JSON documents.

# Secondary indexing support

The go-redis client library now supports all the features in the [Redis query engine](https://redis.io/docs/latest/develop/interact/search-and-query/). Back to our shopping cart example, if you want to check what carts contain a specific item or maybe refine the search further to include the desired criteria, this is possible using the API available in go-redis. Consider the following example, where we’ll create an index.

```javascript
// Clean up the index
client.FTDropIndexWithArgs(ctx, "json_session_idx", &redis.FTDropIndexOptions{DeleteDocs: true})

// Fields definition
id_idx := &redis.FieldSchema{FieldName: "$.cart[*].id", FieldType: redis.SearchFieldTypeTag, As: "id"}
loc_idx := &redis.FieldSchema{FieldName: "$.location", FieldType: redis.SearchFieldTypeGeo, As: "location"}
price_idx := &redis.FieldSchema{FieldName: "$.cart[*].price", FieldType: redis.SearchFieldTypeNumeric, As: "price"}

// Create the index
client.FTCreate(ctx, "json_session_idx",
	&redis.FTCreateOptions{OnJSON: true, Prefix: []interface{}{"session:"}}, id_idx, loc_idx, price_idx).Result()

```

The previous code does the following.

1. It cleans up an eventual index named json_session_idx together with the data indexed
1. It defines what data in the cart is required to be indexed. The specified fields are:
  1. All the items’ product IDs, for which we require an [exact match](https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/query_syntax/#tag-filters) using the [TAG field index](https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/tags/)
  1. The locations of the users, expressed by the pairs (longitude, latitude), for which we require the [GEO geographical indexing](https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/query_syntax/#geo-filters)
  1. We require a numeric search provided by the [NUMERIC field type](https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/query_syntax/#numeric-filters-in-query) for the price of the items in the cart.
1. It creates the index, specifying that JSON documents prefixed by “session:” should be indexed.

Once the index is created, all the existing and new documents in the database will be added. Index creation is asynchronous, but indexing happens synchronously whenever a new document is added. If you create a new index over an existing dataset, indexing will take instants. Now, let’s add a couple of sessions.

```javascript
session := `{"lastAccessedTime":1673354843, "creationTime":1673354843, "cart":[{"id":"hp-printer","price":59.90,"quantity":1}, {"id":"MacBook","price":2990.99,"quantity":1}], "location":"13.456260,43.300751", "visited":["www.redis.io"]}`

session_2 := `{"lastAccessedTime":1705182581, "creationTime":1705182581, "cart":[{"id":"hp-printer","price":59.90,"quantity":1}], "location":"-94.582306,39.082520", "visited":["www.redis.io"]}`

// Add the documents to the index
client.JSONSet(ctx, "session:3rf2iu23fu", "$", session)
client.JSONSet(ctx, "session:2fh2p9349h", "$", session_2)

```

The first example is an exact match operation that retrieves how many sessions contain a specific item in the cart.

```javascript
// Search for sessions with a cart that contains an item with id "hp-printer"
result := client.FTSearchWithArgs(ctx, "json_session_idx", "@id:{hp\\-printer}", &redis.FTSearchOptions{NoContent: true})
fmt.Println(result.Val().Total)
// Output: 2

```

Now, we will put together multiple criteria to search for the price. The following command returns the prices of those items that are present in all the sessions:

- Have the product ID equal to “hp-printer”
- Are in the range of 60km from a specified location
- Are more expensive than 50 dollars

```javascript
result = client.FTSearchWithArgs(ctx, "json_session_idx", "@id:{hp\\-printer} @location:[$lon $lat $radius $units] @price:[50 +inf]", &redis.FTSearchOptions{Return: []redis.FTSearchReturn{{FieldName: "price"}, {FieldName: "__v_score"}}, Params: map[string]interface{}{"lon": "13.482410", "lat": "43.486019", "radius": 60, "units": "km"}, DialectVersion: 2})

for _, doc := range result.Val().Docs {
	fmt.Println(doc.Fields["price"])
}
// Output: 59.9

```

The [query syntax documentation](https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/query_syntax/) explains the query syntax to be used. Searching our Redis documents is indeed powerful, but things become even more interesting when we introduce semantic search in our application.

# Vector search support

The go-redis client fully supports [vector search](https://redis.io/docs/latest/develop/get-started/vector-database/), which enables semantic search, one of the building blocks of [Redis for AI](https://redis.io/redis-for-ai/), the integrated package for developing GenAI applications. Let’s explore the functionality with a simple example: We will store three sentences and test which sentence in the database is the most semantically similar to a query sentence. Vector search is supported for hash and JSON documents; in this example, we’ll model our sentences once more as JSON documents.

```javascript
doc_1 := "This is a technical document, it describes the SID sound chip of the Commodore 64"
doc_2 := "The Little Prince is a short story by Antoine de Saint-Exupéry, the best known of his literary productions, published on April 6, 1943 in New York"
doc_3 := "Pasta alla carbonara is a characteristic dish of Lazio and more particularly of Rome, prepared with popular ingredients and with an intense flavour."

q := "The Adventures of Pinocchio is a fantasy novel for children written by Carlo Collodi, pseudonym of the journalist and writer Carlo Lorenzini, published for the first time in Florence in February 1883."

```

Once we have defined our dataset and the query sentence, let’s create the index.

```javascript
client.FTDropIndexWithArgs(ctx, "json_doc_idx", &redis.FTDropIndexOptions{DeleteDocs: true})

hnswOptions := &redis.FTHNSWOptions{Type: "FLOAT64", Dim: 1536, DistanceMetric: "COSINE"}

client.FTCreate(ctx, "json_doc_idx",
    	&redis.FTCreateOptions{OnJSON: true, Prefix: []interface{}{"json:doc:"}},
    	&redis.FieldSchema{FieldName: "$.v", FieldType: redis.SearchFieldTypeVector, As: "v", VectorArgs: &redis.FTVectorArgs{HNSWOptions: hnswOptions}}).Result()


```

The former code cleans up the index and the indexed documents; then, it creates an index for vectors with the following features.

- Vectors are floats of 64 bytes.
- Vectors contain 1536 elements, determined by the embedding model we’ll introduce shortly.
- The distance metric is cosine
- The indexing method is of type [HNSW](https://redis.io/docs/latest/develop/interact/search-and-query/basic-constructs/field-and-type-options/#vector-fields)
- We are indexing JSON documents prefixed by “json:doc:”
- The vector is stored in the JSON document at “$.v”

We will create the vector embedding representation to create the database documents. To achieve this, we resort to [OpenAI embedding models](https://platform.openai.com/docs/guides/embeddings/embedding-models). This helper function transforms a sentence into an array of 1536 float64 elements. The chosen OpenAI embedding model is text-embedding-ada-002.

```javascript
func createEmbedding(ctx context.Context, text string) []float64 {
	// Set OPENAI_API_KEY environment variable
	client := openai.NewClient()

	// Using text-embedding-ada-002 model
	params := openai.EmbeddingNewParams{
    	Input:      	openai.F[openai.EmbeddingNewParamsInputUnion](shared.UnionString(text)),
    	Model:      	openai.F(openai.EmbeddingModelTextEmbeddingAda002),
    	EncodingFormat: openai.F(openai.EmbeddingNewParamsEncodingFormatFloat),
	}

	response, err := client.Embeddings.New(ctx, params)
	if err != nil {
    	return nil
	}

	return response.Data[0].Embedding
}

```

Note that you can install the official [Go library for the OpenAI library](https://github.com/openai/openai-go) as follows:

```javascript
go get github.com/openai/openai-go

```

We can now store our sentences with their semantic representation in the database.

```
client.JSONSet(ctx, "json:doc:1", "$", map[string]interface{}{"v": createEmbedding(ctx, doc_1), "content": doc_1})
client.JSONSet(ctx, "json:doc:2", "$", map[string]interface{}{"v": createEmbedding(ctx, doc_2), "content": doc_2})
client.JSONSet(ctx, "json:doc:3", "$", map[string]interface{}{"v": createEmbedding(ctx, doc_3), "content": doc_3})

```

We are ready to search for sentences similar to the query sentence!

```javascript
searchOptionsJSON := &redis.FTSearchOptions{
	Return:     	[]redis.FTSearchReturn{{FieldName: "$.content"}, {FieldName: "__v_score"}},
	SortBy:     	[]redis.FTSearchSortBy{{FieldName: "__v_score", Asc: true}},
	DialectVersion: 2,
	Params:     	map[string]interface{}{"vec": convertFloatsToString(createEmbedding(ctx, q))},
}

result := client.FTSearchWithArgs(ctx, "json_doc_idx", "*=>[KNN 1 @v $vec]", searchOptionsJSON)

// RESP2
for _, doc := range result.Val().Docs {
	fmt.Println(doc.Fields["$.content"])
}
// Output: The Little Prince is a short story by Antoine de Saint-Exupéry, the best known of his literary productions, published on April 6, 1943 in New York

```

As expected, the query sentence (about the “Adventures of Pinocchio”) is more semantically similar to “The Little Prince” rather than the rest of the documents.

# One Redis for every use case

You can test the examples in this article using a [free Redis Cloud database](https://redis.io/try-free/) or the [Redis 8 M02 Docker image](https://hub.docker.com/_/redis/tags) available from Docker Hub. In addition:

- Refer to the [Go guide page](https://redis.io/docs/latest/develop/connect/clients/go/) to learn more about the go-redis client library
- Find additional examples from the [GitHub repository](https://github.com/redis/go-redis)
- Visualize your data, profile the execution of queries, or ask the Copilot all your questions about Redis or your data. Copilot can help you build queries starting from the data in your database with AI. [Download Redis Insight](https://redis.io/insight/); it’s free.

What are you going to build with Redis?
