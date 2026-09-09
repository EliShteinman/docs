---
title: "Building a Health-Care-Provider Finder"
linkTitle: "Building a Health-Care-Provider Finder"
url: "/blog/building-a-health-care-provider-finder/"
description: "For patients, navigating the healthcare landscape can be bewildering. The terminology and options are often unfamiliar, and it can be difficult to even figure out how to get started. A “store..."
date: 2020-05-26
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-04
hidden: true
---

*By Redis   · Published 26 May 2020 · updated 4 March 2025*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

For patients, navigating the healthcare landscape can be bewildering. The terminology and options are often unfamiliar, and it can be difficult to even figure out how to get started. A “store finder” function, commonly found on retail sites, can help by letting you find a doctor or other healthcare provider located near you, based on a postal or zip code.

Unfortunately, though, this functionality isn’t always that easy to create. We live on a sphere, and if we want to find locations within a given distance in any direction, we have to project a circle onto a sphere and use a coordinate system that isn’t perfectly straightforward. All this equates to not-so-simple math. Redis, thankfully, has a wide array of geospatial capabilities to help you build out this type of functionality.

The most basic question we’re answering in this problem is pretty straightforward: “What health-care providers are near me?” To do this, you need the list of healthcare providers, the providers’ locations in latitude and longitude, and the location of the patient asking the question. The list of providers could look something like this:

![](/images/blog/701df4e0e8ed8bff1cfee387da140affa3c9f7a7-633x290.webp)

This is a small list for demonstration purposes, but in Redis this list could be quite vast, limited only by the amount of memory available.

Finding the patient’s location can be done a number of ways: reverse IP, postal-code matching (called a *geocoder)*, or even device GPS. Each method has pros, cons, and specific implementation details that are beyond the scope of this post. Regardless of the method, however, they all resolve down to a latitude and longitude. We’ll just assume the location of 53.5469, -113.4977 for now.

Getting the data into Redis can be a one-time affair or can be updated regularly as the list of providers changes. The GEOADD commands add a location to what’s known as a *geoset*. Geosets are a variant of Sorted Sets that encode the longitude and latitude into a GeoHash, which is stored in the Sorted Set member’s score. Let’s see what that looks like:

> GEOADD providers -113.4967 53.5574 royal-alex

(integer) 1

> GEOADD providers -113.5313 53.5177 cross-cancer-institute

(integer) 1

> GEOADD providers -113.4283 53.4608 grey-nuns-community-hospital

(integer) 1

> GEOADD providers -113.5247 53.5205 university-of-alberta-hospital

(integer) 1

> GEOADD providers -113.6119 53.5207 misericordia-community-hospital

(integer) 1

Of note in this example are the arguments. The first argument is the key, as typical in Redis. The second argument is the longitude, the third is the latitude, and finally the last argument is the member. (It’s super important to note that order of longitude and latitude are reversed from what you’re probably used to seeing.)

Now that we have our data in the system, whenever a user wants to find a provider, we just need to run a single Redis command to find the locations close to them:

> GEORADIUS providers -113.4977 53.5469 5 km

The first argument is our same key from before and the second and third arguments are the longitude and latitude (respectively) of the user. The fourth and fifth arguments are the distance and unit (km for kilometers, mi for miles, f for feet and, m for meters). The output will look like this:

1) "royal-alex"

2) "university-of-alberta-hospital"

3) "cross-cancer-institute"

## Geospatial with additional features

The example above would enable patients to find the healthcare nearest facility, but what if they want to go to a provider that offers something specific? What if they need a facility that offers more than one speciality? Redis can help with this, too.

Instead of using the GEO family of commands, we’ll use the [**Search and Query**](/redis-enterprise/redis-search/) module. Search and Query has a much richer capability to query data, yet retains the geospatial capabilities of the GEO family of commands. These richer capabilities do, however, require us to create a schema first.

> FT.CREATE ft_providers SCHEMA name TEXT services TAG location GEO

This creates an index called ft_providers with three fields: name, services, and location. name is a text field, so it can hold human language; services is a tag field that holds the tags representing the services offered; and finally location holds the latitude and longitude for the location.

Now, let’s add our locations to the index. We’ll use the FT.ADDcommand, which requires the index followed by a document ID to uniquely identify the document and then a document score. After this, the SCHEMA reserved word demarcates the options from the fields of the document, which follow in field name, value order. Let’s take a look:

