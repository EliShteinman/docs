---
title: "First-Ever Redis Modules Hackathon"
linkTitle: "First-Ever Redis Modules Hackathon"
url: "/blog/first-ever-redis-modules-hackathon/"
description: "Every day is a special day, but last Friday was a really special day because of the release of the first release candidate for Redis v4. The new version packs a lot of new stuff, although it’s most..."
date: 2016-12-07
blogCategories:
- "Tech"
authors:
- "Itamar Haber"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Itamar Haber, Technology Evangelist · Published 7 December 2016 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/165eae4946d6491c991d785128c05166396ec2a6-635x200.webp)

![First-Ever Redis Modules Hackathon](/images/site-mirror/165eae4946d6491c991d785128c05166396ec2a6-635x200.webp)

Every day is a special day, but last Friday was a really special day because of the [release of the first release candidate for Redis v4](http://antirez.com/news/110). The new version packs **a lot of new stuff**, although it’s most exciting addition by far is the new modules API – it allows just about anyone to go right ahead and make something more useful with Redis. It literally means endless possibilities and is the reason why the Sunday before was also an extra special day.

Last week’s Sunday was the submissions’ deadline for the Redis Modules Hackathon by Redis – a friendly competition for developers around the theme of the new API. The hackathon ran for 42 days (yep), and was open for anyone to participate online. We also hosted physical onsite sprints in Tel Aviv and San Francisco for participants in these regions. The guidelines for submissions were intentionally open to interpretation – basically anything to do with modules was legit. And just in case that the pure intellectual satisfaction of developing modules wasn’t motivating enough, we had also put out substantial monetary prizes to the winning projects 😉

The winners were picked from the list of 17 finalists by a panel made up of five judges of the Redis community: [Salvatore Sanfilippo](https://twitter.com/antirez), [Pedro Melo](https://twitter.com/pedromelo), [Francois-Guillaume Ribreau](https://twitter.com/FGRibreau), [Dvir Volk](https://twitter.com/dvirsky) and [myself](https://twitter.com/itamarhaber). Every judge independently evaluated and ranked each of the submissions on a scale from 1 to 10. Among the criteria for evaluation were the project’s originality, its potential impact, the design and the overall quality of submission. The scores given by the judges were then summed and the entries possessing the highest scores were chosen as winners.

The scores will not be made public, but I can share an interesting observation about them: although the each judge used his own judgment in evaluating the submissions and assigned them with scores based on his personal weighing methodology and preferences, the resulting order imposed by the scores between all judges’ was remarkably similar. Once the scores were tallied it was an extremely close race, where the top-scorers differed by only a fraction of a point.

Without further ado, I’d like to congratulate our prizewinners and present you with their projects:

The first place is awarded to Brandur Leach for his [redis-cell](https://github.com/brandur/redis-cell) module, which impressively delivers on several fronts. Primarily, redis-cell is a rate limiter that can readily be used to conserve the system’s resources and protect it against unexpected loads. While rate limiting is a common use case for Redis and a seemingly simple problem, the correct implementation of the solution may “take a few tries to get right”. Using the module is dead simple as it exposes a single new command, the output of which can be conveniently used for constructing the appropriate (HTTP) responses. But the module has another aspect that’s probably just as useful as its intended function – it is written using the systems programmers’ shiney new toy, Rust. And while the choice of programming language alone does not merit points by its own accord, Brandur had actually laid solid foundations for what could be a stand-alone library (or crate if you will) that acts as a bridge to Redis modules written in Rust.

Second prize is given to [RedisModuleTimeSeries](https://github.com/saginoam/RedisModuleTimeSeries) submitted by Noam Sagi. The module introduces a new data type that’s used for aggregating time series data, and can be used in either single or streaming modes. Noam was motivated to develop the module to achieve optimal performance in analyzing structured, mostly numerical data. The author claims that other solutions built using state-of-the-art frameworks are less effective when it comes to processing data within predefined numerical ranges, and provides a benchmark showing orders of magnitudes improvements in performance when compared to Elasticsearch.

The third place goes to the to Roi Lipman in recognition of his [Redis Graph](https://github.com/swilly22/redis-module-graph) module, which is a graph database that’s stored in Redis’ native Sorted Set data type. This neat trick is done using the approach described in [Representing and querying graphs using an hexastore](https://redis.io/topics/indexes#representing-and-querying-graphs-using-an-hexastore), but what really makes this submission shine is its choice of Neo4j’s Cypher as query language. While still young, the project has considerable potential and we hope that Roi will continue developing it and contributing to the Redis community.

The winner in our San Francisco regional challenge is Nick Chadwick who had authored the [Redis Zstandard Compressed Values module](https://github.com/chadnickbok/redis-zstd-module). Given its comparatively high price and the implications of running out of it, RAM is always a concern for Redis users. Nick’s module attempts to alleviate that by employing Facebook’s new-ish library for compressing the data as it is store. It runs multiple threads for performing the actual work and can be used with a custom dictionary to improve the compression rate of domain-specific data.

The Tel Aviv regional prize is given to Doron Sadeh for his [Pyrecks](https://github.com/doronsadeh/pyrecks) module. Pyrecks allows executing Python kernels – a term for describing small computational units – in a Redis sandbox. Each kernel is run encapsulated in its own thread and the kernels can be chained one after the other, the former’s output serving as the latter’s input, to implement even more complex processes. Pyrecks had started as a proof of concept at the [Redis TLV Meetup](https://www.meetup.com/Tel-Aviv-Redis-Meetup/events/232330909/), but was developed since then to full alpha status in order to be submitted. It is an awesome demonstration of modules’ potential to extend Redis by bridging it with other languages and its “Future Development” plans suggest that great things are to come.

Although we ran out of prizes to give, there are still a few submissions that deserve special recognition:

- [Reji](https://github.com/akobozev/reji), by Alexey Kobozev and Ilan Bronshtein, for achieving the fourth ranking in the Hackathon. The module is developed in CPP and implements an indexed JSON document store built using native data types.
- [ReDe](https://github.com/TamarLabs/ReDe), by Adam Lev-Libfeld, is a module for dehydrated data (“a fancy delayed queue”) that had gotten to the fifth place.
- [PopRank](https://github.com/poprank) by Sanket More, Louis Valencia, Matthew Kerns and Brian Hoang. The module, which allows ordering entities (e.g. blog posts) according to their popularity and recentness, had received from the judges an honorable mention for the effort and thought invested in it.
- [Shared Memory support for Redis](https://github.com/edgarsi/redis-module-shm), by Edgars Irmejs, connects a modified hiredis client to a local server via shared memory to achieve unparalleled low latency. While effectively exploiting the technique real life is quite hard, an honorable mention is given to it on grounds of being “extra hacky”.

I’d to sign off this post by thanking everyone who took a part: the developer teams who participated for your hard work and invaluable contributions, the HackerEarth staff for helping to orchestrate everything and, of course, the Redis team. It is because of you that this event came out so successful, and I’m certain that is only the first of many more to come. In every competition there are only a few winners, but in this case the real winner is every user in the Redis community.

If you’d like to develop your own Redis module a good place to start is [this blog post](/blog/writing-redis-modules), and we also have a mailing list for module developers at [https://groups.google.com/forum/#!forum/redis-module-devs](https://groups.google.com/forum/#!forum/redis-module-devs). As usual, feel free to [tweet](https://twitter.com/itamarhaber) or [email me](mailto:itamar@redis.com) – I’m highly available 😉
