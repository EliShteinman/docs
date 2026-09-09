---
title: "Get better RAG responses with Ragas"
linkTitle: "Get better RAG responses with Ragas"
url: "/blog/get-better-rag-responses-with-ragas/"
description: "A lot of teams have a hard time measuring their RAG apps. LLMs and techniques for vector search have come a long way, but they still hallucinate, or generate incorrect information. And those out-..."
date: 2024-09-26
blogCategories:
- "Tech"
authors:
- "Robert Shelton"
lastmod: 2026-06-01
hidden: true
---

*By Robert Shelton, AI Engineer at Redis · Published 26 September 2024 · updated 1 June 2026*

![Blog tile image](/images/blog/678fe97776452ca56562463e89aaa31fbf0f9ea2-772x552.webp)

A lot of teams have a hard time measuring their RAG apps. LLMs and techniques for vector search have come a long way, but they still hallucinate, or generate incorrect information. And those out-of-the-box solution architectures still can’t address every pitfall of your specific use case.

As a developer, it’s tough to figure out the best way to solve these problems for your specific needs. And there is no shortage of LinkedIn posts about the next *revolutionary* chunking strategy that your team *must* use or else, fall behind.

Thankfully, evaluating [Retrieval Augmented Generation (RAG)](https://redis.io/glossary/retrieval-augmented-generation/) has also come a long way. So you don’t have to go to production entirely on the anecdotal evidence from your dev and QA teams. Instead, you can adopt a metric-driven development approach. A metrics-driven approach is all about measuring, not guessing. When you measure performance, you improve it—no more wasting time on solutions that don’t make a difference or cause setbacks.

We’ll cover how to get started by establishing a set of baseline metrics. We’ll also use the friendly and pragmatic [RAG Assessment (Ragas) framework](https://docs.ragas.io/en/stable/) to reason more specifically about the performance of our GenAI apps.

## Let’s start with a simple RAG app.

Here’s a quick example of a simple RAG app using LangChain, Redis, and OpenAI to answer questions about financial documents. We’re using Nike’s 2023 10-K document as our contextual data, but feel free to tailor it to your own use case. [The complete code example](https://github.com/redis-developer/redis-ai-resources/blob/main/python-recipes/RAG/06_ragas_evaluation.ipynb) is available within our [AI resources repo](https://github.com/redis-developer/redis-ai-resources/blob/main/python-recipes/RAG/02_langchain.ipynb).

### Split and load the doc

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader

source_doc = "resources/nike-10k-2023.pdf"

loader = UnstructuredFileLoader(
    source_doc, mode="single", strategy="fast"
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2500, chunk_overlap=0
)

chunks = loader.load_and_split(text_splitter)

```

### Create vector embeddings for the chunks and store in Redis as the vector store

```python
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_redis import RedisVectorStore

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

index_name = "ragas_ex"

rds = RedisVectorStore.from_documents(
    chunks,
    embeddings,
    index_name=index_name,
    redis_url=REDIS_URL,
    metadata_schema=[
        {
            "name": "source",
            "type": "text"
        },
    ]
)

```

### Define the LLM and PromptTemplate

```python
import getpass
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OPENAI_API_KEY")

llm = ChatOpenAI(
    openai_api_key=os.environ["OPENAI_API_KEY"],
    model="gpt-3.5-turbo-16k",
    max_tokens=None
)

system_prompt = """
    Use the following pieces of context from financial 10k filings data to answer the user question at the end. 
    If you don't know the answer, say that you don't know, don't try to make up an answer.

    Context:
    ---------
    {context}
"""

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}")
    ]
)

```

### Create RAG question and answer chain

```python
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

question_answer_chain = create_stuff_documents_chain(llm, prompt)
qa = create_retrieval_chain(rds.as_retriever(), question_answer_chain)

```

### Test it out

```python
qa.invoke({"input": "What was nike's revenue last year?"})

```

#### Sample Output

```
{
'input': "What was nike's revenue last year?",
 	'context': [
Document(
metadata={'source': 'resources/nke-10k-2023.pdf'}, 
page_content='As discussed in Note 15 — Operating Segments...'
), 
...other docs
],
 	'answer': "Nike's revenue last year was $51,217 million."
}

```

## Let’s evaluate our RAG app

The Ragas framework consists of four primary metrics: **faithfulness**, **answer relevancy**, **context precision**, and **context recall**. Context precision and recall measure how well the app retrieves data from the vector store, while faithfulness and answer relevance quantify how accurately the system generates results from that data. Together, these metrics give you a complete view of how your app is really performing.

To calculate these metrics, we need to collect four pieces of information from our RAG interactions:

- The question that was asked
- The answer that was generated
- The context that was provided to the LLM to generate the answer
- And, depending on which metrics you’re interested in, a ground-truth answer determined either by a critic LLM or a human-in-the-loop process. In our case, it’s only context recall that uses the ground truth labels.

### First test

Question: Where is Nike headquartered and when was it founded?

Ground truth: Nike is headquartered in Beaverton, Oregon and was founded in 1964.

```python
# helper function to convert the output of our RAG app to an eval friendly version
def parse_res(res, ground_truth=""):
    return {
        "question": [res["query"]],
        "answer": [res["result"]],
        "contexts": [[doc.page_content for doc in res["source_documents"]]],
        "ground_truth": [ground_truth]
    }

