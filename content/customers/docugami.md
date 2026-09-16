---
title: "Docugami drives AI accuracy at scale with Redis"
linkTitle: "Docugami drives AI accuracy at scale with Redis"
url: "/customers/docugami/"
description: "Docugami needed a distributed services architecture that could enable its patented AI to process large workloads with exceptional accuracy, extremely fast response times, and at an affordable cost..."
group: "Technology"
lastmod: 2026-06-04
hidden: true
mirrored: true
---

*updated 4 June 2026*

###### The Challenge

Docugami needed a distributed services architecture that could enable its patented AI to process large workloads with exceptional accuracy, extremely fast response times, and at an affordable cost to let customers directly interact with their own long-form documents in real-time.

Docugami’s use of Redis has expanded dramatically over time. Initially, after experiencing performance and latency challenges with its Apache Spark data processing environment, Docugami sought a solution to store Spark checkpoint data in a cache to speed up processing and reduce COGS.

The company also needed a vector database that could accelerate essential generative AI tasks such as retrieval-augmented generation (RAG), in-context learning (ICL), and vector search.

> “Docugami provides unsurpassed accuracy in AI for business documents. Built for business users, Docugami’s proprietary Business Document Foundation Model, a deep and patented stack with agentic quality control, uses multiple and frequently updated state-of-the-art open-source LLMs to generate knowledge graphs that capture all of the information in complex business documents. Redis is the cornerstone of our service infrastructure, helping us to deliver Docugami’s enterprise-ready industry-leading precision and accuracy at scale, with exceptional response times and affordability.”

###### Solution

Redis provides a comprehensive data management platform that supports virtually every aspect of Docugami’s distributed services architecture. Redis also provides a vector store for Docugami’s ML pipelines in conjunction with auto tiering to extend databases beyond DRAM, document indexing, and AI-powered search capabilities.

###### RESULTS

Redis enables Docugami to process items at a speed and scale that makes it possible for customers to experience real-time interaction with their libraries of long-form documents at massive scale. Redis has also enabled Docugami to eliminate its reliance on Apache Spark and other services, resulting in significant cost savings and streamlining operations. Redis has made it easy to store, search, and update vector embeddings at scale, improving the user experience by ensuring that Docugami’s foundation model receives the most timely, relevant and up-to-date context.

### Powering AI-powered business documents at scale

