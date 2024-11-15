from fastapi.openapi.utils import get_openapi

def configure_openapi(app):
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="Twit-Snap Chat Service",
            description= websocket_doc,
            version="1.0.0",
            routes=app.routes,
        )
        for path, path_item in openapi_schema["paths"].items():
            if path.startswith("/api/v1"):
                for method in path_item.values():
                    if "parameters" not in method:
                        method["parameters"] = []
                    method["parameters"].append(
                        {
                            "in": "header",
                            "name": "user_id",
                            "required": False,
                            "schema": {"type": "string"},
                            "description": "user id",
                        }
                    )
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi


websocket_doc = """
    WebSocket 

    ### Conexión
    - Conectar a `wss://<host>/web_socket/{user_id}` donde `user_id` es del usuario logeado.

    ### Formato de los mensajes

    #### Envío de mensajes:
    - Los mensajes deben ser enviados en formato JSON con la siguiente estructura:
      ```json
      {
          "receiver_id": "1234",
          "message": "Hola"
      }
      ```
    - `receiver_id`: (str) ID del usuario destinatario del mensaje.
    - `message`: (str) Contenido del mensaje que se desea enviar.

    #### Recepción de mensajes:
    - Los mensajes recibidos serán en formato JSON con los siguientes campos:
      ```json
      {
          "chat_id": "5678",
          "sender_id": "4321",
          "message": "Hola",
          "timestamp": "2024-11-14T15:30:00"
      }
      ```
    - `chat_id`: (str) ID único del chat.
    - `sender_id`: (str) ID del usuario que envió el mensaje.
    - `message`: (str) Contenido del mensaje recibido.
    - `timestamp`: Fecha y hora en que se envió el mensaje, en formato ISO 8601."
"""