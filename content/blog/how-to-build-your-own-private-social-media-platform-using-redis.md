---
title: "How to Build Your Own Private Social Media Platform Using Redis"
linkTitle: "How to Build Your Own Private Social Media Platform Using Redis"
url: "/blog/how-to-build-your-own-private-social-media-platform-using-redis/"
description: "To many, the social media experience has become a stressful experience. Newsfeeds have become pinboards for sponsored content. Statuses, comments, and any online interactions expose users to..."
date: 2021-11-18
blogCategories:
- "How To and Tutorials"
- "Tech"
authors:
- "Growth Team"
lastmod: 2025-03-27
hidden: true
---

*By Growth Team · Published 18 November 2021 · updated 27 March 2025*

![Blog tile image](/images/blog/c368779b6d594519b7c38ed5d78ba1f2ec118edd-772x520.webp)

To many, the social media experience has become a stressful experience. Newsfeeds have become pinboards for sponsored content. Statuses, comments, and any online interactions expose users to restless keyboard warriors. Some might say that social media has become *anything but* social.

Now as the kingpins of social media continue to dither, this [Launchpad App](https://launchpad.redis.com/?id=project%3Aletus) has tackled this issue head-on by creating its very own social media platform, Letus. The core value of this app is to provide users with a social media platform that promotes more natural and meaningful interactions between friends, family, and work colleagues.

From start to finish, this application relies on the power, speed and flexibility of RedisGraph. Let’s take a look at how this app was created.

But before we dive in, make sure to have a browse around the [Redis Launchpad](https://launchpad.redis.com/) to discover a range of exciting applications for you to get involved in.

[Click here to view video](https://www.youtube.com/embed/MDlebl9tkd0)

1. What will you build?
1. What will you need?
1. Architecture
1. Getting started
1. How it works

## 1. What will you build?

You’ll build a social media platform that shields users from trolls and liberates them from sponsored content. This mobile application will *only* display posts that are made by your friends, family, or whoever you connect with on Letus.

There won’t be any mysterious algorithm that exposes you to unwanted connections and advertisements. Instead, Letus will give you full control over the content you’ll see. Below we’ll go through A-Z of what actions you need to take to bring this application to life, along with the required components.

## 2. What will you need?

[**RedisGraph**](https://redis.io/docs/stack/graph/)**: **used to sparse matrices to represent the adjacency matrix in graphs and linear algebra to query the graph.

[**Google Cloud Platform (GCP)**](https://cloud.google.com/)**: **used as a public cloud vendor that classifies text and analyzes sentiments in this project.

[**Azure Functions**](https://learn.microsoft.com/en-us/azure/azure-functions/functions-develop-local)**: **used as a serverless solution to write less code, maintain infrastructure, and save on costs.

[**Google Identity**](https://developers.google.com/identity/protocols/oauth2)**: **used as a customer identity and access management (CIAM) platform that authenticates users via web-based Oauth 2.0.

[**Expo**](https://expo.dev/): Used by Mobile developers to build apps

[**Firebase**](https://firebase.google.com/): Backend as a Service


## 3. Architecture

![](/images/blog/6530df506c9e5627b6a29a9e2ea9ae27cb8aec26-1024x480.webp)

## 4. Getting started

### Prerequisites:

- NodeJS runtime (version based on [Azure functions support](https://learn.microsoft.com/en-us/azure/azure-functions/functions-versions)
- VS Code Extension
- Azure Functions

#### Step 1: Clone the repository

```python
$ git clone https://github.com/redis-developer/letus

```

#### Step 2. Install the Expo CLI

```python
$ cd LetusApp

```

```python
$ npm install --global expo-cli

```

#### Step 3. Install the Config Plugins

Node modules with config plugins can be added to the project’s Expo config automatically by using the expo install command

```python
$ npm install

```

```python
$ expo install

```

#### For Local Development environment:

For local development, RedisGraph can be run using the redismod Docker container

```python
$ docker run -d -p 6379:6379 redislabs/redismod

```

You can run just the Expo Go App locally to use, and develop, the react native app. By accessing existing (free) firebase auth and existing (free) Azure functions deployed for DEV only.

- Copy the contents of env.dev.example into your .env file
- Launch the app via expo start
- Register a new user via the mobile simulator and you’re in!

| Developer tools running on http://localhost:19002Opening developer tools in the browser…Starting Metro BundlerMetro waiting on exp://192.168.1.9:19000 |
|---|

#### For Production Environment:

#### Step 4. Setting up Environmental variable

```python
Create a .env.local file to store your local configuration
Set the value of LETUS_API_URL to the location of your API (can use .env if local functions)
Set the value of GOOGLE_WEB_CLIENT_ID to use a Web OAUTH credential created in your Google Identity account.
Set value of firebase config in the .env or .env.local file
FIREBASE_API_KEY=
FIREBASE_AUTH_DOMAIN=
FIREBASE_PROJECT_ID=
FIREBASE_STORAGE_BUCKET=
FIREBASE_MEASSGE_SENDER_ID=
FIREBASE_APP_ID=

```

#### Step 5. Start the development server

```python
$ expo start

```

Press i to launch an iOS simulator or a for Android. (note: Android simulator requires Android Studio and sdk setup)

#### Step 6: Setting up Letus Functions

This project uses [Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/functions-develop-local) which can be accessed directly in your local development. If you wish to publish these functions to the cloud, you must create your own [Azure account](https://azure.microsoft.com/en-us/free/). *Tip: There is a very useful *[*VS Code Extension*](https://learn.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code)* to help manage your azure projects and functions.*

- Azure functions can be run locally. The recommended option is to use [VS Code Extension](https://learn.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code) and then use f5 to launch in debug mode
- Configure the following environment variables (either in local.settings.json or in Azure)
  - The host of the RedisGraph database:

```python
REDIS_HOST

```

- The port used by the RedisGraph database:

```python
REDIS_PORT

```

- Password for the default Redis user:

```python
REDIS_PASS

```

- The name of the graph to use:

```python
REDIS_GRAPH

```

- Google Cloud Platform API Key used for Language processing (AnalyzeSentiment and ClassifyText)

```python
GCP_API_KEY

```

- Add your serviceAccount.json file to LetusFunctions/shared to configure the API’s firebase-admin

#### Step 7: Setting up Authentication

- Letus uses Firebase for authentication in both the Expo app and the Azure functions
- [Create a project for Firebase Auth (web)](https://firebase.google.com/docs/auth/web/start)

#### Step 8: Setting up RedisGraph

Click [/try-free/ ](/try-free/)and setup Redis Enterprise cloud database with RedisGraph as shown below:

![](/images/blog/1cfba29eb482d0e3e8942c45d197439ad825399f-1600x1168.webp)

![Redis Insight](/images/blog/c19f556188de448ce42be280dd0f4ce7dfe22c70-1600x776.webp)

- **GetPosts** – The core of Letus. Uses cypher to traverse the current user’s network and return the relevant, most recent posts:
MATCH (me:Person {userid: $userid})

```python
MATCH (me:Person {userid: $userid}) 
  OPTIONAL MATCH (me)-[:ignores]->(ign:IgnoreSetting) 
  WITH me, ign  
  MATCH (poster:Person)-[:posted]->(post:Post) 
  WHERE (poster = me OR (poster)-[:friended]-(me)) 
  AND (NOT (post)-[:inCategory]->(:Category {name:ign.category}) AND NOT (post)<-[:posted]-(:Person {userid:ign.poster})) 
  WITH post, poster, me 
  OPTIONAL MATCH (post)-[:hasComment]->(comment:Comment)<-[:commented]-(commenter:Person) 
  WHERE commenter = me OR (commenter)-[:friended]-(me) 
  WITH me, post, poster, collect(comment) as comments, collect(commenter) as commenters 
  ORDER BY post.created DESC 
  SKIP $skip
 LIMIT $limit
  RETURN post, poster, comments, commenters

```

- **CreatePost** – Creates a new post with additional information from NLP processing.

```python
MATCH (me:Person {userid:$userid}) ${categories
.map(
(cat, index) =>
    'MERGE (cat' + index + ':Category {name: $cat' + index + '})'
)
.join(
' '
)}  
MERGE (sentiment:Sentiment {name: $sentiment}) 
CREATE (me)-[:posted]->(post:Post {text:$text,created:$now}) 
MERGE (post)-[:hasSentiment]->(sentiment) ${categories
.map((cat, index) => 'MERGE (post)-[:inCategory]->(cat' + index + ')')
.join(' ')} 
RETURN post

```

- **AddComment** – Add your comment to a connection’s Post.


```python
MATCH (me:Person), (post:Post) 
WHERE me.userid = $userid 
AND ID(post) = $onPost 
CREATE (me)-[:commented]->(comment:Comment {text:$text,created:$now}) 
CREATE (post)-[:hasComment]->(comment) 
RETURN post

```

- **AddFriend** – Add a new connection from your direction.

**Note:** single-direction :friended relationships determine pending friend requests

```python
MATCH (me:Person { userid: $userid }) 
MATCH (them:Person { userid: $themid })
MERGE (me)-[:friended]->(them)
RETURN me, them

```

- **GetFriendRequests** – Return the list of Person nodes who have :friended you but are not friended by you.


```python
MATCH (me:Person {userid: $userid}) 
WITH me 
MATCH (them:Person)-[:friended]->(me) 
WHERE NOT (me)-[:friended]->(them) 
RETURN them

```

- **AddIgnoreSetting** – Add a new IgnoreSetting to a User


```python
MATCH (me:Person { userid: $userid }) 
MERGE (me)-[:ignores]->(ignore:IgnoreSetting {poster:$themid, category: $category, sentiment: $sentiment})
RETURN me, ignore

```

- **FindFriends** – Search for unfriended People by name


```python
MATCH (them:Person) 
MATCH (me:Person {userid:$userid}) 
WHERE NOT them.userid = $userid 
AND them.name STARTS WITH $name 
AND NOT (me)-[:friended]->(them) 
RETURN them

```

**NLP Commands**

Using the free tier of [GCP Natural Language](https://cloud.google.com/natural-language), we apply both sentiment analysis and text classification to all posts made in the system.

- **AnalyzeSentiment**
const sslCreds = getApiKeyCredentials();

```python
const sslCreds = getApiKeyCredentials();
const client = new language.LanguageServiceClient({ sslCreds });
const document = {
content: text,
 type: 'PLAIN_TEXT',
};
const [result] = await client.analyzeSentiment({ document: document });
sentiment = mapSentiment(result.documentSentiment.score || 0);

```

- **ClassifyText** – Returns a list of matching [NLP Categories](https://cloud.google.com/natural-language/docs/categories)
let content = text;

```python
// GCP requires 20 words
// we pad with prepositions if between 10-19 words for max coverage
if (len < 20) {
  content = [...content.split(' '), ...preps.slice(0, 20 - len)].join(' ');
}
const sslCreds = getApiKeyCredentials();
const client = new language.LanguageServiceClient({ sslCreds });
 
const document = {
  content,
  type: 'PLAIN_TEXT',
};
const [result] = await client.classifyText({ document: document });
categories = result.categories || [];

```

## Conclusion: Removing trolls and advertisements from social media

As social media continues to intertwine itself into everyday life, trolling remains as pervasive as ever. Facebook, Twitter, Instagram, and even Linkedin have become hunting grounds for restless keyboard warriors.

Then you have the endless bombardment of sponsored content, whose interests are prioritized ahead of the user’s. But by using Redis, this marketplace app was able to create a social media platform for mobile users that removes both of these hazards.

The power and speed of RedisGraph was crucial to building Letus since it allowed the application to query data with maximum efficiency. From what began as just a simple idea, Redis was able to bring this application to life… *but that’s not all.*

Every day people are tapping into the wonders of Redis to create exciting applications that’s having an impact on everyday lives. How can you use Redis to help change society for the better?

For more inspiration, you can visit the [Redis Launchpad](https://launchpad.redis.com/) where you’ll find a whole range of innovative apps. Likewise, you can also discover more about how this app was made by [clicking here](https://www.youtube.com/watch?v=FmgdHGFYj3U).

![](/images/blog/4286535b4f0ad548b626a7e3bc36792d2aa0c568-1600x593.webp)

## Who built this application?

**Matt Pileggi**

Matt has over 20 years of experience in web development and is now the principal engineer for Games24x7.

Make sure to keep to date with all of Matt’s projects on Github by [checking out his page here](https://github.com/withjam).
