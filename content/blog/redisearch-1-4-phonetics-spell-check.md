---
title: "RediSearch 1.4: Phonetics & Spell Check"
linkTitle: "RediSearch 1.4: Phonetics & Spell Check"
url: "/blog/redisearch-1-4-phonetics-spell-check/"
description: "It’s always exciting when a new version of RediSearch comes out—we just released version 1.4 (yes, we skipped 1.3 to align with a new versioning methodology). This new version has two key features..."
date: 2018-08-24
blogCategories:
- "How To and Tutorials"
- "New Product Announcements"
- "Product Releases"
authors:
- "Redis  "
lastmod: 2025-03-04
hidden: true
---

*By Redis   · Published 24 August 2018 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

It’s always exciting when a new version of RediSearch comes out—we just released version 1.4 (yes, we skipped 1.3 to align with a new versioning methodology). This new version has two key features which add quite a bit of smarts to querying:

- Spell Check & Custom Dictionaries
- Phonetic (sound-alike) Matching

## Spell Check

Let’s first take a look at spell check. Everyone knows what spell check is from a broad perspective, but let’s examine how it works in a search engine context. It’s best to think of it as a primitive that would power a “did-you-mean” feature.

Take, for example, this particular query:

> “Hockye stik”

As a human, you probably could know that this means “Hockey stick” but without spell check, the returned results would not be great. Here is how RediSearch 1.4 can help you. First, you run the query through the FT.SPELLCHECK command; it will return nothing (empty list or set) if everything is spelled correctly. If the the query passed into FT.SPELLCHECK has words that seem misspelled, RediSearch will return which words are questionable and some suggestions.

Let’s run that example from above on a populated data set:

```python
127.0.0.1:6379> ft.spellcheck incidents "Hockye stik"
1) 1) "TERM"
   2) "hockye"
   3) 1) 1) "7.3874642939225789e-05"
         2) "hockey"
2) 1) "TERM"
   2) "stik"
   3) 1) 1) "5.7458055619397838e-05"
         2) "stick"

```

Easy enough! Each misspelled word will return “TERM” and the misspelled word, and then any alternatives along with their respective confidence scores, sorted by highest score. The example only has one alternate but you certainly can have more.

Let’s say you have a security guard incident report index created with this command:

```python
127.0.0.1:6379> ft.create incidents SCHEMA report text
OK

```

