---
title: "Redis for Python Developers Course Is Now Live at Redis University"
linkTitle: "Redis for Python Developers Course Is Now Live at Redis University"
url: "/blog/redis-for-python-developers-course-redis-university/"
description: "Our latest course, Redis for Python Developers (RU102PY) is now live at Redis University! You can sign up for free today."
date: 2020-08-11
blogCategories:
- "Company"
authors:
- "Andrew Brookins"
lastmod: 2026-09-01
hidden: true
---

*By Andrew Brookins, Former Curriculum Software Engineer at Redis · Published 11 August 2020 · updated 1 September 2026*

![Blog tile image](/images/site-mirror/77a8fa4bdc8389a26ea4de9142bc72db1a68bf18-1592x922.webp)

Our latest course, Redis for Python Developers (RU102PY) is now live at Redis University! You can [sign up for free](https://university.redis.com/courses/ru102py/) today.

I created this course, so in this post, I want to introduce myself, tell you more about what’s in the course, and give you an example of what you can learn from the full five-week session.

## Meet Andrew Brookins

I’m a 10+ year Python veteran and author of the book [The Temple of Django Database Performance](https://spellbookpress.com/books/temple-of-django-database-performance/). I created the Redis for Python developers course because Redis is an essential part of the modern internet, and yet finding patterns for writing efficient, well-organized code that uses Redis is hard.

## About the course

There are plenty of established patterns in Python for working with relational databases, but what about Redis? I’ve seen many one-off calls to Redis scattered through Python projects, and encountered plenty of apps that could have benefitted from [Redis’ geospatial](https://redis.io/commands/geoadd) capabilities or [Redis Streams](https://redis.io/docs/latest/develop/) but failed to use them. I built this course to give you the definitive patterns for writing Python code using all the powerful features that Redis has to offer. In the course, you’ll integrate Redis deeply with a [Flask](https://flask.palletsprojects.com/) application, gaining hands-on experience modeling data in Hashes, Sets, and Sorted sets, building geospatial indexes, and using [Redis Streams](https://university.redis.com/courses/ru202/).

![](/images/site-mirror/f92e2d4751cf051d36fb5c5e832b351ae0ed3f52-1024x587.webp)

*A map of solar sites in the RediSolar example application*

You’ll also learn how to squeeze every ounce of performance out of Redis with pipelines and Lua scripts. You’ll build rate limiters and leaderboards, learn how Redis 6’s new access control lists (ACLs) work, and more.

## Example content: Using data classes for models

Here’s an example of what you’ll learn in Redis for Python Developers. When you use relational databases from Python, you often do so with an [object relational mapping](/blog/object-relational-mapping-misconceptions/) (ORM) library like the [Django ORM](https://docs.djangoproject.com/en/3.0/topics/db/queries/), [SQLAlchemy](https://www.sqlalchemy.org/), or [Peewee](http://docs.peewee-orm.com/en/latest/). These libraries let you declare your data model, as shown in this example adapted from the Peewee documentation:

```python
from peewee import *
import datetime


db = SqliteDatabase('my_database.db')


class User(Model):
    username = CharField(unique=True)

    class Meta:
        database = db

```

In the example app for the Redis for Python Developers course, we use [data classes](https://www.python.org/dev/peps/pep-0557/#rationale) to declare our Redis data models. Data classes are a feature introduced in Python 3.7 that automatically generate “special” methods such as __init__() and __repr__() based on type hints.

Here’s an example model from the course:

```python
@dataclass(frozen=True, eq=True)
class SiteStats:
    """Reporting stats for a site."""
    last_reporting_time: datetime.datetime
    meter_reading_count: int
    max_wh_generated: float
    min_wh_generated: float
    max_capacity: float

```

This SiteStats model represents stats for a hypothetical solar array site in the example app. Because we specified the fields the class should have, including last_reporting_time and meter_reading_count, the class’s automatically generated __init__() method takes those parameters and adds them as members on new SiteStats instances.

When the app saves a SiteStats instance to Redis, or loads an instance from Redis, it does so using a “schema” class that handles validating, serializing, and deserializing the data.

Notice that the model declaration doesn’t mention Redis. That’s by design, and it’s a major part of the example project’s architecture. Rather than using an ORM to validate and persist data to Redis, we break these functions into separate pieces.

For validation—and serialization—we use a library called [marshmallow](https://marshmallow.readthedocs.io/en/stable/). Marshmallow can work with data classes to automatically validate, serialize, and deserialize data based on the type hints stored in the data classes via “schema” classes. Check out this example, which creates a marshmallow schema class for SiteStats instances, with which we validate, serialize, and deserialize SiteStats data to and from a Python dictionary:

```python
SiteStatsSchema = marshmallow_dataclass.class_schema(SiteStats)

```

Let’s try this out in an ipython terminal. First, let’s create a SiteStats instance.

```python
In [3]: import datetime                                                                                                   

In [4]: now = datetime.datetime.now()                                                                                         
In [5]: stats = SiteStats(last_reporting_time=now, meter_reading_count=5, max_wh_generated=22, min_wh_generated=1, max_capacity=100)                                                                                                          

In [6]: stats                                                                                                                 
Out[6]: SiteStats(last_reporting_time=datetime.datetime(2020, 7, 31, 15, 8, 45, 109063), meter_reading_count=5, max_wh_generated=22, min_wh_generated=1, max_capacity=100)


```

Next, let’s use our marshmallow schema class to serialize, or “dump,” the SiteStats instance to a Python dictionary.

```python
In [3]: import datetime                                                                                                   

In [4]: now = datetime.datetime.now()                                                                                         
In [5]: stats = SiteStats(last_reporting_time=now, meter_reading_count=5, max_wh_generated=22, min_wh_generated=1, max_capacity=100)                                                                                                          

In [6]: stats                                                                                                                 
Out[6]: SiteStats(last_reporting_time=datetime.datetime(2020, 7, 31, 15, 8, 45, 109063), meter_reading_count=5, max_wh_generated=22, min_wh_generated=1, max_capacity=100)


```

Now, let’s deserialize, or “load,” the data from a dictionary to a SiteStats instance, and verify that the new object is the same as the original SiteStats object:

```python
In [10]: stats2 = SiteStatsSchema().load(data)                                                                         
In [11]: stats == stats2                                                                                                      
Out[11]: True

```

That’s handy, but what makes this setup even more useful is validation. What happens if we pass bad data into SiteStatsSchema.load()? Let’s find out in our ipython terminal:

```python
In [13]: SiteStatsSchema().load({"meter_reading_count": "hey"})

[…]

ValidationError: {'meter_reading_count': ['Not a valid integer.'], 'min_wh_generated': ['Missing data for required field.'], 'last_reporting_time': ['Missing data for required field.'], 'max_wh_generated': ['Missing data for required field.'], 'max_capacity': ['Missing data for required field.']}


```

Pretty cool! It can tell we didn’t give it an integer for the “meter_reading_count” key, and that we’re missing the other required fields.

But what about persisting these models to Redis? For that, we use the [data access object](https://en.wikipedia.org/wiki/Data_access_object), or DAO, pattern, which the course covers in depth.

I hope this example piqued your interest in the Redis for Python Developers course!

## Did I mention it’s free?

Did I mention the course is free? All five weeks of instructor-led learning, access to our community chat server, source code for the example app, and the certificate of completion that you can earn are all free!

RU102PY: Redis for Python Developers has something to offer every Python developer, whether you’re building skills for your first Python job or designing a message broker for a microservices architecture. So come and [learn with us](https://university.redis.com/courses/ru102py/)! I’ll be around on our [chat server](https://discord.com/invite/z2N7Hgz) to answer any questions, and I look forward to meeting you.

[Click here to view video](https://www.youtube.com/embed/BxRJRNt7Qwc)
