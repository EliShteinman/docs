"""Giving each reader their own slice of one shared keyspace.

Every visitor's commands run against the same Redis database, so without this
two readers working through the same tutorial write to the same `product:1` and
overwrite each other. The fix is the one redis.io's sandbox uses: each session
gets a prefix, every key it names is stored under that prefix, and every key
handed back has the prefix taken off again. The reader never sees it — they type
`SET product:1` and `KEYS *` answers `product:1`, out of a database holding
everyone else's too.

Three kinds of rewriting, because a key reaches Redis three different ways:

  * As a key argument.       Which arguments those are is not guessable from the
                             command name — SET has one, GEORADIUS may have two
                             depending on its options, EVAL's count is an
                             argument value. Redis knows, and COMMAND GETKEYS
                             tells us, so KeyResolver asks rather than carrying a
                             table that goes stale.

  * As a pattern.            KEYS and SCAN match against the keyspace instead of
                             naming a key, so their pattern is what needs the
                             prefix. HSCAN, SSCAN and ZSCAN look like SCAN and
                             are not: they match fields inside one key, and
                             prefixing those breaks them silently.

  * As an index definition.  FT.CREATE's PREFIX clause is a key pattern that
                             COMMAND GETKEYS does not report, because it is not
                             a key argument. An index left unprefixed indexes
                             every session's documents at once, so a search
                             returns other readers' data — which is why an index
                             created without a PREFIX gets one here.

Replies need the reverse, and only some carry key names: KEYS, SCAN, FT._LIST,
FT.SEARCH, FT.INFO and the TS.M* family. Anything else that could return a key
without being in that list — RANDOMKEY is the example — is denied in the ACL
rather than handled here. Being closed is what makes the short list safe.
"""

import logging

from resp import RespError, RespStatus

LOGGER = logging.getLogger("cli_proxy.namespace")

# What LookupConnection answers with when it cannot reach Redis at all. Distinct
# from any error Redis itself returns, so the two are never confused.
LOOKUP_UNAVAILABLE = "lookup unavailable"

# Commands whose only key-shaped argument is a glob against the keyspace.
PATTERN_COMMANDS = frozenset({"KEYS"})

# SCAN walks the keyspace; the rest walk one key's fields and must not be
# touched. They are listed so the difference is stated rather than implied.
KEYSPACE_SCAN = frozenset({"SCAN"})
FIELD_SCANS = frozenset({"HSCAN", "SSCAN", "ZSCAN"})

# Search commands that name an index in argv[1].
INDEX_COMMANDS = frozenset({
    "FT.CREATE", "FT.SEARCH", "FT.AGGREGATE", "FT.INFO", "FT.DROPINDEX",
    "FT.DROP", "FT.ALTER", "FT.EXPLAIN", "FT.EXPLAINCLI", "FT.PROFILE",
    "FT.TAGVALS", "FT.SPELLCHECK", "FT.SYNUPDATE", "FT.SYNDUMP", "FT.CURSOR",
    "FT.ALIASADD", "FT.ALIASDEL", "FT.ALIASUPDATE", "FT._DROPINDEXIFX",
})
# FT.CURSOR's index is one further along: FT.CURSOR READ <index> <id>.
INDEX_AT_TWO = frozenset({"FT.CURSOR"})
# The alias is argv[1] and the index it points at is argv[2]; both are names in
# the shared namespace.
ALIAS_COMMANDS = frozenset({"FT.ALIASADD", "FT.ALIASUPDATE"})

# Time-series commands that select by label and answer with key names.
TS_MULTI = frozenset({"TS.MRANGE", "TS.MREVRANGE", "TS.MGET", "TS.QUERYINDEX"})


class Namespace:
    """One session's slice of the keyspace, and the names that belong to it."""

    def __init__(self, sid: str) -> None:
        self.prefix = f"{sid}:"

    def apply(self, name: str) -> str:
        # Idempotent: a name that already carries the prefix is left alone, so a
        # value that made a round trip cannot come back double-prefixed.
        if name.startswith(self.prefix):
            return name
        return self.prefix + name

    def strip(self, name: str) -> str:
        if name.startswith(self.prefix):
            return name[len(self.prefix):]
        return name

    def owns(self, name: str) -> bool:
        return name.startswith(self.prefix)


class KeyLookupUnavailable(Exception):
    """Redis could not say which arguments are keys.

    Raised rather than answered with an empty list, because the two mean
    opposite things: no keys means send the command untouched, while no answer
    means we cannot tell where the keys are — and sending it untouched would
    write outside the reader's namespace, into the keyspace everyone shares.
    """


