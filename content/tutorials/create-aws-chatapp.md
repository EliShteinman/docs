---
title: "How to Build a Real Time Chat application on Amazon Web Services using Python and Redis"
linkTitle: "How to Build a Real Time Chat application on Amazon Web Services using Python and Redis"
url: "/tutorials/create/aws/chatapp/"
description: "Real time chat messaging apps are surging in popularity exponentially. Mobile apps like WhatsApp, Facebook, Telegram, Slack, Discord have become “a part and parcel” of our life. Users are addicted..."
group: "For developers"
aliases:
- "/tutorials/create-aws-chatapp/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> Build a real-time chat app on AWS by pairing a Python/Flask backend with Redis Cloud Pub/Sub for instant message delivery and WebSockets (Socket.IO) for bi-directional client-server communication. Redis handles user sessions, room membership, message history (sorted sets), and online presence, while AWS hosts the infrastructure.

Real time chat messaging apps are surging in popularity exponentially. Mobile apps like WhatsApp, Facebook, Telegram, Slack, Discord have become “a part and parcel” of our life. Users are addicted to these live chat mobile app conversations as they bring a personal touch and offer a real-time interaction.

![Illustration of real-time chat messaging between users connected via Redis Pub/Sub](/images/site-mirror/96aaec75c9c21c5376bd91e0bf28cadc8a5a3513-379x252.webp)

There's been a rise in the number of social media apps that bring social elements to enable activities like collaboration, messaging, social interaction and commenting. Such activities require a real-time capability to automatically present updated information to users. More and more developers are tapping into the power of Redis as it is extremely fast & its support for a variety of rich data structures such as Lists, Sets, Sorted Sets, Hashes etc. Redis comes along with a Pub/Sub messaging functionality that allows developers to scale the backend by spawning multiple server instances.

> For the platform-agnostic version of this tutorial, see [How to build a Chat application using Redis](/tutorials/howtos/chatapp/).

## What you'll learn

- How to provision a Redis Cloud database on AWS
- How to use Redis Pub/Sub to broadcast messages across multiple server instances
- How to manage user sessions, rooms, and presence with Redis data structures
- How to connect a React + Socket.IO frontend to a Flask backend
- How Redis sorted sets store and retrieve chat message history

---

## Prerequisites

