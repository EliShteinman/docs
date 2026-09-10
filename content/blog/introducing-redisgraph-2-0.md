---
title: "Introducing RedisGraph 2.0"
linkTitle: "Introducing RedisGraph 2.0"
url: "/blog/introducing-redisgraph-2-0/"
description: "Redis is a noSQL database that enables users to store a variety of data in a variety of data structures. We saw a need for our customers to create highly connected data and derive insight by using..."
date: 2020-04-07
blogCategories:
- "Product Releases"
- "Redis Modules"
authors:
- "Pieter Cailliau"
- "Alex Milowski"
lastmod: 2025-07-03
hidden: true
mirrored: true
---

*By Pieter Cailliau, Alex Milowski · Published 7 April 2020 · updated 3 July 2025*

![Blog tile image](/images/site-mirror/e16c4f6d29d0d217f605d83d1f54b42984a860c3-368x260.webp)

Redis is a noSQL database that enables users to store a variety of data in a variety of data structures. We saw a need for our customers to create highly connected data and derive insight by using graph technology. Originally released in 2018, [RedisGraph](/blog/new-redisgraph-1-0-achieves-600x-faster-performance-graph-databases/) is the result of that effort.

RedisGraph is based on a unique approach and architecture that translates the Cypher query language to matrix operations executed over a [GraphBLAS-based engine](http://graphblas.org/). By using sparse matrices to represent graphs and the power of GraphBLAS to process them, RedisGraph delivers a fast and efficient way to manage and process graph data shown to have [significant advantages over other approaches](https://arxiv.org/pdf/1905.01294.pdf) in some applications.

Since the release of version 1.0 of RedisGraph, the project has gathered 1,000 GitHub stars and over 100,000 Docker pulls. During that time we’ve also been hard at work building the next version, and we’re excited to announce RedisGraph 2.0, designed to fulfill the promise of RedisGraph 1.0 in the areas most important to our customers. Graph databases can support a wide range of use cases from [resource management](https://www.youtube.com/watch?v=PTL7aRPFKt8&t=759s) to [health care](https://www.youtube.com/watch?v=6FYYn-9fPXE&list=PL83Wfqi-zYZEEsbS_e6RHP4BYUkbY9e34&index=7). We’ve been working hard to support the queries necessary for a range of applications in resource management, fraud prevention, graph-aided search, and knowledge graphs.

There are too many RedisGraph enhancements since version 1.0 to list them all here. We’ll summarize them via examples of the improvements to our support of Cypher, full-graph response, the integration of [RediSearch](https://oss.redis.com/redisearch/) for full-text search over graphs. We’ll also detail the enhancements to [RedisInsight](/insight/) to support graphs and introduce two RedisGraph partners: [Linkurious](http://linkurio.us/) and [Graphileon](https://graphileon.com/).

To learn more about the significant performance enhancements in RedisGraph 2.0 and get more info on the benchmarking process, check out [RedisGraph 2.0 Performance Benchmarks](/blog/redisgraph-2-0-boosts-performance-up-to-6x).

## Full-text search now included

The release of [RediSearch 1.6](/blog/redisearch-version-1-6-adds-features-improves-performance/) introduced a new low-level API that allows other modules to consume RediSearch for secondary indexing and full-text search purposes. RedisGraph 2.0 is the first generally available module to take full advantage of this capability. Prior to this release, RedisGraph had indexing capabilities via [skiplists](https://en.wikipedia.org/wiki/Skip_list) that was quite performant, but was limited to exact matches and did not allow for prefix or fuzzy matching. Also, there was no way to leverage two separate indexes on a given label as compound indexes.

RedisGraph 2.0 supports full-text search on property values. An index can be created for a specific node and property combination:

CALL db.idx.fulltext.createNodeIndex('Person','name')

and then can be queried via Cypher as shown here:

CALL db.idx.fulltext.queryNodes('Person','Bob')

YIELD node AS p

RETURN p.name

What follows the CALL expression can be a variety of Cypher expressions. The nodes returned can be combined with a match expression to further qualify the search results. Enriching the search results with the connections of a graph is called graph-aided search.

An example of graph-aided search is finding someone who is connected to an individual by a certain number of degrees of separation. A common example of this is the search functionality in LinkedIn, where people who are more closely connected to you are listed towards the top of the search matches.

![](/images/site-mirror/10c86129c7cdbdb8c03712d62ba49ce1c54b04a7-495x235.webp)

The following query demonstrates how this could be implemented:

CALL db.idx.fulltext.queryNodes('Person','%yif%') YIELD node

MATCH p=(node)-[:CONNECTED*1..3]->(:Person {name:'Pieter'})

RETURN p.name, p.title, length(p) AS connectedness

ORDER BY connectedness ASC LIMIT 20

## Full-graph response

Instead of returning only a tabular result of properties values, RedisGraph 2.0 can now return nodes, relations, and other data types. For example, previously you could return only tabular results (e.g., properties values):

MATCH (me:Person)-->(friend:Person)-->(fof:Person)

WHERE me.name='Pieter'

RETURN friend.name, fof.name

![Redis](/images/site-mirror/22588800fe207c10f5e7c72bef08767c96dc1788-1024x404.webp)

With a [full-graph response](https://redis.io/docs/stack/graph/design/result_structure/), you can return nodes and relations directly. For example, the previous query can return the friend, the friend of the friend, and the relationship between them:

MATCH (me:Person)-->(friend:Person)-[f:FRIEND]->(fof:Person)

WHERE me.name='Pieter'

RETURN friend, f, fof

![Redis](/images/site-mirror/939556ee0135a768b1b8699080f40fdd68e4f3e7-1024x487.webp)

This new feature enables such uses like Object Graph Mapping (OGM), querying subgraphs, and visualizations where the receiving application needs all the nodes and their relationships.

To demonstrate the power of this full-graph response, we want to showcase some the integration with RedisInsight and the partnerships with Linkurious and Graphilean enabled by this feature.

**RedisGraph in RedisInsight**

One such application is [RedisInsight](/insight/), where a user can now enter a query and receive a visualization (as shown above). The full-graph response allows RedisInsight to present a visualization and allows the inspection of all the properties of the nodes and edges returned by the query without having to know these properties in advance.

![](/images/site-mirror/ff260eb890f83d62f4946446bc9a732ccdd1f736-1361x619.webp)

[RedisInsight 1.2](https://docs.redis.com/latest/ri/installing/) provides direct support for exploring and querying the graphs stored in Redis. The new support for full-graph response allows RedisInsight to present the query subgraph as a visualization directly to the user. Subsequently, a user can click on nodes and edges in the graph to inspect property values or expand the graph further.

**Linkurious**

Redis has partnered with the French software developer [Linkurious](https://linkurio.us/), which provides an enterprise platform, [Linkurious Enterprise](https://linkurio.us/product/), for fraud, money laundering, and cyber threat protection via graph analytics. Linkurious has developed the [OGMA](https://doc.linkurio.us/ogma/latest/) library that powers the visualizations inside RedisInsight. This library allows users to visually interact with graphs stored in RedisGraph.

In addition, the full-graph response now available in RedisGraph 2.0 allows integration with Linkurious’ graph visualization and analysis platform. We expect even deeper integration in the future.

![](/images/site-mirror/4501f39e8d32f3d50533c684fe639b107972ebba-1024x578.webp)

**In addition, the full-graph response now available in RedisGraph 2.0 allows integration with Linkurious’ graph visualization and analysis platform. We expect even deeper integration in the future.**

**Graphileon**

![](/images/site-mirror/e83dfc4ef6b56e696c4aaf1e0afbfe0ffd8d23fb-1024x294.webp)

On January 27th, 2020, Redis and Dutch software company [Graphileon](https://graphileon.com/) announced a partnership to let RedisGraph users manage their data and build applications in Graphileon’s advanced graphing tools. The combination of RedisGraph and Graphileon enables our customers to enjoy fast and easy data management and to query and analyze the data using the power of the Cypher query language all the while leveraging the specific strengths of RedisGraph.

## Doing more with Cypher

The list of Cypher enhancements added to RedisGraph 2.0 is [really long](https://github.com/RedisGraph/RedisGraph/releases/tag/v2.0.1). Notable additions include a variety of operators and functions, support for simple case statements, enhanced merge support, counting of aggregates, support for naming paths, and reusing entities in pattern matching. There’s no way to explain all the additions in a blog post, so let’s look at an example of Triadic closure to highlight some of the most interesting ones.

The improved support for merges, paths, and operators allows for new support for graph manipulation. We can follow a particular shared relationship between two unrelated nodes to infer a new relationship. For example, if two people know a common person, a social media service might suggest an introduction. Similarly, if two people are managed by the same person, they are peers in the organization. Computing these new relationships are examples of triadic closure.

Consider the two graphs below. The graph on the left shows a “friend” relationship (i.e., who knows whom). The graph on the right shows an organizational structure (i.e., who manages whom). In both graphs, the relationship between the “B” and “C” nodes is not present in the graph.

We can query for suggested introductions in the left-hand graph by following the “KNOWS” relationship:

MATCH (b:Person)-[:KNOWS]->(a:Person)-[:KNOWS]->(c:Person)

WHERE NOT (b)-[:KNOWS]-(c) AND b <> c

RETURN b, c

The query follows the “KNOWS” relationship from node B to node C via A, but qualifies that we want nodes that do not have an existing relationship (or cycles) via the “WHERE NOT” clause.

In the right-hand graph, we can create a peer relationship (via MERGE) by finding a path where we have two co-managed persons without an existing peer relationship:

MATCH (b:Person)<-[:MANAGES]-(a:Person)-[:MANAGES]->(c:Person)

WHERE NOT (b)-[:PEER]-(c) AND b <> c

MERGE (b)-[:PEER]-(c)

We can further qualify the relationship by adding a role and direction to the edge:

MATCH (b:Person)<-[:MANAGES]-(a:Person)-[:MANAGES]->(c:Person)

WHERE NOT (b)-[:PEER]-(c) AND b <> c

WITH b, c,

CASE b.level

WHEN 'Director' THEN 'mentor'

ELSE 'peer'

END AS role

MERGE (b)-[:PEER {role:role}]->(c)

## What’s next for RedisGraph?

Stay tuned to the Redis blog for more detailed examples of new RedisGraph 2.0 features over the next few months. We’re also working on more enhancements to RedisGraph performance, Cypher coverage (such as OPTIONAL MATCH), and adding graph algorithms via the open-source [LAgraph](https://github.com/GraphBLAS/LAGraph) algorithm collection for GraphBLAS in upcoming releases.

RedisGraph 2.0 is available [via Docker](https://oss.redis.com/redisgraph/#give-it-a-try), in [Redis Enterprise Software (RS) 5.4.14](https://docs.redis.com/latest/rs/release-notes/legacy-release-notes/rs-5-4-14-february-2020/), and in [Redis Cloud Pro](/redis-enterprise-cloud/). If you tried RedisGraph 1.0, check out the latest version to see what’s new and improved. If you’re interested in graph databases, consider looking into the power of RedisGraph 2.0. If you’re a Redis user new to graph databases, now would be a good time to find out what RedisGraph could do for your existing applications.
