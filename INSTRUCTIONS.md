# Agentique Product Requirements Document (PRD)

## 1. Overview

**Agentique** is a multi-language AI platform enabling:

1. **AI Twin Creation**: Users can create AI “agents” that function as the persona/twin of a content creator.  
2. **AI Search**: RAG-based search across all agents.  
3. **Social Media Commenting**: Agents leave relevant comments on Telegram (and later X) posts.  
4. **Payment**: Usage costs 1 credit per action (chat, search, or comment). Creation of an agent is free.

This PRD now incorporates:

- **LangChain** for advanced agent logic (allowing future multi-tool expansions).  
- **OpenAI** (GPT-3.5) as the default LLM for completions **and** embeddings.  
- Custom, editable prompts for each agent.  
- No usage of Replit; we will host the backend on **Railway** and the frontend on **Vercel**.

## 2. Architecture & Technology

### 2.1 Databases

1. **Supabase** (PostgreSQL)  
   - Stores user accounts, credits, agent records, chat history, transactions, etc.  
   - Potentially used for user authentication (later, if we integrate their Auth).

2. **Pinecone** (Vector DB)  
   - Stores embeddings (chunks of scraped content).  
   - Allows quick semantic search for RAG.

### 2.2 Backend

- **FastAPI** in `/backend/`
  - **LangChain** as the core agent framework:
    - For chunking, storing embeddings, building “chains,” and eventually letting agents call “tools.”
    - Integrates with Pinecone for vector retrieval, **OpenAI** for LLM calls.
  - **Architecture**:
    ```
    backend/
    ├── app/
    │   ├── main.py            # FastAPI entry
    │   ├── routes/            # /agent, /search, /comment, /auth, etc.
    │   ├── services/          # ingestion_service, payment_service, ai_service (LangChain logic)
    │   ├── models/            # Pydantic + DB schemas
    │   └── utils/             # chunking, summarization helpers, logging, etc.
    ├── pyproject.toml
    ├── requirements.txt
    └── ...
    ```
  - **Background Tasks**:
    - Use **FastAPI** built-in background tasks or a minimal queue approach (e.g., `Celery` or `RQ`) for large scraping jobs.
    - MVP can rely on FastAPI’s background tasks if volume is low.

### 2.3 Frontend

- **Next.js 13** + **Tailwind CSS** in `/frontend/`  
  - Deployed on **Vercel**  
  - Pages for:
    - **Explore** (view/edit agents, create new agent)
    - **AI-Search** (global search)
    - **Agent Chat** (per agent)
  - Additional directories:
    - `hooks/` for custom React hooks
    - `components/` for shared UI
    - Possibly `lib/` for utility logic

### 2.4 Multi-Language with OpenAI

- **OpenAI** (GPT-3.5-turbo) used for completions & embeddings (`text-embedding-ada-002`) out of the box.  
- **LangChain** orchestrates the RAG pipeline (embedding → Pinecone retrieval → final LLM prompt construction → answer).

### 2.5 In-Memory Caching

- **Where**: Python dictionaries or short-lived cache in the backend.  
- **What**: Store ephemeral results (partial retrievals, repeated queries) for faster responses.  
- **Persistence**: None; resets on server restart. If usage grows, we could shift to Redis or a similar solution.

---

## 3. Data Model

**Using Supabase** for relational data, **Pinecone** for vector storage.

**Supabase** Tables:

1. **users**  
   - `id` (pk), `telegram_id` (or other auth ID), `credits_balance`, timestamps
2. **agents**  
   - `id`, `owner_id`, `expert_name` (the name of the content creator), `status`, `prompt_template`, timestamps
3. **chat_messages**  
   - `id`, `agent_id`, `user_id`, `role` (“system”|“user”|“assistant”), `content`, timestamps
4. **transactions**  
   - `id`, `user_id`, `credits_change`, `reason` (“chat”, “search”, “comment”, “refill”), timestamps

