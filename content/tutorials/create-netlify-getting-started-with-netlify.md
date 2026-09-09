---
title: "Getting Started with Netlify and Redis"
linkTitle: "Getting Started with Netlify and Redis"
url: "/tutorials/create/netlify/getting-started-with-netlify/"
description: "Netlify is a popular static site hosting and serverless platform. It provides a fast way to build, deploy, and scale modern web apps."
aliases:
- "/tutorials/create-netlify-getting-started-with-netlify/"
date: 2026-02-25
lastmod: 2026-02-25
hidden: true
---

*Published 25 February 2026*

> **TL;DR:**
>
> Connect your Netlify serverless functions to Redis Cloud by setting your Redis endpoint and password as Netlify environment variables, then use a Redis client library (like `node-redis` or `ioredis`) inside your serverless functions to cache data, manage sessions, or store real-time state.

## What you'll learn

- How Netlify deploys and serves JAMstack apps through its global CDN
- How to set up a free Redis Cloud database
- How to install and authenticate with the Netlify CLI
- How to configure continuous deployment from a Git repository
- How to connect your Netlify app to Redis Cloud using environment variables
- How to deploy a Next.js caching app powered by Redis to Netlify

## Prerequisites

- A [GitHub](https://github.com/) account
- [Node.js](https://nodejs.org/) (v14 or later) installed
- A free [Redis Cloud](https://redis.io/try-free/) account
- A free [Netlify](https://www.netlify.com/) account

## What is Netlify?

Netlify is a popular static site hosting and serverless platform. It provides a fast way to build, deploy, and scale modern web apps.

Netlify is built primarily for JAMstack sites, which combine JavaScript, APIs, and Markup to deliver apps that are performant, secure, and well suited for both devs and content editors.

![Netlify platform hero illustration](/images/site-mirror/4d2f3050d2e16d138776d1adf2cc4c95879e9ef3-1956x1202.webp)

## Why use Redis with Netlify?

Netlify serverless functions run on-demand and are stateless by default. Redis gives them a fast, shared data layer for:

- **Caching**: Store API responses or computed results to reduce latency and external API calls.
- **Session storage**: Manage user sessions across serverless function invocations.
- **Real-time data**: Share state between edge functions, background functions, and client-side code.
- **Rate limiting**: Throttle requests using Redis counters with automatic expiration.

## How does Netlify work?

![Netlify CI/CD workflow diagram from code to global CDN](/images/site-mirror/895aaa9ad5b100fd2ee7930de778c4a474affe9c-2000x1119.webp)

1. You write code and push it to a Git repository (e.g. GitHub).
2. When a change is merged into the main branch, a webhook notifies Netlify to start a new deploy.
3. Netlify pulls the latest code and runs the build command to generate static site files.
4. Netlify uses plugins and internal processing to pre-render pages as static HTML and optimize assets.
5. The static assets are pushed to Netlify's global CDN for fast delivery.

Netlify also provides:

- Out-of-the-box continuous integration and deployment
- Free SSL, CDN, and DNS management
- Serverless functions and edge functions
- Plugin ecosystem for extending build behavior

## How do I deploy a Redis-powered app to Netlify?

In this tutorial, you deploy a Redis caching app built with Next.js and TailwindCSS to Netlify. The whole process takes about 5 minutes.

### Step 1. Set up a free Redis Cloud account

Visit [redis.io/try-free](https://redis.io/try-free/) to create a free Redis Cloud account. Once your database is provisioned, you'll see an endpoint URL and password. Save these for a later step.

![Redis Cloud database endpoint and password](/images/site-mirror/9fc3e8d2a5449d5449dbedf3f3428662f9da4055-1346x881.webp)

### Step 2. Install the Netlify CLI

The Netlify CLI lets you configure continuous deployment directly from the command line.

```bash
npm install netlify-cli -g
```

Verify the installation:

```bash
netlify version
netlify-cli/8.15.3 darwin-x64 node-v14.17.3
```

### Step 3. Clone the repository

```bash
git clone https://github.com/redis-developer/nextjs-redis-netlify
```

### Step 4. Log in to Netlify

Authenticate with your Netlify account through the CLI:

```bash
netlify login
```

This opens a browser window where you grant access to the Netlify CLI. Once authenticated, you'll see:

<details>
<summary>Result</summary>

```bash
Already logged in via netlify config on your machine

Run netlify status for account details

To see all available commands run: netlify help
```

</details>

### Step 5. Configure continuous deployment

Run `netlify init` to set up continuous deployment for the project. This also creates a `netlify.toml` configuration file if one doesn't exist.

<details>
<summary>Result</summary>

```bash
netlify init
? What would you like to do? +  Create & configure a new site
? Team: Redis
Choose a unique site name (e.g. super-cool-site-by-redisdeveloper.netlify.app) or leave it blank for a random name. You can update the site name later.
? Site name (optional): undefined

Site Created

Admin URL: https://app.netlify.com/sites/super-cool-site-by-redisdeveloper
URL:       https://super-cool-site-by-redisdeveloper.netlify.app
Site ID:   a70bcfb7-b7b1-4fdd-be8b-5eb3b5dbd404

Linked to super-cool-site-by-redis-developer in /Users/redisdeveloper/projects/netlify/basic-caching-demo-nodejs/.netlify/state.json
? Your build command (hugo build/yarn run build/etc): yarn start
? Directory to deploy (blank for current dir): dist
? Netlify functions folder: functions
Adding deploy key to repository...
Deploy key added!

Creating Netlify GitHub Notification Hooks...
Netlify Notification Hooks configured!

Success! Netlify CI/CD Configured!

This site is now configured to automatically deploy from github branches & pull requests

Next steps:

  git push       Push to your git repository to trigger new site builds
  netlify open   Open the Netlify admin URL of your site
```

</details>

This creates a `netlify.toml` file with the following content:

```bash
 [build]
  command = "npm run build"
  publish = ".next"

[[plugins]]
  package = "@netlify/plugin-nextjs"
```

### Step 6. Push changes to GitHub

Push the latest changes to trigger the first Netlify build:

```bash
git add .
git commit -m "Pushing the latest changes"
git push
```

### Step 7. Open the Netlify admin URL

```bash
netlify open --admin
```

### Step 8. Add Redis Cloud environment variables

In the Netlify dashboard, go to **Site settings > Environment variables** and add your Redis Cloud endpoint and password.

![Configuring Netlify environment variables](/images/site-mirror/3813e11b940121beeda4e2e5bbdb33ebd970afc3-1894x800.webp)

### Step 9. Trigger the deployment

Click **Trigger deploy** in the Netlify dashboard to deploy the site with the Redis connection configured.

![Triggering a manual deploy in Netlify](/images/site-mirror/1a5fa2a36c9c107bc3354a1e89360fa8e0b2f271-2000x945.webp)

### Step 10. Access the app

Click the deploy URL to see the running app:

![Screenshot of the Next.js and Redis app running on Netlify](/images/site-mirror/3ee2ffca2f8650d7691be1bbd1e0309c6afddf91-595x378.webp)

## Frequently asked questions

### Can I use Redis with Netlify edge functions?

Yes. Netlify edge functions run on Deno at the edge and can connect to Redis Cloud using a REST-based Redis client or a TCP-compatible client. This lets you add caching or session lookups at the edge for lower latency.

### What Redis client should I use in Netlify serverless functions?

For Node.js-based Netlify functions, use [`node-redis`](https://github.com/redis/node-redis) or [`ioredis`](https://github.com/redis/ioredis). Both support Redis Cloud and handle connection pooling.

### Is Redis Cloud free to use with Netlify?

Redis Cloud offers a free tier that includes a 30 MB database, which is a great starting point for Netlify projects. [Sign up at redis.io/try-free](https://redis.io/try-free/).

## Next steps

- Explore the [Next.js Redis Netlify source code](https://github.com/redis-developer/nextjs-redis-netlify)
- Learn about [Netlify serverless functions](https://docs.netlify.com/functions/overview/)
- Try the [Redis quick start guide](https://redis.io/docs/latest/develop/get-started/)
- Read about [JAMstack architecture](https://jamstack.org/)
- Get started with [Redis Cloud](https://redis.io/try-free/)
