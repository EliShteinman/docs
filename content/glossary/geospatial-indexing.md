---
title: "Geospatial Indexing"
linkTitle: "Geospatial Indexing"
url: "/glossary/geospatial-indexing/"
description: "Geospatial indexing is a technique used in databases to efficiently store and retrieve data based on their geographic location. It involves indexing the spatial data in a database using a..."
lastmod: 2025-06-30
---

*updated 30 June 2025*

## Geospatial Indexing Defined

Geospatial indexing is a technique used in databases to efficiently store and retrieve data based on their geographic location. It involves indexing the spatial data in a database using a specialized data structure that can quickly identify which objects or data points are located within a particular geographic region.

Geospatial indexing is particularly useful in applications that deal with large volumes of geographic data, such as mapping applications, geolocation services, and spatial analytics. By using geospatial indexing, these applications can quickly query and analyze data based on their location, without having to scan through large amounts of data to find the relevant information.

## Redis Geospatial Best Practices

Redis has several commands related to [geospatial indexing](https://redis.io/docs/data-types/geospatial/) (GEO commands) but unlike other commands these commands lack their own data type. These commands actually piggy back on the sorted set datatype. This is achieved by encoding the latitude and longitude into the score of the sorted set using the geohash algorithm.

Adding items to a geospatial index is easy. As an example, let’s assume you are tracking a group of cars as they travel down the road – we’ll call this set of cars simply “cars”. We’ll say your specific car can be identified as the member “my-car” (we use the term *member* because a geo index is just a form of a set). To add car to the set, we can run the command:

The first argument is the set we’re adding to, the second is the longitude, third is the latitude and the fourth is the member name.

To update the location of the car, you’ll just need to run the command again with new coordinates. This works because the geo index is just a set—repeated items are not allowed.

Let’s add a second car to the “cars” set – this time it’s driven by Robin:

Looking at the coordinates, you can tell these two cars are quite close, but how close? You can determine this by running the GEODIST command.

This means the two vehicles are about 90 meters apart. You can also specify other units:

This has pulled the same distance in feet. You can also use miles (mi) or kilometers (km).

Now, let’s see what items are in a radius from a certain point:

This returns all the members with 100 meters of the point given. You can also return members within a radius of another member in the set:

We can also include the distance by adding in the optional argument WITHDIST—this works for GEORADIUS or GEORADIUSBYMEMBER:

Another optional argument for both GEORADIUS and GEORADIUSBYMEMBER is WITHCOORD which returns the coordinates for each member. WITHDIST and WITHCOORD can be used together or separately:

Since geospatial indexes are just an alternate way of manipulating Sorted Sets, some operations can be achieved just by using the sorted set commands. If we want to remove “my-car” from the “cars” set, we’d need to use the sorted set command ZREM:

Redis provides a rich set of geospatial manipulation tools and only the basics were covered in this pattern. You can read more about the full set of commands on redis.io.