- Python 3.6+
- Node.js and Yarn
- A free [Redis Cloud account](https://redis.io/docs/latest/operate/rc/rc-quickstart/)
- Basic familiarity with Flask and React

## What will you build?

In this tutorial, we will see how to build a realtime chat app built with Flask, Socket.IO and Redis Cloud running on Amazon Web Services. This example uses pub/sub features combined with web-sockets for implementing the message communication between client and server.

## How do you set up the project on AWS?

### Step 1: Sign up for a free Redis Cloud account

[Follow this tutorial](https://redis.io/docs/latest/operate/rc/rc-quickstart/) to sign up for a free Redis Cloud account. If you already have an existing account, then all you need are your login credentials to access your subscription.

![Redis Cloud subscription creation page with AWS selected as cloud provider](/images/site-mirror/6c9116f3806d8ae73be8a9bf96cfcfa15e8f12d2-1047x791.webp)

Choose AWS as the Cloud vendor while creating your new subscription. While creating a new database, ensure that you set your own password. At the end of the database creation process, you will get a Redis Cloud database endpoint and port. Save these, you will need them later.

![Redis Cloud database details page showing the endpoint URL and port number](/images/site-mirror/8610ccc3d78a0d02c91ef16e24bf9e4325a3bcd7-1047x803.webp)

> **TIP**
>
> You don't need to create an AWS account for setting up your Redis database. Redis Cloud on AWS is a fully managed database-as-a-service trusted by thousands of customers for high performance, infinite scalability, true high availability, and best-in-class support.

### Step 2: Clone the repository

```bash
git clone https://github.com/redis-developer/basic-redis-chat-app-demo-python
```

### Step 3: Install the required packages

```bash
cd client
yarn install
```

### Step 4: Start the frontend

```bash
yarn start
```

```bash
You can now view client in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.1.9:3000
```

![Chat application login screen with username and password fields](/images/site-mirror/e57605fe3541c485ca5b5c9bcd3e016f7e9bb1f8-1044x1116.webp)

### Step 5: Install the required python modules

```bash
cd ..
pip3 install -r requirements.txt
```

### Step 6: Run the backend

```bash
python3 -m venv venv/
source venv/bin/activate
python3 app.py
```

```bash
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 220-696-610
(8122) wsgi starting up on http://127.0.0.1:5000
```

![Terminal output showing the Flask backend starting up with debugger active on port 5000](/images/site-mirror/df833d31c1162975f9b915e462de6cd41570d268-1047x744.webp)

## How does the chat server work?

The chat app server works as a basic REST API which involves keeping the session and handling the user state in the chat rooms (besides the WebSocket/real-time part). When the server starts, the initialization step occurs. At first, a new Redis connection is established and it's checked whether it's needed to load the demo data.

### How does the server initialize data in Redis?

For simplicity, a key with total_users value is checked: if it does not exist, we fill the Redis database with initial data. EXISTS total_users (checks if the key exists) The demo data initialization is handled in multiple steps:

#### Creating demo users

We create a new user id: INCR total_users. Then we set a user ID lookup key by user name: e.g.

```bash
SET username:nick user:1
```

And finally, the rest of the data is written to the hash set:

```bash
HSET user:1 username "nick" password "bcrypt_hashed_password".
```

Additionally, each user is added to the default "General" room. For handling rooms for each user, we have a set that holds the room ids. Here's an example command of how to add the room:

```bash
SADD user:1:rooms "0"
```

#### Populating private messages between users

First, private rooms are created: if a private room needs to be established, for each user a room id: room:1:2 is generated, where numbers correspond to the user ids in ascending order.

E.g. Create a private room between 2 users:

```bash
SADD user:1:rooms 1:2 and SADD user:2:rooms 1:2
```

Then we add messages for each conversation to this room by writing to a sorted set:

```bash
ZADD room:1:2 1615480369 "{'from': 1, 'date': 1615480369, 'message': 'Hello', 'roomId': '1:2'}"
```

We are using a stringified JSON to keep the message structure and simplify the implementation details for this demo-app. You may choose to use a Hash or JSON

#### Populate the "General" room with messages

Messages are added to the sorted set with id of the "General" room: room:0

### How does Redis Pub/Sub power real-time messaging?

After initialization, a pub/sub subscription is created: SUBSCRIBE MESSAGES. At the same time, each server instance will run a listener on a message on this channel to receive real-time updates.

Again, for simplicity, each message is serialized to JSON, which we parse and then handle in the same manner, as WebSocket messages.

Pub/sub allows connecting multiple servers written in different platforms without taking into consideration the implementation detail of each server.

### How are WebSocket connections and sessions handled?

When a WebSocket connection is established, we can start to listen for events:

- Connection. A new user is connected. At this point, a user ID is captured and saved to the session (which is cached in Redis). Note, that session caching is language/library-specific and it's used here purely for persistence and maintaining the state between server reloads.

A global set with online_users key is used for keeping the online state for each user. So on a new connection, a user ID is written to that set:

```bash
SADD online_users 1
```

Here we have added user with id 1 to the set online_users

After that, a message is broadcasted to the clients to notify them that a new user is joined the chat.

- Disconnect. It works similarly to the connection event, except we need to remove the user for online_users set and notify the clients: SREM online_users 1 (makes user with id 1 offline).
- Message. A user sends a message, and it needs to be broadcasted to the other clients. The pub/sub allows us also to broadcast this message to all server instances which are connected to this Redis:

```bash
PUBLISH message "{'serverId': 4132, 'type':'message', 'data': {'from': 1, 'date': 1615480369, 'message': 'Hello', 'roomId': '1:2'}}"
```

Note we send additional data related to the type of the message and the server id. Server id is used to discard the messages by the server instance which sends them since it is connected to the same MESSAGES channel.

The type field of the serialized JSON corresponds to the real-time method we use for real-time communication (connect/disconnect/message).

The data is method-specific information. In the example above it's related to the new message.

## How is the chat data stored in Redis?

Redis is used mainly as a database to keep the user/messages data and for sending messages between connected servers.

The real-time functionality is handled by Socket.IO for server-client messaging. Additionally each server instance subscribes to the MESSAGES channel of pub/sub and dispatches messages once they arrive. Note that, the server transports pub/sub messages with a separate event stream (handled by Server Sent Events), this is due to the need of running pub/sub message loop apart from socket.io signals.

The chat data is stored in various keys and various data types. User data is stored in a hash set where each user entry contains the next values:

- username: unique user name;
- password: hashed password
- Additionally a set of rooms is associated with user
- Rooms are sorted sets which contains messages where score is the timestamp for each message
- Each room has a name associated with it
- Online set is global for all users is used for keeping track on which user is online.
- User hash set is accessed by key user:{userId}. The data for it stored with HSET key field data. User id is calculated by incrementing the total_users key (INCR total_users)
- Username is stored as a separate key (username:{username}) which returns the userId for quicker access and stored with SET username:{username} {userId}.
- Rooms which user belongs too are stored at user:{userId}:rooms as a set of room ids. A room is added by SADD user:{userId}:rooms {roomId} command.
- Messages are stored at room:{roomId} key in a sorted set (as mentioned above). They are added with ZADD room:{roomId} {timestamp} {message} command. Message is serialized to an app-specific JSON string.

## How do you query chat data from Redis?

Get User HGETALL user:{id}.

```bash
HGETALL user:2
```

where we get data for the user with id: 2.

- Online users: SMEMBERS online_users. This will return ids of users which are online
- Get room ids of a user: SMEMBERS user:{id}:rooms. Example:

```bash
SMEMBERS user:2:rooms
```

This will return IDs of rooms for user with ID: 2

- Get list of messages ZREVRANGE room:{roomId} {offset_start} {offset_end}.

Example:

```bash
ZREVRANGE room:1:2 0 50
```

Which will return 50 messages with 0 offsets for the private room between users with IDs 1 and 2.

## Next steps

- [Build a chat application using Redis](/tutorials/howtos/chatapp/) – the platform-agnostic Python version of this tutorial
- [Build an AI chatbot with Redis vector search](/tutorials/howtos/solutions/vector/gen-ai-chatbot/) – add generative AI to your conversational app
- [Building a realtime chat app demo in .Net](https://github.com/redis-developer/basic-redis-chat-app-demo-dotnet)
- [Building a realtime chat app demo in Java](https://github.com/redis-developer/basic-redis-chat-app-demo-java)
- [Building a realtime chat demo in NodeJS](https://github.com/redis-developer/basic-redis-chat-app-demo-nodejs)
- [Building a realtime chat app demo in Go](https://github.com/redis-developer/basic-redis-chat-demo-go)
- [Building a Redis chat application demo in Ruby](https://github.com/redis-developer/basic-redis-chat-demo-ruby)
