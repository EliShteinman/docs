---
title: "Introducing Redis Feature Form: An enterprise-grade feature store for production ML"
linkTitle: "Introducing Redis Feature Form: An enterprise-grade feature store for production ML"
url: "/blog/introducing-redis-feature-form/"
description: "When Redis acquired Featureform last October, we were already a core part of how teams served real-time data to models, especially in production systems where latency and reliability matter...."
date: 2026-04-20
blogCategories:
- "Tech"
authors:
- "Simba Khadder"
lastmod: 2026-04-20
hidden: true
mirrored: true
---

*By Simba Khadder, Head of Context Engine at Redis. · Published 20 April 2026*

![Redis](/images/site-mirror/5aba89ba06f36351bf71258419c2514dc6282ed7-1200x628.webp)

When Redis acquired Featureform last October, we were already a core part of how teams served real-time data to models, especially in production systems where latency and reliability matter. Featureform added the missing orchestration layer: a way to define, manage, and serve features consistently across training and inference, without forcing teams to rebuild their stack around a single vendor.

Today, we're introducing Redis Feature Form, a complete managed feature store platform for production ML. It covers the full feature lifecycle, from definition and pipeline orchestration through versioning, lineage, and sub-millisecond online serving. Redis is no longer just the online store, but the system that helps teams define features once, keep them governed, and serve them reliably at scale.

The new Feature Form builds on what made the platform valuable to early adopters and makes it more useful for enterprise ML teams. We’ve made Feature Form easier to run across multiple teams, safer in production, and more predictable as feature pipelines evolve over time.

We’ve added several improvements:

- **Unified batch and streaming pipelines:** Improved support for tiling, backfills, and incremental updates, reducing custom pipeline work.
- **Workspaces for multi-tenancy:** Teams can now isolate providers, data, auth, and observability at the workspace level, making Feature Form better suited for organizations with multiple ML teams and shared platform infrastructure.
- **Fine-grained job control:** New planning, impact analysis, split materializations, and queue-based job management give teams more visibility into changes before they write data or affect production systems.
- **Atomic DAG updates:** Instead of versioning individual resources in isolation, Feature Form can now manage graph-level changes atomically, which makes rollback and change history much cleaner.
- **Enhanced RBAC and security:** Workspace-scoped access controls, API key pairs, a more granular model role, audit logs, secret-provider improvements, mTLS, and encrypted internal transport strengthen the platform for enterprise environments.
- **Simplified deployment:** A leaner two-service deployment model reduces operational complexity while still leaving room for more advanced deployment patterns.
- **A fully redesigned dashboard:** The UI has been rebuilt to support these workflows directly, including configuration of workspaces and providers from the interface.

Feature Form helps ML teams move features from definition to production with less glue code, less drift between training and serving, and less operational overhead. That matters in the places where production ML is already delivering measurable value: fraud detection, credit and risk scoring, personalization, recommendation systems, and other use cases where stale or inconsistent features quickly become a business problem. It also matters for platform teams that have spent too much time maintaining homegrown pipelines and would rather give data scientists and ML engineers a governed path to self-service.

Feature Form expands Redis’ role in the ML stack. Historically, we often showed up as the serving layer inside a larger feature architecture. That worked, but it also left the platform decision to someone else. Feature Form changes that. It gives Redis a stronger position higher in the stack, where teams are deciding how features are defined, versioned, orchestrated, and governed across their environment. Redis is no longer only the fast system behind feature serving. It becomes part of the control plane for production ML itself.

We’re investing in multiple lanes at once: real-time context for agents, token and latency optimization, high-performance search, and now a more complete feature platform for classical ML. Those are distinct problems, but they share the same underlying requirement: reliable, real-time access to data that systems can actually use. Feature Form is the piece that anchors that story for structured ML features. It shows that Redis is not treating machine learning as a side use case layered onto an old database story. It is building toward a future where Redis supports both modern AI systems and long-lived production ML workloads from the same data platform foundation.
