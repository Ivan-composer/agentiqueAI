# Agentique Backend step-by-step plan

## **Step 1: Project Initialization & Virtual Environment**

1. **Create/Enter** `agentique/backend/`:
   ```bash
   mkdir -p agentique/backend
   cd agentique/backend
   ```
2. **Set Up** a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # or .\venv\Scripts\activate on Windows
   ```
3. **Install** required dependencies (production-oriented, in `requirements.txt`):
   ```text
   fastapi
   uvicorn[standard]
   supabase-py
   pinecone-client
   langchain
   requests
   python-dotenv
   openai
   telethon
   ```
4. **Confirm** environment variables in a `.env` file; eventually use them in production (Railway).

5. **(Optional)** **Tiny Test Script** for `/health`  
   - Create `test_health.py` (or `tests/test_health.py`) with minimal code:
     ```python
     import requests

     def test_health():
         # Ensure server is running on localhost:8000
         url = "http://127.0.0.1:8000/health"
         resp = requests.get(url)
         assert resp.status_code == 200
         data = resp.json()
         assert data.get("status") == "ok"
     ```
   - This ensures you can quickly test your environment. You’ll run the server (`uvicorn app.main:app --reload`) in one terminal, then run `pytest test_health.py` in another.

---

## **Step 2: Database & Environment Config (Supabase)**

### **2.1 Minimal Table Creation Commands**

You can run these in the **Supabase** SQL editor or via the CLI:

```sql
-- users table
create table if not exists users (
  id text primary key,
  telegram_id text,
  username text,
  credits_balance integer default 0,
  created_at timestamp default now(),
  updated_at timestamp default now()
);

-- agents table
create table if not exists agents (
  id text primary key,
  owner_id text references users (id),
  expert_name text,
  prompt_template text,
  status text,
  created_at timestamp default now(),
  updated_at timestamp default now()
);

-- chat_messages table
create table if not exists chat_messages (
  id text primary key,
  agent_id text references agents (id),
  user_id text references users (id),
  role text,
  content text,
  created_at timestamp default now()
);

