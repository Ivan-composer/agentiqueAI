"""
logger.py: Comprehensive logging setup capturing both application and server logs.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
os.makedirs(logs_dir, exist_ok=True)

# Configure logging
logger = logging.getLogger("agentique")
logger.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
console_handler.setFormatter(console_formatter)

# File handler
file_handler = RotatingFileHandler(
    os.path.join(logs_dir, "app.log"),
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
file_handler.setFormatter(file_formatter)

# Add handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Configure root logger to capture all logs
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)

# Configure Uvicorn logger
uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.handlers = []  # Remove default handlers
uvicorn_logger.addHandler(file_handler)
uvicorn_logger.addHandler(console_handler)

# Also capture other important loggers
for logger_name in ["uvicorn.error", "fastapi", "telethon", "pinecone", "openai"]:
    module_logger = logging.getLogger(logger_name)
    module_logger.handlers = []  # Remove any existing handlers
    module_logger.addHandler(file_handler)
    module_logger.addHandler(console_handler)

# Export the logger object
__all__ = ['logger'] 