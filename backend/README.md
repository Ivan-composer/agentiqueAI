# Backend Documentation

## Technologies
- **FastAPI**: For building the API.
- **Pinecone**: For vector database management.
- **OpenAI**: For AI-twin functionalities (embeddings and completions).
- **LangChain**: For orchestrating the Retrieval-Augmented Generation (RAG) pipeline.
- **Telethon**: For Telegram scraping and ingestion.
- **Logging**: Custom logging setup to capture and persist logs.

## Folder Structure
```plaintext
backend/
├── app/
│   ├── main.py                # FastAPI entry point
│   ├── routes/                # API endpoint definitions (/agent, /search, /comment, /auth, etc.)
│   ├── services/              # Business logic and service integrations (ingestion_service, payment_service, ai_service, rag_service)
│   ├── models/                # Pydantic models and DB schemas
│   ├── utils/                 # Utility functions and helpers (chunking, summarization, logging)
│   │   └── logger.py          # Logging setup
│   └── logging-solution.md    # Detailed logging instructions
├── tests/                     # Test scripts
│   └── test_health.py         # Example health check test
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Coding Standards
- **Core Logic**: Keep core logic lines minimal to enhance readability and maintainability.
- **Docstrings & Comments**: Thoroughly document all functions, classes, and complex logic using docstrings and inline comments. These do **not** count against the "fewer lines" rule.
- **Naming Conventions**:
  - Use `snake_case` for Python functions, variables, and file names.
  - Use `PascalCase` for class names.
- **Type Hints**: Utilize Python type hints for all functions and methods to improve code clarity and assist Cursor in providing accurate suggestions.

### Example:
```python
def read_root() -> dict:
    """
    Root endpoint returning a welcome message.

    Returns:
        dict: A dictionary containing the welcome message.
    """
    return {"message": "Welcome to the Agentique backend!"}
```

## Development

### 1. Set Up Virtual Environment
1. **Navigate** to the backend directory:
   ```bash
   cd backend
   ```
2. **Create and activate** a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
1. **Create** a `.env` file in the `backend/` directory with the following variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_ENVIRONMENT=your_pinecone_environment  # e.g., us-west1-gcp
   TELEGRAM_API_ID=your_telegram_api_id
   TELEGRAM_API_HASH=your_telegram_api_hash
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token   # if using a bot
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```

### 4. Run the Development Server
```bash
uvicorn app.main:app --reload
```
- **Access** the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs)

### 5. Verify Setup
- **Run** the tiny test script to ensure the `/health` endpoint is working:
  ```bash
  pytest tests/test_health.py
  ```
- **Check** logs in `logs/server.log` to confirm logging is operational.

## Logging
- **Setup**: Logging is configured to write to `logs/server.log` for persistent log access.
- **Configuration**: Refer to [`logging-solution.md`](app/logging-solution.md) for detailed instructions on the logging setup.
- **Usage**:
  ```python
  from app.utils.logger import logger

  logger.info("Creating a new agent with channel link %s", channel_link)
  ```

## Features & Services

### AI Service Implementation
The centralized AI service (`backend/app/services/ai_service.py`) handles:
- **OpenAI** embeddings generation and completions.
- **Pinecone** vector similarity search.
- Vector upserting and deletion.
- **Proper error handling and logging**.

### Retrieval-Augmented Generation (RAG)
To unify chat and search functionalities:
- **Single RAG Function**: A unified function `rag_retrieve_and_summarize(query: str, agent_id: Optional[str] = None) -> str` handles both single-agent chat (with `agent_id`) and global search (without `agent_id`).
- **Consistent References**: Ensures both chat and search responses include `source_link` in a uniform format.

### Handling Large Telegram Channels / Partial Ingestion
- **Partial Ingestion**: Store `last_msg_id` or `last_date` in the database to ingest new content incrementally.
- **Edge Cases**: Handle media-only messages, pinned messages, and Telegram API rate limits gracefully.
- **Background Tasks**: Utilize FastAPI’s built-in background tasks for ingestion to prevent timeouts.

## Testing
- **Unit Tests**: Located in the `tests/` directory, use `pytest` to run tests.
  ```bash
  pytest
  ```
- **Integration Tests**: Ensure end-to-end functionality, such as agent creation, ingestion, and chat operations.
- **Health Check**: Verify the `/health` endpoint returns `{"status": "ok"}`.
- **Logging Verification**: Confirm that relevant actions are logged in `logs/server.log`.

## Environment Variables and Secrets
### Required for AI Service
```
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment  # e.g., us-west1-gcp
TELEGRAM_API_ID=your_telegram_api_id
TELEGRAM_API_HASH=your_telegram_api_hash
TELEGRAM_BOT_TOKEN=your_telegram_bot_token   # if using a bot
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### Accessing Environment Variables
**Backend** (Python):
```python
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
```

## Additional Tips
1. **Minimal Code, Thorough Docstrings**:
   - Keep core logic lines minimal, but do not limit comment or docstring lines. Ensure all complex logic is well-documented.
2. **Refer to Logging**:
   - For advanced file-based logging that Cursor can see outside the main console, refer to **`logging-solution.md`**.
3. **Partially Ingest Large Channels**:
   - Maintain an offset (`last_msg_id` or `last_date`) to avoid re-downloading everything on each run.
4. **Single RAG Function for Chat vs. Search**:
   - Use a unified retrieval function with an `agent_id` filter for chat and no filter for search to minimize code duplication.
5. **Extend Error Handling**:
   - Implement minimal error handling with `HTTPException` for service downtimes and insufficient credits. Log all errors appropriately.

## Deployment
- **Backend**: Deploy on **Railway**
  - Ensure environment variables are securely stored in Railway’s secrets.
  - Use a `Procfile` if necessary:
    ```text
    web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    ```
- **Frontend**: Deploy on **Vercel**
  - Configure environment variables in Vercel project settings.
