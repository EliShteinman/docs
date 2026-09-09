---
title: "The Number of Unsecured Redis Servers Keeps Declining"
linkTitle: "The Number of Unsecured Redis Servers Keeps Declining"
url: "/blog/fewer-unsecured-redis-servers/"
description: "Earlier today, security firm TrendMicro published a blog post with findings from the company’s security researchers. The team had used Shodan, the popular search engine for internet-connected or..."
date: 2020-04-02
blogCategories:
- "Company"
authors:
- "Itamar Haber"
lastmod: 2025-03-27
hidden: true
---

*By Itamar Haber, Technology Evangelist · Published 2 April 2020 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

Earlier today, security firm TrendMicro published a [blog post](https://blog.trendmicro.com/trendlabs-security-intelligence/more-than-8000-unsecured-redis-instances-found-in-the-cloud/) with findings from the company’s security researchers. The team had used [Shodan](https://shodan.io/), the popular search engine for internet-connected or Internet of Things (IoT) devices, to identify more than 8,000 unsecure Redis servers across various clouds. When left unsecured, such servers could be used by cybercriminals for nefarious purposes.

## A declining number of exposed Redis servers

That number is substantial, but it demonstrates a constant, if not declining, number of exposed servers overall. About three years ago, I used the same method to count [9,916](https://twitter.com/itamarhaber/status/821087241669869573) such servers, and a year later Shodan had [confirmed](https://twitter.com/shodanhq/status/1002460006187495425) that newer versions of Redis, specifically version 4.0, had “drastically improved/lowered the numbers of publicly accessible Redis instances”—counting 17,443 unsecured servers worldwide.

This drastic improvement is due to the [protected mode](https://redis.io/topics/security#protected-mode) introduced in Redis version 4.0 and backported to Redis version 3.2.0. This special mode, enabled by default, prevents unsecure access to the server from the outside. Looking at the top Redis versions used by unsecure servers, we see that a significant part of the exposed server are still using outdated versions.

[Watch the video](https://www.shodan.io/search?query=product%3Aredis+redis_version)

Taken from the Shodan report, the table above shows the exposed Redis servers’ version (right side) and their respective counts (left). The fact that there are exposed servers running Redis v3.2.0 and above is concerning, of course. It means that the administrators of these Redis servers deliberately disabled protected mode and didn’t set passwords for their databases. The motivations for intentionally doing that are unclear; it seems no amount of security protections are enough to fully overcome the possibility of human error.

## Continuing to improve Redis security

That said, we’re continuing to improve on open source Redis’ security. Managed service provided by Redis is secure out of the box, and eliminates the need for users to figure out their own security practices. In addition, security is a key focus of the next version of open source Redis, expected to be released later this April. The upcoming [Redis version 6.0](http://antirez.com/news/131) adds Transport Layer Security (TLS) encryption to all three communication channels: client-server, master-replica, and cluster bus. Furthermore, Redis 6.0 includes a new [Access Control List (ACL)](/blog/getting-started-redis-6-access-control-lists-acls/) mechanism integrated into the server, which allows the definition of fine-grained user permissions for accessing and manipulating data.

Redis always treated security risks with extreme seriousness and our enterprise products are designed to help prevent them. The Redis Enterprise stack blocks the creation of passwordless databases. Additional security features of Redis Enterprise include TLS encryption and tight integration with the organizational identity management system, as discussed [here](/redis-enterprise/technology/redis-security-reliability/) and [here](/blog/securing-redis-with-redis-enterprise-for-compliance-requirements/).

## Conclusion

Looked at in context, the blog post from Trend Micro actually shows an encouraging and declining trend of the number of open source Redis servers that are exposed. Newer versions, meanwhile, improve open source Redis’ security model by reducing the attack surface, encrypting communication channels, and adding permissions management.

By its very nature, however, open source software—including Redis—can be easily configured with all, some, or none of the available security features. So when it comes to using Redis in production, users should carefully review their security settings—or opt for the production-proven and security-hardened [Redis Enterprise](/).
