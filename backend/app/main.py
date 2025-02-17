"""
Main FastAPI application module.
"""
import os
from dotenv import load_dotenv

# Load environment variables before importing services
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.utils.logger import logger
from app.services.openai_service import client as openai_client
from app.services.pinecone_service import pc as pinecone_client
from app.services.db_service import supabase
from app.routes import agent, auth, telegram

app = FastAPI(title="Agentique API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(agent.router, prefix="/agent", tags=["agent"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(telegram.router, prefix="/telegram", tags=["telegram"])

@app.get("/health")
async def health_check():
    """
    Health check endpoint that verifies all external services are accessible.
    
    Returns:
        dict: Status of each service and overall health
        
    Raises:
        HTTPException: If any critical service is unavailable
    """
    status = {
        "status": "healthy",
        "services": {
            "openai": "unknown",
            "pinecone": "unknown",
            "supabase": "unknown"
        }
    }
    
    try:
        # Check OpenAI
        await openai_client.models.list()
        status["services"]["openai"] = "healthy"
    except Exception as e:
        logger.error("OpenAI health check failed: %s", str(e))
        status["services"]["openai"] = "unhealthy"
    
    try:
        # Check Pinecone
        pinecone_client.list_indexes()
        status["services"]["pinecone"] = "healthy"
    except Exception as e:
        logger.error("Pinecone health check failed: %s", str(e))
        status["services"]["pinecone"] = "unhealthy"
    
    try:
        # Check Supabase
        supabase.table("users").select("*").limit(1).execute()
        status["services"]["supabase"] = "healthy"
    except Exception as e:
        logger.error("Supabase health check failed: %s", str(e))
        status["services"]["supabase"] = "unhealthy"
    
    # If any service is unhealthy, mark overall status as unhealthy
    if any(s == "unhealthy" for s in status["services"].values()):
        status["status"] = "unhealthy"
        raise HTTPException(
            status_code=503,
            detail=status
        )
    
    return status 