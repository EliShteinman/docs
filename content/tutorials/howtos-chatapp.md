---
title: "How to build a Chat application using Redis"
linkTitle: "How to build a Chat application using Redis"
url: "/tutorials/howtos/chatapp/"
description: "Real-time chat is an online communication channel that allows you to conduct conversations instantly. More and more developers are tapping into the power of Redis as it is extremely fast and..."
aliases:
- "/tutorials/howtos-chatapp/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> Build a real-time chat application using **Redis Pub/Sub** for cross-server messaging, **WebSockets** (Socket.IO) for client-server communication, and **Flask** as the Python backend. Redis handles user presence tracking, message storage with sorted sets, and room management with sets. [Clone the demo repo](https://github.com/redis-developer/basic-redis-chat-app-demo-python) and follow the steps below to get it running.

Real-time chat is an online communication channel that allows you to conduct conversations instantly. More and more developers are tapping into the power of Redis as it is extremely fast and supports a variety of rich data structures such as Lists, Sets, Sorted Sets, and Hashes. Redis also includes [Pub/Sub](https://redis.io/docs/latest/develop/interact/pubsub/) messaging that allows developers to scale the backend by spawning multiple server instances.

> **WARNING**
>
> While this traditional chat application tutorial remains insightful, we encourage you to dive into our [AI chatbot tutorial](/tutorials/howtos/solutions/vector/gen-ai-chatbot) to unlock the potential of modern conversational experiences.

> **INFO**
>
> This code is open source. You can find the link at the end of this tutorial.

## What will you learn?

- How to use [Redis Pub/Sub](https://redis.io/docs/latest/develop/interact/pubsub/) for real-time message broadcasting across server instances
- How to store and retrieve chat messages using [Redis sorted sets](https://redis.io/docs/latest/develop/data-types/sorted-sets/)
- How to manage user sessions and presence tracking with [Redis sets](https://redis.io/docs/latest/develop/data-types/sets/) and [hashes](https://redis.io/docs/latest/develop/data-types/hashes/)
- How to integrate WebSockets (Socket.IO) with Redis for a scalable chat backend

## What will you build?

A real-time chat application with:

- User authentication and session management
- Public and private chat rooms
- Online/offline user presence tracking
- Cross-server message delivery via Redis Pub/Sub

[YouTube: https://www.youtube.com/embed/miK7xDkDXF0](https://www.youtube.com/embed/miK7xDkDXF0)

## Prerequisites

- Python 3.6+
- [Node.js](https://nodejs.org/) and [Yarn](https://yarnpkg.com/) for the frontend
- A running [Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/) instance

## How do you set up the chat application?

### Step 1. Clone the repository

```bash
git clone https://github.com/redis-developer/basic-redis-chat-app-demo-python
```

### Step 2. Install frontend dependencies

```bash
cd client
yarn install
```

### Step 3. Start the frontend

```bash
yarn start
```

```bash
You can now access a chat window in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.1.9:3000
```

![Chat application login screen showing the user selection interface and available chat rooms](/images/site-mirror/2e442d7eafb85f2c752af9f4b12344c65e5c504a-1044x1116.webp)

### Step 4. Install the required Python modules

```bash
cd ..
pip3 install -r requirements.txt
```

### Step 5. Run the backend

```bash
python3 -m venv venv/
source venv/bin/activate
python3 app.py
```

```bash
python3 app.py
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 220-696-610
(8122) wsgi starting up on http://127.0.0.1:5000
```

![Terminal output showing the Flask backend starting with Socket.IO and the WebSocket server listening on port 5000](/images/site-mirror/8eeeb4b3ef443c4ba6f94a48ec792714da85f67f-2000x1422.webp)

## How does the chat application work?

The server works as a basic REST API that handles session management and user state in the chat room, alongside the WebSocket/real-time messaging layer. When the server starts, the initialization step occurs. First, a new Redis connection is established and it checks whether it needs to load demo data.

### How is the data initialized?

For simplicity, a key with a `total_users` value is checked: if it does not exist, the Redis database is filled with initial data.

```bash
EXISTS total_users
```

The demo data initialization is handled in multiple steps:

### How are users created?

A new user id is created by incrementing the counter:

```bash
INCR total_users
```

Then a user ID lookup key is set by username:

```bash
SET username:nick user:1
```

And the rest of the user data is written to a hash set:

```bash
HSET user:1 username "nick" password "bcrypt_hashed_password"
```

Each user is also added to the default "General" room. A set holds the chat room ids for each user:

```bash
SADD user:1:rooms "0"
```

### How are private rooms created?

For private messaging, a room id is generated from both user ids in ascending order. For example, to create a private room between users 1 and 2:

```bash
SADD user:1:rooms 1:2
SADD user:2:rooms 1:2
```

Messages are then added to this room using a sorted set, where the score is the timestamp:

```bash
ZADD room:1:2 1615480369 "{'from': 1, 'date': 1615480369, 'message': 'Hello', 'roomId': '1:2'}"
```

A stringified JSON keeps the message structure and simplifies the implementation for this demo application.

The "General" room is populated with messages in the same way, using `room:0` as the sorted set key.

### How does Redis Pub/Sub enable real-time messaging?

After initialization, a Pub/Sub subscription is created:

```bash
SUBSCRIBE MESSAGES
```

Each server instance runs a listener on this channel to receive real-time updates. Every message is serialized to JSON, parsed, and then handled in the same manner as WebSocket messages.

Pub/Sub allows connecting multiple servers written in different platforms without taking into consideration the implementation details of each server.

### How does session and presence tracking work?

When a WebSocket connection is established, the server listens for these events:

- **Connection.** A new user connects. The user ID is captured and saved to the session (cached in Redis for persistence across server reloads). A global set tracks online users:

```bash
SADD online_users 1
```

After adding the user, a message is broadcasted to all clients to notify them that a new user has joined.

- **Disconnect.** Works similarly to the connection event, except the user is removed from the `online_users` set and clients are notified:

```bash
SREM online_users 1
```

- **Message.** When a user sends a message, it is broadcasted to other clients via Pub/Sub, which also delivers it to all connected server instances:

```bash
PUBLISH message "{'serverId': 4132, 'type':'message', 'data': {'from': 1, 'date': 1615480369, 'message': 'Hello', 'roomId': '1:2'}}"
```

The server id is included so that the originating server instance can discard its own messages (since it is also subscribed to the `MESSAGES` channel). The `type` field corresponds to the real-time event type (connect/disconnect/message), and the `data` field contains method-specific information.

## How is chat data stored in Redis?

Redis is used as the primary database for user and message data, and for sending messages between connected server instances.

The real-time functionality is handled by Socket.IO for server-client messaging. Additionally, each server instance subscribes to the `MESSAGES` Pub/Sub channel and dispatches messages as they arrive. The server transports Pub/Sub messages with a separate event stream (handled by Server Sent Events) to run the Pub/Sub message loop independently from Socket.IO signals.

Chat data is stored across various keys and data types:

- **User data** is stored in [hash sets](https://redis.io/docs/latest/develop/data-types/hashes/) where each entry contains `username` and `password` (hashed). Each user hash is accessed by key `user:{userId}`. User IDs are generated by incrementing the `total_users` key (`INCR total_users`).
- **Username lookups** are stored as separate keys (`username:{username}`) that return the `userId` for quick access, stored with `SET username:{username} {userId}`.
- **Chat rooms per user** are stored at `user:{userId}:rooms` as a [set](https://redis.io/docs/latest/develop/data-types/sets/) of room ids, added with `SADD user:{userId}:rooms {roomId}`.
- **Messages** are stored at `room:{roomId}` in a [sorted set](https://redis.io/docs/latest/develop/data-types/sorted-sets/) with the timestamp as the score, added with `ZADD room:{roomId} {timestamp} {message}`. Messages are serialized to an app-specific JSON string.

## How do you access chat data?

Get a user's data:

```bash
HGETALL user:2
```

Get online users:

```bash
SMEMBERS online_users
```

Get room ids for a user:

```bash
SMEMBERS user:2:rooms
```

Get the latest messages from a room:

```bash
ZREVRANGE room:1:2 0 50
```

This returns the 50 most recent messages from the private room between users 1 and 2.

## Next steps

- Build an [AI chatbot with Redis](/tutorials/howtos/solutions/vector/gen-ai-chatbot) for a modern conversational experience using vector search
- Explore the [social network application tutorial](/tutorials/howtos/socialnetwork/) to see how Redis powers user relationships and activity feeds
- Learn about [streaming LLM output with Redis Streams](/tutorials/howtos/solutions/streams/streaming-llm-output/) for another real-time Redis use case
- Try [.NET stream basics with Redis](/tutorials/develop/dotnet/streams/stream-basics/) for working with Redis Streams in C#
- Browse the chat app implementations in other languages:
    - [Chat app in .NET](https://github.com/redis-developer/basic-redis-chat-app-demo-dotnet)
    - [Chat app in Java](https://github.com/redis-developer/basic-redis-chat-app-demo-java)
    - [Chat app in Node.js](https://github.com/redis-developer/basic-redis-chat-app-demo-nodejs)
    - [Chat app in Go](https://github.com/redis-developer/basic-redis-chat-demo-go)
    - [Chat app in Ruby](https://github.com/redis-developer/basic-redis-chat-demo-ruby)
