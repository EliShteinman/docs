---
title: "MEO turns to Redis and achieves 71% OTT user growth"
linkTitle: "MEO turns to Redis and achieves 71% OTT user growth"
url: "/customers/meo/"
description: "MEO, Portugal’s largest telecom operator, needed to transition from its established internet protocol television (IPTV) system to an over-the-top (OTT) streaming platform. This shift was driven by..."
lastmod: 2025-09-12
hidden: true
---

*updated 12 September 2025*

###### The Challenge

MEO, Portugal’s largest telecom operator, needed to transition from its established internet protocol television (IPTV) system to an over-the-top (OTT) streaming platform. This shift was driven by growing consumer demand for high-quality, on-demand streaming, but it also introduced considerable technical challenges.

Moving from a stable, vendor-supported IPTV system to a complex, multi-layered OTT platform wasn’t simple. It meant integrating over 30 commercial and in-house components into a unified infrastructure, built to handle high-volume data transactions.

MEO needed a fast, scalable solution that could handle high data loads and deliver a smooth user experience across all kinds of devices, including AndroidTV, AppleTV, set-top-boxes, and Android and Apple iOS devices.

> “When pursuing the best quality of service and experience for our customers, we have to have the best-in-class solutions to make sure everything works. Redis has been exactly that for us.”

![MEO building](/images/site-mirror/415af662210699198d7a1b02e41bbb075227bfcb-2664x1609.webp)

### Boosting performance with a new microservices architecture

MEO chose Redis for fast, low-latency, scalable caching that could handle high request volumes and simplify their infrastructure. Redis seamlessly integrated with their microservices and .NET framework, handled high request volumes, and simplified code, resulting in a resilient, future-ready infrastructure.

"The transformation was surprisingly straightforward because our code was already structured for it,” says Cristiano Lima Veiga de Freitas, Tech Lead at MEO. “Redis made it easy to boost performance and scalability, letting us adapt quickly and keep everything running smoothly for our users."

Redis was set up as a caching layer for SQL and NoSQL databases, making data access faster and reducing load on primary data stores. This directly improved read and write performance, service response times, and transaction throughput.

MEO also integrated Redis with Azure for development and testing and VMware on-prem for production and critical services. This made backend interactions fast and helped build an efficient microservices architecture.

These changes were key to powering customer authentication, real-time personalization, and media delivery. MEO maintained seamless performance across devices and grew its OTT platform user base by 71%—from 350,000 to 600,000—in just 14 months.

![Redis](/images/site-mirror/dc0cd698ba5a68971f15291b8fcd1d24545c4ec2-842x494.svg)

### Handling traffic surges during the 2023 Euro Cup

Redis played a critical role in helping MEO manage unprecedented traffic during the 2023 Euro Cup, a major event that saw massive viewership spikes. To handle the anticipated load, MEO scaled its Redis infrastructure by adding four additional shards, keeping things fast and reliable under heavy demand.

During the matches, Redis operated at 94% capacity but maintained flawless performance due to strategic backend caching improvements and optimized cache key time-to-live (TTL) settings. “We reached 184GB of used memory, and while the beginning and end of the game were hard on our backend, it was not noticed by our clients,” says Armando Luis Fernandes Alves, General Director at MEO. “Redis delivered.”

Redis lets MEO deliver a smooth, high-quality streaming experience on any device—even during major events when the pressure’s on.

### Delivering fast, reliable, & scalable OTT experiences

With Redis powering its infrastructure, MEO cut response times in half, made backend call resolutions faster, and delivered near-instant transaction processing. These upgrades transformed its OTT services and cemented its spot as a leader in on-demand streaming.
How Redis helped MEO get ahead:

- **Sub-10-millisecond latency **
50% of requests are now completed in under 12 milliseconds, significantly improving response times for time-sensitive user interactions.
- **Unmatched reliability **
Achieved 99.999% uptime, keeping services running uninterrupted and users happy.
- **Faster transaction handling **
Process tens of millions of daily transactions, with 99% completed in under 350 milliseconds—even during demand surges.
- **Improved high-traffic event management **
Use Redis’ dynamic sharding and flexible TTL configurations to adapt to high-traffic events like major sporting matches.
- **Faster feature delivery **
Development cycles are now 15-20% faster, helping launch new features and updates sooner to meet user demands.
- **Reduced response times **
Cut response times by 50%, boosting performance of critical OTT services and the overall UX.
- **Optimized backend operations **
Improved data flow and reduced backend load by using Redis as a caching layer for SQL and NoSQL databases.
- **Achieved cost savings **
ISaved on infrastructure with efficient memory use and avoided penalties from missed SLAs.

### The bold shift from IPTV to OTT drives 71% user growth

Redis was central to MEO's OTT transformation. It helped reduce response times by 50%, process millions of daily transactions, and deliver reliable performance during high-traffic events like the Euro Cup. With Redis, MEO scaled its OTT user base by 71%—meeting growing demand without any performance degradation.

For devs, Redis streamlines the environment, cuts down on system complexity, and makes iterations faster. This lets MEO focus on building new features and getting them to market faster. The updated infrastructure also positions MEO for long-term scalability, making it easier to keep up with changing market demands and user needs.

MEO’s move to OTT shows how the right tech partner can tackle challenges and fuel growth. With Redis, MEO boosted technical performance, set new benchmarks for reliability and user satisfaction, and paved the way for continued success in the competitive OTT market.
