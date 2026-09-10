---
title: "5 Microservices Misconceptions"
linkTitle: "5 Microservices Misconceptions"
url: "/blog/5-microservices-misconceptions/"
description: "Many misconceptions about microservices persist, often to the detriment of companies hoping it’s the silver bullet to solve all their problems."
date: 2023-02-28
blogCategories:
- "Company"
authors:
- "David Gaule"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By David Gaule, Contributor · Published 28 February 2023 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/cdde96f6cbc9ec52e88e9bb064f865f3cd50a390-772x550.webp)

**Many misconceptions about microservices persist, often to the detriment of companies hoping it’s the silver bullet to solve all their problems.**

A drive to be perceived as cool and trendy isn’t reserved for awkward teenagers. That motivation can also cause full-grown business executives to chase the latest shiny, new technology just because the cool (and successful) companies are using it.

That’s not to say that any given technology lacks value. However, sometimes the new item—such as [microservices](/solutions/microservices/), [Kubernetes](/blog/redis-enterprise-operator-for-kubernetes), Lambda functions, or [insert your own cool, new tech du jour]—is embraced or rejected for all the wrong reasons. Too often the adoption comes from [people who know the terms only as buzzwords](/blog/the-marketing-buzzwords-that-developers-hate/) rather than the technology’s benefit as an actually useful solution that applies to a genuinely annoying problem. Which may not be theirs. That leads to hyperbole, and that’s unfair to the tech at hand.

Microservices is today’s victim of corporate mythology, where software assumptions create barriers to sensible adoption and usage. It’s time to clear the air with the help of technologists who have hands-on experience. These are the microservices misconceptions they encounter most often.

## Misconception: Microservices solve all your problems

Microservices are great – as long as they solve a problem your company actually has. The old adage is relevant here: “When all you have is a hammer, everything looks like a nail.”

“Many companies think, ‘We have this application landscape, and microservices are the answer,’” says Lars Rosenquist, a partner solution architect at Redis. “But first you need to understand what microservices are; next, you need to understand the problems of your own application architecture; then there needs to be a match between the two. And there rarely is.”

