from pydantic import BaseModel
from typing import List

class Chat(BaseModel):
    chat_id: str
    user_1_id: str
    user_2_id: str
    messages: List[Message]
