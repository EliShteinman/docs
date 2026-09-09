---
title: "On the release of RedisGraph v1.0 Preview"
linkTitle: "On the release of RedisGraph v1.0 Preview"
url: "/blog/release-redisgraph-v1-0-preview/"
description: "TLDR: We’ve been developing a graph database that transforms queries into linear algebra problems, and the result is an architecture that can perform many standard operations on millions of..."
date: 2018-07-31
blogCategories:
- "Benchmarks"
- "New Product Announcements"
- "Product Releases"
- "Redis Modules"
authors:
- "Jeffrey Lovitz"
lastmod: 2025-03-04
hidden: true
---

*By Jeffrey Lovitz, Programmer · Published 31 July 2018 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

*TLDR: We’ve been developing a graph database that transforms queries into linear algebra problems, and the result is an architecture that can perform many standard operations on millions of elements in sub-second time.*

Nearly two years after starting development, we reached a major milestone with the release of RedisGraph v1.0 today. RedisGraph is a graph database architecture implemented as a [Redis module](/community/redis-modules-hub/), using GraphBLAS sparse matrices for internal data representation and linear algebra for query execution. It is implemented purely in C, and has been tested on Linux and OS X distros. We are using Cypher as our query language, and look forward to working toward GQL with the graph database community!

In this blog, we’ll provide a quick overview of how RedisGraph uses matrix representations to solve traditional graphing problems, share some performance benchmarks, and discuss some next steps toward making our architecture as efficient and versatile as possible.

### Matrix representations of graphs

#### Building for speed and sparsity

Matrices are a classic encoding format for graph data, starting with the pleasantly intuitive adjacency matrix: a square table with all nodes along each axis, and a value for each connected pair. Naively implemented, this approach scales terribly for graphs that model real-world problems, which tend to be very sparse. Space and time complexity for a matrix are governed by its dimensions (**O*****(n²)*** for square matrices), making alternatives like adjacency lists more appealing for most practical applications with scaling requirements.

#### Enter GraphBLAS

