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


def normalize_result(result):
    """Convert redis-py Python types to RESP-like values for the CLI frontend."""
    if result is True:
        return "OK"
    if result is False:
        return "(nil)"
    if isinstance(result, bytes):
        return result.decode("utf-8", errors="replace")
    if isinstance(result, dict):
        flat = []
        for k, v in result.items():
            flat.append(normalize_result(k))
            flat.append(normalize_result(v))
        return flat
    if isinstance(result, (list, tuple)):
        return [normalize_result(item) for item in result]
    if isinstance(result, set):
        return [normalize_result(item) for item in result]
    return result


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
            cmd_upper = parts[0].upper()
            result = client.execute_command(*parts)
            if cmd_upper == "PING" and result is True:
                result = "PONG"
            replies.append({"error": False, "value": normalize_result(result)})
        except redis.RedisError as e:
            replies.append({"error": True, "value": str(e)})

    return jsonify({"replies": replies, "id": sid})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8090")))
