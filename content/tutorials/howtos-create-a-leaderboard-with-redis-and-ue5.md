---
title: "Creating a Real-time Leaderboard with UE5 and Redis"
linkTitle: "Creating a Real-time Leaderboard with UE5 and Redis"
url: "/tutorials/howtos/create-a-leaderboard-with-redis-and-ue5/"
description: "Build a real-time multiplayer leaderboard by combining Redis sorted sets with an Unreal Engine 5 game client. You'll create a Node.js REST API backed by Redis, then call it from UE5 Blueprints..."
aliases:
- "/tutorials/howtos-create-a-leaderboard-with-redis-and-ue5/"
date: 2026-02-25
lastmod: 2026-02-25
hidden: true
---

*Published 25 February 2026*

Build a real-time multiplayer leaderboard by combining Redis sorted sets with an Unreal Engine 5 game client. You'll create a Node.js REST API backed by Redis, then call it from UE5 Blueprints using the VaRest plugin to submit and display player rankings.

## What you'll learn

- How Redis sorted sets power real-time leaderboard ranking
- How to build a Node.js REST API that writes and reads leaderboard data with `ZADD` and `ZRANGE`
- How to integrate a REST API into Unreal Engine 5 using the VaRest plugin
- How to connect your game backend to Redis Cloud for production use

## Prerequisites

