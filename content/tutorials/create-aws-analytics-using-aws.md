---
title: "How to Build and Deploy Your Own Analytics Dashboard using NodeJS and Redis on the AWS Platform"
linkTitle: "How to Build and Deploy Your Own Analytics Dashboard using NodeJS and Redis on the AWS Platform"
url: "/tutorials/create/aws/analytics-using-aws/"
description: "An interactive analytics dashboard serves several purposes. They allow you to share data and provide you with all those vital information to make game-changing decisions at a faster pace. Building..."
group: "For developers"
aliases:
- "/tutorials/create-aws-analytics-using-aws/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> Build and deploy a real-time analytics dashboard on AWS using Node.js and Redis Bitmaps. Clone the sample app, connect it to a Redis Cloud database on AWS, and visualize traffic, sales, and user engagement metrics through an interactive dashboard.

An interactive analytics dashboard serves several purposes. They allow you to share data and provide you with all those vital information to make game-changing decisions at a faster pace. Building a real-time dynamic dashboard using a traditional relational database might require a complex set of queries. By using a NoSQL database like Redis, you can build a powerful interactive and dynamic dashboard with a small number of Redis commands.

## What you'll learn

- How to set up a Redis Cloud database on AWS
- How to use Redis Bitmaps, Sets, and Strings to model analytics events
- How to track page views, traffic sources, and product purchases
- How to calculate cohort and retention metrics with Redis
- How to deploy a Node.js analytics dashboard backed by Redis

## Prerequisites

