---
title: "How to create a simple application with Redis Cloud and Node.js"
linkTitle: "How to create a simple application with Redis Cloud and Node.js"
url: "/blog/create-simple-application-redis-cloud-node-js/"
description: "Sometimes, I “think” in Redis. It’s a bit hard to describe, but I tend to think of real-life problems in terms of how I would solve them in Redis (I… think it might be a sickness). I’ve been..."
date: 2019-01-24
blogCategories:
- "How To and Tutorials"
authors:
- "Redis  "
lastmod: 2026-09-01
hidden: true
---

*By Redis   · Published 24 January 2019 · updated 1 September 2026*

![Blog tile image](/images/blog/634a27197c9849c8f737cf292c30c1d0e2b7d7e8-1600x840.webp)

Sometimes, I “think” in Redis. It’s a bit hard to describe, but I tend to think of real-life problems in terms of how I would solve them in Redis (I… think it might be a sickness). I’ve been renovating my house for a couple of years now and one of the most unexpected challenges is dealing with how long it takes to plaster, paint, apply adhesive and the like to dry and cure. Some things take weeks to cure before you can move on to the next step. I had a minor annoyance/disaster this weekend and I told myself that I’m not going to let it happen again. So… off to Redis to do an application speedrun.

In this post I’m going to build a small application that uses Node.js and [Redis Enterprise Cloud](/redis-enterprise/) to keep track of when things are “dry” or cured. You can record when you applied “paint” (we just use this as a generalized “material” but it could be anything) and it won’t let you paint again if it’s not dry. Finally, you can also check on the status of a coat of paint by finding out how long it’s got left. I know, it’s elegant, yet way over engineered – I’ll have VC funding in no time!

