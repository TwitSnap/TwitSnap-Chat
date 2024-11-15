from pydantic import BaseModel


class CreateChatRequest(BaseModel):
    uid: str
