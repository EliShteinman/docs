---
title: "Running Redis on Windows 8.1 (and previous versions) – Part II of III"
linkTitle: "Running Redis on Windows 8.1 (and previous versions) – Part II of III"
url: "/blog/redis-on-windows-8-1-and-previous-versions/"
description: "Update 7/28/25: You can now use Redis natively on Windows with Memurai Enterprise Edition. We've partnered with Memurai to offer a fully compatible and officially supported Windows port of Redis..."
date: 2018-07-31
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2026-09-01
hidden: true
---

*By Redis   · Published 31 July 2018 · updated 1 September 2026*

***Update 7/28/25: ****You can now use Redis natively on Windows with Memurai Enterprise Edition. We've partnered with Memurai to offer a fully compatible and officially supported Windows port of Redis that brings the full power and performance of Redis to Windows.* [*Read more here*](/blog/use-redis-natively-on-windows-with-memurai/) *for more information, tutorials, and to download an installation package.*

### Why Windows for Redis?

It’s an open secret that more developers code on Windows than any other OS. Every year Stack Overflow shares its developer survey, and every year [Windows is the most popular OS](https://insights.stackoverflow.com/survey/2018#technology-developers-primary-operating-systems) for development, and [Visual Studio is the most popular IDE](https://insights.stackoverflow.com/survey/2017#technology-most-popular-developer-environments-by-occupation). Of course, there are many ways to slice the data, but it suffices to say A LOT of you reading this post are using Windows right now. What isn’t obvious, however, is how to install [Redis](/) on Windows so you can develop applications that use Redis. Even if you access Redis remotely (ex: [Redis Enterprise Cloud](/redis-enterprise/cloud/)), you still need a Redis client compiled for your local Windows machine.Today there is one way to develop with Redis natively on Windows 8.1 (and earlier versions of Windows), and that is with an unsupported port of Redis 3.2.1 for Windows.

In part 1 of this “Redis on Windows” series, I explain how to run Redis on Windows 10 via the Windows Subsystem for Linux (WSL). In this post, I explain how to run Redis on earlier versions. In a future post, I will explain how to run Redis in a Docker container.

### Port of Redis 3.2.1 for Windows

Officially, Redis is not supported on Windows. There is, however, a 3.2.1 version of Redis that was ported to Windows by MSOpenTech. It’s over two years old and has some drawbacks, so the link from the redis.io Downloads page has been removed. That said, newer versions of Redis are backward compatible, so if you don’t need new commands, then this 3.2.1 version of Redis might work for your development purposes.

Note: There have been many security fixes and other improvements since version 3.2.1, so I highly recommend against running older versions of Redis in production. This blog post expects that you want to run Redis on your developer machine for development purposes only. As always, you should develop your code on a non-open, trusted network that is behind a firewall.

### Download, Install and Run Redis 3.2.1 Port for Windows

1. Visit the archived MSOpenTech Redis Github repository at [https://github.com/MicrosoftArchive/redis/](https://github.com/MicrosoftArchive/redis/).
1. Scroll down to the “Redis on Windows” section and click on the [release page](https://github.com/MicrosoftArchive/redis/releases) link.
1. Find the latest version (currently 3.2.100)
1. Download and run the .msi file and walk through the Setup Wizard instructions. Accept the Wizard’s default values, but make sure to check the “Add the Redis installation folder to the Path environment variable” checkbox.
Option #2: If you are unable to run the Setup Wizard, then follow these steps to install via .zip file. (Note: You may also download the forked Redis source code and [build it to run on your version of Windows](https://github.com/MicrosoftArchive/redis#how-to-build-redis-using-visual-studio), but these steps will not be covered in this blog post):
  1. 
    1. Download the .zip file to your hard drive.
    1. Unzip the files into any location, such as ‘C:Program FilesRedis’.
    1. Follow these additional steps to complete the installation of Redis (Note that these steps are for Windows 7 Professional; other versions may require different steps):
      1. Add the path of your Redis folder as a Windows ‘environment variable.’
        1. Open your “Control Panel” application and search for “Edit the system management variables.”
        1. Open the “Environmental Variables” window.
        1. Under “User Variables,” find the variable named “Path” and click “Edit.”
        1. Add “C:Program FilesRedis” to the end of the variable value and click “OK.”
        1. If the Path variable doesn’t exist, then click “New,” add “C:Program FilesRedis” and click “OK.”
      1. Install Redis as a Windows Service.
        1. Open your Command Prompt (ex: cmd.exe).
        1. From your Redis folder (ex: C:Program FilesRedis) run the following command:
 Note: To uninstall Redis as a Windows Service type:

> redis-server --service-install

> redis-server --service-uninstall

1. To run Redis 3.2.1 port on Windows 8.1 (or previous editions):
  1. Open your Command Prompt (ex: cmd.exe) and type:


> redis-server --service-start

  1. The Redis API will create a default Redis which is ready to accept connections on port 6379. You may now connect to it with the redis-cli.exe file.

Note: To save and stop the Redis database, type: Note: To shut down the Redis server, type:

> redis-server shutdown save

> redis-server --service-stop

1. Secure your Redis
  1. Security is very important, especially while connected to the Internet. Redis 3.2 is the [first version that addresses security by default](https://www.reddit.com/r/redis/comments/3zv85m/new_security_feature_redis_protected_mode/). This version, and versions after it, have protected mode until the user specifies a password or an IP address. This means that you will only be able to access your Redis from your local machine using 127.0.0.1 or localhost. Nonetheless, it is always a good idea to specify a password and the network addresses which you want to access your Redis.
    - Password: The password is set by the system administrator in clear text inside the redis.conf file. Open the file, uncomment the #, and change “mypassword” to a very strong and very long value.

requirepass mypassword

    - Network address: It is also possible to bind Redis to your laptop by adding a line like the following to your redis.conf file:

bind 127.0.0.1

  1. You should also read the [security page](https://redis.io/topics/security) on redis.io to identify the right security configuration for your situation.

### Connect to Redis for Windows

1. Open your Command Prompt (ex: cmd.exe)
1. From your Redis folder (ex: C:Program FilesRedis) run the following command:
 You will get a response: “pong” if the server is running.

> redis-cli ping

1. If you need to connect to Redis across a network, you must type the host name (or IP address), such as:


> redis-cli -h redis15.local.net -p 6739 -a mypassword ping (or > redis-cli -h 123.456.789.012 -p 6739 -a mypassword ping)

1. You can also specify a password, such as:


> redis-cli -a mypassword ping

1. To save keyboard clicks, you can establish a continuous session with the Redis server by typing:
 Now you can just type your command, such as:

> redis-cli -a mypassword

> ping

1. For memory and security reasons, it is a good idea to shutdown Redis when not in use. To save your data and stop Redis, type:


> redis-cli -a mypassword shutdown save

### Summary

Now that you have Redis running on your developer machine, you’ll want your application to talk to Redis. Check out the [Redis clients section](https://redis.io/docs/latest/) on redis.io for a list of Redis client libraries. In particular, look at the [C# clients](https://redis.io/clients#c) ServiceStack.Redis and StackExchange.Redis.
