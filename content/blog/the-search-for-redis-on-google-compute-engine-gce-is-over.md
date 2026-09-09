---
title: "The Search for Redis on Google Compute Engine (GCE) is Over!"
linkTitle: "The Search for Redis on Google Compute Engine (GCE) is Over!"
url: "/blog/the-search-for-redis-on-google-compute-engine-gce-is-over/"
description: "Update: the beta is over and we’re generally available on Goolge Compute Engine – all the details are at our pricing page."
date: 2014-02-12
blogCategories:
- "Company"
authors:
- "Itamar Haber"
lastmod: 2025-03-27
hidden: true
---

*By Itamar Haber, Technology Evangelist · Published 12 February 2014 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

![](/images/site-mirror/eae541727abfeac27a806d42c7337e2a59122193-635x200.webp)

**Update:** the beta is over and we’re generally available on Goolge Compute Engine – all the details are at our [pricing page](/pricing).

I am pleased to announce the immediate availability of Redis Cloud on Google Compute Engine (GCE). Even before GCE’s GA launch, a lot of developers had contacted us and asked whether we’ll offer our services there – this is our positive answer to that question. Naturally, we’re very excited to add this new and promising platform to our offerings. As is the case with every new cloud, we’ll be kicking it off with a beta.

The new Redis Cloud Google Compute Engine 1GB beta plan is available today for free to anyone with a Redis account.

**[Don’t have one yet? What are you waiting for? **[**Create your free 1GB Redis instace**](/?signup=1)** – minimum details, no credit card is required, no spam is sent – ever]**

You can find all the details on [our pricing page](/pricing) by selecting **GCE/us-central1** in the Cloud drop-down box and if you add the free beta subscription you’ll be able to have a go at your very own Google-flavored Redis Cloud instance in seconds.

Apropos having a go, you can connect to your new Redis Cloud instance on Google Compute Engine with an idiomatic Go foobar:

```javascript
package main
import (
    "fmt"
    "github.com/garyburd/redigo/redis"
)
func main() {
    c, err := redis.Dial("tcp", "pub-redis-6379.us-central.gce.garantiadata.com:6379")
    _, err = c.Do("AUTH", "123456")
    _, err = c.Do("SET", "foo", "bar")
    value, err := c.Do("GET", "foo")
    fmt.Printf("foo is %sn", value)
}


```

Our free beta will be available for one month and during this time we will work with users to get feedback and improve the offering. During that time, you’ll experience how easy it is to get started developing your Redis-based application built on Google Compute Engine.

Once the beta is over, we’ll publish our GCE plans’ pricing and provide plenty of time for you to switch your beta to a free or a paid subscription. You can subscribe to any or all of our beta plans simultaneously and switching from beta to regular subscription is instant and does not involve any downtime, configuration changes or data loss.

Questions? Ideas? Requests? Feel free to hit me at [itamar@redis.com](mailto:itamar@redis.com) or on Twitter at [@itamarhaber](https://twitter.com/@itamarhaber). Thanks in advance for trying out our new beta – I’m looking forward to hearing your feedback on the service.
