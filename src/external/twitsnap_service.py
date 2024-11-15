from utils.requester import requester
from config.settings import (
    USER_API_URI,
    USER_API_GET_USER_PATH,
    logger,
)


class TwitsnapService:
    def __init__(self, requester):
        self.requester = requester

    async def get_user(self, user_id: str):
        url = f"{USER_API_URI}{USER_API_GET_USER_PATH}{user_id}"
        headers = {"user_id": user_id}
        response = await self.requester.get(url, headers=headers)
        return response.json()


twitsnap_service = TwitsnapService(requester)
