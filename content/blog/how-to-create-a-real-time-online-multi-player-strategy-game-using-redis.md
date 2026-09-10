---
title: "How to Create a Real-Time Online Multi-Player Strategy Game Using Redis"
linkTitle: "How to Create a Real-Time Online Multi-Player Strategy Game Using Redis"
url: "/blog/how-to-create-a-real-time-online-multi-player-strategy-game-using-redis/"
description: "Multiplayer gaming remains colossal in the gaming industry. And why wouldn’t it be? To settle old scores, solve disputes, or even satisfy that competitive itch , battling it out online against..."
date: 2021-12-23
blogCategories:
- "How To and Tutorials"
- "Tech"
- "Uncategorized"
authors:
- "Growth Team"
lastmod: 2025-03-04
hidden: true
mirrored: true
---

*By Growth Team · Published 23 December 2021 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/ded7b5a6b9b2f66bafff3d79fee39b96cfe5b595-772x550.webp)

Multiplayer gaming remains colossal in the gaming industry. And why wouldn’t it be? To settle old scores, solve disputes, or even satisfy that competitive itch , battling it out online against other users is just as cathartic as it is entertaining.

This is why [this Launchpad app](https://www.youtube.com/watch?v=xVbdLyBARvA) has created its own real time strategy game, *Pizza Tribes*, that involves…wait for it… *mice*! The gameplay involves training a population of mice to bake and sell pizzas for coins, with the overarching objective being to generate more coins than any other player.

For all its creativity, this application wouldn’t be able to provide users with real time gameplay without Redis’ ability to transmit data between components efficiently. Any delays would have made real time gameplay impossible.

Let’s take a look at how this application was created. But before we go any further, we’d like to point out that we have an excellent range of applications that are having an impact on everyday life for you to[ check out on the Redis Launchpad](https://launchpad.redis.com/).

[Click here to view video](https://www.youtube.com/embed/_yhE_bhmF-g)

1. What will you build?
1. What will you need?
1. Architecture
1. Getting started
1. The game state update

## 1. What will you build?

You’ll build a multiplayer browser-based real time strategy game using Redis. Below we’ll go through each step in chronological order and outline all of the components that you’ll need to create this application.

Ready to get started? Ok, let’s dive straight in.

![](/images/site-mirror/6d7ea4fd82897055f2b883854e63fc17aa4acee0-816x1006.webp)

## 2. What will you need?

- [**Typescript**](https://www.typescriptlang.org/)**:** used as a superset of the JavaScript language
- [**Golang**](https://golang.org/)**: **the preferred programming language used to build efficient software
- [**RedisTimeSeries**](https://oss.redis.com/redistimeseries/)**: **provides time series data
- [**RedisJSON**](https://oss.redis.com/redisjson/)**: **stores, updates, and fetches JSON values from Redis keys

## 3. Architecture

![](/images/site-mirror/0f664e8bb26a72d0be79c8ece668ac388a30768f-1468x1396.webp)

The application has an unconventional approach when it comes to client-server communication. This is because it relies heavily on web sockets to carry out responsibilities that would normally be fulfilled by an HTTP request/response.

Below is an example of a typical web-socket flow:

1. The *Web App* sends commands over the Web socket
1. The *Web API* enqueues the command on a Redis queue *wsin* (RPUSH)
1. A *Worker*
  1. Pulls the command from the Redis queue *wsin *(BLPop)
  1. Executes the command
  1. May push a response to another Redis queue *wsout* (RPUSH)
1. The *Web API*
  1. Pulls a response from the Redis queue *wsout* (BLPOP)
  1. Sends the response back to the corresponding Web socket

### Web sockets

Since this application is reliant on Web-Sockets, we’re going to spend a bit more time going over the role that they play. Firstly, web socket communication relies heavily on Redis to send and retrieve messages.

The API does not do any game logic but simply validates client messages before pushing them to Redis. Meanwhile, the workers can be horizontally scaled whilst relying on Redis to push messages efficiently through the system.

Since Web Socket bidirectional lightweight communication protocol over a single TCP connection, it is not easy to scale the Web API (holding the sockets).

This solution attempts to minimize load on the Web API so that it can focus on shoveling data to the clients.
**Note: **messages are not sent between the API and workers using Redis Pub/Sub. Instead, Redis lists (RPush and BLPop) are used. One of the advantages of this is that the workers or the API can be restarted without losing messages, whereas with Redis Pub/Sub everything will be forgotten.

### Updater (Delayed Tasks)

The worker will need to delay some tasks (e.g., finish construction of the building after 5 minutes). This is accomplished by carrying out updates to the Sorted set *user_updates*. The updater then pulls the top record of the sorted set which is determined by time. If the time has passed, it will remove the record from the set and will then update the game state of that user.

Below is a simplified typical flow:

1. The *Web App* sends the command to start the construction of a building
1. A *worker* processes the command by carrying out a number of commands

i. Validates the command

ii. Updates the user game state:

```python
JSON.ARRAPPEND user:$user_id:gamestate .constructionQueue $constructionItem

```

iii. Discovers the next time the user game state needs to be updated (e.g. when the construction is completed)

iv. Sets the next updated time of the user game state:

```python
ZADD user_updates $timestamp $user_id

```

3. An *updater* updates the user game state at the next update time by carrying out a number of commands:

i) Runs the following command to fetch the next user that needs to be updated (and at what time)

```python
ZRANGE user_updates 0 0 WITHSCORES

```

ii) If the score (timestamp) has been passed

a) Remove the next update time:

```python
REM user_updates $user_id

```

b) Perform game state update

c) Find next time the user game state needs to be updated again

d) Set next update time:

```python
ZADD user_updates $timestamp $user_id

```

![](/images/site-mirror/ce843e0495bded7e27c88bd0179b38c120439e0a-1600x942.webp)

### Client-server protocol

Protocol Buffers are used to define the messages that are sent between the client/server and the server/client.

### Client Messages

Below is the full definition.

```python
syntax = "proto3";
package pizzatribes;

option go_package = "github.com/fnatte/pizza-tribes/internal/models";

import "education.proto";
import "building.proto";
import "research.proto";

message ClientMessage {
  message Tap {
    string lotId = 1;
  }

  message ConstructBuilding {
    string lotId = 1;
    Building building = 2;
  }

  message UpgradeBuilding {
    string lotId = 1;
  }

  message RazeBuilding {
    string lotId = 1;
  }

  message CancelRazeBuilding {
    string lotId = 1;
  }

  message Train {
    Education education = 1;
    int32 amount = 2;
  }

  message Expand {
  }

  message Steal {
    int32 amount = 1;
    int32 x = 2;
    int32 y = 3;
  }

  message ReadReport {
    string id = 1;
  }

  message StartResearch {
    ResearchDiscovery discovery = 1;
  }

  string id = 1;
  oneof type {
    Tap tap = 2;
    ConstructBuilding constructBuilding = 3;
    UpgradeBuilding upgradeBuilding = 4;
    Train train = 5;
    Expand expand = 6;

    Steal steal = 7;
    ReadReport readReport = 8;
    RazeBuilding razeBuilding = 9;
    StartResearch startResearch = 10;
    CancelRazeBuilding cancelRazeBuilding = 11;
  }
}

```

### Server messages

Below is the full definition.

```python
syntax = "proto3";
package pizzatribes;

option go_package = "github.com/fnatte/pizza-tribes/internal/models";

import "gamestate.proto";
import "stats.proto";
import "report.proto";

message ServerMessage {
  message Response {
    string requestId = 1;
    bool result = 2;
  }

  message User {
    string username = 1;
  }

  message Reports {
    repeated Report reports = 1;
  }

  string id = 1;
  oneof payload {
    GameStatePatch stateChange = 2;
    User user = 3;
    Response response = 4;
    Stats stats = 5;
    Reports reports = 6;
  }
}

```

### File Tree

```python
.
├── cmd (golang source files for each command/process)
│   ├── api
│   ├── migrator
│   ├── updater
│   └── worker
├── docs
├── internal (shared golang source files)
├── protos (protobuf files used by both backend and frontend)
└── webapp (frontend application)
    ├── fonts
    ├── images
    ├── plugins
    ├── src
    └── tools

```

## 4. Getting started

**Prerequisite:**

- **Docker**
- **Docker Compose**

### Step 1: Running the application locally

There are two ways you can run the application locally. You can either run everything (Redis, services, web app) in a Docker container Or, you can pick and choose for faster development.

**Clone the repository**
git clone [https://github.com/redis-developer/pizza-tribes](https://github.com/redis-developer/pizza-tribes)

#### Start the services

This is arguably the easiest way to run the project locally. To get started, you need to execute the docker-compose command as shown below:

```python
cd pizza-tribes
cp .env.default .env
docker-compose up --build -d

```

This command will achieve the following:

- **Build all of the services: **the web app and the caddy front
- **Run everything: **this includes Redis and RedisInsight

When this command is carried out, the following is achieved:

- redis server running at port 6379
- Redisinsight running at port 8001
- The webapp running at port 8080

### Picking and choosing for faster development

If you want to make changes then you’ll benefit from Hot Module Replacement (HMR) in the web app. This will allow you to build the Go apps more efficiently. To achieve this, run Redis using docker-compose, and then run the services and web app on your host OS:

```python
printf "HOST=:8080\nORIGIN=http://localhost:3000\n" > .env
docker-compose up -d redis redisinsight
make -j start # Build and run go services (see Makefile for details)
cd webapp # in another terminal
npm install
npm run dev

```

Once carried out, this command should give you:

- Redis server running via Docker at 6379
- The Redis GUI ‘Reedisinsight” via docker at 8001
- The webapp running on the host system at 3000
- api via host OS at 8080

[**Note: **](Note: The web app will proxy calls to /api to )[The web app will proxy calls to ](Note: The web app will proxy calls to /api to )[*/api*](Note: The web app will proxy calls to /api to )[ to ](Note: The web app will proxy calls to /api to )*http://localhost:8080* (see *webapp/vite.config.ts*).

### Step 2: Registering new players

The users are stored as a hash set in key user:{user_id} containing fields. These include:

- id
- username
- hashed_password

The user_id can be looked up using the username via username:{username}.

**Registration** is achieved through the following commands:

- Generate unique id (rs/xid)
- redis cmd:

```python
SET username:{username} user_id

```

- redis cmd:

```python
HSET user:{user_id} "id" user_id "username" username "hashed_password" hash

```

**Authentication** is done like so:

- redis cmd (get user id):

```python
GET username:{username}

```

- redis cmd:

```python
HGETALL user:{user_id}

```

- Verify hashed_password

**Note: **If the hashes match, create JWT

### Step 3: Storing the user Game State

Using RedisJSON, the user game state is stored as a JSON value in the key user.

```python
user:{user_id}:gamestate

```

It does this with the following structure:

```python
syntax = "proto3";
package pizzatribes;
 
option go_package = "github.com/fnatte/pizza-tribes/internal/models";
 
import "google/protobuf/wrappers.proto";
import "education.proto";
import "building.proto";
import "research.proto";
 
message OngoingResearch {
  int64 complete_at = 1;
  ResearchDiscovery discovery = 2;
}
 
message Training {
  int64 complete_at = 1;
  Education education = 2;
  int32 amount = 3;
}
 
message Construction {
  int64 complete_at = 1;
  string lotId = 2;
  Building building = 3;
  int32 level = 4;
  bool razing = 5;
}
 
message Travel {
  int64 arrival_at = 1;
  int32 destinationX = 2;
  int32 destinationY = 3;
  bool returning = 4;
  int32 thieves = 5;
  int64 coins = 6;
}
 
message GameState {
  message Resources {
    int32 coins = 1;
    int32 pizzas = 2;
  }
 
  message Lot {
    Building building = 1;
    int64 tapped_at = 2;
    int32 level = 3;
  }
 
  message Population {
    int32 uneducated = 1;
    int32 chefs = 2;
    int32 salesmice = 3;
    int32 guards = 4;
    int32 thieves = 5;
    int32 publicists = 6;
  }
 
  Resources resources = 1;
  map<string, Lot> lots = 2;
  Population population = 3;
  int64 timestamp = 4;
  repeated Training trainingQueue = 5;
  repeated Construction constructionQueue = 6;
  int32 townX = 7;
  int32 townY = 8;
  repeated Travel travelQueue = 9;
  repeated ResearchDiscovery discoveries = 10;
  repeated OngoingResearch researchQueue = 11;
}
 
message GameStatePatch {
  message ResourcesPatch {
    google.protobuf.Int32Value coins = 1;
    google.protobuf.Int32Value pizzas = 2;
  }
 
  message LotPatch {
    Building building = 1;
    int64 tapped_at = 2;
    int32 level = 3;
    bool razed = 4;
  }
 
  message PopulationPatch {
    google.protobuf.Int32Value uneducated = 1;
    google.protobuf.Int32Value chefs = 2;
    google.protobuf.Int32Value salesmice = 3;
    google.protobuf.Int32Value guards = 4;
    google.protobuf.Int32Value thieves = 5;
    google.protobuf.Int32Value publicists = 6;
  }
 
  ResourcesPatch resources = 1;
  map<string, LotPatch> lots = 2;
  PopulationPatch population = 3;
  google.protobuf.Int64Value timestamp = 4;
  bool trainingQueuePatched = 5;
  repeated Training trainingQueue = 6;
  bool constructionQueuePatched = 7;
  repeated Construction constructionQueue = 8;
  google.protobuf.Int32Value townX = 9;
  google.protobuf.Int32Value townY = 10;
  bool travelQueuePatched = 11;
  repeated Travel travelQueue = 12;
  bool discoveriesPatched = 13;
  repeated ResearchDiscovery discoveries = 14;
  bool researchQueuePatched = 15;
  repeated OngoingResearch researchQueue = 16;
}

```

The game state is accessed in different ways depending on the use case. But for a complete retrieval, the following is used:

- redis cmd:

```python
JSON.GET user:{user_id}.gamestate

```

In other cases, a path is used to retrieve only a subset of the data:

- redis cmd (retrieve building info at lot 5):

```python
JSON.GET user:{user_id}.gamestate '.lots["5"]'

```

- redis cmd (retrieve population data):

```python
JSON.GET user:{user_id}.gamestate .population

```

## 5. The Game State Update

The game state update is what makes the game tick and it’s one of the most important processes in the game. Its purpose is to:

- Extrapolate resources (i.e. increase resources with produced amounts since the last update)
- Complete buildings
- Complete training sessions for the characters
- Complete travels (i.e. thieves moving between towns)

In addition, the game state update will also:

- Insert resource data points for RedisTimeSeries
- Update the leaderboard (because the resources have changed)

### Discovering which user needs the update

The updater runs in a loop that queries a sorted set that’s called user_updates. It retrieves the top record in the sorted set by running the following command:

```python
ZRANGE user_updates 0 0 WITHSCORES
{1.6208459243016696e+18 c2e16taink8s73ejr3qg}

```

By utilizing WITHSCORES we also retrieve the timestamp of when that user needs a game state. As such, the updater can check if timestamp < now. If so, then the user can carry out the following commands:

```python
ZREM user_updates c2e19af8q04s73f8j8lg

```

2. Proceed to update the game state

**Note: **there is some level of risk involved because if the game state update fails, the user will no longer have a record in the user_updates sorted set. When this happens, no game state update will be scheduled.

To avoid this, the game will ensure that the user is scheduled for game state updates when logging in.

### Updating the Game State

The update is executed with a check-and-set approach (WATCH, MULTI, EXEC). This is achieved through the following steps:

```python
WATCH user:{user_id}:gamestate

```

```python
JSON.GET user:{user_id}:gamestate

```

- Run game state process to figure out how to transform the game state
- MULTI
- Run all modifying commands to convert to the game state calculated in the previous step
- EXEC

For more details of a simple game state update, see the trace below:

```python
watch user:c2e19af8q04s73f8j8lg:gamestate: OK
JSON.GET user:c2e19af8q04s73f8j8lg:gamestate .: {"resources":{"coins":20,"pizzas":0},"lots":{"1":{"building":3},"2":{"building":0},"9":{"building":1},"10":{"building":2}},"population":{"uneducated":8,"chefs":1,"salesmice":1,"guards":0,"thieves":0},"timestamp":1620845911,"trainingQueue":[],"constructionQueue":[],"townX":51,"townY":58,"travelQueue":[]}
[multi: QUEUED
	JSON.SET user:c2e19af8q04s73f8j8lg:gamestate .timestamp 1620845921: OK
	JSON.SET user:c2e19af8q04s73f8j8lg:gamestate .resources.coins 22: OK
	JSON.SET user:c2e19af8q04s73f8j8lg:gamestate .resources.pizzas 0: OK
	exec: []]
unwatch: OK

```

**Note: **Extrapolating resources, completing buildings, trainings and complete travels are all implemented using the flow described above.

### Scheduling the next game update

When the game state has been updated, you’ll have to schedule the next one. Here’s how to do it:

- Determine when the game state needs to be updated
  - Is a building being completed?
  - Is a training session being completed?
  - Is travel being completed?

```python
ZADD user_updates {timestamp_of_next_update} {user_id}

```

### Inserting data points with RedisTimeSeries

The RedisTimeseries module is used to track the changes in user resources. The resources are tracked using the following keys:

```python
user:c2e19af8q04s73f8j8lg:ts_coins

```

```python
User:c2e19af8q04s73f8j8lg:ts_pizzas

```

When every game state update is carried out, a new data point is inserted into each key. Below is an example:

```python
TS.ADD user:{user_id}:ts_coins {timestamp_now} {current_amount_of_coins} TS.ADD user:{user_id}:ts_pizzas {timestamp_now} {current_amount_of_pizzas}

```

When the user wants to look at their resource history, the following command is used to retrieve the aggregated data points from the last 24 hours.

```python
from := now - 24 hours
	to := now
	timeBucket := 1 hour
 
	TS.RANGE user:{user_id}:ts_coins {from} {to} AGGREGATION avg {timeBucket}
	TS.RANGE user:{user_id}:ts_pizzas {from} {to} AGGREGATION avg {timeBucket}

```

### Updating the Leaderboard

The game state update will change the number of coins a user has which is why we need to update the leaderboard. The leaderboard is a sorted set with the key leaderboard. It’s updated by running the following command:

```python
ZADD leaderboard {current_amount_of_coins} {user_id}

```

When any user wants to have access to the leaderboard, the data is retrieved with the following command:

```python
ZREVRANGE leaderboard 0 20 WITHSCORES

```

## Conclusion: Keeping Everything in Real Time Using Redis

From a performance perspective, achieving real-time gameplay is one of the most important objectives behind creating a successful online multiplayer game. Failing to achieve this will drastically hamper the user’s experience, irrespective of how advanced other qualities of the game are.

Despite having a complicated architecture, Redis removed this obstacle through its ability to zip data between different components with ease. Having no lags, no delays, and no data setbacks *whatsoever* allowed this Launchpad App to create a complex yet engaging online multiplayer strategy game where users from around the world can battle it out against each other for the top spot.

If you want to get more of an insight into how this application was made then you may want to [check out this YouTube video](https://www.youtube.com/watch?v=xVbdLyBARvA).

We should also let you know that we have an exciting range of game-changing applications (excuse the pun) on the [Redis Launchpad](https://launchpad.redis.com/). Here you’ll discover a collection of apps that are having an impact on everyday life by everyday programmers.

So make sure to check it out!

[Watch the video](https://launchpad.redis.com/)

## Who built this application?

![](/images/site-mirror/1615f28909e8da34b60a093cb9457f7eff22e911-400x400.webp)

**Matteus Hemström**

From Matteus is a highly innovative software engineer who currently plies his trade at Nuway.

If you want to keep up to date with all of the projects he’s been involved with, then head over to his [GitHub page here](https://github.com/fnatte).
