# Agentique Backend: Final Step-by-Step Plan

## 1. Project Initialization & Environment Setup

1. **Create/Go to your backend folder** (e.g., `agentique/backend/`)
2. **Set up a Python virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate      # or .\venv\Scripts\activate on Windows
   ```
3. **Install required dependencies** (example `requirements.txt`):
   ```text
   fastapi
   uvicorn[standard]
   supabase-py
   pinecone-client
   langchain
   requests
   python-dotenv
   deepseek  # or the official client library if it exists
   ```
   *(If no official DeepSeek R1 library, place a placeholder or your custom code for calling its API.)*

4. **Set up environment variables**
   - Create a `.env` (excluded from git) with:
     ```
     SUPABASE_URL=...
     SUPABASE_KEY=...
     PINECONE_API_KEY=...
     PINECONE_ENV=...
     DEEPSEEK_API_KEY=...
     TELEGRAM_BOT_TOKEN=...  # If needed for Telegram
     ```
   - Plan to store these as **Railway** environment variables in production

## 2. Basic FastAPI + LangChain Skeleton

1. **Directory Structure** (example):
   ```
   agentique-backend/
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

2. **Create `main.py`**:
   ```python
   from fastapi import FastAPI
   from app.routes import agent, search, comment, auth  # you'll create these files

   app = FastAPI()

   # Include routers for agent, search, comment, and auth
   app.include_router(agent.router, prefix="/agent", tags=["Agent"])
   app.include_router(search.router, prefix="/search", tags=["Search"])
   app.include_router(comment.router, prefix="/comment", tags=["Comment"])
   app.include_router(auth.router, prefix="/auth", tags=["Auth"])

   @app.get("/health")
   def health_check():
       return {"status": "ok"}
   ```

3. **Run locally**:
   ```bash
   uvicorn app.main:app --reload
   ```
   Confirm at `http://localhost:8000/health`

## 3. Database (Supabase-py) & Pinecone Initialization

1. **Create `db_service.py`** (under `services/`) to handle **Supabase** connections:
   ```python
   import os
   from supabase import create_client

   SUPABASE_URL = os.getenv("SUPABASE_URL")
   SUPABASE_KEY = os.getenv("SUPABASE_KEY")

   supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
   ```

2. **Create `pinecone_service.py`** (or a single `vector_service.py`) to handle Pinecone:
   ```python
   import os
   import pinecone

   pinecone.init(
       api_key=os.getenv("PINECONE_API_KEY"), 
       environment=os.getenv("PINECONE_ENV")
   )

   if "agentique-index" not in pinecone.list_indexes():
       pinecone.create_index(name="agentique-index", dimension=1536)  # Dimension depends on DeepSeek embeddings

   pinecone_index = pinecone.Index("agentique-index")
   ```
   - We'll store chunk embeddings with metadata like `{"agent_id": ..., "source_link": ...}`

## 4. DeepSeek R1 Integration (Embeddings + Completions)

1. **Check if DeepSeek has a Python client**. Otherwise, create a custom `deepseek_service.py` with functions:
   ```python
   def embed_text(text: str) -> list:
       # Call DeepSeek R1 embedding endpoint and return the vector
       ...

   def generate_completion(prompt: str) -> str:
       # Call DeepSeek R1 completion endpoint
       ...
   ```

2. **Create a custom LangChain LLM** or embedding class** if needed** (e.g., `DeepSeekEmbeddings`, `DeepSeekLLM`) so you can use them in LangChain:
   ```python
   from langchain.llms.base import LLM
   from typing import Optional, List

   class DeepSeekLLM(LLM):
       def __init__(self, api_key: str, ...):
           self.api_key = api_key
           # any init logic

       def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
           return generate_completion(prompt)  # your custom function

       @property
       def _identifying_params(self):
           return {"name_of_llm": "DeepSeek R1"}

       @property
       def _llm_type(self) -> str:
           return "deepseek"
   ```
   *(Analogous approach for embeddings if needed.)*

## 5. Ingestion / Agent Creation (Scraping & Embedding)

1. **Decide** how you'll fetch Telegram channel posts:
   - Using the **Telegram API** (e.g., Telethon)

2. **Write `ingestion_service.py`**:
   ```python
   def ingest_telegram_channel(channel_url: str, agent_id: str):
       # 1) Connect to Telegram API, fetch public posts
       # 2) chunk each post (a few hundred tokens each)
       # 3) embed each chunk with deepseek_service.embed_text()
       # 4) store in pinecone_index.upsert(vectors, metadata)
       # 5) update supabase agent status to "ready"
   ```

