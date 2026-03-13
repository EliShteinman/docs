import json
import os
import uuid

import redis
from flask import Flask, request, jsonify

app = Flask(__name__)

pool = redis.ConnectionPool(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", "6379")),
    decode_responses=True,
)

sessions: dict[str, redis.Redis] = {}


def get_client(session_id: str | None) -> tuple[redis.Redis, str]:
    if session_id and session_id in sessions:
        return sessions[session_id], session_id

    sid = session_id or str(uuid.uuid4())
    client = redis.Redis(connection_pool=pool)
    sessions[sid] = client
    return client, sid


@app.route("/healthz")
def healthz():
    return "ok"


@app.route("/cli", methods=["POST"])
def cli():
    body = request.get_json(silent=True) or {}
    commands = body.get("commands", [])
    session_id = body.get("id")

    client, sid = get_client(session_id)
    replies = []

    for cmd in commands:
        parts = cmd.split()
        if not parts:
            replies.append({"error": True, "value": "empty command"})
            continue
        try:
            result = client.execute_command(*parts)
            replies.append({"error": False, "value": result})
        except redis.RedisError as e:
            replies.append({"error": True, "value": str(e)})

    return jsonify({"replies": replies, "id": sid})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8090")))
