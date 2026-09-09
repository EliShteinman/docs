---
title: "Redis Ziplist"
linkTitle: "Redis Ziplist"
url: "/glossary/redis-ziplist/"
description: "A ziplist is a specialized data structure used in Redis, an in-memory data storage system. It is designed to efficiently store a sequence of small-sized elements, such as strings, integers, or..."
lastmod: 2025-06-30
---

*updated 30 June 2025*

## What is a ziplist?

A ziplist is a specialized data structure used in Redis, an in-memory data storage system. It is designed to efficiently store a sequence of small-sized elements, such as strings, integers, or floating-point numbers.

A ziplist is a compressed list representation that optimizes memory usage and provides efficient access to elements. It achieves this by using a sequential layout where the elements are stored one after another in a compact format. This eliminates the need for separate memory allocations and reduces memory overhead.

The structure of a ziplist consists of a series of entries. Each entry represents an element and contains the following components:

1. Prevlen: This field stores the length of the previous entry. It allows for efficient traversal in both forward and backward directions within the ziplist.
1. Entrylen: This field stores the length of the current entry.
1. Content: This field contains the actual data of the element, such as a string, integer, or floating-point value.

The elements in a ziplist are stored consecutively, which means there are no pointers or additional metadata between them. This compact representation reduces memory overhead compared to other data structures, such as linked lists, which require extra memory for pointers and metadata.

Ziplists also provide efficient access to elements by allowing direct indexing. Since the elements are stored sequentially, accessing an element at a specific index can be done in constant time. This is particularly useful when retrieving elements by their position or performing range-based operations.

Redis automatically switches between ziplist and other data structures, such as linked lists or hash tables, based on certain criteria. The decision to use ziplists depends on factors like the number of elements and their sizes. Redis provides configuration options to control the threshold values for switching between different representations.

## Redis Ziplist Best Practices

To gain an understanding of the potential efficiency of ziplists, let’s examine the basic structure known as a LIST. In a typical doubly linked list, nodes represent each value in the list. These nodes contain pointers to the previous and next nodes, along with a pointer to the string within the node. Each string value is stored as three parts: an integer indicating the length, an integer denoting the number of remaining free bytes, and the string itself followed by a null character. Figure 9.1 provides an example of this structure, showcasing the string values “one,” “two,” and “ten” as part of a larger linked list.

However, if we disregard some additional details that make linked lists appear less favorable, we realize that each of these three strings, consisting of three characters each, requires substantial overhead. In fact, they occupy space for three pointers, two integers (length and remaining bytes), the string, and an extra byte. On a 32-bit platform, this amounts to 21 bytes of overhead to store a mere 3 bytes of actual data. Please note that this estimation underestimates the actual storage requirements.

On the other hand, ziplists offer a more efficient representation by storing a sequence of length, length, and string elements. The first length represents the size of the previous entry for easy scanning in both directions, the second length denotes the size of the current entry, and the string represents the stored data itself. Although there are further details about the practical implications of these lengths, for the three example strings mentioned earlier, the lengths will only require 1 byte each. Consequently, in this example, the ziplist manages to reduce the overhead from 21 bytes per string to approximately 2 bytes.

Now, let’s explore how we can ensure the utilization of the compact ziplist encoding.

###### UTILIZING THE ZIPLIST ENCODING

To guarantee the selective use of ziplist representations and minimize memory consumption, Redis incorporates six configuration options. These options, as depicted in Listing 9.1, determine when the ziplist representation is applied to LISTs, HASHes, and ZSETs.

Configuration options for ziplist representation of different structures

- list-max-ziplist-entries: 512
- list-max-ziplist-value: 64
(Limits for ziplist usage with LISTs)
- hash-max-ziplist-entries: 512
- hash-max-ziplist-value: 64
(Limits for ziplist usage with HASHes; previous versions of Redis used different names and encodings for this)
- zset-max-ziplist-entries: 128
- zset-max-ziplist-value: 64
(Limits for ziplist usage with ZSETs)

The fundamental configuration options for LISTs, HASHes, and ZSETs share similar structures, consisting of “-max-ziplist-entries” settings and “-max-ziplist-value” settings. Their semantics are essentially identical across all three cases. The “entries” settings specify the maximum number of items allowed in the respective data structure for ziplist encoding to be employed. On the other hand, the “value” settings indicate the maximum size, in bytes, of each individual entry. If either of these limits is exceeded, Redis converts the structure (LIST, HASH, or ZSET) into a nonziplist representation, thereby increasing memory usage.

By default, Redis 2.6 installations should possess the same settings as those provided in Listing 9.1. Let’s experiment with the ziplist representations of a simple LIST object by adding items and examining its representation, as demonstrated in the following listing.

Determining ziplist storage for a structure

The crucial information we seek is the “encoding” field, which informs us that this LIST is stored using the ziplist encoding and occupies 24 bytes of memory.

The LIST remains in the ziplist representation, and its size has increased to 36 bytes. This increase precisely corresponds to 2 bytes of overhead (1 byte for data) for each of the four newly added items.

When an item larger than the allowed encoding limit is pushed, the LIST is automatically converted from ziplist encoding to a standard linked list representation.

Although the serialized length decreases, it is important to note that for nonziplist encodings (except for the special encoding of SETs), this number does not accurately reflect the actual memory consumption.

Once a ziplist is converted to a regular structure, it remains in that form even if it later fulfills the criteria for ziplist encoding.

With the introduction of the new DEBUG OBJECT command, determining whether an object utilizes ziplist storage becomes a useful approach to reduce memory consumption.

It is worth noting that one structure noticeably absent from the special ziplist encoding is the SET. Although SETs also possess a compact representation, they have different semantics and limitations, which we will explore in the following sections.
