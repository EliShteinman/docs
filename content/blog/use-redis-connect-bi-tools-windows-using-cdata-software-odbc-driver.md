---
title: "How to Use Redis to Connect to BI Tools on Windows Using CData Software ODBC Driver"
linkTitle: "How to Use Redis to Connect to BI Tools on Windows Using CData Software ODBC Driver"
url: "/blog/use-redis-connect-bi-tools-windows-using-cdata-software-odbc-driver/"
description: "Redis is well known as an in-memory database that’s designed for various use cases, including session management, caching, high speed transactions, pub/sub, data streaming, analytics, and more...."
date: 2018-11-19
blogCategories:
- "Redis Open Source"
authors:
- "Jerod Johnson"
lastmod: 2025-03-27
hidden: true
---

*By Jerod Johnson, Technology Evangelist · Published 19 November 2018 · updated 27 March 2025*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

Redis is well known as an in-memory database that’s designed for various use cases, including session management, caching, high speed transactions, pub/sub, data streaming, analytics, and more. Redis is also popular for its support of client libraries and its wide-ranging list of programming languages. You can develop apps with most popular programming languages and connect them to your Redis database with zero hassle.

Another reason Redis is versatile is its extensibility as a multi-model database. For example, you can import a RediSearch module into Redis and get an extremely fast, in-memory, search engine. Similarly, you can also use Redis as a graph database, with the help of the RedisGraph module.

All of this, of course, begs the question: Can you use Redis as a relational database? The answer is simple: An ODBC connector to Redis can power numerous applications, such as Tableau, DataBind Charts, Crystal Reports, LINQPad, Entity Framework 6, etc.; with the ODBC driver, you can obtain an SQL-like access to Redis, so you can even connect the ubiquitous Microsoft Excel to Redis data.

The good news is, Redis’ partner — CData Software — has developed an ODBC driver for Redis, making Redis even more accessible.

With the CData ODBC Driver for Redis, users [can connect to data](https://www.cdata.com/drivers/redis/) sources from various BI, analytics and reporting tools, but stored in Redis. In order to configure the driver for Windows, download the appropriate ODBC driver from the options listed [here ](https://www.cdata.com/drivers/redis/download/)and[ follow the simple steps](https://www.youtube.com/watch?v=wFLODgSHXww) listed below.

### Step 1: Read and accept the EULA

![EULA](/images/blog/c5c5c72dddd862ed22e9436ab4832a8f919f2323-499x388.webp)

Before the driver is able to help you connect to Redis and Redis Enterprise instances, you must read through and agree to the end user license agreement. After you click “I agree,” you will be able to begin the installation process.

### Step 2: Make the necessary customizations for installation

After you have accepted the EULA, you will encounter several screens prompting you to select an installation destination as well as the components you want to install.

![select destination](/images/blog/28b5aec9d8143b3cac219545e952ea2a3f58f1df-499x388.webp)

The destination folder for the installation should be pre-populated, so as long as you have enough space available, you will be able to proceed by clicking “next.”

![configure](/images/blog/63f028d08a4a35c4fa9101c63a21f0dcb7f3fc63-499x388.webp)

The subsequent screen will allow you to select which components you would like to install. Here, it is important to note that the bitness — whether 32-bit or 64-bit — of your ODBC Driver does not refer to bitness of your machine. Instead, it refers to the bitness of the applications you will use with the driver. According to Johnson, it makes sense for most users to install both versions of the driver.

On this same screen, you will also notice that there are help files included, which provide more details about the driver’s features and how they are meant to be used. There are some demo applications as well, which provide simple, straightforward examples of what using the driver can look like. Then, there is the final component — [the SQLBroker](https://www.cdata.com/kb/articles/sqlgateway-overview.rst), a lightweight application that allows you to connect to your Redis data remotely using Tabular Data Stream or MySQL protocol. After you have selected these components, click “next” to continue.

![menu](/images/blog/cd7376f673a0a823bbe4ab12c788ac4a1fb43e3e-499x388.webp)

On the following screen, you will be prompted to select the start menu folder for the driver’s shortcuts, and to enter a name for this new folder. Then, click “next” again, and you should see a screen letting you know that the driver is ready to install. Click “install” to continue, and you will observe all of the components you previously selected being installed. Once the installation is complete, you should see an option to configure an ODBC data source for the driver, which can be used to connect to Redis data from any number of other applications. Click “finish” to open the data source configuration wizard.

![Installation complete](/images/blog/13df491fea385e0b7f808ec559e776a547b1dbe5-499x388.webp)

### Step 3: Use the data source configuration wizard to explore and set connection properties

Once you open the wizard, you will see a new screen listing the connection properties used to connect to your Redis instance:

![image 8](/images/blog/7a8911720eea94a1311c87597af76d584dcbea0f-650x505.webp)

Now, you should start by entering the IP address or fully qualified domain name for the Redis server. Then, enter the port for your Redis instance. If your Redis instance is protected by a password, you can indicate that under “Auth Scheme.” If it isn’t, you can simply set the Auth Scheme to “none.”

Once you have made these basic customizations, you can go on to explore the other connection properties. For example, take a look at the Define Tables property:

![Table Configuration](/images/blog/5caff67c601964871517801cf1c27097ce75cd91-650x505.webp)

This property enables you to group keys based on a key pattern; these groups will then be treated as a table. In other words, table patterns set up key patterns that will be used to define tables by discovery. For example, suppose you specify that Table_1 will include all of the keys that begin with prefix:, and that Table_2 will include all of the keys beginning with prefix:prefix2. If you set the Table Pattern property to prefix:*, then the ODBC driver will only highlight keys that begin with prefix:. If you use the default value instead, then the driver will expose all keys that use a colon to separate hierarchies.

There are also numerous other connection properties available, which will allow you to do anything from connecting through a proxy or firewall to configuring any logging and secure connectivity.

### Step 4: Test the connection

Now that you have indicated your installation and connection preferences, you are ready to test the driver’s functionality. At the top of the screen within the data source configuration wizard, click “test connection”:

![Connection successfull](/images/blog/4fed2995a4e4de14c31dce71386a6997863859d1-650x505.webp)

If the connection test is successful — which it should be if you have correctly followed the above steps — click “OK” to save your connection settings and close the wizard.

With the DSN configured, you are now ready to connect to your Redis data from any number of third-party BI, reporting, ETL and custom applications. If you have any questions, you can reach out to CData Software’s support team at support@cdata.com. Good luck with the installation process!
