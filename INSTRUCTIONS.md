# Agentique Product Requirements Document (PRD)

## 1. Overview

**Agentique** is a multi-language AI platform enabling:

1. **AI Twin Creation**: Users can create AI "agents" that function as the persona/twin of a content creator
2. **AI Search**: RAG-based search across all agents
3. **Social Media Commenting**: Agents leave relevant comments on Telegram (and later X) posts
4. **Payment**: Usage costs 1 credit per action (chat, search, or comment). Creation of an agent is free

This PRD now incorporates:

- **LangChain** for advanced agent logic (allowing future multi-tool expansions)
- **DeepSeek R1** as the default LLM
- Custom, editable prompts for each agent
- No usage of Replit; we will host the backend on **Railway** and the frontend on **Vercel**

## 2. Architecture & Technology

### 2.1 Databases

1. **Supabase** (PostgreSQL)
   - Stores user accounts, credits, agent records, chat history, transactions, etc.
   - Potentially used for user authentication (later, if we integrate their Auth)

2. **Pinecone** (Vector DB)
   - Stores embeddings (chunks of scraped content)
   - Allows quick semantic search for RAG

### 2.2 Backend

- **FastAPI** in `/backend/`
  - **LangChain** as the core agent framework:
    - For chunking, storing embeddings, building "chains," and (eventually) letting agents call "tools"
    - Integrates with Pinecone for vector retrieval, DeepSeek R1 for LLM calls
  - **Architecture**:
    ```
    backend/
    ├── app/
    │   ├── main.py            # FastAPI entry
    │   ├── routes/            # /agent, /search, /comment, /auth, etc.
    │   ├── services/          # ingestion_service, payment_service, ai_service (LangChain logic)
    │   ├── models/            # Pydantic + DB schemas
    │   └── utils/             # chunking, summarization helpers
    ├── pyproject.toml
    ├── requirements.txt
    └── ...
    ```
  - **Background Tasks**:
    - Use **FastAPI** built-in background tasks or a simple queue approach (e.g., `Celery` or `RQ`) for large scraping jobs
    - MVP can leverage FastAPI's background tasks if volume is low

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

### 2.4 Multi-Language with DeepSeek R1

- **DeepSeek R1** as the LLM for embeddings or completions:
  - If it provides an embeddings endpoint, we use it; otherwise, we might still use text-embedding-ada-002 for embeddings
  - The chat completions come from **DeepSeek R1**, handling multi-language queries and content seamlessly
- **LangChain** orchestrates the RAG pipeline (embedding → Pinecone retrieval → LLM prompt construction → final answer)

### 2.5 In-Memory Caching

- **Where**: Python dictionaries or short-lived cache in the backend
- **What**: Store ephemeral results (partial retrievals, repeated queries) for faster responses
- **Persistence**: None; resets on server restart. If usage grows, we could shift to Redis

## 3. Data Model

(Using Supabase for relational, Pinecone for vector.)

**Supabase** Tables:

1. **users**
   - `id`, `telegram_id` (or other auth ID), `credits_balance`, timestamps
2. **agents**
   - `id`, `owner_id`, `creator_name`, `status`, `prompt_template` (editable prompt), timestamps
3. **chat_messages**
   - `id`, `agent_id`, `user_id`, `role` ("user"/"assistant"), `content`, timestamps
4. **transactions**
   - `id`, `user_id`, `credits_change`, `reason` ("chat", "search", "comment", "refill"), timestamps

**Pinecone**:
- Index storing chunk embeddings with metadata: `agent_id`, `source_link`, possibly `language`, etc.

**LangChain**:
- Each agent in Supabase references a **LangChain** "chain" or "agent" that uses:
  - The agent's custom `prompt_template`
  - A vector store connection (Pinecone) filtered by `agent_id`

## 4. Feature Breakdown

### 4.1 Agent Creation (AI Twin)

