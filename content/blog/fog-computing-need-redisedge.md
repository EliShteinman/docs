---
title: "Fog Computing and the need for RedisEdge"
linkTitle: "Fog Computing and the need for RedisEdge"
url: "/blog/fog-computing-need-redisedge/"
description: "Internet of Things (IoT) solutions present a unique challenge for any database. They produce increasingly large and fast data from a very broad spectrum of IoT devices, while requiring near-instant..."
date: 2018-10-25
blogCategories:
- "Product Releases"
- "Redis Modules"
- "Tech Redis Modules"
authors:
- "Rob Schauble"
lastmod: 2025-03-27
hidden: true
---

*By Rob Schauble, Senior Executive · Published 25 October 2018 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

Internet of Things (IoT) solutions present a unique challenge for any database. They produce increasingly large and fast data from a very broad spectrum of IoT devices, while requiring near-instant response times. Given this, the solution’s data processing and analysis must increasingly be handled at the network edge, as close as possible to the sensors, actuators and other IoT devices. We no longer have the luxury of being able to crunch IoT data in a cloud environment, where there is seemingly limitless compute and storage resources, because the latency would be unacceptable. Thankfully, there are powerful databases and platforms tackling this challenge head-on. But before we explore the solutions, it’s important to have a solid grasp of the data requirements unique to IoT environments.

Edge computing has increasingly become table stakes for IoT and big data applications, given their volume, velocity, variety and veracity (the “four V’s”) requirements, and the distributed nature of most use cases. So is there a way to maintain the data processing capabilities we have long enjoyed (and the very reason we’ve had a massive trend to cloud computing over the past ten years), if we move back to distributed computing at the edge? Can we have our cake and eat it too?

### Bringing Cloud Principals to the Edge with Fog Computing

Fortunately, in this case – with the popularization and growing trend of fog computing – the answer is yes. The solution is to bring cloud principals to the edge, where the fog and cloud environments operate in tandem to handle complex IoT use cases. When you have critical latency requirements (for example with smart city or connected car IoT use cases), that data must be handled by ruggedized fog nodes close to the IP cameras and other sensors, while non-latency critical data can still be synchronized to the core or cloud. In this way, data from all edge devices and fog nodes in your IoT solution can be aggregated at a core level (for example, a city block in the smart city use case), and ultimately to the cloud or data center environment for more in-depth business intelligence and other analytics.

![Fog Bridging the continuum between Cloud and Things](/images/site-mirror/20daa0af1efb926875fc46e02f0e7e3f925dfcee-1513x1072.webp)

With fog computing, we refer to data communication between IoT devices, edge devices, fog nodes and the cloud as “north-south” communication, and data communication between the edge/fog nodes across the system as “east-west” communication. For this to be effective, you must have common cloud or data center environment capabilities at the edge, such as machine learning, deep learning and image recognition. This presents our next challenge: how do we handle these needs, given the distributed nature and modest storage and compute capabilities of edge devices and fog nodes? Having fog and cloud environments operating in tandem is critical. For example, with machine learning, you might need to train models in the cloud (where you have vast compute and storage resources), and deploy those trained models to fog nodes and/or edge devices (so they can be served close to IoT devices for minimal latency).

### A Database for the “Intelligent Edge”

The “intelligent edge” has arrived and rescued us from these seemingly unsolvable problems (or Kobayashi Maru for you Star Trek fans). The edge is the battleground for IoT today, but is there a database on the planet that can handle its massively large and high-velocity data from potentially thousands of sensors, cameras and other devices? One that can process that data in real-time, with many different database models, and with a small footprint?

Fortunately, RedisEdge is a multi-model database that delivers blazing fast performance with the ability to ingest[ millions of writes per sec with <1ms latency](/docs/linear-scaling-benchmark-50m-ops-sec/) at the IoT edge. It can do this with a small hardware and software footprint, so it is perfectly suited to live on fog nodes, edge gateway devices and even IoT devices in some cases. RedisEdge has many native data structures (sets, sorted sets, lists, hashes, streams, etc.), providing ultimate flexibility for IoT application developers. Furthermore, with the many modules that already exist to extend it, RedisEdge can handle very diverse workloads required at the IoT edge (time-series, graph, machine learning, search, etc.). Rather than deploying five different databases to support these needs, RedisEdge can manage them all with a single instance, tremendously simplifying your architecture.

### Microsoft Azure IoT Edge + RedisEdge = Better Together

Now that we’ve shown there is a database worthy to take on the intelligent edge of IoT, you might wonder which platform is best-suited for running RedisEdge? Fortunately, the new Azure IoT Edge from Microsoft is purpose-built to take on this challenge! We are delighted to[ partner with Microsoft Azure](https://azure.microsoft.com/en-us/blog/azure-iot-edge-generally-available-for-enterprise-grade-scaled-deployments/) on IoT edge solutions, since both Redis and Microsoft are putting significant focus and investment into accelerating intelligence and computing at the edge. With RedisEdge integrated into the Azure IoT Edge runtime environment, joint customers and partners will enjoy a fast general data store, a [message broker](/solutions/messaging/) between Azure Edge modules, streams processing, a time-series database, and in-memory processing (for machine learning model serving, graph processing, etc.) to ensure the best possible performance.

Stay tuned over the coming weeks as we share more details on how the IoT community will benefit from our joint IoT edge solutions.
