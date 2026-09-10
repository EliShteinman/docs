---
title: "How to Build an App that Connects Blood Donors with Patients by Using Redis"
linkTitle: "How to Build an App that Connects Blood Donors with Patients by Using Redis"
url: "/blog/launchpad-building-zindagi-blood-donor-app/"
description: "Giving blood is an easy and safe way to save a life. Yet, complications still exist in matching donors and patients with the right blood type. Time is a limited commodity when it comes to blood..."
date: 2022-04-18
blogCategories:
- "Launchpad"
authors:
- "Redis Growth Team"
lastmod: 2025-07-03
hidden: true
mirrored: true
---

*By Redis Growth Team · Published 18 April 2022 · updated 3 July 2025*

![Blog tile image](/images/site-mirror/56642da8fd0ddb11ab6d5459228d621127f52aa2-772x550.webp)

Giving blood is an easy and safe way to save a life. Yet, complications still exist in matching donors and patients with the right blood type. Time is a limited commodity when it comes to blood donations, making it absolutely fundamental to align donors with the right patients.

The more efficient this process is, the more lives are saved. Taking on this challenge was Bhanu Korthiwada, who created a phenomenal application, Zindagi, that speeds up the entire blood donation process by matching blood donors with the ideal patients.

At the heart of this application was a fundamental need for data to be transmitted with maximum efficiency to provide users with updates in real-time. A lag or a delay would hamper the user’s experience and not keep up to speed with the fast-paced demands for blood donations.

Due to these demands, Redis was used as the application’s main database, which had a dramatic impact on performance. Data was transmitted with maximum efficiency. Users received real-time updates. And blood donations became seamless.

Let’s take a look at how Bhanu created this application. But before we examine the ins and outs of this app, we’d like to point out that we have an exciting range of other apps for you to check out on the Redis Launchpad.

So make sure to have a browse after this post!

