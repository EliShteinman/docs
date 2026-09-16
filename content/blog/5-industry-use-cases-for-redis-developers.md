---
title: "Redis Use Case Examples for Developers"
linkTitle: "Redis Use Case Examples for Developers"
url: "/blog/5-industry-use-cases-for-redis-developers/"
description: "Redis has a great reputation – but where’s it used? Developers rely on Redis Enterprise for critical use cases across several industries. Learn several scenarios where Redis has made a difference..."
date: 2022-07-12
blogCategories:
- "Tech"
authors:
- "Ajeet Raina"
lastmod: 2026-06-01
hidden: true
mirrored: true
---

*By Ajeet Raina, Technical Marketing Manager · Published 12 July 2022 · updated 1 June 2026*

![Blog tile image](/images/site-mirror/410736c7b5cc2709de8898b79b1f69024a30fe59-4899x3062.webp)

**Redis has a great reputation – but where’s it used? Developers rely on Redis Enterprise for critical use cases across several industries. Learn several scenarios where Redis has made a difference in application development for gaming, retail, IoT networking, and travel.**

How are developers using Redis for their database needs? We began as Redis open source, but in the subsequent [13 years](/blog/redis-architecture-13-years-later/), the must-haves for any growing digital business have shifted, and now what’s required is more of everything. That means more availability, more [persistence](/blog/importance-of-database-persistence-and-backups/), and never any room for lags in performance, so add backup-enabled and instant failover to the mix of required features.

Painless business scalability is an objective goal for any programming team. Building applications with an in-memory Redis [cache](/solutions/caching/) and Redis database cuts through complexity and latency since [Redis Enterprise ](/try-free/)provides dual support in a single system.

Everything comes down to speed. It means faster application interactions (such as quick data retrieval and a balanced load of backend services with caching) and software that scales on user demand ([build low latency microservice architectures](/solutions/microservices/) with Redis’ multi-model database).

Let’s explore some popular Redis uses and customer real-world Redis performance examples.

## Fast fraud detection for real-time decisions

