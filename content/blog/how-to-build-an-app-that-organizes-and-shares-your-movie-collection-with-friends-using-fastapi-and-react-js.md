---
title: "How to Build an App that Organizes and Shares Your Movie Collection With Friends Using FastAPI and React.js"
linkTitle: "How to Build an App that Organizes and Shares Your Movie Collection With Friends Using FastAPI and React.js"
url: "/blog/how-to-build-an-app-that-organizes-and-shares-your-movie-collection-with-friends-using-fastapi-and-react-js/"
description: "Search for movies. Organize your collection. And share with your friends. Movify opens the door to exciting movie experiences by creating a social media-like platform where interactions are solely..."
date: 2022-02-21
blogCategories:
- "Uncategorized"
authors:
- "Redis Growth Team"
lastmod: 2025-10-01
hidden: true
mirrored: true
---

*By Redis Growth Team · Published 21 February 2022 · updated 1 October 2025*

![Blog tile image](/images/site-mirror/9b5d82e955f1bff8e5d4c3f96dde3bd0c853de70-772x550.webp)

Search for movies. Organize your collection. And share with your friends. Movify opens the door to exciting movie experiences by creating a social media-like platform where interactions are solely film-based. Here you can view the activity of people in your network and see what movies they’re watching, liking, and sharing.

Redis’ advanced capabilities maximized the user’s experience through its ability to transmit data between components at lightning speed. Achieving this consistently optimized the application’s functionality by keeping users engaged. This allowed commands and social interactions on the platform to be carried out in real-time, mirroring the pace of real-life events.

