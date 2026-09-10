---
title: "How to add Redis as a datasource in Grafana and build customize dashboards for Analytics"
linkTitle: "How to add Redis as a datasource in Grafana and build customize dashboards for Analytics"
url: "/tutorials/operate/observability/redisdatasource/"
description: "The Redis Data Source for Grafana is a plug-in that allows users to connect to the Redis database and build dashboards in Grafana to easily monitor Redis and application data. It provides an out-..."
group: "For operators"
aliases:
- "/tutorials/explore/redisdatasource/"
- "/tutorials/operate-observability-redisdatasource/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> Install the Redis Data Source plug-in for Grafana, point it at your Redis instance, and import the predefined dashboard to start visualizing Redis metrics. You can also create custom panels to monitor the specific data points that matter to your application.

The Redis Data Source for Grafana is a plug-in that allows users to connect to the Redis database and build dashboards in Grafana to easily monitor Redis and application data. It provides an out-of-the-box predefined dashboard, but also lets you build customized dashboards tuned to your specific needs.

## What you'll learn

- How to install Grafana and the Redis Data Source plug-in using Homebrew, Docker, or Docker Compose
- How to connect Redis as a Grafana datasource and configure connection settings
- How to import the predefined Redis dashboard for instant data visualization
- What Redis commands are supported by the Grafana Redis connector
- How to build custom analytics dashboards with Redis data in Grafana

## Prerequisites

