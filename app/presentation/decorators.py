import logging
from functools import wraps
from typing import Callable, Any

from fastapi import HTTPException

from app.application.exceptions import (
    ApplicationException,
    ValidationException,
    ServiceUnavailableException,
)

logger = logging.getLogger(__name__)


def handle_service_errors(endpoint_name: str = None):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            name = endpoint_name or func.__name__
            try:
                return await func(*args, **kwargs)
            except ValidationException as exc:
                logger.error("%s VALIDATION ERROR: %s", name.upper(), exc)
                raise HTTPException(status_code=400, detail=str(exc))
            except ServiceUnavailableException as exc:
                logger.error(
                    "%s AI SERVICE ERROR: %s (original: %s)",
                    name.upper(),
                    exc,
                    exc.original_error if getattr(exc, "original_error", None) else "N/A",
                    exc_info=True
                )
                raise HTTPException(status_code=502, detail=f"AI service error: {str(exc)}")
            except ApplicationException as exc:
                logger.error("%s APPLICATION ERROR: %s", name.upper(), exc)
                raise HTTPException(status_code=400, detail=str(exc))
            except Exception as exc:
                logger.error("%s CRITICAL ERROR: error=%s", name.upper(), exc, exc_info=True)
                raise HTTPException(status_code=500, detail=f"Failed to process {name} request")

        return wrapper

    return decorator
