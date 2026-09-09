---
title: "Starlogik’s ‘Power of Free’ connects millions on a single Redis Cluster"
linkTitle: "Starlogik’s ‘Power of Free’ connects millions on a single Redis Cluster"
url: "/customers/starlogik/"
description: "Once Starlogik implemented this vision with a handful of African mobile carriers, they faced scalability challenges due to extremely high call volumes processing through their systems and no..."
lastmod: 2025-09-12
hidden: true
---

*updated 12 September 2025*

###### The challenge

Once Starlogik implemented this vision with a handful of African mobile carriers, they faced scalability challenges due to extremely high call volumes processing through their systems and no trustworthy way to load and process all the data generated and store it efficiently in an ongoing manner.

###### Solution

First utilizing open-source Redis before migrating to Redis Cloud, Starlogik sought a managed Database-as-a-Service (DBaaS) which would allow their services to plug into a new cluster that could serve as a short term cache for heavy amounts of data. Further, they set up an architecture to batch process the cached data to a data warehouse for further analyzing, while not interrupting the flow of calls on the frontend of the app and nonstop data entering its systems.

###### Benefits

Utilizing just a single cluster on Redis Cloud, Starlogik has seen an efficient and seamless scaling process that now allows them to process over 110 million calls per day, often totaling thousands of calls per second. Because of the trust the team has in Redis Cloud, they have goals of exceeding one billion calls a day in the future, as the platform has been benchmarked at north of 30,000 transactions per second per node.

> "We love the millisecond latency at scale and wholeheartedly recommend Redis Cloud. It’s a rare high-performance, low cost technology that delivers on its promise."

While the quest for faster data networks grabs the industry focus, it masks some sobering statistics. Over 80% of the world’s population live within existing cellular coverage, [yet only one in two people are connected](https://www.gsma.com/newsroom/blog/understanding-7-billion-counting-connections-and-people/)). Some 90% of people in emerging markets are prepaid users, 30% of which have zero airtime balance on any given day and cannot raise a call. Prepaid, which has dominated the cellular landscape for over two decades, has reached market saturation, with average revenue per user in decline. The next billion users simply cannot afford to feed a phone.

Prior to [Starlogik](https://starlogik.com/)‘s ZRO technology, consumers with zero prepaid balance were barred from ringing, encountering the network error “You have insufficient credit to complete this call”. Starlogik hooks this universal billing exception (known as “insufficient credit”) redirecting this failed voice traffic from the mobile network operator to the Starlogik cloud-hosted switch to permit contact by delivering a single ring at the dialed destination. This breakthrough advance to core signaling and switching exquisitely pivots cellular from prepaid to free allowing zero balance callers to connect freely without credit.

ZRO is literally a cellular ping pong, the lightest most scalable telecommunications protocol ever created, operating uniquely in the natively addressed mass dial stream and instantly available to any caller who has exhausted their prepaid airtime. Consumers simply dial the person they wish to speak to—and with an instant one second flash ring—the call recipient is automatically signaled with a missed call display to prompt a callback.

Starlogik is processing over 110 million calls a day, with over 220 million unique users to-date. They have currently switched over 120 billion total connections and counting. At this scale they are processing at peak thousands of calls per second, which leads to massive amounts of data to process.

![Redis & Starlogik](/images/site-mirror/31df92c9690c1da85052b2f14b9cafe7920a6000-640x524.webp)

### Connecting the Next Billion Voices

From a transactional perspective, Starlogik is handling such a high call volume that much of the database ecosystems on the market were not able to withstand the kind of throughput that they do on a minimal server capacity. In testing out solutions, the team found that most database services (DBaaS) could not withstand the pressure and traffic of these call volumes. They ultimately landed on Redis Cloud, where the cache is implemented on a two-hour rolling basis and then processes are set up downstream to move that data into a warehouse for processing and analytics.

“The technology is carrier grade and the scale we operate at is rare,” notes Ash Brener, Starlogik’s CTO. “A single node can handle north of 30,000 transactions per second, and that’s over a billion calls a day. We’re stimulating billions of minutes of use on the network that never would have transpired from subscribers in states of zero credit.”

Landing with Redis Cloud on AWS was also [a simple plug-and-play approach](https://redis.io/redis-enterprise-cloud/migrate/) for Starlogik. The team built out an exact replica of its database from Amazon ElastiCache on Redis Cloud and pointed its live traffic at this new cluster seamlessly and in under 30 minutes.

“We needed a low latency transactional cache and Redis Cloud has performed brilliantly beginning with the migration to the peace of mind that comes with zero administration.” says Brener. “We love the millisecond latency at scale and wholeheartedly recommend Redis Cloud. It’s a rare high-performance, low cost technology that delivers on its promise.”

### Everybody Benefits Together

For the telecom industry Starlogik’s technology opens a substantial new market demographic and untapped revenue streams for operators while connecting the unconnected.

Results to-date demonstrate how carriers can expand their definition of market boundaries to drive greater differentiation from their competitors and loyalty among customers by utilizing the power of free.

The psychological impact for people who have been marginalized and who discover they suddenly have a new found freedom to make a phone call without economic constraint, has the potential to impact many corners of their lives.

“It takes 6 to 18 months to deploy core services on a mobile network. Starlogik is deployed on a carrier in under 30 minutes,” notes Brener. “There’s no hardware, no software, and no CapEx required. Effectively, we issue our telco partners an IP address and the carrier connects right in.”

In addition to handling the massive transactional throughput that Starlogik requires, Redis Cloud has enabled the company to achieve this global scale on a single Redis cluster. They maintain long reaching goals of plugging as many carriers, on as many continents as possible, into this light cluster. There’s no need for a server room the size of a football field to connect the world.
