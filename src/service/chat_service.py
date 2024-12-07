import json
import uuid
from datetime import datetime
from typing import Dict
from fastapi import WebSocket
from repository.chat_repository import chat_repository
from repository.chat_repository import ChatRepository
from config.settings import logger
from external.twitsnap_service import twitsnap_service
from models.message import Message
from exceptions.resource_not_found_exception import ResourceNotFoundException
from fastapi.websockets import WebSocketDisconnect
from exceptions.bad_request_exception import BadRequestException
from dtos.chat import Chat
from dtos.chat_messages_response import ChatMessagesResponse
from dtos.message import MessageResponse


class ChatService:
    def __init__(self, chat_repository: ChatRepository, twitsnap_service):
        self.active_connections: Dict[str:Dict[str:WebSocket]] = {}
        self.chat_repository = chat_repository
        self.twitsnap_service = twitsnap_service

    def add_connection(self, user_id: str, device_id:str, websocket: WebSocket):
        if user_id not in self.active_connections:
            self.active_connections[user_id] = {}
        self.active_connections[user_id][device_id] = websocket

    def remove_connection(self, user_id: str, device_id: str ):
        del self.active_connections[user_id][device_id]

    async def manage_connection(self, websocket: WebSocket, user_id: str):
        device_id = str(uuid.uuid4())
        self.add_connection(user_id,device_id,websocket)
        try:
            while True:
                data = await websocket.receive_text()
                logger.debug(f"Data received: {data}")
                message = json.loads(data)
                await self.broadcast_message(user_id, message)
        except WebSocketDisconnect:
            logger.debug(f"User {user_id} disconnected")
            self.remove_connection(user_id, device_id)

    async def create_chat(self, my_user: str, other_user: str):
        verify_other_user = await self.twitsnap_service.get_user(other_user)
        if verify_other_user is None:
            raise ResourceNotFoundException(detail="User not found")

        if my_user == other_user:
            raise BadRequestException(detail="Cannot create chat with yourself")

        existing_chat = await self.chat_repository.get_chat_by_participants(
            my_user, other_user
        )
        if existing_chat:
            logger.debug(f"Chat already exists: {existing_chat}")
            logger.debug(f"Chat id: {existing_chat.get('_id')}")
            return Chat(id=str(existing_chat.get("_id")),
                        participants=existing_chat.get("participants"))

        logger.debug(f"Creating new chat between {my_user} and {other_user}")
        chat = await self.chat_repository.create_chat(my_user, other_user)
        logger.debug(f"Chat id: {chat.get('_id')}")
        return Chat(id=str(chat.get("_id")),
                    participants=chat.get("participants"))

    async def create_message(self, msg: Message):
        return await self.chat_repository.create_message(msg)

    async def update_chat(self, chat_id: str, message_id: str):
        return await self.chat_repository.update_chat(chat_id, message_id)

    async def broadcast_message(self, sender_id: str, message: dict):
        my_user = await twitsnap_service.get_user(sender_id)
        receiver_user = await twitsnap_service.get_user(message.get("receiver_id"))
        if receiver_user is None:
            logger.debug(f"websocket: user {message.get('receiver_id')} not found")
            return

        chat = await self.create_chat(sender_id, message.get("receiver_id"))
        chat_id = chat.id
        message["sender_id"] = sender_id
        message["chat_id"] = chat_id

        msg = await self.create_message(
            Message(
                chat_id=chat_id,
                sender_id=sender_id,
                message=message.get("message"),
                timestamp=datetime.now(),
            )
        )
        logger.debug(f"Message created: {msg}")
        message['id'] = str(msg.get("_id"))
        result = await self.update_chat(chat_id, msg.get("_id"))

        if result.modified_count == 0:
            logger.debug(f"Chat not updated: {result}")

        logger.debug(f"Broadcasting message: {message}")
        logger.debug(f"active connections: {self.active_connections.keys()}")
        for user_id in chat.participants:
            if user_id in self.active_connections:
                for device_id, websocket in self.active_connections[user_id].items():
                    await websocket.send_json(message)
        logger.debug(f"Message broadcasted")

        # if receiver_user.get("uid") not in chat.participants:
        logger.debug(f"Sending push notification to {receiver_user.get('uid')}")
        await self.twitsnap_service.send_new_message_notification(my_user.get("username"), receiver_user.get("device_token"))

    async def _get_chat_by_id(self, chat_id: str):
        chat = await self.chat_repository.get_chat_by_id(chat_id)
        if chat is None:
            raise ResourceNotFoundException("Chat not found")
        return chat

    async def get_chat_by_id(self, chat_id: str, limit: int, cursor: str):
        logger.debug(f"Getting messages for chat {chat_id}")
        messages = await self.chat_repository.get_chat_messages(chat_id, limit, cursor)

        if len(messages)>0:
            cursor = str(messages[-1].get("_id"))
        else:
            cursor = None
        messages = [MessageResponse(id=str(msg.get("_id")),
                            sender_id=msg.get("sender_id"),
                            message=msg.get("message"),
                            timestamp=msg.get("timestamp"))
                            for msg in messages]

        res = ChatMessagesResponse(messages=messages, next_cursor=cursor)
        logger.debug(f"return chat: {res}")
        return res

    async def get_my_chats(self, user_id: str, limit: int, offset: int):
        res = []
        chats = await self.chat_repository.get_my_chats(user_id, limit, offset)

        for chat in chats:
            chat["participants"].remove(user_id)
            user = await self.twitsnap_service.get_user(chat.get("participants")[0])
            last_message = await self.chat_repository.get_message_by_id(
                chat.get("last_message")
            )
            res.append(
                Chat(
                    id=str(chat.get("_id")),
                    user={
                        "uid": user.get("uid"),
                        "username": user.get("username"),
                        "photo": user.get("photo"),
                    },
                    last_message=MessageResponse(
                        id=str(last_message.get("_id")),
                        sender_id=str(last_message.get("sender_id")),
                        message=last_message.get("message"),
                        timestamp=last_message.get("timestamp"),
                    )
                )
            )
        logger.debug(f"return chats: {res}")
        return res


chat_service = ChatService(chat_repository, twitsnap_service)
