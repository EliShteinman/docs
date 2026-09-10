---
title: "Data replication and microservices compatibility powers emergency services"
linkTitle: "Data replication and microservices compatibility powers emergency services"
url: "/customers/mutualink/"
description: "Mutualink’s product required a fair amount of installation and configuration. However, to grow by orders of magnitude, Mutualink needed to add efficiencies throughout their stack; not only in how..."
group: "Technology"
lastmod: 2025-09-12
hidden: true
---

*updated 12 September 2025*

### Why Mutualink Selects Redis Enterprise

Mutualink’s product required a fair amount of installation and configuration. However, to grow by orders of magnitude, Mutualink needed to add efficiencies throughout their stack; not only in how entities are managed and configured but even in how devices are built and deployed.

Achieving a more self-service scalable deployment means that Mutualink has had to turn to more modern practices like microservices. Redis Enterprise was the best database for their needs because thanks to its microservice friendly architecture, they could overcome the inherent challenges of a stateless and highly distributed application.

Redis Enterprise’s CRDT-based active-active replication was also a product game-changer. When Mutualink found out Redis offered active-active architecture, it became such “must-have” that the team rethought significant elements of its next-generation system. As one of two NoSQL database providing CRDT-based active-active replication, Redis Enterprise offers real-time and conflict-free data consolidation among geographically distributed applications necessary for Mutualink’s future growth.

> "The importance of sub-millisecond latency and synchronization across all database instances cannot be emphasized enough. It’s crucial to our core mission and future growth, and the fact that Redis Enterprise could address that for us made it a clear winner."

### Customer requirements

- Extreme scalability with active-active replication. With plans to scale by several orders of magnitude, Mutualink needed a highly scalable database that could provide data consistency and consolidation across an ever-growing network of geographically distributed applications.
- Microservices compatibility. Mutualink’s next-gen system is built on microservices and required a database that inherently understands the stateless nature of this environment.
- High performance.The emergency nature of the communications that Mutualink’s system facilitates requires sub-millisecond latency.

### Redis Enterprise benefits

- CRDT-based active-active replication. As the only NoSQL database providing CRDT-based active-active replication, Redis Enterprise offers real-time and conflict-free data consolidation among geographically distributed applications.
- Microservices-friendly architecture. Built specifically with microservices in mind, Redis Enterprise has many features to achieve data persistence in a stateless microservices environment.
- Flexible data structures and commands. The individualities of many small datasets (e.g. text, video, file) are efficiently addressed for lightning fast emergency communications.

### A Next-Generation Database for a Next-Generation System

Mutualink’s hardware and software empower agencies worldwide to interoperate and communicate. The company connects two-way radio, phone, video, text, and data among thousands of global customers on its network. As Mutualink embarked on the next generational design of its popular emergency communications solution, a primary goal was to build a system that would allow the company to increase the scale of its deployments by a factor of hundreds, if not thousands, of users.

Achieving more efficient, self-service deployment has meant leveraging modern development and deployment practices such as microservices to achieve scalability and faster time to market. It’s also meant prioritizing the system’s ability to provide instantaneous data consistency and consolidation across an ever-growing network of geographically distributed applications. “At any point in time, our client programs might need to spontaneously deliver traffic to a different data center in a different part of the country,” said Kurmas. “In an emergency situation, we can’t tell our customers ‘sorry, you have to log out and log back in again because your mobile call moved to another data center’ so we need to ensure seamless rerouting in real time without data loss or conflict.” These next-generation system requirements translated into an urgent need to find a database that could overcome the inherent challenges of the stateless and highly distributed application environment that comes with microservices.

### Redis Enterprise Gets to the Heart of It

Redis Enterprise is the core of the central junction point operations for the next-generation system that Mutualink is building. This central junction point, referred to internally as the edge server, is the clearinghouse where all normalized multi-media communications among Mutualink’s customers interconnect. In this role, Redis Enterprise will act as a real-time, high-speed data store, performing many critical functions, including:

- Storage of the directory (i.e., living model) of the network that Mutualink publishes to its clients
- Knowledge management of all active conversations taking place so that Mutualink can track participation and make fine-grained authorization decisions in real time regarding who is allowed to take part in ongoing collaborations
- Multi-media event synchronization, and event distribution to topics or queues—either locally or between different geographic data centers, depending upon the event’s destination
- High-performing search across Mutualink’s directory of users with robust suggestions based on phonetic well as a direct spell to make it easy for customers to identify and engage other agencies during an emergency response quickly

To accomplish these functions, Mutualink takes advantage of Redis Enterprise’s many flexible data structures such as lists, strings, and hashes, as well as specialized features such as task queues, atomic calendar, and the RediSearch text search and secondary indexing engine.

Additionally, the development team intends to bring Redis’ newest data structure type, Redis Streams, along with Redis’ powerful geospatial data capabilities into the new system’s design. “We view location information as a key application asset, and so Redis’ geo-spatial commands are something we anticipate using strongly in the very near future,” said Kurmas. “And the efficiency of Streams definitely speaks to allocation of work in a microservices model.”
