from fastapi import FastAPI
from routes.routes import router
from config.open_api_doc import configure_openapi
from config.middleware import configure_middleware
from config.settings import HOST, PORT
import uvicorn
app = FastAPI()
app.include_router(router)
configure_openapi(app)
configure_middleware(app)

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=int(PORT))

# TODO:
# - 1 paginar los endpoints
# - 2 agregar tests
