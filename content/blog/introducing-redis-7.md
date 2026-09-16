---
title: "Redis 7.0: An Evolution Across Multiple Fronts"
linkTitle: "Redis 7.0: An Evolution Across Multiple Fronts"
url: "/blog/introducing-redis-7/"
description: "The release of Redis 7.0 is on track, and we’ve just published its second release candidate. This release candidate is a planned milestone intended to complete the version’s features, but it’s also..."
date: 2022-03-02
blogCategories:
- "Announcements"
- "Company"
authors:
- "Redis  "
lastmod: 2026-09-01
hidden: true
mirrored: true
---

*By Redis   · Published 2 March 2022 · updated 1 September 2026*

![Blog tile image](/images/site-mirror/dd803210e9ea43497bf6c58b9d070cd550956aed-772x550.webp)

The release of Redis 7.0 is on track, and we’ve just published its second release candidate. This release candidate is a planned milestone intended to complete the version’s features, but it’s also an opportunity for us to present additional content in the new version. For example, [Redis Functions](https://redis.io/docs/latest/develop/interact/programmability/functions-intro/) has evolved from the existing support for scriptings that Redis had since version 2.6. Similarly, more of Redis’ features have evolved.

In nature, evolution happens apparently at random and natural selection takes care of sorting out its results. Generally, in software in general, and specifically with Redis, this process occurs backward: we select the desired path and evolve the project to follow it accordingly. Rather than letting randomness dictate the future, our roadmap’s planning and execution are primarily guided by the users’ feedback and new use cases where Redis is a good fit.

In Redis 7.0, the Access Control List (ACL) had also stepped up the evolutionary ladder. Introduced in Redis 6.0, ACL had reversed the long-time view about security as being out of the project’s scope by adding the mechanisms to manage users and their permissions. However, our community quickly educated us that while it was a step taken in the right direction, the feature still lacked the necessary capabilities.

One of the gaps in ACL was already addressed by Redis 6.2, namely controlling the allowed patterns of Pub/Sub channel names. But that was only a partial stop-gap and it took us longer to come up with a simple and effective approach to address the remaining ones.

ACL’s original design had only provisioned for basic permission-control use cases. It enabled granting or denying access only to a single set of commands, keys’, and channels’ names patterns per user. It was impossible, for example, to restrict the [`SET` command](https://redis.io/docs/latest/commands/set/) to one subset of keys, and at the same time allow `[GET](https://redis.io/docs/latest/commands/get/)` to another subset of keys for a given user. Effectively, ACL wasn’t an effective mechanism for implementing security policies.

Redis 7.0’s Access Control List, or ACLv2 for short, is compatible with the original but adds two important improvements. Firstly, ACLv2 is all about selectors. Secondly, ACLv2 allows setting [access type permissions](https://redis.io/topics/acl#key-permissions) to specific keys. This capability makes it possible to exclusively limit the user to read-only, write-only, or read-write operations to a subset of the keys.

The original ACL design provided only one selector per user – the default selector. The selector describes the keys and channels that the user can access, categories and commands. ACLv2 allows adding any number of selectors on top of the default that are applied in order. This approach satisfies the requirements of more demanding security policies and brings ACL nearer to completeness.

The server’s introspective abilities are another aspect of Redis that have significantly advanced in version 7.0. Redis exposes an API, its commands’ dictionary, through which it interacts. As the project evolved, the number of different commands (and their sub-commands) grew, reaching an excess of 380 in version 7.0. Because every Redis command is specialized for given tasks, documenting each command’s invocation arguments and behavior is a core principle of the project. This documentation is the only contract between the server and its clients.

Historically, commands were documented externally to the project itself in a separate code repository. We kept all documentation in a (mostly) human-readable format because it was intended to be read by people. This presented a challenge for the machines (or rather, the people who program machines) because translating prose to code is messy and brittle. Specifically, authors of clients for Redis could only hope to keep their project up-to-date by monitoring changes to the documentation and reading the release notes.

So, by version 2.8, we realized that we also needed a programmatic way that allows the server to report its commands. The aptly-named (but also tongue-twister) `[COMMAND](https://redis.io/commands/command)` command lists in runtime the commands that the server supports. Furthermore, the `[COMMAND GETKEYS](https://redis.io/commands/command-getkeys)` subcommand lets clients send a verbatim command and its arguments to have the server extract any names of keys from it. Extracting key names from a command is required so the client can direct the operation correctly in a clustered deployment.

Partly driven by ACLv2-related efforts but also to make the runtime commands list more useful for clients, version 7.0 overhauls much of the internal mechanisms of the server’s command management. In addition, we’ve enriched the metadata that the server keeps about each command, making it possible to build sophisticated clients that have (almost) no a prior knowledge about the server’s capabilities. Lastly, the revamped commands table is built in such a way that Redis modules can extend it with their respective commands, to provide the same level of introspection as core commands.

The new [command key specifications](https://redis.io/docs/latest/develop/reference/key-specs/) allow clients to locally extract keys from verbatim commands without involving the cluster’s servers, thus improving latency and reducing network bandwidth. The metadata about [command arguments](https://redis.io/docs/latest/develop/reference/command-arguments/) lets clients discover and adapt to changes in commands’ syntax between server versions. Clients can obtain even more information about executing commands under special circumstances and different deployment types from the [command tips](https://redis.io/docs/latest/develop/reference/command-tips/).

This effort also included the promotion of subcommands to first-class citizens of the server’s commands table. Originally, subcommands were introduced to Redis to combat the ever-growing cardinality of the API. The reasoning was that instead of adding a new command for every task, related tasks are invoked by calling just one “parent” command. The “parent” command accepts as its first argument the name of the subcommand, which in turn dictates the action performed. From a technical standpoint, subcommands inherited all of their parent command’s traits (e.g., ACL category, read/write flags, key specification, and so forth), making it impossible to obtain a fine-grained distinction between their different behaviors.

For example, the `[CLIENT](https://redis.io/commands/client)` command is a catch-all basket for connection management tasks that boasts no less than 15 different subcommands. Some of its subcommands, like `[CLIENT SETNAME](https://redis.io/commands/client-id)`, are routinely called by normal client connections, whereas others such as `[CLIENT KILL](https://redis.io/commands/client-kill)` have the potential for misuse and should therefore be restricted to admin use alone. Earlier versions of Redis lacked the internal mechanisms that support making such distinctions, thereby directing developers to the documentation and creating confusion. In Redis 7.0, however, every subcommand has its own set of traits, regardless of its parents or siblings, allowing for its accurate description.

This post had turned out to be quite the wall of text that goes perhaps into too much technical detail towards its end (if there’s even such a thing as too much technical detail). We hope it wasn’t all boring though, and that we’ve shed some light on the new version and its fit in the project. We’re working on the final release candidate(s) towards the version’s general availability, but stay tuned for our next posts in the series that will continue the new version’s tour.
