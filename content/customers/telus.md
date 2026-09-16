---
title: "TELUS’ Optik TV service gains greater reliability with Active-Active Redis"
linkTitle: "TELUS’ Optik TV service gains greater reliability with Active-Active Redis"
url: "/customers/telus/"
description: "TELUS had deployed Redis open source, but ran into challenges managing and maintaining Redis availability for their mission-critical applications on Optik TV. TELUS experienced an outage for their..."
group: "Telecommunications"
lastmod: 2025-09-12
hidden: true
mirrored: true
---

*updated 12 September 2025*

###### Challenge

TELUS had deployed Redis open source, but ran into challenges managing and maintaining Redis availability for their mission-critical applications on Optik TV. TELUS experienced an outage for their customer-facing application Showcase that led to a negative customer experience which included leaving key menu options unavailable and ultimately required significant time to fully restore all services to customers.

###### Solution

After experiencing these availability issues for critical customer-facing features, TELUS migrated to Redis Enterprise to support the Showcase application. The application required greater availability and failover support as Showcase acts as a central hub of personalized content for TELUS’ Optik TV customers to discover what they’re most likely going to watch next.

###### Benefits

Once Redis Enterprise was deployed to the Showcase application, TELUS saw significant benefits in resilience, reliability, and overall performance of the application. This resulted in easier, more reliable operations as part of TELUS’ DevOps processes as well as a better customer experience thanks to Active-Active Redis. Even a Redis service disruption was not noticeable to Optik TV customers. Additionally, the Showcase application’s two second load performance SLA has only been achieved with Redis Enterprise as the caching solution.

> For us, it wasn’t the dollars and cents business case. It was the operational availability of support and the fact that Redis Enterprise offered high availability without manual intervention.

[TELUS](https://www.telus.com/en/) offers streaming TV to more than 1.5 million customers in Western Canada and Quebec through their [Optik TV](https://www.telus.com/en/tv/optik) IPTV product. The company’s technology strategy team oversees third-party integrations with Optik TV, such as Amazon Prime, Netflix, and other streaming services.

*Showcase* is an Optik TV application that provides customers with seamless access to all of their local and streaming content. *Showcase* is designed to allow people to discover new Video On Demand content, watch recordings and new episodes, follow their favorite TV shows, or even jump back into watching incomplete episodes with ease*—everything* is accessible. 

Streaming TV viewers expect real-time performance. That’s why *Showcase* was originally built on Redis open source. The goal was to use Redis as a fast mechanism to transfer data onto the set-up box efficiently because no other database was capable of supporting the amount of data being transferred with the lowest possible latency.

According to Steve Allen, Manager, Technology Strategy at TELUS, “Due to the amount of information we present to just one customer through Showcase, it would be impossible for us to tune another database to be fast enough. When the Showcase project was initiated, we concluded either we use Redis, or we can’t get the application to load for the customer in three seconds or less.”

### One outage. One lost business day. And a hampered user experience.

*Showcase* utilized two Redis deployments, one located in Edmonton and another in Calgary. TELUS configured the cache to use an active-passive approach, with a primary Redis Cluster in Edmonton and a replica in Calgary. 

*Showcase had been relying on Redis* *open source* *for four years successfully, yet when a failure occurred,* it took TELUS’ technology team a full business day to manually get a cold standby spun up*—*a task that was both time-consuming and tedious. And the longer a service disruption takes to resolve only results in increased damage to customer experiences and brand reputation.

With *Showcase*’s performance on the line, TELUS knew they needed an enterprise-grade cache that offered greater reliability and failover to avoid future lengthy service disruptions. The outage had put the *Showcase* service on standby for a full day, but the team had already paid the heaviest price*—*a hampered user experience that lasted up to 24 hours.

Understandably, leadership was concerned as to how this kind of incident could happen in the first place and stressed the importance of a proper post-incident evaluation.

### Adopting a database devs and ops can love

A few months after the *Showcase* service disruption, Steve Allen took over as manager of *Showcase*’s development team. Having experienced the incident first-hand as a developer on the team, Allen was already familiar with the struggles that came with running such a dense application on Redis *open source,* and the potential consequences should downtime occur.

“TELUS has been on a DevOps journey for the past six years, so that has brought the development and operations sides closer together, and we aren’t throwing features over the wall and leaving operations to sort out,” says Allen. “We’d been looking at our vulnerabilities from an operational response if systems went down, and Redis was a prime one to look at given how heavily it is used for our premier application.”

Between the recent events with the *Showcase* application and the overall focus on streamlining development and operations, it was a perfect time for the development team to migrate from open source to Redis Enterprise and set the team up for success and scale. 

Allen shares, “For us, it wasn’t a simple dollars and cents business case. It was the operational availability of having enterprise customer support and the fact that Redis Enterprise offered high availability without manual intervention.”

And Redis Enterprise can seamlessly process a high volume of data in real-time with high availability for the hundreds of millions of transactions per month that *Showcase* generates.

“Our monitoring stance on caching, especially around Redis, has gone from essentially nothing, to at a very high level, is the first system we know about when there’s an issue,” Allen adds.

### Redis Enterprise showcases the TELUS IT team

Several months after deploying Redis Enterprise, another major incident occurred when the link between servers in Edmonton and Calgary broke, causing TELUS to lose connectivity to all of their servers in Calgary. If TELUS had not installed Redis Enterprise, the outcome would have been catastrophic because the servers weren’t available to migrate back to Edmonton.

However, TELUS and their customers not only didn’t experience an outage, they didn’t even know the failure had occurred. Redis Enterprise’s cluster management system sent an alert before any other internal TELUS system about the disruption to the Calgary server.

This is thanks to Redis Enterprise’s [Active-Active geo-distribution](https://redis.io/active-active/), which enabled TELUS to navigate the outage with zero downtime or impact on the application. Both the Edmonton and Calgary Redis Enterprise clusters function as primary deployments and operate with a single endpoint. Traffic is automatically routed only to healthy clusters.

Allen notes, “The recovery process for where we were at two years ago with an outage*—*it would have taken us weeks to recover. With Redis Enterprise, we didn’t notice any issues. We just got an influx of alerts from Redis, and we were able to work it out. Losing Redis would impact a dozen of our applications for a full day, which isn’t out of the realm of possibility if we had still been on open source.”

Thanks to Redis Enterprise’s reliability and ability to scale with ease, TELUS now has greater confidence across the company in the performance of the Optik TV applications. This has enabled the Technology Strategy team to showcase their skills to deliver an extensive range of applications relying on Redis Enterprise, and the use cases only continue to expand.

Allen concludes, “We now have a significant number of applications beyond *Showcase* relying on Redis Enterprise because we’ve been able to gain greater confidence in our systems and approach to caching. We’ve shielded ourselves from customer calls and leadership escalations if there ever is a failure in our systems moving forward.”
