---
title: "Fully managed platform serves an average of 3TB of data and 200 million keys"
linkTitle: "Fully managed platform serves an average of 3TB of data and 200 million keys"
url: "/customers/biocatch/"
description: "With 70 million users and up to 40,000 operations per second, BioCatch’s database needed to be incredibly responsive, highly available, and easy to scale."
lastmod: 2025-09-12
hidden: true
---

*updated 12 September 2025*

###### The Challenge

With 70 million users and up to 40,000 operations per second, BioCatch’s database needed to be incredibly responsive, highly available, and easy to scale.

###### Solution

BioCatch relies on Redis Cloud, a fully managed Database-as-a-Service, which serves an average of 3TB of data and 200 million keys at any given moment to the many microservices that power the company’s applications architecture.

###### Benefits

Because Redis Cloud is a fully managed service, the BioCatch team’s time and resources have been freed up to work on strategic projects. Plus, since deploying Redis Cloud, BioCatch has had zero downtime and realizes an average latency of less than 0.96 milliseconds, even at peak traffic.

> “Most of our data now resides in Redis Cloud because it’s always available and it’s always highly responsive, no matter how you query it.”

James typically texts using his index finger. One day, he’s driving in his car with his daughter and gets a message from his wife. He asks his daughter to respond, and like most teenagers, she uses her thumbs to rapidly type out the message.

James’ wife never notices the difference, which doesn’t matter in this case. But BioCatch, the global leader in behavioral biometrics, uses its game-changing technology to note differences in the way users handle their phones for fraud detection and mitigation. BioCatch can track subtle differences in how users hold their phones or scroll across a screen to identify users in a wide variety of use cases.

As BioCatch’s unique technology attracted more customers, however, its existing stack could not keep pace with the 5 billion transactions per month the company was processing. Plus, scaling concerns consumed the technology team’s attention, leaving few resources to focus on new product features.

### Turning to Redis Cloud

A redesigned technology stack became top of mind for the next incarnation of BioCatch’s solution. With 70 million users and up to 40,000 operations per second, BioCatch needed its database to have performance, high availability, and seamless scalability. Another priority was decoupling compute and state to make the system more elastic. Session state was being kept across many virtual machines—if a VM failed, all of its sessions were lost. This configuration was a liability within the context of critical real-time fraud detection, but also very difficult and expensive to scale.

BioCatch chose Redis Cloud for its ease of implementation and exceptionally high performance. Redis Cloud became the centerpiece—and only stateful component—of BioCatch’s redesigned technology stack.

“We initially looked to Redis Cloud for caching, but quickly discovered that it is really good as a database—not just a simple database, but also a system configuration database,” says Dekel Shavit, BioCatch Vice President of Operations and Chief Information Security Officer. “Most of our data now resides in Redis Cloud because it’s always available and it’s always highly responsive, no matter how you query it.”

[Redis Cloud](https://redis.io/redis-enterprise-cloud/) is installed inside BioCatch’s virtual private cloud within the Microsoft Azure public cloud. Redis Cloud serves an average of 3TB of data and 200 million keys at any given moment to the many microservices that power the company’s applications. The biometrics company runs a few other databases alongside Redis Cloud, including Microsoft SQL Server, Apache Cassandra, and Apache Impala, but has been migrating more and more data into Redis Cloud.

BioCatch has leveraged many of Redis Enterprise’s features and data structures to create a single-source-of-truth database that serves a variety of mission-critical information across the entire organization, including behavioral, meta, and API data captured during active user sessions; user behavior profile subsets; predefined fraudulent behavior profiles; geolocation data; and system configurations.

### Zero downtime, issues, or operational hassles

As a Database-as-a-Service, Redis Cloud is fully managed by Redis. Since deploying Redis Cloud, BioCatch realizes an average latency of less than .96 milliseconds, even at peak traffic times, and has had zero downtime, zero issues, and zero operational hassles. This reliable managed services approach affords BioCatch the breathing room to focus on more strategic projects that serve the company’s core mission.

“It just works,” says Shavit. “We no longer need to cater to anything related to data at scale and we no longer need to try to anticipate the future infrastructure requirements of an ever-changing market 24 months in advance. We simply insert building blocks into Redis Cloud as we go and rest easy knowing that, whatever the future holds, Redis has us covered.

### Plans for the future

BioCatch may not be able to predict what the fast-moving identity fraud market has in store, but it does have a strong idea of where it wants to take Redis Cloud in the near future.

“Implementing Redis on Flash is a top priority,” says Shavit. “We have a big data set, but only a small working set, so Redis on Flash’s ability to store cold data in cost-effective Flash will bring us significant infrastructure cost savings.”

Another Redis Cloud capability BioCatch would like to leverage is Active-Active geo-distribution, which will improve support for multiregional clients and the timely sharing of fraudulent behavior profiles, so that insights gleaned from one region can quickly and automatically benefit all regions. As heavy users of Apache Spark, BioCatch is also interested in investigating Redis to better bridge the gap between the learning and predictive sides of its machine learning operations.

“Redis Cloud has been our silver bullet,” says Shavit. “It has helped us accomplish things we didn’t even originally plan to do that we now can’t live without, and we’re excited to keep exploring its many versatile capabilities.”
