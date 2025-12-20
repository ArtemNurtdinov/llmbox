import logging
from functools import wraps
from typing import Callable, Any

from fastapi import HTTPException

from app.domain.exceptions import DomainException, UnknownAIAssistantException, AIServiceException

logger = logging.getLogger(__name__)


def handle_service_errors(endpoint_name: str = None):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            name = endpoint_name or func.__name__
            try:
                return await func(*args, **kwargs)
            except UnknownAIAssistantException as exc:
                logger.error("%s VALIDATION ERROR: %s", name.upper(), exc)
                raise HTTPException(status_code=400, detail=str(exc))
            except AIServiceException as exc:
                logger.error(
                    "%s AI SERVICE ERROR: %s (original: %s)",
                    name.upper(),
                    exc,
                    exc.original_error if exc.original_error else "N/A",
                    exc_info=True
                )
                raise HTTPException(status_code=502, detail=f"AI service error: {str(exc)}")
            except DomainException as exc:
                logger.error("%s DOMAIN ERROR: %s", name.upper(), exc)
                raise HTTPException(status_code=400, detail=str(exc))
            except Exception as exc:
                logger.error("%s CRITICAL ERROR: error=%s", name.upper(), exc, exc_info=True)
                raise HTTPException(status_code=500, detail=f"Failed to process {name} request")

        return wrapper

    return decorator
