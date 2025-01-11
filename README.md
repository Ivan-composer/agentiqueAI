# AgentiqueAI

Agentique is an AI-powered platform that allows users to interact with AI-twins of content creators for personalized consultations. The project is structured as a monorepo with separate `frontend` and `backend` directories.

## Technologies Used
- **Frontend**: React, Next.js, Tailwind CSS
- **Backend**: Python, FastAPI, Pinecone

## Project Structure
```
agentiqueAI/
├── README.md
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
    ├── main.py
    └── app/
        ├── __init__.py
        ├── routes/
        ├── services/
        └── utils/
```

## Getting Started
### Frontend
1. Navigate to `frontend/`
2. Install dependencies: `npm install`
3. Run the development server: `npm run dev`

### Backend
1. Navigate to `backend/`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the server: `uvicorn main:app --reload`

## API Documentation
The backend API is documented using FastAPI's automatic Swagger UI available at `/docs` when the server is running.

## Contribution Guidelines
- Ensure consistent code style using Prettier for frontend and Black for backend.
- Write clear docstrings for Python functions and comments for React components.