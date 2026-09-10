---
title: "Tracing Kubernetes Adoption, From Inception to the Cloud"
linkTitle: "Tracing Kubernetes Adoption, From Inception to the Cloud"
url: "/blog/kubernetes-adoption-inception-to-cloud/"
description: "Among the factors contributing to developers’ growing reliance on Kubernetes are its hybrid cloud capabilities, team-friendly portability, and cost-consciousness for cloud deployments."
date: 2022-12-14
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Redis   · Published 14 December 2022 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/f0674bebcd20ff95e4ce92d70d47853e75d89dc6-772x550.webp)

**Among the factors contributing to developers’ growing reliance on Kubernetes are its hybrid cloud capabilities, team-friendly portability, and cost-consciousness for cloud deployments.**

[Kubernetes](/enterprise/redis-enterprise-on-kubernetes/) has come a long way since 2014 when Google first introduced it as an open source answer to [Borg](https://kubernetes.io/blog/2015/04/borg-predecessor-to-kubernetes/), Google’s internal container orchestration solution.

![](/images/site-mirror/e5fc1d6fc507ac5ab6a41a94f22b43f6a9352ca0-601x192.webp)

Since then, the deployment system and containerized application tool has had many technical upgrades. After releasing Kubernetes v1.0 in 2015, it began supporting [OpenAPI](https://kubernetes.io/blog/2016/12/kubernetes-supports-openapi/) in December 2016, which enabled API providers to define their operations and opened the path for developers to automate their tools. By 2018, Kubernetes had become so mainstream that Google dedicated an entire [podcast](https://cloud.google.com/blog/products/gcp/introducing-kubernetes-podcast-from-google/) to it.

Flash forward to the present day. Kubernetes’ popularity skyrocketed in tandem with the adoption of [cloud-native services](/redis-enterprise-cloud/overview/). According to the recent [Splunk State of Kubernetes report](https://www.splunk.com/en_us/blog/learn/state-of-kubernetes.html#:~:text=more%20than%20300%25%20increase%20in%20container%20production%20usage%20in%20the%20past%205%20years.), there’s been a “300% increase in container production usage in the past five years,” with large organizations being the predominant driving force behind Kubernetes’ mainstream adoption.

According to the [Cloud Native Computing Foundation](https://www.cncf.io/wp-content/uploads/2020/12/CNCF_Survey_Report_2020.pdf) (CNCF) [2020 Annual Survey](https://www.cncf.io/wp-content/uploads/2020/12/CNCF_Survey_Report_2020.pdf), organizations using or evaluating Kubernetes ballooned from 78% in 2019 to 96% in 2022, making it the go-to platform for [*building*](https://www.youtube.com/@Redisinc/playlists?view=50&sort=dd&shelf_id=3/)[ platforms](https://www.youtube.com/@Redisinc/playlists?view=50&sort=dd&shelf_id=3/).

That’s not to say that Kubernetes was immediately accepted by the development community. For a while, container orchestration required a [technology choice among Kubernetes, Docker, and Mesosphere](https://www.hpe.com/us/en/insights/articles/the-basics-explaining-kubernetes-mesosphere-and-docker-swarm-1702.html). Eventually, Docker and Kubernetes made friends with one another, and developers are comfortable using both. Mesosphere, however, lost their attention.

Kubernetes has stayed open source, and one mark of its prevalence is the number of contributions to its codebase. There have been over [2.8 million contributions to Kubernetes](https://k8s.devstats.cncf.io/d/9/companies-table?orgId=1&var-period_name=Last%20decade&var-metric=contributions) made by companies.

Kubernetes, as we know it today, comes with many automations already baked in, making it easier for development teams to get started. It’s easy to tick off the advantages on your fingers: Everything is managed through code and is easily portable if running on cloud. Kubernetes’ flexibility makes [scaling applications](https://www.youtube.com/playlist?list=PL83Wfqi-zYZH5UtjOEsA5pC88sQkQVy-R/) a simple process. Containers are lean by design; they store only the must-have resources an application needs to run. That makes applications significantly faster and lighter and Kubernetes all the more appealing to developers.

## Kubernetes: a solid foothold in the cloud

With each passing year, cloud computing has continued to gain traction while on-prem Kubernetes deployments have taken a 3% hit year over year, according to VMware Tanzu’s [The State of Kubernetes 2022](https://hello-tanzu.vmware.com/state-of-kubernetes-2022/)report. Most Kubernetes deployments are in multicloud or hybrid clouds. “When we asked people about growth plans in the coming year,” the report states, “almost half (48%) expect the number of Kubernetes clusters they operate to grow by more than 50%; an additional 28% expect the number of [clusters](/redis-enterprise/technology/redis-enterprise-cluster-architecture/) to increase notably (20% to 50%).

Kubernetes’ growth is thanks in part to its continued investment in [software](/enterprise/) development and infrastructure efficiency. Development teams have come to rely on the flexibility that orchestrating from on-prem, single-cloud, hybrid cloud, or [multicloud](/redis-enterprise-cloud/multicloud/) provides. These container-based hybrid cloud and multicloud environments allow teams to handle massive workloads with minimal refactoring or replatforming.

![](/images/site-mirror/e5fc1d6fc507ac5ab6a41a94f22b43f6a9352ca0-601x192.webp)

This developer efficiency is particularly true when building [microservice-based applications](/solutions/microservices/). Since they’re comprised of different units, teams can more readily put their resources to the right tasks while working in one platform. That’s a considerably tougher request when working with a monolithic architecture. It’s a useful way of keeping too many proverbial cooks out of the proverbial kitchen, so to speak.

Kubernetes’ bread and butter are its automations. By taking highly repeatable commands and setting them to automate, teams can eliminate unnecessary headcounts and sidestep any time-consuming IT tinkering. When surveyed, 45% of registrants in VMware’s report indicated they rely on Kubernetes because of its product capabilities and roadmap.

## Kubernetes growth

The cloud infrastructure market grew 24% year over year in Q3 2022, according to [Synergy Research](https://www.srgresearch.com/articles/q3-cloud-spending-up-over-11-billion-from-2021-despite-major-headwinds-google-increases-its-market-share). With more large enterprises including containerized cloud deployments in their stack and looking to freely move their data from cloud to cloud with no lock-ins, the ability to work in a hybrid cloud environment is becoming mission-critical for most large organizations; that ongoing trend is reflected in the 41% of respondents that choose Kubernetes for this very reason, as per VMware’s report.

Most major cloud service platforms have a Kubernetes distribution tailored to their respective services, points out [a 2022 Evans Data Cloud Development Survey](https://evansdata.com/reports/viewRelease.php?reportID=27). Foremost, 37% of developers use dedicated Kubernetes-based cloud services, such as AWS’s Amazon EKS or Microsoft’s Azure Kubernetes Service. “These implementations of Kubernetes, with varying levels of service, use these companies’ internal cloud back-ends for container orchestration,” the report explains. In the Evans Data report, 32% of developers use a commercial Kubernetes distribution, and 28% own a managed “vanilla” Kubernetes.

The pandemic drove digital services and experiences into overdrive, which encouraged the already-in-progress transition to businesses moving services online. One result was that cloud deployments escalated – along with application load. Back in June 2018, [Kubernetes 1.11](https://kubernetes.io/blog/2018/06/27/kubernetes-1.11-release-announcement/) was released, which introduced IPVS-based in-cluster load balancing, an advancement that greatly increased application production scalability.

Load balancing is key, as it’s a hands-free means of maintaining infrastructure efficiency, which in turn, keeps cloud costs from skyrocketing. According to Cast.ai, companies spent an exorbitant [$16.2B in cloud waste](https://cast.ai/blog/the-cloud-waste-problem-how-to-stop-overprovisioning-resources/) in 2022. This overprovisioning is blood-letting dev teams of their available resources. Automations that save money, time, and manpower are the goal, though that has required teams to implement their own tools for [automatic failover](/redis-enterprise/technology/highly-available-redis/) through the commercial support of an [operator](/blog/redis-enterprise-operator-for-kubernetes/).

## Operators for Kubernetes

As mentioned before, the core of Kubernetes has many built-in automations, but thanks to the Kubernetes [operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/#operators-in-kubernetes), it’s possible to automate tasks beyond what’s in the Kubernetes software.

Kubernetes is great at keeping costs low by load-balancing cluster nodes in order to reach their ideal state. An operator goes a step further by adding an extra layer of orchestration, one that automatically steps in in the event of an automatic failover, monitors resources via a reconciliation loop, or even scales a cluster automatically.

And if you use Redis – or you are considering doing so – we make it even easier. [The Redis Enterprise Operator for Kubernetes](/blog/redis-enterprise-operator-for-kubernetes/) streamlines and automates the management of the Kubernetes layer. It’s the result of everything learned, millions of cluster deployments later.

[Click here to view video](https://www.youtube.com/embed/7UBlNsyHSQA)

For anyone running [Redis on Kubernetes](/enterprise/redis-enterprise-on-kubernetes/) and interested in comparing the Redis operator and Helm charts, read [An Introduction to the Helm Tool and Helm Charts](/blog/redis-enterprise-release-using-helm-charts/).
