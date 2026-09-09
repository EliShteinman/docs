---
title: "How to Build a Visual Project Management App Using Redis"
linkTitle: "How to Build a Visual Project Management App Using Redis"
url: "/blog/how-to-build-a-visual-project-management-app-using-redis/"
description: "Task management can be gruelling. For managers, monitoring tasks that are scattered and disconnected from one another remains just as much a norm as a bane in their profession. Being able to..."
date: 2021-10-27
blogCategories:
- "How To and Tutorials"
- "Tech"
- "Uncategorized"
authors:
- "Growth Team"
lastmod: 2025-03-27
hidden: true
---

*By Growth Team · Published 27 October 2021 · updated 27 March 2025*

![Blog tile image](/images/blog/199fa2fa348a3e91130683750326fdc9637a3c3a-772x520.webp)

Task management can be gruelling. For managers, monitoring tasks that are scattered and disconnected from one another remains just as much a norm as a bane in their profession. Being able to instantly understand the progress of projects without having to waste time digging for this information is an invaluable asset to any manager.

Having a project management system that can provide a clear visualization of the progress of each assignment will save time, reduce errors and allow managers to plan their next move with more precision.

Such an application requires a powerful database to effectively display graphs and resources to the user, which is why this Launchpad App used Redis to create its own project management application.

RedisGraph was at the start of this application, due to its ability to simplify the traversal of highly connected data and deliver contextual insights.

