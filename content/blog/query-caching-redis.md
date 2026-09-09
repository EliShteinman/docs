---
title: "Query Caching with Redis"
linkTitle: "Query Caching with Redis"
url: "/blog/query-caching-redis/"
description: "Find out if your cache is enterprise-grade, and learn how to: Scale globally while maintaining low latency and cache more efficiently to lower costs"
date: 2019-04-30
blogCategories:
- "How To and Tutorials"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 30 April 2019 · updated 27 March 2025*

![Blog tile image](/images/blog/ee217db664458240a4f1ac3febbd4435de267834-202x210.webp)

[*Find out if your cache is enterprise-grade, and learn how to: Scale globally while maintaining low latency and cache more efficiently to lower costs*](/meeting/)

When I started out building websites, I didn’t focus much on performance. Performance is a luxury you worry about once you’ve mastered the basics, like HTML and CSS or whatever programming language you’re using on the backend. A beginner’s goal is to stand a site up, be able to get from page-to-page and make sure it looks good on a bunch of devices. Caching and performance are things we figure out later.

There are many great reasons to look into caching solutions. From an SEO perspective, Google penalizes slow websites. If your site has a long load time, your ranking could be impacted, which of course could have a serious revenue impact. [John Mueller of Google says that page load times over two seconds “impact crawling” of your site and that he looks for “[less than] 2-3 seconds.”](https://twitter.com/JohnMu/status/802420206375079936) Another factor is the usability impact of slow loading sites. When I started coding, around eight seconds was acceptable to completely load a page. Only if it took longer than that, did you worry about people abandoning the page. [Today that time is probably around two seconds and may be even less depending on your industry](https://www.thinkwithgoogle.com/marketing-resources/data-measurement/mobile-page-speed-new-industry-benchmarks/).

The bottom line: the faster your site, the better it ranks and the more visitors will stay and interact. But still, this issue didn’t come to a head for me until my client called and said their new site was “too slow.” To be fair, it had some heavy images on it and they were using a terrible hosting company. This was also back in the day when $10 hosting meant your site was on a shared server. Their idea of server optimization was to install the latest version of CPanel (yikes). After some digging, I built a basic page caching system and it worked great. The client was happy, I started learning a new skill, and things were good. But soon I realized that although page-level caching was a great tool, it was only one tool.

### When page caching falls short

Page caching works like this: a request comes in, the server processes it and then stores the resulting HTML. For the purposes of this blog post, let’s use an example with Redis. The next time someone requests our page, it will check the cache first. If the page is there, the system will use that instead of processing the request at the server level.

This scenario works well for pages that don’t change too much, e.g. the terms and conditions or privacy policy. These pages aren’t trafficked the same as the main application, which probably has user-based dynamic data.

Let’s imagine we’ve got an application that acts as a user directory and allows filtering based on some sort of activity. Users can view a list of people and see their email address and phone number. Our app uses a SQL database, so to get that data out we need a simple select query:
SELECT username, email, phone_number FROM users WHERE activity='baseball';

In our app, let’s say that activity is a list users set up when they sign up. So, the types of activities people can see vary by user. We’ll store the activity list in another table and would require that information on this page too.

SELECT name, id FROM activity_list WHERE user_id=1;

In this situation, we’ve got a query that needs to run against the current user. The data this user will see is a subset of the whole list that’s unique to them. Given this, we can’t cache the page, so we need to cache each individual query instead.

### Cache queries, not pages

Now we need to think about when to cache the queries and how. One easy solution is to use Redis Hashes to store our result set. We can store the data as a JSON-encoded string, and when we’re ready, just pull that out and use it in our codebase.

So what does caching look like? Here’s some pseudo-code:
1. > HGET user-activity-list cache

2. if the result is not nil return the result set else go to step 3

3. run the query and save the DB result set to a variable

4. if the DB result size is > 0

5. transform the result set data to a JSON string

6. > HSET user-activity-list cache JSON string result set

7. else result set <= 0 throw error

In regards to the above pseudo-code, I should point out that of course we’re ignoring the fact that this is actually a session store pattern. In the real world, you’re not going to want to just cache these queries forever in Redis, you’d create and store them only while the user is logged into and active on your site. I’ve created this generic *user-activity-list* key in Redis only as an example to demonstrate the theory and spark ideas for how you could do this in your own code.

Along with that, our key name isn’t the best. The name *user-activity-list* is again just for this very generic and very narrow example. For an actual application, you’d want to name your keys in a more predictable way. If I was doing this for real, the key would have the username in it somewhere and this would all be part of the user session so it’d be easy to retrieve and use.

Moving on, there are a couple of problems we should address. First, we’re getting the *user-activity-list*, but after we run this query once, we should probably expire the query so we don’t risk showing our user some rather stale data. There are a couple of different ways we could solve this issue.

### Expire on write

Assume this list of activities is something the user herself updates. She would go to the settings page, fiddle with some stuff, and save the change. She may only do this once every week or once a month. In this case, we could keep the cache around until the user changes something:
1. user adds "sportsball" their list and saves

2. in response to the user save we UNLINK user-activity-list

You could do the first and second part any way you like. For this system, I’m pretending we have a way to register/push events. That part doesn’t matter much, but what does matter is that our system deletes the cache every time we update. We don’t need to worry about re-caching the data, since that’s the job of the original function.

### Expire on time

Expire on write may not work for every scenario. There are cases where we’ll want to cache the query for a set amount of time only. For these, we can use Redis to expire our keys.

Let’s take our first caching solution and see what that looks like with a Redis EXPIRE in it:
1. > HGET user-activity-list cache

2. if the result is not nil return the cached value else go to step 3

3. run the query and save DB result set to a variable

4. if the DB results size is > 0

5. transform the result set data to a JSON string

HSET user-activity-list cache JSON string results

EXPIRE user-activity-list 100



The trick here is in step five. After setting the key, we use Redis to set up an expire time (in seconds) for that key. Redis will delete the key for us so we don’t have to worry about managing that in our code.

### Conclusion

In situations where page level caching doesn’t work or won’t be effective, caching database queries is a great alternative. We can use Redis to set and get a hash value with saved query values, and return those values instead of hitting the database. This would speed up our site incredibly. Think about this: the standard time to access and return information from a database to a user is 100 milliseconds, while the average time from Redis is only two milliseconds. That’s a massive performance gain.

| Page views per hour | Database queries per page | Time per query | # of database queries | Performance impact per hour |
|---|---|---|---|---|
| 1,000 | 2-5 | 100ms | 2,000-5,000 | 3.33-8.33 minutes |

In our fictional app, if users hit this activity page 1000 times an hour and we have to hit the database each time, that’s going to add up (and this is for only one query). Imagine if this page has 2-5 queries? What if those queries required complex joins with multiple tables? Three synchronous queries on a page could easily take upwards of 300 milliseconds just to return data from the database. In a world where we only have 2-3 seconds to capture our user’s attention, why put ourselves at that disadvantage?

Now, imagine that we can retrieve the data from our cache 90% of the time.

| Page views per hour | Database queries per page | Time per query | Time per cache hit | Cache hit | # of database queries | # of Redis calls | Performance impact per hour |
|---|---|---|---|---|---|---|---|
| 1,000 | 2-5 | 100ms | 2ms | 90% | 200-500 | 1,800-4,500 | 23.5-59 seconds |

Caching queries in Redis could turn that 300 milliseconds into just six milliseconds on a single page. Across the entire site, this drops time spent grabbing data from many minutes in an hour to just a few seconds. That’s a performance boost that should make for very happy clients.

In our fictional app, if users hit this activity page 1000 times an hour and we have to hit the database each time, that’s going to add up (and this is for only one query). Imagine if this page has 2-5 queries? What if those queries required complex joins with multiple tables? Three synchronous queries on a page could easily take upwards of 300 milliseconds just to return data from the database. In a world where we only have 2-3 seconds to capture our user’s attention, why put ourselves at that disadvantage?

Now, imagine that we can retrieve the data from our cache 90% of the time.

Caching queries in Redis could turn that 300 milliseconds into just six milliseconds on a single page. Across the entire site, this drops time spent grabbing data from many minutes in an hour to just a few seconds. That’s a performance boost that should make for very happy clients.
