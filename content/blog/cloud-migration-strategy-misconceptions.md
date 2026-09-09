---
title: "Cloud Migration Strategy Misconceptions"
linkTitle: "Cloud Migration Strategy Misconceptions"
url: "/blog/cloud-migration-strategy-misconceptions/"
description: "We bust persistent myths about migrating your workloads to a large cloud provider like AWS."
date: 2023-07-03
blogCategories:
- "Uncategorized"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 3 July 2023 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/d5f66087270aa88fff842f8c450c3535a87cf41b-772x550.webp)

**We bust persistent myths about migrating your workloads to a large cloud provider like AWS.**

You’re committed to a cloud migration. Great. But you need to get the data out of your existing system and into the new one.

No problem, you think. You know just the right way to go about it!

Or do you? Several experienced tech experts suggest that plenty of people make wrong assumptions that cost time and money while causing unnecessary frustration. For something that no longer seems novel, a remarkable number of misconceptions about migrating to the cloud persist. That’s true even when the issue is the practical matter of the migration process —the data transfer process, as we discuss here—rather than overall misconceptions about operating in the cloud in general.

We explore what causes people to get these wrong ideas, explain what the reality is, and offer resources to help you learn more.

## #1: You should always start your cloud migration plan with a “lift and shift.”

One common cloud migration misconception is that you should always use a “lift and shift” approach to get your workloads into the cloud as quickly as possible. “Lift and shift” means porting applications and data as is from an on-prem environment to a cloud vendor infrastructure without rearchitecting them for the cloud. Just get it moved over, and think about redesigning later!

Many companies employ this strategy with the very best of intentions. They start with a lift and shift to get everything into the cloud as quickly as possible, and they have grand plans to rewrite everything to be cloud-native later on. Spoiler alert: the company often never gets around to doing that.

There usually are valid reasons for starting a migration this way. It seems the fastest way to get your workload into the cloud—like throwing all your belongings into boxes and organizing everything once you move into the new house. Sometimes there’s an urgent need to get workloads out of physical on-prem servers and into the cloud, and those reasons are justified, such as an office lease termination, a company acquisition, or fears about aging equipment that is at risk of failing (“We need to get our critical applications off this sinking ship before it’s too late!”).

**THE REALITY: **Sometimes a “lift and shift” approach is the right one. But it should not be your default choice for a cloud migration strategy.

One example of the need to think things through is when the legacy system technology architecture is outdated and there are no equal technology components in the new cloud environment. In such a scenario, you don’t really have a choice. You can’t lift and shift because there’s no parallel system to which to “shift” it.

Sometimes the decision to migrate is motivated by the fact that your existing licensing costs are too high, and you’ve found an alternative technology in the cloud. But in such a scenario, it’s much better to retire the old system. Take the time to refactor and rearchitect the application from scratch, remodel the data, and run that new cloud native version in the cloud. Because while you *can* pitch all your belongings into random boxes and sort it out later in the new house, it’s silly to do so if you can go about the process in a more organized manner. If nothing else, it means you have a better chance of finding the coffee maker on the first morning.

The misconception is that you should *always* start with a lift and shift. The problem is with the “always.” Sometimes it actually is the right way to get started. If your strategy when developing your on-prem applications was always to be cloud first—for example, you use containerization technologies in your on-prem environment—then it’s very easy to lift and shift workloads to the cloud because they will run there the same way as they do on prem.

So if you have been employing virtualization techniques right from the beginning in your on-prem applications, you are already cloud ready; a lift and shift makes sense. (AWS offers helpful automation tools such as AWS Application Migration Service to help you get started.)

## #2: You can handle a cloud migration by yourself. You already know everything you need to know.

Many companies believe that a cloud migration can be handled by a small team of in-house generalists, or that it’s a good idea to hire consultants or contractors to handle the migration and then transfer maintenance to an internal team after it’s complete. A related misconception is that you will save on staff costs after migrating to the cloud.

But none of this is necessarily true.

**THE REALITY: **Migrating to the cloud is a complex process that calls for subject matter experts with deep cloud technology expertise to manage the project. A successful migration requires an experienced team. Ideally, those individuals include a migration solutions architect, data architect, cloud solutions architect, enterprise architect, and IT or DevOps engineer. Those are specialized skill sets, and while one person can wear many hats, the roles are not interchangeable.

Nor is it true that these roles are superfluous once the migration is done. A cloud migration is rarely a one-time event, especially for large companies with numerous legacy applications to bring into the cloud over time. Plus, data residency requirements often need some upstream or downstream systems to remain on premises, and you must maintain a bi-directional path between the cloud environment and the on-prem one. In such a scenario, you need to retain those experienced cloud experts to maintain these complex systems.

Going the consultant/contractor route comes with its own set of problems. Often the handoff to your internal team once the project is finished is rushed and abrupt, and your existing staff doesn’t understand the intricacies of a system that they were not involved in building. Nor are consultants always focused on building a system that is maintainable, so it’s out of date in a few months after they have turned in their deliverable.

All of these factors are why it’s important to make sure you have the right team in place to both handle the migration and maintain the system afterward.

## #3: You should migrate the least important workloads first so you can test the process beforehand.

