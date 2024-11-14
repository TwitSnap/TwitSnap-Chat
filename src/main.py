from fastapi import FastAPI
from routes.routes import router
from config.open_api_doc import configure_openapi

app = FastAPI()
app.include_router(router)

# TODO:

# - 2 implementar un endpoint para crear un chat entre dos usuarios, si ya existe devolver id chat existente
# - 3 implementar un endpoint para obtener chat por id
# - 4 implementar un endpoint para obtener todos los chats de un usuario ??
# - 5 teatear los endpoints con postman
# - 6 paginar los mensajes de un chat
