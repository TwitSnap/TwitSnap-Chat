from fastapi import APIRouter

from controller.chat_controller import chat_router

router = APIRouter(prefix="/api/v1")

router.include_router(chat_router)