import logging
from functools import wraps
from typing import Callable, Any

from fastapi import HTTPException

logger = logging.getLogger(__name__)


def handle_service_errors(endpoint_name: str = None):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            name = endpoint_name or func.__name__
            try:
                return await func(*args, **kwargs)
            except ValueError as exc:
                logger.error("%s VALIDATION ERROR: error=%s", name.upper(), exc)
                raise HTTPException(status_code=400, detail=str(exc))
            except Exception as exc:
                logger.error("%s CRITICAL ERROR: error=%s", name.upper(), exc, exc_info=True)
                raise HTTPException(status_code=500, detail=f"Failed to process {name} request")

        return wrapper

    return decorator
