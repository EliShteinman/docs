---
title: "Bits and Bats"
linkTitle: "Bits and Bats"
url: "/blog/bits-and-bats/"
description: "In this article you’re going to learn how to perform bithree books on NodeJStwise operations on Redis keys, as well as setting, getting and comparing binary values. To begin, let’s think about how..."
date: 2018-05-21
blogCategories:
- "Tech"
authors:
- "Sandro Pasquali"
lastmod: 2025-03-27
hidden: true
---

*By Sandro Pasquali · Published 21 May 2018 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

In this article you’re going to learn how to perform bithree books on NodeJStwise operations on Redis keys, as well as setting, getting and comparing binary values. To begin, let’s think about how “flipping bits” can be a useful way of storing information in general, and then how we can execute binary operation with Redis.

Take the following example: there are 30 Major League Baseball teams, and each team plays 162 games per year. There are 2430 total games played each year. These games are played over roughly six months. We know a month never has more than 31 days, so we can store the playing schedule of a single team over one month using 31 bits of a 32-bit number.

As you already know one (1) byte is 8 bits, and bits are tracked “right-to-left” in binary (base 2) numbers. The zero (0) bit is rightmost and smallest. The largest number you can represent with 8 bits is 256:

```python
11111111
(2^7)+(2^6)+(2^5)+(2^4)+(2^3)+(2^2)+(2^1)+(2^0)
 128 + 64 +  32 +  16 +  8  +  4  +  2  +  1 = 256

```

In the examples below, we’ll be working with 32-bit numbers (4 bytes), with the 31st bit position (the largest possible in any given month) addressed at 2^30.

Let’s say The New York Yankees play on the 1st, the 3rd to the 10th, the 13th-28th and the 31st. In bits, beginning rightmost, where the zero bit represents the first day, this looks like:

```python
1001111111111111111001111111101
^31st                ^10th    ^1st

Or in decimal:

1342174205

```

This shows that we’ll need 10 bytes to store the monthly schedule for an MLB team. Which means we can store the schedules for every team in 10 * 30 bytes (bytes * number of teams), which is not many bytes, and on top of that we can prove that this is the maximum space we’ll *ever* need, unless the rules governing baseball change.

If you wanted to know if the team was playing on the 13th, you would need to get a bitmask for the 13th bit (using the left-shift operator <<):

1 << 12 // 4096

Using a language like JavaScript we can demonstrate the left-shift and implied 0 padding on a 31 bit number more clearly:

```python
parseInt('0000000000000000001000000000000', 2) // 4096

```

Or visualized as the comparison of two strings of zeros and ones:

```python
1001111111111111111001111111101
& 0000000000000000001000000000000
                    ^      
                    1 & 1 === true

```

Similarly, we can set the 13th bit using the OR(|) operator:

1342174205 | 4096

Or more explicitly:

```python
1242174205 | Math.pow(2^12)

```

Neat! Now let’s use Redis to store much larger amounts of binary data.

## How does Redis enable bitwise operations?

Redis is a data structure store built on the key/value paradigm, and the most basic operation is to store a string in a key:

```python
redis-cli> set mykey 1
redis-cli> get mykey
redis-cli> "1"

```

The Redis BITOP-family of commands allow you to perform bit operations on string keys. Using the well named SETBIT and GETBIT commands you can… set and get bits on a key. You can set comparison keys using the bitwise operators AND, OR, and XOR, as we did with the MLB schedule above. For example, let’s turn on the 3rd bit key test:

```python
> SETBIT test 3 1
> GETBIT test 3 // 1
> GETBIT test 2 // 0 (not set)

```

That was easy. It should be clear how to accomplish the test above by setting bits on certain days of a team schedule, or creating masks.

Let’s use bitmaps to solve the problem of storing the win/loss record of the Yankees. We know they will play 162 games in a year. If 1 is a win and 0 is a loss, we can create a Redis key ‘yankees_record’ and set all the wins like this:

```python
> SETBIT yankees_record 2 1 // Won game 2
> SETBIT yankees_record 3 1
> SETBIT yankees_record 10 1 // Breaking 6 game losing streak!
> SETBIT yankees_record 11 1
> ...

```

By applying bitmasks mapping a range of bits to other binary values, you can make very rapid and memory-efficient analytical comparisons. In the next section we will learn some typical examples of how to use this technique.

