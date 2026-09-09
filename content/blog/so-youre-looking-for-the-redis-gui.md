---
title: "So, You’re Looking for the Redis GUI?"
linkTitle: "So, You’re Looking for the Redis GUI?"
url: "/blog/so-youre-looking-for-the-redis-gui/"
description: "Update: In April 2019, we acquired RDBTools from HashedIn and created its successor RedisInsight, a browser-based management interface for your Redis deployment."
date: 2014-09-11
blogCategories:
- "Tech"
authors:
- "Itamar Haber"
lastmod: 2026-06-01
hidden: true
---

*By Itamar Haber, Technology Evangelist · Published 11 September 2014 · updated 1 June 2026*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

![RedisInsight](/images/site-mirror/ee932eea0bdbb68bb1d8ca8fdbac4c4ed514e983-120x120.svg)

### RedisInsight

**Update:** In April 2019, we acquired RDBTools from HashedIn and created its successor [RedisInsight](/insight/), a browser-based management interface for your Redis deployment.

---

![](/images/site-mirror/57c334d5218119cde4c7c946c2ae2f76ed43e319-635x200.webp)

It all comes down to preferences. While there are Redis users who are familiar with the Redis command line interface (CLI) and rely on it to inspect, visualize and perform manual updates, there are those who prefer to using a Graphical User Interface (GUI) to achieve that. There are several Redis GUIs available, for different platforms, and in this article I’ll try to review a few of them.

**Important: **Before using any of these tools in production, keep in mind that some GUIs rely on the (“evil”) [KEYS](https://redis.io/commands/keys/) command. Should you have a large database, your Redis server might freeze and cause issues in your production applications.

## Redsmin: My Go-To-Tool for the Cloud (and Below)

![](/images/site-mirror/ad1247f6bfde4120e6e9eee7c0ddd26a0670f393-635x227.webp)

[https://redsmin.com/](https://redsmin.com/)

I’m starting off with Redsmin – my personal favorite. It mixes perfectly my on-the-go needs with a sane and objective way to work with my databases. It is a different kind of offering as it is a web based service that offers not only a GUI for inspecting your Redis data, but also monitoring and runtime server reconfiguration. Redsmin provides several plans, including a free one that can be used to evaluate a small dataset (up to 100,000 keys). Since redsmin is a hosted service, connection to your Redis server can be done directly over the internet, optionally [SSL authenticated and encrypted](/blog/secure-redis-ssl-added-to-redsmin-and-clients/), or by using a proxy service that you run on your servers that exposes your Redis instances to Redsmin in a secure way.

Redsmin has plenty of extra features, such as slowlog inspection, a list of currently connected clients that allows you to disconnect them, a multi keys editor for batch operations and great search features. With plans starting as low as 5,99€/mo, you can lift all limitations and connect to multiple Redis instances.

**Pros:** the most extensive features set, ease of use, no install

**Cons:** requires an internet connect, anything else contact Redsmin’s awesome support.

## Redis Commander: A Free Node.js Powerful Choice

![](/images/site-mirror/da8ae4a637ff33772abf626343a20dd0b55aabfb-635x505.webp)

[https://www.npmjs.org/package/redis-commander](https://www.npmjs.org/package/redis-commander)

Redis Commander is a Node.js web application that can be used to view, edit and manage your Redis databases from the comfort of your browser. It allows you to directly manipulate all of Redis’ data types. It’s freely available (although it doesn’t specify under which license) and can be easily installed via npm, provided you have a working node.js installation.

Like most Redis GUIs, Redis Commander allows you to connect to multiple database and Redis server instances simultaneously. Besides having an editor, Redis Commander also includes a terminal with auto completion (for both commands and keys), documentation and import/export functionality.

Redis Commander does require direct access to your Redis servers, but you can get around that by running it directly in your Redis servers so you can access it remotely without having to expose your Redis server over the internet.

**Pros:** it’s free, powerful, in your browser and runs wherever Node.js is.

**Cons:** requires direct connectivity, only runs where Node.js is.

## Redis Desktop Manager: Cross-Platform, Pure Desktop GUI

![](/images/site-mirror/7954183c38fac72ee39229736346f0928c56ff49-1085x678.webp)

[https://redisdesktop.com/](https://resp.app/)

Redis Desktop Manager is a cross-platform desktop Redis client, available for Windows, MacOSX and Linux desktops. It’s freely available under the MIT [LGPL](https://github.com/uglide/RedisDesktopManager/commit/7ff4f5ce7bc4465d4c20af7c0e74ea2e9d344358) license.

Like most other Redis GUIs, it allows you to connect simultaneously to multiple Redis databases or instances, inspect and modify your data and use an interactive terminal. You can also search for keys across multiple databases and view a system console which logs all Redis commands.

However. One unique feature of Redis Desktop Manager is that it allows you to establish connections via SSH tunnels, enabling secure connections to remote servers.

**Pros:** free, dead simple installation, runs on the desktop, SSH tunneling a breeze

**Cons:** if you’re comfortable using a desktop GUI, there are none. Update: there seems to be a minor issue with OpenGL under a VM that’s fixable as instructed [here](https://github.com/uglide/RedisDesktopManager/issues/3471) (hat tip: **Adam Christie**).

## Induction: You Can Guess By the Name That It’s for Mac OS X

https://inductionapp.com/

**UPDATE:** the project has been discontinued.

Induction is a Mac OS X database client. It’s not Redis specific as it also supports PostgreSQL, MySQL, SQLite and MongoDB, and therefore isn’t the the most complete Redis GUI. Nevertheless, it allows to inspect and query your Redis database. Similarly to other Redis clients, it requires a direct connection to your server.

The alpha version is free available under an open source license.

**Pros:** An holistic view on polyglot persistency

**Cons:** limited Redis-specific functionality, MacOS-specific

## redis-browser: The Runner Up

![](/images/site-mirror/f05dacca586ac70d79162a865e28f45dd502847e-635x343.webp)

[https://github.com/humante/redis-browser](https://github.com/humante/redis-browser)

This web-based explorer view of your Redis database is delivered as a Ruby gem. It is the youngest of the tools in this review and probably the simplest. Simplicity, however, is sometime a virtue, especially when you need a no-frills, dead-simple GUI. Give it a shot and encourage [@Monterail](https://twitter.com/monterail) to keep up the good work!

## Conclusion

There are several other Redis GUI alternatives that are available, both for the desktop and ones that are web-based, with similar characteristics to the ones shown here. The ones highlighted here are the most popular and actively developed, but YMMV. They were picked as examples to allow developers that are less CLI-savvy to gain insight into their Redis databases and quickly perform some updates. If you have other favorites [tell](mailto:itamar@redis.com) [me](https://twitter.com/itamarhaber) – I’m highly available 🙂
