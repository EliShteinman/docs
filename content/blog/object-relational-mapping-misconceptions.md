---
title: "3 Common Misconceptions About Object-relational Mapping"
linkTitle: "3 Common Misconceptions About Object-relational Mapping"
url: "/blog/object-relational-mapping-misconceptions/"
description: "Most software developers are familiar with object-relational mapping (ORM), a coding technique that creates an abstraction layer between object-oriented programming languages and databases. But..."
date: 2022-09-13
blogCategories:
- "Tech"
- "Uncategorized"
authors:
- "William Johnston"
lastmod: 2025-03-27
hidden: true
---

*By William Johnston, Head of Technical Marketing · Published 13 September 2022 · updated 27 March 2025*

![Blog tile image](/images/blog/c62c6dcbcbc44e5ac575796389cb916ef572c99f-772x550.webp)

**Most software developers are familiar with ****object-relational mapping**** (ORM), a coding technique that creates an abstraction layer between object-oriented programming languages and databases. But despite its value, ORM isn’t ideal in all situations – particularly when programmers make wrong assumptions about its use. We debunk several such mistaken beliefs so that you can use ORM the right way.**

---

Don’t get the wrong message: We appreciate ORMs. Redis supports the technology enthusiastically, with support for several programming languages. But it’s important to get off on the right foot.

In its purest form, an ORM serves as a translator that bridges systems. They offer a lot of flexibility by allowing programmers to streamline communications through their preferred programming language rather than relying directly on Structured Query Language (SQL) or other database-specific languages. Because systems often depend on different programming languages and store data differently, it’s all too easy to insert complexity. Without ORMs, many object-oriented applications would struggle to communicate with databases.

Still, programmers can get misguided about the role of ORMs, which leads to confusion and sometimes frustration.

These three misconceptions can prevent you from using ORMs correctly and getting the most benefit from the technology. That’d be a shame.

## 1. Because ORMs obfuscate interactions with the database, you don’t need to know SQL

Surely you’re familiar with SQL, the standardized language for storing, manipulating, and retrieving data in a relational database. You interact with the database using specific queries: INSERT, SELECT, UPDATE, DELETE, DROP TABLE, and so many more.

ORMs help programmers to interact with databases in their preferred language (say, Python) rather than by manually writing SQL queries from scratch. That’s a significant plus. With an ORM, data is modeled in a structured way, which helps programmers interact with the database’s layout and content.

You don’t have to use SQL, as the ORM does a lot of work for you. That saves time and energy, particularly for people who don’t know SQL or lack confidence in their skills. Only 56.9% of developers use SQL worldwide, according to a 2020 StackOverflow survey. But a shortcut is not the same thing as a justification for ignorance. Some developers assume that “I don’t need to know SQL in depth” is the same as “Learning database concepts is unnecessary because ORMs do everything, from start to finish.”

This is not true.

ORMs are great for straightforward SQL queries. However, when you do anything complex, you need to know what SQL can do to wring the last bit of functionality out of it. This shouldn’t be a surprise. You do the same with other development tools. Tools are supposed to support our work, not replace our understanding.

Yet, developers sometimes generalize, “I have a tool that helps me” into “If you have a tool, you don’t need to know anything about database design.” High-level abstractions don’t always write the best code. They are susceptible to errors, and you need to understand SQL to recognize when that’s the case. If you don’t understand SQL, debugging, tuning for performance, or collating complex data becomes more tedious and frustrating.

Knowing SQL gives you more control over your application and allows you to tune SQL queries to optimize performance. Use ORMs to help you work faster– not to keep you from thinking.

## 2. The only function an ORM offers is writing SQL code

Some anti-ORM folks adopt the attitude that it’s always better to write SQL queries yourself. They assume that the only functionality ORMs offer is to write the SQL code.

But the software goes beyond writing queries. The ORM gets involved with the object-oriented model and how data moves between the database and that model; this is orthogonal to actually writing SQL queries.

ORMs also promote code maintainability and reuse, as they enable the developer to think in terms of objects instead of atomized pieces of data.

## 3. If you use ORMs, you don’t have to worry about database security

The result of a SQL injection can be catastrophic, leading to unauthorized database access. Fortunately, ORMs are more effective in shielding applications from SQL injection attacks. They can map objects and actions into database-related code, so you don’t have to manually write security-specific code.

However, “it helps” is not the same as “…so it’s foolproof.” ORM packages do not make your database application immune from a cyber security attack. As with any software, ORM can have bugs (even Hello World is vulnerable), leaving data-driven applications exposed to another area of attack.

The primary way ORMs shield against SQL injection attacks is by using parameterized queries. However, not all ORMs work this way. Before you assume a particular ORM is safe, you should at least verify how it translates your actions into SQL.

For better protection, implement all the database security techniques you would employ if the code was written by hand. No matter how the application is created, make sure that your software QA process includes a full security test suite (not only for SQL injection attacks). ORMs may reduce the likelihood of security vulnerabilities, but it’s best to be safe.

## Does Redis have an ORM?

At Redis, we’re enthusiastic about any tool that makes application development faster, more accurate, and more effective – leaving the programmer to contemplate innovative ways to help a data-driven application better serve its users. So sure, we’re fully behind ORMs. They promote code reusability and provide a cleaner separation in the data access layer.

The Redis OM client Libraries introductionexplains how object mappers help you get the most out of Redis’ modules. Redis OM’s goal is to provide a toolbox of high-level abstractions that make it easy to work with Redis data in the programming environments with which you’re most familiar. It contains four high-level client libraries for Redis, which we invite you to explore:

- Redis OM for .NET
- Redis OM for Node.JS
- Redis OM for Python
- Redis OM for Spring

Looking for definitions to other related concepts? Check out our glossary section.
