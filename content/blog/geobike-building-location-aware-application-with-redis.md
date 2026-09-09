---
title: "GeoBike: Building Location Aware Application with Redis"
linkTitle: "GeoBike: Building Location Aware Application with Redis"
url: "/blog/geobike-building-location-aware-application-with-redis/"
description: "I travel a lot on business as a Developer Advocate for Redis! I’m not much of a car guy, so when I have some free time, I prefer to walk or bike around a city. Many of the cities I’ve visited on..."
date: 2017-12-19
blogCategories:
- "Company"
- "Tech"
authors:
- "Tague Griffith"
lastmod: 2025-03-27
hidden: true
---

*By Tague Griffith, Head of Developer Advocacy · Published 19 December 2017 · updated 27 March 2025*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

![](/images/blog/122a3557fcaacede10c48be519b365783f772124-5000x3335.webp)

I travel a lot on business as a Developer Advocate for [Redis](https://redis.com)! I’m not much of a car guy, so when I have some free time, I prefer to walk or bike around a city. Many of the cities I’ve visited on business have bike share systems which let you borrow a bike for a few hours. Most of these systems have an app for renting bikes, but they only share the details of their system. This got me thinking – using publicly available bike share information to build an “app” showing you global information would be a fun way to demonstrate the geospatial features of Redis. With that GeoBike, the Redis bike share application was born.

GeoBike incorporates data from many different sharing systems, including the [CitiBike Bikeshare](https://www.citibikenyc.com/) in New York City. We are going to take advantage of the General Bikeshare Feed provided by Citi Bike system and use their data to demonstrate some of the features we can build using Redis to index geospatial data. The CitiBike data is provided under the [NYCBS Data Use Policy](https://www.citibikenyc.com/data-sharing-policy).

**General Bikeshare Feed Specification**

The General Bikeshare Feed Specification (GBFS) is an [open data specification](https://github.com/NABSA/gbfs) developed by the [North American Bike Share Association](http://nabsa.net/) to make it easier for map and transportation applications to add bike share systems into their platforms. The specification is currently in use by over 60 different sharing systems in the world.

The feed consists of several simple JSON data files containing information about the state of the system. The feed starts with a top level JSON file referencing the URLs of the subfeed data:

```python
{
    "data": {
        "en": {
            "feeds": [
                {
                    "name": "system_information",
                    "url": "https://gbfs.citibikenyc.com/gbfs/en/system_information.json"
                },
                {
                    "name": "station_information",
                    "url": "https://gbfs.citibikenyc.com/gbfs/en/station_information.json"
                },
            ]
        }
    },
    "last_updated": 1506370010,
    "ttl": 10
}

```

The first thing we’re going to focus on is loading information about the bike sharing stations into Redis. For this part of our application, we’re going to need data from the system_information and station_information feeds.

The system_information feed will provide us with the system ID, which is a short code that we will use to create namespaces for our Redis keys. The GBFS spec doesn’t specify the format of the system ID, but does guarantee that it is globally unique. Many of the Bikeshare feeds use short names like coast_bike_share, boise_greenbike, or topeka_metro_bikes for system IDs. Others use familiar geographic abbreviations such as NYC or BA, and one uses a UUID. Our code uses the identifier as a prefix to construct unique keys for the given system.

The station_information feed provides static information about the sharing stations that comprise the system. Stations are represented by [JSON](/redis-enterprise-documentation/developing/modules/rejson/) objects with several fields. There are several mandatory fields in the station object that provide the ID, name and location of the physical bike station. There are also several optional fields that provide helpful information such as “cross-street” or “accepted payment methods.” This is the primary source of information for this part of the bike sharing application.

**Building Our Database**

I’ve written a sample application, load_station_data.py, that mimics what would happen in a backend process for loading data from external sources.

**Finding the Bike Share Stations**

![](/images/blog/bc2183ed30bc82548bc7059422a551b8d5ffd06a-2403x2762.webp)

Loading the bike share data starts with the [systems.csv](https://github.com/NABSA/gbfs/blob/master/systems.csv) file from the [GBFS repository on Github](https://github.com/NABSA/gbfs).

The [systems.csv](https://github.com/NABSA/gbfs/blob/master/systems.csv) file provides the discovery URL for registered Bike Share Systems with an available GBFS feed. The discovery URL is the starting point for processing bike share information.

The load_station_data application takes each discovery URL found in the systems file and uses it to find the URL for two sub-feeds: system information and station information. The system information feed provides us with a key piece of information: the unique ID of the system. *Note, the system ID is also provided in the systems.csv file, but some of the identifiers in that file do not match the identifiers in the feeds, so we will always fetch the identifier from the feed.* Details on the system, like rental URL, phone numbers and emails could be useful in future versions of our application, so we’ll store the data in a Redis hash using the key ${system_id}:system_info.

**Loading the Station Data**

The station information provides us with data about every station in the system, including the location of the system. The load_station_data application iterates over every station in the station feed and stores the data about the station into a Redis hash using a key of the form ${system_id}:station:${station_id}. The location of each station is added to a [geospatial](/solutions/redis-geospatial-data/) index for the bike share using the GEOADD command.

**Updating Data**

On subsequent runs, we don’t want our code to remove all of the feed data from Redis and reload it into an empty Redis database, so we need to think about how we handle in-place updates of the data.

Our code starts by loading the set which contains all of the bike sharing stations information for the system currently being processed into memory. When information is loaded for a station, the station (by key) is removed from the in-memory set of stations. Once all of the station data is loaded, we’re left with a set containing all of the station data that must be removed for this system.

Our application iterates over this set of stations and creates a transaction to delete the station information, remove the station key from the geospatial indexes and remove the station from the list of stations for the system.

**Notes on the Code**

There are a few interesting things we should point out in the sample code. First you’ll notice that we added items to the geospatial indexes using the GEOADD command, but removed them using the ZREM command. The underlying implementation of the geospatial type uses sorted sets, so items are removed using ZREM. A word of caution: for simplicity, the sample code demonstrates working with a single Redis node; the transaction blocks will need to be restructured to run in a cluster environment.

If you are using Redis 4.0 (or later), you have some alternatives to the DELETE and HMSET commands used in this code. Redis 4.0 provides the [UNLINK](https://redis.io/commands/unlink) command as an asynchronous alternative to the DELETE command. UNLINK will remove the key from the keyspace but reclaims the memory in a separate thread. The [HMSET](https://redis.io/commands/hmset) command is [deprecated in Redis 4.0 and the HSET command is now variadic.](https://raw.githubusercontent.com/antirez/redis/4.0/00-RELEASENOTES)

**Notifying Clients**

At the end of the process, we send out a notification to those clients relying on our data. Using the Redis Pub/Sub mechanism, we send out a notification on the geobike:station_changed channel with the ID of the system.

**Data Model**

When structuring your data in Redis, the most important thing to think about is how you are going to query the information. For our bike share application, the two main queries we need to support are:

- Find stations near us
- Display information about stations

Redis provides two main data types that will be useful for storing our data, Hashes and Sorted Sets. The [hash type](https://redis.io/topics/data-types#Hashes) maps well to the JSON objects that represent stations and since Redis hashes don’t enforce a schema, so we can use them to store our variable station information.

Of course, to find stations geographically, we will want to build a geospatial index to search for stations relative to some coordinates. Redis provides [several commands](https://redis.io/commands#geo) to build up a geospatial index using the [Sorted Set](https://redis.io/topics/data-types-intro#redis-sorted-sets) data structure.

We’ll construct keys using the format ${system_id}:station:${station_id} for the hashes containing information about the stations and keys using the format ${system_id}:stations:location for the geospatial index used to find stations.

**Mapping the Results**

Let’s check the results of our data load by generating a map of the data loaded into Redis. We can create a map for the data by constructing a [KML (Keyhole Markup Language)](https://developers.google.com/kml/documentation/kml_tut) file and loading it into [Google Maps](https://mymaps.google.com). I’ve provided the generate_station_kml.py script to generate a KML file of the station locations for a station ID. Google maps limits KML files to 10 layers and 5000 features, so the KML generator application will only generates a file for a single system.

The application uses a redis-py scan_iter to iterate over the station keys (keys matching the pattern ${system_id}:station:*) and uses the [Python minidom package](https://docs.python.org/3.0/library/xml.dom.minidom.html) to construct the output XML.

I ran the generate_station_kml.py script against my Redis instance after running load_station_data.py and generated the following map of the New York City CitiBike system.

Map example:

If we look for the [6th and Canal Bike Station](https://www.google.com/maps/d/u/0/edit?mid=1OMAS6KznB9jJhzOI2Ph60t5BzOY&ll=40.72256343858286%2C-74.00527976306626&z=19) on our custom map, we see the coordinates 40.72242, -74.00566 and a blue pin on top of the CitiBike Station on the base layer of our map. Of course this is not a complete QA cycle, but a good way to eyeball the data to build confidence in our code.

In the next GeoBike post, we’ll look at how a developer can query the data in the database to add interesting features to an application. In the meantime, you can get the associated code from this post on Github. If you have any questions about this post, please connect with me (@tague) on Twitter.
