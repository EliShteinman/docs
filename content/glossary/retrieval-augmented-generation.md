---
title: "Retrieval augmented generation"
linkTitle: "Retrieval augmented generation"
url: "/glossary/retrieval-augmented-generation/"
description: "A large language model is a type of artificial intelligence designed to understand and generate human language. It processes vast amounts of text data, learning patterns and structures to perform..."
lastmod: 2026-09-01
---

*updated 1 September 2026*

**A large language model is a type of artificial intelligence designed to understand and generate human language. It processes vast amounts of text data, learning patterns and structures to perform tasks like translation, summarization, and text generation. Built on advanced algorithms, these models can handle complex language tasks, making them useful in applications like chatbots, virtual assistants, and content creation.**

RAG is designed to address the limitations of traditional language models that generate responses based solely on the input they receive and the information they have been trained on. While these models are effective in many scenarios, they can struggle with tasks that require specific, factual knowledge or the ability to reference multiple sources of information.

Before continuing it will be important to familiarize yourself with some related concepts:

**Retrieval**: This refers to the process of obtaining or fetching data or information from a storage location. In the context of databases or search engines, it’s about fetching the relevant data based on a specific query.

**Vector Similarity Search**: At its core, [vector similarity search](https://redis.io/solutions/vector-database/) involves comparing vectors (lists of numbers) to determine how similar they are. It’s often used in machine learning and AI to find the most similar items in a database, based on a given input.

**Vector Database**: A database that is designed to store vectors, typically used in conjunction with machine learning models. These databases are optimized for vector similarity searches.

**LLM**: It stands for “Learned Language Model”, a type of machine learning model designed to work with text. LLMs are trained on vast amounts of text data to understand and generate human-like text based on patterns they recognize.

**Chunking**: This is the process of taking input data (like text) and dividing it into smaller, manageable pieces or “chunks”. This can make processing more efficient, especially in contexts like natural language processing where the input might be very long.

**Embeddings**/**Vectors**: In machine learning, embeddings refer to the conversion of discrete items (like words or products) into continuous vectors. These vectors capture the semantic meaning or relationship between the items in a way that can be processed by algorithms.

**K Nearest Neighbors (KNN)**: This is a type of algorithm used in classification and regression. Given an input, KNN finds the ‘k’ training examples that are closest to that input and makes a decision based on their values or labels.

**Token Limit**: In the context of natural language processing and machine learning models, a token is a unit of text (like a word or a character). The token limit refers to the maximum number of tokens a model can handle in a single input.

**Fine Tuning**: After a machine learning model has been pre-trained on a general task, it can be “fine-tuned” on a more specific task. This involves further training the model on a smaller dataset that’s more relevant to the specific problem you’re trying to solve, refining its capabilities.

## The Concept of RAG

The concept of RAG is relatively straightforward. It involves two main components: a document retriever and a large language model (LLM). The document retriever is responsible for finding relevant information from a large corpus of documents based on the input question using semantic search. This information is then passed to the LLM, which generates a response.

The unique aspect of RAG is the way it combines these two components. Instead of retrieving documents and then generating a response in two separate steps, RAG uses a joint process where the document retrieval and response generation steps are connected. This allows the model to consider multiple documents simultaneously when generating a response, leading to more accurate and contextually relevant outputs.

The RAG approach is particularly effective for tasks that require a deep understanding of context and the ability to reference multiple sources of information. This includes tasks such as question answering, where the model needs to consider multiple sources of knowledge and choose the most appropriate one based on the context of the question.

In summary, Retrieval Augmented Generation represents a significant advancement in the field of Generative AI and LLM-based applications, offering a powerful tool for tasks that require a combination of deep understanding, contextual awareness, and factual accuracy.

For a more in-depth look at RAG check out: [Redis Cloud Integration With Amazon Bedrock Now Available](/blog/amazon-bedrock-integration-with-redis-enterprise/)

## Using RAG on Large Language Models (LLMs)

The application of Retrieval-Augmented Generation (RAG) on Large Language Models (LLMs) is a significant advancement in the field of natural language processing. This section provides a technical overview of how RAG can be used with LLMs.

### Integration of RAG and LLMs

RAG is a method that combines the strengths of pre-trained transformers and efficient information retrieval methods. When applied to LLMs, it enhances the model’s ability to generate more accurate responses and reduce hallucinations by retrieving relevant documents from a large corpus of text and using these documents to inform the generation process.

The integration of RAG into LLMs involves two main components: the retriever and the generator. The retriever is responsible for finding relevant documents based on the input query, while the generator uses the retrieved documents and the original query to generate a response.

### The Retriever

The retriever in a RAG-LLM setup captures more complex semantic relationships between the query and the documents, leading to more accurate retrieval results. The retriever can embed documents and queries into a high-dimensional vector space, where the distance between vectors corresponds to the relevance of the document to the query. Documents that are less relevant to the input query would have a larger “distance” and thus should be ignored as irrelevant. Setting this threshold is part of the design and is based on ‌application requirements. These dense embeddings are typically stored in a vector database for performing the vector similarity search.

The retriever takes the input query, converts it into a vector using the query encoder, and then finds the most similar document vectors in the corpus. The documents associated with these vectors are then passed to the generator.

The number of documents retrieved in any given step can be adjusted based on the specific requirements of the task. For tasks demanding a broad understanding of a topic, a more expansive set of documents might be summoned. Conversely, for tasks that hinge on precision, a narrower set of documents might suffice.

An essential aspect to consider during retrieval is the accuracy of the documents fetched. Retrieval accuracy can often be quantified using a distance measure, such as vector similarity in the context of machine learning models. Essentially, documents that are not pertinent to the input query will exhibit a greater “distance” from the query vector, suggesting their irrelevance. This distance serves as a metric to discern the relevance of documents to the query.

Setting a threshold for this distance is crucial. Documents that fall beyond this threshold can be disregarded, ensuring only the most relevant ones are considered. It’s worth noting that deciding on this threshold isn’t purely a technical decision— it’s also a business choice. The threshold should be aligned with the overarching objectives, whether it’s to provide a comprehensive overview or to pinpoint specific details.

### The Generator

The generator in a RAG-LLM setup is a large transformer model, such as GPT3.5, GPT4, Llama2, Falcon, PaLM, and BERT. The generator takes the input query and the retrieved documents, and generates a response.

The retrieved documents and the input query are concatenated and fed into the generator. The generator then uses this combined input to generate a response, with the retrieved documents providing additional context and information that helps the generator produce a more informed and accurate response, reducing hallucinations.

### Training RAG-LLM Models

Training a RAG-LLM model involves fine-tuning both the retriever and the generator on a question-answering dataset. The retriever is trained to retrieve documents that are relevant to the input query, while the generator is trained to generate accurate responses based on the input query and the retrieved documents.

## Applications of RAG with LLMs

### Use Cases

Retrieval Augmented Generation (RAG) with LLMs have a wide range of applications in the field of Generative AI and Natural Language Processing (NLP). They are particularly effective in tasks that require a deep understanding of context and the ability to reference multiple sources of information.

Question Answering: RAG excels at question-answering tasks. They can retrieve relevant documents based on the input question and generate a precise answer. The ability to consider multiple documents simultaneously allows RAG models to generate answers that aren’t only accurate but also contextually relevant.

Text summarization: RAG can be used to generate summaries of long documents. The document retrieval component can identify the most important parts of the document, and the LLM can generate a concise summary that captures the main points.

Text completion: RAG models can be used to complete partial texts in a way that is consistent with the existing content and contextually relevant. This can be useful in tasks such as email drafting, code completion, and more.

Translation: While not their primary use case, RAG models can also be used for translation tasks. The document retrieval component can retrieve relevant translations from a corpus, and the LLM can generate a translation that’s consistent with these examples.

### Advantages of RAG-LLMs

The main advantage of using RAG with LLMs is that it allows the model to leverage external knowledge stored in a large corpus of text. This can significantly improve the model’s ability to generate accurate and informative responses, especially for queries that require knowledge that isn’t present in the model’s pre-training data.

RAG helps reduce hallucination by grounding the model on the retrieved context, thus increasing factuality. Also, it’s cheaper to keep retrieval indices up-to-date than to continuously pre-train an LLM. This cost efficiency makes it easier to provide LLMs with access to recent data via RAG. Finally, if we need to update or remove data, it’s easier to update the retrieval index (compared to fine-tuning or prompting an LLM not to generate bad outputs).

Furthermore, because the retriever and the generator are trained separately, they can be updated independently. This means that improvements in retrieval or generation methods can be incorporated into the model without needing to retrain the entire model.
