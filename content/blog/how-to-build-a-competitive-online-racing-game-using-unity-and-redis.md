---
title: "How to Build a Competitive Online Racing Game Using Unity and Redis"
linkTitle: "How to Build a Competitive Online Racing Game Using Unity and Redis"
url: "/blog/how-to-build-a-competitive-online-racing-game-using-unity-and-redis/"
description: "If you’re into gaming and love creating things, then you may take inspiration from this Launchpad App. By using Redis, Graham Pinsent created his very own online racing game where friends, family,..."
date: 2021-11-11
blogCategories:
- "How To and Tutorials"
- "Tech"
authors:
- "Growth Team"
lastmod: 2025-03-04
hidden: true
---

*By Growth Team · Published 11 November 2021 · updated 4 March 2025*

![Blog tile image](/images/blog/700cbfcaa20da331a192e12271d21af3f5507a93-772x520.webp)

If you’re into gaming and love creating things, then you may take inspiration from this Launchpad App. By using Redis, Graham Pinsent created his very own online racing game where friends, family, and colleagues can settle old scores and compete against each other for the finish line.

Just like any racing game, the ultimate objective is to get from A to B in the fastest possible time. Players are given a car, times are contested, and the winner is decided based on whoever can zoom through each lap the fastest.

But for this application to function optimally, data must be transmitted with hyper-efficiency to ensure player commands are carried out in real time. Failing to achieve this would create a disconnect between the player’s commands and their in-game vehicle, leading to a frustrating gaming experience.

To prevent this from happening, Graham leveraged Redis’ advanced capabilities to create an application where components are able to seamlessly transmit data between one another with maximum efficiency.

