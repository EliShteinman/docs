---
title: "How to Build a Powerful E-Learning Platform Using Scala and Redis"
linkTitle: "How to Build a Powerful E-Learning Platform Using Scala and Redis"
url: "/blog/how-to-build-a-powerful-e-learning-platform-using-scala-and-redis/"
description: "Never before has online learning been so accessible. Whether you want to discover more about cryptocurrency, sharpen your programming skills or even just learn a new language, the digital age has..."
date: 2021-11-05
blogCategories:
- "How To and Tutorials"
- "Tech"
authors:
- "Growth Team"
lastmod: 2025-03-27
hidden: true
---

*By Growth Team · Published 5 November 2021 · updated 27 March 2025*

![Blog tile image](/images/blog/3466217c8543b62c874674d5c4b850710d58766f-772x520.webp)

Never before has online learning been so accessible. Whether you want to discover more about cryptocurrency, sharpen your programming skills or even just learn a new language, the digital age has gifted everyone access to a phenomenal amount of content.

However, over time e-learning has been viewed as just another digital commodity, where users expect all online content to be instantaneous. Speed remains crucial to performance, where any lags or delays in page loading time kills the user’s experience.

And so these high expectations require any competent e-learning platform to be powered by a database that’s capable of handling, processing and transmitting data with hyper-efficiency…which is *exactly* why this [Launchpad App](https://launchpad.redis.com/?id=project%3Ax-mentor) used Redis.

From start to finish, this application was built to connect, educate and empower learners by connecting them with the most relevant courses based on their interests.

Let’s investigate how this was achieved. But before we dive in, you may also want to check out all of the other amazing applications that we have on the [Launchpad](https://launchpad.redis.com/).

[Click here to view video](https://www.youtube.com/embed/7k1EXPh3m4s)

1. What will you build?
1. What will you need?
1. Architecture
1. Getting started

## 1. What will you build?

You’ll build a powerful e-learning platform that will connect students and teachers with one another along with a diverse library of online courses. With speed being the linchpin to performance, you’ll deploy a number of different Redis components to achieve this objective.

Below we’ll reveal what components are required to make this application come to fruition along with the functionality of each item.

![](/images/blog/3b66592d52173a2842509e7cbd67c1f86c9e13ef-1600x871.webp)

## 2. What will you need?

- [**Scala**](https://www.scala-lang.org/)**/**[**Play Framework**](https://www.playframework.com/)**/Akka Streams: **used as an open-sourced web application that makes building apps with Java and Scala easy.
- [**React**](https://react.dev/)**: **used as a Javascript library to build user interfaces easily.
- [**RedisGraph**](https://redis.io/docs/stack/graph/)**: **used as a powerful graph database that translates Cypher queries to matrix operations executed over a GraphBLAS engine.
- [Redis Streams](https://redis.io/docs/data-types/streams-tutorial/): manages data consumption
- [**RedisBloom**](/modules/redis-bloom/)**: **provides Redis with support for additional probabilistic data structures.
- [**RedisGears**](/learn/howtos/redisgears/)**: **used as the engine for data processing in Redis
- [**RediSearch**](https://redis.io/docs/stack/search/index.html)**: **provides a powerful search engine for Redis.
- [**RedisJSON**](/json/)**:** implements ECMA-404 The JSON Data Interchange Standard as a native data type
- [**RedisTimeSeries**](https://redis.io/docs/stack/timeseries/)**: **provides time series data
- [**Keycloak**](https://www.keycloak.org/)**: **used as an open-sourced identity and access management solution for modern applications

## 3. Architecture

![](/images/blog/3200b1cfaca0beb68a23217599b808ff6a803ed4-1024x554.webp)

The data model is expressed through nodes and relations using RedisGraph. The model is very simple since it involves the Student, Course and Topic entities expressing the different kinds of relations between each other.

![](/images/blog/e0609071215e6593548055613407978b27f2659d-1600x1184.webp)

X-Mentor follows an Event Driven Architecture approach in which the following Domain Events are considered:

- student-enrolled
- student-interested
- student-interest-lost
- course-created
- course-rated
- course-recommended
- Student-progress-registered

## 4. Getting started

### Prerequisites

- Docker Engine and Docker Compose

#### Step 1: Clone the repository

```python
https://github.com/redis-developer/x-mentor

```

#### Step 2: Start the docker

```python
$ docker-compose ps
Name                         Command               State            Ports              
---------------------------------------------------------------------
x-mentor_x-gears_1           python3 init.py --url redi ...   Up                                   
x-mentor_x-keycloak_1        /opt/jboss/tools/docker-en ...   Up       0.0.0.0:8880->8080/tcp, 8443/tcp
x-mentor_x-mentor-client_1   /docker-entrypoint.sh ngin ...   Up       0.0.0.0:3000->80/tcp            
x-mentor_x-mentor-core_1     /opt/docker/conf/wait-for- ...   Up       0.0.0.0:9000->9000/tcp          
x-mentor_x-redis_1           redis-server --loadmodule  ...   Up       0.0.0.0:6379->6379/tcp          
[node1] (local) root@192.168.0.8 ~/x-mentor
$ 

```

#### Step 3: Accessing the application

Wait until Keycloak and x-mentor-core are ready, then go to http://localhost:3000.

![](/images/blog/3c54d8f60ad299c96e5e7ab1facbf23c944467e1-1600x430.webp)

You can access Keycloak via 8880 port as shown below:

![](/images/blog/2bd8a17460176ca9123bac5fdbd01e5bb79679b6-1600x925.webp)

Use admin/admin to login into keycloak.

![](/images/blog/a09ba6839d6d1316975f405cf5d27da048f11609-1600x927.webp)

#### Step 4: Logging in

This step starts the authentication process against Keycloak by:

1. Verifying if the user’s username already exists in users bloom filter
1. Providing an auth token

Use the following code to check and see whether the username already exists in users bloom filter:

```python
BF.EXISTS users '${student.username}'

```

![](/images/blog/f7c6d6d8c603a921a9eb58dd791bae0e776cf91d-1181x1600.webp)

#### Step 5: Signing up

Signing up involves 4 steps:

1. Registering a user against Keycloak
1. Adding a user’s username to users bloom filter
1. Creating a user in RedisGraph
1. Adding student’s time series key (needed for registering student progress)

![](/images/blog/c443e77f1d319954bf0b376be011a7cc76c7a5dd-1600x1077.webp)

- To add a username to users bloom filter, insert the following code

```python
BF.ADD users '${student.username}'

```

- To integrate students into the graph, use the below code

```python
GRAPH.QUERY xmentor "CREATE (:Student {username: '${student.username}', email: '${student.email}'})"

```

- To create student progress timeseries key, use the below code

```python
TS.CREATE studentprogress:${username} RETENTION 0 LABELS student ${username}

```

#### Step 6: Creating Courses

In this step we’re going to show you how to create courses to go on the e-learning platform. Each course is going to be stored as a JSON in RedisJSON.

:

Follow the commands below:

1. Obtain the last course id from the Redis key: course-last-index

```python
GET course-last-index

```

1. Increase course id key in 1

```python
INCR course-last-index

```

1. Store course as JSON in redisJSON

```python
JSON.SET course:${course.id} . '${course.asJson}'

```

1. Add course id to courses bloom filter

```python
BF.ADD courses '${course.id}'

```

1. Create course in the graph

```python
GRAPH.QUERY xmentor "CREATE (:Course {name: '${course.title}', id: '${course.id.get}', preview: '${course.preview}'})"

```

1. Publish course-created event which sends notifications by Server Sent Event to the frontend

```python
XADD course-created $timestamp title ${course.title} topic ${course.topic}

```

#### Step 7: Enrolling courses

Here we’ll uncover how you can enroll a student in a specific course.

![](/images/blog/9a290d390fb99247df6db4dbe425db9cf19a5067-1600x845.webp)

Below are the steps for you to follow:

- To verify if a student exists in users bloom filter:

```python
BF.EXISTS users ${student.username}

```

- To get course as JSON from redisJSON

```python
JSON.GET course:${course.id}

```

- To highlight a relationship between the student and the course in redisGraph

```python
GRAPH.QUERY xmentor "MATCH (s:Student), (c:Course) WHERE s.username = '${studying.student}' AND c.name = '${studying.course}' CREATE (s)-[:studying]->(c)"

```

#### Step 8: Course review

As part of any online resource, users generally are able to provide a review. To make this functionality happen, you need to carry out the following steps:

1. First, verify if a studying relationship exists between the student and the course.
1. Next, verify whether a rates relation exists between the student and the course.
1. Thirdly, create the rate relation in the graph (see diagram below).
1. Publish event course-rated stream

The following diagram illustrates the interaction between Redis Graph and Redis Streams.

![](/images/blog/26352c34243590d74e4147e1f2155bac20908165-1600x1012.webp)

To bring make this functionality happen, follow the below commands:

- Filter courses by student

```python
GRAPH.QUERY xmentor "MATCH (student)-[:studying]->(course) where student.username = '$student' RETURN course"

```

- Get courses rated by user

```python
GRAPH.QUERY xmentor "MATCH (student)-[:rates]->(course) where student.username ='$student' RETURN course"

```

- Create rates relation in the graph

```python
GRAPH.QUERY xmentor "MATCH (s:Student), (c:Course) WHERE s.username = '${rating.student}' AND c.name = '${rating.course}' CREATE (s)-[:rates {rating:${rating.stars}}]->(c)"

```

- Publish event to course-rated stream

```python
XADD course-rated $timestamp student $student_username course $course 
	starts $stars

```

#### Step 9: Course search

**All**

The following commands retrieves courses by query from redisJSON with rediSearch

FT.SEARCH courses-idx ${query}*

**By ID**

BF.EXISTS courses ${course.id}

JSON.GET course:${course.id}

#### By Student

GRAPH.QUERY xmentor “MATCH (student)-[:studying]->(course) where student.username = ‘$student’ RETURN course”

FT.SEARCH courses-idx ${course.title}

#### Step 10: Student’s interests

Now we’ll show you how to allow students to filter preferred courses based on their interests. Here’s how to do it:

1. Get all of the interested relations from RedisGraph.
1. Distinguish the difference between already existing relations and new ones. This’ll allow you to separate new interests from existing ones.
1. Create new interested relations into RedisGraph
1. Remove interested relations that don’t apply anymore
1. Publish to student-interest-lost and student-interested stream

The following diagram shows the interaction between RedisGraph and Redis Streams.

![](/images/blog/08677c925b64eb41bab4ccaafcaa1b02a2fb6053-1600x1228.webp)

Below are the commands for you to follow:

- Capture all student interests

```python
GRAPH.QUERY xmentor "MATCH (student)-[:interested]->(topic) WHERE 
student.username ='$student' RETURN topic"

```

- Create interest relation

```python
GRAPH.QUERY xmentor "MATCH (s:Student), (t:Topic) WHERE s.username = 
	'${interest.student}' AND t.name = '${interest.topic}' CREATE 
(s)-[:interested]->(t)"

```

- Delete interest relation

```python
GRAPH.QUERY xmentor "MATCH (student)-[interest:interested]->(topic) WHERE student.username='${interest.student}' and topic.name='${interest.topic}' DELETE interest"

```

- Publishing to student-interested stream

```python
XADD student-interest-lost $timestamp student ${student.username} topic $topic

```

- Publishing to student-interest-lost stream

```python
XADD student-interest-lost $timestamp student ${student.username} topic $topic

```

#### Step 11: Course recommendation system

Here we’re going to show you how to create a course recommendation system that connects users with courses that are most relevant to their interests. A lot of this comes down to the advanced capabilities of RedisGraph.

Searching for relations between nodes in the graph database is the easiest way to implement the most effective recommendation strategies. Let’s have a look at how to do this.

In order for you to create a special recommendation system that matches users’ personal interests with the most relevant courses

##### How to carry out the enrolled recommendation strategy

1. Randomly select a course the student is enrolled in
1. Get the topic of the course
1. Look for students enrolled on the same course
1. Search for courses on the same topic based on the students who are currently enrolled
1. Recommend those courses

##### How to carry out the interest recommendation strategy

1. Randomly select a student’s interest
1. Look for students who are enrolled to the course of that topic
1. Search for other courses of the same topic based on the students who are currently enrolled
1. Provide the recommended courses

##### How to carry out the discover recommendation strategy

1. Get all topics
1. Identify all of the topics that the students are interested in
1. Gather all of the topics the user is enrolled in
1. Choose a topic where the user is neither interested in nor enrolled for
1. Get the courses of that chosen topic and recommend them

##### How the graph data is accessed

- All student’s courses

```python
GRAPH.QUERY xmentor "MATCH (student)-[:studying]->(course) where student.username = '$student' RETURN course"

```

- Get all topics

```python
GRAPH.QUERY xmentor "MATCH (topic:Topic) RETURN topic"

```

- Obtain topic by course

```python
GRAPH.QUERY xmentor "MATCH (topic:Topic)-[:has]->(course:Course) 

```

- Identify students who are enrolled in (studying relation) a course

```python
GRAPH.QUERY xmentor "MATCH (student)-[:studying]->(course) WHERE course.name = '$course' RETURN student"

```

- Generate courses by topic

```python
GRAPH.QUERY xmentor "MATCH (topic)-[:has]->(course) WHERE 
	topic.name = '${topic.name}' RETURN course"

```

- Uncover student’s interests

```python
GRAPH.QUERY xmentor "MATCH (student)-[:interested]->(topic) WHERE student.username ='$student' RETURN topic"

```

- Filter courses the student is enrolled in based on topic

```python
GRAPH.QUERY xmentor "MATCH (student)-[:studying]->(course), 
	(topic)-[:has]->(course) where student.username = '${student.username}'  
	and topic.name = '${topic.name}' RETURN course"

```

- Identify topics the user is enrolled in

```python
GRAPH.QUERY xmentor "MATCH (student)-[:studying]->(course), (topic)-[:has]->(course) WHERE student.username = '${student.username}' RETURN topic"

```

#### Step 12: Student progress registration

This functionality will allow you to track the amount of time users spend watching courses on the platform. That information will then be used to implement the Leaderboard.

![](/images/blog/5eed96cbe004fefec9c7aff70024aeffcc7fc3c8-1600x743.webp)

Once x-mentor-core receives the request, it will then publish the Student Progress Registration Domain Event. This will end up as an element inside student-progress-registered stream (which is a Redis Stream) via the following command:

```python
XADD student-progress-registered $timestamp student $student_username duration $duration

```

All of the data sent to RedisGears will be pushed to the stream and will then sink this data into Redis TimeSeries using the following command:

```python
TS.ADD studentprogress:$student_username $timestamp $duration RETENTION 0 LABELS student $student_username

```

#### Step 13: Leaderboard

The Leaderboard functionality enables you to have a board that displays the rankings of the top students that use X-Mentor. Students are ranked based on the amount of time they spend watching content on the platform – the more you watch, the higher you rank.

To accomplish this, you need to separate two functionalities:

- Register the student progress
- Getting the board data

![](/images/blog/7907da80d3003b9c2528d265019cbe09d58c7364-1600x860.webp)

When the user request for the leaderboard data, first look at Redis for the time series keys

```python
LRANGE student-progress-list 0 -1 // to retrieve all the list elements

```

For each key, you need to use Redis TimeSeries to get the range of samples in a time window of three months performing sum aggregation. You can use the code below to make this happen:

```python
TS.RANGE $student_key $thee_months_back_timestamp $timestamp AGGREGATION sum 1000

```

Below are additional requisites that need to be implemented for this to happen.

- student_key is the student’s time series key. For example: studentprogress:codi.sipes is the time series key for student codi.sipes.
- three_months_back_timestamp is a Unix Timestamp that represents a point in time three months back than timestamp(in order to have a time window of three months).
- timestamp the current timestamp (in Unix Timestamp format).
- Next perform a sum aggregation of the sample values in those time windows using a Time Bucket of 1000 milliseconds.

Carrying out these commands will provide you with the accumulated screen time of each student. Once you receive these rankings, you can create a ranking system based on those who have the most screen time.

## Conclusion: Empowering Learners With Redis

Being this far into the digital age, a simple prerequisite of any application is for it to operate at maximum speed. This is especially true for e-learning platforms where users are meant to be engaged with its course content for long periods of time.

A mere lag will create friction between users and the application, inhibiting its ability to connect teachers with students as well as providing value through its courses. Having Redis as the application’s main database removed this threat and helped to create a fully optimal application that catered to the user’s demands with ease.

To get a more visual insight into how this application was created, then you can watch this [YouTube video here](https://youtu.be/7k1EXPh3m4s). We also have a diverse range of applications for you to check out on the [Redis Launchpad](https://launchpad.redis.com/) that are having an impact on everyday life around the world.

So make sure to check them out!

![](/images/blog/4286535b4f0ad548b626a7e3bc36792d2aa0c568-1600x593.webp)

## Who built this application?

![](/images/blog/98e6dbe33e1f12e074c30278fa4afe98c728436c-460x460.webp)

**Sergio Cano**

Sergio is a full-stack engineer and in his own words ‘loves solving problems and learning new stuff.’

Being an enthusiastic learner, it’s not difficult to see where he got the inspiration to build this application.

Make sure to [check out his profile here](https://github.com/serdeliverance/x-mentor) and see what other projects he’s been involved in.
