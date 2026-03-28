import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.bootstrap import get_logger, load_config
from app.llm.infrastructure import routes as ai_routes

load_dotenv()

app = FastAPI(title="LLMBox", description="API для работы с LLM", version="1.0.0", docs_url="/docs", openapi_url="/docs/openapi.json")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    get_logger().log_error(f"GLOBAL EXCEPTION: {request.method} {request.url} - {str(exc)}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error", "error": str(exc)})


app.include_router(ai_routes.router)

if __name__ == "__main__":
    config = load_config()
    host = config.application.host
    port = config.application.port

    logger = get_logger()

    logger.log_info(f"Запуск на http://{host}:{port}")

    uvicorn.run("main:app", host=host, port=port, reload=False, log_level="info")
