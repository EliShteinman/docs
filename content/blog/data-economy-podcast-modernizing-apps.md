---
title: "The Data Economy: Modernizing Apps for Real-time Analytics, Streaming, IoT, and AI"
linkTitle: "The Data Economy: Modernizing Apps for Real-time Analytics, Streaming, IoT, and AI"
url: "/blog/data-economy-podcast-modernizing-apps/"
description: "The Data Economyis a video podcast series about leaders who use data to make positive impacts on their business, customers, and the world. To see all current episodes, explore the podcast episodes..."
date: 2022-03-22
blogCategories:
- "Company"
- "Guest Blogs"
- "Podcast"
authors:
- "Isaac Sacolick"
lastmod: 2025-03-27
hidden: true
---

*By Isaac Sacolick, Contributor · Published 22 March 2022 · updated 27 March 2025*

![Blog tile image](/images/blog/0e1f160716bd2f8a644960b06535fc8a860824df-500x356.webp)

***The Data Economy****is a video podcast series about leaders who use data to make positive impacts on their business, customers, and the world. To see all current episodes, explore the podcast episodes library below.*

---

Here’s a way to collaborate and have some fun with your technical and business colleagues. Ask everyone to identify the top experience, architecture, security, and data issues that characterize legacy applications and other technical debt.

It’s likely to be a long list covering everything from frontend user-experience issues to the underlying platform and infrastructure deficiencies. But there’s one often overlooked characteristic of legacy applications that is a sure, tell-tale sign of an application that requires modernization.

That characteristic is whether applications were designed for the slow “batch world” where the end-users waited for data processing, infrastructure constraints, and architecture limitations limited experiences, analytics, and machine learning capabilities.

The transition from batch processing to real-time streaming flow and streaming analytics was the discussion topic during episode two of [The Data Economy](/the-data-economy-podcast/), a podcast presented by Redis and hosted by Michael Krigsman of [CXOTalk](https://cxotalk.com/). Watch the [episode](/the-data-economy-podcast/episode-2/) to hear from guests Mike Gualtieri, VP and Principal Analyst at Forrester Research, and Norm Judah, a former enterprise CTO at Microsoft.

## Business advantages of real-time data

Mike and Norm lay out a compelling argument for why more businesses in non-tech industries and even SMBs can gain significant business advantages by changing to real-time paradigms and simplifying app development with a [robust multi-model data platform](/redis-enterprise-cloud/overview/).

Real-time data processing is not just for Wall Street trading platforms or large-scale tech platforms like Uber. In the [podcast](/the-data-economy-podcast/episode-2/), Mike and Norm share several examples of [streaming flow applications](/blog/use-redis-streams-apps/) where the data from a transaction in one system is shared in real-time with other systems. One example is travel, where a booked plane ticket should update loyalty systems in real-time because top flyers will check their point status right after booking.

More complex use cases require tracking state or enriching transactions with reference data. Tracking state is important for anomaly detection, such as monitoring temperature fluctuations in industrial systems, or for optimizing [fraud detection ](/solutions/fraud-detection/)in financial applications.

Many internet of things (IoT) use cases start with monitoring sensors, but real-time decisions and analytics are only possible after enriching data with reference data. For example, an IoT streaming flow from a fleet truck might include a device ID and location, but predicting optimal driving routes can only be computed after enriching the data with the truck type, driver, work schedule, and other information.

Shifting to real-time often creates differentiating capabilities. For example, finding out whether your mortgage application was approved is often considered a slow decision process, but companies that develop real-time analytics and decision capabilities may be able to win business by speeding up to a faster, more real-time response.

Many of these examples revolve around making quicker, more accurate predictions and aiding people in making real-time decisions. Smarter and faster decision-making is a competitive currency, and IT leaders must consider that [latency is the new outage](/docs/latency-is-the-new-outage/).

In the podcast, Mike suggests two questions that can help leaders identify opportunities. He recommends asking, “Is there something I could predict here to make this a more intelligent process, bypass a step, or make a better-automated decision? And is there something I could do quicker about this process?”

[Click here to view video](https://www.youtube.com/embed/Hdx0Os5AMFE)

## Real-time analytics and machine learning require app modernization

Norm and Mike go really deep into some of the technical challenges facing architects when designing real-time capabilities, and why building on top of legacy architectures is a nonstarter.

Consider how many applications were developed before [multicloud](/redis-enterprise-cloud/multicloud/), [microservices](/solutions/microservices/), in-memory databases, [caching solutions](/solutions/caching/), and streaming flow capabilities became readily available.

Developers often built legacy monolithic applications with a single-use case in mind, but today’s data streams must support many opportunities. “You actually don’t really know all the possible end-user cases,” says Norm. “The data analyst or the storage architect has this terrible dilemma of trying to understand the possible scenarios.”

Architects face several questions: Where should data and processing be performed in the cloud versus on the edge? What reference data is stored in memory to enable enriching? How should databases store real-time versus historical data?

And when you’re working with multiple streams of real-time data, Norm shares another key design criteria architects must consider: “The sequence of the data is incredibly important, and it’s easy to say but much harder to do. When I have a data source sending data to multiple places, you want to make sure that they all get the same data in the same sequence.”

## Real-time, multicloud data platforms enable AI experimentation

But Mike lays out the key business technology challenge around machine learning, especially when applied to real-time data sources. According to Mike, “The nasty thing about machine learning and investment is that you don’t know if it works until you try it.”

You can take his statement as a warning or as a technology challenge. It’s both. The technology challenge is in creating versatile, real-time data processing architecture that serves multiple business needs. The business reality and warning is that leveraging machine learning and real-time analytics will require ongoing experimentation to develop the algorithms, deliver applications, and support ongoing enhancements.

The key for architects is to establish a versatile, [real-time data platform](/redis-enterprise/advantages/) that runs at any scale that the business demands. It requires building [multicloud or hybrid cloud platforms](/redis-enterprise-cloud/multicloud/) for long-term business opportunities and working with partners that accelerate a seamless migration.

Because once the race begins and competitors create differentiating capabilities with real-time data platforms, it will be very hard for lagging businesses to catch up.

---

Watch more episodes of [**The Data Economy**](/the-data-economy-podcast/)podcast.