According to a May 2024 report by Microsoft, 75 percent of today’s knowledge workers use generative AI systems for their work [[1](https://www.microsoft.com/en-us/worklab/work-trend-index/ai-at-work-is-here-now-comes-the-hard-part)]. Docugami is on the crest of this rising wave with a unique family of large language models (LLMs) that can be applied to corporate business documents with the accuracy, efficiency, and security that enterprises demand.

Docugami’s proprietary Business Document Foundation Model unlocks the critical data and information in corporate documents and uses it to generate reports, uncover insights, create new documents, and develop data streams for enterprise apps—all without requiring clients to invest in machine learning, staff training, or IT development.

“Docugami provides unsurpassed accuracy in AI for business documents. Built for business users, Docugami’s proprietary Business Document Foundation Model, a deep and patented stack with agentic quality control, uses multiple and frequently updated state-of-the-art open source LLMs to generate Knowledge Graphs that capture all of the information in complex business documents,” says Jean Paoli, CEO of Docugami. “Redis is the cornerstone of our service infrastructure, helping us to deliver Docugami’s enterprise-ready industry-leading precision and accuracy at scale, with exceptional response times and affordability.”

The process begins by ingesting a client’s internal data and business documents. For an insurance company, that might include policies and claims. For a commercial real estate firm, documents would include listing agreements, purchase agreements, and bills of sale. Docugami creates a hierarchical representation of the content of each document in its entirety, known as a knowledge graph, which allows its LLMs to assemble new documents, generate insights, and identify key data that can drive line-of-business systems.

Docugami’s AI algorithms convert the output of this process into “chunk embeddings” and store them in Redis. Embeddings are numeric representations of unstructured data that capture semantic information. Redis vector capabilities enable Docugami to capture, search, and update these embeddings at scale.

Redis is also used for chat-based retrieval from business documents, which are maintained as XML knowledge graphs. This functionality not only improves Docugami’s ability to understand the relevance of each document, but also accelerates the feedback loop when users query the LLMs, enhancing the overall user experience.

Redis is heavily integrated into Docugami’s document processing workflows. The architecture ensures that documents can be processed and data can be generated in real-time, driving business logic and workflows. This is especially critical for ensuring that the models Docugami builds remain responsive and can be applied to ongoing and future business operations.

Docugami is progressively porting their entire service to Redis. This shift reflects their confidence in Redis’ ability to handle growing workloads, ensuring scalability as the company expands its offerings.

“We initially began using Redis Enterprise to help improve our Apache Spark document processing pipeline and enhance semantic search for our document chunk embeddings,” says Mike Palmer, co-founder and head of technologies at Docugami. “As we’ve gotten to know more about its capabilities, we’ve migrated more and more of our mission-critical functions to Redis, and we’ve been consistently impressed with its power, performance, resilience and cost-effectiveness. At this point, I cannot imagine building a distributed services architecture without Redis.”

### Finding greater speed and responsiveness with Redis

Foundation models are the cornerstone of generative AI apps because they enable companies like Docugami to build specialized, domain-specific systems that put today’s AI and ML technologies to work. Docugami had used Apache Spark for its document processing and analytics pipeline, but Spark’s “chatty” architecture required excessive I/O operations, which over-stressed the storage layer. Docugami found that even small scheduling delays made the system feel unresponsive to users.

Docugami transitioned to Redis to handle the delays they were experiencing. Redis dramatically improved performance, providing sub-second response times, enabling Docugami to process work items at speeds that feel interactive to the end-user.

“Our new architecture powered by Redis facilitates the rapid processing of tasks at scale, enabling the real-time interactions that our customers expect, particularly as they are chatting with their document data,” Mike Palmer says [[2](https://www.docugami.com/blog/redis)].

Redis simplifies the Docugami architecture by supplying one software solution to solve many unique technology problems. For example, Docugami uses Redis as a vector store for its ML pipelines to reclaim space occupied by deleted or outdated data. Flex allows Docugami to efficiently process extremely large data sets that are too big to fit in memory.

### The right vector database for LLMs

More than 80 percent of today’s business data is unstructured, stored as text, images, audio, video, and other formats. To discern the inherent patterns, terminology, and relationships in this data, Docugami’s generative AI solutions employ a variety of popular techniques such as retrieval-augmented generation (RAG), in-context learning (ICL), and few-shot prompting with patented techniques combining them to create Docugami’s XML knowledge graphs.

Redis complements and extends these generative AI techniques. For example, Docugami uses Redis as a persistent, hierarchical database for storing documents in domain-specific knowledge bases as part of the generative AI process. Redis enables AI-powered search capabilities such as vector search, which use deep learning and other advanced techniques to answer queries based on a contextual understanding of the content.

In addition, Redis RAG capabilities enable Docugami’s foundation model to access up-to-date or context-specific data, improving the accuracy and performance of queries and searches. Redis also provides powerful hybrid semantic capabilities to infuse relevant contextual data into user prompts before they are sent to the LLM.

Finally, Redis stores external domain-specific knowledge to improve the quality of search results from Docugami’s Document XML knowledge graph. This capability allows people to search unstructured data using natural language prompts. “Through Redis, we’ve seen a dramatic increase in the performance of our Document XML knowledge graph and a notable reduction in costs,” Palmer says. “These operational improvements have facilitated a more efficient, reliable document processing workflow.”

> "We initially began using Redis to help improve our Apache Spark document processing pipeline and enhance semantic search for our document chunk embeddings. As we’ve gotten to know more about its capabilities, we’ve migrated more and more of our mission-critical functions to Redis, and we’ve been consistently impressed with its power, performance, resilience and cost-effectiveness. At this point, I cannot imagine building a distributed services architecture without Redis."

### Powering advanced retrieval-augmented generation (RAG)

Docugami is one of the leaders in a promising area of AI, known as retrieval-augmented generation (RAG). One of the biggest concerns about standard Generative AI is the propensity of many models to invent inaccurate information in response to user prompts, a process sometimes called “hallucinations.” Such inaccuracies are unacceptable in a critical business setting, so Docugami is laser-focused on techniques that ensure accuracy and validity that customers can rely on.

Instead of solely relying on pre-trained LLM models to generate results, RAG retrieves relevant information from the user’s documents or external knowledge bases, integrating it into the generation process. This improves the model’s accuracy, making responses more context-aware and factually grounded.

Docugami’s KG-RAG (Knowledge graph-RAG) outperforms other RAG approaches because it uses exclusive hierarchical semantic chunking to create a comprehensive XML knowledge graph from an organization’s own unstructured documents in their entirety, which can then be used as the basis for augmenting query responses, enabling far more accurate RAG.

Redis supports Docugami’s RAG execution in a variety of ways. First, Redis excels at high-performance, low-latency data retrieval, which is crucial for RAG pipelines. In a RAG system, previously confirmed internal information or external knowledge is typically fetched from a database or vector store to augment the generative model’s responses.

Redis can act as a vector database, storing embeddings of documents, knowledge bases, or business-related content. When the LLM queries this knowledge during the generation process, Redis quickly retrieves the most relevant vectors nearly instantaneously, providing the sub-second responses essential for interactive AI applications like chatbots or document generation systems.

### Building with exceptional RAG capabilities

Docugami is one of the leaders in a promising area of AI, known as retrieval-augmented generation (RAG). One of the biggest concerns about standard Generative AI is the propensity of many models to invent inaccurate information in response to user prompts, a process sometimes called “hallucinations.” Such inaccuracies are unacceptable in a critical business setting, so Docugami is laser-focused on techniques that ensure accuracy and validity that customers can rely on.

1. Redis’ native support for vector similarity search makes it a powerful tool in RAG architectures, allowing LLMs to efficiently pull in context from vast repositories of documents, articles, or business data.
1. Redis’ caching capabilities also enhance RAG systems by storing frequently retrieved data. In a scenario where similar queries are made multiple times (e.g., FAQs, repeated business inquiries), Redis can cache those retrieval results, speeding up the entire process by bypassing redundant database calls.
1. Redis supports more complex workflows in RAG implementations, particularly when documents or data sources are spread across multiple databases or systems. Using Redis as a federated caching layer, businesses can unify different caches or data stores into a single, cohesive data access point.
1. Redis offers high scalability for RAG architectures, ensuring that as the amount of data or the number of queries grows, the system can handle these increased workloads without a degradation in performance.
1. Redis can serve as a fast, real-time data layer during the training or fine-tuning of AI models in a RAG system. As AI models improve through retrieval-augmented generation, they often need to be updated with new data or insights in real-time. Redis can manage this inflow of new data, ensuring the model is trained or fine-tuned with the most up-to-date and relevant information.
1. Redis supports real-time feedback loops in interactive RAG-based applications. As users interact with the system, Redis can immediately store and retrieve new data inputs, allowing the RAG model to adapt quickly based on new information.

### Improving performance, reliability, and scalability

Since standardizing on Redis, Docugami has seen steady improvements in performance and reliability, overcoming the business problems they experienced with their previous database management systems.

“We are very happy with Redis because it allows us to do a better job faster and more reliably,” Palmer says. “This is a core business tenet for us. Redis is a game-changer. It is a fast, high-performance vector database—and Redis is a wonderful partner.”

“Our adoption of Redis has led to remarkable improvements in our ML pipeline, ML Ops, and overall document processing operations. Redis is helping us deliver on our commitment to accuracy and efficiency through better chunking, a more efficient vector database, and dramatic advances in scalability,” Palmer concluded.
