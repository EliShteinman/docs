---
title: "How to build agent memory with Redis Agent Memory and LangGraph"
linkTitle: "How to build agent memory with Redis Agent Memory and LangGraph"
url: "/tutorials/redis-agent-memory-with-langgraph/"
description: "YouTube: https://youtu.be/OWsCEs8Wt4"
group: "For developers"
date: 2026-05-18
lastmod: 2026-05-18
hidden: true
mirrored: true
---

*Published 18 May 2026*

> **TL;DR:** In this tutorial, you will build a LangGraph travel agent that uses Redis Agent Memory for both short-term and long-term memory. Short-term session memory keeps the active conversation coherent, while long-term memory stores durable user facts and preferences across sessions.

[YouTube: https://youtu.be/OWsCEs8_Wt4](https://youtu.be/OWsCEs8_Wt4)

> **Note:** This tutorial uses the code from the following GitHub repository:
>
> `https://github.com/redis-developer/redis-agent-memory-with-langgraph-demo`

Agent memory helps AI apps move beyond single-turn prompts. A useful agent should remember the current conversation, recall durable preferences, and avoid treating every detail as something it should store forever.

Redis fits this problem because memory retrieval needs to be fast and scoped correctly. In this demo, Redis Agent Memory handles session memory, long-term memory, and vector-backed recall behind a Python client API. You will build a small travel agent with Python, FastAPI, LangGraph, OpenAI, Docker, and the `redis-agent-memory` client.

## Memory model comparison

| Memory layer                | Backed by                                | Lifetime                                   | Used for                                      | Demo UI panel              | Key code                                               |
| --------------------------- | ---------------------------------------- | ------------------------------------------ | --------------------------------------------- | -------------------------- | ------------------------------------------------------ |
| Short-term memory           | Redis Agent Memory session APIs          | One session ID                             | Current conversation continuity               | Current Session            | `retrieve_session_context()`, `add_session_event()`    |
| Long-term memory            | Redis Agent Memory long-term APIs        | Across sessions for an owner and namespace | Durable facts and preferences                 | Retrieved Long-Term Memory | `search_long_term_memory()`                            |
| Extracted memory candidates | Structured LLM output before write       | One turn unless accepted                   | Proposed durable memories                     | Extracted Long-Term Memory | `MemoryExtraction`, `bulk_create_long_term_memories()` |
| Transient task details      | Kept in short-term memory, not extracted | Current session                            | Active itinerary details, dates, and requests | Current Session            | Extraction prompt rules                                |

Store durable preferences in long-term memory. Keep active task context in short-term memory. Filter and dedupe candidates before you write new durable memories.

## Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose.
- An [OpenAI API key](https://platform.openai.com/api-keys).
- A [Redis Agent Memory](https://redis.io/iris/) data-plane URL, store ID, and API key.
- [Redis Insight](https://redis.io/insight/) for optional inspection.
- Basic familiarity with Python, FastAPI, and LangGraph.

> **Note:** The demo does not start a local Redis instance or deploy Redis Agent Memory. It expects an existing Redis Agent Memory service endpoint.

### Setup

Clone the demo repo and create an environment file:

```bash
git clone https://github.com/redis-developer/redis-agent-memory-with-langgraph-demo.git
cd redis-agent-memory-with-langgraph-demo
cp .env.example .env
```

Set these values in `.env`:

| Variable                  | Required | Description                                                                                     |
| ------------------------- | :------: | ----------------------------------------------------------------------------------------------- |
| `OPENAI_API_KEY`          |   Yes    | API key used by the LangGraph agent.                                                            |
| `AGENT_MEMORY_SERVER_URL` |   Yes    | Redis Agent Memory data-plane base URL obtained from [Redis Cloud](https://redis.io/try-free/). |
| `AGENT_MEMORY_STORE_ID`   |   Yes    | Store ID used by the Redis Agent Memory API.                                                    |
| `AGENT_MEMORY_API_KEY`    |   Yes    | API key used by the Redis Agent Memory API.                                                     |
| `OPENAI_MODEL`            |    No    | OpenAI model used for responses and memory extraction.                                          |
| `DEMO_OWNER_ID`           |    No    | Stable user identifier for long-term memories.                                                  |
| `DEMO_NAMESPACE`          |    No    | Logical namespace for this demo's memories.                                                     |
| `DEMO_AGENT_ID`           |    No    | Actor ID used when writing assistant session events.                                            |

Build and run the app:

```bash
docker compose up --build
```

Open `http://localhost:8080`.

## How the demo works

The web app has three parts:

1. Nginx serves the static frontend.
2. FastAPI handles `/api/*` routes.
3. The backend creates a Redis Agent Memory client per request, then calls `RedisAgentMemoryService.run_turn()` to run one LangGraph workflow.

Each chat request returns the assistant response and the memory state needed by the UI:

```python
class ChatResponse(BaseModel):
    session_id: str
    user_message: str
    assistant_message: str
    short_term_memory: list[str]
    long_term_memory: list[str]
    extracted_long_term_memory: list[str]
```

The UI renders the assistant output plus three memory panels: current session memory, retrieved long-term memory, and newly extracted long-term memory.

![Architecture diagram showing Nginx, FastAPI, LangGraph, OpenAI, and Redis Agent Memory working together](/images/site-mirror/cde6040d1271fe0855a5b85e2927a7465f2819aa-1200x620.svg)

## Why Redis Agent Memory?

Redis Agent Memory gives the app one client interface for two different memory scopes. The app stays responsible for deciding what to retrieve, what to pass to the LLM, and what to write.

### Session-scoped memory

Session memory stores events for one `session_id`. The demo uses `get_session_memory()` to read previous events, `add_session_event()` to append the latest user and assistant messages, and `delete_session_memory()` to clear the current session.

This gives the agent continuity without making the frontend resend the full chat history on every request.

### Durable long-term memory

Long-term memory stores owner- and namespace-scoped facts and preferences. The demo uses `search_long_term_memory()` to recall relevant memories before the LLM call and `bulk_create_long_term_memories()` to write accepted new memories after the LLM responds.

The app does not need to manage the Redis data structures or vector search implementation directly. Redis Agent Memory exposes memory operations at the agent layer.

### App-level control

The demo uses Redis Agent Memory session APIs rather than LangGraph's native checkpointer. LangGraph organizes the turn, while Redis Agent Memory stores and retrieves the memory.

That split gives the app clear control over:

- Which session events go into the prompt.
- Which long-term memories match the current user request.
- Which extracted facts deserve durable storage.
- Which owner and namespace isolate memory for this user and app.

### Trade-offs to keep in mind

- Redis Agent Memory must be reachable from the backend.
- LLM-based extraction can vary by model and phrasing.
- Bad owner IDs or namespaces can mix users' memories.
- Long-term memory should store durable preferences, not every conversational detail.

## 1. Configure the FastAPI app and memory client

### How it works

The backend loads configuration once, builds a service around that configuration, and opens a Redis Agent Memory client inside each API request that needs memory.

### Data flow

1. `load_config()` reads `.env` and environment variables.
2. `get_service()` creates and caches `RedisAgentMemoryService`.
3. `agent_memory_client()` builds the Redis Agent Memory client from the cached config.
4. FastAPI routes use the client inside a context manager.

### Code walkthrough

The full implementation lives in `backend/memory.py` and `backend/app.py`.

```python
def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def load_config() -> DemoConfig:
    load_dotenv()
    return DemoConfig(
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        agent_memory_server_url=require_env("AGENT_MEMORY_SERVER_URL"),
        agent_memory_store_id=require_env("AGENT_MEMORY_STORE_ID"),
        agent_memory_api_key=require_env("AGENT_MEMORY_API_KEY"),
        owner_id=os.getenv("DEMO_OWNER_ID", "riferrei"),
        namespace=os.getenv("DEMO_NAMESPACE", "langgraph-travel-demo"),
        agent_id=os.getenv("DEMO_AGENT_ID", "travel-agent"),
    )
```

```python
@lru_cache
def get_service() -> RedisAgentMemoryService:
    return RedisAgentMemoryService(load_config())


def agent_memory_client(service: RedisAgentMemoryService) -> AgentMemory:
    config = service.config
    return AgentMemory(
        config.agent_memory_server_url,
        store_id=config.agent_memory_store_id,
        api_key=config.agent_memory_api_key,
    )
```

The backend exposes these endpoints:

| Endpoint                           | Purpose                                                |
| ---------------------------------- | ------------------------------------------------------ |
| `POST /api/sessions`               | Start a new session.                                   |
| `POST /api/chat`                   | Run one agent turn.                                    |
| `GET /api/sessions/{id}/memory`    | Read current session short-term memory.                |
| `DELETE /api/sessions/{id}/memory` | Delete current session short-term memory.              |
| `GET /api/health`                  | Check backend liveness.                                |
| `GET /api/ready`                   | Check backend readiness, including Redis Agent Memory. |

The readiness endpoint calls Redis Agent Memory before it reports success:

```python
@app.get("/api/ready", response_model=ReadinessResponse)
def ready() -> ReadinessResponse:
    service = get_service()
    try:
        with agent_memory_client(service) as agent_memory:
            agent_memory_health = agent_memory.health(timeout_ms=3000)
    except Exception as exc:
        logger.warning("Redis Agent Memory readiness check failed", exc_info=True)
        raise HTTPException(
            status_code=503,
            detail="Redis Agent Memory is not ready",
        ) from exc
```

Key details:

1. **Required variables fail fast.** Missing Redis Agent Memory credentials raise a runtime error during config loading.
2. **The service is cached.** FastAPI creates one service with stable config instead of rebuilding the LLM wrappers for every route.
3. **The client is request-scoped.** Each route opens the Redis Agent Memory client with `with agent_memory_client(service)`.
4. **Readiness checks the dependency.** `/api/ready` verifies Redis Agent Memory availability before the frontend treats the backend as ready.

### Trade-offs

- Simple request-scoped client usage is easy to reason about.
- Readiness depends on external Redis Agent Memory availability.

## 2. Retrieve short-term memory for the current session

### How it works

Short-term memory is session-scoped. The backend reads memory by `session_id`, converts events into prompt-friendly lines, and returns an empty list when the session does not exist yet.

### Redis Agent Memory mapping

| App concept           | Redis Agent Memory operation               |
| --------------------- | ------------------------------------------ |
| Current conversation  | `get_session_memory(session_id=...)`       |
| Missing new session   | Not-found response handled as empty memory |
| Prompt context window | Last `SESSION_CONTEXT_LIMIT` events        |

### Code walkthrough

Inside the LangGraph node, the service reads session events and keeps the latest 12 entries:

```python
def retrieve_session_context(state: AgentState) -> dict:
    try:
        response = agent_memory.get_session_memory(session_id=state["session_id"])
    except Exception as exc:
        if is_not_found_error(exc):
            return {"session_context": []}
        raise explain_agent_memory_error("session memory read", exc)

    session_context = []
    for event in coerce_events(response)[-SESSION_CONTEXT_LIMIT:]:
        text = get_event_text(event).strip()
        if text:
            session_context.append(f"{get_event_role(event)}: {text}")
    return {"session_context": session_context}
```

The public helper uses the same pattern for the UI endpoint:

```python
def read_session_context(self, agent_memory: AgentMemory, session_id: str) -> list[str]:
    try:
        response = agent_memory.get_session_memory(session_id=session_id)
    except Exception as exc:
        if is_not_found_error(exc):
            return []
        raise explain_agent_memory_error("session memory read", exc)

    session_context = []
    for event in coerce_events(response)[-SESSION_CONTEXT_LIMIT:]:
        text = get_event_text(event).strip()
        if text:
            session_context.append(f"{get_event_role(event)}: {text}")
    return session_context
```

Key details:

1. **STM is session-scoped.** The lookup uses only the current `session_id`.
2. **The frontend does not resend history.** Redis Agent Memory stores prior events for the session.
3. **Deletes stay scoped.** Deleting session memory clears only this session, not durable long-term memory.
4. **Prompt size stays bounded.** `SESSION_CONTEXT_LIMIT = 12` keeps the latest events instead of injecting the whole session.

### Trade-offs

- Simple truncation is predictable, but it is less nuanced than summarization.
- Session memory should not become the storage location for every durable fact.

## 3. Search long-term memory before the LLM call

### How it works

Before the model responds, the graph searches long-term memory with the current user message. The search is filtered by owner and namespace, so the result set belongs to the right user and app context.

### Redis Agent Memory mapping

| App concept              | Redis Agent Memory operation                |
| ------------------------ | ------------------------------------------- |
| Current user request     | Search query text                           |
| User isolation           | `ownerId` filter                            |
| App or environment scope | `namespace` filter                          |
| Relevant durable recall  | `search_long_term_memory()` with `limit: 5` |

### Code walkthrough

The retrieval node finds the latest human message and searches long-term memory:

```python
def retrieve_long_term_memories(state: AgentState) -> dict:
    last_user_message = next(
        (message for message in reversed(state["messages"]) if isinstance(message, HumanMessage)),
        None,
    )
    query = message_text(last_user_message) if last_user_message else ""

    try:
        response = agent_memory.search_long_term_memory(
            request={
                "text": query,
                "limit": 5,
                "filter": {
                    "ownerId": {"eq": state["owner_id"]},
                    "namespace": {"eq": state["namespace"]},
                },
                "filterOp": models.FilterConjunction.ALL,
            }
        )
    except Exception as exc:
        raise explain_agent_memory_error("long-term memory search", exc)
    recalled = [get_memory_text(memory) for memory in coerce_memories(response)]
    return {"recalled_memories": recalled}
```

Key details:

1. **The query comes from the current turn.** The demo searches with the user's latest message.
2. **Owner ID separates users.** Use a stable per-user value in real apps.
3. **Namespace separates apps and environments.** This prevents unrelated memories from leaking into the demo.
4. **Recall is relevance-based.** The app asks for up to five relevant memories, not a full dump of all memories.
5. **Redis Agent Memory hides plumbing.** The app calls memory APIs instead of direct Redis vector search code.

### Trade-offs

- Relevant recall depends on memory quality and query phrasing.
- Shared demo defaults can pollute results. Use stable owner IDs and separate namespaces in production.

## 4. Inject memory into a LangGraph agent turn

### How it works

LangGraph turns one request into a clear sequence of nodes. The graph retrieves session memory, searches long-term memory, calls the model, writes memory, and ends.

```text
START -> retrieve_session_context -> retrieve_long_term_memories -> call_model -> write_memory -> END
```

### Data flow

The graph state keeps short-term memory and long-term memory in separate fields:

```python
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    owner_id: str
    session_id: str
    namespace: str
    session_context: list[str]
    recalled_memories: list[str]
    extracted_memories: list[str]
```

The graph edges make each step explicit:

```python
builder = StateGraph(AgentState)
builder.add_node("retrieve_session_context", retrieve_session_context)
builder.add_node("retrieve_long_term_memories", retrieve_long_term_memories)
builder.add_node("call_model", call_model)
builder.add_node("write_memory", write_memory)
builder.add_edge(START, "retrieve_session_context")
builder.add_edge("retrieve_session_context", "retrieve_long_term_memories")
builder.add_edge("retrieve_long_term_memories", "call_model")
builder.add_edge("call_model", "write_memory")
builder.add_edge("write_memory", END)
return builder.compile()
```

### Code walkthrough

The model call assembles short-term and long-term context into the system prompt:

```python
def call_model(state: AgentState) -> dict:
    session_context = "\n".join(f"- {event}" for event in state["session_context"])
    if not session_context:
        session_context = "- No previous turns in this session."

    long_term_context = "\n".join(f"- {memory}" for memory in state["recalled_memories"])
    if not long_term_context:
        long_term_context = "- No relevant long-term memories found."

    system_prompt = f"""You are a polished travel concierge.

Use short-term memory for continuity within the current session.
Use long-term memory for durable user facts, preferences, and constraints.
Do not mention implementation details.
Keep answers concise, specific, and naturally personalized.

Short-term memory from this session:
{session_context}

Relevant long-term memories:
{long_term_context}
"""
    response = self.llm.invoke([SystemMessage(content=system_prompt), *state["messages"]])
    return {"messages": [response]}
```

Key details:

1. **LangGraph makes the turn observable.** Each node has one job.
2. **STM and LTM stay separate.** The state has `session_context` and `recalled_memories` fields.
3. **The prompt tells the model how to use each scope.** Short-term memory supports continuity. Long-term memory supports durable personalization.
4. **The assistant hides implementation details.** The model is instructed not to mention the memory plumbing.

### Trade-offs

- A small graph is easy to teach and debug.
- More complex agents may add tool calls, routing, summarization, or human review nodes.

## 5. Write session events and extract durable memories

### How it works

After the model responds, the graph writes the user and assistant messages to session memory. Then it asks the LLM for structured durable memory candidates and writes accepted candidates to long-term memory.

### Redis Agent Memory mapping

| App concept               | Redis Agent Memory operation                         |
| ------------------------- | ---------------------------------------------------- |
| User turn                 | `add_session_event(... role=MessageRole.USER)`       |
| Assistant turn            | `add_session_event(... role=MessageRole.ASSISTANT)`  |
| Durable memory write      | `bulk_create_long_term_memories(memories=...)`       |
| Idempotent demo record ID | Deterministic `memory_id(owner_id, namespace, text)` |

### Code walkthrough

Structured output keeps the extraction result predictable:

```python
class MemoryCandidate(BaseModel):
    text: str = Field(description="A durable memory written as one concise sentence.")
    topics: list[str] = Field(default_factory=list)
    memory_type: Literal["semantic", "episodic"] = "semantic"


class MemoryExtraction(BaseModel):
    memories: list[MemoryCandidate] = Field(default_factory=list)
```

The write node stores both sides of the turn as session events:

```python
agent_memory.add_session_event(
    session_id=state["session_id"],
    actor_id=state["owner_id"],
    role=models.MessageRole.USER,
    content=[{"text": user_text}],
    created_at=now_ms(),
    metadata={"source": DEMO_SOURCE},
)
agent_memory.add_session_event(
    session_id=state["session_id"],
    actor_id=self.config.agent_id,
    role=models.MessageRole.ASSISTANT,
    content=[{"text": assistant_text}],
    created_at=now_ms(),
    metadata={"source": DEMO_SOURCE},
)
```

The extraction prompt tells the model what belongs in long-term memory and what should stay in the current session:

```python
SystemMessage(
    content=(
        "Extract only durable user facts, persistent preferences, and stable constraints "
        "that the user explicitly states in the current message and that should help in future "
        "unrelated sessions. Do not extract active task details, current itinerary details, "
        "dates, destinations, booking requests, or other context that only matters for this "
        "conversation unless the user explicitly asks to remember it for later. Do not extract "
        "anything that is only mentioned by the assistant or already present in existing "
        "long-term memories. "
        "If the message is a short reply, a confirmation, a single word, a number, or only "
        "makes sense in the context of the current conversation, return an empty list.\n\n"
        "Examples of messages that should produce NO memories:\n"
        "- '1st' (a date fragment answering a question)\n"
        "- 'yes' (a confirmation)\n"
        "- 'June 15th' (a date answering a question)\n"
        "- 'I am planning a trip to Lisbon next month' (transient travel plan)\n\n"
        "Examples of messages that SHOULD produce memories:\n"
        "- 'My name is Ricardo' → 'The user's name is Ricardo.'\n"
        "- 'I always fly Delta' → 'The user prefers to fly Delta Airlines.'\n"
        "- 'I am vegetarian' → 'The user is vegetarian.'\n"
    )
)
```

The demo normalizes candidate text, skips duplicates, and writes deterministic IDs:

```python
known_memory_texts = {
    normalize_memory_text(memory)
    for memory in state["recalled_memories"]
}
accepted_memory_texts = set(known_memory_texts)
for memory in extraction.memories:
    text = memory.text.strip()
    if not text:
        continue
    normalized_text = normalize_memory_text(text)
    if not normalized_text or normalized_text in accepted_memory_texts:
        continue
    accepted_memory_texts.add(normalized_text)
    record_id = memory_id(state["owner_id"], state["namespace"], text)
    extracted_texts.append(text)
    records.append(
        {
            "id": record_id,
            "text": text,
            "ownerId": state["owner_id"],
            "namespace": state["namespace"],
            "sessionId": state["session_id"],
            "topics": memory.topics or ["travel"],
            "memoryType": memory.memory_type,
        }
    )

if records:
    try:
        agent_memory.bulk_create_long_term_memories(memories=records)
    except Exception as exc:
        raise explain_agent_memory_error("long-term memory write", exc)
```

The deterministic ID helper uses the user, namespace, and memory text:

```python
def memory_id(owner_id: str, namespace: str, text: str) -> str:
    digest = hashlib.sha256(f"{owner_id}:{namespace}:{text}".encode("utf-8")).hexdigest()
    return f"demo-{digest[:32]}"
```

Key details:

1. **Every turn updates STM.** The backend writes both user and assistant events to the current session.
2. **The extractor is selective.** Durable facts, stable preferences, and constraints can become long-term memory.
3. **Transient details stay in STM.** Dates, destinations, and active booking requests should not become long-term memory unless the user asks the agent to remember them.
4. **Duplicates are filtered.** The demo dedupes against recalled long-term memory and accepted candidates from the same turn.
5. **Deterministic IDs help idempotency.** Repeating the same memory for the same owner and namespace produces the same ID.

### Trade-offs

- LLM extraction can still vary.
- Deduping only against retrieved memories can miss duplicates that were not recalled.
- Real apps may need user confirmation, review queues, or deletion controls for long-term memory.

## 6. Show memory behavior in the web UI

### How it works

The frontend keeps the demo visible and teachable. It shows chat messages, the current session ID, short-term memory, retrieved long-term memory, and newly written long-term memory.

### Data flow

1. The browser sends `session_id` and `message` to `/api/chat`.
2. FastAPI returns the assistant message and memory arrays.
3. The UI renders each memory array in its panel.
4. The `+` button creates a new session with the same owner ID.
5. The `×` button deletes current session memory only.

### Code walkthrough

The `sendMessage()` function handles the chat response and memory panels:

```javascript
async function sendMessage(message) {
    setBusy(true);
    appendMessage('user', '👤 You', message);
    try {
        const payload = await api('/api/chat', {
            method: 'POST',
            body: JSON.stringify({ session_id: state.sessionId, message }),
        });
        setSession(payload.session_id);
        appendMessage('ai', '🤖 AI', payload.assistant_message);
        renderList(
            els.stm,
            payload.short_term_memory,
            'No short-term memory yet.',
        );
        renderList(
            els.ltm,
            payload.long_term_memory,
            'No long-term memory retrieved yet.',
        );
        renderList(
            els.written,
            payload.extracted_long_term_memory,
            'No long-term memory written this turn.',
        );
    } catch (error) {
        appendMessage('system', 'Error', error.message);
    } finally {
        setBusy(false);
        els.input.focus();
    }
}
```

The UI defines the three memory panels in `frontend/index.html`:

```html
<section class="memory-section">
    <div class="section-heading">
        <span>STM</span>
        <h2>Current Session</h2>
    </div>
    <ul id="stmList" class="memory-list empty">
        <li>No short-term memory yet.</li>
    </ul>
</section>

<section class="memory-section">
    <div class="section-heading">
        <span>LTM</span>
        <h2>Retrieved Long-Term Memory</h2>
    </div>
    <ul id="ltmList" class="memory-list empty">
        <li>No long-term memory retrieved yet.</li>
    </ul>
</section>

<section class="memory-section">
    <div class="section-heading">
        <span>New</span>
        <h2>Extracted Long-Term Memory</h2>
    </div>
    <ul id="writtenList" class="memory-list empty">
        <li>No long-term memory written yet.</li>
    </ul>
</section>
```

Nginx serves the frontend and proxies API requests to the backend container:

```nginx
location /api/ {
    proxy_pass http://backend:8000;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

Key details:

1. **Memory is visible.** The UI makes hidden agent memory behavior easy to inspect.
2. **New sessions demonstrate LTM reuse.** The `+` button starts a new session but keeps the same configured owner ID.
3. **Deleting STM demonstrates scope separation.** The `×` button clears the current session without deleting durable memory.
4. **The frontend stays minimal.** Nginx serves static files and proxies `/api/*` to FastAPI.

### Trade-offs

- The UI is intentionally minimal.
- It is not an auth or multi-user production frontend.

## Running the demo

Use this flow to see both memory scopes in action:

1. Start Docker:

    ```bash
    docker compose up --build
    ```

2. Open `http://localhost:8080`.
3. Send: `My name is Ricardo.`
4. Send: `Remember that I prefer flying Delta.`
5. Send: `I am planning a trip to Lisbon next month.`
6. Watch the memory panels. The name and airline preference can become long-term memory. The active trip detail should stay in short-term memory unless the user explicitly asks the agent to remember it.
7. Click `+` to start a new session.
8. Ask: `What do you remember about me?`
9. Confirm that durable long-term memory persists across sessions.
10. Click `×` to delete the current session memory and note that long-term memory remains.

> **Caveat:** If the UI does not load, check `/api/ready` and verify your Redis Agent Memory credentials.

> **Caveat:** If memory extraction looks different from the examples, remember that model output can vary by model version and phrasing.

> **Note:** If long-term memory looks polluted, change `DEMO_OWNER_ID` or `DEMO_NAMESPACE` for a clean run.

## Running the tests

The demo tests mock Redis Agent Memory and OpenAI calls, so they do not need external services.

Install the test dependencies and run pytest:

```bash
uv add --dev pytest httpx
uv run pytest
```

The tests cover three areas:

- `tests/test_utils.py` for pure helper functions.
- `tests/test_api.py` for FastAPI endpoints with `TestClient`.
- `tests/test_service.py` for service behavior and long-term memory deduplication.

## Production considerations

Before you adapt this pattern for production, account for memory as user data:

- Use real authentication and stable user IDs instead of demo defaults.
- Add delete, export, and review paths for long-term memory where needed.
- Keep namespaces separate for each app and environment.
- Monitor readiness, Redis Agent Memory latency, and downstream LLM latency.
- Consider summarization when session memory grows beyond simple truncation.
- Consider human-in-the-loop review before storing sensitive memories.
- Avoid storing secrets or sensitive transient details as long-term memory.

## Next steps

- Add a memory review screen before writing long-term memory.
- Add user-specific auth and owner IDs.
- Add summarization for older session events.
- Add [Redis Iris](https://redis.io/iris/) to bring in real travel data.
- Inspect memory with Redis Insight if available.
- Deploy with a managed Redis or Redis Agent Memory setup.

## References

- [Redis Iris](https://redis.io/iris/)
- [Demo source](https://github.com/redis-developer/redis-agent-memory-with-langgraph-demo)
- [Build a memory-aware AI agent with Redis Agent Memory and Redis Context Retriever](https://redis.io/tutorials/redis-iris-call-agent/)
- [Redis Agent Memory package](https://pypi.org/project/redis-agent-memory/)
- [LangGraph documentation](https://langchain-ai.github.io/langgraph/)
- [OpenAI docs](https://platform.openai.com/docs)
- [Redis Cloud free tier](https://redis.io/try-free/)
- [What is Agent Memory? Example using LangGraph and Redis](/tutorials/what-is-agent-memory-example-using-langgraph-and-redis/)
- [Build a car dealership AI agent with Google ADK and Redis Agent Memory Server](/tutorials/build-a-car-dealership-agent-with-google-adk-and-redis-agent-memory/)
