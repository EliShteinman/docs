---
title: "The Many Flavors of Multi-Cloud"
linkTitle: "The Many Flavors of Multi-Cloud"
url: "/blog/the-many-flavors-of-multi-cloud/"
description: "As Amazon, Microsoft, and Google fight it out in an epic struggle to dominate the cloud, a lot of companies and analysts are tossing around the term “multi-cloud.” But as Inigo Montoya immortally..."
date: 2020-03-05
blogCategories:
- "Company"
authors:
- "Fredric Paul"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Fredric Paul, Director of Content · Published 5 March 2020 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

As Amazon, Microsoft, and Google fight it out in an epic struggle to dominate the cloud, a lot of companies and analysts are tossing around the term “multi-cloud.” But as Inigo Montoya immortally states in the movie *Princess Bride*, “[You keep using that word. I do not think it means what you think it means](https://www.gutcheckit.com/blog/i-dont-think-that-word-means-what-you-think-it-means/#:~:text=Throughout%20The%20Princess%20Bride%2C%20the,You%20keep%20using%20that%20word.).”

Multi-cloud actually comes in a wide variety of flavors, intended to solve a wide variety of business and technical issues. And the most common multi-cloud implementations may not be the ones most people are thinking of when they hear or say “multi-cloud.”

This is much more than an academic discussion. As these proof points show, multi-cloud is a very big deal:

- A recent[ ZDNet headline](https://www.zdnet.com/article/multicloud-everything-you-need-to-know-about-the-biggest-trend-in-cloud-computing/) calls multi-cloud “the biggest trend in cloud computing.”
- In the [2019 RightScale State of the Cloud report](https://www.flexera.com/about-us/press-center/rightscale-2019-state-of-the-cloud-report-from-flexera-identifies-cloud-adoption-trends.html), 84% of respondents said they have a multi-cloud strategy and are running applications on an average of almost five different public and private clouds!
- In 2018, a [Forrester/Virtustream survey](https://www.virtustream.com/lp/forrester-multicloud-study) found that 86% of respondents labeled their company’s cloud strategy as ‘multi-cloud.’
- [According to Gartner](https://www.gartner.com/smarterwithgartner/why-organizations-choose-a-multicloud-strategy/), “most enterprise adopters of public cloud services use multiple providers.” And in a recent Gartner survey, “81% of respondents said they are working with two or more providers.”

With that kind of impact, it’s important to understand the wide variety of approaches and architectures that can fall under the “multi-cloud umbrella.” Let’s take a look at some of the common ways the term is applied.

## One workload, multiple clouds

The [most common usages of the term “multi-cloud”](https://en.wikipedia.org/wiki/Multicloud) often seem to focus on running a given workload on multiple different clouds—each providing parallel capabilities. That definitely happens, perhaps for load balancing or to avoid vendor lock-in or for increased resiliency in case one cloud suffers a massive outage. It may also be a way to host data closer to the user, either to improve performance or to comply with regulations about keeping data local, often referred to as [data sovereignty](https://whatis.techtarget.com/definition/data-sovereignty). (The global scale of the big three cloud providers, however, means that they each have multiple availability zones and are likely to be able to provide local coverage almost anywhere you need it.)

The issue, of course, is that if your application has to work in *every* cloud, it may not work optimally in *any* cloud. It may not be able to take advantage of an individual cloud’s competitive advantage—not to mention the additional IT overhead of maintaining the expertise to understand and manage multiple cloud infrastructures and vendor relationships.

Alternatively, a single application or service could run in multiple clouds because specific parts of the application need to take advantage of specific services from a specific cloud provider. You might run *most* of a particular application on Amazon Web Services, for example, but put some portion on Google Cloud (perhaps the AI processing) to take advantage of that service’s technology.

## Multiple workloads, each in its own cloud

![hybrid cloud strategy pictured as flavors of ice cream](/images/site-mirror/39d79df73f3a2a6241ff0c8eb554641509c65b6a-300x200.webp)

But while those approaches may be useful in some situations, they’re actually less-common implementations of a multi-cloud strategy. More common by far are companies where a multi-cloud strategy means running different workloads in different clouds. That can be on purpose, to let one application take advantage of specific proprietary services and features in a given cloud offering while other applications take advantage of other services from other providers.

This kind of multi-cloud can make it easier for a company to maintain ongoing relationships with multiple cloud providers, so it can move quickly in any direction at any time. In his post on [Why Organizations Choose a Multi-Cloud Strategy](https://www.gartner.com/smarterwithgartner/why-organizations-choose-a-multicloud-strategy/), [Laurence Goasduff](https://blogs.gartner.com/smarterwithgartner/author/lgoasduf/) quotes Gartner VP Analyst [Michael Warrilow](https://www.gartner.com/analyst/44368/Michael-Warrilow) explaining that the dominance of the mega-vendors in the public cloud services market is the main driver for enterprise buyers to choose multiple cloud providers: “Most organizations adopt a multi-cloud strategy out of a desire to avoid vendor lock-in or to take advantage of best-of-breed solutions. … We expect that most large organizations will continue to willfully pursue this approach.”

In many cases, however, running separate workloads in different clouds isn’t actually a strategy at all, but a relic of past technology and business decisions. For example, a company standardized on AWS might acquire another company that’s a dedicated Microsoft shop running a .NET environment, and thus deeply committed to Azure. Similarly, the ongoing prevalence of shadow IT practices often lead to multi-cloud environments, whether or not the CIO approves or even knows about it.

Multi-cloud isn’t “free,” of course. On the one hand, it’s sometimes possible to play cloud vendors off against each other to lower costs. But cloud vendors typically offer significant volume discounts, so splitting workloads across multiple clouds can lead to increased cloud costs. Dealing with multiple cloud vendors can also make it harder to keep track of and optimize your total cloud spending.

More significant for many companies are the costs and hassles of managing multiple providers and multiple technologies. Every cloud vendor has its own constantly evolving set of services, interfaces, APIs, and preferred ways of connecting, even for similar services. And that can add complexity to your applications, as well as make life more challenging for engineers who have to deal with multiple cloud providers and keep track of how to interact with each one.

Not surprisingly, the more dominant a cloud vendor, the less likely they are to help out with multi-cloud implementation. In fact, in Spiceworks’ *Public Cloud Trends in 2019 and Beyond* survey, 15% of enterprises say they need more help from cloud vendors in ‘Managing multiple cloud solutions’—while 22–23% of SMBs share that concern. Finally, that extra layer of management complexity only gets worse if multi-cloud adoption occurs on an *ad hoc* basis instead of as part of a carefully planned strategy.

## Multi-cloud, microservices, and containers

Fortunately, there are ways to make multi-cloud environments easier to work with. You can’t talk about multi-cloud in 2020 without considering the [growing impact of microservices](/solutions/microservices/) architectures and containers. Because containers package and isolate apps with their runtime environment, the rise of containers (Docker) and container orchestration (Kubernetes) helps solve a number of portability issues and accelerates application deployment to make it easier to move containerized apps among different clouds while retaining full functionality. The accelerating trend away from monolithic applications toward microservices—which breaks down applications into a collection of smaller, independent components—also helps make applications easier to deploy in multi-cloud environments.

## What about the hybrid cloud?

![private cloud vs public cloud. hybrid cloud strategy ](/images/site-mirror/2a4ece820548b48333d3c7367ba18a77e923febb-300x192.webp)

You may have noticed something missing from this multi-cloud discussion so far: What about the hybrid cloud? The idea behind the hybrid cloud is combination of at least one public cloud with at least one private cloud and/or an on-premises data center. I left hybrid cloud for the end of this post because the cloud community can’t quite seem to agree on exactly how the two concepts fit together.

[Many observers](https://searchcloudcomputing.techtarget.com/definition/multi-cloud-strategy) say the two strategies are related but different. In the [blog post mentioned above](https://www.gartner.com/smarterwithgartner/why-organizations-choose-a-multicloud-strategy/), Gartner describes multi-cloud as a *subset* of hybrid cloud. And still others consider hybrid cloud just another flavor of a multi-cloud strategy. However you fit it in, even as the public cloud continues its meteoric rise, the long shelf life and huge sunk costs in legacy on-premises infrastructures means that hybrid cloud architectures will always have a place linking the two, especially in highly regulated industries like finance and healthcare.

## Which flavor of multi-cloud tastes best?

Multi-cloud strategies continue to gain momentum in the enterprise, but it’s hardly a one-dimensional concept. If you’re fixated on a single kind multi-cloud, you may be missing the point. There are almost as many flavors of multi-cloud as there are companies and use cases.

In fact, as cloud vendors work to differentiate themselves by optimizing for particular situations, services, and types of customers, multi-cloud approaches are expected to become even more widespread and complex—we’re likely to see even more flavors of multi-cloud. The issue will increasingly become deciding on what cloud features you really need, and then choosing the fastest, simplest, least expensive, most resilient, most secure cloud—or combination of clouds—to meet your requirements.

*Whatever flavor of multi-cloud you choose, as a cloud-agnostic database Redis Enterprise offers the best Redis experience for all types of multi-cloud and hybrid cloud deployments. *[***Try it now free in the cloud!***](/redis-enterprise-cloud/)
