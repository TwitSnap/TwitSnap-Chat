import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from utils.web_socket_manager import web_socket_manager

from config.settings import logger

chat_router = APIRouter()

@chat_router.websocket("/web_socket/{user_id}")
async def websocket_endpoint(websocket: WebSocket, sender_id: str):
    await websocket.accept()
    logger.debug(f"WebSocket connection established for user {sender_id}")
    web_socket_manager.add_connection(sender_id, websocket)

    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)
            receiver_id = data.get("receiver_id")
            message_content = data.get("message")
            timestamp = data.get("timestamp")
            logger.debug(f"Received message from user {sender_id} to user {receiver_id}: {message_content}")
            await web_socket_manager.broadcast_message(sender_id, data)

    except WebSocketDisconnect:
        logger.info(f"WebSocket connection closed for user {sender_id}")
        web_socket_manager.remove_connection(sender_id)
