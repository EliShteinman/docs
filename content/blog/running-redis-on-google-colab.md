---
title: "Running Redis on Google Colab"
linkTitle: "Running Redis on Google Colab"
url: "/blog/running-redis-on-google-colab/"
description: "Because of the increasing use of Redis for data science and machine learning, it is handy to run Redis directly from a Google Colab notebook. However, running Redis on Google Colab differs from how..."
date: 2022-01-28
blogCategories:
- "How To and Tutorials"
- "Tech"
authors:
- "Nava Levy"
lastmod: 2025-03-27
hidden: true
---

*By Nava Levy, Developer Advocate, Data Science & ML Operations · Published 28 January 2022 · updated 27 March 2025*

![Blog tile image](/images/blog/bf06bd62eb0cdad539214994a4674468e34b0d73-772x550.webp)

Because of the increasing use of Redis for data science and machine learning, it is handy to run Redis directly from a Google Colab notebook. However, running Redis on Google Colab differs from how you would set it up on your local machine or using Docker. In this post, I show you how you can run Redis on your Colab notebook, in two simple steps, directly from your browser.

[Google Colab](https://www.kdnuggets.com/2020/06/google-colab-deep-learning.html) is a popular browser-based environment for executing Python code on hosted Jupyter notebooks and training models for machine learning (ML), including free access to GPUs. It is a platform for data scientists and machine learning (ML) engineers to help them learn and develop ML models in Python. [Redis](https://hub.docker.com/_/redis) is an in-memory open source database that is increasingly being used in machine learning – from caching, [messaging](/solutions/messaging/) and [fast data ingest](/solutions/fast-data-ingest/), to semantic search and [online feature stores](/blog/building-feature-stores-with-redis-introduction-to-feast-with-redis/).

![An image with Redis and Colab logos](/images/blog/c972e1669e96d1fbf9934fa9aa7057bdd4689ccb-960x540.webp)

### Step 1: Installation

While Jupyter Notebooks support many languages, Colab supports only Python. To use Redis with [Python](https://www.python.org/), you need a[ Redis P](https://redis.io/docs/clients/python/)ython client. In this tutorial, we demonstrate the use of [redis-py](https://redis.io/docs/clients/python/), a Redis Python client, which we install using the [%pip install](https://ipython.readthedocs.io/en/7.23.0/interactive/magics.html#magic-pip) redis command.

You can run a shell command in Jupyter Notebook or Google Colab with [IPython](https://jakevdp.github.io/PythonDataScienceHandbook/01.05-ipython-and-shell-commands.html) by prefixing it with the ! character or % to use magic commands. A list of useful magic commands for data scientists is described in [Top 8 magic commands in Jupyter Notebook](https://towardsdatascience.com/top-8-magic-commands-in-jupyter-notebook-c1582e813560).

To install Redis and the Redis Python client:

```python
!curl -fsSL https://packages.redis.io/redis-stack/redis-stack-server-6.2.6-v7.focal.x86_64.tar.gz -o redis-stack-server.tar.gz 
!tar -xvf redis-stack-server.tar.gz
!pip install redis

```

### Step 2: Start the Redis Server

To start the Redis server run:

```python
!./redis-stack-server-6.2.6-v7/bin/redis-stack-server --daemonize yes

```

That’s it! It’s that simple.

## Connecting to the Redis server and Redis command functions

Let’s now look at the commands we need to verify that Redis is running, connect to it, and read and write data.

To verify that Redis is up and running, create a connection to Redis using the Python client redis-py and then ping the server:

```python
import redis
client = redis.Redis(host = 'localhost', port=6379)
 
client.ping()

```

If you get a response True, then you are good to go!

Once you are connected to Redis, you can read and write data [with Redis command functions](https://redis.io/docs/clients/python/). In this example, we use Redis as a [key value database](/nosql/key-value-databases/) (also called key value store). The following code snippet assigns the value bar to the Redis key foo, reads it back, and returns it:

```python
client.set('foo', 'bar')
client.get('foo')

```

If you want to play with the commands yourself, consult the[ Redis with Colab notebook](https://colab.research.google.com/drive/1S_5RmbxALznmJVVcO-yl3ylnJerTiX66?usp=sharing), which includes the code in this tutorial.