Let’s take a look at how this application was made in more detail. But before we go any further, we’d like to highlight that we have a great variety of innovative apps for you to discover on the [Redis Launchpad.](https://launchpad.redis.com/)

So if you enjoy this post, make sure to have a browse after!

[Click here to view video](https://www.youtube.com/embed/HOyi2tFYJHo)

## How to build an app that organizes and shares your movie collection with friends

1. What will you build?
1. What will you need?
1. Architecture
1. Getting started
1. Setting up the backend
1. How data is stored
1. How data is accessed
1. How it works
1. Conclusion

## 1. What will you build?

You’ll build a social platform that allows people to connect all around the world based on movie preferences. This involves managing your own movie collections, liking other people’s movie activity as well as creating a fun and easy way to discover movies that are hidden from the mainstream spotlight.

Below we’ll highlight what components you’ll need to bring this application to life as well as walk you through each step of the implementation process.

Ready to get started?

OK, let’s get straight into it.

**What will you need?**

- [**Nginx**](https://www.nginx.com/?m=0&_bt=573371260691&_bk=&_bm=&_bn=g&_bg=134448916920&gclid=Cj0KCQiA3rKQBhCNARIsACUEW_aPV_iM2RUfaB2o4qoo2qpoc__BsS0Xeef_DT3VKWpK3NBRUkvvGrAaAhDPEALw_wcB)**: **Used as an open source software for a whole range of tasks including web serving, reverse proxying, caching load balancing, and much more.
- [**React**](https://reactjs.org/)**: **Used as an open source Javascript library.
- [**Fast API backend**](https://fastapi.tiangolo.com/)**: **Used as a fast, modern, web framework for building APIs with Python 3.6+.
- [**Google App Engine**](https://cloud.google.com/appengine)**: **Used as a cloud computing platform for developing and hosting web applications.
- [**Docker**](https://www.docker.com/)**: **Used as a platform for developers to package applications to containers.
- [**Docker Compose**](https://docs.docker.com/compose/)**: **Used for defining and running multi-container Docker applications.
- [**JSON**](https://oss.redis.com/redisjson/): Used as a Redis module that implements ECMA-404 The JSON Data Interchange Standard as a native data type.
- [**TMDB API**](https://www.themoviedb.org/about): An open community API to programmatically fetch and access database.(735,597 movies, 126,552 tv shows and 3,253,968 images)

## 3. Architecture

- The frontend is served by the app engine which consists of the NGINX and React App
- On the Google Kubernetes Engine, we have both the backend and Redis.
- The Movie Database (**TMDB**) API is an external API that provides a fast, consistent and reliable way to get 3rd-party movie data. TMDB API is used to search and retrieve new movies that are hidden amongst a huge collection of films. The results are cached by the server with an LRU policy. User-generated data is stored in a graph and in JSON clusters. Here, everything can be updated with the JSON.
- All of the requests to the external APIs are proxied through the backend.

## 4. Getting started

Install the below software on your local machine:

- [Git](https://git-scm.com/downloads)
- [Docker](https://docs.docker.com/desktop/mac/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Step 1: Clone the repository

```python
git clone https://github.com/redis-developer/movify

```

### Step 2: Setting up local installation

To launch the app locally, you’ll need a docker-compose. For security reasons, backend/.env is not on this repo. Since we rely on Google Sign-in for authentication, you’ll need to create a [Web client](https://console.cloud.google.com/apis/credentials?pli=1) and register [http://127.0.0.1:8000/api/auth](http://127.0.0.1:8000/api/auth) as an authorized redirect URI.

Next you’ll have to generate a random string for the encryption openssl rand -hex 16. And finally you’ll need to create a TMDB account and [get an API key](https://developers.themoviedb.org/3/getting-started/introduction).

You can now fill the .env file as follows:

```python
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
SECRET_KEY=
TMDB=

```

### Step 3. Defining the microservices

The Docker compose file defines the services that make up your app. In this case, there are 3 services – frontend, backend, and Redis.

```python
version: '3.7'
services:
  nginx:
  image: nginx:1.17
  volumes:
     - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
  ports:
    - 8000:80
  depends_on:
    - backend
    - frontend
redis:
  image: redislabs/redismod:latest
  command: --loadmodule /usr/lib/redis/modules/redisearch.so --loadmodule /usr/lib/redis/modules/redisgraph.so --loadmodule       
           /usr/lib/redis/modules/rejson.so --dir /data
  #   ports:
    #     - 6379:6379
  volumes:
     - ./redis-data:/data
  frontend:
  image: redis21_frontend
  volumes:
     - ./frontend:/app
  backend:
  image: redis21_backend
  entrypoint: uvicorn main:app --host 0.0.0.0 --port 8000 --root-path /api --reload
  depends_on:
    - redis
  environment:
    - HOST=http://127.0.0.1:8000
  volumes:
     - ./backend:/app

```

### Step 4. Execute the script to bring up the application containers:

```python
docker build -t redis21_backend backend/
docker build -t redis21_frontend frontend/
docker-compose up

```

The script run.sh will build the images and start the containers.

## 5. Getting started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

In the project directory, you can run the following commands:

```javascript
npm start
```

This runs the app in the development mode.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits. You’ll also see any lint errors in the console.

```javascript
npm test
```

This command launches the test runner in the interactive watch mode. You can visit the section about [running tests](https://create-react-app.dev/docs/running-tests/) for more information.

```javascript
npm run build
```

Builds the app for production to the build folder. This correctly bundles React in production mode and optimizes the build for the best performance. The build is minified and the filenames include the hashes. At this point, your app will be ready to be deployed!

See the section about [deployment](https://create-react-app.dev/docs/deployment/) for more information.

```javascript
npm run eject
```

**Note: **This is a one-way operation. Once you eject, you can’t go back!

If you aren’t satisfied with the build tool and configuration choices, then you can always eject at any time. This command will remove the single build dependency from your project. Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them.

All of the commands except eject will still work. However, they will point to the copied scripts so you can tweak them. At this point, you’re on your own.

What’s also important to know is that you don’t ever have to use eject. The curated feature set is suitable for small and middle deployments, so you shouldn’t feel obligated to use this feature.

## 6. Setting up the backend

Use the TMDB API to search and retrieve new movies that are hidden amongst a huge collection of films. The results are cached by the server with an LRU policy. User-generated data is stored in a graph and in JSON clusters. Here, everything can be updated with the JSON.

### Data Modeling

There are three types of nodes in this data model:

```javascript
Users
Collection 
Movie
```

There are three types of edges:

```javascript
User - [: FOLLOWS]> User
User - [:HAS]> Collection 
Collection - [:CONTAINS]> Movie {time}
```

To create those classes we made the abstract nodes and upside edges which both make it very simple to work with CRUD operations.

Having these collections will provide you with flexible and efficient querying. The metadata associated with users and collections is stored as JSON.

```javascript
User {id, picture, name}
Collection {id, name, description}
```

### CRUD operations & Cypher for Queries

Below we have abstract classes for CRUD operations. This makes it very simple to create certain types of nodes and get all of the CRUD operations in a single line of code.

However, for queries we prefer to use cypher.

Everything has been timestamped. This was very handy when we wanted to add the friends’ activity view – which was the addition of a simple cypher query on our already timestamped relations.

## 8. How it works

### Step 1: Homepage

The homepage is where a friend’s recent activity is displayed. Here you’ll have a share link to connect with other users on the platform.

### Step 2: Collection

Movies are organized in collections which are then shared with your friends.

### Step 3: Search

Searching for movies is done by using external APIs and responses are cached using an LRU eviction policy.

### Step 4: Movie details

To get additional information about a movie, you may need to make a couple more calls. Here we’re using TMDB API to request information about a movie. Another one is made gather information about the crew and cast members.

## Conclusion: Building a platform where film lovers can discover new movies and connect

One of the most frustrating endeavors any movie fan can relate to is trying to discover captivating movies that are concealed from the spotlight. These hidden gems are hard to locate and often require a lot of time investment to dig them out from underneath the mainstream surface.

But with Movify, fans can navigate more efficiently to their favorite movies by connecting with people with similar POVs and cinematic tastes, enabling users to share. Their activities and see what films others are liking, sharing, and watching.

From a performance perspective, Redis’ powerful caching capabilities guaranteed low latency, allowing users to interact with each other in real-time. This removes the likelihood of any lags from occurring and contaminating the user experience, enabling users to seamlessly interact with other movie fans seamlessly.

If you want to discover more about how this application was made, [watch the YouTube video here](https://www.youtube.com/watch?v=HOyi2tFYJHo). But that’s not all. We also have a whole range of innovative applications for you to check out on the [Redis Launchpad](https://launchpad.redis.com/).

Programmers from all around the world are unlocking their creative potential by using Redis and* you can too.*

Head on over. Be inspired. And have fun with Redis.

## Who created this application?

## Matthias Hasler

![](/images/site-mirror/3fb22807dba8e8a655de96fc8b5dedf29236e341-245x245.webp)

Despite still being a student, Matthias has a whole range of experience in programming, artificial intelligence, machine learning, and much more. To stay up date with all of the projects he’s involved in, [check out his GitHub page here](https://github.com/mhslr/redis21).
