---
title: "Storing counters in Redis"
linkTitle: "Storing counters in Redis"
url: "/glossary/storing-counters-in-redis/"
description: "As we monitor our application, being able to gather information over time becomes ever more important. Code changes (that can affect how quickly our site responds, and subsequently how many pages..."
lastmod: 2025-06-30
---

*updated 30 June 2025*

As we monitor our application, being able to gather information over time becomes ever more important. Code changes (that can affect how quickly our site responds, and subsequently how many pages we serve), new advertising campaigns, or new users to our system can all radically change the number of pages that are loaded on a site. Subsequently, any number of other performance metrics may change. But if we aren’t recording any metrics, then it’s impossible to know how they’re changing, or whether we’re doing better or worse.

In an attempt to start gathering metrics to watch and analyze, we’ll build a tool to keep named counters over time (counters with names like site hits, sales, or database queries can be crucial). Each of these counters will store the most recent 120 samples at a variety of time precisions (like 1 second, 5 seconds, 1 minute, and so on). Both the number of samples and the selection of precisions to record can be customized as necessary. The first step for keeping counters is actually storing the counters themselves.

## Updating a counter

In order to update counters, we’ll need to store the actual counter information. For each counter and precision, like site hits and 5 seconds, we’ll keep a HASH that stores information about the number of site hits that have occurred in each 5-second time slice. The keys in the hash will be the start of the time slice, and the value will be the number of hits. Figure 5.1 shows a selection of data from a hit counter with 5-second time slices.

As we start to use counters, we need to record what counters have been written to so that we can clear out old data. For this, we need an ordered sequence that lets us iterate one by one over its entries, and that also doesn’t allow duplicates. We could use a LIST combined with a SET, but that would take extra code and round trips to Redis. Instead, we’ll use a ZSET, where the members are the combinations of precisions and names that have been written to, and the scores are all 0. By setting all scores to 0 in a ZSET, Redis will try to sort by score, and finding them all equal, will then sort by member name. This gives us a fixed order for a given set of members, which will make it easy to sequentially scan them. An example ZSET of known counters can be seen in figure 5.2.

![RIA](/images/site-mirror/2d1a120c85fe9145055d1f2a2a1f9db2b8e19508-273x93.svg)

*Figure 5.1A HASH that shows the number of web page hits over 5-second time slices around 7:40 a.m. on May 7, 2012*

![ZSET](/images/site-mirror/77fc2cbd4dc18f24bca75ac4c060556b67563d97-267x93.svg)

*Figure 5.2A ZSET that shows some known counters*

Now that we know what our structures for counters look like, what goes on to make that happen? For each time slice precision, we’ll add a reference to the precision and the name of the counter to the known ZSET, and we’ll increment the appropriate time window by the count in the proper HASH. Our code for updating a counter looks like this.Listing 5.3The update_counter() functionPRECISION = [1, 5, 60, 300, 3600, 18000, 86400]

The precision of the counters in seconds: 1 second, 5 seconds, 1 minute, 5 minutes, 1 hour, 5 hours, 1 day—adjust as necessary.def update_counter(conn, name, count=1, now=None): now = now or time.time()

Get the current time to know which time slice to increment. pipe = conn.pipeline()

Create a transactional pipeline so that later cleanup can work correctly. for prec in PRECISION:

Add entries for all precisions that we record. pnow = int(now / prec) * prec

Get the start of the current time slice. hash = ‘%s:%s’%(prec, name)

Create the named hash where this data will be stored. pipe.zadd(‘known:’, hash, 0)

Record a reference to the counters into a ZSET with the score 0 so we can clean up after ourselves. pipe.hincrby(‘count:’ + hash, pnow, count)

Update the counter for the given name and time precision. pipe.execute()

Updating the counter information isn’t so bad; just a ZADD and HINCRBY for each time slice precision. And fetching the information for a named counter and a specific precision is also easy. We fetch the whole HASH with HGETALL, convert our time slices and counters back into numbers (they’re all returned as strings), sort them by time, and finally return the values. The next listing shows our code for fetching counter data.Listing 5.4The get_counter() functiondef get_counter(conn, name, precision): hash = ‘%s:%s’%(precision, name)

Get the name of the key where we’ll be storing counter data. data = conn.hgetall(‘count:’ + hash)

Fetch the counter data from Redis. to_return = [] for key, value in data.iteritems(): to_return.append((int(key), int(value)))

Convert the counter data into something more expected. to_return.sort()

Sort our data so that older samples are first. return to_return

We did exactly what we said we were going to do. We fetched the data, ordered it sequentially based on time, and converted it back into integers. Let’s look at how we prevent these counters from keeping too much data.

## Cleaning out old counters

Now we have all of our counters written to Redis and we can fetch our counters with ease. But as we update our counters, at some point we’re going to run out of memory if we don’t perform any cleanup. Because we were thinking ahead, we wrote to our known ZSET the listing of known counters. To clean out the counters, we need to iterate over that listing and clean up old entries.

WHY NOT USE EXPIRE? One limitation of the EXPIRE command is that it only applies to whole keys; we can’t expire parts of keys. And because we chose to structure our data so that counter X of precision Y is in a single key for all time, we have to clean out the counters periodically. If you feel ambitious, you may want to try restructuring the counters to change the data layout to use standard Redis expiration instead.

