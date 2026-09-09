---
title: "How to build a Real-Time Geo-distributed Multiplayer Top-down arcade shooting game using Redis"
linkTitle: "How to build a Real-Time Geo-distributed Multiplayer Top-down arcade shooting game using Redis"
url: "/blog/how-to-build-a-real-time-geo-distributed-multiplayer-top-down-arcade-shooting-game-using-redis/"
description: "As the gaming industry continues to grow in size, the need to create a unique and dynamic user experience has become even more mandatory. Because of its fandom, businesses have to maximize the..."
date: 2021-10-01
blogCategories:
- "Tech"
authors:
- "Growth Team"
lastmod: 2025-03-27
hidden: true
---

*By Growth Team · Published 1 October 2021 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/77ca578c79c1cc151e88e2e1fc72fa6ad01aa18f-772x520.webp)

As the [gaming industry ](/industries/gaming/)continues to grow in size, the need to create a unique and dynamic user experience has become even more mandatory. Because of its fandom, businesses have to maximize the multiplayer gaming experience to drive customer acquisition and retention. However, companies are faced with a number of obstacles when trying to scale multiplayer games, all of which can be solved through Redis.

Personalized interactions and high-speed reactions are at the heart of creating a unique user experience. Redis provides game publishers with [a powerful database](/docs/redis-enterprise-for-gaming/) that can support low-latency gaming use cases. Recently a Launchpad App built a unique application that could have only been deployed by Redis due to its unmatched speed in transmitting data.

This is crucial because participants play from all around the world. Interactions between players must be executed in real-time to support gameplay, requiring the latency to be less than one millisecond.

