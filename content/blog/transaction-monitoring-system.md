---
title: "What is a transaction monitoring system & how does it work?"
linkTitle: "What is a transaction monitoring system & how does it work?"
url: "/blog/transaction-monitoring-system/"
description: "The Financial Crimes Enforcement Network (FinCEN) issued a $1.3 billion penalty against TD Bank in 2024 for broad anti-money laundering (AML) program failures, including trillions of dollars in..."
date: 2026-03-23
blogCategories:
- "Tech DE"
authors:
- "Jim Allen Wallace"
lastmod: 2026-03-24
hidden: true
mirrored: true
---

*By Jim Allen Wallace, Sr. Product Marketing Manager · Published 23 March 2026 · updated 24 March 2026*

![What is a transaction monitoring system & how does it work?](/images/site-mirror/16c9ec03438df178f1f09500d91fb22f86a53915-2400x1256.webp)

The Financial Crimes Enforcement Network (FinCEN) issued a $1.3 billion [penalty against TD Bank](https://www.fincen.gov/news/news-releases/fincen-assesses-record-13-billion-penalty-against-td-bank) in 2024 for broad anti-money laundering (AML) program failures, including trillions of dollars in transactions that went unmonitored annually, according to the consent order. The Financial Conduct Authority (FCA) [fined Metro Bank](https://www.fca.org.uk/news/press-releases/fca-fines-metro-bank-16m-financial-crime-failings) £16 million after a data error left over 60 million transactions unchecked for more than four years. This shows how quickly data and systems gaps can turn into regulatory exposure.

If you're responsible for the systems behind AML compliance or fraud detection, the infrastructure under your monitoring stack matters as much as the rules running on top of it. This article covers what a transaction monitoring system does, how the data pipeline works end to end, and what a modern reference architecture looks like under the hood.

## What is a transaction monitoring system?

A transaction monitoring system (TMS) is the internal control financial institutions use to detect, investigate, and report suspicious financial activity. Under the Bank Secrecy Act (BSA), every covered financial institution must have an [AML program](https://www.fincen.gov/resources/statutes-regulations/guidance/guidance-existing-aml-program-rule-compliance-obligations) designed to prevent money laundering and terrorist financing. In U.S. banking supervision, BSA/AML systems are treated as important controls within that framework. That framing matters because these programs are legally required. A TMS often sits near the center of that program, handling three core functions.

### AML compliance

AML monitoring watches for patterns that suggest illicit activity, including cash transactions above [BSA reporting thresholds](https://www.fincen.gov/resources/statutes-and-regulations/bank-secrecy-act) and behaviors like structuring or layering. That means tracking both individual transactions and aggregated behavior over time.

### Fraud detection

Fraud controls flag unusual behavior across accounts and channels, monitoring wire transfer patterns, identifying gaps in originator or beneficiary information, and catching anomalies that don't match a customer's profile. Many institutions run fraud and AML controls side by side because the same payment event can raise both kinds of risk.

### Regulatory reporting

When an investigation warrants it, institutions file Suspicious Activity Reports (SARs) to FinCEN. That also means preserving the evidence trail behind filing decisions, including decisions not to file. Taken together, those functions make a TMS part detection engine, part workflow system, and part audit trail.

## How transaction monitoring systems work

With those functions defined, the next question is how the pipeline moves from raw data to filed SARs. A modern TMS processes transactions through a multi-stage flow that combines streaming, rule engines, machine learning (ML) models, and human investigation workflows.

### Data ingestion & enrichment

The pipeline begins with source systems such as core banking, Know Your Customer (KYC) platforms, payment rails, and transaction repositories. Before anything gets evaluated, transactions are enriched with customer risk profiles, historical patterns, beneficial ownership data, and sanctions-screening context. Regulators and industry guidance often stress documenting these source systems and data flows, so many firms maintain formal data lineage diagrams even when the exact format is left to the institution.

### Detection: rules & ML together

Once the data is enriched, two detection approaches often run in parallel. Rule-based systems apply fixed thresholds and scenario logic, such as structuring detection below the $10,000 Currency Transaction Report threshold or rapid fund-movement patterns. These rules are familiar to regulators, but they can be slow to update when new typologies emerge.

Traditional AML monitoring often produces high false-positive rates, which is one reason many teams are modernizing TMS stacks. AI and ML approaches can help reduce that burden while catching patterns rules miss.

### Investigation & reporting

From there, alerts move into human review. Larger institutions often use tiered review models where front-line analysts validate alerts, investigators perform deeper analysis, and senior staff make SAR filing decisions.

That handoff between automated detection and human review is one reason processing speed matters. Some risks can wait for overnight analysis, but in certain payment flows, you may need a decision before a payment leaves the institution.

## Real-time vs. batch transaction monitoring

That workflow leads to the next design choice: when monitoring happens. The shift from batch to real-time monitoring isn't just a performance upgrade. It's increasingly shaped by EU payment rules and related compliance demands.

Under the [EU instant-payment rollout](https://www.ecb.europa.eu/paym/retail/instant_payments/html/instant_payments_regulation.en.html), euro instant-credit-transfer requirements are tightening decision windows across the region. In instant-payment flows, that compresses fraud checks and related screening controls into a near-real-time path instead of leaving hours for downstream review. And because instant payments are hard to reverse, detection often has to happen before authorization rather than after settlement.

That said, batch processing still matters. It's a good fit for layering schemes, behavioral drift over time, and slower-developing typologies like funnel account networks. In practice, most modern architectures use both: real-time controls for immediate decisioning, and batch analysis for deeper retrospective review.

## Key capabilities every transaction monitoring system should include

Because most institutions end up with that hybrid model, the next step is the capability set behind it. Four areas matter most when you're evaluating or building a TMS.

- **BSA/AML compliance foundation:** Customer Identification Programs (CIP), Customer Due Diligence (CDD), suspicious activity aggregation, structuring detection, and multi-location monitoring. In U.S. programs, aggregation typically supports SAR decisioning against applicable thresholds ($5,000 in many bank scenarios and $2,000 for some money services business cases under FinCEN rules and guidance), though specific requirements vary by institution type.
- **AI-augmented detection:** Anomaly detection, behavioral profiling, and AI-driven typology recognition can catch patterns that static rules miss. The UK FCA has supported [synthetic data](https://www.turing.ac.uk/news/new-data-science-project-uses-synthetic-data-address-main-barriers-innovation-field-money) work with banks and research partners to help improve model training and testing where real transaction data is limited or sensitive.
- **Cross-channel data integration:** Risk assessment improves when it pulls together customer profiles, KYC data, transaction history, and external inputs like sanctions lists, adverse media, and politically exposed person (PEP) data. Without that broader view, teams end up scoring isolated events instead of customer behavior.
- **Automated workflow & case management:** Automation can reduce routine review work and help route higher-risk cases to the right investigators faster. How much you automate depends on your risk appetite and what your regulators expect.

No single capability carries the system on its own. Detection, data integration, compliance controls, and case management work best as a coordinated stack, not four separate tools.

## Reference architecture: the data & AI layer under a transaction monitoring system

Those capability requirements drive the architecture beneath the TMS. Most teams are looking for a stack that supports low-latency scoring for individual transactions without giving up deeper analytical processing for pattern detection.

### Stream ingestion & processing

The streaming ingestion layer needs to handle high event volumes with minimal latency. Once events are validated and normalized, they're routed to downstream scoring and decisioning services.

### Feature store & in-memory layer

A feature store usually has to support both batch access for training jobs and low-latency feature serving for real-time inference. Velocity features such as transaction count in the last hour or transfers to new recipients in the last day are often precomputed so they can be used immediately during scoring.

The in-memory data layer acts as the online serving tier for that feature store, providing the fast access real-time scoring depends on. Current balances, recent transaction history, and device fingerprints can be held in memory and updated through change data capture pipelines from core systems. In a typical fraud detection architecture, payment systems have roughly 100 ms to pull data, score fraud risk, and authorize a transaction, with ML model scoring typically consuming 10–50 ms of that budget.

Redis can serve as this in-memory layer for low-latency operational and AI workloads. [Redis Streams](https://redis.io/docs/latest/develop/data-types/streams/) supports event streaming with features like simplified multi-consumer-group management and idempotent production with at-most-once production guarantees. Sorted sets and hashes can maintain velocity counters and session state. For ML-generated vector embeddings used in pattern retrieval, the [Redis Query Engine](https://redis.io/docs/latest/develop/ai/search-and-query/vectors/) provides native vector search alongside full-text search and hybrid search with re-ranking.

### Model serving, graph analysis, & storage

At that point, scores and relationships have to be computed. Models often run as separate services, with one path for historical training and another for live inference, while graph analysis adds entity resolution and ring detection where relationship-based patterns matter.

To control cost, the data layer usually tiers storage. Hot data such as active sessions and scoring context stays in memory, while older history, audit trails, and training data move to lower-cost storage. [Redis Flex](/blog/introducing-another-era-of-fast/), available in Redis Cloud and Redis Software, combines RAM and SSD in a tiered storage model, shifting less-active data to SSD while keeping hot data in memory. It can cut memory costs by up to 80% in deployments where the workload fits.

## Building & modernizing a transaction monitoring system

Modernizing a TMS usually takes months, and the hard part is often less about new models than about validation, controls, and data quality. The practical question is how to get there without breaking coverage.

### Run systems in parallel

Start with parallel runs. Feed the same transactions into both the legacy and new systems, then compare outputs so each alert difference can be classified as either false-positive reduction or a coverage gap.

### Plan for continuous validation

Just as important, plan tuning and review. Models should be reviewed regularly and independently validated, especially because some institutions still run AML scenarios built years ago without revision.

### Build hybrid from the start

Design for hybrid monitoring from day one rather than bolting on real-time processing later. Instant-payment fraud, unauthorized access, layering, and correspondent banking typologies don't all operate on the same timeline.

### Fix data quality first

Before you evaluate tools, remember Metro Bank. Their 60+ million unmonitored transactions came from a data error, not a model failure. Monitoring quality starts upstream.

### Treat AI as a tool, not a black box

Explainability matters for any AI-driven detection approach. [Fed risk guidance](https://www.federalreserve.gov/supervisionreg/srletters/SR2108.htm) emphasizes that risk management for BSA/AML systems should remain consistent with safety and soundness principles, even as more institutions adopt AI for fraud and financial crime detection.

## Transaction monitoring is now a fast-data architecture problem

Transaction monitoring is moving from a back-office batch job toward a real-time infrastructure challenge. As payment windows shrink and regulatory expectations tighten, many firms are looking for systems that can ingest events fast, enrich them with current context, score them with sub-millisecond latency, and route the right cases into investigation workflows.

That's where Redis fits. Instead of managing separate systems for caching, event streaming, and vector search, Redis combines all three in a single real-time data platform with a memory-first architecture. It serves state in memory, processes events with streams, and supports vector search for AI-driven pattern matching. If you're trying to consolidate your scoring and feature-serving infrastructure while keeping access fast, that combination is worth a close look.

[Try Redis free](https://redis.io/try-free/) to test it against your workload, or [talk to our team](https://redis.io/meeting/) about how Redis fits into your transaction monitoring architecture.
