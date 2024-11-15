from config.middleware import configure_middleware
from fastapi import FastAPI
from config.open_api_doc import configure_openapi
from routes.routes import router

app = FastAPI()
configure_middleware(app)
app.include_router(router)
configure_openapi(app)