- **Unreal Engine 5** installed via the Epic Games Launcher
- **Basic C++ or Blueprints knowledge** for UE5 development
- **Docker Desktop** to run the game backend and local Redis
- **VS Code** or an IDE of your choice
- **Postman** (optional) to test the REST API
- A free **Redis Cloud** account for the cloud deployment section ([sign up here](https://redis.io/try-free/))

For a general introduction to leaderboards with Redis, see [How to build a real-time leaderboard with Redis](/tutorials/howtos/leaderboard/).

## Why use Redis for game leaderboards?

Redis's performance, low latency, and versatility make it an excellent choice for building responsive and scalable game backends, especially for real-time multiplayer games. There are several use cases where Redis can improve your game development pipeline, the most common and impactful are real-time leaderboards and matchmaking. Other use cases include: session management, game state data caching, inventory, analytics, rate limiting.

### Why combine Redis with Unreal Engine 5?

Unreal Engine is a cornerstone of the video game industry, trusted by AAA studios and indie developers alike for its unmatched graphical fidelity, flexible architecture, and powerful Blueprints system. As a real-time 3D creation platform, Unreal enables developers to build immersive, interactive experiences across platforms—from PC and consoles to mobile and XR.

Redis, the world's most popular in-memory data store, brings extreme speed, simplicity, and scalability to real-time applications. With sub-millisecond response times, built-in data structures (such as lists, sets, sorted sets, hashes, and streams), and support for pub/sub messaging, Redis is a perfect match for the demanding performance needs of multiplayer games, live leaderboards, matchmaking, state synchronization, and analytics.

## How do you set up the leaderboard project?

Welcome to this tutorial on creating a real-time leaderboard with Redis and Unreal Engine 5. To get you started, we have an example project named Redis Racer that you can download from [GitHub](https://github.com/redis-developer/redis-racer). There is also a written version of this tutorial for your reference. The links to which will be in the description below.

For our leaderboard, we will be using a sorted set as the data type. A sorted set is a collection of unique strings (members) ordered by an associated score, which is perfect for showing the names and current scores of the top scoring players.

## How do you build the leaderboard REST API?

[YouTube: https://www.youtube.com/watch?v=2UhkGLJpM_s](https://www.youtube.com/watch?v=2UhkGLJpM_s)

### How does the leaderboard code work?

1.  [Download the project from GitHub](https://github.com/redis-developer/redis-racer) and open the project in VS Code
2.  Look at the `game-backend` leaderboard code, specifically the `addLeaderboardEntry` and the `getLeaderboard` functions:

```javascript
export async function addLeaderboardEntry(key, score, member) {
    const redis = await getClient();
    const date = new Date();

    //ZADD key score member, where member is a string that includes the member name and the date
    const result = await redis.zAdd(key, [
        {
            value: member.toUpperCase() + '-' + date.toISOString(),
            score: score,
        },
    ]);

    if (result > 0) {
        return {
            status: 200,
            message: 'ZADD success, added new leaderboard entry.',
        };
    } else {
        return { status: 400, message: 'ZADD failed...' };
    }
}
```

In this function, we use the Redis client to send the ZADD command to add a new member to a sorted set. If there is currently no sorted set with this key, the ZADD command will also create a new sorted set. The member variable is the initials of the player appended to the current timestamp to allow for multiple entries of the same initials to be added to the leaderboard. If the result of the ZADD command is an integer greater than 0, the command was successful, otherwise the command failed.

```javascript
export async function getLeaderboard(key, count) {
    const redis = await getClient();

    //ZRANGE key start stop [WITHSCORES] [REV]
    const result = await redis.zRangeWithScores(key, 0, count - 1, {
        REV: 'true',
    });

    if (result.length === 0) {
        return { status: 404, message: 'No leaderboard entries found.' };
    }

    const leaderboard = {
        leaderboard: result,
    };

    return leaderboard;
}
```

In this function the Redis client is used to send a ZRANGE command with the WITHSCORES and REVERSE options. The count variable is the total number of entries we want to retrieve from the leaderboard. Since the result is a zero-based array, we will pass in 0 for the start parameter and count -1 for the stop parameter. If the result is an empty array, no leaderboard entries were found.

### How do you test the REST API?

1.  Run the Docker containers

```bash
cp .env.example .env
docker compose up -d
```

1. Test the RestAPI with curl or Postman:

```bash
curl -X GET "http://localhost:3000/api/leaderboard/<key-name>?count=<number_of_entries>"

// example
curl -X GET "http://localhost:3000/api/leaderboard/redis-racer?count=10"
```

```bash
curl -X POST http://localhost:3000/api/leaderboard -H "Content-Type: application/json" -d "{\"key\": <key_name>, \"score\": <score>, \"member\": <player_initials>}"

// example
curl -X POST http://localhost:3000/api/leaderboard -H "Content-Type: application/json" -d "{\"key\": \"redis-racer\", \"score\": 1564, \"member\": \"rrt\"}"
```

## How do you integrate the leaderboard into Unreal Engine 5?

[YouTube: https://www.youtube.com/watch?v=qw4TsDdjrrc](https://www.youtube.com/watch?v=qw4TsDdjrrc)

### How do you add the VaRest plugin?

1.  Claim the [VaRest plugin](https://www.fab.com/listings/d283e40c-4ee5-4e73-8110-cc7253cbeaab) in the Fab Marketplace
2.  In the Epic Launcher, install the plugin to UE.
3.  Open the RedisRacer project.
4.  Go to Edit → Plugins
5.  Search for VARest
6.  Tick the checkbox to enable the plugin and restart the editor.

### How do you create the BP_Leaderboard blueprint?

1.  In the Content Browser, create a new blueprint actor named BP_Leaderboard.
2.  In the Event Graph, create 3 custom events:
3.  AddLeaderboardEntry,
4.  GetLeaderboard, and
5.  CreateRaceEndWidget
6.  For EventBeginPlay,
7.  Get the game mode, cast it to RedisRacerGameMode and promote it to variable.
8.  From the RedisRacerGameMode, bind event to event RaceEnd
9.  Create a custom event called RaceEnd
10. Promote win, score, and initials to variables.
11. Call the AddLeaderboardEntry event
12. Followed by the GetLeaderboard event

![UE5 Blueprint Event Graph showing EventBeginPlay setup with RedisRacerGameMode cast and RaceEnd event binding](/images/site-mirror/dc7111788ff0af59633e22e454e059c3e6a6cce2-1628x496.webp)

1.  AddLeaderboardEntry ⇒ RestAPI call to update leaderboard
2.  For the AddLeaderboardEntry, we'll use the VARest subsystem
3.  ConstructJsonRequest
4.  It will be a POST API call with Json as the ContentType
5.  From the return value of the Json Request, we will find SetRequestObject
6.  Drag out from the JsonObject and MakeJson
7.  Add 3 string elements to the JsonObject
8.  key,
9.  score, and
10. member
11. Create a new variable and name it LeaderboardKey, remember to compile and input the leaderboard key name later.
12. Connect the variables, LeaderboardKey, Score, and Initials to the MakeJson node.
13. Drag out from the return value of the ConstructJsonRequest and find ProcessURL
14. The URL will be http://localhost:3000/api/leaderboard
15. From the return value of the ConstructJsonRequest find BindEventToOnRequestComplete and BindEventToOnRequestFail
16. We will create one custom event for both of these events.
17. GetResponseContentAsString and connect it to a PrintString

![UE5 Blueprint showing the AddLeaderboardEntry event with VaRest POST request to the Redis-backed leaderboard API](/images/site-mirror/2db63b0bf67858e83cfa9b4ee44cd011d78e9fb0-1834x453.webp)

1.  GetLeaderboard ⇒ RestAPI call to retrieve leaderboard
2.  Use the VARest subsystem.
3.  ConstructJsonRequest
4.  The verb is GET and ContentType is Json
5.  From the return value, find ProcessURL
6.  I'll copy the URL from our testing in Postman
7.  From the return value of the ConstructJsonRequest find BindEventToOnRequestFail and BindEventToOnRequestComplete, but this time we will create two separate custom events.
8.  GetLeaderboardFail, will be the same GetResponseContentAsString connected to a PrintString for debugging.

![UE5 Blueprint showing the GetLeaderboard event with VaRest GET request to retrieve player rankings from Redis](/images/site-mirror/a3b57f0212c975a692bff6e54d50bfcc618bf3eb-1901x526.webp)

1.  For GetLeaderboardComplete
2.  Connect GetResponseObject to a BreakJson
3.  Add one element named "leaderboard" (all lowercase), and it is an array of objects.
4.  From the array of objects, get a ForEachLoop, for each array element:
5.  GetStringField with the FieldName of "value"
6.  GetIntegerField with the FieldName of "score"
7.  For the string field
8.  We'll take a left with count 3, this is to get just the player initials
9.  We will then append the array index + 1 to designate the player rank on our leaderboard.
10. Create a Leaderboard variable with the type of string:integer map to store the results from the GetLeaderboard API call.
11. Get a reference to the Leaderboard variable we just created and find Add to add entries.
12. Plug in the StringField result and the IntegerField into the Leaderboard.
13. When the ForEachLoop is completed, call CreateRaceEndWidget

![UE5 Blueprint showing GetLeaderboardComplete event that parses the JSON response and populates the leaderboard map](/images/site-mirror/c6cbf7ef698b1c5fc6369e049a24f9ffb4666f9c-1872x463.webp)

1.  CreateRaceEndWidget
2.  CreateWidget, find W_RaceEnd
3.  Connect the Win, Leaderboard, and Score variables to the input of the W_RaceEnd Widget.
4.  Then add the widget to viewport.

![UE5 Blueprint showing the CreateRaceEndWidget event that builds and displays the race-end leaderboard UI widget](/images/site-mirror/c0513752bf70a5dce598fca4a5a8dc2a71afc066-1143x332.webp)

1.  Compile and set the default value for the LeaderboardKey variable, which is "redis-racer" for this tutorial.
2.  Add the BP_Leaderboard blueprint to the level, and test play!

## How do you connect the leaderboard to Redis Cloud?

### How do you create a new Redis Cloud database?

1.  Go to [https://redis.io/try-free/](https://redis.io/try-free/) to create a new account or sign into the [Redis Cloud console](https://cloud.redis.io/#/).
2.  Click New database, you can try 30 MB Redis Essentials for free with no time limit.
3.  Rename the database if you'd like
4.  Select your preferred cloud vendor and the region closest to you.
5.  Select the 30 MB free option and click Create database.
6.  Wait for the database to be provisioned and copy the Public endpoint.

### How do you update the environment variables?

Now we need to update our game backend code to use the Redis Cloud database. Here, we have two choices: continue using Docker to run our game backend container or run the game backend server with NodeJS. Both methods require updating the Redis URL to point to the Redis Cloud database. The difference is which environment variable file to update.

#### To continue using Docker

1.  Open the .env.docker environment variable file and replace the localhost connection string with your Redis Cloud public endpoint.
2.  Go back to the Redis Cloud console and scroll down to find the Security section.
3.  Click on the header to expand the security section
4.  Then click Copy under Default user password to copy the password.
5.  Note that you can change the password by clicking on the Edit button near the top right corner.
6.  Go back to the .env.docker file in VS Code
7.  Append the username and password to the connection string

```bash
REDIS_URL="redis://default:<password>@<public_endpoint>"
```

1. Save and run the docker containers

```bash
docker compose down
docker compose up -d
```

1. In Docker Desktop
2. Stop the local Redis container but leave the game backend leaderboard running.

##### If you would rather use NodeJS

1.  Create an .env file by copying the .env.example file
2.  Make changes to the .env file instead of the .env.docker file

```bash
cp .env.example .env
npm install
npm run dev
```

#### How do you connect to Redis Cloud from UE5?

[YouTube: https://www.youtube.com/watch?v=wNb-AiHVpe8](https://www.youtube.com/watch?v=wNb-AiHVpe8)

1.  Go back to our project folder and open the Redis Racer UE5 project by clicking on the uproject file.
2.  There's a shortcut to reach the finish line without going through the entire course and that's to go in reverse.
3.  Test play the game, wait until the timer in the top right corner starts, and drive backwards!
4.  This will call the RaceEnd event in the BP_Leaderboard which will add an entry to the Redis Cloud leaderboard and get the top scores to display in the W_RaceEnd widget.
5.  Do this a few more times to add a few entries into our leaderboard.

#### How do you view the Redis Cloud database using Redis Insight?

We can use Redis Insight to get a graphical user interface of our Redis databases. Previously, you had to install the desktop application and connect it to your cloud database but now we have Redis Insight in the cloud! That means you can look at your Redis Cloud database in your web browser without having to install the desktop application.

1.  To access Redis Insight in the Cloud, simply go to your database in the Redis Cloud console, under the General section, click Connect.
2.  In the panel that opens up, click Redis Insight dropdown and click Launch Redis Insight web.

There we have it, we can see our leaderboard entries! Our game backend is now connected to Redis Cloud and we have a real-time leaderboard with Redis and Unreal Engine 5!

## Next steps

Now that you have a working real-time leaderboard in UE5 backed by Redis, here are some ways to extend your project:

- **Add pagination** to your leaderboard API so players can browse beyond the top scores using `ZRANGE` with offset and count parameters.
- **Implement multiple leaderboards** for different game modes, time periods (daily, weekly, all-time), or levels by using separate sorted set keys.
- **Add player authentication** to your game backend so only verified players can submit scores.
- **Explore Redis Pub/Sub** to push leaderboard updates to connected clients in real time instead of polling the API.
- **Learn more about Redis sorted sets** and other leaderboard patterns in the [How to build a real-time leaderboard with Redis](/tutorials/howtos/leaderboard/) tutorial.