- A running Redis instance (local, self-hosted, or [Redis Cloud](https://redis.io/cloud/))
- One of the following installed on your system:
    - [Homebrew](https://brew.sh/) (macOS/Linux)
    - [Docker](https://docs.docker.com/get-docker/) (v18.03+ on Windows/Mac)
    - [Docker Compose](https://docs.docker.com/compose/install/)
- Basic familiarity with Grafana concepts (datasources, dashboards, panels)

![Grafana dashboard displaying Redis data visualization with key metrics and custom panels](/images/site-mirror/61edb69e8e42ca60adaa8faf80fd87eedb0f8c1c-1047x486.webp)

## What features does the Redis Grafana datasource support?

- Grafana 7.1 and later with a new plug-in platform supported.
- Data Source can connect to any Redis database. No special configuration is required.
- Redis Cluster and Sentinel supported since version 1.2.
- Data Source supports:
- [Redis Time Series](https://redis.io/docs/latest/develop/data-types/timeseries/): `TS.GET, TS.INFO, TS.MRANGE, TS.QUERYINDEX, TS.RANGE`
- [Search](https://redis.io/docs/latest/develop/ai/search-and-query/): `FT.INFO`

## How do you install the Redis Grafana datasource with Homebrew?

### Step 1. Install Grafana

```bash
 brew install grafana
```

### Step 2. Install the Redis datasource plug-in

Homebrew downloads and untars the files into /usr/local/Cellar/grafana/version.

### Step 3. Start the Grafana service

```bash
 brew services start grafana
```

### Step 4. How do you access the Grafana dashboard?

Open `https://IP:3000` to access grafana. The default username/password is admin/admin.

![Grafana login screen and initial dashboard overview after first launch](/images/site-mirror/31690e78fc9569aa4312693839c60b8ccb313542-1047x1082.webp)

### Step 5. Open the Configuration menu

![Clicking the Configuration gear icon in the Grafana sidebar navigation](/images/site-mirror/fbff19564b2f4dabf574a3eb122da827ce1f09c9-1047x522.webp)

### Step 6. Add Redis as a data source

![Adding a new data source from the Grafana Configuration page](/images/site-mirror/79dd8ef8fd1dd28fa68932553c93d28fb21f0f7c-1047x654.webp)

### Step 7. Select "Redis" as the data source type

![Selecting the Redis data source type from the list of available Grafana datasources](/images/site-mirror/a62200520235cd60e0a7ff192ede90edecdb421d-1047x496.webp)

### Step 8. How do you configure the Redis connection?

Add the Redis database name, endpoint URL, and password. This assumes you already have a Redis server and database up and running in your infrastructure. You can also use [Redis Cloud](https://redis.io/cloud/) as shown in the example below.

![Configuring Redis data source connection settings including endpoint URL, database name, and password](/images/site-mirror/3d1bfdc9714b5f3dd7a33e75cc11a0a07ef1ea25-1047x1187.webp)

### Step 9. Import the predefined Redis dashboard

![Importing the pre-built Redis analytics dashboard from the data source settings page](/images/site-mirror/b3f88303108e1fa6153fbae0d89f17b6fb0fc4e0-1047x432.webp)

### Step 10. View the Redis datasource dashboard

![The imported Redis data source dashboard showing real-time metrics and data visualization panels](/images/site-mirror/11aba09d827575383dac0c59643a1f45a3a2fa62-1047x483.webp)

### What Redis commands does the Grafana datasource support?

Data Source supports various Redis commands using custom components and provides a unified interface to query any command.

![Grafana query editor showing the list of supported Redis commands for building dashboard panels](/images/site-mirror/ab5206ce72c761bf2312cba045bc70e8c5f6c770-1047x360.webp)

[Embedded Content](https://youtu.be/LquDQyEncLE)

### Further references for Homebrew

- [Introducing the Redis Data Source Plug-in for Grafana](https://redis.io/blog/introducing-the-redis-data-source-plug-in-for-grafana/)
- [How to Use the New Redis Data Source for Grafana Plug-in](https://redis.io/blog/how-to-use-the-new-redis-data-source-for-grafana-plug-in/)
- [3 Real-Life Apps Built with Redis Data Source for Grafana](https://redis.io/blog/3-real-life-apps-built-with-redis-data-source-for-grafana/)
- [How to Manage Real-Time IoT Sensor Data in Redis](https://redis.io/blog/how-to-manage-real-time-iot-sensor-data-in-redis/)
- [Real-time observability with Redis and Grafana](https://grafana.com/go/observabilitycon/real-time-observability-with-redis-and-grafana/)

## How do you set up the Redis Grafana datasource with Docker?

You can install and run Grafana using the official Docker image.

### Step 1. Install Docker

The first step is to install Docker for your operating system. Run the `docker version` command in a terminal window to make sure that Docker is installed correctly.

> **NOTE**
>
> On Windows and Mac, install Docker version 18.03 or higher. You can run docker version to find out your Docker version.

### Step 2. How do you run Grafana with the Redis datasource in Docker?

Specify the plugins you want installed to Docker as a comma-separated list in the `GF_INSTALL_PLUGINS` environment. This sends each plugin name to `grafana-cli plugins install ${plugin}` and installs them when Grafana starts. In our case, we will be using redis-datasource.

```bash
 docker run -d -p 3000:3000 --name=grafana -e "GF_INSTALL_PLUGINS=redis-datasource" grafana/grafana
```

### Step 3. Access the Grafana dashboard

Open `https://IP:3000` to access Grafana. The default username/password is admin/admin.

![Grafana login screen and initial dashboard overview when running in Docker](/images/site-mirror/a53a6fde34f9444dd4fc9e35995975873a0e122f-1262x1304.webp)

### Step 4. Open the Configuration menu

![Clicking the Configuration gear icon in the Grafana sidebar when using Docker](/images/site-mirror/628fb82e39bd12c6b117bc3166fccb0653715bda-1578x786.webp)

### Step 5. Add Redis as a data source

![Adding a new data source from the Grafana Configuration page in a Docker deployment](/images/site-mirror/c66c7489c7326e0a52e53780b3a111fca5d6619a-1562x976.webp)

### Step 6. Select "Redis" as the data source type

![Selecting the Redis data source type from the available Grafana datasources list in Docker](/images/site-mirror/430d70ebfd230a1ea3deeafd04d14c25d04f0b3b-1554x736.webp)

### Step 7. How do you configure the Redis connection in Docker?

Add the Redis database name, endpoint URL, and password. This assumes you already have a Redis server up and running in your infrastructure. You can also use [Redis Cloud](https://redis.io/cloud/) as demonstrated below.

![Configuring Redis data source connection settings including endpoint, database, and password in Docker](/images/site-mirror/88a02f68e5600f764e72954b84111fd5c6bb1bfd-1324x1500.webp)

### Step 8. Import the predefined Redis dashboard

![Importing the pre-built Redis analytics dashboard in a Docker-based Grafana deployment](/images/site-mirror/f184cd8156554fc0690f845c6d8023026e99986b-1562x644.webp)

### Step 9. View the Redis datasource dashboard

![The imported Redis data source dashboard displaying real-time metrics in Docker](/images/site-mirror/b6622da61e140c0dc23823fc88770ac79c7b6560-1570x724.webp)

### What Redis commands does the Docker datasource support?

Data Source supports various Redis commands using custom components and provides a unified interface to query any command.

![Grafana query editor showing supported Redis commands for custom panel creation in Docker](/images/site-mirror/84c8becaca1d963451f17931424a2b2b565d363c-1316x452.webp)

[Embedded Content](https://youtu.be/LquDQyEncLE)

### Further references for Docker

- [Introducing the Redis Data Source plug-in for Grafana](https://redis.io/blog/introducing-the-redis-data-source-plug-in-for-grafana/)
- [How to use the New Redis Data Source for Grafana plug-in](https://redis.io/blog/how-to-use-the-new-redis-data-source-for-grafana-plug-in/)
- [3 real-life apps built with Redis Data Source for Grafana](https://redis.io/blog/3-real-life-apps-built-with-redis-data-source-for-grafana/)
- [How to manage real-time IoT Sensor Data in Redis](https://redis.io/blog/how-to-manage-real-time-iot-sensor-data-in-redis/)
- [Real-time observability with Redis and Grafana](https://grafana.com/go/observabilitycon/real-time-observability-with-redis-and-grafana/)

## How do you set up the Redis Grafana datasource with Docker Compose?

Assuming that Docker Compose is already installed on your system, follow these steps:

### Step 1. Clone the repository

```bash
 git clone https://github.com/RedisGrafana/grafana-redis-datasource
 cd grafana-redis-datasource
```

### Step 2. Start the services with Docker Compose

The project provides a `docker-compose.yml` file that starts Redis with all modules and Grafana.

```bash
 docker-compose up -d
```

### Step 3. Access the Grafana dashboard

![Grafana login screen and initial dashboard overview when using Docker Compose](/images/site-mirror/a53a6fde34f9444dd4fc9e35995975873a0e122f-1262x1304.webp)

### Step 4. Open the Configuration menu

![Clicking the Configuration gear icon in the Grafana sidebar with Docker Compose](/images/site-mirror/628fb82e39bd12c6b117bc3166fccb0653715bda-1578x786.webp)

### Step 5. Add Redis as a data source

![Adding a new data source from the Grafana Configuration page in a Docker Compose deployment](/images/site-mirror/c66c7489c7326e0a52e53780b3a111fca5d6619a-1562x976.webp)

### Step 6. Select "Redis" as the data source type

![Selecting the Redis data source type from the available Grafana datasources in Docker Compose](/images/site-mirror/430d70ebfd230a1ea3deeafd04d14c25d04f0b3b-1554x736.webp)

### Step 7. How do you configure the Redis connection in Docker Compose?

Add the Redis database name, endpoint URL, and password. This assumes you already have a Redis server up and running in your infrastructure. You can also use [Redis Cloud](https://redis.io/cloud/) as shown below:

![Configuring Redis data source connection settings including endpoint, database, and password in Docker Compose](/images/site-mirror/88a02f68e5600f764e72954b84111fd5c6bb1bfd-1324x1500.webp)

### Step 8. Import the predefined Redis dashboard

![Importing the pre-built Redis analytics dashboard in a Docker Compose Grafana deployment](/images/site-mirror/f184cd8156554fc0690f845c6d8023026e99986b-1562x644.webp)

### Step 9. View the Redis datasource dashboard

![The imported Redis data source dashboard displaying real-time metrics in Docker Compose](/images/site-mirror/b6622da61e140c0dc23823fc88770ac79c7b6560-1570x724.webp)

### What Redis commands does the Docker Compose datasource support?

Data Source supports various Redis commands using custom components and provides a unified interface to query any command.

![Grafana query editor showing supported Redis commands for custom panel creation in Docker Compose](/images/site-mirror/84c8becaca1d963451f17931424a2b2b565d363c-1316x452.webp)

[Embedded Content](https://youtu.be/LquDQyEncLE)

### Further references for Docker Compose

- [Introducing the Redis Data Source Plug-in for Grafana](https://redis.io/blog/introducing-the-redis-data-source-plug-in-for-grafana/)
- [How to Use the New Redis Data Source for Grafana Plug-in](https://redis.io/blog/how-to-use-the-new-redis-data-source-for-grafana-plug-in/)
- [3 Real-Life Apps Built with Redis Data Source for Grafana](https://redis.io/blog/3-real-life-apps-built-with-redis-data-source-for-grafana/)
- [How to Manage Real-Time IoT Sensor Data in Redis](https://redis.io/blog/how-to-manage-real-time-iot-sensor-data-in-redis/)
- [Real-time observability with Redis and Grafana](https://grafana.com/go/observabilitycon/real-time-observability-with-redis-and-grafana/)

## Next steps

- [Monitor Redis Software with Prometheus and Grafana](/tutorials/operate/observability/redis-software-prometheus-and-grafana/) - Set up full-stack Redis observability using Prometheus as a metrics collector alongside Grafana dashboards.
- [Monitor Redis with Datadog](/tutorials/operate/observability/datadog/) - Integrate Redis monitoring into Datadog to track latency, memory usage, and cache hit rate.
- [Redis Time Series documentation](https://redis.io/docs/latest/develop/data-types/timeseries/) - Learn more about the time series data type that the Grafana Redis datasource can query.