The feature assumes that any word that exists in the index is spelled correctly (e.g. there is no built-in dictionary of valid words). However, you may have words that you want to assume are spelled correctly that are not yet indexed. This index will contain reports from people involved in security incidents and might have [many slang words](https://theculturetrip.com/north-america/canada/articles/how-to-speak-like-a-torontonian/).

```python
127.0.0.1:6379> ft.spellcheck incidents "Toonie toque kerfuffle"
1) 1) "TERM"
   2) "toonie"
   3) (empty list or set)
2) 1) "TERM"
   2) "toque"
   3) (empty list or set)
3) 1) "TERM"
   2) "kerfuffle"
   3) (empty list or set)

```

(empty list or set) means that the spell check thinks that it is misspelled, but it doesn’t have a correction. To remedy this situation, we’ll add some slang words to a dictionary:

```python
127.0.0.1:6379> FT.DICTADD slang timmies toque toonie serviette kerfuffle chesterfield
(integer) 6

```

Now, we can run a spell check on a query and EXCLUDE these terms. The terminology here is a bit confusing, but think of it as excluding words from being spell checked, e.g. assuming they are spelled correctly.

```python
127.0.0.1:6379>  FT.SPELLCHECK incidents "Toonie toque kerfuffle" TERMS EXCLUDE slang
(empty list or set)

```

The response of (empty list or set) means that all the words in the passed string are not spelled incorrectly. This only gets us so far though. What happens if one of these new words are misspelled? Let’s see.

```python
127.0.0.1:6379> FT.SPELLCHECK incidents "Tooni toque kerfuffle" TERMS EXCLUDE slang
1) 1) "TERM"
   2) "tooni"
   3) (empty list or set)

```

So, the spell check has identified the word is spelled wrong but it doesn’t know how to correct it. To do this, you’ll need to INCLUDE the dictionary as well as EXCLUDE it.

```python
127.0.0.1:6379> FT.SPELLCHECK incidents "Tooni toque kerfuffle" TERMS EXCLUDE slang TERMS INCLUDE slang
1) 1) "TERM"
   2) "tooni"
   3) 1) 1) "0"
         2) "toonie"

```

Now you can see that it’s correcting the spelling.

It’s important to revisit that you don’t need to bother with the custom dictionaries if you already have documents with these terms. Let’s say you have a document like this:

```python
127.0.0.1:6379> FT.ADD incidents report42 1 FIELDS report "Complainant A described that he went to Timmies in his favourite toque, gave the cashier a toonie for his double-double and grabbed for a serviette, while Defendant B tried to steal his hat. Complainant A and Defendant B ended up in a real kerfuffle falling onto the chesterfield."

```

Since this report contains all these slang words, they are automatically populated into the spell check without custom dictionaries, both inclusively and exclusively:

```python
127.0.0.1:6379> FT.SPELLCHECK incidents "toonie tque kerfuffle"
1) 1) "TERM"
   2) "tque"
   3) 1) 1) "1"
         2) "toque"

```

So it’s best to use custom dictionaries for domain-specific terms that haven’t been mentioned in your existing documents yet.

## Phonetic Matching

Phonetic Matching solves the canonical problem of searching for someone named “Jon” but typing it as “Jo**h**n”—sounds the same, but they’re spelled differently. If you want to go down a rabbit hole, try to figure out why both spellings exist as modern English names. I digress.

This is a tricky search problem because even with the tricks that search engines use (like stemming) this doesn’t help. To combat this, search engines can use algorithms that break text down into language-specific codes based on the linguistic pronunciation rules. RediSearch does this using an algorithm called Double Metaphone, which has a fascinating history, look it up sometime.

First you need to define the fields you want to index phonetically (only TEXT fields obviously). Let’s create a small index with two phonetic fields:

So, now we have phonetics enabled as we add documents on both the name and almamater fields. Let’s add some documents:

```python
127.0.0.1:6379> FT.ADD complainants foo64 1 FIELDS name "jon" almamater Trent
OK
127.0.0.1:6379> FT.ADD complainants foo65 1 FIELDS name "john" almamater Toronto
OK

```

When RediSearch adds the documents to the index, it isn’t just recording “jon” or “john,” it’s recording both with their metaphone codes. In this case, both “jon” and “john” translate into JN. To search for these you’ll just need to search on a specific field that is denoted as PHONETIC.

```python
> FT.SEARCH complainants "@name:john"
1) (integer) 2
2) "foo64"
3) 1) "name"
   2) "jon"
   3) "almamater"
   4) "Trent"
4) "foo65"
5) 1) "name"
   2) "john"
   3) "almamater"
   4) "Toronto"

```

See how this is matching both “john” and “jon”? This is because they have the same Double Metaphone translation. At this point, you may be dancing at your desk at the wonder that is phonetic matching in a search engine. All of your problems are solved!

Not so fast—phonetic matching should be used carefully. It’s a very sharp tool, but it can cut you. Let’s take for example the second field in our micro-example:

```python
127.0.0.1:6379> FT.SEARCH complainants "@almamater:trent"
1) (integer) 2
2) "foo65"
3) 1) "name"
   2) "john"
   3) "almamater"
   4) "Toronto"
4) "foo64"
5) 1) "name"
   2) "jon"
   3) "almamater"
   4) "Trent"
127.0.0.1:6379> FT.SEARCH complainants "@almamater:toronto"
1) (integer) 2
2) "foo64"
3) 1) "name"
   2) "jon"
   3) "almamater"
   4) "Trent"
4) "foo65"
5) 1) "name"
   2) "john"
   3) "almamater"
   4) "Toronto"

```

“Trent” and “Toronto” look and sound nothing alike! This not a bug, but rather a weakness in the Double Metaphone algorithm that takes away some information and emphasizes others. Metaphone should be used carefully on fields that are likely to not contain sound-alikes. You can also use an attribute to turn off phonetic searching:

```python
127.0.0.1:6379> FT.SEARCH complainants "@almamater:(toronto=>{$phonetic:false})"
1) (integer) 1
2) "foo65"
3) 1) "name"
   2) "john"
   3) "almamater"
   4) "Toronto"

```

RediSearch 1.4 has some exciting features that add gobs of flexibility to search. These features get at the heart of what a good search engine does: it accommodates human error without losing sight of the user’s true intention.
