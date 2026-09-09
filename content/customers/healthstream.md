---
title: "HealthStream scales its SaaS platform reliably with Redis Enterprise"
linkTitle: "HealthStream scales its SaaS platform reliably with Redis Enterprise"
url: "/customers/healthstream/"
description: "HealthStream’s SaaS model leverages microservices and cloud components as expected from any SaaS-based model. Considering the geographic distance and network challenges for some of their customers,..."
lastmod: 2025-09-12
hidden: true
---

*updated 12 September 2025*

###### The Challenge

HealthStream’s SaaS model leverages microservices and cloud components as expected from any SaaS-based model. Considering the geographic distance and network challenges for some of their customers, HealthStream always needs to minimize server processing time to achieve the performance their customers require.

###### Solution

HealthStream selected Redis Enterprise as a performance-enhancing component of its solution due to Redis Enterprise’s sub-millisecond latency, high availability, and performance. Complementing the expertise shown in Redis’ open-source database are no-hassle enterprise deployment processes and trouble-free maintenance provided through customer support specialists.

###### Benefits

Since initially adopting Redis Enterprise for its data caching speed and performance, HealthStream has expanded its use to realize additional performance gains in areas such as large, enterprise reports delivery.

> “One of the key benefits of implementing Redis Enterprise has not only been maintaining low latency on their servers, but they’ve [HealthStream] been able to solve problems that weren’t originally anticipated.”

[HealthStream](https://www.healthstream.com/) initially introduced its learning management system as its singular application to healthcare organizations, adding extensive content offerings, starting primarily around the year 2000 and thereafter. The popularity and efficacy of online learning for training and development in healthcare quickly escalated as the company grew and began offering additional applications on its platform—all focused on supporting the healthcare workforce. Today, HealthStream’s hStream platform is used for customers’ access to multiple application suites for a wide range of needs by healthcare professionals. Given its expansive ecosystem of applications, tools, and content, HealthStream is the nation’s leading provider of workforce solutions for the U.S. healthcare industry.

HealthStream’s very early learning and development solution began in the 1990’s during the early days of computer-based training with a networked MacIntosh-based product. As the Internet became ubiquitous, the company moved towards delivering their platform as a service written in a monolithic Microsoft technology stack.

“This redesign turned out to be pretty effective because we haven’t had to do a full-blown redesign until today, and now we’re starting to break apart pieces and turn them into services,” notes Spenser Aden, Senior Director of Product Architecture at HealthStream.

### Scaling a SaaS Platform with the Rise of Digital Learning

As utilization of HealthStream’s platform grew over time, HealthStream’s product architects had a choice: continue to add hardware to meet their scalability needs––which ultimately doesn’t last terribly long––or think creatively about their architecture and design of the platform.

HealthStream concluded that one critical technology which could solve their scaling needs was to implement a cache. After trying different options, they found not only a solution, but also a partner with Redis Enterprise. The product’s built-in enterprise-grade reliability, and, if issues do arise, the quality of the Redis customer support services effectively eliminate the need for HealthStream to fix a problem if they ever do arise.

Aden says, “It really wasn’t cost effective to maintain [open source] Redis internally; it was a lot better to get involved with others who were experts in the technology. Plus, as generally is the case, you get a better product up front that’s more reliable for a production application at scale.”

### Finding Creative Solutions with Caching

One of the key benefits of implementing Redis Enterprise has not only been maintaining low latency on their servers, but they’ve been able to solve problems that weren’t originally anticipated. A critical feature that many of HealthStream’s customers require is monthly organizational reporting, which can sometimes involve hundreds of thousands of student record entries for a single customer.

Because the reports need to encompass time-sensitive data and are repeatedly executed by various administrators, the monthly reports had started to become a pain point in the performance of the platform. Aden’s team came up with an innovative, easy solution: cache the enormous reports in Redis Enterprise the first time an administrator pulls the report and subsequent pulls from that customer are executed from the stored data in the cache.

“Because the data was already in Redis and it’s been a big success, everybody will have forgotten that that’s where we started,” says Aden. “But it was a big pain point for our large customers, and this was a really easy solution to that specific performance issue when they need to run monthly reports.”

### Delivering Excellence in Healthcare Workforce Development

Today, as HealthStream continues its innovative product evolution to meet the challenges of the evolving healthcare landscape, the company continues to leverage the cloud—as all new applications are being developed for cloud deployment and delivery. As they proceed, Redis Enterprise will continue to provide the performance and flexibility HealthStream requires without wasted infrastructure resources. For HealthStream, this means greater ability to focus on its innovative solutions to support the healthcare workforce in delivering patient care excellence.
