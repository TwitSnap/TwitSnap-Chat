from pydantic import BaseModel
from typing import List, Optional
from dtos.message import MessageResponse

class ChatMessagesResponse(BaseModel):
    messages: List[MessageResponse]
    next_cursor: Optional[str] = None