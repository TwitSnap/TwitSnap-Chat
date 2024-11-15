from dataclasses import field
from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional
from typing import List
from bson import ObjectId


class Chat(BaseModel):
    participants: List[str]
    last_message: Optional[str] = None
    last_updated: Optional[datetime] = datetime.now()

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
