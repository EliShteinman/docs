---
title: "How to build a NodeJS based application on Heroku using Redis"
linkTitle: "How to build a NodeJS based application on Heroku using Redis"
url: "/tutorials/how-to-build-a-nodejs-based-application-on-heroku-using-redis/"
description: "Create your Redis Cloud account. Follow this link to create Redis Cloud subscription and database as shown below:"
date: 2026-02-25
lastmod: 2026-02-25
hidden: true
---

*Published 25 February 2026*

> **TL;DR:**
>
> Create a Redis Cloud database, install the Heroku CLI, clone a Node.js sample app, set your Redis connection credentials as Heroku config vars, and run `git push heroku` to deploy. The app connects to Redis Cloud using the `REDIS_ENDPOINT_URI` and `REDIS_PASSWORD` environment variables.

## What you'll learn

- How to create a Redis Cloud database and retrieve connection credentials
- How to set up a Heroku account and install the Heroku CLI
- How to configure environment variables in Heroku for Redis Cloud
- How to deploy a Node.js application to Heroku with `git push`

## Prerequisites

- A [Redis Cloud](https://redis.io/try-free/) account (free tier available)
- A [Heroku](https://signup.heroku.com/login) account (requires a verified billing method)
- [Node.js](https://nodejs.org/) installed locally
- [Git](https://git-scm.com/) installed locally
- Basic familiarity with [Node.js and Redis](/tutorials/develop/node/gettingstarted/)

> Note: Heroku no longer offers a free tier. You will need a verified Heroku account with a billing method to complete this tutorial.

## How do I create a Redis Cloud database?

Create your Redis Cloud account. [Follow this link to create Redis Cloud](https://redis.io/try-free/) subscription and database as shown below:

![Redis Cloud subscription and database creation page](/images/site-mirror/38b53573f86c7cee03a5daf0230104249f6b20a5-1286x988.webp)

Save the database endpoint URL and password for future reference. You will need these values to connect your Heroku app to Redis.

## How do I set up Heroku for a Node.js app?

If you are using Heroku for the first time, create your new Heroku account [through this link](https://signup.heroku.com/login).

![Heroku account sign up page](/images/site-mirror/f1b3cd61014510d10183c6d6186f2bf9c73e751e-900x1156.webp)

### Install the Heroku CLI

Install the Heroku CLI so you can deploy from your terminal:

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

## How do I connect a Node.js app to Redis Cloud on Heroku?

For this demonstration, we will be using a [Sample Rate Limiting application](https://github.com/redis-developer/basic-redis-rate-limiting-demo-nodejs) built with Express and the node-redis client.

### Clone the repository

```bash
git clone https://github.com/redis-developer/basic-redis-rate-limiting-demo-nodejs
```

### Create a Heroku app

Run the below CLI to have a functioning Git repository that contains a simple application as well as a `package.json` file:

```bash
heroku create
Creating app... done, ⬢ rocky-lowlands-06306
https://rocky-lowlands-06306.herokuapp.com/ | https://git.heroku.com/rocky-lowlands-06306.git
```

### Set Redis environment variables

Go to Heroku dashboard, click "Settings" and set `REDIS_ENDPOINT_URI` and `REDIS_PASSWORD` under the Config Vars. Refer to your Redis Cloud database credentials from the first step.

You can also set these from the CLI:

```bash
heroku config:set REDIS_ENDPOINT_URI=<your-redis-endpoint> REDIS_PASSWORD=<your-redis-password>
```

![Configuring Redis environment variables in the Heroku settings dashboard](/images/site-mirror/817f9aebd3ade7f03789e83606e6fa7c074d0703-1452x318.webp)

## How do I deploy the Node.js app to Heroku?

Push your code to Heroku to trigger a deployment:

```bash
git push heroku
```

Wait for the build to complete. You will see output similar to:

```bash
remote: -----> Launching...
remote:        Released v3
remote:        https://rocky-lowlands-06306.herokuapp.com/ deployed to Heroku
remote:
remote: Verifying deploy... done.
To https://git.heroku.com/rocky-lowlands-06306.git
 * [new branch]      main -> main
```

### Access the running application

Open your app URL to see the deployed application:

```bash
heroku open
```

![Screenshot of the Node.js application running on Heroku](/images/site-mirror/6eacda23ef0dca2fcbf6b254d9e0730fdf46de23-2000x702.webp)

## Next steps

- Learn the basics of [Node.js with Redis](/tutorials/develop/node/gettingstarted/) including connection management and core commands
- Explore the [Python on Heroku with Redis](/tutorials/howtos/herokupython/) tutorial for a similar workflow in Python
- Browse [Redis Cloud documentation](https://redis.io/docs/latest/operate/rc/) for database scaling and configuration options