[Click here to view video](https://www.youtube.com/embed/MGFpnvtPZcE)

Fraud costs money, and the cost is only going up. Opportunists follow the growth, leading them to the digital space, with [retail](/industries/retail/), [gaming](/industries/gaming/), and [finance](/industries/financial-services/) among the verticals hit hardest by fraudsters. “Every $1 of fraud now costs U.S. retail and e-commerce merchants $3.75,” a [LexisNexis](https://risk.lexisnexis.com/insights-resources/research/us-ca-true-cost-of-fraud-study/) report asserts; that’s up 19.8% since 2019)

[BioCatch](/customers/biocatch/) is an Israeli digital-identity company that uses groundbreaking biometrics tracking to stay ahead of fraudsters. As the company’s business rapidly grew to 70 million users, 40,000 operations per second, and 5 billion transactions per month, the BioCatch team needed a way to deal with significant database scaling issues.

This isn’t a unique challenge. Online transactions soared as a result of COVID-19. According to Morgan Stanley’s global[ e-commerce growth forecast](https://www.morganstanley.com/ideas/global-ecommerce-growth-forecast-2022) 2022 report, the market is estimated to soar from $3.3 trillion today to $5.4 trillion by 2026. With that growth comes cybersecurity dangers: digital identity threats, cybercrime, and customer fraud. Phishing and counterfeit pages increased by 53% in 2021, reports[ Bolster.AI](https://boost.bolster.ai/rs/540-rfh-299/images/2022_phishingandfraudreport.pdf/).

Your data layer needs lightning-fast speed to build finely-tuned [fraud detection ](/industries/financial-services/)algorithms that respond in under 40 milliseconds before anything can negatively influence the customer experience.

Data breaches have become their own epidemic. IBM reports that 83% of organizations have had multiple data breaches. The average cost of each instance is approximately $4.3 million. The United States earned the top spot for the 12th year in a row for countries with the highest average total cost of a data breach.

The increased complexity, volume, and sophistication of threats require more advanced fraud detection methods to keep up with malicious actors and build more substantial fortifications against them. Because traditional data platforms often struggle to keep up with modern online transactions’ speed, scale, and complexity, it is difficult to detect and stop fraud in real-time.

In need of blazing performance, high availability, and seamless scalability from its data layer, BioCatch turned to[ Redis Enterprise](https://www.youtube.com/watch?v=JWX0j6z7hoU) to decouple the compute from the data. After initially considering Redis Enterprise as a cache, the team soon realized that Redis would also make a great system configuration NoSQL database.

BioCatch uses Redis features, and various [data structures](/redis-enterprise/data-structures/) to create a single source-of-truth database that serves mission-critical information across the entire organization. BioCatch captures behavioral, meta, and API data during active user sessions. It also creates user behavior profile subsets and predefined fraudulent-behavior profiles.

With 3 petabytes of data, 300 million keys, and 40 databases running on [Microsoft Azure](/cloud-partners/microsoft-azure/), BioCatch relies on Redis Enterprise to serve data for all its microservices. Since operating with our enterprise-grade Redis cache, BioCatch has had zero downtime and no operational hassles, giving its team breathing room to focus on the strategic projects that serve its core mission.

Learn more about real-time fraud detection and exabyte analytics in our Data Economy podcast vlog.

## Modern gaming experiences

In 2021, the global gaming market topped $198.40 billion and is expected to reach a value of $339.95 billion by 2027, according to[ Mordor Intelligence](https://www.mordorintelligence.com/industry-reports/global-gaming-market). This massive estimated growth is due in large part to[ mobile gaming](/industries/gaming/).

Successful mobile games require a great user experience, which can post significant infrastructure challenges, especially for real-time multiplayer games. Users must be able to launch the game, connect to a server, and collaborate with other players; any lag or hiccup can ruin the experience. The gaming experience also includes transactions in real-time, sometimes with real money involved. For the customer, the expectation is an immediate transaction, with personal payment details cached at the ready.

![](/images/site-mirror/5c2b7c7fb64081a0d363e4ef300e96694ef91cf4-1024x520.webp)

*Redis Enterprise for game developers*

Developers rely on Redis’[ low latency](/blog/how-to-reduce-latency-and-minimize-outages/) to deliver high performance and virtually unlimited scale critical in gaming situations where large volumes of data arrive at high speed. Take[ fantasy sports](https://www.globenewswire.com/news-release/2022/07/26/2486049/0/en/fantasy-sports-market-worth-us-47940-million-by-2028-research-reports-with-global-analysis.html/), for instance, which is estimated to become a $48 billion market by 2028. American football is the most popular fantasy sport in the United States, with 35 million players. But that pales in comparison to India’s fantasy cricket leagues, which stand at around 100 million players, according to a [study](https://descrier.co.uk/culture/sport/which-fantasy-sports-are-the-most-popular/) by the Federation of Indian Fantasy Sports (FIFS).

In India, teams release their game rosters before a match, and online players only have 10-15 minutes to update their respective fantasy teams. This is a massive amount of data to intake, and it should not impact the customer’s experience, especially when time is of the essence.

For game developers, serving game elements such as graphics, pictures, thumbnails, and music requires a robust caching solution that can reduce the load on datastores operating on a relational database such as[ MySQL](/docs/modernize-your-mysql-database-with-redis-enterprise/) while ensuring blazing fast response times.

Caching helps provide a responsive user experience with minimal overhead. Case in point: Scopely.

Scopely, which makes mobile games like[ The Walking Dead: Road to Survival,](https://scopely.com/game/the-walking-dead/) relies on Redis Enterprise for various needs, including[ leaderboards](/solutions/leaderboards/), API management, and queue workload management.

Scopely needed to support a variety of data structures and features, such as customizable expiration, eviction, intelligent caching, request pipelining, data persistence, and high availability. These needs can’t be fulfilled with a [SQL database](/blog/nosql-data-modeling/), not without the need for a complex load balancing cluster.

Discover more detailed information in our e-book,[ Why Your Game Needs a Real-Time Leaderboard](/docs/why-your-game-needs-real-time-leaderboards/).

## An omni-channel e-commerce framework

Creating a comprehensive digital presence as an online business is a massive endeavor with a steep learning curve. An excellent digital business needs a backend that ensures store pages are available, an[ inventory management ](/solutions/real-time-inventory/)system, a rapid-speed cache for autocomplete functions to the site, a [search engine ](/search/)for products, and machine learning technology for creating personalized customer experiences in real-time. And it all must be performant; according to a 2020 YOTTA [study](https://www.yottaa.com/download-content/?type=ebook&fid=10046&vid=&vidid=&form=https%3a%2f%2fspeed.yottaa.com%2fl%2f730313%2f2020-07-28%2f6xmr1), 90% of shoppers say they will abandon a site if it is too slow.

However, modern multi-channel retailers are turning to [real-time inventory systems](/solutions/real-time-inventory/) to optimize their inventory, yield, and supply-chain logistics, with the aim of improving the customer experience and supply chain. Building and maintaining these complex systems is daunting for application developers.

Here too, performance is critical. Delayed or inaccurate inventory information can frustrate customers, leading to[ shopping cart abandonment](https://www.dynamicyield.com/blog/shopping-cart-abandonment-ebook-announcement/) (an $18 billion problem of its own) and order cancellations, lost revenues, higher costs, and brand damage.

![](/images/site-mirror/0c5cbd3f897e3d2034323657f9fcb3efc3c5a209-600x766.webp)

*The Gap’s real-time inventory use case*

Apparel retailer[ Gap Inc](/blog/what-gap-and-alliance-data-say-about-the-power-of-redis-enterprise/). wanted to give its e-commerce customers real-time shipping information for each item shoppers added to their carts. The company faced issues with delays and inaccurate inventory information.

This issue created a poor customer experience that inflated costs and eroded brand loyalty.

Application developers at Gap Inc. found Redis Enterprise’s[ linear scalability](/blog/redis-enterprise-delivers-linear-scale-proven-time/) and[ sub-millisecond performance](/blog/10m-opssec-1msec-latency-6-ec2-nodes/) at a massive scale to be a huge assist, particularly for seasonal Black Friday peaks. In microservice environments, fast and flexible [data models ](/blog/nosql-data-modeling/)protect from overprovisioning parts of the infrastructure that are not used during slower periods.

Availability, speed, performance, and experiences: a true 360° omni-channel journey keeps these balls in the air and never lets them drop.

[Click here to view video](https://www.youtube.com/embed/k-deoUp6LsI)

## Unlock new revenue streams with real-time analytics and high-speed data ingestion

In the era of big data, businesses require software that instantly collects, stores, and processes large volumes of data. Yet many of today’s solutions that include a [data ingestion tool](https://redis.io/solutions/fast-data-ingest/) are complex and over-engineered for simple requirements such as streaming real-time data from the internet of things (IoT) and event-driven applications.

In these applications, data must be analyzed quickly to make rapid business decisions. D ata loss is typically not permissible for these use cases.

![](/images/site-mirror/2ac0c5802678eaa8f7398d7508b9064640cfef68-1024x300.webp)

However, data loss does occur, predominantly when working with a relational database. A SQL database is usually created around a known use case at the onset. Introducing another data structure or data model into a SQL stack can bog down the system with slower speed, slower ingestion, and lost data, as the data has to be altered to fit the database’s chosen model.

Lost data equals lost opportunities. Any lost data could be the gateway to an entirely new revenue stream.

A notable Redis usage example of fast data ingestion is [Inovonics](/customers/inovonics/), which provides high-performance wireless sensor networks with more than 10 million devices deployed worldwide. For most of its 30-year history, Inovonics considered itself primarily a wireless technology provider. But the rise of big data helped the company realize that the unique data sets collected by its wireless devices and sensors could also have tremendous value.

Inovonics’ edge platform required robust data platform capabilities for resilience and performance while minimizing the operational footprint and operating costs. With the application of [Redis Enterprise Cloud](/redis-enterprise-cloud/overview/), a fully automated Database-as-a-Service (DBaaS), Inovonics centralized all its data on [Google Cloud](/cloud-partners/google/), opening up new product offerings in the form of insightful, easy-to-access [data analytics](/blog/data-economy-podcast-modernizing-apps/).

![](/images/site-mirror/fea8908696b6a8819b9549a90b7c9673ca89c4f3-1024x531.webp)

*Inovonics solution architecture/flow.*

Inovonics uses Redis Enterprise on its IoT edge devices to push data to its gateways and to the company’s virtual private Google Cloud from those gateways.

On Google Cloud, the application of Redis Enterprise is used for [data ingestion to store](/solutions/fast-data-ingest/) the millions of daily[ messages](/solutions/messaging/) coming from Inovonics’ sensor networks and to provide a central, aggregated view from which to analyze the data. Redis Enterprise also stores the application data model so incoming messages can correlate with representational information such as sensor location.

[Click here to view video](https://www.youtube.com/embed/fbG_1LzUcVo)

## Painless business scalability

In addition to challenging in-store retail, the COVID-19 crisis has forced technology vendors to re-calibrate and customize their operations and application delivery models. To maintain business continuity at scale without any downtime, businesses need the right tools and techniques to scale their infrastructure and accelerate their application response times.

For example, consider [Freshworks](/press/redis-labs-extreme-performance-and-flexible-data-structures-wins-over-freshworks/), which builds cloud-based suites of business software. Due to extraordinary growth over the past six years, the company was straining the capabilities of its application architecture and development operations. As the company’s database load grew, it struggled to maintain performance. Looking to dynamically scale its cluster without compromising availability, the team also wanted to reduce the burden on Freshworks’ primary MySQL database and speed application responses.

After evaluating NoSQL in-memory databases like Aerospike and [Hazelcast](/comparisons/redis-enterprise-vs-hazelcast/), Freshworks chose the high performance and flexibility of Redis. Ultimately, the team chose Redis Enterprise Cloud to ensure high availability and seamless database experience as an infrastructure service for developers.

![](/images/site-mirror/753f5cdbd271db477db791b619468dd440ed5bee-1024x471.webp)

*Freshdesk application server architecture*

In addition to using Redis Enterprise as a frontend cache for its MySQL database, Freshworks uses Redis Enterprise’s highly optimized hashes, lists, and sorted set data structures and built-in Redis commands to meter the API requests coming into its Freshdesk software.

Redis Enterprise also serves as a persistent store for background jobs stored on disk. And as Freshworks transitions to microservices, the company has started to separate critical workloads out of its monolithic Ruby on Rails web application framework. One of the first microservices to result from this effort is dedicated to authentication and uses Redis Enterprise as a [session store](/solutions/session-management/).

Finally, Freshworks leverages Redis Enterprise’s powerful data structures, including HyperLogLog, bitmaps, and sets, as a frontend database for user analytics.

[Click here to view video](https://www.youtube.com/embed/oa1ns12KFhQ)

The case studies above are merely a sample of the use cases where Redis Enterprise is an optimal choice. But there are a few features worth highlighting.

#### Caching

A caching layer stores repeatedly requested data. Ideally, that data is served with a sub-millisecond response time that enables faster loads and eases backend costs.

At an enterprise-grade level, an [in-memory cache](/docs/caching-at-scale-with-redis/) scales linearly across clouds and suffers no performance degradation. Quick data retrieval equals a faster response time for the user. A fast cache also balances backend service loads, allowing existing hardware to operate at peak performance.

(Note: Some Redis service providers, such as[ Amazon ElastiCache](/cloud-partners/aws/), support Redis only as a cache and not as a primary database.)

#### Chat, messaging, and queues

Robust [messaging solutions](/solutions/messaging/) are vital in a microservices architecture. These various collections of services need to communicate with one another in a loosely connected environment.

Messaging protocols such as Pub/Sub aid live broadcasting notifications and are extremely useful for message dispersal when minimal latency and massive throughput are essential. These protocols make a difference. A Sorted Set and Hashes power chat rooms, social media feeds, real-time comment streams, and server intercommunications. Another structure, Lists, can help create lightweight [messaging queues.](https://www.youtube.com/watch?v=hu6Q6s0432A/)

#### Session store

[Session management](/solutions/session-management/) is all about personalization. Applications need to handle high volumes of data, all while caching and retrieving user-profiles and session metadata. With a reliable session store, it’s possible to scale to billions of field-value pairs with sub-millisecond response times and to handle unexpected spikes in traffic.

A [session store ](https://www.youtube.com/watch?v=i69TRwbxk_E)manages session data and improves usability, authentication, user profiles, and logging performance by caching IDs and tokens. This reduces the load on the primary database and computes resources, saving money in the end.

#### Geospatial indexes

[Geospatial data](/glossary/geospatial-indexing/) can integrate location-based features in an application. Common examples including estimating distance, arrival times, and nearby recommendations.

With a geospatial index, it’s possible to store and search for coordinates using a geospatial command, such as GEOADD (to add one or more geospatial items using a Sorted Set, or GEODIST, GEOHASH, and many others.

See what Redis geospatial indexes can do in the video below.

[Click here to view video](https://www.youtube.com/embed/qftiVQraxmI)

## Fast, powerful, easy-to-use. What else do you want?

Developers have to scramble to deliver new applications with compelling features. That keeps them busy, as it’s hard to match the expectations.

To speed time to market, development teams must unlock sub-millisecond response time performance and find easy ways to apply multiple data models to get the freedom they need to build software the right way.

What way will you go when you start building tomorrow’s next great application? Explore these impactful ways to use Redis and build powerful applications with speed and performance.
