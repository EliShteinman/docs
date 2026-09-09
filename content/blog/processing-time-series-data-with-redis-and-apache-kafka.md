---
title: "Processing Time-Series Data with Redis and Apache Kafka"
linkTitle: "Processing Time-Series Data with Redis and Apache Kafka"
url: "/blog/processing-time-series-data-with-redis-and-apache-kafka/"
description: "RedisTimeSeries is a Redis module that brings native time-series data structure to Redis. Time-series solutions, which were earlier built on top of Sorted Sets (or Redis Streams), can benefit from..."
date: 2021-06-22
blogCategories:
- "How To and Tutorials"
- "Tech"
- "Tech Redis Modules"
- "Uncategorized"
authors:
- "Abhishek Gupta"
lastmod: 2025-03-27
hidden: true
---

*By Abhishek Gupta, Microsoft Senior Developer Advocate · Published 22 June 2021 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/3098118e032727396b8b279289e3f8ed3c55c4c0-772x520.webp)

[RedisTimeSeries](https://oss.redis.com/redistimeseries/) is a Redis module that brings native time-series data structure to Redis. Time-series solutions, which were earlier built on top of Sorted Sets (or Redis Streams), can benefit from RedisTimeSeries features such as high-volume inserts, low-latency reads, flexible query language, down-sampling, and much more!

Generally speaking, time-series data is (relatively) simple. Having said that, we need to factor in other characteristics as well:

- Data velocity: e.g. Think hundreds of metrics from thousands of devices per second
- Volume (Big data): Think data accumulation over months (even years)

Thus, databases such as RedisTimeSeries are just a part of the overall solution. You also need to think about how to **collect **(ingest), **process, **and **send **all your data to RedisTimeSeries. What you really need is a scalable data pipeline that can act as a buffer to decouple producers and consumers.

That’s where [Apache Kafka](https://kafka.apache.org/) comes in! In addition to the core broker, it has a rich ecosystem of components, including [Kafka Connect](https://kafka.apache.org/documentation/#connect) (which is a part of the solution architecture presented in this blog post), client libraries in multiple languages, [Kafka Streams](https://kafka.apache.org/documentation/streams/), Mirror Maker, etc.

![kafka map](/images/site-mirror/b06115e1474ef255696e2b60976d1e98450ce0cb-1024x369.webp)

This blog post provides a practical example of how to use RedisTimeSeries with [Apache Kafka](https://redis.io/compare/redis-enterprise-and-kafka/) for analyzing time-series data.

*The code is available in this GitHub repo https://github.com/abhirockzz/redis-timeseries-kafka*

Let’s start off by exploring the use case first. Please note that it has been kept simple for the purposes of the blog post and then further explained in the subsequent sections.

## Scenario: Device monitoring

Imagine there are many locations, each of them has multiple devices, and you’re tasked with the responsibility to monitor device metrics—for now we will consider temperature and pressure. These metrics will be stored in RedisTimeSeries (of course!) and use the following naming convention for keys—<metric name>:<location>:<device>. For example, temperature for device 1 in location 5 will be represented as temp:5:1. Each time-series data point will also have the following [Labels](https://redis.io/docs/data-types/timeseries/) (key-value pairs)—metric, location, device. This is to allow for flexible querying as you will see in the upcoming sections.

Here are a couple of examples to give you an idea of how you would add data points using the TS.ADD command:

# temperature for device 2 in location 3 along with labels:

TS.ADD temp:3:2 * 20 LABELS metric temp location 3 device 2

# pressure for device 2 in location 3:

TS.ADD pressure:3:2 * 60 LABELS metric pressure location 3 device 2

## Solution architecture

Here is what the solution looks like at a high level:

![Solution architecture](/images/site-mirror/62ea5216cd6320580f9eedf2ad7532c35cd31163-1024x529.webp)

Let’s break it down:

**Source (local) components**

- MQTT broker (mosquitto): [MQTT](https://mqtt.org/) is a de-facto protocol for IoT use cases. The scenario we will be using is a combination of IoT and Time Series – more on this later.
- Kafka Connect: The [MQTT source connector](https://www.google.com/url?q=https://docs.confluent.io/kafka-connect-mqtt/current/mqtt-source-connector/index.html&sa=D&source=editors&ust=1624397707606000&usg=AOvVaw1un7RgqfjiX9-QWyKTIJvP) is used to transfer data from MQTT broker to a Kafka cluster.

**Azure services**

- [Azure Cache for Redis Enterprise tiers](https://docs.microsoft.com/azure/azure-cache-for-redis/quickstart-create-redis-enterprise?WT.mc_id=data-17927-abhishgu): The Enterprise tiers are based on Redis Enterprise, a commercial variant of Redis from Redis. In addition to [RedisTimeSeries](https://docs.redis.com/latest/modules/redistimeseries/), Enterprise tier also supports [RediSearch](https://docs.redis.com/latest/modules/redisearch/) and [RedisBloom](https://docs.redis.com/latest/modules/redisbloom/). Customers don’t need to worry about the license acquisition for Enterprise tiers. Azure Cache for Redis will facilitate this process wherein, customers can obtain and pay for a license to this software through an Azure Marketplace offer.
- [Confluent Cloud on Azure](https://docs.microsoft.com/azure/partner-solutions/apache-kafka-confluent-cloud/overview?WT.mc_id=data-17927-abhishgu): A fully managed offering that provides Apache Kafka as a service, thanks to an integrated provisioning layer from Azure to Confluent Cloud. It reduces the burden of cross-platform management andprovides a consolidated experience for using Confluent Cloud on Azure infrastructure, thereby allowing you to easily integrate Confluent Cloud with your Azure applications.
- [Azure Spring Cloud](https://docs.microsoft.com/azure/spring-cloud/?WT.mc_id=data-17927-abhishgu): Deploying Spring Boot microservices to Azure is easier thanks to Azure Spring Cloud. Azure Spring Cloud alleviates infrastructure concerns, provides configuration management, service discovery, CI/CD integration, blue-green deployments, and more. The service does all the heavy lifting so developers can focus on their code.

*Please note that some of the services were hosted locally just to keep things simple. In production grade deployments you would want to run them in Azure as well. For example you could operate the Kafka Connect cluster along with the MQTT connector in Azure Kubernetes Service.*

To summarize, here is the end-to-end flow:

- A script produces simulated device data that is sent to the local MQTT broker.
- This data is picked up by the MQTT Kafka Connect source connector and sent to a topic in the Confluent Cloud Kafka cluster running in Azure.
- It is further processed by the Spring Boot application hosted in Azure Spring Cloud, which then persists it to the Azure Cache for Redis instance.

It’s time to start off with the practical stuff! Before that, make sure you have the following.

## Prerequisites:

- An Azure account —[you can get one for free here](https://azure.microsoft.com/free/?WT.mc_id=data-17927-abhishgu)
- Install [Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli?WT.mc_id=data-17927-abhishgu)
- JDK 11 for e.g. [OpenJDK](https://openjdk.java.net/projects/jdk/11/)
- A recent version of [Maven](https://maven.apache.org/download.cgi) and [Git](https://git-scm.com/downloads)

## Set up the infrastructure components

Follow the documentation to [provision Azure Cache for Redis (Enterprise Tier)](https://docs.microsoft.com/azure/azure-cache-for-redis/quickstart-create-redis-enterprise?WT.mc_id=data-17927-abhishgu) which comes with the RedisTimeSeries module.

![infrastructure components](/images/site-mirror/46a12a4f672e6ceec930f695577e84a41e817da8-1024x220.webp)

Provision [Confluent Cloud cluster on Azure Marketplace](https://docs.microsoft.com/azure/partner-solutions/apache-kafka-confluent-cloud/create?WT.mc_id=data-17927-abhishgu). Also [create a Kafka topic](https://docs.confluent.io/cloud/current/get-started/index.html#step-2-create-a-ak-topic) (use the name mqtt.device-stats) and [create credentials](https://docs.confluent.io/cloud/current/client-apps/api-keys.html#create-resource-specific-api-keys-in-the-ui) (API key and secret) that you will use later on to connect to your cluster securely.

![kafka cluster](/images/site-mirror/df089d338a1087a71810bdf93c043ee7d64d8427-1024x227.webp)

You can provision an instance of Azure Spring Cloud [using the Azure portal](https://docs.microsoft.com/azure/spring-cloud/quickstart-provision-service-instance?tabs=Azure-portal&pivots=programming-language-java&WT.mc_id=data-17927-abhishgu#provision-an-instance-of-azure-spring-cloud-1) or [use the Azure CLI](https://docs.microsoft.com/cli/azure/ext/spring-cloud/spring-cloud?view=azure-cli-latest&WT.mc_id=data-17927-abhishgu#ext_spring_cloud_az_spring_cloud_create):

```javascript
az spring-cloud create -n <name of Azure Spring Cloud service> -g <resource group name> -l <enter location e.g southeastasia>
```

![Southeast Asia](/images/site-mirror/60207e0295b56de2432694895f8ebad4e145aded-1024x215.webp)

Before moving on, make sure to clone the GitHub repo:

```javascript
git clone https://github.com/abhirockzz/redis-timeseries-kafka
cd redis-timeseries-kafka
```

## Setup local services

The components include:

- [Mosquitto](https://mosquitto.org/) MQTT broker
- Kafka Connect with the [MQTT source connector](https://docs.confluent.io/kafka-connect-mqtt/current/mqtt-source-connector/index.html)
- [Grafana](https://grafana.com/) for tracking time-series data in dashboards

### MQTT broker

I installed and started the mosquitto broker locally on Mac.

```javascript
brew install mosquitto
brew services start mosquitto
```

You can [follow steps corresponding to your OS](https://mosquitto.org/download/) or feel free to use this[ Docker image](https://hub.docker.com/_/eclipse-mosquitto).

### Grafana

I installed and started Grafana locally on Mac.

```javascript
brew install grafana
brew services start grafana
```

You can do the same for your OS or feel free to use this [Docker image](https://hub.docker.com/r/grafana/grafana).

```javascript
docker run -d -p 3000:3000 --name=grafana -e "GF_INSTALL_PLUGINS=redis-datasource" grafana/grafana
```

### Kafka Connect

You should be able to find the connect-distributed.properties file in the repo that you just cloned. Replace the values for properties such as bootstrap.servers, sasl.jaas.config etc.

First, [download and unzip Apache Kafka](https://kafka.apache.org/downloads) locally.

**Start a local Kafka Connect cluster:**

```javascript
export KAFKA_INSTALL_DIR=<kafka installation directory e.g. /home/foo/kafka_2.12-2.5.0>

$KAFKA_INSTALL_DIR/bin/connect-distributed.sh connect-distributed.properties
```

To [install MQTT source connector manually](https://docs.confluent.io/legacy/platform/5.2.4/connect/kafka-connect-mqtt/index.html):

- Download the connector/plugin ZIP file [from this link](https://www.confluent.io/hub/confluentinc/kafka-connect-mqtt), and,
- Extract it into one of the directories that is listed on the Connect worker’s plugin.path configuration properties

*If you’re using Confluent Platform locally, simply use the Confluent Hub CLI: confluent-hub install confluentinc/kafka-connect-mqtt:latest*

**Create MQTT source connector instance**

Make sure to check the mqtt-source-config.json file. Make sure you enter the right topic name for kafka.topic and leave the mqtt.topics unchanged.

```javascript
curl -X POST -H 'Content-Type: application/json'
http://localhost:8083/connectors -d @mqtt-source-config.json

# wait for a minute before checking the connector status
curl http://localhost:8083/connectors/mqtt-source/status
```

## Deploy the device data processor application

In the GitHub repo you just cloned, look for the application.yaml file in the consumer/src/resources folder and replace the values for:

- Azure Cache for Redis host, port and primary access key
- Confluent Cloud on Azure API key and secret

Build the application JAR file:

```javascript
cd consumer

export JAVA_HOME=<enter absolute path e.g. /Library/Java/JavaVirtualMachines/zulu-11.jdk/Contents/Home>

mvn clean package
```

Create an Azure Spring Cloud application and deploy the JAR file to it:

```javascript
az spring-cloud app create -n device-data-processor -s <name of Azure Spring Cloud instance> -g <name of resource group> --runtime-version Java_11

az spring-cloud app deploy -n device-data-processor -s <name of Azure Spring Cloud instance> -g <name of resource group> --jar-path target/device-data-processor-0.0.1-SNAPSHOT.jar
```

## Start simulated device data generator

You can use the script in the GitHub repo you just cloned:

```javascript
./gen-timeseries-data.sh
```

Note—all it does is use the mosquitto_pub CLI command to send data.

Data is sent to the device-stats MQTT topic (this is *not* the Kafka topic). You can double check by using the CLI subscriber:

```javascript
mosquitto_sub -h localhost -t device-stats
```

Check the Kafka topic in the Confluent Cloud portal. You should also [check the logs](https://docs.microsoft.com/cli/azure/ext/spring-cloud/spring-cloud/app?view=azure-cli-latest&WT.mc_id=data-17927-abhishgu#ext_spring_cloud_az_spring_cloud_app_logs) for the device data processor app in Azure Spring Cloud:

```javascript
az spring-cloud app logs -f -n device-data-processor -s <name of Azure Spring Cloud instance> -g <name of resource group>
```

## Enjoy Grafana dashboards!

Browse to the Grafana UI at localhost:3000.

![Grafana dash](/images/site-mirror/aa1e55f69bb9ea3c370a1d9c815a1e79ef4dd3e4-880x807.webp)

The Redis Data Source plugin for Grafana works with any Redis database, including Azure Cache for Redis. Follow the [instructions in this blog post](https://abhishek1987.medium.com/an-easy-to-use-monitoring-solution-for-redis-5a8a73d56129) to configure a data source.

Import the dashboards in the grafana_dashboards folder in the GitHub repo you had cloned (refer to the [Grafana documentation](https://grafana.com/docs/grafana/latest/dashboards/export-import/#importing-a-dashboard) if you need assistance on how to import dashboards).

For instance, here is a dashboard that shows the average pressure (over 30 seconds) for device 5 in location 1 (uses TS.MRANGE).

![avg pressure](/images/site-mirror/4254961d3a4e64304387c2ee371dd0a8b1d6ad0e-1024x548.webp)

Here is another dashboard that shows the maximum temperature (over 15 seconds) for multiple devices in location 3 (again, thanks to TS.MRANGE).

![max temp](/images/site-mirror/a8553a319551d0b8b06a2e285714bdfa445bb35a-1024x549.webp)

## So, you want to run some RedisTimeSeries commands?

Crank up the redis-cli and connect to the Azure Cache for Redis instance:

```javascript
redis-cli -h <azure redis hostname e.g. myredis.southeastasia.redisenterprise.cache.azure.net> -p 10000 -a <azure redis access key> --tls
```

Start with simple queries:

```javascript
# pressure in device 5 for location 1
TS.GET pressure:1:5

# temperature in device 5 for location 4
TS.GET temp:4:5
```

Filter by location and get temperature and pressure for **all **devices:

```javascript
TS.MGET WITHLABELS FILTER location=3
```

Extract temperature and pressure for all devices in one or more locations within a specific time range:

```javascript
TS.MRANGE - + WITHLABELS FILTER location=3
TS.MRANGE - + WITHLABELS FILTER location=(3,5)
```

– + refers to everything from beginning up until the latest timestamp, but you could be more specific.

MRANGE is what we needed! We can also filter by a specific device in a location and further drill down by either temperature or pressure:

```javascript
TS.MRANGE - + WITHLABELS FILTER location=3 device=2
TS.MRANGE - + WITHLABELS FILTER location=3 metric=temp
TS.MRANGE - + WITHLABELS FILTER location=3 device=2 metric=temp
```

All these can be combined with aggregations.

```javascript
# all the temp data points are not useful. how about an average (or max) instead of every temp data points?
TS.MRANGE - + WITHLABELS AGGREGATION avg 10000 FILTER location=3 metric=temp
TS.MRANGE - + WITHLABELS AGGREGATION max 10000 FILTER location=3 metric=temp
```

It’s also possible to create a rule to do this aggregation and store it in a different time series.

Once you’re done, don’t forget to delete resources to avoid unwanted costs.

## Delete resources

- [Follow the steps in the documentation](https://docs.microsoft.com/azure/partner-solutions/apache-kafka-confluent-cloud/manage?WT.mc_id=data-17927-abhishgu#delete-confluent-organization) to delete the Confluent Cloud cluster—all you need is to delete the Confluent organization.
- Similarly, you should [delete the Azure Cache for Redis instance](https://docs.microsoft.com/azure/azure-cache-for-redis/cache-go-get-started?WT.mc_id=data-17927-abhishgu#clean-up-resources) as well.

On your local machine:

- Stop the Kafka Connect cluster
- Stop the mosquito broker (e.g. brew services stop mosquito)
- Stop Grafana service (e.g. brew services stop grafana)

We explored a data pipeline to ingest, process, and query time-series data using Redis and Kafka. When you think about next steps and move towards a production grade solution, you should consider a few more things.

## Additional considerations

![downsampling ](/images/site-mirror/16fb044c209cbd7e7341299bc6f94075d1e3681d-1024x428.webp)

**Optimizing RedisTimeSeries**

- [Retention policy](https://oss.redis.com/redistimeseries/configuration/#retention_policy): Think about this since your time-series data points **do not** get trimmed or deleted by default.
- Down-sampling and Aggregations [Rules](https://oss.redis.com/redistimeseries/commands/#aggregation-compaction-downsampling): You don’t want to store data forever, right? Make sure to configure appropriate rules to take care of this (e.g. TS.CREATERULE temp:1:2 temp:avg:30 AGGREGATION avg 30000).
- Duplicate data policy: How would you like to handle duplicate samples? Make sure that the default policy (BLOCK) is indeed what you need. If not, consider [other options](https://oss.redis.com/redistimeseries/configuration/#duplicate_policy).

This is not an exhaustive list. For other configuration options, please refer to the [RedisTimeSeries documentation](https://oss.redis.com/redistimeseries/configuration/)

## What about long term data retention?

Data is precious, including time series! You may want to process it further (e.g. run machine learning to extract insights, predictive maintenance ,etc.). For this to be possible, you will need to retain this data for a longer time frame, and for this to be cost-effective and efficient, you would want to use a scalable object storage service such [Azure Data Lake Storage Gen2](https://docs.microsoft.com/azure/storage/blobs/data-lake-storage-introduction?WT.mc_id=data-17927-abhishgu) (ADLS Gen2).

![data retention](/images/site-mirror/9733360f243e01fa14562cf08767280682d8b580-789x322.webp)

There is a connector for that! You could enhance the existing data pipeline by using the fully-managed [Azure Data Lake Storage Gen2 Sink Connector for Confluent Cloud](https://docs.confluent.io/cloud/current/connectors/cc-azure-datalakeGen2-storage-sink.html) to process and store the data in ADLS and then run machine learning using [Azure Synapse Analytics](https://docs.microsoft.com/azure/synapse-analytics/spark/apache-spark-machine-learning-mllib-notebook?WT.mc_id=data-17927-abhishgu#predictive-analysis-example-on-nyc-taxi-data) or [Azure Databricks](https://docs.microsoft.com/azure/databricks/applications/machine-learning/?WT.mc_id=data-17927-abhishgu).

**Scalability**

Your time-series data volumes can only move one way—up! It’s critical for your solution to be scalable:

- Core infrastructure: Managed services allow teams to focus on the solution rather than setting up and maintaining infrastructure, especially when it comes to complex distributed systems such as databases and streaming platforms such as Redis and Kafka.
- Kafka Connect: As far as the data pipeline is concerned, you’re in good hands since Kafka Connect platform is inherently stateless and horizontally scalable. You’ have a lot of options in terms of how you want to architect and size your Kafka Connect worker clusters.
- Custom applications: As was the case in this solution, we built a custom application to process data in Kafka topics. Fortunately, the same scalability characteristics apply to them as well. In terms of horizontal scale, it is limited only by the number of Kafka topic partitions you have.

**Integration**: It’s not just Grafana! RedisTimeSeries also integrates with [Prometheus](https://github.com/RedisTimeSeries/prometheus-redistimeseries-adapter) and Telegraf. However, there is no Kafka connector at the time this blog post was written—this would be a great add-on!

## Conclusion

Sure, you can use Redis for (almost) everything, including time-series workloads! Be sure to think about the end-to-end architecture for data pipeline and integration from time-series data sources, all the way to Redis and beyond.
