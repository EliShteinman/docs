---
title: "JSON Web Tokens (JWT) are Dangerous for User Sessions—Here’s a Solution"
linkTitle: "JSON Web Tokens (JWT) are Dangerous for User Sessions—Here’s a Solution"
url: "/blog/json-web-tokens-jwt-are-dangerous-for-user-sessions/"
description: "Download the JSON Web Tokens (JWTs) are not safe e-book here"
date: 2021-06-24
blogCategories:
- "How To and Tutorials"
- "Tech"
- "Uncategorized"
authors:
- "Raja Rao"
lastmod: 2026-05-21
hidden: true
---

*By Raja Rao, Head of Growth Marketing · Published 24 June 2021 · updated 21 May 2026*

![Blog tile image](/images/blog/b3bc7ea76e3d51e208f219a603c096edbaae9543-773x520.webp)

[*Download the JSON Web Tokens (JWTs) are not safe e-book here*](/docs/json-web-tokens-jwts-are-not-safe/)

Sometimes, people take technologies that are intended to solve a narrow problem and start applying them broadly. The problem may appear similar, but utilizing unique technologies to solve general issues could create unanticipated consequences. To use a metaphor, if you are a hammer, everything looks like a nail. JWT is one such technology.

![](/images/blog/c0c7debf17405238ddeac0b4845c7f549d74c537-1024x181.webp)

