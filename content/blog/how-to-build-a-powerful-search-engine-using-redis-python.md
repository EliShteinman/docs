---
title: "How to Build a Powerful Search Engine Using Python & RediSearch"
linkTitle: "How to Build a Powerful Search Engine Using Python & RediSearch"
url: "/blog/how-to-build-a-powerful-search-engine-using-redis-python/"
description: "While Google dominates the search engine landscape, it remains an awkward tool for programmers to have access to niche-specific resources on software development. This community feeds off content..."
date: 2021-10-22
blogCategories:
- "How To and Tutorials"
- "Tech"
- "Uncategorized"
authors:
- "Growth Team"
lastmod: 2025-03-27
hidden: true
---

*By Growth Team · Published 22 October 2021 · updated 27 March 2025*

![Blog tile image](/images/blog/afce574fd41fb6bc76981022daf35a9d2d87169b-772x520.webp)

While Google dominates the [search engine](/docs/redisearch-a-high-performance-search-engine-as-a-redis-module/) landscape, it remains an awkward tool for programmers to have access to niche-specific resources on software development. This community feeds off content on how to deploy software through different programming languages, which can be found in different awesome lists.

Google ranks websites through a strict optimization process that isn’t entirely compatible with content about programming. These in-demand resources are buried deeper in Google’s congested library, making it more challenging for programmers to have access to the most valuable programming content.

