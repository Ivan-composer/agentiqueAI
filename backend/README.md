# Backend Documentation

## Technologies
- **FastAPI**: For building the API.
- **Pinecone**: For vector database management.
- **OpenAI**: For AI-twin functionalities.

## Folder Structure
- `routes/`: API endpoint definitions.
- `services/`: Business logic and service integrations.
- `utils/`: Utility functions and helpers.

## Coding Standards
- Use snake_case for Python function and variable names.
- Write docstrings for all functions and classes.
- Use type hints for better code clarity and Cursor assistance.

## Development
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```bash
   uvicorn main:app --reload
   ```

4. Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs)

## Environment Variables
Create a `.env` file in the backend directory with the following variables:
```
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
``` 