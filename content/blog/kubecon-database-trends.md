---
title: "Database Trends Spotted at KubeCon Europe"
linkTitle: "Database Trends Spotted at KubeCon Europe"
url: "/blog/kubecon-database-trends/"
description: "Database vendors need to become more active in the cloud-native community — particularly to counter the scaling issues related to Kubernetes and stateful applications."
date: 2023-04-26
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 26 April 2023 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/d8679fcc176b1a75e84985ac1eb5d5b6cda68b93-772x550.webp)

**Database vendors need to become more active in the cloud-native community — particularly to counter the scaling issues related to Kubernetes and stateful applications.**

Containerization and [Kubernetes](/enterprise/redis-enterprise-on-kubernetes/) continue to revolutionize the development and deployment of cloud-native applications, largely because these technologies provide enhanced scalability, portability, and flexibility. But integrating databases into these environments raises a new set of challenges.

I’d like to say that those challenges are being overcome. But, after attending last week’s[ KubeCon + CloudNativeCon Europe 2023](https://events.linuxfoundation.org/kubecon-cloudnativecon-europe/) in Amsterdam, I have to conclude that we’re still a long way from fixing these problems.

## Combining stateless and stateful environments

The database/container issue all boils down to questions about [data persistence and storage](/blog/importance-of-database-persistence-and-backups/). Containers are ephemeral. They’re easily created, destroyed, and replaced. While this is beneficial for[ stateless applications](/learn/operate/orchestration/kubernetes-operator/), it poses a significant challenge for stateful applications that depend on databases, which, in turn, require persistent storage to maintain data integrity.

True, Kubernetes offers[ Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) (PV) and Persistent Volume Claims (PVC) to provide a [durable storage](/redis-enterprise/technology/durable-redis/) solution for stateful applications. PV and PVC allow databases to maintain their data even if the container running the database is replaced or destroyed.

But that’s not enough. This is not a solved problem.

“I think it’s one of the most important problems to solve right now,” said Petter Sveum, Veritas senior distinguished engineer, in a KubeCon panel discussion. “There are lots of different solutions available to the market, but database scale remains a real problem.”

“You have larger workloads being driven into Kubernetes with multi-terabyte volumes across multiple namespaces, perhaps even multiple sites,” Sveum pointed out. “Solving it requires a lot of attention to detail in traditional architecture. So why would it be any different than Kubernetes?”

Instead, Sveum has run into several teams that were really surprised. They go, ‘Oh, my 10-terabyte volume can’t be snapshotted within the time I expect!’ They don’t get that ‘It’s not fast, right? It takes minutes, hours.'”

Guillaume Savage de Saint Marc, a Cisco VP of engineering, agreed with Sveum’s assessment. “It’s awkward dealing with edge computing that needs the combined resources from stateful and serverless services in a cloud-native environment.”

Progress has been made with databases and [cloud-native](/redis-enterprise-cloud/overview/) computing. But the bottom line, said Xudong Ren, Huawei’s chief open source liaison officer, “There’s no mature solution.”

## Database companies need to be more involved in cloud-native computing

Everyone agreed that DBMS vendors need to do more with Kubernetes.

“We’re still relying on the legacy infrastructure component instead of investing in porting it to Kubernetes,” Sveum said. In his view, DBMSs remain in virtual machines (VMs) and servers and are called upon, as needed, from Kubernetes-orchestrated containers. We need more and better integration among DBMSs, containers, and Kubernetes, he asserted.

That isn’t stopping companies from running databases in containers. According to the [Data on Kubernetes](https://dok.community/) (DoK) community, many organizations are already running data services via[ Kubernetes operators](/blog/redis-enterprise-operator-for-kubernetes/) – software extensions that use custom resources to manage applications and their components. Ideally, an operator encapsulates a real-world operations team’s knowledge and expertise and codifies it into software.

Notice the ominous word “custom”? The top problem for using data on Kubernetes is a lack of integration with existing tools. As [a DoK report](https://dok.community/data-on-kubernetes-2022-report/) notes, “There remain few known good practices for running data on Kubernetes.”

Melisa Logan, DoK director and CEO of Constantia summed it up during a KubeCon DoK panel. “To handle Day-2 operations for data workloads on Kubernetes, organizations rely heavily on operators. But they present several challenges, including lack of integration with existing tools; lack of interoperability with the rest of their stack; varying degrees of quality; and lack of standardization.”

Yet most people use at least 20 operators, according to the[ 2022 Data on Kubernetes Report](https://dok.community/wp-content/uploads/2022/10/DoK_Report_2022.pdf). “For those evaluating their options, the challenge is further complicated by choice; the number of operators continues to grow, with[ Operator Hub](https://operatorhub.io/) currently listing over 270,” said Logan. “Without operator standards, how can end users possibly evaluate each one to know whether it meets their needs?” Clearly, much more work needs to be done.

## A dearth of qualified techies

Now, if only there were more people who were qualified in both Kubernetes and databases! This is a common refrain heard by Kubernetes users, not just from those who work with databases. There is not enough Kubernetes expertise to go around, never mind DBAs who know their way around Kubernetes.

As Sveum remarked, “We have a real shortage of people with an understanding of systems and infrastructure, how they actually are executed, and how they can leverage automation platforms as well as stacks like Kubernetes.”

We need people who can be the glue between the developer team that makes grandiose requests and then expect the platform to deliver.

## Oh, some database-related announcements

That’s not to say that Kubecon had no database news. There were a few announcements. For example, Cisco introduced a new open-source project,[ VMClarity](https://github.com/openclarity/vmclarity), for securing VMs in cloud-native environments. VMs, of course, host both containers and DBMSs.

Alternatively, some database news is narrowly implemented. For instance,[ Fermyon Technologies](https://www.fermyon.com/) added local stateful storage capacity with its[ Fermyon Cloud Key Value Store](https://www.fermyon.com/blog/introducing-fermyon-cloud-key-value-store), With this, users can persist non-relational data in a key/value that remains available for a serverless application via WebAssembly framework[ Spin](https://www.fermyon.com/spin). A developer can make what appear to be ordinary API calls to DBMSs such as Redis, PostgreSQL, or MySQL. Naturally, this only works in the Fermyon ecosystem, but it’s still an interesting step forward.

Taken all-in-all, the message I got from KubeCon is that more work – much more work – remains to be done with DBMSs and Kubernetes. Yes, you can do useful things today with stateful workloads and cloud-native computing. But it requires custom programming, which doesn’t scale well. Bridging this gap requires more effort both from the cloud-native and DBMS industries and communities.

Redis is at the forefront of database companies taking advantage of the container ecosystem, as we explain in [Running Redis on Kubernetes](/enterprise/redis-enterprise-on-kubernetes/).
