---
title: "Ruby and Redis"
linkTitle: "Ruby and Redis"
url: "/tutorials/develop/ruby/"
description: "Use Redis with Ruby via the redis-rb gem. This tutorial walks you through installation, connecting to a Redis server, and performing basic operations so you can integrate Redis into your Ruby..."
group: "For developers"
aliases:
- "/tutorials/develop-ruby/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
mirrored: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> Install the `redis` gem (`gem install redis`), create a connection with `Redis.new`, and call methods like `set` and `get` to store and retrieve data.

Use Redis with Ruby via the **redis-rb** gem. This tutorial walks you through installation, connecting to a Redis server, and performing basic operations so you can integrate Redis into your Ruby applications.

## What you'll learn

- How to install and configure the redis-rb gem
- How to connect a Ruby application to a Redis server
- How to run basic Redis commands from Ruby
- Where to find example apps built with Ruby on Rails and Redis

## Prerequisites

- **Ruby 2.7+** installed (check with `ruby -v`)
- **Bundler** for dependency management (`gem install bundler`)
- A running Redis server (see the [Redis quick-start tutorial](/tutorials/howtos/quick-start/) for setup options)

## How do I start a Redis server?

You can run Redis locally, in Docker, or in the cloud. The [Redis quick-start guide](/tutorials/howtos/quick-start/) covers every option in detail.

Once Redis is running, verify the connection with the CLI:

```bash
redis-cli
127.0.0.1:6379>
```

By default Redis listens on port **6379**. You can change this in your Redis configuration file. If you have authentication enabled, the CLI will prompt for a password.

## How do I install redis-rb?

You can install the redis-rb gem directly:

```bash
gem install redis
```

Or add it to a **Gemfile** for use with Bundler:

```ruby
gem 'redis'
```

Then run:

```bash
bundle install
```

Verify the installation:

```bash
bundle info redis
```

You should see output confirming the gem version and its source repository at [github.com/redis/redis-rb](https://github.com/redis/redis-rb).

## How do I connect to Redis from Ruby?

Create a connection using `Redis.new` and start issuing commands:

```ruby
require 'redis'

redis = Redis.new(host: "localhost", port: 6379, db: 11)
redis.set("mykey", "hello world")
redis.get("mykey")
```

Replace `host`, `port`, and `db` with the values for your Redis instance. You can test this by saving the snippet as `connect.rb` and running:

```bash
ruby connect.rb
```

To confirm the commands reached Redis, open a second terminal and run `MONITOR`:

```bash
127.0.0.1:6379> monitor
OK
1614684665.728109 [0 [::1]:50918] "select" "11"
1614684665.728294 [11 [::1]:50918] "set" "mykey" "hello world"
1614684665.728435 [11 [::1]:50918] "get" "mykey"
```

## Ruby on Rails example apps

### Rate-limiting app

![Screenshot of a rate-limiting demo application built with Ruby on Rails and Redis](/images/site-mirror/271cddc6b0e097ad39e8b596fefc914d639b5f5c-1228x1102.webp)

[Rate-limiting app](https://github.com/redis-developer/basic-redis-rate-limiting-demo-ruby) built in Ruby on Rails — demonstrates how to use Redis to throttle requests.

---

### Leaderboard app

![Screenshot of a leaderboard demo application built with Ruby on Rails and Redis](/images/site-mirror/6b6f855fbc408fb50b8d94fda09f2655a5b921ba-1280x1106.webp)

[Leaderboard app](https://github.com/redis-developer/basic-redis-leaderboard-demo-ruby) built in Ruby on Rails — shows how to implement sorted-set-backed rankings.

## Next steps

- Browse the [redis-rb source and documentation](https://github.com/redis/redis-rb/)
- Try [Async::Redis](https://github.com/socketry/async-redis) for an asynchronous Ruby client with TLS support
- Follow the [Redis quick-start tutorial](/tutorials/howtos/quick-start/) to explore more Redis features
- Explore tutorials for other languages: [Python](/tutorials/develop/python/fastapi/), [Node.js](/tutorials/develop/node/gettingstarted/), [Java](/tutorials/develop/java/getting-started/), [.NET](/tutorials/develop/dotnet/)
