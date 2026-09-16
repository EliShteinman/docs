---
title: "Use Redis with no setup required with Redis Sandbox"
linkTitle: "Use Redis with no setup required with Redis Sandbox"
url: "/tutorials/howtos/redis-sandbox/"
description: "Redis Sandbox (also known as Redis Playground) is an interactive, online Redis console that lets you experiment with Redis commands in a safe, isolated environment—no setup required. Whether you're..."
group: "For developers"
aliases:
- "/tutorials/howtos-redis-sandbox/"
date: 2026-02-25
lastmod: 2026-02-25
hidden: true
mirrored: true
---

*Published 25 February 2026*

> **TL;DR:**
>
> Want to try Redis without installing anything? [Redis Sandbox](https://redis.io/try/sandbox/) is a free, browser-based tool that lets you run Redis commands instantly—no downloads, no configuration, no account required.

Redis Sandbox (also known as Redis Playground) is an interactive, online Redis console that lets you experiment with Redis commands in a safe, isolated environment—no setup required. Whether you're [learning what Redis is](/tutorials/what-is-redis/), testing queries, or demonstrating features, Redis Sandbox is the perfect place to get hands-on experience and test Redis commands online.

## What you can do

- **Run read queries** against preloaded sample datasets
- **Run write queries** in a temporary session with automatic expiry
- **Browse predefined queries** covering common Redis operations and data types
- **View query history** to revisit and re-run past commands
- **Share queries** with a generated link—great for collaboration or teaching
- **Explore Redis data types** like strings, hashes, lists, sets, and sorted sets

## Accessing Redis Sandbox

Visit the Redis Sandbox at: [https://redis.io/try/sandbox/](https://redis.io/try/sandbox/)

You'll be greeted with an interface designed for quick experimentation.

![Redis Sandbox interactive interface overview](/images/site-mirror/8d016a28a5177c24d3ba68f2d31e6b07937f25b0-1038x577.webp)

## Exploring the Interface

### Selecting a Predefined Query

- Click `Select query` in the left sidebar.

![Clicking the Select query button in the Redis Sandbox sidebar](/images/site-mirror/d245180f8e2fbfd0c112a448f40e10526dad9cc1-1038x553.webp)

- A popup will appear with a list of predefined queries covering common Redis operations.

![Popup menu showing a list of predefined Redis queries](/images/site-mirror/5854cae6da32cb6b7e00b55250b8db1dabb0375e-1038x491.webp)

- Click any query to load it into the query editor.

![Loading a selected query into the Redis Sandbox editor](/images/site-mirror/73180af444f5c77d8a0a2eaa3480764cebab61f2-1038x551.webp)

### Writing Your Own Query

- You can also type or paste your own Redis commands directly into the query editor.
- The editor supports multi-line queries and syntax highlighting for better readability.

### Query Panel

- Displays the currently selected or written query.
- You can edit, run, or reset the query here.

![Query panel displaying the currently active Redis command](/images/site-mirror/9966ee72a22b7aaed3ed900de7bfe2294457e1c7-1038x552.webp)

![Query panel control buttons for running and resetting queries](/images/site-mirror/13ce5ded59286c956ba63bbbec73665326b0951f-1038x490.webp)

### DBIndex Panel

- Shows index details related to the selected query.

![DBIndex panel showing index metadata for the selected query](/images/site-mirror/50ca418bd4d63e5db0a9fff391c2da86d3da92ba-1038x551.webp)

### DataSource Panel

- Displays sample data associated with the selected query and index.
- Helps you visualize the data your query will operate on.

![DataSource panel visualizing sample data for the active query](/images/site-mirror/c95d5475e42e56aadb83c94b0b683a4d6a5b78b5-1038x552.webp)

### Run Query

- Click the `Run` button to execute your query.
- The results will appear in the Results panel.

![Clicking the Run button to execute a Redis query](/images/site-mirror/35902d32c1a91212b6a2d044b7e6d6246c5458e0-1038x551.webp)

### Results Panel

- View the output of your query in a structured table or as raw text.

![Results panel displaying query output in a table format](/images/site-mirror/6014dec4dec7e7e1cd8f4e42cf65341cf621e078-1038x552.webp)

- Toggle between views using the `Switch View` icon in the Results panel header.

![Switching between table and raw text views in the Results panel](/images/site-mirror/cddd81713bea48abfe1891f7eba86544b7e204a0-1038x549.webp)

![Results panel raw text output view](/images/site-mirror/28b98c9522bdb86383f38581350ecabaad99d504-1038x551.webp)

### Share Query

- Click the Share button to generate a shareable link for your current query.
- You can also modify the query before sharing.

![Generating a shareable link for a Redis query](/images/site-mirror/cbf85badeae4f7bffb6a3c057b120ace6a44008f-1038x551.webp)

### Reset Query

- Made changes you want to undo? Click `Reset` to revert to the originally selected query.

![Resetting the query editor to the originally selected query](/images/site-mirror/84dd44027fda727755cf28a417a231977f74b1e3-1038x551.webp)

### Navigating related queries

- Quickly switch between related queries by clicking their names in the left sidebar.

![Navigating related queries in the sidebar](/images/site-mirror/568db319738d4866fe4a991ad4ccb8180847cf4b-1038x551.webp)

### Query History

- Click the history icon in the query panel header to view your past successful queries.

![Accessing the query history from the header](/images/site-mirror/06860de6091c4f0bd9f2d547ec5dbc36c9972396-1038x552.webp)

![Viewing a list of past successful Redis queries](/images/site-mirror/7fd758c40f8e3c54ee08b64438290556cd99c802-1038x483.webp)

- Reload any previous query with a single click and run it again.

![Reloading a query from history into the editor](/images/site-mirror/71c7abc483390d63649fd80efeda10214bdb2b6f-1038x488.webp)

- Delete your query history if needed.

![Deleting past queries from history](/images/site-mirror/6ea1dbfffb1b83dad887ded0465034f49336172f-1038x490.webp)

### Replay tour

- Click `Replay tour` in the sidebar to revisit the guided walkthrough.

![Selecting the Replay tour option from the sidebar](/images/site-mirror/524adf2868a672b6db03857ead911eb43cb469ff-1038x552.webp)

## Session (write) Queries

- When you execute a write query, a unique session is created for you.

Sample write query:

![Sample write query demonstrating the pg: key prefix](/images/site-mirror/38fcf7adc666aa4e071c1db490bfc644448dc09a-1038x196.webp)

- All subsequent queries in that session will operate on your session's data.
- Sessions have an expiry setting; data is deleted after the session expires.
- Note: Every key in your write query must use the `pg:` prefix.

> **Note:** The session status is shown in the header

- Before starting a session:

![Session status indicator showing no active write session](/images/site-mirror/bd028811e6f943d718bea121d8a3c0f458b6cfef-1038x58.webp)

- After starting a session:

![Session status indicator showing an active write session with TTL](/images/site-mirror/89ba13eb453f3251e48a641981d086a2171ec60c-1038x73.webp)

## Next steps

Now that you've explored Redis Sandbox, take the next step in your Redis journey:

- [Redis quick start guide](/tutorials/howtos/quick-start/) - Install Redis locally and connect your first application.
- [What is Redis?](/tutorials/what-is-redis/) - Learn about Redis architecture, data structures, and common use cases.
- [Redis documentation](https://redis.io/docs/latest/) - Dive into the official Redis documentation.
- [Redis University](https://university.redis.io/) - Take free online courses and earn certifications.
- [Redis Cloud](https://cloud.redis.io/) - Deploy a managed Redis instance in minutes.
