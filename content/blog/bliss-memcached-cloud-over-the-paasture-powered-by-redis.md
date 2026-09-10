---
title: "Bliss: Memcached Cloud Over the PaaSture (Powered by Redis)"
linkTitle: "Bliss: Memcached Cloud Over the PaaSture (Powered by Redis)"
url: "/blog/bliss-memcached-cloud-over-the-paasture-powered-by-redis/"
description: "With winter storms on the attack around much of the world, it’s always nice to visualize some calming imagery, which today’s news inspired us to do. We are pleased to announce the graduation of our..."
date: 2013-12-18
blogCategories:
- "Company"
authors:
- "Itamar Haber"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Itamar Haber, Technology Evangelist · Published 18 December 2013 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/aab77b2dc6149b0e9f2168e2bf21cdda46adc03e-140x92.webp)

![](/images/site-mirror/43e53148f048bb5c807f52aea1abd3089d38fe21-635x181.webp)

With winter storms on the attack around much of the world, it’s always nice to visualize some calming imagery, which today’s news inspired us to do. We are pleased to announce the graduation of our Memcached Cloud add-ons from beta to general availability (GA) across major PaaS(ture) providers, including Heroku, AppFog and AppHarbor.

Memcached is an extremely popular [open source caching solution](/solutions/caching/) among large enterprises and startups for a variety of use cases, and many of these developers offload their infrastructure management to PaaS vendors so they can focus their R&D resources on developing great companies.

With this backdrop, our Memcached Cloud add-ons offer developers the best and easiest step up to fail-safe caching in the PaaS environment.

### Already using Memcached Cloud on Heroku, AppFog, or AppHarbor?
What’s Next?

During our PaaS beta period for the Memcached Cloud add-ons, we offered it with 1GB of free capacity. As part of our transition to the GA version, we’re now discontinuing the free version and providing several plan options with our usual pricing models. Previous users should visit their PaaS provider’s add-on pages for transition and pricing details:

Heroku: [https://addons.heroku.com/memcachedcloud](https://addons.heroku.com/memcachedcloud)
AppFog: [https://docs.appfog.com/add-ons/memcachedcloud](https://docs.appfog.com/add-ons/memcachedcloud)
AppHarbor: [https://appharbor.com/addons/memcachedcloud](https://appharbor.com/addons/memcachedcloud)

Upgrading is very simple, and will ensure that you continue to benefit from the only Memcache add-on that guarantees high availability and top performance for your app. Our technology combines persistent storage and in-memory replication, so your app can hum along smoothly without fear of losing data or performance. If you’re anything like us then your probably more comfortable around code, so here’s a short pseudo-code snippet we’ve prepared for you to run through and see what’s next:

```javascript
if not
  (
    yourapp.memcached is None
  ):
if yourapp.memcached.type == 'Memcached Cloud':
if yourapp.memcached.memcached.plan == 'PaaS 1GB Free Beta':
switchPlanToFreeOrUpgrade
  (
    '30', 'days'
  )
elif yourapp.isUsingPaaS():
considerSwitchingToAddOn() else:
# DYI Memcached or another add-on - maybe information will help
browser.open
  (
    '/memcached'
  )
browser.open
  (
    '/memcached/memcached-comparison'
  )
```

Memcached Cloud offers developers the best benefits of Garantia Data’s Redis Cloud – including true high availability (storage engine, replication, and auto-failover), infinite scalability, stable top performance, and zero management – without requiring you to change Memcached protocols. As a result, you can finally rely on your application’s cache to provide your users with consistent, uninterrupted, top-notch service and performance, regardless of failure events or scale challenges. If you’re already using our Memcached Cloud service then you are familiar with its rock-steady stability and unparalleled wealth of features.

Our production-proven functionality includes unique benefits such as scheduled and on-demand backups, data persistence, static endpoints and seamless scaling without any interruptions to the service. Because Memcached Cloud is tapping directly into raw Redis power, you can actually use Redis’ KEYS and MONITOR commands to see what’s stored in your Memcached, or even just scroll through the CSV backup file. If your Memcached-based application is deployed with a major PaaS provider, our competitively-priced add-on can be automatically connected with it and with each of our Memcached Cloud plans you cam to create multiple buckets under the same subscription for no extra charge.

Once you sign up, you’ll be able to start using Memcached Cloud immediately without any changes to your app, and you’ll gain the most advanced, high performance, and cost-effective enterprise-class hosted Memcached service. Of course, new users who don’t use PaaS can create a Memcached Cloud account [here](/?signup=1) as usual.
