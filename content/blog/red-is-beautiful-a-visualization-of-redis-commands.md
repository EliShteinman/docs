---
title: "Red is Beautiful: A Visualization of Redis Commands"
linkTitle: "Red is Beautiful: A Visualization of Redis Commands"
url: "/blog/red-is-beautiful-a-visualization-of-redis-commands/"
description: "Sometimes inspiration strikes and you feel compeled to follow it. That’s exactly what had happened to me when I was reviewing Redis’ documentation repository – while browsing through the..."
date: 2014-07-14
blogCategories:
- "Tech"
authors:
- "Itamar Haber"
lastmod: 2026-09-01
hidden: true
mirrored: true
---

*By Itamar Haber, Technology Evangelist · Published 14 July 2014 · updated 1 September 2026*

![Blog tile image](/images/site-mirror/7d8ffb8cb65e2d7f9ea7f1e388257fed5680db37-650x664.webp)

![](/images/site-mirror/4cbfb2596699ffe2549a81e308d78b1bcaedf2c1-150x150.webp)

Sometimes inspiration strikes and you feel compeled to follow it. That’s exactly what had happened to me when I was reviewing Redis’ [documentation repository](https://github.com/antirez/redis-doc) – while browsing through the [commands.json](https://github.com/antirez/redis-doc/blob/master/commands.json) file, I felt an inexplicable urge to haul it into [D3.js](https://d3js.org). The result is a web toy, an eye candy that serves no practical purpose apart from being that which it is. The [code of this experiment](http://gist.github.com/itamarhaber/e9a87c39467075e2ba76) was adopted from Mike Bostock’s [example](http://mbostock.github.io/d3/talk/20111116/pack-hierarchy.html).

Redis’ 160 or so commands are grouped by topic and zooming in/out is by clicking the mouse. Each command is represented by circle, whose size roughly corresponds to the command’s asymptotic time complexity. Clicking a command will open its documentation page from [redis.io](https://redis.io/docs/latest/commands/). I hope you’ll enjoy it and do feel free to [email](mailto:itamar@redis.com) or [tweet](https://twitter.com/itamarhaber) me with any feedback – I’m highly available 🙂

![](/images/site-mirror/7d8ffb8cb65e2d7f9ea7f1e388257fed5680db37-650x664.webp)
