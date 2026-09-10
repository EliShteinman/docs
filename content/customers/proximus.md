---
title: "Proximus powers public safety services with a real-time data"
linkTitle: "Proximus powers public safety services with a real-time data"
url: "/customers/proximus/"
description: "Proximus faced challenges handling large volumes of mobile signaling traffic while ensuring they met strict requirements for accurate location data storage. Their existing SQL-based solutions..."
group: "Telecommunications"
lastmod: 2025-09-12
hidden: true
---

*updated 12 September 2025*

###### A closer look at the challenge

Proximus faced challenges handling large volumes of mobile signaling traffic while ensuring they met strict requirements for accurate location data storage. Their existing SQL-based solutions weren’t up to the task, as they were too slow and couldn’t keep up with demand. Real-time processing is essential for Proximus’s commercial applications and legal obligations, such as government reporting, emergency services, and law enforcement requests. This meant the team needed a low-latency solution to deliver immediate and precise location data for seamless operations.

###### Finding the solution

They deployed Redis on virtual machines, with each data center hosting its own cluster. By leveraging core data structures within clustered databases, they achieved millions of operations per second while ensuring the high availability needed for an "always-on" service.

###### use case details

### Real-time crowd management (RTCM)

Real-time crowd management is what keeps the public safe during large events. Powered by Redis, the Proximus RTCM ‌app breathes life into complex data, mapping the movement of people with precision. Event organizers, police forces, and emergency teams rely on RTCM real-time updates supported by Redis. They now maintain throughput of 196,000 operations per second and a latency of 13.05 milliseconds, to create detailed heat maps and track crowd paths. Whether it’s a bustling festival, a packed sports event, or a major city gathering, RTCM ensures that authorities have the foresight to manage movements, respond to potential hazards, and keep public spaces secure.

> "Redis helps Proximus safeguard our communities by providing the real-time reliability needed for crucial services like emergency response and public safety alerts."

### BeAlert real-time location store (RTLS)

Proximus uses Redis to power its BeAlert RTLS—an advanced system that provides real-time location data for mobile users in specific incident areas. With Redis, Proximus achieves fast processing of location updates, handling an average of 750,000 operations per second with an average latency of just 0.9ms. This efficiency allows BeAlert RTLS to quickly send SMS alerts to people in affected areas during emergencies, greatly improving crisis response and public safety.

### Location-based data store (LBDS)

Proximus’ LBDS offers real-time tracking of mobile users during calls, crucial for maintaining public safety. Boasting an average throughput of 878,000 ops/s and a latency of just 1.31ms, LBDS guarantees precise caller location data for emergency call centers. This precision delivers accurate caller location, the power to detect fraudulent “fake calls,” and the ability to seamlessly support law enforcement when every second counts. Beyond legal obligations, LBDS is vital for emergency response and police interventions, enabling swift crisis responses.

###### conclusion

With public safety at an all-time focus for all global organizations, Proximus uses Redis at the forefront of interconnectivity. Proximus's strategic Redis integration has addressed critical challenges in handling high mobile signaling traffic volumes, as well as revolutionized its telecommunications services, legal compliance, and public safety initiatives. These achievements not only underscore Proximus’ commitment to technological innovation but also highlight its pivotal role in shaping a safer, more connected future for Belgium and beyond.
