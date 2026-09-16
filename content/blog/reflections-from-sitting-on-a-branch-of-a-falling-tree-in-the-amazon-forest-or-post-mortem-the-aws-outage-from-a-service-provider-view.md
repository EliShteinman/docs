---
title: "Reflections from Sitting on a Branch of a Falling Tree in the Amazon Forest or Post-Mortem: The AWS Outage From a Service Provider View"
linkTitle: "Reflections from Sitting on a Branch of a Falling Tree in the Amazon Forest or Post-Mortem: The AWS Outage From a Service Provider View"
url: "/blog/reflections-from-sitting-on-a-branch-of-a-falling-tree-in-the-amazon-forest-or-post-mortem-the-aws-outage-from-a-service-provider-view/"
description: "You’ve probably already heard about AWS’s outage last Sunday around noon PDT. The thud of that “minor” network-cum-storage issue in one of the busiest data regions of the Amazon forest cloud was..."
date: 2013-08-28
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Redis   · Published 28 August 2013 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/8bb21643bb9d36edc1f85f46232224d6652c03e8-140x92.webp)

![Beware of falling limbs!](/images/site-mirror/fe1427d29975eb27614bf9d733372947ad2fc519-635x200.webp)

You’ve probably [already heard](http://blogs.wsj.com/digits/2013/08/25/amazon-web-services-outage-cuts-off-big-names/) about AWS’s outage last Sunday around noon PDT. The thud of that [“minor” network-cum-storage issue](http://gigaom.com/2013/08/25/amazon-web-services-experienced-minor-outage-on-sunday/) in one of the busiest data regions of the Amazon forest cloud was heard loud and clear. Even before that fallen zone tree’s leaves touched the ground, reports about the collapse of some of the better-known social brands (i.e. [Instagram, Vine & IFTTT](http://techcrunch.com/2013/08/25/instagram-vine-and-ifttt-went-dark-thanks-to-amazon-web-services-issues/)) started coming in.

As usual, AWS has not divulged the full extent of the incident’s impact, but it stands to reason that there were other, albeit smaller, casualties as well. Our Redis Cloud and Memcached Cloud services use resources from that zone, and we manage a number of fairly large clusters in it. We use network and storage heavily, given the nature of our replicated and durable in-memory databases, so naturally our dashboard flared bright red at the first sinister splintering sound.

From the extent of damage we monitored in our environment, we believe it’s possible that 15-30 percent of that zone’s services were affected by the event. Even after the network started degrading, our systems were thankfully able to withstand the interruption. Our replication streams were not laggy for the most part, and the response latency impact was relatively small.

Things looked a little shaky for the availability of our non-Multi-AZ instances for a while, but we held on tight. But just when it seemed that the worst was over and the shakes were subsiding, we experienced plummeting performance with the accelerated decline of our storage.
*Cliffhanger.*

### Did You Know?

Although somewhat counterintuitive at first, in-memory database do use storage. However, they use it only to store data instead of reading and writing from/to it like disk-based database.

Writing the data to disk endows the in-memory database with persistency – a highly desirable trait that comes in very handy when recovering from a meltdown, but that’s a different story. However, it also means that when the storage becomes unavailable the database can’t ensure the data’s durability. It can still serve read requests, but in most cases a read-only database is like a fish on a bicycle.

This is why most in-memory databases are designed to cease operating without accessible storage, Redis included.

### And now back to our regularly scheduled programming…

With storage failing on multiple nodes simultaneously, our systems did the only thing they could: work around the failure to recover themselves and keep the service operational.

Affected nodes continued serving the non-persistent Redis Cloud instances while immediate action was taken with the persistent ones. Persistence-enabled Redis Cloud instances were quickly migrated to unaffected server and storage resources before causing any disruption to our service. Granted, the extra load we put on the network and storage in moving the data from one place to the other wasn’t meant as a resolution to the developing issues, but was aimed at making a hasty retreat to neighboring shelters.

### Eventually, we were able to clear the danger zone – in less than 20 minutes.

After all the dust had settled, we ran a quick survey of our users and were relieved to learn that none had experienced any issues with our service during that period (despite our logs looking like the work of a psychotic ax murderer). Of course, the scenario might have been different had this outage been marginally less minor.

We’re glad that wasn’t the case, and feel validated to obtain real-life proof of how a system that’s designed for dynamic stability copes with the challenges it was built for.
