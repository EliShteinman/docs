---
title: "Apna Empowers India’s Job Seekers with Redis Cloud’s Resiliency and Low Latency"
linkTitle: "Apna Empowers India’s Job Seekers with Redis Cloud’s Resiliency and Low Latency"
url: "/customers/apna/"
description: "To manage billions of rows of data and 50,000 read/write operations per second, Apna needed a high-performance database caching solution that could handle an escalating volume of traffic,..."
group: "Technology"
lastmod: 2025-09-12
hidden: true
---

*updated 12 September 2025*

###### The Challenge

To manage billions of rows of data and 50,000 read/write operations per second, Apna needed a high-performance database caching solution that could handle an escalating volume of traffic, mitigating issues with latency that were causing customer churn.

###### Solution

Redis Cloud caches data on millions of jobs, and cache prefetching improves query performance by anticipating what each Apna user wants to see from moment-to-moment.

###### Benefits

By boosting response time and delivering pertinent details about relevant jobs, Redis fills a critical gap between employers and individuals searching for work.

> “Redis Cloud allows us to pre-fetch pertinent details about relevant jobs, so it’s super-fast. The user experience is seamless. There is no lag time.”

Amidst the COVID-19 pandemic, which led to a loss of over 10 million jobs in India, [Apna](https://apna.co/) rose to the occasion, creating a go to platform for job search and professional networking. Apna now offers a unified platform for job seekers to explore opportunities, showcase their skills, and connect with diverse local communities across various industries.

Established in 2019, Apna has risen to prominence as India’s premier professional networking and comprehensive job search platform, empowering countless job seekers across diverse industries. With a presence spanning 70+ Indian cities, Apna boasts an impressive user base of 51 million citizens and partners with 500,000 employers, facilitating a multitude of job opportunities and fostering a thriving community through its robust platform.

Apna means “one’s own” in Hindi, which gives rise to the company’s forward-looking slogan: “Our time will come.” It’s an encouraging mantra to the site’s rapidly growing user base, many of whom are first-time internet users who need an easy way to access professional opportunities, collaborate with others, gain new skills, and join like-minded communities that can help motivate them to find jobs. Redis Enterprise is at the heart of Apna’s ability to deliver opportunities for these individuals.

“Soon after I started at Apna, we grew from 12 million users to 24 million users in six months,” says Suresh Khemka, head of platform engineering and infrastructure at Apna. “My job was to make sure that our velocity remains the same, along with the same level of security, reliability, and performance. Redis Cloud’s high availability and reliability has been tremendous.”

### The science of cache prefetching

Apna’s smartphone app uses AI technology to match job candidates with employers. Users simply need a phone number to create an account that gives them access to millions of job listings. Once they enter their personal information, Apna creates a virtual business card that can be passed on to employers.

Job seekers can log in at any time to search for pertinent job listings. With 500,000 daily job applications, displaying the right information to the right users at the right time is no small task. In order to keep users engaged, the data Apna displays needs to be germane to each search, personalized to each user, and presented instantly.

To manage as many as 50,000 queries per second, Apna loads session data into a Redis cache. “Most people spend 10 or 15 minutes in the Job Search area,” Khemka says. “As soon as they login, we pre-fetch their data and bring it into Redis.”

[Cache prefetching](https://redis.io/solutions/caching/) improves query performance by anticipating what each user wants to see, then grabbing that data from the storage subsystem before it is explicitly requested by the user. This technology is commonly used for continuous replication when write-optimized and read-optimized workloads have to stay in sync. With this caching pattern, the application writes directly to the database. The data is replicated to Redis as it changes in the system of record, so the data arrives in the cache before the application needs to read it.

### Upgrading to Redis Enterprise

Apna decided to standardize on Redis Cloud due to a common predicament: With billions of rows of data and a burgeoning volume of read/write operations, its previous database caching engine was not able to handle the load.

“With rapid growth we started seeing issues,” Khemka admits. “Our infrastructure was very fragile, causing excessive latency, lots of outages, and customer churn on the platform.”

At the time, Apna had about a dozen Redis caches running in Google Cloud Memorystore, but the infrastructure team wanted to explore other configuration options. “We determined that we could either build Redis Enterprise Software clusters on-premises, running on virtual machines, Kubernetes, or something of that nature,” he recalls. “Or we could complement and extend our Google Cloud environment with Redis Cloud.”

While both the on-premises and cloud versions of Redis Enterprise could easily handle the heightened activity, the team opted for the cloud version because they didn’t want to spend time managing hardware and software infrastructure. It was a prescient choice: In short order, supplementing the Google Cloud environment with [Redis Cloud](https://redis.io/cloud-partners/google/) not only boosted performance, but also lowered costs. 

“Redis Cloud has been 15 to 20 percent less expensive than other in-house and cloud based caching solutions, and it delivers better performance,” Khemka confirms. “Redis Enterprise is working out very well for us.”

### One versatile database platform powers myriad of use cases

In addition to caching data for Apna’s Job Search portal, Redis Cloud now powers a **Job Feed service** that proactively delivers information about open positions to users who subscribe to various career feeds. 

In addition, as part of Apna’s **Communications service**, Redis Cloud sends more than 1 billion notifications per month via email, SMS, Android RC, WhatsApp, and other channels. In some cases, recruiters and job listers impose time constraints on these communications, which causes occasional spikes in volume. For example, some employers might require applicants to notify them only during business hours, which can lead to traffic surges just after 9 AM and just before 6 PM each day. Redis Cloud scales automatically to process these variable communication loads.

Redis Cloud also handles **session management and authentication** by managing fine-grained permissions for millions of users. For each user session, data is cached in Redis Cloud to control access privileges, authorize access to resources, and enforce data privacy requirements. Redis Cloud protects sensitive data and ensures superior performance by granting instant access to data in each user’s feed. 

“Redis Cloud is part of our extended architecture,” Puneet Kala, Head of Engineering, Marketplace sums up. “Whenever we build a new service, our developers ask, ‘Do I need Redis? Do I need a cache?’ In many cases, the answer is yes.”

### Powering new opportunities for India’s growing workforce

Initially, Apna built its application stack on a monolithic software architecture. However, as usage escalated, they began migrating to a microservices architecture—a collection of loosely coupled services that can be developed and deployed independently, and owned by small teams.

Redis Cloud facilitates microservices development by allowing developers to choose the data model that suits the performance needs and data-access requirements of each software deployment. Each microservice maintains its own data and can have its own Redis cluster.

“We began with our core services, such as the Job Feed service and Authentication service,” explains Ranveer Singh, Head of Engineering, Growth & Community at Apna. “And we are expanding from there. Currently we have 32 Redis clusters in Google Cloud. We don’t have to spend time managing the environment, which has resulted in a big boost to developer productivity.”

### Leveraging Google Cloud Marketplace to simplify scaling

As Apna’s user base continues to grow, it’s easy to add additional Redis Cloud clusters to support the rising activity. Apna purchased [Redis Enterprise through the Google Cloud Marketplace](https://console.cloud.google.com/marketplace/product/redislabs-public/redis-enterprise), which allows administrators to make purchases and request upgrades through Apna’s Google Cloud account.

“We like the marketplace services because Redis Enterprise is very well integrated with Google Cloud,” Khemka concludes. “Set up is easy, networking is fast, and we know that our data is secure. It’s very simple to create a new cluster or modify an existing cluster. If we have to scale up or scale down, we know Redis will *just work*.”
