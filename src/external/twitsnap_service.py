from utils.requester import requester
from config.settings import (
    USER_API_URI,
    USER_API_GET_USER_PATH,
    logger,
)

from exceptions.resource_not_found_exception import ResourceNotFoundException

from config.settings import NOTIFICATION_API_URI, NOTIFICATION_API_SEND_PATH
from dtos.notification import Notification

from config.settings import API_KEY


class TwitsnapService:
    def __init__(self, requester):
        self.requester = requester

    async def get_user(self, user_id: str):
        url = f"{USER_API_URI}{USER_API_GET_USER_PATH}{user_id}"
        headers = {"user_id": user_id,
                   "api_key": API_KEY}
        response = await self.requester.get(url, headers=headers)
        if response.status_code == 404:
            return None
        return response.json()

    async def send_new_message_notification(self, username: str, device_token: list[str]):
        url = NOTIFICATION_API_URI + NOTIFICATION_API_SEND_PATH
        header = {"api_key": API_KEY}
        req = Notification(
            type="push",
            params={"title": "Has recibido un mensaje directo",
                    "body": f"{username} te envio un mensaje directo"},
            notifications={"type": "push", "destinations": device_token},
        )
        logger.debug(
            f"[NotificationService] - Attempting to send new direct message to {username} with data: {req.model_dump()}"
        )

        res = await self.requester.post(url, json_body=req.model_dump(), headers=header)
        logger.debug(
            f"[NotificationService] - Attempt to send new direct message to {username} - response: {res.text}"
        )



twitsnap_service = TwitsnapService(requester)
