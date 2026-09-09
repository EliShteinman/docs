---
title: "With Redis Enterprise’s Vector Database, Superlinked is Revolutionizing Personalization"
linkTitle: "With Redis Enterprise’s Vector Database, Superlinked is Revolutionizing Personalization"
url: "/customers/superlinked/"
description: "Watch the video"
lastmod: 2026-09-01
hidden: true
---

*updated 1 September 2026*

###### Watch the case study video

[Watch the video](http://youtube.com/watch?v=e7x-bIaaGXQ&feature=youtu.be)

###### Challenge

Today’s software developers are tasked with creating applications that understand user behavior so they can surface relevant content, match users with each other, detect malicious bots, and segment users by behavior.

###### Solution

Redis Cloud provides a highly responsive, scalable vector database and index that powers Superlinked’s management of the process to represent users and content with vector embeddings.

###### Benefits

Superlinked makes machine learning technology more accessible and easier to embed in popular applications. Developers can launch personalized experiences in hours, without the need for advanced machine learning, MLOps, or data science expertise. Since deploying Redis Cloud, Superlinked has sustained periods of non-stop heavy usage (100+ vector search queries per second) with 95 percentile latency at 30ms.

> "Our real-time recommender infrastructure needs to search and update vector embeddings in milliseconds to deliver a blazing fast experience for our marketplace, e-commerce and social customers. We benchmarked all the leading vector databases on the market, and Redis Cloud came out on top."

### Introduction: Empowering developers to create personalized user experiences

To engage today’s discerning users, software applications must be intelligent enough to immediately adapt to individual needs, including delivering custom content and recommendations. A growing number of organizations use machine learning (ML) technology to create these adaptive, personalized experiences. However, while personalization shows tremendous potential, the vast majority of corporate ML initiatives are struggling to move beyond the test stages.1 According to a recent Gartner survey, nearly two-thirds of digital marketing leaders have difficulty offering personalized experiences to their customers. Meanwhile, those organizations that succeed in putting machine learning into production typically see a 3 to 15 percent increase in profit margins.2

Superlinked helps software developers build applications that understand users and deliver personalized and engaging experiences. This small but rapidly growing company has developed a software infrastructure that empowers machine learning operations (MLOps) teams to create models that understand user preferences, content properties, and other variables. Sometimes called “ML infrastructure as-a-service,” Superlinked’s unique data processing and configuration engine makes ML technology both accessible and easy to use.

“We help organizations that don’t have large data science teams to access ML technology and use it within their applications,” says Daniel Svonava, co-founder at Superlinked. “Vector database technology from Redis is playing a key role as our customers build these complex products. It’s all about ingesting data about your content, understanding what users are doing, and capturing information as people create accounts, sign up for services, and indicate their preferences. We encode all of this information as vector embeddings. Redis Cloud helps us store and index the information.”

By tailoring content to the needs of each application, Superlinked’s technology platform helps organizations build detailed customer profiles and, consequently, deliver more relevant content and recommendations. Its unique personalization technology is quickly gaining traction among social media platforms, online marketplaces, and first-party data-focused e-commerce companies.

“We had very specific requirements for a vector database,” Svonava reports. “We looked at the available options, and determined that the Redis Cloud best fit our needs.”

### The right database technology for the job

Vectors are mathematical representations of data points. This type of database structure is useful for AI and ML apps that function by transforming unstructured data into numeric representations. [Vector search](https://redis.io/solutions/vector-database/) capabilities allow a machine learning app to find data points that are similar to a given query vector. They are commonly used for recommendation systems, image and video searches, natural language processing, and anomaly detection.

“A lot of benchmarks for vector databases focus on search performance,” Svonava explains. “However, we are more interested in the speed of data input and data output for vector operations. When we compared these measurements among the leading offerings, Redis Cloud was the top performer.”

Another distinguishing factor was that Redis Cloud allows developers to execute code inside the system rather than merely querying external code modules. According to Svonava, the C++ language, which Redis Cloud supports, is preferable for these embedded code modules because of its sophisticated memory management capabilities. He also likes having the ability to offload part of a database index into flash memory to maximize performance.

“Some of the other vector databases use garbage collection for memory management,” Svonava adds. “These databases can have difficulty satisfying our real-time requests because they introduce random latency spikes, which make some queries ten times slower. C++ support in Redis Cloud is important for us.”

Superlinked has built a “Vector Ops” platform that ingests contet, users, and events and enables real-time recommendations and search. All of this is made possible by leveraging Redis Enterprise as a vector database. **See example diagram below.**

![Redis](/images/site-mirror/ba8a71f57665b18e69633d98c911a1f251a2d6f4-815x360.svg)

### Turning behavior signals into engaging experiences

Any site or application that utilizes user-generated content can benefit from the Superlinked infrastructure because it helps to personalize the stream of data and information that is presented. “Accurate, relevant content is what keeps people engaged,” Svonava says. “Real-time data crunching in Redis Cloud reveals what users are interested in and how best to present the right content to them. It has to be done quickly as people scroll through their feeds.”

According to Svonava, the software industry is moving from relatively crude matching algorithms, which utilize hard-coded rules to personalize content, and towards interactive, real-time experiences, in which the system observes and responds to user behavior. Consider job marketplaces, which automatically match open positions with available candidates. In one such marketplace, Superlinked uses the Redis Cloud to store semi-structured data about the various properties of each open job and each candidate. Redis Enterprise’s vector technology allows this customer’s job marketplace to observe how users behave in real time. “Instead of having a fixed set of filters, it learns from how people interact with the data,” Svonava adds.

Other job recommendation engines use rigid scoring mechanisms that can’t discern the many subtle, ever changing relationships within these data sets. Lists of locations, job titles, seniority, and other data points are hard coded in these rules, and data is extracted through a basic search interface.

### Easy, cost-effective deployment in Google Cloud

Superlinked purchased [Redis Cloud](https://redis.io/cloud-partners/google/) through the Google Cloud Marketplace, which allows Svonava and his team to leverage the advanced capabilities of Redis without having to deal with the operational overhead of installing and managing complex software infrastructure. Tight integration between Redis Enterprise and Google Cloud makes it easy to build cloud-native applications.

“Redis is easy to use with the one-click Redis Cloud setup,” he confirms. “We have one account in Google Cloud. We installed Redis Enterprise through this account, which allows us to pay for everything through the Google Cloud Marketplace. It’s really convenient.”

These types of cost-effective, cloud-native software deployments are helping to fuel steady growth in some of the technology industry’s fastest growing markets. For example, the MLOps market reached $1.1 billion in 2022, and is expected to grow 41% per year to $5.9 billion by 2027.3 According to Precedence Research, the broader AI market reached $119 billion in 2022, and is slated to grow 38% per year to $1.5 trillion by 2030.4 This growth coincides with a surging demand for personalization engines that can be adapted to all types of use cases. User modeling accounts for a large portion of both the technology and talent needed to take advantage of these market opportunities.

“Users expect great search and recommendation functionality in every application and website they encounter,” Svonava sums up, “yet more than 80 percent of business data is unstructured—stored as text, images, audio, video, or other formats. That’s why vector databases with powerful search features will fuel the next generation of applications.”

1 IEEE Access, “Machine Learning Operations (MLOps): Overview, Definition, and Architecture,” March 27, 2023
2 “Emerging Technologies Are Key to Executing an Effective Personalization Strategy for Digital Marketing,” (Gartner press release, April 14, 2021)
3 Markets and Markets, “MLOps Global Forecast,” December 2022 (Report Code: TC 8518).
4 AI Market Forecast, 2022 to 2030.
