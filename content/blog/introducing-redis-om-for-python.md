---
title: "Introducing Redis OM for Python"
linkTitle: "Introducing Redis OM for Python"
url: "/blog/introducing-redis-om-for-python/"
description: "I’m excited to introduce Redis OM for Python, a powerful new developer-centric library for Redis that gives you features like object mapping, data validation, and more."
date: 2021-12-08
blogCategories:
- "How To and Tutorials"
- "New Product Announcements"
- "Tech"
authors:
- "Andrew Brookins"
lastmod: 2025-03-27
hidden: true
---

*By Andrew Brookins, Former Curriculum Software Engineer at Redis · Published 8 December 2021 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/5f588e4f7d6461f7c7e7dc0e354be633cd8cc1c9-772x550.webp)

## Intuitive Object Mapping and Fluent Queries for Redis and Python

I’m excited to introduce Redis OM for Python, a powerful new developer-centric library for Redis that gives you features like object mapping, data validation, and more.

This preview release of Redis OM for Python lets you model data with **declarative models** that will feel right at home to users of object-relational mappers (ORMs) like SQLAlchemy, Peewee, and the Django ORM.

But there’s more! Every Redis OM model is also a [Pydantic](https://github.com/samuelcolvin/pydantic) model, so you can use Pydantic’s robust and extensible data validation features. Moreover, Redis OM models will work anywhere that a Python library expects Pydantic models. So, you can use a Redis OM model with FastAPI to automatically validate and generate API documentation for API endpoints.

Another feature dear to my heart is that Redis OM supports fluent query expressions and secondary indexes. Redis OM for Python also supports both asynchronous (asyncio) and synchronous programming in the same library. And the list of awesome features goes on!

Continue reading to learn about how I built this library and some behind-the-scenes details about a few key features. Or, if you’re ready to play with the code, check out the [getting started tutorial](https://github.com/redis/redis-om-python/blob/main/docs/getting_started.md).

## Declarative models for Redis

Developers usually access Redis through a client library to create Redis *data structures* (e.g., Hashes) and then *commands* against them.

Many people enjoy this command-based interface because it’s simpler than writing SQL queries with a relational database. But when was the last time you wrote SQL? Developers using modern web frameworks tend to use ORMs instead, especially with declarative models.

What I love about ORMs is that they remove a lot of complexity that isn’t related to the problem you’re trying to solve. We created Redis OM so you can finally have the same experience with Redis.

## Hashes or JSON, your choice

Redis OM for Python includes two base model classes that you can use to build your models: **HashModel** and **JsonModel.**

Open-source Redis users can use **HashModel** to store data in Redis as Hashes, while users who have the RedisJSON Redis module installed or are using [Redis Enterprise Cloud or Software](/try-free/) can use **JsonModel** to store data natively as JSON objects. I’ll talk more about the difference between these classes later, but for now, we’ll use **HashModel.**

## Concise model definitions

Take a look at this example Redis OM code that defines a **Customer** model and uses it to save data to Redis:

```python
import datetime
from typing import Optional

from pydantic import EmailStr

from redis_om import HashModel


class Customer(HashModel):
    first_name: str
    last_name: str
    email: EmailStr
    join_date: datetime.date
    age: int
    bio: Optional[str]


# First, we create a new `Customer` object:
andrew = Customer(
    first_name="Andrew",
    last_name="Brookins",
    email="andrew.brookins@example.com",
    join_date=datetime.date.today(),
    age=38,
    bio="Python developer, works at Redis, Inc."
)

# The model generates a globally unique primary key automatically
# without needing to talk to Redis.
print(andrew.pk)
# > '01FJM6PH661HCNNRC884H6K30C'

# We can save the model to Redis by calling `save()`:
andrew.save()

# To retrieve this customer with its primary key, we use `Customer.get()`:
assert Customer.get(andrew.pk) == andrew

```

This concise model definition immediately gives you methods like `get()` and `save()`. Behind the scenes, these methods manage data in Redis Hashes.

Redis OM does much more though. It also generates globally unique and sortable primary keys. This part is super useful, so let me explain how it works.

## Globally unique primary keys

Redis OM automatically generates a globally unique primary key for every model instance. You can use this primary key to save and retrieve model data in Redis.

These primary keys are guaranteed to be globally unique, but they’re also generated entirely in the client without any request to Redis. They’re also sortable and compact. All of this is possible thanks to the Universally Unique Lexicographically Sortable Identifiers (ULID) specification.

Redis OM primary keys are ULIDs, courtesy of [python-ulid](https://github.com/mdomke/python-ulid). You can read more about the ULID specification [here](https://github.com/ulid/spec). It’s very cool!

Aside from these persistence features, though, you also get data validation with [Pydantic](https://github.com/samuelcolvin/pydantic). Let’s dig into how validation works.

## Data validation with Pydantic

One difference between Redis and relational databases is that Redis does not enforce a schema, so you can write a string in Redis and then overwrite it with a number later. This is more flexible than relational databases, but also means applications are responsible for data validation.

We think you shouldn’t have to figure out the best way to handle validation in your applications, so every Redis OM model is also a Pydantic model. This means you get Pydantic validation based on the type hints in your model, and you can control validation through standard Pydantic hooks, including custom validators.

Here’s some example code that shows how validation works:

```python
import datetime
from typing import Optional

from pydantic import EmailStr, ValidationError

from redis_om import HashModel


class Customer(HashModel):
    first_name: str
    last_name: str
    email: EmailStr
    join_date: datetime.date
    age: int
    bio: Optional[str]


try:
    Customer(
        first_name="Andrew",
        last_name="Brookins",
        email="Not an email address!",
        join_date=datetime.date.today(),
        age=38,
        bio="Python developer, works at Redis, Inc."
    )
except ValidationError as e:
    print(e)
    """
    pydantic.error_wrappers.ValidationError: 1 validation error for Customer
     email
       value is not a valid email address (type=value_error.email)
    """

```

If Redis OM for Python only gave you persistence methods and data validation, I’d think it was pretty cool. But we wanted to handle even more complexity for you, and to do that we needed to help you write expressive queries just like you would with an ORM. Next, I’ll talk about how these queries work.

## Fluent query expressions

ORMs don’t just give you declarative models. They also provide an API that lets you query for data based on attributes *other* than the primary key. Imagine finding all customers over a certain age, customers who signed up before a certain date, etc.

Out of the box, Redis is great at looking up data with a primary key. It is, after all, a key-value store whose values are data structures. But Redis doesn’t include a querying and secondary indexing system, so if you want to index and query data, you have to manage indexes yourself in complex ways.

Here again, we wanted to handle this complexity for you, so we built fluent query expressions on top of an essential Redis module: [RediSearch](/search/). RediSearch is a source-available module that gives you the querying and indexing capabilities missing from Redis.

Let’s see what happens if we mark a few fields on our **Customer **model as `index=True`. Now, we can use the model to query:

```python
import datetime
from typing import Optional

from pydantic import EmailStr

from redis_om import (
    Field,
    HashModel,
    Migrator
)
from redis_om import get_redis_connection

                 
class Customer(HashModel):
    first_name: str
    last_name: str = Field(index=True)
    email: EmailStr
    join_date: datetime.date
    age: int = Field(index=True)
    bio: Optional[str]


# Now, if we use this model with a Redis deployment that has the
# RediSearch module installed, we can run queries like the following.

# Before running queries, we need to run migrations to set up the
# indexes that Redis OM will use. You can also use the `migrate`
# CLI tool for this!
redis = get_redis_connection()
Migrator(redis).run()

# Find all customers with the last name "Brookins"
Customer.find(Customer.last_name == "Brookins").all()

# Find all customers that do NOT have the last name "Brookins"
Customer.find(Customer.last_name != "Brookins").all()

# Find all customers whose last name is "Brookins" OR whose age is 
# 100 AND whose last name is "Smith"
Customer.find((Customer.last_name == "Brookins") | (
        Customer.age == 100
) & (Customer.last_name == "Smith")).all()

```

This expression syntax may look familiar— it’s a blend of everything I like about [Peewee](http://docs.peewee-orm.com/en/latest/), [SQLAlchemy](https://www.sqlalchemy.org), and the [Django ORM](https://docs.djangoproject.com/en/3.2/topics/db/).

## Embedded models

As you model complex data with Redis, you inevitably want to store embedded data. If you were modeling customer data using Redis Hashes, you might want to store data like the customer’s shipping addresses within an individual customer’s Hash. Unfortunately, Redis Hashes can’t store nested containers like Lists, Sets, or other Hashes, so this doesn’t work.

Here’s where storing data as a native JSON object can make a lot of sense. If you model the customer data as a JSON document, you can embed whatever you want inside the record for a single customer.

However, Redis does not natively support JSON. This is exactly why we created the source-available [RedisJSON module](https://redis.io/docs/data-types/json/). RedisJSON makes it possible to use Redis as a document database, storing and querying complex JSON objects with ease.

With Redis OM for Python, if your Redis instance has RedisJSON installed, you can use the **JsonModel** class. This model class lets you embed **JsonModels **within other **JsonModels**. Imagine customers having an array of orders, each of which has an array of items, and so on.

Here’s what embedded JSON models look like with Redis OM for Python:

```python
import datetime
from typing import Optional

from redis_om import (
    EmbeddedJsonModel,
    JsonModel,
    Field,
    Migrator,
)
from redis_om import get_redis_connection


class Address(EmbeddedJsonModel):
    address_line_1: str
    address_line_2: Optional[str]
    city: str = Field(index=True)
    state: str = Field(index=True)
    country: str
    postal_code: str = Field(index=True)


class Customer(JsonModel):
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    email: str = Field(index=True)
    join_date: datetime.date
    age: int = Field(index=True)
    bio: Optional[str] = Field(index=True, full_text_search=True,
                               default="")

    # Creates an embedded model.
    address: Address


# With these two models and a Redis deployment with the RedisJSON 
# and RediSearch modules installed, we can run queries like the
# following.

# Before running queries, we need to run migrations to set up the
# indexes that Redis OM will use. You can also use the `migrate`
# CLI tool for this!
redis = get_redis_connection()
Migrator(redis).run()

# Find all customers who live in San Antonio, TX
Customer.find(Customer.address.city == "San Antonio",
              Customer.address.state == "TX")

```

Not only do you get the flexibility to store complex JSON objects, but Redis OM for Python is aware of these nested structures and lets you write query expressions against them. Awesome!

## Trying Redis OM for Python

I hope you can tell how excited I am about Redis OM for Python. I’ve worked to bring some of the best of the current Python ecosystem together to handle complexity for Redis developers that, in my opinion, no one should have to deal with.

If I’ve piqued your interest, check out the [getting started tutorial](https://github.com/redis/redis-om-python/blob/main/docs/getting_started.md). Redis OM for Python is in a *very early stage, *which we call a “Preview.” So there are rough spots, you’ll run into bugs, and we’re still working to deliver complete documentation. But the vision is there, and I encourage you to check it out.

Finally, I’ll say that we started with declarative data models, but we have so much more we want to build— both for data modeling and beyond. Stay tuned for more exciting Redis OM features!
