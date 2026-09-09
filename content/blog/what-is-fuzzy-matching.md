---
title: "What is fuzzy matching?"
linkTitle: "What is fuzzy matching?"
url: "/blog/what-is-fuzzy-matching/"
description: "Exact matching breaks the moment a user types \"seperate\" instead of \"separate.\" Fuzzy matching (also called approximate string matching) finds strings, names, or records that are similar, not..."
date: 2026-03-14
blogCategories:
- "Tech"
authors:
- "Jim Allen Wallace"
lastmod: 2026-05-21
hidden: true
---

*By Jim Allen Wallace, Sr. Product Marketing Manager · Published 14 March 2026 · updated 21 May 2026*

![Blog tile image](/images/site-mirror/772ee1cb99ea3440c615040e902fb03f1fa11160-1200x628.webp)

Exact matching breaks the moment a user types "seperate" instead of "separate." Fuzzy matching (also called approximate string matching) finds strings, names, or records that are similar, not identical, so your app can return the best candidates instead of nothing. In search engines, this technique is often called fuzzy search.

This guide covers what fuzzy matching is, how it works, where it's used, the most common algorithms behind it, and how search infrastructure can support it.

## How does fuzzy matching work?

Fuzzy matching compares two strings using a similarity score, often based on edit distance, and treats "close enough" as a match. Instead of a strict yes/no result, it produces a score you can use to include near matches and rank results by closeness.

The most common approach measures how many small edits it takes to turn one string into another. These edits include insertions, deletions, and substitutions. Fewer edits means the strings are more similar, and a score of 0 means an exact match.

Most systems also apply a cutoff so only results within a chosen tolerance are returned. A stricter cutoff reduces false positives but can miss legitimate variations, while a looser cutoff finds more candidates but needs stronger ranking or follow-up validation to stay useful.

## Fuzzy matching vs. exact matching

Exact matching returns results only when a query is identical to the stored value. Fuzzy matching returns results that are similar enough based on a distance or similarity score, which makes it much more forgiving with real-world input.


| Feature | Exact matching | Fuzzy matching |
|---|---|---|
| Match requirement | Identical strings only | Strings within a distance threshold |
| Handles typos | No | Yes |
| Handles name variations | No | Yes |
| Returns a match score | No | Yes |
| False positive risk | None | Present at higher thresholds |
| Performance cost | Lower | Higher |

Exact matching is a good fit when identifiers are clean and controlled (like stock keeping units). Fuzzy matching matters most when data comes from humans or multiple systems, where inconsistent spelling and formatting are normal.

## Fuzzy matching use cases

Fuzzy matching is commonly used in search, deduplication, fraud detection, and record linkage. It's especially useful anywhere you need to reconcile "nearly the same" text across sources, inputs, or records.

Common examples include:

