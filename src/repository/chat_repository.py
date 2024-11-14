from xml.sax import parse

from models.chat import Chat
from models.message import Message
from config.database import db
from config.settings import logger
from typing import List
from bson import ObjectId


class ChatRepository:
    def __init__(self, db):
        self.db = db
        self.chat_collection = db.get_collection("chats")
        self.message_collection = db.get_collection("messages")

    async def create_chat(self, uid_1: str, uid_2: str):
        new_chat = Chat(participants=[uid_1, uid_2], messages=[])
        result = await self.chat_collection.insert_one(new_chat.dict())
        return await self.chat_collection.find_one({"_id": result.inserted_id})

    async def create_message(self, msg: Message):
        result = await self.message_collection.insert_one(msg.dict())
        return await self.message_collection.find_one({"_id": result.inserted_id})

    async def update_chat(self, chat_id: str, message_id: str):
        return await self.chat_collection.update_one(
            {"_id": ObjectId(chat_id)}, {"$set": {"last_message": ObjectId(message_id)}}
        )


chat_repository = ChatRepository(db.get_db())
