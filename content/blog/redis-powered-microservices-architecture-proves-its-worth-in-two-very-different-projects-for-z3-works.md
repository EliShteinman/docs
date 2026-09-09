---
title: "Redis-Powered Microservices Architecture Proves Its Worth for Z3 Works"
linkTitle: "Redis-Powered Microservices Architecture Proves Its Worth for Z3 Works"
url: "/blog/redis-powered-microservices-architecture-proves-its-worth-in-two-very-different-projects-for-z3-works/"
description: "(As organizations look to modernize their applications, many are turning to a microservices architecture to deconstruct their legacy apps into collections of loosely coupled services. This profound..."
date: 2020-03-10
blogCategories:
- "Company"
authors:
- "Miguel Allende"
lastmod: 2025-03-27
hidden: true
---

*By Miguel Allende, Customer Advocacy Manager · Published 10 March 2020 · updated 27 March 2025*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

*(As organizations look to modernize their applications, many are turning to a microservices architecture to deconstruct their legacy apps into collections of loosely coupled services. This profound change inspired us to reach out to Redis users in various stages of this journey to microservices architectures. We are telling their microservices stories in a series of blog posts, which *[*began in late 2019*](/blog/how-mutualink-uses-redis-to-support-a-life-saving-microservices-architecture/)*.)*

![](/images/blog/c015aa9e05a1de16c909d59b35f2fcc78c97e152-300x300.webp)

If you thought microservices architectures could be used for only a limited set of projects, a quick chat with the folks at [Z3 Works](http://www.z3works.com/) might convince you of the approach’s versatility. At the Brazilian software agency, Co-Founder Marcelo Nozari’s 20-person team designs and builds software for projects across a variety of industries, then passes off the code to his clients to deploy.

## Monoliths to microservices

![](/images/blog/602a935c4ef780b1fcc7abde8507b19d2f0ee0b1-290x300.webp)

Marcelo’s team helps a home-security company collect data from its video cameras, doorbell activity, and more, for example, providing real-time notifications to its clients. And Z3 Works’ newest project is helping a retailer transition its monolithic applications to a microservices architecture. While each project is in a different stage of production, microservices play a critical role in ensuring that the applications run effectively and in real-time.

For Marcelo, a microservices architecture means creating clear, separate services to help better manage the project. “Whenever you have smaller projects and smaller services, microservices makes it easier for you to deploy and avoid crashing everything else,” Marcelo says. The microservices architecture allows Marcelo’s team to work on small components and update and fix code as quickly and as often as needed.

To show the value Z3 is getting from its microservices approach, let’s take a closer look at a couple of very different projects:

## Home security systems

![](/images/blog/eb97875f328840a0f927b1f136526f67845a4d1f-1024x683.webp)

If your family is on a month-long vacation, chances are you’ll want to check on your home every so often. That can create a challenge for home-security companies. With so many different pieces in a home security system—from doorbells to security cameras to motion detectors to alarms—these companies need to compile all interactions in a single, up-to-date application.

At the same time, it’s increasingly important for security companies to provide real-time notifications to their clients. That lets clients learn about incidents as trivial as a package delivery while they’re on vacation—so they can ask their neighbors to bring the box in to prevent theft—as well as alerting them to critical threats such as a potential burglary.

Z3 Works partnered with a home security company that needed to manage all this data. The application Marcelo’s team built pulls data from 3–5 different kinds of data sources (including more than 7,000 different cameras!) into a Redis database running in the cloud. The system uses Redis as a caching layer, as speed is critical—customers expect an instant notification of any activity at their homes. “For doorbell pushes, for example, Redis makes it really fast to get this image from the cache and send it to the apps as a notification for users,” Marcelo says. Redis Pub/Sub also acts as a message broker for image requests, communicating between software functions responsible for fetching and those deploying the images.

The home-security project has been in production for about a year, Marcelo says, processing up to a terabyte of video every day and ingesting up to 3 million pieces of data per hour into a 50 GB database. Redis is a critical component of the home security vendor’s microservices architecture application—it uses Redis Pub/Sub to communicate between different services of the application and hold the tokens and counters for the vendor APIs, which are central to the data integrations, Marcelo says. If Redis went down, the application would no longer be able to process the data and deliver it to the user, who wouldn’t be able to see any new footage.

By using a microservices architecture, the application avoids bottlenecks and the team can easily fix code and small components as needed. Redis’ speed, high availability, and fast failover makes it critical for implementing a microservices architecture. Plus, Z3 Works can scale the client’s application as needed, making it more effective in the long run.

## Retail moves away from the monolith

Marcelo’s team recently started working with a major retailer to transition its monolithic architecture to microservices as part of an overall migration to the cloud. This project is still in the planning stages, Marcelo says, but the new architecture will combine some 10 different services.

With Redis-based microservices architecture projects spanning multiple industries, Z3 Works makes it clear that the combination is a powerful approach to turbocharge a wide variety of applications and use cases.

*Looking to learn more about microservices? Check out how *[*Mutualink*](/blog/how-mutualink-uses-redis-to-support-a-life-saving-microservices-architecture/)* uses Redis for a life-saving microservices architecture, and hear Redis Developer Advocates Kyle Davis and Loris Cro discuss their new free e-book, “*[*Redis Microservices for Dummies*](/docs/redis-microservices-for-dummies/)*,” on *[*The New Stack podcast*](/blog/redis-microservices-for-dummies-podcast-kyle-davis-loris-cro-the-new-stackj/)*.*
