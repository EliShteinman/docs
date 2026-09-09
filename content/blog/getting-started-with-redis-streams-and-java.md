---
title: "Getting Started with Redis Streams and Java"
linkTitle: "Getting Started with Redis Streams and Java"
url: "/blog/getting-started-with-redis-streams-and-java/"
description: "As a new Enterprise Technical Account Manager at Redis, one of my first tasks was to learn more about Redis. So I started digging in, and quickly discovered Redis Streams. As a big fan of..."
date: 2020-01-07
blogCategories:
- "Tech"
authors:
- "Tugdual Grall"
lastmod: 2026-09-01
hidden: true
---

*By Tugdual Grall, Technical Marketing Manager · Published 7 January 2020 · updated 1 September 2026*

![Blog tile image](/images/site-mirror/0e2e20f04c3d701f9cabf8a32edc06102a36a24d-386x237.webp)

As a new Enterprise Technical Account Manager at [Redis](https://www.redis.com/), one of my first tasks was to learn more about Redis. So I started digging in, and quickly discovered [Redis Streams](https://redis.io/docs/latest/develop/). As a big fan of streaming-based applications, I am thrilled to share what I’ve learned about how to use Redis Streams and Java.

## What is Redis Streams?

Redis Streams is a Redis data type that represents a log, so you can add new information and message in an append-only mode *(Note: This is not 100% accurate, since you can remove messages from the log, but it’s close enough.)* Redis Streams lets you build “Kafka-like” applications, which can:

- Create applications that publish and consume messages. Nothing extraordinary here, you could already do that with Redis Pub/Sub.
- Consume messages that are published even when the client application (consumer) is not running. This is a big difference from Redis Pub/Sub.
- Consume messages starting from a specific point. For example, read the whole history or only new messages.

In addition, Redis Streams has the concept of **consumer groups**. Redis Streams consumer groups, like the similar concept in [Apache Kafka](https://kafka.apache.org/), allows client applications to consume messages in a distributed fashion (multiple clients), making it easy to scale and create highly available systems.

So, while it may be tempting to compare Redis Streams and Redis Pub/Sub and decide that one is better than the other, these two features aim to accomplish different things. If you’re evaluating Pub/Sub and Redis Streams and it’s not immediately clear, you might want to think either more about your problem to be solved or re-read the documentation on both.

![](/images/site-mirror/51a94e625f79eeda9cde2cc74d6f1cdf483b0adb-1012x321.webp)

(Enroll in the [Redis University: Redis Streams](https://university.​redis.​com/courses/ru202/) course to learn more.)

## Java and Redis Streams

The best way to learn how to use Redis Streams and Java, is to build a sample application. The [redis-streams-101-java GitHub repository](https://github.com/tgrall/redis-streams-101-java) contains sample code that shows how to post messages to a Stream and consume messages using a consumer group. To get started, you’ll need Redis 5.x, Java 8 or later, Apache Maven 3.5.x, and Git.

Redis has many Java clients developed by the community, as you can see on [Redis.io](https://redis.io/clients#java). My current favorite for working with Redis Streams is [Lettuce](https://lettuce.io/), so what I use in this sample app. Let’s walk through the steps involved in creating the sample project:

#### Step 1: Adding Lettuce to your Maven project

Add the dependency below to your project file:

```python
<dependency>
  <groupId>io.lettuce</groupId>
  <artifactId>lettuce-core</artifactId>
  <version>5.1.8.RELEASE</version>
</dependency>

```

#### Step 2: Connecting to Redis

Import the following classes:

```python
import io.lettuce.core.*;
import io.lettuce.core.api.StatefulRedisConnection;
import io.lettuce.core.api.sync.RedisCommands;

```

Then connect with:

```python
RedisClient redisClient = RedisClient.create("redis://password@host:port"); // change to reflect your environment
StatefulRedisConnection<String, String> connection = redisClient.connect();
RedisCommands<String, String> syncCommands = connection.sync();

```

When your application is done with the connection, disconnect using the following code:

```python
connection.close();
redisClient.shutdown();

```

#### Step 3: Sending a message to Redis Streams

Once you have a connection, you can send a message. In this example, I let Redis generate the message ID, which is time-based, and build the body using a map representing Internet of Things weather data capturing wind speed and direction in real-time:

```python
public static void main(String[] args) {

    RedisClient redisClient = RedisClient.create("redis://localhost:6379"); // change to reflect your environment
    StatefulRedisConnection<String, String> connection = redisClient.connect();
    RedisCommands<String, String> syncCommands = connection.sync();

    Map<String, String> messageBody = new HashMap<>();
    messageBody.put( "speed", "15" );
    messageBody.put( "direction", "270" );
    messageBody.put( "sensor_ts", String.valueOf(System.currentTimeMillis()) );

    String messageId = syncCommands.xadd(
            "weather_sensor:wind",
            messageBody);

    System.out.println( String.format("Message %s : %s posted", messageId, messageBody) );

    connection.close();
    redisClient.shutdown();

}

```

Here’s what’s happening in the code:

- Lines 3-5 connect to Redis
- Lines 7-10 create the message body, using a map, since Redis Streams messages are string key/values in Java.
- Lines 12-14 call the syncCommands.xadd() method using the streams key “weather_sensor:wind” and the message body itself. This method returns the message ID.
- Line 16 prints the message ID and content.
- Lines 18-19 close the connection and the client.

(The complete producer code is available [here](https://github.com/tgrall/redis-streams-101-java/blob/master/src/main/java/com/kanibl/redis/streams/simple/RedisStreams101Producer.java).)

#### Step 4: Consuming messages

Redis Streams offers several ways to consume and read messages using the commands: [XRANGE](https://redis.io/commands/xrange), [XREVRANGE](https://redis.io/commands/xrevrange), [XREAD](https://redis.io/commands/xread), [XREADGROUP](https://redis.io/commands/xreadgroup). To focus on how to build an application with Apache Kafka, let’s use the [XREADGROUP](https://redis.io/commands/xreadgroup) command from Lettuce.

The consumer group allows developers to create a group of clients that will cooperate to consume messages from the streams (for scale and high availability). It is also a way to associate the client to specific applications roles; for example:

- A consumer group called “data warehouse” will consume messages and send them to a data warehouse
- Another consumer group called “aggregator” will consume the messages and aggregate the data and send the aggregated result to another sink (another stream or storage)

Each of these consumer groups will act independently, and each of this group could have multiple “consumers” (clients).

Here’s how it works in Java:

```python
...

        try {
            // WARNING: Streams must exist before creating the group
            //          This will not be necessary in Lettuce 5.2, see https://github.com/lettuce-io/lettuce-core/issues/898
            syncCommands.xgroupCreate( XReadArgs.StreamOffset.from("weather_sensor:wind", "0-0"), "application_1"  );
        }
        catch (RedisBusyException redisBusyException) {
            System.out.println( String.format("\t Group '%s' already exists","application_1"));
        }


        System.out.println("Waiting for new messages");

        while(true) {

            List<StreamMessage<String, String>> messages = syncCommands.xreadgroup(
                    Consumer.from("application_1", "consumer_1"),
                    XReadArgs.StreamOffset.lastConsumed("weather_sensor:wind")
            );

            if (!messages.isEmpty()) {
                for (StreamMessage<String, String> message : messages) {
                    System.out.println(message);
                    // Confirm that the message has been processed using XACK
                    syncCommands.xack(STREAMS_KEY, "application_1",  message.getId());
                }
            }

        }

...

```

This code is a subset of the main() method. I removed the connection management part to make it more readable. Let’s take a look at the code.

- Lines 3 to 10, using the method xgroupCreate(), that matches the [XGROUP CREATE](https://redis.io/commands/xgroup) command:
  - Creates a new group called application_1.
  - Consume messages from the stream weather_sensor:wind.
  - The consumer group starts reading at the first message in the stream, indicated using the message ID 0-0. (*Note: You can also indicate to the group to start to read at a specific message ID, or to read only new messages using $ special ID (or the helper method XReadArgs.StreamOffset.latest()*.
- Lines 15 to 30 use an infinite loop (while(true)) to wait for any new messages published to the streams.
- Lines 17 to 20 use the method xreadgroup() to return the messages based on the group configuration:
  - Line 18 defines the consumer named consumer_1 that is associated with the group application_1. You can create a new group do distribute the read to multiple clients.
  - Line 19 indicates where to start, in this case, StreamOffset.lastConsumed(“weather_sensor:wind”). The consumer will consume messages that have not already been read. With the current configuration of the group (offset 0-0), when the consumer starts for the first time, it will read all the existing messages.
- Lines 22 to 28, the application iterates on each message, and:
  - Line 24, process the message, a simple print in this case
  - Line 26, sends an acknowledgment using xack() command. You have to use the ack command to confirm that a message has been read and processed. The XACK command removes the message from the pending list of the consumer group.

The complete consumer code is available [here](https://github.com/tgrall/redis-streams-101-java/blob/master/src/main/java/com/kanibl/redis/streams/simple/RedisStreams101Consumer.java).

## Build and run the simple Java application

Now that you have a better understanding of the code, let’s run the producer and consumer. You can run this from your IDE, or using Maven, but here’s how it works in the Maven CLI. Start by opening two terminals, one to produce messages and one to consume them, then follow these steps:

*Step 1: Clone and build the project:*

```python
> git clone https://github.com/tgrall/redis-streams-101-java.git

> cd redis-streams-101-java

> mvn clean verify

```

*Step 2: Post a new message:*

```python
> mvn exec:java -Dexec.mainClass="com.kanibl.redis.streams.simple.RedisStreams101Producer"

```

*Step 3: Consume messages*

Open a new terminal and run this command:

```python
> mvn exec:java -Dexec.mainClass="com.kanibl.redis.streams.simple.RedisStreams101Consumer"

```

The consumer will start and consume the message you just posted, and wait for any new messages.

*Step 4: In the first terminal, post 100 new messages:*

```python
> mvn exec:java -Dexec.mainClass="com.kanibl.redis.streams.simple.RedisStreams101Producer" -Dexec.args="100"

```

The consumer will receive and print all the messages.

*Step 5: Kill the consumer and post more messages*

Let’s do another test: Stop the consumer using a simple Ctrl+C and then post five new messages:

```python
> mvn exec:java -Dexec.mainClass="com.kanibl.redis.streams.simple.RedisStreams101Producer" -Dexec.args="5"

```

The messages are not yet consumed by any application, but are still stored in Redis Streams. So when you start the consumer, it consumes these new messages:

```python
> mvn exec:java -Dexec.mainClass="com.kanibl.redis.streams.simple.RedisStreams101Consumer"

```

This is one of the differences between [Redis Streams](https://redis.io/docs/latest/develop/) and [Redis Pub/Sub](https://redis.io/topics/pubsub). The producer application has published many messages while the consumer application was not running. Since the consumer is run with StreamOffset.lastConsumed(), when the consumer is starting, it looks to the last consumed ID, and starts to read the streams from there. This method generates a XGROUPREAD command with the group.

## Conclusion

This small project was designed to show you how to use Lettuce, a Java client for Redis, to publish messages to a stream, create a consumer group, and consume messages using the consumer group.

This is a very basic example, and in upcoming posts I plan to dive into how to work with multiple consumers and how to configure the consumer group and consumers to control which messages you want to read.
