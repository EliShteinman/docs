---
title: "Redis Labs’ Modules License Changes"
linkTitle: "Redis Labs’ Modules License Changes"
url: "/blog/redis-labs-modules-license-changes/"
description: "For the latest information, please read the RSALv2 + SSPL license blog."
date: 2019-02-21
blogCategories:
- "Announcements"
- "Redis Modules"
- "Tech Redis Modules"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 21 February 2019 · updated 27 March 2025*

![Blog tile image](/images/blog/00d6e832d2ab431e2b67eba41a6dd5432229b696-1600x840.webp)

For the latest information, please read the [RSALv2 + SSPL license blog](/blog/rsalv2-sspl-announcement/).

### Background

Early in August 2018, Redis was one of the first open source companies to realize that the current open source licensing scheme falls short when it comes to use by cloud providers. We wanted to make sure open source companies could continue to contribute to their projects, while still maintaining sustainable business in the cloud era. That’s why we changed the license of our [Redis Modules](/community/redis-modules-hub/) from [AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html) to *Apache2 modified with *[*Commons Clause*](https://commonsclause.com/).

It was not an easy move for us, and we probably didn’t communicate the change clearly enough. This caused some confusion when some people incorrectly assumed that the Redis core [went proprietary](https://twitter.com/webmink/status/1032016976170967040?lang=en), which was never the case (see more [here](#here)).

However, over time, other respected open source companies, like [MongoDB](https://www.mongodb.com/blog/post/mongodb-now-released-under-the-server-side-public-license) and [Confluent](https://www.confluent.io/blog/license-changes-confluent-platform), created their own proposals for modern variants to open source licensing. Each company took a different approach, but all shared the same goal — stopping cloud providers from taking successful open source projects that were developed by others, packaging them into proprietary services, and using their market power to generate significant revenue streams.

Since last summer’s announcement, we’ve continued to manage our Redis Modules projects in the same way we manage our other open source projects. Our open and transparent manner helped the majority of our community accept the license change. Certain large enterprises even preferred it over AGPL, which we had previously used for those modules. During this period, we also received honest feedback from multiple users about how we could further improve our license to favor developers’ needs.

We identified three areas that needed to be addressed:

- The term *Apache2 modified by Commons Clause* caused confusion with some users, who thought they were only bound by the Apache2 terms.
- Common Clause’s language included the term “substantial” as a definition for what is and what isn’t allowed. There was a lack of clarity around the meaning of this term.
- Last but not least, some Commons Clause restrictions regarding “support” worked against our intention to help grow the ecosystem around Redis Modules.

Given all of these considerations, and after many discussions with members of our community, we decided to change the license of our Redis Modules to [Redis Source Available License (RSAL)](/legal/licenses/).

### What is Redis Source Available License (RSAL)?

RSAL is a [software license](/legal/licenses/) created by Redis for certain Redis Modules running on top of open source Redis. RSAL grants equivalent rights to permissive open source licenses for the vast majority of users. With RSAL, developers can use the software; modify the source code’ integrate it with an application; and use, distribute or sell their application. The only restriction is that the application cannot be a database, a caching engine, a stream processing engine, a search engine, an indexing engine or an ML/DL/AI serving engine.

For additional information, please see our [detailed FAQs](/legal/licenses/).

With RSAL in place, the Redis licensing model looks like this:

![](/images/blog/339d67369639ccc582aaf97115f3606b79edc776-1961x994.webp)

### This has no impact on the Redis core license

This change has zero effect on the Redis core license, which is and will always be licensed under the 3-Clause-BSD. Unlike many other open source database companies, we have built a dedicated team (led by Salvatore Sanfilippo, the creator of Redis), who manages the Redis core in a completely independent manner. Additionally, we have chosen **not** to limit the functionality of open source Redis by moving core components to closed source. Consequently, open source Redis includes all the ingredients needed to run a distributed database system — replication, auto-failover, data-persistence and clustering.

This open approach sometimes works against our commercial interest, since the cloud providers don’t have to do much in order to offer a viable Redis service. But we have a much bigger vision of helping modern applications provide instant experiences to their users. The only way to guarantee end-to-end instant application response time, which today is considered anything under 100msec, is by ensuring your database constantly and consistently responds to application requests in less than 1msec. Of course, we believe there’s only one database that can do this — and that is Redis!

### There is hope on the horizon

Most recently, we are seeing some cloud providers think differently about how they can collaborate with open source vendors. We believe those cloud providers that build the right collaboration infrastructure will be the ones that eventually benefit the most from open source projects.
