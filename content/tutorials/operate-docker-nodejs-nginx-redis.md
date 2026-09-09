---
title: "How to build and run a Node.js application using Nginx, Docker and Redis"
linkTitle: "How to build and run a Node.js application using Nginx, Docker and Redis"
url: "/tutorials/operate/docker/nodejs-nginx-redis/"
description: "This guide walks you through building a multi-container Docker application with Node.js, Nginx as a reverse proxy, and Redis for data storage. You'll use Docker Compose to orchestrate a visitor-..."
aliases:
- "/tutorials/operate-docker-nodejs-nginx-redis/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> Define four services in a `docker-compose.yml` — Redis, two Node.js web servers, and an Nginx load balancer — then run `docker compose up -d` to start everything. Nginx distributes traffic across the Node.js containers, and Redis tracks the total visit count.

This guide walks you through building a multi-container Docker application with [Node.js](https://nodejs.dev/), Nginx as a reverse proxy, and Redis for data storage. You'll use Docker Compose to orchestrate a visitor-counter app that load-balances requests across two Node.js instances while persisting hit counts in Redis.

## What you'll learn

- How to define a multi-container Docker application with Docker Compose
- How to configure Nginx as a reverse proxy and load balancer for Node.js
- How to connect a Node.js application to Redis inside a Docker network
- How to monitor Redis commands in real time

![Architecture diagram showing Nginx load balancing traffic between two Node.js containers that connect to a Redis container](/images/site-mirror/d3e8083029bdb43a2ebb7a974cef1bbf8d590ffb-1890x1422.webp)

## What do you need?

- **[Node.js](https://nodejs.dev/)**: An open-source, cross-platform JavaScript runtime environment that executes JavaScript outside a web browser.
- **[Nginx](https://nginx.org/)**: An open-source web server used for reverse proxying, load balancing, and caching.
- **[Docker](https://www.docker.com/)**: A containerization platform for developing, shipping, and running applications.
- **[Docker Compose](https://docs.docker.com/compose/)**: A tool for defining and running multi-container Docker applications.

## What does the project structure look like?

```bash
.
├── docker-compose.yml
├── redis
├── nginx
│   ├── Dockerfile
│   └── nginx.conf
├── web1
│   ├── Dockerfile
│   ├── package.json
│   └── server.js
└── web2
    ├── Dockerfile
    ├── package.json
    └── server.js
```

## Prerequisites

Install [Docker Desktop](https://docs.docker.com/desktop/) on your local machine. Docker Desktop is available for [Mac](https://docs.docker.com/desktop/install/mac-install/), [Windows](https://docs.docker.com/desktop/install/windows-install/), and [Linux](https://docs.docker.com/desktop/install/linux/).

![Screenshot of Docker Desktop running with containers listed](/images/site-mirror/e4a74cccc1afc75aeec958183051657b9b394ccf-1514x1016.webp)

> **INFO**
>
> Docker Desktop comes with Docker Compose installed by default, so you don't need to install it separately.

If you're new to running Redis in Docker, see [How to Deploy and Run Redis in a Docker container](/tutorials/create/docker/) first.

## How do you define the Docker Compose file?

Create a file named `docker-compose.yml` with the following content:

```yaml
version: '3.9'
services:
    redis:
        image: 'redis:alpine'
        ports:
            - '6379:6379'
    web1:
        restart: on-failure
        build: ./web
        hostname: web1
        ports:
            - '81:5000'
    web2:
        restart: on-failure
        build: ./web
        hostname: web2
        ports:
            - '82:5000'
    nginx:
        build: ./nginx
        ports:
            - '80:80'
        depends_on:
            - web1
            - web2
```

The compose file defines an application with four services: `redis`, `web1`, `web2`, and `nginx`. When deploying the application, Docker Compose maps port 80 of the Nginx container to port 80 of the host. The two Node.js web servers run on ports 81 and 82, and Redis runs on its default port 6379.

> **INFO**
>
> By default, Redis runs on port 6379. Make sure you don't run another instance of Redis on your system or that port 6379 on the host is not being used by another container, otherwise the port should be changed.

## How do you configure Nginx as a reverse proxy?

Create an `nginx` directory and add the following files.

### nginx/nginx.conf

```nginx
upstream loadbalancer {
  server web1:5000;
  server web2:5000;
}

server {
  listen 80;
  server_name localhost;
  location / {
    proxy_pass http://loadbalancer;
  }
}
```

This configuration tells Nginx to distribute incoming requests between `web1` and `web2` using round-robin load balancing. Both Node.js servers listen on port 5000 inside their containers, and Docker networking resolves the hostnames automatically.

### nginx/Dockerfile

```dockerfile
FROM nginx:1.21.6
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
```

## How do you build the Node.js web server?

Create a `web` directory and add the following files.

### web/Dockerfile

```dockerfile
FROM node:14.17.3-alpine3.14

WORKDIR /usr/src/app

COPY ./package.json ./
RUN npm install
COPY ./server.js ./

CMD ["npm","start"]
```

### web/package.json

```json
{
    "name": "web",
    "version": "1.0.0",
    "description": "Running Node.js and Express.js on Docker",
    "main": "server.js",
    "scripts": {
        "start": "node server.js"
    },
    "dependencies": {
        "express": "^4.17.2",
        "redis": "3.1.2"
    },
    "author": "",
    "license": "MIT"
}
```

### web/server.js

```javascript
const express = require('express');
const redis = require('redis');
const app = express();
const redisClient = redis.createClient({
    host: 'redis',
    port: 6379,
});

app.get('/', function (req, res) {
    redisClient.get('numVisits', function (err, numVisits) {
        numVisitsToDisplay = parseInt(numVisits) + 1;
        if (isNaN(numVisitsToDisplay)) {
            numVisitsToDisplay = 1;
        }
        res.send('Number of visits is: ' + numVisitsToDisplay);
        numVisits++;
        redisClient.set('numVisits', numVisits);
    });
});

app.listen(5000, function () {
    console.log('Web application is listening on port 5000');
});
```

The Express app connects to the `redis` service by hostname — Docker Compose automatically sets up DNS resolution between containers on the same network. Each request increments a visit counter stored in Redis.

## How do you deploy the multi-container application?

Run Docker Compose to build and start all four containers:

```bash
docker compose up -d
```

```bash
Creating nginx-nodejs-redis_redis_1 ... done
Creating nginx-nodejs-redis_web1_1  ... done
Creating nginx-nodejs-redis_web2_1  ... done
Creating nginx-nodejs-redis_nginx_1 ... done
```

### Expected result

List the running containers to verify the deployment:

```bash
docker compose ps
           Name                        Command              State           Ports
------------------------------------------------------------------------------------------
nginx-nodejs-redis_nginx_1   /docker-entrypoint.sh ngin     Up      0.0.0.0:80->80/tcp
                             ...
nginx-nodejs-redis_redis_1   docker-entrypoint.sh redis     Up      0.0.0.0:6379->6379/tcp
                             ...
nginx-nodejs-redis_web1_1    docker-entrypoint.sh npm       Up      0.0.0.0:81->5000/tcp
                             start
nginx-nodejs-redis_web2_1    docker-entrypoint.sh npm       Up      0.0.0.0:82->5000/tcp
                             start
```

## How do you test the application?

After the application starts, navigate to `http://localhost` in your web browser or run:

```bash
curl localhost:80
web1: Total number of visits is: 1
```

```bash
curl localhost:80
web1: Total number of visits is: 2
```

```bash
curl localhost:80
web2: Total number of visits is: 3
```

```bash
curl localhost:80
web2: Total number of visits is: 4
```

Notice how Nginx alternates between `web1` and `web2`, demonstrating the round-robin load balancing. The visit count increments across both servers because they share the same Redis instance.

## How do you monitor Redis keys?

Use the Redis CLI `MONITOR` command to watch commands in real time. Connect to the Redis container:

```bash
redis-cli
127.0.0.1:6379> monitor
OK
1646485507.290868 [0 172.24.0.2:34330] "get" "numVisits"
1646485507.309070 [0 172.24.0.2:34330] "set" "numVisits" "5"
1646485509.228084 [0 172.24.0.2:34330] "get" "numVisits"
1646485509.241762 [0 172.24.0.2:34330] "set" "numVisits" "6"
1646485509.619369 [0 172.24.0.4:52082] "get" "numVisits"
1646485509.629739 [0 172.24.0.4:52082] "set" "numVisits" "7"
1646485509.990926 [0 172.24.0.2:34330] "get" "numVisits"
1646485509.999947 [0 172.24.0.2:34330] "set" "numVisits" "8"
1646485510.270934 [0 172.24.0.4:52082] "get" "numVisits"
1646485510.286785 [0 172.24.0.4:52082] "set" "numVisits" "9"
1646485510.469613 [0 172.24.0.2:34330] "get" "numVisits"
1646485510.480849 [0 172.24.0.2:34330] "set" "numVisits" "10"
1646485510.622615 [0 172.24.0.4:52082] "get" "numVisits"
1646485510.632720 [0 172.24.0.4:52082] "set" "numVisits" "11"
```

The alternating IP addresses in the `MONITOR` output confirm that requests are being distributed across the two Node.js containers.

## Next steps

- [How to Deploy and Run Redis in a Docker container](/tutorials/create/docker/) — learn the fundamentals of running Redis in Docker
- [Getting started with Node.js and Redis](/tutorials/develop/node/gettingstarted/) — connect to Redis from a Node.js application using `node-redis`
- [Docker orchestration with Redis](/tutorials/operate/orchestration/docker/) — manage Redis containers at scale
- [Complete source code for this tutorial](https://github.com/ajeetraina/awesome-compose/tree/master/nginx-nodejs-redis) — clone the repo and try it yourself
