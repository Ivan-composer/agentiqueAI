from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import chat_routes, auth, comment, agent
import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
import sys

# Create logs directory if it doesn't exist
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(
            log_dir / "server.log",
            maxBytes=10000000,  # 10MB
            backupCount=5
        ),
        logging.StreamHandler(sys.stdout)
    ]
)

# Get logger for this module
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Agentique API",
    description="API for Telegram channel agents with RAG capabilities",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with correct prefixes
app.include_router(chat_routes.router, prefix="/chat", tags=["chat"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(comment.router, prefix="/comment", tags=["comment"])
app.include_router(agent.router, prefix="/agent", tags=["agent"])

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting Agentique API server...")
    from .services.vector_service import vector_service
    await vector_service.verify_index()
    logger.info("Vector service initialized")

@app.get("/")
async def root():
    """Root endpoint for health check"""
    logger.info("Health check requested")
    return {
        "status": "ok",
        "message": "Agentique API is running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.info("Health check requested")
    return {
        "status": "healthy",
        "version": "1.0.0"
    }
