---
title: "An Introduction to Redis-ML (Part Four)"
linkTitle: "An Introduction to Redis-ML (Part Four)"
url: "/blog/introduction-redis-ml-part-four/"
description: "This post is part four of a series of posts introducing the Redis-ML module. The first article in the series can be found here."
date: 2017-08-28
blogCategories:
- "Company"
- "Tech"
authors:
- "Tague Griffith"
lastmod: 2025-03-27
hidden: true
---

*By Tague Griffith, Head of Developer Advocacy · Published 28 August 2017 · updated 27 March 2025*

![Blog tile image](/images/blog/cf3eb9dd6b8252d7d100cccc68508e2b16b2a5ea-313x275.webp)

*This post is part four of a series of posts introducing the Redis-ML module. The first article in the series can be found *[*here*](/blog/introduction-redis-ml/)*.*

In this post, we’re going to look at the matrix operations provided by the Redis-ML module and show some examples of how to process Matrix data using the Redis database.

**Technical Requirements**

The example code in this post is written in Python and requires a Redis instance running Redis-ML. The instructions for setting up Redis can be found in either part [one](/blog/introduction-redis-ml/) or part [two](/blog/introduction-redis-ml-part-two/) of this series.

**Matrices in Redis**

[Watch the video](https://en.wikipedia.org/wiki/Matrix_multiplication#/media/File:Matrix_multiplication_diagram_2.svg)

Matrices are common in machine learning, statistics, finance and a host of other domains, so they were a natural addition to Redis. The Redis-ML module adds matrices as a native Redis data type. It also provides mathematical operations that combine matrices to create new values.

Reading and writing matrix values is performed through the ML.MATRIX.SET and the ML.MATRIX.GET commands which have the following syntax:

```javascript
ML.MATRIX.SET key n m entry11 .. entrynm
ML.MATRIX.GET key
```

When working with the Redis-ML module, remember that commands use [row-major](https://en.wikipedia.org/wiki/Row-_and_column-major_order) format. Multiplication and addition are supported by the ML.MATRIX.MULTIPLY and the ML.MATRIX.ADD commands.

```javascript
ML.MATRIX.MULTIPLY a b result
ML.MATRIX.ADD a b result
```

These commands combine two matrices that are already in Redis and store the result in a new key.

If I wanted to compute a basic Matrix equation such as y = Ax + b using the Redis-ML module, I would enter the following commands into the Redis CLI:

```javascript
127.0.0.1:6379> ML.MATRIX.SET a 3 3 4 0 0 0 2 0 0 0 1
127.0.0.1:6379> ML.MATRIX.SET x 3 1 1 4 1
127.0.0.1:6379> ML.MATRIX.SET b 3 1 1 1 1
127.0.0.1:6379> ML.MATRIX.MULTIPLY a x tmp
127.0.0.1:6379> ML.MATRIX.ADD tmp b y
127.0.0.1:6379> ML.MATRIX.GET y

1) (integer) 3
2) (integer) 1
3) "5"
4) "9"
5) "2"
```

Redis returns the result to our client with the shape of the matrix (in this case 3 rows and 1 column) followed by each of the elements of the matrix in row-major order.

I could also compute the Matrix equation A’ = cA (where c is a scalar value) using the following code:

```javascript
127.0.0.1:6379> ML.MATRIX.SET a 3 3 4 0 0 0 2 0 0 0 1
127.0.0.1:6379> ML.MATRIX.SCALE a 3
127.0.0.1:6379> ML.MATRIX.GET a

 1) (integer) 3
 2) (integer) 3
 3) "12"
 4) "0"
 5) "0"
 6) "0"
 7) "6"
 8) "0"
 9) "0"
10) "0"
11) "3"
```

Matrices are used for a wide range of applications, from linear transforms to representing multivariate probability distributions. In the next post, we’ll look at decision trees and random forests, two additional classification models supported by Redis.

Please connect with me on twitter ([@tague](https://twitter.com/tague)) if you have questions regarding this or previous posts in the series.