- **Deduplication:** Finding [duplicate records](https://redis.io/solutions/deduplication/) that don't look identical, like customer entries with slightly different names or formats.
- **Fraud detection:** Matching [flagged entities](https://redis.io/solutions/fraud-detection/) and transaction details even when names are misspelled or intentionally obscured.
- **Healthcare record linkage:** Connecting patient records across systems where names are often entered inconsistently. In one [study of 398,939 patient records](https://pmc.ncbi.nlm.nih.gov/articles/PMC4832129/) at a single institution, misspellings accounted for 53% of first-name discrepancies and 33% of last-name discrepancies—the kind of variation that exact matching misses entirely.
- **Search & autocomplete:** Returning relevant results even when users mistype queries. Redis' [Search and Query](https://redis.io/search/) work has long included fuzzy matching support for scenarios like [auto-suggest engines](/blog/adding-search-engine-redis-adventures-module-land/).

In practice, these use cases usually mix fuzzy matching with normalization and other signals, because "close spelling" isn't always the same as "same entity."

## Common fuzzy matching algorithms

Most fuzzy matching algorithms are variations on edit distance: how many edits separate two strings. The right choice depends on what kinds of mistakes you expect (missing letters, swapped letters, fixed-length IDs, etc.).

### Levenshtein distance

Levenshtein distance measures the minimum number of single-character insertions, deletions, and substitutions needed to transform one string into another. For example, "Cristian" → "Christian" has a distance of 1 (insert "h"), and "Power" → "Powder" also has a distance of 1 (insert "d"). This is the distance metric behind Redis Query Engine's [fuzzy term operator](https://redis.io/docs/latest/develop/ai/search-and-query/advanced-concepts/query_syntax/) in full-text search.

### Hamming distance

Hamming distance counts how many positions differ between two equal-length strings or bit vectors, regardless of the underlying encoding. When applied to characters, it compares the binary representation of each position. For example, the binary codes for "N" (1001110) and "L" (1001100) differ in two bit positions, giving a Hamming distance of 2.

This makes Hamming distance useful when you're working with fixed-length data, which is common in error-detection contexts. It's less flexible for names and text search because it can't handle insertions or deletions.

### Damerau-Levenshtein

Damerau-Levenshtein extends Levenshtein distance by also treating a swap of adjacent characters as a single operation. That makes it better at catching common typos like "Micheal" vs. "Michael," where the mistake is a transposition rather than a missing character.

## How to think about accuracy in fuzzy search

Fuzzy matching improves recall, but accuracy depends on context, ranking, and rules, not just string distance. If your threshold is too loose, you'll pull in "close" strings that aren't actually the right result.

In practice, better results usually come from combining fuzzy scoring with normalization. Normalization is the process of cleaning up input before comparison, like converting everything to lowercase, stripping punctuation, and expanding abbreviations so that "St." and "Street" aren't treated as different values. These steps remove surface-level noise so the fuzzy algorithm can focus on real differences rather than formatting quirks.

Many systems also use fuzzy matching as one signal among others, rather than the only way a record can match. Adding domain-specific constraints on top of normalized, fuzzy-scored results helps filter out candidates that are textually close but contextually wrong.

## Fuzzy matching with Redis

Redis supports fuzzy matching in full-text search through the [Redis Query Engine](https://redis.io/resources/redis-query-engine/) (the search and indexing layer available with Redis 8 and later), not the core key-value engine alone. In that full-text layer, fuzzy term queries use Levenshtein distance with a configurable distance of up to 3 edits to match near-miss spellings and typos in indexed text fields.

Fuzzy term matching sits alongside other Redis Query Engine retrieval modes, including full-text operators and [vector search](/blog/vector-databases-101/). For the exact query syntax and limits, the [full-text docs](https://redis.io/docs/latest/develop/ai/search-and-query/query/full-text/) are the source of truth.

## Fuzzy matching & the shift toward hybrid search

Fuzzy matching helps with spelling variation, but it doesn't capture meaning. Two terms can be semantically related while looking nothing alike at the character level, which is a core limitation of edit-distance methods.

That's why many search stacks pair fuzzy matching with vector search: fuzzy matching covers typos and surface variation, while vector embeddings help retrieve semantically similar content. Redis Query Engine supports this style of hybrid querying through the [FT.HYBRID](https://redis.io/docs/latest/commands/ft.hybrid/) command, available in Redis 8.4 and later. FT.HYBRID fuses full-text relevance and vector similarity scores using Reciprocal Rank Fusion or linear combination, all within a single query. You can read more about the design in this [hybrid search post](/blog/revamping-context-oriented-retrieval-with-hybrid-search-in-redis-84/).

This combination shows up often in AI retrieval workloads, including [retrieval-augmented generation (RAG)](/blog/rag-at-scale/) pipelines, where both spelling tolerance and semantic relevance matter.

## Approximate matches, more usable search

Fuzzy matching makes search and record matching more forgiving when your data isn't perfect, which is most of the time. It reduces "no results" failures from typos, small spelling differences, and inconsistent formatting, while still letting you rank candidates by how close they are.

Redis Query Engine is one example of a search layer that includes fuzzy matching alongside full-text and vector search. If you want to try it in practice, you can [try Redis free](https://redis.io/try-free/), or [talk to our team](https://redis.io/meeting/) about what an integrated search layer could look like for your production workload.

## FAQs about fuzzy matching

### What is the difference between Levenshtein distance and Damerau-Levenshtein distance for fuzzy matching?

The key difference is how they handle transpositions. Levenshtein distance treats swapping two adjacent characters (like "teh" → "the") as two separate operations—a deletion and an insertion—giving it a distance of 2. Damerau-Levenshtein counts that same swap as a single operation, giving it a distance of 1.

This makes Damerau-Levenshtein more aligned with how humans actually make typos. Damerau's original 1964 research found that over 80% of misspellings result from a single insertion, deletion, substitution, or transposition. The computational cost is slightly higher than Levenshtein, but for user-facing search interfaces where typo tolerance matters, it's often the better choice.

### How do you set the right fuzzy matching threshold to balance false positives and missed matches?

Start with a threshold based on your data's expected error rate—most teams measure edit distance as a percentage of string length (e.g., one edit per five characters) rather than using a fixed number. Then refine by testing against a labeled dataset and tracking precision (false matches) versus recall (true matches captured).

In production, monitor cases where users reformulate queries after poor results, as this often signals your threshold is too strict. Many systems also use adaptive thresholds or expose similarity scores through result ranking rather than hard cutoffs, letting the application layer make final decisions based on context.

### How does Redis implement fuzzy matching in its full-text search query engine?

Redis implements fuzzy matching through its Redis Query Engine using the % fuzzy term operator. The number of % pairs around a term controls the Levenshtein distance: %term% allows distance 1, %%term%% allows distance 2, and %%%term%%% allows distance 3 (the maximum). The engine uses its indexing to perform efficient distance calculations without scanning every string at search time.

This fuzzy capability can be combined with other Redis Query Engine operators—including exact phrase matching, wildcards, and vector search—within [FT.SEARCH](https://redis.io/docs/latest/commands/ft.search/) and [FT.HYBRID](https://redis.io/docs/latest/commands/ft.hybrid/) queries, making it straightforward to build nuanced search experiences.

### What is hybrid search and how does combining fuzzy matching with vector search improve results?

Hybrid search combines multiple retrieval methods in a single query to cover complementary blind spots. Fuzzy matching handles surface-level variations like misspellings ("machne lerning" → "machine learning"), while vector search captures conceptual similarity between phrases that share no common characters, like "affordable housing" and "low-cost apartments."

This pairing is especially valuable in RAG systems and customer-facing search, where users may misspell terms but still expect semantically relevant results. Many implementations use weighted scoring so you can adjust how much influence each method has on the final ranking.

### What are the best practices for combining fuzzy matching with data normalization to improve accuracy?

Before applying fuzzy algorithms, standardize case, whitespace, and punctuation so that strings like "O'Brien" and "obrien" aren't penalized unnecessarily. You should also remove noise like titles (Dr., Mr.), suffixes (Jr., III), and abbreviations (Street/St.) that inflate edit-distance scores without adding matching value.

For stronger results, consider phonetic normalization (Soundex, Metaphone) to catch sound-alike variations, token reordering so "John Michael Smith" matches "Smith, John Michael," and field-specific weighting where exact matches on high-signal fields like email override weaker fuzzy matches on names.
