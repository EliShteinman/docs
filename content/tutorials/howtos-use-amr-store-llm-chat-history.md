---
title: "Use Azure Managed Redis to store LLM chat history"
linkTitle: "Use Azure Managed Redis to store LLM chat history"
url: "/tutorials/howtos/use-amr-store-llm-chat-history/"
description: "Learn how to deploy a Streamlit-based LLM chatbot whose conversation history is stored in Azure Managed Redis. Setup takes just five minutes, with built-in capabilities like per-user memory, TTL,..."
group: "For developers"
aliases:
- "/tutorials/howtos-use-amr-store-llm-chat-history/"
date: 2026-02-25
lastmod: 2026-02-25
hidden: true
mirrored: true
---

*Published 25 February 2026*

> **TL;DR:**
>
> Store LLM chat history in Redis by using the [redisvl](https://docs.redisvl.com/en/latest/) library's `StandardSessionManager`. Each user's messages are persisted as Redis hashes with keys like `mysession:UserName:entry_id`, giving you per-user conversation memory, configurable TTLs, and token counting out of the box.

Learn how to deploy a Streamlit-based LLM chatbot whose conversation history is stored in Azure Managed Redis. Setup takes just five minutes, with built-in capabilities like per-user memory, TTL, token counts, and custom system instructions.

## What you'll learn

- How to store and retrieve LLM chat history in Azure Managed Redis
- How to manage separate conversation memories for multiple users
- How to count tokens over stored chat context to stay within model limits
- How to trim context to the last _n_ messages
- How to set per-user TTLs on chat history entries
- How to configure custom system instructions for LLM behavior

## Architecture

The demo app consists of three main Azure components working together to deliver a multi-user LLM chatbot with persistent memory:

1. Azure App Service hosts the Streamlit web app (LLMmemory.py). When a user submits a prompt, the app's managed identity obtains an Azure AD token and forwards the request to Azure OpenAI.
2. Azure OpenAI Service (GPT-4o) processes each incoming chat request. The Streamlit app sends the most recent context (based on the “Length of chat history” setting) alongside a system prompt to the OpenAI endpoint, which returns the assistant's response.

Azure Managed Redis stores every message—user prompts, AI replies, and system instructions—as Redis hashes under keys like `mysession:UserName:entry_id`. The [redisvl](https://docs.redisvl.com/en/latest/) library's StandardSessionManager abstracts reads and writes, enabling features such as per-user chat history, TTL, and token counting. This approach to persistent chatbot memory complements other Redis-powered AI patterns like [agent memory with LangGraph](/tutorials/what-is-agent-memory-example-using-langgraph-and-redis/) and [RAG chatbots using vector search](/tutorials/howtos/solutions/vector/gen-ai-chatbot/).

![Architecture diagram showing the Streamlit web app connecting to Azure OpenAI for LLM inference and Azure Managed Redis for persistent chat history storage](/images/site-mirror/1e4b1a246907031d79f700fcabad545b4b988343-1038x683.webp)

By using managed identities for both Redis and OpenAI, no secrets are required in the code or configuration. All resources are provisioned via Bicep in the infra/ folder, and the Azure Developer CLI (azd up) ties them together, creating the resource group, App Service, Azure Cognitive Services instance, and Redis cache in one seamless deployment.

## Prerequisites

- An active [Azure subscription](https://azure.microsoft.com/free/)
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) installed
- [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd) installed
- Python 3.10 or later
- Access to Azure OpenAI Service (GPT-4o)

### Set up

#### Install/update Azure CLI\*

```bash
brew update

brew install azure-cli
```

#### Azure login

```bash
az login
```

This should open a new browser window or tab to authenticate into your Azure account. 

#### Install Azure Developer CLI

```bash
brew install azure/azure-dev/azd
```

If you have trouble installing the Azure Developer CLI from above, try grabbing it from here

```bash
curl -fsSL https://aka.ms/install-azd.sh | bash
```

#### Verify the version

```bash
azd version
```

You should see azd version 1.x

#### Clone the demo repository and get into the folder

```bash
git clone git@github.com:robertopc1/Redis_LLMmemory.git

cd Redis_LLMmemory
```

#### Azure Development CLI login

```bash
azd auth login
```

If you're not an Admin/Owner of the Azure account you're using, then before you run the demo, make sure your Azure user has the Cognitive Services contributor role. If you still hit errors while running azd up, being assigned the owner of the resource group unblocks most errors. If you need to troubleshoot with various permissions, resource groups, etc., remember to run azd auth logout and then azd auth login to refresh your session in your terminal after making changes in Azure. 

#### Start your instance

```bash
azd up
```

Most of the time, everything stands up by itself within five minutes. And you'll get a URL endpoint to the app in the terminal that looks something like this:

Deploying services (azd deploy)

(✓) Done: Deploying service web

- Endpoint: https://web-fostjta2f5eww.azurewebsites.net/

Occasionally, it may time out while creating/updating resources:

![Terminal output showing a temporary timeout error during Azure Developer CLI deployment of the LLM chatbot resources](/images/site-mirror/392c60d3bd8318647592eafc9b36732ae231cfc2-1038x194.webp)

Rerun `azd up`, and it will finish creating the resources.

### Feature walkthrough

#### How do you store separate chat memories for multiple users?

By specifying a list of users and initializing a StandardSessionManager with a distinct session_tag per user, each person's chat history is stored under keys like `mysession:Luke:<id>` versus `mysession:Leia:<id>`. Switching the “Select User” dropdown changes which Redis‐backed session is active.

```python
# Define users
users = ["Luke", "Leia", "Han"]

@st.cache_resource
def initSessionManager(_redis_client):
    session_manager = StandardSessionManager(
        name='mysession',
        redis_client=_redis_client
    )
    session_manager.clear()  # Clear any existing data
    for user in users:
        # Preload a system message separately for each user
        session_manager.add_message(
            {"role": "system", "content": "You are a helpful assistant."},
            session_tag=user
        )
    return session_manager

# Initialize Redis client and SessionManager
credential_provider = create_from_default_azure_credential(("https://redis.azure.com/.default",))
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_client = redis.Redis(
    host=redis_host,
    port=redis_port,
    ssl=True,
    credential_provider=credential_provider
)
session_manager = initSessionManager(redis_client)

# Default Streamlit state for which user is active
if "userselectbox" not in st.session_state:
    st.session_state.userselectbox = "Luke"
if "contextwindow" not in st.session_state:
    st.session_state.contextwindow = 5

# Sidebar control to switch active user
user = st.sidebar.selectbox("Select User", users, key="userselectbox")
```

#### How do you track token usage across stored chat history?

This function computes the total token count over the last n messages by encoding each message with tiktoken. The sidebar metric displays “Chat history tokens” in real time, helping you gauge prompt length versus model limits.

```python
def calculate_tokens(text):
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens_per_message = 3
    tokens_per_name = 1
    num_tokens = 0
    for message in text:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # Add tokens for assistant priming
    return num_tokens

# Fetch the last N messages and show token count in the sidebar
chathistory = session_manager.get_recent(
    top_k=st.session_state.contextwindow,
    session_tag=st.session_state.userselectbox,
    as_text=False
)
tokens = st.sidebar.metric(
    label="Chat history tokens",
    value=calculate_tokens(chathistory)
)
```

#### How do you trim chat context to the last _n_ messages?

A sidebar slider lets you choose how many recent messages to send as context. During each LLM call, only the top contextwindow messages (excluding the system message) are retrieved, effectively pruning older history.

```python
# Sidebar slider to select how many messages to keep in context
contextwindow = st.sidebar.slider("Length of chat history", 1, 20, key="contextwindow")

# When sending a new prompt:
historylength = st.session_state.contextwindow
# Retrieve only the last ‘historylength' messages (skip system at index 0)
messages = session_manager.get_recent(
    top_k=historylength,
    session_tag=st.session_state.userselectbox
)[1:]
# Pass `messages` into the LLM API call
```

#### How do you set a TTL on per-user chat history?

By selecting a TTL value and clicking “Set TTL,” the code grabs the most recent contextwindow entries for that user and calls redis_client.expire on each entry's key. Those hashes will auto-expire after the chosen number of seconds.

```python
def add_ttl(ttl_length, contextwindow, user):
    # Fetch raw entries for the last `contextwindow` messages
    messages = session_manager.get_recent(
        top_k=contextwindow,
        session_tag=user,
        raw=True
    )
    # Set expiration on each key
    for m in messages:
        key_id = m["id"]
        redis_client.expire(key_id, ttl_length)

# Sidebar controls for TTL
ttl_length = st.sidebar.slider("TTL time (seconds)", 1, 600, 60)
ttl_submit = st.sidebar.button("Set TTL of chat history")
if ttl_submit:
    add_ttl(
        ttl_length,
        st.session_state.contextwindow,
        st.session_state.userselectbox
    )
```

#### How do you configure custom system instructions for the LLM?

A dropdown offers three presets—“Standard ChatGPT,” “Extremely Brief,” and “Obnoxious American.” When changed, update_system_instructions finds the user's system message in Redis (the very first entry) and overwrites its content field via hset. The next LLM call uses that updated system prompt.

```python
systeminstructions = [
    "Standard ChatGPT",
    "Extremely Brief",
    "Obnoxious American"
]

def update_system_instructions(user, systeminstruction):
    # Retrieve the first (system) message for this user
    messages = session_manager.get_recent(
        top_k=100,
        session_tag=user,
        raw=True
    )
    systemmessage = messages[0]
    keyname = systemmessage["id"]

    if systeminstruction == "Standard ChatGPT":
        redis_client.hset(
            keyname,
            "content",
            "You are a helpful assistant."
        )
    elif systeminstruction == "Extremely Brief":
        redis_client.hset(
            keyname,
            "content",
            "You are a VERY brief assistant. Keep your responses as short as possible."
        )
    elif systeminstruction == "Obnoxious American":
        redis_client.hset(
            keyname,
            "content",
            "You are a VERY pro-American assistant. "
            "Make sure to emphasize how great the good ole' USA is in your responses."
        )

# Sidebar dropdown to select the instruction
st.sidebar.selectbox(
    "System Instructions",
    systeminstructions,
    key="systeminstructions",
    on_change=lambda: update_system_instructions(
        st.session_state.userselectbox,
        st.session_state.systeminstructions
    )
)
```

## Clean up

When you're ready to shut down the app, remember to tear down your resources:

```bash
azd down
```

## Next steps

Now that you've built a multi-user LLM chatbot with persistent conversation history in Azure Managed Redis, explore these related tutorials:

- [What is agent memory? Example using LangGraph and Redis](/tutorials/what-is-agent-memory-example-using-langgraph-and-redis/) — Learn how to give AI agents long-term memory across sessions using Redis.
- [Build a RAG GenAI Chatbot with Redis](/tutorials/howtos/solutions/vector/gen-ai-chatbot/) — Combine vector search with LangChain and Redis to build a retrieval-augmented generation chatbot.
- [Streaming LLM output with Redis Streams](/tutorials/howtos/solutions/streams/streaming-llm-output/) — Use Redis Streams to deliver real-time LLM responses to your users.