For RedisGraph, we’ve employed the GraphBLAS library to gain the benefits of matrix representations while optimizing for sparse data sets. (Special thanks to [Tim Davis](http://faculty.cse.tamu.edu/davis/suitesparse.html), who has worked closely with us to integrate his work as effectively as possible!)

GraphBLAS encodes matrices in compressed sparse column (CSC) form, which has a cost determined by the number of non-zero elements contained. In total, the space complexity of a matrix is:

(# of columns + 1) + (2 * # of nonzero elements)

For a dense graph, this is still bounded by *O(n2)*, but for a complete diagonal (the identity matrix) is only 3n + 1.

This encoding is highly space-efficient, and also allows us to treat graph matrices as mathematical operands. As a result, database operations can be executed as algebraic expressions without needing to first translate data out of a form (like a series of adjacency lists).

### Solving graph problems with linear algebra

The GraphBLAS interface allows the majority of our library invocations to be direct mathematical operations, such as matrix multiplications and transposes. These calls are evaluated lazily and optimized behind the scenes.

As an example, let’s take a simple graph that has 6 nodes, 4 of which have the label Person and 2 of which have the label Country:

![As an example, let’s take a simple graph that has 6 nodes, 4 of which have the label Person and 2 of which have the label Country](/images/site-mirror/4c88519e0ab1bde0c1ac6d84f6920892522bf935-251x247.webp)

The Cypher query we’ll run is:

MATCH (:person {name: ‘Jeff’})-[:friend]->(:person)-[:visited]->(:country)

This will find out which countries have been visited by my friends. The query will have a filter operation to only select `**person**` nodes with a matching `**name**` property, and we will have to traverse two adjacency matrices, **friend** and **visited**.

Thanks to the minimal impact of values in the CSC encoding, our adjacency matrices always represent all node IDs. This is in contrast to representing a matrix like visited with people as rows and countries as columns. The same relationships are shown in either case, but the CSC approach allows all matrices to have the same dimensions, with row/column indices that describe the same entities., As such, we can combine any of these matrices in algebraic expressions without needing to first convert them into comparable forms.

Our starting point for this query will be the `**friend**` adjacency matrix:

![Friend adjacency matrix](/images/site-mirror/5a42f41510665d19bf2374e70d221fdeb4eb198b-577x150.webp)

![friend adjacency diagram](/images/site-mirror/13d37236dfe4ddb3e545471acaf98721113ee001-226x227.webp)

I have Node ID 0, so entries in the first row of this matrix denote the IDs of individuals I am friends with. At the moment, filters are applied node-by-node, but an optimization we’re currently developing is applying them to the matrix at this stage. This will result in a modified adjacency matrix where only my friends are represented:

![modified adjacency matrix](/images/site-mirror/42dbaadecdf439ac4b94a4fe1d848547cc474a1a-577x150.webp)

Now we take the `visited` matrix, which has the same dimensions and describes all nodes in the same order:

![Visited matrix](/images/site-mirror/87e9ced620ad5edbce19b27b8aed1f73232c7e07-579x151.webp)

![Visited matrix diagram](/images/site-mirror/7602d6b43aa068772fb6251e8832bd3167eff572-324x298.webp)

By multiplying the filtered `friend` matrix against `visited`, we obtain a matrix which connects my node (as a row) to the countries that my friends have visited (as columns):

![Multiplying the filtered friend matrix against visited](/images/site-mirror/b31400a3cd81572d2e0afd977c34015e981c84f0-576x150.webp)

(For space optimization, we actually use boolean matrices here, so both entries would be 1 in practice.)

Testing the database’s performance on real data sets and more complex problems has yielded promising results.

### Benchmarks

All of the below values were built with the [Wikipedia top categories](https://snap.stanford.edu/data/wiki-topcats.html) data set on a 2016 Macbook Pro (2 GHz i5, 16gb RAM). The resulting graph contains 1,791,489 nodes and 28,511,807 edges.

Here are the performance results we achieved:

![](/images/site-mirror/a76f5fea4f34db444e3058951a2a3f83b8066fd8-456x174.webp)

A few notes:

- Create Graph — The in-module architecture we invoked here was effective, though this process will be substantially faster once we improve the additional tooling. CSV files are passed to RedisGraph in batches on the standard Redis pipeline, which takes 55 queries that are currently blocking operations. We’ll work on this soon!
- Who’s connected / Find two hops neighbors — This is what the matrix optimizations are most easily suited for, and I’m pretty happy with these metrics.
- Self-referencing nodes and memory consumption — One of our upcoming improvements will be a centralized property store, which I expect to improve both of these.

### Roadmap

Our development on RedisGraph is still highly active, and the most significant tasks ahead of us are:

- Support properties on edges
- Support index optimizations on label-property pairs
- Parallelism (GraphBLAS has many features for this that we haven’t started to invoke yet, and there is a lot of room to optimize the execution plan we construct and enact from queries)
- Allow for graphs distributed across multiple clusters
- Add a visualization utility
- Additional clients (we have built Python and Ruby interfaces so far)
- Optimization, optimization, optimization (this is a task without end, but we have some ideas that will be very fun to play out)

This is very much a wishlist, incidentally! In the spirit of Redis, RedisGraph is an open source project and contributors are always welcome. Feel free to reach out to us on GitHub if you have any comments, or if you’re interested in becoming involved.

### Further reading

- The project: [https://github.com/RedisGraph/RedisGraph](https://github.com/RedisGraph/RedisGraph)
- Documentation: [https://oss.redis.com/redisgraph/](https://oss.redis.com/redisgraph/)
- GraphBLAS homepage: [http://graphblas.org/](http://graphblas.org/)
- RedisConf videos:
  - [The Next-Generation RedisGraph](https://www.youtube.com/watch?v=9h3Qco_x0QE)
  - [Lower Latency Graph Queries in Cypher with RedisGraph](https://youtu.be/xnez6tloNSQ)
    - Yiftach Shoolman, CTO of Redis
    - Roi Lipman, project author, Redis
    - Tim Davis, professor, Texas A&M University
