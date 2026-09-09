---
title: "Redis Game Mechanics: Scoring"
linkTitle: "Redis Game Mechanics: Scoring"
url: "/blog/redis-game-mechanics-scoring/"
description: "First, let me warn you that I am not a game developer. So this post, which has been rattling around in my head for a number of years now, is partly a look at how a theoretical game would work with..."
date: 2020-04-01
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 1 April 2020 · updated 27 March 2025*

![Blog tile image](/images/blog/ed76c13eff5863c77ee648a9a09c49f508748b64-635x628.webp)

First, let me warn you that I am not a game developer. So this post, which has been rattling around in my head for a number of years now, is partly a look at how a theoretical game would work with Redis but also a metaphor to help readers understand how Redis works.

Phew!

With all that out of the way, let’s talk about implementing a game that is powered by Redis. We’re going to call this game *Super Redis Brothers—*it’s an action platformer connected to a central server. It stars Redisman, who needs to collect coins, use those coins for power-ups, and avoid being killed by radiation. Redisman started life as Sal, an Italian software developer who was bitten by a Redis module, turned into the stick-figure Redisman, and transported into this topsy-turvy world. Today we’re going to cover the aspects of scoring in *Super Redis Brothers* (aka collecting coins).

Setting aside all the other mechanics of the game, how do you manage the coin count of your character? You could use something as simple as a string to store and manipulate the coin count. Getting a coin could be something like:

> INCR pID123

Getting more than one point at a time would employ the INCRBY command, and losing points by either DECRBY or INCRBY with a negative increment. This is all fine and good, but what happens if you want to implement some sort of leaderboard or player-matching system? Using a simple string in Redis would not be very effective. What we need is a Sorted Set: this would allow us to pull a leaderboard quite efficiently, but can we use it to *also* track the scores of the individual players?

Let’s take a look!

## Collecting coins with a Sorted Set

Sorted Sets consist of members, each with a numerical score all stored under one key in Redis. Like normal Sets, members cannot have repeats, but it is possible to have multiple members with the same score. While using string/counter operations in Redis is a O(1) operation, write operations on Sorted Sets are O(log(n)) operations (where *n* is relative to the members in the set), so still respectable. All sorted set commands in Redis use the prefix “Z”.

Modeling the game mechanics of collecting coins, we’ll use a single key for all the players’ scores, the member is the player identifier and the score for this member is the number of coins that player has. As players collect coins, we’ll use ZINCRBY to increment the scores by the number of points collected. If a player has yet to collect a coin, then Redis will start with zero and increment accordingly. Note that sorted sets allow for a zero score (a distinct difference from a member that is not in the set) as well as a negative number. Let’s take a look at this visually.

(**Note:** Obviously, I am not a game artist!)

![](/images/blog/5b0d7e0c085a468368329a33769e2137e48cc7ca-1024x576.webp)

So, as Redisman comes in contact with the 10 coin, we useZINRCBY to increase the score of the member by 10. The same thing happens when Redisman comes in contact with the 20 coin, except with the appropriate value.

Also in the above graphic you can see the heads-up coin display. The initial value can be retrieved by using ZSCORE, which, when supplied with the key and member name will return the score. Upon collecting points, ZINCRBY will return the new score of the member, so the result can be used to update the coins heads-up display.

![](/images/blog/2196531637506ab346dc2e0a2259e838a25af974-1024x576.webp)

Let’s look at some more operations. Say we want to implement a power up that exchanges 10 coins for freezing enemies. This can be implemented by using the same ZINCRBY command, except with a negative increment argument. Another encounter might be something that reduces your coin count to zero (think Sonic the Hedgehog losing his rings). In this case we’d use ZADD with a score of 0. ZADD might seem counterintuitive in this situation, but think of ZADD as an upsert—this operation will update a score if the member already exists or add it with the new score when it doesn’t exist. Like ZINCRBY, ZADD will return the score, so we can also use this to update the heads up display.

