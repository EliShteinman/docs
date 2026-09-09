---
title: "Multi-Model Redis Database on Minikube for Developers"
linkTitle: "Multi-Model Redis Database on Minikube for Developers"
url: "/blog/multi-model-redis-database-minikube-developers/"
description: "Setting up your development environment is rarely straightforward and hassle-free. Whatsmore, given modern applications’ appetite for polyglot persistence and containerized deployment, it becomes..."
date: 2018-06-11
blogCategories:
- "Company"
- "How To and Tutorials"
authors:
- "Itamar Haber"
lastmod: 2025-03-27
hidden: true
---

*By Itamar Haber, Technology Evangelist · Published 11 June 2018 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

Setting up your development environment is rarely straightforward and hassle-free. Whatsmore, given modern applications’ appetite for polyglot persistence and containerized deployment, it becomes quite challenging to bootstrap your laptop with all the infrastructural goodness needed for a simple “Hello, World!”. In this post, I’m going to show you how to quickly get started developing your application with a multi-model Redis database on Kubernetes.

A multi-model database is one that supports multiple data models against a single backend. While [Redis](/redis-features/redis) is, at its core, a key-value-like data structures store, modules can extend it in almost any conceivable way. Presently, Redis’ open source modules add the following capabilities to Redis:

- Full text search, aggregations and secondary indexing with [RediSearch](https://oss.redis.com/redisearch)
- Graph databases and OpenCypher queries with [Redis Graph](https://oss.redis.com/redisgraph)
- Machine learning model serving with [Redis-ML](https://oss.redis.com/redisml)
- Document store with [ReJSON](https://oss.redis.com/rejson)
- Probabilistic data types with ReBloom

Redis Enterprise already includes all these modules and can readily be [deployed and run on Kubernetes](/blog/running-redis-enterprise-kubernetes-service/). However, up until recently there was no ready-made open source Redis container image that delivered the same functionality. So I made one, automated its build and put it on Docker Hub: [https://hub.docker.com/r/redislabs/redismod](https://hub.docker.com/r/redislabs/redismod)

The redismod container provides a default installation (i.e. not production-hardened) of a single-instance Redis server. It is also configured to load all five modules upon startup, but you’re more than welcome to override this behavior. Running the container is just a matter of executing the following command at your terminal prompt:

docker run -p 6379:6379 redis/redismod

To use the redismod image (alongside your application’s) on Kubernetes, assuming you don’t have access to Kubernetes deployment, you can use [minikube](https://kubernetes.io/docs/getting-started-guides/minikube/). As stated by minikube’s documentation:

> “Minikube is a tool that makes it easy to run Kubernetes locally. Minikube runs a single-node Kubernetes cluster inside a VM on your laptop for users looking to try out Kubernetes or develop with it day-to-day.”

It takes just five steps to get your minikube “cluster” up and running the redismod container:

1. Install minikube: [https://kubernetes.io/docs/tasks/tools/install-minikube/](https://kubernetes.io/docs/tasks/tools/install-minikube/)
1. Start minikube:
minikube start
1. Deploy the redismod image:
kubectl run redismod --image=redis/redismod --port=6379
1. Expose the deployment:
kubectl expose deployment redismod --type=NodePort
1. Optionally, check that the pod’s status is ‘running’:
kubectl get pod

Once that’s done, you can connect to the redismod service like so:

```javascript
$ redis-cli -u $(minikube service --format "redis://{{.IP}}:{{.Port}}" --url redismod)
192.168.99.100:31501> PING
PONG
192.168.99.100:31501> MODULE LIST
1) 1) "name"
   2) "redis-ml"
   3) "ver"
   4) (integer) 9901
2) 1) "name"
   2) "ft"
   3) "ver"
   4) (integer) 10100
3) 1) "name"
   2) "graph"
   3) "ver"
   4) (integer) 1
4) 1) "name"
   2) "ReJSON"
   3) "ver"
   4) (integer) 10001
5) 1) "name"
   2) "bf"
   3) "ver"
   4) (integer) 10100

```

That’s basically all there is to it – all you have to do now is connect to redismod from your application to start modeling your data with multiple modules on Redis. Questions? Feedback? [Email](mailto:itamar@redis.com) or [tweet at me](https://twitter.com/itamarhaber) – I’m highly available 🙂
