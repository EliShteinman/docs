---
title: "What You Missed at Redis Day Seattle"
linkTitle: "What You Missed at Redis Day Seattle"
url: "/blog/what-you-missed-at-redis-day-seattle/"
description: "A little snow couldn’t stop the Redis community from coming out in force to our first Redis Day of the year in Seattle. Held on January 13–14 at the Hyatt Regency, Redis Day Seattle brought..."
date: 2020-01-22
blogCategories:
- "Company"
authors:
- "Jane Paek"
lastmod: 2025-03-27
hidden: true
---

*By Jane Paek, Solution Architect Manager · Published 22 January 2020 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/1800d303b814db4266f0329b2d1d68fa45218902-1600x1200.webp)

A little snow couldn’t stop the Redis community from coming out in force to our first Redis Day of the year in Seattle. Held on January 13–14 at the Hyatt Regency, [Redis Day Seattle](https://connect.redis.com/redisdayseattle/mktg) brought together some 300 developers, engineers, software architects, programmers, and business professionals for intensive training, thought leadership, and networking.

On day one, Redis users from beginners to experts packed the conference room for a full schedule of hands-on training covering everything from Redis basics to [Redis Streaming Architectures](/docs/build-apps-using-redis-streams/), [Probabilistic Data Structures](/blog/how-to-get-started-with-probabilistic-data-structures-count-min-sketch/), [RediSearch](/redis-enterprise/redis-search/), and [RedisTimeSeries](/redis-enterprise/redis-time-series/). The following day, attendees heard from representatives of Zulily, Twilio, MDmetrix, AWS, and other cutting-edge customers on how Redis helps solve some of their business problems.

![](/images/site-mirror/ba07c766e590c75f1e977c5e4d82923c13fb75fc-1024x768.webp)

*Redis’ Head of Developer Advocacy Kyle Davis and Developer Advocate Guy Royse present during training day.*

We had a grand time in Seattle, and can’t wait to be back again. For now though, here’s a recap on what went down.

## Using Redis for shopping, medical treatments, and more

Redis Day Seattle was a great way to discover how to use Redis beyond traditional use cases, and demonstrated how Redis has been embraced by many frameworks, like Protobuf, Rust, and ASP.NET. Attendees were treated to out-of-the-box presenters, like Adam McCormick from Sinclair Broadcasting, who started his presentation by having the entire audience stand up and sit down with the progression of pages deployed. That didn’t take long—Sinclair publishes a new webpage every 15 seconds on more than 16 million websites!

> Adam McCormick demonstrates how [@WeAreSinclair](https://twitter.com/WeAreSinclair?ref_src=twsrc%5Etfw) uses Redis to help monitor deployments of millions of web pages [#RedisDay](https://twitter.com/hashtag/RedisDay?src=hash&ref_src=twsrc%5Etfw) [#Seattle](https://twitter.com/hashtag/Seattle?src=hash&ref_src=twsrc%5Etfw) [pic.twitter.com/Jlk3xvYC2t](https://t.co/Jlk3xvYC2t)
— Dave Nielsen (@davenielsen) [January 15, 2020](https://twitter.com/davenielsen/status/1217293535818350592?ref_src=twsrc%5Etfw)

One point that struck many attendees was the wide variety of businesses from completely different industries that all have one thing in common: Redis is part of their technology stack. From Seattle-based Zulily, Mohamed Elmergawi shared how the ecommerce giant uses Redis to build a super-fast, super-reliable global customer session service that handles millions of requests per day while delivering a great customer experience. For medtech company MDmetrix, RedisGraph helps track medical treatments so hospitals can carefully track doses, reducing overmedication and drug addiction, said Co-Founder and CTO Matthew Goos. Cloud service company Twilio, meanwhile, uses APIs to connect people around the world via voice, SMS, video, and WhatsApp, said Principal Software Engineer [Scott Haines](https://twitter.com/newfront?lang=en). And I got the chance to explain how to use Redis to power a metering and rate limiting app to protect your APIs—using an example of keeping folks from drinking too much.

> Jane Paek of [@Redis](https://twitter.com/Redis?ref_src=twsrc%5Etfw) shows a metering and rate limiting app that demonstrates how to protect your APIs (or in this case, prevents a user from drinking too much) [#UseRedis](https://twitter.com/hashtag/UseRedis?src=hash&ref_src=twsrc%5Etfw) [#DrinkWisely](https://twitter.com/hashtag/DrinkWisely?src=hash&ref_src=twsrc%5Etfw) [#RedisDay](https://twitter.com/hashtag/RedisDay?src=hash&ref_src=twsrc%5Etfw) [#Seattle](https://twitter.com/hashtag/Seattle?src=hash&ref_src=twsrc%5Etfw) [pic.twitter.com/gdaB5QnAvm](https://t.co/gdaB5QnAvm)
— Dave Nielsen (@davenielsen) [January 14, 2020](https://twitter.com/davenielsen/status/1217233067355435009?ref_src=twsrc%5Etfw)

## I didn’t know Redis could do that!

Many attendees were surprised to learn about Redis’ capabilities beyond caching. Cameron Vander Wal, a software engineer at the survey firm Qualtrics, for example, said he was surprised to learn that Redis had a streaming capability. “We’ve really only used Redis for a simple key-value search,” he said. “To have a message queue like that seems pretty useful.”

Redis Day Seattle attendees were also treated to a special keynote from Redis CTO and Co-Founder [Yiftach Shoolman](https://twitter.com/Yiftachsh), who traced the growth of NoSQL data models like TimeSeries, Graph, JSON, Key-value, and Search, as discussed some of the most-desired features of the upcoming Redis 6. Later in the day, Redis’ Security Product Manager [Jamie Scott](https://twitter.com/iamateapot418) explained some of the new security features in Redis 6, including TLS and ACLs. And, of course, it wouldn’t be a Seattle tech event without tech staples Amazon Web Services and Microsoft, who presented on Redis Commands and ASP.NET Core with Redis, respectively.

![](/images/site-mirror/a9edc0aea544f0897666d69cd4ef0d2707727701-1024x768.webp)

*Yiftach Shoolman, CTO and Co-Founder of Redis, shared some of the new features of Redis 6.*

The second day closed with a networking happy hour where developers, presenters, and experts alike could mingle and share their Redis stories. It was a great opportunity to bounce ideas off Redis users with a wide variety of experiences, all eager to learn something new. Plus, everyone left happy with a brand new Redis t-shirt and laptop stickers.

Despite the blanket of fluffy white stuff, Redis Day Seattle turned out to be a great event, bringing together the Pacific Northwest Redis community to kick off the new year and the new decade, Redis style.

Interested in attending future Redis events? Save the date for RedisConf 2020 in San Francisco:

[RedisConf 2020](https://events.redis.com/redisconf20/)

When: May 12–14, 2020

Where: SVN West, 10 S Van Ness Ave, San Francisco, CA 94103
