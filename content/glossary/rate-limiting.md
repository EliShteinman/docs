---
title: "Rate Limiting"
linkTitle: "Rate Limiting"
url: "/glossary/rate-limiting/"
description: "Rate limiting is a technique used in computer systems to control the rate at which requests are sent or processed in order to maintain system stability and security. In web applications, rate..."
lastmod: 2025-12-08
---

*updated 8 December 2025*

## Rate Limiting Defined

Rate limiting is a technique used in computer systems to control the rate at which requests are sent or processed in order to maintain system stability and security. In web applications, rate limiting restricts the number of requests that a client can make to a server within a given time period to prevent abuse and ensure fair usage of resources among multiple clients.

As our reliance on web applications and services grows, so does the risk of cyber attacks. In 2020, there were over 2 billion cyber attacks, according to [a report by RiskIQ](https://www.forbes.com/sites/chuckbrooks/2021/03/02/alarming-cybersecurity-stats-------what-you-need-to-know-for-2021/?sh=762cc97f58d3). Rate limiting is an effective tool for protecting against such attacks. It can help prevent overload by limiting the amount of traffic that can access a website or application within a given time frame. This technique can keep cyber threats at bay and maintain the stability of the system.

Overall, rate limiting is an important mechanism that helps ensure the security and reliability of computer systems, and it is commonly used in various applications, including web APIs, web servers, and network infrastructure.

## Why is rate limiting necessary for applications and systems?

Rate limiting is an essential component of any security strategy for practical application and system management. It helps prevent a wide range of malicious activities, such as DDoS attacks, brute force attacks, credential stuffing, inventory hoarding attacks, and data scraping, by limiting the number of requests or connections that can be made to an application or system.

Implementing rate limiting can help organizations ensure that resources are available to all users and prevent malicious activity from overwhelming the system. By limiting the number of requests, companies can protect against various types of attacks, such as:

**DDoS attacks**: By restricting the number of requests to a reasonable level, organizations can prevent DDoS attacks from overloading their system and bringing it down.

**Credential stuffing:** Limiting login attempts from a single IP address or user can prevent credential stuffing attacks, where attackers use automated scripts to try different combinations of usernames and passwords until they find a good match.

**Brute force attacks:** Limiting the number of requests or attempts to access a resource can help prevent brute force attacks, where attackers try different combinations of characters to gain access to a system or application.

**Data scraping:** Rate limiting can help prevent data scraping by restricting the number of requests made by a single user or IP address. Attackers are prevented from scraping sensitive data.

**Inventory hoarding attacks:** Limiting the number of requests for a particular item or resource can thwart inventory hoarding attacks, where attackers try to purchase all available inventory of a popular item to resell at a higher price.

Overall, rate limiting is a necessary tool for applications and systems to ensure the security and reliability of resources while protecting against malicious activity. By implementing rate limiting, companies can improve their security posture and prevent attacks, ensuring that resources are available to all users.

## Types of rate limiting

**IP-Based**

One common type of rate limiting is IP-based, which restricts access based on the source IP address of the request. It can help prevent attacks from a small number of IP addresses, but it can be less effective against distributed attacks.

**User-Based**

User-based rate limiting is another method that restricts access based on the user account making the request. It can help prevent credential stuffing attacks, but it requires identifying unique users across different sessions, which can be challenging.

**Application-Based**

Application-based rate limiting restricts access based on the type of application making the request. It can help prevent inventory hoarding and data scraping attacks, but it may not be effective against attacks coming from legitimate applications.

**Token Bucket**

Token bucket rate limiting is a popular approach that regulates the flow of requests using a token bucket. Each request consumes a token from the bucket, and once the bucket is empty, no more requests are allowed until the bucket is refilled.

Organizations should regularly review and update their rate limiting policies to ensure they remain effective against new and emerging threats. Additionally, it’s essential to choose the rate limiting method that best fits your organization’s specific needs and requirements.

## How does rate limiting work?

Rate limiting is something like a bouncer at a nightclub. A bouncer assess the flow of people into the club and stops entry if things are becoming overcrowded and unsafe. Similarly, rate limiting controls the number of requests to an application to prevent it from becoming overwhelmed or crashing. Just as the bouncer may limit entry to a certain number of people per hour, rate limiting can limit requests to a certain number per second or minute. By carefully managing the flow of people or requests, both the bouncer and rate limiting help to maintain a safe and reliable environment for everyone.

Rate limiting normally is based on tracking IP addresses and measures the time between each request. When a user makes a request, the system tracks it and compares the number of requests made to a predefined threshold. If the number of requests exceeds the threshold, rate limiting kicks in and the system will not fulfill the user’s requests for a certain amount of time.

## Algorithms used for rate limiting

Rate-limiting algorithms are essential tools that enable organizations to control and limit the rate of incoming requests to their applications and systems. Different algorithms can be used depending on the specific needs of the application or system.

**Fixed-window rate limiting:** This is a straightforward algorithm that counts the number of requests received within a fixed time window, such as one minute. Once the maximum number of requests is reached, additional requests are rejected until the next window begins. This algorithm is easy to implement and effective against DDoS attacks but may limit legitimate users.

**Sliding-window rate limiting:** This algorithm tracks the number of requests received in the recent past using a sliding window that moves over time. This algorithm is more flexible than fixed-window rate limiting and can adjust to spikes in traffic, making it a better choice for applications with varying usage patterns. However, it may not be as effective against sustained attacks.

**Token bucket rate limiting:** This maintains a token bucket that is refilled at a fixed rate. Each request consumes a token, and additional requests are denied once the bucket is empty. Token bucket rate limiting is suitable for handling bursts of traffic, as it can allow a certain number of requests to be processed simultaneously. However, it may not be as effective against sustained traffic.

**Leaky bucket rate limiting:** Similar to token bucket rate limiting but puts requests into a “bucket” that gradually empties over time, allowing more requests to be processed. This algorithm is effective against bursts of traffic and helps to prevent overload, but it may not be as effective against sustained attacks.

Choosing the right rate-limiting algorithm depends on several factors, including the application’s traffic patterns and the desired level of protection against malicious activity. Organizations must strike a balance between protecting their systems and providing a good user experience. Regularly reviewing and updating rate-limiting policies is also essential to ensure that they remain effective against new and emerging threats.

## Rate limiting use cases

Many popular websites and applications use rate limiting to prevent malicious attacks, improve performance, and ensure fair usage for all users. Here are some real-world use cases for rate limiting:

1. Google Maps API – The Google Maps API is a popular tool for developers to integrate maps and location-based services into their applications. However, due to its popularity, the API is a frequent target of malicious traffic, which can overload the service and affect legitimate users. Google Maps API uses [rate limiting](https://cloud.google.com/architecture/rate-limiting-strategies-techniques) to protect against these attacks and ensure all users can access the service.
1. GitHub API – GitHub is a code hosting platform millions of developers worldwide use. The GitHub API provides programmatic access to many platform features, such as creating and managing repositories. Excessive API usage can cause performance issues for the platform and affect other users. [GitHub uses rate limiting](https://docs.github.com/en/apps/creating-github-apps/creating-github-apps/rate-limits-for-github-apps) to prevent these issues and ensure all users can access the API fairly.
1. Twitter API – The Twitter API allows developers to build applications that interact with the Twitter platform, such as posting tweets or retrieving user data. Abusive or spammy API usage can harm the platform and other users. [Twitter uses rate limiting](https://developer.twitter.com/en/docs/twitter-api/rate-limits#:~:text=Users'%20rate%20limits%20are%20shared,per%20user%20rate%20limit%20bucket.) to prevent these issues and ensure all users can access the API without interruption.
1. Cloudflare – Cloudflare is a popular content delivery network and security service many websites and applications use. [Cloudflare uses rate limiting](https://developers.cloudflare.com/support/firewall/tools/configuring-cloudflare-rate-limiting/#:~:text=Cloudflare%20Rate%20Limiting%20automatically%20identifies,for%20individual%20Cloudflare%20data%20centers.) to prevent DDoS attacks and other malicious traffic from overwhelming websites and applications, ensuring their availability and security.

In all these examples, rate limiting has helped these websites and applications protect themselves from attacks and ensure their services remain available to legitimate users.

## Redis Rate Limiting Best Practices

Building a rate limiter with Redis is easy because of two commands [INCR](https://redis.io/commands/incr) and [EXPIRE](https://redis.io/commands/expire). The basic concept is that you want to limit requests to a particular service in a given time period. Let’s say we have a service that has users identified by an API key. This service states that it is limited to 20 requests in any given minute.

To achieve this we want to create a Redis key for every minute per API key. To make sure we don’t fill up our entire database with junk, expire that key after one minute as well. Visualize it like this:

*User API Key = zA21X31, Green represents unlimited and red represents limited.*

The key is derived from the User API key concatenated with the minute number by a colon. Since we’re always expiring the keys, we only need to keep track of the minute—when the hour rolls around from 59 to 00 we can be certain that another 59 don’t exist (it would have expired 58 minutes prior).

With pseudocode, let’s see how this would work.

- Query and increment the counter, adding or updating the expiration:
- If the result from INCR is less than 20 (or unset) then show an error message and end the connection. Exit.
- Do service stuff.

Two key points to understand from this routine:

1. INCR on a non-existent key will always be 1. So, the first call of the minute will be result the value of 1
1. EXPIRE is inside a MULTI transaction along with the INCR, which means form a single atomic operation.

The worse-case failure situation is if, for some very strange and unlikely reason, the Redis server dies between the INCR and the EXPIRE. When restoring either from an AOF or in-memory replication, the INCR will not be restored since the transaction was not complete.

With this pattern, it’s possible that anyone one user will have two limiting keys, one that is being currently used and the one that will expire during the same minute window, but it is otherwise very efficient.