[Watch the video](https://www.linkedin.com/in/rdegges/)

![not default](/images/blog/5d7295ce3a80af2f61b5e914ec4ded784acfd2e3-1024x94.webp)

![Ptacek](/images/blog/bb22685294247ddb1cae8ae6e785c9a27d44fb40-1024x206.webp)

There are many in-depth articles and videos from SMEs of companies like Okta talking about the potential dangers and inefficiencies of using JWT tokens[1]. Yet, these warnings are overshadowed by marketers, YouTubers, bloggers, course creators, and others who knowingly or unknowingly promote it.

If you look at many of these videos and articles, they all just talk about the perceived benefits of JWT and ignore the deficiency. More specifically, they just show how to use it but don’t talk about revocations and additional complexities that JWT adds in a real production environment. They also never compare it with the existing battle-tested approaches deep enough to really weigh the pros and cons.

Or maybe it’s the perfect, buzzworthy, and friendly name that’s leading to its popularity. “JSON” (generally well-liked), “Web”(for web), and “Token”(implies stateless) make people think that it’s perfect for their web authentication job.

So I think this is a case where the marketing has beaten engineers and security experts. But, it’s not all bad because there are regular long and passionate debates about JWT on Hacker News (see [here](https://news.ycombinator.com/item?id=21783303), [her](https://news.ycombinator.com/item?id=27136539)[e](https://news.ycombinator.com/item?id=27136539) and, [here](https://news.ycombinator.com/item?id=24352360)), so there is hope.

If you think about it, these constant debates themselves should be a red flag because you should never see such debates, especially in the security realm. Security should be binary. Either technology is secure or it’s not.

In any case, in this blog post, I’d like to focus on the potential dangers of using JWT and also talk about a battle-tested solution that’s been around for a decade.

For further understanding, when I talk about JWT, I mean “stateless JWT,” which is the primary reason for the popularity of JWTs and the biggest reason to use a JWT in the first place. Also, I’ve listed all the other articles in the resources section down below that go into the nitty-gritty of JWT.

Before we understand why it’s dangerous, let’s first understand how it works by taking an example use case.

### The use case

Imagine you are using Twitter. You log in, write a tweet, like a tweet, then retweet someone else’s tweet. So you did four actions. For each action, you need to be authenticated and authorized before you can perform that specific action.

Below is what happens in the traditional approach.

## The traditional approach

1. You log in with your username and password:
  1. The server first authenticates the user.
  1. The server then creates a session token, stores that token along with the user’s info in some database. (Note: A session token is a long unidentifiable string—aka opaque string—that looks like this: fsaf12312dfsdf364351312srw12312312dasd1et3423r)
1. The server then sends you a session token to the front-end mobile or web application.
  1. This token is then stored in the cookie or in the local storage of the app.
1. Next, say you wrote and submitted a tweet. Then along with your tweet, your app will also send the session token (through a cookie or a header) so that the server can identify who you are. But the token is just a random string, so how can the server know who you are just from the session token?
1. When the server receives the session token, it won’t know who the user is, so it sends that to the database to retrieve (4a) the actual user’s info (like userId) from that token.
1. If the user exists and is allowed to do that action (i.e send a tweet), the server allows them to do the action.
1. And finally, it tells the front end that the tweet was sent.

![Grey 2](/images/blog/54044a18b5b4cd195def9d4c9ab86336999ce019-1024x687.webp)

## The main problem with the traditional approach

The problem is that step four is slow and needs to be repeated for every single action the user does. So every single API call leads to at least two slow DB calls which can slow down the overall response time.

### There are two ways to solve this problem

1. Somehow eliminate database lookup for users completely (i.e. eliminate step four).
1. Make the extra database lookup much faster so that the additional hop won’t matter.

### Option 1: Eliminate database lookup (step 4)

There are different ways of achieving this.

1. You can store the state in the server’s memory. But this causes issues when you scale since this state is only available on a specific server.
1. Use “sticky sessions”. Here you tell the load balancer to always direct the traffic to a specific server even after you scale up. Again this causes different scaling issues and if the server goes down (scale down), you’ll lose all the state.
1. The third alternative is, JWT. We’ll look into this next.

Now let’s look at the JWT way.

## The JWT way

JWT, especially when used as a session, attempts to solve the problem by completely eliminating the database lookup.

The main idea is to store the user’s info in the session token itself! So instead of some long random string, store the actual user info in the session token itself. And to secure it, have part of the token signed using a secret that’s only known to the server.

So even though the client and the server can see the user info part of the token, the second part, the signed part, can only be verified by the server.

In the picture below, the pink section of the token has the payload (user’s info) and can be seen by both the client or the server.

But the blue part is signed using a secret string, the header, and the payload itself. And so if the client tampers with the payload (say impersonates a different user), the signature will be different and won’t be authenticated.

![Encoded](/images/blog/9b12356282f2209b999d92473c1c88cd86ad173a-1024x560.webp)

Here is how our use case would look like with JWT:

1. You log in with your username and password:
  1. The server authenticates the user by querying the database
  1. The server then creates a JWT session token using the user’s info and the secret (no DB is involved)
1. The server then sends you a JWT token to the front-end application. For future activities, the user can just send the JWT token to identify the user instead of logging in every time.
  1. A JWT token looks like this: <header>.<payload>.<signature>
1. Next, say you wrote and submitted a tweet. When you send it, along with your Tweet’s text, your app will also send the JWT token (through a cookie or a header) so that the server can identify who you are. But how can the server know who you are just from the JWT token? Well, part of the token already has the user information.
1. So when the server receives the JWT token, It uses the secret to validate the signed part and gets the user info from the payload part. Thus eliminating the DB call.
1. If the signature checks out, it allows them to do the action.
1. Finally sends the frontend that the tweet was saved

Going forward for every user action, the server simply verifies the signed part, gets the user info, and lets the user do that action. Thus completely skipping the DB call.

![Grey 1](/images/blog/468034a634b1c6b829eb5464273439db7b1c6c4e-1024x724.webp)

### Token expiration

But there is one additional and important thing to know about the JWT tokens. And that is that it uses an expiration time to expire itself. It’s typically set to 5 minutes to 30 minutes. And because it’s self-contained, you can’t easily revoke/invalidate/update it. This is really where the crux of the problem lies.

## So why is JWT dangerous for user authentication?

The biggest problem with JWT is the token revoke problem. Since it continues to work until it expires, the server has no easy way to revoke it.

Below are some use cases that’d make this dangerous.

1. Logout doesn’t really log you out!

Imagine you logged out from Twitter after tweeting. You’d think that you are logged out of the server, but that’s not the case. Because JWT is self-contained and will continue to work until it expires. This could be 5 minutes or 30 minutes or whatever the duration that’s set as part of the token. So if someone gets access to that token during that time, they can continue to access it until it expires.

1. Blocking users doesn’t immediately block them.

Imagine you are a moderator of Twitter or some online real-time game where real users are using the system. And as a moderator, you want to quickly block someone from abusing the system. You can’t, again for the same reason. Even after you block, the user will continue to have access to the server until the token expires.

1. Could have stale data

Imagine the user is an admin and got demoted to a regular user with fewer permissions. Again this won’t take effect immediately and the user will continue to be an admin until the token expires.

1. JWT’s are often not encrypted so anyone able to perform a man-in-the-middle attack and sniff the JWT now has your authentication credentials. This is made easier because the MITM attack only needs to be completed on the connection between the server and the client.

## Other complexities and considerations

### Library and spec issues:

It’s been found that many libraries that implement JWT have had many security issues over the years and even the spec itself had security issues. Even Auth0 itself, who promotes JWT [got hit with an issue](https://insomniasec.com/blog/auth0-jwt-validation-bypass).

### Length of tokens:

In many complex real-world apps, you may need to store a ton of different information. And storing it in the JWT tokens could exceed the allowed URL length or cookie lengths causing problems. Also, you are now potentially sending a large volume of data on every request.

### The state needs to be maintained anyway (for rate-limiting, IP-whitelisting, etc.)

In many real-world apps, servers have to maintain the user’s IP and track APIs for rate-limiting and IP-whitelisting. So you’ll need to use a blazing fast database anyway. To think somehow your app becomes stateless with JWT is just not realistic.

### Suggested workarounds

One popular solution is to store a list of “revoked tokens” in a database and check it for every call. And if the token is part of that revoked list, then block the user from taking the next action. But then now you are making that extra call to the DB to check if the token is revoked and so deceives the purpose of JWT altogether.

### Bottom line

Although JWT does eliminate the database lookup, it introduces security issues and other complexities while doing so. Security is binary—either it’s secure or it’s not. Thus making it dangerous to use JWT for user sessions.

### Where can I use it?

There are scenarios where you are doing server-to-server (or microservice-to-microservice) communication in the backend and one service could generate a JWT token to send it to a different service for authorization purposes. And other narrow places, such as reset password, where you can send a JWT token as a one-time short-lived token to verify the user’s email.

## If I can’t use JWT, what else can I do?

The solution is to not use JWT at all for session purposes. But instead, do the traditional, but battle-tested way more efficiently.

I.e. make the database lookup so blazing fast (sub-millisecond) that the additional call won’t matter.

### Option 2: Make the look up blazing fast that it won’t matter (a battle-tested solution)

Is there any database out there so blazing fast that it can serve millions of requests in sub-milliseconds?

Of course, there is.** It’s called Redis!** **Thousands of companies that serve billions of users daily use Redis just for this exact purpose!**

And Redis Enterprise is an enhanced version of the Redis OSS that provides 99.999% availability and can serve trillions of requests. It can be used as free software on private clouds or in the cloud on any of the top-3 clouds.

What’s more? Redis Enterprise has now evolved from just being a cache or session store, to a fully-fledged multi-model database with its [module ecosystem](/modules/get-started/) that runs natively with core Redis. For example, you can use [JSON](/json/) ([10x faster](https://oss.redis.com/redisjson/performance/) vs. the market leader) and essentially have a real-time MongoDB-like database, or use the [Search and Query feature](/search/) ([4–100x faster](/blog/search-benchmarking-redisearch-vs-elasticsearch/)) and implement real-time full-text search like Algolia.

If you simply use Redis as a session store and some other Database as a primary database, this is how your architecture would look. One thing to note is that Redis Enterprise provides [four types of caching](/solutions/caching/): Cache-aside (Lazy-loading), Write-Behind (Write-Back), Write-Through, and Read-replica, unlike Redis OSS which only provides one (Cache-aside).

Note that the lightning emoji indicates a blazing fast speed. And the snail emoji indicates slow speed.

![Session JWT](/images/blog/ea31b8c9658ab575d0a5ddf924fa325bd8825185-1024x771.webp)

As mentioned earlier, you can also use Redis as a primary database for your entire data layer. In this scenario, your architecture becomes much simpler and basically, everything becomes blazing fast.

![Db JWT](/images/blog/9b5150c34e3126c404a1399162285ceb99a2df08-1024x771.webp)

## Does it scale?

Of course, companies use Redis not just as a standalone database but as a cluster of geographically distributed databases.

![](/images/blog/62dbcacace673999e363436a5158d2e3975e833f-1015x398.webp)

### [1] References:

1. [Stop using JWT for sessions](http://cryto.net/~joepie91/blog/2016/06/13/stop-using-jwt-for-sessions/)
1. [JWT should not be your default for sessions](https://evertpot.com/jwt-is-a-bad-default/)
1. [Why JWTs Are Bad for Authentication – Randall Degges (Head of Dev Relations, Okta)](https://www.youtube.com/watch?v=GdJ0wFi1Jyo)
1. [Stop using JWT for sessions, part 2: Why your solution doesn’t work](http://cryto.net/~joepie91/blog/2016/06/19/stop-using-jwt-for-sessions-part-2-why-your-solution-doesnt-work/)
1. [Thomas H. Ptacek on Hacker News](https://news.ycombinator.com/item?id=13866883)
1. [My experience with JSON Web Token](https://x-team.com/blog/my-experience-with-json-web-tokens/)
1. [Authentication on the Web (Sessions, Cookies, JWT, localStorage, and more)](https://youtu.be/2PPSXonhIck)
1. [Thomas H. Ptacek’s blog](https://flaked.sockpuppet.org/about/)
