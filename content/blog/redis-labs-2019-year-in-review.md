---
title: "Redis Labs’ 2019 Year in Review"
linkTitle: "Redis Labs’ 2019 Year in Review"
url: "/blog/redis-labs-2019-year-in-review/"
description: "Is it just us, or did 2019 seem to fly by? Maybe it just seemed that way because 2019 was such a big year for us here at Redis: We continued to invest heavily in Redis Open Source and its..."
date: 2019-12-30
blogCategories:
- "Company"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 30 December 2019 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/2cd9a200ead6a67c8b10a73a3538fbbdb8494aee-500x316.webp)

Is it just us, or did 2019 seem to fly by? Maybe it just seemed that way because 2019 was such a big year for us here at Redis: We continued to invest heavily in Redis Open Source and its ecosystem, we introduced important new features to Redis Enterprise, partnered with Google Cloud to offer Redis Enterprise as a native service on the GCP console, hosted events all around the world, welcomed legions of new customers, grew our staff and bolstered our executive team, and much more.

And as 2020 rolls into town, we’re proud to say that Redis is still the fastest NoSQL database, still the most-loved database by developers, still the #1 database container, and the [#1 cloud database](https://www.sumologic.com/brief/state-modern-apps-report/). The Redis world has a lot to look forward to in the new year, including more proof of how development and operations teams are increasingly taking Redis beyond caching to serve as a primary database powering their most critical applications. In the meantime, here’s a recap 2019’s biggest and most memorable moments:

## Product developments

2019 saw slew of big announcements for Redis Enterprise, further demonstrating that the power of Redis goes beyond just caching.

We started the year by announcing that [Redis Enterprise for Intel Optane DC persistent memory](/press/redis-labs-delivers-fastest-multi-model-database-intel-optane-dc-persistent-memory-3/) was available across multiple cloud services or as downloadable software. Compared to a traditional DRAM-only memory configuration, Redis Enterprise on [**Intel Optane**](/press/redis-enterprise-intel-optane-dc-persistent-memory-offers-cost-effective-scaling-petabytes-2/) offers comparable performance with up to 40% memory cost savings.

We continued by announcing several new modules designed to enrich the data models and use cases supported by Redis:

- [**RedisTimeSeries**](/blog/redistimeseries-ga-making-4th-dimension-truly-immersive/) was built for time-series use cases where fast data ingest and real time complex queries are important.
- [**RedisAI**](/blog/redis-ai-first-steps/) (now in beta) significantly improves AI serving by running your trained models close to your data (in Redis) and across multiple AI platforms like TensorFlow, PyTorch, and ONNX runtime.
- [**RedisGears**](/blog/introduction-to-redisgears/) (also in beta), is a serverless platform that enables infinite programmability options in Redis, across data models and shards.

We then introduced [**RedisInsight**](/insight/), a free(!) browser-based UI and management system designed to help ease Redis deployments. Finally, [**RedisEdge**](/blog/redisedge-iot-database-for-edge-computing/) enables deploying Redis on tiny Raspberry Pi-based edge devices while processing hundreds of thousands of events per second with enhanced functionality, including RediStreams, RedisTimeSeries, and RedisAI— programmable with RedisGears.

We also set a new performance standard for Redis Enterprise. In our latest benchmark published in June, Redis Enterprise delivered more than [**200 million ops/sec**](/blog/redis-enterprise-extends-linear-scalability-200m-ops-sec/), with less than 1 millisecond latency, on as few as 40 AWS instances. This represents a 2.6X performance improvement from our previous record in just 15 months!

During 2019 we also invested in enterprise-grade Kubernetes deployment of Redis. **Redis Enterprise Operator** ensures that your cluster is properly utilizing the Kubernetes Stateful Set with support for anti-affinity, multi-AZ (failure domains), rolling upgrades, and Active-Active deployment across multiple Kubernetes clusters. And we recently announced **Automated Cluster Recovery**, which not only improves the availability of your Redis deployment but also allows users to manage a stateful service as if it were stateless. Our Kubenetes distro is available across all the leading Kubernetes platforms: GKE, AKS, EKS, PKS, RedHat OpenShift, and native Kubernetes.

![](/images/site-mirror/74b7b8df7e0adca2cea0c4d0cddddaeea5a435d7-1362x619.gif)

