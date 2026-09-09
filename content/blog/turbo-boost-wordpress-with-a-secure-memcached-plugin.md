---
title: "Turbo Boost WordPress with a Secure Memcached Plugin"
linkTitle: "Turbo Boost WordPress with a Secure Memcached Plugin"
url: "/blog/turbo-boost-wordpress-with-a-secure-memcached-plugin/"
description: "Recently we released the Memcached Cloud Plugin for WordPress, implementing the WordPress Object Cache. The plugin is based on the PECL Memcached extension (note the ending ‘d’), working against..."
date: 2014-07-23
blogCategories:
- "Tech"
authors:
- "Matan Kehat"
lastmod: 2025-03-27
hidden: true
---

*By Matan Kehat · Published 23 July 2014 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

![](/images/site-mirror/b42bfda714ca695bb984febb91367a00bc3be0fc-635x200.webp)

Recently we released the [Memcached Cloud Plugin for WordPress](https://wordpress.org/plugins/memcached-cloud/), implementing the WordPress Object Cache. The plugin is based on the [PECL Memcached extension](https://pecl.php.net/package/memcached) (note the ending ‘d’), working against the [libmemcached](https://libmemcached.org/) library, ensuring a better and efficient performance as well as advanced features on top of the core memcached functions, such as multi set and get methods, ‘by key’ functions and many more- all are [documented on php.net](https://il1.php.net/memcached). We basically extended the [wordpress-memcached-backend](https://github.com/tollmanz/wordpress-memcached-backend), so credits and many thanks goes to [Zack Tollman](https://github.com/tollmanz).

As the PECL Memcached extension supports secured connection to Memcached servers using [SASL](https://code.google.com/p/memcached/wiki/SASLHowto) authentication mechanism since [version 2.2.0](https://pecl.php.net/package/memcached/2.2.0), working against a [libmemcached](https://libmemcached.org/) built with SASL enabled, we wanted to provide a simple solution for WordPress users which their site is deployed in untrusted networks, and are requiring secured connection to their Memcached servers, or would like to exercise a bit more control over the clients connecting. Our [Memcached Cloud](/memcached-cloud) service is of course allowing its users to configure their buckets with SASL effortlessly, providing a perfect and secured backend for the [Memcached Cloud Plugin](https://wordpress.org/plugins/memcached-cloud/).

If you went over the [installation](https://wordpress.org/plugins/memcached-cloud/installation/) section of the plugin, as we encourage you to do, you probably noticed that installing the plugin involves building libmemcached with SASL enabled and then [installing](https://il1.php.net/manual/en/memcached.installation.php) the PECL Memcached extension, ver. 2.2.0, against the previously installed libmemcached library.

This process can be a bit non-trivial for the average user, and one solution can be taking advantage of the [Heroku](https://www.heroku.com/) platform. [Heroku’s PHP environment supports third-party extensions](https://devcenter.heroku.com/articles/php-support), that can be enabled through the composer.json file. Memcached; built against a version of libmemcached with [SASL](https://en.wikipedia.org/wiki/Simple_Authentication_and_Security_Layer) support, is supported as third-party extension. The Memcached Cloud Plugin natively supports Heroku’s [Memcached Cloud](https://addons.heroku.com/memcachedcloud) configuration.

Below we’ll demonstrate an easy and straightforward method of deploying a WordPress application to Heroku with [Memcached Cloud Plugin for WordPress](https://wordpress.org/plugins/memcached-cloud/) and [Memcached Cloud add-on for Heroku](https://addons.heroku.com/memcachedcloud), as a backend:

### Step 1 – Download

Start by downloading WordPress:

```python
curl -sS http://wordpress.org/latest.zip > wordpress.zip
unzip wordpress.zip
rm wordpress.zip
mv wordpress/wp-config-sample.php wordpress/wp-config.php

```

Next, download the Memcached Cloud WordPress plugin:

```python
curl -sS http://downloads.wordpress.org/plugin/memcached-cloud.zip > memcached-cloud.zip
unzip memcached-cloud.zip 
rm memcached-cloud.zip
mv memcached-cloud/object-cache.php wordpress/wp-content/object-cache.php

```

### Step 2 – Configure

Create the file wordpress/Procfile with the following contents:

```python
web: vendor/bin/heroku-php-nginx

```

Next, create the file wordpress/composer.json with the following contents:

```python
{
    "require": {
        "ext-memcached": "*"        
    }
}

```

Lastly, edit your wordpress/wp-config.php file and set your database’s parameters.

### Step 3 – Deploy

Initialize your git repository:

```python
cd wordpress
git init
git add .
git commit -m "initial commit”

```

Next, create the Heroku app and add the Memcached Cloud add-on to it:

```python
heroku create
heroku addons:add memcachedcloud

```

**Note:** this would also be a good time to add the database add-on to your app.

Finally, deploy the app:

```python
git push heroku master

```

That’s all there is to it! Your WordPress is now deployed to Heroku and will use a secure connection to Memcached Cloud for that extra performance boost. I’d love to get your feedback on the plugin so please give your rating to it at the [WordPress plugin page](https://wordpress.org/plugins/memcached-cloud/) and discuss it at the plugin’s [support forum](https://wordpress.org/support/plugin/memcached-cloud). Happy blogging!
