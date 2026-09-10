---
title: "How to build a Java based application on Heroku using Redis"
linkTitle: "How to build a Java based application on Heroku using Redis"
url: "/tutorials/how-to-build-a-java-based-application-on-heroku-using-redis/"
description: "Deploy a Java application on Heroku with a Redis Cloud database. This tutorial walks through every step from account setup to a live deployment using a sample rate-limiting app built with the Jedis..."
group: "For developers"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> Create a Redis Cloud database, install the Heroku CLI, clone the [sample Java rate-limiting app](https://github.com/redis-developer/basic-rate-limiting-demo-java), set `REDIS_ENDPOINT_URI` and `REDIS_PASSWORD` as Heroku config vars, and run `git push heroku` to deploy.

Deploy a Java application on Heroku with a [Redis Cloud](https://redis.io/cloud/) database. This tutorial walks through every step from account setup to a live deployment using a sample rate-limiting app built with the [Jedis](https://github.com/redis/jedis) client.

## What you'll learn

- How to create a Redis Cloud database and retrieve connection credentials
- How to set up a Heroku account and install the Heroku CLI
- How to connect a Java application to Redis Cloud using environment variables
- How to deploy a Java app to Heroku with `git push`

## What are the prerequisites?

Before you begin, make sure you have:

- **Java 11+** installed (check with `java -version`)
- **Git** installed (check with `git --version`)
- A free [Redis Cloud](https://redis.io/try-free/) account
- A [Heroku](https://signup.heroku.com/login) account (Heroku requires a verified account with a payment method on file)

> **Note:** Heroku no longer offers a free tier. Review [Heroku's current pricing](https://www.heroku.com/pricing) before proceeding. If you are looking for a free way to get started with Redis, see the [Redis Cloud free tier](https://redis.io/try-free/).

---

## How do I create a Redis Cloud database?

Create your free Redis Cloud account. [Follow this link to create a Redis Cloud](https://redis.io/try-free/) subscription and database as shown below:

![Redis Cloud subscription and database creation page](/images/site-mirror/38b53573f86c7cee03a5daf0230104249f6b20a5-1286x988.webp)

Save the database endpoint URL and password for future reference. You will need them when configuring Heroku environment variables.

For a deeper look at Redis Cloud setup, see the [Redis on Heroku](/tutorials/create/heroku/portal/) portal tutorial.

## How do I set up Heroku?

### Create a Heroku account

If you are using Heroku for the first time, create your new Heroku account [through this link](https://signup.heroku.com/login).

![Heroku account registration and login page](/images/site-mirror/f1b3cd61014510d10183c6d6186f2bf9c73e751e-900x1156.webp)

### Install the Heroku CLI

```bash
brew install heroku
```

### Log in to Heroku

```bash
heroku login
heroku: Press any key to open up the browser to login or q to exit:
Opening browser to https://cli-auth.heroku.com/auth/cli/browser/XXXXXXXXXXA
Logging in... done
Logged in as your_email_address
```

## How do I connect a Java app to Redis Cloud on Heroku?

For this demonstration, we will be using a [sample rate-limiting application](https://github.com/redis-developer/basic-rate-limiting-demo-java) that showcases Redis-backed request throttling with the Jedis client.

### Clone the repository

```bash
git clone https://github.com/redis-developer/basic-rate-limiting-demo-java
```

### Create a Heroku app

```bash
heroku create
Creating app... done, ⬢ hidden-woodland-03996
https://hidden-woodland-03996.herokuapp.com/ | https://git.heroku.com/hidden-woodland-03996.git
```

### Set environment variables

Go to the Heroku dashboard, click **Settings**, and set `REDIS_ENDPOINT_URI` and `REDIS_PASSWORD` under **Config Vars**. Use the credentials you saved when creating your Redis Cloud database.

![Configuring Redis environment variables in the Heroku dashboard](/images/site-mirror/817f9aebd3ade7f03789e83606e6fa7c074d0703-1452x318.webp)

You can also set config vars from the CLI:

```bash
heroku config:set REDIS_ENDPOINT_URI=redis://your-endpoint:port
heroku config:set REDIS_PASSWORD=your-password
```

## How do I deploy the Java app to Heroku?

Heroku generates a random name (in this case `hidden-woodland-03996`) for your app, or you can pass a parameter to specify your own app name. Deploy your code:

```bash
git push heroku
remote:        BUILD SUCCESSFUL in 1m 5s
remote:        12 actionable tasks: 12 executed
remote: -----> Discovering process types
remote:        Procfile declares types -> web
remote:
remote: -----> Compressing...
remote:        Done: 298.9M
remote: -----> Launching...
remote:        Released v3
remote:        https://hidden-woodland-03996.herokuapp.com/ deployed to Heroku
remote:
remote: Verifying deploy... done.
To https://git.heroku.com/hidden-woodland-03996.git
 * [new branch]      master -> master
```

## How do I access the deployed application?

Open `https://hidden-woodland-03996.herokuapp.com/` (replace with your app URL) to see the running application:

![Screenshot of the Java-based application running on the Heroku platform](/images/site-mirror/6eacda23ef0dca2fcbf6b254d9e0730fdf46de23-2000x702.webp)

---

## Next steps

- **Learn Java + Redis fundamentals:** [Getting Started with Redis and Java](/tutorials/develop/java/getting-started/) covers the Jedis client, connections, and basic operations.
- **Explore the Heroku + Redis ecosystem:** The [Redis on Heroku](/tutorials/create/heroku/portal/) portal walks through managing Redis Cloud as a Heroku add-on.
- **Try another language on Heroku:** See how to [deploy a Node.js app on Heroku with Redis](/tutorials/how-to-build-a-nodejs-based-application-on-heroku-using-redis/).
- **Build more with Redis:** Browse the full [Redis tutorials](/tutorials/) catalog for caching, rate limiting, session management, and more.
