---
title: ".NET Vector Search Simplified"
linkTitle: ".NET Vector Search Simplified"
url: "/blog/net-vector-search-simplified/"
description: "Redis OM .NET now supports Redis vector search and integrates with embedding generation APIs using OpenAI, Azure OpenAI, Hugging Face, and ML.NET."
date: 2024-01-24
blogCategories:
- "Tech DE"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 24 January 2024 · updated 27 March 2025*

![Blog tile image](/images/blog/85f1c59ca816219c956389fbd6e7018e6c90cf84-772x550.webp)

## A Walkthrough of Redis OM .NET’s Vector Search and Semantic Caching Capabilities

**Redis OM .NET now supports Redis vector search and integrates with embedding generation APIs using OpenAI, Azure OpenAI, Hugging Face, and ML.NET.**

[Vector database](/solutions/vector-search/) technology is reshaping the way we think about data. Passages of text, images, and audio can all be encoded and indexed as vectors so that they can be searched semantically. We are rapidly moving from a world where the machine-readable semantics of your data are within its content, rather than its structure.

However, [vector databases](/blog/vector-databases-101/) can be unintuitive. You need to know how to properly construct your vector index, how to convert your unstructured data into a usable vector, how to add that data to your data source, and how to construct queries. Effectively, this means creating vector representations from unstructured data and then using those representations to query your stored vectors. So, this isn’t exactly your traditional SELECT/FROM/WHERE.

