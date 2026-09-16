---
title: "How to Build a Real-Time Bidding Platform using NodeJS, AWS Lambda and Redis"
linkTitle: "How to Build a Real-Time Bidding Platform using NodeJS, AWS Lambda and Redis"
url: "/tutorials/create/aws/bidding-on-aws/"
description: "Digital technology has propelled us forward to an exciting new era and has transformed almost every aspect of life. We're more interconnected than ever as communication has become instant. Working..."
group: "For developers"
aliases:
- "/tutorials/create-aws-bidding-on-aws/"
date: 2026-02-25
lastmod: 2026-02-25
hidden: true
mirrored: true
---

*Published 25 February 2026*

> **TL;DR:**
>
> Build a real-time bidding platform using Node.js, AWS Lambda, and Redis. Redis Hashes store auction and bid data, while Socket.IO delivers live bid updates to all connected clients. AWS Cognito handles authentication and AWS Lambda provides serverless scalability for high-concurrency auctions.

Digital technology has propelled us forward to an exciting new era and has transformed almost every aspect of life. We're more interconnected than ever as communication has become instant. Working from home has now become the norm, helping us pivot to a new way of working during the pandemic. And our ability to reduce carbon emissions by attending work-related events online has meant that we've taken greater strides to combat global warming. Continuing this trend is [Shamshir Anees and his team](https://github.com/shamshiranees), who have created an application that can host digital auctions. By using Redis, data transmission between components was carried out with maximum efficiency, providing users with real-time bidding updates on the dashboard.

Let's take a look at how this was achieved.

### What you'll learn

- How to integrate Redis Cloud with AWS Lambda for serverless auction processing
- How to use Redis Hashes to store and retrieve auction, bidding, and user data
- How to deliver real-time bid updates to clients using Socket.IO
- How to implement dynamic closing logic that extends auction end times when late bids arrive
- How to authenticate users with Amazon Cognito and notify them via Amazon SNS/SES

### What will you build?

You'll build an application that will allow users to attend and take part in digital auctions. The application will allow users to create an account, put in bids, and even set up their own auction. Below we'll uncover the required components, their functionality, and how to deploy them within this architecture.

Ready to get started? Ok, let's dive straight in.

### Prerequisites

- [Node.js](https://nodejs.org/en/) (v14 or later) and [NPM](https://www.npmjs.com/)
- A free [Redis Cloud](https://redis.io/try-free/) account
- An [AWS account](https://aws.amazon.com/) with access to Lambda, Cognito, SNS, and SES
- Basic familiarity with JavaScript and REST APIs

### What will you need?

- NodeJS: used as an open-source, cross-platform, backend JavaScript runtime environment that executes Javascript code outside a web browser.
- [Amazon Cognito](https://aws.amazon.com/cognito/): used to securely manage and synchronize app data for users on mobile.
- [Redis Cloud](https://redis.io/try-free/): used as a real-time database, cache, and message broker.
- [Socket.IO](https://socket.io/): used as a library that provides real-time, bi-directional, and event-based communication between the browser and the server.
- [AWS Lambda](https://aws.amazon.com/lambda/): used as a serverless compute service that runs your code in response events and manages the underlying compute service automatically for you.
- [Amazon SNS/Amazon SES](https://aws.amazon.com/sns/): a fully managed messaging service for both application-to-application (A2A) and application-to-person (A2P) communication.

### Architecture

![Digital auction platform architecture on AWS with Redis Cloud, Cognito, and Lambda](/images/site-mirror/46c7021967130cdb5caebbc317be702c6028797d-1047x485.webp)

### How does real-time bidding work with Redis?

#### All auctions

NodeJS connects to the Redis Cloud database.

The frontend then communicates with the NodeJS backend through API calls.

`GET : /api/auctions` fetches all the keys from Auctions Hash.

NodeJS uses the Redis module to work with Redis Cloud. The Redis client is then created using the Redis credentials and hmget(). This is the equivalent of the HMSET command that's used to push data to the Redis database.

#### Each auction

`GET : /api/auctions/{auctionId}` fetches each auction item by id.

NodeJS uses the Redis module to work with Redis Cloud. The Redis client is then created using the Redis credentials and hmget(). This is the equivalent of the HMSET command that's used to push data to the Redis database.

All bidding data of an auction item

`GET : /api/bidding/{auctionId}`

NodeJS uses the Redis module to work with Redis Cloud. The Redis client is then created using the Redis credentials and hmget(). This is the equivalent of the HMSET command that's used to push data to the Redis database.

#### How are user profiles and settings stored?

`GET : /api/settings`

NodeJS uses the Redis module to work with Redis Cloud. The Redis client is then created using the Redis credentials and hmget(). This is the equivalent of the HMSET command that's used to push data to the Redis database.

#### User info

`GET : /api/users/{email}`

NodeJS uses the Redis module to work with Redis Cloud. The Redis client is then created using the Redis credentials and hmget(). This is the equivalent of the HMSET command that's used to push data to the Redis database.

### Getting started

### Step 1. Sign up for a Free Redis Cloud Account

[Sign up for a free Redis Cloud account.](https://redis.io/try-free/)
Choose AWS as a Cloud vendor while creating your new subscription. At the end of the database creation process, you will get a Redis Cloud database endpoint and password. You can save it for later use

### Step 2: Clone the backend GitHub repository

```bash
https://github.com/redis-developer/NR-digital-auction-backend
```

### Step 3. Install the package dependencies

The 'npm install' is a npm cli-command that does the predefined thing i.e install dependencies specified inside package.json

```bash
npm install
```

### Step 4. Setting up environment variables

```bash
export REDIS_END_POINT=XXXX
export REDIS_PASSWORD=XXX
export REDIS_PORT=XXX
```

### Step 5. Building the application

```bash
npm run build
```

### Step 6. Starting the application

```bash
npm start
```

### Step 7. Cloning the Frontend GITHUB repository

```bash
git clone https://github.com/redis-developer/NR-digital-auction-frontend
```

### Step 8. Building the application

```bash
npm run build
```

### Step 9. Starting the application

```bash
npm start
```

### Step 10. Accessing the application

![Digital auction application homepage showing featured items](/images/site-mirror/b45f6bba8a4bd35018aa0f908e836965e1d76964-1047x559.webp)

### Step 11. Signing up to the application

![User sign-up page for the digital auction application](/images/site-mirror/566ef568aae95cf7b0ba51d6777d7a27277b85c8-1047x637.webp)

### Step 12. Sign-in

![User sign-in page for the digital auction application](/images/site-mirror/62a4f63f036409c1f7c533a443689855532b04d7-1047x620.webp)

### Step 13. Accessing the dashboard

![Auction dashboard displaying active auction items](/images/site-mirror/e86abde44e98d15061a81ce4eb65092bbb6fba9a-1047x576.webp)

### Step 14. Listing the auction item

![Form for listing a new item for auction](/images/site-mirror/61cf1dcc66df589e7e826d3c93b683e82c02319c-1047x574.webp)

### Step 15. Accessing the bidding page

![Bidding page for an item showing current high bid and history](/images/site-mirror/f3e33a9af363698e8ee55120825295d65a25ca64-1047x574.webp)

### How is auction data stored in Redis?

The [Redis Cloud](https://redis.io/try-free/) database is what you'll use to install the data.

### Auctions

- Type - Redis Hash.
- Used for storing auctions data.
- UUID generated from the backend (NodeJS) serves as the key
- JSON data which represents the Auction object and includes the following keys
    - auctionId
    - auctionItemName
    - description
    - lotNo
    - quantity
    - buyersPremium
    - itemUnit
    - minBidAmount
    - bidIncrement
    - startDateTime
    - endDateTime
    - images
    - currentBid
- NodeJS connects to the Redis Cloud database. The Frontend communicates with the NodeJS backend through API calls.
- POST : /api/auctions.
- The request body has JSON data to be inserted into the database.
- NodeJS uses the Redis module to work with Redis Cloud. The Redis client is created. using the Redis credentials and hmset(). This is the equivalent of the HMSET command that's used to push data to the Redis database.

### Biddings

- Type - Redis Hash
- Used for storing the bids placed on each auction item
- NodeJS connects to the Redis Cloud database. The Frontend communicates with the NodeJS backend through API calls.
- POST : `/api/bidding`
- The request body has JSON data to be inserted into the database.
- AuctionId from request body serves as the key
- JSON data which includes keys:
    - currentBid
    - currentBidTime
    - currentBidEndTime, and
    - biddings array (id, auctionId, userId, username, bidAmount, bidTime)

- The bidding array has all of the bids placed for a particular auction item.
- Based on the current BidEndTime and BidTime, the auction end date is extended based on the Dynamic closing concept.
- Current dynamic closing logic - If a new bid is placed within the last 5 minutes of the auction end time, the end time is extended by 1 hour.
- This will be configurable in the SaaS solution.
- NodeJS uses the Redis module to work with Redis Cloud. The Redis client is created using the Redis credentials and hmset(). This is the equivalent of the HMSET command that's used to push data to the Redis database.

### Profile Settings

- Type - string
- JSON data which includes keys - serves as a value
- NodeJS connects to the Redis Cloud database. The frontend communicates with the NodeJS backend through API calls.
- POST : `/api/settings`
- The request body has JSON data to be inserted into the database.
- NodeJS uses the Redis module to work with Redis Cloud. The Redis client is created using the Redis credentials and hmset(). This is the equivalent of the HMSET command that's used to push data to the Redis database.

### Users

- Type - Redis Hash
- Used for storing user details
- NodeJS connects to the Redis Cloud database. The Frontend communicates with the NodeJS backend through API calls.
- POST : `/api/users`
- The request body has JSON data to be inserted into the database
- The email id serves as the key
- The JSON data which includes keys - serves as a value
- NodeJS uses the Redis module to work with Redis Cloud. The Redis client is created using the Redis credentials and hmset(). This is the equivalent of the HMSET command that's used to push data to the Redis database.

### How do you navigate the auction application?

### Creating an account

When you go onto the Digital Auction's homepage, you'll come across a range of items that are to be auctioned (see below). Click on the 'Welcome' button to create an account.

![Auction dashboard displaying active auction items](/images/site-mirror/e86abde44e98d15061a81ce4eb65092bbb6fba9a-1047x576.webp)

You'll then be taken to the sign-up page. Enter your details and click 'sign-up.' Once you've completed the sign-up form, you'll receive a confirmation email to activate your account.

### Placing a bid

Go to the homepage to have access to view all of the items and their auction details. All of the data here is being populated by Redis and Redis Cloud. Scroll through the page and click on the item that you want to place a bid for.

When you click on an item, you'll see the details for the bidding process at the top of the page. You'll also have the option to set a reminder by receiving an email of whenever the bidding process of this item begins.

On the right-hand side of the image, you'll see the highest bid that's been placed for this item. Below is a list of previous bids made by different users which are updated in real-time.

Click on the 'Place Bid' button to make a bid.

To access the meta-data information or view more images of the item, simply scroll down the page (see below).

![Bidding page for an item showing current high bid and history](/images/site-mirror/f3e33a9af363698e8ee55120825295d65a25ca64-1047x574.webp)

### Viewing your Bidding History

Click on 'My biddings' at the top of the navigation bar to view your bidding history (see below).

![Viewing personal bidding history in the application](/images/site-mirror/bddb645b0eb9b76fb2d0749d00bc164f7246438b-1047x597.webp)

### Viewing upcoming auctions

Click on 'Auctions' at the top of the navigation bar to view all upcoming auctions.

![Viewing all upcoming auctions in the navigation bar](/images/site-mirror/7e2ef04df5db20fe3207c442fc844101e9a5a54d-1047x597.webp)

### Conclusion: Leveraging Redis and AWS to Empower Auctioneers with Real-time Data

Digital technology has had a ripple effect across all aspects of modern life. The ability to complete important tasks online instead of in-person has revolutionized the way we live, helping us to reduce carbon emissions, save time from traveling and have instant access to reams worth of data that we never had before.

However, the success of such events hinges on a database's ability to transmit data in real-time. Any blips in transmission would create a disconnect between users and the auction, impeding auctioneers' reactions to bids. This would only result in frustration, disengagement, and a complete divorce of users from the application.

But thanks to Redis, the components that made up the architecture system became vastly more interconnected so data was able to be sent, processed, and received in real-time. Achieving this paves the way for a smooth bidding process where users can interact with events in real-time without interruptions, ultimately enhancing the functionality of the app.

[NR-Digital-Auction](https://github.com/redis-developer/NR-digital-auction-backend) is a fantastic example of how innovations can be brought to life by using Redis. Everyday programmers are experimenting with Redis to build applications that are impacting everyday life from around the world and you can too!

So what can you build with Redis? If you're ready to get started building, quickly spin up a free database [Redis Cloud](https://redis.io/try-free/).

### Next steps

- **[Build a Real-Time Analytics Dashboard on AWS](/tutorials/create/aws/analytics-using-aws/):** Pair your bidding platform with a Redis-powered analytics dashboard to visualize auction performance, bid velocity, and user engagement in real time.
- **[Build a Real-Time Chat App on AWS](/tutorials/create/aws/chatapp/):** Add live chat to your auction platform so bidders can communicate during events, using Redis Pub/Sub for instant message delivery.
- **[Get started with Redis Cloud](https://redis.io/try-free/):** Spin up a free Redis Cloud database to start building your own real-time applications.
