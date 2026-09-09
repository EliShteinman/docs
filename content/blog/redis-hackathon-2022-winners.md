---
title: "Meet the Redis Hackathon 2022 Winners"
linkTitle: "Meet the Redis Hackathon 2022 Winners"
url: "/blog/redis-hackathon-2022-winners/"
description: "Three winners. Three unique applications – and plenty of innovation in real-time application performance."
date: 2022-10-20
blogCategories:
- "Announcements"
- "Company"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 20 October 2022 · updated 27 March 2025*

![Blog tile image](/images/blog/cc7dc16e7f2e22d539e6bbc59b4a1e437e8e7331-772x550.webp)

**Three winners. Three unique applications – and plenty of innovation in real-time application performance.**

The 2022 [Redis Hackathon](https://dev.to/devteam/announcing-the-redis-hackathon-on-dev-3248/) launched in collaboration with [DEV](https://dev.to/) in August 2022. Redis called upon the dev.to community’s most engaged, creative minds to build applications using [Redis Enterprise](/try-free/)’s many functions, [modules](/modules/), and products. Redis’ strengths go well beyond [caching](/solutions/caching/), so the contest challenged the community to showcase what’s possible in building applications backed by enterprise-grade performance.

Download our e-book [*Enterprise Caching: Strategies for Optimizing App Performance*](/docs/supercharge-app-performance-with-enterprise-caching/)*.*

We received 91 valid submissions in four project categories:

- **Minimalism Magicians:** Improve an open source demo application in [Amazon Web Services](/cloud-partners/aws/) (AWS), [Microsoft Azure](/cloud-partners/microsoft-azure/), or [Google Cloud Platform](/cloud-partners/google/) (GCP) and replace data systems with the power of Redis
- **Microservice Mavens**: Build a lightning-fast event-driven [microservices](/solutions/microservices/) application using Redis features
- **MEAN/MERN Mavericks:** Create a MEAN/MERN stack (or port an existing one from open source) in [one of three ways](https://dev.to/devteam/announcing-the-redis-hackathon-on-dev-3248#:~:text=MEAN/MERN%20Mavericks,Mongo%20for%20storage).)
- **Wacky Wildcards:** Build an application that doesn’t fit the other categories but with a playful, outside-the-box, sky-is-the-limit approach

The Redis Hackathon selected five grand prize winners, 20 runners-up, and 25 extra participants that included a video of five minutes in length or longer with their submission.

All of them achieved remarkable things, so we asked three of our grand prize winners to share the technical details of their projects, including their plans to expand their applications with Redis.

## Subham Sahu: OneSocial, an application for creators

Hi, I’m Subham Sahu, an engineer who loves exploring and building things. I’m a recent undergrad from the Indian Institute of Technology Ropar.

![OneSocial application architecture diagram](/images/blog/21b0f134e5fecb8a5f7ae1952c0d57474ecc9052-1024x887.webp)

**What does OneSocial do?**

It’s an app for creators and their audiences. With OneSocial, anyone can share their thoughts on their blog, manage an active newsletter, organize events, and make their content more discoverable. Want more? One can sell digital offerings, such as notion templates, design illustrations, or stock images, as well as services like video consultation, mock interviews, resume reviews, etc

**How will OneSocial make creators/influencers’ lives easier?**

Creators have to use multiple websites and social platforms to run their businesses. As a result, creators’ audiences are scattered across many social media channels. To ensure that the latest announcement reaches them, the creator has to post the same thing repeatedly on various websites. It is time-consuming, cumbersome, and possibly destructive to one’s brand, as asking loyal followers to subscribe to your content on multiple platforms could be a big ask.

The aim of OneSocial is to build a single platform that provides creators with all the necessary tools and functions from top to bottom, so they can have their entire audience under a single roof.

**Techie details: How did you build your application?**

The communication between server-to-server, server-to-client, and client-to-server is done via GraphQL. The front end is built using Next.js, and the back end uses Express (Node.js library). We’re using Cloudinary and Google Cloud Storage to store images and files securely.

Stripe powers the payments module, while [Redis queue ](/solutions/messaging/)serves as the notifications system. The chat module uses [Redis Streams](https://redis.io/docs/data-types/streams/), WebSockets, and GraphQL subscriptions to keep persistent connections and deliver messages instantly.

The data is stored as [Redis JSON](/json/), and we use the [Redis-OM Node.JS](/blog/redis-om-node-js/) library to interact with the database. All major fields and attributes are indexed or sorted for best performance based on the design requirements. We’re also using [RediSearch](/search/) to perform a full-text search on the data in Redis. Finally, we’re using [Redis Streams](https://redis.io/docs/data-types/streams-tutorial/) to publish and subscribe to events across multiple services.

**Stay connected with Subham**
View Subham’s [submission](https://github.com/subhamX/onesocial/)
Portfolio: [subhamx.dev](https://www.subhamx.dev/)
Follow Subham on Twitter: [@subhamx](https://twitter.com/subhamx_)

## Nabil Alamin: Pic-Placeholder, a stylish image placeholder

Hello. I’m Nabil, a contract developer based in Nigeria.

Pic-Placeholder is a stylish image placeholder with more than 500 images in six categories: animals, cats, dogs, houses, landscapes, and people.

**What was the lightbulb moment that led to Pic-Placeholder?**

When I heard about the Redis hackathon, I didn’t know what to build, but I still wanted to participate. I’d been hearing about Redis for a while but never had a chance to work with it.

I was helping a friend with a real estate app, and we wanted to use [lorem picsum](https://picsum.photos/) as a base for placeholder images, but we couldn’t because it was too generic, so I ended up building my own.

**What can Pic-Placeholder users hope to accomplish with this app?**

The project’s goal was to create a tool for quick prototyping when building image-centric sites.

**How did you use Redis to develop your app, and what other components were used along the way to create the final product?**

I started development by getting images from Unsplash in all my categories and converting them into JSON as the metadata. RedisJSON and [RediSearch](/search/) were used to house this data; the images were stored on AWS S3.

The entire app was built using Next.js, the client that served as the demo and server for calling the endpoints. The endpoints were:

- Random image from a category
- Random image from the database
- Specific image from the database
- Specific image from a category
- JSON outputs for all images in the database or by category

**Get more details about Nabil’s submission:**
View the Pic-Placeholder [demo](https://picc.vercel.app/)
See the Pic-Placeholder [repo](https://github.com/arndom/pic-placeholder/)

## Fred Spencer: Meatballs.live, a discovery tool for interesting social conversations

My name is Fred Spencer, and I am an Experience Architect in the United States. I’m the founder of [Elm Story](https://www.elmstory.com/en/), a design tool and platform for interactive storytelling.

**Project: **Meatballs.live, powered by [Redis Stack](https://redis.io/docs/stack/) and HackerNews, is an automated recommendation network and web app for discovering interesting conversations across social news.

**What technological components helped you realize this project?**

The entire Meatballs.live project is written in TypeScript, utilizing Redis Stack features, including [RedisGraph](/modules/redis-graph/), [RedisJSON](/json/), [RedisTimeSeries](/timeseries/), [Pub/Sub](/glossary/pub-sub/), and [caching](/solutions/caching/). I used [RedisInsight](/insight/) extensively to visually surface insights as data was collected in real-time. [Redis Cloud](/redis-enterprise-cloud/overview/) hosts the primary Redis database.

Get more of the technical details on [dev.to](https://protect-us.mimecast.com/s/bSSQCW6RrMhjRl6gH6vfMO?domain=dev.to/).

**What professional pain points is Meatballs.live designed to solve?**

You can think of this project as a “super-aggregator” designed to [ingest](/solutions/fast-data-ingest/), remix, and blend data from disparate aggregation sources.

By connecting and analyzing large amounts of structured, temporal data, meatballs.live can generate daily collections of top stories with a bias for the comment section. Daily collections serve as recommendations for the most engaging comments and related stories. The app experience can save time and cognitive load for users by reducing addictive scrolling. Temporal aspects provide context.

The live chat feature enables real-time engagement between meatballs.live users. The latest comments from Hacker News are blended with the stream, providing links to relevant threads.

**Are you planning to do more with this project? If you had/have time to improve it, what would you add?**

My number one priority is to warehouse historical data. With one data source, Meatballs.live generates 1 GB/mo. Given the current app’s feature set, it is unnecessary and inefficient for all this data to live in-memory. Next, I hope to add support for additional data sources, such as Reddit and Twitter.

I’d also like to port ingest services from Node to Rust, enhance live chat to support more real-time insight, and expand user features to include collection reactions.

There are no limits when remixing big data with the [Redis Stack](/blog/introducing-redis-stack/).

**Stay connected with Fred**
View Fred’s [submission](https://protect-us.mimecast.com/s/SjunCXDRvNTnVp4yUVO0sq?domain=github.com/).
Follow Fred on Twitter: @[r1tsuke](https://twitter.com/r1tsuke/) / @[elmstorygames](https://twitter.com/ElmStoryGames/)

## Thank you for innovating with Redis

We want to thank everyone who participated in our Hackathon with dev.to. We saw some truly inspired ideas come to fruition and hope to see these Redis-built applications go to market soon!

To see more applications built with Redis, please visit our [Launchpad](https://launchpad.redis.com/) site, full of engaging demos and inspiration for anyone building applications.
