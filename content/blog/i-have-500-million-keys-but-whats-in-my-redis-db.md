---
title: "I Have 500 Million Keys But What’s In My Redis DB?!?"
linkTitle: "I Have 500 Million Keys But What’s In My Redis DB?!?"
url: "/blog/i-have-500-million-keys-but-whats-in-my-redis-db/"
description: "While you could consider them a “Rich People Problems,” big databases do present big challenges. Scaling and performance are perhaps the most popularly-debated of these, but even trivial operations..."
date: 2014-06-02
blogCategories:
- "Tech"
authors:
- "Yoav Steinberg"
lastmod: 2025-03-04
hidden: true
mirrored: true
---

*By Yoav Steinberg · Published 2 June 2014 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

## Or: The Bigger They Are, The Harder They F(etch)all

While you could consider them a “Rich People Problems,” big databases do present big challenges. Scaling and performance are perhaps the most popularly-debated of these, but even trivial operations can become insurmountable as the size of your database grows. Recently, while working on a memory fragmentation issue with one of our users’ databases, I was reminded of that fact.

For my investigation of the fragmentation issue, I needed information about the database’s keys. Specifically, to understand what had led to the high fragmentation ratio that the database exhibited, I wanted to estimate the size of the keys’ values, their TTL and whether they were being used. The only problem was that that particular database had an excess of 500,000,000 keys. As such, iterating over all the keys to obtain the information I was looking for wasn’t a practical option. So, instead of using the brute force approach, I developed a [little Python script](https://gist.github.com/yoav-steinberg/d7f9c6924b3d7d1761da) that helped me quickly arrive at a good estimate of the data. Here’s a sample of the script’s output:

```javascript
Skipped 0 keys
Size range  Count   Volatile   Avg TTL  Avg idle
0-49        9346    9346       188522   26039
600-649     32      32         35055    48105
650-699     241     241        35690    47514
700-749     231     231        41808    41045
750-799     62      62         42681    40406
800-849     64      64         42840    39630
850-899     17      17         59546    24997
900-949     3       3          82829    3570
1050-1099   4       4          44159    39322

```

Instead of crunching the entire mountain of data, my script basically uses a small (definable) number of random samples to generate the data I needed (i.e. average data sizes, TTLs and so forth). While the script’s results aren’t as accurate as a fetch-and-process-all maneuver, it gave me the information I was looking for. You can find the script’s source immediately below and I hope you’ll find it useful.

```python
import redis

r = redis.Redis()
base = 0 # Smallest allowed key in samples
jump = 50 # Key size bins
top = 1300 # Largest allowed key in sample
samples = 1000 # Numbers of samples

bins = []
for i in xrange(1+(top-base)/jump):
  bins.append({'count':0,'ttl':0,'idle':0,'volatile':0})

found = 0
for i in range(samples):
    k = r.randomkey()
    idle = r.object("idletime", k) # Must read idle time first before accessing the key
    if not r.type(k) == 'string':
        continue
    l = r.strlen(k)
    if l < base or l > top:
        continue
    found += 1
    ttl = r.ttl(k)
    b = bins[(l - base)/jump]
    b['count'] += 1
    if ttl is not None:
        b['ttl'] += ttl
        b['volatile'] += 1
    b['idle'] += idle

start = base
print "Skipped %d keys"%(samples - sum([b['count'] for b in bins]))
print '%-13s %-10s %-10s %-10s %-10s'%('Size range', 'Count', 'Volatile', 'Avg TTL', 'Avg idle')
for b in bins:
    if b['count']:
        print "%-13s %-10d %-10d %-10d %-10d"%('%d-%d'%(start, start+jump-1), b['count'], b['volatile'], b['ttl']/b['volatile'] if b['volatile'] else 0, b['idle']/b['count'])
    start += jump

```
