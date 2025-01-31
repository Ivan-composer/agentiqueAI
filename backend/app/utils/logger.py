"""
logger.py: Comprehensive logging setup capturing both application and server logs.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

# Ensure we have a logs directory
os.makedirs("logs", exist_ok=True)

# Create formatters
detailed_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
uvicorn_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

# Set up file handler
file_handler = RotatingFileHandler(
    "logs/server.log",
    maxBytes=5_000_000,  # 5 MB
    backupCount=3        # keep up to 3 old log files
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(detailed_formatter)

# Set up console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(detailed_formatter)

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

# Configure our application logger
logger = logging.getLogger("agentique")
logger.setLevel(logging.DEBUG)
logger.propagate = False  # Prevent double logging
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Also capture other important loggers
for logger_name in ["uvicorn.error", "fastapi", "telethon", "pinecone", "openai"]:
    module_logger = logging.getLogger(logger_name)
    module_logger.handlers = []  # Remove any existing handlers
    module_logger.addHandler(file_handler)
    module_logger.addHandler(console_handler)

# Export the logger object
__all__ = ['logger'] 