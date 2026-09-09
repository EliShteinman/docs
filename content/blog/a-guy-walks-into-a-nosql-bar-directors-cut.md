---
title: "A Guy Walks Into a NoSQL Bar [Director’s Cut]"
linkTitle: "A Guy Walks Into a NoSQL Bar [Director’s Cut]"
url: "/blog/a-guy-walks-into-a-nosql-bar-directors-cut/"
description: "A couple of months ago I published a post over at the Google Cloud Platform blog called “A guy walks into a NoSQL bar and asks: how many servers to get 1 million ops. a second?” That particular..."
date: 2015-05-29
blogCategories:
- "Tech"
authors:
- "Itamar Haber"
lastmod: 2025-03-27
hidden: true
---

*By Itamar Haber, Technology Evangelist · Published 29 May 2015 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/e3195514364c3b35f578b21723e4af89ba4fa0a0-140x92.webp)

![A Guy Walks Into a NoSQL Bar](/images/site-mirror/2bc3d3de7495c7187a726235b99f44841376ba82-635x200.webp)

## or DataStax, Aerospike, Couchbase and Redis: Serving 1M Writes/Sec From Google Compute Engine

A couple of months ago I published a post over at the Google Cloud Platform blog called [“A guy walks into a NoSQL bar and asks: how many servers to get 1 million ops. a second?”](http://googlecloudplatform.blogspot.com/2015/04/a-guy-walks-into-a-NoSQL-bar-and-asks-how-many-servers-to-get-1Mil-ops-a-second.html) That particular post had gone through several editing cycles and I’m very happy with the final result. When I wrote that particular post, I abbreviated my cheeky story, but given [Couchbase’s recent announcement](http://blog.couchbase.com/couchbase-server-hits-1m-writes-with-3b-items-with-50-nodes-on-google-cloud) about getting to 1M writes/sec with **only 50 servers (!)**, I thought it would be relevant to share the full glory of my analogy here.

**Note:** the joke is still not very funny – suggestions for improvement are welcome!

### Preface

Comparisons are as hard to do right as they are easy to do wrong and when the subjects of comparison are different the problem is only compounded. Therefore, when practicing comparative “advertising” I often feel that the results begotten should be interpreted in spirit rather be presented as numbers to quibble about. With that in mind, let me share a brief related story…

### Prologue

A guy walks into a NoSQL bar looking quite upset. “Can I have a glass of red wine and a glass of white wine?” he asks the bartender. “Right away sir,” says the bartender, “but may I ask why the long face?” “I was in that other NoSQL bar further down the road, the Spiky Aerrow,” answers the patron, “and asked for that exact same order. The server there is known for his speed (some people swear he can do several things at once) as well as the amazing way he prepares drinks, so I was kind of expecting a show.”

The bartender, whose bar has been open for quite a few years, nods sympathetically and says, “I’m guessing he didn’t quite dazzle you?” “On the contrary,” replies the customer, it was an awesome show. To prepare my glass of red, that spectacular master of liquids uncorked no less than 30 bottles of wine in a fraction of a second! He then continued by whirlwinding between all these bottles and pouring a little wine from each into my glass. A lot of wine splashed around and spilled, given the speeds involved, but it was a heck of a show. And then, he did the same thing for the white… but with 50 bottles!”

### Introduction

Some time ago, we at Redis set out to answer the question: “How many Google Compute Engine nodes do you need to serve 1 million write operations per second?” The question, besides sounding like a variation of the lightbulb joke, is quite open-ended in terms of defining the actual nature of the write operation based on[ previous](http://googlecloudplatform.blogspot.com/2014/12/aerospike-hits-one-million-writes-Per-Second-with-just-50-Nodes-on-Google-Compute-Engine.html) [work](http://googlecloudplatform.blogspot.com/2014/03/cassandra-hits-one-million-writes-per-second-on-google-compute-engine.html) on the subject. Given our experience with cloud platforms in general, and particularly with Google’s, we were fairly confident that we’d need only a few so we set out to find out.

### Benchmark Setup

To run the benchmark, we chose the biggest Google Compute Engine nodes currently available in us-central – the n1-highcpu-16 type – and we ended up using just two such servers to run our Redis Enterprise Cluster software (freely downloadable from [here](/redis-enterprise-downloads)). We used another pair of servers – this time n1-highcpu-8 – to generate the load with [memtier_benchmark](https://github.com/Redis/memtier_benchmark) using the following command line arguments:

memtier_benchmark -s 10.0.0.1 -p 6379 --ratio=1:1 --test-time=120 -d 100 -t 2 -c 50 --pipeline=50 --ratio=1:0

### Benchmark Results

We ran the benchmark three times, first serving only reds reads, then serving only whites writes, and finally both in equal mix. Here are the results from those tests:

1. For read-only operations, our Redis database provided throughput of **1.29M read operations per second** at an average latency of 0.15 millisecond per operation.
1. With the write-only load, the cluster’s measured throughput was at **1.14M operations per second** at 0.36sec average latency per request.
1. An equal mix of read and write operations gave a throughput of **1.16M operations per second** at an average latency of 0.17msec per operation.

![Redis Enterprise Cluster on Google Cloud Platform - Over 1M ops/sec](/images/site-mirror/b096f15c68d002886c81e2319231e54caac4bb54-635x396.webp)

### Conclusion

Redis needed only two Google Cloud Engine servers in the cluster to cross the 1M op/sec threshold.

### Epilogue

Before the man can finish his story, the bartender had finished preparing the order (using just one bottle of white and one bottle of red, mind you). He placed the drinks alongside the bill in front of the customer, and said “sounds like an amazing show indeed, but I still don’t understand why you’re so unhappy.” “I’ll tell you why,” answered the man, “guess who had to pay for all 80 bottles of spilled wine?”

The barman smiled and said, “You should consider yourself lucky then, sir. I heard of a place further uptown called Dat Stacks where for every glass of white wine they charge for 300 bottles.”

![1M Ops/Sec on Google Cloud Platform: Your bill, sir](/images/site-mirror/737ae62dd4dbb43224f8a78b53a23d8e1adea566-635x677.webp)

Ok, so maybe this joke isn’t really that funny, but neither is paying too much for less-than-top-notch performance 🙂 With Redis, reaching and exceeding the 1 million operations per second mark doesn’t require a truckload of cloud servers – just one or two will do nicely.
