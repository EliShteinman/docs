---
title: "Redis OM .NET Update"
linkTitle: "Redis OM .NET Update"
url: "/blog/redis-om-net/"
description: "Embedded documents, indexed arrays, and other awesome additions to Redis OM .NET!"
date: 2022-08-04
blogCategories:
- "How To and Tutorials"
- "New Product Announcements"
- "Tech"
authors:
- "Steve Lorello"
lastmod: 2025-03-27
hidden: true
---

*By Steve Lorello, Developer Advocate · Published 4 August 2022 · updated 27 March 2025*

![Blog tile image](/images/blog/3317475c449f3066691f0e8f9e1b2b562c195f99-772x550.webp)

**Embedded documents, indexed arrays, and other awesome additions to Redis OM .NET!**

In November 2021, we released the v0.1.0 version of Redis OM .NET (an object mapping library for Redis). Naturally, as with any early release software, there’s more to be done. Since then, we worked out a few of the library’s quirks. We also added several exciting new features to .NET to get developers productive quickly.

Before we look at what’s new, if you need a general overview of Redis OM, you can check out the announcement post or watch the video below.

[Click here to view video](https://www.youtube.com/embed/DFNKmbGKa5w)

Now, let’s check out the new features added to Redis OM .NET!

### Embedded object indexing and querying

Redis OM .NET now allows you to index the fields in embedded objects within your model. For example, suppose you have a Customer model with an embedded Address model:

```csharp
[Document(StorageType = StorageType.Json)]
public class Customer
{
   [Indexed] public string FirstName { get; set; }
   [Indexed] public string LastName { get; set; }
   public string Email { get; set; }
   public Address Address {get; set;}
}

public class Address
{
    public string StreetName { get; set; }
    public string ZipCode { get; set; }
    public string City { get; set; }
    public string State { get; set; }
    public GeoLoc Location { get; set; }
    public int HouseNumber { get; set; }
}

```

Previously, you would not have been able to index the embedded Address within Customer. Now, Redis OM .NET provides two ways to do this.

### Direct JSON paths

Let’s say you want to share your embedded model between other models and don’t want to over-index fields within the embedded model.

You can leave the embedded model alone and index it from your model using JSON paths relative to the root of your model. To index City and State within the Address of the Customer:

```
[Document(StorageType = StorageType.Json)]
public class Customer
{
   [Indexed] public string FirstName { get; set; }
   [Indexed] public string LastName { get; set; }
   public string Email { get; set; }
   [Indexed(JsonPath = "$.City")]
   [Indexed(JsonPath = "$.State")]
   public Address Address {get; set;}
}

```

### Cascading into the embedded document

Another way to accomplish this is to declare what you want indexed within the Address class, and cascade into it using the IndexedAttribute’s “CascadeDepth” property. So with the following Address Model:

```csharp
[Document(StorageType = StorageType.Json)]
public class Address
{
    public string StreetName { get; set; }
    public string ZipCode { get; set; }
    [Indexed] public string City { get; set; }
    [Indexed] public string State { get; set; }
    [Indexed] public GeoLoc Location { get; set; }
    [Indexed] public int HouseNumber { get; set; }
}

```

You can Index from your customer model like so:

```csharp
[Document(StorageType = StorageType.Json)]
public class Customer
{
   [Indexed] public string FirstName { get; set; }
   [Indexed] public string LastName { get; set; }
   public string Email { get; set; }
   [Indexed(CascadeDepth=1)]
   public Address Address {get; set;}
}

```

CascadeDepth refers to how deep into the object’s graph you want to index. Setting the Cascade depth will cause Redis OM to follow all of IndexedAttribute‘s and SearchableAttribute‘s for fields to index within your model’s object graph.

With one of these two modes followed, when you create the index, the embedded document will be indexed as you would expect, and when you then run LINQ queries like this:

```
customers.Where(c=>c.Address.ZipCode == "10001");

```

… Redis OM knows how to properly build the query based on the provided model.

### Queryable arrays

Another awesome feature we’ve added to Redis OM since v0.1.0 is the ability to index and query arrays of strings within JSON objects. Decorate the array with the IndexedAttribute***.***

```csharp
[Document(StorageType = StorageType.Json, Prefixes = new []{"Person"})]
public class Person
{

    [RedisIdField] [Indexed]public string? Id { get; set; }
    [Indexed] public string[] Skills { get; set; } = Array.Empty<string>();    
    [Indexed] public string? FirstName { get; set; }
    [Indexed] public string? LastName { get; set; }
}

```

With this done, you can query these arrays using the Array’s ***Contains*** method:

```csharp
people.Where(x => x.Skills.Contains(skill));

```

### Indexing enums, ULIDs, GUIDs, and booleans

Redis OM previously only supported the indexing of numerics, strings, and GeoLocs. Since version 0.2.0, you can also index Enums, ULIDs, GUIDs, and Booleans. To do so, use the IndexedAttribute to decorate those fields within your model.

### Aggregating fields not marked as Aggregatable

One pain point for users of aggregations is that not all fields can be marked as or necessarily are marked as aggregatable. As a result, those fields were previously ineligible to be used in Aggregation within Redis OM. NET. With the new Load and LoadAll methods within the AggregationSet in Redis OM, it is now possible to Load the fields not marked as aggregatable.

Let’s take the Customer model we used earlier and add an age field to show how it works.

```csharp
public class Customer
{
    [Indexed] public string FirstName { get; set; }
    [Indexed] public string LastName { get; set; }
    [Indexed] public int Age { get; set; }
    public string Email { get; set; }
    [Indexed(JsonPath = "$.City")]
    [Indexed(JsonPath = "$.State")]
    public Address Address {get; set;}
}

```

Age is indexed, but not marked as aggregatable. Previously, we could not use Age in our aggregation pipeline. If we ran something like this, we’d get an error because Age is not loaded in the pipeline:

```csharp
var aggregations = provider.AggregationSet<Customer>();
await aggregations.Apply(c=>c.RecordShell.Age + 5, "Age_plus_five")
    .ToArrayAsync();

```

Now, in Redis OM .NET, you can call Load on the AggregationSet Loading either a single field or many (by initializing an anonymous object):

```csharp
await aggregations.Load(x=>x.RecordShell.Age)
    .Apply(c=>c.RecordShell.Age + 5, "Age_plus_five")
    .ToArrayAsync();

```

To just load the Age Or:

```csharp
await aggregations.LoadAll
    .Apply(c=>c.RecordShell.Age + 5, "Age_plus_five")
    .Apply(c=>string.Format("My Name is {0}",c.RecordShell.FirstName), "myNameIs")
    .ToArrayAsync();

```

To load multiple fields out of the model, notice the anonymous type.

### New hydration API

Another quirk of aggregations is that they do not return well-formed objects. The reason for this is that the aggregation returns with the result of its pipeline, which is usually exactly what it needed to complete all the operations requested of it, and the results of its operations. That’s fixed now.

With the new Hydration API, you can cobble these bits into a more usable format, allowing you to fully or partially hydrate your model from a RedisAggreagtionResult.

Let’s revisit the examples from the Load section. What if we wanted to bring back our entire customer model along with the results of the apply function? We can do so by calling LoadAll instead of Load. Then we call Hydrate on each RedisAggregationResult, as it is enumerated. Hydrate attempts to bind anything in the AggregationResult to your model. Therefore, may have empty fields that were not present in the result.

```csharp
var collection = new RedisAggregationSet<Person>(_connection);
await foreach (var result in aggregations.LoadAll
    .Apply(c=>c.RecordShell.Age + 5, "Age_plus_five")
    .Apply(c=>string.Format("My Name is {0}",c.RecordShell.FirstName), "myNameIs"))
{
    var person = result.Hydrate(); //now a fully hydrated Person object!
}

```

### Simplified object updates

In previous iterations of Redis OM, if you wanted to update an item, you needed to enumerate it, update it, and then save the whole RedisCollection. This can be burdensome. We added a new API to allow you to easily update the objects you stored in Redis.

```csharp
await collection.UpdateAsync(object);

```

### Easier deletes

Similarly, we made it easier to delete objects you inserted into Redis. To delete objects, execute:

```csharp
await customers.DeleteAsync(object);

```

#### Bring your own ConnectionMultiplexer

One requested feature is a passed ConnectionMultiplexer to initialize the RedisConnectionProvider. This constructor allows you to use whatever multiplexer you are already injecting into your other services with Redis OM.

#### Configurable chunk sizes

Redis OM now supports configurable chunk sizes for automatic pagination under the hood. Previously, a fixed chunk size could have performance implications with huge query results. Small, non-configurable chunk sizes, combined with large result sets, can lead to many round trips that Redis OM has to make to materialize the entire result set. Now, you can pass in the desired chunk size to Redis OM.

```csharp
var customers = provider.RedisCollection<Customer>(10000);

```

Note that this is subject to the MAXSEARCHRESULT configuration parameter in RediSearch.

### Wrapping up

We’ve been up to quite a lot over the past few months, with many exciting new features added to Redis OM .NET and the inevitable bug-bashing that comes with any piece of software. You can keep an eye out for new features by watching the GitHub Repository. If there are features that you are interested in seeing in the library, please open an issue on GitHub.

#### Resources

- A skeleton application demonstrating how to integrate Redis OM .NET into your ASP.NET Core Applications is available on GitHub.
- A tutorial on the Redis Developer site gives some gritty details of how to use Redis OM .NET.
- The reference docs for Redis OM .NET are available on the repository’s github-pages site.
- If you have any questions about the library, open an issue on GitHub or contact us on the Redis Discord Server