This creates a need for a search engine that can cut through the clutter to identify in-depth tutorials, blogs and step-by-step guides that can be found on [awesome lists](https://github.com/topics/awesome)… and this is where Awesome Search comes into play.

Unlike Google, this tool is more specific than general in its purpose, catering to search terms that demand curated resources about programming that might not rank well on Google.

Thanks to Redis, this tool was able to come to fruition. Data transmission between components occurred at lightning-speed and the search engine capabilities of RediSearch made indexing and querying hyper-efficient.

Let’s investigate how [this Launchpad app](https://launchpad.redis.com/?id=project%3Aawesome-search) got this done. But before we go any further, make sure to check out all of the other exciting applications we have on the [Launchpad](https://launchpad.redis.com/).

[Click here to view video](https://www.youtube.com/embed/Hbpb-Y0dXPs)

1. What will you build?
1. What will you need?
1. Architecture
1. Getting started (Frontend and Backend commands)
1. How it works
1. Conclusion

## 1. What will you build?

In this application you’ll build a search engine that specializes in identifying curated pieces of content on awesome lists. Below we’ll go through each stage in chronological order, highlighting what components are required to create this app as well as unpacking each one’s functionality.

### What is awesome list?

An awesome list is a curated list of coding projects within a specific niche, application or use case. Trying to find high-quality programming coding has always been a time-consuming process. Awesome lists removes this barrier by storing these curated lists of code projects in one area, making them more easily accessible for programmers.

## 2. What will you need?

- [**RediSearch**](/search/)**: **enables users to search for curated articles on awesome lists
- [**Django-redis**](https://github.com/jazzband/django-redis)**: **used to configure Redis as the backend for Django’s cache.
- [**Python**](https://www.python.org/)**: **the preferred programming language
- [**redis-py Client library**](https://github.com/andymccurdy/redis-py)**: **used as the python interface to the Redis key-value store
- [**Redis Queue**](/glossary/event-queue/)**: **used to submit new indexing jobs
- [**Raycast**](https://www.raycast.com/)**: **provides a more versatile way of controlling tools and installing script commands. Raycast is used as the CLI in this application.

## 3. Architecture

![](/images/blog/49e4372dfe214885ac7076b7621c9fe52c69917a-1364x1262.webp)

- Resources across different sources are stored in a variety of keys and data types using Redis.
- Resource data is stored as a JSON serialized string.
- [django-redis](https://github.com/jazzband/django-redis) is used to configure Redis as the backend for Django’s cache. This allows for neatly managing the connection for the [redis-py](https://github.com/andymccurdy/redis-py) and [redisearch-py](https://github.com/RediSearch/redisearch-py) client instances using the below command:

```python
get_redis_connection()

```

- CLI and [Raycast](https://www.raycast.com/) both query the Django app which is currently running on app engine
- The App engine queries the Redis instance which has the RediSearch module
- Data is transmitted from the Django app to Redis Queue to submit new indexing jobs

## 4. Getting Started

To get started, you’ll have to install the CLI along with Raycast. Let’s see how this is done.

**Pre-requisites:**

- Redis Enterprise Cloud
- Google App Engine (Django in App Engine)
- GitHub Personal Access Token

### Step 1. Set Up Redis Enterprise Cloud

Go to [/try-free/](/try-free/) and create a new Redis Enterprise Cloud subscription account. Afterwards, create a new database selecting RediSearch as a Module (shown below).

Once your database is set up, make sure to save the Endpoint URL and credentials in a safe place.

### Step 2. Setting up GitHub Personal access token

Under this section we’ll generate a token that can be used to access the [GitHub API](https://docs.github.com/).

The next step you should take is to request a personal access token for the Github API [here](https://github.com/settings/tokens).

### Step 3. Deploy Django on Google App Engine

For detailed steps for deploying Django on the App Engine see the official [documentation](https://cloud.google.com/python/django/appengine).

```python
$ gcloud auth login

```

1. Select the right project
1. Enable Cloud SQL Admin API

![](/images/blog/83dddfb937376934949a59b113a17df17fe95aad-1146x490.webp)

1. [Install and initialize the Cloud SDK](https://cloud.google.com/sdk/docs/install)

In the searchapp/ root.

Set your project ID:

```python
$ gcloud config set project <projectname>

```

1. [Create a MySQL database](https://cloud.google.com/python/django/appengine#creating_a_cloud_sql_instance).

![](/images/blog/28e1243ab362b267e23b57b7e7c74532779e693f-1238x1374.webp)

Then set the connection string/password in the deployment config.ini.

### To deploy run

```python
$ gcloud app deploy

```

### To view your application in the web browser

```python
$ gcloud app browse

```

### Step 4. Clone the repository

```python
$ git clone https://github.com/redis-developer/awesome-search

```

```python
$ cd awesome-search

```

### Step 5. Preparing the configuration file

```python
% cd searchapp
% cat config.ini
[redis]
PORT=13520
HOST=redis-13520.c276.us-east-1-2.ec2.cloud.redislabs.com
PASSWORD=<add your password>

[github]
ACCESS_TOKEN=<Add your GitHub Personal Access Token here>

[prod]
SECRET_KEY=
MYSQL_NAME=awesome-search-base
MYSQL_USER=root
MYSQL_CONNECTION_NAME=
MYSQL_PASS=

```

### Step 6. Setting up CLI

Create a dist bundle.

```python
$ python setup.py sdist

```

### Step 7. Push to PyPi

Before you push the python package, make sure to create an account with [https://pypi.org/](https://pypi.org/). Now let’s install twine Python module using the below command:

```python
$ pip install twine

```

Upload your python module:

```python
$ twine upload dist/*

```

You can directly install awesome-search in your local system using the below command:

### Step 8. Install awesome-search

You can directly install awesome-search in your local system using the below command:

```python
$ pip install awesome-search

```

**Usage:**

```python
awesome "[query]"

```

A search example would be to search ‘django redis’ projects. Make sure to sort results by stars.

```python
$ awesome "django redis" -l python -s

```

```python
awesome "django redis" -l python -sdjango-redis - Full featured redis cache backend for Django.Stars 2053 https://github.com/jazzband/django-redis
django-rq - A simple app that provides django integration for RQ (Redis Queue)Stars 1377 https://github.com/rq/django-rq
django-redis-cache - A Redis cache backend for djangoStars 995 https://github.com/sebleier/django-redis-cache
django-websocket-redis - Websockets for Django applications using Redis as message queueStars 846 https://github.com/jrief/django-websocket-redis
django-redisboard - Redis monitoring and inspection tool in django admin.Stars 228 https://github.com/ionelmc/django-redisboard

```

**Options**

Comma-delimited list of languages.

```python
--languages python,javascript

```

Use comma-delimited list of terms to filter awesome lists results. For example, ‘redis,django’ for awesome-redis, awesome-django.

```python
awesome "django redis" -l python,javascript -sdjango-redis - Full featured redis cache backend for Django.Stars 2053 https://github.com/jazzband/django-redis
django-rq - A simple app that provides django integration for RQ (Redis Queue)Stars 1377 https://github.com/rq/django-rq
django-redis-cache - A Redis cache backend for djangoStars 995 https://github.com/sebleier/django-redis-cache
django-websocket-redis - Websockets for Django applications using Redis as message queueStars 846 https://github.com/jrief/django-websocket-redis
django-redisboard - Redis monitoring and inspection tool in django admin.Stars 228 https://github.com/ionelmc/django-redisboard

```

```python
--lists [terms]

```

**Sort results by stars.**

```python
--stars

```

Hits to return.

```python
--results 5

```

```python
awesome "django redis" -l python,javascript -s --stars django-redis - Full featured redis cache backend for Django.Stars 2053 https://github.com/jazzband/django-redis
django-rq - A simple app that provides django integration for RQ (Redis Queue)Stars 1377 https://github.com/rq/django-rq
django-redis-cache - A Redis cache backend for djangoStars 995 https://github.com/sebleier/django-redis-cache
django-websocket-redis - Websockets for Django applications using Redis as message queueStars 846 https://github.com/jrief/django-websocket-redis
django-redisboard - Redis monitoring and inspection tool in django admin.Stars 228 https://github.com/ionelmc/django-redisboard

```

**Step 9. How to install Raycast**

Raycast is a piece of software that offers a more versatile way of controlling your tools and installing script commands. With just a few keystrokes, you can execute these commands from anywhere on your desktop.

It’s an efficient way of speeding up everyday tasks such as converting data, opening bookmarks and triggering dev workflows.

To add the script follow the instructions on the [Raycast script commands ](https://github.com/raycast/script-commands#install-script-commands-from-this-repository)page.

If you already have a script directory for your Raycast scripts simply copy the raycast/awesome_search.py script to it.

**Install Script Commands**

To install Raycast, you first need to install Script Commands:

**Step 1:** Choose your script from the [community repo](https://github.com/raycast/script-commands/tree/master/commands#apps) and save them into a new directory. Alternatively, you can use the [_enabled-commands](https://github.com/raycast/script-commands/tree/master/_enabled-commands) folder for this.

**Step 2:**Open the Extensions tab in the Raycast preferences

**Step 3: **Click the plus button

**Step 4: **Add Script Directory

**Step 5:** Select directories containing your Script Commands

**Useful tip: **It’s recommended that you don’t directly load the community script directories into Raycast. This is to avoid potential restructuring and new script commands suddenly appearing in Raycast.

![](/images/blog/c74435d3e2a7fb017cfdfcb4b95afceea25fb164-1600x981.webp)

## How it works

### Schema

All types of resources are prefixed with resource:. This will give you flexibility in extending new resource types such as blogs.

### Github Repos

To track which awesome lists appear on a repository list, you can simply use a set. The Redis SADD command is used to add members to a set stored at the key. SADD commands return the number of elements that were added to the set. This does not include all of the elements already present in the set.

Once you’ve indexed the contents, the set is added as a documentary property for filtering search results by awesome list.

```python
SADD resource:github:{owner}:{repo_name}:lists {list}
SET resource:github:{owner}:{repo_name} 
{
	'repo_name': resource['name'],
	'lists': # SMEMBERS resource:github:{owner}:{repo_name}:lists
	'body': resource['description'],
	'stargazers_count': resource['stargazers_count'],
	'language': resource['language'],
	'svn_url': resource['svn_url']
}

```

Additionally, when you insert a new resource, make sure to maintain a list of unique awesome lists and languages to implement faceted search.

```python
SADD resource:data:languages {language}
SADD resource:data:awesome_lists {list}

```

### Indexing

Next you must define the index. You define an index by using the RediSearch library.

### Index

All keys storing resource data are prefixed with resource:. This makes it a lot easier to define a RediSearch index with all the different resource types we want to search.

```python
definition = IndexDefinition(prefix=['resource:'])

```

As an option, if only specific resources such as Github Repos were to be indexed, more specific prefixes could be specified:

```python
prefix=['resource:github']

```

However, before making any queries the index needs to be built.

```python
self.client.create_index([TextField('body', weight=1),
                                      TextField('repo_name', weight=1.5),
                                      TextField('language', weight=1),
                                      TagField('lists')], definition=definition)

```

This specifies which fields should be indexed. Additionally the weight argument allows for increasing the effect of matches in certain fields such as “repo_name”.

Once the index is created documents are indexed in real-time as they are added to Redis. To add new documents to the index simply create a hash for that document.

### General Search

```python
GET /search?query=

```

Full text search across all the resources.

```python
FT.SEARCH {index} {query}

```

### Faceted Search

Faceted search is a programming trick that involves improving conventional search techniques. It allows users to narrow down search results by applying multiple filters based on faceted classification of the items.

```python
GET /search?query=&source=&language=&awesome-list=

```

RediSearch supports field modifiers in the query. Modifiers can be combined to implement filtering on multiple fields. You can use field modifiers to implement faceted search on specific sources, languages and awesome lists.

```python
FT.SEARCH {index} @resouce:(tweets|github) @language:(Python|C) @awesome_list:(awesome-python) {query}

```

Alternatively, instead of specifying the source (i.e tweet or GitHub) as a field modifier, separate indexes could be built for each source by providing a more specific key prefix.

```python
definition_git = IndexDefinition(prefix=['resource:github'])
definition_tweet = IndexDefinition(prefix=['resource:tweet'])

```

Having separate indexes will result in faster queries as well as introducing additional complexity for ranking/pagination if the user chooses to search across both sources.

## Conclusion: Bridging programmers with high-quality content

Google’s algorithms are not compatible with the resources on active lists, creating a barrier between users and this content that’s in demand. But thanks to Redis, this Launchpad app was able to create Awesome Search, providing programmers with access to invaluable coding content that would otherwise be buried deep in Google’s library.

Although each component played a crucial role in its formulation, RediSearch’s ability to find and index content with great efficiency was the crux of creating a powerful search engine. Without these elements, building Awesome Search would not be possible.

If you want to discover more about this app, then feel free to check it out on the [Redis Launchpad](https://launchpad.redis.com), where we also have a diverse range of different applications for you to discover.

[Watch the video](https://launchpad.redis.com/)

## Who created this application?

![](/images/blog/a37705510f4fec5b1f9896e7f8f7a3e174106de7-400x400.webp)

**Marko Arezina**

Marko is a specialist in backend development and is currently sharpening his skills with Shopify.

Make sure to [check out his GitHub profile](https://github.com/mrkarezina) to see what other activities he’s been involved in.
