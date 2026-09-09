---
title: "How to Build an Application to Power Your Log Analysis Using Redis"
linkTitle: "How to Build an Application to Power Your Log Analysis Using Redis"
url: "/blog/how-to-build-an-application-to-power-your-log-analysis-using-redis/"
description: "As your IT infrastructure grows in size and becomes complex, you may be forced to spend more attention ensuring that everything is managed properly."
date: 2021-12-02
blogCategories:
- "How To and Tutorials"
- "Tech"
authors:
- "Growth Team"
lastmod: 2025-03-04
hidden: true
---

*By Growth Team · Published 2 December 2021 · updated 4 March 2025*

![Blog tile image](/images/blog/1804154c4ee919127aef02346c7c529e2d4c27dc-772x520.webp)

As your IT infrastructure grows in size and becomes complex, you may be forced to spend more attention ensuring that everything is managed properly.

Since the rise of the cloud, this has become especially more relevant, given that we now have an abundance of technical information spread across many different locations.

But being able to carry out comprehensive log analysis can be tedious, time-consuming and *painfully boring.*

A simple yet effective way to liberate yourself from this burden is to use software or applications that are designed to make monitoring logs easy… and that’s exactly what Alexis Gardin has done in his application, [Logub](https://www.youtube.com/watch?v=SQXpUkSwwPM).

Unlike many other SaaS solutions, Logub can carry out these actions on-premises and open source. By following the steps below, you’ll be able to create an application that will collect, explore, and analyze application logs for you.

At the heart of this application was a reliance on RediSearch’s ability to explore and analyze logs across different locations with unrivaled efficiency. Let’s look into how Alexis brought this application together.

But before we dive in, we should let you know that we also have an exciting range of applications for you to check out on the [Redis Launchpad](https://launchpad.redis.com/).


[Click here to view video](https://www.youtube.com/embed/6ZqfboCjLtk)

1. What will you build?
1. What will you need?
1. Architecture
1. Getting started
1. How data is stored
1. How data is queried
1. How does the search bar work?
1. How to integrate Logub to your project?
1. Conclusion

## 1. What will you build?

You’ll build a special app that’s powered by Redis to collect, analyse and explore log applications. In the steps below, we’ll go through A-Z of what’s required to build this application, along with the required components.

Even if you’re new to Redis, we’ll show you exactly how to get to grips with this powerful database. Are you ready to get started?

Ok, let’s dive straight in.


## 2. What will you need?

- [**Fluentd**](https://www.fluentd.org/)**: **used as a cross-platform open-source data collection software for processing logs.
- [**Redis output plugin for Fluent:**](https://github.com/fluent-plugins-nursery/fluent-plugin-redis)fluent-plugin-redis is a fluent plugin to output to redis.RediSearch:
- [**Docker**](https://www.docker.com/)**: **used as a platform for developers to package applications to containers.
- [**Docker Compose**](https://docs.docker.com/compose/)**: **used for defining and running multi-container Docker applications.

## 3. Architecture

![](/images/blog/285d5eed01912d4772e5537aa40038ef7b9ce20c-1600x382.webp)

- Fluentd collects all of the logs from each application across various destinations
- Fluentd then formats each log and sends them to Redis for storage
- The data is stored using the Fluentd Redis plugin – a fluent plugin to output to redis.
- The Logub backend allows RediSearch to carry out a full-text search and index fields defined by the user.

## 4. Getting Started

In the demo, a DEMO app will publish logs in Logub. You’ll be able to interact with this DEMO app to generate your logs. You’ll then be able to request them in Logub

## Prerequisites

- Docker
- Docker Compose

Firstly, make sure that the given ports are open on your system: 8080, 8081, 3000 & 6379.

### Step 1: Clone the repository

git clone https://github.com/redis-developer/logub

### Step 2. Bring up the DEMO app

- Go to /demo folder (cd ./demo)
- Launch the docker-compose with the given command:

```python
docker-compose up -d

```

### Launch Logub demo

```python
% docker-compose ps
NAME                      COMMAND                  SERVICE             STATUS              PORTS
demo_fluentd_1            "tini -- /bin/entryp…"   fluentd             running             5140/tcp, 0.0.0.0:24224->24224/tcp, :::24224->24224/tcp, 0.0.0.0:24224->24224/udp, :::24224->24224/udp
demo_logub-controller_1   "java -XX:+UnlockExp…"   logub-controller    running             0.0.0.0:8080->8080/tcp, :::8080->8080/tcp
demo_logub-generator_1    "java -XX:+UnlockExp…"   logub-generator     running             0.0.0.0:8081->8081/tcp, :::8081->8081/tcp
demo_logub-ui_1           "docker-entrypoint.s…"   logub-ui            running             0.0.0.0:3000->3000/tcp, :::3000->3000/tcp
demo_redis_1              "redis-server /usr/l…"   redis               running             0.0.0.0:6379->6379/tcp, :::6379->6379/tcp

```

Go to [localhost:3000](localhost:3000) to explore logs.

![](/images/blog/fd6d228fbb08266c4a6fd5c27ffb3a4f8823d102-1600x921.webp)

It may take around one minute for you to see the logs coming. You can view the logs on the page by filtering them with the sidebar on the right. Alternately, you search for them by filter or full-text query via the search bar at the top.

When you click on a log, the details will be displayed and you’ll have the option to index business properties. These business properties can be used as filters afterwards.

![](/images/blog/dbd48476ac99aa39ff17bb46ee64dafdb23f4e3b-1600x1326.webp)

Next, go to localhost:3000/demo to access the playground and add your custom logs. This demo page will allow you to:

- create fake users in the demo fake app and see them in logs.
- publish your logs in the system.

![](/images/blog/02ecfcfb988efffe072851518e426a82f38618d7-1600x896.webp)

If you return to the main page, you can try to search for the logs you’ve just generated.

**Note:** There is a latency of around 1 minute between the production of a log in a container and its display in Logub. This latency is caused by the process of collecting, formatting, and ingesting the logs into the database.

## 5. How does it work?

### How data is stored

Data is stored using the [Fluentd Redis Plugin](https://github.com/fluent-plugins-nursery/fluent-plugin-redis). It stores each log with HSET. For example: HSET level DEBUG message “Hello World” thread main

### How data is queried

```python
public class LogubLog {
  @Builder.Default
  private String id = UUID.randomUUID().toString();

  @Builder.Default
  private String index = "principal";

  @NonNull
  private SystemProperties systemProperties;

  @Builder.Default
  private Map<String, Object> businessProperties = Collections.emptyMap();

  @Builder.Default
  private Optional<String> message = Optional.empty();

  @Builder.Default
  private Instant timestamp = Instant.now();

  @Builder.Default
  private Optional<String> service = Optional.empty();

  @Builder.Default
  private Optional<String> logger = Optional.empty();

  @Builder.Default
  private Optional<String> thread = Optional.empty();

  @Builder.Default
  private Optional<String> source = Optional.empty();

  @Builder.Default
  private LogLevel level = UNKNOWN;

}

public class SystemProperties {
  @Builder.Default
  Optional<String> imageName = Optional.empty();

  @Builder.Default
  Optional<String> containerName= Optional.empty();

  @Builder.Default
  Optional<String> containerId= Optional.empty();

  @Builder.Default
  Optional<String> env= Optional.empty();

  @Builder.Default
  Optional<String> host= Optional.empty();

}

```

This is the object that you’ll use to manipulate logs and retrieve them from Redis. Carrying out this action will allow the Logub UI to display the logs. To make complex queries in your logs, you can use RediSearch.

Since you’re able to change the RediSearch schema dynamically, you can use the ‘List’ data structure to keep track of which schema is indexed.

```python
public class LogSearch {

 @Builder.Default
 private List<LogubFieldSearch> texts = emptyList();

 @Builder.Default
 private List<LogubFieldSearch> systemProperties = emptyList();

 @Builder.Default
 private List<LogubFieldSearch> businessProperties = emptyList();

 @Builder.Default
 private List<LogubFieldSearch> basicProperties = emptyList();

 @Builder.Default
 private List<LogubFieldSearch> levels = Collections.emptyList();

 @Builder.Default
 private int limit = 25;

 @Builder.Default
 private int offset = 0;

 @Builder.Default
 private Optional<LogubSort> sort = Optional.empty();

 @Builder.Default
 private Instant beginAt = Instant.now().minus(15, ChronoUnit.MINUTES);

 @Builder.Default
 private Instant endAt = Instant.now();


 @SneakyThrows
 public QueryBuilder toQuery() {
  var query = new QueryBuilder();
  var businessPrefix = "businessProperties.";
  var systemPropertiesPrefix = "systemProperties.";

  for (LogubFieldSearch properties : businessProperties) {
    query.append(QueryBuilders.tag(businessPrefix + properties.getName(), properties.getValues(),
    properties.isNegation()));
  }
  for (LogubFieldSearch properties : systemProperties) {
    query.append(QueryBuilders
    .tag(systemPropertiesPrefix + properties.getName(), properties.getValues(),
    properties.isNegation()));
  }
  for (LogubFieldSearch properties : basicProperties) {
    query.append(QueryBuilders
    .tag(properties.getName(), properties.getValues(),
    properties.isNegation()));
  }

  if (!levels.isEmpty()) {
    for (LogubFieldSearch level : levels) {
      var onError = !level.getValues().stream().allMatch(v -> Arrays.stream(LogLevel.values())
      .anyMatch(enumLevel -> enumLevel.name().equalsIgnoreCase(v)));
      if(onError){
        log.error("bad payload for levels {}", level);
        throw new IllegalArgumentException("bad payload for level");
      }
    query.append(QueryBuilders.tag("level",level.getValues(), level.isNegation()));
    }
  }
  for (LogubFieldSearch text : texts) {
    if(!text.getType().equals(LogubFieldType.FullText)){
      log.warn("type {} not handle for text search", text.getType());
    }
    for (String value : text.getValues()) {
      query.append(QueryBuilders.text("message", value, text.isNegation()));
    }
  }

  return query;
 }


}

```

The above command will allow you to create a plain text RediSearch query based on the user input. There are a bunch of small QueryBuilders built on the top of the RediSearch library. It’s the same command that will be sent by Logub UI to carry out a comprehensive and efficient search in your logs.

### Step 2: How to work the search bar

You can carry out the search by tag or full-text search. Below are some examples you can use as models if you get stuck.

- env:dev Ut ea vero voluptate* will search all logs in the dev environment with a message that start with Ut ea vero voluptate
- -env:prod Ut ea vero voluptate* will search all logs in all environnement except prod with a message that start with Ut ea vero voluptate
- originRequest:France originRequest:USA will search all logs that have a field originRequest with a value set at France or USA
- “dog” “cat” will search all logs that contain the words “dog” and “cat”
- -“dog” “cat” will search all logs that don’t contain “dog” but contain “cat”

For you to have a good testing experience with the app, we highly recommend that you create your own log with the playground, add business properties and then do some experimentation just to get a feel for it.

### Step 3: How to integrate Logub into your project

#### You will require the below list of Docker images to operate Logub:

- Logub Fluentd image to collect and send logs to Redis – [Logub Fluentd Image](https://hub.docker.com/r/logub/logub-fluentd)
- Redis image with RediSearch module [Redis Mod Image](https://hub.docker.com/r/redislabs/redismod)
- Logub controller image to serve log exploring functionalities – [Logub Contoller Image](https://hub.docker.com/r/logub/logub-controller)
- Logub UI to explore and query logs – [Logub UI Image](https://hub.docker.com/r/logub/logub-ui)

#### Logub log format

For now, Logub can handle only one particular log format. In the future, this format will be extended and more customizable.

Here’s the Logub format

```python
{
 "level": "....",
 "thread": "....",
 "logger": "....",
 "message": "....."
}

```

Please note, these fields are not mandatory.

If you want to add your business properties, you’ll need to add a nested JSON object that has “mdc” as the key. For example:

```python
{
 "level": "....",
 "thread": "....",
 "logger": "....",
 "message": ".....",
 "mdc":{
    "myproperties": "....",
    "anotherOne":".....",
 }
}

```

#### Publishing logs in Logub

To explore logs in Loghub, your containers need to use the Docker Fluentd logging driver. Here’s a configuration example for customer integration.

```python
# Your container(s)
  MY-CUSTOM-APP:
    image: "MY-CUSTOM-APP-IMAGE"
    logging:
      driver: "Fluentd"
      options:
        Fluentd-address: localhost:24224
        tag: MY-CUSTOM-TAG
  ## Logub Fluentd + Redis conf
  logub-controller:
    image: "logub/logub-controller:0.1"
    ports:
      - "8080:8080"
    depends_on:
      - redis
    links:
      - "Fluentd"
      - "redis"
  logub-ui:
    image: "logub/logub-ui:0.1"
    ports:
      - "3000:3000"
    depends_on:
      - redis
  Fluentd:
    image: "logub/logub-Fluentd:0.1"
    links:
      - "redis"
    ports:
      - "24224:24224"
      - "24224:24224/udp"
  redis:
    image: "redislabs/redismod"
    command: ["/usr/local/etc/redis/redis.conf","--bind","redis","--port", "6379"]
    volumes:
      - ./redis/data:/data
      - ./redis/redis.conf:/usr/local/etc/redis/redis.conf
    ports:
      - "6379:6379"

```

### Step 4: Setting up Redis in Logub

**RediSearch**

Logub uses the functionality of RediSearch to process application logs. When logs are persisted in the Redis database, they’re accompanied by 3 types of fields:

- **System properties: **are information that Docker and Fluentd provide us when sending the logs (e.g the environment, the container name etc).
- **Basic properties: **are the basic information that a log has (e.g timestamp, service etc). These properties are automatically indexed in RediSearch.
- **Business properties: **are given by a logub user in a specific field. The user here has to respect a Key-Value (Map) format. Thanks to the advanced capabilities of RediSearch, you’ll be able to index these ‘business properties’ if you want to do some research on them.

```python
{
  "timestamp": "2021-05-14 11:01:11.686",
  "level": "WARN",
  "thread": "scheduling-1",
  "mdc": {
    "app": "Toughjoyfax",
    "correlationId": "521f075f-36be-4f85-957e-d1c87ad71aa8",
    "originRequest": "Tonga",
    "origin": "LoremIpsum"
  },
  "logger": "com.loghub.loggenerator.service.LoggerService",
  "message": "Doloremque dolores ut minima sed."
}

```

Here we have an example of a log that describes how our tool functions when Fluentd flattens and persists in the Redis database. The Logub API will allow the user or the company to index one or all fields of the mdc object.

In this project, the** Tag Datatype** is widely used. Logs are often searched based on business properties when searching in logs (eg a customer id). Moreover, we also use the *TextField Datatype* for log messages. This allows the user to do a full-text search in this field.

Here’s a simplified schema of the search process:

![](/images/blog/1c7dc8cf26fb2c64e2b56154869dd11e08344165-1600x506.webp)

**Redis**

Redis is used to store logs by Fluentd like this in the *HashSet type* of Redis.

![](/images/blog/1a295e3668f7d8be6e6b55fbf180820324d20583-1600x514.webp)

To keep track of the indexed field by the user, you can also add a ‘schema’ object which uses the *List type* of Redis.

![](/images/blog/093567a0b377e6bcdefc109583db73bf32af2478-1600x567.webp)

## Conclusion: Cutting Through The Clutter With RediSearch

A drawback to the explosion of digital innovations, such as the cloud, is that monitoring IT infrastructure can become complex. Applications are likely to be scattered across different locations, making it challenging to difficult to pull every log into one location.

However, by using Redis, the monotony of this process is removed, allowing you to search, gather and store logs with ease. If you want to learn more about the ins and outs of how this application was made, then you can check out Alexis’ [YouTube video here](https://www.youtube.com/watch?v=6ZqfboCjLtk).

We also have an exciting range of innovative applications that have been developed by talented programmers just like Alex on our [Launchpad](https://launchpad.redis.com/). Check it out, be inspired and see what innovations you can come up with using Redis.

[Watch the video](https://launchpad.redis.com/)

**Who built this application?**

![](/images/blog/9735c1370b546b402fd5370c40e0da3ce02ce296-400x400.webp)

**Alexis Gardin**

Alexis is an innovative software engineer who currently works for Zendoc. Head over to [his GitHub page](https://github.com/alexisgardin) to see what other projects he’s been involved in.
