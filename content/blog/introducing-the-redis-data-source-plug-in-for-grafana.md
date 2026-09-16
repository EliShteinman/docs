---
title: "Introducing the Redis Data Source Plug-in for Grafana"
linkTitle: "Introducing the Redis Data Source Plug-in for Grafana"
url: "/blog/introducing-the-redis-data-source-plug-in-for-grafana/"
description: "Grafana is a well-known and widely used open source application monitoring tool. And now, thanks to the new Redis Data Source for Grafana plug-in, it works with Redis!"
date: 2020-08-25
blogCategories:
- "Tech"
authors:
- "Alexey Smolyanyy"
- "Mikhail Volkov"
lastmod: 2025-07-03
hidden: true
mirrored: true
---

*By Alexey Smolyanyy, Mikhail Volkov · Published 25 August 2020 · updated 3 July 2025*

![Blog tile image](/images/site-mirror/896454453542a9dcdfa7f82591f33e5384ba7919-1849x946.webp)

Grafana is a well-known and widely used open source application monitoring tool. And now, thanks to the new [Redis D](https://grafana.com/grafana/plugins/redis-datasource)[ata Source for Grafana ](https://grafana.com/grafana/plugins/redis-datasource)plug-in, it works with Redis!

With this new capability, DevOps practitioners and database admins can use a tool they are already familiar with to easily create dashboards to monitor their Redis databases and application data. The new [Grafana Redis Data Source ](https://grafana.com/grafana/plugins/redis-datasource)plug-in allows you to visualize [RedisTimeSeries data](/blog/unlocking-timeseries-data-redis/) and core Redis data types like Strings, Hashes, Sets, and more. Also, it can parse and display the output of Redis admin commands, such as SLOWLOG GET, INFO, and CLIENT LIST.

![Redis](/images/site-mirror/480aa4e91bdc402dd129ea126fe87484b93d6e8c-1024x524.webp)

Don’t miss the other blogs in this series: [**How to Use the New Redis Data Source for Grafana Plug-in**](/blog/how-to-use-the-new-redis-data-source-for-grafana-plug-in/) and [**3 Real-Life Apps Built with Redis Data Source for Grafana**](/blog/3-real-life-apps-built-with-redis-data-source-for-grafana/)

## Getting started with the Redis Data Source for Grafana

The new Redis Data Source for Grafana can connect to any Redis database—including open source Redis, Redis Enterprise, Redis Enterprise Cloud—and works with Grafana 7.0 and later. If you already have Grafana 7.0, you can install the Data Source plug-in with this grafana-cli command:

grafana-cli plugins install redis-datasource

If you don’t have Grafana installed, or just want to try the new data source, you can easily get started with Grafana in a Docker container:

docker run -d -p 3000:3000 --name=grafana -e "GF_INSTALL_PLUGINS=redis-datasource" grafana/grafana

Setting up Redis Data Source for Grafana is just as easy as working with any other Grafana data source. There are additional configuration options available, besides the server address and port, including database password and Transport Layer Security ([TLS](https://en.wikipedia.org/wiki/Transport_Layer_Security)) connection.

![](/images/site-mirror/bb1a51e98051d07f788666589fe2992e4ba10e5f-728x933.webp)

*Redis Data Source for Grafana configuration options.*

After you complete the initial configuration, you can start to create panels displaying Redis data! The Redis Data Source plug-in supports three different command types: Redis commands, RedisTimeSeries commands, and universal inputs.

![](/images/site-mirror/d094fe3c634d6785890154e52a8271f80edb4527-500x338.webp)

*The Redis Data Source for Grafana has a drop-down list to choose command type.*

1.** Redis commands** comprise a number of predefined commands to retrieve core Redis data types, such as Hashes, Sets, Strings, Streams, etc. The command’s output is pre-formatted for easy use in the Grafana interface. This mode also allows you to execute Redis admin commands: SLOWLOG GET, INFO, CLIENT LIST. Their output comes in newly introduced data frames, so you can apply [Grafana transformations](https://grafana.com/docs/grafana/latest/panels/transformations/) to modify the standard output.

![Redis](/images/site-mirror/744916b4bb2d8958034146ef57d8b10a2eda8721-800x472.webp)

2.** RedisTimeSeries commands** offer an interface to let you work with the [RedisTimeSeries](http://redistimeseries.io/) module. Currently, it supports two commands: TS.RANGE and TS.MRANGE, which let you query a range from one or more time series. The example below shows the number of downloads of the Redis Data Source from the Grafana repository.

![Redis](/images/site-mirror/f21c7481c0c54d40fe1d3eb147334ec528a9b4d5-1024x530.webp)

3.** Universal input** allows you to use other commands, not supported by the first two modes. Please keep in mind that:

- Universal input does not support all Redis commands.
- The output of these commands is not preformatted for Grafana, so some Grafana features may not work correctly.

## Real-time monitoring with the INFO command

To get started, install the [Redis Monitoring Dashboard](https://grafana.com/grafana/dashboards/12776), built for the new Grafana Data Source, and play with it.

The monitoring dashboard uses various sections of the INFO command with the relevant Grafana transformation. Additionally, it has a SLOWLOG panel, so you can quickly identify your slowest queries (which can impact the performance of your Redis database), and a CLIENT LIST panel displaying the information about client connections.

![Redis](/images/site-mirror/bb38f8d8cda07c155e8daf19ad9ce8c023d05192-1019x505.webp)

There are endless possibilities to use the new Redis Data Source Plug-in for Grafana; we plan to share more example dashboards, including a fun application for weather geeks, in the coming weeks. So please stay tuned!
