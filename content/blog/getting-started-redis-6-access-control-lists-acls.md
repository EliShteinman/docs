---
title: "Getting Started with Redis 6 Access Control Lists (ACLs)"
linkTitle: "Getting Started with Redis 6 Access Control Lists (ACLs)"
url: "/blog/getting-started-redis-6-access-control-lists-acls/"
description: "With the arrival of Redis 6 come a few new features for better security and compliance. The easiest one to explain is probably support for SSL, which enables secure communication between your..."
aliases:
- "/blog/getting-started-with-redis-6-access-control-lists-acls/"
date: 2020-01-31
blogCategories:
- "How To and Tutorials"
authors:
- "Redis  "
lastmod: 2025-03-04
hidden: true
---

*By Redis   · Published 31 January 2020 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/74720be5b55facbeefc63e8e2fbc88680011d8a9-1600x1032.webp)

With the arrival of[ Redis 6](http://antirez.com/news/131) come a few new features for better security and compliance. The easiest one to explain is probably support for SSL, which enables secure communication between your application servers and Redis. But the most notable new feature is Access Control Lists (ACLs).

With ACLs you can create multiple users and specify login passwords, and the keys and commands they are allowed to use for each. This makes it trivial to implement security and safety features such as:

- Preventing libraries from calling KEYS on a production server
- Preventing administrators from calling FLUSHALL by mistake
- Designating a key prefix for sensitive information that only some users can access

The list could go on and on, but these three examples should be enough to get your gears spinning.

## Technical details

Before we jump into how to use ACLs, let’s quickly dive into the technical implications behind ACLs.

The first notable point is that ACLs are a self-contained mechanism that you can opt-in to when the server is started. **This means that there won’t be a performance hit if you don’t enable ACLs**, which can be of the utmost importance for those who use Redis as a heavy-duty caching engine.

The second point is that ACLs are also very lightweight when enabled. Enabling restrictions on commands doesn’t require any pattern matching as Redis keeps a bitmap of enabled commands for each user, making the check extremely fast. While enabling restrictions on key names does require pattern matching, the computational cost will still be minimal for the common use case of using key prefixes for namespacing.

The last point is about the code itself. Most of the code related to ACLs is in [acl.c](https://github.com/antirez/redis/blob/unstable/src/acl.c), a file with fewer than 1,800 lines of C code (as of publication), making the feature easy to inspect for those who want a deep understanding of the tools they use.

## Upgrading from older versions of Redis

Before v6, Redis did not include the notion of users, and the only authentication strategy was a single login password. To make the transition smoother for existing codebases that rely on the previous behavior, Redis 6 includes a default user named ‘default’.

This means that by setting up a password for the ‘default’ user, along with any command or key restriction you might find appropriate, you will be able to immediately transition to Redis 6 from previous versions without having to change a single line of code in your applications.

To put this in practical terms, before Redis 6 the AUTH command took only one argument: the server password. Now, in Redis 6, AUTH can take either a single argument, for retrocompatibility, or two (username and password). When called with a single argument it will assume you’re providing a password for the ‘default’ user.

## Working with ACLs

Let’s start by creating a basic user with all permissions:

127.0.0.1:6379> acl setuser antirez on >hunter2 allcommands allkeys

This command creates a new user called ‘antirez’, enables the user for login by providing the ‘on’ option, sets the user’s password to ‘hunter2’, and enables all permissions.

Using the same syntax, it is also possible to apply changes to the user in a free-form way by simply concatenating the changes you want to apply to it:

127.0.0.1:6379> acl setuser antirez nocommands +get +set

In this invocation we first reset the list of enabled commands (so we went from all commands to no commands allowed at all), and then we enabled GET and SET. Note that all the other properties (the user being enabled, restrictions on key patterns) are left untouched.

Now let’s add some restrictions on keys:

127.0.0.1:6379> acl setuser antirez resetkeys ~secret ~redis:*

After this command, the user will only be allowed to call SET and GET on the ‘secret’ key and all other keys that are prefixed with ‘redis:’.

## Password management and rotation

Another important characteristic of ACLs is the ability to set up robust password management schemes for your users.

In the previous example, we set the password ‘hunter2’ for the user ‘antirez’. Let’s see what happens if we discover that the password was compromised, maybe because [it got disclosed on IRC, for example](http://bash.org/?244321).

A reasonable first step would be to immediately disable the user:

127.0.0.1:6379> acl setuser antirez off

Note how this command doesn’t clobber the existing set of permissions, it just disables the ability of the user to log in. After this is done, the next step is to remove the existing password and add a new one:

127.0.0.1:6379> acl setuser antirez on resetpass >hunter3

With this command we re-enabled the user, removed any previously set password, and added ‘hunter3’, all in one atomic command.

Let’s say that some time has passed and it’s now time to rotate out ‘hunter3’ in favor of a newer password. Since this time the password has not been compromised, we want to transition away from it without causing a service disruption. To allow a seamless transition, we need to add the new password while leaving the old one enabled as the change rolls out to our services:

127.0.0.1:6379> acl setuser antirez >newpass

After running this command, the user ‘antirez’ will be able to authenticate with both ‘hunter3’ and ‘newpass’. After the transition is completed (i.e., all services have been restarted and are now using the new password), it’s time to remove the old password:

127.0.0.1:6379> acl setuser antirez <hunter3

And with this, you’re done. ACLs also offer the ability of managing passwords by hash value, instead of having to remember the plaintext value, and also provide facilities for generating secure passwords automatically. Use the ‘acl help’ command for more details.

## Next steps

To try out ACLs all you need is [Redis 6](https://redis.io/download).

While this is just a simple introduction to ACLs, there are certainly more usage scenarios than what’s presented here. As with many other Redis features, they take only a moment to learn, but require more time to master. Try your hand at working through how ACLs can integrate with your existing user management schemes, and let us know [on Twitter](https://twitter.com/redis) if you have any feedback.
