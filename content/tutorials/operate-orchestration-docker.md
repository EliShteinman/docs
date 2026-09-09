---
title: "How to Deploy and Run Redis in a Docker Container"
linkTitle: "How to Deploy and Run Redis in a Docker Container"
url: "/tutorials/operate/orchestration/docker/"
description: "Before running a Redis container, pull the latest official Redis image from Docker Hub:"
aliases:
- "/tutorials/operate-orchestration-docker/"
date: 2026-02-25
lastmod: 2026-02-25
hidden: true
---

*Published 25 February 2026*

> **TL;DR:**
>
> Pull the official Redis image with `docker pull redis:latest`, then run it with `docker run -d --name my-redis -p 6379:6379 redis:latest`. Add `-v /path/to/data:/data` and `-e REDIS_ARGS="--appendonly yes"` for persistent storage.

## What you'll learn

- How to pull and run the Redis Docker image
- How to connect to Redis inside a container using `redis-cli`
- How to persist data with Docker volumes
- How to set a Redis password in Docker
- How to run Redis with Docker Compose

## Prerequisites

- [Docker](https://docs.docker.com/engine/install/) installed on your system
- Basic familiarity with the command line

## How do I pull the Redis Docker image?

Before running a Redis container, pull the latest official Redis image from Docker Hub:

```bash
docker pull redis:latest
```

You can verify the image was downloaded by listing your local Docker images:

```bash
docker images redis
```

## How do I run Redis in a Docker container?

Execute the following command to run the Redis container in the background:

```bash
docker run -d --name my-redis -p 6379:6379 redis:latest
```

- `-d` runs the container in detached (background) mode
- `--name my-redis` assigns a name to the container
- `-p 6379:6379` maps the container's Redis port to your host machine
- `redis:latest` specifies the Docker image

Verify the container is running:

```bash
docker ps
```

You should see output similar to:

```bash
CONTAINER ID   IMAGE          COMMAND                  STATUS         PORTS                    NAMES
885568fdf77e   redis:latest   "docker-entrypoint.s…"   Up 3 minutes   0.0.0.0:6379->6379/tcp   my-redis
```

## How do I connect to Redis inside a Docker container?

Use `docker exec` to open an interactive shell inside the running container, then launch `redis-cli`:

```bash
docker exec -it my-redis redis-cli
```

Test the connection:

```bash
127.0.0.1:6379> PING
PONG
```

You can also run Redis commands directly without entering the interactive shell:

```bash
docker exec my-redis redis-cli SET mykey "Hello from Docker"
docker exec my-redis redis-cli GET mykey
```

## How do I persist data with Docker volumes?

By default, data stored in a Redis container is lost when the container is removed. To persist data, mount a Docker volume and enable append-only file (AOF) persistence:

```bash
docker run -d \
  --name my-redis \
  -p 6379:6379 \
  -v redis-data:/data \
  -e REDIS_ARGS="--appendonly yes" \
  redis:latest
```

- `-v redis-data:/data` creates a named Docker volume mapped to Redis's data directory
- `--appendonly yes` enables AOF persistence so every write operation is logged to disk

You can also use a bind mount to store data in a specific host directory:

```bash
docker run -d \
  --name my-redis \
  -p 6379:6379 \
  -v /path/to/your/data:/data \
  -e REDIS_ARGS="--appendonly yes" \
  redis:latest
```

## How do I set a Redis password in Docker?

To secure your Redis container with a password, pass `--requirepass` via the `REDIS_ARGS` environment variable:

```bash
docker run -d \
  --name my-redis \
  -p 6379:6379 \
  -v redis-data:/data \
  -e REDIS_ARGS="--requirepass your_password_here --appendonly yes" \
  redis:latest
```

Connect with authentication:

```bash
docker exec -it my-redis redis-cli -a your_password_here
```

## How do I run Redis with Docker Compose?

For more complex setups, Docker Compose provides a declarative way to configure and run Redis. Create a `docker-compose.yml` file:

```yaml
services:
    redis:
        image: redis:latest
        container_name: my-redis
        ports:
            - '6379:6379'
        volumes:
            - redis-data:/data
        environment:
            - REDIS_ARGS=--requirepass your_password_here --appendonly yes
        restart: unless-stopped

volumes:
    redis-data:
        driver: local
```

Start the service:

```bash
docker compose up -d
```

Stop and remove the containers:

```bash
docker compose down
```

Docker Compose is especially useful when Redis is part of a larger application stack. See [How to build and run a Node.js application using Nginx, Docker and Redis](/tutorials/operate/docker/nodejs-nginx-redis/) for a full multi-container example.

## Next steps

- Learn how to [build a Node.js app with Nginx, Docker, and Redis](/tutorials/operate/docker/nodejs-nginx-redis/)
- Explore [Redis persistence options](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/) to choose between RDB snapshots and AOF
- Read about [Redis configuration](https://redis.io/docs/latest/operate/oss_and_stack/management/config/) for advanced tuning
