---
title: "Redis Keys in RAM"
linkTitle: "Redis Keys in RAM"
url: "/blog/redis-keys-in-ram/"
description: "Adapted from Dr. Seuss’ “Green Eggs and Ham”. Link to text, art copyrighted by Dr. Seuss."
date: 2015-10-05
blogCategories:
- "Tech"
authors:
- "Itamar Haber"
lastmod: 2026-08-13
hidden: true
mirrored: true
---

*By Itamar Haber, Technology Evangelist · Published 5 October 2015 · updated 13 August 2026*

![Blog tile image](/images/site-mirror/3319a3cec387cd4e94d0023116555615140d1dd4-140x92.webp)

![Redis Keys in RAM](/images/site-mirror/2182571fcb2a3e3be98baa5d32141d08915bbf40-635x356.webp)

*Adapted from Dr. Seuss’ “Green Eggs and Ham”. *[*Link to text*](https://www.site.uottawa.ca/~lucia/courses/2131-02/A2/trythemsource.txt)*, art copyrighted by Dr. Seuss.*

![I am San. Do you like Redis keys in RAM?](/images/site-mirror/6a9b5041099e641b45eade1fb9972729e29506cf-635x357.webp)

I am San.
I am San.
San I am.

That San-I-am!
That San-I-am!
I do not like that San-I-am!

Do you like Redis keys in RAM?

I do not like them San-I-am
I do not like Redis keys in RAM.

![Would you like them large or small?](/images/site-mirror/1a7c8a634a8d96dccd60762179dced610dda0c21-635x357.webp)

Would you like them large[1](#fn1) or small?

I would not like them large or small.
I would not like them not at all.
I do not like Redis keys in RAM.
I do not like them San-I-am.

![Would you like them as a String?](/images/site-mirror/a8654c74b77928223c26189c9aa8b4bc1332bdf0-635x357.webp)

Would you like them as a String?
Would you serialize everything?

I do not like them as a String.
I do not like to serialize things.
I do not like them large or small.
I do not like them not at all.
I do not like Redis keys in RAM.
I do not like them San-I-am.

![Would you like them in a Hash?](/images/site-mirror/41608e0c2c036d83e5845531dc70d1a387e9cb78-635x357.webp)

<a
</a
Would you like them in a Hash?
Would you like a Hash as cache?

Not in a Hash. Not as a cache.
Not as a String. No serialized, no anything.
I do not want them large or small.
I do not want them, not at all.
I do not want Redis keys in RAM.
I do not want them, San-I-am.<a
</a

![Would you want them as a List instead?](/images/site-mirror/f9faa914300c834ee7f748724c08f2fa67e1e0ae-635x357.webp)

<a
</a
Would you want them as a List instead?
Do you want to access tail, body and head?

Not as a List. Not as a Hash.
Not as a String. Not as a cache.
Small or large I will have naught.
Goodbye San-I-am and thanks a lot.

![Would you? Could you? As a Set?](/images/site-mirror/d8aace9135a84572db593f65611603fe470b5fbe-635x357.webp)

<a
</a
Would you? Could you? As a Set?
Get the difference! Store a union! Or just intersect…

I would not, could not, as a Set.

You may like them.
You’ll see for sure.
You may like
Sorted Sets by score?

![http://try.redis.io](/images/site-mirror/6f0a1fca3c20c3a9de9759d1212ac116bb65ff31-635x356.webp)

<a
</a
I would not, could not by a score.
No more Sets! I say no more!
I do not like them as a List
Stop this now – I do insist.
I do not like them as String or Hash
I do not like an in-memory database or cache.
I do not want Redis keys in RAM.
I do not want them, San-I-am.

You do not like them. So you say.
[https://redis.io/try-free/](https://redis.io/try-free/)! Try them! And you may.
Try them and you may, I say.

![Say! Data structures are so much FUN!](/images/site-mirror/c5d78187d48212ad2307026d25ff9297adc221d2-635x357.webp)

San! If you will let me be,
I will try them. You will see.

<a
</a
Say! I like Redis keys in RAM!
I do! I like them, San-I-am!
So I will have them as a String.
And as a Hash, a List or anything.
And as a Set – both unordered and an ordered one.
Say! Data structures are so much FUN!

I do so like Redis keys in RAM
Thank you! Grazie, San-I-am

---

### Afternote

I presented the above as part of my [“Use Redis in Odd and Unusual Ways”](http://www.slideshare.net/itamarhaber/use-redis-in-odd-and-unusual-ways) talk at [Percona Live Europe 2015 in Amsterdam](https://www.percona.com/live/europe-amsterdam-2015/). While mainly focused around MySQL, the conference’s program had **no less than four sessions** solely about Redis.Excluding my own. Being a Redis advocate, that’s probably the best thing I could hope for, but as a presenter it posed a challenge: how do I prepare a talk that is relevant to an audience that’s heterogeneous not only in its experience with Redis, but also with NoSQL at large?

So the result is a mix of basic and advanced Redis topics that I hope both newcomers as well as Redis veterans can benefit from. The DR.ediseuss motif merits a little background: like many before me, when I took my first steps red-bricked road I was somewhat befuddled[2](#fn1) with the API’s naming scheme. While soaking it all in, I came up with a little “poem” that was but the first step to all that. For your enjoyment, here’s the first (and only) page from my “Dr. Seuss Reads Redis” book:

This is my friend
His name is ZADD
ZADD’s a lad
Who’s always SADD

It’s really bad
that ZADD is SADD
I don’t know why
And that makes me SCARD

I hope that ZADD
Will be someday glad
And that he’ll get over
This stupid PFADD

Lawsuits? Critical acclaim? [Email](mailto:itamar@redis.com?subject=With%20regards%20to%20your%20Redis%20Keys%20in%20RAM%2C%20I%20just%20wanted%20to%20say) or [tweet](https://twitter.com/itamarhaber) me – I’m highly available 🙂

---

FN#1 Keys in Redis can be up to 512MB and are binary safe. Simple string values can be up to 512MB and are binary safe as well. Other data structures can hold 232 elements, each up to 512MB.

FN#2 Note of encouragement to fellow beginners – it will soon fall perfectly into place and you’ll wonder what was so befuddling in the first place 🙂
