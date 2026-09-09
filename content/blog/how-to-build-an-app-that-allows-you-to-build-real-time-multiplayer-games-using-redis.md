---
title: "How to Build an App That Allows You to Build Real Time Multiplayer Games Using Redis"
linkTitle: "How to Build an App That Allows You to Build Real Time Multiplayer Games Using Redis"
url: "/blog/how-to-build-an-app-that-allows-you-to-build-real-time-multiplayer-games-using-redis/"
description: "Online games are rapidly becoming one of the most popular forms of entertainment. The technological boom, along with our increased usage of the internet, has made games more accessible, allowing..."
date: 2022-02-10
blogCategories:
- "How To and Tutorials"
- "Tech"
authors:
- "Growth Team"
lastmod: 2025-03-27
hidden: true
---

*By Growth Team · Published 10 February 2022 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/b916726681b6461eb02af986eee7636da07af826-772x550.webp)

Online games are rapidly becoming one of the most popular forms of entertainment. The technological boom, along with our increased usage of the internet, has made games more accessible, allowing people from all over the world to compete against each other.

Because of this geographical spread of players, games must operate with a low latency database to allow users to interact with each other in real time. Any instances where there’s a delay between the command and gaming response will create friction and hamper engagement.

Advanced programmer [Tinco Andringa](https://github.com/tinco) took this challenge on and created his own gaming platform, Topscorio. By using Redis, data is sent, processed, and retrieved in real time with exceptional consistency, [creating a gaming platform](/industries/gaming/) that’s hyper-responsive to player commands.

Let’s take a look at how Tinco put this application together. But before we go any further, we’d like to point out that we have an exciting range of applications for you to check out on the [Redis Launchpad](https://launchpad.redis.com/). So make sure to give them a peek after this post!

[Click here to view video](https://www.youtube.com/embed/NHEjqVq23z4)

## How to Build an App That Allows you to Build Real Time Multiplayer Games

1. What will you build?
1. What will you need?
1. Architecture
1. Getting started
1. How it works
1. How data is stored
1. How data is accessed
1. Conclusion

## 1. What will you build?

You’ll build an app that will allow developers to create their own online multiplayer game. Topscorio optimizes the gaming experience by keeping track of high scores without having to worry about players cheating and managing big network infrastructures.

Below we’ll show you how to build this application from the bottom up, highlighting what components you’ll need along with its functionality.

![](/images/site-mirror/ba35182de63b6bd67635ebadf261a17330c8de2f-1600x781.webp)

## 2. What will you need?

- [**JavaScript**](https://www.javascript.com/)**: **Used as the preferred programming language.
- [**TypeScript**](https://www.typescriptlang.org/)**: **Used as a typed programming language that builds on Javascript.
- [**Redis**](https://redis.io/)**: **Used as an open-source, in-memory data structure store, database, cache, and message broker.
- [**RedisJSON**](/blog/redis-as-a-json-store/)**: **Allows storing, updating, and fetching JSON values from Redis keys
- [**WebSocket.IO**](https://socket.io/)**:** Used as a library to abstract WebSocket connections.

## 3. Architecture

![](/images/site-mirror/7a9b85a7e32d34ccbc1d37cea2fdaf327655061e-1600x925.webp)

- The frontend connects to the backend through a WebSocket.
- The frontend sends requests to the backend, requesting subscriptions on channels, and executing commands.
- The backend then broadcasts channels to all connected clients and sends messages with updates as responses to client commands.
- User sessions and information are stored in the Redis database with an expiry set.
- Game logs are instances of players using a game together. This is where all game moves and states are saved. Persistence is also recommended here.

## 4. Getting started

### Prerequisite:

- Git
- NPM
- Sendgrid API configured via [https://app.sendgrid.com/settings/api_keys](https://app.sendgrid.com/settings/api_keys)
- Redis Enterprise Cloud Subscription

### Step 1: Clone the repository

git clone [https://github.com/redis-developer/topscorio](https://github.com/redis-developer/topscorio)

### Step 2. Set up Redis Enterprise Cloud

Create your free [Redis Enterprise Cloud account](/try-free/). Once you click on ‘Get Started,’ you’ll receive an email with a link to activate your account and complete the signup process.

![My Image](/images/site-mirror/1cd937f45a22b8f38f70e466b17d168c00e7840e-1600x1161.webp)

### Step 3. Create your subscription

Next, you’ll have to create a Redis Enterprise Cloud subscription. In the Redis Enterprise Cloud menu, click ‘Create your Subscription.’

Follow [https://docs.redis.com/latest/rc/rc-quickstart/](https://docs.redis.com/latest/rc/rc-quickstart/) to create Redis Enterprise Cloud with RedisJSON module enabled.

### Step 4. Enter database details

Click ‘Create Database’. Enter the database name and choose RedisJSON module.

![My Image](/images/site-mirror/c990a4578b7f01c8a05fc9dd4662ab9725409eab-1256x850.webp)

### Step 5. Set up environmental variables

Create an empty .env file and add the below parameters:

```javascript
NODE_ENV=development
SERVER_PORT=5020
SESSION_REDIS=redis://default:<pass>@<url>
USERS_REDIS=redis://default:<pass>@<url>
GAMES_REDIS=redis://default:<pass>@<url>
GAME_LOGS_REDIS=redis://default:<pass>@<url>
SENDGRID_API_KEY=<SENDGRID_API_KEY>
```

Fill in database addresses, passwords, and the sendgrid API key as needed.

Then in one terminal run:

```javascript
npm install
npm run backend

```

```javascript
topscorio-auth@1.0.0 backend /root/topscorio> npm run build && node .
```

Then, in another terminal, run the following command:

```javascript
npm run frontend
```

```javascript
npm run frontend

> topscorio-auth@1.0.0 frontend /root/topscorio
> webpack serve


> topscorio-auth@1.0.0 build /root/topscorio
> tsc && webpack build

ℹ ｢wds｣: Project is running at http://localhost:5010/
ℹ ｢wds｣: webpack output is served from /
ℹ 「wds」: Content not from webpack is served from /root/topscorio/dist/frontend

```

And navigate to [http://localhost:5010](http://localhost:5010/) in your browser.

Click ‘Start now’ and enter the email address:

![](/images/site-mirror/5449a1eb5cfb9566adc8e8c87b6d6a6aa29746c1-1088x864.webp)

The app has an example chess game implemented, opening up multiple browser sessions to test this.

![Screenshot showing online multiplayer chess](/images/site-mirror/1b3f1d10aa004d170cfa9c5a0e8f8b3ea57bcea3-1600x792.webp)

## 5. How data is stored

**Users and sessions**

User and session storage is managed in backend/authentication_store.ts. This generates a unique session token for each session. Here’s an example:

```javascript
SETEX session-123abc 259200 {"some": "json"}.
```

Sessions are resumed by fetching the setting from localStorage and then retrieving the session from Redis. Here’s an example:

```javascript
GET session-123abc
```

New authentication tokens are stored in the same way but with a shorter expiry.

Users are stored using the following command:

```javascript
JSON.SET
```

**Note:** The email address is used as the key.

Users are retrieved using the following command:

```javascript
JSON.GET
```

**Note: **This is used as the path to retrieve the whole object.

## 6. How it works

- The frontend connects to the backend through a WebSocket.
- The frontend sends requests to the backend, requesting subscriptions on channels, and executing commands.
- The backend then broadcasts channels to all connected clients and sends messages with updates as responses to client commands.
- User sessions are stored in the SESSION_REDIS database, with an expiry set.
- User information is stored in USERS_REDIS. Recommended persistence is enabled for this database.
- Games are saved in GAMES_REDIS; this should also be persisted. Game logs are instances of players using a game together. This is where all game moves and states are saved. Persistence is also recommended here.

Games and game logs storage are managed in backend/games_store.ts. A cache of all games is stored in the Redis database under the following key: all-games. When the server starts up it’s first retrieved using the following command:

```javascript
JSON.GET all-games
```

If it’s null, then it will populate with the below command:

```javascript
JSON.SET all-games . {"newest": []}
```

When the server starts up, it will subscribe to the newest channel on the games database as well as the open channel on the game logs database. It does this with the SUBSCRIBE command like so:

```javascript
SUBSCRIBE newest
```

Whenever a client shows interest in a channel, the server will initiate a subscription. For example, when a user joins a game with the id abc123, the server will subscribe to that game using the following command:

```javascript
SUBSCRIBE abc123
```

At the moment, the server does not UNSUBSCRIBE. When a user creates a game the server publishes a message on the newest channel, like so:

```javascript
PUBLISH newest { "gameInfo": ... } 
```

Moreover, the server carries out the following command to add the user’s game to all of the game’s newest array:

```javascript
JSON.ARRAPPEND all-games .newest {"gameInfo" : ... }
```

To make sure that it doesn’t overflow, the server will follow up with the following command to shorten its backup:

```javascript
JSON.arrtrim all-games .newest <begin> <end>
```

Once created, the games are retrieved using the following command:

```javascript
JSON.GET game-<gameid>
```

## 7. How the application works

**Signing in/signing up**

Both signing in and signing up share the same process. First, you need to click on the ‘Start Now’ button on the homepage. Next, you’ll be required to provide your email address for a confirmation email. Open this email in your inbox, copy the sign-up link and then paste it onto your browser.

You’ll then be taken to a new page. Click on the ‘Start Now’ button to get started.

![](/images/site-mirror/3d7b91bff0cabf6467ffd8052bfeee7e71308eaa-1600x841.webp)

**Creating a new game**

When you log in you’ll immediately land on the ‘Create a new game’ page. At the top, enter the name of your game in the given field. You’ll then need to paste your game logic in the big empty box below.

Once you’ve done this, press ‘create game’ to proceed to the next step.

![](/images/site-mirror/e8214a9f9a2d31bb0a14404aeb831aa46f8a14a3-1600x841.webp)

## Conclusion: Enhancing the gaming experience with low latency

Players today expect games to be hyper-responsive in all aspects, where delays between commands are almost non-existent. Even just one lag is enough to damage the user experience and frustrate players, which will only push them towards games that can run smoothly without any hiccups.

With Redis, Tinco was able to maximize the gaming experience through its ability to provide users with real-time responses. Components within the architecture became more interconnected where data transmission became both seamless and consistent, allowing players to compete with each other online in real-time, irrespective of their location.

To get the full visual demonstration of how this application was made, watch Timo’s [YouTube video here](https://www.youtube.com/watch?v=NHEjqVq23z4). If you enjoyed this article, you should know that this is only the tip of the iceberg when it comes to Redis’ capabilities.

All around the world, programmers are using Redis to build innovative applications that are having a profound impact on everyday life. Make sure to check out the [Redis Launchpad](https://launchpad.redis.com/) to have access to an exciting array of applications to inspire you.

[Watch the video](https://launchpad.redis.com/)

## Who Built This App?

### Tinco Andringa

![](/images/site-mirror/4eb292eb27e07fb4efbebac18e866287f0314b92-360x360.webp)

Tinco is a leading software engineer at AeroScan. Make sure to visit his [GitHub page](https://github.com/tinco/topscorio) to keep up to date with all of the projects he’s involved with.
