---
title: "GeoBike Part Two: Querying The Data"
linkTitle: "GeoBike Part Two: Querying The Data"
url: "/blog/geobike-part-two-querying-the-data/"
description: "Indexing The Data"
date: 2018-02-01
blogCategories:
- "Tech"
authors:
- "Tague Griffith"
lastmod: 2025-03-27
hidden: true
---

*By Tague Griffith, Head of Developer Advocacy · Published 1 February 2018 · updated 27 March 2025*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

![](/images/blog/9d4f66dee2245475cbc5f418709e59612ad70634-5000x3333.webp)

**Indexing The Data**

In a [previous post](/blog/geobike-building-location-aware-application-with-redis/), we built the back end for a location-aware application using Redis and talked about how to use a Python program to load data from a [General Bikeshare Feed Specification](https://github.com/NABSA/gbfs) (GBFS) data feed and store information about bike-sharing systems operating throughout the world. Our program parsed the JSON structured data from the feed to store metadata about each station in Redis, and then index the location of each station using Redis’ [geospatial data structure](https://redis.io/commands#geo).

Our indexing and parsing program loaded the metadata for sharing stations into Redis using structured keys in the form ${system_id}:station:${station_id} with the system_id and the station_id being unique identifiers specified in the GBFS data. The geospatial location index of all the stations in a particular sharing system is stored using the key ${system_id}:stations:location.

Now that we have built a back-end database of sharing stations and indexed it with location information, we can use that data to find sharing stations located near a user’s current location.

**Getting the User’s Location**

The next step in building out our application is to determine the user’s current location. Most applications accomplish this through built-in services provided by the operating system. The OS can provide applications with a location based on GPS hardware built into the device or approximated from the device’s available WiFi networks.

On Apple devices, you can find the user’s current location using [CoreLocation](https://developer.apple.com/documentation/corelocation), which is available in all Apple device SDKs. If you are experimenting with our code and want to try this out on your Mac OS X laptop, you can download and build the [whereami](https://github.com/victor/whereami) tool which uses CoreLocation to estimate your computer’s current longitude and latitude.

**Finding Stations**

After we have found the user’s current location, we want to locate any bike sharing stations that are nearby. Using the [geospatial functions of Redis](/solutions/redis-geospatial-data/), we can look up stations within a given distance of our current coordinates. Let’s walk through an example of this using the Redis CLI.

Imagine I’m at the Apple Store on Fifth Avenue and I want to head downtown to Mood on West 37th to catch up with my buddy [Swatch](https://twitter.com/swatchthedog). I could take a taxi or the subway, but I’d rather bike. Are there any nearby sharing stations where I could borrow a bike for my trip?

![](/images/blog/fe0fb77361be5d3c484aa19c7335523ea76a2b79-747x445.webp)

The Apple store is located at 40.76384, -73.97297. We can draw a 500 ft radius around the store (in blue) on the map overlay we created as part of the first post and see that two Bike Share Stations—Grand Army Plaza & Central Park South and E 58th St & Madison—fall within the radius.

Using the Redis GEORADIUS command, I can query the index we loaded for the NYC system for stations within a 500-foot radius by issuing the following command to Redis:

```python
127.0.0.1:6379> GEORADIUS NYC:stations:location -73.97297 40.76384 500 ft
1) "NYC:station:3457"
2) "NYC:station:281"

```

Redis returns the two elements found within that radius. The elements in our geospatial index are the keys for the metadata about a particular station, so we’ll look up the names for the two stations:

```python
127.0.0.1:6379> hget NYC:station:281 name
"Grand Army Plaza & Central Park S"

127.0.0.1:6379> hget NYC:station:3457 name
"E 58 St & Madison Ave"

```

We find those keys correspond to the stations we identified from the map above. We can add additional flags to the GEORADIUS command to get a list of elements, their coordinates and their distance from our current point:

```python
127.0.0.1:6379> GEORADIUS NYC:stations:location -73.97297 40.76384 500 ft WITHDIST WITHCOORD ASC
1) 1) "NYC:station:281"
  2) "289.1995"
  3) 1) "-73.97371262311935425"
     2) "40.76439830559216659"
2) 1) "NYC:station:3457"
   2) "383.1782"
   3) 1) "-73.97209256887435913"
      2) "40.76302702144496237"

```

After looking up the names associated with those keys, we can present an ordered list of stations to the user so that they can choose ah location. Redis doesn’t provide any directions or routing capability, so you will need to use the routing features of the device’s OS to plot a course for the user from their current location to the selected bike station.

The GEORADIUS function can be easily implemented inside an API in your favorite development framework to add location functionality to an app.

**Other Query Commands**

In addition to the GEORADIUS command, Redis provides three other commands for querying data from the index: GEOPOS, GEODIST, and GEORADIUSBYMEMBER.

The GEOPOS command can be used to get the coordinates for a given element from the geohash. For example, if I know that there is a bike sharing station at W 38th and 8th and Its ID is 523, then the element name for that station is NYC:station:523. Using Redis, we can find the longitude and latitude of that particular station:

```python
127.0.0.1:6379> GEOPOS NYC:stations:location NYC:station:523
1) 1) "-73.99138301610946655"
   2) "40.75466497634030105"

```

The GEODIST command provides the distance between two elements of the index. If I wanted to find the distance between the station at Grand Army Plaza & Central Park South and the station at E 58th St & Madison, I would issue the following command:

```python
127.0.0.1:6379> GEODIST NYC:stations:location NYC:station:281 NYC:station:3457 ft
"671.4900"

```

Finally, the GEORADIUSBYMEMBER command is similar to the GEORADIUS command, but instead of taking a set of coordinates, the command takes the name of another member of the index and returns all of the members within a given radius centered on that member. To find all of the stations within 1000 feet of the Grand Army Plaza & Central Park South, enter the following:

```python
127.0.0.1:6379> GEORADIUSBYMEMBER NYC:stations:location NYC:station:281 1000 ft WITHDIST

1) 1) "NYC:station:281"
   2) "0.0000"
2) 1) "NYC:station:3132"
   2) "793.4223"
3) 1) "NYC:station:2006"
   2) "911.9752"
4) 1) "NYC:station:3136"
   2) "940.3399"
5) 1) "NYC:station:3457"
   2) "671.4900"

```

The geospatial indexing functions of Redis make it easy for developers to add location-aware features to their applications. If you have any questions regarding this post, please connect with me ([@tague](https://twitter.com/tague)) on Twitter.