[Click here to view video](https://www.youtube.com/embed/zHvYt8fqNrY)

## How to build an app that connects blood donors with patients

1. What will you build?
1. What will you need?
1. Architecture
1. Getting started
1. How to use the application?
1. How does it work?

## 1. What will you build?

You’ll build an application that will match blood donors with patients who have the same blood type. This will promote a more seamless and efficient blood donation process that saves time to save lives.

Below we’ll go through the A-Z of what’s required to bring this application to life, as well as highlight what components you’ll need. From start to finish, we’ll break everything down into bite-sized steps to make building this application as easy as possible.

Ready to get started?

Ok, let’s dive straight in.

## 2. What will you need?

[**RedisJSON**](/json/)**: **Implements ECMA-404, the JSON Data Interchange Standard, as a native data type.

[**RediSearch**](https://oss.redis.com/redisearch/)**: **Provides advanced querying, secondary indexing, and full-text search for Redis.

[**Redis Pub/Sub**](https://redis.io/topics/pubsub/)**: **Used for event messaging and can provide messages to any number of subscribers on a channel.

[**Telerik**](https://www.telerik.com/)**: **Provides an array of software tools for web, mobile, desktop application, development, and much more.

[**Blazor**](https://dotnet.microsoft.com/apps/aspnet/web-apps/blazor)**: **Used as a free open source web framework that allows developers to build web apps using C# and HTML.

[**.NET Core Runtime**](https://docs.microsoft.com/en-us/dotnet/core/introduction) – Provides basic services for internet-connected apps

## 3. Architecture

![](/images/site-mirror/0b496b10d86f4bf20dff3fa10045f203b411ba1c-1024x840.webp)

## 4. Getting started

#### Prerequisites

- .NET Core – v5.0.x (latest patch version)
- Visual Studio 2019 16.9 or Visual Studio Code 1.55
- Docker – v19.03.13 (optional)
- Auth0:
  - Domain
  - Client ID
  - Client Secret
- SMTP (Optional): This is an optional feature. There are multiple providers for SMTP. We can use one based on need and pricing. Below are a few of them:
  - [SendGrid by Twilio](https://docs.sendgrid.com/for-developers/sending-email/integrating-with-the-smtp-api)
  - [Amazon SES](https://aws.amazon.com/premiumsupport/knowledge-center/ses-create-smtp-credentials)
  - [Mail Jet](https://documentation.mailjet.com/hc/en-us/articles/360043229473-How-can-I-configure-my-SMTP-parameters)
  - [Mailgun](https://www.mailgun.com/email-api)
- SMS: SMS feature code is not yet implemented. However, it is planned. Below are some of popular providers:
  1. [Msg91](https://msg91.com/transactional-sms)
  1. [Twilio](https://www.twilio.com/sms)

#### Setting up a local installation using the docker

**Prerequisite**

- Docker
- Docker Compose

#### Step 1. Clone the repo:

```javascript
git clone https://github.com/redis-developer/rediszindagi
```

Update .env file with Auth0 and SMTP details

#### Step 2. Examining the Docker Compose file

```python
version: '3.7'

services:
  redismod:
    image: redis/redis-stack:latest
    container_name: redis
    restart: unless-stopped
    environment:
      EMAIL: zindagi@bhanu.dev
    volumes:
      - ./persistence/redismod/data:/data
    networks:
      - default
    ports:
      - 6379:6379

  rediszindagi:
    image: ghcr.io/bhanukorthiwada/rediszindagi:latest
    container_name: zindagi
    restart: unless-stopped
    environment:
      ASPNETCORE_ENVIRONMENT: ${APP_ENV}
      AUTH0__DOMAIN: ${APP_AUTH0_DOMAIN}
      AUTH0__CLIENTID: ${APP_AUTH0_CLIENTID}
      AUTH0__CLIENTSECRET: ${APP_AUTH0_CLIENTSECRET}
      SMTP__DISABLE: ${APP_SMTP_DISABLE}
      SMTP__FROM: ${APP_SMTP_FROM}
      SMTP__HOST: ${APP_SMTP_HOST}
      SMTP__PORT: ${APP_SMTP_PORT}
      SMTP__USERNAME: ${APP_SMTP_USERNAME}
      SMTP__PASSWORD: ${APP_SMTP_PASSWORD}
      SMTP__USESSL: ${APP_SMTP_USESSL}
      CONNECTIONSTRINGS__REDIS: ${APP_REDIS_CONNECTIONSTRING}
    volumes:
      - ./persistence/zindagi/logs:/app/logs
    networks:
      - default
    ports:
      - 80:80
    depends_on:
      - redismod

networks:
  default:
    name: network_default
    driver: bridge

```

The above Compose file defines two basic services:

- Redismod
- rediszindagi.

Redismod has in-built modules like RedisJSON and RediSearch that are used for this project. You’ll need to pass a number of auth0 environmental variables. SMTP remains optional. For persistence, Docker volumes mount has been added and the app is exposed to port 80.

From terminal/command prompt run docker-compose up -d

The application can be accessed using localhost.

## 5. How data is stored

- The request data is stored in various keys and various data types.
  - For each of the requests:
    - ID: Guid as a string
    - Blood Group, Donation Type, Priority, Status: C# ENUM
- Redis JSON
  - User Profile Key: prefix: USER_PROFILE postfix: Auth0 name identifier
  - Request Key: prefix: BLOOD_REQUEST postfix: Guid string
- Redis Publish:
  - Requests: Any new blood request will publish request id as a message to topic URN:BLOODREQUESTS:NEW

### How the data is accessed:

- C# Repository pattern is used, every call will create an instance using Connection Multiplexer

## 6. How to use the application

### Creating an account or logging in

To get the full benefits of the application, blood donors have to create an account. You can do this on the main dashboard by clicking on ‘Register Now.’

### Giving a blood donation

Click on the blood donation button at the top of the navigation bar. You’ll then have a number of fields to fill in that will inform the database about your blood type and the quantity you want to donate.

### Receiving a request for a blood donation

Once you’ve created an account, patients who are the right fit for your blood donation will be notified of your availability. They’ll then be able to send you a request for your blood donation. To access your full list of requests, click on the ‘Requests’ tab at the top of the navigation bar. Here you’ll have a complete overview of all the requests patients have sent for your donation.

## Conclusion: Bridging patients with blood donors to save lives through Redis

Fast access to blood is the difference between life and death for many patients. Matching donors with the right patients is often a time-consuming process, where every second jeopardizes the patient. Bhanu’s application helps to remove this obstacle through Redis’ ability to send data between components at lightning-fast speed.

Having data transmitted with such efficiency allows Zindagi to quickly match blood donors with the right patients based on the given criteria. This accelerates the entire blood donation process, enabling donors and patients to interact with each other in real-time and arrange a possible blood donation.

At the heart of this application is an ability to pull all parties together, providing the optimum direction for progress. This means more donations, less time wasted, and a totally seamless experience for everyone involved.

To get more of a visual insight into how this application works, check out this [YouTube video](https://www.youtube.com/watch?v=zHvYt8fqNrY). If you enjoyed this post, make sure to check out the [Redis Launchpad](https://launchpad.redis.com/) where you’ll have access to a wide variety of innovative applications that are having an impact on everyday life.

We have applications that track buses in real-time on a map. We have applications that prevent supply shortages in hospitals in developing nations. And we have *so much more* for you to discover.

So make sure to check them out!

[Watch the video](https://launchpad.redis.com/)

## Who created the app?

**Bhanu Korthiwada**

![](/images/site-mirror/c94789d9af4ddb9fec4a6d8e16c31bf53c7d44f6-736x736.webp)

Bhanu is an experienced software engineer who’s currently working as a senior consultant for ADP. If you want to keep up to date with all of his latest projects, make sure to follow him on [GitHub](https://github.com/bhanudev-org).
