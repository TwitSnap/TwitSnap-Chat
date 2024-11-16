from pydantic import BaseModel
class User(BaseModel):
    uid: str
    username: str
    photo: str