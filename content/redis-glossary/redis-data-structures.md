---
title: "Redis Data Structures"
linkTitle: "Redis Data Structures"
url: "/glossary/redis-data-structures/"
description: "As shown in table 1.1, Redis allows us to store keys that map to any one of five different data structure types; STRINGs, LISTs, SETs, HASHes, and ZSETs. Each of the five different structures have..."
lastmod: 2026-09-01
mirrored: true
---

*updated 1 September 2026*

## What Redis data structures look like

As shown in table 1.1, Redis allows us to store keys that map to any one of five different data structure types; STRINGs, LISTs, SETs, HASHes, and ZSETs. Each of the five different structures have some shared commands (DEL, TYPE, RENAME, and others), as well as some commands that can only be used by one or two of the structures. We’ll dig more deeply into the available commands in chapter 3.

Among the five structures available in Redis, STRINGs, LISTs, and HASHes should be familiar to most programmers. Their implementation and semantics are similar to those same structures built in a variety of other languages. Some programming languages also have a set data structure, comparable to Redis SETs in implementation and semantics. ZSETs are somewhat unique to Redis, but are handy when we get around to using them. A comparison of the five structures available in Redis, what they contain, and a brief description of their semantics can be seen in table 1.2.

Command Listing As we discuss each data type in this section, you’ll find small tables of commands. A more complete (but partial) listing of commands for each type can be found in chapter 3. If you need a complete command listing with documentation, you can visit [https://redis.io/commands](https://redis.io/docs/latest/commands/).

Throughout this section, you’ll see how to represent all five of these structures, and you’ll get a chance to start using Redis commands in preparation for later chapters. In this book, all of the examples are provided in Python. If you’ve installed Redis as described in appendix A, you should also have installed Python and the necessary libraries to use Redis from Python as part of that process. If possible, you should have a computer with Redis, Python, and the redis-py library installed so that you can try everything out while reading Table 1.2 The five structures available in Redis.

Reminder About Installing Redis and Python Before you continue, you’ll want to install Redis and Python. Again, quick and dirty installation instructions for both Redis and Python can be found in appendix A. Even quicker and dirtier instructions for Debian-based Linux distributions are as follows: download Redis from [https://redis.io/download](https://redis.io/download), extract, run make && sudo make install, and then run sudo python -m easy_install redis hiredis (*hiredis* is an optional performance-improving C library).

If you’re familiar with procedural or object-oriented programming languages, Python should be understandable, even if you haven’t used it before. If you’re using another language with Redis, you should be able to translate everything we’re doing with Python to your language, though method names for Redis commands and the arguments they take may be spelled (or ordered) differently.

Redis with Other Languages Though not included in this book, all code listings that can be converted have translations to Ruby, JavaScript, and Java available for download from the Manning website or linked from this book’s Manning forum. This translated code also includes similar descriptive annotations so that you can follow along in your language of choice.

As a matter of style, I attempt to keep the use of more advanced features of Python to a minimum, writing functions to perform operations against Redis instead of constructing classes or otherwise. I do this to keep the syntax of Python from interfering with the focal point of this book, which is solving problems with Redis, and not “look at this cool stuff we can do with Python.” For this section, we’ll use a redis-cli console to interact with Redis. Let’s get started with the first and simplest structure available in Redis: STRINGs.
