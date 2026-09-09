---
title: "What’s Up With Redis OM for Node.JS?"
linkTitle: "What’s Up With Redis OM for Node.JS?"
url: "/blog/redis-om-node-js/"
description: "Redis OM for Node.js is still in its early days, but we’re making a lot of progress. Here’s what we added in the latest version and where we’re headed."
date: 2022-08-04
blogCategories:
- "How To and Tutorials"
- "New Product Announcements"
authors:
- "Guy Royse"
lastmod: 2025-03-31
hidden: true
---

*By Guy Royse, Developer Advocate · Published 4 August 2022 · updated 31 March 2025*

![Blog tile image](/images/site-mirror/c00f92bb6fd5f3fd8c418c4a8036029f60f5ce87-772x550.webp)

**Redis OM for Node.js is still in its early days, but we’re making a lot of progress. Here’s what we added in the latest version and where we’re headed.**

I released a preview of [Redis OM for Node.js](https://github.com/redis/redis-om-node) a few months back. I was pretty happy with it at the time. It did the things it was supposed to do, at least this early in a development cycle.

One element that made me particularly happy was the fluent interface for searching. You know, this thing:

```javascript
const albums = await repository.search()
  .where('artist').equals('Mushroomhead')
  .and('title').matches('butterfly')
  .and('year').is.greaterThan(2000)
    .return.all()

```

But the best part—the part I’ve been most happy with—is how much Redis OM for Node.js has been embraced and used by the developer community. Many of you have given me a lot of useful and actionable feedback, often via our [Discord server](https://discord.com/invite/redis). Plus, you fixed bugs and even sent in complete features from my rather sparsely defined issues on GitHub. Your assistance is truly appreciated.

I’ve incorporated your feedback and your pull requests, and your contributions. In this post, I summarize some of the changes that we—and by “we” I mean “you and I”—have made to Redis OM.

### Easier Entity creation

Early on, [some rando](https://www.youtube.com/fireship) on the Internet suggested that calls to .createEntity should take initial values for that Entity. I thought this was a great idea and adopted it in Redis OM.

So what was once a bit verbose:

```javascript
const album = albumRepository.createEntity()
album.artist = "Mushroomhead"
album.title = "The Righteous & The Butterfly"
album.year = 2014
album.genres = [ 'metal' ]
album.outOfPublication = true

const id = await albumRepository.save(album)

```

Became much tidier:

```javascript
const album = albumRepository.createEntity({
  artist: "Mushroomhead",
  title: "The Righteous & The Butterfly",
  year: 2014,
  genres: [ 'metal' ],
  outOfPublication: true
})

const id = await albumRepository.save(album)

```

I even added a .createAndSave method to eliminate the call to .save because this is such a common pattern:

```javascript
const album = await albumRepository.createAndSave({
  artist: "Mushroomhead",
  title: "The Righteous & The Butterfly",
  year: 2014,
  genres: [ 'metal' ],
  outOfPublication: true
})

```

Thanks for the suggestion. It was a solid one.

### Expiring Entities

Redis makes an awesome database but also a pretty good cache. Many of you suggested we needed a way to create expiring Entities.

Ask and ye shall receive:

```javascript
const ttlInSeconds = 12 * 60 * 60  // 12 hours
await albumRepository.expire('01FVDN241NGTPHSAV0DFDBXC90', ttlInSeconds)

```

Not sure why you’d want to expire a Mushroomhead album, but *de gustibus non est disputandum*.

### Point and date types

Nobody asked for these, but I wanted them anyhow! RediSearch has good support for location with the GEO type, and dates are used in all sorts of applications. So I added them as point and date, respectively.:

```javascript
const studioSchema = new Studio(Studio, {
  name: { type: 'string' },
  city: { type: 'string' },
  state: { type: 'string' },
  location: { type: 'point' },
  established: { type: 'date' }
})

```

And, of course, they’re perfectly usable with the fluent search interface:

```javascript
const studios = await studioRepository.search()
  .where('established').after(date)
  .return.all()

const studios = await studioRepository.search()
  .where('location').inRadius(
    circle => circle.origin(-81.7758995, 41.4976393).radius(50).miles)
  .return.all()

```

### Better integration with Node Redis

Probably my favorite change in Redis OM for Node.js is how it works with [Node Redis](https://github.com/redis/node-redis). In the preview, you could .open a client that used Node Redis behind the scenes:

```javascript
const client = new Client()
await client.open('redis://localhost:6379')

```

Now, you can .use an existing connection from Node Redis:

```javascript
import { createClient } from 'redis'

const redis = createClient('redis://localhost:6379')
await redis.connect()
const client = await new Client().use(redis)

```

This lets you connect to Redis in [all sorts of ways](https://github.com/redis/node-redis/blob/master/docs/client-configuration.md), not just with a simple connection string. I also changed .open and .use to return the Client to allow nifty one-liners:

```javascript
const client = await new Client().open('redis://localhost:6379')

```

## Some breaking changes

No preview is perfect; that’s why it’s a preview. I learned a lot by watching people’s mistakes while using Redis OM for Node.js. Mistakes that were the result of misunderstanding parts of the interface to Redis OM. Parts that need improvement because I had not sufficiently thought them through. These improvements resulted in a few important but breaking changes.

### Renaming some types

I noticed a lot of folks being confused when they were using a string as a TEXT versus a TAG in RediSearch. So I made this distinction explicit by breaking the string type into two types: string and text.

I also learned that it was unclear that the array type could only be an array of strings. I changed it to string[]:

```javascript
let albumSchema = new Schema(Album, {
  artist: { type: 'string' },
  title: { type: 'text' },
  year: { type: 'number' },
  genres: { type: 'string[]' },
  outOfPublication: { type: 'boolean' }
})

```

### JSON is the default

Almost everyone using Redis OM was using RediSearch *and* RedisJSON. They were choosing to store their documents as JSON documents. But in the preview, Redis OM used Hashes as the default storage mechanism.

This resulted in everyone having to tell Redis OM to use JSON explicitly:

```javascript
let albumSchema = new Schema(Album, {
  artist: { type: 'string' },
  title: { type: 'string' },
  year: { type: 'number' },
  genres: { type: 'string[]' },
  outOfPublication: { type: 'boolean' }
}, {
  dataStructure: 'JSON'
})

```

To avoid this step, I changed the default:

```javascript
let albumSchema = new Schema(Album, {
  artist: { type: 'string' },
  title: { type: 'string' },
  year: { type: 'number' },
  genres: { type: 'string[]' },
  outOfPublication: { type: 'boolean' }
})

```

This change really didn’t impact all that many developers as you were all using JSON anyhow. But it is nice to know that you can now delete just a little more code!

## Software is never done

Of course, software is never complete. I have more things I want to add to Redis OM than I probably have time to implement. Here’s a few of the things that I’m looking at for future releases:

- **Embeddable Entities**: This is easily the most requested feature. Right now, Entities are flat. You can’t create nested objects in your JSON with Redis OM. I’m working on this as you read this blog post. Expect it soon.
- **Bring your own keys**: This is another popular request. Redis OM generates a key when you create an Entity, calling it the entity ID. But you often already have a primary key you’d like to use. I’ll probably tackle this after embeddable Entities.
- **Decorators**: I’d like to use decorators so that the information in your Schema can just be annotated instead. [TypeScript](https://www.typescriptlang.org/docs/handbook/decorators.html) has them, and while they are still “experimental”, if decorators are good enough for Next.js, they’re probably good enough for me. Maybe [JavaScript](https://github.com/tc39/proposal-decorators) will get them someday soon too. This is probably a 2.0 feature for RedisOM for Node.js.

## Some helpful resources

I’ve also been working on some helpful content if you’re getting started with Redis OM:

- I wrote a [simple sample API](https://github.com/redis-developer/redis-om-node-skeleton-app) with Express and Redis OM. Think of it as a starter code. Fork it, make your change, and go.
- I put together a video workshop that walks you through building an API with Express and Redis OM. Essentially, this is the aforementioned starter code, but it walks you through building the API.
- All the new features, and the old ones, are documented in the [README](https://github.com/redis/redis-om-node#readme). If you want to know how to do something, it’s probably in there.
- If you get stuck, I’m on the [Redis Discord](https://discord.gg/redis) server a lot. Probably more than is healthy. Take advantage of it!
- I, and some of my peers, stream all sorts of stuff—including a lot of Redis OM and Redis Stack stuff—on [Twitch](https://www.twitch.tv/redisinc). Watch us there.

## Thanks

So how’s that for a summary of what’s new with Redis OM for Node.js? Redis OM is what it is because of the assistance from folks in the community. So, I’d like to close with a hearty “Thank you” to some of the helpful folks who have… well… helped:

- [Aviv Ben Yosef](https://github.com/pogiii) for the very first PR from someone outside of Redis.
- [Benjamin Winkler](https://github.com/abwinkler999) for improvements to the README.
- [Dani Patko](https://github.com/danipatko) for implementing .sortBy, .min, and .max.
- [DidaS](https://github.com/DidaS-git) for all the help in improving Redis OM’s performance and the code’s quality. And for his linter.
- [Luc](https://github.com/lucemans) for making the changes [that rando](https://www.youtube.com/fireship) suggested. And for his enthusiastic support.
- [Simon Green](https://github.com/captaincodeman) for making the test suite orders of magnitude faster.
- My good friend [Nilanjan](https://github.com/nraychaudhuri) for actually daring to use preview software in production and providing tons of feedback. *Fortuna audentes iuvat*.

I’m sure I’ve missed some of you, but know that GitHub’s commit history will never forget.