Any key in a Redis database can store (2^32 – 1) bits, or just under 512 MiB ([for now](https://twitter.com/antirez/status/956110696911200256)). This means that there are approximately 4.29 billion columns, or offsets, that can be set per key. This is a large number of bits referenced in a single key. We can set bits along these ranges to describe the characteristics of an item we would like to track, such as the number of users who have viewed a given article.

Assume that we are serving many different articles and each article is assigned a unique identifier. Also assume that we have 100,000 active members on our website, and that each user also has a unique identifier—a number between 1 and 100,000. We can use bit operations to track view activity by creating a key unique to that article and setting bits corresponding to the ID of the user viewing the given article. The following example shows that article 808 has been viewed by users 4, 6, 9-11, and so on:

article:808:01-03-2018 : 00010100111010001001111...

This key represents article 808 on a specific date, efficiently storing the unique user IDs of viewers on that day by flipping a bit at the offset corresponding to the user’s assigned ID. Whenever a user views an article, we use the [SETBIT](https://redis.io/commands/setbit) command to set a bit at the offset provided by that user’s ID:

```python
client.GETBIT('article:808:01-03-2018', userId, 1)

```

Let’s create data for three articles:

```python
const redis = require('redis');
const client = redis.createClient(/* your configuration info */);
const multi = client.multi();
// Create three articles with randomized hits representing user views
let id = 100000;
while(id--) {
    multi.SETBIT('article1:today', id, Math.round(Math.random(1)));
    multi.SETBIT('article2:today', id, Math.round(Math.random(1)));
    multi.SETBIT('article3:today', id, Math.round(Math.random(1)));
}
multi.exec(err => {
    // done
})

```

Here, we simply created three Redis keys, article (1-3):today, and randomly set 100,000 bits on each key—either 0 or 1. Using the technique of storing user activity based on user ID offsets, we now have sample data for a hypothetical day of traffic against three articles.

To count the number of users who have viewed an article, we can use BITCOUNT:

```python
client.bitcount('article1:today', (err, count) => {
    console.log(count)
})

```

This method is straightforward: the number of users who saw the article equals the number of bits set on the key. Now, let’s count the total number of article views:

```python
client.multi([
    ["bitcount", "article1:today"],
    ["bitcount", "article2:today"],
    ["bitcount", "article3:today"]
]).exec((err, totals) => {
    let total = totals.reduce(function(prev, cur) {
        return prev + cur;
    }, 0);
    console.log("Total views: ", total);
})

```

Once [MULTI](https://redis.io/commands/multi) returns an array of results corresponding to the results [SETBIT](https://redis.io/commands/setbit) returned from Redis for each operation (a count of bits), we reduce the count to a sum representing the total number of views of all our articles.

If we are interested, instead, in how many articles user 123 has viewed today, we can use [GETBIT](https://redis.io/commands/getbit), which simply returns the value (either 0 or 1) at a given offset. The result will be in the range 0–3:

```python
client.multi([
    ["GETBIT", "article1:today", 123],
    ["GETBIT", "article2:today", 123],
    ["GETBIT", "article3:today", 123]
]).exec((err, hits) => {
    let total = hits.reduce(function(prev, cur) {
        return prev + cur;
    }, 0);
    console.log(total); // 0, 1, 2 or 3
})

```

These are very useful and direct ways to glean information from bit representations. Let’s go a little further and learn about filtering bits using bitmasks and the AND, OR, and XOR operators.

What if we want to check whether user 123 has read both articles? Using the [BITOP](https://redis.io/commands/bitop) AND, this is easy to accomplish:

```python
client.multi([
    ['SETBIT', 'user123', 123, 1],
    ['BITOP', 'AND','123:sawboth','user123','article1:today', 'article3:today'],
    ['GETBIT', '123:sawboth', 123]
]).exec((err, result) => {
    let sawboth = result[2];
    console.log('123 saw both articles: ', !!sawboth);
});

```

First, we create a mask that isolates a specific user stored at the key *user123*, containing a single positive bit at offset 123 (again, representing the user’s ID). The results of an AND operation on two or more bit representations is not returned as a value by Redis but rather written to a specified key, which is given in the preceding example as “123:sawboth.” This key contains the bit representation that answers the question of whether or not both the article keys contain bit representations that also have a positive bit at the same offset as the user123 key.

The OR operator works well when trying to find the total number of users who have seen at least one article:

```python
client.multi([
    ['BITOP', 'OR','atleastonearticle','article1:today','article2:today','article3:today'],
    ['bitcount', 'atleastonearticle']
]).exec((err, results) => {
    console.log("At least one: ", results[1]);
});

```

Here, the *atleastonearticle* key flags bits at all offsets that were set in any one of the three articles. We can use these techniques to create a simple recommendation engine.

For example, if we are able to determine via other means that two articles are similar (based on tags, keywords, and so on), we can find users who have read one and recommended the other. To do this we use XOR to find all users that have read the first article or the second article, but not both. We then break that set into two lists: those who have read the first article and those who have read the second article and compare these lists to offer recommendations:

```python
client.multi([
    ['BITOP','XOR','recommendother','article1:today','article2:today'],
    ['BITOP','AND','recommend:article1','recommendother','article2:today'],
    ['BITOP','AND','recommend:article2','recommendother','article1:today'],
    ['bitcount', 'recommendother'],
    ['bitcount', 'recommend:article1'],
    ['bitcount', 'recommend:article2'],
    ['del', 'recommendother', 'recommend:article1','recommend:article2']
]).exec((err, results) => {
    // Note result offset due to first 3 setup ops
    console.log("Didn't see both articles: ", results[3]);
    console.log("Saw article2; recommend article1: ", results[4]);
    console.log("Saw article1; recommend article2: ", results[5]);
})

```

While it is not necessary, we also fetch a count of each list and delete the result keys when we are done.

To calculate the total number of bytes occupied by a binary value in Redis, divide the largest offset by 8. Storing access data for 1,000,000 users on one article requires a maximum of ~125 kB—not a very large amount of memory or storage to spend in return for such a rich set of analytics data. Because we can accurately measure the space needed, this also gives us some confidence when planning storage costs, scaling and so forth.

## About the Author

Sandro Pasquali formed a technology company named Simple in 1997, that sold the world’s first JavaScript-based application development framework and was awarded several patents for deployment and advertising technologies that anticipated the future of Internet-based software. He has written three books on NodeJS. He builds enterprise-class software for private clients, often deploying the incredibly versatile Redis to help meet complex information management requirements for large clients.