1. **Explore Page** → "Make AI-agent" (free, no credits deducted)
2. User inputs public links (Telegram channel, etc.)
3. **Background Task**:
   - Use scraping or Telegram API
   - **LangChain** chunking + embedding → store in Pinecone
   - Create a new record in Supabase `agents` with an editable `prompt_template`
   - Mark agent `status = "ready"` when done

**Prompt Template**
- Each agent has a dedicated prompt that can be updated in future. E.g., "You are [Creator Name], an expert in X. Respond only with content from your knowledge base, referencing sources..."

### 4.2 Agent Chat

1. 1 **credit** per user message
2. Chat route: `POST /agent/{agent_id}/chat`
   - Check user credits
   - Use **LangChain** chain/agent approach:
     - Query Pinecone (filtered by `agent_id`)
     - Construct the final prompt with the agent's `prompt_template` + user's message + relevant chunks
     - Call **DeepSeek R1** for the chat response
   - Return a structured answer (numbered list with source links)
3. Save conversation to `chat_messages`. Update user's `credits_balance -= 1`

### 4.3 AI Search

1. 1 **credit** per search
2. `POST /search` endpoint:
   - Query across all agent content in Pinecone
   - Summaries generated by LangChain with **DeepSeek R1**
   - Return top 5 results in a Perplexity-style layout with references
3. Deduct 1 credit from user. Record a transaction in `transactions`

### 4.4 Social Media Commenting

1. Summon the agent in a public Telegram post
2. The agent fetches the post content, uses **LangChain** for RAG retrieval, calls **DeepSeek R1** to generate a relevant comment
3. 1 credit deducted from user's balance
4. The bot posts the comment with references

### 4.5 Payment & Credits

1. **No cost** for agent creation
2. Each usage action (chat message, search query, comment) = **1 credit**
3. If `credits_balance < 1`, block the request
4. Save the usage in `transactions` with reason = "chat", "search", or "comment"

## 5. Additional Implementation Details

### 5.1 Telegram Scraping vs. API

- **Preferred**: Official Telegram API (like `Telethon`) if it can retrieve posts from public channels
- **Fallback**: Basic scraping with `requests` and `BeautifulSoup` if no direct API
- A background ingestion task to avoid timeouts on large channels

### 5.2 Authentication

- **Initial**: Telegram-based. Possibly checking the user's Telegram ID upon login
- **Future**: Third-party auth providers or Supabase Auth if you want standard email/password or OAuth

### 5.3 Background Tasks

- **FastAPI's** built-in `BackgroundTasks` or a minimal queue approach for ingestion
- For high-scale operations, consider Celery or RQ with a separate worker process

### 5.4 Deployment

- **Backend**: Railway for container-based FastAPI
  - Store environment variables (Supabase keys, Pinecone keys, DeepSeek R1 keys) in Railway secrets
- **Frontend**: Vercel for Next.js 13
  - Project environment variables (API base URL, etc.) in Vercel settings

## 6. Roadmap & Future Expansions

1. **YouTube Transcripts**: Similar ingestion approach, with `langchain.document_loaders` for YouTube or custom scripts
2. **Advanced Agent Tools**:
   - Additional "tools" for each agent to browse the web, manipulate external data, etc.
   - LangChain's agent tool system makes this easier
3. **Redis or Another Cache**: If in-memory caching is insufficient at scale
4. **Subscription Tiers**: Instead of pay-per-use, monthly plans with included credits
5. **Extended Auth**: Beyond Telegram-based, e.g. Auth0, Supabase Auth, or custom JWT

## 7. Security & Edge Cases

1. **Secrets**: Keep **DeepSeek R1** key, Pinecone key, Supabase key in environment variables
2. **Large Channel**: If Telegram channel is huge, ingestion might fail or partial. Mark `status = "error"` or `status = "partial"`
3. **Multi-Language**: If DeepSeek R1 handles multi-language, confirm it can embed or interpret non-English text well. If not, fallback to another embeddings approach
4. **Editing Agent Prompt**: Provide a route or UI for owners to edit the `prompt_template`. If changed, it affects subsequent chat responses
