from fastapi import APIRouter, WebSocket, Request, Query
from config.settings import logger
from service.chat_service import chat_service
from exceptions.bad_request_exception import BadRequestException
from dtos.create_chat import CreateChatRequest
from exceptions.exception_handler import ExceptionHandler
from dtos.chat_messages_response import ChatMessagesResponse
from dtos.chat import Chat
from typing import List

chat_router = APIRouter()


@chat_router.websocket("/websocket")
async def websocket(websocket: WebSocket):
    try:
        user_id = websocket.headers.get("user_id")
        logger.debug(f"User id found in headers: {user_id}")
        logger.debug(
            f" attempting to establish WebSocket connection for user {user_id}"
        )
        await websocket.accept()
        logger.info(f"WebSocket connection established for user {user_id}")
        await chat_service.manage_connection(websocket, user_id)
    except Exception as e:
        return ExceptionHandler.handle_exception(e)


@chat_router.post("/", response_model=Chat, response_model_exclude_unset=True)
async def create_chat(req: Request, create_chat_request: CreateChatRequest):
    try:
        my_user_id = get_current_user(req)
        logger.debug(f"user_id found in headers: {my_user_id}")
        return await chat_service.create_chat(my_user_id, create_chat_request.uid)
    except Exception as e:
        return ExceptionHandler.handle_exception(e)


@chat_router.get("/{chat_id}/messages", response_model=ChatMessagesResponse, response_model_exclude_unset=True)
async def get_chat_by_id(
    chat_id: str, limit: int = Query(10, le=100), cursor: str = Query(None)
):
    try:
        return await chat_service.get_chat_by_id(chat_id, limit, cursor)
    except Exception as e:
        return ExceptionHandler.handle_exception(e)


@chat_router.get("/", response_model=List[Chat], response_model_exclude_unset=True)
async def get_my_chats(
    req: Request, limit: int = Query(10, le=100), offset: int = Query(0, ge=0)
):
    try:
        my_user_id = get_current_user(req)
        return await chat_service.get_my_chats(my_user_id, limit, offset)
    except Exception as e:
        return ExceptionHandler.handle_exception(e)


def get_current_user(req: Request):
    user_id = req.headers.get("user_id")
    logger.debug(f"User id found in headers: {user_id}")
    if user_id is None:
        raise BadRequestException(detail="User id not found in headers")
    return user_id
