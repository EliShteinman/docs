---
title: "Data Durability vs Data Availability: Streaming Video Helps Explain"
linkTitle: "Data Durability vs Data Availability: Streaming Video Helps Explain"
url: "/blog/data-durability-vs-availability/"
description: "Need to understand the difference between data durability and data availability? Your favorite binge-watch can help illuminate the distinctions."
date: 2022-12-28
blogCategories:
- "Tech"
authors:
- "Talon Miller"
lastmod: 2025-03-27
hidden: true
---

*By Talon Miller, Principal Technical Marketer · Published 28 December 2022 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/a250ef3aa461fdc2b9307bda57e10be3d8551f89-772x550.webp)

**Need to understand the difference between data durability and data availability? Your favorite binge-watch can help illuminate the distinctions.**

Data has a shelf life. Data is vulnerable to bit rot – also known as data decay, bit decay, and data rot. That’s true of software and media, such as websites that disappear, taking with them years of news articles, movies, or other information, only a fragment of which is captured by the [Wayback Machine](https://archive.org/web/).

However, bit decay also applies to the physical media of a storage device and the resulting deterioration in the data integrity of the information stored there. Losing a bit here and a byte there over time adds up to data that can’t be trusted. Data loss means, well, data is *gone* – possibly important documents, such as historical e-commerce records or tax information. Worse, a drive failure can mean that data is stored inaccurately, which means wrong information.

It isn’t merely a technical problem. In industries like [financial services](/industries/financial-services/), the consequences of vulnerable or slow data could cost a trusted brand name its customer loyalty, tarnish its reputation, and lead to lost revenue.

Now, raise your hand if you have a favorite show on a streaming service.

According to [Statista](https://www.statista.com/statistics/318778/subscription-based-video-streaming-services-usage-usa/), 83% of American consumers used a video-on-demand streaming service in 2022. Typically, customers want to watch their favorite TV shows when they want them, wherever in the world they may be. The media of that TV show – let’s say it’s *Andor* – is the same set of bits wherever it’s viewed, so it serves as a good example of persistent data**. **It illuminates the importance of data durability and [availability](/redis-enterprise/technology/highly-available-redis/), as well as the implications of working with bad data.

No, durability and availability are not one and the same! However, to work with trusted data, it’s important that both durability and availability work in tandem. It’s not possible to deliver true data quality with one and not the other.

Using your go-to binge-worthy show, let’s explore why that is.

## What is data durability?

Data durability is a means of safeguarding data from loss or corruption in the event of an outage or failure.

Data durability is the process by which one ensures data is (and remains) intact, devoid of any degradation. In essence, durable data means uncompromised data.

In streaming media terms, imagine you’re sitting down to watch the latest Star Wars spin-off series. Your 4K TV is set. You’ve heard the effects are mind-boggling. Yet, for some reason, the show starts up, and the quality leaves a lot to be desired.

In this instance something may have interfered with the data durability of the streaming, i.e. the quality has degraded but the the information is still available.

***Learn how Redis improves with ***[***data durability***](/redis-enterprise/technology/durable-redis/)*** through AOF and snapshot persistence options.***

## How is durability maintained?

Data durability relies on persistent data.

When data is persistent, it is accessible and ready to be used at the start of the next [application session](/solutions/session-management/). The expectation is to suffer no data loss between the last session and the next.

To maintain data durability, it’s critical to persist the data to disk. Data is persisted to disk at set intervals in one of two different ways: **append-only files** (AoF) and **snapshots**.

AoF provides two choices for appending write operations to disk:

- Every second (faster, but not as comprehensive) or
- Every write (most trustworthy, but not as fast).

AoF generally is the wisest choice for any organization that needs uncompromised data in real-time.

A snapshot is a kind of data replication that captures the state of the database at a specific point in time. Unlike AoF, snapshots are typically written to disk in intervals of 1, 6, or 12 hours.

The criteria for database persistence are not universal. The persistence configuration depends on the database type (whether it’s [NoSQL](/blog/schemaless-databases/) or a relational database) and database size, and other matters. Therefore, it’s best if you make configuration decisions when establishing your architecture.

The other option is to edit an existing database’s configuration. Note that the change is not automatic. Changing a database’s persistence model can take time to complete.

### How is durability measured?

In other words, how do you measure a database’s resiliency against corruption from bit decay or loss?

Durability is usually illustrated in percentages, such as 11 nines (99.9999999%) or 99.9999999% durability, which according to [Google Cloud](https://cloud.google.com/blog/products/storage-data-transfer/understanding-cloud-storage-11-9s-durability-target), means that “even with one billion objects, you would likely go a hundred years without losing a single one!”

The math behind all these nines requires some dense statistics, so know that the main statistical measurements used to measure data durability are typically the Poisson distribution and binomial distribution. Whereas the [Poisson distribution](https://www.investopedia.com/terms/p/poisson-distribution.asp) measures the probability of an event occurring (k) times in a given interval of time, the [binomial distribution](https://www.investopedia.com/terms/b/binomialdistribution.asp) assesses the probability of one of two results in a repeatable test, namely “success” or “failure.”

## What is data availability?

Data availability means the data is operational. When the data is requested, it is delivered. In other words, data availability is a synonym for system uptime.

That’s why data durability and availability, together, create the perfect equation: uncompromised data plus uptime and accessibility or immediate access to uncorrupted files.

Oh yes! Back to the new Star Wars series for a second.

You reach a cliffhanger in the show, but you have to make it to the airport for an international business trip. You can start a new session once you get to your hotel. When you restart the show, like magic, you pick up where you left off, even if the location is halfway across the planet. That’s the beauty of both availability and high availability. It gives you the power to say, “I want my Baby Yoda crisp, clear, and on the attack when I’m in Italy, even though I paused him mid-action back in Kansas.”

Despite your significant location change, what makes this following session so smooth and possible is Active-Active Geo-Distribution – not “The Force,” alas, however cool that might be. Active-Active Geo-Distribution takes a database’s replicated data and makes it available to nodes distributed across various available zones. By establishing local nodes with a replica, latency is vastly reduced, enriching the viewing experience.

Baby Yoda moves slowly enough. Your database shouldn’t make matters worse.

### How is data availability measured?

Data availability is measured by taking total uptime and dividing it by the sum of that uptime plus downtime: **Availability = Uptime ÷ (Uptime + Downtime)**.

Availability is usually phrased as “five nines” or “eleven nines” but is typically expressed as a percentage, such as 99.999%. When it’s all said and done, “five nines” averages out to about five minutes of total downtime in a year.

Put into context, suppose we know that an instance was only available for 145 hours in a week (168 hours). That’s a 13-hour difference. In that case, the calculation would look something like this: **145 ÷ (145 + 13) = 91.772% availability.**

High-availability architecture is really interesting, and (for techies) it is fun to unpack what’s possible when used to its optimum potential. Check out [High-Availability Architecture Demystified](/blog/high-availability-architecture/) and [What Is Data Replication](/blog/what-is-data-replication/) for more information on clustering and disaster recovery.

[Click here to view video](https://www.youtube.com/embed/mCOX-2ez-m4)

### The ramifications of unavailable data

In 2022, Uptime Institute’s Outage Analysis found that “[over 60% ](https://uptimeinstitute.com/about-ui/press-releases/2022-outage-analysis-finds-downtime-costs-and-consequences-worsening#:~:text=The%20proportion%20of%20outages%20costing,15%25%20over%20that%20same%20period.)[of failures result in at least $100,000 in total losses](https://uptimeinstitute.com/about-ui/press-releases/2022-outage-analysis-finds-downtime-costs-and-consequences-worsening#:~:text=The%20proportion%20of%20outages%20costing,15%25%20over%20that%20same%20period./), up substantially from 39% in 2019. The share of outages that cost upwards of $1 million increased from 11% to 15% over that same period.”

That’s a real-world result. The metaverse and gaming platform Roblox suffered a 73-hour outage in October 2021. It left the company with [an estimated $25 million in lost bookings](https://www.datacenterfrontier.com/cloud/article/11427329/uptime-longer-data-center-outages-are-becoming-more-common/), according to Data Center Frontier.

In the financial industry, for example, where billion-dollar deals are dependent on who gets there first – every millisecond that data isn’t available could translate to lost revenue, partnership opportunities, and a potential exodus of customers.

Netflix had an outage for 1.5 hours in July 2022 that affected customers in the United States, France, and India. That elicited negative responses like, “Friday Night and @netflix is down! How’s your Friday Night going?” reported [Reuters](https://www.reuters.com/business/media-telecom/netflix-down-thousands-users-2022-07-15/).

Hopefully, your Friday night with Baby Yoda is going just great!

Curious to learn more about Redis Enterprise’s built-in disaster recovery capabilities? Watch our [Tech Talk](/events/build-vs-buy-dr-in-redis-oss-vs-redis-enterprise/).
