---
title: "Safe and Informed: Try Out Our New Alerts & SSL Support"
linkTitle: "Safe and Informed: Try Out Our New Alerts & SSL Support"
url: "/blog/safe-and-informed-try-out-our-new-alerts-ssl-support/"
description: "Lately we’ve been busy establishing and expanding our service’s presence on the IBM SoftLayer Cloud and Google Compute Engine. But, that doesn’t mean that we’ve been neglecting our core service..."
date: 2014-03-04
blogCategories:
- "Company"
authors:
- "Itamar Haber"
lastmod: 2025-03-27
hidden: true
---

*By Itamar Haber, Technology Evangelist · Published 4 March 2014 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

![](/images/site-mirror/296920b212048191bf34680fcae5395c64f9858e-635x200.webp)

Lately we’ve been busy establishing and expanding our service’s presence on the IBM SoftLayer Cloud and [Google Compute Engine](/blog/the-search-for-redis-on-google-compute-engine-gce-is-over). But, that doesn’t mean that we’ve been neglecting our core service development. As a matter of fact, today, by popular demand, I am pleased to announce the public availability of two new features for our services across all clouds: Email Alerts and SSL support.

Our first addition, Email Alerts, allows you to get pertinent notifications regarding the usage and performance of your Redis resources. You can enable the new alerting mechanism for any resource from the service’s console. By default, emails alerts are turned off for your existing resources, but you can easily change the alert settings by editing any Redis Cloud instance or Memcached Cloud bucket and expanding the **Advanced Options** section.

![](/images/site-mirror/89b551b31704730698562b37bbd012fb974893a2-635x130.webp)

Each email alert trigger can be toggled on or off independently and have its threshold configured. You can set up the triggers to get email alerts for the following conditions:

- **Increase in latency**: Use our *“Latency is higher than”* trigger to receive an alert once your application’s requests latency is above a certain threshold. Latency is measured as the time between receiving a request and the reply being ready to be sent back. Normally, latency should be no more than 1 millisecond for simple commands.
- **Throughput changes:** The *“Throughput is lower than”* trigger is useful if you want to be alerted when your application’s traffic drops below a set threshold. Similarly, the *“Throughput is higher than”* alert will fire once traffic picks up and crosses the threshold. Depending on your app’s use case, changes in throughput may indicate developing issues, so you can use these alerts as an early warning signal.
- **Connections usage:** Several of our fixed-size Redis Cloud plans set a limit on the number of concurrent connections allowed per database. Once your allotted quota is exhausted, attempts to open new connections will be refused. Our *“Number of open connections exceeds”* email alert can be used to help monitor your app’s usage of its database’s connection resources and avoid ECONNREFUSED errors.
- **Memory usage:** You can monitor memory usage and be alerted once your datasets’ size reaches a certain percentage (e.g. 80%) of the subscription’s capacity. Depending on your data and databases’ configuration, running out of memory may result in data eviction and/or out of memory (OOM) errors. The *“Total size of datasets in the subscription has reached”* and *“Dataset size has reached”* alerts are available for fixed-size and pay-as-you-go subscriptions, respectively, to provide you a heads up before you run out of space.

In addition to all of these great notification tools, we’ve officially added support for SSL authentication and encryption after a successful private beta. Standard Redis and Memcached do not feature built-in security mechanisms other than password protection. This is an omission by design, because both technologies are primarily aimed for use near the application, inside a trusted and secure network. By putting security out of scope, these open-source projects can stay focused on their primary goals, without adding functionality that would eventually bloat them.

At Redis, however, we provide our services’ resources from public clouds, which of course requires more security. Our resources can be configured with Source IP and (AWS) Security Groups access control rules to restrict access to them. Password protection and access control rules are great means for authentication, but leave the communication channel unsecure. This could potentially expose your data to eavesdropping, man-in-the-middle attacks and other security threats.

SSL ensures that the communication channel between your application servers and your Redis resources is secure and strongly encrypted. Since SSL is not native to Redis or Memcached, your application will need to use a secure proxy such as [stunnel](http://stunnel.org) to connect to our resources using SSL. SSL-enabled plans cost twice as much as our Standard plans and are offered exclusively via our custom plans.

We are working on adding SSL support to popular Redis clients so that eventually the use of a secure proxy will be optional. Contact me at [itamar@redis.com](mailto:itamar@redis.com) or on Twitter at [@itamarhaber](https://twitter.com/@itamarhaber) to let me know if you want SSL support added to a specific client and if you want to help in developing one – you’ll get a 100MB SSL-enabled subscription, free of charge for a whole year!
