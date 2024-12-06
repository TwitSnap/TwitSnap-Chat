from pydantic import BaseModel


class Notification(BaseModel):
    type: str
    params: dict
    notifications: dict
