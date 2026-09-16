---
title: "Introducing Redis Launchpad"
linkTitle: "Introducing Redis Launchpad"
url: "/blog/introducing-redis-launchpad/"
description: "The Redis community has always been at the core of what makes Redis great. Thanks to this group, Redis, for the 5th time in a row, was picked as the most-loved database in the Stack Overflow’s..."
date: 2021-09-22
blogCategories:
- "Announcements"
- "Company"
- "Tech"
authors:
- "Mike Anand"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Mike Anand, Former Chief Marketing Officer · Published 22 September 2021 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/40073852eb25d73ab1a8e16a2cca121e140e7adf-772x520.webp)

The Redis community has always been at the core of what makes Redis great. Thanks to this group, Redis, for the 5th time in a row, was picked as the most-loved database in the [Stack Overflow’s developer survey](https://insights.stackoverflow.com/survey/2021). As Redis’s popularity grows, so do the use cases across developer communities, industries verticals, and geographies.

Empowering, growing, and harnessing the power of Redis through a [single vision](https://www.youtube.com/watch?v=5qSTeiimNXE) with the love of our community is why we dreamed up [Redis Launchpad](https://launchpad.redis.com/). Today, we are excited to introduce Redis Launchpad, a hub of 75+ sample applications built by us and you on Redis. Redis Launchpad provides developers and architects an easy, tangible way to find and visualize numerous sample apps that use Redis as a real-time data platform and primary database in one central location. Here you can dive into high-quality sample apps that show different architectures, data modeling, data storage, and commands, allowing you to start building fast apps faster.

[Click here to view video](https://www.youtube.com/embed/oA7pWrbRd9w)

These apps come in various **languages** (JavaScript, Java, Python, etc.), cater to different **industry verticals** (Financial services, Gaming, Retail, etc), use different Redis modules (RedisJSON, RediSearch, etc), and showcase varying capabilities. You can even drill down and search for **individual commands** to see how they are used in different apps and different languages!

# How can you use Redis Launchpad?

Well, simply hop over to https://launchpad.redis.com and search for any app based on various criteria. Click on the app and you should see a video and detailed description of how that app was built and works. This includes things like data modeling, commands to add the data, and commands to retrieve the data.

[Watch the video](https://launchpad.redis.com/?id=project%3Abasic-analytics-dashboard-redis-bitmaps-nodejs)

What’s more, in some of the apps, you get ready to use deploy buttons. So you can quickly deploy it into Heroku, Vercel, Google Cloud, and more.

# Redis Launchpad itself is built on Redis!

As they say, we love to drink our own champagne. We’re thrilled to be able to use our own product and showcase the power of Redis beyond cache.

Let’s get into the technical aspects of how we built it and how it works.

We currently use Redis [Hashes](https://redis.io/commands#hash) to store the metadata of apps, and index it using [RediSearch](https://oss.redis.com/redisearch/index.html). Then everything else—the left pane filters, the fuzzy search, the apps gallery, and pagination—are all supported just by RediSearch!

In order to make a Github repo part of the Launchpad, you need to first make it part of the [redis-developer](https://github.com/redis-developer) Github account. And secondly, also have a “marketplace.json” metadata file. This file describes everything about the app, including the app’s name, description, the programming language used, videos, commands, and so on. The content of this file is the only thing that’s added to the Redis database for searching and filtering purposes.

And here is how the rest of it works:

1. We have an independent backend service that regularly goes through all the repositories in the Redis-Developer Github account and looks into the marketplace.json file. If it finds that file, then push the content into Redis Hashes data structure inside a production Redis database cluster running on our [Redis Enterprise Cloud](/try-free).
1. RediSearch instantly indexes the data in real-time and makes them available for searching.

![](/images/site-mirror/b83f86d572c54fe3eca75067ca090a580b3e3f76-1024x712.webp)

*Picture 1: Shows how we add and index apps metadata from different repositories into RediSearch running on Redis Enterprise.*

And once we have the data in the database, the next step is to simply query it and show the result in the browser. This is how it works:

1. We have a different backend Node.js app that queries the database using numerous search queries (Picture 2).
1. Finally, we have a frontend Next.JS (React) app that implements faceted search, pagination, fuzzy search, and displays search results in a simple grid.

![](/images/site-mirror/8a56b4a339dfaf714bf3e5794e1de0a41072af57-1024x352.webp)

*Picture 2: Shows how Launchpad web app talks to Redis and RediSearch.*

## How can you add your app to Redis Launchpad?

We’d love to see you add your app to the Launchpad. And we’d also be happy to promote it on our social media on a case-by-case basis. The first requirement is that your app should be built on Redis and use Redis as the primary database. Secondly, you should have clear and detailed instructions for us to QA and for the community to easily understand how it works.

Once you think you have those requirements met, follow these instructions to add the metadata file and let us know:

1. Modify and add the following marketplace.json file to your repository’s root.
1. Open an issue on this project asking for us to fork it.
1. Make sure the “hidden” flag is true. We’ll switch it to false after we review it and fork it.
1. Your app will be live automatically.

## The marketplace.json file details

This file contains your app’s metadata. For the latest details, please click on the “Add your app” button in Launchpad. But here are the details as of this writing:

**Example metadata.json:**

```python
{
    "app_name": "Basic Redis caching example in Nodejs",  //Name of the app
    "description": "Showcases how to implement caching in NodeJS", // One line description
    "hidden": false, // Can be "true" or "false". If true, this app won't show up in the Launchpad.
    "rank": 20, // This is used to sort the apps in the Launchpad. 1 to 20 are reserved. Enter greater than 20
    "type": "Building Block", //Can be "Building Block" or "Full App"
    "contributed_by": "Redis", // Can be "Redis" or "Community" or "Partner"
    "repo_url": "https://github.com/redis-developer/basic-caching-demo-nodejs", //This is the Github Repo's URL.
    "download_url": "https://github.com/redis-developer/basic-caching-demo-nodejs/archive/main.zip",
    "hosted_url": "", //The URL of the app. if you are hosting this app somewhere
    "quick_deploy": "true", //"true" if the project has Heroku, Vercel, Google deploy buttons
    "deploy_buttons": [
        {
            "heroku": "https://heroku.com/deploy?template=https://github.com/redis-developer/basic-caching-demo-nodejs" //Deploy button URL for deploying on Heroku
        },
        {
            "vercel": "https://vercel.com/new/git/external?repository-url=https%3A%2F%2Fgithub.com%2Fredis-developer%2Fbasic-caching-demo-nodejs&env=REDIS_ENDPOINT_URI,REDIS_PASSWORD&envDescription=REDIS_ENDPOINT_URI%20is%20required%20at%20least%20to%20connect%20to%20Redis%20clouding%20server" //Deploy button URL for deploying on Vercel
        },
        {
            "Google": "https://deploy.cloud.run/?git_repo=https://github.com/redis-developer/basic-caching-demo-nodejs.git" //Deploy button URL for deploying on Google cloud.
        }
    ],
    "language": ["JavaScript"], // Backend technologies: "JavaScript", "Java", "Python", "Go", "C#", "Ruby", "PHP", etc. 
    "redis_commands": ["SETEX"], // Enter all the Redis commands
    "redis_features": ["caching"],// Enter any core Redis feature or leave it blank.
    "redis_modules": [], //Value can be one or more of "RediJSON", "RediSearch", "RedisTimeseries", "RedisAI"  "RedisGears" or "RedisGraph" listed in an array. 
    "app_image_urls": [
        "https://github.com/redis-developer/basic-caching-demo-nodejs/blob/main/docs/screenshot001.png?raw=true"
    ], // Provide any image urls in an array.
    "youtube_url": "", //Provide a Youtube link to your app's video
    "special_tags": [], // "Hackathon", "Paid", or any event names.
    "verticals": ["Healthcare", "Financial"], // Can be: "Healthcare", "Financial", "Tourism", "Retail", "Oil & Gas", "Manufacturing", "Technology","Education", "Construction"  
    "markdown": "https://raw.githubusercontent.com/redislabs-training/redis-sitesearch/master/README.md" // Link to the RAW Markdown.
}

```

We’re super excited to launch this. Redis is very versatile and Redis Launchpad will now show exactly how you can harness the power of Redis to use it as a real-time data platform and a primary database.

Check it out and let us know what you think by tagging @redisinc on social media. 🚀
