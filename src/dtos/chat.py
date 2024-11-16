from pydantic import BaseModel
from dtos.user import User
from dtos.message import MessageResponse
from typing import List, Optional


class Chat(BaseModel):
    id: str
    participants: Optional[List[str]]= []
    user: Optional[User] = None
    last_message: Optional[MessageResponse] = None