Furthermore, we worked hard to help customers use Redis Enterprise across multiple clouds in just a few clicks, with the unification of Redis Enterprise Cloud and Memcached Enterprise Cloud into [**Redis Cloud Essentials**](/blog/introducing-redis-cloud-pro-essential-versions/). We also renamed Redis Enterprise VPC as **Redis Cloud Pro**, supporting Active-Active, Redis on Flash, and modules.

## Redis Enterprise as native service on Google Cloud

At Google Cloud Next, Google Cloud CEO Thomas Kurian invited me [on stage to announce](https://www.youtube.com/watch?v=ciA5C6mfBuo) an expanded partnership with the goal of giving our joint customers a simplified and streamlined experience for building and running modern high-performance applications. A few months ago we announced the first step of this cooperation by making Redis Enterprise available on the [**Google Cloud Marketplace**](/blog/redis-enterprise-google-cloud-platform-marketplace/), and allowing Google Cloud customers to consume enterprise grade Redis services with their existing Google credit.

## Continued massive investment in open source

2019 officially marked Redis’ [**10th open source anniversary**](/blog/redis-turns-10/), exactly a decade since Redis was first shared on [Hacker News](https://news.ycombinator.com/item?id=494649).

During 2019 we continued our strong investment in the Redis core and its ecosystem, and to round out the year, Redis Creator Salvatore Sanfilippo announced the first release candidate of [**Redis 6**](http://antirez.com/news/131) in December. Some of the new features include SSL, ACLs, RESP3, client-side caching, new module APIs, a better expire cycle, a new distributed-queue capability with Disque modules, and more.

We’ve also made it easy to demonstrate your mastery of Redis with our new [**Redis Developer Certification**](/blog/redis-developer-certification-is-here/) program, which launched in November. Getting certified shows you’ve mastered a wide variety of Redis skills, and passing the exam earns you a digital badge and certificate—perfect for LinkedIn and job applications.

## Events: Redis around the world

In April we held our [fifth annual ](/blog/wrap-redisconf-19-recap/)[**RedisConf**](/blog/wrap-redisconf-19-recap/), gathering more than 1,500 Redis Geeks on San Francisco’s Pier 27. Attendees were treated to special keynotes from Redis creator Salvatore Sanfilippo and Redis Co-founders Ofer Bengal and Yiftach Shoolman, plus more than 100 breakout sessions led by Redis experts and customers as well as world-class networking. Be sure to save the date for [RedisConf 2020](/redisconf/), coming May 12-14 at SVN West in San Francisco.

Meanwhile, we brought Redis to you with** Redis Days **in Tel Aviv, New York, and [London](/blog/everything-you-missed-at-redis-day-london/). Attendees boosted their skills in hands-on training days and heard from Redis customers on innovative ways they are using Redis. If you’re in the neighborhood, don’t miss our first 2020 Redis Days in January: [Seattle](/blog/redis-day-seattle-2020/) and [Bangalore](/blog/redis-day-bangalore-2020/)!

![](/images/site-mirror/6c664bc204e3aad843c84f9cd3b78e4ddcf26d6a-2000x1333.webp)

*Redis Day London!*

Finally, at [**AWS re:Invent**](/blog/redis-labs-at-aws-reinvent-2019/), we went all in on the theme Growth Happens: as your company and database needs scale, Redis Enterprise offers the best Redis experience for dealing with that growth smoothly and effectively. We had a blast in Vegas, [interviewing people on the show floor](https://twitter.com/Redis/status/1202746843547029504?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E1202746843547029504&ref_url=https%3A%2F%2Fredis.com%2Fblog%2Fredis-labs-at-aws-reinvent-2019%2F), [watching our sponsored sumo wrestler win the Sumo Logic Slam Jam](https://twitter.com/howardting/status/1202481580238704640?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E1202481580238704640&ref_url=https%3A%2F%2Fredis.com%2Fblog%2Fredis-labs-at-aws-reinvent-2019%2F), and [hearing top customers](/blog/what-gap-and-alliance-data-say-about-the-power-of-redis-enterprise/) like Gap and Alliance Data share how they get the most from Redis Enterprise.

![](/images/site-mirror/d402f03bcbca0025ed2b9c77724bc108b407aa95-2560x1252.webp)

*A standing-room-only audience takes in a presentation at the Redis booth at AWS re:Invent 2019.*

## Company milestones

We’re excited to continue building Redis for the next decade, fueled by our [**$60 Million Series E**](/press/redis-labs-raises-60-million-series-e-financing-bring-instant-experiences-everywhere/) funding round led by Francisco Partners in February, bringing our total funding to $146 million.

And in April, we announced that [Redis ](/press/redis-labs-delivers-confidence-speed-enterprises-microsoft-azure/)[has achieved co-sell ready status through the Microsoft One Commercial Partner program](/press/redis-labs-delivers-confidence-speed-enterprises-microsoft-azure/)[, ](/press/redis-labs-delivers-confidence-speed-enterprises-microsoft-azure/)an elite group of independent software vendors selected by Microsoft for intensive joint sales, support and go-to-market initiatives.

We also expanded our workforce and leadership team! In January, Alvin Richards, previously Chief Education Officer, was promoted to Chief Product Officer. In February, Rafael Torres joined as CFO and, in April, Howard Ting was named Chief Marketing Officer. Overall, **the Redis team grew more than 50%** in 2019!

We’ve also proud to serve all the customers who adopted Redis Enterprise in 2019. Our momentum in the Fortune 1000 continued to increase, with companies such as [Deutsche Börse](/customers/deutsche-borse/), which expanded its use of Redis Enterprise as an intelligent cache to rapidly process and organize data, and Turner Broadcasting, which has boosted its real-time analytics performance and uses Redis Enterprise to help ingest data quickly. And we’re especially excited about the dramatic increase in organizations using Redis Enterprise as a primary database, such as [HolidayMe](/blog/how-holidayme-uses-redis-enterprise-as-its-primary-database/) and Charter Communications.

## Awards and accolades

It’s also nice that other folks noticed our big year. Redis was named to a number of key industry lists in 2019, including [**Deloitte’s North America Technology Fast 500**](/press/redis-labs-named-to-deloittes-north-america-technology-fast-500-third-consecutive-year/) (for the third consecutive year!) and as a [**Leader by Forrester in the NoSQL Wave**](/press/redis-labs-recognized-leader-independent-analyst-report-big-data-nosql-platforms/).

Even more important, perhaps, [**Redis was named most-loved database**](/blog/redis-named-loved-database-third-consecutive-year/) for the third consecutive year in Stack Overflow’s 2019 Developer Survey. Plus we were also named to Gartner’s January 2019 [**Peer Insights Customers’ Choice**](/blog/redis-labs-named-january-2019-gartner-peer-insights-customers-choice-operational-database-management-systems/) list, based on how our customers review their experiences with us. In less than a year, we received more than 100 reviews while maintaining a 4.6 ranking.

We’re especially proud of accolades that celebrate our workplace culture. [**Redis was named a great place to work on 3 continents**](/blog/redis-labs-a-great-place-to-work-on-three-continents/), earning a place on Deloitte’s EMEA Fast 500 list, Dun & Bradstreet’s list of 10 best startups to work in Israel, and in Sequoia Consulting Group’s 2019 Healthiest Employees of the Bay Area program. Earlier in the year, global investment firm Battery Ventures included Redis on its list of [**50 Highest Rated Private Cloud Computing Companies to Work For**](/press/redis-labs-named-one-50-highest-rated-private-cloud-computing-companies-work/), which ranks companies based on Glassdoor employee feedback.

## Redis content

2019 was a great year for Redis-related content of all kinds, highlighted by the publication of our new ebook—[**Redis Microservices for Dummies**](/docs/redis-microservices-for-dummies/)! Written by Developer Evangelists Kyle Davis and Loris Cro, this free 64-page volume can help you understand the fundamentals of a microservices architecture and how to use Redis to optimize your data layer to make your apps more scalable.

And finally, to help the Redis community stay up to date, we relaunched two newsletters in 2019: RedisWatch and Redis Enterprise. Subscribe to the **Redis Watch** newsletter for a monthly dose of technical goodness on everything Redis. Sign up for our **Redis Enterprise** newsletter—relaunched in December—for the latest on Redis, including product updates event highlights, top blog posts, and more.

2019 was a great year for Redis and Redis, and we owe it all to the incredibly vibrant community of developers, operations teams, and DevOps practitioners who use Redis and Redis Enterprise to address an incredible variety of business and technical use cases—not to mention Redis’ customers, partners, and dedicated roster of employees. We’re excited to continue building and growing Redis Enterprise as a primary database powering the most critical applications. We can’t wait to see what 2020—and the new decade—brings.
