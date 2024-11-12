from pydantic import BaseModel

class User(BaseModel):
    uid: str
    name: str
    chats: list[str]
