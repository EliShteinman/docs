---
title: "Because What The World Needs is Another Memcached CLI"
linkTitle: "Because What The World Needs is Another Memcached CLI"
url: "/blog/because-what-the-world-needs-is-another-memcached-cli/"
description: "Today I’m proud to present my latest contribution to the open source community – bmemcached-cli. It is a simple Python wrapper around python-binary-memcached that provides an easy way to interact..."
date: 2014-06-12
blogCategories:
- "Tech"
authors:
- "Itamar Haber"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Itamar Haber, Technology Evangelist · Published 12 June 2014 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

![](/images/site-mirror/7175d24f6a273782a64c3c59a32489b13749ec05-635x200.webp)

Today I’m proud to present my latest contribution to the open source community – [bmemcached-cli](https://github.com/RedisLabs/bmemcached-cli). It is a simple Python wrapper around python-binary-memcached that provides an easy way to interact with a Memcached bucket via a command line interface. What makes it (arguably) unique is that it supports the Simple Security and Authentication Layer (SASL).

Here at Redis we are quite focused on providing the [best cloud-hosted Redis service](/redis-cloud). We do, however, also offer a similar [service for Memcached](/memcached-cloud) that’s actually built on top of our Redis technology. Memcached, despite being comparatively less robust than Redis, is still a popular choice for the caching layer, and a significant number of our users are using it. In fact, there are use cases where[ Memcached is preferable](https://stackoverflow.com/questions/23601622/if-redis-is-already-a-part-of-the-stack-why-is-memcached-still-used-alongside-r) to Redis (gasp!).

Like Redis, Memcached uses a plaintext protocol for client-server communication (that’s why you can use telnet to connect to your server). Unlike Redis, Memcached can also be configured with SASL authentication that, when used, switches communication to a binary protocol (BTW, if you’re looking for an authenticated and encrypted channel for your Redis, we also [offer](/blog/safe-and-informed-try-out-our-new-alerts-ssl-support) [SSL](/blog/secure-redis-ssl-added-to-redsmin-and-clients) for it). Memcached’s SASL authentication is primarily used to protect a bucket against unauthorized access. Additionally, one might argue that using SASL also makes it harder for eavesdroppers to intercept the traffic and that it helps in reducing the bandwidth.

Our Memcached Cloud service allows its users to configure their buckets with SASL effortlessly and with no interruption to their service. All you need to do to enable SASL is edit your bucket’s properties, tick the appropriate check box and supply a username and password. Once you’ve added SASL to your Memcached resource, you can no longer use plaintext to connect to it. This makes sense from a security perspective, but it makes debugging the contents of your cache more cumbersome. In fact, after searching the internets high and low, I couldn’t find even one CLI that supports Memcached’s binary protocol. So… I rolled up my sleeves and wrote one.

[>>> go to bmemcached-cli’s repository on github <<<](https://github.com/RedisLabs/bmemcached-cli)

Ok, I admit I didn’t have to write it from scratch. I stood on the shoulders of the giant Andrew W. Gross and shamelessly hacked his [labor of love](https://github.com/andrewgross/memcache-cli) to suit my needs. It was a short and fun project – I hope you find it useful. Questions? Feedback? [Email](mailto:itamar@redis.com) or [tweet](https://twitter.com/@itamarhaber) me – I’m highly available 🙂
