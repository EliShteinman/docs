---
title: "RedisDays New York 2022 Overview"
linkTitle: "RedisDays New York 2022 Overview"
url: "/blog/redisdays-new-york-2022-overview/"
description: "After kicking things off in London with a day centered on all-things real-time data, followed by a developer-focused day in San Francisco, RedisDays 2022 came to a close in New York with a day of..."
date: 2022-04-22
blogCategories:
- "Company"
authors:
- "Henry Tam"
lastmod: 2025-03-27
hidden: true
---

*By Henry Tam · Published 22 April 2022 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/d3657077879acc023e14018eb341db1b22093ba3-772x550.webp)

After kicking things off in [London](/blog/redisdays-london-2022-recap/) with a day centered on all-things real-time data, followed by a developer-focused day in [San Francisco](/blog/redisdays-san-francisco-2022-overview/), RedisDays 2022 came to a close in New York with a day of sessions all about the latest Redis developments in [artificial intelligence](/press/redis-labs-delivers-powerful-data-platform-for-next-wave-of-ai-applications/) / [machine learning](/press/redis-labs-introduces-landmark-machine-learning-module-redis-redis-ml/) (AI/ML).

The RedisDays New York sessions made it clear that any modern data stack has to be built with a performance-first approach. That means it must “support modern data models, and processing engines, enable AI/ML, and deliver composable [microservices](/solutions/microservices/),” as described by Redis CMO Mike Anand in the keynote. The dev experience should be **fast, smart,** and** simple**. How are microservice-based apps and analytics powered by AI/ML algorithms helping to deliver an end-to-end real-time user experience? Let’s take a look at the day’s sessions, what they covered, and even watch the full recordings on-demand.

## Keynote: Infuse Real-Time AI Into Your “Financial Services” Applications

**Mike Anand**
**Chief Marketing Officer, Redis**

“The digital world is so deeply ingrained in our daily routines,” says Mike Anand. “Making an online purchase, playing online games, transferring money, paying by credit card – this is all performed with real-time data.” So many of our everyday processes are distinctly connected to real-time data.

![mike anand quote redisdays ny](/images/site-mirror/fec623afc9c3cba66ecda074b188628ef1fbe1f0-1024x585.webp)

Today’s customers demand instantaneous results and as simple a process as possible. That’s why companies relying on legacy systems need to catch up and start creating modern applications. As Mike notes in the keynote, companies need to “rethink [their] applications using new design patterns like **microservices** or **event-streaming architectures**.”

