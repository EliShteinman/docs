---
title: "Inovonics: Choosing the Right Sensor to Work with RedisEdge for IoT Applications"
linkTitle: "Inovonics: Choosing the Right Sensor to Work with RedisEdge for IoT Applications"
url: "/blog/inovonics-choosing-right-sensor-work-redisedge-iot-applications/"
description: "In my previous post, I gave a high-level overview of our Redis-based, industrial Internet of Things (IoT) technology at Inovonics, which is the leader in wireless networks. I will give more details..."
date: 2019-06-19
blogCategories:
- "Guest Blogs"
authors:
- "Lalit Pandit"
lastmod: 2025-03-04
hidden: true
mirrored: true
---

*By Lalit Pandit, Software Development Manager · Published 19 June 2019 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/af8cd92e892e69cbe569f72942c141bfc9cf8b7f-800x800.webp)

In my [previous post](/blog/inovonics-uses-redis-enterprise-drive-real-time-iot-data-analytics/), I gave a high-level overview of our Redis-based, industrial Internet of Things (IoT) technology at Inovonics, which is the leader in wireless networks. I will give more details on each of our system components in this and subsequent posts, and introduce you to some of the more technical features of Redis (and Redis Enterprise in particular) that we use at Inovonics.

To recap my previous [post](/blog/inovonics-uses-redis-enterprise-drive-real-time-iot-data-analytics/), the following components comprise a full IoT system:

1. Sensors (also known as “end points” or collectively referred to as the “edge”): Devices used to measure a property, such as pressure, position, temperature or acceleration, and respond with feedback. Examples include video doorbells, wi-fi thermostats, security cameras, etc.
1. Network: The protocols, payload and mesh for transmitting data between sensors and gateways. Examples of network protocols are Wi-Fi, Lora, 900MHz proprietary protocols, ZWave, ZeeBee, etc.
1. Gateways (or “routers”): The bridge devices between sensors and the cloud.
A Wi-Fi router is one such gateway.
1. Cloud data store and application: The central repository for storing and analyzing messages, and displaying information from the messages.
1. Network engineering: The art and science of placing sensors strategically to maximize the information obtained.

Be aware that gateways, cloud data stores and network engineering can be configured in several different ways, and in some cases can be skipped altogether. At a minimum, an IoT system needs sensors, a network and some way of managing data from the sensors. Redis offers a portfolio of technologies and products for data storage, event triggering and analytics across all of these components. For this post, let us discuss the eyes and ears of the system, namely its sensors.

In choosing or designing sensors for a specific application, consider the following list of criteria:

- Environment: Operating conditions play a huge role in the longevity of a sensor. For example, a sensor built for dry, indoor conditions may not survive the temperature and humidity of an outdoor coastal area. Similarly, sensors built for a home environment may not be able to withstand the dust and smoke at an industrial complex.
- Line/battery power: Sensors can be line-powered and/or battery-powered. For a line-powered sensor, you will have to ensure that power lines are available at the sensor site; for battery-powered sensors, you have to be sure that battery life will meet or exceed the expected longevity in the field. Some of Inovonics’ battery-powered sensors work for 10-plus years without requiring any maintenance.
- Transmit/receive: Sensors can work in a “transmit only” or “transmit/receive” mode. In transmit only, sensors can only send data to the gateway, whereas in receive mode, they will accept data or commands for execution.
- Listener/doer: Sensors can act as listeners and/or doers. For example, in listening mode, a sensor will report only the temperature in your house. However, in doer mode, it can actually perform the task of shutting off your furnace if the temperature exceeds a certain threshold.
- Simple vs intelligent: Currently, more intelligence is being added to sensors. For example, instead of sending raw data and messages for collection, sensors can perform filtering and send only required triggers as necessary.
- Field/over-the-air upgradeable: Sensor firmware can either be upgraded remotely, or it requires a technician to go to the site to service the sensor in-person.
- Location awareness: Many sensors these days have location awareness through GPS or a programmable location, so they can easily be located.
- Security: The physical security of a sensor has to do with theft prevention and tamper proofing, while cybersecurity concerns center mainly around hacking, through which a sensor’s behavior could be modified.
- Data rates: Sensors’ data rates can vary widely depending on the application. For instance, temperature sensors typically send small amounts of data at designated rates, while video sensors can send large continuous streams. Making the edge more intelligent can reduce data rates by sending only relevant information.

Last but not least, when selecting a sensor, the cost of the sensor itself is a major consideration. This includes both the sensor’s material cost and the installation cost. Keep in mind that each application may require other, more specific criteria for sensor selection. For example, when choosing sensor electronics, data treatment implications also influence its performance (speed) and the cost of your sensors. A sensor might work with its data in any of the following modes:

**Sensor without separate explicit data storage**: In this model, the sensor simply sends and receives messages when triggered. For example, a temperature sensor may send a notification when the temperature rises above a certain threshold. In addition, the sensor may be equipped with some electronics in order to perform calculations (e.g., counters). Some pulse-encoded sensors send a message when the number of pulses exceeds a certain value since the last message. Typically, hardware electronics manage the state of the sensor without requiring a separate data store.

**Sensor with short-term data storage**: Here, the sensor is equipped with storage—such as internal flash or local storage—to temporarily buffer the data. The sensor may process and send only information of interest, or it may simply choose to send data in batches. Buffering can help synchronize the speed of sensing and transmitting data. A buffer can also guard against wireless network outages because the sensor simply resends the data. A sensor may choose to store its state as well, in which case a power cycle on the sensor will not cause any loss of state or data. A sensor fitted with a camera for pictures or videos will usually have a temporary data store.

**Sensor with long-term data storage**: One scenario for longer-term storage is when a sensor may not have any means of communicating on a wired or wireless network. In these cases, a technician visits the sensor periodically to retrieve its data. If you use these types of sensors for applications with stringent demands, it is very important to ensure that the data does not get lost due to any hardware or software issues.

If your application demands high volumes of data storage for either the short or long term, [RedisEdge from Redis](/solutions/redisedge/) can be an excellent complement to your IoT environment. It is a multi-model database that was purpose-built for the demanding conditions at the IoT edge. Since RedisEdge can ingest millions of writes per second with <1ms latency and a very small footprint (<5MB), it works great for constrained compute environments. And even though RedisEdge is best known for its blazing-fast performance, its reliability in storing data also adds value to applications where performance may not be the driving factor. RedisEdge gracefully meets the diverse data services needs of IoT edge environments that might require multiple data models (e.g., time-series or graph data) to support video streaming analytics, image recognition or other complex computing requirements.

Regardless of the data store you choose, there are several trade-offs you may decide to make in your sensor selection. For example, a more “intelligent” sensor may require more powerful processing at the edge, which would drive up costs and impact battery life (due to higher power draw). In addition, harsh environmental conditions and tamper proofing requirements to bolster physical security may necessitate sturdier devices, which would increase costs as well. Given all of this, it is always important to analyze your short-term and longer-term application requirements and determine the ideal sensor for your use case. In my next blog, I will discuss network implications to consider for designing your IoT system.
