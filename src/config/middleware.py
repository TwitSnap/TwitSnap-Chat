from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from config.settings import logger


def configure_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def log_request_middleware(request: Request, call_next):
        method = request.method
        url = request.url
        logger.info(f"Request url: {url} | Method: {method} ")
        response = await call_next(request)
        logger.info(f"Response status code: {response.status_code}")
        return response
