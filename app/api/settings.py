from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.mode_service import get_llm_mode, set_llm_mode


router = APIRouter(prefix="/api/settings", tags=["settings"])


class LLMModeRequest(BaseModel):
    mode: str


@router.get("/llm-mode")
def get_current_llm_mode():
    return {
        "mode": get_llm_mode()
    }


@router.post("/llm-mode")
def update_llm_mode(data: LLMModeRequest):
    try:
        mode = set_llm_mode(data.mode)
        return {
            "mode": mode,
            "message": f"Режим NLP переключён на {mode}"
        }
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))