---
title: "Introducing Redis OM for Node.js"
linkTitle: "Introducing Redis OM for Node.js"
url: "/blog/introducing-redis-om-for-node-js/"
description: "I wrote a thing—well, actually several of us wrote things—I just wrote the Node.js version. I think it’s a pretty cool thing that’s worthy of your attention, and I’m excited about it. The thing I’m..."
date: 2021-12-08
blogCategories:
- "How To and Tutorials"
- "New Product Announcements"
- "Tech"
authors:
- "Guy Royse"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Guy Royse, Developer Advocate · Published 8 December 2021 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/c00f92bb6fd5f3fd8c418c4a8036029f60f5ce87-772x550.webp)

## Fast and easy object mapping for JavaScript and TypeScript

I wrote a thing—well, actually several of us wrote things—I just wrote the Node.js version. I think it’s a pretty cool thing that’s worthy of your attention, and I’m excited about it. The thing I’m talking about: [Redis OM for Node.js](https://github.com/redis/redis-om-node).

What’s Redis OM? Redis OM is a library that makes it easy to use Redis by mapping Redis data structures straight to your code. The OM bit stands for *object mapping*, but we plan to do more than just that in the future.

Read on for more details.

# Faster than fast

You probably already know that Redis is fast—faster than fast—and it stores the sorts of things your programs care about: hashes, lists, sets, things like that. These are the structures I think in as a programmer. When I’m explaining what Redis is to an uninitiated techie, I tell them that Redis is all those data structures you learned about in college with a wire-protocol plopped in front of them.

[Features](/modules/redis-bloom/) make Redis even awesomer (yes, I know that’s not a word) by introducing *new* data structures for your programs to care about. [Probabilistic](/modules/redis-bloom/) adds probabilistic data structures like Bloom and Cuckoo filters.

# The most awesomest modules

But there are two modules in particular that make Redis the powerful in-memory database every programmer wants it to be: [JSON](/json/) and [Search and Query](/search/).

JSON brings hierarchy to the table. Hashes are great, but what if you want to embed hashes in your hash? JSON has you covered by letting you store my hierarchical data in JSON documents.

Meanwhile, Search and Query lets you *find* the data structures you care about. Sure, you can create manual indices using sets, but that approach is limited and manual. Yuck. Search and Query lets you write queries to go right to the data you want.

Combined, Search and Query and JSON make Redis a pretty nifty document database. You get the hierarchy you want and the ability to find the things in it that you care about. Best of both worlds and all that.

In fact, we think this is such a tasty combination, we’re [rolling them together](/blog/redisjson-public-preview-performance-benchmarking/) and just calling them JSON.

# Redis OM for Node.js

The [query language](https://redis.io/docs/interact/search-and-query/query/) for Search and Query is powerful. Very powerful. It allows you to search Hashes and JSON documents within Redis in varied and sophisticated ways. And when I need all that power, it’s very cool. But sometimes I don’t need all that power. And I *am* a lazy developer—I want it to be as easy as possible (and no easier).

Making things as easy as possible is what I was trying to do when I wrote [Redis OM for Node.js](https://github.com/redis/redis-om-node). Redis OM makes it simple to add Redis to your Node.js application by mapping hashes and JSON documents to classes that you define. No complex commands, just pure code with a fluent interface. Take a look.

Define an entity:

```python
class Album extends Entity {}

let schema = new Schema(Album, {
  artist: { type: 'string' },
  title: { type: 'string', textSearch: true },
  year: { type: 'number' }
});

```

Create a new entity and save it:

```python
let album = repository.createEntity()
album.artist = "Mushroomhead"
album.title = "The Righteous & The Butterfly"
album.year = 2014
await repository.save(album)

```

Search for matching entities:

```python
let albums = await repository.search()
  .where('artist').equals('Mushroomhead')
  .and('title').matches('butterfly')
  .and('year').is.greaterThan(2000).returnAll()

```

Now I’m fairly biased since I wrote this library and all, but I think that’s pretty dadgum cool! Let’s take a closer look at this syntax and learn how it works.

# How it works

There are four classes you need to care about in Redis OM for Node.js. They are Entity, Schema, Client, and Repository.

```python
import { Entity, Schema, Client, Repository } from 'redis-om'

```

```python
class Album extends Entity {}

```

```python
let schema = new Schema(Album, {
  artist: { type: 'string' },
  title: { type: 'string' },
  year: { type: 'number' },
  genres: { type: 'array' },
  outOfPublication: { type: 'boolean' }
})

```

```python
let client = new Client()
await client.open('redis://localhost:6379')

```

```python
let repository = new Repository(schema, client)

```

```python
let album, id

// create an entity and save it
album = repository.createEntity()

album.artist = "Mushroomhead"
album.title = "The Righteous & The Butterfly"
album.year = 2014
album.genres = [ 'metal' ]
album.outOfPublication = true

id = await repository.save(album) // '01FJYWEYRHYFT8YTEGQBABJ43J'

// read an entity
album = await repository.fetch('01FJYWEYRHYFT8YTEGQBABJ43J')

// update an entity
album.genres = [ 'metal', 'nu metal', 'avantgarde' ]
album.outOfPublication = false

id = await repository.save(album) // '01FJYWEYRHYFT8YTEGQBABJ43J'

// delete an entity
await repository.remove('01FJYWEYRHYFT8YTEGQBABJ43J')

```

```python
let albums = await repository.search()
  .where('artist').equals('Mushroomhead')
  .and('title').matches('butterfly')
  .and('year').is.greaterThan(2000).returnAll()

```

**Entities** are the classes that you work with. The things being created, read, updated, and deleted. The things being searched for. Any class that extends Entity is an entity. Usually, you’ll define an entity with a single line of code, but you can add custom logic in there as well:

```python
import { Entity, Schema, Client, Repository } from 'redis-om'

```

```python
class Album extends Entity {}

```

```python
let schema = new Schema(Album, {
  artist: { type: 'string' },
  title: { type: 'string' },
  year: { type: 'number' },
  genres: { type: 'array' },
  outOfPublication: { type: 'boolean' }
})

```

```python
let client = new Client()
await client.open('redis://localhost:6379')

```

```python
let repository = new Repository(schema, client)

```

```python
let album, id

// create an entity and save it
album = repository.createEntity()

album.artist = "Mushroomhead"
album.title = "The Righteous & The Butterfly"
album.year = 2014
album.genres = [ 'metal' ]
album.outOfPublication = true

id = await repository.save(album) // '01FJYWEYRHYFT8YTEGQBABJ43J'

// read an entity
album = await repository.fetch('01FJYWEYRHYFT8YTEGQBABJ43J')

// update an entity
album.genres = [ 'metal', 'nu metal', 'avantgarde' ]
album.outOfPublication = false

id = await repository.save(album) // '01FJYWEYRHYFT8YTEGQBABJ43J'

// delete an entity
await repository.remove('01FJYWEYRHYFT8YTEGQBABJ43J')

```

```python
let albums = await repository.search()
  .where('artist').equals('Mushroomhead')
  .and('title').matches('butterfly')
  .and('year').is.greaterThan(2000).returnAll()

```

**Schemas** define the fields on your entity, their types, and how they are mapped internally to Redis. By default, entities map to Hashes in Redis, but you can also map them to JSON documents:

```python
import { Entity, Schema, Client, Repository } from 'redis-om'

```

```python
class Album extends Entity {}

```

```python
let schema = new Schema(Album, {
  artist: { type: 'string' },
  title: { type: 'string' },
  year: { type: 'number' },
  genres: { type: 'array' },
  outOfPublication: { type: 'boolean' }
})

```

```python
let client = new Client()
await client.open('redis://localhost:6379')

```

```python
let repository = new Repository(schema, client)

```

```python
let album, id

// create an entity and save it
album = repository.createEntity()

album.artist = "Mushroomhead"
album.title = "The Righteous & The Butterfly"
album.year = 2014
album.genres = [ 'metal' ]
album.outOfPublication = true

id = await repository.save(album) // '01FJYWEYRHYFT8YTEGQBABJ43J'

// read an entity
album = await repository.fetch('01FJYWEYRHYFT8YTEGQBABJ43J')

// update an entity
album.genres = [ 'metal', 'nu metal', 'avantgarde' ]
album.outOfPublication = false

id = await repository.save(album) // '01FJYWEYRHYFT8YTEGQBABJ43J'

// delete an entity
await repository.remove('01FJYWEYRHYFT8YTEGQBABJ43J')

```

```python
let albums = await repository.search()
  .where('artist').equals('Mushroomhead')
  .and('title').matches('butterfly')
  .and('year').is.greaterThan(2000).returnAll()

```

When you create a Schema, it modifies the Entity you handed it, adding getters and setters for the properties you define. The type those getters and setters accept and return are defined with the type property above.

**Clients** connect you to Redis. A Client has methods to open, close, and execute raw commands against Redis. You’ll mostly use open and close:

```python
import { Entity, Schema, Client, Repository } from 'redis-om'

```

```python
class Album extends Entity {}

```

```python
let schema = new Schema(Album, {
  artist: { type: 'string' },
  title: { type: 'string' },
  year: { type: 'number' },
  genres: { type: 'array' },
  outOfPublication: { type: 'boolean' }
})

```

```python
let client = new Client()
await client.open('redis://localhost:6379')

```

```python
let repository = new Repository(schema, client)

```

```python
let album, id

// create an entity and save it
album = repository.createEntity()

album.artist = "Mushroomhead"
album.title = "The Righteous & The Butterfly"
album.year = 2014
album.genres = [ 'metal' ]
album.outOfPublication = true

id = await repository.save(album) // '01FJYWEYRHYFT8YTEGQBABJ43J'

// read an entity
album = await repository.fetch('01FJYWEYRHYFT8YTEGQBABJ43J')

// update an entity
album.genres = [ 'metal', 'nu metal', 'avantgarde' ]
album.outOfPublication = false

id = await repository.save(album) // '01FJYWEYRHYFT8YTEGQBABJ43J'

// delete an entity
await repository.remove('01FJYWEYRHYFT8YTEGQBABJ43J')

```

```python
let albums = await repository.search()
  .where('artist').equals('Mushroomhead')
  .and('title').matches('butterfly')
  .and('year').is.greaterThan(2000).returnAll()

```

A Schema and a Client are required to instantiate a Repository. **Repositories** provide the means to read, write, and remove entities. And the means to search for them:

```python
import { Entity, Schema, Client, Repository } from 'redis-om'

```

```python
class Album extends Entity {}

```

```python
let schema = new Schema(Album, {
  artist: { type: 'string' },
  title: { type: 'string' },
  year: { type: 'number' },
  genres: { type: 'array' },
  outOfPublication: { type: 'boolean' }
})

```

```python
let client = new Client()
await client.open('redis://localhost:6379')

```

```python
let repository = new Repository(schema, client)

```

```python
let album, id

// create an entity and save it
album = repository.createEntity()

album.artist = "Mushroomhead"
album.title = "The Righteous & The Butterfly"
album.year = 2014
album.genres = [ 'metal' ]
album.outOfPublication = true

id = await repository.save(album) // '01FJYWEYRHYFT8YTEGQBABJ43J'

// read an entity
album = await repository.fetch('01FJYWEYRHYFT8YTEGQBABJ43J')

// update an entity
album.genres = [ 'metal', 'nu metal', 'avantgarde' ]
album.outOfPublication = false

id = await repository.save(album) // '01FJYWEYRHYFT8YTEGQBABJ43J'

// delete an entity
await repository.remove('01FJYWEYRHYFT8YTEGQBABJ43J')

```

```python
let albums = await repository.search()
  .where('artist').equals('Mushroomhead')
  .and('title').matches('butterfly')
  .and('year').is.greaterThan(2000).returnAll()

```

Once we have a repository, we can use it to create, read, update, and delete entities. Here I’m doing just that with a favorite album of mine by Mushroomhead:

```python
import { Entity, Schema, Client, Repository } from 'redis-om'

```

```python
class Album extends Entity {}

```

```python
let schema = new Schema(Album, {
  artist: { type: 'string' },
  title: { type: 'string' },
  year: { type: 'number' },
  genres: { type: 'array' },
  outOfPublication: { type: 'boolean' }
})

```

```python
let client = new Client()
await client.open('redis://localhost:6379')

```

```python
let repository = new Repository(schema, client)

```

```python
let album, id

// create an entity and save it
album = repository.createEntity()

album.artist = "Mushroomhead"
album.title = "The Righteous & The Butterfly"
album.year = 2014
album.genres = [ 'metal' ]
album.outOfPublication = true

id = await repository.save(album) // '01FJYWEYRHYFT8YTEGQBABJ43J'

// read an entity
album = await repository.fetch('01FJYWEYRHYFT8YTEGQBABJ43J')

// update an entity
album.genres = [ 'metal', 'nu metal', 'avantgarde' ]
album.outOfPublication = false

id = await repository.save(album) // '01FJYWEYRHYFT8YTEGQBABJ43J'

// delete an entity
await repository.remove('01FJYWEYRHYFT8YTEGQBABJ43J')

```

```python
let albums = await repository.search()
  .where('artist').equals('Mushroomhead')
  .and('title').matches('butterfly')
  .and('year').is.greaterThan(2000).returnAll()

```

We can also use it to search for entities:

```python
import { Entity, Schema, Client, Repository } from 'redis-om'

```

```python
class Album extends Entity {}

```

```python
let schema = new Schema(Album, {
  artist: { type: 'string' },
  title: { type: 'string' },
  year: { type: 'number' },
  genres: { type: 'array' },
  outOfPublication: { type: 'boolean' }
})

```

```python
let client = new Client()
await client.open('redis://localhost:6379')

```

```python
let repository = new Repository(schema, client)

```

```python
let album, id

// create an entity and save it
album = repository.createEntity()

album.artist = "Mushroomhead"
album.title = "The Righteous & The Butterfly"
album.year = 2014
album.genres = [ 'metal' ]
album.outOfPublication = true

id = await repository.save(album) // '01FJYWEYRHYFT8YTEGQBABJ43J'

// read an entity
album = await repository.fetch('01FJYWEYRHYFT8YTEGQBABJ43J')

// update an entity
album.genres = [ 'metal', 'nu metal', 'avantgarde' ]
album.outOfPublication = false

id = await repository.save(album) // '01FJYWEYRHYFT8YTEGQBABJ43J'

// delete an entity
await repository.remove('01FJYWEYRHYFT8YTEGQBABJ43J')

```

```python
let albums = await repository.search()
  .where('artist').equals('Mushroomhead')
  .and('title').matches('butterfly')
  .and('year').is.greaterThan(2000).returnAll()

```

And, for your copy-and-pasting convenience, here’s that sample as one big block of code:

```python
import { Entity, Schema, Client, Repository } from 'redis-om'

class Album extends Entity {}
let schema = new Schema(Album, {
  artist: { type: 'string' },
  title: { type: 'string' },
  year: { type: 'number' },
  genres: { type: 'array' },
  outOfPublication: { type: 'boolean' }
})

let client = new Client()
await client.open('redis://localhost:6379')

let repository = new Repository(schema, client)

let album, id

// create an entity and save it
album = repository.createEntity()

album.artist = "Mushroomhead"
album.title = "The Righteous & The Butterfly"
album.year = 2014
album.genres = [ 'metal' ]
album.outOfPublication = true

id = await repository.save(album) // '01FJYWEYRHYFT8YTEGQBABJ43J'

// read an entity
album = await repository.fetch('01FJYWEYRHYFT8YTEGQBABJ43J')

// update an entity
album.genres = [ 'metal', 'nu metal', 'avantgarde' ]
album.outOfPublication = false

id = await repository.save(album) // '01FJYWEYRHYFT8YTEGQBABJ43J'

// delete an entity
await repository.remove('01FJYWEYRHYFT8YTEGQBABJ43J')

let albums = await repository.search()
  .where('artist').equals('Mushroomhead')
  .and('title').matches('butterfly')
  .and('year').is.greaterThan(2000).returnAll()

```

And that’s Redis OM for Node.js in, as they say, a nutshell.

# Wrapping up

This has been a quick overview of what Redis OM for Node.js can do. If you’d like to learn more, there’s a [tutorial](https://github.com/redis-developer/redis-om-node-tutorial) that will guide you through building a simple service with Redis OM. And if you want to go deeper, and you totally should, check out the [README](https://github.com/redis/redis-om-node) and [API docs](https://github.com/redis/redis-om-node/tree/main/docs) on GitHub.

Of course, this is brand new software that hasn’t been tested in the wild yet. **You** are that wild. Please try it out. Kick the tires. Try to break it. See what’s there and what could be there. And when you find that bug or think of that perfect feature, let me know by [opening an issue](https://github.com/redis/redis-om-node/issues) or [sending a pull request](https://github.com/redis/redis-om-node/pulls). Your help in making Redis OM better is sincerely appreciated. Thanks!