First things first, get a small Redis instance. Redis Enterprise Cloud is great for this as they give you a free 30 mb instance for as long as you use it. [I suggest reading the Redis Enterprise Cloud quick setup](https://docs.redis.com/latest/rc/quick-setup-redis-cloud/) – it will walk you through the process in detail. I estimate that each coat of paint and all the keys associated with it in Redis will take up about 300 bytes. So, the free instance can easily handle about 100,000 rooms – big enough for my house.

After signing up you should have a port, a host and a password. You can use these to create a small JSON file. We’ll use this to instruct the Node.js script of your credentials and hostname. Keep in mind that all of this is private, so don’t put in your project folder (too easy to accidentally upload it to github or something). Here is an example of how the JSON file should be structured:

```python
{
  "port": 1234,

  "password": "yourrealysecurepassword",

  "host": "host.name.of.your.redis.cloud.instance"
}

```

Now, let’s create a new directory, initialize npm, and load some dependencies.

```python
$ mkdir dryyet
$ cd ./dryyet
$ npm init
/*(Answer the `npm init` questions to your liking)*/
$  npm install redis yargs parse-duration

```

Let’s go over the three dependencies:

- 
- 
- 

Before we dive in, let’s look at the theory of what we’re going to do. To achieve the functionality, described above we need just a handful of commands. We have two application operations – paint to apply a layer of paint and readytopaint to check if you’re ok to paint. Both of these operations require two commands together in a way that is dependent on the sequence, we’ll use a [MULTI](https://redis.io/commands/multi)/[EXEC](https://redis.io/commands/exec) block.

Let’s look at the paint operation first. We can achieve this operation with the Redis commands of [SADD](https://redis.io/commands/sadd) (set add) and [SET](https://redis.io/docs/latest/commands/set/). SADD will track if a room exists over the long term (more on that later) and enable multiple users. I did warn you that this was over-engineered. The key for the set data type key is structured like rooms:userid, in this case, the userid can be anything. The member is the name of the room you’re painting. The second operation is a SET command, but with some unusual arguments. The key is structured to include both the userid and the room and looks like paint:userid:room. The first argument is the value – here we actually don’t care about the value (we just set it to “p” as a placeholder) – all the data is held in the key itself. The next two arguments are EX and time it takes the paint to dry in seconds. Finally, we have the argument NX. These last three values are what make it work – starting from the end the NX argument means “Only do this command if it’s a completely new key.” The EX and time to dry are actually TTL values, meaning that the key will last until the paint is dry and then the key will evaporate, just like the paint solvent.

The SADD operation will return a 1 if the item was added to the set or 0 if the item already exists in the set. The SET … EX … NX will return either “OK” if it set the key or null/(nil) if the operation couldn’t happen because the key already exists. What’s nice about this is that you have two operations that can boil down into two boolean values. Let’s map out the logic here:

|  | Return | Return | Return | Return |
|---|---|---|---|---|
| SADD | 0 (false) | 0 (false) | 1 (true) | 1 (true) |
| SET … EX … NX | OK (true) | null/nil (false) | OK (true) | null/nil (false) |
| Result | Allow to repaint | Don’t allow repaint | Allow to repaint (this is the first coat) | Not a possible state |

The other operation is to check if the room is ready to be painted. We can achieve this with [SISMEMBER](https://redis.io/commands/sismember) and [TTL](https://redis.io/commands/ttl) again in the MULTI/EXEC block. We use the key patterns as mentioned above and the arguments are straight forward:

- 
- 

SISMEMBER will return either a 0 for not a member of the set and 1 will be returned if it is a member of the set. TTL, on the other hand is a little more complicated as far as return values. If there is a time to live, it will be 0 or above. If the key doesn’t have a TTL but the key exists, it will be -1 and if the key doesn’t exist -2. In this case, we really shouldn’t have a -1, so we can just see if it’s 0 or higher. So, we can still have two boolean values:

|  | Return | Return | Return | Return |
|---|---|---|---|---|
| SISMEMBER | 0 (false) | 0 (false) | 1 (true) | 1 (true) |
| TTL | >=0 (true) | <0 (false) | >=0 (true) | <0 (false) |
| Result | Not a possible state | The room doesn’t exist | Still needs to dry | The room can be repainted |

To facilitate all this, we’ll use yargs and define each operation as a command off the yargs module. Each command takes a object where we will define the command syntax and the desc (which defines help text) and finally, the actual execution of the command occurs in the handler function. After the Redis command executes and closes the redis connection so the process can terminate.

```python
const
  redis = require('redis'),
  parseDuration = require('parse-duration');
let
  client;


function createConnection(argv) {
  client = redis.createClient(require(argv.connection));
}

require('yargs')
  .option('connection', {
    describe: 'JSON File with Redis connection options',
    demandOption: true,
  })
  .command({
    command: 'paint <userid> <room> <duration>',
    desc: 'Add a coat of paint',
    handler: (argv) => {
      createConnection(argv);
      let duration = parseDuration(argv.duration);
      let durationSeconds = duration > 999 ? Math.round(duration / 1000) : 1;
      client.multi()
        .sadd(
          `rooms:${argv.userid}`,
          argv.room
        )
        .set(
          `paint:${argv.userid}:${argv.room}`,
          'p',
          'EX',
          durationSeconds,
          'NX'
        )
        .exec((err, responses) => {
          if (err) { throw err; }
          let newRoom = Boolean(responses[0]);
          let ttlSet = responses[1] === 'OK' ? true : false;
          console.log(`Hi ${argv.userid}.`);
          if (newRoom) {
            if (ttlSet) {
              console.log(`The first coat for room ${argv.room} will be dry in ${durationSeconds} second(s).`);
            } else {
              console.log('This is impossible.');
            }
          } else {
            if (ttlSet) {
              console.log(`You can repaint ${argv.room} and it will be dry in ${durationSeconds} second(s).`);
            } else {
              console.log(`The room ${argv.room} was recently painted and you shouldn't repaint.`);
            }
          }
          client.quit();
        });
    }
  })
  .command({
    command: 'readytopaint <userid> <room>',
    desc: 'Check if you are ready to paint again',
    handler: (argv) => {
      createConnection(argv);
      client.multi()
        .sismember(`rooms:${argv.userid}`, argv.room)
        .ttl(`paint:${argv.userid}:${argv.room}`)
        .exec((err, responses) => {
          if (err) { throw err; }
          console.log(`Hi ${argv.userid}.`);
          let roomExists = Boolean(responses[0]);
          let ttlResponse = responses[1];
          let timeLeftToLive = ttlResponse >= 0;
          if (timeLeftToLive) {
            if (roomExists) {
              console.log(`The room ${argv.room} still needs to dry. It will be ready to re-coat in ${ttlResponse} second(s)`);
            } else {
              console.log('This is invalid.');
            }
          } else {
            if (roomExists) {
              console.log(`The room ${argv.room} can be repainted.`);
            } else {
              console.log(`${argv.room} doesn't exist.`);
            }
          }
          client.quit();
        });
    }
  })
  .demandCommand()
  .help()
  .argv;

```

Finally, you have demandCommand() that triggers the requirement the command and errors out if it’s not there and the help() that takes care of rendering help text if needed. Finally, you end with .argv which will sit this all in motion.

To run the application you can paint a room with:

| $ node index.js paint kyle bedroom 60minutes --connection ~/path-to-your-file.json |
|---|

If you want to check if a room is paintable, then run the command:

| $ node index.js readytopaint kyle bedroom --connection ~/path-to-your-file.json |
|---|

There you have it! In less than 100 lines we have a useful little utility that uses Node.js and Redis Enterprise Cloud. Now, you might think the usefulness as a command line utility is limited, but the same base here could be easily ported with little effort over to a web framework like [Express](https://github.com/expressjs/express) and you too can start your service that watches paint dry.
