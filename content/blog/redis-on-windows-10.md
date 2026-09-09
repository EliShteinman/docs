---
title: "Running Redis on Windows 10"
linkTitle: "Running Redis on Windows 10"
url: "/blog/redis-on-windows-10/"
description: "Update 7/28/25: You can now use Redis natively on Windows with Memurai Enterprise Edition. We've partnered with Memurai to offer a fully compatible and officially supported Windows port of Redis..."
date: 2022-03-19
blogCategories:
- "How To and Tutorials"
- "Redis Open Source"
authors:
- "Redis  "
lastmod: 2026-06-01
hidden: true
---

*By Redis   · Published 19 March 2022 · updated 1 June 2026*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

***Update 7/28/25:**** You can now use Redis natively on Windows with Memurai Enterprise Edition. We've partnered with Memurai to offer a fully compatible and officially supported Windows port of Redis that brings the full power and performance of Redis to Windows.* [*Read more here*](/blog/use-redis-natively-on-windows-with-memurai/) *for more information, tutorials, and to download an installation package.*

In this guide, we will cover several topics that will help you install Redis on Windows 10. We also address if this is indeed the best setup.

> ***Ready to experience Redis Cloud? ***[***Sign up for a free account now.***](/try-free/)

### Menu

- [Running Redis on Windows 10](#redis10)
- [How to download, install, and run Redis on a precompiled Windows binary](#installredis)
- [How to download and install Python for Windows](#python)
- [How to install the Redis client library](#client)
- [Drawbacks of Redis on Windows](#drawbacks)

## How to download, install, and run Redis on a precompiled Windows library

You can download a moderately out-of-date precompiled version of Redis for 32-bit and 64-bit Windows thanks to Dusan Majkic from [his GitHub page](https://github.com/dmajkic/redis).

After you download Redis on Windows, you’ll need to extract the executables from the zip file. As long as you’re using a version of Windows more recent than Windows XP, you should be able to extract Redis without any additional software.

![Redis running in windows](/images/blog/f0f0d9da61e674ace459ca3cfbf94ce8e7c89f16-644x449.svg)

After you’ve extracted either the 32- or 64-bit version of Redis to a location of your choice (depending on your platform and preferences; remember that 64-bit Windows can run 32- or 64-bit Redis, but 32-bit Windows can only run 32-bit Redis), you can start Redis by double-clicking on the redis-server executable. After Redis has started, you should see a window similar to figure A.1.

#### Compiling Redis on Windows yourself

If you find yourself in the position of needing the most up-to-date version of Redis on Windows as possible, you’ll need to compile Redis yourself. Your best option is to use [Microsoft’s official port](https://github.com/microsoftarchive/redis), which requires Microsoft Visual Studio, though the free Express 2010 works just fine. If you choose to go this route, be warned that Microsoft makes no guarantees as to the fitness of their ports to Windows for anything except development and testing.

**You can install **[**Redis cache**](/solutions/caching/)** on Windows 10 using Windows Subsystem for Linux(a.k.a WSL2). WSL2 is a compatibility layer for running Linux binary executables natively on Windows 10 and Windows Server 2019. WSL2 lets developers run a GNU/Linux environment(that includes command-line tools, utilities, and applications) directly on Windows.**

## Running Redis on Windows 10

Ever since [Jessica Deen](https://twitter.com/jldeen) explained how WSL works at my [SVDevOps Meetup](https://www.meetup.com/SVDevOps/events/235908130/), I’ve recommended Redis Windows 10 users run Redis on their own dev machines. Yes, you heard right. Starting with Windows 10 (v1709 – 2017-09, [Fall Creators Update](https://blogs.msdn.microsoft.com/commandline/2017/10/11/whats-new-in-wsl-in-windows-10-fall-creators-update/)), you can run at least a half-dozen flavors of Linux on the Windows Subsystem for Linux (WSL), and you can run Redis on top of them. No VM required. No Docker. No joke!

#### How do I know if I have Windows 10 with WSL?

To answer the question “[Which version of Windows is my PC is running?](https://support.microsoft.com/en-us/help/13443/windows-which-operating-system)” press your Windows logo key + R, type “***winver***,” then select OK. Starting with version 10, you’ve got a command called “***wslconfig***.” It lists distros you have and controls which one starts by typing “bash.” Try it out!

#### How to set up WSL

1. To install Redis Windows Subsystem for Linux, follow the instructions on [Microsoft Docs](https://docs.microsoft.com/en-us/windows/wsl/install-win10#install-the-windows-subsystem-for-linux). The short version is: In Windows 10, Microsoft replaces Command Prompt with PowerShell as the default shell. Open PowerShell as Administrator and run this command to enable Windows Subsystem for Linux (WSL):

Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux

1. Reboot Windows after making the change—note that you only need to do this one time.
1. Download and install one of the supported Linux distros from the [Microsoft Store](http://microsoft.com/store).
- [Ubuntu 18.04](https://www.microsoft.com/en-us/p/ubuntu-1804/9n9tngvndl3q) (installs Redis v4.09)
- [Debian GNU/Linux ](https://www.microsoft.com/en-us/p/debian-gnu-linux/9msvkqc78pk6)(installs Redis v3.2.6)

#### Install and test Redis on Windows 10

You can run Redis on Windows 10 using Windows Subsystem for Linux(a.k.a WSL2). WSL2 is a compatibility layer for running Linux binary executables natively on Windows 10 and Windows Server 2019. WSL2 lets developers run a GNU/Linux environment (that includes command-line tools, utilities, and applications) directly on Windows.

You can either follow the written steps below or watch this video where Guy Royse shows you how to install the latest version of Redis on Windows 10 using the Windows Subsystem for Linux (WSL).

[Click here to view video](https://www.youtube.com/embed/_nFwPTHOMIY)

Follow these instructions to run a Redis database on Microsoft Windows 10.

### Step 1: Turn on Windows Subsystem for Linux[​](/learn/create/windows/#step-1-turn-on-windows-subsystem-for-linux)

In Windows 10, Microsoft replaced Command Prompt with PowerShell as the default shell. Open PowerShell as Administrator and run this command to enable Windows Subsystem for Linux (WSL):

```
 Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux

```

Reboot Windows after making the change — note that you only need to do this once.

### Step 2: Launch Microsoft Windows Store[​](/learn/create/windows/#step-2-launch-microsoft-windows-store)

```
 start ms-windows-store:

```

Then search for Ubuntu, or your preferred distribution of Linux, and download the latest version.

### Step 3: Install Redis server[​](/learn/create/windows/#step-3-install-redis-server)

Installing Redis is simple and straightforward. The following example works with Ubuntu (you’ll need to wait for initialization and create a login upon first use):

```
 sudo apt-add-repository ppa:redislabs/redis sudo apt-get update sudo apt-get upgrade sudo apt-get install redis-server

```

NOTE

The sudo command may or may not be required based on the user configuration of your system.

### Step 4: Restart the Redis server[​](/learn/create/windows/#step-4-restart-the-redis-server)

Restart the Redis server as follows:

```
 sudo service redis-server restart

```

### Step 5: Verify if your Redis server is running[​](/learn/create/windows/#step-5-verify-if-your-redis-server-is-running)

Use the redis-cli command to test connectivity to the Redis database.

```
 $ redis-cli 127.0.0.1:6379> set user:1 "Jane" 127.0.0.1:6379> get user:1"Jane"

```

NOTE

By default, Redis has 0-15 indexes for databases, you can change that number databases NUMBER in redis.conf.

### Step 6: Stop the Redis Server[​](/learn/create/windows/#step-6-stop-the-redis-server)

```
 sudo service redis-server stop

```

#### Further information

- **How does Linux run within Windows 10?** Instead of calling the Linux Kernel, the system calls (syscalls) that these unmodified Linux libraries use are redirected to Windows, which handles the call instead of Linux. For more information about WSL, visit the [Windows Subsystem for Linux Documentation on MSDN](https://docs.microsoft.com/en-us/windows/wsl/about).
- **How do I access files stored in the Linux environment?** If you want to edit Windows files in Windows AND in Linux, then keep your files in /mnt/c/ so you can edit them with either OS. Don’t use Windows to “reach into the Linux file system.” As Scott Hanselman says on his [WSL blog post](https://www.hanselman.com/blog/VIDEOHowToRunLinuxAndBashOnWindows10AnniversaryUpdate.aspx), “There be dragons!” For further information about the WSL storage, visit Jack Hammon’s blog post on MSDN titled “[WSL File System Support](https://blogs.msdn.microsoft.com/wsl/2016/06/15/wsl-file-system-support/).”

Now that Redis on Windows is up and running, it’s time to download and install Python.

## How to download and install Python on Windows

If you already have Python 2.6 or 2.7 installed, you’re fine. If not, you’ll want to download the latest version of Python 2.7, because that’s the most recent version of Python that has support for the Redis library. Go to [http://www.python.org/download/](http://www.python.org/download/) and select the most recent version of the 2.7 series that’s available for Windows in either the 32- or 64-bit version (again, depending on your platform). When Python is done downloading, you can install it by double-clicking on the downloaded .msi file.

Assuming that you accepted all of the default options for installing Python 2.7, Python should be installed in C:Python27. From here, you only need to install the Python Redis library to be ready to use Redis with Python. If you’re using Python 2.6, any time the book refers to *Python27*, you can instead use *Python26*.

## How to install the Redis client library

To help you to install the Redis client library, you’ll use the easy_install utility from the setuptools package. This is because you can easily download setuptools from the command line. To get started, open a command prompt by going into the Accessories program group in the Start menu and clicking on Command Prompt.

After you have a command prompt open, follow along with the next listing; it shows how to download and install setuptools and the Redis client library.

Listing A.6 Installing the Redis client library for Python on Windows

```javascript
C:Usersjosiah>c:python27python
```

Start Python by itself in interactive mode.

```javascript
Python 2.7.3 (default, Apr 10 2012, 23:31:26) [MSC v.1500 32 bit...
Type "help", "copyright", "credits" or "license" for more information.
```

```javascript
>>> from urllib import urlopen
```

Import the urlopen factory function from the urllib module.

```javascript
>>> data = urlopen('http://peak.telecommunity.com/dist/ez_setup.py')
```

Fetch a module that will help you install other packages.

```javascript
>>> open('ez_setup.py', 'wb').write(data.read())
```

Write the downloaded module to a file on disk.

```javascript
>>> exit()
```

Quit the Python interpreter by running the builtin exit() function.

```javascript
C:Usersjosiah>c:python27python ez_setup.py
```

Run the ez_setup helper module.

```javascript
Downloading http://pypi.python.org/packages/2.7/s/setuptools/...

```

Finished processing dependencies for setuptools==0.6c11

The ez_setup helper downloads and installs setuptools, which will make it easy to download and install the Redis client library.

```javascript
C:Usersjosiah>c:python27python -m easy_install redis
Searching for redis

```

Finished processing dependencies for redis

Use setuptools’ easy_install module to download and install Redis.

```javascript
C:Usersjosiah>
```

Now that you have Python and the Redis client library installed, read on to find out if Redis on Windows is the best setup for you.

## Drawbacks of Redis on Windows

The main drawback of Redis on Windows is that Windows isn’t officially supported on Redis. Specifically, Windows doesn’t support the fork system call, which Redis uses in a variety of situations to dump its database to disk. Without the ability to fork, Redis is unable to perform some of its necessary database-saving methods without blocking clients until the dump has completed.

Recently, Microsoft has contributed engineering time helping to address background saving issues, using threads to write to disk instead of a forked child process.

As of this writing, Microsoft does have an alpha-stage branch of Redis 2.6, but it’s only available as source, and Microsoft makes no guarantees as to its worthiness in production scenarios.

At least for the short term, there’s the previously mentioned unofficial port of Redis by Dusan Majkic that offers precompiled binaries for Redis 2.4.5. However, Redis blocks when dumping the database to disk.

Get started now with a free [Redis Cloud account](/try-free/).
