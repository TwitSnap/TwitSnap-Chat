from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId


class Message(BaseModel):
    chat_id: str
    sender_id: str
    content: str
    timestamp: datetime

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
