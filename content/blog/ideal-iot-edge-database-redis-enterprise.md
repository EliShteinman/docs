---
title: "The Ideal IoT Edge Database – Redis Enterprise"
linkTitle: "The Ideal IoT Edge Database – Redis Enterprise"
url: "/blog/ideal-iot-edge-database-redis-enterprise/"
description: "Internet of Things (IoT) solutions present a unique challenge for any database. There’s increasingly large and fast data coming from a very broad spectrum of IoT devices, coupled with critical..."
date: 2018-06-27
blogCategories:
- "Company"
- "New Product Announcements"
- "Redis Open Source"
authors:
- "Rob Schauble"
lastmod: 2025-03-27
hidden: true
---

*By Rob Schauble, Senior Executive · Published 27 June 2018 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

Internet of Things (IoT) solutions present a unique challenge for any database. There’s increasingly large and fast data coming from a very broad spectrum of IoT devices, coupled with critical latency requirements. Given this, the data’s processing and analysis must increasingly be handled at the network edge, close to the sensors, actuators and other IoT devices. We no longer have the luxury of being able to crunch IoT data in a cloud environment, where there is seemingly limitless compute and storage resources, because the latency would be unacceptable. Thankfully, there are powerful database and platform solutions tackling this challenge head-on, which we’ll explore below. But first, let’s review some of the data requirements unique to IoT environments.

Edge computing has increasingly become table stakes, given the volume, velocity, variety and veracity (the “four V’s”) requirements of IoT and big data, and the distributed nature of many of these use cases. So is there a way to maintain the capabilities we have long enjoyed (and the very reason we’ve had a massive trend to cloud computing over the past 10 years) if we move back to distributed computing at the edge? Can we have our cake and eat it too?

***Bringing Cloud Principals to the Edge with Fog Computing***

Fortunately, in this case – with the popularization and growing trend of fog computing – the answer is yes. The solution is to bring cloud principals to the edge, where the fog and cloud environments operate in tandem to handle complex IoT use cases. When you have critical latency requirements, for example with smart city IoT use cases like gunshot detection or criminal face recognition, your data must be handled by ruggedized fog nodes close to IP cameras and other sensors. Non-latency critical data can still be synchronized to the core or cloud. In this way, data from all edge devices and fog nodes in your IoT solution can be aggregated at a core level (for example, a city block in the smart city use case), and ultimately to the cloud or data center environment for business intelligence and other analytics.

![](/images/site-mirror/20daa0af1efb926875fc46e02f0e7e3f925dfcee-1513x1072.webp)

Image courtesy of the [OpenFog Consortium](https://openfogconsortium.org)

With fog computing, we refer to data communication between IoT devices, edge devices, fog nodes, and the cloud as “north-south” communication, and data communication between the edge/fog nodes across the system as “east-west” communication. For this to be effective, we must have common cloud or data center environment capabilities at the edge, such as machine learning, deep learning and other artificial intelligence. This presents the next challenge: how do we handle these needs, given the distributed nature and modest storage and compute capabilities in edge devices and fog nodes? Having fog and cloud environments operating in tandem is critical. For example, with machine learning, we need to train models in the cloud where we have vast compute and storage resources, and deploy those trained models to the fog nodes and/or edge devices so they can be served close to IoT devices to minimize latency.

***A Database for the “Intelligent Edge”***

The “intelligent edge” has arrived and rescued us from these seemingly unsolvable problems (or Kobayashi Maru for you Star Trek fans). The edge has become the battleground for IoT today, but is there a database on the planet that can handle this massively large and high-velocity data from potentially thousands of sensors, cameras and other devices? One that can process that data in real-time, with many different database models, and with a small footprint?

Fortunately, there is one such database! [Redis Enterprise](/redis-enterprise/) has blazing fast performance with the ability to ingest [millions of writes per sec with <1ms latency](/docs/linear-scaling-benchmark-50m-ops-sec/) at the IoT edge. It can do this with a small hardware and software footprint, so it is perfectly suited to live on fog nodes, edge gateway devices, and even IoT devices in some cases. Redis Enterprise has many native data structures (sets, sorted sets, lists, hashes, streams, etc.), providing ultimate flexibility for IoT application developers. Furthermore, with the many modules that already exist to extend it, Redis Enterprise is a multi-model database that can handle very diverse workloads required at the IoT edge: time-series, graph, machine learning, search, etc. Rather than deploying six different databases to support these needs, Redis Enterprise can manage them all, tremendously simplifying your architecture. Many mission critical IoT use cases are distributed geographically across many regions – another use case Redis Enterprise handles gracefully with high availability, active-active (with CRDTs), disaster recovery, and auto scaling capabilities.

***Microsoft Azure IoT Edge + Redis Enterprise = Better Together***

Now that we’ve shown there is a database worthy to take on the intelligent edge, you might wonder which platform is best-suited for running Redis Enterprise at the IoT edge? Fortunately, the new Azure IoT Edge from Microsoft is purpose-built to take on this challenge! Redis is delighted to [partner with Microsoft Azure](https://azure.microsoft.com/en-us/blog/azure-iot-edge-generally-available-for-enterprise-grade-scaled-deployments/) on IoT edge solutions, since both companies are putting significant focus and investment in accelerating intelligence and computing at the edge. With Redis Enterprise integrating into the Azure IoT Edge runtime environment over the coming weeks, joint customers and partners will enjoy a fast general data store, a message broker between Azure Edge modules, streams processing, a time-series database, and in-memory processing (machine learning model serving, graph processing, etc.) for the best possible performance.

Stay tuned over the coming weeks as we share more details on how the IoT community will benefit from our joint IoT edge solutions. But if you’re looking for a quick read on the criteria to choose the right database for your IoT solution, [here](/docs/4-steps-select-right-database-iot-solution/) is a quick read.
