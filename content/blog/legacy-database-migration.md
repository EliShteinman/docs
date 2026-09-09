---
title: "Legacy Database Migration: What To Know Before You Start"
linkTitle: "Legacy Database Migration: What To Know Before You Start"
url: "/blog/legacy-database-migration/"
description: "Legacy database migration. Those three little words can strike fear in the hearts of IT professionals — but they don’t have to! Let’s break down the process of migrating legacy data, outline the..."
date: 2022-10-28
blogCategories:
- "Company"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 28 October 2022 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/b8950c5010380c7077fd3462ec46264c5660f555-772x550.webp)

**Legacy database migration. Those three little words can strike fear in the hearts of IT professionals — but they don’t have to! Let’s break down the process of migrating legacy data, outline the pros and cons, and highlight considerations that industry professionals wish they knew before moving legacy data to an advanced system.**

For IT teams tasked with [migrating data](/redis-enterprise-cloud/migrate/) from legacy systems to a more advanced environment such as a [cloud database](/try-free/), a successful migration can have an enormous payoff. Still, the consequences of a failed execution could be dire. There’s no one-size-fits-all approach to database migration, but there are some key factors anyone attempting a migration should consider for a relatively painless experience. Let’s explore legacy database migration in both concept and execution.

## What is database migration?

Database migration is the process of transferring data from one database management system to another, or from one version of a database management system to a newer version. This process typically involves several steps, including extracting the data from the source database, transforming it if necessary to match the schema of the target database, and loading it into the target database.

Database migrations track the controlled transfer of a [schema](/blog/schemaless-databases/) from its existing state to a new environment. In any database migration, historical data is transferred from an older system to a new (and usually modern) database. Among the important goals are keeping the existing functionality working, optimizing performance, and improving maintainability.