- [Node.js](https://nodejs.org/) v12.19.0 or later
- [NPM](https://www.npmjs.com/) v6.14.8 or later
- A [Redis Cloud](https://redis.io/try-free/) account (free tier available)
- An AWS account (Redis Cloud subscription uses AWS as the cloud vendor)
- Basic familiarity with JavaScript and the command line

## Getting started

### Step 1. Sign up for a free Redis Cloud account

[Sign up for a free Redis Cloud account](https://redis.io/try-free/) and choose AWS as your cloud vendor when creating a new subscription. At the end of the database creation process, you will get a Redis Cloud database endpoint and password. Save these for later use.

### Step 2. Clone the repository

```bash
git clone https://github.com/redis-developer/basic-analytics-dashboard-redis-bitmaps-nodejs
```

### Step 3. Set up the backend environment

First, set up the environment variables. Go to the `/server` folder and copy the example env file:

```bash
cd ./server
cp .env.example .env
```

Open the `.env` file and add your Redis Cloud database endpoint URL, port, and password:

```bash
PORT=3000

# Host and a port. Can be with `redis://` or without.
# Host and a port encoded in redis uri take precedence over other environment variable.
# preferable
REDIS_ENDPOINT_URI=redis://redis-XXXX.c212.ap-south-1-1.ec2.cloud.redislabs.com:15564

# Or you can set it here (ie. for docker development)
REDIS_HOST=redis-XXXX.c212.ap-south-1-1.ec2.cloud.redislabs.com
REDIS_PORT=XXXX

# You can set password here
REDIS_PASSWORD=reXXX

COMPOSE_PROJECT_NAME=redis-analytics-bitmaps
```

### Step 4. Install backend dependencies

```bash
npm install
```

### Step 5. Run the backend

```bash
npm run dev
```

### Step 6. Set up the frontend environment

Go to the `client` folder and copy the example env file:

```bash
cd ./client
cp .env.example .env
```

Add the API URL for your backend:

```bash
VUE_APP_API_URL=http://localhost:3000
```

### Step 7. Install frontend dependencies

```bash
npm install
```

### Step 8. Run the frontend

```bash
npm run serve
```

![Interactive analytics dashboard UI showing traffic metrics, sales data, and user engagement charts built with Node.js and Redis on AWS](images/inline-1-722c47bdd6c16760bdb5c44634680f4868106820-1047x387.jpg)

## How does the analytics data model work?

The event data is stored in various Redis keys and data types. The key design uses a combination of time spans, scopes, and data types to organize analytics events efficiently.

### Time spans

- **year:** e.g. `2021`
- **month:** e.g. `2021-03` (March 2021)
- **day:** e.g. `2021-03-03` (3rd March 2021)
- **weekOfMonth:** e.g. `2021-03/4` (4th week of March 2021)
- **anytime**

### Scopes

- source
- action
- source + action
- action + page
- userId + action
- global

### Data types used

- **count** — Integer stored as a String, incremented with `INCR`
- **bitmap** — Bit array tracking individual user actions with `SETBIT`
- **set** — Collection of unique user IDs tracked with `SADD`

### Key naming convention

Keys follow this pattern:

```bash
rab:{type}[:custom:{customName}][:user:{userId}][:source:{source}][:action:{action}][:page:{page}]:timeSpan:{timeSpan}
```

Values in `[]` are optional.

### How are analytics events stored in Redis?

For each generated key like `rab:count:*`, data is stored with `INCR`:

```bash
INCR rab:count:action:addToCart:timeSpan:2015-12/3
```

For each generated key like `rab:set:*`, data is stored with `SADD`:

```bash
SADD rab:set:action:addToCart:timeSpan:2015-12/3 8
```

For each generated key like `rab:bitmap:*`, data is stored with `SETBIT`:

```bash
SETBIT rab:bitmap:action:addToCart:timeSpan:2015-12/3 8 1
```

## How does cohort tracking work with Redis?

Cohort data tracks users who register and then buy products (the action order matters). For each buy action in December, the app checks whether the user previously performed a register action (register counter must be greater than zero). If so, the user's bit is set to 1:

```bash
SETBIT rab:bitmap:custom:cohort-buy:timeSpan:{timeSpan} {userId} 1
```

For example:

- User ID 2 bought 2 products on 2015-12-17 but never registered. This is **not** stored.
- User ID 10 bought 1 product on 2015-12-17 and registered on 2015-12-16. This **is** stored:

```bash
SETBIT rab:bitmap:custom:cohort-buy:timeSpan:2015-12 10 1
```

The app assumes that a user cannot buy without registering first.

## How does retention tracking work?

Retention means users who bought on two different dates. For each buy action, the app checks if the user bought more products anytime than on the current particular day (excluding the current purchase). If so, the user ID is added to a set:

```bash
SADD rab:set:custom:retention-buy:timeSpan:{timeSpan} {userId}
```

For example:

- User ID 5 bought 3 products on 2015-12-15. Retention is **not** stored (products bought on that day: 2, products bought anytime before: 0).
- User ID 3 bought 1 product on 2015-12-15 and previously bought 1 product on 2015-12-13. Retention **is** stored (products bought on that day: 0, products bought anytime before: 1):

```bash
SADD rab:set:custom:retention-buy:timeSpan:2015-12 3
```

## How is the analytics data queried?

### Total traffic

Query total unique visitors for December:

```bash
BITCOUNT rab:bitmap:custom:global:timeSpan:2015-12
```

Query a specific week of December (e.g. week 3):

```bash
BITCOUNT rab:bitmap:custom:global:timeSpan:2015-12/3
```

### Traffic per page

Pages include: `homepage`, `product1`, `product2`, `product3`.

December traffic for a specific page:

```bash
BITCOUNT rab:bitmap:action:visit:page:homepage:timeSpan:2015-12
```

A specific week of December for a page:

```bash
BITCOUNT rab:bitmap:action:visit:page:product1:timeSpan:2015-12/2
```

### Traffic per source

Sources include: `Google`, `Facebook`, `email`, `direct`, `referral`, `none`.

December traffic from a source:

```bash
BITCOUNT rab:bitmap:source:referral:timeSpan:2015-12
```

A specific week of December from a source:

```bash
BITCOUNT rab:bitmap:source:google:timeSpan:2015-12/1
```

### Trend traffic

To get daily traffic trends, run `BITCOUNT` across each day in the range. For example, for the 5th week of December:

```bash
BITCOUNT rab:bitmap:action:visit:homepage:timeSpan:2015-12-29
BITCOUNT rab:bitmap:action:visit:homepage:timeSpan:2015-12-30
BITCOUNT rab:bitmap:action:visit:homepage:timeSpan:2015-12-31
```

Weekly ranges:

- 1st week: 2015-12-01 to 2015-12-07
- 2nd week: 2015-12-08 to 2015-12-14
- 3rd week: 2015-12-15 to 2015-12-21
- 4th week: 2015-12-22 to 2015-12-28
- 5th week: 2015-12-29 to 2015-12-31

### Total products bought

December total:

```bash
GET rab:count:action:buy:timeSpan:2015-12
```

A specific week (e.g. week 1):

```bash
GET rab:count:action:buy:timeSpan:2015-12/1
```

## Next steps

- Explore the [Redis Bitmaps documentation](https://redis.io/docs/latest/develop/data-types/bitmaps/) to learn more about bit-level operations
- Try adding new metrics like session duration or conversion funnels using Redis Sorted Sets
- Deploy the dashboard to production on AWS using Elastic Beanstalk or ECS
- Connect your dashboard to live data sources by integrating Redis Pub/Sub for real-time event streaming
- Check out the [Redis Cloud on AWS](https://redis.io/cloud/aws/) page for production deployment options
