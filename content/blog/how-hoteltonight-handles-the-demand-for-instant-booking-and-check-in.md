---
title: "How HotelTonight Handles The Demand For Instant Booking And Check-In"
linkTitle: "How HotelTonight Handles The Demand For Instant Booking And Check-In"
url: "/blog/how-hoteltonight-handles-the-demand-for-instant-booking-and-check-in/"
description: "Originally published on fastcolabs.com"
date: 2014-12-12
blogCategories:
- "Company"
authors:
- "Steven Melendez"
lastmod: 2026-08-13
hidden: true
---

*By Steven Melendez · Published 12 December 2014 · updated 13 August 2026*

![Blog tile image](/images/site-mirror/a9e7978fcba393b4c6389c92b7ce705124eb32ec-140x92.webp)

Originally published on [fastcolabs.com](http://www.fastcolabs.com/3039625/how-hoteltonight-handles-the-demand-for-instant-booking-and-check-in)

The app HotelTonight is built around last-minute hotel booking. Users depend on the app to quickly deliver room rates and vacancies, especially when they have a spotty cell connection and it’s a busy holiday weekend.

“We can have customers that are standing outside a hotel and booking a room and walking in and expecting to be able to check in,” says HotelTonight cofounder and chief architect [Chris Bailey](//www.fastcompany.com/person/chris-bailey).

![](/images/site-mirror/523cdad581ed2487ee1c196f0c7d04bb35d64503-260x384.webp)

The app’s backend needs to be able to quickly sync reservations and vacancy information with a range of [hotel reservation systems](http://www.fastcolabs.com/explore/hotel-reservation-systems) and users’ phones and tablets, so it doesn’t fail to display a convenient deal or, worse, book someone a room that’s already taken, says Bailey. The app’s Black Friday traffic peaked at eight times normal load levels, with a [$7 room special selling out in under seven minutes](https://www.hoteltonight.com/2014/11/black-friday-room-sale/).

“Historically in the industry, people aren’t booking so much last minute, but that’s really shifted,” he says, thanks to [mobile devices](http://www.fastcolabs.com/technology/mobile-devices). “They can be in the back of a cab; they can be at a bar; maybe they’re at a party and decide, ‘Hey, I don’t want to drive home tonight.’”

To keep data updated in [real time](https://www.fastcolabs.com/explore/real-time) even under heavy load, the company uses the speedy [Redis](https://redis.io/), an open source data structure server that is currently sponsored by [Pivotal](http://www.pivotal.io/big-data/redis). Bailey says it also helps engineers quickly add and tweak new features and record new stats without painstakingly building traditional database tables.

“We didn’t initially start with Redis, but we pretty quickly figured out a need for it there,” he says, explaining the company still uses MySQL for some of its infrastructure. “All these things that you thought well, shoot, I don’t really want to write that to MySQL—it just seems like a lot of overhead, I have to create a table and manage a schema and there’s a lot of overhead—now I just write it to Redis.”

The database system also helps with a common issue for HotelTonight: handling network timeouts and other errors in communicating with customers’ devices and third-party services like booking APIs, says Bailey.

Redis includes atomic counters—that is, variables that can be incremented in a single operation so they report and store consistent values even when accessed by multiple processes—which help keep track of how often an [API](http://www.fastcolabs.com/technology/api) call or other operation has failed.

Partially to avoid focusing too much on the uptime and scaling of Redis and other core services itself, HotelTonight relies on cloud providers, including Amazon [Web Services](http://www.fastcolabs.com/explore/web-services) and hosting from [Redis](https://www.fastcolabs.com/company/redis-labs), he says.

“It allows us to not have to have as much expertise in house and rely on true experts in those technologies for things like Redis or some of the other services that we use,” he says.

That, and the flexibility of the kind of data that can be stored in Redis, make it easy build custom logic to track and handle failures of different types of operations, from rapidly scheduling retries to failing over to alternative providers, says Bailey.

“What’s really nice about that is from the customer perspective we avoid giving them an error message,” he says. “There’s no error for the customer; they get what they’re after.”

Using Redis also makes database changes more painless, as engineers can effectively tweak what’s stored in the database without rebuilding formally specified [SQL](http://www.fastcolabs.com/programminglanguage/sql) tables, which used to require downtime, he says.

“Don’t get me wrong—you will have a schema, so to speak, at some point,” he says. “It’s more about how officially defined is it.”