class KeyResolver:
    """Which arguments of a command are keys, according to Redis itself.

    Asks COMMAND GETKEYS over a connection of its own, never the session's. A
    session inside MULTI answers every command with QUEUED, so a lookup on that
    connection would return QUEUED instead of the key list — and quietly queue a
    COMMAND GETKEYS into the reader's transaction.

    Only one thing is cached: that a command takes no keys at all. That answer
    depends on the command name alone and never changes, unlike key positions,
    which for EVAL, ZUNIONSTORE and GEORADIUS depend on the argument values.
    """

    def __init__(self, execute) -> None:
        self._execute = execute
        self._keyless: set[str] = set()

    def keys_of(self, argv: list[str]) -> list[str]:
        name = argv[0].upper()
        if name in self._keyless:
            return []

        reply = self._execute(["COMMAND", "GETKEYS", *argv])
        if isinstance(reply, RespError):
            message = str(reply).lower()
            # "The command has no key arguments" and "Invalid command specified"
            # both mean there is nothing to rewrite. A command Redis cannot parse
            # will fail on its own when it is sent for real.
            if "no key arguments" in message:
                self._keyless.add(name)
                return []
            if LOOKUP_UNAVAILABLE in message:
                raise KeyLookupUnavailable(str(reply))
            return []
        if not isinstance(reply, list):
            return []
        return [item for item in reply if isinstance(item, str)]


class CommandRewriter:
    """Rewrites a reader's command so it lands inside their own namespace."""

    def __init__(self, resolver: KeyResolver, scan_min_count: int) -> None:
        self._resolver = resolver
        self._scan_min_count = scan_min_count

    def rewrite(self, argv: list[str], namespace: Namespace) -> list[str]:
        name = argv[0].upper()

        if name in FIELD_SCANS:
            return self._rewrite_keys(argv, namespace)
        if name in KEYSPACE_SCAN:
            return self._rewrite_scan(argv, namespace)
        if name in PATTERN_COMMANDS:
            return self._rewrite_pattern(argv, namespace)
        if name in INDEX_COMMANDS:
            return self._rewrite_index(argv, namespace)
        return self._rewrite_keys(argv, namespace)

    def _rewrite_keys(self, argv: list[str], namespace: Namespace) -> list[str]:
        keys = self._resolver.keys_of(argv)
        if not keys:
            return argv

        rewritten = list(argv)
        claimed: set[int] = set()
        for key in keys:
            for position in range(1, len(rewritten)):
                if position in claimed or rewritten[position] != key:
                    continue
                rewritten[position] = namespace.apply(key)
                claimed.add(position)
                break
        return rewritten

    def _rewrite_pattern(self, argv: list[str], namespace: Namespace) -> list[str]:
        if len(argv) < 2:
            return argv
        return [argv[0], namespace.apply(argv[1]), *argv[2:]]

    def _rewrite_scan(self, argv: list[str], namespace: Namespace) -> list[str]:
        rewritten = list(argv)

        match_at = _option(rewritten, "MATCH")
        if match_at is not None:
            rewritten[match_at + 1] = namespace.apply(rewritten[match_at + 1])
        else:
            rewritten += ["MATCH", namespace.apply("*")]

        # A COUNT the reader chose is a floor, not a ceiling: their 10 would
        # return an empty page, and an empty page reads as "no keys".
        count_at = _option(rewritten, "COUNT")
        if count_at is not None:
            rewritten[count_at + 1] = str(max(_as_int(rewritten[count_at + 1]), self._scan_min_count))
        else:
            rewritten += ["COUNT", str(self._scan_min_count)]
        return rewritten

    def _rewrite_index(self, argv: list[str], namespace: Namespace) -> list[str]:
        name = argv[0].upper()
        at = 2 if name in INDEX_AT_TWO else 1
        if len(argv) <= at:
            return argv

        rewritten = list(argv)
        rewritten[at] = namespace.apply(rewritten[at])
        if name in ALIAS_COMMANDS and len(rewritten) > at + 1:
            rewritten[at + 1] = namespace.apply(rewritten[at + 1])
        if name == "FT.CREATE":
            rewritten = _rewrite_index_prefixes(rewritten, namespace)
        return rewritten


