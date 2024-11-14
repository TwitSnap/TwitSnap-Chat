import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from config.settings import logger
from service.chat_service import chat_service
from exceptions.bad_request_exception import BadRequestException
from dtos.create_chat import ChatCreate


chat_router = APIRouter()
@chat_router.websocket("/web_socket/{user_id}")
async def websocket(websocket: WebSocket, user_id: str):
    logger.debug(f" attempting to establish WebSocket connection for user {user_id}")
    await websocket.accept()
    logger.debug(f"WebSocket connection established for user {user_id}")
    chat_service.add_connection(user_id, websocket)

    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)
            receiver_id = data.get("receiver_id")
            message_content = data.get("message")
            logger.debug(
                f"Received message from user {user_id} to user {receiver_id}: {message_content}"
            )
            await chat_service.broadcast_message(user_id, data)

    except WebSocketDisconnect:
        logger.info(f"WebSocket connection closed for user {user_id}")
        chat_service.remove_connection(user_id)

@chat_router.post("/")
async def create_chat(req: Request, create_chat_request: ChatCreate):
    my_user_id = get_current_user(req)
    return await chat_service.create_chat(my_user_id, create_chat_request.uid)

@chat_router.get("/{chat_id}")
async def get_chat_by_id(chat_id: str):
    logger.debug(f"Getting messages for chat {chat_id}")
    return await chat_service.get_chat_by_id(chat_id)

@chat_router.get("/")
async def get_my_chats(req: Request):
    my_user_id = get_current_user(req)
    return await chat_service.get_my_chats(my_user_id)

def get_current_user(req: Request):
    user_id = req.headers.get("user_id")
    logger.debug(f"User id found in headers: {user_id}")
    if user_id is None:
        raise BadRequestException(detail="User id not found in headers")
    return user_id