Note that there’s a key oversimplification in the picture above: In the current setup, if Redisman has 0 coins and collides with the enemy freeze powerup, then his coins will drop to -10, which is probably not what we want. In pseudocode, we’ll be doing:

currentScore = ZSCORE scores pID1234

increment = -10

member = pID1234



//multiplying by -1 to invert negative numbers

If (currentScore >= increment*-1) {

Return ZINCRBY scores increment member

}

All the script pseudocode is doing is checking first if there are enough coins, and if so, then allow the negative increment to go through. This is a really great job for a simple Lua script:

> EVAL "if tonumber(redis.call('zscore',KEYS[1],ARGV[2])) >= (ARGV[1]*-1) then return tonumber(redis.call('zincrby',KEYS[1],ARGV[1],ARGV[2])) end" 1 scores -10 pID1234

If you’re not familiar with Lua this might be a little overwhelming, but is about as simple as you can get: get the score, make sure it won’t go below zero, if so, do decrement. The nice thing about Lua is that it runs atomicly. With this script there is no way for Redis to modify anything between the ZSCORE and the ZINCRBY. In a production scenario, you would probably use SCRIPT LOAD and EVALSHA instead of EVAL, but the principal is the same.

## Getting a leaderboard

Sorted Sets are a near-perfect data structure for leaderboards. In this example, we’re using the coins as the score in a Sorted Set, so the leaderboard functionality is practically built-in. Leaderboards are most often rendered from high score to low, so we’ll use the ZREVRANGE command.

> ZREVRANGE scores 0 9 WITHSCORE

This will show the top ten players with the highest scoring player first. It will keep track of ties as well, so it’s possible that the top ten will have 10 players all with the same score.

![](/images/blog/8cd2d6eff4d19c2a1f8913b909ee8a27e1f3e5dc-220x300.webp)

Showing the top ten might not be optimal in all situations, though, especially for new players with a low score. What a player probably wants to see is the people they are slightly better than and those who are slightly worse than them. To do this, first you want to get the rank of the player in question. You can use ZREVRANK, then feed the results into ZREVRANGE with the number of results you want above and below the player in question.

## Scaling and limits

You might have noticed that the examples in this post always refer to the same key *scores*. This highlights a flaw in this method when used in an actual game at scale. Because you are touching the same key over and over, you could create a very *hot key*. In clustered Redis, the key determines which shard or node the data is stored on. Activity on a single key will end up on the same machine until a resharding occurs. In this case, even if you had a cluster composed of many nodes and shards, all the scoring activity would be on a single shard, so you’ll eventually be limited by the resources of this shard. The number will be high, but could be reached in a heavily used game with frequent coin gathering or spending across multiple players.

There are a few solutions: You can go back to using INCR and a single key for each player, then using SCAN to periodically update a Sorted Set, but that would lose the real-time-ness of the leaderboard and create extra processes to make the Sorted Set update.

Another option would be to use a Redis Enterprise [Active-Active deployment](/active-active/) in a slightly unusual way. Active-Active in Redis Enterprise is designed primarily to facilitate geo-distribution by having multiple replica peer clusters spread over wide geographic area to reduce intrinsic latency: read and write to a nearby instance and Redis Enterprise takes care of any conflicts using the concept of [Conflict-free Replicated Data Types (CRDTs)](/docs/under-the-hood/). Using this method, you could just as easily set up several peer clusters then round-robin write to these different clusters. The writes would be accepted at the speed of the individual cluster then resolved to the different clusters. While this wouldn’t be *exactly* real-time, it would provide a seamless way of scaling the number of writes at a single key, especially if the workload has a bursting traffic pattern.

There you have it, remote score recording made easy with Redis. Sorted Sets make a really keen data structure for recording and displaying scores, both for individual users and in a leaderboard. Just keep in mind your strategies for managing potentially whitehot keys. Then go collect those coins!
