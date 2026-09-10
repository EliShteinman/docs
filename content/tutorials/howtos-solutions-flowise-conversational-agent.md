---
title: "Build a Conversational Agent with Redis Using Flowise"
linkTitle: "Build a Conversational Agent with Redis Using Flowise"
url: "/tutorials/howtos/solutions/flowise/conversational-agent/"
description: "In this tutorial, we will learn how to build a conversational agent with Redis using Flowise. Flowise is a powerful, open-source, and user-friendly AI platform that allows you to build and deploy..."
group: "For developers"
aliases:
- "/tutorials/howtos-solutions-flowise-conversational-agent/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> Use Flowise's drag-and-drop visual builder to create a no-code conversational AI agent. Wire up ChatOpenAI for language understanding, SearchAPI for real-time web results, and Redis-backed chat memory for persistent conversation history — all without writing a single line of code.

In this tutorial, we will learn how to build a conversational agent with Redis using [Flowise](https://flowiseai.com/). Flowise is a powerful, open-source, and user-friendly AI platform that allows you to build and deploy conversational agents (and many other LLM flows) quickly using a simple and intuitive interface.

## What you'll learn

- What Flowise is and why it's useful for building AI agents visually
- How to set up Flowise locally with Docker
- How to create a conversational agent chatflow with tool integration
- How to use Redis as persistent chat memory for your agent
- How to extend your agent with a Redis vector store for RAG-based retrieval
- How to export and import chatflows for sharing and backup

## What is Flowise?

[Flowise](https://flowiseai.com/) is an open-source, low-code platform for building LLM-powered applications through a visual drag-and-drop interface. Instead of writing code to chain together language models, tools, and memory, you connect pre-built nodes in a browser-based canvas. Flowise supports a wide range of integrations — including OpenAI models, vector stores like Redis, and external APIs — making it a popular choice for prototyping and deploying conversational AI agents without deep programming expertise.

## What is a conversational agent?

Normal LLMs (Large Language Models) like GPT-4 are general-purpose models trained on diverse datasets to perform a wide range of language-related tasks, such as text generation, translation, summarization, and more.

Conversational agents, however are more sophisticated and designed specifically for managing conversations effectively. They often integrate multiple specialized agents or modules to handle specific tasks, providing a comprehensive and interactive experience.

## How does a conversational agent differ from a normal LLM?

> **Example**
>
> **User question:**
>
> ```text
> Who won the latest 2024 elections in India?
> ```
>
> **Normal LLM (GPT-4) response:**
>
> ```text
> Sorry, I don't have real-time access to current events or updates, including recent election outcomes. To find out who won the latest 2024 elections in India, I recommend checking the most recent news on a reliable news website or a trusted media outlet.`
> ```
>
> **Conversational agent response:**
>
> ```text
> Prime Minister Narendra Modi's Bharatiya Janata Party (BJP) and its National Democratic Alliance (NDA) won the most seats in the latest 2024 elections in India.
> ```

- A normal LLM cannot answer questions about the latest news, projects, etc., as it is not trained on real-time data.

- In contrast, a conversational agent can handle such queries because it integrates an LLM at its core along with other specialized agents to manage specific tasks. In our conversational agent example, we will use **ChatOpenAI** combined with a **SearchAPI** agent to answer questions about the latest news, weather, and other real-time information. For a code-based approach to building a similar chatbot, see [How to Build a RAG GenAI Chatbot Using Vector Search with LangChain and Redis](/tutorials/howtos/solutions/vector/gen-ai-chatbot/).

- The [SearchAPI](https://www.searchapi.io/) agent is a specialized module capable of fetching data from Google search results, enabling our conversational agent to provide up-to-date and relevant answers.

- We can use multiple specialized agents like **SearchAPI**, **Calculator**, **Python Interpreter**, **Custom Tool**, **Custom Function/ API**, etc., to enhance the capabilities of our conversational agent. LLM will pick the right tool to handle specific types of queries.

## How do you set up Flowise?

There are [different ways](https://docs.flowiseai.com/getting-started) to install Flowise. For this tutorial, we'll use the docker compose method to install Flowise.

### 1> Clone the Flowise repository from GitHub

```bash
git clone https://github.com/FlowiseAI/Flowise.git
```

### 2> Navigate to the docker folder

```bash
cd Flowise/docker
```

### 3> Copy the .env file

Copy the example environment file and rename it to .env. This file contains configuration settings for your docker containers.

```bash
cp .env.example .env
```

### 4> Start the docker application

Use the following command to start the docker application in detached mode. This command will download the necessary docker images and start the Flowise application.

```bash
docker-compose up -d
```

### 5> Access Flowise in your browser

Open your browser and navigate to [http://localhost:3000](http://localhost:3000) to access the Flowise application.

### 6> Stop the docker containers

If you need to stop the docker containers, you can do so with the following command:

```bash
docker-compose stop
```

By following these steps, you will have Flowise up and running on your local machine, ready for you to start building and testing your conversational agents.

## How do you create a new chatflow?

### 1> Navigate to the Chatflows menu

Open your browser and go to [http://localhost:3000](http://localhost:3000). In the Flowise application, navigate to the Chatflows menu.

### 2> Create a new chatflow

Click on the **+ Add new** button to create a new chatflow.

![Creating a new chatflow in the Flowise interface](/images/site-mirror/b408c00bbbc046c20bc0880d380938836ff35e78-1038x460.webp)

### 3> Save and name your chatflow

Click on the save icon. A prompt will appear asking you to name your chatflow. Enter a meaningful name that describes the purpose of your chatflow.

![Saving and naming the new chatflow](/images/site-mirror/d20d28989b6311da85dd1d7059a769b7749f3612-1038x406.webp)

By following these steps, you will create an empty chatflow in Flowise, setting the foundation for building your conversational agent.

## How do you add a conversational agent node?

![Dragging the Conversational Agent node into the Flowise workspace](/images/site-mirror/ca43efa69dd0e4fa7c8fb678538bbcf8d28551cd-800x377.webp)

### 1> Drag the conversational agent node

From the **Agents** section in the Flowise interface, drag the **Conversational Agent** node into your chatflow workspace.

### 2> Modify additional parameters

In the node's interface, you have the option to modify the system message prompt. This prompt is used to set the context for the chatbot, ensuring it understands the specific domain or behavior you want it to exhibit. Also, click on the save icon to ensure your modifications are not lost.

By following these steps, you will have successfully added a conversational agent node to your chatflow and set the initial context for your chatbot. In subsequent sections, we will integrate additional nodes and configure the chatbot to interact with Redis and other specialized agents.

## How do you add a SearchAPI node?

![Integrating the SearchAPI node into the chatflow](/images/site-mirror/d269c3bab0bb0f07593c728ac65ba4f9aff950c9-800x377.webp)

### 1> Drag the SearchAPI node

From the **Tools** section in the Flowise interface, drag the **SearchAPI** node into your chatflow workspace. The SearchAPI node acts as an agent capable of fetching data from Google search results.

### 2> Connect to conversational agent node

Connect the **SearchAPI** node to the **Conversational Agent** node by drawing a line from the output of the `Conversational Agent` node to the input of the `SearchAPI` node. This connection allows the conversational agent to utilize the search capabilities provided by the `SearchAPI`.

### 3> Set the SearchAPI key

In the interface of the SearchAPI node, enter your SearchAPI key. This key is necessary for the node to authenticate and perform search queries.

### 4> Combine multiple tools

You can enhance the capabilities of your Conversational Agent by adding multiple tools. For example, you can integrate **SearchAPI**, **Calculator**, **Python Interpreter** or **Custom Tool** node. The Conversational Agent will automatically select the appropriate tool to handle specific types of queries. For this demo, we will be just adding **SearchAPI** node. Also, click on the save icon to ensure all configurations and connections are stored.

By following these steps, you will have successfully integrated a SearchAPI node into your chatflow, let's add other nodes in next steps.

## How do you add a ChatOpenAI node?

![Adding the ChatOpenAI node to the conversational workflow](/images/site-mirror/2c5a923035de8a9cb2503df5880be49a77c13ad0-800x377.webp)

### 1> Drag the ChatOpenAI node

From the **Chat Models** section in the Flowise interface, drag the **ChatOpenAI** node into your chatflow workspace.

### 2> Create an OpenAI key

If you haven't already created an OpenAI key, do so by clicking on the **Create New** menu within the node's interface. This key is essential for authenticating requests to the OpenAI API.

### 3> Choose a model

Select a model like GPT-3, GPT-4 ..etc from the available options. The model determines the behavior and capabilities of your conversational agent.

### 4> Set the temperature

The temperature parameter controls the randomness of the model's responses. It ranges from 0 to 1:

- **Low temperature** (e.g., 0.2): Produces more deterministic and focused responses.

- **High temperature** (e.g., 0.8): Produces more creative and varied responses.

### 5> Set additional parameters

Configure other parameters such as **Max Tokens**, which defines the maximum number of tokens (words or parts of words) the model can generate in a single response. Ensure you save your chatflow regularly to preserve all changes.

By following these steps, you will have successfully added and configured a **ChatOpenAI** node in your chatflow. This node will serve as the core conversational engine, leveraging OpenAI's powerful language models to generate responses. In subsequent sections, we will further enhance your chatflow with additional nodes.

## How do you add Redis-backed chat memory?

![Dragging the Redis Backed Chat Memory node into the workspace](/images/site-mirror/e1788bcf4541e55ed68f011f785fd34ea3ef2ddd-800x377.webp)

### 1> Drag the Redis chat memory node

From the **Memory** section in the Flowise interface, drag the **Redis Backed Chat Memory** node into your chatflow workspace.

### 2> Choose Redis connection key

In the node's interface, choose or create a connection key for the Redis instance. This connection key will be used to store and retrieve chat memory data.

### 3> Set chat key prefix

In the additional parameters section, you can set a chat key prefix. This prefix helps in organizing and identifying the chat memory records stored in Redis. Finally, save your chatflow to ensure all configurations and connections are persisted.

> **Redis**
>
> Why Use Redis for chat memory?
>
> **Speed:** Redis is an in-memory data store, which means it can quickly read and write data, providing low-latency access to chat history. This speed is crucial for maintaining a seamless and responsive conversational experience.
>
> **Persistence:** Redis also supports persistence, allowing chat data to be stored permanently. This means even if the application restarts or crashes, the chat history can be recovered, ensuring continuity in conversations.

By following these steps, you will have successfully added a Redis chat memory node to your chatflow. This integration ensures that your conversational agent can remember and utilize past interactions, enhancing the overall user experience. To learn more about using Redis for vector-based semantic search in your AI applications, see the [Vector Semantic Text Search](/tutorials/howtos/solutions/vector/semantic-text-search/) tutorial. In the next section, we will test the chatflow setup.

## How do you test the chatflow?

![Interacting with the conversational agent in the Flowise chat interface](/images/site-mirror/00f891c5e811c72c20a36383792e9962c1faf47f-800x377.gif)

### 1> Start the chat

Click on the chat icon to interact with your newly created conversational agent.

### 2> Ask questions

Test the functionality by asking any questions on latest news/ events.

### 3> Check the response

Evaluate the response provided by the chatflow. Ensure that it correctly fetches and presents information based on the connected tools (e.g., SearchAPI). Click on the tool button above the chatflow response message to view details of the tools used.

![Viewing details of the SearchAPI tool used by the chatbot](/images/site-mirror/05fbc245d0805d2e4e85f25a7f9d398a5c50310c-1038x432.webp)

By following these steps, you will be able to test and validate the functionality of your chatflow, ensuring that your conversational agent is working as expected and providing accurate and relevant responses.

## How do you verify chatflow data with Redis Insight?

[Redis Insight](https://redis.io/insight/) is a powerful GUI tool that allows you to interact with Redis data visually. It provides an easy way to verify and manage the persisted data in your Redis instance.

![Redis Insight showing conversational chat data stored as a Redis list](/images/site-mirror/275e221ff8612ffaf928a8e6a46f9b174502e6e9-1038x570.webp)

### Example of stored chat data

In our example, Redis stores the chat data in a list with each entry representing a message in the conversation. Here are **samples** of how these entries might look:

```json
[
    {
        "type": "ai",
        "data": {
            "content": "Prime Minister Narendra Modi's Bharatiya Janata Party (BJP) and its National Democratic Alliance (NDA) won the most seats in the latest 2024 elections in India. However, they fell short of securing an outright majority in parliament.",
            "tool_calls": [],
            "invalid_tool_calls": [],
            "additional_kwargs": {},
            "response_metadata": {}
        }
    },
    {
        "type": "human",
        "data": {
            "content": "Who won the latest 2024 elections in India?",
            "additional_kwargs": {},
            "response_metadata": {}
        }
    }
]
```

- **Type**: Indicates the origin of the message. It can be either ai (response generated by the AI) or human (message input by the user).
- **Data**:
    - **Content**: The main text of the message. For AI responses, this is the generated answer. For human messages, this is the user's input.
    - **Tool calls**: A list of calls made to external tools or APIs during the generation of the response.
    - **Invalid tool calls**: A list of tool calls that failed or were invalid.
    - **Additional kwargs**: Additional keyword arguments that might have been used during the message processing.
    - **Response metadata**: Metadata associated with the response, such as timestamps or processing details.

By using Redis Insight, you can easily monitor and manage the data generated by your conversational agent, ensuring that all interactions are correctly logged and stored in Redis. This can be invaluable for debugging, improving the agent's performance, and maintaining a high-quality user experience.

## How do you export and import chatflows?

Flowise allows you to easily export and import chatflows, enabling you to save your work for future use or share it with others. Below are the steps to export and import chatflows.

### Exporting a chatflow

![Exporting a chatflow as a JSON file from Flowise settings](/images/site-mirror/fb559c99413baa6d2764caa6ce861ca325308146-1038x470.webp)

#### 1> \*\*Select an existing chatflow

Go to the **Chatflows** menu in the Flowise interface. Choose the chatflow you want to export from the list of existing chatflows.

#### 2> Export the chatflow

Click on the settings icon and select the **Export Chatflow** menu item. The chatflow will be exported as a JSON file, which you can [download](https://cdn.builder.io/o/assets%2Fbf70e6aa643f4e8db14c5b0c8dbba962%2F208413b9b9b04d75a275004aa601d015?alt=media&token=69092e3a-e59a-4945-aadc-dad76759df51&apiKey=bf70e6aa643f4e8db14c5b0c8dbba962) and save for future use.

### Importing a chatflow

![Loading an existing chatflow JSON file into Flowise](/images/site-mirror/9bec378b94cc7021aebdeaaddb6592cbe9aaa86b-1038x299.webp)

#### 1> Create a new chatflow

Go to the **Chatflows** menu in the Flowise interface. Click on the **+ Add new** button to create a new chatflow.

#### 2> Import the chatflow

Click on the settings icon and select the **Load chatflow** menu item. Upload the previously exported JSON file.

#### 3> Configure the imported chatflow

The imported chatflow will appear without credentials. Ensure you provide the necessary credentials for any nodes requiring authentication (e.g., OpenAI key, SearchAPI key and Redis key) and save the chatflow to persist the changes. Once the chatflow is imported and configured, initiate a chat session to ensure it works as expected.

By following these steps, you can efficiently export and import chatflow in Flowise, facilitating easy backup, sharing, and reuse of your conversational agent.

## How can you use Redis as a vector store with Flowise?

In addition to using **chat memory** in Flowise, you can also leverage Redis as a **vector store** to store and retrieve embeddings for your conversational agent. This functionality is beneficial for tasks such as **semantic search, recommendation systems**, and more.

Below sample chatflow demonstrates how to use Redis as a vector store to perform semantic search using the **RAG** (Retrieval-Augmented Generation) concept.

![Advanced chatflow example implementing RAG with a Redis vector store](/images/site-mirror/637082246192cecca7bd102116e67d0684bec882-800x377.webp)

### Quick steps to use the advanced example

#### 1> Import the Chatflow

Download and import the provided [chatflow JSON file](https://cdn.builder.io/o/assets%2Fbf70e6aa643f4e8db14c5b0c8dbba962%2Ffd37e5a0c4f44cdb991a7c9bd4e67f5a?alt=media&token=321e9663-a4bd-4227-a70c-6db73339874f&apiKey=bf70e6aa643f4e8db14c5b0c8dbba962) into Flowise and save it.

#### 2> Configure Nodes

- Redis Node: Set up the Redis nodes with your connection key.
- OpenAI Node: Configure the OpenAI nodes with your API key and necessary parameters.

#### 3> Upload Sample Data

Unzip and upload the provided [sample products](https://cdn.builder.io/o/assets%2Fbf70e6aa643f4e8db14c5b0c8dbba962%2F12d4009ad4cc4a7996766beb6dc05272?alt=media&token=029cf553-80c3-419a-9394-2d13687cbb84&apiKey=bf70e6aa643f4e8db14c5b0c8dbba962) or any other text files into the **Text File** node of this chat flow. The uploaded data will be used for semantic search and recommendations.

#### 4> Test the Chatflow

Initiate the chatflow and perform searches or queries to see how the system retrieves and utilizes the embeddings stored in Redis to generate meaningful responses.

## Conclusion

By following this tutorial, you have successfully built a sophisticated conversational agent using Flowise and Redis. Flowise's intuitive interface and powerful integration capabilities, combined with Redis's speed and persistence, provide a robust platform for creating and deploying highly interactive and responsive AI chatbots. With these tools, you can handle complex queries, fetch real-time data, and maintain seamless user interactions.

## Next steps

- **Build a code-based RAG chatbot:** Follow the [RAG GenAI Chatbot with LangChain and Redis](/tutorials/howtos/solutions/vector/gen-ai-chatbot/) tutorial to build a similar chatbot using Python and LangChain instead of a visual builder.
- **Add video Q&A capabilities:** Learn how to build an [AI-Powered Video Q&A Application](/tutorials/howtos/solutions/vector/ai-qa-videos-langchain-redis-openai-google/) that uses Redis vector search to answer questions about video content.
- **Explore semantic search:** Dive into [Vector Semantic Text Search](/tutorials/howtos/solutions/vector/semantic-text-search/) to understand how Redis handles embedding storage and similarity queries under the hood.
- **Try Redis Cloud:** Deploy your Redis instance on [Redis Cloud](https://redis.io/cloud/) for a fully managed production environment with built-in vector search support.