# invoke the RAG app to generate a result and parse
question = "Where is Nike headquartered and when was it founded?"
res = qa.invoke(question)
parsed_res = parse_res(res, ground_truth="Nike is headquartered Beaverton, Oregon and was founded in 1964.")

# utilize the ragas python library to import the desired metrics and evaluation function to execute
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas import evaluate
from datasets import Dataset

ds = Dataset.from_dict(parsed_res)

# generate the result and store as a pandas dataframe for easy viewing
eval_results = evaluate(ds, metrics=[faithfulness, answer_relevancy, context_precision, context_recall])
eval_df = eval_results.to_pandas()
eval_df[["faithfulness", "answer_relevancy", "context_precision", "context_recall"]]

```

### Results of our test

## Each metric shows a different flavor of quality

Let’s start with the metrics that look promising.

### Answer relevancy

Answer relevancy is calculated under the hood by asking an LLM to generate hypothetical questions based on the answer returned, and then taking the average cosine similarity between those generated questions.

A high score means there’s not much variation in how the answer could be determined. It makes sense intuitively for our example that this score is high since it’s fairly obvious what sort of questions lead to the answer, “Nike is headquartered in Beaverton, Oregon and was founded in 1967.” But a low score? That gives us an indication of a vague answer that isn’t necessarily related to what was asked.

### Context precision

Next, the context precision for our question/answer pair was 1.0. Context precision measures how *good* the returned context was and is defined as:

A true positive is a document that **is relevant** and **was returned** in the result set and a false positive is a document that was **not relevant** and **was returned** in the result set.

In this case, the evaluation showed that all the docs returned were relevant to the ground truth provided. This is good but does require a bit of faith in the LLM’s ability to determine what is relevant, and that’s a whole other topic on its own. I recommend reading the [full paper](https://arxiv.org/pdf/2309.15217) for those interested in gaining more insight on this front.

### Faithfulness

Moving to the metrics that were less promising, faithfulness is defined‌ as:

For our example, there are two claims that can be determined from the answer: “Nike is headquartered in Beaverton, Oregon and was founded in 1967.”

1. Nike is headquartered in Beaverton, Oregon.

2. Nike was founded in 1967.

The context doesn’t mention Nike being in Beaverton, Oregon, so that claim can’t be inferred from the text.

But the claim that Nike was founded in 1967 can be inferred from the context, since the doc specifically mentions Nike being incorporated in 1967. This result highlights an important point about faithfulness—**it doesn’t measure accuracy**. What’s interesting here is that the claim about Beaverton (Nike is located in Beaverton), though factually correct, **couldn’t **be pulled from the context.

On the flip side, the claim about Nike being founded in 1967 is incorrect but **can** be inferred from the text.

**Faithfulness measures how true to the text an answer was. It doesn’t tell us if the answer was correct or not**.

### Context recall

Accuracy can be understood from context recall, which is defined as:

Context recall is the only metric of the four that utilizes the ground truth data.

The ground truth we provided for this example was `Nike is headquartered in Beaverton, Oregon and was founded in 1964` which can be broken down into two sentences/claims:

1. Nike is headquartered in Beaverton.

2. Nike was founded in 1964.

Neither of these claims can be inferred *correctly* from the context; therefore, context recall is 0/2 or 0.

The first example question provided here is intentionally general and meant to bring up an important point about RAG: RAG is an architecture designed to answer **specific** questions about a context. It is not necessarily ideal for answering **general** questions—that is what an LLM is for.

The question “Where is Nike located and when was it founded?” is a general knowledge question that isn’t specific to the 10-K document we loaded into our context. When designing a test and educating users about how to best interact with a RAG app, it’s important to emphasize what type of questions are meant to be answered by the app.

**This is also why an agent layer can be essential to chat experience because general questions should be handled by a general language model, while specific contextual questions should be handled by RAG, and a layer to determine the difference can greatly improve performance.**

## Let’s ask a different question

```python
question = "What is NIKE's policy regarding securities analysts and their reports?"
res = qa.invoke(question)

parsed = parse_res(res, ground_truth="NIKE's policy is to not disclose any material non-public information or other confidential commercial information to securities analysts. NIKE also does not confirm financial forecasts or projections issued by others. Therefore, shareholders should not assume that NIKE agrees with any statement or report issued by any analyst, regardless of the content.")

ds = Dataset.from_dict(parsed)

eval_results = evaluate(ds, metrics=[faithfulness, answer_relevancy, context_precision, context_recall])
eval_df = eval_results.to_pandas()

