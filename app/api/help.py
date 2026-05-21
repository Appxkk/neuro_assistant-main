from fastapi import APIRouter
from pydantic import BaseModel

from app.services.help_service import get_help_answer


router = APIRouter(prefix="/api/help", tags=["help"])


class HelpChatRequest(BaseModel):
    question: str


@router.post("/chat")
def help_chat(request: HelpChatRequest):
    result = get_help_answer(request.question)

    return {
        "question": request.question,
        "answer": result["answer"],
        "source": result["source"],
        "fallback": result["fallback"],
    }