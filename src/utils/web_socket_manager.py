from fastapi import WebSocket
from typing import Dict

from config.settings import logger


class WebSocketManager:
    def __init__(self,):
        self.active_connections: Dict[str, WebSocket] = {}

    def add_connection(self, user_id: str, websocket: WebSocket):
        self.active_connections[user_id] = websocket

    def remove_connection(self, user_id: str):
        del self.active_connections[user_id]

    async def broadcast_message(self, sender_id: str, message: dict):
        logger.debug(f"active connections: {self.active_connections}")
        for user_id, websocket in self.active_connections.items():
            message["sender_id"] = sender_id
            if user_id == sender_id or user_id == message.get("receiver_id"):
                await websocket.send_json(message)


web_socket_manager = WebSocketManager()
