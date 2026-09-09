---
title: "Why Should You Care About Kubernetes?"
linkTitle: "Why Should You Care About Kubernetes?"
url: "/blog/why-should-you-care-about-kubernetes-k8s/"
description: "Is your development team working with microservices architectures? Or are you still trying to wrap your mind around how to get started? Or maybe you’re already at the disillusionment stage where..."
date: 2020-04-14
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 14 April 2020 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

Is your development team working with microservices architectures? Or are you still trying to wrap your mind around how to get started? Or maybe you’re already at the disillusionment stage where you’re back to writing monolithic applications, [like Kelsey Hightower predicted](https://twitter.com/kelseyhightower/status/940259898331238402?s=20)?

Regardless of which stage you’re currently in, you most certainly know that microservices require the use of an orchestration platform like Kubernetes (also called K8s). But the real question is whether this is also true in the opposite direction: can Kubernetes be useful in situations that don’t employ a microservices architecture?

Adopting Kubernetes is not a lighthearted decision, and it’s reasonable to want to avoid the extra complexity, especially if it turns out to be not a good long-term investment. Still, I’d like to make the argument that gaining some K8s know-how will still prove useful in the eventuality that microservices, and even containers, fall out of fashion.

## Why orchestration platforms?

Kubernetes is made up of many different tools, most of which are optional. At its core, K8s is a tool that keeps a cluster of services up and running, allowing you to ask for modifications to the cluster by editing one or more configuration files that concretely define what “up and running” means.

Before Kubernetes, we relied on a mix of process monitoring tools and ad-hoc automation tools to keep services up in our systems. Then cloud providers started offering simplified ways of deploying services, like Google Cloud’s [AppEngine](https://cloud.google.com/appengine), Amazon Web Services’ [BeanStalk](https://aws.amazon.com/elasticbeanstalk/), and Microsoft Azure’s [App Service](https://azure.microsoft.com/en-us/services/app-service/). All these vendor-specific systems used to have significant limitations compared to what is possible nowadays. I still remember my first AppEngine instance back in 2013, where the only languages supported were Python and Go, and the only database available was Google Datastore.

In other words, even if you’re not doing microservices, having Kubernetes at your disposal is a good way to maintain your clusters without having to rely on the services your cloud provider offers. For example, it’s trivial to spawn a small Redis instance alongside your containers by [applying the K8s sidecar pattern](https://thenewstack.io/tutorial-apply-the-sidecar-pattern-to-deploy-redis-in-kubernetes/).

## Why stateless applications?

Orchestration tools like Kubernetes have also proven extremely useful for handling scaling requirements. The recent Covid-19 pandemic that forced people to stay at home caused huge traffic spikes for many popular online services, yet as of mid-April, no major outages have been reported. This is the result of amazing engineering on the part of the online service providers who have been able to keep their systems linearly scalable.

To keep a system linearly scalable, you need to ensure that important services can be scaled horizontally (i.e. you can spawn multiple instances at the same time). One common prerequisite for horizontal scalability is statelessness. A service that keeps state in memory requires special operational care that is often not worth the effort when the state could be offloaded to a dedicated database system. Distributed caching and sessions are a good example of this, a topic which I [recently discussed at NDC London](https://youtu.be/WqibJHxQ5wU).

In other words, modern applications still need a high degree of automation when it comes to dealing with failures and scalability, and Kubernetes is a very valid way of achieving that, regardless of the architectural choices made during development.

## Do you need K8s if containers go out of fashion?

You might have expected this point to be clickbait designed to grab your attention, but I’m actually serious. Containers solve two problems for which new technologies may be about to provide arguably better solutions.

**Application portability**

The first problem solved by containers is application portability. Moving an application around without containers is not fun, as any DevOps professional can tell you. The main problem is that applications often have a lot of dependencies whose deployment details differ for each operating system (even if we’re just talking about different distributions of Linux!). For example, even a simple Django application will require you to install Python, a few Python packages, and any system dependency those might have. Bundling the application in a container lets you ferry around a binary file that contains everything—sidestepping a lot of problems.

Thankfully, not all languages require convoluted steps like Python, Ruby, or JavaScript occasionally do. If you write an application in Go or Rust, for example, you will produce a single binary that can even be compiled to be completely static (i.e. without any form of runtime dependency). Once an application becomes a single binary, wrapping it in a container does little more than add an extra layer of complexity.

**Resource management**

The second problem solved by containers is limiting an application’s access to resources. Without containers it’s more difficult, but still possible, to limit the amount of DRAM that an application can consume, or restrict access to a specific directory. Containers make it easy to specify these restrictions simply as configuration options.

One new technology trying to address the same issue is [WebAssembly](https://webassembly.org/), a new type of virtual machine with security as a primary goal. A WebAssembly application will need to explicitly ask permission to make use of memory or any other resource. WebAssembly support is being rolled out in major web browsers, but it’s not limited to the web. You can run WebAssembly applications without a browser and open source developers have been experimenting with the idea of writing an entire OS kernel with support for WebAssembly. To complete the picture, it’s possible to create WebAssembly executables from many programming languages, including Go and Rust.

**Kubernetes without containers?**

Yes, that’s a real possibility. In a world where most applications compile down to a single binary with proper attention to security already baked-in, containers could become a vestigial abstraction layer with no further use.

That said, you will still need orchestration, and I can see Kubernetes’ continued relevance. But let’s assume that a new orchestration technology takes over. Would investing in K8s then be a waste? In my opinion, if done the right way, it won’t.

Kubernetes has a few concepts that are universally useful. Let me give you some examples:

- [Pods](https://kubernetes.io/docs/concepts/workloads/pods/pod/) are groups of containers that should be treated as a unit when orchestrating.
- [LoadBalancers](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) are a way of accepting external traffic and routing it to a horizontally scaled service. Load balancers existed way before K8s got its original name from *Star Trek* (it used to be called Borg internally at Google).
- [StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/) are a type of service that requires a stable way of identifying replicas and eventually connecting them to a storage volume.

All these concepts are fundamental building blocks for any distributed system. Now, not every Kubernetes-related technology is as obviously timeless as the ones mentioned above. For example, the final cost-benefit analysis of service meshes like [Istio](https://istio.io/) is left to posterity. I don’t necessarily recommend buying into every single new K8s-related trend, but the core ideas are solid and will probably outlive K8s itself.

## The value of Kubernetes

We often hear Kubernetes mentioned alongside microservices architectures, and to some people the two concepts are almost synonymous. In reality, though, K8s is a very useful piece of tooling for medium-to-big organizations that want to streamline service deployment and orchestration regardless of the architectural paradigms they use. Even if you’re skeptical about microservices, investing in K8s should prove a good choice in the long run because modern applications will always require good engineering practices (e.g. statelessness) to be efficiently orchestrated.

Of course, many people already have complete faith in Kubernetes, and for them [we have created an Operator](https://docs.redis.com/latest/platforms/kubernetes/) that supports OSS K8s and a few other flavors, with the goal of supporting all major Kubernetes offerings in the near future. For those who want to be more cautious, we can offer [Redis Enterprise as a managed service in your cloud of choice](/redis-enterprise-cloud/). Even if you remain skeptical of K8s, they’re worth checking out.
