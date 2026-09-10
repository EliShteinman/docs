---
title: "PHP and Redis"
linkTitle: "PHP and Redis"
url: "/tutorials/develop/php/"
description: "Redis is a high-performance, in-memory data store used for caching, session management, and real-time analytics. The PhpRedis extension gives your PHP applications direct access to Redis with..."
group: "For developers"
aliases:
- "/tutorials/develop-php/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> Install the PhpRedis extension via PECL (`pecl install redis`), create a `Redis` instance, call `connect()` with your host and port, then use methods like `set()`, `get()`, and `del()` to read and write data.

Redis is a high-performance, in-memory data store used for caching, session management, and real-time analytics. The [PhpRedis](https://github.com/phpredis/phpredis) extension gives your PHP applications direct access to Redis with minimal overhead.

## What you'll learn

- How to install the PhpRedis extension with PECL
- How to connect a PHP application to a Redis server
- How to perform basic CRUD operations (set, get, delete)
- How to add Redis caching to your PHP application

## Prerequisites

- **PHP 7.4 or later** (PHP 8.x recommended)
- **PECL** (included with most PHP installations; install `pkg-php-tools` on Debian/Ubuntu if needed)
- A running Redis server (see the [quick start guide](/tutorials/howtos/quick-start/#setup-redis))

## How do I install PhpRedis?

PhpRedis is a C-based PHP extension installed through PECL. If you don't have PECL available, install it first:

```bash
apt install pkg-php-tools
```

Then install the PhpRedis extension:

```bash
pecl install redis
```

After installation, make sure the extension is enabled in your `php.ini`:

```ini
extension=redis.so
```

Restart your web server or PHP-FPM for the change to take effect.

## How do I connect to Redis from PHP?

Create a new `Redis` instance and call `connect()` with your Redis server's hostname and port:

```php
<?php

$redis = new Redis();
$redis->connect('hostname', port);
$redis->auth('password');

if ($redis->ping()) {
    echo "PONG";
}

?>
```

Replace `hostname`, `port`, and `password` with the values for your Redis instance, then save the file as `connect.php`.

Run the script:

```bash
php connect.php
```

You should see `PONG` printed to the terminal. You can verify the connection on the server side with the `MONITOR` command:

```bash
127.0.0.1:6379> monitor
OK
1614778301.165001 [0 [::1]:57666] "PING"
```

## How do I perform CRUD operations with PhpRedis?

Once connected, use the built-in methods on the `Redis` object to store and retrieve data:

```php
<?php

$redis = new Redis();
$redis->connect('127.0.0.1', 6379);

// Create / Update
$redis->set('user:1:name', 'Alice');

// Read
$name = $redis->get('user:1:name');
echo $name; // Alice

// Delete
$redis->del('user:1:name');

?>
```

PhpRedis also supports hashes, lists, sets, sorted sets, and streams. See the [PhpRedis documentation](https://github.com/phpredis/phpredis#readme) for the full API.

## How do I add Redis caching to a PHP application?

A common pattern is to check Redis for cached data before querying a slower data source:

```php
<?php

$redis = new Redis();
$redis->connect('127.0.0.1', 6379);

$cacheKey = 'products:featured';
$cached = $redis->get($cacheKey);

if ($cached !== false) {
    $products = json_decode($cached, true);
} else {
    // Fetch from database or API
    $products = fetchFeaturedProductsFromDb();
    // Cache for 5 minutes
    $redis->setex($cacheKey, 300, json_encode($products));
}

?>
```

You can also use Redis as a PHP session handler by adding the following to `php.ini`:

```ini
session.save_handler = redis
session.save_path = "tcp://127.0.0.1:6379"
```

## What about Predis vs PhpRedis?

[Predis](https://github.com/predis/predis) is a pure-PHP Redis client that requires no compiled extension. PhpRedis is a C extension and is generally faster. Choose Predis if you cannot install C extensions in your environment; choose PhpRedis for best performance. Both support Redis Cluster and Sentinel.

## Next steps

- [PhpRedis GitHub repository](https://github.com/phpredis/phpredis) -- full API reference and examples
- [Redis Cluster support for PhpRedis](https://github.com/phpredis/phpredis/blob/develop/cluster.md)
- [Redis Sentinel support for PhpRedis](https://github.com/phpredis/phpredis/blob/develop/sentinel.md)
- [Predis GitHub repository](https://github.com/predis/predis) -- pure-PHP alternative
- [Redis distributed locks in PHP](https://github.com/ronnylt/redlock-php)
- [Getting Started with Redis & PHP](https://github.com/redis-developer/redis-php-getting-started/)