-- transactions table
create table if not exists transactions (
  id text primary key,
  user_id text references users (id),
  credits_change integer,
  reason text,
  created_at timestamp default now()
);
```

### **2.2 Minimal Code for DB Connection**

```python
# app/services/db_service.py
import os
from supabase import create_client

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)
```

*(Minimal logic, but keep docstrings for each function or file where needed.)*

---

## **Step 3: Minimal `main.py` & Route Skeleton**

1. **Directory** structure:
   ```
   backend/
   ├── app/
   │   ├── main.py
   │   ├── routes/
   │   ├── services/
   │   ├── models/
   │   └── utils/
   ├── requirements.txt
   ├── .env
   └── ...
   ```
2. **Create** `main.py`:
   ```python
   """
   main.py: Minimal FastAPI setup for Agentique backend.
   """
   from fastapi import FastAPI
   from app.routes import agent, search, comment, auth

   app = FastAPI()

   app.include_router(agent.router, prefix="/agent", tags=["Agent"])
   app.include_router(search.router, prefix="/search", tags=["Search"])
   app.include_router(comment.router, prefix="/comment", tags=["Comment"])
   app.include_router(auth.router, prefix="/auth", tags=["Auth"])

   @app.get("/health")
   def health_check():
       """
       Simple endpoint to ensure the server runs.
       """
       return {"status": "ok"}
   ```
3. **Test** by running:
   ```bash
   uvicorn app.main:app --reload
   ```
   Visit [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health).

4. **Skeleton Route Stubs**  
   Create minimal files in `app/routes/` for `agent.py`, `search.py`, etc. Example:

   ```python
   # app/routes/agent.py
   from fastapi import APIRouter

   router = APIRouter()

   @router.get("/")
   def list_agents_stub():
       """
       Stub route to confirm /agent/ is reachable.
       """
       return {"agents": []}
   ```
   - You can do similar short stubs for `search.py`, `comment.py`, `auth.py`.

---

## **Step 4: Pinecone Vector Index Setup**

1. **Create** `pinecone_service.py`:
   ```python
   """
   pinecone_service.py: Manages Pinecone index and references for vector retrieval.
   """
   import os
   import pinecone

   pinecone.init(
       api_key=os.getenv("PINECONE_API_KEY"),
       environment=os.getenv("PINECONE_ENV")
   )

   if "agentique-index" not in pinecone.list_indexes():
       pinecone.create_index("agentique-index", dimension=1536)

   pinecone_index = pinecone.Index("agentique-index")
   ```

2. **Metadata** in Pinecone for each chunk:
   ```json
   {
     "agent_id": "<agent-id>",
     "source_link": "<link-to-public-post>"
   }
   ```
   - We specifically want **`source_link`** to store **the public post link** for referencing data later.

---

## **Step 5: OpenAI Integration (Embeddings & Completions)**

1. **Create** `openai_service.py`:
   ```python
   """
   openai_service.py: Minimal wrappers for OpenAI embeddings and completions.
   """
   import openai
   import os

   openai.api_key = os.getenv("OPENAI_API_KEY")

   def embed_text(text: str) -> list:
       """
       Convert text into a vector using text-embedding-ada-002.
       """
       resp = openai.Embedding.create(
           model="text-embedding-ada-002",
           input=text
       )
       return resp["data"][0]["embedding"]

   def generate_completion(prompt: str) -> str:
       """
       Calls gpt-3.5-turbo for a single user prompt.
       Returns the assistant's text response.
       """
       resp = openai.ChatCompletion.create(
           model="gpt-3.5-turbo",
           messages=[{"role": "user", "content": prompt}]
       )
       return resp["choices"][0]["message"]["content"]
   ```
2. **Optionally** define a custom `OpenAIEmbeddings` or `OpenAILLM` if using advanced LangChain features.  
3. **Test** by calling each function in a Python REPL.

---

## **Step 6: Telegram Ingestion with Device Info & Partial Ingestion**

### 6.1 Goal

- Use **Telethon** to scrape Telegram channels while specifying the **device info** to avoid logging out from your personal session.  
- Implement a **partial ingestion** approach if the channel is large.  
- Possibly handle concurrency or rate limits to avoid Telegram API issues.

### 6.2 Implementation Details

1. **Device Info**  
   ```python
   DEVICE_MODEL = "MacBook Pro"
   SYSTEM_VERSION = "macOS 11.5"
   APP_VERSION = "9.3.2"
   LANG_CODE = "en"
   SYSTEM_LANG_CODE = "en"
   ```
   - Provide these to the Telethon client so Telegram sees you as a separate “Mac device,” not your real session.

2. **Partial Ingestion**  
   - If channels are large, you can store a “last_msg_id” or “last_date” in the `agents` table.  
   - Each ingestion run starts from the saved offset/ID to avoid re-fetching older messages.  

3. **Possible Rate Limits**  
   - If the channel is very active, you might add a small **sleep** or **rate-limit** logic if you see Telethon raise “FloodWaitError.”  
   - Keep code minimal, but add docstrings explaining it.

4. **Edge Cases**  
   - **Media-only** or pinned messages might appear; for now just skip them.
   - If channel is private or user lacks access, handle the error gracefully.

### 6.3 Testing Step 6

**How to verify**:
1. **Use** a small Telegram channel for local tests (like a test group with a handful of messages) in our case its https://t.me/johndoetest12.  
2. **Check** logs or database entries to confirm partial ingestion.  
   - Example: After scraping, you see new embeddings in Pinecone with `{"agent_id": ..., "source_link": ...}`.  
3. **If** there are many messages, ensure that on repeated runs, it picks up from `last_msg_id`.  
4. **Optional**: Try an intentionally large channel to see partial ingestion in action (like ingest 100 messages, see if it stops gracefully, and can resume).

---

## **Step 7: Payment Logic, Partial Ingestion Approach, Admin Route for Top-Ups**

### 7.1 Goal

- Introduce **credits** usage for each chat/search action.  
- Provide an **admin route** or method to top up user credits.  
- Optionally expand partial ingestion logic (like scheduling or bigger tasks) if the channel is huge.

### 7.2 Implementation Details

1. **Credits & Transactions**  
   - `users.credits_balance` holds the balance.  
   - Insert a row in `transactions` for each usage.  
   - A minimal function:
     ```python
     def deduct_credits(user_id: str, amount: int, reason: str):
         """
         Deduct 'amount' credits from user. Insert a transaction row. Raise error if insufficient.
         """
         # Minimal lines, docstring to clarify usage
         # fetch user => check balance => if < amount => raise error
         # else update user => add transaction row
     ```
2. **Admin Route** for top-ups:
   ```python
   @router.post("/admin/topup")
   def admin_topup(user_id: str, amount: int):
       """
       Only admin calls this. Increases user credits_balance by 'amount'.
       """
       # minimal code => do supabase update => add transaction record
       ...
   ```
   - Possibly protect it with a small “admin password” in environment or a user role check.

3. **Enhancing Partial Ingestion**  
   - If the channel is too big, you might automatically schedule ingestion runs or do a chunk-based approach. Keep code minimal but docstrings explaining repeated tasks.

### 7.3 Testing Step 7

1. **Verify** you can top up a user’s credits, then **deduct** them with the same logic.  
2. **Check** `transactions` table logs each usage or top-up with a reason.  
3. **Ingestion** expansions: run the partial ingestion multiple times, see if it picks up from the correct offset or date.  
4. **Ensure** if a user tries to chat without enough credits, you return an error.

---

## **Step 8: Unify Chat vs. Search RAG Logic**

*(Addressing **Point 2** from overall comments: chat & search overlap, consistent references)*

### 8.1 Goal

- **Minimize duplication** by using a **single function** that does retrieval + summarization.  
- For chat (per-agent), filter `agent_id`; for search (all agents), no filter.  
- Ensure consistent reference format in final results.

### 8.2 Implementation Example

```python
"""
rag_service.py: Unifies retrieval for chat vs. search.
"""
from typing import Optional
from app.services.openai_service import embed_text, generate_completion
from app.services.pinecone_service import pinecone_index

