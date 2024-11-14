from pydantic import BaseModel, Field
from typing import Optional
from typing import List
from bson import ObjectId


class Chat(BaseModel):
    participants: List[str]
    last_message: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
