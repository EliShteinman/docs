---
title: "What’s New in Redis OM Spring?"
linkTitle: "What’s New in Redis OM Spring?"
url: "/blog/redis-om-spring/"
description: "The Redis OM projects are progressing nicely. After six months of hard work, the team has created a usable and stable set of APIs for Redis Stack. We expect these 10 new features in Redis OM Spring..."
date: 2022-08-12
blogCategories:
- "Product Releases"
authors:
- "Brian Sam-Bodden"
lastmod: 2025-03-27
hidden: true
---

*By Brian Sam-Bodden, Principal Applied AI Engineer · Published 12 August 2022 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/25899604c3197b0843e26d3b4c8fa453aaf4b882-772x550.webp)

**The Redis OM projects are progressing nicely. After six months of hard work, the team has created a usable and stable set of APIs for Redis Stack. We expect these 10 new features in Redis OM Spring to simplify and optimize Redis-powered Spring applications.**

The release of [Redis Stack](https://redis.io/docs/stack/) in [March 2022](/blog/introducing-redis-stack/) marked a watershed moment in Redis distribution. Redis Stack is the first publicly available Redis distribution that integrates several popular and battle-tested Redis modules. Redis Stack packages a JSON document database, a full-blown search engine, a time-series database, a graph database, and [probabilistic data structures](/blog/streaming-analytics-with-probabilistic-data-structures/).

## Redis OM

The Redis object mapping (OM) family of libraries started life as an effort to provide high-level APIs to several of Redis’ supported modules. With the release of Redis Stack, our efforts have been refocused on the modules and functionality provided by Stack. The first wave of functionality is centered around the JSON document database (RedisJSON) and its integration with the search engine (RediSearch).

## The latest features in Redis OM Spring

As you probably know, [Redis OM Spring is a client library](https://github.com/redis/redis-om-spring) that helps you model your domain and persist data to Redis in Spring applications. The latest release of ROMS (version 0.6.0) reflects our focus on Documents and Search (although we sneaked in a few other features in preview form).

So what’s new since [we announced the project in late 2021](/blog/introducing-redis-om-spring/) and published a [Redis OM Spring tutorial](https://redis.io/docs/stack/get-started/tutorials/stack-spring/)? Here are the highlights.

### Nested object mapping

Redis OM Spring, as an extension to Spring Data Redis, is centered around working with “persistent entities:” Java objects annotated so that they can be serialized and stored in a data store. Redis OM Spring is one of the first Spring data projects to offer multi-model persistence of Java entities, such as Redis Hashes and Redis JSON Documents. In the GA release, you can now mark nested objects with @Indexed and search based on the nested object properties:

```java
@Document
public class Person {
  @Id private String id;
  //...
  @Indexed @NonNull private Address address;
}

```

With such mapping, you could, for example, declare a method in a repository to search for a Person given the City in their Address:

```java
// Performing a tag search on city
Iterable<Person> findByAddress_City(String city);

```

Or, if you wanted to search by City and State, you could declare a method like:

```java
// Performing a full-search on street
Iterable<Person> findByAddress_CityAndAddress_State(String city, String state);

```

### “Catch-All” search method

If you have any full-text search methods in an entity, you can search over *all* the fields at once, simply by declaring a method called “search“:

```java
 // Performing a text search on all text fields:
 Iterable<Person> search(String text);

```

### Finer control over text indices

The Indexed and Searchable annotations provide full control on the generation of the underlying search index:

```java
 @Searchable(sortable = true, nostem = true, weight = 20.0)
 private String buildingType;

```

The ability to pass fine-tuning parameters to the underlying RediSearch engine opens the possibility for more powerful queries. In the example, the definition of the buildingType field includes the sortable, nostem, and weight parameters. The sortable parameter speeds up sorting by the specific field at the cost of some extra memory; the nostem parameter can speed up indexing by disabling the stemming of the field; and finally, the weight parameter is a multiplier that affects the importance of the field when calculating result accuracy.

### Custom GSON transformers integration

Several utility classes were added to control how objects are serialized. For example, say you wanted to store a Set of Strings as a comma-delimited string in your JSON document. You would use the @JsonAdapter GSON annotation with the Redis OM SetToStringAdapter class:

```java
 @Indexed(separator = ",")
 @JsonAdapter(SetToStringAdapter.class)
 private Set<String> workType;

```

### Sorting and pagination queries

On top of the CrudRepository, a PagingAndSortingRepository abstraction adds additional methods to ease paginated access to entities. The RedisDocumentRepository implements this interface and allows the passing of a Pageable object to any declared method to return “pages” of results. The findAllByTitleStartingWith method retrieves all instances of the MyDoc entity with a title starting with a given prefix:

```java
Page<MyDoc> findAllByTitleStartingWith(String prefix, Pageable pageable);

```

Such a query could return millions of results. In a typical web application, we might prefer to show a page with a few hundred results at most. Now, using a page request, we can ask only to return the first page of results containing 100 records:

```java
Pageable pageRequest = PageRequest.of(0, 100);
Page<MyDoc> result = repository.findAllByTitleStartingWith("hel", pageRequest);

```

### Retrieve entity IDs paginated

Applications often need to get a list of IDs of one sort or another: user IDs, customer numbers, and so on. Redis OM Spring RedisDocumentRepository provides a built-in getIds method that takes a page object to retrieve IDs for an entity efficiently:

```java
Pageable pageRequest = PageRequest.of(0, 1);
Page<String> ids = repository.getIds(pageRequest);
ids = repository.getIds(pageRequest.next());

```

### Update a single JSON field without retrieving the whole document

In real applications, JSON documents can become very large. Retrieving a whole document can become an expensive and time-consuming operation.

Imagine that you’ve saved an object using the RedisDocumentRepository. You can now update a single field efficiently using the updateField method and Entity Metamodel class:

```java
Company redisInc = repository.save( //
   Company.of(
     "RedisInc", 
     2011, 
     new Point(-122.066540, 37.377690), 
     "stack@redis.com"
   )
 );
 repository.updateField(redisInc, Company$.NAME, "Redis");

```

### Audit fields

Redis OM Spring provides sophisticated support to transparently keep track of when a change happens to an entity. You must equip your entity classes with auditing metadata to benefit from that functionality. You can define them using the annotations @CreatedAt; to store when the entity was created and @LastModifiedDate; to store when the entity was last changed:

```java
 @CreatedDate
 private Date createdDate;
 @LastModifiedDate
 private Date lastModifiedDate;

```

### Retrieve all distinct collection values

If you have an indexed collection in your entity, such as

```java
 @Indexed
 private Set<String> colors = new HashSet<String>();

```

You can declare a method in your repository like

```java
Iterable<String> getAllColors();

```

That efficiently returns all distinct values in that collection across all documents.

### Autocomplete

RediSearch provides a Suggestions/Autocomplete API. This API is surfaced in Redis OM Spring via the @AutoComplete and @AutoCompletePayload annotations.

For example, imagine you have an entity representing Airports with the airport name, code, and state:

```java
@Document
 public class Airport {
   @Id 
   private String id;

   @AutoComplete
   private String name;

   @AutoCompletePayload("name")
   private String code;

   @AutoCompletePayload("name")
   private String state;
}

```

You can declare methods that start with "autoComplete*”, as shown below for the “name” property:

```java
public interface AirportsRepository extends RedisDocumentRepository<Airport, String> {
 List<Suggestion> autoCompleteName(String query);
 List<Suggestion> autoCompleteName(String query, AutoCompleteOptions options);
}

```

And get a list of suggestions/autocompletions given a query string:

```java
@Test
 public void testGetAutocompleteSuggestions() {
   List<Suggestion> suggestions = repository.autoCompleteName("col");
   List<String> suggestionsString = suggestions.stream().map(Suggestion::getString).collect(Collectors.toList());
   assertThat(suggestionsString).containsAll(List.of("Columbia", "Columbus", "Colorado Springs"));
}

```

Also, if you pass an “AutoCompleteOptions” you can control how the search is performed (fuzzy or not) and also include in the payload any of the fields marked with the @AutoCompletePayload annotation:

```java
@Test
 public void testGetAutocompleteSuggestionsWithPayload() {
   String columbusPayload = "{\"code\":\"CMH\",\"state\":\"OH\"}";
   String columbiaPayload = "{\"code\":\"CAE\",\"state\":\"SC\"}";
   String coloradoSpringsPayload = "{\"code\":\"COS\",\"state\":\"CO\"}";

   List<Suggestion> suggestions = repository.autoCompleteName("col", AutoCompleteOptions.get().withPayload());

   List<String> suggestionsString = suggestions.stream().map(Suggestion::getString).collect(Collectors.toList());

   List<Object> payloads = suggestions.stream().map(Suggestion::getPayload).collect(Collectors.toList());

   assertThat(suggestionsString) //
     .containsAll(List.of("Columbia", "Columbus", "Colorado Springs"));

   assertThat(payloads) //
     .containsAll( //
       List.of(columbusPayload,columbiaPayload,coloradoSpringsPayload)
   );
 }

```

### Bloom filters

One powerful feature of Redis Stack is the RedisBloom module which provides a collection of probabilistic data structures. A Bloom filter is a probabilistic data structure that provides an efficient way to verify that an entry is certainly not in a set. This feature is ideal when you search for items on expensive-to-access resources and is particularly useful if you have extremely large data collections.

Imagine that you had a list of users for your SaS application, and you reached FAANG levels of users, say a little more than 100 million. (Congratulations!) In your early days, it was easy to check if an email address was already used in the system since you only had to query a dataset of thousands and not several hundred million. But that’s changed.

The RedisBloom feature makes this process easier. Use the @Bloom annotation to create and maintain a Bloom filter for the email property:

```java
 @Bloom(name = "bf_person_email", capacity = 100000, errorRate = 0.001)
 String email;

```

With the filter in place, add an “existence” query to the repository:

```java
 boolean existsByEmail(String email);

```

The query runs in linear time, ensuring a consistent and responsive UI for your customers.

## Where we’re headed

This is the beginning of a journey as we work to make Redis Stack useful and enjoyable for developers across multiple languages and platforms. This release will remain fairly stable on the JSON/Search front; we expect minor changes to the current APIs. We have begun working on the remaining modules and APIs and are excited about what comes next.
