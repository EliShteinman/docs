---
title: "Tracking Bigfoot with Redis and Geospatial Data"
linkTitle: "Tracking Bigfoot with Redis and Geospatial Data"
url: "/blog/tracking-bigfoot-with-redis-and-geospatial-data/"
description: "I think one of the coolest features of Redis—one that surprised me when I discovered it—is the geospatial data structure. Since I thought it was cool, I thought y’all might as well. So, I’m going..."
date: 2020-04-23
blogCategories:
- "Tech"
authors:
- "Guy Royse"
lastmod: 2025-03-27
hidden: true
---

*By Guy Royse, Developer Advocate · Published 23 April 2020 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

I think one of the coolest features of Redis—one that surprised me when I discovered it—is the geospatial data structure. Since I thought it was cool, I thought y’all might as well. So, I’m going to share it with you.

Redis’ geospatial data structures are fairly straightforward to work with but have some interesting nooks and crannies. We’re going to cover both. And, since I can’t write a blog post without a fun theme for my examples, this time I’m going to be using my favorite dataset of all: [Bigfoot sightings](https://github.com/timothyrenner/bfro_sightings_data).

## The Bigfoot dataset

The Bigfoot dataset has lots of great stuff in it. Each row is an account of a Bigfoot sighting and includes the full text of the account, when it happened, and even a classification. The classification is my favorite bit although the accounts are fun to read, too!

It’s not relevant to what we are doing today—I’m sharing this just for the fun of it— but here are the three classes of Bigfoot sightings:

- **Class A**: I saw Bigfoot.
- **Class B**: I found evidence of Bigfoot, like a footprint or bit of fur.
- **Class C**: Someone told me they saw Bigfoot.

Today, we’ll be playing with just the longitude, the latitude, and the report number of the Bigfoot sightings. If you want to load the data up and play along, I’ve set up a [repository](https://github.com/guyroyse/bigfoot-redis) with the data, the code to transform it, and instructions on running it. Of course, you’ll need [an install](https://redis.io/topics/quickstart) of Redis as well.

## The straightforward bits

A Geo Set is the key data structure for working with geospatial data in Redis. It holds a named set of locations on the globe. Adding and updating members to this set is easy. Just use the [GEOADD](https://redis.io/commands/geoadd) command:

> GEOADD bigfoot:sightings:locations -89.15173 37.61335 report:40120

This command asks Redis to add or update a member named report:40120 to the Geo Set bigfoot:sightings:locations at longitude -89.15173 and latitude 37.61335. If the member doesn’t exist, it will be inserted. If it does, its location will be updated.

**Note:** This type of operation is called an upsert—a portmanteau of update and insert—and is a popular pattern in Redis. Another pattern you’ll see repeatedly is the variadic command—a command that takes a variable number of arguments.

GEOADD is a variadic command as you can also upsert multiple members. Like this:

> GEOADD bigfoot:sightings:locations -89.15173 37.61335 report:40120

-88.55 41.33 report:12140

**Note:** The longitude and latitude are presented in the command in that order. *Longitude—*then the *latitude*. If you’re like a lot of people, your instinct will be to enter the latitude first. This is easy to get wrong. Watch for it.

Great. We’ve upserted a Bigfoot sighting in southern Illinois and one just west of Chicago. If you’re playing along at home you can look them up with these commands:

> HGETALL bigfoot:sightings:report:40120

> HGETALL bigfoot:sightings:report:12140

You can also look them up from their original source on the [Bigfoot Field Researchers Organization’s website](http://bfro.net/). There isn’t a way to find them by report number, but it is part of [the link](http://bfro.net/GDB/show_report.asp?id=40120) so you can probably figure it out.

Anyhow, that covers creating and updating. But what about reading and querying? There are several ways to do this. If you just want to pull out the coordinates you can use the [GEOPOS](https://redis.io/commands/geopos) command:

> GEOPOS bigfoot:sightings:locations report:40120

You can also query for members variadicly:

> GEOPOS bigfoot:sightings:locations report:40120 report:12140

This will return the coordinates with, perhaps, a bit more precision than they were entered with. That’s an artifact of how they are stored and is something we’ll talk about in a bit:

```javascript
1) 1) "-89.15173262357711792"
   2) "37.61334955747530984"
2) 1) "-88.55000048875808716"
   2) "41.330001054529383"
```

Again, note that the two sets of coordinates returned are longitude first and then latitude.

You might want to do something a little more sophisticated. Maybe you want to determine the distance between a couple of Bigfoot sightings. You can find out with the [GEODIST](https://redis.io/commands/geodist) command:

> GEODIST bigfoot:sightings:locations report:40120 report:12140

Just hand GEODIST a key and two members and it will tell you how far apart they are in meters. If you’re not interested in meters and prefer kilometers or Freedom Units (i.e. feet and miles), you can just specify which you want at the end of the command:

> GEODIST bigfoot:sightings:locations report:40120 report:12140 m

> GEODIST bigfoot:sightings:locations report:40120 report:12140 km

> GEODIST bigfoot:sightings:locations report:40120 report:12140 ft

> GEODIST bigfoot:sightings:locations report:40120 report:12140 mi

These two sightings are about 260 miles apart.

You can also find members of the Geo Set in a radius around a specific point. That point can be [a coordinate pair](https://redis.io/commands/georadius) or [another member of the Geo Set](https://redis.io/commands/georadiusbymember). Southeastern Ohio is actually a hotbed of Bigfoot sightings. Let’s see how many sightings there are near [Athens](https://en.wikipedia.org/wiki/Athens,_Ohio)—the largest city in that part of the state:

> GEORADIUS bigfoot:sightings:locations -82.109149 39.319950 25 mi

Quite a few:

1) "report:4982"

2) "report:9042"

...snip...

15) "report:8017"

16) "report:10945"

Here’s the same command using a member instead of coordinates:

> GEORADIUSBYMEMBER bigfoot:sightings:locations report:9042 25 mi

You can also request extra information on those locations by adding WITHCOORD and/or WITHDIST at the end:

> GEORADIUS bigfoot:sightings:locations -82.109149 39.319950 25 mi WITHCOORD WITHDIST

```javascript
1) 1) "report:4982"
   2) "16.2549"
   3) 1) "-82.3997005820274353"
      2) "39.25109119711087402"
   ...snip...
16) 1) "report:10945"
    2) "24.7297"
    3) 1) "-81.85806065797805786"
       2) "39.01971931496525059"
```

So that’s GEOADD, GEOPOS, GEODIST, GEORADIUS, and GEORADIUSBYMEMBER. These commands allow you to create, read, and update geospatial data in Redis. However, you might notice I have talked only about three of the four legs of CRUD. Where’s the GEO-something-or-other command to remove members? Well, that’s one of the first interesting bits.

## Where’s the delete?

So before we can talk about delete, we need to talk about [geohashing](https://en.wikipedia.org/wiki/Geohash). Geohashing is a clever way to store coordinates in a single integer and then represent that as a base-32 encoded string.

Geohashing stores the coordinates one bit at time as you subdivide the Earth. The first division splits the globe in twain along the prime meridian. The most significant integer is 0 if the location is in the western hemisphere or a 1 if it is in the eastern hemisphere. The next bit splits along the northern and southern hemispheres. Northern gets a 1 and southern gets a 0. You keep dividing like this, east and west then north and south, and keep adding bits until you are at a resolution you are happy with. Then, you encode the bits.

Redis can do this for you with the GEOHASH commands. It works just like GEOPOS but instead of returning coordinates, it returns a geohash. And, of course, it’s variadic:

> GEOHASH bigfoot:sightings:locations report:40120 report:12140

1) "dn8tgr39wh0"

2) "dp350gzueq0"

These are base-32 encoded numbers. This means that a Geo Set could be represented as a set with a numeric value. Redis has a data type like that: the Sorted Set. And, that’s exactly how Redis implements Geo Sets.

Behind the scenes, Geo Sets are Sorted Sets. The number in a sorted set is a 64-bit floating-point number. The integer representing the geohash is stored in that float and can safely be no larger than a 52-bit integer (which is plenty). When you call GEOHASH, Redis gets the number and base-32 encodes it. When you call GEOPOS, Redis gets the number and converts it to coordinates, which is why the coordinates you enter aren’t exactly the ones you get back.

And since Geo Sets are Sorted Sets, all the [Sorted Set commands](https://redis.io/commands#sorted_set) work on Geo Sets—although some come with caveats. For example, want to get the underlying integer for the geohash?

> ZSCORE bigfoot:sightings:locations report:40120

"1781261397121617"

Want to get all the members?

> ZRANGE bigfoot:sightings:locations 0 -1

1) "report:8059"

2) "report:4886"

3) "report:1031"

...snip...

Actually, don’t do that. Use [ZSCAN](https://redis.io/commands/zscan) instead:

> ZSCAN bigfoot:sightings:locations 0 COUNT 5

So, how would you remove a member? With [ZREM](https://redis.io/commands/zrem):

> ZREM bigfoot:sightings:locations report:40120 report:12140

And now when you go to get them, they’re gone:

> GEOPOS bigfoot:sightings:locations report:40120 report:12140

1) (nil)

2) (nil)

## Wrapping up the search for Bigfoot

That’s pretty much everything you can do to a Geo Set. But it certainly isn’t everything you can do *with* a Geo Set. There are plenty of applications for geospatial data. In addition to the rather whimsical tracking of Bigfoot, you could also combine geospatial data with Pub/Sub to do real-time tracking of whatever you’d like—be that users of a mobile app, trucks in your fleet, or non-cryptozoological animals in an environmental study.