def _rewrite_index_prefixes(argv: list[str], namespace: Namespace) -> list[str]:
    """Point a new index at this session's documents and no one else's.

    FT.CREATE takes `PREFIX <count> <prefix>...`. Each of those is a key pattern
    and gets the namespace. An index declared without the clause matches every
    key in the database, so one is added — otherwise the first reader to run the
    search tutorial builds an index over everybody's documents.

    An added clause goes in front of SCHEMA, not on the end: everything after
    SCHEMA is field definitions, and Redis rejects the whole command if the
    clause lands among them.
    """
    prefix_at = _option(argv, "PREFIX")
    if prefix_at is None:
        clause = ["PREFIX", "1", namespace.prefix]
        schema_at = _keyword(argv, "SCHEMA")
        if schema_at is None:
            return [*argv, *clause]
        return [*argv[:schema_at], *clause, *argv[schema_at:]]

    count = _as_int(argv[prefix_at + 1])
    rewritten = list(argv)
    for offset in range(count):
        position = prefix_at + 2 + offset
        if position < len(rewritten):
            rewritten[position] = namespace.apply(rewritten[position])
    return rewritten


class ReplyFilter:
    """Takes the namespace back off anything that hands a name to the reader."""

    def filter(self, argv: list[str], reply: object, namespace: Namespace) -> object:
        name = argv[0].upper()

        if isinstance(reply, (RespError, RespStatus)):
            return reply
        if name in PATTERN_COMMANDS or name == "FT._LIST" or name == "TS.QUERYINDEX":
            return self._names(reply, namespace)
        if name in KEYSPACE_SCAN:
            return self._scan(reply, namespace)
        if name in ("FT.SEARCH", "FT.AGGREGATE", "FT.PROFILE"):
            return self._search(reply, namespace)
        if name == "FT.INFO":
            return self._pairs(reply, namespace, "index_name")
        if name in TS_MULTI:
            return self._series(reply, namespace)
        if name in INDEX_COMMANDS:
            return reply
        return reply

    def _names(self, reply: object, namespace: Namespace) -> object:
        if not isinstance(reply, list):
            return reply
        return [namespace.strip(item) for item in reply
                if isinstance(item, str) and namespace.owns(item)]

    def _scan(self, reply: object, namespace: Namespace) -> object:
        if not isinstance(reply, list) or len(reply) != 2:
            return reply
        return [reply[0], self._names(reply[1], namespace)]

    def _search(self, reply: object, namespace: Namespace) -> object:
        """FT.SEARCH answers [total, key, fields, key, fields, ...] — sometimes.

        NOCONTENT drops the field arrays and WITHSCORES adds a score, so the
        document keys are not at a fixed stride and counting positions gets one
        of the three shapes wrong. Every name this session owns is unwrapped
        instead, wherever it sits: the index is already scoped to the session, so
        the only namespaced strings in the reply are its own document keys.
        """
        return _unwrap_owned(reply, namespace)

    def _pairs(self, reply: object, namespace: Namespace, field: str) -> object:
        """A flat [name, value, ...] map with one value that is a namespaced name."""
        if not isinstance(reply, list):
            return reply
        unwrapped = list(reply)
        for position in range(0, len(unwrapped) - 1, 2):
            if unwrapped[position] == field and isinstance(unwrapped[position + 1], str):
                unwrapped[position + 1] = namespace.strip(unwrapped[position + 1])
        return unwrapped

    def _series(self, reply: object, namespace: Namespace) -> object:
        """TS.MRANGE and friends answer [[key, labels, values], ...].

        These select by label, not by key, so they reach every session's series
        and the ones that are not ours have to be dropped, not just unwrapped.
        """
        if not isinstance(reply, list):
            return reply
        kept = []
        for entry in reply:
            if not isinstance(entry, list) or not entry or not isinstance(entry[0], str):
                continue
            if not namespace.owns(entry[0]):
                continue
            kept.append([namespace.strip(entry[0]), *entry[1:]])
        return kept


def _unwrap_owned(value: object, namespace: Namespace) -> object:
    """Take the namespace off every name in a reply that belongs to this session.

    Used where a reply's shape shifts with the command's options and counting
    positions would get one variant wrong. Safe because the prefix is a UUID: a
    string that carries it is a name this proxy wrote, not a reader's data.
    """
    if isinstance(value, RespStatus) or isinstance(value, RespError):
        return value
    if isinstance(value, str):
        return namespace.strip(value)
    if isinstance(value, list):
        return [_unwrap_owned(item, namespace) for item in value]
    return value


def _option(argv: list[str], name: str) -> int | None:
    """Where a named option sits, if it is present and has a value after it."""
    for position in range(1, len(argv) - 1):
        if argv[position].upper() == name:
            return position
    return None


def _keyword(argv: list[str], name: str) -> int | None:
    """Where a bare keyword sits, value or not."""
    for position in range(1, len(argv)):
        if argv[position].upper() == name:
            return position
    return None


def _as_int(text: str, fallback: int = 0) -> int:
    try:
        return int(text)
    except (TypeError, ValueError):
        return fallback