def rag_retrieve_and_summarize(query: str, agent_id: Optional[str] = None) -> str:
    """
    1) embed query
    2) pinecone_index.query() with or without 'agent_id' filter
    3) build a context prompt referencing top chunks
    4) call generate_completion to finalize
    5) return the final text, referencing 'source_link' in bullet points if desired
    """
    # minimal logic, docstrings for clarity
    # references might be '• {chunk_text} (source: {source_link})' for each chunk
    ...
```

### 8.3 Different Output Styles

- **Chat** might want a more conversational result: “Sure, here’s a bullet list: ...”.
- **Search** might want “Here are the top 5 results with references: ...”.  
- Keep the same function but add a `mode="chat"|"search"` param if needed.

### 8.4 Consistent References

- Make sure both chat and search code **show** `source_link` from Pinecone’s metadata in a uniform way, e.g. `(source: <link>)`.
- Possibly unify them so the user sees the same reference format across chat or search, if that’s desired.

### 8.5 Testing Step 8

1. **Chat** route calls `rag_retrieve_and_summarize(query, agent_id=some_id)`.  
   - Confirm you only get chunks from that agent.  
   - Confirm references appear in the final text.  
2. **Search** route calls `rag_retrieve_and_summarize(query, agent_id=None)`.  
   - Confirm it returns global results from all agents.  
   - Check references are bullet or any consistent format.  
3. **Edge Cases**: If agent has zero data or query is empty, handle gracefully (like returning “No relevant chunks found.”).

---

## **Step 9: Extended Error Handling, Docstrings, Minimal Testing**

### 9.1 Error Handling

- **Pinecone** or **OpenAI** downtime => `HTTPException(status_code=503, detail="Service Unavailable")`.  
- **Insufficient credits** => `HTTPException(status_code=403, detail="Not enough credits")`.  
- **Telegram** scraping error => `HTTPException(status_code=500, detail="Telegram ingestion error")`.

Keep the **logic** minimal, but add short docstrings on each route explaining how errors are thrown.

### 9.2 Docstrings

- Each route: docstring with param details, return shape, possible errors.  
- Each service function: docstring describing usage. Minimal code lines, but thorough comments.

### 9.3 Testing Step 9

- **Unit Tests** for route-level errors:
  - Chat with insufficient credits => expect 403.  
  - If Pinecone is offline => handle or mock pinecone calls to ensure 503 is returned.  
- **Integration**: For docstrings, just confirm every route or function has them. Possibly automate with `pydocstyle` or a short script.

---

## **Step 10: Production Deployment on Railway**

### 10.1 Minimal Setup

- **Procfile**:
  ```text
  web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```
- **requirements.txt** is already there.  
- In **Railway** dashboard, add your env vars:
  - `SUPABASE_URL`, `SUPABASE_KEY`, `PINECONE_API_KEY`, `PINECONE_ENV`, `OPENAI_API_KEY`, `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, etc.

### 10.2 Testing Step 10

- **Check** logs after deploy.  
- Confirm you can call `https://your-railway-url/health`.  
- Possibly run a small ingestion or a single chat message to ensure external calls (OpenAI, Pinecone, Telegram) succeed with production credentials.

### 10.3 Optional Concurrency

- If usage is high, mention a note:
  ```text
  web: gunicorn app.main:app -k uvicorn.workers.UvicornWorker --workers 4 --bind 0.0.0.0:$PORT
  ```
- Keep code minimal but docstring explaining multiple workers can handle concurrent requests.

---

## Conclusion

Steps 6–10 now include:

- **Step 6**: Refined partial ingestion logic & Telegram device info, mention big channel edge cases.  
- **Step 8**: Unify chat vs. search retrieval, ensuring consistent references. Possibly a `mode` param for final formatting.  
- A short **testing** approach on each step, verifying either partial ingestion, credit usage, or global search references.  
- Minimal code lines remain the priority, but docstrings & comments ensure future devs understand the system thoroughly.