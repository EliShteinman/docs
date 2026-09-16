---
title: "Session Store"
linkTitle: "Session Store"
url: "/solutions/session-store/"
description: "Provide responsive, scalable, and consistent user sessions with Redis Enterprise"
lastmod: 2026-05-21
mirrored: true
---

*updated 21 May 2026*

Provide responsive, scalable, and consistent user sessions with Redis Enterprise

Apps commonly use session stores to track user identity, login credentials, personalization information, recent actions, shopping cart items, and more. The application reads and writes this data only to the session store, so speed and durability are critical. Redis Enterprise provides all the essential requirements for a session store: speed, scale, availability, and cost efficiency.

## How session store works for mobile banking

1. When the user logs into the app, a user session is created.
1. For the duration of the user session, the session data is stored in Redis Enterprise as a key-value pair with the user identifier as the key and session data as the value. While the session is live, the app can consult and update the user information in Redis Enterprise.

## Redis Enterprise solves your challenges

## Why use Redis Enterprise for session storage

- More responsive apps with more responsive user sessions
- Increased scalability to ensure users sessions perform seamlessly even during times of peak demand
- High availability and resilience avoid application outages for the session store that render apps unavailable or unusable

## Learn more

### Developer Resources

[Tutorials](https://redis.io/learn/develop/node/nodecrashcourse/sessionstorage)

### DevOp and Architect Resources

[Watch our Intro to Session Management Tech Talk](https://redis.io/events/intro-to-session-management-with-redis/)

[See a session store in action with the Redis Enterprise for mobile banking solution brief](https://redis.io/resources/redis-enterprise-for-mobile-banking/)

[Read our cache vs session store blog post](/blog/cache-vs-session-store/)

## Related resources

## FAQs

### What is a session store?

A session store is a location where an application stores data about user interactions and current status during a given session, such as a website or a game. Session state is typically stored as a [key-value](https://redis.io/nosql/key-value-databases/) pair, with user identifier as the key and session data as the value.

### What kind of data can be stored in session storage?

Apps commonly store data related to user activity like identity, login credentials, personalization information, recent actions, shopping cart, and more. Session data can vary by application type or industry, for example an e-commerce retailer may hold a customer’s login and authentication details, shopping cart items, browsing history, preferences, and recommendations. A session for a brokerage application may store an investor’s portfolio details, preferred portfolio views, current trades, and open orders. A video game session may keep the player’s current level, score, and control configuration and maintain the game’s state.

### How long does session data last?

Session data is held in Redis Enterprise for the duration of a user session, it can then be volatile (and discarded) or persisted to a primary database.

### When should I use session storage?

Session storage should be used for all customer-facing applications, especially when there is a large volume of users and application responsiveness is important.