Let’s take a deep dive into how this was done. But before we do so, make sure to have a browse through the exciting range of different applications that we have on the [Launchpad](https://launchpad.redis.com/).

[Click here to view video](https://www.youtube.com/embed/EOwTOVoIEp4)

1. What will you build?
1. What will you need?
1. Architecture
1. Getting started
1. How to use the RedisGears function list
1. Conclusion: overcoming geographical barriers with phenomenal active

## 1. What will you build?

You’ll build a real-time Geo-distributed multiplayer top-down arcade shooting game using Redis. The backbone of the application is Redis, for it acts as an efficient real-time database that enables you to store and distribute data.

As we progress through each stage chronologically, we’ll unpack important terminology as well as each Redis function.

## 2. What will you need?

Let’s identify the different components you’ll need to create this game. The application consists of 3 main components:

- [Redis:](https://redis.io/) used as a database, cache, and message broker.
- [RedisGears](/modules/redis-gears/): defines game function and enables interactions with the game state and user events
- [RediSearch](https://www.javascript.com/): enables robust querying experience
- [JavaScript client](https://www.javascript.com/): captures user inputs and sends inputs to the backend. Also uses phaser 3 engine for rendering and physics simulations 3 game engine
- [NodeJS backend](https://nodejs.org/en/) and [WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket): Communication interface between users and Redis. Primarily used for building the game logic and enabling Redis API

## 3. Architecture

![](/images/site-mirror/007312501a84d5f71eebb97225337a1768775cc9-1024x388.webp)

The main idea of this multiplayer game is to keep it real-time and distribute it geographically. That means that all the instances in your cluster should be updated so that you don’t run out of synchronization. Now let’s take a look at the architecture.

- NodeJS forms a communication interface between the players and the Redis database.
- JavaScript and Phaser 3 library is used for rendering the game state and passing user input to Redis via NodeJS
- RedisGears is used to enable interaction with the Game State and user events

## 4. How it works

![](/images/site-mirror/e04baf51fe89e5e84681f26b487b27b1b8da7f36-1024x381.webp)

Now let’s take a look at the flow of the architecture.

- Everything begins by using Javascript, which then flows through to Node JS (or WebSocket), in-between the user and backend which is Redis.
- Players manoeuvre their character through the terrain by using the arrow keys
- Missiles are launches at enemies by clicking the mouse button
- All of these commands are being sent through WebSocket to Redis
- RedisGears parses these commands and updates the state by determining whether the command is valid or not
- This will distribute the commands back to other users and players
- If the command is wrong, RedisGears will remove certain players from the game

![](/images/site-mirror/85c0d9e28d7b885374e6fde0182fd4068b51bdd5-1024x606.webp)

- User navigates through the terrain using the arrow keys and fires missiles at opponents by clicking on the mouse
- When the user carries out an action, these commands are sent to RedisGears via the WebSocket.
- Valid commands will then be redistributed to other users via Redis Streams.

![](/images/site-mirror/99def42397329cd816d9d0d609ba6455efc85fd7-1024x588.webp)

- NodeJS forms a communication channel between the user and Redis
- A user is able to find a game and join it.
- It allows users to invite other users to join the game
- In case, the game is not available, it allows users to create a new game too.
- RedisGears in turn enables the interaction with the game state and user events
- RedisGears parses the data and determines where they should be distributed based on the user commands.
- RediSearch allows users to search for a game

## 5. Getting started

### Prerequisites

- Docker
- Docker-compose

### Clone the repository

```python
git clone https://github.com/redis-developer/online_game/

```

Under the root of the repository, you will find a Docker compose YAML file:

```python
version: '3.8'
services:
  redis:
    build:
      dockerfile: ./dockerfiles/Dockerfile_redis
      context: .
    environment:
      - ALLOW_EMPTY_PASSWORD=yes
      - DISABLE_COMMANDS=FLUSHDB,FLUSHALL,CONFIG,HSCAN
    volumes: 
      - ./redis/redis_data:/data
      - ./redis/redis.conf:/usr/local/etc/redis/redis.conf
    ports:
      - 6379:6379
    restart: always
  backend:
    build:
      dockerfile: ./dockerfiles/Dockerfile_node_backend
      context: .
    environment:
      - NODE_ENV=development
    volumes: 
      - ./game_conf.json:/game_config/game_conf.json
    ports:
      - 8080:8080
      - 8082:8082
    restart: always

```

Under this YAML file, there are two major services that are defined – redis and backend.

**Below is how the Dockerfile for Redis looks like:**

```python
FROM redislabs/redismod:latest
COPY ./redis/redis_functions /functionsCOPY ./redis/start_redis.sh /start_redis.sh
RUN chmod +x /start_redis.sh
ENTRYPOINT ["bash"]CMD ["/start_redis.sh"]

```

**Below is the Dockerfile for NodeJS backend:**

```python
FROM node:15.14WORKDIR /home/node/app
COPY ./app/package*.json ./RUN npm install --only=production
COPY ./app .CMD [ "npm", "start" ]

```

**Bringing up the services**

Ruin the following commands from the online_game directory

```python
docker-compose up

```

You access the online WebServer via [http://127.0.0.1:8080](http://127.0.0.1:8080)

## 6. How to use the RedisGears function list

There are three RedisGears functions that each have their own set of sub-functions:

- [database_functions.py](https://github.com/redis-developer/online_game/blob/main/redis/redis_functions/database_functions.py)
- [game_functions.py](https://github.com/redis-developer/online_game/blob/main/redis/redis_functions/game_functions.py)
- [player_functions.py](https://github.com/redis-developer/online_game/blob/main/redis/redis_functions/player_functions.py)

## find_game function

Once a user starts the game, the first thing the user will do is search for a game using RediSearch. If the game is present then that person will try and join the game. If not then RedisGears is triggered to create a new game. See the function below

```python
def find_game(user_id):
    game = query()
     if game != [@] and type(game) == list:
         return game[1].split(":") [1]

     # CREATE A NEW GAME IF THERE ARE NO GAMES
     game = execute("RG.TRIGGER", "create_new_game", f"USER:{user_id}")

     if game:
     return game[@]

   (
        GB( 'CommandReader ' )
        .map(lambda x: find_game(*x[1:]))
        .register(trigger=self.command_name
   )


```

Once the user has created a new game, then other players will join and everyone will be able to play.

## create_new_game function

```python
class CreateNewGameFunctionBuilder(BaseFunctionBuilder):
    def __init__(self):
        super().__init__(command_name='create_new_game')


    def register_command(self):
        """
            Registers create_new_game redis gears fucntion to redis.
            For each generate_new_game call creates a new HASH under game namespace:
                GAME:[game_id] owner [user_id], secret [hash], private [bool], playercount [int]
            Returns:
                redis key [GAME:game_id]
            Trigger example:
                RG.TRIGGER create_new_game USER:123 1 secret123
        """

        def subcall(user, private=0, secret=""):
            game_id = uuid.uuid4().hex
            key = f"GAME:{game_id}"

            execute("HSET", key, "owner", user, "secret", str(secret), "private", int(private), "playercount", 0)
            execute("EXPIRE", key, SECONDS_IN_DAY)

            return game_id
        (
            GB('CommandReader')
            .map(lambda x: subcall(*x[1:]))
            .register(trigger=self.command_name, mode='sync')
        )

```

If no game is present, then RedisGears is triggered to create a new one.

Once the user has created a new game, then other players will join and everyone will be able to play.

## create_new_user function

```python
class CreateUserFunctionBuilder(BaseFunctionBuilder):
    def __init__(self):
        super().__init__(command_name='create_new_user')
        

    def register_command(self):
        """
            Registers create_new_user redis gears fucntion to redis.
            For each create_new_user call creates a new HASH under user namespace:
                USER:[u_id] name [str], settings [str], secret [str]
            Returns:
                redis key [USER:u_id]
            Trigger example:
                RG.TRIGGER create_new_user hhaa Player1 '' aahh
        """

        def subcall(user_id, name, settings='{}', secret=""):
            key = f"USER:{user_id}"

            execute("HSET", key, "name", name, "setttings", settings, "secret", str(secret))
            execute("EXPIRE", key, SECONDS_IN_DAY * 30)

            return key
        (
            GB('CommandReader')
            .map(lambda x: subcall(*x[1:]))
            .register(trigger=self.command_name)
        )

```

This function adds a new player to the game and it has the same approach as Create_new_game function. Again, RedisGears is triggered which then creates a new user

## join_game function

```python
class JoinGameFunctionBuilder(BaseFunctionBuilder):
    def __init__(self):
        super().__init__(command_name='join_game')

    def register_command(self):
        """
            Determines best public server to join to.
                 - Assings User to the Game.
                 - Increments playercount
            Arguments:
                user, game, secret (optional)
            Returns:
                redis key [GAME:game_id]
            Trigger example:
                RG.TRIGGER join_game user1 game1
                RG.TRIGGER join_game user1 game1 secret123
        """

```

When a user joins the game, RedisGears is triggered to enable the Join_game function. This also increments the player count of the game_instance (HINCRBY).

## leave_game function

```python
class LeaveGameFunctionBuilder(BaseFunctionBuilder):
    def __init__(self):
        super().__init__(command_name='leave_game')

    def register_command(self):
        """
            Determines best public server to join to.
                 - Removes USER to the ROOM.
                 - Decrements playercount
                 - Publishes a notification
            Arguments:
                user, game
            Returns:
                None
            Trigger example:
                RG.TRIGGER leave_game user1 game1
        """

        def subcall(user_id, game_id, secret=None):
            execute("HDEL", f"GAME:{game_id}", f"USER:{user_id}")
            execute("HINCRBY", f"GAME:{game_id}", "playercount", -1)

        (
            GB('CommandReader')
            .map(lambda x: subcall(*x[1:]))
            .register(trigger=self.command_name, mode='sync')
        )

```

When a user is eliminated from the game or chooses to leave, RedisGears is triggered to facilitate the process. This also automatically reduces the player count and automatically creates a notification to confirm that this action has been completed.

## player_actions functions

During gameplay, players will fire missiles to eliminate other competitors. When a player fires a missile, the below sub-function is then triggered:

```python
def click(self, game_id, user_id, x, y, o):
        """
        Handle player main key pressed event.
        """
        player = self.games_states[game_id]["players"][user_id]

        self.games_states[game_id]["projectiles"].append({
            "timestamp": self.ts,   # server time
            "x": player["x"] if player['x'] is not None else 9999,
            "y": player["y"] if player['y'] is not None else 9999,
            "orientation": o,       # radians
            "ttl": 2000,            # ms
            "speed": 1,             # px/ms
            "user_id": user_id
        })

        return True

```

If a missile hits another player, then that user will be eliminated from the game. The below code determines whether a player has been hit by a missile.

```python
def hit(self, game_id, user_id, enemy_user_id):
        """
        Determines if the projectile has hit a user [user_id]
        Extrapolates projectile position based on when projectile has spawned, and the time now.
        Publishes a hit even if target is hit.
        """
        projectiles = self.games_states[game_id]["projectiles"]
        player = self.games_states[game_id]["players"][enemy_user_id]

        for projectile in projectiles:
            time_diff = self.ts - projectile['timestamp']
            orientation = float(projectile["orientation"])
            x = projectile['x'] + ( math.cos(orientation) * (projectile['speed'] * time_diff) )
            y = projectile['y'] + ( math.sin(orientation) * (projectile['speed'] * time_diff) )


            if abs(player['x'] - x < 50) and abs(player['y'] - y < 50):
                self.games_states[game_id]['players'][projectile['user_id']]['score'] += 1
                execute('PUBLISH', game_id, f"hit;{enemy_user_id}")
                return False
        return False

    def respawn(self, game_id, user_id, x, y):
        player = self.games_states[game_id]["players"][user_id]

        player["respawns"] = player["respawns"] + 1
        player["x"] = x
        player["y"] = y

        return True

```

## Player_actions Stream Reader explained

1. The client connects to node.js WebSocket server.
1. The user is then being subscribed SUBSCRIBED to the game_id Redis PubSub channel.3
1. From there on in, all channel messages the user is subscribed to (on the backend) are also forwarded to the WebSocket (to the frontend).
1. MESSAGE_EVENT_HANDLERS object stores event -> function mapping, and on an incoming message one of the message event functions is being called (see function list below).

## List of Client message event handler:

| MESSAGE_EVENT_HANDLERS | Explanation |
|---|---|
| p (pose) args: [user_id, x, y, orientation]; | A client receives a user_id position update |
| c(click) args: [user_id, x (where it was clicked at), y (where it was clicked at), angle (from the player position to click position)]; | A client receives user_id click event |
| r (respawn) args: [user_id, x, y]; | A client receives user_id has respawned |
| l (leave) args: [user_id]; | A client receives user_id has left the game |
| j (join) args: [user_id, x, y] | A client receives user_id has joined the game, and user_id has spawned in the (x, y) position |
| uid (user id) args: [is_valid]; | A client receives the response whether it is possible to find ‘log the user in |
| gid (game id) args: [is_valid]; | A client receives if the user is part of the game (is user authorized) |
| hit args: [user_id]; | A client receives a message that user_id has been hit / client can remove user_id from rendering it |

## RediSearch

RediSearch indexes are registered on container startup in the redis/start_redis.sh

Created Redis Search indexes:

```python
FT.CREATE GAME ON HASH PREFIX 1 GAME: SCHEMA owner TEXT secret TEXT private NUMERIC SORTABLE playercount NUMERIC SORTABLE

FT.CREATE USER ON HASH PREFIX 1 USER: SCHEMA name TEXT settings TEXT secret TEXT

```

## Query to find a game:

```python
FT.SEARCH "GAME" "(@playercount:[0 1000])" SORTBY playercount DESC LIMIT 0 1

```

## Conclusion: Overcoming geographical barriers with phenomenal active-active

As with any Redis database, one of the most adored assets is its ability to transmit data between components with unrivalled efficiency. Yet in this application, without the exceptional latency speed that Active-Active provides, the game would simply not be able to function.

Gameplay is purely interactive, where users from all around the world react and fire missiles at other players. From start to finish, RedisGears deploys a sequence of functions based on the chronological order of the application set-up.

This is done with ease due to the efficiency of RedisGears which enables an active-active geo-distributed top-down arcade shooter application to be deployed.

If you want to find out more about this exciting application you can see the full app on the [Redis Launchpad](https://launchpad.redis.com/?id=project%3Aonline_game). Also make sure to check out all of [the other ](https://launchpad.redis.com/)[*exciting *](https://launchpad.redis.com/)[applications](https://launchpad.redis.com/) we have available for you.

[Watch the video](https://launchpad.redis.com)

## Who created this application?

Jānis Vilks

Jānis is a Big Data engineer who works at Shipping Technology.

If you want to discover more about his work and the projects he’s been involved in, then make sure to [visit his GitHub profile here](https://github.com/VilksJanis).
