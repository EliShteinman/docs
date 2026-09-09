---
title: "RedisConf18 in Review"
linkTitle: "RedisConf18 in Review"
url: "/blog/redisconf18-in-review/"
description: "Over 1,200 Redis enthusiasts took over Pier 27 on the San Francisco waterfront for three days of training, talks and fun at RedisConf18. The theme of this year’s conference was “Everywhere” and..."
date: 2018-05-23
blogCategories:
- "Announcements"
- "Tech"
authors:
- "Tague Griffith"
lastmod: 2025-03-04
hidden: true
---

*By Tague Griffith, Head of Developer Advocacy · Published 23 May 2018 · updated 4 March 2025*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

![](/images/blog/4bb12096c9a1469d051c01f856e2cb16af1e74d1-1920x1280.webp)

Over 1,200 Redis enthusiasts took over Pier 27 on the San Francisco waterfront for three days of training, talks and fun at RedisConf18. The theme of this year’s conference was “Everywhere” and with over 60 breakout sessions across six concurrent tracks, Redis really was everywhere.

![](/images/blog/319e41e60f91f8a62f6234fb75815d670fbe8362-801x1277.webp)

This year RedisConf moved to the beautiful Pier 27 with panoramic views of the San Francisco Bay, both bridges and several iconic San Francisco landmarks. Pier 27 is the San Francisco Cruise Terminal originally built as a staging site for the 2013 America’s Cup. The pier serves as a cruise terminal and a conference venue during the off-season.

Moving RedisConf to the waterfront allowed the conference to accommodate the growing number of participants, hold more sessions and stage some really fun things to do in-between sessions. This year we had a DJ, a table full of stickers, a geek lounge and a giant Light Bright wall which featured some amazing pictures built by attendees.

A host of food trucks rolled up for lunch, providing attendees with everything from BBQ to Korean Fried Chicken (FYI: cheesesteak and old fashioned donuts are now the Official Lunch™ of Redis Geeks everywhere).

**Training Day**

Salvatore Sanfillipo, the creator of Redis, kicked off the all-day Redis training with his explanation of the primary data structures of Redis, followed by a talk on the new Streams data structure. This year’s training day featured two tracks: an introductory track for new

![Salvatore Sanfillipo on stage](/images/blog/e6b1cd98e33f2b65d6d0a93bbe8c726e01da5587-444x608.webp)

Redis users and an advanced track for power users. Developers who attended either track had a chance to learn about Redis directly from folks like Salvatore, Dvir Volk, Itamar Haber and several other contributors to the Redis project.

The training session covered a wide range of topics, from the Redis version of “Hello World” to improving performance with the Redis Cluster API. Attendees spent the day listening to Redis experts and working through a number of coding exercises to deepen their understanding of Redis.

This is the second year we’ve hosted a training event on the day before RedisConf, and it’s been a great way for folks to really sharpen their Redis skills and get the most out of the conference.

**Redis is Everywhere**

RedisConf18 featured six concurrent speaking sessions and over 75 speakers sharing their knowledge and experience with the community; Redis truly was *everywhere*. This year’s talks covered everything, from using Redis on an avocado farm to deploying Redis applications with Google Skaffold, as well as a practical tutorial on Redis memory optimization.

![Matt Rickard of Google speaking on Kubernetes](/images/blog/26dac1059d2d052c25d8f9c0f58675787fb44b15-891x1100.webp)

Following Salvatore’s keynote, Ofer Bengal and Yiftach Shoolman of Redis made a [series of announcements](/press/redis-labs-broadens-redis-enterprise-capabilities/) around Redis modules, Active-Active geo distribution using CRDTs for all major Redis data types, a new University for Redis, and upcoming innovations with Persistent Memory. The Redis modules announcement included the new RediSearch aggregations functionality and changes to the architecture of the Redis Graph module that utilize GraphBLAS technology for even greater efficiency in execution. Prof. Tim Davis of Texas A&M University, the creator of GraphBlas, explained the sparse matrix multiplication algorithms behind GraphBLAS while Roi Lipman from Redis laid out the usage of GraphBlas supercharges Redis Graph to outperform other graph databases by up to 100x. Prof. Carlos Baquero of the Universidade do Minho (one of the lead CRDT researchers) explained the history and research behind CRDT, the technology used to add active-active functionality to Redis CRDTs. Ken Gibson and Andy Rudoff from Intel explained how Redis on Flash can benefit from utilizing Intel’s new Persistent Memory technology.

Over 75 speakers from all over the world joined us at the conference to share their unique experiences with Redis. First-time speaker Glenn Edgar of LaCima Ranch had one of the most unique talks in RedisConf history, detailing how he combines Redis with IoT sensors to run LaCima Avocado Ranch. Using Redis, Linux and ARM devices, Glenn walked us through a history of building a custom, open-source system to manage irrigation and other tasks on the ranch.

![](/images/blog/2cbda5e7b1dfc41911e7b014a028ab12d883c86a-1012x1036.webp)

Many other first-time speakers like Jiaqi Wang of [Redfin](http://www.redfin.com/) (“Serving Automated Home Values with Redis and Kafka”), Aditya Vaidya of Oath (“Video Experience Operational Insights in Real Time”), and Darren Chinen of Malwarebytes (“Transforming Vulnerability Telemetry with Redis Enterprise”) joined Glenn in making their debut appearances this year.

Several alumni speakers and community leaders like Dmitry Polyakovsky (“Integrating Redis with ElasticSearch”), Stefano Fratini (“Amazing User Experiences with Redis & RedisSearch”), Sripathi Krishnan (“Redis Memory Optimization”), and Dvir Volk (“Introducing Real-Time Insights with the RediSearch Aggregations”) made return appearances to share more of their experience with the Redis community.

And of course, no RedisConf is complete without a glimpse into the future of Redis from Salvatore. Salvatore spent the keynote talking about the future of Redis looking forward to some of the possible work for Redis 6 and 7. Some of that work, including the new version of the [RESP protocol](https://gist.github.com/antirez/2bc68a9e9e45395e297d288453d5d54c), is already starting to emerge. Salvatore held a breakout session to explain the design principles behind the Streams data type.

This year saw the conference expand into two focused tracks—one on Microservices and one on DevOps—to bring information about technologies often used in conjunction with Redis. Attendees in these sessions had an opportunity to learn about deploying Redis via Kubernetes and how to manage development, testing and production Redis resources using OpenShift.

If you missed out on this year’s conference (or you came but didn’t get to go to every session), never fear—all the breakout sessions and keynote talks were recorded and will be published to the [Redis YouTube channel](https://www.youtube.com/channel/UCD78lHSwYqMlyetR0_P4Vig) once they are edited. While you’re there, check out some of the talks from previous conferences!

**Looking ahead to RedisConf19**

Even though we just finished this year’s conference, the team is already thinking about RedisConf19. The growth of the conference over the years has been astounding and next year we want to bring you another great lineup of speakers and fun activities to make for a memorable experience. Keep an eye out for announcements about 2019 and especially the open call for speakers—if you haven’t spoken at RedisConf before, why not make 2019 your debut?

We want to thank all of our sponsors, speakers and attendees for contributing to a fantastic conference this year! We hope to see you next year for RedisConf 2019 for what should be, in the words of our attendees, another:

![The Giant Light Bright](/images/blog/e5340600538dd10cd72172e3c42c888c86fdcee0-730x544.webp)