As we process and clean up old counters, a few things are important to pay attention to. The following list shows a few of the more important items that we need to be aware of as we clean out old counters:

- New counters can be added at any time.
- Multiple cleanups may be occurring at the same time.
- Trying to clean up daily counters every minute is a waste of effort.
- If a counter has no more data, we shouldn’t try to clean it up any more.

With all of those things in mind, we’ll build a daemon function similar in operation to the daemon functions that we wrote back in chapter 2. As before, we’ll repeatedly loop until the system is told to quit. To help minimize load during cleanup, we’ll attempt to clean out old counters roughly once per minute, and will also clean up old counters at roughly the schedule that they’re creating new entries, except for counters that get new entries more often than once per minute. If a counter has a time slice of 5 minutes, we’ll try to clean out old entries from that counter every 5 minutes. Counters that have new entries more often (1 second and 5 seconds in our example), we’ll clean out every minute.

To iterate over the counters, we’ll fetch known counters one by one with ZRANGE. To clean a counter, we’ll fetch all of the start times for a given counter, calculate which items are before a calculated cutoff (120 samples ago), and remove them. If there’s no more data for a given counter, we’ll remove the counter reference from the known ZSET. Explaining what goes on is simple, but the details of the code show some corner cases. Check out this listing to see the cleanup code in full detail.Listing 5.5The clean_counters() functionsdef clean_counters(conn): pipe = conn.pipeline(True) passes = 0

Keep a record of the number of passes so that we can balance cleaning out per-second vs. per-day counters. while not QUIT:

Keep cleaning out counters until we’re told to stop. start = time.time()

Get the start time of the pass to calculate the total duration. index = 0 while index < conn.zcard(‘known:’):

Incrementally iterate over all known counters. hash = conn.zrange(‘known:’, index, index)

Get the next counter to check. index += 1 if not hash: break hash = hash[0] prec = int(hash.partition(‘:’)[0])

Get the precision of the counter. bprec = int(prec // 60) or 1

We’ll take a pass every 60 seconds or so, so we’ll try to clean out counters at roughly the rate that they’re written to. if passes % bprec:

Try the next counter if we aren’t supposed to check this one on this pass (for example, we’ve taken three passes, but the counter has a precision of 5 minutes). continue hkey = ‘count:’ + hash cutoff = time.time() – SAMPLE_COUNT * prec

Find the cutoff time for the earliest sample that we should keep, given the precision and number of samples that we want to keep. samples = map(int, conn.hkeys(hkey))

Fetch the times of the samples, and convert the strings to integers. samples.sort() remove = bisect.bisect_right(samples, cutoff)

Determine the number of samples that should be deleted. if remove: conn.hdel(hkey, *samples[:remove])

Remove the samples as necessary. if remove == len(samples):

The data HASH may be empty. try: pipe.watch(hkey) if not pipe.hlen(hkey): pipe.multi() pipe.zrem(‘known:’, hash)

Watch the counter hash for changes.

Verify that the counter hash is empty, and if so, remove it from the known counters. pipe.execute() index -= 1

If we deleted a scounter, then we scan use the same sindex next pass. else: pipe.unwatch()

The hash isn’t empty; keep it in the list of known counters. except redis.exceptions.WatchError: pass

Someone else changed the counter hash by adding counters, which means that it has data, so we’ll leave the counter in the list of known counters. passes += 1 duration = min(int(time.time() – start) + 1, 60)

passes += 1 duration = min(int(time.time() – start) + 1, 60) time.sleep(max(60 – duration, 1))

Sleep the remainder of the 60 seconds, or at least 1 second, just to offer a bit of a rest.

As described earlier, we iterate one by one over the ZSET of counters, looking for items to clean out. We only clean out counters that should be cleaned in this pass, so we perform that check early. We then fetch the counter data and determine what (if anything) should be cleaned up. After cleaning out old data as necessary, if we don’t believe that there should be any remaining data, we verify that there’s no more data for the counter and remove it from our ZSET of counters. Finally, after passing over all of the counters, we calculate how long it took to perform a pass, and sleep roughly the remainder of the minute we left for ourselves to perform the full cleanup, until the next pass.

Now that we have counter data, are cleaning it up, and can fetch it, it’s just a matter of building an interface for consuming the data. Sadly, that part is out of the scope of this book, but there are a few usable JavaScript plotting libraries that can help you out on the web side of things (I’ve had goodexperiences with jqplot [[http://www.jqplot.com/](http://www.jqplot.com/)], Highcharts [[http://www.highcharts.com/](http://www.highcharts.com/)], dygraphs [[http://dygraphs.com/](http://dygraphs.com/)], and D3 [[http://d3js.org/](http://d3js.org/)] for personal and professional uses).

When dealing with the depth of complexity in a real website, knowing that a page gets hit thousands of times a day can help us to decide that the page should be cached. But if that page takes 2 milliseconds to render, whereas another page gets one tenth the traffic but takes 2 seconds to render, we can instead direct our attention to optimizing the slower page. In the next section, we change our approach from keeping precise counters that give us data over time, to keeping aggregate statistics to help us make more nuanced decisions about what to optimize.
