---
title: "Six Things to Consider When Using Redis on Heroku"
linkTitle: "Six Things to Consider When Using Redis on Heroku"
url: "/blog/six-things-to-consider-when-using-redis-on-heroku/"
description: "Earlier this week, Flights With Friends wrote this post evaluating alternatives for using Redis on Heroku. Even though we were not selected as their favorite choice, we think they did a fair job..."
date: 2012-11-09
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-04
hidden: true
mirrored: true
---

*By Redis   · Published 9 November 2012 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/7fb8fab8b7fa498fc7dd89c5b070e4f821d93642-242x208.webp)

Earlier this week, Flights With Friends wrote [this post](http://blog.flightswithfriends.com/post/35215688010/heroku-redis-hosting-options) evaluating alternatives for using Redis on Heroku. Even though we were not selected as their favorite choice, we think they did a fair job and want to share what we think should be the most important things to consider when selecting a Redis add-on for your Heroku app:

1. **True high-availability**: By this, we’re referring to instant failover – if a node fails, data should *instantly* be served from a replacement node in a *seamless* manner. In addition, it’s important to have an automated recovery process so that failover does not require human intervention.
1. **Infinite seamless scalability**: Your dataset should be able to grow to any size (even beyond the largest cloud instance) without being limited in Redis commands. When upgrading or downgrading your plan, you shouldn’t need to move your dataset between cloud instances – it should be a simple matter of changing your memory limit setting.
1. **Performance**: Although most add-ons use a single CPU, it’s much better for your Redis dataset to run on more than one CPU and the strongest cloud instances. Make sure your add-on uses advanced techniques to maximize cloud-based Redis performance for any dataset size.
1. **Multiple databases**: You may want to create several databases (DBs), and most Redis add-ons on Heroku today have this capability. However, this is likely to be deprecated in the next Redis version, because Redis is based on a single threaded architecture so if you use one DB, all others are stalled. Make sure each DB runs in a dedicated process and in a non-blocking manner.
1. **Database connections limit**: Make sure your Redis add-on is not limited in the number of connections it allows. Most are!
1. **Who’s behind the add-on**? Redis is fantastic. In fact, according to a recent study by a leading analysts firm Redis is only second to MongoDB in terms of actual NoSQL deployments (probably the reason that so many new vendors are now offering it on Heroku). However, Redis is a database, which is probably the most sensitive piece in your application architecture. So when you select a Redis add-on, we recommend you look into who’s behind it. Who are the people? What are their technical capabilities? Do they solve real-life issues, or just “package” standard Redis? Do they support platforms other than Heroku? Can you grow with them knowing they will solve your specific needs ?

Redis Cloud was developed by a group of specialists in the fields of databases and application acceleration. We have been serving production databases since January 2012, many with over 100GB in size. Already, we’ve overcome three AWS outages without losing a single byte of customers’ data. So why are we still in beta? It took us time and great effort to build our novel dynamic clustering technology around standard Redis, which enables capabilities like true high-availability, infinite and seamless scalability, [high performance at any dataset size](/blog/its-true-even-modest-datasets-can-enjoy-the-speediest-performance#.UJwiT28tS4h), multiple databases (each in a dedicated process), and unlimited database connections. We want to make absolutely sure it works properly over time before we remove the “beta” label. In regards to questions around pricing, at this time we can only promise it will be very competitive, so stay tuned!
