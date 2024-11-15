import json
from datetime import datetime
from typing import Dict
from fastapi import WebSocket, status
from repository.chat_repository import chat_repository
from repository.chat_repository import ChatRepository
from config.settings import logger
from external.twitsnap_service import twitsnap_service
from models.message import Message
from exceptions.resource_not_found_exception import ResourceNotFoundException
from fastapi.websockets import WebSocketDisconnect
from exceptions.bad_request_exception import BadRequestException


class ChatService:
    def __init__(self, chat_repository: ChatRepository, twitsnap_service):
        self.active_connections: Dict[str, WebSocket] = {}
        self.chat_repository = chat_repository
        self.twitsnap_service = twitsnap_service

    def add_connection(self, user_id: str, websocket: WebSocket):
        self.active_connections[user_id] = websocket

    def remove_connection(self, user_id: str):
        del self.active_connections[user_id]

    async def manage_connection(self, websocket: WebSocket, user_id: str):
        self.add_connection(user_id, websocket)
        try:
            while True:
                data = await websocket.receive_text()
                logger.debug(f"Data received: {data}")
                message = json.loads(data)
                await self.broadcast_message(user_id, message)
        except WebSocketDisconnect:
            logger.debug(f"User {user_id} disconnected")
            self.remove_connection(user_id)

    async def create_chat(self, uid_1: str, uid_2: str):
        if uid_1 == uid_2:
            raise BadRequestException(detail="Cannot create chat with yourself")

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
        chat_id = chat.get("chat_id")
        message["sender_id"] = sender_id
        message["chat_id"] = chat_id

        msg = await self.create_message(
            Message(
                chat_id=str(chat.get("chat_id")),
                sender_id=sender_id,
                message=message.get("message"),
                timestamp=datetime.now(),
            )
        )
        logger.debug(f"Message created: {msg}")

        result = await self.update_chat(chat_id, msg.get("_id"))

        if result.modified_count == 0:
            logger.debug(f"Chat not updated: {result}")

        logger.debug(f"Broadcasting message: {message}")
        for user_id, websocket in self.active_connections.items():
            if user_id == sender_id or user_id == message.get("receiver_id"):
                logger.debug(f"sending message to user {user_id}")
                await websocket.send_json(message)

    async def _get_chat_by_id(self, chat_id: str):
        chat = await self.chat_repository.get_chat_by_id(chat_id)
        if chat is None:
            raise ResourceNotFoundException("Chat not found")
        return chat

    async def get_chat_by_id(self, chat_id: str, limit: int, offset: int):
        logger.debug(f"Getting messages for chat {chat_id}")
        msg = await self.chat_repository.get_chat_messages(chat_id, limit, offset)
        res = {"chat_id": chat_id, "messages": msg}
        logger.debug(f"return chat: {res}")
        return res

    async def get_my_chats(self, user_id: str, limit: int, offset: int):
        res = {"chats": []}
        chats = await self.chat_repository.get_my_chats(user_id, limit, offset)
        for chat in chats:
            chat["chat_id"] = str(chat.get("_id"))
            chat["participants"].remove(user_id)
            user = await self.twitsnap_service.get_user(chat.get("participants")[0])
            last_message = await self.chat_repository.get_message_by_id(
                chat.get("last_message")
            )
            res["chats"].append(
                {
                    "chat_id": str(chat.get("_id")),
                    "user": {
                        "uid": user.get("uid"),
                        "username": user.get("username"),
                        "photo": user.get("photo"),
                    },
                    "last_message": last_message,
                }
            )
        logger.debug(f"return chats: {res}")
        return res


chat_service = ChatService(chat_repository, twitsnap_service)
