# Project Overview
Agentique is an AI-powered platform allowing users to interact with "AI-twins" of content creators for personalized consultations. The project is structured as a monorepo with two main directories:

- frontend/ – A Next.js application (using Tailwind CSS).
- backend/ – A FastAPI-based Python application.

We use Replit to host and run two separate Repls (one for the frontend, one for the backend) and GitHub for version control. Cursor is our local AI-powered coding assistant to help with generating, refactoring, and documenting code.

## Monorepo Structure
```
agentique-project/
├── README.md
├── INSTRUCTIONS.md         # This file
├── frontend/
│   ├── package.json
│   ├── tailwind.config.js
│   ├── next.config.js
│   └── src/
│       ├── pages/
│       ├── components/
│       └── styles/
└── backend/
    ├── requirements.txt
    ├── pyproject.toml
    ├── main.py
    └── app/
        ├── __init__.py
        ├── routes/
        ├── services/
        └── utils/
```

## Frontend Details
Framework: Next.js (React)
Styling: Tailwind CSS

Typical Scripts:
- `npm install` to install dependencies
- `npm run dev` to start the development server
- `npm run build` for production build

## Backend Details
Framework: FastAPI (Python)

Key Dependencies:
- fastapi, uvicorn for the server
- openai (>=1.0.0) for embeddings generation
- pinecone-client (>=2.2.4) for vector similarity search
- python-dotenv (>=1.0.0) for environment variable management
- pydantic (>=2.4.2) for data validation
- black (>=23.11.0) for code formatting

Typical Scripts:
- `pip install -r requirements.txt` to install dependencies
- `uvicorn main:app --reload` to start the FastAPI server

## AI Service Implementation
The project includes a centralized AI service (`backend/app/services/ai_service.py`) that handles:
- OpenAI embeddings generation
- Pinecone vector similarity search
- Vector upserting and deletion
- Proper error handling and logging

Example AI Service Usage:
```python
from app.services.ai_service import AIService

# Initialize the service
ai_service = AIService()

# Generate embeddings
embedding = ai_service.generate_embedding("Your text here")

# Query similar vectors
results = ai_service.query_pinecone(embedding)
```

## Coding Standards

### General
- Keep code modular and well-structured.
- Write descriptive commit messages (what was changed and why).
- Use docstrings/comments for complex logic or unclear code sections.

### Frontend (Next.js & Tailwind)
- Component Naming: Use PascalCase for React components.
- Functional Components: Prefer functional components over class components.
- Tailwind Usage:
  - Keep styling inline using Tailwind classes (`className="bg-blue-500 text-white p-4"`).
  - Avoid mixing external CSS files for basic styling if possible.
- Commenting: Use JSDoc-style comments for component documentation.

Example:
```jsx
/**
 * A sample header component for the Agentique front-end.
 * @returns {JSX.Element} The rendered header.
 */
const Header = () => (
  <header className="bg-blue-500 p-4 text-white">
    <h1>Agentique</h1>
  </header>
);
export default Header;
```

### Backend (FastAPI & Python)
- Naming: Use snake_case for functions, variables, and file names.
- Type Hints: Add Python type hints wherever possible (`def my_function(param: str) -> int:`).
- Docstrings: Provide docstrings for all functions and classes (Google or NumPy style is fine).

Example:
```python
def read_root() -> dict:
    """
    Root endpoint returning a welcome message.

    Returns:
        dict: A dictionary containing the welcome message.
    """
    return {"message": "Welcome to the Agentique backend!"}
```

Project Organization:
- routes/ for FastAPI endpoints
- services/ for business logic or third-party integrations (e.g., AI calls)
- utils/ for helper functions

## Linters & Formatters

### Frontend: Use Prettier for code formatting
Example .prettierrc:
```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "es5"
}
```

### Backend: Use Black for code formatting
Example pyproject.toml:
```toml
[tool.black]
line-length = 88
target-version = ['py38']
```

## Development Workflow

### Local Development (Cursor + GitHub)
1. Clone the project locally with --depth 1 to save disk space.
2. Open the entire agentique-project/ folder in Cursor so it can assist with both frontend/ and backend/.
3. Make changes (new features, bug fixes, documentation) with Cursor's guidance.
4. Commit changes and push to GitHub.

### Deployment on Replit
We have two separate Repls:
- Frontend Repl (imports frontend/ from GitHub)
- Backend Repl (imports backend/ from GitHub)
- Pull the latest changes into each Repl from GitHub to see your updates run live.

### Testing & Iteration
- Frontend: Access your Next.js dev server (e.g., on localhost:3000 locally or Replit's generated URL).
- Backend: Access your FastAPI endpoints at localhost:8000 (or Replit's URL), with interactive docs at /<your-repl-url>/docs.

## Environment Variables and Secrets

### Required Environment Variables for AI Service:
```
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment  # e.g., us-west1-gcp
```

### Replit Secrets Manager:
Store the following API keys in each Repl's Secrets panel:
- OPENAI_API_KEY: For OpenAI API access
- PINECONE_API_KEY: For Pinecone vector database access
- PINECONE_ENVIRONMENT: Your Pinecone environment (e.g., us-west1-gcp)

### Accessing Secrets:
Backend (Python):
```python
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

Frontend (Next.js):
- Use .env.local for local development, Replit's Secrets for production.
- Access via process.env.NEXT_PUBLIC_API_URL or similar.

## Helpful Commands & Scripts

### Frontend (from frontend/)
```bash
npm install         # Install dependencies
npm run dev         # Start dev server
npm run build      # Build for production
npm run start      # Start the production server
```

### Backend (from backend/)
```bash
pip install -r requirements.txt          # Install dependencies
uvicorn main:app --reload               # Run in dev mode
uvicorn main:app --host 0.0.0.0 --port 8000 # Custom host/port
```

### Git & GitHub
Add & Commit:
```bash
git add .
git commit -m "Descriptive commit message"
```

Push to GitHub:
```bash
git push origin main
```

Pull in Replit:
- Open each Repl, go to Version Control, click Pull.

## Additional Tips
- Consistent, Frequent Commits: Commit small, incremental changes often with clear messages.
- Testing: Test each feature in local dev (Cursor environment) and again on Replit.
- Refactoring: Use Cursor's AI capabilities to refactor and optimize code regularly.
- Documentation: Update these instructions and each folder's README as the project evolves.

## Final Notes
- Cursor: Always refer to this file for guidance on code style, folder structure, and best practices.
- Renaming: We've renamed the project from Fantique to Agentique, so ensure references use Agentique.
- Long-Term Goal: Build a maintainable, scalable AI-based platform for personalized content creator interactions.

Thank you for contributing to Agentique! 