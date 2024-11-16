from dataclasses import field
from typing import Optional

from pydantic import BaseModel
from datetime import datetime

class MessageResponse(BaseModel):
    id : Optional[str] = None
    chat_id: Optional[str] = None
    sender_id: Optional[str] = None
    message: Optional[str] = None
    timestamp: Optional[datetime] = None