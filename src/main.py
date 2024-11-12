from fastapi import FastAPI
from config.database import db
from routes.routes import router
from fastapi.responses import HTMLResponse

db.connect()
app = FastAPI()
app.include_router(router)

# a html page to test the websockets
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/api/v1/web_socket/1");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
@app.get("/")
async def get():
    return HTMLResponse(html)
# TODO:
# - 1 implementar persistencia de mensajes de cada chat en la base de datos
# - 2 implementar un endpoint para crear un chat (id de los dos usuarios) (devuelve el id del chat)
# - 3 implementar un endpoint para obtener todos los mensajes de un chat
# - 4 implementar un endpoint para obtener todos los chats (id) de un usuario ??
# - 5 teatear los endpoints con postman