Many technologies solve specific problems at a specific scale. “If you’re a company like Netflix and [your applications consume a third of internet traffic](https://time.com/3901378/netflix-internet-traffic/#:~:text=Netflix's%20dominance%20over%20our,from%20about%2035%25%20in%20November.), you’re going to have to do things with your architecture to make that work,” explains Rosenquist. “But if you’re a smaller company, such as a local bank, you’re not operating at that scale—so you don’t need to fix that problem. People often optimize for the problems they want and not necessarily for the problems they have.”

People often optimize for the problems they want and not necessarily for the problems they have.

Lars Rosenquist

Partner Solution Architect, Redis

- 1

Most use cases do not require microservices. Avoid the “monolith is bad, monolith is the old way of doing things” mentality, suggest several programming experts. Instead, try to prove yourself wrong about that premise before you adopt a microservices approach.

## Misconception: Microservices reduce complexity

In fact, a [microservice architecture](/blog/microservice-architecture-key-concepts/) almost always *adds* complexity. Worse: If left unchecked, it turns into a distributed monolith – and that gets messy.

Microservices do not fix system design problems. “If you can’t create a monolithic design with high cohesion and low coupling, you’re likely to do worse with microservices,” says George Dinwiddie, a software development consultant, and coach at iDIA Computing.

Start with a monolith, and then extract services from it as you add teams and suggest several developers. [Conway’s Law](https://martinfowler.com/bliki/ConwaysLaw.html) applies.

“With a monolithic application you have all the logic, communication, and complexity in one application,” says Rosenquist. “With microservices, you turn this inside out.” The result: All these communication patterns and such are now part of your infrastructure.

Many companies don’t really understand this problem, Rosenquist believes. They think they can make the complexity go away with microservices. But you don’t really make it go away; you just move it to a different layer of abstraction.

“Let’s say you have two application components communicating with each other. They live in the same application, in the same process, in the same CPU. That application is pretty fast and is not very likely to fail,” says Rosenquist. But with microservices, you put those application components on different machines, with a network in between them, a whole battery of infrastructure, and maybe even different [clouds](/redis-enterprise-cloud/overview/). “That becomes a completely different challenge—not just in terms of communication and failure modes but also in terms of performance.”

Managing the complexity has become easier with the tooling that’s now available, but don’t discount that the complexity still exists. For one thing, complexity makes it harder to debug applications. To make managing that complexity somewhat easier, ensure that your monitoring and observability work is in place.

While a microservices approach certainly makes your code less complex, Rosenquist points out that it’s not always easier when it comes to deploying or managing it. “Instead of having one application to debug, you now have six or ten. Those applications are also running on multiple instances, which are also load-balanced across the entire architecture.” To assemble all that, pay attention to things like log aggregation and observability. All of which are generally more complex than having a single application.

Less complex code does not necessarily translate to a less complex system. “From a code standpoint, individual services might be slightly easier to understand in a silo,” points out William Johnston, developer growth leader at Redis. “But the complexity of the system you create with microservices becomes way more complex than in a monolith.”

That also means more development time, particularly in smaller teams that are already overloaded. That’s not always a bad thing because it forces developers to learn the application domain and the entire system. That can make refactoring easier in the long run since it makes the whole system less coupled. However, that comes with a high cost, and developer productivity might drop significantly.

That affects quality assurance, too. Typically, a microservice has so many dependencies that it makes it harder to test.

Taking it slow isn’t always possible for teams that need to meet tight deadlines or that may lack the background to adopt the technology quickly. “[Microservices] can be overwhelming technology for a smaller group of engineers or groups unfamiliar with it. It’s quite a different way of operating,” says John Obelenus, a software engineer at Boston-area startups.

## Misconception: One architecture works for everything

Don’t imagine that you can take one architecture and apply it to your entire landscape. Nor should you assume that you can immediately begin refactoring your old applications. Your old applications may not support these kinds of patterns, Rosenquist says.

Distinguish between monoliths, microservices, and functions. A function does only one thing. They are really for specific architectures because they are more event-driven, says Rosenquist. That’s the case, especially with enterprise processes. If you decompose all your systems, you end up with a thousand things, and all your advantages are lost.

The best approach really depends on the specific use case. A bank, for example, is apt to have quite a few monoliths, says Rosenquist. “But if you look at the most run-of-the-mill applications that are powering your mobile banking app, that’s going to be microservices—say around 50% to 60%. Functions make up the remainder. So a typical enterprise will end up with a diverse landscape in terms of architectures, not a single one.”

At the end of the day, it really comes down to the people who build your software. “A great engineering team finds a way to be effective regardless of what software architecture or pattern you’re using,” says Johnston, “And a dysfunctional team will find a way to screw something up, whether it’s microservices, monolith, or anything else.”

And speaking of teams …

## Misconception: Microservices are primarily a technology

“One of the most common misconceptions about microservices is that they solve a technology problem,” says Johnston. “But really they solve a business or organization scalability problem.” If microservices don’t accomplish that goal, it’s a waste of time—and not the technology’s fault.

“I see a lot of people who are starting a new application, even as part of a large business, and they believe they need to start by separating the domains and start with microservices,” Johnston points out. “But if you don’t have a clearly defined business domain, you don’t want to start with microservices.”

To once again cite Conway’s Law, the communication patterns in your software landscape mimic those of your organization as a whole. “Say you want to go from a monolithic architecture to a microservices architecture,” says Rosenquist. “Look at how your organization is organized. Split up the teams to make sure that one microservice belongs to one team, for example.” This is a management issue more than a technology challenge.

Make sure that everyone understands what microservices are and how the technology is envisioned to solve the business problem. Different departments often have differing viewpoints on the nature of microservices. The advantages of adopting a microservice architecture are going to depend on the problem space and the organization adopting the technology.

## Misconception: Microservices allow teams to use their preferred technology

This isn’t a full-on misconception, according to Johnston and Rosenquist, because there is some truth to this perception. It’s just not always a good idea for teams to use different platforms.

One common perceived benefit of microservices is that everyone can use the languages, tools, and platforms they prefer. That does make sense in some ways, says Johnston. “If you have a very large organization with several teams distributed throughout the world, some teams may excel at [.NET](https://university.redis.com/courses/ru102n/), for example, and others at [Java](https://university.redis.com/courses/ru102j/). Then depending upon the business domain for their particular service, it might benefit them to use one technology over the other.” But, he cautions, support for additional development environments comes at the cost of increased complexity in the system. “This is why enterprise architects exist,” says Johnston. “They need to understand the system complexity.”

“Yes, you can choose a different technology for every microservice you have, but I really suggest you don’t,” advises Rosenquist. “If you have 500 microservices, you shouldn’t have 500 different technologies. Somewhere around five would be a better number.” Those are examples, of course; there is no one-size-fits-all approach. Use common sense and find a middle ground between what’s manageable and what holds developers back.

## Microservices misconceptions abound

While the misconceptions we shared in this post are definitely some of the more prevalent ones floating around, they are by no means the only ones. Some other microservice myths that our experts raised include:

- **Microservices make things faster: **“Microservices can lead to a slowdown because of the increase in network hops. You have to embrace eventual consistency, which you don’t necessarily have to do in other sorts of applications,” explains Johnston.
- **Microservices are actually small:** Don’t get lost on the “micro” in microservices, says Graham Lea, co-founder of technology consulting firm Archium. “Microservices should be smaller than monoliths, but ideally, a service encapsulates a medium-sized domain.” Small is a relative term; but the effort to get them very small is not the point, he adds.
- **You need one microservice per client type: **“Nobody thinks they think this, but they keep doing it!” says DevOps architect Mark W. Schumann of consulting firm Blue Herring. “Instead, consider one microservice per resource.”

If you didn’t harbor any of these misconceptions, congratulations—you’re an expert yourself. But if you did, don’t feel bad. You’re not alone. And we hope that you can now move forward with a higher degree of confidence, speak with more authority on this topic in your company, and embrace the benefits that microservices can offer.

Ready to adopt microservices in your shop? Learn how [Redis can help](/solutions/microservices/).
