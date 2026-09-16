---
title: "How to build a language processing pipeline using AI with Redis"
linkTitle: "How to build a language processing pipeline using AI with Redis"
url: "/blog/how-to-build-a-language-processing-pipeline-using-ai-with-redis/"
description: "Confirmation bias is a problem that all medical professionals have to wrestle with. Not being able to consider different ideas that challenge pre-existing views blights their ability to entertain a..."
date: 2021-10-20
blogCategories:
- "How To and Tutorials"
- "Tech"
authors:
- "Growth Team"
lastmod: 2026-09-01
hidden: true
mirrored: true
---

*By Growth Team · Published 20 October 2021 · updated 1 September 2026*

![Blog tile image](/images/site-mirror/b2a0bdd433cde0b9ab6e644f87dee914a417249c-772x520.webp)

Confirmation bias is a problem that all medical professionals have to wrestle with. Not being able to consider different ideas that challenge pre-existing views blights their ability to entertain a new diagnosis in the face of an established one.

This is a problem rooted in medical literature, where professionals are more likely to lean towards articles that support their pre-existing views. Diversity of opinion is crucial to moulding a holistic perspective capable of delivering effective diagnoses.

In response, a language processing machine learning pipeline was created by this [Launchpad App ](https://launchpad.redis.com/?id=project%3Athe-pattern)to weed out confirmation bias in medical literature. Using Redis, the Launchpad App created a pipeline that was able to translate text into a knowledge graph through the efficient transmission of data.

Let’s investigate how the team was able to achieve this. But before we dive in, make sure to check out all of the different and innovative apps we have on the [Launchpad](https://launchpad.redis.com/).

[Click here to view video](https://www.youtube.com/embed/c9BLQZ6pPFE)

1. What will you build?
1. What will you need?
1. Architecture
1. Getting Started
1. Navigating the Redis Knowledge Graph site
1. Conclusion

## 1. What will you build?

Let’s explore how you can build a pipeline for Natural Language Processing (NLP) using Redis.

We’ll reveal how Redis was used to bring this idea to life by highlighting each of the components used as well as unpacking their functionality.

![](/images/site-mirror/e9ed7aaac99db3e887c71d5a98ae3bd505fc03c5-1600x867.webp)

## 2. What will you need?

- [**Python 3.6**](https://www.python.org/downloads/release/python-360/)**:** robust, powerful and fast programming language
- [**Redis Streams**](https://redis.io/docs/latest/develop/)**: **manages data consumption from cord-19 and transmits data to RedisGears
- [**RedisGears**](/modules/redis-gears/)**: **pre-processes existing articles from cord-19
- [**RedisGraph**](/modules/redis-graph/)**:**stores information that’s processed from RedisGears
- [**RedisAI**](/modules/redis-ai/)**: **carries out deep learning/machine learning models to manage data in RedisGears
- [**Cord-19**](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge)**: **is a growing resource of scientific papers on Covid-19 and related historical coronavirus research. It’s designed to enhance the development of text mining and information retrieval systems over its in-depth collection of metadata and structured full-text papers.

## 3. Architecture

### NLP Pipeline 1: Turning Text into a Knowledge Graph

![](/images/site-mirror/e5407bca7240bdcf3a646a307a0736adc2c56d76-1024x620.webp)

From start to finish, Redis is the data fabric of this pipeline. Its function is to turn text into a knowledge graph. Let’s have a quick overview of what a knowledge graph is and its function in this project.

### What is a knowledge graph?

Systems today go beyond storing folders, files and web pages. Instead, they’re cobwebs of complexity that are composed of entities, such as objects, situations or concepts. A knowledge graph will highlight each of their properties along with the relationship between them. This information is usually stored in a graph database and visualized as a graph structure.

### What are the components of a knowledge graph?

A knowledge graph is made up of 2 main components:

- **Nodes:** represents an object, place, person or concept
- **Edges:** defines the relationship between nodes

Below is an example of how nodes and edges are used to integrate data.

![](/images/site-mirror/dd038100b5267906a8585b09ef7ae54180775673-1084x964.webp)

### How it works

1. **Ingest documents: **[Cord-19](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge) documents are parsed and taken out of body_text. These are then saved under paragraphs in Redis Cluster.
1. **Detect language: **RedisGears registers key readings from the text and discards any of the medical literature that’s not in English.
1. **Split paragraphs into sentences: **paragraphs are then mapped into a sentence.
1. **Spell checker: **symspell library and its map are used to process outputs and save them into hash.
1. **Matcher: **pre-build [Aho-Corasick](https://automata.tech/?utm_source=bing&utm_term=automata&utm_campaign=Automata+brand+campaign&utm_medium=ppc&hsa_mt=p&hsa_ad=&hsa_net=adwords&hsa_src=s&hsa_kw=automata&hsa_tgt=kwd-84250558926797:loc-188&hsa_cam=12526155739&hsa_acc=4064841676&hsa_ver=3&hsa_grp=1348002096966528&msclkid=10b95b0dd2861dab8ba93a3d644746f4) automata is then used to match incoming words to medical concepts using UMLS Methathesaurus
1. **Populate RedisGraph: **matched sentences are then loaded into edges RedisGraph with Nodes being Concept (CUI)
1. **Front-end repository: **sourcecode for this project and upcoming VR/AR
1. **Flask API server: **Just simple Flask API server to query RedisGraph

In the first pipeline, you’ll discover how to create the knowledge graph for medical literature by using a medical dictionary. This processes information using RedisGears and stores it in RedisGraph.

First, use the below code to unzip and parse metadata.zip, where names of files, titles and years are extracted into HASH:

```python
redis_client.hset(f"article_id:{article_id}",mapping={'title': each_line['title']})
redis_client.hset(f"article_id:{article_id}",mapping={'publication_date':each_line['publish_time']})

```

The following code works by reading JSON files – samples in the [data/sample_folder](https://github.com/redis-developer/the-pattern/tree/main/the-pattern-platform/data/sample_folder): [the-pattern-platform/RedisIntakeRedisClusterSample.py](https://raw.githubusercontent.com/redis-developer/the-pattern/main/the-pattern-platform/RedisIntakeRedisClusterSample.py)

It also parses JSON into String:

```python
rediscluster_client.set(f”paragraphs:{article_id}“,” “.join(article_body))

```

And the following code is the main pre-processing task that uses RedisGears: [the-pattern-platform/gears_pipeline_sentence_register.py](https://raw.githubusercontent.com/redis-developer/the-pattern/main/the-pattern-platform/gears_pipeline_sentence_register.py)

It also listens to updates on paragraphs: key:

```python
gb = GB('KeysReader')
gb.filter(filter_language)
gb.flatmap(parse_paragraphs)
gb.map(spellcheck_sentences)
gb.foreach(save_sentences)
gb.count()
gb.register('paragraphs:*',keyTypes=['string','hash'], mode="async_local")

```

This uses RedisGears and HSET/SADD.

**How to turn sentences into edges (Sentence) and nodes(Concepts) using the Aho-Corasick algorithm**

The first step is to use the[ following code](https://raw.githubusercontent.com/redis-developer/the-pattern/main/the-pattern-platform/sentences_matcher_register.py):

```python
bg = GearsBuilder('KeysReader')
bg.foreach(process_item)
bg.count()
bg.register('sentence:*',  mode="async_local",onRegistered=OnRegisteredAutomata)

```

The next line of code will create a stream on each shard:

```python
'XADD', 'edges_matched_{%s}' % shard_id, '*','source',f'{source_entity_id}','destination',f'{destination_entity_id}','source_name',source_canonical_name,'destination_name',destination_canonical_name,'rank',1,'year',year)

```

Below is to increase the sentence score:

```python
zincrby(f'edges_scored:{source_entity_id}:{destination_entity_id}',1, sentence_key)

```

**How to populate RedisGraph from RedisGears**

[the-pattern-platform/edges_to_graph_streamed.py](https://raw.githubusercontent.com/redis-developer/the-pattern/main/the-pattern-platform/edges_to_graph_streamed.py) works by creating nodes, edges in RedisGraph, or updating their ranking:

```python
"GRAPH.QUERY", "cord19medical","""MERGE (source: entity { id: '%s', label :'entity', name: '%s'}) 
         ON CREATE SET source.rank=1
         ON MATCH SET source.rank=(source.rank+1)
         MERGE (destination: entity { id: '%s', label: 'entity', name: '%s' })
         ON CREATE SET destination.rank=1
         ON MATCH SET destination.rank=(destination.rank+1)
         MERGE (source)-[r:related]->(destination)
         ON CREATE SET r.rank=1, r.year=%s
         ON MATCH SET r.rank=(r.rank+1)
         ON CREATE SET r.rank=1
         ON MATCH SET r.rank=(r.rank+1)""" % (source_id ,source_name,destination_id,destination_name,year))

```

### How to query RedisGraph data during API calls

[the-pattern-api/graphsearch/graph_search.py](https://raw.githubusercontent.com/redis-developer/the-pattern/main/the-pattern-api/graphsearch/graph_search.py)

Edges with years node ids, limits and years:

```python
"WITH $ids as ids MATCH (e:entity)-[r]->(t:entity) where (e.id in ids) and (r.year in $years) RETURN DISTINCT e.id, t.id, max(r.rank), r.year ORDER BY r.rank DESC LIMIT $limits"""

```

Nodes:

```python
"""WITH $ids as ids MATCH (e:entity) where (e.id in ids) RETURN DISTINCT e.id,e.name,max(e.rank)"""

```

Next use the following code to find the most scored articles:

```python
app.py uses zrangebyscore(f"edges_scored:{edges_query}",'-inf','inf',0,5)

```

**Using the most humorous code in the pipeline**

Show the below code to your security architect:

```python
import httpimport
    with httpimport.remote_repo(['stop_words'], "https://raw.githubusercontent.com/explosion/spaCy/master/spacy/lang/en/"):
        import stop_words
    from stop_words import STOP_WORDS

    with httpimport.remote_repo(['utils'], "https://raw.githubusercontent.com/redis-developer/the-pattern-automata/main/automata/"):
        import utils
    from utils import loadAutomata, find_matches

```

This is necessary because RedisGears doesn’t support the submission of projects or modules.

### NLP pipeline 2: BERT QA

![](/images/site-mirror/ad4ff28b4c2f2942bf3e589e2acc2549f44018e4-1600x906.webp)

BERT stands for Bidirectional Encoder Representations from Transformers. It was created by researchers at Google AI and is a world leader in processing national language tasks, including Question Answering (SQuAD v1.1.), Natural Language Inference (MNLI) and others.

Below are some popular use cases of the BERT model:

- **Next sentence prediction text: **this happens when your Gmail autocompletes your sentences.
- **Text summarization: **provides concise yet meaningful summaries of lengthy articles.
- **Question answering: **automatically answers questions by users in a natural language
- **Text classification: **categorizes text into organized groups to make content easier to access and understand.

The most advanced code is in[ the-pattern-api/qasearch/qa_bert.py](https://raw.githubusercontent.com/redis-developer/the-pattern/main/the-pattern-api/qasearch/qa_bert.py). This queries the RedisGears + RedisAI cluster, providing users with a question:

```python
get "bertqa{5M5}_PMC140314.xml:{5M5}:44_When air samples collected?"

```

This queries bertqa prefix on shard {5MP} wherePMC140314.xml:{5M5}:44 (see below)is the key of pre-tokenized REDIS AI Tensor (potential answer) and “When air samples collected?” is the question from the user.

```python
PMC140314.xml:{5M5}:44

```

RedisGears then captures the keymiss event [the-pattern-api/qasearch/qa_redisai_gear_map_keymiss_np.py](https://raw.githubusercontent.com/redis-developer/the-pattern/main/the-pattern-api/qasearch/qa_redisai_gear_map_keymiss_np.py):

```python
gb = GB('KeysReader')
gb.map(qa_cached_keymiss)
gb.register(prefix='bertqa*', commands=['get'], eventTypes=['keymiss'], mode="async_local")

```

RedisGears then runs the following:

- redisAI.getTensorFromKey
- redisAI.createModelRunner
- redisAI.createTensorFromBlob
- redisAI.modelRunnerAddInput
- redisAI.modelRunnerRunAsync in async/await

For the non-blocking main thread mode, models are preloaded on each shard using AI.modelset in [the-pattern-api/qasearch/export_load_bert.py](https://raw.githubusercontent.com/redis-developer/the-pattern/main/the-pattern-api/qasearch/export_load_bert.py).

### NLP Pipeline 3: T5 for Summarization

![](/images/site-mirror/2aab384d0547e68e6f247765305cefff30526644-1600x1098.webp)

Summarization works by running on sentence: prefix and running t5-base transformers tokenizer, saving results in RedisGraph using simple SET command and python.pickle module, adding summary key (derived from article_id) into:

```python
rconn.sadd('processed_docs_stage3_queue', summary_key)

```

The following subscribes to queue running simple SET and SREM commands:

```python
summary_processor_t5.py

```

This will then update hash in RedisGraph:

```python
redis_client.hset(f"article_id:{article_id}",mapping={'summary': output})

```

## 4. Getting started

Redis provides [rgcluster Docker image ](https://hub.docker.com/r/redislabs/rgcluster/dockerfile)as well as redis-cluster script. It’s important to make sure that the cluster is deployed in high availability configuration. Each master has to have at least one replica. This is because masters will have to be restarted when you deploy your machine learning models.

If masters is restarted, and there isn’t a replica, then the cluster will become a failed state and you’ll have to manually recreate it.

Other parameters include execution time and memory. Dirt models are 1.4 GB in memory and that’s where you’re required to include proto buffer memory. You also need to increase execution time for both cluster and gears chart because all tasks are computationally extensive, so you need to make sure that the time-outs are accommodated for.

### Step 1. Prerequisite

Make sure that you install virtualenv in your system, Docker and Docker compose.

```python
apt install docker-compose
brew install pyenv-virtualenv 

```

### Step 2. Clone the repository

```python
git clone --recurse-submodules https://github.com/redis-developer/the-pattern.git
cd the-pattern
./start.sh
cd ./the-pattern-platform/
source ~/venv_cord19/bin/activate #or create new venv
pip install -r requirements.txt
bash cluster_pipeline.sh

```

Wait for a bit and then check the following:

RedisGraph has been populated:

```python
redis-cli -p 9001 -h 127.0.0.1 GRAPH.QUERY cord19medical "MATCH (n:entity) RETURN count(n) as entity_count" 
redis-cli -p 9001 -h 127.0.0.1 GRAPH.QUERY cord19medical "MATCH (e:entity)-[r]->(t:entity) RETURN count(r) as edge_count"

```

Whether if the API responds

```python
curl -i -H "Content-Type: application/json" -X POST -d '{"search":"How does temperature and humidity affect the transmission of 2019-nCoV"}' http://localhost:8080/gsearch

```

### Step 3: Start the UI

```python
cd the-pattern-ui
npm install 
npm install -g @angular/cli@9
ng serve

```

### Step 4. Question Answering API

```python
cd the-pattern-api/qasearch/
sh start.sh

```

**Note: **this will download and pre-load 1.4 GB BERT QA model on each shard. Because of its size, there’s a chance that it might crash on a laptop. Validate by running:

```python
curl -H "Content-Type: application/json" -X POST -d '{"search":"How does temperature and humidity affect the transmission of 2019-nCoV?"}' http://localhost:8080/qasearch

```

### Step 5: Summarizing the pipeline

Go to the repository on RedisGears cluster from “the-pattern” repo:

```python
cd the-pattern-bart-summary
# source same enviroment with gears-cli (no other dependencies required)
source ~/venv_cord19/bin/activate 
gears-cli run --host 127.0.0.1 --port 30001 tokenizer_gears_for_sum.py --requirements requirements.txt

```

This task may time out, but you can safely re-run everything.

On the GPU or server, configure NVidia drivers:

```python
sudo apt update
    sudo apt install nvidia-340
    lspci | grep -i nvidia
    sudo apt-get install linux-headers-$(uname -r)
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID | sed -e 's/\.//g')
    wget https://developer.download.nvidia.com/compute/cuda/repos/$distribution/x86_64/cuda-$distribution.pin
    sudo mv cuda-$distribution.pin /etc/apt/preferences.d/cuda-repository-pin-600
    sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/$distribution/x86_64/7fa2af80.pub
    echo "deb http://developer.download.nvidia.com/compute/cuda/repos/$distribution/x86_64 /" | sudo tee /etc/apt/sources.list.d/cuda.list
    sudo apt-get update
    sudo apt-get -y install cuda-drivers
    # install anaconda
    curl -O https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh
    sh Anaconda3-2020.11-Linux-x86_64.sh
    source ~/.bashrc
    conda create -n thepattern_env python=3.8
    conda activate thepattern_env
    conda install pytorch==1.7.1 torchvision==0.8.2 torchaudio==0.7.2 cudatoolkit=11 -c pytorch

```

Configure access from instance to RedisGraph docker image (or use Redis Enterprise)

```python
git clone https://raw.githubusercontent.com/redis-developer/the-pattern-bart-summary.git
#start tmux 
conda activate thepattern_env
pip3 install -r requirements.txt
python3 summary_processor_t5.py

```

### Walkthrough

While RedisGears allows you to deploy and run machine learning libraries like [spacy](https://github.com/AlexMikhalev/cord19redisknowledgegraph/blob/master/spacy_sentences_geared.py) and [BERT transformers](https://github.com/AlexMikhalev/cord19redisknowledgegraph/blob/master/tokenizer_bert_geared.py), the solution below adopts a simpler approach:

![](/images/site-mirror/38739d23a220769bc34a1bed2f8315703484a80a-1600x376.webp)

**Here’s a quick overview of the overall pipeline: **The above 7 lines allow you to run logic either in a distributed cluster or on a single machine using all available CPUs. As a side note, no changes are required until you need to scale over more than 1000 nodes.

Use KeysReader registered for namespace paragraphs for all strings or hashes. Your pipeline will need to run in async mode. If you’re a data scientist, we would recommend using gb.run to help ensure that RedisGears works and that it will run in batch mode. It will then run in batch mode. Afterwards, change it to register to capture new data.

By default, functions will return to output, hence the need for count () – to prevent fetching the whole dataset back to the command issuing machine (90 GB for Cord19).

Overall, pre-processing is a straightforward process. You can access the full code [here](https://github.com/applied-knowledge-systems/the-pattern-platform/blob/main/gears_pipeline_sentence_register.py).

### Important things to keep in mind

1. The node process can only save locally. We don’t move data, anything you want to save should have a hashtag. For example, to add to the set of processed_docs, use the following:

![](/images/site-mirror/5598acbe04ae2631b466abffbb26a56fb33f2de9-1546x108.webp)

1. Make sure to load external libraries into the computational threat. For example, symspell requires additional dictionaries and needs two steps to load:

![](/images/site-mirror/e9612fc2db3f41a6f25c1c937783d060c891bf61-1546x856.webp)

You can build Aho-Corasick automata directly from UMLS data. Aho-Corasick will allow you to match incoming sentences into pairs of nodes, and present sentences as edges in a graph. The Gears related code is simple:

```python
bg = GearsBuilder('KeysReader')
bg.foreach(process_item)
bg.count()
bg.register('sentence:*',  mode="async_local",onRegistered=OnRegisteredAutomata)

```

## 5. Navigating the Redis Knowledge Graph site

The Redis Knowledge Graph is designed to create knowledge graphs based on long and detailed queries.

![](/images/site-mirror/71482313f4bbf5eb5302ea92f487accfd1f09c24-1600x995.webp)

**Preliminary step**: Select ‘Get Started’ and choose either ‘Nurse’ or ‘Medical student.”

**Step 1: **Type in your query into the search bar

![](/images/site-mirror/ae80345679854ff9f163ccb83403b08d59559c91-1600x941.webp)

**Step 2: **Select the query that’s most relevant to your search

![](/images/site-mirror/ad77c94f6d6926e5bc7fead57ae9c9ce001ccd58-1600x1249.webp)

**Step 3: **Browse between the different nodes and change the dates of your search with toggle bar at the bottom

![](/images/site-mirror/e9ed7aaac99db3e887c71d5a98ae3bd505fc03c5-1600x867.webp)

## Conclusion: Eliminating confirmation bias with Redis

Using Redis, the Launchpad App created a pipeline which helps medical professionals navigate through medical literature without suffering from confirmation bias. The tightly integrated Redis system promoted a seamless transmission of data between components, giving birth to a knowledge graph for medical professionals to utilize.

You can discover more about the ins and outs of this innovative application by visiting the [Redis Launchpad](https://launchpad.redis.com/?id=project%3Athe-pattern). When you’re there, you might also want to browse around our [exciting range of applications](https://launchpad.redis.com/) that we have available.

You can head over to the [Launchpad](https://launchpad.redis.com/) to discover more about the application along with many others in our exciting collections of apps.

![](/images/site-mirror/4286535b4f0ad548b626a7e3bc36792d2aa0c568-1600x593.webp)

## Who created this application?

**Alexander Mikhalev**

![](/images/site-mirror/af58554337a114041f2726a41a9b10c17254305b-800x800.webp)

Alexander is a passionate researcher and developer who’s always ready to dive into new technologies and develop ‘new things.’

Make sure to [visit his GitHub page](https://github.com/applied-knowledge-systems) to see all of the latest projects he’s been involved in.
