import logging
import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from app.composition.config_bootstrap import load_config
from app.composition.logging_bootstrap import setup_logging
from app.presentation.api import routes as ai_routes

load_dotenv()
config = load_config()
setup_logging(config.logging)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="LLMBox",
    description="API для работы с LLM",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/docs/openapi.json"
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    client_ip = request.client.host
    method = request.method
    url = str(request.url)

    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"REQUEST ERROR: {method} {url} - Error: {str(e)} - Time: {process_time:.2f}s", exc_info=True)
        return JSONResponse(status_code=500, content={"detail": "Internal server error", "error": str(e)})


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"GLOBAL EXCEPTION: {request.method} {request.url} - {str(exc)}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal server error", "error": str(exc)})


app.include_router(ai_routes.router)

logger.info("FastAPI application started successfully")

if __name__ == "__main__":
    host = config.application.host
    port = config.application.port

    logger.info(f"Запуск LLMBox на http://{host}:{port}")
    logger.info(f"Документация API: http://{host}:{port}/docs")
    logger.info(f"Health check: http://{host}:{port}/health")
    logger.info(f"Логи сохраняются в файл: {config.logging.file}")

    uvicorn.run("main:app", host=host, port=port, reload=False, log_level="info")
