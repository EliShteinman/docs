---
title: "The Top 3 Game Changing Redis Use Cases"
linkTitle: "The Top 3 Game Changing Redis Use Cases"
url: "/blog/the-top-3-game-changing-redis-use-cases/"
description: "Two weeks ago the Redis team had exhibited in the 2014 Game Developers Conference. As the name suggests, the conference was packed with game developers and I had great discussions about how Redis..."
date: 2014-04-03
blogCategories:
- "Tech"
authors:
- "Itamar Haber"
lastmod: 2026-08-14
hidden: true
mirrored: true
---

*By Itamar Haber, Technology Evangelist · Published 3 April 2014 · updated 14 August 2026*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

Two weeks ago the Redis team had exhibited in the 2014 Game Developers Conference. As the name suggests, the conference was packed with game developers and I had great discussions about how Redis is used in building games that scale. Here’re the top use cases for Redis in the multi-player gaming industry.

### 1st Place: Leaderboards

If there’s one Redis feature that’s a definite blockbuster with game developers it’s its sorted sets. Almost every online multi-player game sports at least one ranked list of its players, and most [manage multiple such leaderboards](/solutions/leaderboards/) concurrently. For example, an online FPS could rank players by the number of frags and keep a global leaderboard as well as regional and per tournament ones. Such lists are constantly hit with updates and are paged through frequently to display their contents.

Redis practically lends itself to the task – to update a leaderboard just [ZADD](https://redis.io/commands/zadd) the player’s identifier. Want to get a player’s rank? [ZRANK](https://redis.io/commands/zrank) it! And getting the top n players or paging through the leaderboard is a simple matter of [ZRANGE](https://redis.io/commands/zrange).

### 2nd Place: Session Management

[Session management is key to any online application](/solutions/session-management/), and games are no different in that respect. If anything, realtime games’ session management requirements are stricter than those of the average shopping or social site. While shopping carts and social streams updates can take a couple of seconds to complete, the success of a game often depends on its responsiveness and accuracy of the players current stats (e.g. hit points, buffs, etc…).

Managing sessions in Redis is a wildly-popular practice and the efficient hash data structure makes it easy-peasy to manage (i.e. [HINCRBY](https://redis.io/commands/HINCRBY)) a player’s counters.

### 3rd Place: Player Profile

Another piece of information that gets hit quite heavily is the player’s profile. Depending on the game, the profile consists of any number of odd ends that the player is associated with. Although the profile is updated less frequently (at least compared to player rank and session data), it is still accessed often both by the narcissist player and by his peers/opponents. Again, Redis hashes make this a breeze.

### Perfect Combos

I’m a huge fan of polyglot persistence and I certainly got my fix in that show. A lot of game developers that I spoke with had reported using Redis to augment the capabilities of another datastore – MySQL, Cassandra and MongoDB being the common technologies in use. The following quote from of the developers really caught my fancy: “everything numerical goes into Redis, the rest to Cassandra”.

Want to share your story? Have any questions or feedback? [Email](mailto:itamar@redis.com) or [tweet](https://twitter.com/@itamarhaber) me, I’m highly available.
