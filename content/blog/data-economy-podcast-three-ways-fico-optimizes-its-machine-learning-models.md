---
title: "The Data Economy: Three Ways FICO Optimizes Its Machine Learning Models for Real-Time Financial Services"
linkTitle: "The Data Economy: Three Ways FICO Optimizes Its Machine Learning Models for Real-Time Financial Services"
url: "/blog/data-economy-podcast-three-ways-fico-optimizes-its-machine-learning-models/"
description: "The Data Economyis a video podcast series about leaders who use data to make positive impacts on their business, customers, and the world. To see all current episodes, explore the podcast episodes..."
date: 2022-05-03
blogCategories:
- "Company"
- "Podcast"
authors:
- "Isaac Sacolick"
lastmod: 2025-03-27
hidden: true
---

*By Isaac Sacolick, Contributor · Published 3 May 2022 · updated 27 March 2025*

![Blog tile image](/images/blog/c90b511f8f55f810bd56b53d13ae71f0871cff52-500x356.webp)

***The Data Economy****is a video podcast series about leaders who use data to make positive impacts on their business, customers, and the world. To see all current episodes, explore the podcast episodes library below.*

---

You can’t just put your [machine learning](/press/redis-labs-introduces-landmark-machine-learning-module-redis-redis-ml/) (ML) models in the cloud when your algorithms must process thousands to tens of thousands of transactions per second within 10 and 20 milliseconds.

And you can’t sacrifice accuracy or explainability when your ML models impact roughly 80% of all credit card transactions.

These are some of the requirements Scott Zoldi, [FICO](https://www.fico.com/)’s Chief Analytics Officer, shares in his recent interview for *The Data Economy* podcast. And Zoldi isn’t shy about sharing challenges, insights, and methodologies on how a 60-year-old company like FICO pushes the boundaries on the R&D, infrastructure, and ongoing management of its real-time machine learning models.

Scott, with over one hundred authored patents, shares the following insights, but you’ll have to watch the podcast to get all his detailed nuggets of wisdom.

## Tip 1: Understand the customer impact

Scott simplifies the latency requirements from a customer perspective: “Can you imagine if you’re at a point of sale and it takes two seconds for you to wait for your credit card to clear? No one has patience for that.”

It’s not just latency that drives FICO’s requirements, because making the wrong decision around fraud and credit decisions hurts consumers, merchants, banks, and other financial institutions. Zoldi shares insights on the tradeoffs between latency, analytics accuracy, costs, and other constraints when FICO architects its customer solutions.

In the podcast, [CIOs](/business/), CDOs, and IT leaders will learn how FICO creates new business opportunities, protects its reputation, and gains a competitive edge through its data science and technology methodologies. As Scott says, “For FICO, what’s unique is that we’ve been real-time at scale for more than thirty years. It’s really part of our bread and butter.”

For data and IT leaders, selecting[ enterprise real-time data platforms](/redis-enterprise-cloud/overview/) and operating them in [multicloud environments](/redis-enterprise-cloud/multicloud/) is the foundation for building, testing, integrating, and deploying machine learning models.

[Click here to view video](https://www.youtube.com/embed/oshYnZYnvkI)

## Tip 2: Optimize infrastructure and ML models for real-time data processing requirements

In a real-time streaming environment, knowing the data sequence is critical for decision-making. For example, you probably hope FICO sees that your email was changed seconds before a large transaction and then flags the merchant about a highly likely fraudulent transaction—all in real-time.

The speed and accuracy of ML models go into FICO’s architecture decision on what parts of the data processing and model run on edge computing and other elements that operate in the cloud. “If I chew up milliseconds, just getting to the cloud and back, that adds overhead to the overall value proposition,” Scott stresses.

And it’s not just an infrastructure constraint. Scott shares this key insight around why his team researches and develops ML models before readying them for production use cases: “Some of the commodity functionality you find in a cloud-based environment may not be really meant for real-time computing.”

It’s a key insight for data and IT leaders debating their architectures, especially around optimizing hybrid and multicloud architectures, scaling the data layer (hint: FICO looks well beyond traditional relational databases), or managing low latency and high quality of service.

A key strategy for data and IT architects is to develop[ flexible data structures](/redis-enterprise/data-structures/) such as key-value data stores, geospatial indexes, and data streams to support managing, indexing, and querying a variety of real-time data sets.

## Tip 3: Foster multidisciplinary collaboration to support the full life cycle of ML models

While Scott oversees FICO’s analytics functions, it requires a strong collaboration between data scientists, software developers, and cloud engineers to integrate models into real-time production environments. “We are part product managers because we have a view of what we need to meet the business objective,” says Scott. “We have to advance the state of the art of how our software deals with real-time constraints. We have this tight interlink between the role of us, a data scientist, a product manager, and a software developer.”

For FICO, developing and supporting full life cycle support starts with R&D teams that only explore fully explainable ML models. The company also doesn’t throw all its data resources at every problem, and it doesn’t want to impute bias by bringing more data than required. Scott recognizes that “each data element brought into a solution adds liability to the decision.”

The team looks beyond explainable AI, and in the podcast, Scott shares his definitions of “humble AI,” “responsible AI,” and “interpretable AI.” He believes that in the future, consent on whether, how, and when customers permit their data to be used in models will require a new wave of compliance and innovation.

Please tune in to the podcast to hear more of Scott’s insights on developing and supporting ML models for [real-time financial services](/industries/financial-services/).

---

Watch more episodes of [**The Data Economy**](/the-data-economy-podcast/)podcast.
