---
title: "How a Leading FinTech Company Leverages Redis Enterprise to Boost Uptime and Quadruple Throughput"
linkTitle: "How a Leading FinTech Company Leverages Redis Enterprise to Boost Uptime and Quadruple Throughput"
url: "/blog/how-a-leading-fintech-company-leverages-redis-enterprise-to-boost-uptime-and-quadruple-throughput/"
description: "Alice loves to flash her favorite clothing store’s corporate credit card. As a frequent shopper, Alice receives points for her purchases that she can redeem for discounts, free shipping, and other..."
date: 2020-02-13
blogCategories:
- "Company"
authors:
- "Miguel Allende"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Miguel Allende, Customer Advocacy Manager · Published 13 February 2020 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

![](/images/site-mirror/1f454240fda8bbde19298809dca9ff23e48c26b4-300x191.webp)

Alice loves to flash her favorite clothing store’s corporate credit card. As a frequent shopper, Alice receives points for her purchases that she can redeem for discounts, free shipping, and other perks. And the benefits go both ways—the store can collect information about her shopping habits to tailor its marketing, loyalty programs, and promotional materials.

The liaison between Alice, the clothing store, and the branded credit card is a leading fintech company, which manages more than 300 branded credit card programs and their integrated marketing campaigns. This fintech firm recognized that the aging content management system it used to run those campaigns was lagging compared to its competitors. The company needed a high-performing, scalable, and stable database to manage all customer information and marketing campaigns, as well as scale a more efficient client-onboarding process.

The database also needed to provide all the normal credit card services so customers like Alice could enjoy a seamless experience. An outage—or even more detrimental, a data loss—would be a major problem, damaging the company’s services and reputation as it competes with other fintech firms focusing on technological innovation.

## Redis Enterprise means low-maintenance operations

Before switching to Redis Enterprise, the company relied on a monolithic architecture nearly a decade old. The IT team decided to transition to a microservices architecture to improve scalability and allow for specific parts of its content management system to be updated independently. The transition—which took close to a year and was completed in November, 2018—encouraged the team to look for new highly available solutions. The team eventually settled on Redis, MongoDB, and Couchbase, each powering a different use case.

Redis stood out, though, for being super easy to set up and maintain. Redis Enterprise removes business operations from the forefront of the team’s minds. Letting them focus on innovation instead of “How do we operate?”

The team was thrilled and surprised that Redis Enterprise installation was completed in only two days, just as promised. They quickly learned that training developers—even those who had never used Redis before—was similarly fast and intuitive. The ability for a developer to go from never-heard-of-Redis to actually being hands-on in the code and contributing to the project was a huge differentiator, according to the team.

Because of Redis Enterprise’s low maintenance requirements, operations issues are no longer top of mind for the team, allowing it to streamline client onboarding and profitably serve less-lucrative clients it would once have had to pass over.

## Big changes at scale

It’s a big change for a massive application. The company’s content management system pushes out more than 200,000 publishing transactions an hour. The repository contains millions of snippets of personalized content for each client’s brand.

Redis Enterprise powers the queueing system that sends that content out to customers. With just two 3-node clusters across a pair of data centers, the company processes roughly 1,000 ops/sec, while also syncing communication between the company’s publishing and deployment servers. Since transitioning to Redis Enterprise, the company has enjoyed dramatic performance improvements. Throughput is 4 times faster, and system uptime jumped from 70% to almost 99%. And Redis Enterprise has also enabled the company to scale up more efficiently by minimizing its database footprint—a single 3-node cluster supports as many as 200 web application servers at any time.

Critically, the performance improvements are also helping speed the company’s time to market, because it’s able to publish content faster. When it needs to get a marketing campaign or banner out there right away, the tool no longer slows the team down. It helps them get there faster.

## Future solutions with Redis Enterprise

One member of the firm’s team called Redis Enterprise a “fire hose” because it’s always putting out fires. But even as the company relies on Redis Enterprise to solve today’s problems and help streamline its content management system, it plans to standardize on Redis Enterprise as its primary enterprise caching tool, replacing Oracle Coherence. The team is also hoping to develop a chatbot application using Redis Enterprise.

*Looking to learn more about *[*microservices architectures*](/docs/redis-microservices-for-dummies/)*? Check out how *[*Mutualink*](/blog/how-mutualink-uses-redis-to-support-a-life-saving-microservices-architecture/)*’s microservice architecture helps save lives and how online travel agency *[*HolidayMe*](/blog/how-holidayme-uses-redis-enterprise-as-its-primary-database/)* uses Redis as a primary database.*
