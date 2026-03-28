from collections.abc import Callable
from functools import wraps
from typing import Any

from fastapi import HTTPException

from app.llm.application.exception.unavailable_service import ServiceUnavailableException
from app.llm.application.exception.validation import ValidationException


def handle_service_errors(endpoint_name: str = None):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            name = endpoint_name or func.__name__
            try:
                return await func(*args, **kwargs)
            except ValidationException as exc:
                raise HTTPException(status_code=400, detail=str(exc))
            except ServiceUnavailableException as exc:
                raise HTTPException(status_code=502, detail=f"AI service error: {str(exc)}")
            except Exception:
                raise HTTPException(status_code=500, detail=f"Failed to process {name} request")

        return wrapper

    return decorator
