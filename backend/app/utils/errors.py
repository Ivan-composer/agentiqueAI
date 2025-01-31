"""
errors.py: Centralized error handling for the application.

This module defines custom exceptions and error handlers for various
service-level errors that can occur in the application.
"""
from fastapi import HTTPException
from typing import Optional, Dict, Any

class ServiceError(Exception):
    """Base class for service-level errors."""
    def __init__(self, message: str, status_code: int = 500, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class ServiceUnavailableError(ServiceError):
    """Raised when an external service (OpenAI, Pinecone) is unavailable."""
    def __init__(self, service_name: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"{service_name} service is currently unavailable",
            status_code=503,
            details=details
        )

class InsufficientCreditsError(ServiceError):
    """Raised when a user doesn't have enough credits."""
    def __init__(self, current_balance: int, required_amount: int):
        super().__init__(
            message="Insufficient credits for this operation",
            status_code=403,
            details={
                "current_balance": current_balance,
                "required_amount": required_amount
            }
        )

class TelegramError(ServiceError):
    """Raised when there's an error with Telegram operations."""
    def __init__(self, operation: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"Telegram {operation} operation failed",
            status_code=500,
            details=details
        )

def handle_service_error(error: ServiceError) -> HTTPException:
    """Convert a ServiceError to an HTTPException."""
    return HTTPException(
        status_code=error.status_code,
        detail={
            "message": error.message,
            "details": error.details
        }
    ) 