---
title: "What’s New in RedisGraph 1.2.0"
linkTitle: "What’s New in RedisGraph 1.2.0"
url: "/blog/whats-new-redisgraph-1-2-0/"
description: "Last week, we released RedisGraph 1.2.0. If you’ve been using RedisGraph or considering trying out the module, this is a good time to see what we’ve been up to as we continue to enhance its graph..."
date: 2019-05-02
blogCategories:
- "New Product Announcements"
authors:
- "Roi Lipman"
lastmod: 2025-03-04
hidden: true
---

*By Roi Lipman, Senior Engineer · Published 2 May 2019 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/99f38cc34cb4c7c53ae53eb6211846ecefd21f0b-260x241.webp)

Last week, we released RedisGraph 1.2.0. If you’ve been using RedisGraph or considering trying out the module, this is a good time to see what we’ve been up to as we continue to enhance its graph processing capabilities. Let’s review some of the more notable additions in the new release:

### 

### Multiple edges of the same type

Up until this release, connecting node A to node B via an edge of type R and then forming another connection of the same type between the two was not possible. as the latter would overwrite the former one, because of the way connections used to be represented in RedisGraph.

For every relation type, e.g. `friend`, `works_at` or `owns`, RedisGraph maintains a mapping matrix M, in which M[I,J] = EdgeID where I and J are the source and destination node IDs, respectively. Forming the first connection of type R between A and B would have M[I,J] set to X, and introducing a second edge of type R between the two would overwrite M[I,J] with Y.

![](/images/site-mirror/61b5685f67788b29b7d998fa4bca4f56a52630bf-300x91.webp)

###### Multiple edges of the same type

With release 1.2.0, RedisGraph now enables multiple edges of the same type. Our mapping matrix M can hold a pointer to an array of edge IDs, M[I,J] = [ID0, ID1, … IDn], specifying each edge of type R connecting I to J.

To avoid high memory fragmentation, consider a graph with 500 million edges none of which share source or destination nodes, i.e. no multiple edges of the same type between any two nodes. A naive approach would have allocated 500M arrays of length 1, increasing our memory consumption significantly. To encounter this, our mapping matrix entry type remained the same (UINT64). Starting with an empty graph – M[I,J] is empty – when the first edge E is formed, connecting I to J, M[I,J] = ID(E) is a simple constant and no extra memory is allocated. At some point, I is connected once again to J with an edge X of the same type as E, M[I,J] = [ID(E), ID(X)], an array is allocated and a pointer is placed in M[I,J].

![](/images/site-mirror/f5bec25e0bed3f0fa53d5cff203dbee838574ef3-300x82.webp)

###### M[1,3] edge ID, M[3,1] array pointer

### Seeking nodes in constant time

Whenever a graph entity (Node, Edge) is created, an internal unique ID is assigned to it. This ID is immutable throughout the entity life, and you can retrieve an entity ID by using the *ID* function: *MATCH (N) RETURN N, ID(N) LIMIT 10. *Similarly, finding a node by its ID: “*MATCH (N) WHERE ID(N) = 9 RETURN N” *used to perform a full scan, inspecting each node in the graph.

Our latest release of RedisGraph introduces an optimization that replaces these full-scan and filter operations with a single `seek node by id` operation, which runs in constant time.

![](/images/site-mirror/dd5f32d80868bad5913c106a313fad29e5434519-536x35.webp)

###### Full scan and filter O(N),

![](/images/site-mirror/cda05ce4b7a491c2ad6137f5d0b2b675f72f53ec-491x35.webp)

###### Optimized node seek O(1)

### Transpose once

In RedisGraph, traversals are performed by matrix multiplication. For example, consider the search pattern: *(A)-[X]->(B)-[Y]->(c). *To find all source nodes (A) that are connected to destination nodes (C), we’re simply multiplying matrix [X] by matrix [Y], *X*Y=Z*, and Z’s rows and columns represent A and C respectively.

If we’re interested in just a handful of C nodes, we’ll want to avoid performing *X*Y,* as these might be very large matrices. As such, we’ll tack on a small filter matrix F, (*F*X)*Y*. By multiplying *F*X* first, we’re reducing any intermediate matrix computed dimensions, dramatically reducing computation time.

Depending on the result of *F*X*Y,* we might find ourselves computing a different filter matrix F and re-evaluating this expression to get additional C nodes. This process may repeat itself several times before we have enough data. Now, whenever a search pattern contains left-to-right and right-to-left edges: *(A)-[X]->(B)<-[Y]-(C), *we’ll have to transpose Y, (*F*X)*Transpose(Y) = Z*.

![](/images/site-mirror/d79d9da67aec3335807bb02c15f292bb3bbf6181-300x80.webp)

###### Filter * X * Transpose(Y)

Previous versions of RedisGraph transposed Y on every evaluation of this expression, which was costly. Now, as of release 1.2.0, we’ll only transpose once on the first evaluation. Although this results in higher memory consumption per query, the latency gain is definitely worth it.

Overall RedisGraph 1.2.0 contains both overdue features and some interesting optimizations,[give it a try](https://github.com/RedisGraph/RedisGraph) let us know what you think!
