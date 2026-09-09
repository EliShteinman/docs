---
title: "How to Build a Music Sharing App using NodeJS and Redis"
linkTitle: "How to Build a Music Sharing App using NodeJS and Redis"
url: "/blog/how-to-build-a-music-sharing-app-using-nodejs-and-redis/"
description: "Music is magic. It has the power to create new memories, friends, and unforgettable sensations."
date: 2022-03-15
blogCategories:
- "Tech"
authors:
- "Redis Growth Team"
lastmod: 2025-07-03
hidden: true
---

*By Redis Growth Team · Published 15 March 2022 · updated 3 July 2025*

![Blog tile image](/images/site-mirror/cc3edb43ac3dc921c78eb2d00d84c3401261d55c-772x550.webp)

Music is magic. It has the power to create new memories, friends, and unforgettable sensations.

All of us love music but for some, it’s a passion. Listening and sharing different tunes that tap into our emotions is a hobby that strengthens social bonds as well as pulls many friendships together.

But given that we live in a more globalized age where many of our friends are dotted across the globe, trying to organize anything social with them can be difficult.

Being both a music-lover and an innovator, Franco Chen took on this challenge by creating an application that allows users to listen, share and discover new music with their friends, irrespective of their location.

To maximize the user’s experience, the application needed to operate with a database that’s capable of transmitting, processing, and retrieving data in real time. With Redis, Franco was able to create a low latency application where commands and interactions between users were hyper-responsive.

