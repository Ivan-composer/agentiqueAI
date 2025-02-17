"""
Main FastAPI application file for the Agentique backend.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import agent, auth, chat, search, admin, credits

app = FastAPI(
    title="Agentique API",
    description="Backend API for the Agentique AI platform",
    version="1.0.0"
)

# Define allowed origins
origins = [
    "http://localhost:3000",  # Frontend in development
    "https://your-frontend-domain.com",  # Frontend in production - replace with actual domain
]

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(agent.router, prefix="/agent", tags=["Agents"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(credits.router)

@app.get("/")
async def root():
    """Root endpoint returning a welcome message."""
    return {"message": "Agentique Backend API is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint to verify server status."""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