```javascript
> FT.ADD ft_providers royal-alex 1.0 FIELDS name "Royal Alex Hospital" services "kidneyclinic,footclinic,gastroscopy,geriatrics,intensivecare,plasticsurgery,ultrasound" location "-113.4967 53.5574"
OK
> FT.ADD ft_providers cross-cancer-institute 1.0 FIELDS name "Cross Cancer Institute" services "ultrasound,fluoroscopy,mri,mammography,physicaltherapy,tumourtriage" location "-113.5313 53.5177"
OK
> FT.ADD ft_providers grey-nuns-community-hospital 1.0 FIELDS name "Grey Nuns Community Hospital" services "respiratorytherapy,orthopedics,nucelarmedicine,labouranddelivery,fluoroscopy,intensivecare" location "-113.4283 53.4608"
OK
> FT.ADD ft_providers university-of-alberta-hospital 1.0 FIELDS name "University of Alberta Hospital" services "colonoscopy,intensivecare,nucelarmedicine,respiratorytherapy,gastroscopy" location "-113.5247 53.5205"
OK
> FT.ADD ft_providers misericordia-community-hospital 1.0 FIELDS name "Misericordia Community Hospital" services "orthopedics,geriatrics,footclinic,ultrasound,labouranddelivery" location "-113.6119 53.5207"
OK
```


Once we have the data in Search and Query, we can start searching for facilities. In Search and Query we use a command called FT.SEARCH. The first argument is the index to search and the second argument is the *query*. In Search and Query, you specify a query that will determine what results are returned back to you. Queries can be quite simple or very complex, but, unlike in some other databases, the queries never do anything administrative or destructive.

Let’s say you want to find providers near the sample location used above, but only providers that offer ultrasound services. In Search and Query, the query would look like this:

```javascript
> FT.SEARCH ft_providers "@location:[-113.4967 53.5574 5 km] @services:{ultrasound}"
1) (integer) 2
2) "cross-cancer-institute"
3) 1) "name"
   2) "Cross Cancer Institute"
   3) "location"
   4) "-113.5313 53.5177"
   5) "services"
   6) "ultrasound,fluoroscopy,mri,mammography,physicaltherapy,tumourtriage"
4) "royal-alex"
5) 1) "name"
   2) "Royal Alex Hospital"
   3) "location"
   4) "-113.4967 53.5574"
   5) "services"
   6) "kidneyclinic,footclinic,gastroscopy,geriatrics,intensivecare,plasticsurgery,ultrasound"
```


The @ symbol in Search and Query means “search in a specific field.” The first part of the query is a search clause for a geospatial field named *location*. You’ll notice between the square brackets are the same arguments you’d see in a GEORADIUS command: longitude followed by latitude, then the search radius and unit. The second @ symbol is followed by the field name *services, *which means we’re searching in the services field of each document. Enclosed in curly braces is the name of tags that are required to be in the field. In this case, we’re looking for documents that contain the tag *ultrasound*. There is a space between the location and services search clauses—in Search and Query this is an implicit AND.

When building a UI, you can compose various user input into the same query to refine the results. Here’s a rough sketch of how this might work:

![](/images/blog/e8dae489d24a584e9528753e5f328a3031a453e9-1024x576.webp)

From the perspective of your application, the UI elements are a representation of the string, and as they change you template them into the string that is passed to FT.SEARCH. String interpolation inside things like SQL queries is risky (see [little ](https://xkcd.com/327/)Bobby Tables) due to administrative operations in the SQL language. In contrast, Search and Query queries can only find documents and not perform administrative operations, so only simple input validation and sanity checks are required.

Stepping up the complexity of the search, if a user checks both *ultrasound* and *geriatrics*, you would change the *services* clause to include both by inserting a pipe (|) between the two tags, as shown here:

```javascript
> FT.SEARCH ft_providers "@location:[-113.4967 53.5574 5 km] @services:{ultrasound|geriatrics}"
1) (integer) 2
2) "royal-alex"
3) 1) "name"
   2) "Royal Alex Hospital"
   3) "location"
   4) "-113.4967 53.5574"
   5) "services"
   6) "kidneyclinic,footclinic,gastroscopy,geriatrics,intensivecare,plasticsurgery,ultrasound"
4) "cross-cancer-institute"
5) 1) "name"
   2) "Cross Cancer Institute"
   3) "location"
   4) "-113.5313 53.5177"
   5) "services"
   6) "ultrasound,fluoroscopy,mri,mammography,physicaltherapy,tumourtriage"
```


Search and Query is flexible enough to handle practically any other feature you’d need in this type of application. Operations like name and name prefix search, sound-alikes names, and street names are all just incremental steps on this type of query. For example, you could add a cool wait-time feature by including a numeric field in the schema—because Search and Query is a real-time search engine, it is possible to update this value rapidly, so patients trying to find the provider with the shortest wait time would always get-up-to-date results.

Redis can help you [build a simple health-care-provider](/industries/healthcare/) finder with just a few lines of code, and Search and Query can fill out practically any feature you might need so patients can find the provider that meets their needs. Because Redis and Search and Query have built-in geospatial capabilities, you don’t need to do any math. Search and Query gives you a rich query capability that is safe to accept input from patients and is able to be updated in real-time, meaning you can make changes without delivering out-of-date information to your patients.