Let’s take a look at how Franco brought this application to life. But before we go any further, we’d like to point out that we also have a range of exciting applications for you to check out on the [Redis Launchpad](https://launchpad.redis.com/).

[Click here to view video](https://www.youtube.com/embed/GHf4Ngl6Qfk)

1. What will you build?
1. What will you need?
1. Architecture
1. Getting started
1. Data Modeling
1. How data is accessed/stored
1. How it works

## 1. What will you build?

You’ll build a platform that allows you to listen to and share music with your friends online. The application works by creating private or public online rooms where you can invite people with different tastes to join in the experience.

In its purest sense, the application is a gateway to venturing deeper into different genres, tastes, and preferences through interacting with people who have a shared appreciation of music. Below we’ll show you how to create this application from scratch by highlighting the different components as well as walking you through each stage of the implementation process.

Ready to get started?

Ok, let’s get started!

## 2. What will you need?

[**Socket.IO**](https://socket.io/): Used as a Javascript library for real-time web apps.

[**Javascript**](https://www.javascript.com/): Used as the preferred programming language that allows you to make web pages interactive.

[**RedisJSON**](/json/)**: **A JSON data type for Redis that allows storing, updating and fetching JSON values from Redis keys

[**RediSearch**](/search/)**: **Used for querying, secondary indexing, and full text search for Redis.

[**Chakra UI**](https://chakra-ui.com/)**: **Provides you with basic building blocks that can help you build the front end of your application.

[**Redux**](https://redux.js.org/)**: **Used as an open source Javascript library for managing and centralizing application state.

[**Axios**](https://www.axios.com/)**: **Used as a promise-based HTTP client for Node.js and the browser.

[**Node.js**](https://nodejs.org/en/)**: **Used as an open source, cross-platform that executes JavaScript code outside of a web browser.

[**Express**](https://expressjs.com/)**: **Used as a flexible Node.js web application framework that provides a robust set of features for web and mobile applications.

## 3. Architecture

- The client requests and receives data from our Node.js server using both HTTP requests and Socket.IO.
- Redis stores all of the application’s data, both persistent and non-persistent data. This gives the application low latency for data retrievals, which creates a more fluid and responsive app. Achieving low latency is especially important for this application because there’s a lot of data moving between the server and the client.
- All Socket.IO data is sent through RedisPubSub, which minimizes the need to add more Node.js servers.

## 4. Getting started

**Prerequisites**

- Node v14.16.1
- npm v6.14.12
- Redis v6.2.3 with RediSearch v2.0 and RedisJSON v1.0
- Docker
- Docker Compose

### Step 1: Clone the repository

git clone https://github.com/spatialdj/frontend

### Step 2: Setting up a frontend

Use the [RedisMod](https://github.com/RedisLabsModules/redismod) docker image to set up the Redis modules. In the root directory of the frontend, type in the following code to install the frontend dependencies:

npm install

### Step 3: Setting up a backend

Go to the backend’s root directory and create a file called config.js with the following contents:

```python
export default {
  redisHost: 'localhost',
  redisPassword: 'your_password_for_redis_here',
  sessionSecret: 'somesessionsecret',
  passwordSaltRounds: 10,
  youtube_key: 'youtube_api_key'
}

```

Type in the following command to install backend dependencies:

npm install

Run the following command in the backend’s root directory:

npm start

### Step 4: Accessing the application

Your app should be running at localhost:3000

## 5. Data Modeling

**Room**

- Prefix: room:
- Type**: **HASH
- Fields:
  - messages: Redis key to message this room
  - id: ID of this room
  - json: JSON representation of this room (used because RediSearch doesn’t support JSON yet)
  - numMembers: The number of members currently in the room
  - description: The description of the room
  - name: The name of the room
  - private: (True | False) whether the room is searchable

genres: Genres the room is geared towards

Indices (RediSearch):

- name: TEXT
- description: TEXT
- genres: TAG
- numMembers: NUMERIC
- private: TAG

private: TAG

**Commands:**

Get JSON representation of this room

```python
HGET ${roomId} json

```

Create a new room or update room (not all fields required)

```python
HSET room:${roomId} id ${roomId} name ${name} description ${description} private ${private} genres ${genres} numMembers ${numMembers} json ${roomJson}

```

Check if a room exists (used when attempting to join room):

```python
EXISTS ${roomId}

```

Used for rooms page for searching:

```python
FT.SEARCH @name|description:(${searchQuery}) @private:{false} @genres:{${genres}} SORTBY numMembers DESC LIMIT ${offset} ${limit}:

```

**User queue**

- Prefix: queue:
- Type: LIST
- Data: A list of usernames of users in the queue of the associated room
- Commands:
  - RPUSH queue:${roomId} ${username}: Add user to queue or create queue
  - LRANGE queue:${roomId} 0 -1: Get all users in the queue
  - LREM queue:${roomId} -1, ${username}: Remove user from queue
  - LMOVE queue:${roomId} queue:${roomId} LEFT RIGHT: Cycle through queue (move user from front of queue to back of queue)

**Session**

- Prefix: sess:
- Type: STRING
- Data: Stores session data for authentication
- Commands:
  - SET sess:${sessionId} ${data}: Create a new session. Used by connect-redis
  - GET sess:${sessionId}: Get session data. Used by connect-redis
  - EXISTS sess:${sessionId}: Check if session exists. Used by connect-redis

**User**

- Prefix: user:
- Type: JSON
- Fields:
  - username: Username of user
  - password: Hashed and salted password using bcrypt
  - profilePicture: URL to an image
  - selectedPlaylist: User’s currently selected playlist
  - playlist: Playlist objects

Example playlist:

```python
"db168000-fa58-491b-81d0-1287d866fcf7": {
  "id": "db168000-fa58-491b-81d0-1287d866fcf7",
  "name": "Text playlist",
  "user": "exampleuser",
  "queue": [
      {
      "videoId": "TT4PHY0_hwE",
      "title": "Ekcle - Pearl Jigsaw",
      "thumbnails": {
          "default": {
          "url": "https://i.ytimg.com/vi/TT4PHY0_hwE/default.jpg",
          "width": 120,
          "height": 90
          }
      },
      "channelTitle": "Ekcle",
      "id": "2f7473db-2aec-4ec1-a2bd-623ed6b3ce48",
      "duration": 348000
      }
  ]
}

```

Example user:

```python
{
    "username": ...,
    "password": ...,
    "profilePicture": ...,
    "playlist": { ... },
    "selectedPlaylist": …
 }

```

- Commands:
  - Create a new user or update user data:

```python
JSON.SET user:${username} ${path} ${userJson}

```

- Get user data:

```python
JSON.GET user:${username} ${path}

```

**Messages**

- Prefix: message:
- Type: LIST
- Data: JSON-stringified objects, with fields id, timeSent, text, sender (which contains fields username and profilePicture)
- Commands:
  - Add a new message to the room’s message history:

```python
LPUSH message:${messagesId} ${data}

```

- Get message history of a room, starting with the newest and going backwards:

```python
LRANGE message:${messagesId} ${start} ${end}

```

**Socket**

- Prefix: socket:
- Type: STRING
- Data: The username that this socket belongs to
- Commands:
  - Create a new socket:

```python
SET socket:${socketId} ${username}

```

- Get associated username associated with socket:

```python
GET socket:${socketId}

```

- Delete socket:

```python
DEL socket:${socketId}

```

## 6. How the data is accessed or stored

- For users:
  - When a user registers, a user is created like:

```python
JSON.SET user:${username} . ${userJson}

```

- To log a user in, a new session is created:

```python
SET sess:${sessionId} ${data}

```

- To retrieve user information:

```python
JSON.GET user:${username} ${path}

```

- For sockets:
  - When a new socket is connected to the server and the request is authenticated (user is logged in), a new socket is created and the associated username is stored:

```python
SET socket:${socketId} ${username}

```

- When a socket is disconnected from the server, it is deleted:

```python
DEL socket:${socketId}

```

- For rooms:
  - When a room is searched for, RedisSearch is used to make the search:

```python
FT.SEARCH @name|description:(${searchQuery}) @private:{false} @genres:{${genres}} SORTBY numMembers DESC LIMIT ${offset} ${limit}

```

- When a new room is created, a room is created like this:

```python
HSET room:${roomId} id ${roomId} name ${name} description ${description} private ${private} genres ${genres} numMembers ${numMembers} json ${roomJson}

```

- When a room is updated, it is updated as seen below (all fields are optional):

```python
HSET room:${roomId} id ${roomId} name ${name} description ${description} private ${private} genres ${genres} numMembers ${numMembers} json ${roomJson}

```

- For queues:
  - When a user joins the queue, a queue is created/the user is added to the queue:

```python
RPUSH queue:${roomId} ${username}

```

- When it’s a user’s turn to play a song, the user is moved to the end of the queue:

```python
LMOVE queue:${roomId} queue:${roomId} LEFT RIGHT

```

- At the same time, the song played is moved to the end of the user’s playlist:

```python
song = JSON.ARRPOP user:${username} .playlist.${playlistId}.queue 0

```

```python
JSON.ARRAPPEND user:${username} .playlist.${playlistId}.queue song

```

- For playlists:
  - When a new playlist is created/updating an existing playlist:

```python
JSON.SET user:${username} .playlist.${playlistId} ${playlistJson}

```

- When a playlist is deleted:

```python
JSON.DEL user:${username} .playlist.${playlistId}

```

- When the user selects a playlist:

```python
JSON.SET user:${username} .selectedPlaylist ${playlistId})

```

- When a song is added to a playlist:

```python
JSON.ARRAPPEND user:${username} .playlist.${playlistId}.queue ${song}

```

- To get songs from a playlist:

```python
JSON.GET user:${username} .playlist.${playlistId}.queue

```

#### Code Example: Delete a Specific Song from a User’s Playlist

```python
const songs = JSON.parse(await jsonGetAsync(getUserKey(username), `.playlist.${playlistId}.queue`))
const songIndex = songs.findIndex(song => song.id === songId)
const success = songIndex !== -1
 
if (success) {
  songs.splice(songIndex, 1)
}
 
try {
  await jsonSetAsync(getUserKey(username), `.playlist.${playlistId}.queue`, JSON.stringify(songs))
} catch (error) {
  return res.status(400).json(error)
}

```

## 7. How it works

### Logging in or registering an account

On the homepage, you can log in or create a new account by clicking on either one of these icons on the navigation bar on the right-hand corner of the screen.

### Creating a room

Rooms are online communities that host a range of music depending on the criteria outlined by the host. Here you’ll be able to connect and interact with different people to discover new music based on your preferred tastes and genres.

Once you click on the ‘Create Room’ icon on the homepage, you’ll have to provide a description about the room you want to host. Here you can add a bit of character in the description to communicate the type of vibe and people you want to join in the room, along with the type of music that should be shared here.

### Creating a playlist

Friends who join the room will appear with their character icons.

Once everyone has joined, you’ll need to create a playlist where you can share music. Click on the arrow at the bottom left-hand side of the screen to begin this process. Next, a search bar that’s connected to YouTube will appear.

From here, you can search for the different songs you want to include and add them onto the playlist by clicking on the plus sign. RediSearch will identify and add songs to your playlist based on the phrases entered into the search engine.

### Listening and providing feedback to each other’s songs

When each song is playing, the music video will appear in the center of the screen. You’ll also see a chat window on the right-hand side of the screen where everyone in the room can share their opinion on each song.

At the bottom left-hand corner of the screen, you’ll be able to like or dislike a song. If over half of the people in the room dislike the song, then the application will skip to the next tune on the playlist.

## Conclusion: Achieving low latency to maximize the music experience

Transmitting reams of data between different components with hyper-efficiency was always going to be one of the biggest obstacles for Franco to overcome. In today’s digi-sphere, users expect commands and responses to be in real time and they expect nothing less.

This was especially important for this application, given the amount of data moving between the server and the client. Leveraging Redis’ advanced data capabilities gave the application low-latency for data retrievals, creating a completely fluid and responsive app that allowed users to listen, share, and comment on each other’s music *in real time*.

To get a more visual insight into the ins and outs of how this app was created, make sure to give Franco’s [YouTube video](https://www.youtube.com/watch?v=GHf4Ngl6Qfk) a watch.

If you’ve enjoyed this post, we have many more for you to dive into on the [Redis Launchpad](https://launchpad.redis.com/). Here you’ll have access to an excitingrange of applications that are having an impact on everyday life around the world.

These include real time vehicle tracking systems, an app that accelerate the blood donation process, split testing software, and much more.

Check them out. Be inspired. And join in the Redis fun.

## Who built this application?

**Franco Chen**

![](/images/site-mirror/483329e7c963b37b39aacfd0b7c33285645429e0-265x265.webp)


Franco has over nine years worth of experience in software engineering and is currently studying at the University of Waterloo. If you want to keep up to date with all of his projects then make sure to follow him on [GitHub here.](https://github.com/KevinLu)