**Pinecone**:  
- Index storing chunk embeddings with metadata: `agent_id`, `source_link` (link to public post), etc.

**LangChain**:  
- Each agent references a chain or “agent” using:
  - The agent’s `prompt_template`
  - Pinecone (filtered by `agent_id` if needed)

---

## 4. Feature Breakdown

### 4.1 Agent Creation (AI Twin)

1. **Explore Page** → “Make AI-agent” (no credits deducted).  
2. User inputs public links (Telegram channel, etc.).  
3. **Background Task** (FastAPI or minimal queue):
   - Use **Telegram** scraping/API with partial ingestion if the channel is large (store offsets in DB).
   - **LangChain** chunking + embed with **OpenAI** → store in Pinecone.
   - Insert a new row in Supabase `agents` with an editable `prompt_template`.  
   - Mark agent `status = "ready"` when done.

**Prompt Template**:  
- Each agent has a dedicated system prompt. e.g. “You are [Expert Name], respond using the data in your knowledge base, referencing sources.”

### 4.2 Agent Chat

1. 1 **credit** per user message.  
2. `POST /agent/{agent_id}/chat`:  
   - Check user credits.  
   - Use **LangChain** to retrieve from Pinecone (filtered by `agent_id`).  
   - Combine the retrieved context + user message → pass to **OpenAI**.  
   - Return a structured answer referencing `source_link`.  
   - Save the conversation in `chat_messages`.  
   - Deduct 1 credit from user’s `credits_balance`.

### 4.3 AI Search

1. 1 **credit** per search.  
2. `POST /search`:  
   - Query across **all** agent content (no filter).  
   - Summaries generated by **OpenAI** with a single call.  
   - Return top results with references.  
   - Deduct 1 credit from user, record transaction.

### 4.4 Social Media Commenting

1. Summon the agent in a public Telegram post.  
2. The agent fetches post content, runs RAG retrieval + **OpenAI** for a relevant comment.  
3. Deduct 1 credit. The bot posts the final comment with references.

### 4.5 Payment & Credits

- **No cost** for agent creation.  
- **1 credit** per usage action.  
- If `credits_balance` < 1, block the request.  
- Transaction logs each usage with reason = “chat” / “search” / “comment”.

---

## 5. Additional Implementation Details

### 5.1 Telegram Scraping vs. API & Partial Ingestion

- **Preferred**: Official **Telegram API** (e.g., Telethon) for stable scraping.  
- **Device Info**: Must specify `DEVICE_MODEL`, etc., to avoid logging out your real session.  
- **Partial Ingestion**: Store an offset or `last_msg_id` in DB for large channels so you only ingest new content each run.

### 5.2 Single Environment for MVP

- We only use **one** environment file (`.env`) for local + production references.  
- In production (Railway), environment variables are set in the hosting config.  

### 5.3 Single RAG Function to Unify Chat vs. Search

- If you prefer minimal duplication:  
  - A single function to embed the query, retrieve from Pinecone (with optional `agent_id` filter), build a final prompt, call **OpenAI**.  
  - Chat calls it with `agent_id`, search calls it with `None`.

### 5.4 Minimal Code, Thorough Comments & Docstrings

- Keep core logic lines minimal, but **docstrings** and inline comments do **not** count as lines.  
- Each route or function should have a short docstring describing parameters, returns, and possible errors.

### 5.5 Extended Error Handling & Logging

- If Pinecone or OpenAI fails, raise a short `HTTPException(503, “Service Unavailable”)`.  
- If insufficient credits, `HTTPException(403, “Not enough credits”)`.  
- For advanced file-based logging that Cursor can see outside the main console, see a separate doc (e.g., `logging-solution.md`).  

### 5.6 Deployment

- **Backend** on **Railway**:
  - Provide a `Procfile` or rely on minimal `uvicorn` command.  
  - Store environment variables in Railway’s secrets.
- **Frontend** on **Vercel**:
  - Next.js 13 with environment variables in Vercel project settings.

---

**End of instructions.md**.
