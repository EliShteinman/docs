---
title: "How to Build an App That Will Tackle Social Issues by Using Redis"
linkTitle: "How to Build an App That Will Tackle Social Issues by Using Redis"
url: "/blog/how-to-build-social-issues-app/"
description: "An injured animal. A tipped trash can. And a polluted hotspot. Most of us are likely to have come across one of these in our local community. But knowing how to react quickly to these scenarios can..."
date: 2022-01-05
blogCategories:
- "How To and Tutorials"
- "Tech"
authors:
- "Growth Team"
lastmod: 2026-09-01
hidden: true
mirrored: true
---

*By Growth Team · Published 5 January 2022 · updated 1 September 2026*

![Blog tile image](/images/site-mirror/4f661945fe0185c33e762b8036ff3513ec07a7a0-772x550.webp)

An injured animal. A tipped trash can. And a polluted hotspot. Most of us are likely to have come across one of these in our local community. But knowing how to react quickly to these scenarios can be a challenge. Who do I contact? What’s the process for reporting a health hazard? How much time will this take out of my day?

Not knowing the answer to any of these questions could be the difference between action and inaction. What it boils down to is that community *is everything, *and if we’re able to report community issues with ease then we could promote a healthier, safer, and greener planet.

Taking on this challenge is Bryon Rosas Salguero. Through his innovative application, [Helplanet](https://launchpad.redis.com/?id=project%3Ahelplanet), individuals can instantly report local risks or accidents from just a few taps on their phone. But for this application to function, data had to be transmitted in real time to keep up with events that were happening in real life.

Redis was crucial to achieving this and it enabled Byron’s innovations to come to life. Let’s take a look at how he was able to put this app together. But before we get down to the nitty gritty of it all, we’d like to let you know that we have a diverse range of interesting applications for you to check out on the [Redis Launchpad](https://launchpad.redis.com/).

So don’t forget to check them out after this post!

[Click here to view video](https://www.youtube.com/embed/N5fb9rP8hqM)

1. What will you build?
1. What will you need?
1. Architecture
1. Getting started
1. Using the Redis commands
1. How the application works

## 1. What will you build?

You’ll build an application that allows people to report social issues in their community. These can include:

- An injured animal
- Contamination and pollution
- Neglected garbage and trash cans
- Vandalism
- Crime

Below we’re going to walk you through each step of the application building process and highlight the components you’ll need along with their functionality.

Ready to get started? Ok, let’s dive straight in.

## 2. What will you need?

- [**Angular**](https://angular.io/)**: **used as a platform and framework for building single-page client applications using HTML and TypeScript.
- [**SocketIO**](https://socket.io/)**:**
- [**Ionic**](https://ionicframework.com/)**: **used as a collection of UI components and native APIs that allow users to build iOS, Android and Progressive Web Apps under one shared codebase.
- [**Bootstrap**](https://getbootstrap.com/)**: **used as an open source front end development framework for building websites and apps.
- [**Leaflet**](https://leafletjs.com/)**: **used as a JavaScript library for interactive maps
- [**Node.js**](https://nodejs.org/en/)**: **used as an open-source, cross-platform that executes JavaScript code outside a web browser.
- [**Redis Streams**](https://redis.io/docs/latest/develop/)**: **manages data consumption from cord-19 and transmits data to RedisGears
- [**RediSearch**](/search/)**: **provides querying, secondary indexing, and full-text search for Redis

## 3. Architecture

![](/images/site-mirror/f5ee659cb2ca14a0b77940cc7574524ba29495c6-1600x990.webp)

### Reporting an issue on the app

- User sends a message on the Helplanet app via their mobile device.
- Redis Streams manages the data consumption and transmits data to the organization dashboard.
- The organization receives a notification in real time.
- Both the organization and the user will then be connected via a chat window that operates just like Facebook Messenger.

### Searching for issues on the Helplanet dashboard

- Organizations can enter a query in the Helplanet search engine based on the social issue they wish to tackle first.
- This query is then processed by RediSearch which carries out a full-text search.
- RediSearch filters the most relevant results.
- The organization can then choose which user to send messages to.

## 4. Getting started

### Prerequisites

- Node.js: (v14.16.1)
- NPM: (v7.11.2)
- Docker: (v20.10.2)
- Redis: (v6.0.1)

#### Step 1: Clone the repository

Clone this project or download as zip

```python
git clone https://github.com/byronrosas/helplanet.git

```

#### Step 2: Setting up local installation

Exec redis ([https://github.com/RedisLabsModules/redismod](https://github.com/RedisLabsModules/redismod))

```python
docker run -p 6379:6379 --name myredis  redislabs/redismod

```

```python
sudo docker start myredis

```

#### Step 3. Install dependencies (for server, helplanet mobile app and helplanet-support)

```python
cd helplanet/server

```

```python
npm install

```

#### Step 4. Install the ionic CLI package globally

```python
cd help-planet
npm install
npm install -g @ionic/cli
npm install @ionic-native/core@4 --save

```

#### Step 5. Install Angular CLI globally

```python
cd helplanet-support
npm install
npm install -g @angular/cli

```

(Open three terminals)

First start server (start services) with this commands:

- PORT => 3006 (dataserver notification-service)
- PORT => 3001 (dataserver session-service)
- PORT => 3002 (dataserver organization-service)
- POST => 3003 (dataserver report-service)

```python
cd ..
cd server
npm run build
npm run dev

```

Second start ionic app ([http://localhost:8100](http://localhost:8100/))

```python
cd help-planet
ionic serve

```

Third start web angular app ([http://localhost:4200](http://localhost:4200/))

```python
cd helplanet-support
ng serve

```

## 5. Using the RediSearch commands

Below are the RediSearch CLI commands for each of the services

**Redis utils**

- Removing index for users

```python
FT.DROPINDEX usersIdx

```

- Removing index for notifications

```python
FT.DROPINDEX notificationsIdx

```

- Adding a secondary index for users

```python
FT.CREATE usersIdx ON HASH PREFIX 1 hpa:users: SCHEMA username TEXT password TEXT email TAG status NUMERIC role NUMERIC

```

- Adding a secondary index for notifications

```python
FT.CREATE notificationsIdx ON HASH PREFIX 1 hpa:notifications: SCHEMA geo GEO userId TAG userOrg TAG

```

- For token utils (SET)

```python
SET hpa:session:byron@hotmail.com "xyaszTOKENsdsjlvj" EX 24*60*60

```

- For token utils (DEL)

```python
DEL hpa:session:byron@hotmail.com

```

- For token utils (GET)

```python
GET hpa:session:byron@hotmail.com

```

### Notification Repository

- Saving a new notification: Add data on hash

```python
HSET "hpa:notifications:1621188142413-0" userId "byron@reporter.com" level "0" text "trash" situation "garbage" geo "-78.62285039999999,-1.2543408"

```

And

```python
EXPIRE "hpa:notifications:1621188142413-0" 172800

```

- Attend Cancel

```python
HDEL "hpa:notifications:1621188142413-0" userOrg dateAttention

```

- Attend Notification

```python
HSET "hpa:notifications:1621188142413-0" userId "byron@reporter.com" level "0" text "trash" situation "garbage" geo "-78.62285039999999,-1.2543408" serOrg x@hotmail.com dateAttention new Date()

```

- Remove notification

```python
DEL "hpa:notifications:1621188142413-0"

```

- Get All (Notifications with pagination)

```python
FT.SEARCH notificationsIdx * LIMIT 0 10

```

- Get All By User(Notifications)

```python
FT.SEARCH notificationsIdx @userId:{email/@hotmail/.com} LIMIT 0 10

```

- Add Stream (Notification data):

```python
XADD hpa:report MAXLEN 30 * userId "user@x.com" level "0" situation "garbage" lat "-7.54545" lon "-0.4545" text "trash"

```

- List Streams

```python
XRANGE hpa:report 1621188142413 1621188142413

```

- Get One Stream

```python
XRANGE hpa:report 1621188142413-0 + COUNT 1

```

- Get One (Notification)

```python
HGETALL "hpa:notifications:1621188142413-0"

```

- Get Near (Notifications):

```python
FT.SEARCH notificationsIdx @geo:[ "-0.4545" "-7.54545"  15 m]

```

### User Repository

- Save User

```python
HSET hpa:users:byron@hotmail.com username "byronman" password "encryptpassword" email "byron@hotmail.com" role "0"

```

- Get By Email (Users)

```python
FT.SEARCH usersIdx @email:{email@x.com}

```

- Get By Id (Users):

```python
HGETALL hpa:users:byron@hotmail.com

```

- Update By Email

```python
HSET hpa:users:byron@hotmail.com username "byronman" password "encryptpassword" email "byron@hotmail.com" role "0"

```

- Get By Email (Users):

```python
FT.SEARCH usersIdx @email:{email@x.com}

```

- Get All Users (Users with pagination):

```python
FT.SEARCH  * LIMIT 0 10

```

### Socket service

- Send new report (send data through io socket)

### Index (Notification Service)

- Listen reports (Real time):

```python
XREAD COUNT 1 BLOCK 5000 STREAMS hpa:report $

```

Middleware is also used for each of the routes:

- isAuth (verifies that the user has a valid token and is authorized to access all services )
- isUserReport (verifies that the user has the role of reporter )
- isUserOrganization (verifies that the user has the role of organization)
- isAdmin (verifies that the user has the role of administrator )

## 6. How the application works

### How users can use the app

If somebody comes across a hazard or a social concern in their community, they can report it via the Helplanet application. Users simply have to open the app and they’ll then be faced with a number of options (see below).

![](/images/site-mirror/8eb3b295f477a46cced3b6f1a6265fd54cd36615-470x770.webp)

The user will then select the option that best describes the issue or concern they’ve come across. Much like Facebook Messenger, a chat will appear where they’ll be able to provide more detail about the incident they’re reporting (see below).

**Note:** Everything will be reported in real time thanks to Redis.

![](/images/site-mirror/a96032e23bac3f0226e07b27c22e648fe703a10e-470x770.webp)

### How organizations can use the app

The organization will receive notifications from all incidents that have been reported by members of the public. They’ll be able to gain a holistic view of all reported incidents on their dashboard (see below).

![](/images/site-mirror/c1e79ab1ad4f5a7d890a89866c6f1098c82dbe04-1600x794.webp)

From here, an organization can select an incident and view it in more detail. The information that will be provided about the incident will include:

- Location
- Date and time
- Incident type
- Whether it’s being attended to or not
- Chat history with users

Organizations can filter everything based on location. This will allow them to get a quick insight as to where every instant is on the map (see below).

![](/images/site-mirror/43d509413cc28af9374f34d8fd60952bfa5237c8-1600x731.webp)

An organization can also view a user’s personal details if they want to get in touch with them in a different form of communication e.g email (see below).

![](/images/site-mirror/abf07356afa3da4ea31941bb380515df847a84ac-1600x731.webp)

## Conclusion: Bringing communities together by tackling social issues with Redis

Society thrives on individuals who bear the responsibility of reporting issues that pose a threat to their local community. But with so many different organizations and professionals to contact, the entire reporting process can be just as unclear as tedious.

Byron’s application was able to eliminate these barriers by creating a powerful application that made the entire process easy and simple. Yet for this app to function effectively and promote a seamless experience, data needed to be transmitted in real time.

Thanks to Redis, components in the application’s architecture became more interconnected where data transmission was both seamless and hyper-efficient.

If you want to discover more about how Helplanet was created, then make sure to watch the [YouTube video here](https://youtu.be/N5fb9rP8hqM).

We also have a variety of other breakthrough applications that you can check out on the [Redis Launchpad](https://launchpad.redis.com/). Here you’ll get an insight into how Redis can be used to create exciting apps that are having an impact on everyday life around the world.

So what can you build with Redis?

[Watch the video](https://launchpad.redis.com/)

## Who built this app?

### Byron Rosas Salguero

Byron is a highly innovative software engineer who works independently as a freelancer. Make sure to keep up to date with all of his activity by visiting his [GitHub page](https://github.com/byronrosas).
