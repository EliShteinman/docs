---
title: "3 Real-Life Apps Built with Redis Data Source for Grafana"
linkTitle: "3 Real-Life Apps Built with Redis Data Source for Grafana"
url: "/blog/3-real-life-apps-built-with-redis-data-source-for-grafana/"
description: "Update 3/29/21: https://coronavirusapi.com/ has recently closed free access to its data, making it only available for registered first-responders. While this unfortunately means the coronavirus..."
date: 2020-09-28
blogCategories:
- "Tech"
authors:
- "Alexey Smolyanyy"
- "Mikhail Volkov"
lastmod: 2025-07-03
hidden: true
---

*By Alexey Smolyanyy, Mikhail Volkov · Published 28 September 2020 · updated 3 July 2025*

![Blog tile image](/images/site-mirror/ffc921d20c84f35077d2649620f0f2fc4178dc7f-1591x658.webp)

***Update 3/29/21: ***[***https://coronavirusapi.com/***](https://coronavirusapi.com/)*** has recently closed free access to its data, making it only available for registered first-responders. While this unfortunately means the coronavirus case visualization project demo won’t work anymore, our hints will still be useful for many other implementations when you need to display RedisTimeSeries data on the Grafana Worldmap panel.***

In previous posts, we introduced and showed how to use the new [Redis Data Source for Grafana](https://grafana.com/grafana/plugins/redis-datasource):

- [Introducing the Redis Data Source Plug-in for Grafana](/blog/introducing-the-redis-data-source-plug-in-for-grafana/)
- [How to Use the New Redis Data Source for Grafana Plug-in](/blog/how-to-use-the-new-redis-data-source-for-grafana-plug-in/)

In this post, we want to explore some real-life examples designed to give you ideas about the many interesting datasets you can store in Redis and visualize in Grafana. We’ll cover three different applications:

1. Weather dashboard
1. Coronavirus cases visualization
1. Pop-up store demo

## 1. Weather dashboard

Do I really think that the world needs yet another weather dashboard? Yes, I do!

Sure, most of the time I’m not much of a weather geek. I often don’t really care what the weather is like. And even when I do, the best weather dashboard is usually just a window looking out of my house. But sometimes, perhaps when I find some spare time to go out to take some pictures or fly my drone, my inner weather geek awakens.

The big question, of course, is where should I go? There are a lot of interesting locations within a couple of hours drive from my house in New Jersey, and the weather can be very different from one to another. What I really want is a dashboard that shows the weather in a dozen locations on one screen, so I can compare conditions at a glance. Critically, I don’t just want to compare locations near each other.

![](/images/site-mirror/353a5113b69b32598547aa628a31be9e36777206-640x640.webp)

Just as important, I love working with numbers. I know that landscape photography works best when the amount of cloud cover is somewhere between 20% – 50%. For flying my drone, wind speeds below 10 mph are ideal, 10 – 20 mph is tough, and anything above 20 mph can be dangerous. So a cute weather icon like this doesn’t do me much good:

With that in mind, here is how I built a weather dashboard using Redis.

Fortunately, raw weather data is now widely available via a broad selection of weather APIs, many of them free (with some limitations). I chose to use[ OpenWeatherMap API](https://openweathermap.org/api/one-call-api), because its free plan gives me everything I need: a 48-hour hourly forecast, a 7-day daily forecast, and current conditions.

I wrote a simple [Python script](https://github.com/RedisTimeSeries/redis-weather) to pull the data from the API and put hourly/daily forecasts into the Redis database using the [RedisTimeSeries](https://oss.redis.com/redistimeseries/) module and current conditions into another set of time series for history.

My weather dashboard follows my two mandatory dashboard rules:

1. All the data should be displayed on one screen, no scrolling required.
1. A person should be able to understand the situation displayed on the dashboard as quickly as possible.

![Redis](/images/site-mirror/8b21ff4c71e98d47efe00e1fa4a50994479b9582-1024x424.webp)

The top section of the dashboard shows the current conditions for one location, which can be the primary or favorite or just selected from the list of available places (there is a Grafana template variable selection list in the top left corner of the dashboard). It also displays the periods of time good for the particular activity at that location. Grafana allows me to highlight low/high zones for temperature, dangerous zones for wind speed, display the degree of cloudiness, and mark periods of daytime and nighttime.

The bottom section group locations by activity, making it easy to compare them. The bigger the circle, the more hours are good for a certain activity in a certain location.

![Redis](/images/site-mirror/c4216e652a15c9e98442d4515a3cc3e8d7934edc-1024x401.webp)

## 2. Coronavirus cases visualization

I love traveling, but 2020 made millions of people stay home for months on end (I hope not forever!). Now, as many states gradually start to reopen, it’s very important to travel smart and understand the COVID-19 situation in both your origin and destination locations. That means paying attention not only to the current picture but also the longer-term trends.

This is what my [Grafana U.S. States Coronavirus Dashboard](https://github.com/RedisGrafana/redis-coronavirus-map) shows. It is based on the [Coronavirus API](https://coronavirusapi.com/) data, loaded into the [RedisTimeSeries](https://oss.redis.com/redistimeseries/) module.

![Redis](/images/site-mirror/bc2940ac9516fda57434bc0beac06edc6496e39e-923x540.webp)

Besides standard graph representation, data is also drawn on the map.[ The Redis Data Source plug-in](https://github.com/RedisTimeSeries/grafana-redis-datasource) is not officially supported by the [Grafana Worldmap panel](https://grafana.com/grafana/plugins/grafana-worldmap-panel), but you can make it work in two simple steps:

**Step 1: **Apply the transformation “Labels to fields” to the time-series output result:

![](/images/site-mirror/b31b2c04b8fb52fc0a72f292e228fa280fffbad7-845x373.webp)

**Step 2:** Change the map parameter “Location Data” to table mode and map the relevant fields:

![](/images/site-mirror/3bcad192fe81da552b20172430af4f83b9c15a3c-367x712.webp)

These two steps will allow you to stick the time-series value to the relevant point on the map, which is set by the “geohash” label of RedisTimeSeries. The label “state” is used to display the name of the location on the map.

## 3. Pop-up store demo

I am a big fan of [Redis Streams](https://redislabs.com/wp-content/uploads/2021/08/DS-Redis-Streams.pdf), a new data type introduced in Redis 5.0, and I was looking for a fast and simple solution to monitor queues for data processing. While working on the Redis Data Source, our team started to explore [RedisGears](/redis-enterprise/redis-gears/)—a dynamic framework that lets developers write and execute [functions](https://oss.redis.com/redisgears/functions.html) that implement data flows in Redis while abstracting away the data’s distribution and deployment—for another project and we decided to use them together for this data-pipeline demo for a pop-up store.

RedisGears supports several types of readers that operate on different types of input data. To watch streams messages, we used [StreamReader](https://oss.redis.com/redisgears/readers.html#streamreader) in the event mode. In this mode, the reader is executed in response to events generated by new messages added to the stream.

```javascript
# Add Time-Series
def tsAdd(x):
   xlen = execute('XLEN', x['key'])
   execute('TS.ADD', 'ts:len:'+x['key'], '*', xlen)
   execute('TS.ADD', 'ts:enqueue:' + x['key'], '*', x['value'])

# Stream Reader for any Queue
gb = GearsBuilder('StreamReader')
gb.countby(lambda x: x['key']).map(tsAdd)
gb.register(prefix='queue:*', duration=5000, batch=10000, trimStream=False)
```

StreamReader accepts multiple arguments that control how it is triggered. In our case, we want the reader to be triggered every 5 seconds or after it receives 10,000 messages. The last option, trimStream, specifies not to trim the stream after execution.

We used RedisTimeSeries to store the number of incoming messages and the queue-size samples. As explained in the [introductory blog post on the Redis Data Source Plug-in for Grafana,](/blog/introducing-the-redis-data-source-plug-in-for-grafana/) time series can be easily visualized in Grafana.

![](/images/site-mirror/47e824751e6315b9e0b2af86ff20c83630d5af50-1024x422.webp)

*The data-pipeline demo diagram for a pop-up store.*

To demonstrate how Redis Streams, RedisTimeSeries, RedisGears, and Redis Data Source can work together, we created the [Pop-up store demo](https://github.com/RedisTimeSeries/redis-pop-up-store) with a dynamic dashboard:

![Redis](/images/site-mirror/3f7a7abc107a70407633f3b1167260ca12e660f3-1200x516.webp)

This Grafana dashboard displays:

- **Product Available:** the value of product key, which decreases as orders complete
- **Customers Ordering, Orders Processing, and Orders Completed:** the length of queue:customers, queue:orders, and queue:complete streams
- **Customers Overflow: **the difference between customer-submitted orders and orders completed
- **Customers Ordering:** orders created in 5 seconds
- **Orders In Queue: **orders waiting to be processed
- **Completed Flow:** orders completed in 5 seconds

Please take a look at the [GitHub repository for this project](https://github.com/RedisTimeSeries/redis-pop-up-store) to see how we generated the load, the RedisGears scripts we used, and how to configure Redis Data Source to query RedisTimeSeries data using the [TS.RANGE](https://redis.io/docs/data-types/timeseries/quickstart/) command.

## Conclusion

These three real-life scenarios demonstrate ways to use Redis Data Source for Grafana with various Redis modules. We hope they inspire you to use this technology and build your own applications.

You’ll be in good company. Since the Redis Data Source plug-in was published in the [Grafana repository](https://grafana.com/grafana/plugins/redis-datasource) it has already been downloaded more than 10,000 times, included in [popular community plug-ins that can improve your Grafana dashboard](https://grafana.com/blog/2020/08/26/popular-community-plugins-that-can-improve-your-grafana-dashboards/?), added support for Redis cluster, Sentinel, Unix socket, and access control lists ([ACL](/blog/getting-started-redis-6-access-control-lists-acls)s):

![Redis](/images/site-mirror/3b77eecbad53057f5ef5914ceac070f91c597d9c-801x1024.webp)

But that’s not all. Stay tuned to the [Redis Tech blog](/blog/tech-blog/) to learn about an exciting project combining Grafana streaming capabilities with interactivity to take Grafana beyond observability with a redis-cli panel.