Let’s take a look at how they managed to bring this project to life. But before we dive in, make sure to check out our range of exciting apps on the [Launchpad](https://launchpad.redis.com/).

[Click here to view video](https://www.youtube.com/embed/PjqnpUQCD9U)

1. What will you build?
1. What will you need?
1. Architecture
1. Getting started
1. How it works

## 1. What will you build?

You’ll build a powerful visual project management application that will help users visualize and categorize tasks whilst highlighting the different relationships between them using Redis. A task can be an idea, goal, epic feature, simple task or bug.

From start to finish, the core objective of this application is to make monitoring clusters of tasks simple and easy. Below we’ll take you through each step,along with the required components and their functionality.


## 2. What will you need?

- [**Ruby on Rails**](https://rubyonrails.org/)**: **the preferred open-sourced software to build web applications
- [**RedisGraph**](https://oss.redis.com/redisgraph/)**:** sparses matrices to represent the adjacency matrix in graphs and linear algebra to query the graph.
- [**PostgreSQL**](https://www.postgresql.org/)**: **used as a powerful open-source object-relational database system.
- [**TailwindCSS**](https://tailwindcss.com/)**: **used as a utility first CSS framework that helps to build the user interface.
- [**Webpack**](https://webpack.js.org/)**: **used as a module bundler that bundles JavaScript files for usage in a browser.
- [**Docker**](https://www.docker.com/)**: **deployed as an open platform for developing and running applications.

## 3. Architecture

![](/images/blog/24d9118801fb9a09ee3c88f7e0902121d9da641b-1024x724.webp)

- The application is conceived as a single Ruby on Rails monolith. The app also stores its data relationally by using PostgreSQL and in a graph using RedisGraph.
- Administrative data (such as users and projects) are stored relationally, while storage of tasks and the relationships between them is delegated to the graph storage.
- The graph storage layer features a small custom built DSL, that translates method calls in the style of ActiveRecord into RedisGraph queries.
- Plain HTML and Javascript is the genetic makeup of the app (Stimulus for interactivity and D3.js/cola.js for graph visualization)
- The HTML is rendered server side before being sent to the client. This means that instead of using JSON to transfer data between the server and client, HTML is sent and the only part of the DOM that changes is replaced. Please refer to [Turbo](https://turbo.hotwired.dev/) and [Stimulus](https://stimulus.hotwired.dev/) documentation for more information.
- Graph data is fetched from a JSON endpoint using D3’s JSON plugin. [Hotwire](https://hotwired.dev/) is used as the framework to ensure that its functionality remains efficient.
- Finally, the UI is built using [TailwindCSS](https://tailwindcss.com/), [Heroicons](https://heroicons.com/), [Collecticons](http://collecticons.io/) and [QuillJS](https://quilljs.com/) for the rich text editor.

## 4. Getting started

### Prerequisites

#### Step 1. Installing the Pre-requisites

Install the below software:

- Docker
- Docker Compose

#### Step 2. Clone the repository

| git clone https://github.com/redis-developer/code-red |
|---|

First, ensure that you have a working Docker environment. Pull the images and start the containers:

```python
docker-compose up -d

```

```python
code-red % docker-compose up -d                   
[+] Running 5/5
 ⠿ Network code-red_default       Created                                                                                                    0.1s
 ⠿ Container code-red_postgres_1  Started                                                                                                    1.6s
 ⠿ Container code-red_redis_1     Started                                                                                                    1.6s
 ⠿ Container code-red_reset_1     Started                                                                                                    3.3s
 ⠿ Container code-red_app_1       Started

```

#### Step 3. Compile the front code:

```python
docker-compose run --rm app bin/webpack

```

#### Step 4. Set up the PostgreSQL database:

```python
docker-compose exec app rails db:setup

```

Database ‘codered_development’ and ‘codered_test’ gets created.

Once you’ve set this up, load the sample data into the PostgreSQL and Redis databases:

```python
docker-compose exec app rails database:seed

```

```python
docker-compose exec app rails database:seed
== Creating users ==
== Creating projects ==
== Creating tasks ==

```

The application should now be available at [http://localhost:3000.](about:blank)

## 5. How it works

### Creating tasks

First click on the plus sign on the top left hand side of the screen to create a new task. You’ll then be presented with the below image. At the top you can create a title for the task along with a description in the text box below.

Sitting just below the title you’ll see a panel of drop down menus. On the far left you can decide on the nature of the task. In the middle you can set the due date for the task to be completed and on the far right you can assign the task to a specific individual.

![](/images/blog/61105a89dcbc8debe4d4c9b930e0482741cdc1b2-1600x945.webp)

### Creating relationships

A core benefit of this app is being able to see the relationships between different tasks, as you’ll see from the following image.

To achieve this, first click on a task to get access to its core menu. From here you’ll see a drop-down menu at the bottom called ‘Add relationship’ (see image below), where you can decide what relationship this task will have with others.

On the right-hand side of this bar, you can choose which task you want the relationship to be shared with.

![](/images/blog/1499756da30e0f596e0d152e888d61ecc4ed9565-948x986.webp)

![](/images/blog/a9d3d437cab82da40bcc30b6293b66c85e5b4527-1580x1312.webp)

### How to view a task

As a user, you’ll want to view a task. A popup should display the title, description, deadline, status, type and the person who’s assigned the task.

### Modifying a task

You can modify the title, description, deadline, status, type and assigned person of the task. Doing so is easy. Click on a task and you’ll have the

### Deleting tasks

To delete a task, simply click on the trash icon at the bottom right hand side of the task menu. A confirmation modal should be displayed before the task is deleted.

### Fetching relationships

![](/images/blog/24215e5a8dae0910e99aa6032de03294308cb1ed-1363x1600.webp)

### Adding relationships

As a user, you’ll want to create a relationship between two tasks. A relationship should have the following type:

```python
blocks`/`blocked_by`,`parent_of`/`child_of

```

Or

```python
related

```

### Deleting relationships

At some point you’ll probably want to delete a relationship. No confirmation modal should be displayed before the task is deleted.

![](/images/blog/9a6791b5d9f5f59363e4a4373ee0ad549bdc176d-1494x1488.webp)

### How to create projects

Projects are stored relationally in PostgreSQL. A project has the following properties:

**id:** User identifier

**user: **Owner of the project

**name:** Human readable name of the project

The project is linked to a graph (using id as graph name) A graph has many tasks.

### How to create tasks

![](/images/blog/f95cfb145c9fe17bf19fe95382adf24549ee960b-1600x995.webp)

Tasks are stored as nodes in Redis Graph. A task is a graph node and has the following properties:

- **Title: **Task title
- **Description: **Rich text, multiline description of the task
- **Deadline:** Date
- **Status:** One of Todo, In Progress, Review or Done
- **Type: One** of Idea, Goal, Epic, Feature, Task or Bug – user: Assignee

![](/images/blog/815cd2693014ebf1ab05f4a74221d8d9c160749e-1542x1124.webp)

![](/images/blog/22b409325f65d109a35d8b863793ae84b3f92505-1600x1046.webp)

A task can be linked to many other tasks by relationships.

### How to create relationships

Relationships are stored as edges in Redis Graph. A relationship is a directed graph edge and has the following properties:

**from:** Source node

**type**: One of

```python
Blocked By

```

```python
Child Of

```

```python
Related To

```

**to**: Destination node

Relationships are stored as directed edges, but in the interface both directions are rendered. For example, if Task A is blocked by Task B, Task B will be shown as “blocks Task A”. It’s also possible to add relationships in both directions.

### How to fetch tasks

A graph has many tasks, which are fetched using the following Redis Graph query:

```python
"GRAPH.QUERY" "055616f0-a130-42b1-a3fd-81b7c8a3ef1b" "MATCH (n:Task) RETURN n" "--compact"

```

### How to create/update a task

A task is created and updated with all its properties using the following query:

```python
"GRAPH.QUERY" "055616f0-a130-42b1-a3fd-81b7c8a3ef1b" "MERGE (n:Task {id: 'f5ec1f25-0cee-49d0-9a85-1043f04ea845'}) SET n.created_at = '2021-05-15 10:20:28 UTC', n.updated_at = '2021-05-15 10:20:28 UTC', n.graph = '#<Graph name=055616f0-a130-42b1-a3fd-81b7c8a3ef1b>', n.id = 'f5ec1f25-0cee-49d0-9a85-1043f04ea845', n.title = 'Submit hackathon app', n.description = '<p>Description of my task</p>', n.deadline = '2021-05-15', n.status = 'todo', n.type = 'task', n.user_id = '25714246-be92-4d96-b1ce-cbb57aaf4747'" "--compact"


```

### How to delete a task

A task is deleted using the following query:

```python
"GRAPH.QUERY" "055616f0-a130-42b1-a3fd-81b7c8a3ef1b" "MATCH (n:Task {id: 'f5ec1f25-0cee-49d0-9a85-1043f04ea845'}) DELETE n" "--compact"

```

### How to fetch a relationship

A task’s related nodes are always queried based on relationship type. The related tasks are fetched using the following query:

```python
"GRAPH.QUERY" "055616f0-a130-42b1-a3fd-81b7c8a3ef1b" "MATCH (n:Task {id: 'c9bc52a0-c436-499c-954c-da40e82f50b2'}) -[r:blocked_by]-> (m:Task) RETURN n, m, type(r) AS t" "--compact"

```

### How to add a relationship

Two tasks are linked to each other using the following query:

```python
"GRAPH.QUERY" "055616f0-a130-42b1-a3fd-81b7c8a3ef1b" "MATCH (n:Task {id: '1ad21814-69d7-47d0-a7bb-de678b86c653'}), (m:Task {id: '07427e6b-7bba-44e4-b967-8fb5ca098053'}) MERGE (n) -[r:blocked_by]-> (m)" "--compact"

```

### How to delete a relationship

Two tasks are unlinked from each other using the following query:

```python
"GRAPH.QUERY" "055616f0-a130-42b1-a3fd-81b7c8a3ef1b" "MATCH (n:Task {id: '1ad21814-69d7-47d0-a7bb-de678b86c653'}) -[r:related_to]-> (m:Task) DELETE r" "--compact"

```

### Domain Specific Language (DSL)

A DSL was built to accommodate and simplify graph persistence. Its functionality is to provide a small but robust interface that will be familiar to developers who are used to Active Record’s API. The main class that’s implementing this construction can be found at [app/graph/dsl.rb](https://github.com/floriandejonckheere/code-red/blob/master/app/graph/dsl.rb).

Here’s an example of a query:

```python
query = graph
  .match(:n, from.class.name, id: from.id)
  .to(:r, type)
  .match(:m, to.class.name)
  .delete(:r)

query.to_cypher

# => "MATCH (n:Task {id: 'c9bc52a0-c436-499c-954c-da40e82f50b2'}) -[r:blocked_by]-> (m:Task) DELETE r"

query.execute

# => []

```

## Conclusion: Empowering managers through task visualization

Disconnected and hidden tasks are a threat to any organization looking to maximize efficiency and outgrow their competitors.

Managers who can leverage an application capable of providing a clear visualization of assignments and their relationships can be more organized, think linearly and make quicker decisions in high-pressure situations.

RedisGraph is a crucial component as it allows data to be transmitted efficiently whilst projecting a visualization of each task and their relationships.

If you want to learn more about this app you can visit it on the [Redis Launchpad](https://launchpad.redis.com/?id=project%3Acode-red). And whilst you’re there, make sure to explore all of[ the other innovative applications](https://launchpad.redis.com/) that we have available for you.

![](/images/blog/478133b790db7cb070dd0b045833e75d9aa8a207-1600x593.webp)

## Who created this application?

![](/images/blog/af580a05cd43f696490244bdc366469eeb9d1d31-500x500.webp)

**Florian Dejonckheere**

Florian is an experienced Ruby on Rails developer who works as a software engineer at NephroFlow.

[You can check out his Github page here.](https://github.com/floriandejonckheere)