```

### Results

### Our second analysis gets better results

For this test, we saw better Ragas scores, largely because the question is well-suited for our RAG app.

– The question directly connects to the context.

– It uses specific terms that help with matching in the vector space.

– The ground truth is similar to the doc content.

With RAG, the question format really matters, just like using the right keywords in a Google search. Since we’re using math to process natural language, we have to be mindful of interacting with the system in a way that lends itself to that paradigm.

Coincidentally, this is why query rewriting in your apps can be really powerful.You’re making conversions that are obvious to humans but not to machines, and it can really improve performance. Plus, now you have the tools to test it yourself.

## We’ll evaluate our RAG app using a test dataset

Now that we have an understanding of the metrics in play and a better idea of what they tell us about our app, the next question becomes: How do we go about creating a dataset to test our specific app? This is where the [Ragas library](https://docs.ragas.io/en/latest/getstarted/testset_generation.html) really shines.

Ragas is designed to be ‘reference-free’ and gives us a helper class for auto-generating a test set. In fact, the second example question was generated this way. It’s worth noting that generating a synthetic dataset is not a replacement for collecting user data or labeling your own set of test questions with ground truth; but, it can be a very effective baseline for getting an initial sense of app performance when a polished test set is not yet available or feasible.

In the [initial paper](https://arxiv.org/pdf/2309.15217) proposing Ragas, a pairwise comparison between human annotators and the Ragas approach found that the two were in agreement 95%, 78%, and 70% of the time, respectively, for faithfulness, answer relevance, and contextual relevance. Note: This was research done on the WikiEval dataset, which is probably one of the easier datasets for LLMs. Even so, it shows that Ragas is a solid and reliable first step.

There’s no special trick to creating a test set. All you need is a set of questions labeled with ground truth answers either by you or your favorite model. An hour of thought and labeling effort is a valuable exercise and could even be used as an example to an LLM for the type of questions you expect and want your app to be tested with.

Code to generate a test set with the Ragas library:

```python
from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context
from ragas.run_config import RunConfig
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

run_config = RunConfig(
    timeout=200,
    max_wait=160,
    max_retries=3,
)

generator_llm = ChatOpenAI(model="gpt-3.5-turbo-16k")
critic_llm = ChatOpenAI(model="gpt-4o-mini")
embeddings = OpenAIEmbeddings()

generator = TestsetGenerator.from_langchain(
    generator_llm,
    critic_llm,
    embeddings,
    run_config=run_config,
)

testset = generator.generate_with_langchain_docs(
    chunks, 
    test_size=10, 
    distributions={
        simple: 0.5, 
        reasoning: 0.25, 
        multi_context: 0.25
    },
    run_config=run_config
)

```

Note: Depending on which model you use and your personal/company limits, it isn’t uncommon to hit rate limits when generating a test set. If this happens, don’t be afraid to try smaller models or generate questions in batches.

Running the test set generation process will output something like this:

It’s important to go through each question and the ground-truth answers carefully. Although the LLM generally does a good job of coming up with questions and answering them, it can definitely miss the mark sometimes. If that happens, don’t worry. Just check your source data, try answering the question yourself, and update the value. The test set generator class helps us create a solid test set but it doesn’t have to be where we stop, and the more care you put into your test set the better your results will be.

## Let’s run it again with more questions this time

The above code was used to generate a test set with 15 questions to evaluate the basic RAG app. The results are shown in the table below.

The performance of our RAG in this case is mediocre. While there are no exact target ranges for these values, you should definitely be concerned to see numbers below 0.5 as a rule of thumb.

On the other hand,if you’re seeing perfect scores across the board, it might be worth double-checking if your test set is challenging enough. Values between 0.75-0.95 are solid, but whether you need to optimize further depends on your app’s purpose. For example, having near perfect faithfulness might be great for fact retrieval, but it could make for a chat experience that’s not as fluid, or conversational.

What’s great about this approach is that while writing this blog, I quickly ran the same tests with a few different chunk sizes to see how they compared and found that 2500 produced the best overall results.

Without taking a metrics-driven approach, it would be really hard for me to gain any idea of how the changes were affecting my system. This little study also leads me to realize that optimizing chunk size alone doesn’t have a giant effect on my app performance overall. This is critical. One of the biggest challenges of every engineering team is knowing what to prioritize. A system of evaluation helps us figure out what’s important much quicker than going on a hunch.

### Output of alternative chunk sizes

## Wrapping up

In this blog, we covered:

1. How to build a simple RAG app, generate a test set, and get started with the Ragas framework.
1. How metrics-driven development can help improve our apps by zeroing in on the optimizations that matter most.
1. How to use Ragas for offline evaluations to track regression between RAG app versions.
1. Design considerations around what type of questions work best for RAG.
1. Simple guidelines and rules of thumb to think about when making sense of your metric results.

For a full Ragas example plus more AI recipes from the team at Redis check out our [AI resources repo](https://github.com/redis-developer/redis-ai-resources).
