---
title: "How to build a Python based application on Heroku using Redis"
linkTitle: "How to build a Python based application on Heroku using Redis"
url: "/tutorials/howtos/herokupython/"
description: "Create your Redis Cloud account. Follow this link to create a Redis Cloud subscription and database as shown below:"
aliases:
- "/tutorials/howtos-herokupython/"
date: 2026-02-25
lastmod: 2026-02-25
hidden: true
---

*Published 25 February 2026*

> **TL;DR:**
>
> To deploy a Python app with Redis on Heroku, create a Redis Cloud database, install the Heroku CLI, clone your Flask app, set your Redis connection details as Heroku config vars, and push to Heroku with `git push heroku`. Your app connects to Redis Cloud over a secure endpoint.

## What you'll learn

- How to create a Redis Cloud database and retrieve connection credentials
- How to set up a Heroku account and install the Heroku CLI
- How to configure a Python Flask app to connect to Redis Cloud
- How to deploy a Python web app to Heroku using Git

## What do you need before starting?

- A [Redis Cloud account](https://redis.io/try-free/) (free tier available)
- A [Heroku account](https://signup.heroku.com/login) with a verified payment method
- [Python 3](https://www.python.org/downloads/) installed locally
- [Git](https://git-scm.com/downloads) installed locally
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed locally

> Heroku no longer offers a free tier. You'll need a paid Heroku plan (Eco dynos or higher) to complete this tutorial. See [Heroku's pricing page](https://www.heroku.com/pricing) for current options.

## How do I create a Redis Cloud database?

Create your Redis Cloud account. [Follow this link to create a Redis Cloud](https://redis.io/try-free/) subscription and database as shown below:

![Redis Cloud console showing the new subscription and database creation form with plan selection and database naming fields](/images/site-mirror/38b53573f86c7cee03a5daf0230104249f6b20a5-1286x988.webp)

Save the database endpoint URL and password for future reference. You'll need these values to connect your Python app to Redis.

## How do I create a Heroku account?

If you are using Heroku for the first time, create your new Heroku account [through this link](https://signup.heroku.com/login).

![Heroku sign-up page with fields for first name, last name, email, role, and country](/images/site-mirror/f1b3cd61014510d10183c6d6186f2bf9c73e751e-900x1156.webp)

## How do I install the Heroku CLI?

Install the Heroku CLI so you can manage your apps from the terminal:

```bash
brew install heroku
```

For other operating systems, see the [Heroku CLI installation docs](https://devcenter.heroku.com/articles/heroku-cli).

## How do I log in to Heroku from the command line?

```bash
heroku login
heroku: Press any key to open up the browser to login or q to exit:
Opening browser to https://cli-auth.heroku.com/auth/cli/browser/XXXXXXXXXXA
Logging in... done
Logged in as your_email_address
```

## How do I connect a Python Flask app to Redis Cloud on Heroku?

For this demonstration, we will use a [sample rate-limiting application](https://github.com/redis-developer/basic-rate-limiting-demo-python) built with Python and Flask.

### Clone the repository

```bash
git clone https://github.com/redis-developer/basic-rate-limiting-demo-python
```

Then create a new Heroku app:

```bash
$ heroku create
Creating app... done, ⬢ fast-reef-76278
https://fast-reef-76278.herokuapp.com/ | https://git.heroku.com/fast-reef-76278.git
```

## How do I set Redis environment variables on Heroku?

Go to the Heroku dashboard, click **Settings**, and set `REDIS_ENDPOINT_URI` and `REDIS_PASSWORD` under **Config Vars**. Use the endpoint URL and password you saved when creating your Redis Cloud database.

You can also set them from the CLI:

```bash
heroku config:set REDIS_ENDPOINT_URI=<your-redis-endpoint> REDIS_PASSWORD=<your-redis-password>
```

![Heroku dashboard Settings tab showing the Config Vars section with REDIS_ENDPOINT_URI and REDIS_PASSWORD entries](/images/site-mirror/817f9aebd3ade7f03789e83606e6fa7c074d0703-1452x318.webp)

## How do I deploy the Python app to Heroku?

Heroku generates a random name (in this case `fast-reef-76278`) for your app, or you can pass a parameter to specify your own app name. Deploy your code by pushing to the Heroku remote:

```bash
$ git push heroku
Enumerating objects: 512, done.
Counting objects: 100% (512/512), done.
Delta compression using up to 12 threads
Compressing objects: 100% (256/256), done.
Writing objects: 100% (512/512), 1.52 MiB | 660.00 KiB/s, done.
Total 512 (delta 244), reused 512 (delta 244)
remote: Compressing source files... done.
remote: Building source:
remote:
remote: -----> Building on the Heroku-20 stack
remote: -----> Determining which buildpack to use for this app
remote: -----> Python app detected
…

remote: -----> Compressing...
remote:        Done: 59.3M
remote: -----> Launching...
remote:        Released v5
remote:        https://fast-reef-76278.herokuapp.com/ deployed to Heroku
remote:
remote: Verifying deploy... done.
To https://git.heroku.com/fast-reef-76278.git
 * [new branch]      master -> master
```

## How do I access the deployed application?

Open the app URL (for example, `https://fast-reef-76278.herokuapp.com/`) to see your application running with Redis Cloud:

![Sample rate-limiting demo application running in a browser, showing the request counter and rate limit status powered by Redis](/images/site-mirror/6eacda23ef0dca2fcbf6b254d9e0730fdf46de23-2000x702.webp)

## Next steps

- Learn more about [Redis Cloud](https://redis.io/cloud/) features and pricing
- Explore [rate limiting patterns with Redis](https://redis.io/glossary/rate-limiting/)
- Try other [Redis tutorials](https://redis.io/tutorials/) for Python and Flask
- Read the [Heroku Python deployment guide](https://devcenter.heroku.com/articles/getting-started-with-python) for production best practices
