from pydantic import BaseModel


class ChatCreate(BaseModel):
    uid: str
