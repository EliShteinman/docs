---
title: "Pop the Red Box’s Lid: Redis Lua Debugger"
linkTitle: "Pop the Red Box’s Lid: Redis Lua Debugger"
url: "/blog/pop-the-red-boxs-lid-redis-lua-debugger/"
description: "Imagine a red box. You put something in the box and wait for something else to come out (or not). Whatever comes out (or not) of the box depends entirely on what you told the box you wanted it to..."
date: 2014-12-31
blogCategories:
- "Tech"
authors:
- "Itamar Haber"
lastmod: 2025-03-27
hidden: true
---

*By Itamar Haber, Technology Evangelist · Published 31 December 2014 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/e4a9513232aff1833607baff3d87c6b5fcb32924-635x200.webp)

![](/images/site-mirror/41f747c83134c98f3c3e551ad1e8ec298b940cbb-635x200.webp)

### Update: redis-lua-debugger is not compatible with Redis v3 and above

Imagine a red box. You put something in the box and wait for something else to come out (or not). Whatever comes out (or not) of the box depends entirely on what you told the box you wanted it to do. The box originated from [Terrah](http://antirez.com/news/57)‘s moon so it only understands moon-language, a language that’s both foreign and at the same time similar to what you’re already used to. For it to do your bidding, you need to explain everything you want it to do in meticulous details, or else the box doesn’t work at all. When the box does work, what you get back isn’t always what you thought you’d get. The red box has a wry sense of humor and appears to thrive on your growing frustration as you try peeping inside its workings to understand what went wrong.

This is how I sometimes felt when trying to write even the most trivial Redis Lua scripts. It’s not that the box is broken, not at all. The problem’s entirely my programmering skillz and the unique tendency I have of sprinkling bugs all over the place. I recently wrote about the [5 Methods For Tracing and Debugging Redis Lua Scripts](/blog/5-methods-for-tracing-and-debugging-redis-lua-scripts), but all of these methods (excluding the last one) require tediously adding and removing debug printouts in your code. So I found a better way to do it and the result is our Redis Lua Debugger (or just “rld”), which boasts the following features:

- A fully non-interactive debugger
- Easy & native installation, only ~6KB payload
- Output printing to local and remote consoles
- Code line execution tracing
- State-of-the-art automatic watch mechanism, which reports new variables and value changes
- Reports function calls, returns and arguments – and does on-the-fly profiling

The first thing to know about the Redis Lua Debugger is that it is written in Lua and it runs in Redis. That means you don’t need anything besides the script and Redis to use rld. To use rld, you’ll first need to load it to your Redis by running it like any regular script – this will cause rld to burrow into your Redis’ Lua environment until the next server restart or a call to SCRIPT FLUSH.

rld can use both Redis’ log file and Pub/Sub (methods 1 and 4 in the abovementioned post, respectively) for its output. To keep track with it just tail the log file and/or subscribe to the `rld` channel. Note that after you’ve loaded rld, it will stay dormant until explicitly activated by your Lua script and will remain active as long as the script runs or until rld is stopped.

So, to actually use rld for debugging your script, you’ll need to switch it on by calling its `start` function – simply add the following line at the beginning of your Lua script:

```python
rld.start()

```

Now you can run your script. It will be executed normally (or rather abnormally since we are talking about debugging after all) , but at the same time rld will be tracking it and printing information about its execution. Read the output carefully until you’ve arrived at that Aha!/#facepalm moment.

Here’s an example – consider the following Lua script called prog.lua:

```python
rld.start()

local function isanswer(n)
  local answer = 42
  if n == answer then
    return true
  else
    return false
  end
end

local t = isanswer(ARGV[1])

return ARGV[1] .. " " .. (t and "is" or "isn't") .. " the answer"

```

Now, load rld (if you haven’t already) and run the script – since I’m passing 42 as the argument, I expect it to be the right answer:

```python
foo@bar:~$ redis-cli --eval rld.lua
"rld v0.1.0 loaded to Redis"
foo@bar:~$ redis-cli --eval prog.lua , 42
"42 isn't the answer"

```

Wowza! Wait! What just happened? Easy, just loog in your lok:

```python
foo@bar:~$ tail -n 19 /var/log/redis_6379.log 
[891] 31 Dec 06:37:09.001 # [rld] -- rld v0.1.0 loaded to Redis
[891] 31 Dec 06:37:09.492 # [rld] -- rld v0.1.0 started
[891] 31 Dec 06:37:09.492 # [rld] ARGV[1] = '42'
[891] 31 Dec 06:37:09.492 # [rld] at Lua:@user_script (line: 10)
[891] 31 Dec 06:37:09.493 # [rld] at Lua:@user_script (line: 12)
[891] 31 Dec 06:37:09.493 # [rld] new [isanswer] = (function)
[891] 31 Dec 06:37:09.493 # [rld] call to function Lua:isanswer
[891] 31 Dec 06:37:09.493 # [rld]     args [n] = '42'
[891] 31 Dec 06:37:09.493 # [rld]     at Lua:isanswer (line: 4)
[891] 31 Dec 06:37:09.493 # [rld]     at Lua:isanswer (line: 5)
[891] 31 Dec 06:37:09.493 # [rld]     new [answer] = 42
[891] 31 Dec 06:37:09.493 # [rld]     at Lua:isanswer (line: 8)
[891] 31 Dec 06:37:09.493 # [rld] return from function Lua:isanswer
[891] 31 Dec 06:37:09.493 # [rld] at Lua:@user_script (line: 14)
[891] 31 Dec 06:37:09.493 # [rld] new [t] is false
[891] 31 Dec 06:37:09.493 # [rld] return from function Lua:@user_script
[891] 31 Dec 06:37:09.494 # [rld] -- profiler summary:
[891] 31 Dec 06:37:09.494 # [rld] --   Lua:isanswer called x1 times
[891] 31 Dec 06:37:09.494 # [rld] -- rld exited: end of script.

```

Can you say Halle-Lua? Isn’t this really va-Lua-ble? rld can be downloaded from [https://github.com/RedisLabs/redis-lua-debugger](https://github.com/RedisLabs/redis-lua-debugger). I hope you’ll find it useful at least as much as I had fun making it. Sure, there’s still a lot that can be done to improve and extend rld but I feel it’s already an MVP so I’m releasing it now. As for prog.lua… well, I’m still trying to remember what I forgot in order to fix it. If you spot the bug, please call tonumber: 555-1234.

Questions? Feedback? Feel free to email me ([itamar@redis.com](mailto:itamar@redis.com)) or tweet me ([@itamarhaber](https://twitter.com/itamarhaber)) about anything and everything – I’m highly avai-Lau-ble 🙂
