---
title: "Digging into Redis Enterprise on Google Cloud"
linkTitle: "Digging into Redis Enterprise on Google Cloud"
url: "/blog/digging-into-redis-enterprise-on-google-cloud/"
description: "It used to be that Redis Enterprise was just one of many offerings in the Google Cloud Marketplace, but now thanks to the partnership between Redis and Google, Redis Enterprise is integrated into..."
date: 2020-03-27
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 27 March 2020 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/76d62bead0954c01c1053088a89e87726add512f-800x500.webp)

It used to be that Redis Enterprise was just one of many offerings in the Google Cloud Marketplace, but now thanks to [the partnership](/blog/redis-enterprise-google-cloud-platform-marketplace/) between Redis and Google, Redis Enterprise is integrated into the [Google Cloud Console](https://console.cloud.google.com/getting-started). This integration means you not only can enjoy unified billing, but also that you can use your Google Cloud credits to pay for Redis Enterprise.

## Enabling the service

Let’s take a look at how to enable the Redis Enterprise API in your Google Cloud project.

The starting point is the sidebar of your Cloud Console. At the bottom you will find Redis Enterprise alongside other third-party services. Click on Redis Enterprise to go to a page where you can set up your billing information.

![](/images/site-mirror/83cc8839dda8dcc92d9e7d4a142ee0ea06bbbdf9-483x395.webp)

I won’t go into the details of this step. It’s straightforward if you have a personal account, but you will have to coordinate with your IT management if you’re part of a big organization. Once you have set up billing and enabled the API, you can start creating Redis Enterprise databases.

## Connect an application

![](/images/site-mirror/ff9e98ad3fddd43aa0938233f41dbabc9b6443f5-300x300.webp)

Once you set up your Redis Enterprise API, you’re ready to see how it works. The sample application [in this GitHub repository](https://github.com/RedisLabs/redis-microservices-for-dummies) was written for the new [Redis Microservices for Dummies](/docs/redis-microservices-for-dummies/) book. It implements some of the functionality of a fully automated library using a microservices architecture. You can request books and return them, and all the code can be run on your computer. The application also depends on a Redis database, so we will create one on our new Redis Enterprise service.

## Create a new database

Click the “MANAGE ON PROVIDER” button to go to the Redis’ website, where you can create a new subscription and corresponding database.

![](/images/site-mirror/7f9965624b2cf1ae6035fb5a665d57a21b200b3f-628x217.webp)

Select a name for your subscription and specify whether you want Redis on Flash and where your nodes should be located. If you want more information about a specific topic, the (i) icons provide more details.

[Watch the video](/wp-content/uploads/2020/03/image4-2.png)

The next screen lets you decide the settings for the database, including the name, protocol, and resource consumption. This is also where you can enable [Redis modules](/redis-enterprise/modules/), if you need any. Make sure to look at the persistence options, you may need to enable them, depending on your use case.

[Watch the video](/wp-content/uploads/2020/03/image6-1.png)

Saving the changes brings you to the review page where you can double check that you configured everything as needed. After you’ve made sure that everything looks right, it’s time to give the final confirmation.

[Watch the video](/wp-content/uploads/2020/03/image11.png)

It takes a moment to set up the entire Redis Enterprise cluster, so after a few minutes the system will send you an email confirming that everything is up and running.

[Watch the video](/wp-content/uploads/2020/03/image3-1.png)

After you receive the confirmation email, it’s time to get the endpoint information to connect to your database. In the [Redis Enterprise Cloud](https://app.redis.com) interface you can see the database you just created and its connection options. For the next step you will need to know your endpoint and password to access the database.

[Watch the video](/wp-content/uploads/2020/03/image2-4.png)

## Download the library demo from GitHub

Now you need to get the code so that you can run it. Git fans won’t need any pointers, but others can go on [the GitHub page](https://github.com/RedisLabs/redis-microservices-for-dummies) and easily download the project as a Zip file using the green “Clone or download” button.

[Watch the video](/wp-content/uploads/2020/03/image5-3.png)

**Install the dependencies**

After you put the files on your local machine, it’s just a matter of installing the dependencies. The repository is a Python project, so you will need to have a Python interpreter on your machine. On a Mac you can get it with [Homebrew](https://brew.sh/), while on Windows you can use [Chocolatey](https://chocolatey.org/).

Once Python is installed on your system, to get the project-specific dependencies all you have to do is navigate into the project’s main directory and run:

$ pip install -r requirements.txt

You can now run the application!

## Run the library-demo project

To run the application, you need to launch main.py. Launching it with the -h argument shows all the options at your disposal. In this case you want to specify –address and –password.

[Watch the video](/wp-content/uploads/2020/03/image8.png)

Now it’s time to copy all the details about our new database from the Redis Enterprise Cloud control panel and use them to invoke main.py. Note that the script requires you to specify a unique name when you launch it. This is an application-specific setting not related to Redis, that allows multiple instances to run at the same time. (If you want to learn more about the library application, download [Redis Microservices for Dummies](/docs/redis-microservices-for-dummies/).) For our purposes, any name will be fine, so let’s use “worker1”.

$ python main.py --address redis://YOUR-URL.redis.com:1234

--password your-password worker1

Note how the address needs to be prefixed with redis://.

If you do this correctly, the terminal will show a “Ready to process events…” line.

It’s now time to play with it!

**Request some books**

To interface with the system, you need to open a new tab in your terminal to run get_books.py. This script lets you request and return books. It still needs the same connection options as the previous script, but after that it expects an action, a username, and a series of book names. Let’s see what the help says:

[Watch the video](/wp-content/uploads/2020/03/image7-1.png)

Below are a series of invocations that would make sense, where two users request a few books, some of which are already taken by the other. Feel free to copy and paste these commands or to come up with your own sequence.

$ python get_books.py --address redis://YOUR-URL.redis.com:1234

--password your-password request loris fight-club the-witcher lotr

OK

$ python get_books.py –address redis://YOUR-URL.redis.com:1234
–password your-password return loris fight-club
OK

$ python get_books.py --address redis://YOUR-URL.redis.com:1234

--password your-password request itamar fight-club the-witcher hitchhikers-guide

OK

If you now look in the other tab, where main.py is running, you can see the result of each action:

[Watch the video](/wp-content/uploads/2020/03/image9.png)

Note how Itamar, the second user, was not able to obtain The Witcher because it was taken by Loris.

## What’s next?

This demo shows how easy it is to provision a new Redis Enterprise cluster in Google Cloud and connect it to an application. The next step is to learn more about what you can do with Redis. You can find inspiration by checking out the [Redis website](https://redis.com), taking a course at [Redis University](/university/), or watching a talk on the Redis [YouTube channel](https://www.youtube.com/channel/UCD78lHSwYqMlyetR0_P4Vig/featured).