We released the [Redis OM](/blog/introducing-redis-om-client-libraries/) libraries two years ago to build an intuitive abstraction over Redis’ search and query capabilities. We’re now extending that abstraction to make it easier to perform vector search for your AI-powered applications. Let’s walk through these new enhancements to [Redis OM .NET](https://github.com/redis/redis-om-dotnet) to enable [Redis Vector Search](https://redis.io/docs/interact/search-and-query/advanced-concepts/vectors/).

The latest additions to the Redis OM .NET API make it easier to store and query vector data, even if you’ve never used vectors before. Indeed, Redis OM .NET now includes intuitive interfaces for vector search and semantic caching. Specifically, we’ve built:

1. Redis vector indexing, data modeling, and querying capabilities
1. A set of easy-to-use vectorizers (a.k.a., embedding generators) that integrate with OpenAI, Azure OpenAI, Hugging Face, and the ML.NET framework
1. A semantic caching implementation that works with any vectorizer and reduces expensive LLM calls

All of these bits together collapse what can be a difficult-to-understand and implement process into a couple of simple lines of code.

## Modeling and Index Creation

Let’s say we have a product catalog with a series of items, and we want to be able to look for items with similar stock images or similar product descriptions. We also want to be able to further refine our queries based on a series of facets. Now all we need is this model:

```csharp
[Document(StorageType = StorageType.Json)]
public class Product
{
    [RedisIdField] [Indexed] public int Id { get; set; }

    [Indexed(Algorithm = VectorAlgorithm.HNSW, DistanceMetric = DistanceMetric.COSINE)] 
    [ImageVectorizer]
    public Vector<string> ImageUrl { get; set; }    

    [Indexed(Algorithm = VectorAlgorithm.FLAT, DistanceMetric = DistanceMetric.COSINE)]
    [SentenceVectorizer] 
    public Vector<string> ProductDisplayName { get; set; }
    
    public VectorScores? Scores { get; set; }

    [Indexed] public string Category { get; set; }

    [Indexed] public string ArticleType { get; set; }

    [Indexed] public string BaseColor { get; set; }

    [Indexed] public string Season { get; set; }

    // other facets 
}

```

Once we’ve defined the model, we can create the required index in Redis by invoking the CreateIndex method:

```as3
var provider = new RedisConnectionProvider("redis://localhost:6379");
provider.Connection.CreateIndex(typeof(Product))

```

## Inserting

Now that the index is created, we can go ahead and start inserting items into our Redis database:

```csharp
var collection = provider.RedisCollection<Product>();
var entry = new Product { 
    Id = id, 
    ImageUrl = Vector.Of(imageUrl), 
    ProductDisplayName = Vector.Of(productDisplayName),
    Category = category, 
    ArticleType = articleType, 
    BaseColor = baseColour, 
    Season = season
    // etc…
};
await collection.InsertAsync(entry);

```

Notice from the model that we’ve defined two fields as vectors: ImageUrl and ProductDisplayName. When we go to write an entry, Redis OM will create the vector representations of these fields for you using the supplied vectorizer. In this case, we are using the ImageVectorizer found in the Redis.OM.Vectorizers.ResNet18 package and the sentence Vectorizer found in the Redis.OM.Vectorizers.AllMiniLML6V2 package.

These Vectorizers are implementations of **VectorizerAttribute<T>**. The attributes tell Redis OM which **IVectorizer<T>** to use, as well as the type and shape of the generated vectors. Under the hood, both of these vectorizers use ML.NET to create the vectors. The **VectorizerAttribute<T>** and **IVectorizer<T>** types let you abstract away the logic of creating vectors, making your choice of vectorizer extensible and customizable. Additionally, [Redis OM .NET](/blog/introducing-redis-om-net/) includes vectorizers for straight double and float arrays as well as vectorizers for OpenAI, Azure OpenAI, and Hugging Face. To use OpenAI, Azure OpenAI, or Hugging Face for vector generation, you simply provide an API key and, in some cases, a model ID or resource name.

## Querying

Once we’ve defined our model, created our indexes, and inserted data, we can issue vector queries. To do this, we use the **IRedisColleciton.NearestNeighbors** and **Vector<T>.VectorRange** methods with the Boolean expressions we’d use with any other LINQ query.

### Nearest Neighbors

One nearest neighbor search is supported per query. Whether it’s a k-nearest neighbor or approximate-nearest neighbor is determined by the algorithm you’ve declared in your IndexAttribute in the model. To run a nearest neighbor search, simply call NearestNeighbor on the RedisCollection:

```csharp
var response = collection.NearestNeighbors(x => x.ImageUrl, 15, url).ToList();

```

### Vector Range

To perform a vector range search (filtering vectors within a certain distance of your vector), use the VectorRange method on your vector field within your expression:

```csharp
var item = collection.First(x => x.ImageUrl.VectorRange(url, .15, "distance"));

```

### Hybrid Queries

Hybrid queries combine traditional search filters with vector search. To do this in Redis OM .NET, combine your usual Boolean expressions with a vector range and/or nearest neighbor query. The query below retrieves all apparel products in the fall season, and whose images are within a distance of .15 of the provided image, selecting the nearest neighbor.

```csharp
var item = collection
    .NearestNeighbors(x => x.ImageUrl, 1, url)
    .First(x=>x.ImageUrl.VectorRange(url, .15, "distance") && x.Season == "Fall" && x.Category == "Apparel")

```

In this case, Redis OM .NET figures out how to build the query and then issues it.

## Semantic Caching

Semantic caching is a new caching technique made possible by recent advances in embedding generation and vector search. Traditionally, we think of Redis caching as storing some precise value at some precise key. You need the entire key to recover your cached item. This of course makes a lot of sense when you’re storing something such as a distributed session state or the result of an expensive API call or query.

However, requiring exact key-value matching is a problem when you’re caching prompt/response pairs from an LLM. That’s because semantic caching lets you store and retrieve prompts by meaning (i.e., semantically) rather than just by key/value pairs. This means two related queries like “What is the tallest building in the world?” and “What’s the tallest building in the world?” have meanings close enough that when either question is stored, they both should return the same LLM response.In Redis OM .NET, semantic caching uses the same vectorizers as vector search. To use the semantic cache, you can either initialize a SemanticCache directly or use one of the ones provided by the Redis.OM.Vectorizers package:

```csharp
var provider = new RedisConnectionProvider("redis://localhost:6379");
var cache = provider.OpenAISemanticCache(apiKey, threshold: .15, ttl: 3600000);
cache.Store("What is the capital of France?", "Paris");
var res = cache.GetSimilar("What really is the capital of France?").First();

```

In this case, we are using the OpenAI REST API to build our vector. All that’s needed to make this work is an OpenAI API key. We’ve configured our semantic cache to store the items for an hour. When we retrieve items, we get those whose distance is less than .15 (distances for cosine similarity are normalized between 0 and 1).

## Custom Vector Generation

If Redis OM .NET doesn’t already provide the Vectorizer you need for your project, you can implement your own. You will just need an **IVectorizer<T>** to perform the actual Vectorization, and you will need a **VectorizerAttribute<T>** to decorate your **Vector<T>** fields within your model. The **VectorizerAttribute<T>** is responsible for telling Redis OM .NET how to construct the index and how to create the vectors at insertion or query time.

## Conclusion

Vector databases are proliferating rapidly. With Redis OM .NET, you no longer need to be an expert at transforming your data into vectors to use one. Redis OM .NET’s new vectorizers, vector search, and semantic caching features remove the hassle of building vector indexes, converting your data into vectors, and constructing vector queries. In other words, it’s an intuitive, powerful tool for using Redis’ lighting-fast vector search features more easily.

## Related resources

- The Vector Search Examples are pulled from the Product Catalog Redis OM .NET Demo repo on [GitHub](https://github.com/redis-developer/product-catalog-redis-om-dotnet).
- To learn how to configure the different vectorizers, see [Redis OM .NET’s README](https://github.com/redis/redis-om-dotnet#vectors).
- To learn more about the Redis vector search API, take a look at [the Redis vector docs.](https://redis.io/docs/interact/search-and-query/advanced-concepts/vectors/)
