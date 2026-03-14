from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
import services.chatbot_service as chatbot_service

router = APIRouter(prefix="/api/chat", tags=["chatbot"])


@router.get("/ask", response_class=PlainTextResponse)
def ask_bot(message: str):
    return chatbot_service.get_bot_response(message)