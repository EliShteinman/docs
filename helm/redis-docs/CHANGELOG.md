# Changelog

> **[גרסה בעברית](CHANGELOG-he.md)**

What changed in each chart version, and what to change in your values when you upgrade.
The CI build publishes every chart version with a patch bump. A new minor series starts at
`.1`, because the build bumps the patch of the version committed to `Chart.yaml`.

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
