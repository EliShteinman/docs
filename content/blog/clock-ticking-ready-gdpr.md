---
title: "The clock is ticking – are you ready for GDPR?"
linkTitle: "The clock is ticking – are you ready for GDPR?"
url: "/blog/clock-ticking-ready-gdpr/"
description: "You’ve likely heard about the General Data Protection Regulation (GDPR) that begins on May 25, 2018. These requirements put forward by the European Commission, harmonize data privacy laws across..."
date: 2018-03-28
blogCategories:
- "Company"
authors:
- "Priya Balakrishnan"
lastmod: 2025-03-27
hidden: true
---

*By Priya Balakrishnan, Sr. Director of Product and Partner Marketing · Published 28 March 2018 · updated 27 March 2025*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

You’ve likely heard about the General Data Protection Regulation (GDPR) that begins on May 25, 2018. These requirements put forward by the European Commission, harmonize data privacy laws across the EU with the overall intent of protecting private information for European citizens. GDPR’s key principles revolve around data privacy and subject rights in our increasingly data-driven world.

Under this regulation, when there is a data breach in an organization that holds EU citizens’ information, there are strict procedures for how the company must respond. Given this data privacy overhaul, all of us need to become more diligent about how we collect and store data, and what we do with it. In this blog, let’s explore some of GDPR’s critical new data protection frameworks, and how you should adapt your environment in order to meet them.

**1**

**It’s not just an EU thing!**

We’re all impacted by privacy laws and non-compliance penalties are big. This new regulation broadly affects all organizations, government agencies and companies throughout the world that collect or use personal data tied to EU residents (irrespective of any physical operating presence in the EU). Any organization failing to satisfy the new regulations will face maximum penalties of 4% of global revenues or €20M, whichever is higher, as well as the potential suspension of further data processing.

Lots of organizations are preparing for it, but many are unlikely to be fully compliant by May 2018. Gartner [predicts](https://www.gartner.com/en/newsroom/press-releases/2017-05-03-gartner-says-organizations-are-unprepared-for-the-2018-european-data-protection-regulation) that more than 50% of organizations will still not be in full compliance by the end of this year — seven months after the regulation takes effect. Yet while complying with GDPR is a HUGE initiative, organizations that make the effort will gain the faith and trust of their customers.

These policies completely change the way data has to be handled and are going to change how you approach your data. So, how do you prepare?

**2**

**Data-related policies:**

GDPR has many regulations directly related to how data is accessed, stored and protected in the database layer. Here are a few to consider surrounding data design and storage:

- *Privacy by Design* requires that optimal data protection is provided as standard, by default, across all uses and applications. Organizations need to focus on data privacy from their initial design stages and throughout the complete development process of new products, processes or services that process personal data.
- *Right to Access* demands that organizations outline and provide individuals with copies of information about whether or not personal data is being processed.
- *Data Portability* mandates that organizations provide a copy of personal data in a commonly used machine-readable format if desired by the individual.

**3**

**Database compliance:**

It is important to note that full compliance with GDPR cannot be enforced with infrastructure changes alone. It is a heavy process involving policy definition and enforcement, evaluation of the complex application and IT landscape, automation (where possible) to enforce governance and modernization of infrastructure if necessary. One such layer that definitely needs evaluation and compliance is your database. Let’s look at some of the specific database implications below:

1. **Know where your data is:** You are likely to store data in a number of places, be it multiple databases or stashed away in various other locations. You might have data stored on legacy systems or backups that you aren’t even aware of. All of this needs to be accounted for, so the first thing to do is create a map of your data and an audit of which databases, data stores, and file systems contain personal data. Some key questions to assess include:
  - What personal data, is processed?
  - How is the data collected and stored?
  - Is the data stored locally on your servers or in the cloud or across both environments?
  - Is the data backed up?
  - Is the data hosted by a third-party vendor?
  - Is the data minimized to only what you explicitly require?
1. **Ensure true data erasure**: As more and more systems are added on top of each other, there is no one system that hosts all the data in a single place. Identify the personal data your organization has, and ensure that you can securely erase it from your database once the expiration period has been reached. You’ll want to have answers to the below questions:
  - For how long is data stored, and when is the data deleted?
  - When data is no longer necessary for its original purpose, do you need to keep it in the system?
  - Is the data accurate and kept up to date?
  - Is deleted data really gone?
1. **Decide who should have access to the data**: Not everyone needs access to all your data. To mitigate risk, you need to restrict access to as few people as possible. Access controls allow you to manage who has access to what data. Ask questions like:
  - What controls do employees and users have, over data collection and retention?
  - What data protection training have those individuals received?
  - What security measures do those individuals work with?
  - What data breach notification and alert procedures are in place?
1. **Protect your data**: Protecting your data by pseudonym-ising and/or encryption can help ensure the privacy and security of personal data. Consider:
  - Is the data encrypted?
  - Is it anonymized or pseudonymized?
  - What data breach notification and alert procedures do you have in place?
1. **Maximize security**: Set up your security systems to do the most to protect your databases. While data travels across the firm in all kinds of ways, it is important to not only track it, but to also put all of the protection and security layers you need in place. Find out:
  - What are the technical and security measures at the data’s host location?
  - If data is transferred outside the European Union, what are its protective measures and safeguards?

While you’re reviewing your processes and changing your organization’s data policies to meet regulations, your business, of course, cannot be interrupted. So, how do you ensure that it continues to meet business demands while also preparing for these imminent compliance requirements? It’s a good idea to simplify your assessments and secure your environment by using solutions and tools that inherently meet the standards of compliance.

**4**

**Redis Enterprise meets GDPR compliance standards!**

For the database layer, we at Redis have spent a LOT of time making sure your deployments are secure. With Redis Enterprise, you can simplify compliance and protect your data to meet any self-imposed or industry standard security needs. We understand that data is the most valuable asset organizations have today. How it is captured, used and stored is the key to capitalizing on new technology and developing new revenue streams. Since the announcement from the European Commission, we’ve been working diligently to ensure our database software meets all GDPR regulations — demonstrating our commitment to data protection.

Redis Enterprise is a [secure database](/redis-enterprise/technology/enterprise-grade-redis-security/) that provides a great deal of controls to help you meet security standards. Each database in the system can be isolated using distinct credentials, limiting access to data. It offers multi-layer security configuration for access control, authentication, encryption, forensics, availability and more. Redis Enterprise’s capabilities include data encryption both at rest and in transit. For more on this, check out our recent [webinar](/events/redis-security-and-access-management-build-vs-buy/) about how Redis Enterprise helps deliver advanced data security and encryption or the cross-links in this post that describe our security architecture in great detail.

Lastly, another great opportunity to learn more about Redis Enterprise is at our annual user conference, [RedisConf](/redisconf/). It is just over a month away—April 24th through the 26th in San Francisco—and will include training programs that deep dive into the inner workings of Redis, as well as a slew of keynotes, sessions, and topics delivered by industry leaders, community speakers and Redis experts. We hope you will join us there to learn how Redis Enterprise takes you one step closer towards data compliance, as you prepare for D-Day 🙂

If you have any questions, please do not hesitate to [reach out to us](/meeting/).
