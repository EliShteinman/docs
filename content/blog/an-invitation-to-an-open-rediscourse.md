---
title: "An Invitation to an Open (Re)Discourse"
linkTitle: "An Invitation to an Open (Re)Discourse"
url: "/blog/an-invitation-to-an-open-rediscourse/"
description: "Arguably, one of the strongest benefits of the open source movement is that the community can get actively involved in the development of projects. Having access to the source code of an..."
date: 2013-09-18
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 18 September 2013 · updated 27 March 2025*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

![](/images/blog/1e5ce16de97edd6f44b100b44fa8a735dd9679f7-635x200.webp)

Arguably, one of the strongest benefits of the open source movement is that the community can get actively involved in the development of projects. Having access to the source code of an application allows anyone to modify it at will to suit specific needs (within the boundaries of its licensing). Naturally, we at Garantia Data not only use the open sourced Redis and Memcached software in our service, but also contribute our own developments back to the community.

Most of our contributions are tied into the projects we use, but once in a while we also diverge slightly. One such case is that of the popular [Discourse project](https://github.com/discourse/discourse) – an open source discussion platform that’s used for operating forums. It is built using Ruby and relies on Redis for job queuing, rate limiting and caching among others.

While it appears to be a solid piece of engineering, we have gotten several support calls from our users who had tried using it with our Redis Cloud service. The crux of the issue is that Discourse uses Redis’ shared databases capability.

Our service, by design, deliberately blocks any attempt to use this functionality because of performance considerations – you can read more on that topic in [this post](/blog/benchmark-shared-vs-dedicated-redis-instances). That limits our users that want to put their Redis Cloud instances to use with Discourse. To resolve this, we asked our engineers to dig into Discourse’s code and develop the fixes necessary to make it compatible with our service. They were successful, and we put in a [pull request](https://github.com/discourse/discourse/pull/1431) to have these fixes merged with Discourse’s sources.

Until then, you are welcome to use our Discourse fork, available from [our github](https://github.com/GarantiaData/discourse).

Do you have an open source project that you want us to take a look at? Are you experiencing any issues using our service with other software? Feel free to drop us a line and tell us about it. We can’t promise anything, but we’ll do our best to help!
