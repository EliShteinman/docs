---
title: "Procesio cut latency by 60% with Redis Cloud & unlocked real-time automation"
linkTitle: "Procesio cut latency by 60% with Redis Cloud & unlocked real-time automation"
url: "/customers/procesio/"
description: "As Procesio grew, its architecture shifted from a monolith to a more flexible microservices model. This shift created a critical challenge: their MySQL database couldn’t provide the low-latency..."
lastmod: 2025-08-01
hidden: true
---

*updated 1 August 2025*

###### Challenge

### Scaling pains & performance bottlenecks

As Procesio grew, its architecture shifted from a monolith to a more flexible microservices model. This shift created a critical challenge: their MySQL database couldn’t provide the low-latency data access needed for real-time service communication. At first, the team used a basic, open-source Redis cache, but as platform usage surged, a new problem emerged.

"When the platform reached a certain number of users, we started processing millions of actions per day," says Alexandru Gal, CTO at Procesio. "We saw that from time to time, there was some data loss. We couldn't find some values in the cache." Data loss was not an option for a platform handling critical enterprise processes like real-time e-invoicing for the Romanian government. The team needed a solution that could guarantee both speed and 100% data integrity at scale.

> Redis is the backbone of Procesio. Its speed and reliability are fundamental to our promise of being the world's fastest automation platform. From handling mission-critical government invoicing to empowering our partners to innovate, Redis gives us the performance we need to scale without compromise.”

###### The solution

### High-throughput caching for real-time speed

Procesio didn’t pick Redis Cloud just for caching. They needed a solution that met a very specific demand: massive throughput with a relatively small data footprint. "What we need is high throughput of data," Alexandru explains. "Because of that, we need to choose a very performant system."

Redis Cloud offered a cost-effective plan built for Procesio’s unique requirements, providing high throughput at a lower cost than the standard offerings from their cloud service provider. "It was a very good selling point to our management team," adds Alexandru.

### Automation platform architecture

![Automation platform architecture](/images/site-mirror/aba6085056a3c5472658ecd841cd358885f29ab9-843x436.svg)

Redis Cloud was integrated as the central, high-speed caching layer for Procesio's multi-cloud architecture. It now serves as the backbone for the entire platform, caching process templates and execution states that need to be accessed by microservices in milliseconds. This ensures that whether the platform is deployed on AWS, Azure, or on-premises, its performance remains consistently fast.

###### The impact

### Drastic performance gains, unshakeable reliability, & lower costs

To deliver on its promise of being the world’s fastest automation platform, Procesio turned to Redis Cloud. The migration delivered three key benefits:

##### Unlocking real-time performance at scale

At Procesio's scale, speed is a feature. By caching frequently accessed data, Redis Cloud slashed execution latency by up to 60% and reduced calls to the primary database by over 80%. This raw performance is critical for enterprise use cases like e-transport, where goods must be registered with government systems in near real-time to avoid costly fines.

“Using a fast caching system allows us to create faster processes, faster integration systems, faster ways of asking this information,” says Alexandru. “Having Redis in the core of processing things improved everything.”

##### A more flexible and powerful platform

The reliability and speed of Redis Cloud have given Procesio’s engineering team the confidence to build more complex and powerful features. Redis’s performance underpins Procesio's unique architecture, which uses a dynamic "collection of variables" to pass data between process steps—a model that offers far more flexibility than traditional automation platforms.

This foundation for innovation is critical as the company adds a new feature nearly every week. "Now that we are exploring Redis, we can count on the features that Redis offers to support our roadmap, and that's invaluable for us," notes Alejo Roze, Head of Partnerships at Procesio.

##### How Procesio saved on costs and eliminated risk

Since moving to Redis Cloud, Procesio has eliminated the data loss incidents that occurred with its previous caching solution, even while doubling platform usage in just three months. This has solidified customer trust and de-risked the platform for mission-critical operations.

"Our clients put their faith in us that we deliver the data on time. We don't delay it, we don't lose it," says Alexandru. "It's not a high risk to use Processio; it's a very safe choice." This reliability, combined with a significant reduction in database load and a cost-effective Redis Cloud plan, has lowered overall infrastructure costs while simultaneously boosting performance.

### Redis: the backbone of Procesio's high-speed automation

For Procesio, Redis Cloud is more than just a cache—it's a strategic component that enables the company's core value proposition of speed and reliability. It allows the engineering team to innovate faster, support increasingly complex customer demands, and scale without fear of hitting a performance wall.

Redis is now critical to how Procesio innovates fast and scales reliably. It provides the:

- **Scalability** to handle explosive growth and process millions of daily actions.
- **Performance** to deliver latency of <50 milliseconds for a seamless, real-time user experience.
- **Efficiency** to dramatically reduce database load and lower operational costs.
- **Reliability** to guarantee data integrity for mission-critical enterprise apps.