That’s where [**Redis Stack**](https://redis.io/docs/stack/) comes in. “[Redis Stack](/blog/introducing-redis-stack/) allows you to power your legacy systems that may still be in place without a risky rip and replace strategy,” he continues. With Redis Stack, companies can begin their application modernization journey by delivering advanced AI/ML-powered services like [fraud detection](/docs/fight-financial-fraud-with-real-time-data-platform/), algorithmic trading, loan approval, underwriting, middle office, back-office processes, and more.

Listen to the keynote to hear more from Mike Anand on how businesses can integrate AI/Ml into their standard operations and how they can sidestep the challenge of operationalizing AI/ML.

**Taimur Rashid**
**Chief Business Development Officer, Redis**

The keynote progressed to an overview of trends in the [financial services industry](/industries/financial-services/) and specific use cases that can be addressed when applications are strengthened by AI capabilities and become more real-time. Taimur Rashid, Chief Business Development Officer at Redis notes that the key differentiator is **the customer experience**.

![taimur presentation in financial services](/images/site-mirror/1bce235248a9f9f813992a0e78c29b0050fe899b-1024x576.webp)

“When you look at digital applications’ capabilities becoming more real-time, there’s a variety of imperatives that most modern applications have,” he notes. Chief among them are “**speed**, scalability, staying always-on, global distribution, security, and **AI-enhanced**.” Speed is the most important variable here. “In the financial services industry, speed really matters. Milliseconds can make the difference between millions, sometimes billions of dollars.”

In the keynote, Taimur highlights some of the trends in financial services, like digital capabilities, the customer experience, new business growth, as well as **financial crime**, and [**cybersecurity**](/blog/data-economy-podcast-improving-security-with-digital-twins/). “As more businesses move their operations online,” he says, “there’s a need to make sure that money that’s being moved globally is being moved in the proper way and according to the right regulations. Organizations need to protect themselves from financial crime. With more activity being shifted online, cybersecurity is very important. How do you protect yourself against bad actors and threats that are outside your organization?”

![pascal belaud quote](/images/site-mirror/a69b07337310e5be87fcc05579d24bdcbbcdf6a8-1024x585.webp)

After a demo from Redis Sr. Product Manager AI/ML Ed Sandoval on [vector similarity search](/blog/build-intelligent-apps-redis-vector-similarity-search/) in action (more on this in the following session), Taimur sat down for a discussion with Microsoft’s Managing Director for Customer Success Data and AI Group, Pascal Belaud.

![redisdays new york 2022 pascal belaud quote](/images/site-mirror/5b44b99630b0d26878d474f37e7dbc9b010a5fdd-1024x585.webp)

During this chat, Pascal breaks down how Microsoft works with different customers, like Allstate Insurance, for instance, to leverage AI/ML. Some of the uses he specifies include capturing voice calls with customers, which are then transcribed using AI techniques. These transcripts are immediately enriched with all the details Allstate needs to handle any claims without having to contact the customer a second time. It’s all part of the customer experience AI/ML-infused digital applications are working toward.

Watch the full [**keynote**](/redisdays/).

## Behind the Scenes: Using AI to Reveal Trading Signals Buried in Corporate Filings

![ed sandoval agenda](/images/site-mirror/8f6fd333b8e2edfec95e250e00dc5924fd0e097e-1024x523.webp)

Midway through the keynote, Ed Sandoval presented a demo featuring the vector similarity search available in Redis. In this session, Ed is joined by Charles Morris, the Head of Enterprise Data Science and Financial Services at Microsoft, to present a behind-the-scenes look at how that demo was built. While Ed focuses on Redis’ vector similarity technology, Charles focuses on Microsoft Azure’s ML infrastructure and the services used to build the demo.

![charles morris redisdays quote](/images/site-mirror/fd03061e87c23cc70f5d3cdf9daf3e597d17cffd-1024x585.webp)

In this demo, Ed and Charles demonstrate how AI is used to surface copious amounts of buried valuable information out of U.S. public company corporate filings submitted to the SEC. Watch and see as they both share insights from their collaboration and some of the key lessons learned along the way.

Watch the [**behind-the-scenes demonstration**](/redisdays/).

## Operationalizing AI/ML in the Enterprise

What are the tools and processes that empower data scientists? What needs to be done to push everything into production when integrating AI/ML into your operations?

In this panel discussion, Taimur Rashid is joined by Mike Gualtieri, VP, Principal Analyst at Forrester Research, and Mike Del Balso, Co-Founder and CEO of [Tecton](https://www.tecton.ai/), to talk about the transformational qualities of machine learning. Companies are trying to mainstream AI/ML tech, but how does it get scaled reliably? Many organizations run on legacy systems, but how do they modernize with growing needs in the digital space?

“AI has become foundational,” says Mike Gualtieri. “It’s become strategic for enterprises. It’s not a science fair experiment. It’s not an innovation experiment. Most companies believe that they’re going to need AI. AI is software and those software development processes are very important to getting that model, to operationalizing it, and getting the business value on those applications.”

![](/images/site-mirror/7214cce82b1991fd1618230d28c47c1a65b588c1-1024x585.webp)

Mike Del Balso of Tecton shared some of his experiences with ML, in particular with regard to his previous role at Uber. “Our goal with the ML platform at Uber (Michaelangelo) was to democratize ML,” he says. “To make ML possible for the 100+ use cases we identified from the beginning, where ML intelligence could really influence the product and the customer experience.”

Get the full scope when you watch “[**Operationalizing AI/ML in the Enterprise**](/redisdays/).”

## Microservice Patterns Made Easy

What are the best ways to implement best practices design patterns to build and scale microservice apps reliably? That’s the topic of discussion in this session between Redis’ Field CTO Allen Terleto and Viren Baraiya, Co-Founder and CTO of [Orkes](https://orkes.io/).

“The overhead and inflexibility of a monolithic application is unacceptable,” says Mike Anand before introducing the speakers. “With the shift to microservices, one of the main benefits is that each service can have its own fully decentralized data store and each component can be changed and updated quickly without impacting the entire service while reducing the blast radius if a microservice goes down.”

![redisdays-new-york-2022-viren-baraiya-quote](/images/site-mirror/c09728f6e42316d5179eca4202d5b71404efdf26-1024x585.webp)

In this session, Allen and Viren look into microservice issues, such as orchestration, state management, error handling, and observability. But as noted by Allen, growing microservices at scale can be complicated. He notes that when moving to componentized microservices, “[you have] new architectural patterns, architectural concerns, new technologies, a laundry list of pitfalls to worry about, especially as you scale to hundreds of microservices.”

Uncover more insights into microservice design patterns when you watch “[**Microservice Patterns Made Easy**](/redisdays/).”

---
