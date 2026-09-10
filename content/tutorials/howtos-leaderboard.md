---
title: "How to build a Real-Time Leaderboard app Using Redis"
linkTitle: "How to build a Real-Time Leaderboard app Using Redis"
url: "/tutorials/howtos/leaderboard/"
description: "The concept of a leaderboard—a scoreboard showing the ranked names and current scores of the leading competitors—is essential to the world of computer gaming, but leaderboards are now about more..."
group: "For developers"
aliases:
- "/tutorials/howtos-leaderboard/"
date: 2026-02-25
lastmod: 2026-02-25
hidden: true
---

*Published 25 February 2026*

> **TL;DR:**
>
> Use Redis Sorted Sets to build a real-time leaderboard. Store scores with `ZADD`, retrieve rankings with `ZREVRANGE`, and look up a player's rank with `ZREVRANK`. Redis handles millions of score updates per second with O(log N) complexity, making it the go-to data store for ranking systems.

## What you'll learn

- Why Redis Sorted Sets are the best fit for real-time leaderboards
- How to store and update player scores with `ZADD` and `ZINCRBY`
- How to query rankings, top-N lists, and score ranges with `ZREVRANGE`, `ZRANK`, and `ZCOUNT`
- How to run a complete leaderboard demo application with Docker

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose installed
- Basic familiarity with Redis commands
- Java JDK and Gradle (for running the backend outside Docker)

## Why use Redis for leaderboards?

The concept of a leaderboard—a scoreboard showing the ranked names and current scores of the leading competitors—is essential to the world of computer gaming, but leaderboards are now about more than just games. They are about gamification, a broader implementation that can include any group of people with a common goal (coworkers, students, sales groups, fitness groups, volunteers, and so on).

Leaderboards can encourage healthy competition in a group by openly displaying the current ranking of each group member. They also provide a clear way to view the ongoing achievements of the entire team as members move towards a goal.

Redis Sorted Sets are purpose-built for this use case. Every member in a sorted set is associated with a floating-point score, and Redis keeps the set ordered by score at all times. This gives you:

- **O(log N) inserts and updates** — adding or changing a score is nearly instant, even with millions of entries.
- **O(log N + M) range queries** — fetching the top 10, bottom 10, or any slice of the leaderboard is fast regardless of total size.
- **Atomic score increments** — `ZINCRBY` lets you adjust scores without read-modify-write race conditions.
- **Built-in ranking** — `ZREVRANK` returns a player's position without scanning the entire set.

These properties make Redis the go-to choice for real-time ranking systems in multiplayer games, sales dashboards, fitness apps, and anywhere else you need live standings.

![Illustration of a real-time leaderboard application built with Redis showing ranked player scores](/images/site-mirror/601a33cf050d33c872fd7fd4776faea2b5e5db30-2000x1095.webp)

## How do you set up the leaderboard project?

### Step 1. Clone the repository

```bash
git clone https://github.com/redis-developer/basic-redis-leaderboard-demo-java
```

### Step 2. Run Docker Compose

```bash
docker network create global
docker-compose up -d --build
```

### Step 3. Verify the containers are running

```bash
 docker-compose ps
            Name                           Command               State             Ports
--------------------------------------------------------------------------------------------------
redis.redisleaderboard.docker   docker-entrypoint.sh redis ...   Up      127.0.0.1:55000->6379/tcp
```

### Step 4. Configure environment variables

Copy `.env.example` to create `.env` and provide the values for your environment:

```bash
REDIS_URL=
REDIS_HOST=redis://localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=
```

If you're using Redis Cloud, supply the database endpoint, password, port, and database name instead.

## How do you build and run the backend?

### Step 5. Install dependencies

- Install Gradle by following the [official Gradle installation guide](https://gradle.org/install/).
- Install JDK by following the [Oracle JDK installation guide](https://docs.oracle.com/javase/10/install/installation-jdk-and-jre-macos.htm).

Load the environment variables:

```bash
export $(cat .env | xargs)
```

### Step 6. Generate the Gradle wrapper

```bash
gradle wrapper
```

Expected output:

```bash
Welcome to Gradle 6.8.3!

Here are the highlights of this release:
 - Faster Kotlin DSL script compilation
 - Vendor selection for Java toolchains
 - Convenient execution of tasks in composite builds
 - Consistent dependency resolution

For more details see https://docs.gradle.org/6.8.3/release-notes.html

Starting a Gradle Daemon (subsequent builds will be faster)

BUILD SUCCESSFUL in 29s
1 actionable task: 1 executed
```

### Step 7. Build the project

```bash
./gradlew build
```

### Step 8. Run the application

```bash
./gradlew run
```

Once the Spring Boot application starts, you can access the leaderboard at `http://localhost:5000`.

![Screenshot of the real-time leaderboard application showing company rankings by market cap](/images/site-mirror/601a33cf050d33c872fd7fd4776faea2b5e5db30-2000x1095.webp)

## How does the Redis data model work?

### How is leaderboard data stored?

Company details like market cap and country are stored in a Redis Hash:

```bash
HSET "company:AAPL" symbol "AAPL" market_cap "2600000000000" country USA
```

Rankings are maintained in a Sorted Set where the score represents the market cap:

```bash
ZADD companyLeaderboard 2600000000000 company:AAPL
```

### How do you query the leaderboard?

Top 10 companies:

```bash
ZREVRANGE companyLeaderboard 0 9 WITHSCORES
```

All companies:

```bash
ZREVRANGE companyLeaderboard 0 -1 WITHSCORES
```

Bottom 10 companies:

```bash
ZRANGE companyLeaderboard 0 9 WITHSCORES
```

Between rank 10 and 15:

```bash
ZREVRANGE companyLeaderboard 9 14 WITHSCORES
```

Show ranks of specific companies:

```bash
ZREVRANGE companyLeaderBoard company:AAPL company:FB company:TSLA
```

### How do you update scores in real time?

Adding 1 billion to a company's market cap:

```bash
ZINCRBY companyLeaderBoard 1000000000 "company:FB"
```

Reducing 1 billion from a company's market cap:

```bash
ZINCRBY companyLeaderBoard -1000000000 "company:FB"
```

### How do you filter by score range?

Companies between 500 billion and 1 trillion:

```bash
ZCOUNT companyLeaderBoard 500000000000 1000000000000
```

Companies over a trillion:

```bash
ZCOUNT companyLeaderBoard 1000000000000 +inf
```

## Next steps

- **Unreal Engine integration** — Learn how to connect a Redis leaderboard to a game engine in [Creating a Real-time Leaderboard with UE5 and Redis](/tutorials/howtos/create-a-leaderboard-with-redis-and-ue5/).
- **Try other languages** — The same leaderboard pattern works across stacks:
    - [Node.js leaderboard demo](https://github.com/redis-developer/basic-redis-leaderboard-demo-nodejs)
    - [Ruby leaderboard demo](https://github.com/redis-developer/basic-redis-leaderboard-demo-ruby)
    - [Python leaderboard demo](https://github.com/redis-developer/basic-redis-leaderboard-demo-python)
    - [.NET leaderboard demo](https://github.com/redis-developer/basic-redis-leaderboard-demo-dotnet)
    - [Go leaderboard demo](https://github.com/redis-developer/basic-redis-leaderboard-demo-go)
- **Learn more about Sorted Sets** — See the [Redis Sorted Sets documentation](https://redis.io/docs/latest/develop/data-types/sorted-sets/) for the full command reference.