It’s natural to think in terms of starting small when a company is beginning to migrate its data and applications to the cloud. It’s common to begin by migrating the least important workloads with the fewest dependencies so the team can learn the process and gain confidence in the migration’s technical demands. In fact, this is a recommended approach, and AWS offers advice on how to prioritize applications for initial migration, including choosing low-risk, low-complexity workloads to reduce risk at the outset.

But just choosing the “least important” app is not necessarily the right approach.

**THE REALITY: **You should conduct a cloud readiness assessment to prioritize your workloads. Make this a key part of your cloud migration plan.

Which workloads should you migrate first? Ideally, choose a workload that has maximum business impact with minimum risks involved. Keep the overall process iterative. Migrate in small increments, with a crawl-walk-run approach as you learn the process and gain confidence.

But while you’re learning, you also want to deliver value. No company wants to invest in the cloud without seeing some business value. Part of the workload assessment should include “What’ll impress the boss?” even if you don’t word it that way on the report.

A cloud migration is also probably not the best time to “learn on the job.” It’s a complex process that should be managed by a team of people who have cloud expertise. Such professionals should know how to best prioritize workloads for initial migration, ensuring that the cloud migration initiative brings value to the business quickly.

## #4: Expect similar or better SLAs immediately after the migration is complete.

It’s easy to think of on-prem legacy systems as antiquated and outdated, while the cloud has a reputation as cutting-edge, advanced technology. So techies can assume that once they migrate their workloads to the cloud, they will have similar or better SLAs right out of the gate.

If you drive an old clunker for years and then buy a new sports car, it makes sense to expect a much faster ride the minute you drive your new car off the lot. But when it comes to a cloud migration, that’s not always the case.

**THE REALITY: **When you migrate your existing infrastructure and system architecture to the cloud, it won’t necessarily operate the same way. Nor will it necessarily be faster or better immediately. Even though you may get a better ride quality in your new sports car on day one, it can come at the cost of other things, such as fuel efficiency and familiarity.

Improving the SLAs is a laudable goal. But, as with any other element in migrating data to the cloud, it takes planning.

First, define your existing system’s SLAs and its configurations. Then run a separate benchmark in the cloud to determine how those SLAs are affected. Is latency increased because of additional hops in the system architecture, or is it much faster? Define those SLAs in the new cloud environment and then choose your cloud resources accordingly, depending upon the system requirements. Then tweak the configurations to achieve those required SLAs.

This is work that is normally done by the cloud architect, data architect, and migration solutions architect on your migration team. Only after you have done all this careful configuration should you conduct the actual migration.

## #5: Getting your workloads into the cloud removes the need for complicated replication and failover plans.

Another misconception is that, if you bring all of your architecture and technology stack over to the cloud, you no longer need complicated replication and failover plans to protect applications. The thinking is that once your workloads are in the cloud, they are “safe,” like a file that was backed up into cloud storage.

This idea might come from the abstraction of the cloud as a non-physical space, as opposed to the very physical presence of on-prem servers, which are clearly vulnerable to damage from natural disasters and other disruptive events. But it’s a dangerous idea.

**THE REALITY:** It’s a misconception that if you simply bring your applications, architecture, and full technology stack to the cloud, then replication, failover, and high availability is all ensured. It’s not. The truth is, it depends on how you configure your cloud instance.

When you bring your workloads to the cloud, you must make a choice whether or not to run them across multiple regions. The entire cloud and global infrastructure is divided into regions, and within each region there are data centers, also known as availability zones (AZs). For example, the AWS Cloud currently spans 99 AZs within 31 geographic regions around the world, and Amazon has plans to expand that. You can think of these AZs as “data centers,” each of which is at least 150 miles away from one another. You could design and deploy an application in the cloud and bring it to only one region; if there’s a natural disaster such as an earthquake and the system goes down, then so does your entire application. But if you choose a multi-region deployment, your application will have failover protection. So it really comes down to how you design your deployment.

If you are currently running your system on prem, you always want to have multiple copies of your data and multiple server instances running so that if one fails, your data is backed up and you are protected. But now your organization has made the decision to migrate to the cloud. You could just move the bare bones, the one single copy of your application first to get it up and running in the cloud, see how it performs, and go from there. Or you can bring the entire complexity over with it—the replication failover, the entire technology stack. But if you do that, you bring more complexity to the cloud without even knowing how it’s going to run there.

Don’t further complicate your migration project. Migrate the application over as is, without worrying about all bells and whistles. Bring the simplest form of your application to the cloud, see how that goes. After the bare bones functionality is working in the cloud—and you can demonstrate its value to upper management—add the high availability aspect, the failover aspect, the replication aspect

## The cloud beckons

A well-executed cloud migration plan requires careful planning, expert guidance, and a phased approach that prioritizes workloads effectively. Embrace the opportunities and navigate the challenges of cloud adoption wisely, ensuring a successful and efficient migration process for your applications and data.

For detailed, step-by-step instructions on how to get your cloud migration off the ground, read this helpful guide, Migrate Redis Workloads to Redis Enterprise Cloud on AWS.

*Many thanks to Redis Senior Cloud Solutions Architect Srinivas Pendyala for his insight and help with this post.*
