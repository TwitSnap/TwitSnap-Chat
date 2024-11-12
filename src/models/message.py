from pydantic import BaseModel
from datetime import datetime

class Message(BaseModel):
    sender_id: str
    content: str
    timestamp: datetime
