---
title: "Accelerating Avatars with Redis Enterprise"
linkTitle: "Accelerating Avatars with Redis Enterprise"
url: "/blog/accelerating-avatars-redis-enterprise/"
description: "First a little bit about us: created in 2011, Silkke strives to create animated 3D avatars of unsurpassed quality that are usable in various applications, virtual universes and compatible internet..."
date: 2018-03-29
blogCategories:
- "Company"
- "Tech"
authors:
- "Baptiste Leterrier"
lastmod: 2025-03-04
hidden: true
---

*By Baptiste Leterrier · Published 29 March 2018 · updated 4 March 2025*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

First a little bit about us: created in 2011, [Silkke](http://silkke.com/) strives to create animated 3D avatars of unsurpassed quality that are usable in various applications, virtual universes and compatible internet websites. Our mission is to create a human element in digital platforms, integrating with various brands to bring them closer to their customers by offering them a unique, personalized experience.

![](/images/blog/67492acb72449a053a9be84da2fc16f2eaa7a5eb-87x43.webp)

## Managing our RabbitMQ queue content

Creating an avatar requires several tasks, from the initial scan of the person to the 3D life-like clone. There are four separate steps involved in the scanning process, and even though that doesn’t seem like much, this places major strain on the total capacity of one booth performing scans. Each booth can scan up to one person each minute! Now multiply this by the number of booths around the world.

That’s a lot of work.

As this process occurs, scalability is more than necessary, as we don’t know how many avatars we will have to process. So we use RabbitMQ to create queues that assign work to every process that renders part of an avatar. Doing so permits us to scale the processing power as the queue fills up.

This presents another challenge: how best to organize the content that’s in the queue?

As it fills up, we can’t know the order of a set of instructions in the queue. And what if we need to modify an instruction on the go—we can’t edit something without removing all the initial elements and then requeuing them, thus changing the global order and potentially risking a slow down of production.

![](/images/blog/356df8a3a314038bae3336239b392ceb3bc354e0-560x335.webp)

First, we needed a system that could process a lot—and fast!— so we used RabbitMQ. But we also needed a simple system that supports designing and querying on the software side (query all then parse and show), as well as that ability to natively propose FIFO. Rather than develop a new queuing solution from scratch, one that can address all of our needs, why not take the practical approach and integrate an existing technology that works well with RabbitMQ? , That’s why we chose Redis!

We introduced a new process that duplicated all instructions: one in RabbitMQ for processing and one in Redis for monitoring/editing:

![](/images/blog/1299b791b6582ad6dcd068ceda6c208ef8aa9554-805x506.webp)

As one message goes into RabbitMQ, the same is put in a Redis Set FIFO style. As the workers process the queue, they also remove/put the messages in Redis, keeping our Set in sync with the RabbitMQ.

Next we developed a web interface to control and show what is in Redis. It also controls the state of the queue as a Redis value with expiration that tells the worker whether or not it should consume the queue (we can stop the consumption of a queue temporarily without stopping the workers).

For record purposes, a global event can have up to 10-20 messages per second (for 1 booth), and we have booths all over the world – but thanks to [Redis Enterprise Cloud’s](https://app.redis.com/#/sign-up/cloud?direct=true) awesomeness, it can be scaled!

## Building Architecture for Multiplayer Rooms

Unlike some applications that just *display *the avatar of a person, Silkke faced the challenge of exhibiting dynamic character movement. For example, avatars needed to wander and interact by chatting and sending messages. Though there were already some solutions for multiplayer support on the market, none were able to fit our needs—especially on the server side. The main problem we faced was how to synchronize the display of one avatar in the game with others.

The Answer: rooms.

Like chat room for text, we needed a solution to register which avatar is currently present. As for the previous problem, we could have three avatars to several thousands at the same time, but only with random connection spikes.

![](/images/blog/1caf58b323ed5ecc7a333824b62c29ebd25d1290-1202x969.webp)

Luckily Redis came to save the day again! We can create rooms where we store the ID of avatars for each person that connects to the app. The architecture is simple: a set for each person. But by benchmarking it, we thought of a new way to implement Redis. How about using it for the chat system, using the pub sub system and a socket system? Then things got pretty good. We could handle 5,000 people in one room. And rather than only using it for text messages, it doubles as a relay for commands.

Say you want your avatar to go take a drink at the bar. From your phone you click “grab a drink,” and that’s it. But under the hood, Redis demonstrates its power. In under one second, it checks your Auth key, checks if your avatar is in the scene and connected, sends the instruction to go to the bar, checks whether the instruction started correctly and notifies you. All with pub-sub, expiration and hash-maps. Then we can scale it to every avatar you see in the picture. Redis is once again the perfect fit for our needs.

Several more projects are in the think tank for now, and Redis is vital when solving problems of speed, reliability and scalability.

To get started quickly with Redis, you can sign up for Redis Cloud for free at: [/redis-enterprise-cloud-free-30-mb-plan](/redis-enterprise-cloud-free-30-mb-plan)
