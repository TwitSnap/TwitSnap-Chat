from datetime import datetime
from typing import Dict
from fastapi import WebSocket, status
from repository.chat_repository import chat_repository
from repository.chat_repository import ChatRepository
from config.settings import logger
from external.twitsnap_service import twitsnap_service
from models.message import Message
from exceptions.resource_not_found_exception import ResourceNotFoundException


class ChatService:
    def __init__(self, chat_repository: ChatRepository, twitsnap_service):
        self.active_connections: Dict[str, WebSocket] = {}
        self.chat_repository = chat_repository
        self.twitsnap_service = twitsnap_service

    def add_connection(self, user_id: str, websocket: WebSocket):
        self.active_connections[user_id] = websocket

    def remove_connection(self, user_id: str):
        del self.active_connections[user_id]

    async def create_chat(self, uid_1: str, uid_2: str):
        existing_chat = await self.chat_repository.get_chat_by_participants(
            uid_1, uid_2
        )
        if existing_chat:
            logger.debug(f"Chat already exists: {existing_chat}")
            logger.debug(f"Chat id: {existing_chat.get('_id')}")
            return {"chat_id": str(existing_chat.get("_id"))}

        logger.debug(f"Creating new chat between {uid_1} and {uid_2}")
        chat = await self.chat_repository.create_chat(uid_1, uid_2)
        logger.debug(f"Chat id: {chat.get('_id')}")
        return {"chat_id": str(chat.get("_id"))}

    async def create_message(self, msg: Message):
        return await self.chat_repository.create_message(msg)

    async def update_chat(self, chat_id: str, message_id: str):
        return await self.chat_repository.update_chat(chat_id, message_id)

    async def broadcast_message(self, sender_id: str, message: dict):
        logger.debug(f"active connections: {self.active_connections.keys()}")

        chat = await self.create_chat(sender_id, message.get("receiver_id"))
        logger.debug(f"Chat created: {chat}")
        chat_id = chat.get("chat_id")
        message["sender_id"] = sender_id
        message["chat_id"] = chat_id

        msg = await self.create_message(
            Message(
                chat_id=str(chat.get("chat_id")),
                sender_id=sender_id,
                content=message.get("message"),
                timestamp=datetime.now(),
            )
        )
        logger.debug(f"Message created: {msg}")

        result = await self.update_chat(chat_id, msg.get("_id"))

        if result.modified_count == 0:
            logger.debug(f"Chat not updated: {result}")

        for user_id, websocket in self.active_connections.items():
            if user_id == sender_id or user_id == message.get("receiver_id"):
                # logger.debug(f"Sending message to user {user_id}, message: {message}")
                await websocket.send_json(message)


chat_service = ChatService(chat_repository, twitsnap_service)