With [open source](https://redis.io/) and relational systems such as [MySQL](https://redis.io/compare/redis-enterprise-and-mysql/) and [Oracle databases](/blog/why-your-oracle-db-needs-redis/), it can be challenging to make schema changes without jeopardizing data integrity. SQL databases infamously crunch data to fit their structure. Migrations are common for many reasons – developers regularly try out new tools – but when an application and its data store are both outdated and well-entrenched throughout an organization, moving data from one system to another presents additional difficulties. Quite often, these legacy database migrations are accompanied by a transition from a relational system, such as a [MySQL](/docs/modernize-your-mysql-database-with-redis-enterprise/) database, to a [NoSQL](/docs/8-data-modeling-patterns-in-redis/), or serverless environment, including the [cloud](/redis-enterprise-cloud/overview/).

## When should you perform a legacy database migration?

Old applications rely on older software ecosystems. Even if a legacy application appears to work – if it ain’t broke, don’t fix it, as the saying goes – the ecosystem may fail. Perhaps the host operating system is no longer supported. The hardware can’t keep up. The application (and its data) depends on APIs that are no longer supported, and it can no longer interact efficiently with newer systems. Or you inherit an application whose code and database design are arcane… but the programmer who knew the system retired.

Sometimes, the reasons for the change are due to business success. As the user base scales, so does the amount of data. It’s essential to make provisions for more users and more data, ensure that there’s no failover or [latency](/docs/latency-is-the-new-outage/), support a global user base, maintain speed, and deliver data in real-time.

Use cases change over time, too. Remember,[ Netflix started with DVDs](https://www.linkedin.com/posts/netflix_this-is-about-as-motivational-as-were-gonna-activity-6849148772665192448-B5_Y/). What happens when a business taps into a new revenue stream, but the legacy system can’t keep up? Older databases sometimes cannot take advantage of the potential of a new architecture.

Besides, there are technical advantages to adopting the newer technology, such as taking advantage of features that didn’t exist in the legacy system. The new-and-improved application can accomplish much more with an in-memory, multi-model, real-time database.

## What to consider before the migration process

Every database migration is unique, but people have been upgrading database systems since the second database was released. It’s wise to plumb the experience of those who have gone before.

To provide actionable guidelines on how to survive the experience, we solicited advice from dozens of IT professionals, developers, and database administrators who performed legacy database migrations. They recommend you include these items on your data migration checklist. (Identities are obfuscated because an individual’s historical experience may not reflect a current employer.)

### Immerse yourself in the new technology

Learn about the new-to-you technology before you start. You need to become confident using the new database. If you run into a snag, you want to know if you encountered a technical problem or whether you’re discovering the depths of your own ignorance.

You need to understand how and why things were done the way they are in the old system. And you also need to understand the new system’s capabilities and processes before you start the migration. Only then can you match the approach taken with the old system to the features and best practices used in the new system.

This isn’t just a data migration. It’s also a problem-solving migration.

Be open to new approaches. Sticking to “the old way” can result in a poorly designed new system. Users often blame the new system for that, not the migration.

### Design the data model and test it

Before you touch any data, model each query and compare how it’s used in both the old database and the new one. That can help you spot problems when they’re still on the whiteboard before anyone begins typing.

Some data won’t map well from one application to another. It’s best to find out how to address those issues before an entire team is committed to the project.

### Construct a complete software assurance plan

Quality Assurance should get involved early. They need to address the challenges in both data integrity and the applications that access the database in its new home. And they’re used to thinking about all the ways that things can go wrong – and to recommend what to do in failure scenarios.

Do you have a way to confirm that the data matches in both the legacy database and the new one? And to ensure that any system integration works correctly with old not-yet-migrated applications and the new ones that inspired the migration project. Think about that now instead of later.

Create full-stack integration tests that can test both “before” and “after” results against your endpoints, API, etc., to ensure the data is the same. This isn’t easy; subtle changes against IDs and dates can be challenging.

Run tests against a test database whose configuration is an exact copy of production or as close as you can make it. That means you need to create those tests.

You may need to schedule lead time to build a custom test framework if the system is unusual. That may be time-consuming, but experienced database professionals insist that building these tests and tools helps you to move tables to different schemas without a problem.

### Conduct a data review

Make sure your data is up-to-date and accurate in your current system before trying to move it to a new one. A data audit helps you make sure the data is up to date. Wasting resources on migrating erroneous data “builds rework into the process from the beginning,” says Karen, a software analyst.

Otherwise, you will start with garbage. Plus, everyone blames the new, unfamiliar technology rather than the data quality.

Don’t think about migration until you clean up your data. “Anything else is sloppy and will build rework into the process from the beginning,” says Karen. “This is an equally critical first step when moving any application to the cloud.”

“Always eliminate superfluous data,” says Karen. “Confirm that you are only requesting and sending the data required for the running processes.”

Find out how much data you actually need to migrate and in what time frame. It may be feasible to address the legacy database in stages or to use interim tools – though that can raise additional issues.

This process may be a project on its own. Your organization may need to ascertain the data retention compliance requirements, especially for historical data. Take care of that before you shift data from one database to another.

### Back up, back up, back up

Data is the lifeblood of every organization. Don’t skip on the design or the protection: security, backups, and verifications.

Make sure you have backups from before the migration starts. “I’ve seen companies trying to roll back to standby servers only to realize they’ve already replicated their bad data,” says one sadder but wiser database specialist.

Have a rollback plan for when things go wrong. Test that plan before you start making database changes.

You can lose time. But you don’t dare lose any data.

### Get executive sponsorship

The challenges in data migration generally aren’t technical challenges. They are business challenges.

A legacy database migration project is not trivial. If you find out that you lack the political capital to change processes, suggests one experienced developer, “Find another contract now before you waste 18 months of your life and come down with a stress-induced illness!”

If you encounter resistance from Management for any of these pre-migration tasks, take note, says an IT professional who learned to identify red flags. Be sure you get a signoff, in writing, on how much data loss is acceptable when restoring from backup. Expect to be told, “No data loss is acceptable!” Just tell them that’s fine, suggests the IT pro. “But lay out the time and costs involved in developing the tools necessary to ensure (and test) that replaying data from the new system onto the standby is reliable. Quite often, you’ll find they’re more accommodating to data loss, or they’ll identify a subset of data that must not be lost.”

## What to consider during the migration process

Once everything is set up, it’s time for the actual migration. Just be sure you pay attention to these suggestions.

### Log everything

Keep a table to map the legacy identity alongside the new identity for every row you insert so that everything is auditable. You have to be able to map any subsequent child rows to the appropriate parent.

### Hurry, but don’t rush

Don’t migrate to a target database in one fell swoop, or what’s called a “big bang migration.” That’s a lesson Andy, a DevOps specialist, learned the hard way. He regrets opting for that choice when his team moved from a SQL Server database to a cloud database. “We bit more off than we could chew, falling short of a seamless migration,” he says.

Andy wishes that he had connected the old database to the new one, then synchronized each piece of data in real-time, little by little. Then he could use the new database whenever possible, with an easy way to switch back and force the prioritization of the data. “The danger here is to migrate so slowly that you end up with the databases never completing the migration,” he admits. A general plan of attack and some deadlines are important.

Joseph, whose team managed the migration from a Microsoft SQL server to the cloud, warns of the same pitfall but also addresses that a balance is recommended. “You need to migrate in small increments,” he says, “but you can’t go so slow that neither the legacy SQL server nor the new cloud database gets the updated data.”

## What to consider after the migration process

Hurrah, the data is transferred to the new database. You’re done, right? Not hardly.

### Check for data accuracy

Verify that the data matches before and after the migration says Sue, who runs the computer systems for a small, family-owned contractor. Her company’s computerized data goes back to 1985, with at least four major database migrations since then.

Depending on the urgency of the legacy database migration, it may make sense to run systems in parallel. “Inject a shim into your data layer so that any activity on the legacy database also runs on the new database,” suggests Zack, a database administrator. “The layer can compare results before returning the app tier.” This method allows you to run the new and old databases side by side for a while and to confirm that the new database is operating correctly before you cut over.

### Plan for post-migration hijinks even if things apparently went well

“We definitely had a few issues post-migration,” reminisced Guillermo. “Some required us to learn more about the new system, such as monitoring, tracing, and telemetry. Some issues required us to upgrade to a newer version of software than we’d chosen, which meant reading patch notes. We also needed to create a few custom log analysis tools.”

### Make stakeholders responsible for the results

One database specialist has made an entire career performing legacy database migrations. For Elena, a key factor is creating a dedicated test environment for the new system (both front end and back, if possible) so that stakeholders can log in and review the results in the test environment.

Make sure the stakeholders sign off on their acceptance. “Never run a line of code in production that hasn’t had the results tested and approved in test,” Elena advises. “This gives stakeholders ownership over the results.”

### Resolve the data that doesn’t migrate right

If you encounter data that just doesn’t translate, don’t just say it’s impossible, Elena says. “Sit down with the stakeholders and ask them why they need that data and have them walk you through what they’re going to use it for. Once you have the actual business use case, you can almost always find a workaround to accomplish what they need.”

## Get familiar with migration tools

Custom systems aren’t always necessary. At least, you can build on existing migration deployment strategies, tools, and products.

### Data ingestion

The task of migrating from a legacy system to a target database is akin to a physical move into a new home. In that analogy, a [data ingestion tool](https://redis.io/solutions/fast-data-ingest/) would be the movers who package up all your assets, store the items safely for transport, deliver your goods, and decorate the new place (if you did your data audit right, that is).

Learn[ 6 Ways To Speed Up Your Application](/blog/data-ingestion-speed-up-your-application/) when you migrate to the cloud using [data ingestion](/solutions/fast-data-ingest/).

### Multicloud and hybrid cloud solutions

Perhaps a business needs a little bit of column A and a little bit of column B. A full migration of an on-prem to a new system doesn’t work for all. Introduce a[ caching](/solutions/caching/) layer into the existing stack to create a [hybrid environment](/redis-enterprise-cloud/multicloud/) that softens the cost of scaling operations entirely to cloud.

Read more on[ Enterprise Caching: Strategies for Caching at Scale](/docs/enterprise-caching-strategies-for-caching-at-scale/).

## Benefits of database migration

Is it worth it? Most of the time, yes.

Some legacy databases rely on third-party technology — technology that could become obsolete at any moment, leaving the data’s security in jeopardy. But there’s more besides the danger of archaic systems and getting trapped by vendor lock-ins.

Read[ Top 5 Benefits of Adopting a Cloud Migration Proof Data Layer](/docs/top-five-benefits-of-adopting-a-cloud-migration-proof-data-layer/) to understand the full value of the cloud.

## Migrate to cloud and experience real-time data performance

The first step to a legacy database migration is testing the waters. Remember, it’s not all or nothing—test drive data in a real-time cloud environment for free with [Redis Enterprise Cloud](/try-free/).

Looking for definitions to other related concepts? Check out our [glossary section](/glossary/).
