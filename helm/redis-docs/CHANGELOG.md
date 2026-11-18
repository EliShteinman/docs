# Changelog

> **[גרסה בעברית](CHANGELOG-he.md)**

What changed in each chart version, and what to change in your values when you upgrade.
The CI build publishes every chart version with a patch bump. A new minor series starts at
`.1`, because the build bumps the patch of the version committed to `Chart.yaml`.

## 3.2.0

### Action required

- **Only if you set `externalLinks.gitMirrors`:** an entry whose name is not in
  `files/external-links.yaml` used to be ignored without a word. It now fails the install
  with a message, unless the entry gives `repo: <owner>/<name>`. Entries for catalog names
  keep working as they are.
- **Only if you edited `files/external-links.yaml` in a copy of the chart:** a `git-mirrors`
  entry now names its repository with `repo: <owner>/<name>` (plus `aliases`), not with a
  `from` URL.

### Changed

- **Git-mirror links match the whole repository name.** `redis/redis` used to catch every link
  starting with it, so links to `redis/redis-py`, `redis/redis-om-*` and `redis/redisinsight`
  went to the redis copy. They now go to their own copy, or stay on GitHub.
- **Links to what a GitLab copy lacks stay on GitHub:** pull requests, issues, discussions,
  security advisories, the wiki and Actions. They used to be sent to a GitLab page that does
  not exist.
- **Release links get their GitLab form:** `releases/latest` goes to
  `/-/releases/permalink/latest`, and `releases/download/<tag>/<file>` to
  `/-/releases/<tag>/downloads/<file>`. A line range `#L10-L20` becomes `#L10-20`.
- **Links added to a page after it loads are rewritten too.**

### Added

- **34 repositories in the git-mirror catalog** (was 12), all off by default: the client
  libraries, `redis/docs`, redisctl, RIOT-X, Redis Insight tutorials, the Arrow Flight server,
  the ADBC driver and the Grafana data source. Each entry also answers to the older names
  GitHub still redirects, such as `RedisInsight/RedisInsight`, which moved to `redis/RedisInsight`.
- **The copies themselves** are made with `scripts/airgap-mirrors`, which also writes the
  `gitMirrors` values for you. See `MIRRORS-SETUP-he.md`.

No new images or ports. `appVersion` and every image tag are unchanged.

## 3.1.1

### Action required

- **Remove `externalLinks.overrides.nav-mobile-menu` from your values, if present.** The key
  no longer exists. An override for it is ignored, so leaving it in does not break the
  install, but it does nothing.
- **Remove `externalLinks.families.header.sub-families.mobile` from your values, if
  present.** The sub-family no longer exists, for the same reason.

### Changed

- **The mobile menu (hamburger) is always shown.** It used to belong to the external-links
  catalog as `nav-mobile-menu`, so with `externalLinks.enabled: false` it was hidden, together
  with the internal pages inside it. It now opens with Redis Iris, Redis install, Data types,
  Tools, and Community. The external items inside it (Docs, Sign up, Login) keep their own keys
  (`nav-docs`, `nav-try-redis`, `nav-login`) and stay hidden while those keys are off.
- **The full top menu appears from 1280px wide, not from 1024px** (upstream change). Below
  1280px the header shows the logo and the hamburger. The fork's "More from Redis" menu follows
  the same breakpoint.

### Added

- **Redis Iris documentation** (upstream): Agent Memory, Context Gateway, Intent Router,
  Agent Playbooks, and Lens, under `/develop/ai/context-engine/` and `/operate/iris/`.
  LangCache moved from `/develop/ai/context-engine/langcache/` to `/develop/ai/langcache/`.
  The old addresses redirect to the new ones.

No new images, values, or ports.
