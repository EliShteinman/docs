---
title: "Redis on Heroku"
linkTitle: "Redis on Heroku"
url: "/tutorials/create/heroku/portal/"
description: "Heroku is a cloud Platform as a Service (PaaS) that supports multiple programming languages and is used as a web application deployment platform. Heroku lets developers build, run, and scale apps..."
aliases:
- "/tutorials/create-heroku-portal/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> To set up Redis on Heroku, create a [Redis Cloud account](https://redis.io/try-free/), provision a database, then add your Redis connection string to your Heroku app's config vars. Redis Cloud gives you a fully managed Redis instance that integrates with any Heroku application.

Heroku is a cloud Platform as a Service (PaaS) that supports multiple programming languages and is used as a web application deployment platform. Heroku lets developers build, run, and scale apps across all supported languages including Java, Node.js, Python, PHP, Ruby, and Go. This guide walks you through setting up Redis on Heroku using Redis Cloud so you can add a managed Redis database to your Heroku applications.

## Prerequisites

Before you begin, make sure you have:

- A [Heroku account](https://signup.heroku.com/login) (a paid plan is required; Heroku [discontinued its free tier](https://blog.heroku.com/next-chapter) in November 2022)
- The [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed on your system
- [Git](https://git-scm.com/downloads) installed
- A [Redis Cloud account](https://redis.io/try-free/) (the free tier includes 30 MB)

## What is Redis Cloud?

Redis Cloud is a fully managed cloud service for hosting and running your Redis dataset in a highly available and scalable manner with predictable, stable performance. Redis Cloud lets you run Redis in the cloud and access your instance through Redis Insight, the Redis CLI, or any Redis client library. You can get started instantly with your first Redis database and then add more databases or resize your plan without affecting existing data.

## How do I set up Redis on Heroku?

You can connect Redis Cloud to your Heroku app by provisioning a Redis Cloud database and configuring your Heroku app's environment with the Redis connection string.

### 1. Create a Redis Cloud account

Create your free Redis Cloud account by visiting [redis.io/try-free](https://redis.io/try-free/). Follow the [Redis Cloud quickstart guide](https://redis.io/docs/latest/operate/rc/rc-quickstart/) to create your database and retrieve your endpoint, port, and credentials. You will need these values to configure the Heroku Redis connection string later.

### 2. Create a Heroku account

If you don't already have one, create a Heroku account at [signup.heroku.com](https://signup.heroku.com/login).

> **NOTE**
>
> Heroku [discontinued its free tier](https://blog.heroku.com/next-chapter) in November 2022. You will need a paid Heroku plan (Eco, Basic, or higher) to deploy applications.

### 3. Install the Heroku CLI

Install the Heroku CLI on your system:

```bash
brew install heroku
```

For other installation methods, see the [Heroku CLI documentation](https://devcenter.heroku.com/articles/heroku-cli).

### 4. Log in to Heroku

```bash
heroku login
heroku: Press any key to open up the browser to login or q to exit:
Opening browser to https://cli-auth.heroku.com/auth/cli/browser/XXXXXXXXXXA
Logging in... done
Logged in as your_email_address
```

### 5. Connect your application to Redis Cloud

For this walkthrough, we'll use a [sample rate-limiting application](https://github.com/redis-developer/basic-rate-limiting-demo-python).

#### Clone the repository

```bash
git clone https://github.com/redis-developer/basic-rate-limiting-demo-python
```

#### Create a Heroku app

Run the command below to create a new Heroku app:

```bash
heroku create
Creating app... done, ⬢ lit-bayou-75670
https://lit-bayou-75670.herokuapp.com/ | https://git.heroku.com/lit-bayou-75670.git
```

![Terminal output of the heroku create command showing the application URL](/images/site-mirror/68fd12cfb8346d46fe9281ea36a5857116069fbc-1047x409.webp)

### 6. How do I configure the Heroku Redis connection string?

Go to the Heroku dashboard, click **Settings**, and add the following under **Config Vars**:

- `REDIS_URL` — your Redis Cloud endpoint (e.g., `redis://default:<password>@<host>:<port>`)
- `REDIS_PASSWORD` — your Redis Cloud database password

Refer to [Step 1](#1-create-a-redis-cloud-account) for the correct values.

![Configuring Redis environment variables in the Heroku dashboard settings](/images/site-mirror/6551a6eb20de6c96da47b65cf6273f73fb623771-1047x581.webp)

You can also set config vars from the CLI:

```bash
heroku config:set REDIS_URL="redis://default:<password>@<host>:<port>"
heroku config:set REDIS_PASSWORD="<password>"
```

### 7. Deploy to Heroku

Push your code to the Heroku remote:

```bash
git push heroku
remote: -----> Build succeeded!
remote: -----> Discovering process types
remote:        Procfile declares types -> web
remote:
remote: -----> Compressing...
remote:        Done: 32.9M
remote: -----> Launching...
remote:        Released v5
remote:        https://lit-bayou-75670.herokuapp.com/ deployed to Heroku
remote:
remote: Verifying deploy... done.
To https://git.heroku.com/lit-bayou-75670.git
* [new branch]      main -> main
```

#### Check the logs

```bash
heroku logs --tail
2021-03-27T03:48:30.000000+00:00 app[api]: Build succeeded
2021-03-27T03:48:33.956884+00:00 heroku[web.1]: Starting process with command `node server/index.js`
2021-03-27T03:48:36.196827+00:00 app[web.1]: App listening on port 11893
```

### 8. Access the app

Open the deployed application in your browser:

```bash
heroku open
```

![Screenshot of the rate limiting application frontend on Heroku](/images/site-mirror/96942177c810e26c7b07ba78df1d3d022f490b47-1047x701.webp)

## Next steps

Now that you have Redis running on Heroku, explore these related tutorials:

- [How to build a Python-based application on Heroku using Redis](/tutorials/howtos/herokupython/) — deploy a Python app on Heroku with Redis Cloud integration.
- [How to build a Node.js-based application on Heroku using Redis](/tutorials/how-to-build-a-nodejs-based-application-on-heroku-using-redis/) — deploy a Node.js app on Heroku connected to Redis Cloud.
- [Redis Cloud quickstart](https://redis.io/docs/latest/operate/rc/rc-quickstart/) — learn more about provisioning and managing Redis Cloud databases.