3. **Background Tasks** (FastAPI's built-in) to avoid blocking the main thread. In your `routes/agent.py`:
   ```python
   from fastapi import APIRouter, BackgroundTasks
   from app.services.ingestion_service import ingest_telegram_channel

   router = APIRouter()

   @router.post("/create")
   def create_agent(channel_link: str, agent_name: str, background_tasks: BackgroundTasks):
       # 1) create agent record in supabase -> agent_id
       # 2) background_tasks.add_task(ingest_telegram_channel, channel_link, agent_id)
       # 3) return {"agent_id": agent_id, "status": "ingesting"}
   ```

## 6. LangChain "Agent" Logic & Custom Prompt

1. **Custom Prompt** stored in `agents.prompt_template` column
   - Example: "You are {agent_name}, respond only with your content. Provide references as a numbered list with source links..."

2. **Build** a route for chatting: `POST /agent/{agent_id}/chat`
   - **Construct** a LangChain retrieval-based "agent" that:
     - Filters Pinecone metadata by `agent_id`
     - Uses `DeepSeekLLM` or `DeepSeekEmbeddings`
     - Loads the custom `prompt_template` from Supabase
   - **Single Call** to produce an integrated answer referencing top relevant chunks

3. **Route Implementation** Example:
   ```python
   from langchain.chains import RetrievalQA
   from app.services.db_service import supabase
   from app.services.pinecone_service import pinecone_index
   from app.services.deepseek_service import DeepSeekLLM   # if you made that
   from fastapi import APIRouter

   router = APIRouter()

   @router.post("/{agent_id}/chat")
   def chat_agent(agent_id: str, user_message: str, user_id: str):
       # 1) check user credits, if <1 => error
       # 2) retrieve agent record -> agent_prompt
       # 3) build a retrieval chain with filter on {agent_id}
       # 4) pass user_message + agent_prompt to chain => get final answer
       # 5) deduct 1 credit => record transaction
       # 6) store chat in chat_messages => supabase
       # 7) return final answer
       ...
   ```

## 7. Payment Logic & Manual Credit Management

1. **Add** a transaction service in `services/payment_service.py`:
   ```python
   def deduct_credits(user_id: str, amount: int, reason: str):
       # 1) fetch user from supabase
       # 2) if user.credits_balance < amount => raise error
       # 3) supabase.table("users").update({"credits_balance": user.credits_balance - amount}).eq("id", user_id).execute()
       # 4) insert a transaction row in "transactions"
   ```

2. **Manual** credit top-up:
   - For MVP, an admin or developer can update `credits_balance` in the Supabase dashboard

## 8. AI Search Endpoint (Single Call Summaries)

1. **Route**: `POST /search` (in `routes/search.py`)
2. **Implementation**:
   - 1 credit per user's search
   - Use Pinecone across **all** agents (no filter on agent_id)
   - Summarize top 5 chunks in a single LLM call for a unified "Perplexity-style" answer
   - Deduct credits, save a transaction

## 9. Telegram Auth & Social Commenting

1. **Telegram Auth**:
   - Possibly do a web flow: user logs in with Telegram's official login widget or pass their Telegram ID to your backend for verification

2. **Social Commenting** (optional at MVP stage):
   - A Telegram bot that, when mentioned, calls your internal `agent/{agent_id}/comment` route
   - The route retrieves the post text from the Telegram message, runs a retrieval + LLM call, posts the comment
   - Deduct 1 credit from user who invoked the agent

## 10. Deployment on Railway

1. **Optional Docker** vs. **Auto-Detection**:
   - **Auto**: Provide a `requirements.txt` + a `Procfile` with e.g. `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Docker**: Create a `Dockerfile` for more control

2. **Set Env Vars** in Railway's dashboard:
   - `SUPABASE_URL`, `SUPABASE_KEY`, `PINECONE_API_KEY`, `PINECONE_ENV`, `DEEPSEEK_API_KEY`, etc.

3. **Test** your deployed endpoint (e.g., `https://agentique-railway.app`) with your Next.js front-end (deployed on Vercel)

## Final Recap for Cursor

1. **Initialize** a FastAPI project with the indicated folders
2. **Use** `supabase-py` for DB and **pinecone** for vector storage
3. **DeepSeek** handles both embeddings and completions (set up custom classes or direct calls)
4. **Background tasks** with **FastAPI** for ingestion
5. **Telegram** API for channel scraping
6. **Telegram**-only authentication (store Telegram ID in `users`)
7. **Manually** adjust user credits for MVP
8. **Single LLM call** to produce integrated search results
9. **LangChain** from day one with an "Agent" approach (especially for future multi-tool expansions)
10. **Store chat** in Supabase, run ephemeral in-memory caching if needed
11. **Deploy** to **Railway**, attach environment variables, and confirm the front-end can call each route successfully

This plan ensures **Cursor** (or any developer) can systematically implement each step, align with your clarified decisions, and build out the Agentique backend.