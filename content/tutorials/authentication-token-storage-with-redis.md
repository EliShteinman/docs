---
title: "How to store authentication tokens with Redis"
linkTitle: "How to store authentication tokens with Redis"
url: "/tutorials/authentication-token-storage-with-redis/"
description: "You'll build a Bun and Express API with auth routes and a protected todo CRUD. The auth routes are:"
date: 2026-03-19
lastmod: 2026-03-25
hidden: true
---

*Published 19 March 2026 · updated 25 March 2026*

> **TL;DR:**
>
> Store opaque auth tokens in Redis with `SET ... EX`, validate on each request with `GET`, rotate on refresh, and delete on logout. TTL handles cleanup automatically.

> **Note:** This tutorial uses the code from the following git repository:
>
> [https://github.com/redis-developer/authentication-token-storage-with-redis](https://github.com/redis-developer/authentication-token-storage-with-redis)

## What you'll learn

- How to store auth tokens in Redis with automatic TTL-based expiry
- How to validate a bearer token on every request with a single `GET`
- How to rotate a token on refresh
- How to revoke a token instantly on logout
- How to protect API routes with token middleware

## What you'll build

You'll build a Bun and Express API with auth routes and a protected todo CRUD. The auth routes are:

- `POST /api/auth/register` — create an account
- `POST /api/auth/login` — log in and receive a bearer token
- `POST /api/auth/logout` — revoke the token
- `POST /api/auth/refresh` — rotate the token
- `GET /api/auth/me` — get current user info

The todo routes (`GET`, `POST`, `PATCH`, `DELETE` under `/api/todos`) all require a valid `Authorization: Bearer <token>` header.

A login response looks like this:

```json
{
    "token": "d6ad7dae-c147-4513-a58b-2a2516cff3b7",
    "username": "alice"
}
```

## What is token-based authentication?

Token-based authentication is a pattern where the server issues a token after a user logs in. The client sends that token as a bearer token with every subsequent request. The server validates the token, identifies the user, and decides whether to allow the request.

The server needs a fast way to validate, rotate, and revoke tokens. That is where Redis fits—it stores the live token state so every request gets a sub-millisecond lookup, and TTL handles cleanup automatically.

## Why use Redis for authentication token storage?

Redis is a strong fit when you need fast token lookup and instant revocation. A database can store token state, but Redis gives you low-latency reads, built-in TTL-based expiration, and single-command invalidation with `DEL`.

This app uses Redis as a token registry, not as the identity provider. The API decides who can log in, but Redis stores the live token state your app checks on every request.

## Prerequisites

- [Bun](https://bun.sh/)
- [Docker](https://www.docker.com/)
- A Redis instance, either local or [Redis Cloud](https://redis.io/try-free/)
- Basic familiarity with TypeScript and HTTP headers

## Step 1. Clone the repo

```bash
git clone https://github.com/redis-developer/authentication-token-storage-with-redis.git
cd authentication-token-storage-with-redis
bun install
```

## Step 2. Configure environment variables

Copy the sample file:

```bash
cp .env.example .env
```

If you run Redis locally, the default `REDIS_URL` points at `redis://localhost:6379`. If you use Redis Cloud, replace that value with your cloud connection string. The file also documents optional variables like `TOKEN_TTL` (default 3600 seconds).

## Step 3. Run the app with Docker

```bash
bun docker
```

## Step 4. Run the tests

```bash
bun test
```

The test suite includes unit tests for validation schemas and integration tests that cover the full auth lifecycle—register, login, access a protected route, refresh, and logout.

## How does the app store tokens in Redis?

The app uses two key prefixes:

| Key                | Value                                                      | TTL                         | Redis command |
| ------------------ | ---------------------------------------------------------- | --------------------------- | ------------- |
| `tokens:{uuid}`    | The username that owns the token                           | `TOKEN_TTL` (default 3600s) | `SET ... EX`  |
| `users:{username}` | JSON string with username, password hash, and created date | None                        | `SET ... NX`  |

Token validation is a single `GET`:

1. Look up `tokens:{token}` in Redis.
2. If the key exists, the value is the username—the token is valid.
3. If the key is missing, the token has either expired (TTL removed it) or been deleted (logout removed it). Return `401`.

This is the core Redis pattern. Every token check is one `GET` with O(1) complexity, and Redis removes expired tokens automatically.

## How does registration work?

`POST /api/auth/register` creates a new user account. The app hashes the password with `Bun.password.hash()` and stores the user data in Redis with `SET ... NX`.

The `NX` flag tells Redis to set the key only if it does not already exist. This prevents duplicate accounts atomically—no separate "check then insert" step that could race.

Example request:

```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"s3cureP@ss"}'
```

Example response:

```json
{
    "username": "alice",
    "createdDate": "2026-03-19T12:00:00.000Z"
}
```

Under the hood, Redis stores:

```text
SET users:alice '{"username":"alice","passwordHash":"$2b$...","createdDate":"2026-03-19T12:00:00.000Z"}' NX
```

## How does login work?

`POST /api/auth/login` accepts a username and password. The app reads the user record from Redis with `GET`, verifies the password hash with `Bun.password.verify()`, and generates a UUID token. It stores the token in Redis with `SET ... EX` so the token expires automatically after `TOKEN_TTL` seconds.

Example request:

```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"s3cureP@ss"}'
```

Example response:

```json
{
    "token": "d6ad7dae-c147-4513-a58b-2a2516cff3b7",
    "username": "alice"
}
```

Under the hood, Redis stores:

```text
SET tokens:d6ad7dae-c147-4513-a58b-2a2516cff3b7 alice EX 3600
```

The client includes this token in all subsequent requests as `Authorization: Bearer d6ad7dae-...`.

## How does request validation work?

Every protected route runs through the `requireAuth` middleware. The middleware:

1. Extracts the bearer token from the `Authorization` header.
2. Calls `GET tokens:{token}` in Redis.
3. If the key exists, the value is the authenticated username. The request continues.
4. If the key is missing (expired or deleted), the middleware returns `401`.

Example request to a protected route:

```bash
curl http://localhost:8080/api/todos \
  -H "Authorization: Bearer d6ad7dae-c147-4513-a58b-2a2516cff3b7"
```

The lookup is a single `GET`—no joins, no secondary index, no parsing. Redis returns the username or `nil`.

## How does token refresh work?

`POST /api/auth/refresh` rotates the token. The middleware validates the current token, then the handler deletes the old key and creates a new one with a fresh TTL.

The steps:

1. `GET tokens:{old-token}` — retrieve the username.
2. `DEL tokens:{old-token}` — remove the old token.
3. `SET tokens:{new-token} username EX 3600` — store the new token with a fresh TTL.

Example request:

```bash
curl -X POST http://localhost:8080/api/auth/refresh \
  -H "Authorization: Bearer d6ad7dae-c147-4513-a58b-2a2516cff3b7"
```

Example response:

```json
{
    "token": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

After the refresh, the old token returns `401` and the new token is the only valid one.

## How does logout work?

`POST /api/auth/logout` deletes the token from Redis with a single `DEL`. The next request using that token gets `nil` from `GET` and the middleware returns `401`.

```bash
curl -X POST http://localhost:8080/api/auth/logout \
  -H "Authorization: Bearer d6ad7dae-c147-4513-a58b-2a2516cff3b7"
```

No revocation markers, no cleanup jobs. `DEL` removes the key immediately and the token is invalid from that moment forward.

## How it works

The full token lifecycle breaks into two sequences:

```mermaid
sequenceDiagram
    participant C as Client
    participant A as Express API
    participant R as Redis

    C->>A: POST /api/auth/register
    A->>R: SET users:alice ... NX
    R-->>A: OK
    A-->>C: 201 created user

    C->>A: POST /api/auth/login
    A->>R: GET users:alice
    R-->>A: user JSON
    A->>A: Verify password hash
    A->>R: SET tokens:{uuid} alice EX 3600
    R-->>A: OK
    A-->>C: 200 token + username
```

```mermaid
sequenceDiagram
    participant C as Client
    participant A as Express API
    participant R as Redis

    C->>A: GET /api/todos with bearer token
    A->>R: GET tokens:{uuid}
    R-->>A: alice
    A-->>C: 200 todos

    C->>A: POST /api/auth/refresh
    A->>R: DEL tokens:{old-uuid}
    A->>R: SET tokens:{new-uuid} alice EX 3600
    R-->>A: OK
    A-->>C: 200 new token

    C->>A: POST /api/auth/logout
    A->>R: DEL tokens:{uuid}
    A-->>C: 204 no content
```

Redis stores the token records as strings with TTL and the user records as JSON strings. TTL handles cleanup automatically—even if a client never logs out, the token expires and Redis removes the key.

## FAQ

### Should I store JWTs in Redis?

If you need instant revocation or a server-side view of active sessions, store token state in Redis. This tutorial uses opaque tokens (random UUIDs), which is the simplest pattern for lookup and revocation. If you use signed JWTs, Redis still helps when you need a blocklist, a token registry, or a refresh-token store.

### How do I revoke auth tokens with Redis?

Delete the token key with `DEL`. The next `GET` for that token returns `nil`, and the middleware rejects the request immediately. No expiry window, no eventual consistency—revocation takes effect on the next request.

### How long should auth tokens live in Redis?

It depends on the risk profile. This tutorial defaults to 3600 seconds (1 hour). Shorter TTLs reduce the window if a token leaks, but force more frequent refreshes. Longer TTLs improve UX but keep tokens valid longer after a credential change. Choose based on your threat model and adjust `TOKEN_TTL` in the `.env` file.

### When should I use Redis sessions vs token storage?

Use Redis sessions when your app owns a single server-side session ID and the browser simply presents that ID (typically via a cookie). Use token storage when clients present bearer tokens and you need refresh, rotation, or per-token invalidation—common in APIs, mobile apps, and SPAs.

## Troubleshooting

### The app starts but returns a Redis error

Check that `REDIS_URL` in your `.env` file points to a running Redis instance. If you use Docker, verify the container is healthy:

```bash
docker ps
```

### Registration or login returns an unexpected error

Make sure the app container has finished starting. Check the server logs:

```bash
docker logs server
```

### Docker Compose fails to start

Make sure Docker is running and that port 8080 is not already in use by another service.

## Next steps

- Read [Mobile banking session management](/tutorials/howtos/solutions/mobile-banking/session-management/) to compare token storage with session storage.
- Read [API gateway caching](/tutorials/howtos/solutions/microservices/api-gateway-caching/) to see how Redis helps when auth data sits at the gateway.
- Read [Rate limiting](/tutorials/howtos/ratelimiting/) to see another TTL-heavy Redis control pattern.
- Read [Slackbot distributed locking](/tutorials/chat-sdk-slackbot-distributed-locking/) for another example of fast, server-side state control with Redis.

## Additional resources

- [Redis docs](https://redis.io/docs/latest/)
- [Redis clients](https://redis.io/docs/latest/develop/clients/)
- [Redis Insight](https://redis.io/insight/)
