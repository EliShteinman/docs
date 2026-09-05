"""Every knob the CLI proxy reads from its environment, in one place.

Plain os.environ rather than pydantic-settings: this runs as a sidecar whose
image carries flask and gunicorn and nothing else, and a settings library is a
dependency in an air-gapped bundle for the sake of a dozen scalars.
"""

import os

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
SOCKET_TIMEOUT = float(os.environ.get("REDIS_TIMEOUT", "5"))

# The restricted user from files/sandbox.acl. Everything a reader types runs as
# this user. Empty means connect unauthenticated, for a Redis started without
# the ACL file.
REDIS_USERNAME = os.environ.get("REDIS_USERNAME", "")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")

# Sessions are sticky (see sessions.SessionRegistry) so they have to be bounded,
# or every visitor's connection is held for the life of the process. A session
# goes when it has been idle this long, and the oldest go early if the cap is
# reached first; either way the reader gets a fresh session on their next
# command.
SESSION_IDLE_TTL = float(os.environ.get("SESSION_IDLE_TTL", "1800"))
SESSION_MAX = int(os.environ.get("SESSION_MAX", "500"))
# Idle sessions are swept on the way into a request rather than by a background
# thread: an idle process has nothing to collect, and this keeps the sidecar to
# the one thread pool gunicorn already runs.
SWEEP_INTERVAL = float(os.environ.get("SESSION_SWEEP_INTERVAL", "60"))

# Whether commands are namespaced into a per-session slice of the keyspace.
# Off means every reader shares one flat keyspace and overwrites each other's
# keys, which is what this proxy did before namespacing existed.
NAMESPACE_ENABLED = os.environ.get("NAMESPACE_ENABLED", "true").lower() != "false"

# Redis filters SCAN's MATCH *after* walking the table, so a small COUNT over a
# large keyspace returns an empty page and the reader sees nothing. Measured on
# redis.io's sandbox: SCAN 0 COUNT 50 over ~400k keys came back empty. Every
# scan is floored to this many.
SCAN_MIN_COUNT = int(os.environ.get("SCAN_MIN_COUNT", "10000"))

# How many keys the janitor deletes per round trip when reclaiming a session.
CLEANUP_BATCH = int(os.environ.get("CLEANUP_BATCH", "500"))
# Whether a reclaimed session's keys and indexes are deleted. Off leaves them to
# accumulate, which is what happens on a Redis with no eviction policy set.
CLEANUP_ENABLED = os.environ.get("CLEANUP_ENABLED", "true").lower() != "false"

PORT = int(os.environ.get("PORT", "8090"))
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
