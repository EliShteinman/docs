---
title: "Cache Coherence"
linkTitle: "Cache Coherence"
url: "/glossary/cache-coherence/"
description: "Cache coherence refers to the consistency and synchronization of data stored in different caches within a multiprocessor or multicore system. In such systems, each processor or core typically has..."
lastmod: 2026-05-03
---

*updated 3 May 2026*

## Introduction to Cache Coherence

Cache coherence refers to the consistency and synchronization of data stored in different caches within a multiprocessor or multicore system. In such systems, each processor or core typically has its own cache memory to improve performance. Cache memory plays a crucial role in computer architecture by providing fast access to frequently used data. However, maintaining data consistency across these private caches can be challenging, leading to the cache coherence problem.

Cache coherence ensures that all processors observe a consistent view of shared memory, preventing data inconsistencies and ensuring reliable program execution. The cache coherence problem arises when multiple caches store copies of the same data, and modifications made by one cache need to be propagated to other caches. Failure to maintain cache coherency can result in data corruption and incorrect program behavior.

Learn how to speed up and simplify your microservices applications with the [Cache and Message Broker for Microservices](https://redis.io/docs/caching-for-microservices/) solutions brief.

### Cache Memory in Computer Architecture

Cache memory plays a crucial role in modern computer architecture. It is a small, high-speed memory that stores frequently accessed data and instructions, providing faster access compared to main memory. Cache memory consists of cache lines, which are fixed-size blocks that store a subset of the data present in main memory.

The cache coherence problem arises due to the presence of multiple caches storing copies of the same data. When a cache modifies a cache line, it needs to ensure that all other caches holding copies of that line are updated or invalidated to maintain cache coherency. Cache coherence protocols address this problem by coordinating cache operations and ensuring consistent data access across the system. This will be covered in greater detail below in the section heading Methods to Resolve Cache Coherence.

## Cache Coherence Protocols

Cache coherence protocols are mechanisms designed to maintain cache coherence in multiprocessor systems. These protocols govern how caches communicate and coordinate their operations to ensure data consistency. Two commonly used cache coherence protocols are Snoopy Bus Protocols and Directory-Based Protocols.

### Snoopy Bus Protocols

Snoopy Bus Protocols rely on a shared bus that connects all caches in a multiprocessor system. These protocols monitor the bus for memory transactions and employ snooping logic to maintain cache coherence. Two popular policies used in Snoopy Bus Protocols are the Write-Invalidate policy and the Write-Update policy.

1. Write-Invalidate Policy: In the Write-Invalidate policy, when a cache performs a write operation on a shared memory block, it invalidates or marks as invalid all other copies of that block in other caches. When a cache wants to read a memory block, it first checks if any other cache holds a modified copy. If so, it requests the updated data from the cache that has the latest copy or from main memory.
1. Write-Update Policy: In the Write-Update policy, when a cache performs a write operation on a shared memory block, it updates the value in its own cache and also updates all other copies of that block in other caches. This approach reduces the need for subsequent cache-to-cache transfers for read operations. However, it requires more bus bandwidth for broadcasting updates to all caches.

Snooping Logic and Broadcast Messages: Snoopy Bus Protocols rely on snooping logic implemented in each cache controller. The snooping logic monitors bus transactions to determine if a cache’s copy of a memory block is still valid or needs to be invalidated or updated. When a cache performs a write operation, it broadcasts a message on the bus to inform other caches of the change. Caches with the snooping logic update their copies accordingly.

### Directory-Based Protocols

Directory-Based Protocols use a centralized directory to maintain cache coherence information. The directory keeps track of which caches hold copies of each memory block and manages the permissions for accessing and modifying the blocks. Two key features of Directory-Based Protocols are a common directory for maintaining coherence and permission-based data sharing.

1. Common Directory for Maintaining Coherence: In Directory-Based Protocols, a central directory maintains the coherence information for all memory blocks. It keeps track of which caches have copies of each block and their respective states (e.g., shared, modified). Caches communicate with the directory to request permission for accessing and modifying memory blocks.
1. Permission-Based Data Sharing: Directory-Based Protocols manage data sharing through permissions. When a cache wants to read or write a memory block, it requests permission from the directory. The directory grants permission based on the current state of the block and the coherence protocol in use. Caches coordinate with the directory to ensure that they have the required permissions before performing operations on shared memory blocks.

Directory-Based Protocols generally have higher overhead due to the centralized directory. However, they can provide better scalability and reduce bus contention compared to Snoopy Bus Protocols in large-scale multiprocessor systems.

By incorporating Snoopy Bus Protocols and Directory-Based Protocols, cache coherence can be effectively maintained in multiprocessor systems. These protocols enable efficient communication, coordination, and synchronization of caches, ensuring consistent and reliable data access across the system.

## Methods to Resolve Cache Coherence

Cache coherence protocols employ different methods to resolve the cache coherence problem. The cache coherence problem poses challenges in multiprocessor systems where each processor or core has its own cache memory. The presence of multiple caches storing copies of the same data requires coordination to maintain cache coherency. Cache coherence protocols address this problem by defining states, transitions, and communication mechanisms among caches. Two common approaches are the invalidation-based approach and the update-based approach. In the invalidation-based approach, when a cache modifies a shared memory block, it invalidates or marks as invalid copies of that block in other caches. The update-based approach, on the other hand, propagates updates to shared memory blocks among caches, ensuring that all caches have the latest version of the data.

### Write Through

In the Write Through policy, any write operation performed by a cache is simultaneously updated in both the cache and the main memory. This approach ensures that data modifications are immediately reflected in the main memory, keeping it consistent with the cache copies.

1. Simultaneous Updating of Cache and Main Memory: With Write Through, when a cache writes to a memory block, it propagates the update to both the cache and the main memory. This guarantees that the main memory always holds the most up-to-date data.
1. Benefits and Limitations: The Write Through policy simplifies cache management as there is no need to track modified blocks for later write-back. It provides a strong level of consistency since every write operation updates both the cache and main memory. However, it can introduce higher memory access latency due to the additional write operation to main memory for each cache write. It can also generate significant bus traffic in multiprocessor systems, as every write operation requires bus transactions to update both the cache and main memory.

### Write Back

In the Write Back policy, modifications are initially made only in the cache. The updates are later written back to the main memory when the cache block is replaced or evicted. This deferred write strategy optimizes memory access and reduces bus traffic by grouping multiple updates before writing to main memory.

1. Updating Cache Only, Main Memory Update on Block Replacement: With Write Back, a cache modifies a memory block solely in its cache. The modified data remains in the cache until the cache block is evicted or replaced. When that happens, the modified data is written back to the main memory.
1. Advantages and Disadvantages: Write Back offers lower memory access latency compared to Write Through since writes are initially performed only in the cache. This reduces the frequency of main memory writes, improving performance. Write Back also reduces bus traffic as updates are accumulated and written to memory in batches during cache block replacement. However, it introduces the risk of inconsistent data between the cache and main memory until a write-back occurs. This may require additional mechanisms, such as write invalidations or coherence protocols, to ensure data consistency among caches.

Choosing between Write Through and Write Back depends on the specific requirements and characteristics of the system. Write Through provides strong consistency at the cost of potential latency and bus traffic. Write Back offers improved performance by minimizing memory writes but introduces the need for cache-to-memory synchronization.

By implementing either Write Through or Write Back policies in cache coherence protocols, multiprocessor systems can effectively manage data modifications, maintain coherence, and optimize memory access based on the specific trade-offs and considerations of each policy.

## Cache Coherence Protocols in Multiprocessor Systems

Cache coherence protocols are crucial in multiprocessor systems to ensure data consistency and coordination among caches. Let’s explore some widely used cache coherence protocols and their key features.

### MSI Protocol (Modified, Shared, Invalid)

1. States and Transitions: The MSI protocol defines three states for cache blocks: Modified, Shared, and Invalid. The Modified state indicates that a cache block has been modified and differs from the main memory. The Shared state indicates that the cache block is valid and has multiple copies across different caches. The Invalid state denotes that the cache block is invalid or not present in the cache.
1. Handling Modified and Shared Data: In the MSI protocol, when a cache block is in the Modified state, any write operation triggers an invalidation of other copies in different caches. The Modified state allows the cache to retain ownership of the block, ensuring exclusive modification rights. When a cache block is in the Shared state, read operations can be performed, but write operations require transitioning to the Modified state.

### MOSI Protocol (Modified, Owned, Shared, Invalid)

1. Introduction to Owned State: The MOSI protocol extends the MSI protocol by introducing an additional Owned state. The Owned state indicates that a cache holds the exclusive ownership of a block, allowing both read and write operations without invalidating other copies.
1. Improved Handling of Ownership: The Owned state in the MOSI protocol provides an advantage over the MSI protocol. When a cache wants to modify a block in the Owned state, it can directly update the block without invalidating other copies. This reduces bus traffic and improves performance compared to the MSI protocol.

### MESI Protocol (Modified, Exclusive, Shared, Invalid)

1. Widely Used Cache Coherence Protocol: The MESI protocol is one of the most commonly used cache coherence protocols. It extends the MSI protocol by introducing the Exclusive state, which allows a cache to hold a copy of a block exclusively, indicating that no other cache has a copy.
1. Advantages of Exclusive and Modified States: The Exclusive state in the MESI protocol enables faster read operations by allowing caches to read the block without checking for other copies. When a cache wants to modify a block in the Exclusive state, it can transition to the Modified state directly without invalidating other copies. This reduces the need for unnecessary bus transactions, enhancing performance.

### MOESI Protocol (Modified, Owned, Exclusive, Shared, Invalid)

1. Comprehensive Coherence Protocol: The MOESI protocol further extends the MESI protocol by introducing the Owned state, similar to the MOSI protocol. This state provides the advantage of allowing both read and write operations without invalidating other copies.
1. Enhanced Performance and Data Sharing: The MOESI protocol combines the benefits of the Modified, Owned, Exclusive, Shared, and Invalid states. It optimizes performance by minimizing bus traffic, reducing the need for invalidations, and improving data sharing among caches. This comprehensive protocol offers efficient handling of various scenarios, promoting better performance in multiprocessor systems.

These cache coherence protocols—MSI, MOSI, MESI, and MOESI—provide different levels of complexity and trade-offs. Each protocol addresses the challenges of maintaining cache coherence in multiprocessor systems, offering various states and transitions to ensure data consistency and efficient data sharing among caches. The choice of protocol depends on factors such as system requirements, performance considerations, and the desired trade-offs between complexity and efficiency.

## Performance Impact and Considerations

Efficient cache coherence plays a vital role in the performance of multiprocessor systems. Let’s delve into various performance impacts and considerations associated with cache coherence.

### Coherence Overhead and Cache Misses

Cache coherence introduces additional overhead compared to single-processor systems. Coherence protocols require cache-to-cache communication, invalidations, and updates, which incur latency and consume bus bandwidth. These operations increase cache miss rates, leading to longer memory access times. Cache misses, especially coherence-related misses, can result in performance degradation as processors often need to fetch data from main memory or other caches.

### Scalability Challenges in SMPs

Scalability is a significant consideration in multiprocessor systems. As the number of processors increases, maintaining cache coherence becomes more challenging. With a larger number of caches, coherence-related traffic and bus contention rise, potentially leading to performance bottlenecks. Scalability challenges require careful design decisions, such as choosing appropriate coherence protocols, cache hierarchy, interconnect designs, and partitioning strategies to mitigate the impact of coherence overhead.

### Impact on System Performance and Latency

Cache coherence can impact overall system performance and latency. Coherence-related operations, such as invalidations and updates, introduce delays in accessing shared data. Synchronization mechanisms like cache invalidations or message passing between caches incur additional latency, affecting program execution time. Moreover, coherence-induced delays can be amplified in highly parallel applications that heavily rely on shared data, hindering system performance.

### Trade-offs and Design Considerations

Cache coherence protocols involve trade-offs between performance, complexity, and scalability. Coherence protocols that enforce strict consistency guarantees may introduce higher overhead and impact performance. On the other hand, protocols that provide weaker consistency models may offer improved performance but require additional programming considerations to maintain data integrity.

Design considerations encompass various aspects, including cache hierarchy, interconnect topology, cache coherence optimizations, and memory consistency models. Designers need to balance coherence requirements, latency, scalability, and system efficiency. Factors such as cache sizes, associativity, coherence message formats, and protocol optimizations can impact performance and should be carefully evaluated based on the specific requirements of the application and system architecture.

Efficient cache coherence management is crucial to mitigating performance impacts and ensuring optimal system behavior in multiprocessor systems. It involves finding the right balance between coherence overhead, scalability challenges, system performance, and the trade-offs inherent in the design. Through thoughtful analysis, optimization, and selection of appropriate coherence strategies, designers can create high-performance multiprocessor systems that effectively handle data sharing and maintain cache consistency.
