---
title: "Secure Redis: SSL Added to Redsmin and Clients"
linkTitle: "Secure Redis: SSL Added to Redsmin and Clients"
url: "/blog/secure-redis-ssl-added-to-redsmin-and-clients/"
description: "Today we are happy to make two exciting announcements: we’ve made SSL support available for Redsmin and we’re releasing a couple of Redis clients that we’ve patched to support SSL. Since Redis..."
date: 2014-04-14
blogCategories:
- "Tech"
authors:
- "Itamar Haber"
lastmod: 2025-03-27
hidden: true
---

*By Itamar Haber, Technology Evangelist · Published 14 April 2014 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

Today we are happy to make two exciting announcements: we’ve made SSL support available for Redsmin and we’re releasing a couple of Redis clients that we’ve patched to support SSL. Since Redis [doesn’t](https://code.google.com/p/redis/issues/detail?id=71) [include](https://twitter.com/antirez/status/243763404341403648) [native](https://github.com/antirez/redis/issues/675) [support](https://redis.io/topics/security) for secured communication – an extremely valid design decision – all the heavy lifting (e.g. [setting up a secure stunnel proxy](http://bencane.com/2014/02/18/sending-redis-traffic-through-an-ssl-tunnel-with-stunnel/), /ht Benajmin Cane, a.k.a [@madflojo](https://twitter.com/madflojo)) is left to Redis admins and developers. As both Redsmin and Redis offer a turn-key solution for Redis needs (each in its own domain), it is only natural that we rise to the challenge and provide a secure and easy Redis environment.

Redsmin can now connect, [monitor in real-time](https://www.youtube.com/watch?v=hGqp5QFGOM4) and manage Redis databases that are protected with SSL. Connecting to such databases couldn’t be simpler – just copy/paste your certificates to Redsmin and you’re good to go! The following screencast shows how simple it is to get started:

[Click here to view video](https://www.youtube.com/embed/kHmfhkClDhs)

Another piece missing from the pu-ssl-e was the availability of Redis clients that support SSL. Applications using SSL to connect to their Redis database had to deploy an additional component in the server’s stack by [installing stunnel](/kb/read-more-ssl) (or any other secure proxy) to successfully establish a connection. This approach had not only introduced complexity to the app’s operations, but was also impractical in cases in which the app is hosted.

Luckily, adding SSL support to popular Redis clients proved to be an easy task for our developers and the fruits of their labor are presented in the list below:

- Ruby’s redis-rb
  - Fork: [https://github.com/Redis/redis-rb](https://github.com/Redis/redis-rb)
  - Pull request: [https://github.com/redis/redis-rb/pull/419](https://github.com/redis/redis-rb/pull/419)
  - [UPDATE] As of April 18th, 2017 (v3.3) redis-rb supports SSL: [https://github.com/redis/redis-rb](https://github.com/redis/redis-rb) (ty Jonty Wareing for the tip!)
- Java’s [Jedis](https://github.com/Redis/jedis)
  - Fork: [https://github.com/Redis/jedis](https://github.com/xetorthio/jedis)
  - [Pull request: ](https://github.com/Redis/jedis)[https://github.com/xetorthio/jedis/pull/611](https://github.com/xetorthio/jedis/pull/611)
  - [UPDATE] As of December 4th, 2015 the original pull request has been replaced by [https://github.com/xetorthio/jedis/pull/1173](https://github.com/xetorthio/jedis/pull/1173)
  - [UPDATE] As of July 22nd, 2016 (v2.8.2 and v2.9.0) Jedis supports SSL: [https://github.com/xetorthio/jedis](https://github.com/xetorthio/jedis)
- Python’s redis-py
  - Fork: [https://github.com/Redis/redis-py](https://github.com/Redis/redis-py)
  - Pull request [https://github.com/andymccurdy/redis-py/pull/446](https://github.com/andymccurdy/redis-py/pull/446)
  - [UPDATE] As of May 15th, 2014 redis-py supports SSL: [https://github.com/andymccurdy/redis-py](https://github.com/andymccurdy/redis-py/)
- PHP’s predis
  - Fork: [https://github.com/RedisLabs/predis](https://github.com/RedisLabs/predis)
  - Pull request: [https://github.com/nrk/predis/pull/158](https://github.com/nrk/predis/pull/158)
  - [UPDATE] As of June 2nd, 2016 (v1.1.0) Predis supports TLS/SSL [https://github.com/nrk/predis](https://github.com/nrk/predis)
- Node.js’s node_redis
  - Fork by Paddy Byers: [https://github.com/paddybyers/node_redis](https://github.com/paddybyers/node_redis)
  - Pull request [https://github.com/mranney/node_redis/pull/527](https://github.com/mranney/node_redis/pull/527)
  - [Update] As of November 25th, 2015, version 2.4.0 of node_redis supports TLS: [https://github.com/NodeRedis/node_redis](https://github.com/NodeRedis/node_redis)
- .NET’s StackExchange.Redis
  - [UPDATE] As of April 16th, 2014 StackExchange.Redis supports SSL: [https://github.com/StackExchange/StackExchange.Redis](https://github.com/StackExchange/StackExchange.Redis)

Currently, these modified clients are yet to be merged into their respective trunks, so feel free download the forks and to cast your vote on the their pull requests. If you have any requests for a Redis client that’s not on the list – just let us know, and if you want to help in developing one you’ll get [free Redsmin](https://www.redsmin.com/) and [Redis Cloud](/pricing) environments from us – so what are you waiting for?
