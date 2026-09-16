---
title: "Databases"
linkTitle: "Databases"
url: "/glossary/databases/"
description: "Today, data is a speed game. You’ve probably heard the stat that 90% of all data created since the dawn of time has been created within the last two years. As data has exploded, sprawled, and eaten..."
lastmod: 2025-06-30
mirrored: true
---

*updated 30 June 2025*

Today, data is a speed game. You’ve probably heard the stat that [90% of all data](https://explodingtopics.com/blog/data-generated-per-day) created since the dawn of time has been created within the last two years. As data has exploded, sprawled, and eaten the world, we’ve moved from talking about Big Data (“Wow, there’s so much of it!”) to talking about how we can better make use of that data (“What does it all mean?”). 

How we make use of that data depends on how quickly and easily we can store, access, and query it. This is where databases come in.

But what exactly is a database, and why has this technology become so indispensable in today’s software-led business environment? Let’s dive into the dizzying world of databases, exploring their origins, the key types, and how they can be used to push the frontiers of what is possible.

## What is a database?

A database is a structured collection of information that is stored electronically. You can think of a database as a digital library, where instead of books, you have data. This data can range from a simple list of customer names and contact information to complex transactional records for multinational corporations to vector databases that store unstructured data for AI applications.

Related content: [Redis as a Cache vs Redis as a Primary Database](/blog/redis-cache-vs-redis-primary-database-in-90-seconds/)

### Evolution of databases

The concept of databases isn’t new. Long before the advent of computerized databases, people used physical filing systems—cabinets filled with folders, ledgers, and records. However, as businesses grew and technology advanced, the need for (and benefits of) a more efficient, electronic method to store and manage vast amounts of data became evident.

The 1960s and 1970s saw the birth of the first electronic database models, which were primarily hierarchical and navigational. The real revolution came with the introduction of the relational database management system (RDBMS) in the late 1970s, championed by Dr. Edgar F. Codd. RDBMS introduced the concept of tables (relations) where data could be stored and efficiently queried using a database access language called structured query language (SQL).

### Database prevalence

In today’s digital age, databases are everywhere. Every time you make an online purchase, book a flight, or even like a post on social media, you’re interacting with a database. They ensure that the digital services we rely on daily run smoothly, storing vast amounts of data that can be quickly retrieved and analyzed. Databases play a pivotal role in:

- **E-commerce**: Storing product information, customer details, and transaction records.
- **Healthcare**: Maintaining patient records, treatment histories, and drug information.
- **Banking**: Managing account details, transaction histories, and credit scores.
- **Social media**: Keeping track of user profiles, posts, likes, and connections.

## Why are databases important?

In the digital realm, data can be likened to oil—a valuable resource that powers modern businesses, technologies, and innovations. Database management systems (DBMS), as structured repositories of this data, play a pivotal role in harnessing its potential. But why exactly are databases so crucial?

- **Centralized storage**: One of the primary advantages of databases is their ability to centralize data storage. Instead of scattering information across multiple files or systems, databases provide a single location where data can be stored, updated, and retrieved. This centralization not only simplifies database management but also ensures data consistency and data integrity.
- **Efficient data retrieval**: Speed is of the essence in the digital age. Databases, with their complex queries, are optimized for quick data retrieval, ensuring that applications and services can access the required information in real time.
- **Data security and integrity**: Databases come equipped with robust security mechanisms to safeguard data. From user authentication protocols to encryption techniques, database systems ensure that sensitive information remains protected from unauthorized access.
- **Scalability and flexibility**: Modern databases are designed to scale. As businesses grow and data volumes increase, databases can be expanded to accommodate this growth without compromising performance. Additionally, databases offer flexibility, allowing organizations to tailor their data structures and storage strategies to meet specific needs.
- **Data relationships and analysis**: Databases, especially relational ones, excel at establishing relationships between different data sets. This ability to interlink data allows for complex querying and analyses, providing businesses with valuable insights.
- **Support for transactional operations**: Databases are integral to supporting transactional operations, ensuring that data remains consistent even in the face of multiple simultaneous transactions.

## How a database works

The magic of databases lies in their ability to store, organize, and retrieve vast amounts of structured data with remarkable efficiency. But what mechanisms and processes underpin these capabilities? In this section, we’ll peel back the layers of an RDBMS to understand the inner workings of databases.

### Basic architecture and components:

Databases are more than just storage bins for data. For example, an RDBMS is a complex system with multiple components working in tandem:

- **Database engine**: The core component responsible for data storage, retrieval, and management. It processes SQL queries, fetches data from storage, and ensures data integrity and security.
- **Tables**: Fundamental storage structures, tables store data in rows and columns, much like a spreadsheet. Each table is designed to store specific types of data type, such as customer details or product information.
- **Indexes**: These are data structures that improve the speed of data retrieval operations on a database system. By creating pointers to data, indexes allow databases to skip directly to the data’s location, bypassing the need to scan every row.

### Data storage, retrieval, and manipulation:

The essence of a database’s functionality revolves around these three operations:

- **Storage**: When data is input into a database, it’s stored in tables. The database engine determines the optimal location for storage, ensuring efficient retrieval later.
- **Retrieval**: When a user or application requests data, the database engine parses the request, identifies the location of the data using indexes, and fetches it.
- **Manipulation**: Databases enable data manipulation through operations like insertion, updates, and data deletion. These operations are executed while ensuring data integrity and consistency.

### Query processing:

Databases use a specific language for data operations, most commonly SQL. When a SQL query is submitted:

- **Parsing**: The database engine breaks down the SQL query to understand its intent.
- **Optimization**: The engine determines the most efficient way to execute the query, often using indexes to speed up data retrieval.
- **Execution**: The optimized query is run, and the results are returned to the user or application.

### Concurrency and transactions:

Databases often cater to multiple users or applications simultaneously. To manage this, they have:

- **Concurrency control**: Databases use mechanisms like locking to ensure that multiple operations don’t conflict with each other.
- **Transactions**: A transaction is a sequence of one or more SQL operations executed as a single unit. Databases ensure that transactions are completed in their entirety (commit) or not at all (rollback) to maintain data integrity.

### Backup and recovery

Databases are equipped with backup and recovery mechanisms to safeguard against data loss.

- **Backup**: Regular snapshots of the database are taken and stored securely. These backups can be used to restore the database in case of failures.
- **Recovery**: In the event of system crashes or failures, databases use transaction logs to recover and restore data to its last consistent state.

## Different types of databases

The world of databases is vast and varied, with different types designed to cater to specific needs, from handling structured business data to managing vast amounts of unstructured information. In this section, we’ll explore the diverse landscape of database types and understand their unique characteristics and use cases.

### Relational databases:

The most common type of database, relational databases, store data in structured tables with rows and columns. They use SQL for querying and are known for being sturdy and reliable.

- **Characteristics**: Data integrity, [ACID properties](https://redis.io/glossary/acid-transactions/), use of primary and foreign keys to establish relationships.
- **Popular examples**: Oracle, MySQL, Microsoft SQL Server.
- **Use cases**: Business applications, CRM systems, e-commerce platforms.

### NoSQL databases

Non-relational databases, also called [NoSQL databases](https://redis.io/nosql/what-is-nosql/), emerged to address the limitations of relational databases, especially when dealing with large volumes of unstructured data or real-time applications. Types of NoSQL databases include:

- **Document-based**: Document databases store data in [document-like structures.](https://redis.io/nosql/document-databases/) Ideal for hierarchical data. Example: MongoDB.
- **Key-value stores**: These simple databases store data as [key-value](https://redis.io/nosql/key-value-databases/) pairs, making them highly scalable and fast. Example: Redis.
- **Columnar databases**: Column-oriented databases are designed for storing and querying large datasets. Data is stored in columns rather than rows. Example: Cassandra.
- **Graph databases**: [Graph databases](https://redis.io/glossary/graph-database/) are designed for data with intricate relationships, like social networks. Example: Neo4j.
- **Time series databases**: [Time series databases](https://redis.io/nosql/timeseries-databases/) are specifically designed to handle time-stamped data, like logs or sensor data.

![NoSQL Database](/images/site-mirror/58d70d0ccd01c3005c0a0bdc9f13519d2e28a086-787x253.svg)

### Cloud databases

Databases hosted on cloud platforms, offering scalability, flexibility, and cost-effectiveness.

- **Characteristics**: On-demand scalability, managed backups, global distribution.
- **Popular examples**: Amazon RDS, Google Cloud SQL, Azure SQL Database.
- **Use cases**: Startups to large enterprises looking for cost-effective database solutions without the hassle of physical infrastructure management.

### Event store databases

Designed to store sequences of events or transactions, useful for systems based on event sourcing.

- **Characteristics**: Immutable logs, event replay capabilities.
- **Popular examples**: Event Store, [Kafka](https://redis.io/compare/redis-enterprise-and-kafka/).
- **Use cases**: Audit trails, [real-time analytics](https://redis.io/docs/real-time-analytics-redis/), system monitoring.

### Multi-model databases

These databases combine features of multiple database types, offering flexibility in data storage and querying.

- **Characteristics**: Supports [multiple data models](https://redis.io/redis-enterprise/multi-model/), like document, graph, and key-value.
- **Popular examples**: ArangoDB, OrientDB.
- **Use cases**: Applications requiring varied data storage and retrieval methods.

## Database management systems (DBMS)

Behind every effective database lies a powerful system responsible for its management, organization, and security. This system, known as the DBMS, plays a pivotal role in ensuring that databases operate optimally. In this section, we’ll delve into the world of DBMS, exploring its functions, types, and significance in the realm of databases.

### What is a DBMS?

A DBMS is specialized software designed to interact with the user, applications, and the database itself to capture, store, and analyze structured data. It provides a systematic way to manage large amounts of data using a clear and structured framework.

### Core functions of a DBMS

- **Data storage and data management**: The DBMS is responsible for storing data in a structured manner, ensuring efficient retrieval and updates.
- **Data retrieval**: Using a querying language like SQL, a DBMS fetches data for applications and users based on specific criteria.
- **Data security**: A DBMS offers robust security mechanisms, from user authentication to encryption, ensuring that data remains protected from unauthorized access.
- **Data integrity and accuracy**: By enforcing data constraints and validation rules, a DBMS ensures the accuracy and reliability of data.
- **Backup and recovery**: The DBMS regularly backs up data, ensuring that in the event of failures, data can be restored without loss.
- **Concurrency control**: In multi-user environments, a DBMS manages simultaneous data access, ensuring data consistency and preventing conflicts.

### Types of DBMS

- **Hierarchical DBMS**: Data is structured in a tree-like model, with parent-child relationships. This is one of the earliest types of DBMS.
- **Network DBMS**: Similar to hierarchical but allows many-to-many relationships, forming a web-like structure.
- **Relational database management systems**: A RDBMS uses tables to store data and establish relationships. Examples include Oracle, MySQL, and SQL Server.
- **Object-oriented relational DBMS**: Combines the principles of RDBMS with object-oriented programming, allowing for the storage of objects.
- **NoSQL DBMS**: A non-relational DBMS designed for large volumes of rapidly changing data. Types include document, key-value, columnar, and graph databases.

### Choosing the right DBMS

The choice of a DBMS depends on several factors:

- **Data volume and velocity**: For large, rapidly changing datasets, NoSQL databases might be more appropriate.
- **Data structure**: If data is structured and relational, an RDBMS is typically the best choice.
- **Scalability needs**: Cloud-based DBMS solutions offer on-the-fly scalability for growing datasets.
- **Budget and licensing**: Open-source DBMS options can be cost-effective, while proprietary systems might offer specialized features at a premium.

## Database security

In an era where data breaches and cyberattacks are increasingly common, the security of databases has never been more important. Database security encompasses a range of measures, protocols, and tools designed to protect databases from unauthorized access, threats, and malicious attacks. In this section, we’ll explore the importance of database security, the potential threats faced, and the strategies employed to safeguard data.

### Why is database security crucial?

Databases often house sensitive and critical information, from personal user details to confidential business data. A security breach can lead to:

- **Data theft**: Unauthorized access can result in the theft of valuable data, which can be sold or misused.
- **Data loss**: Malicious attacks can lead to data being altered or deleted entirely.
- **Reputation damage**: Data breaches can tarnish an organization’s reputation, leading to a loss of trust among clients and customers.
- **Financial repercussions**: Breaches can result in hefty fines, especially with data protection regulations like GDPR in place.

### Common database security threats

- **SQL injection**: A technique where malicious SQL code is inserted into a query to manipulate the database.
- **Unauthorized access**: Gaining access to the database without proper authentication.
- **Denial-of-service (DoS) attacks**: Overloading the database with requests, rendering it unavailable.
- **Data tampering**: Unauthorized alteration of data.
- **Malware and ransomware**: Malicious software that can corrupt, steal, or hold data hostage.

### Database security best practices

Here are some best practices to help secure your databases:

- **User authentication and authorization**: Ensure that only authorized individuals can access the database. Implement strong password policies and multi-factor authentication.
- **Data encryption**: Encrypt data both at rest and in transit to ensure that even if data is intercepted, it remains unreadable.
- **Regular backups**: Regularly back up the database to ensure that data can be restored in the event of a breach or failure.
- **Network security**: Implement firewalls, intrusion detection systems, and secure communication protocols to protect the database from network-based threats.
- **Regular audits and monitoring**: Continuously monitor database activity, logging all access and changes. Regularly audit the logs to detect any suspicious activity.
- **Patch management**: Regularly update and patch DBMS software to protect against known vulnerabilities.

## Data integrity and consistency

Data integrity and consistency are foundational principles in the realm of databases. They ensure that data remains accurate, reliable, and valid throughout its lifecycle.

### Understanding data integrity

Data integrity refers to the accuracy and consistency of data stored in a database. It ensures that data remains unchanged and uncorrupted from its source and is delivered in its original form without any unintended alterations.

### Why is data integrity crucial?

- **Reliable decision-making**: Accurate data is essential for making informed decisions. Any inconsistencies can lead to misguided strategies and actions.
- **Regulatory compliance**: Many industries have strict data integrity standards. Non-compliance can result in penalties and legal repercussions.
- **Trustworthiness**: Ensuring data integrity fosters trust among stakeholders, clients, and customers.
- **Operational efficiency**: Consistent and accurate data reduces errors, streamlines operations, and enhances overall efficiency.

### Challenges to Data Integrity

- **Human errors**: Mistakes during data entry, updates, or deletions can compromise data integrity.
- **Software bugs**: Faulty applications or system glitches can inadvertently alter data.
- **Malicious attacks**: Cyberattacks can corrupt, delete, or alter data.
- **Hardware failures**: Physical damages, like disk failures, can lead to data corruption.

### Maintaining Data Integrity

- **Validation rules**: Implement rules that ensure only valid data is entered into the database.
- **Constraints**: Use database constraints, like primary keys and unique constraints, to maintain data uniqueness and relationships.
- **Regular audits**: Periodically review and audit data to detect and correct inconsistencies.
- **Backup and recovery**: Regular backups ensure that data can be restored to its original state in case of corruption or loss.

## What is the CAP theorem?

In researching database options, you might come across the CAP theorem. The CAP theorem posits that with a modern database system, it’s impossible to maintain all three of the following properties at once:

- **Consistency**: Users see the same, most up-to-date data at the same time. If you query one node then another, both would show the same result.
- **Availability**: The system always responds to requests, even if some parts are down or some data is not up to date.
- **Partition tolerance**: The system continues to work even when network issues occur between its parts.

At most, the theorem holds, it’s possible to maintain two of these properties. Often, database systems are classified by which two properties they maintain:

- **Consistency and partition tolerance (CP):** The system will return the most recent data or an error if it can’t ensure consistency across all nodes.
- **Availability and partition tolerance (AP):** The system will always respond, but the data might not be the most up-to-date. In other words, giving up consistency means you and another user may see different values at the same time. 
- **Consistency and availability (CA):** The system will serve the latest data and will be available as long as there are no network partitions. This combination is rarely used in distributed systems because partition tolerance is usually necessary to avoid system failure or unpredictable behavior.

The CAP theorem is important because it helps companies think through what properties are most important for their business applications and select a database that fits those requirements.

It’s also important to note that while AP and CP systems are most common, most database systems today do their best to balance these properties depending on different situations and requirements.

### In the context of the CAP theorem, what kind of system is Redis?

In general, Redis is considered a CP system, where consistency and partition tolerance are prioritized over availability. The biggest risk with a CP system is that data won’t be available in certain scenarios.

However, Redis does have high availability when not using Redis Cluster. For example, [Redis Sentinel](https://redis.io/docs/latest/operate/oss_and_stack/management/sentinel/) provides high availability, as well as other collateral tasks such as monitoring and notifying, as well as acting as a configuration provider for clients.

## Using SQL vs NoSQL databases

Traditionally, [relational and non-relational databases](https://github.com/dotnet/docs/blob/main/docs/architecture/cloud-native/relational-vs-nosql-data.md) are the two most common types of databases that a company will need to choose between. Which database type you pick will depend on factors such as your specific application requirements, data characteristics, scalability needs, and more. 

### When should you use a SQL database?

As we mentioned earlier, a relational or SQL database is the most common choice. You should use a SQL database when:

- **Data structure is consistent:** SQL databases work best with structured data that fits neatly into predefined schemas and tables. 
- **Data growth is predictable:** If your data can fit on a single node, or if your data growth is predictable and can be handled by upgrading a single server, then SQL’s vertical scaling makes it an efficient choice. 
- **You need complex queries:** SQL databases do well maintaining and querying relationships between different data entities. SQL excels at handling complex queries, joins, and transactions across multiple tables. Choose SQL if there are many distinct entities with complex foreign key relationships. 

### When should you use a NoSQL database?

Certain NoSQL databases are optimized for particular scenarios, like graph databases for relationship-heavy data or key-value stores for caching. A NoSQL database might be a good fit your your business in the case of the following:

- **Data is unstructured or semi-structured:** NoSQL databases can efficiently handle various data types, including documents, key-value pairs, and graphs.
- **Storing and handling big data:** NoSQL databases are designed for horizontal scalability, making them suitable for big data applications and high-traffic websites. Choose NoSQL if your data needs are beyond the scope of the production database that holds essential user data. 
- **Flexibility is a top priority:** NoSQL databases offer dynamic schemas, allowing for easy adaptation to changing data structures without migrations. This makes them ideal for diverse applications, such as machine learning applications or highly performant caching operations. 

Redis is an in-memory datastore best known for caching. You can deploy different [caching patterns](https://redis.io/learn/howtos/solutions/microservices/caching)—such as cache prefetching or cache-aside pattern—to speed up database queries while keeping costs low.

Learn more about how to use [Redis for query cachin](https://redis.io/solutions/caching/)g.

## Powering past, present, and future innovation

From physical filing systems to on-premise servers and today’s innovative hybrid cloud models, database solutions have evolved considerably in recent decades to power many of today’s most advanced technologies. This progress allows companies to choose from a wide array of database services and solutions to power their critical applications.

[Try Redis for free](https://redis.io/try-free/) to see the power of our data platform in your tech stack.
