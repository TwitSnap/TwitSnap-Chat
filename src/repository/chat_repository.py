from xml.sax import parse

from models.chat import Chat
from models.message import Message
from config.database import db
from config.settings import logger
from typing import List
from bson import ObjectId
from datetime import datetime

class ChatRepository:
    def __init__(self, db):
        self.db = db
        self.chat_collection = db.get_collection("chats")
        self.message_collection = db.get_collection("messages")

    def create_index(self):
        self.chat_collection.create_index([("participants", 1)])
        self.chat_collection.create_index([("last_updated", -1)])
        self.message_collection.create_index([("timestamp",-1)])
        self.message_collection.create_index([("chat_id", 1)])

    async def create_chat(self, uid_1: str, uid_2: str):
        new_chat = Chat(participants=[uid_1, uid_2], messages=[])
        result = await self.chat_collection.insert_one(new_chat.dict())
        return await self.chat_collection.find_one({"_id": result.inserted_id})

    async def create_message(self, msg: Message):
        result = await self.message_collection.insert_one(msg.dict())
        return await self.message_collection.find_one({"_id": result.inserted_id})

    async def update_chat(self, chat_id: str, message_id: str):
        return await self.chat_collection.update_one(
            {"_id": ObjectId(chat_id)}, {"$set": {"last_message": ObjectId(message_id), "last_updated": datetime.now()}}
        )

    async def get_chat_by_participants(self, uid_1: str, uid_2: str):
        return await self.chat_collection.find_one(
            {"participants": {"$all": [uid_1, uid_2]}}
        )

    async def get_my_chats(self, uid: str, limit: int, offset: int):
        return await (self.chat_collection.find(
            {"participants": {"$in": [uid]}, "last_message": {"$ne": None}})
                      .sort("last_update", -1)
                      .skip(offset)
                      .limit(limit)
                      .to_list(length=limit))

    async def get_chat_messages(self, chat_id: str,limit: int, offset: int)-> List[dict]:
        messages = await (self.message_collection.find({"chat_id": chat_id}, {"_id": 0, "chat_id": 0})
                          .sort("timestamp", -1)
                          .skip(offset)
                          .limit(limit)
                          .to_list(length=limit))
        return messages

    async def get_chat_by_id(self, chat_id: str):
        return await self.chat_collection.find_one({"_id": ObjectId(chat_id)})

    async def get_message_by_id(self, message_id: str):
        return await self.message_collection.find_one(
            {"_id": ObjectId(message_id)},
            {"_id": 0, "chat_id": 0},
        )


chat_repository = ChatRepository(db)
chat_repository.create_index()