Let’s investigate how this was done. We also have a variety of exciting applications created by the Redis community for you to check out. Make sure to catch all of the action on the [Redis Launchpad](https://launchpad.redis.com/).



[Click here to view video](https://www.youtube.com/embed/Tq3yoIn4hLc)

1. What will you build?
1. What will you need?
1. Architecture
1. Getting started
1. How it works

## 1. What will you build?

You’ll build an online racing game that allows players to compete against each other using Redis. Below, we’ll go through each stage chronologically and highlight what components you need to bring this application to life.

Ready to get started? Ok, let’s dive straight in.

## 2. What will you need?

- [**NodeJS**](https://nodejs.org/en/)**: **used as an open-source, cross-platform that executes JavaScript code outside a web browser
- [**Express**](https://expressjs.com/)**: **used as a flexible Node.js web application framework that provides a robust set of features for web and mobile applications.
- [**Unity**](https://unity.com/)**: **used as a real-time development platform for video games
- [**RedisJSON**](/json/): implements ECMA-404 The JSON Data Interchange Standard as a native data type.

## 3. Architecture

![](/images/blog/696078645d700e4d4a9e067cfc99286158c360dc-1406x1036.webp)

1. After every 0.1 seconds, the position of each user’s car is sent to the Node JS server.
1. Node JS processes this data and sends it to the Redis database.
1. The server then sends the position of each user’s car and updates their position.
1. The time of each lap completed by a user will be sent to the Node JS server to be added to the live leaderboard in the Redis database.

## 4. Getting started

### Prerequisites

- Node.js
- NPM
- Unity 2020.3.4f1
- Redis with RedisJSON module

#### Step 1: Install RedisJSON

```python
$ docker run -d -p 6379:6379 redislabs/redismod

```

You can also use Redis Enterprise Cloud with RedisJSON module enabled as shown below:

![](/images/blog/c53c23d480e9952e36f6a33b530c2a3bf74da5a8-1600x999.webp)

#### Step 2. Clone the repository

```python
$ git clone https://github.com/redis-developer/Redis-Racing

```

#### Step 3. Set up Environmental Variable

Under the Node JS folder, create the .env file with details of the database.

```python
HOST=redis-12132.c72.eu-west-1-2.ec2.cloud.redislabs.comPASSWORD=XXXXXPORT=12132

```

#### Step 4. Install dependencies

Change directory to nodejs and execute the below CLI:

```javascript
npm install
```

#### Step 5. Run the server

```python
node index.js

```

#### Step 6. Monitor the Redis server

```python
redis-12132.c72.eu-west-1-2.ec2.cloud.redislabs.com:12132> monitorOK1633172585.553251 [0 122.167.151.216:50970] "json.get" "players"1633172587.637245 [0 122.167.151.216:51147] "auth" "9740535000"1633172587.637245 [0 122.167.151.216:51147] "info"1633172587.793245 [0 122.167.151.216:51147] "keys" "*"1633172587.793245 [0 122.167.151.216:51147] "json.get" "players"


```

Finally, you can either build the game using Unity, or just press play inside the project.

![](/images/blog/d100654121532db298b87eea148423fe9d061716-1600x475.webp)

![](/images/blog/adfc876974696372972e3ee7652eb10c014f8001-1600x580.webp)

Open the web browser https://IP: 3000 to access the game.

![](/images/blog/e5522eaac591c7afd55747a50d2f8d4e96ef7d09-1552x1300.webp)

![](/images/blog/c74770c8e07d6e3ab66a0b471e248d47071b2252-1600x1295.webp)

## 5. How it works

Once a player selects their name and is connected to the server, their position on the map is sent to the Redis database. As the player navigates through the track, their position is being updated 10x/second. This is what the player data might look like:

```python
"players" = {
    "_James" : {"name":"James","xPos":1,"yPos":10,"zRot":-90,"lastping": "2021-05-11T21:44:11.640Z"},
    "_Ryan" : {"name":"Ryan","xPos":20,"yPos":80,"zRot":180,"lastping": "2021-05-11T21:45:11.790Z"},
    "_Paul" : {"name":"Paul","xPos":-2,"yPos":180,"zRot":61,"lastping": "2021-05-11T21:45:15.110Z"}
}

```

Every time a player makes a POST to the server with their new location, the response from the server includes all players current positions and data. This is then used to place everyone else’s car on the track for you to see as you are driving. Linear interpolation is used to smoothen the movement, making it look faster than 10 updates per second.

Once a player crosses the finish line, their time and name are sent to the server. Below is an example of track time data:

```python
"leaderboard" = {
    "_James" : {"name": "James","laptime": 37.19,"created": "2021-05-11T21:56:55.440Z"},
    "_Ryan" : {"name": "Ryan","laptime": 50.56,"created": "2021-05-11T21:57:35.220Z"},
    "_Paul" : {"name": "Paul","laptime": 45.11,"created": "2021-05-11T21:58:51.120Z"}
}

```

This data is used to create a live leaderboard that everyone can see as they race against each other for the fastest time possible. When any car crosses the finish line, the client will request for the new leaderboard data from the server.

---

### Features

#### Choose your name

When a player first starts the game, they’ll be prompted with an option to choose their name. Once they do this and press start, the game client sends a POST request to the server with their name. The server will then carry out checks on the name to validate it, including verifying whether an existing name is already taken.

This is done by obtaining every player’s JSON from the Redis database and pushing it into an array to loop over. When this happens, the server will be checking their name against the data.

```python
client.json_get("players", function (err, results) {
    const currentplayers = Object.values(JSON.parse(results))
    currentplayers.forEach(function (item, index){
        playernames.push(item.name)
    })

```

And finally, after the validation, the server will send a success response back to the client. If the name was invalid then the server will send a failure response.

#### Update Position

Once the player has spawned into the game, a POST request is sent to the server every tenth of a second. The request includes their name, position, and rotation. As soon as the server receives the request, it will add the current time into the JSON then register it in the Redis database.

```python
const namekey = `_${myjson.name}`
client.json_set("players",namekey, JSON.stringify(data))

```

When the player’s new position has been set, the server will then obtain every player’s JSON from the Redis database and send it as a response back to the game.

```python
client.json_get("players", function (err, results) {
    res.send(Object.values(JSON.parse(results)))
})

```

As soon as the game client receives the data, it can update the position of every connected player.

#### Leaderboard

When a player finishes a lap, a POST request will be sent to the server. The information in this request will include the player’s name and the time it took for them to finish the lap. At this point, the server will then automatically try to retrieve their previous lap time(s) from the Redis database.

```python
const namekey = `_${myjson.name}`
client.json_get("leaderboard", `.${namekey}`, function (err, results) {

```

The server then checks whether they had an old-time or if this is the player’s first lap time that they’re submitting. If the player has an old-time, it will compare it with the new time to see if it’s faster. If it is, then it will register the new time into the leaderboard JSON in the database.

```python
if (oldtime) {
    oldtime = JSON.parse(oldtime)
    if (myjson.time < oldtime.laptime) {
        client.json_set("leaderboard", namekey, JSON.stringify(data))
    }
}

```

If it’s their first time, their name and lap-time will be registered into the leaderboard.

```python
else {
    client.json_set("leaderboard", namekey, JSON.stringify(data))
}

```

And finally, the server will obtain all of the leaderboard’s data and send the response back to the game client.

```python
client.json_get("leaderboard", function( err, results) {
    res.send(Object.values(JSON.parse(results)))
})

```

The game client can then form the leaderboard with the data.

#### Remove disconnected players

After every 30 seconds, the server will obtain every player’s JSON data from the Redis database.

```python
client.json_get("players", function (err, results) {

```

When a player closes their game, the game client will stop sending update position requests. The server will loop through all players to check if their last update was more than thirty seconds ago. If it was, then they are deleted from both the player’s JSON and the leaderboard JSON.

```python
playerdata.forEach(function (item, index) {
  var namepath = `._${item.name}`
  var seconds = Math.floor((new Date() - Date.parse(item.lastping)) / 1000);
  if (seconds > 30) {
    client.json_del('players', namepath)
    client.json_del('leaderboard', namepath)
    console.log(`Removed ${item.name}`)
  }
});

```

The same check happens to the game client. If their last update was received more than 30 seconds ago, then their car object will be destroyed.

```python
if (lastPing.AddSeconds(30) < DateTime.Now) {
    isAFK = true;
    GameManager gameManager = GameObject.Find("GameManager").GetComponent<GameManager>();
    gameManager.StartGetLeaderboard();
    gameManager.RemovePlayer(this);
    Destroy(gameObject);
}

```

When you first start the game, you’ll have the opportunity to choose your player’s name as seen below. Once you enter your name and press start, the game client will then send this information as a POST request to the server.

![](/images/blog/6d83dc0ca10e8e6badbd036a82e34cad14f8c130-1222x756.webp)

The server will then perform various checks on the name to validate it. For example, it will check whether or not the name is already taken. This validation process happens by getting every player’s JSON from the Redis database to then push it into an array to loop over and check their name against the data.

```python
client.json_get("players", function (err, results) {
    const currentplayers = Object.values(JSON.parse(results))
    currentplayers.forEach(function (item, index){
        playernames.push(item.name)
    })

```

Once the validation has been completed, the server will send a success response back to the client. If the name was invalid then it will send a failure response back.

#### Updating a position

Once a player has spawned into the game, a POST request will be sent to the server every 0.1 seconds. The request will include their name, position, and rotation. After the server receives the request, it will add the current time into the JSON and set the JSON in the Redis database.

[Gist](https://gist.github.com/Hkazanci93/34a03f03883e85a59a4545c1471c83f2)

As soon as the client receives the data, it will update the position of every player that’s connected to the game.

#### Updating the leaderboard

Whenever a player finishes a lap, a POST request is sent to the server that includes important information, such as their name and the time it took to finish the lap. Prior to this, the server will access and include a player’s previous lap times from the Redis database.

```python
const namekey = `_${myjson.name}`
client.json_get("leaderboard", `.${namekey}`, function (err, results) {

```

At this point, the server checks whether or not this is the player’s first lap time that they’re submitting. As you’d expect, if the player already has a previous lap-time recorded then the server will compare it with the new time to see if it’s faster. If it is, then it will set the new time into the leaderboard JSON in the database.

```python
if (oldtime) {
    oldtime = JSON.parse(oldtime)
    if (myjson.time < oldtime.laptime) {
        client.json_set("leaderboard", namekey, JSON.stringify(data))
    }
}

```

However, if it’s their first time, then their name and time will be recorded and inserted into the leaderboard.

```python
else {
    client.json_set("leaderboard", namekey, JSON.stringify(data))
}

```

And finally, the server will access the entire leaderboard and send the response back to the game client.

```python
client.json_get("leaderboard", function( err, results) {
    res.send(Object.values(JSON.parse(results)))
})

```

At this point, you’ll be able to create the leaderboard with the data.

#### Removing disconnected players

In this application, the server will receive every player’s JSON data from Redis after every 30 seconds.

```python
client.json_get("players", function (err, results) {

```

When a player closes their game, the game client will stop sending updated position requests. This is significant because the server carries out its own checks to see whether if each player is still connected to the game.

The server achieves this by looping through all players to see whether if their last update was more than 30 seconds ago. If it was, then these players will be deleted from both the players JSON and the leaderboard JSON.

```python
playerdata.forEach(function (item, index) {
  var namepath = `._${item.name}`
  var seconds = Math.floor((new Date() - Date.parse(item.lastping)) / 1000);
  if (seconds > 30) {
    client.json_del('players', namepath)
    client.json_del('leaderboard', namepath)
    console.log(`Removed ${item.name}`)
  }
});

```

The same check happens on the game client. If their last update was received more than 30 seconds ago, then their car object will be destroyed.

```python
if (lastPing.AddSeconds(30) < DateTime.Now) {
    isAFK = true;
    GameManager gameManager = GameObject.Find("GameManager").GetComponent<GameManager>();
    gameManager.StartGetLeaderboard();
    gameManager.RemovePlayer(this);
    Destroy(gameObject);
}

```

## Conclusion: Ready, Steady…Redis!

Racing games remain a hot favorite in the gaming industry. First we had Mario Kart, then we had Need for Speed, and now we have something that *you can create* on your own laptop. With Redis, this application is able to operate in real-time and maximize the gaming experience by allowing users to battle it out without any lags.

But that’s not all…

Innovative programmers from all around the world are tapping into the wonders of Redis to create phenomenal applications that are having their own impact on society.

Whether you just want to have a bit of fun or are looking to build something that’ll improve everyday life, Redis can help bring your project ambitions come to life. Make sure to [check out the Redis Launchpad ](https://launchpad.redis.com/)for more inspiration.

Or if you want to learn more about how this application was made, then you can watch the full YouTube video by [clicking here](https://launchpad.redis.com/?id=project%3ARedis-Racing).

[Watch the video](https://launchpad.redis.com/)

## Who built this application?

### Graham Pinsent

![](/images/blog/4b95073ab95c5ca1014d7031b5b2c43f82879a65-800x800.webp)

Graeme is a DevOps engineer who operates in the gambling and sports betting industry. Make sure to head over to his [GitHub page](https://github.com/PerryGraham/Redis-Racing) to see what other projects he’s been involved in.
