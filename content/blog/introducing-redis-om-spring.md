---
title: "Introducing Redis OM Spring"
linkTitle: "Introducing Redis OM Spring"
url: "/blog/introducing-redis-om-spring/"
description: "Redis OM Spring is a new client library designed to help you model your domain and persist data to Redis in your Spring applications. The library works with open source Redis but provides many..."
date: 2021-12-08
blogCategories:
- "How To and Tutorials"
- "New Product Announcements"
- "Tech"
authors:
- "Brian Sam-Bodden"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Brian Sam-Bodden, Principal Applied AI Engineer · Published 8 December 2021 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/25899604c3197b0843e26d3b4c8fa453aaf4b882-772x550.webp)

## Object Mapping, and more, for Redis and Spring

[Redis OM Spring](https://github.com/redis/redis-om-spring) is a new client library designed to help you model your domain and persist data to Redis in your Spring applications. The library works with open source Redis but provides many additional indexing and querying capabilities when used with [RedisJSON](https://oss.redis.com/redisjson/).

Redis, combined with its modules, makes for one of the fastest data platforms on the planet. But it hasn’t always been easy to take advantage of its speed. Redis OM Spring provides a compelling developer experience, and in this post I’m going to show you what you can build with it.

## Motivation

It’s rare, as a developer, to stumble upon a technology that’s both powerful and simple. With OSS Redis alone, you have a host of data structures and associated commands to perform many of the data-oriented and messaging tasks needed by enterprise applications.

Similarly, in the world of enterprise Java development, Spring has, over the last 18 years, tamed the complexity of building large, feature-rich applications. In this space, Redis has been supported by the amazing [Spring Data Redis](https://spring.io/projects/spring-data-redis), which provides both low-level and high-level abstractions for interacting with OSS Redis.

One of the challenges in using Spring Data Redis is that it doesn’t support the Redis modules. Here at Redis, we develop [several game-changing Redis modules](/redis-enterprise/modules/) that enrich the Redis core data structures with search, JSON indexing and querying, graph data, time series data, and a complete framework for server-side computation (Redis Gears). We built [Redis OM Spring](https://github.com/redis/redis-om-spring) to take advantage of these modules and provide an even broader set of capabilities.

## Redis OM Spring

The Redis OM family of client libraries aims to provide high-level abstractions idiomatically implemented for your language/platform of choice. We currently cater to the Node.js, Python, .NET, and Spring communities. Redis OM Spring lets developers easily add the power of Redis to their Spring Boot applications.

Specifically, Redis OM Spring provides a robust repository and custom object-mapping abstractions built on the amazing Spring Data Redis (SDR) framework.

The current preview release provides all of the Spring Data Redis capabilities, plus:

- Java to JSON mapping
- Enhanced Hash mappings
- Automatic search index generation
- Spring Data Repositories backed by RediSearch

#### Java to JSON Mapping

To map Java objects to JSON documents stored in Redis using RedisJSON, you can use the @Document annotation. Like any other Spring Data entity mapping annotation, you add it to the class declaration. For example, imagine you want to map objects of type Company. Simply add @Document as shown below:

```python
package com.yourcompany.domain;

@Document
public class Company {
  @Id private String id;
  @Searchable private String name;
  @Indexed private Point location;
  @Indexed private Set<String> tags = new HashSet<String>();
  @Indexed private Integer numberOfEmployees;
  @Indexed private Integer yearFounded;
  private String url;
  private boolean publiclyListed;

  // ...
}

```

You might notice that the body of this class has several annotations. @Id comes from Spring Data, and it declares the id property as the Redis key that will store our JSON document.

Arguably the most popular feature of the Spring Data family of libraries is declarative Data Repositories. The next two annotations let you use RediSearch to index JSON documents. This is exposed via the RedisDocumentRepository interface:

```python
package com.yourcompany.repositories;

import com.yourcompany.domain.Company;
import com.redis.om.spring.repository.RedisDocumentRepository;

public interface CompanyRepository extends RedisDocumentRepository<Company, String> {
}

```

The empty repository declaration is all you need to get basic CRUD functionality/pagination and sorting for your POJOs.

Redis OM Spring uses the POJO fields annotated with @Indexed or @Searchable to build the index schema. In the case of the Company POJO, we have a name property annotated as “searchable”, which means we get full-text search capabilities over that field. This is reflected in the schema field definition $.name AS name TEXT.

On the other hand, the field tags is annotated as “indexable,” which means we get an index field of type TAG, meaning that we can search for Companies by the exact value of the field. This is, again, reflected in the schema field definition: $.tags[*] AS tags TAG

### Create Simple Dynamic Queries

Perhaps the most compelling feature of Redis OM Spring is its ability to create repository implementations automatically, at runtime, from a repository interface. With the proper fields being indexed, you can now fulfill all of the queries below without having to write any additional code:

```python
package com.yourcompany.repositories;

import java.util.*;

import org.springframework.data.geo.Distance;
import org.springframework.data.geo.Point;
import org.springframework.data.repository.query.Param;

import com.yourcompany.domain.Company;
import com.redis.om.spring.annotations.Query;
import com.redis.om.spring.repository.RedisDocumentRepository;

public interface CompanyRepository extends RedisDocumentRepository<Company, String> {
  // find one by property
  Optional<Company> findOneByName(String name);

  // geospatial query
  Iterable<Company> findByLocationNear(Point point, Distance distance);

  // find by tag field, using JRediSearch "native" annotation
  @Query("@tags:{$tags}")
  Iterable<Company> findByTags(@Param("tags") Set<String> tags);

  // find by numeric property
  Iterable<Company> findByNumberOfEmployees(int noe);

  // find by numeric property range
  Iterable<Company> findByNumberOfEmployeesBetween(int noeGT, int noeLT);

  // starting with/ending with
  Iterable<Company> findByNameStartingWith(String prefix);
}

```

The repository proxy has two ways to derive a store-specific query from the method name:

- By deriving the query from the method name directly.
- By using a manually defined query using the @Query or @Aggregation annotations.

Let’s examine a couple of the method declarations added to the repository interface.

#### findOneByName

Redis OM Spring uses the method name and parameters to generate the appropriate query. It uses the method return type to determine how to package and return the result.

findOneByName returns an Optional of Company. findOne also implies that only one result will be returned, even if there are multiple results. The library parses the method name to determine the number of expected parameters. For example, the ByName portion of the method tells us we expect a single parameter named name.

#### findByLocationNear

Redis OM Spring supports the GeoJSON types to store geospatial data. By using the near keyword in our queries, we’re telling our code to expect a Point (org.springframework.data.geo.Point) and a Distance (org.springframework.data.geo.Distance) type as parameters.

#### Using the Repository

As with other Spring Data Repositories, you can inject a repository into another Spring component:

```python
@RestController
@RequestMapping("/api/companies")
public class CompanyController {
  @Autowired
  CompanyRepository repository;

  @GetMapping("name/{name}")
  Optional<Company> byName(@PathVariable("name") String name) {
    return repository.findOneByName(name);
  }
}

```

### Wrapping Up

This is just a **preview** release of [Redis OM Spring](https://github.com/redis/redis-om-spring). There’s still much more to build, but for now we need your help! You can check out the [README](https://github.com/redis/redis-om-spring#readme) for details on how to install the project in your Spring application. We welcome your feedback, PRs, and issues!
